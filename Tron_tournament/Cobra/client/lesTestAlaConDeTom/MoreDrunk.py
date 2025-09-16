#!/usr/bin/env python3
# smart_tron_bot.py — IA Tron "safe-aggressive" + client TCP protocole C++/Qt
# Python 3.8+ — stdlib uniquement

from __future__ import annotations
import socket, struct, argparse, time, random, sys, zlib
from dataclasses import dataclass
from collections import deque
from typing import List, Tuple

# =========================
# Protocole binaire (little-endian)
# =========================
HDR_FMT = "<HHHH"   # type, len, ver, reserved
HDR_SIZE = struct.calcsize(HDR_FMT)

MSG_HELLO   = 0x0001  # C->S
MSG_WELCOME = 0x0002  # S->C
MSG_INPUT   = 0x0003  # C->S
MSG_STATE   = 0x0004  # S->C
MSG_PING    = 0x0005
MSG_BYE     = 0x0006  # S->C

HELLO_FMT   = "<HHHH I 32s"          # header + want_player + name[32]
WELCOME_FMT = "<HHHH I H H H f f B H H"
INPUT_FMT   = "<HHHH b I"
STATE_HDR_FMT = "<HHHH I H H B"
PLAYERSTATE_FMT = "<B H H B B"
PLAYERSTATE_SIZE = struct.calcsize(PLAYERSTATE_FMT)
BYE_FMT = "<HHHH B"

# Directions (mappage C++)
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
DIRS = [(0,-1),(1,0),(0,1),(-1,0)]
DIR_NAMES = ["UP","RIGHT","DOWN","LEFT"]

INF = 10**9

# =========================
# Modèle IA
# =========================
@dataclass(frozen=True)
class Player:
    id: int
    head: Tuple[int,int]
    dir: int
    alive: bool = True

@dataclass
class GameState:
    W: int
    H: int
    # 0 = libre, >0 = occupé
    grid: List[List[int]]
    me: Player
    enemies: List[Player]

    def wrap(self, p:Tuple[int,int])->Tuple[int,int]:
        return (p[0] % self.W, p[1] % self.H)

    def is_free(self, p:Tuple[int,int])->bool:
        x,y = self.wrap(p)
        return self.grid[y][x] == 0

    def clone(self)->'GameState':
        g = [row[:] for row in self.grid]
        return GameState(self.W, self.H, g,
                         Player(self.me.id,self.me.head,self.me.dir,self.me.alive),
                         [Player(e.id,e.head,e.dir,e.alive) for e in self.enemies])

def add(a, b): return (a[0]+b[0], a[1]+b[1])

def multi_source_bfs(state:GameState, sources):
    W,H = state.W, state.H
    dist = [[INF]*W for _ in range(H)]
    q = deque()
    for s in sources:
        x,y = state.wrap(s)
        if state.grid[y][x] != 0: continue
        dist[y][x] = 0; q.append((x,y))
    while q:
        x,y = q.popleft()
        for dx,dy in DIRS:
            nx = (x+dx) % W; ny = (y+dy) % H
            if state.grid[ny][nx]==0 and dist[ny][nx]==INF:
                dist[ny][nx] = dist[y][x]+1
                q.append((nx,ny))
    return dist

def flood_size_from(state:GameState, start:Tuple[int,int])->int:
    x0,y0 = state.wrap(start)
    if state.grid[y0][x0] != 0: return 0
    W,H = state.W,state.H
    seen = [[False]*W for _ in range(H)]
    q = deque([(x0,y0)]); seen[y0][x0]=True; c=1
    while q:
        x,y = q.popleft()
        for dx,dy in DIRS:
            nx=(x+dx)%W; ny=(y+dy)%H
            if not seen[ny][nx] and state.grid[ny][nx]==0:
                seen[ny][nx]=True; q.append((nx,ny)); c+=1
    return c

def liberties(state:GameState, p:Tuple[int,int])->int:
    x,y = state.wrap(p)
    c=0
    for dx,dy in DIRS:
        nx=(x+dx)%state.W; ny=(y+dy)%state.H
        if state.grid[ny][nx]==0: c+=1
    return c

