# tron_wrapper.py

import struct
import socket
import select
import time

# ===== Constantes de message =====
MSG_HELLO   = 0x0001
MSG_WELCOME = 0x0002
MSG_INPUT   = 0x0003
MSG_STATE   = 0x0004
MSG_PING    = 0x0005
MSG_BYE     = 0x0006

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
TURN_LEFT, TURN_STRAIGHT, TURN_RIGHT = -1, 0, +1


class TronClient:
    """
    Wrapper réseau minimal et robuste pour le serveur Tron (Qt/C++).
    Inspiré du client de référence (tron_ai.py).
    """

    def __init__(self, host, port, name="Bot", endian: str = "<", sock_timeout: float = 5.0):
        # Endianess & formats (recalculés selon 'endian')
        self.ENDIAN = endian
        self.HDR_FMT     = self.ENDIAN + "HHHH"             # type, len, ver, reserved
        self.WELCOME_FMT = self.ENDIAN + "I H H H f f B H H"
        self.PLAYER_FMT  = self.ENDIAN + "B H H B B"
        self.INPUT_FMT   = self.ENDIAN + "b I"
        self.BYE_FMT     = self.ENDIAN + "B"

        self.HDR_SIZE = struct.calcsize(self.HDR_FMT)

        # Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(sock_timeout)
        self.sock.connect((host, port))
        self.sock.setblocking(False)

        self.rx = bytearray()

        # État
        self.name = name.encode("utf-8")[:32]
        self.my_id = None
        self.W = self.H = 0
        self.tick = 0
        self.grid = []
        self.players = []
        self.auto_kill = True
        self._send_hello()

    # ========= Bas niveau =========

    def _send(self, t, payload=b"", ver=1):
        total_len = self.HDR_SIZE + len(payload)
        hdr = struct.pack(self.HDR_FMT, t, total_len, ver, 0)
        try:
            self.sock.sendall(hdr + payload)
        except (BrokenPipeError, OSError):
            pass

    def _send_hello(self):
        want_player = 0
        name_padded = self.name.ljust(32, b"\x00")
        payload = struct.pack(self.ENDIAN + "I 32s", want_player, name_padded)
        self._send(MSG_HELLO, payload)

    def _send_input(self, turn: int, tick_hint: int = 0):
        turn = int(max(-1, min(1, turn)))
        payload = struct.pack(self.INPUT_FMT, turn, int(tick_hint))
        self._send(MSG_INPUT, payload)

    def _try_read_one(self):
        if len(self.rx) < self.HDR_SIZE:
            return None, None
        t, length, ver, _ = struct.unpack(self.HDR_FMT, self.rx[:self.HDR_SIZE])
        if len(self.rx) < length:
            return None, None
        pkt = bytes(self.rx[:length])
        del self.rx[:length]
        return t, pkt

    def _recv_once(self, timeout=0.05):
        r, _, _ = select.select([self.sock], [], [], timeout)
        if r:
            try:
                data = self.sock.recv(65536)
            except BlockingIOError:
                data = b""
            if not data:
                raise ConnectionError("Disconnected")
            self.rx.extend(data)

    def _dispatch_packets(self):
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

    # ========= Handlers =========

    def _handle_welcome(self, pkt: bytes):
        body = pkt[self.HDR_SIZE:]
        vals = struct.unpack(self.WELCOME_FMT, body)
        assigned_id, W, H, tickrate, start_speed, end_speed, auto_kill, length_tick, maps_every = vals
        self.my_id = assigned_id
        self.W, self.H = W, H
        self.auto_kill = bool(auto_kill)

    def _handle_state(self, pkt: bytes):
        body = pkt[self.HDR_SIZE:]
        head_fmt = self.ENDIAN + "I H H B"
        head_sz = struct.calcsize(head_fmt)
        tick, W, H, P = struct.unpack(head_fmt, body[:head_sz])
        off = head_sz

        grid_size = W * H
        grid_bytes = body[off:off + grid_size]
        off += grid_size

        players = []
        psize = struct.calcsize(self.PLAYER_FMT)
        for _ in range(P):
            pid, x, y, d, alive = struct.unpack(self.PLAYER_FMT, body[off:off + psize])
            off += psize
            players.append({"id": pid, "x": x, "y": y, "dir": d, "alive": bool(alive)})

        self.tick = tick
        self.W, self.H = W, H

        self.grid = list(grid_bytes)
        self.players = players

    def _handle_bye(self, pkt: bytes):
        reason_code = struct.unpack(self.BYE_FMT, pkt[self.HDR_SIZE:self.HDR_SIZE + 1])[0]
        reasons = {0: "server closing", 1: "dead", 2: "winner", 3: "kick"}
        raise SystemExit(f"[BYE] reason={reasons.get(reason_code, reason_code)}")
    
    def wait_ready(self, poll_delay=0.05):
        while not self.players:
            self.poll()
            time.sleep(poll_delay)

    def play_loop(self, callback, poll_delay=0.05):
   
        self.wait_ready()
        while self.is_alive():
            self.poll()
            grid = self.get_grid()
            me = self.get_me()
            callback(self, grid, me)
            time.sleep(poll_delay)


    # ========= API haut niveau =========

    def poll(self, timeout=0.05):
        """À appeler dans la boucle principale pour traiter le réseau."""
        self._recv_once(timeout=timeout)
        self._dispatch_packets()

    def rotate_left(self):
        self._send_input(TURN_LEFT, tick_hint=self.tick)

    def rotate_right(self):
        self._send_input(TURN_RIGHT, tick_hint=self.tick)

    def stay_straight(self):
        self._send_input(TURN_STRAIGHT, tick_hint=self.tick)

    def get_grid(self):
        """Retourne la grille comme liste de listes [y][x] (peut être vide avant le 1er STATE)."""
        if not self.grid or self.W == 0 or self.H == 0:
            return []
        return [self.grid[y * self.W:(y + 1) * self.W] for y in range(self.H)]

    def get_players(self):
        return list(self.players)

    def get_me(self):
        return next((p for p in self.players if p["id"] == self.my_id), None)

    def is_alive(self):
        me = self.get_me()
        return bool(me and me["alive"])

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass
