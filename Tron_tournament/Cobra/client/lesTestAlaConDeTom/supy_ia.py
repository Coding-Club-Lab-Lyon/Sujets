#!/usr/bin/env python3
# tron_ai_client_v2.py
import argparse
import socket
import struct
import threading
import time
from dataclasses import dataclass
from typing import List, Tuple, Optional, Deque
from collections import deque

# ===== Protocol (pack(1), little-endian) =====
HDR_FMT = "<HHHH"; HDR_SIZE = struct.calcsize(HDR_FMT)
MSG_HELLO, MSG_WELCOME, MSG_INPUT, MSG_STATE, MSG_PING, MSG_BYE = 0x0001,0x0002,0x0003,0x0004,0x0005,0x0006
HELLO_FMT = "<I32s"; HELLO_SIZE = struct.calcsize(HELLO_FMT)
WELCOME_FMT = "<IHHHffBHH"; WELCOME_SIZE = struct.calcsize(WELCOME_FMT)
INPUT_FMT = "<bI"; INPUT_SIZE = struct.calcsize(INPUT_FMT)
STATE_HEAD_FMT = "<IHHB"; STATE_HEAD_SIZE = struct.calcsize(STATE_HEAD_FMT)
PLAYER_STATE_FMT = "<BHHBB"; PLAYER_STATE_SIZE = struct.calcsize(PLAYER_STATE_FMT)
BYE_FMT = "<B"; BYE_SIZE = struct.calcsize(BYE_FMT)

@dataclass
class Welcome:
    assigned_id: int; width: int; height: int; tickrate: int
    start_speed: float; end_speed: float; auto_kill: bool
    length_tick: int; maps_every: int

@dataclass
class PlayerState:
    id: int; x: int; y: int; dir: int; alive: bool

class TronAIClient:
    def __init__(self, host: str, port: int, name: str):
        self.host, self.port, self.name = host, port, name
        self.sock: Optional[socket.socket] = None
        self.me_id: Optional[int] = None
        self.width = 0; self.height = 0; self.tickrate = 25
        self.auto_kill = True; self.last_tick = 0
        self.grid: List[int] = []; self.players: List[PlayerState] = []
        self.lock = threading.Lock(); self.running = True
        self._last_choice = 0  # hystérèse: mémorise dernier -1/0/+1

    # --- net ---
    def connect(self):
        self.sock = socket.create_connection((self.host, self.port))
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.send_hello()

    def close(self):
        try:
            if self.sock: self.sock.close()
        finally: self.sock = None

    def send(self, data: bytes):
        assert self.sock is not None; self.sock.sendall(data)

    def recv_exact(self, n: int) -> bytes:
        assert self.sock is not None
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk: raise ConnectionError("Socket closed")
            buf += chunk
        return buf

    # --- proto ---
    def send_hello(self, want_player: int = 0):
        name = self.name.encode("utf-8")[:32]; name += b"\x00"*(32-len(name))
        payload = struct.pack(HELLO_FMT, want_player, name)
        h = struct.pack(HDR_FMT, MSG_HELLO, HDR_SIZE+len(payload), 1, 0)
        self.send(h+payload)

    def send_input(self, turn: int, tick_hint: int = 0):
        payload = struct.pack(INPUT_FMT, int(max(-1, min(1, turn))), int(tick_hint))
        h = struct.pack(HDR_FMT, MSG_INPUT, HDR_SIZE+len(payload), 1, 0)
        self.send(h+payload)

    def read_messages_forever(self):
        try:
            while self.running:
                hdr = self.recv_exact(HDR_SIZE)
                msg_type, msg_len, ver, _ = struct.unpack(HDR_FMT, hdr)
                if ver != 1 or msg_len < HDR_SIZE: raise RuntimeError("Protocol error")
                body = self.recv_exact(msg_len - HDR_SIZE) if msg_len > HDR_SIZE else b""
                if msg_type == MSG_WELCOME: self._on_welcome(body)
                elif msg_type == MSG_STATE: self._on_state(body)
                elif msg_type == MSG_BYE:
                    reason, = struct.unpack(BYE_FMT, body[:BYE_SIZE])
                    print(f"[BYE] reason={reason}"); self.running = False
        except (ConnectionError, OSError) as e:
            print(f"[NET] disconnected: {e}"); self.running = False

    def _on_welcome(self, body: bytes):
        v = struct.unpack(WELCOME_FMT, body[:WELCOME_SIZE])
        w = Welcome(*v)
        with self.lock:
            self.me_id = w.assigned_id
            self.width, self.height = w.width, w.height
            self.tickrate = w.tickrate or 25
            self.auto_kill = bool(w.auto_kill)
            self.grid = [0]*(self.width*self.height); self.players = []
        print(f"[WELCOME] id={self.me_id} {self.width}x{self.height} tickrate={self.tickrate} auto_kill={self.auto_kill}")

    def _on_state(self, body: bytes):
        tick, w, h, pcount = struct.unpack(STATE_HEAD_FMT, body[:STATE_HEAD_SIZE])
        off = STATE_HEAD_SIZE
        grid = list(body[off:off+w*h]); off += w*h
        players: List[PlayerState] = []
        for _ in range(pcount):
            pid, x, y, d, alive = struct.unpack(PLAYER_STATE_FMT, body[off:off+PLAYER_STATE_SIZE]); off += PLAYER_STATE_SIZE
            players.append(PlayerState(pid, x, y, d, bool(alive)))
        with self.lock:
            self.last_tick = tick; self.width, self.height = w, h
            self.grid = grid; self.players = players

    # --- Helpers geom / grille ---
    @staticmethod
    def _wrap(n: int, size: int) -> int: return n % size
    def _idx(self, x: int, y: int) -> int: return self._wrap(y, self.height)*self.width + self._wrap(x, self.width)
    def _cell(self, g: List[int], x: int, y: int) -> int: return g[self._idx(x, y)]

    def _dir_left(self, d: int) -> int:  return (d+3)%4
    def _dir_right(self, d: int) -> int: return (d+1)%4
    def _step(self, x: int, y: int, d: int) -> Tuple[int,int]:
        if d==0: return x, self._wrap(y-1, self.height)
        if d==2: return x, self._wrap(y+1, self.height)
        if d==3: return self._wrap(x-1, self.width), y
        return self._wrap(x+1, self.width), y

    # --- IA améliorée ---
    def _my_state(self) -> Optional[PlayerState]:
        if self.me_id is None: return None
        for p in self.players:
            if p.id == self.me_id: return p
        return None

    def _closest_enemy(self, my: PlayerState) -> Optional[PlayerState]:
        best_d = 10**9; best = None
        for p in self.players:
            if not p.alive or p.id == my.id: continue
            dx = min(abs(p.x-my.x), self.width - abs(p.x-my.x))
            dy = min(abs(p.y-my.y), self.height - abs(p.y-my.y))
            d = dx+dy
            if d < best_d: best_d, best = d, p
        return best

    def _auto_kill_allows(self, cell_owner: int, my_id: int) -> bool:
        # marcher sur sa propre trail autorisé si auto_kill==False
        return (not self.auto_kill) and (cell_owner == my_id)

    def _predict_enemy_next_cells(self) -> set:
        """Retourne l’ensemble des cases où une tête adverse peut apparaître au prochain pas."""
        nxt = set()
        for p in self.players:
            if not p.alive or p.id == self.me_id: continue
            for d in (p.dir, self._dir_left(p.dir), self._dir_right(p.dir)):
                nx, ny = self._step(p.x, p.y, d)
                nxt.add((nx, ny))
        return nxt

    def _flood_area(self, g: List[int], start: Tuple[int,int], my_id: int, max_cap: int=2000) -> int:
        """Compte approximativement l’espace atteignable (cases libres ou propres si auto_kill=False)."""
        sx, sy = start
        if self._cell(g, sx, sy) not in (0, my_id) and not self._auto_kill_allows(self._cell(g, sx, sy), my_id):
            return 0
        seen = set(); q: Deque[Tuple[int,int]] = deque()
        seen.add((sx, sy)); q.append((sx, sy)); count = 0
        while q and count < max_cap:
            x, y = q.popleft(); count += 1
            for d in (0,1,2,3):
                nx, ny = self._step(x, y, d)
                c = self._cell(g, nx, ny)
                ok = (c == 0) or self._auto_kill_allows(c, my_id)
                if ok and (nx, ny) not in seen:
                    seen.add((nx, ny)); q.append((nx, ny))
        return count

    def _score_move(self, relative_turn: int, my: PlayerState, target: Optional[PlayerState], enemy_next: set) -> float:
        """Simule un pas et renvoie un score (plus haut = mieux)."""
        # 1) orientation après turn
        d = my.dir
        if relative_turn == -1: d = self._dir_left(d)
        elif relative_turn == +1: d = self._dir_right(d)

        # 2) position next
        nx, ny = self._step(my.x, my.y, d)
        cell = self.grid[self._idx(nx, ny)]

        # 3) collision immédiate ?
        safe = (cell == 0) or self._auto_kill_allows(cell, my.id)
        if not safe:
            return -1e9  # interdit

        # 4) HEAD-ON: si un ennemi peut aussi prendre (nx,ny), danger fort
        head_on = ((nx, ny) in enemy_next)

        # 5) grille simulée: on “occupe” la case next par nous (blocage des autres)
        g2 = self.grid[:]  # copie légère, grille petite
        g2[self._idx(nx, ny)] = my.id

        # 6) espace atteignable (flood-fill)
        area = self._flood_area(g2, (nx, ny), my.id, max_cap=min(5000, self.width*self.height))

        # 7) agressivité (réduire distance à cible) si présente
        aggro = 0.0
        if target:
            # distance torique
            dx = min(abs(target.x - nx), self.width - abs(target.x - nx))
            dy = min(abs(target.y - ny), self.height - abs(target.y - ny))
            dist = dx + dy
            aggro = -dist  # plus proche => meilleur (négatif pour soustraire)

        # 8) anti wiggle: bonus si on répète le même choix (stabilité)
        stabil = 0.2 if relative_turn == self._last_choice else 0.0

        # 9) pondération
        score = (
            area * 1.0           # priorité à l’espace
            + aggro * 0.6        # agressif mais moins que la survie
            + stabil
            - (6.0 if head_on else 0.0)  # gros malus si tête-à-tête plausible
        )
        return score

    def decide_turn(self) -> int:
        with self.lock:
            my = self._my_state()
            if not my or not my.alive: return 0
            target = self._closest_enemy(my)
            enemy_next = self._predict_enemy_next_cells()

            candidates = [-1, 0, +1]
            best_score, best_turn = -1e18, 0
            for rel in candidates:
                sc = self._score_move(rel, my, target, enemy_next)
                if sc > best_score: best_score, best_turn = sc, rel

            # si toutes les options sont -inf (improbable), tente tout droit
            if best_score < -1e8: best_turn = 0
            self._last_choice = best_turn
            return best_turn

    # --- control ---
    def control_loop(self):
        while self.running:
            turn = self.decide_turn()
            with self.lock: tick_hint = self.last_tick; tr = self.tickrate
            try: self.send_input(turn, tick_hint)
            except Exception as e:
                print(f"[SEND] error: {e}"); self.running = False; break
            time.sleep(1.0 / max(12, tr))  # cadence raisonnable

    def run(self):
        self.connect()
        rx = threading.Thread(target=self.read_messages_forever, daemon=True); rx.start()
        try: self.control_loop()
        finally: self.running = False; self.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5555)
    ap.add_argument("--name", default="BRAINBOT_V2")
    args = ap.parse_args()
    TronAIClient(args.host, args.port, args.name).run()

if __name__ == "__main__":
    main()
