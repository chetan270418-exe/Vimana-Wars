"""
game/systems/duel_client.py
Background-thread SocketIO client for online 1v1 duels.
Sends local player inputs at 20Hz, receives opponent state.
"""
import threading
import time
from dataclasses import dataclass, field
from typing import Optional, Callable

@dataclass
class PlayerState:
    game_id: str = ""
    x: float = 450.0
    y: float = 300.0
    dx: float = 0.0
    dy: float = 0.0
    hp: int = 100
    max_hp: int = 100
    firing: bool = False
    dash: bool = False
    last_updated: float = 0.0

@dataclass  
class DuelState:
    local: PlayerState = field(default_factory=PlayerState)
    opponent: PlayerState = field(default_factory=PlayerState)
    connected: bool = False
    opponent_connected: bool = False
    duel_ended: bool = False
    winner_game_id: str = ""
    error: str = ""

class DuelClient:
    """Thread-safe SocketIO client. Create once, call connect(), then use send_input() each frame."""
    
    def __init__(self, api_url: str, token: str, room_code: str, game_id: str, ship_class: str):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.room_code = room_code
        self.game_id = game_id
        self.ship_class = ship_class
        self.state = DuelState()
        self.state.local.game_id = game_id
        self._sio = None
        self._thread: Optional[threading.Thread] = None
        self._last_send = 0.0
        self._lock = threading.Lock()
        self._on_duel_end: Optional[Callable] = None

    def connect(self, on_duel_end: Optional[Callable] = None) -> None:
        self._on_duel_end = on_duel_end
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        try:
            import socketio as sio_lib
            self._sio = sio_lib.Client(reconnection=True, reconnection_attempts=5)
            
            @self._sio.event
            def connect():
                with self._lock:
                    self.state.connected = True
                self._sio.emit("join_duel", {
                    "token": self.token,
                    "room_code": self.room_code,
                    "game_id": self.game_id,
                    "ship_class": self.ship_class,
                })

            @self._sio.event
            def disconnect():
                with self._lock:
                    self.state.connected = False

            @self._sio.on("player_joined")
            def on_player_joined(data):
                if data.get("game_id") != self.game_id:
                    with self._lock:
                        self.state.opponent.game_id = data.get("game_id", "")
                        self.state.opponent_connected = True

            @self._sio.on("opponent_state")
            def on_opponent_state(data):
                with self._lock:
                    op = self.state.opponent
                    op.x = float(data.get("x", op.x))
                    op.y = float(data.get("y", op.y))
                    op.dx = float(data.get("dx", 0))
                    op.dy = float(data.get("dy", 0))
                    op.firing = bool(data.get("firing", False))
                    op.dash = bool(data.get("dash", False))
                    op.last_updated = time.time()

            @self._sio.on("hp_update")
            def on_hp_update(data):
                with self._lock:
                    for entry in data.get("players", []):
                        if entry["game_id"] == self.game_id:
                            self.state.local.hp = entry["hp"]
                        else:
                            self.state.opponent.hp = entry["hp"]

            @self._sio.on("duel_end")
            def on_duel_end(data):
                with self._lock:
                    self.state.duel_ended = True
                    self.state.winner_game_id = data.get("winner_game_id", "")
                if self._on_duel_end:
                    self._on_duel_end(data)

            @self._sio.on("duel_pong")
            def on_pong(data):
                pass  # latency measurement placeholder

            self._sio.connect(self.api_url, transports=["websocket", "polling"])
            self._sio.wait()
        except Exception as exc:
            with self._lock:
                self.state.error = str(exc)
                self.state.connected = False

    def send_input(self, x: float, y: float, dx: float, dy: float, firing: bool, dash: bool) -> None:
        """Call from game loop — throttled to 20 sends/second."""
        now = time.time()
        if now - self._last_send < 0.05:
            return
        self._last_send = now
        with self._lock:
            self.state.local.x = x
            self.state.local.y = y
        if self._sio and self._sio.connected:
            try:
                self._sio.emit("player_input", {
                    "x": round(x, 1),
                    "y": round(y, 1),
                    "dx": round(dx, 2),
                    "dy": round(dy, 2),
                    "firing": firing,
                    "dash": dash,
                })
            except Exception:
                pass

    def report_hit(self, damage: int) -> None:
        """Call when local player's bullet hits the opponent."""
        with self._lock:
            opponent_id = self.state.opponent.game_id
        if self._sio and self._sio.connected and opponent_id:
            try:
                self._sio.emit("hit_registered", {
                    "target_game_id": opponent_id,
                    "damage": min(50, max(1, int(damage))),
                })
            except Exception:
                pass

    def get_state(self) -> DuelState:
        with self._lock:
            import copy
            return copy.deepcopy(self.state)

    def disconnect(self) -> None:
        if self._sio:
            try:
                self._sio.disconnect()
            except Exception:
                pass
