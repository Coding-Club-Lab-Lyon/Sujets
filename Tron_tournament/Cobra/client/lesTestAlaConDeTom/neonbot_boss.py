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

# ========= Utils grille (globaux, utilisés par l’ancienne IA/diagnostic) =========

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

# ========= IA (nouvelle version optimisée) =========

class NeonAI:
    """
    IA 'safe-first + territory + lookahead':
      - BFS torique pour cartes de distances (moi vs adversaires).
      - Territoire exact: cells où dist_me < dist_opp (Voronoï sans sampling).
      - Pénalités de goulots/dead-ends et risque head-on (L/S/R adverses).
      - Beam search depth-limité (budget temps) pour prévoir 6–10 demi-tours.
    """
    # ===== Réglages principaux =====
    MAX_LOOKAHEAD_DEPTH = 14        # profondeur cible (coupée si budget dépassé)
    BEAM_WIDTH = 12                # états gardés par niveau
    TIME_BUDGET_SEC = 0.004        # ~4 ms par STATE (ajuste selon ta machine/map)
    AREA_CAP = 10_000              # plafond flood-fill local

    # Poids du score
    W_TERRITORY   = 0.5
    W_SAFE_AREA   = 1.0
    W_CORRIDOR    = 2.2
    W_TURN        = 0.6
    W_HEADON      = 2000.0
    W_PROX_ENEMY  = 3.9
    W_CUT_CHANCE  = 0.6

    def __init__(self):
        self.auto_kill = True
        self.my_id = 0
        self.last_dir = RIGHT  # par défaut

    def set_welcome(self, welcome):
        self.auto_kill = bool(welcome.get("auto_kill", True))

    # ---------- utils grille ----------
    @staticmethod
    def wrap_next(x, y, d, W, H):
        if d == 0:   # UP
            y = (y - 1) % H
        elif d == 2: # DOWN
            y = (y + 1) % H
        elif d == 3: # LEFT
            x = (x - 1) % W
        else:        # RIGHT
            x = (x + 1) % W
        return x, y

    @staticmethod
    def dir_after_turn(d, t):
        if t == -1:  # left
            return (d + 3) % 4
        if t == 1:   # right
            return (d + 1) % 4
        return d

    @staticmethod
    def neighbors4(x, y, W, H):
        # renvoie (nx,ny) UP,RIGHT,DOWN,LEFT (ordre fixe)
        return ((x, (y-1) % H),
                ((x+1) % W, y),
                (x, (y+1) % H),
                (((x-1) % W), y))

    # ---------- pré-calculs ----------
    def _blocked_mask(self, grid, W, H):
        # True si bloqué (trail/mur). Tolère sa propre trail si auto_kill=False
        blk = [False]*(W*H)
        if self.auto_kill:
            for i,v in enumerate(grid):
                blk[i] = (v != 0)
        else:
            mid = self.my_id
            for i,v in enumerate(grid):
                blk[i] = (v != 0 and v != mid)
        return blk

    def _deg_free(self, blk, W, H):
        # degré libre (0..4) de chaque cellule (utile pour goulots)
        deg = [0]*(W*H)
        for y in range(H):
            for x in range(W):
                i = y*W + x
                if blk[i]:
                    continue
                c = 0
                for nx,ny in self.neighbors4(x,y,W,H):
                    if not blk[ny*W + nx]:
                        c += 1
                deg[i] = c
        return deg

    def _dist_map(self, seeds, blk, W, H, maxd=1<<30):
        # BFS multi-source torique: retourne liste de distances int (maxd = inf)
        from collections import deque
        INF = maxd
        dist = [INF]*(W*H)
        dq = deque()
        for (x,y) in seeds:
            idx = y*W + x
            if blk[idx]:
                continue
            dist[idx] = 0
            dq.append((x,y))
        while dq:
            x,y = dq.popleft()
            base = dist[y*W + x]
            nb = self.neighbors4(x,y,W,H)
            for nx,ny in nb:
                j = ny*W + nx
                if blk[j] or dist[j] <= base+1:
                    continue
                dist[j] = base+1
                dq.append((nx,ny))
        return dist

    def _territory_score(self, dist_me, dist_opp, blk):
        # nombre de cases joignables où dist_me < dist_opp (territoire net)
        s = 0
        cut = 0
        INF = (1<<29)
        for i,(dm,do) in enumerate(zip(dist_me, dist_opp)):
            if blk[i]:
                continue
            if dm < do:
                s += 1
                # "cut chance": on y arrive significativement plus vite
                if do < INF and (do - dm) >= 2:
                    cut += 1
        return s, cut

    def _safe_area_from(self, start_xy, blk, W, H, cap):
        # flood-fill borné (aire atteignable depuis start_xy)
        if start_xy is None:
            return 0
        sx,sy = start_xy
        si = sy*W + sx
        if blk[si]:
            return 0
        seen = {si}
        from collections import deque
        dq = deque([(sx,sy)])
        cnt = 0
        while dq and cnt < cap:
            x,y = dq.popleft()
            cnt += 1
            for nx,ny in self.neighbors4(x,y,W,H):
                j = ny*W + nx
                if blk[j] or j in seen:
                    continue
                seen.add(j)
                dq.append((nx,ny))
        return cnt

    # Prochaine(s) case(s) possible(s) d’un adversaire: L/S/R en évitant les murs
    def _enemy_next_cells(self, p, blk, W, H):
        out = []
        for t in (-1, 0, 1):
            nd = self.dir_after_turn(p["dir"], t)
            nx, ny = self.wrap_next(p["x"], p["y"], nd, W, H)
            if not blk[ny*W + nx]:
                out.append((nx, ny))
        # s’il n’a aucune option “libre”, on considère quand même son tout-droit pour le risque head-on
        if not out:
            nd = self.dir_after_turn(p["dir"], 0)
            out = [self.wrap_next(p["x"], p["y"], nd, W, H)]
        return set(out)

    # ---------- évaluation instantanée ----------
    def _evaluate_after_move(self, me, t, adverses, grid, W, H, blk=None, deg=None):
        # retourne (score, (nx,ny), ndir)
        nd = self.dir_after_turn(me["dir"], t)
        nx, ny = self.wrap_next(me["x"], me["y"], nd, W, H)

        if blk is None:
            blk = self._blocked_mask(grid, W, H)
        if blk[ny*W + nx]:
            return -1e12, None, nd  # crash immédiat

        # Risque head-on: union des 3 cases possibles pour chaque adversaire
        ho_cells = set()
        for a in adverses:
            if not a["alive"]:
                continue
            ho_cells |= self._enemy_next_cells(a, blk, W, H)
        headon = (nx, ny) in ho_cells

        # Cartes de distance (moi depuis (nx,ny), eux depuis leurs positions)
        dist_me = self._dist_map([(nx,ny)], blk, W, H)
        adv_seeds = [(p["x"], p["y"]) for p in adverses if p["alive"]]
        dist_opp = self._dist_map(adv_seeds, blk, W, H) if adv_seeds else [1<<29]*(W*H)

        # Territoire + potentiel de “cut”
        terr, cut = self._territory_score(dist_me, dist_opp, blk)

        # Surface locale atteignable (sécurisation proche)
        area = self._safe_area_from((nx,ny), blk, W, H, cap=min(self.AREA_CAP, W*H))

        # Pénalités de goulots / cul-de-sac
        if deg is None:
            deg = self._deg_free(blk, W, H)
        d_here = deg[ny*W + nx]
        corridor_pen = 0.0
        if d_here <= 1:
            corridor_pen = 3.0  # dead-end
        elif d_here == 2:
            corridor_pen = 1.2  # couloir

        # Proximité ennemis (pression)
        prox_pen = 0.0
        for a in adverses:
            if not a["alive"]:
                continue
            ax, ay = a["x"], a["y"]
            dm = dist_me[ay*W + ax]
            if dm < (1<<29):
                prox_pen += max(0, 6 - min(6, dm))

        # Pénalité de virage (légère)
        turn_pen = self.W_TURN if t != 0 else 0.0

        score = (
            self.W_TERRITORY * terr
            + self.W_SAFE_AREA * area
            - self.W_CORRIDOR * corridor_pen
            - self.W_PROX_ENEMY * prox_pen
            - turn_pen
            - (self.W_HEADON if headon else 0.0)
            + self.W_CUT_CHANCE * cut
        )
        return score, (nx, ny), nd

    # ---------- lookahead (beam search) ----------
    def _plan(self, state):
        start_t = time.time()

        W, H = state["W"], state["H"]
        grid = state["grid"]
        players = state["players"]
        me = next((p for p in players if p["id"] == self.my_id and p["alive"]), None)
        if not me:
            return 0

        adverses = [p for p in players if p["id"] != self.my_id and p["alive"]]

        blk = self._blocked_mask(grid, W, H)
        deg = self._deg_free(blk, W, H)

        # couche 0 : options immédiates
        roots = []
        for t0 in (-1, 0, 1):
            s0, pos0, d0 = self._evaluate_after_move(me, t0, adverses, grid, W, H, blk=blk, deg=deg)
            roots.append({
                "score": s0,
                "turn0": t0,
                "pos": pos0,
                "dir": d0,
                "blk": blk,   # on ne modifie pas la grille d'origine
            })
        roots.sort(key=lambda x: x["score"], reverse=True)
        beam = roots[:self.BEAM_WIDTH]

        if not beam:
            return 0
        best = max(beam, key=lambda x: x["score"])

        depth = 1
        max_depth = self.MAX_LOOKAHEAD_DEPTH
        while depth < max_depth and (time.time() - start_t) < self.TIME_BUDGET_SEC:
            nxt = []
            for node in beam:
                if node["pos"] is None:
                    continue
                # projection d’une case (la case occupée devient virtuellement bloquée)
                vx, vy = node["pos"]
                vdir = node["dir"]
                vblk = list(node["blk"])
                vblk[vy*W + vx] = True

                virtual_me = {"x": vx, "y": vy, "dir": vdir, "id": self.my_id, "alive": True}
                for t in (-1, 0, 1):
                    sc, pos, nd = self._evaluate_after_move(virtual_me, t, adverses, grid, W, H, blk=vblk, deg=deg)
                    nxt.append({
                        "score": node["score"]*0.6 + sc*0.4,  # cumul lissé (évite de tout miser sur feuille)
                        "turn0": node["turn0"],
                        "pos": pos,
                        "dir": nd,
                        "blk": vblk,
                    })
            if not nxt:
                break
            nxt.sort(key=lambda x: x["score"], reverse=True)
            beam = nxt[:self.BEAM_WIDTH]
            cand = beam[0]
            if cand["score"] > best["score"]:
                best = cand
            depth += 1

        return best.get("turn0", 0)

    # ---------- API publique ----------
    def decide(self, state):
        # garde-fou: si toutes options crash → on prend la moins pire immédiate
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
            return 0

        self.last_dir = me["dir"]

        # tentative planning
        t = self._plan(state)

        # vérifie que le plan ne crash pas immédiatement; sinon, prend le meilleur instantané
        blk = self._blocked_mask(grid, W, H)
        s_best = -1e13
        t_best = 0
        for cand in (-1, 0, 1):
            sc, _, _ = self._evaluate_after_move(me, cand, adverses, grid, W, H, blk=blk)
            if sc > s_best:
                s_best, t_best = sc, cand

        sc_plan, _, _ = self._evaluate_after_move(me, t, adverses, grid, W, H, blk=blk)
        if sc_plan <= -1e11:
            return t_best
        return t

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
    ap.add_argument("--name", default="TurboNeonBot")
    ap.add_argument("--endian", choices=["<", ">"], default="<",
                    help="Ordre des octets des structs (par défaut little '<')")
    ap.add_argument("--spam-hz", type=float, default=0.0,
                    help="Fréquence max d’envoi d’inputs (0 = à chaque STATE)")
    args = ap.parse_args()

    client = Client(args.host, args.port, args.name, endian=args.endian, spam_hz=args.spam_hz)
    client.loop()

if __name__ == "__main__":
    main()
