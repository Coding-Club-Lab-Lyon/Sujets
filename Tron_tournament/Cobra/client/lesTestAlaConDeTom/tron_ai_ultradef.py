#!/usr/bin/env python3
import socket, struct, sys, time, select, math
from collections import deque

# ===== Protocol constants =====
MSG_HELLO   = 0x0001
MSG_WELCOME = 0x0002
MSG_INPUT   = 0x0003
MSG_STATE   = 0x0004
MSG_PING    = 0x0005
MSG_BYE     = 0x0006

HELLO_SIZE = 8 + 4 + 32
INPUT_SIZE = 8 + 1 + 4

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3

def pack_header(msg_type, length, ver=1, reserved=0):
    return struct.pack('<HHHH', msg_type, length, ver, reserved)

def pack_hello(name: str, want_player: int = 0) -> bytes:
    bname = name.encode('utf-8')[:32]
    if len(bname) < 32:
        bname += b'\x00' * (32 - len(bname))
    return pack_header(MSG_HELLO, HELLO_SIZE) + struct.pack('<I', want_player) + bname

def pack_input(turn: int, tick: int = 0) -> bytes:
    return pack_header(MSG_INPUT, INPUT_SIZE) + struct.pack('<bI', int(turn), int(tick))

def turn_dir(d, rel):
    if rel == -1: return (d + 3) % 4
    if rel == +1: return (d + 1) % 4
    return d

def step_wrap(x, y, d, W, H):
    if d == UP:    y = (y - 1 + H) % H
    elif d == DOWN:y = (y + 1) % H
    elif d == LEFT:x = (x - 1 + W) % W
    elif d == RIGHT:x = (x + 1) % W
    return x, y

def torus_dist(ax, ay, bx, by, W, H):
    dx = min((ax-bx) % W, (bx-ax) % W)
    dy = min((ay-by) % H, (by-ay) % H)
    return dx + dy

# -------------------- IO helpers --------------------
class Reader:
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buf = bytearray()

    def recv_into_buf(self):
        try:
            data = self.sock.recv(8192)
            if not data:
                return False
            self.buf.extend(data)
            return True
        except (BlockingIOError, InterruptedError):
            return True
        except OSError:
            return False

    def messages(self):
        out = []
        while True:
            if len(self.buf) < 8: break
            msg_type, length, ver, reserved = struct.unpack_from('<HHHH', self.buf, 0)
            if length < 8 or length > 10_000_000:
                raise RuntimeError("Invalid packet length")
            if len(self.buf) < length: break
            pkt = bytes(self.buf[:length])
            del self.buf[:length]
            out.append(pkt)
        return out

# -------------------- Model --------------------
class GameState:
    def __init__(self):
        self.tick = 0
        self.W = 0
        self.H = 0
        self.grid = []      # uint8 W*H: 0=vide, >0 id
        self.players = []   # dicts: {id,x,y,dir,alive}
        self.my_id = 0

    def cell(self, x, y):
        return self.grid[y*self.W + x]

    def is_occupied(self, x, y):
        return self.cell(x, y) != 0

    def my_state(self):
        for p in self.players:
            if p['id'] == self.my_id:
                return p
        return None

# -------------------- Defensive tools --------------------
INF = 10**9

def build_static_occ(state: GameState):
    """Occupe toutes les cases non libres (trails + têtes actuelles, côté client)."""
    W, H = state.W, state.H
    occ = [[False]*W for _ in range(H)]
    g = state.grid
    for y in range(H):
        base = y*W
        for x in range(W):
            if g[base+x] != 0:
                occ[y][x] = True
    return occ

def enemy_heads(state: GameState):
    return [(p['x'], p['y']) for p in state.players if p['alive'] and p['id'] != state.my_id]

def my_head(state: GameState):
    p = state.my_state()
    return (p['x'], p['y'], p['dir']) if p else (0,0,RIGHT)

def enemy_time_map(state: GameState, maxd: int):
    """
    Multi-source BFS torique: earliest arrival time (en pas) pour n'importe quel ennemi.
    Conservative: on considère la grille statique comme murs.
    """
    W, H = state.W, state.H
    occ = build_static_occ(state)
    heads = enemy_heads(state)
    dist = [[INF]*W for _ in range(H)]
    q = deque()

    # Les têtes actuelles sont des sources à t=0 (même si la case est marquée occupée)
    for (sx, sy) in heads:
        dist[sy][sx] = 0
        q.append((sx, sy))

    while q:
        x, y = q.popleft()
        t = dist[y][x]
        if t >= maxd:  # inutile d'aller plus loin pour notre horizon
            continue
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx = (x + dx) % W
            ny = (y + dy) % H
            # Les ennemis ne passent pas à travers les murs/trails statiques
            if occ[ny][nx]: 
                continue
            if dist[ny][nx] > t + 1:
                dist[ny][nx] = t + 1
                q.append((nx, ny))
    return dist