def apply_moves(state:GameState, my_dir:int, enemy_dirs:List[int]) -> GameState:
    ns = state.clone()
    # laisser trail
    if ns.me.alive:
        x,y = ns.me.head; x%=ns.W; y%=ns.H; ns.grid[y][x]=1
    for e in ns.enemies:
        if e.alive:
            x,y=e.head; x%=ns.W; y%=ns.H; ns.grid[y][x]=1
    # nouvelles têtes (wrap)
    my_next = ns.wrap(add(ns.me.head, DIRS[my_dir])) if ns.me.alive else ns.me.head
    enemy_next = []
    for e,d in zip(ns.enemies, enemy_dirs):
        enemy_next.append(ns.wrap(add(e.head, DIRS[d])) if e.alive else e.head)
    # collisions murs/traînées
    me_alive = ns.me.alive and ns.grid[my_next[1]][my_next[0]]==0
    enemies_alive=[]
    for p,e in zip(enemy_next, ns.enemies):
        enemies_alive.append(e.alive and ns.grid[p[1]][p[0]]==0)
    # tête-à-tête même case
    if me_alive:
        for i,(p,ea) in enumerate(zip(enemy_next,enemies_alive)):
            if ea and p==my_next:
                me_alive=False; enemies_alive[i]=False
    # échange de têtes
    if me_alive:
        for i,(e,ea,pnew) in enumerate(zip(ns.enemies,enemies_alive,enemy_next)):
            if ns.me.alive and e.alive and me_alive and ea:
                if pnew==ns.me.head and my_next==e.head:
                    me_alive=False; enemies_alive[i]=False
    ns.me = Player(ns.me.id, my_next if me_alive else ns.me.head, my_dir, me_alive)
    new_enemies=[]
    for (e,ea,pnew,d) in zip(ns.enemies,enemies_alive,enemy_next,enemy_dirs):
        new_enemies.append(Player(e.id, pnew if ea else e.head, d, ea))
    ns.enemies=new_enemies
    return ns

def legal_dirs(state:GameState, head:Tuple[int,int], forbid_back:int|None=None)->List[int]:
    dirs=[]
    for d,(dx,dy) in enumerate(DIRS):
        if forbid_back is not None and (d ^ 2) == forbid_back:
            continue
        nx,ny = state.wrap(add(head,(dx,dy)))
        if state.grid[ny][nx]==0:
            dirs.append(d)
    return dirs

def voronoi_score(state:GameState, my_head:Tuple[int,int]):
    my_dist = multi_source_bfs(state,[my_head])
    enemy_sources = [e.head for e in state.enemies if e.alive]
    enemy_dist = multi_source_bfs(state, enemy_sources) if enemy_sources else [[INF]*state.W for _ in range(state.H)]
    my_cells=0; enemy_cells=0; ties=0
    for y in range(state.H):
        grow = state.grid[y]
        for x in range(state.W):
            if grow[x]!=0: continue
            dm,de = my_dist[y][x], enemy_dist[y][x]
            if dm<de: my_cells+=1
            elif de<dm: enemy_cells+=1
            else: ties+=1
    return (my_cells - enemy_cells + 0.5*ties, my_cells, enemy_cells)

def evaluate(state:GameState)->float:
    if not state.me.alive: return -1e9
    if all(not e.alive for e in state.enemies): return 1e8

    my_lib = liberties(state, state.me.head)
    my_space = flood_size_from(state, state.me.head)
    v_score,_,_ = voronoi_score(state, state.me.head)

    # distance torique manhattan (approx)
    enemy_dist = INF
    for e in state.enemies:
        if e.alive:
            dx = abs(e.head[0]-state.me.head[0])
            dy = abs(e.head[1]-state.me.head[1])
            dx = min(dx, state.W - dx)
            dy = min(dy, state.H - dy)
            enemy_dist = min(enemy_dist, dx+dy)

    base = 60.0*my_lib + 2.2*(my_space**0.5) + 1.0*v_score + 8.0*(0 if enemy_dist==INF else enemy_dist)
    return base

def enemy_policy(state:GameState)->List[int]:
    out=[]
    for e in state.enemies:
        if not e.alive:
            out.append(e.dir); continue
        cands = legal_dirs(state, e.head, forbid_back=e.dir)
        if not cands: out.append(e.dir); continue
        best=None; bests=-1e18
        for d in cands:
            ns = state.clone()
            x,y = ns.wrap(e.head)
            ns.grid[y][x]=1
            nh = ns.wrap(add(e.head, DIRS[d]))
            if ns.grid[nh[1]][nh[0]]!=0: continue
            s = 50*liberties(ns, nh) + flood_size_from(ns, nh)
            if s>bests: bests=s; best=d
        out.append(best if best is not None else random.choice(cands))
    return out

@dataclass
class SearchParams:
    max_depth:int=6
    time_budget_ms:int=40
    beam_k:int=3

