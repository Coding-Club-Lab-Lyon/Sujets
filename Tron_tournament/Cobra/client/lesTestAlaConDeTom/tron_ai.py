#!/usr/bin/env python3
# tron_ai.py – Client IA optimisé pour le serveur Tron (Qt/C++)
# Python 3.8+

import argparse
import socket
import struct
import sys
import time
import select
from collections import deque

# ========= Protocole (voir ./src/Protocol.h) =========
# Hypothèse endianness: little-endian (x86_64). Ajustable par option.
ENDIAN = "<"

MSG_HELLO   = 0x0001
MSG_WELCOME = 0x0002
MSG_INPUT   = 0x0003
MSG_STATE   = 0x0004
MSG_PING    = 0x0005
MSG_BYE     = 0x0006

HDR_FMT = ENDIAN + "HHHH"   # type, len, ver, reserved
HDR_SIZE = struct.calcsize(HDR_FMT)

# Structures utiles
WELCOME_FMT   = ENDIAN + "I H H H f f B H H"  # sans header
PLAYER_FMT    = ENDIAN + "B H H B B"
INPUT_FMT     = ENDIAN + "b I"                # turn, tick
BYE_FMT       = ENDIAN + "B"

# Directions (doivent matcher l'énum C++)
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
TURN_LEFT  = -1
TURN_STRAIGHT = 0
TURN_RIGHT = +1

# ========= Utils grille =========

def wrap_next(x, y, d, W, H):
    if d == UP:
        y = (y - 1) % H
    elif d == DOWN:
        y = (y + 1) % H
    elif d == LEFT:
        x = (x - 1) % W
    else:  # RIGHT
        x = (x + 1) % W
    return x, y

def dir_after_turn(d, t):
    if t == TURN_LEFT:
        return (d + 3) % 4
    if t == TURN_RIGHT:
        return (d + 1) % 4
    return d

def manhattan_wrap(a, b, W, H):
    dx = min((a[0]-b[0]) % W, (b[0]-a[0]) % W)
    dy = min((a[1]-b[1]) % H, (b[1]-a[1]) % H)
    return dx + dy

# ========= IA =========