def flood_fill_safe_area(W, H, blocked_fn, start, cap=6000):
    """Zone accessible en restant dans des cases non bloquées (pour évaluer ‘air time’)."""
    sx, sy = start
    if blocked_fn(sx, sy):
        return 0
    seen = set([(sx, sy)])
    q = deque([(sx, sy)])
    size = 0
    while q:
        x, y = q.popleft()
        size += 1
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx = (x + dx) % W
            ny = (y + dy) % H
            if (nx, ny) in seen: 
                continue
            if blocked_fn(nx, ny):
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
        if size >= cap:  # coupe court sur grandes maps ouvertes
            break
    return size

# -------------------- Planner (Ultra-Def) --------------------
class PlannerUltraDef:
    def __init__(self, depth=12, beam=96, safety_margin=0):
        self.depth = depth
        self.beam  = beam
        # poids heuristiques (défense first)
        self.W_AREA     = 1.0     # taille de zone sûre accessible
        self.W_ENEMYDIST= 0.25    # s'éloigner des têtes
        self.W_STRAIGHT = 0.06    # léger biais en ligne droite
        self.safety_margin = safety_margin  # ex: 0 => on exige our_t < enemy_t

    def choose(self, state: GameState):
        me = state.my_state()
        if not me: 
            return 0
        W, H = state.W, state.H

        # Occupation statique (trails + heads déjà projetées par le serveur)
        static_occ = build_static_occ(state)

        # Temps d'arrivée ennemis (conservateur)
        etime = enemy_time_map(state, self.depth + 2)

        # Pré-calcul: têtes ennemies actuelles
        eheads = enemy_heads(state)

        # Utilitaires inline
        def base_blocked(x, y):
            return static_occ[y][x]

        def cell_safe_at_step(x, y, step_k):
            # Mur/trail ?
            if base_blocked(x, y):
                return False
            # Safety stricte: nous devons arriver AVANT l'ennemi (strict)
            # etime[y][x] == 0 signifie une tête ennemie y est déjà, donc interdit si step_k >= 0
            return step_k + self.safety_margin < etime[y][x]

        # Node = (score, bias_straight, path, x, y, dir, my_trail_frozen_set)
        start = (0.0, 0, [], me['x'], me['y'], me['dir'], frozenset())
        frontier = [start]

        best_first = 0
        best_score = -1e18

        for k in range(1, self.depth + 1):
            newF = []
            for score, sbias, path, x, y, d, myset in frontier:
                for action in (-1, 0, +1):
                    nd = turn_dir(d, action)
                    nx, ny = step_wrap(x, y, nd, W, H)

                    # On ne peut pas repasser par notre futur trail
                    if (nx, ny) in myset:
                        continue
                    # Case sûre par rapport aux ennemis à l'instant k ?
                    if not cell_safe_at_step(nx, ny, k):
                        continue

                    # On "solidifie" la case que l'on quitte (notre trail futur)
                    new_my = set(myset)
                    new_my.add((x, y))
                    new_my = frozenset(new_my)

                    # Zone sûre accessible depuis (nx,ny) en interdisant :
                    # - murs/trails
                    # - notre propre set
                    # - cases où l'ennemi peut arriver à t' <= k' (strict)
                    def blocked(xx, yy):
                        if static_occ[yy][xx]: return True
                        if (xx, yy) in new_my: return True
                        # on refait la contrainte stricte avec la profondeur locale
                        # (ici on reste conservateur: si etime==k' ou moins -> bloqué)
                        return etime[yy][xx] <= k

                    area = flood_fill_safe_area(W, H, blocked, (nx, ny), cap=7000)

                    # Distance minimale à une tête ennemie (plus c'est grand, mieux c'est)
                    mind = INF
                    for (ex, ey) in eheads:
                        mind = min(mind, torus_dist(nx, ny, ex, ey, W, H))
                    if mind == INF: mind = 0

                    bias = 1 if action == 0 else 0

                    new_score = (
                        area * self.W_AREA
                        + mind * self.W_ENEMYDIST
                        + bias * self.W_STRAIGHT
                    )

                    new_path = path + [action]
                    newF.append((new_score, bias, new_path, nx, ny, nd, new_my))

            if not newF:
                break

            newF.sort(key=lambda t: (t[0], t[1]), reverse=True)
            frontier = newF[:self.beam]

            s0, b0, p0, *_ = frontier[0]
            if s0 > best_score:
                best_score = s0
                best_first = p0[0] if p0 else 0

        return best_first