def choose_move(state:GameState, params:SearchParams=SearchParams())->int:
    t_end = time.perf_counter() + params.time_budget_ms/1000.0
    my_moves = legal_dirs(state, state.me.head, forbid_back=state.me.dir)
    if not my_moves:
        # choisir la "moins pire"
        all_dirs = [d for d in range(4) if (d ^ 2) != state.me.dir]
        return max(all_dirs, key=lambda d: liberties(state, state.wrap(add(state.me.head, DIRS[d]))))

    # éviter entrée immédiate dans une tête ennemie
    enemy_heads = {e.head for e in state.enemies if e.alive}
    safe=[d for d in my_moves if state.wrap(add(state.me.head, DIRS[d])) not in enemy_heads]
    if safe: my_moves = safe

    # Bonus tout-droit si c'est safe
    forward = state.me.dir
    fpos = state.wrap(add(state.me.head, DIRS[forward]))
    forward_safe = state.grid[fpos[1]][fpos[0]] == 0
    my_moves.sort(key=lambda d: 0 if (d==forward and forward_safe) else 1)

    # pré-filtre (beam) via éval one-step
    scored=[]
    epol = enemy_policy(state)
    for d in my_moves:
        ns = apply_moves(state, d, epol)
        scored.append((evaluate(ns), d))
    scored.sort(reverse=True)
    beam=[d for _,d in scored[:max(1,min(params.beam_k,len(scored)))]]

    best_d=beam[0]; best_v=-1e18

    def search(s:GameState, depth:int, alpha:float, beta:float)->float:
        if time.perf_counter()>t_end or depth==0 or not s.me.alive:
            return evaluate(s)
        moves = legal_dirs(s, s.me.head, forbid_back=s.me.dir)
        if not moves: return evaluate(s)
        # tri local
        mv = []
        for d in moves:
            nh = s.wrap(add(s.me.head, DIRS[d]))
            mv.append((liberties(s, nh), d))
        mv.sort(reverse=True)
        moves=[d for _,d in mv[:3]]
        val=-1e18
        e_dirs = enemy_policy(s)
        for d in moves:
            ns = apply_moves(s, d, e_dirs)
            v = -search(ns, depth-1, -beta, -alpha)
            if v>val: val=v
            if val>alpha: alpha=val
            if alpha>=beta: break
        return val

    for d in beam:
        ns = apply_moves(state, d, epol)
        v = search(ns, params.max_depth-1, -1e18, 1e18)
        if v>best_v: best_v=v; best_d=d
    return best_d

# =========================
# Anti-spin / stabilisation de mouvement
# =========================
class MoveSmoother:
    def __init__(self, min_turn_interval=5, spin_window=6):
        self.prev_dir = None
        self.last_turn_tick = -999999
        self.min_turn_interval = min_turn_interval
        self.spin_hist = deque(maxlen=spin_window)  # -1 gauche / +1 droite / 0 tout-droit
        self.last_side = 0  # -1 gauche, +1 droite

    def record(self, turn:int, tick:int):
        self.spin_hist.append(turn)
        if turn != 0:
            self.last_turn_tick = tick
            self.last_side = -1 if turn < 0 else +1

    def spinning(self)->bool:
        if len(self.spin_hist) < self.spin_hist.maxlen:
            return False
        seq = [x for x in self.spin_hist if x != 0]
        if len(seq) < 4:
            return False
        alt = all(seq[i] == -seq[i-1] for i in range(1, len(seq)))
        return alt and len(seq) >= 4

    def can_turn(self, tick:int)->bool:
        return (tick - self.last_turn_tick) >= self.min_turn_interval

def dir_to_turn(curr:int, target:int, state:GameState, smoother:MoveSmoother, tick:int)->int:
    # Convertit direction absolue -> -1/0/+1, en évitant 180° et l’oscillation
    if curr == target:
        return 0

    diff = (target - curr) & 3
    if diff == 2:
        # 180° interdit -> choisir côté le plus “ouvert”, avec mémoire
        left = (curr - 1) & 3
        right = (curr + 1) & 3
        lh = state.wrap(add(state.me.head, DIRS[left]))
        rh = state.wrap(add(state.me.head, DIRS[right]))
        llib = liberties(state, lh)
        rlib = liberties(state, rh)

        if llib == rlib and smoother.last_side != 0:
            return -1 if smoother.last_side < 0 else +1
        return -1 if llib >= rlib else +1

    # Ici, diff == 1 (droite) ou 3 (gauche)
    # Cooldown: si on a tourné récemment, et que tout-droit est sûr, reste tout-droit
    forward = curr
    fh = state.wrap(add(state.me.head, DIRS[forward]))
    forward_safe = state.grid[fh[1]][fh[0]] == 0

    if not smoother.can_turn(tick) and forward_safe:
        return 0

    # Si oscillation et que tout-droit est possible: forcer tout-droit
    if smoother.spinning() and forward_safe:
        return 0

    # Sinon, appliquer la cible (gauche/droite)
    return +1 if diff == 1 else -1

