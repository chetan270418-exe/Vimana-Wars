"""Authenticated multiplayer lobby browser.

This screen implements the pre-match layer: create, browse, join, ready,
start, and leave. Combat itself remains authoritative to a future real-time
game session and is intentionally not faked with local-only state.
"""
import math
import random
import arcade

from constants import WIDTH, HEIGHT, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.systems.asset_manager import AssetManager
from game.systems.sound_manager import SoundManager
from game.ui.menu_button import MenuButton
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT, CYAN,
    CYAN_BRIGHT, PARCHMENT, MUTED, RED_BRIGHT,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
)


_RNG = random.Random(77)
_STARS = [(_RNG.randrange(40, WIDTH - 40), _RNG.randrange(30, HEIGHT), _RNG.uniform(0.5, 1.8)) for _ in range(85)]


class MultiplayerView(arcade.View):
    """A network lobby screen backed by the Flask multiplayer API."""

    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self.sound_manager = SoundManager()
        saved = save_system.load()
        self._ship_class = saved.get("last_ship", "pushpaka")
        self._mode = "campaign"
        self._code = ""
        self._lobbies = []
        self._current_lobby = None
        self._selected_lobby = -1
        self._hovered = -1
        self._pulse = 0.0
        self._poll_timer = 0.0
        self._network_busy = False
        self._pending = None
        self._status = ""
        self._status_color = MUTED
        self._api_status = "CONNECTED"
        self._nav_rail = NavRail(current_screen="sangha")

        self._title = arcade.Text(
            "MULTIPLAYER // SANGHA NETWORK", WIDTH // 2, 550,
            GOLD_BRIGHT, font_size=25, bold=True, anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "FORM A VIMANA WING • READY TOGETHER • ENTER THE MAHAYUDDHA",
            WIDTH // 2, 518, CYAN_BRIGHT, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "CLICK A LOBBY TO SELECT   •   TYPE A CODE   •   ESC: BACK",
            WIDTH // 2, 28, MUTED, font_size=9, anchor_x="center", anchor_y="center",
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, 75, MUTED, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._buttons = self._build_buttons()

    def _build_buttons(self):
        data = [
            ("CREATE LOBBY", "create", GOLD),
            ("JOIN CODE", "join", CYAN),
            ("READY / UNREADY", "ready", (100, 240, 190)),
            ("START MATCH", "start", (255, 150, 80)),
            ("LEAVE LOBBY", "leave", RED_BRIGHT),
            ("REFRESH", "refresh", MUTED),
            ("BACK", "back", MUTED),
            ("⚔ LOCAL 1V1 DUEL", "local_duel", GOLD_BRIGHT),
        ]
        ys = (455, 410, 310, 265, 220, 175, 130, 85)
        return [
            (MenuButton(label, 730, ys[i], 205, 31, color), action)
            for i, (label, action, color) in enumerate(data)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        self._buttons = self._build_buttons()
        self._hovered = -1
        self._refresh_lobbies()
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._nav_rail.update(delta_time)
        self._pulse += delta_time
        self._poll_timer += delta_time
        for i, (button, _) in enumerate(self._buttons):
            button.update(delta_time, i == self._hovered)
        if self._current_lobby and self._poll_timer >= 2.0 and not self._network_busy:
            self._poll_timer = 0.0
            self._get_current_lobby()
        if self._pending is not None:
            kind, success, error, body = self._pending
            self._pending = None
            self._network_busy = False
            self._apply_result(kind, success, error, body)

    def _queue_request(self, kind, request_fn) -> None:
        if self._network_busy:
            return
        self._network_busy = True
        self._api_status = "RECONNECTING"
        request_fn(lambda success, error, body: setattr(self, "_pending", (kind, success, error, body)))

    def _refresh_lobbies(self) -> None:
        self._status = "SCANNING ACTIVE LOBBIES..."
        self._status_color = CYAN_BRIGHT
        self._queue_request("list", leaderboard_client.list_lobbies)

    def _get_current_lobby(self) -> None:
        if self._current_lobby:
            self._queue_request("get", lambda done: leaderboard_client.get_lobby(self._current_lobby["code"], done))

    def _apply_result(self, kind, success, error, body) -> None:
        if not success:
            self._api_status = "OFFLINE"
            self._status = error or "Multiplayer request failed"
            self._status_color = RED_BRIGHT
            if kind == "get":
                self._current_lobby = None
            return
        
        self._api_status = "CONNECTED"
        if kind == "list":
            self._lobbies = body.get("lobbies", [])
            self._status = f"{len(self._lobbies)} ACTIVE LOBBY" + ("S" if len(self._lobbies) != 1 else "")
            self._status_color = CYAN_BRIGHT
        elif kind in ("create", "join", "get", "ready", "start"):
            self._current_lobby = body.get("lobby") or self._current_lobby
            if self._current_lobby:
                self._code = self._current_lobby["code"]
                self._status = f"LOBBY {self._code} • {self._current_lobby['status'].upper()}"
                self._status_color = CYAN_BRIGHT
        elif kind == "leave":
            self._current_lobby = None
            self._status = "LEFT LOBBY — READY FOR ANOTHER SORTIE"
            self._status_color = MUTED
            self._refresh_lobbies()

    def _draw_background(self) -> None:
        self.clear()
        for x, y, speed in _STARS:
            sx = (x + self._pulse * speed * 3) % WIDTH
            alpha = int(55 + 35 * math.sin(self._pulse + x * 0.02))
            arcade.draw_circle_filled(sx, y, 1.2, (120, 190, 255, alpha))
        draw_scanlines(0, WIDTH, 0, HEIGHT, CYAN, spacing=20, alpha=5)
        draw_chamfered_panel(265, 585, 95, 485, CYAN, fill=OBSIDIAN, alpha=235, cut=14)
        draw_corner_etching(265, 585, 95, 485, GOLD, length=18, alpha=125)
        draw_chamfered_panel(610, 850, 95, 485, GOLD, fill=OBSIDIAN, alpha=235, cut=14)
        draw_corner_etching(610, 850, 95, 485, CYAN, length=18, alpha=115)

    def _draw_lobby_list(self) -> None:
        arcade.draw_text("OPEN WINGS", 285, 450, GOLD, font_size=11, bold=True)
        if not self._lobbies:
            arcade.draw_text("No open lobbies yet.", 425, 320, MUTED, font_size=12, anchor_x="center")
            arcade.draw_text("Create one and invite another Game ID.", 425, 295, PARCHMENT, font_size=9, anchor_x="center")
            return
        for i, lobby in enumerate(self._lobbies[:7]):
            y = 415 - i * 45
            selected = i == self._selected_lobby
            color = GOLD_BRIGHT if selected else (75, 100, 140)
            fill = SURFACE_HIGH if selected else SURFACE_LOW
            draw_chamfered_panel(280, 570, y - 16, y + 17, color, fill=fill, alpha=240, cut=6)
            players = lobby.get("players", [])
            arcade.draw_text(lobby.get("code", "------"), 298, y, color, font_size=14, bold=True, font_name="Courier New", anchor_y="center")
            
            mode = lobby.get("mode", "campaign").upper()
            mode_icon = "⚔" if mode == "DUEL" else ("🤝" if mode == "CO-OP" else "∞")
            arcade.draw_text(f"{mode_icon} {mode}", 390, y + 6, PARCHMENT, font_size=8, bold=True)
            
            max_p = lobby.get('max_players', 2)
            dots = ""
            for p_idx in range(max_p):
                dots += "● " if p_idx < len(players) else "○ "
            arcade.draw_text(dots.strip(), 390, y - 6, MUTED, font_size=7)
            
            st = lobby.get("status", "waiting").upper()
            st_color = CYAN if st == "WAITING" else (GOLD if st == "FULL" else RED_BRIGHT)
            from game.ui.vedic_theme import draw_state_badge
            draw_state_badge(525, y, st, st_color, width=50)

    def _draw_current_lobby(self) -> None:
        account = leaderboard_client.current_account()
        arcade.draw_text("YOUR GAME ID", 635, 450, MUTED, font_size=8, bold=True)
        arcade.draw_text(account["game_id"] if account else "SIGN IN REQUIRED", 635, 428,
                         CYAN_BRIGHT if account else RED_BRIGHT, font_size=14, bold=True)
        
        # Mode Tabs
        for i, (mode_label, mode_val) in enumerate([("⚔ DUEL", "duel"), ("🤝 CO-OP", "coop"), ("∞ ENDLESS", "endless")]):
            tx = 630 + i * 65
            selected = self._mode == mode_val
            color = GOLD if selected else MUTED
            draw_chamfered_panel(tx, tx + 60, 350, 380, color, fill=SURFACE_LOW, alpha=245, border_width=2 if selected else 1, cut=4)
            arcade.draw_text(mode_label, tx + 30, 365, color, font_size=7, bold=True, anchor_x="center", anchor_y="center")

        arcade.draw_text("LOBBY CODE", 635, 205, MUTED, font_size=8, bold=True)
        draw_chamfered_panel(635, 825, 165, 195, GOLD, fill=SURFACE_LOW, alpha=245, cut=6,
                             selected=True)
        arcade.draw_text(self._code or "TYPE CODE", 730, 180,
                         GOLD_BRIGHT if self._code else MUTED, font_size=20, bold=True, anchor_x="center", anchor_y="center")
        if self._current_lobby:
            lobby = self._current_lobby
            arcade.draw_text(f"{lobby.get('mode', 'campaign').upper()} • {lobby['status'].upper()}", 635, 145,
                             PARCHMENT, font_size=9, bold=True)
            for i in range(lobby.get('max_players', 2)):
                if i < len(lobby.get("players", [])):
                    player = lobby.get("players")[i]
                    is_ready = player.get("ready")
                    host = "HOST" if player.get("host") else "WING"
                    player_name = player.get("game_id", "—")
                    color = CYAN_BRIGHT if is_ready else PARCHMENT
                    cy = 118 - i * 22
                    arcade.draw_polygon_filled(((635, cy+6), (645, cy), (635, cy-6)), color)
                    arcade.draw_text(f"{host}  {player_name}", 655, cy, color, font_size=8, anchor_y="center")
                    if is_ready:
                        pulse = 155 + int(100 * math.sin(self._pulse * 8))
                        arcade.draw_circle_filled(815, cy, 3, (50, 255, 150, pulse))
                        arcade.draw_text("READY", 805, cy, CYAN_BRIGHT, font_size=8, anchor_x="right", anchor_y="center")
                    else:
                        arcade.draw_circle_filled(815, cy, 3, MUTED)
                        arcade.draw_text("STANDBY", 805, cy, MUTED, font_size=8, anchor_x="right", anchor_y="center")
                else:
                    cy = 118 - i * 22
                    arcade.draw_text("WAITING FOR PILOT...", 635, cy, MUTED, font_size=8, anchor_y="center")
        else:
            arcade.draw_text("Select a lobby or create one.", 730, 125, MUTED, font_size=9, anchor_x="center")
            if self._mode == "duel":
                arcade.draw_text("COMING SOON — ONLINE DUEL LAUNCHING SOON", 730, 105, (255, 150, 50), font_size=7, bold=True, anchor_x="center")

    def on_draw(self) -> None:
        self._draw_background()
        logo = AssetManager.texture("vimana_wars_logo.png")
        AssetManager.draw(logo, 75, 535, 30, 30)
        self._title.draw()
        self._subtitle.draw()
        
        if self._api_status == "CONNECTED":
            dot_color = (50, 200, 100)
        elif self._api_status == "RECONNECTING":
            dot_color = (200, 180, 50)
        else:
            dot_color = RED_BRIGHT
        arcade.draw_text(f"● {self._api_status}", WIDTH - 30, 565, dot_color, font_size=8, bold=True, anchor_x="right")

        self._draw_lobby_list()
        self._draw_current_lobby()
        if self._status:
            self._status_text.text = self._status
            self._status_text.color = self._status_color
            self._status_text.draw()
        for button, _ in self._buttons:
            button.draw()
        self._hint.draw()
        self._nav_rail.draw()
        TransitionOverlay.draw()

    def _selected_code(self) -> str:
        if self._code.strip():
            return self._code.strip().upper()
        if 0 <= self._selected_lobby < len(self._lobbies):
            return self._lobbies[self._selected_lobby].get("code", "").upper()
        return ""

    def _require_account(self) -> bool:
        if leaderboard_client.current_account():
            return True
        self._status = "SIGN IN FROM ACCOUNT BEFORE JOINING A MULTIPLAYER WING"
        self._status_color = RED_BRIGHT
        return False

    def _activate(self, action: str) -> None:
        if action == "back":
            target = self.return_view
            if target is None:
                from game.views.menu_view import MenuView
                target = MenuView()
            transition_to(self.window, target)
            return
        if action == "refresh":
            self._refresh_lobbies()
            return
        if action == "local_duel":
            from game.views.difficulty_view import DifficultyView
            # You can route to GameView with 2 players or any Duel view if it exists.
            # Using DifficultyView or similar if "on_local_duel" is mentioned.
            # We can also just transition to game view directly for local duel.
            from game.views.game_view import GameView
            transition_to(self.window, GameView(difficulty="normal", ship_class=self._ship_class))
            return
        if not self._require_account():
            return
        if action == "create":
            self._queue_request("create", lambda done: leaderboard_client.create_lobby(
                self._mode, 2, self._ship_class, done))
        elif action == "join":
            code = self._selected_code()
            if not code:
                self._status = "SELECT A LOBBY OR TYPE ITS SIX-CHARACTER CODE"
                self._status_color = RED_BRIGHT
                return
            self._queue_request("join", lambda done: leaderboard_client.join_lobby(code, self._ship_class, done))
        elif action == "ready":
            if not self._current_lobby:
                self._status = "JOIN OR CREATE A LOBBY FIRST"
                self._status_color = RED_BRIGHT
                return
            account = leaderboard_client.current_account()
            mine = next((p for p in self._current_lobby.get("players", []) if p.get("game_id") == account["game_id"]), {})
            self._queue_request("ready", lambda done: leaderboard_client.set_lobby_ready(
                self._current_lobby["code"], not mine.get("ready", False), done))
        elif action == "start":
            if self._current_lobby:
                self._queue_request("start", lambda done: leaderboard_client.start_lobby(self._current_lobby["code"], done))
            else:
                self._status = "JOIN OR CREATE A LOBBY FIRST"
                self._status_color = RED_BRIGHT
        elif action == "leave":
            if self._current_lobby:
                self._queue_request("leave", lambda done: leaderboard_client.leave_lobby(self._current_lobby["code"], done))

    def _handle_nav(self, key: str) -> None:
        """Delegate navigation from the rail to the appropriate view."""
        self._nav_rail.navigate_to(key, self.window)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)
        new_hovered = -1
        for i, (button, _) in enumerate(self._buttons):
            if button.contains(x, y):
                new_hovered = i
                break
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.18)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        nav = self._nav_rail.on_mouse_press(x, y, self.window)
        if nav:
            self._handle_nav(nav)
            return
        
        # Mode tabs click
        if 350 <= y <= 380:
            for i, mode_val in enumerate(["duel", "coop", "endless"]):
                if 630 + i * 65 <= x <= 690 + i * 65:
                    self._mode = mode_val
                    self.sound_manager.play_ui_click()
                    return

        if 635 <= x <= 825 and 165 <= y <= 195:
            self._code = ""
            return
        for i, lobby in enumerate(self._lobbies[:7]):
            row_y = 415 - i * 45
            if 280 <= x <= 570 and row_y - 16 <= y <= row_y + 17:
                self._selected_lobby = i
                self._code = lobby.get("code", "")
                return
        for i, (menu_button, action) in enumerate(self._buttons):
            if menu_button.contains(x, y):
                self._hovered = i
                self.sound_manager.play_ui_click()
                self._activate(action)
                return

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            self._activate("back")
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            if self._hovered >= 0:
                self._activate(self._buttons[self._hovered][1])
            else:
                self._activate("join")
        elif key == arcade.key.BACKSPACE:
            self._code = self._code[:-1]
        elif key in (arcade.key.UP, arcade.key.W):
            self._hovered = (self._hovered - 1) % len(self._buttons)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._hovered = (self._hovered + 1) % len(self._buttons)

    def on_text(self, text: str) -> None:
        if text.isalnum() and len(self._code) < 6:
            self._code += text.upper()