# -------------------- Bot --------------------
class TronBot:
    def __init__(self, host='127.0.0.1', port=5555, name='UltraDef', depth=12, beam=96, safety_margin=0):
        self.host = host
        self.port = int(port)
        self.name = name
        self.state = GameState()
        self.reader = None
        self.sock = None
        self.planner = PlannerUltraDef(depth=depth, beam=beam, safety_margin=safety_margin)
        self.last_sent_turn = 0

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.settimeout(5.0)
        s.connect((self.host, self.port))
        s.setblocking(False)
        self.sock = s
        self.reader = Reader(s)
        s.sendall(pack_hello(self.name, want_player=0))
        print(f"[+] Connected to {self.host}:{self.port} as {self.name}")

    def run(self):
        try:
            while True:
                try:
                    r, _, _ = select.select([self.sock], [], [], 0.05)
                except (ValueError, OSError):
                    print("[!] Socket invalid/closed")
                    sys.exit(0)

                if r:
                    if not self.reader.recv_into_buf():
                        print("[!] Disconnected (recv)")
                        sys.exit(0)
                    for pkt in self.reader.messages():
                        self.handle_packet(pkt)

                time.sleep(0.003)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print("[!] Fatal:", e)
        finally:
            try:
                if self.sock:
                    self.sock.close()
            finally:
                sys.exit(0)

    def handle_packet(self, pkt: bytes):
        msg_type, length, ver, reserved = struct.unpack_from('<HHHH', pkt, 0)
        body = pkt[8:]

        if msg_type == MSG_WELCOME:
            if len(body) < (4 + 2 + 2 + 2 + 4 + 4 + 1 + 2 + 2):
                return
            off = 0
            assigned_id, = struct.unpack_from('<I', body, off); off += 4
            width, height, tickrate = struct.unpack_from('<HHH', body, off); off += 6
            start_speed, end_speed = struct.unpack_from('<ff', body, off); off += 8
            auto_kill, = struct.unpack_from('<B', body, off); off += 1
            length_tick, maps_every = struct.unpack_from('<HH', body, off); off += 4
            self.state.my_id = assigned_id
            self.state.W = width
            self.state.H = height
            print(f"[WELCOME] id={assigned_id} map={width}x{height} tickrate={tickrate} speed=[{start_speed},{end_speed}]")

        elif msg_type == MSG_STATE:
            if len(body) < 4 + 2 + 2 + 1:
                return
            off = 0
            tick, = struct.unpack_from('<I', body, off); off += 4
            W, H = struct.unpack_from('<HH', body, off); off += 4
            P, = struct.unpack_from('<B', body, off); off += 1
            need = off + (W*H) + (P * 7)
            if len(body) < need:
                return

            grid = list(body[off:off + W*H]); off += W*H
            players = []
            for _ in range(P):
                pid, = struct.unpack_from('<B', body, off); off += 1
                x, y = struct.unpack_from('<HH', body, off); off += 4
                d, alive = struct.unpack_from('<BB', body, off); off += 2
                players.append({'id': pid, 'x': x, 'y': y, 'dir': d, 'alive': alive != 0})

            self.state.tick = tick
            self.state.W, self.state.H = W, H
            self.state.grid = grid
            self.state.players = players

            self.decide_and_send()

        elif msg_type == MSG_BYE:
            reason = body[0] if len(body) >= 1 else 0
            reasons = {0:"server closing",1:"dead",2:"winner",3:"kick"}
            print(f"[BYE] reason={reasons.get(reason, reason)}")
            try:
                self.sock.close()
            finally:
                sys.exit(0)

        # MSG_PING ignoré (non utilisé V1)

    def decide_and_send(self):
        me = self.state.my_state()
        if not me:
            return
        action = self.planner.choose(self.state)  # -1/0/+1
        # Throttle: envoyer uniquement si utile
        if action != 0 or self.last_sent_turn != 0:
            try:
                self.sock.sendall(pack_input(action, tick=self.state.tick))
                self.last_sent_turn = action
            except BrokenPipeError:
                print("[send] Broken pipe")
                sys.exit(0)
            except OSError as e:
                print("[send] OSError:", e)
                sys.exit(0)

# -------------------- main --------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: tron_ai_ultradef.py [host] [port] [name] [depth] [beam] [safety_margin]")
        host, port, name = '127.0.0.1', 5555, 'UltraDef'
        depth, beam, safety = 12, 96, 0
    else:
        host  = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
        port  = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
        name  = sys.argv[3] if len(sys.argv) > 3 else 'UltraDef'
        depth = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        beam  = int(sys.argv[5]) if len(sys.argv) > 5 else 96
        safety= int(sys.argv[6]) if len(sys.argv) > 6 else 0

    bot = TronBot(host, port, name, depth=depth, beam=beam, safety_margin=safety)
    bot.connect()
    bot.run()

if __name__ == '__main__':
    main()
