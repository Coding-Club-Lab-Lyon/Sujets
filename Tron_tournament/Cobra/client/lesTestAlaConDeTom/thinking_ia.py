#!/usr/bin/env python3
import socket, struct, sys, time, select, random, math, os
from collections import deque

# ===== Protocol constants (must match server ./src/Protocol.h) =====
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

def turn_dir(dir_code: int, rel_turn: int) -> int:
    if rel_turn == -1:   return (dir_code + 3) % 4
    if rel_turn == +1:   return (dir_code + 1) % 4
    return dir_code

def step_wrap(x, y, d, W, H):
    if d == UP:     y = (y - 1 + H) % H
    elif d == DOWN: y = (y + 1) % H
    elif d == LEFT: x = (x - 1 + W) % W
    elif d == RIGHT:x = (x + 1) % W
    return x, y

def torus_dist(ax, ay, bx, by, W, H):
    dx = min((ax-bx) % W, (bx-ax) % W)
    dy = min((ay-by) % H, (by-ay) % H)
    return dx + dy  # manhattan torique rapide

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
            if len(self.buf) < 8:
                break
            msg_type, length, ver, reserved = struct.unpack_from('<HHHH', self.buf, 0)
            if length < 8 or length > 10_000_000:
                raise RuntimeError("Invalid packet length")
            if len(self.buf) < length:
                break
            pkt = bytes(self.buf[:length])
            del self.buf[:length]
            out.append(pkt)
        return out

class GameState:
    def __init__(self):
        self.tick = 0
        self.W = 0
        self.H = 0
        self.grid = []  # uint8 W*H
        self.players = []  # dicts: {id,x,y,dir,alive}
        self.my_id = 0

    def cell(self, x, y):
        return self.grid[y*self.W + x]

    def is_occupied(self, x, y):
        return self.cell(x,y) != 0

    def my_state(self):
        for p in self.players:
            if p['id'] == self.my_id:
                return p
        return None

class OpponentPredictor:
    @staticmethod
    def predict_heads(state: GameState, D: int):
        W, H = state.W, state.H
        occ = [[state.grid[y*W+x] != 0 for x in range(W)] for y in range(H)]
        for p in state.players:
            if p['alive']:
                occ[p['y']][p['x']] = True

        preds = [set() for _ in range(D+1)]
        enemies = []
        for p in state.players:
            if not p['alive'] or p['id'] == state.my_id:
                continue
            enemies.append({'x': p['x'], 'y': p['y'], 'dir': p['dir'], 'alive': True})

        for step in range(1, D+1):
            for e in enemies:
                if not e['alive']:
                    continue
                for rel in (0, -1, +1):
                    nd = turn_dir(e['dir'], rel)
                    nx, ny = step_wrap(e['x'], e['y'], nd, W, H)
                    if not occ[ny][nx]:
                        e['x'], e['y'], e['dir'] = nx, ny, nd
                        preds[step].add((nx, ny))
                        occ[ny][nx] = True
                        break
                else:
                    e['alive'] = False
        # also return current living enemy heads
        now_heads = [(p['x'], p['y']) for p in state.players if p['alive'] and p['id'] != state.my_id]
        return preds, now_heads

def flood_fill_area(W, H, is_blocked, start, cap=4000):
    sx, sy = start
    if is_blocked(sx, sy):
        return 0
    seen = set([(sx, sy)])
    q = deque([(sx, sy)])
    cnt = 0
    while q:
        x, y = q.popleft()
        cnt += 1
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx = (x + dx) % W
            ny = (y + dy) % H
            if (nx, ny) in seen or is_blocked(nx, ny):
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
        if cnt > cap:
            break
    return cnt

class Planner:
    def __init__(self, depth=10, beam=80):
        self.depth = depth
        self.beam = beam
        # Heuristic weights (tweak here)
        self.W_AREA = 1.0           # espace propre (défense)
        self.W_STRAIGHT = 0.10      # petit biais ligne droite
        self.W_PRESSURE = 0.35      # mettre la pression (attaque douce)
        self.W_KILLSHOT = 6.0       # gros bonus quand on étouffe un ennemi proche
        self.PRESSURE_R = 6         # portée de pression

    def choose(self, state: GameState):
        me = state.my_state()
        if not me:
            return 0

        W, H = state.W, state.H

        # Static occupancy
        static_occ = [[state.grid[y*W+x] != 0 for x in range(W)] for y in range(H)]
        for p in state.players:
            if p['alive']:
                static_occ[p['y']][p['x']] = True

        preds, enemy_heads_now = OpponentPredictor.predict_heads(state, self.depth)

        def base_blocked(x, y):
            return static_occ[y][x]

        # Precompute enemy degree (free exits) around a cell quickly
        def free_neighbors(x, y, myset):
            cnt = 0
            for dxy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx = (x + dxy[0]) % W
                ny = (y + dxy[1]) % H
                if static_occ[ny][nx]: continue
                if (nx, ny) in myset: continue
                cnt += 1
            return cnt

        start = (0.0, 0, [], me['x'], me['y'], me['dir'], frozenset())
        frontier = [start]

        best_first_move = 0
        best_score_seen = -1e18

        for k in range(1, self.depth + 1):
            new_frontier = []
            for score, straight_bias, path, x, y, d, myset in frontier:
                for action in (-1, 0, +1):
                    nd = turn_dir(d, action)
                    nx, ny = step_wrap(x, y, nd, W, H)

                    # collisions (mur/trail) ou têtes ennemies prédites à k
                    if (nx, ny) in myset or base_blocked(nx, ny) or ((k <= self.depth) and ((nx, ny) in preds[k])):
                        continue

                    # prochain trail : on marque la case qu'on quitte
                    new_myset = set(myset)
                    new_myset.add((x, y))
                    new_myset = frozenset(new_myset)

                    # --- DEFENSE : espace atteignable depuis la tête candidate
                    def is_blocked(xx, yy):
                        if static_occ[yy][xx]: return True
                        if (xx, yy) in new_myset: return True
                        # prudence: bloquer les têtes ennemies proches dans 2 ticks
                        for t in range(k, min(self.depth, k+2)+1):
                            if (xx, yy) in preds[t]:
                                return True
                        return False

                    area = flood_fill_area(W, H, is_blocked, (nx, ny))

                    # --- OFFENSE 1 : pression — se rapprocher raisonnablement
                    pressure = 0.0
                    for (ex, ey) in enemy_heads_now:
                        dist = torus_dist(nx, ny, ex, ey, W, H)
                        if dist <= self.PRESSURE_R:
                            # plus on est proche, plus c'est fort; mais si trop près, on laissera DEF/killshot trancher
                            pressure += (self.PRESSURE_R - dist)

                    # --- OFFENSE 2 : killshot local — réduire les sorties immédiates ennemies
                    # On pénalise l’ennemi si notre nouveau trail lui coupe des issues.
                    killshot = 0.0
                    for (ex, ey) in enemy_heads_now:
                        deg_before = free_neighbors(ex, ey, myset)
                        deg_after  = free_neighbors(ex, ey, new_myset)
                        if deg_after < deg_before:
                            # bonus proportionnel à l’étranglement
                            killshot += (deg_before - deg_after)
                        # si l'ennemi est très proche, améliore le bonus (opportunité)
                        if torus_dist(nx, ny, ex, ey, W, H) <= 2 and deg_after <= 1:
                            killshot += 1.5

                    # --- léger biais pour garder la ligne droite quand égalité
                    bias = 1 if action == 0 else 0

                    new_score = (
                        area * self.W_AREA +
                        bias * self.W_STRAIGHT +
                        pressure * self.W_PRESSURE +
                        killshot * self.W_KILLSHOT
                    )

                    new_path = path + [action]
                    new_frontier.append((new_score, bias, new_path, nx, ny, nd, new_myset))

            if not new_frontier:
                break

            new_frontier.sort(key=lambda t: (t[0], t[1]), reverse=True)
            frontier = new_frontier[:self.beam]

            s0, b0, p0, *_ = frontier[0]
            if s0 > best_score_seen:
                best_score_seen = s0
                best_first_move = p0[0] if p0 else 0

        return best_first_move

class TronBot:
    def __init__(self, host='127.0.0.1', port=5555, name='NeonBot', depth=10, beam=80):
        self.host = host
        self.port = int(port)
        self.name = name
        self.state = GameState()
        self.reader = None
        self.sock = None
        self.planner = Planner(depth=depth, beam=beam)
        self.last_sent_turn = 0

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # courte temporisation pour éviter dead sockets
        s.settimeout(5.0)
        s.connect((self.host, self.port))
        s.setblocking(False)
        self.sock = s
        self.reader = Reader(s)
        # Hello
        s.sendall(pack_hello(self.name, want_player=0))
        print(f"[+] Connected to {self.host}:{self.port} as {self.name}")

    def run(self):
        try:
            while True:
                try:
                    r, _, _ = select.select([self.sock], [], [], 0.05)
                except (ValueError, OSError):  # socket fermé/invalide
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

        elif msg_type == MSG_PING:
            # pas de réponse requise en V1; ignorer
            pass

    def decide_and_send(self):
        me = self.state.my_state()
        if not me:
            return
        action = self.planner.choose(self.state)  # -1/0/+1
        # envoi seulement si utile (réduit le spam)
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

def main():
    if len(sys.argv) < 2:
        print("Usage: ai_client.py [host] [port] [name] [depth] [beam]")
        print("Example: ai_client.py 127.0.0.1 5555 NeonBot 10 80")
        host = '127.0.0.1'
        port = 5555
        name = 'NeonBotAggro'
        depth = 10
        beam = 80
    else:
        host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 5555
        name = sys.argv[3] if len(sys.argv) > 3 else 'NeonBot'
        depth = int(sys.argv[4]) if len(sys.argv) > 4 else 10
        beam = int(sys.argv[5]) if len(sys.argv) > 5 else 80

    bot = TronBot(host, port, name, depth=depth, beam=beam)
    bot.connect()
    bot.run()

if __name__ == '__main__':
    main()