# =========================
# Client TCP
# =========================
class TronClient:
    def __init__(self, host:str, port:int, name:str):
        self.host=host; self.port=port; self.name=name.encode("utf-8")[:32].ljust(32,b"\0")
        self.sock=None
        self.buf=bytearray()
        self.assigned_id=None
        self.W=self.H=0
        self.tick=0
        self.smoother = MoveSmoother(min_turn_interval=5, spin_window=6)

        # Anti “toupie” : recalcul seulement si map/tête changent
        self.last_tick_handled = -1
        self.last_grid_sig = None
        self.last_head = None
        self.turn_sent_tick = -1  # un seul INPUT par tick

    def connect(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host,self.port))
        self.sock=s
        self._send_hello()

    def _send_hello(self):
        h = struct.pack(HDR_FMT, MSG_HELLO, struct.calcsize(HELLO_FMT), 1, 0)
        body = struct.pack("<I32s", 0, self.name)
        self.sock.sendall(h+body)

    def _send_input(self, turn:int, tick:int):
        # Ne jamais envoyer 2 inputs pour le même tick
        if self.turn_sent_tick == tick:
            return
        h = struct.pack(HDR_FMT, MSG_INPUT, struct.calcsize(INPUT_FMT), 1, 0)
        body = struct.pack("<bI", int(turn), int(tick))
        self.sock.sendall(h+body)
        self.turn_sent_tick = tick

    def run(self):
        self.sock.settimeout(0.0)  # non-blocking
        while True:
            # lire données dispo
            try:
                chunk = self.sock.recv(65536)
                if not chunk:
                    print("Disconnected"); return
                self.buf.extend(chunk)
            except BlockingIOError:
                pass

            # parser messages complets
            while True:
                if len(self.buf) < HDR_SIZE: break
                m_type, m_len, m_ver, m_res = struct.unpack_from(HDR_FMT, self.buf, 0)
                if len(self.buf) < m_len: break
                pkt = self.buf[:m_len]
                del self.buf[:m_len]
                if m_type==MSG_WELCOME:
                    self._on_welcome(pkt)
                elif m_type==MSG_STATE:
                    self._on_state(pkt)
                elif m_type==MSG_BYE:
                    reason = struct.unpack_from(BYE_FMT, pkt, 0)[4]
                    print(f"BYE (reason={reason})"); return
                # autres messages ignorés

            time.sleep(0.001)

    def _on_welcome(self, pkt:bytes):
        (_t,_l,_v,_r, assigned_id, W,H,tickrate, start_speed, end_speed, auto_kill, length_tick, maps_every) = \
            struct.unpack_from(WELCOME_FMT, pkt, 0)
        self.assigned_id = assigned_id
        self.W, self.H = W, H
        print(f"[WELCOME] id={assigned_id} map={W}x{H} tickrate={tickrate}")

    def _on_state(self, pkt:bytes):
        (m_type,m_len,m_ver,m_res, tick, W,H,P) = struct.unpack_from(STATE_HDR_FMT, pkt, 0)
        off = struct.calcsize(STATE_HDR_FMT)
        grid_bytes = pkt[off:off+W*H]
        off += W*H
        players=[]
        for _ in range(P):
            (pid, x, y, d, alive) = struct.unpack_from(PLAYERSTATE_FMT, pkt, off)
            off += PLAYERSTATE_SIZE
            players.append((pid, x, y, d, alive))

        # grille -> 0/1
        grid = [[0]*W for _ in range(H)]
        it = iter(grid_bytes)
        for y in range(H):
            for x in range(W):
                grid[y][x] = 1 if next(it)!=0 else 0

        me=None; enemies=[]
        for pid,x,y,d,alive in players:
            if alive==0: continue
            if pid == self.assigned_id:
                me = Player(pid, (x,y), d, True)
            else:
                enemies.append(Player(pid, (x,y), d, True))

        # Si pas encore spawné, ne rien faire
        if me is None:
            return

        # === Détection de changement réel ===
        grid_sig = zlib.adler32(grid_bytes)  # rapide et suffisant
        head = me.head

        # 1) Skip si tick identique ET grille identique ET tête identique
        # => pas de recalcul, pas d'input
        if (tick == self.last_tick_handled) and (grid_sig == self.last_grid_sig) and (head == self.last_head):
            return

        # 2) On recalcule et n'envoie qu'une fois par tick (debounce)
        s = GameState(W,H,grid, me, enemies)
        target_dir = choose_move(s)
        turn = dir_to_turn(me.dir, target_dir, s, self.smoother, tick)

        self._send_input(turn, tick)
        self.smoother.record(turn, tick)

        # Mémoriser l'état traité
        self.last_tick_handled = tick
        self.last_grid_sig = grid_sig
        self.last_head = head

# =========================
# Entrée programme
# =========================
def main():
    ap = argparse.ArgumentParser(description="Smart Tron Bot (client auto)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5555)
    ap.add_argument("--name", default="DrunkMeMore")
    args = ap.parse_args()

    bot = TronClient(args.host, args.port, args.name)
    try:
        bot.connect()
        bot.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        time.sleep(0.1)

if __name__ == "__main__":
    main()