class NeonAI:
    """
    IA orientation 'safe-first + space-max':
      1) Évite les collisions immédiates (murs/traînées + head-on probable).
      2) Score par option (-1/0/+1) = Aire atteignable (BFS) + Voronoi-lite
         - pénalités proximité de têtes
         - légère pénalité de virage (anti zig-zag)
      3) Fallback: première option non head-on sinon tout droit.
    """
    def __init__(self):
        self.auto_kill = True
        self.my_id = 0
        self.last_dir = RIGHT

    def set_welcome(self, welcome):
        self.auto_kill = bool(welcome["auto_kill"])

    def decide(self, state):
        """state: dict avec keys: W,H,grid(bytearray), players(list of dict), tick(int)"""
        W, H = state["W"], state["H"]
        grid = state["grid"]
        players = state["players"]

        me = None
        adverses = []
        for p in players:
            if p["id"] == self.my_id and p["alive"]:
                me = p
            elif p["alive"]:
                adverses.append(p)
        if me is None:
            return TURN_STRAIGHT

        self.last_dir = me["dir"]

        adv_pos = [(p["x"], p["y"]) for p in adverses]
        adv_next = [wrap_next(p["x"], p["y"], p["dir"], W, H) for p in adverses]

        options = [TURN_LEFT, TURN_STRAIGHT, TURN_RIGHT]
        best = (float("-inf"), TURN_STRAIGHT)

        def cell_blocked(x, y):
            v = grid[y*W + x]
            if v == 0:
                return False
            if (not self.auto_kill) and (v == self.my_id):
                return False
            return True

        def reachable_area(from_xy, cap=2000):
            start = from_xy
            if cell_blocked(*start):
                return 0
            seen = set([start])
            dq = deque([start])
            count = 0
            while dq and count < cap:
                x, y = dq.popleft()
                count += 1
                for nd in (UP, RIGHT, DOWN, LEFT):
                    nx, ny = wrap_next(x, y, nd, W, H)
                    if (nx, ny) in seen:
                        continue
                    if cell_blocked(nx, ny):
                        continue
                    seen.add((nx, ny))
                    dq.append((nx, ny))
            return count

        def voronoi_score(seed, sample_step=max(1, min(W, H)//12)):
            sx, sy = seed
            mine = 0
            theirs = 0
            for yy in range(0, H, sample_step):
                for xx in range(0, W, sample_step):
                    if grid[yy*W + xx] != 0 and not ((not self.auto_kill) and grid[yy*W+xx]==self.my_id):
                        continue
                    dm = manhattan_wrap((sx, sy), (xx, yy), W, H)
                    da = 10**9
                    for ap in adv_pos:
                        da = min(da, manhattan_wrap(ap, (xx, yy), W, H))
                    if dm < da:
                        mine += 1
                    elif da < dm:
                        theirs += 1
            return mine - theirs

        def head_on_penalty(next_xy):
            return -100000 if next_xy in adv_next else 0

        for t in options:
            ndir = dir_after_turn(me["dir"], t)
            nx, ny = wrap_next(me["x"], me["y"], ndir, W, H)

            if cell_blocked(nx, ny):
                score = -1e9
            else:
                area = reachable_area((nx, ny), cap=W*H)
                vscore = voronoi_score((nx, ny))
                prox_pen = 0
                for ap in adv_pos:
                    d = manhattan_wrap((nx, ny), ap, W, H)
                    if d <= 2:
                        prox_pen -= (6 - 2*d)  # -4, -2, 0…
                turn_pen = - (0.8 if t != TURN_STRAIGHT else 0.0)
                ho_pen = head_on_penalty((nx, ny))
                score = 1.0*area + 1.8*vscore + prox_pen + turn_pen + ho_pen

            if score > best[0]:
                best = (score, t)

        if best[0] == -1e9:
            # Aucune option safe → éviter head-on si possible
            for t in options:
                ndir = dir_after_turn(me["dir"], t)
                nx, ny = wrap_next(me["x"], me["y"], ndir, W, H)
                if (nx, ny) not in adv_next:
                    return t
            return TURN_STRAIGHT

        return best[1]

# ========= Client réseau =========

class Client:
    def __init__(self, host, port, name, endian="<", spam_hz=0.0):
        global ENDIAN, HDR_FMT, WELCOME_FMT, PLAYER_FMT, INPUT_FMT, BYE_FMT
        ENDIAN = endian  # au cas où
        HDR_FMT = ENDIAN + "HHHH"
        WELCOME_FMT = ENDIAN + "I H H H f f B H H"
        PLAYER_FMT = ENDIAN + "B H H B B"
        INPUT_FMT = ENDIAN + "b I"
        BYE_FMT = ENDIAN + "B"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(5.0)
        self.sock.connect((host, port))
        self.sock.setblocking(False)
        self.rx = bytearray()
        self.name = name.encode("utf-8")[:32]
        self.my_id = 0
        self.ai = NeonAI()
        self.W = self.H = 0
        self.tick = 0
        self.auto_kill = True
        self.last_input_time = 0.0
        self.spam_period = (1.0/spam_hz) if spam_hz > 0.0 else 0.0

        # Anti-toupie / cadence de virages
        self.last_pos = None          # (x,y) la dernière case vue pour moi
        self.turn_armed = False       # True si un virage non-nul a été envoyé et on attend d'avancer
        self.last_sent_turn = 0

        self._send_hello()

    # ---- envoi ----

    def _send(self, t, payload=b"", ver=1):
        total_len = HDR_SIZE + len(payload)
        hdr = struct.pack(HDR_FMT, t, total_len, ver, 0)
        try:
            self.sock.sendall(hdr + payload)
        except (BrokenPipeError, OSError):
            pass

    def _send_hello(self):
        want_player = 0
        name_padded = self.name.ljust(32, b"\x00")
        payload = struct.pack(ENDIAN + "I 32s", want_player, name_padded)
        self._send(MSG_HELLO, payload)

    def send_input(self, turn):
        payload = struct.pack(INPUT_FMT, int(turn), int(self.tick))
        self._send(MSG_INPUT, payload)

    # ---- parsing ----

    def _try_read_one(self):
        if len(self.rx) < HDR_SIZE:
            return None, None
        t, length, ver, _ = struct.unpack(HDR_FMT, self.rx[:HDR_SIZE])
        if len(self.rx) < length:
            return None, None
        pkt = bytes(self.rx[:length])
        del self.rx[:length]
        return t, pkt

    def _handle_welcome(self, pkt):
        body = pkt[HDR_SIZE:]
        vals = struct.unpack(WELCOME_FMT, body)
        assigned_id, W, H, tickrate, start_speed, end_speed, auto_kill, length_tick, maps_every = vals
        self.my_id = assigned_id
        self.W, self.H = W, H
        self.auto_kill = bool(auto_kill)
        self.ai.my_id = assigned_id
        self.ai.set_welcome({
            "auto_kill": self.auto_kill
        })
        print(f"[WELCOME] id={assigned_id} map={W}x{H} tickrate={tickrate} auto_kill={self.auto_kill}")

    def _handle_state(self, pkt):
        body = pkt[HDR_SIZE:]
        head_fmt = ENDIAN + "I H H B"
        head_sz = struct.calcsize(head_fmt)
        tick, W, H, P = struct.unpack(head_fmt, body[:head_sz])
        off = head_sz

        grid_size = W*H
        grid = body[off:off+grid_size]
        off += grid_size

        players = []
        psize = struct.calcsize(PLAYER_FMT)
        for _ in range(P):
            pid, x, y, d, alive = struct.unpack(PLAYER_FMT, body[off:off+psize])
            off += psize
            players.append({"id": pid, "x": x, "y": y, "dir": d, "alive": bool(alive)})

        self.tick = tick
        state = {"W": W, "H": H, "grid": grid, "players": players, "tick": tick}
        self._think_and_act(state)

    def _handle_bye(self, pkt):
        reason = struct.unpack(BYE_FMT, pkt[HDR_SIZE:HDR_SIZE+1])[0]
        reasons = {0:"server closing",1:"dead",2:"winner",3:"kick"}
        print(f"[BYE] reason={reasons.get(reason,reason)}")
        raise SystemExit(0)

    # ---- décision (anti-toupie inclus) ----

    def _think_and_act(self, state):
        now = time.time()
        if self.spam_period > 0.0 and (now - self.last_input_time) < self.spam_period:
            return

        # trouver "moi"
        me = None
        for p in state["players"]:
            if p["id"] == self.my_id and p["alive"]:
                me = p
                break
        if me is None:
            return

        cur_pos = (me["x"], me["y"])
        moved = (self.last_pos is not None and cur_pos != self.last_pos)

        # si on vient de bouger, on réarme la possibilité de tourner
        if moved:
            self.turn_armed = False
            self.last_sent_turn = 0

        desired = self.ai.decide(state)

        # Garde-fou anti-toupie :
        # - si un virage non-nul a déjà été envoyé et qu'on n'a pas bougé, forcer 0
        # - sinon, n'autoriser qu'UN seul virage non-nul avant la prochaine case
        if self.turn_armed:
            send_turn = 0
        else:
            if desired != 0:
                send_turn = desired
                self.turn_armed = True
                self.last_sent_turn = desired
            else:
                send_turn = 0

        self.send_input(send_turn)
        self.last_input_time = now
        self.last_pos = cur_pos

    # ---- boucle ----

    def loop(self):
        try:
            while True:
                r, _, _ = select.select([self.sock], [], [], 0.05)
                if r:
                    try:
                        data = self.sock.recv(65536)
                    except BlockingIOError:
                        data = b""
                    if not data:
                        print("[NET] Disconnected")
                        break
                    self.rx.extend(data)

                while True:
                    t, pkt = self._try_read_one()
                    if t is None:
                        break
                    if t == MSG_WELCOME:
                        self._handle_welcome(pkt)
                    elif t == MSG_STATE:
                        self._handle_state(pkt)
                    elif t == MSG_BYE:
                        self._handle_bye(pkt)
                    elif t == MSG_PING:
                        pass
        except KeyboardInterrupt:
            pass
        finally:
            try:
                self.sock.close()
            except:
                pass

# ========= main =========

def main():
    ap = argparse.ArgumentParser(description="IA Tron (client Python)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5555)
    ap.add_argument("--name", default="NeonBot")
    ap.add_argument("--endian", choices=["<", ">"], default="<",
                    help="Ordre des octets des structs (par défaut little '<')")
    ap.add_argument("--spam-hz", type=float, default=0.0,
                    help="Fréquence max d’envoi d’inputs (0 = à chaque STATE)")
    args = ap.parse_args()

    client = Client(args.host, args.port, args.name, endian=args.endian, spam_hz=args.spam_hz)
    client.loop()

if __name__ == "__main__":
    main()
