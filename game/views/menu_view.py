"""
Vimana Wars Command Deck — Main Menu View.
Reskinned per Section 7.1 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, Hero Vimana hologram panel, real Pilot Record dossier,
primary Celestial Gold [ DEPLOY SORTIE ] button, and three-card mode row.
"""
import math
import random
import arcade

from constants import WIDTH, HEIGHT, REALMS
from game.entities.ship_classes import SHIP_CLASSES
from game.systems import save_system, achievement_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.systems.leaderboard_client import leaderboard_client
from game.ui.nav_rail import NavRail
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    VOID, OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, ASTRA_RED, PARCHMENT, STARLIGHT, GREY, MUTED,
    FONT_CEREMONIAL, FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_segmented_bar,
    draw_scanlines, draw_telemetry_ticks, pulse_alpha, draw_state_badge,
)


_RNG = random.Random(42)
_STARS = [
    (_RNG.randint(220, WIDTH), _RNG.randint(0, HEIGHT),
     _RNG.uniform(0.6, 1.8), _RNG.randint(80, 210), _RNG.uniform(0.5, 1.5))
    for _ in range(80)
]


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        self.sound_manager = SoundManager()
        self.nav_rail = NavRail("menu")

        # Load real game state
        saved = save_system.load()
        self._reduced_flashes = bool(saved.get("reduced_flashes", False))
        self._high_score = saved.get("high_score", 0)
        self._last_diff = saved.get("difficulty", "normal").upper()
        self._last_ship_id = saved.get("last_ship", "pushpaka")
        self._last_wave = max(0, int(saved.get("last_wave", 0)))

        # Calculate real unlocked realms
        unlocked = sum(1 for start in (1, 4, 7, 10, 13, 16, 19) if self._last_wave >= start)
        self._unlocked_realms = max(1, unlocked)

        # Calculate real ships unlocked
        self._unlocked_ships = sum(
            1 for s in SHIP_CLASSES.values()
            if self._last_wave >= s.get("unlock_wave", 0)
        )

        # Calculate real trophies
        achievements = achievement_system.get_all()
        self._unlocked_trophies = sum(1 for a in achievements if a.get("unlocked", False))
        self._total_trophies = len(achievements)

        # Current realm name
        realm_id = min(7, max(1, self._unlocked_realms))
        self._current_realm_name = REALMS.get(realm_id, {}).get("name", "Swarga")

        # Primary Sortie Action Button (Celestial Gold)
        self._btn_deploy = MenuButton(
            "DEPLOY SORTIE  ▶", 560, 168,
            width=620, height=44, accent=GOLD, variant="celestial"
        )

        # Mode row buttons (Metallic)
        self._mode_buttons = [
            (MenuButton("CAMPAIGN MAP", 340, 102, 195, 34, accent=CYAN, variant="metallic"), "map"),
            (MenuButton("ENDLESS MODE", 560, 102, 195, 34, accent=(180, 140, 255), variant="metallic"), "endless"),
            (MenuButton("LEADERBOARDS", 780, 102, 195, 34, accent=GOLD, variant="metallic"), "leaderboard"),
        ]

        self._hovered_mode = -1
        self._hovered_deploy = False

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()
        # Refresh dynamic state
        saved = save_system.load()
        self._last_wave = max(0, int(saved.get("last_wave", 0)))
        self._high_score = saved.get("high_score", 0)
        self._last_ship_id = saved.get("last_ship", "pushpaka")

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)

        self._btn_deploy.update(delta_time, self._hovered_deploy)
        for i, (btn, _) in enumerate(self._mode_buttons):
            btn.update(delta_time, i == self._hovered_mode)

    def on_draw(self) -> None:
        self.clear()

        # ── Background Parallax Drift (x=220 to WIDTH) ───────────────────────
        for sx, sy, radius, base, speed in _STARS:
            x = 220 + ((sx - 220 + self._pulse * speed * 6.0) % (WIDTH - 220))
            y = (sy + self._pulse * speed * 1.5) % HEIGHT
            brightness = int(base + 20 * math.sin(self._pulse * 0.8 + sx * 0.01))
            arcade.draw_circle_filled(x, y, radius, (brightness, brightness, min(255, brightness + 20)))

        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        # Wordmark & Context
        arcade.draw_text("COMMAND DECK // BRIDGE CONSOLE", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(f"CURRENT THEATER: {self._current_realm_name.upper()} // WAVE {self._last_wave:02d}",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Online Sync Badge
        saved = save_system.load()
        game_id = saved.get("game_id", "")
        sync_label = f"VMN-{game_id[-6:]}" if game_id else "LOCAL GUEST"
        is_online = leaderboard_client.is_online()
        sync_color = CYAN_BRIGHT if is_online else GREY

        draw_state_badge(WIDTH - 70, 574, "ONLINE" if is_online else "OFFLINE", sync_color, width=74)
        arcade.draw_text(sync_label, WIDTH - 120, 574, STARLIGHT,
                         font_size=9, bold=True, anchor_x="right", anchor_y="center",
                         font_name=FONT_TELEMETRY)

        # ── Left Hero Vimana Panel (x=240 to 550, y=225 to 530) ─────────────
        draw_chamfered_panel(240, 550, 225, 530, CYAN, fill=SURFACE_LOW, alpha=225, cut=10.0)
        draw_corner_etching(240, 550, 225, 530, GOLD, length=14.0, alpha=110)

        arcade.draw_text("ACTIVE VIMANA CRAFT", 256, 508, CYAN_BRIGHT,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)

        ship_data = SHIP_CLASSES.get(self._last_ship_id, SHIP_CLASSES["pushpaka"])
        arcade.draw_text(ship_data["name"].upper(), 256, 488, GOLD_BRIGHT,
                         font_size=16, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(ship_data.get("subtitle", "Celestial Flagship"), 256, 472, PARCHMENT,
                         font_size=8, bold=True, font_name=FONT_INTERFACE)

        # Counter-rotating hologram halo rings
        cx, cy = 395, 355
        ring_angle = 0.0 if self._reduced_flashes else self._pulse * 14.0
        ring_alpha = pulse_alpha(self._pulse, 20, 55, 1.8, self._reduced_flashes)
        arcade.draw_circle_outline(cx, cy, 65, (*GOLD, 40), 1)
        arcade.draw_arc_outline(cx, cy, 140, 140, (*CYAN, ring_alpha),
                                ring_angle, ring_angle + 240, 2)
        arcade.draw_arc_outline(cx, cy, 175, 175, (*GOLD, max(15, ring_alpha // 2)),
                                -ring_angle, -ring_angle + 200, 1)

        # Hero ship sprite
        hero_tex = AssetManager.texture(ship_data.get("sprite", "pushpaka.png"))
        float_y = 0.0 if self._reduced_flashes else math.sin(self._pulse * 1.2) * 4.0
        if not AssetManager.draw(hero_tex, cx, cy + float_y, 110, 110):
            arcade.draw_triangle_filled(cx, cy + 50 + float_y, cx - 40, cy - 40 + float_y,
                                        cx + 40, cy - 40 + float_y, ship_data["color"])

        # Reticle crosshair
        arcade.draw_line(cx - 18, cy + float_y, cx + 18, cy + float_y, (*CYAN, 75), 1)
        arcade.draw_line(cx, cy - 18 + float_y, cx, cy + 18 + float_y, (*CYAN, 75), 1)

        # Weapon loadout strip
        arcade.draw_line(256, 260, 534, 260, (*CYAN, 55), 1)
        arcade.draw_text("SYSTEMS ARMED // READY FOR SORTIE", 256, 242, (*CYAN, 190),
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # ── Right Pilot Record Dossier (x=570 to 880, y=225 to 530) ─────────
        draw_chamfered_panel(570, 880, 225, 530, GOLD, fill=SURFACE_LOW, alpha=225, cut=10.0)
        draw_corner_etching(570, 880, 225, 530, CYAN, length=14.0, alpha=110)

        arcade.draw_text("PILOT DOSSIER // CAMPAIGN RECORD", 586, 508, GOLD,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_text("AKASHIC CHRONICLES", 586, 488, GOLD_BRIGHT,
                         font_size=16, bold=True, font_name=FONT_INTERFACE)

        # Campaign Progress Bar
        arcade.draw_text("CAMPAIGN RESONANCE", 586, 452, STARLIGHT,
                         font_size=9, bold=True, font_name=FONT_INTERFACE)
        prog_pct = int((self._unlocked_realms / 7.0) * 100)
        arcade.draw_text(f"{prog_pct}%  ({self._unlocked_realms}/7 REALMS)", 864, 452, GOLD_BRIGHT,
                         font_size=9, bold=True, anchor_x="right", font_name=FONT_TELEMETRY)
        draw_segmented_bar(586, 864, 436, 444, self._unlocked_realms / 7.0,
                           color=GOLD, segments=7, gap=4.0)

        # Real Statistics Grid
        stat_rows = [
            ("HIGHEST WAVE REACHED", f"WAVE {self._last_wave:02d} / 20", CYAN_BRIGHT),
            ("VESSELS COMMISSIONED", f"{self._unlocked_ships} / 9 SHIPS", STARLIGHT),
            ("HONORIFIC TROPHIES", f"{self._unlocked_trophies} / {self._total_trophies} UNLOCKED", GOLD_BRIGHT),
            ("COMBAT DIFFICULTY", f"{self._last_diff}", PARCHMENT),
            ("LIFETIME HIGH SCORE", f"{self._high_score:,}", GOLD_BRIGHT),
        ]

        sy = 398
        for label, val, val_col in stat_rows:
            arcade.draw_text(label, 586, sy, GREY, font_size=8, bold=True, font_name=FONT_TELEMETRY)
            arcade.draw_text(val, 864, sy, val_col, font_size=9, bold=True, anchor_x="right", font_name=FONT_TELEMETRY)
            arcade.draw_line(586, sy - 6, 864, sy - 6, (*GREY, 35), 1)
            sy -= 32

        # ── Primary Deploy Sortie Button ─────────────────────────────────────
        self._btn_deploy.draw()

        # ── Three-Card Mode Row ──────────────────────────────────────────────
        for btn, _ in self._mode_buttons:
            btn.draw()

        # ── Bottom Command Hints ─────────────────────────────────────────────
        arcade.draw_text(
            "SPACE / ENTER: DEPLOY SORTIE   •   V: TRAILER (PV)   •   ESC: QUIT",
            560, 32, MUTED, font_size=9, bold=True, anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY
        )

        # ── Draw 220px Navigation Rail ───────────────────────────────────────
        self.nav_rail.draw()

        # Transition Wipe
        TransitionOverlay.draw()

    def _activate(self, action: str) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        if action == "play":
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView())
        elif action == "arsenal":
            from game.views.ship_select_view import ShipSelectView
            transition_to(self.window, ShipSelectView())
        elif action == "map":
            from game.views.realm_map_view import RealmMapView
            transition_to(self.window, RealmMapView())
        elif action == "endless":
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView())
        elif action == "multiplayer":
            from game.views.multiplayer_view import MultiplayerView
            transition_to(self.window, MultiplayerView(return_view=self))
        elif action == "leaderboard":
            from game.views.leaderboard_view import LeaderboardView
            transition_to(self.window, LeaderboardView(return_view=self))
        elif action == "codex":
            from game.views.codex_view import CodexView
            transition_to(self.window, CodexView(return_view=self))
        elif action == "account":
            from game.views.account_view import AccountView
            transition_to(self.window, AccountView(return_view=self))
        elif action == "stats":
            from game.views.stats_view import StatsView
            transition_to(self.window, StatsView(return_view=self))
        elif action == "achievements":
            from game.views.achievements_view import AchievementsView
            transition_to(self.window, AchievementsView(return_view=self))
        elif action == "settings":
            from game.views.settings_view import SettingsView
            transition_to(self.window, SettingsView(return_view=self))
        elif action == "quit":
            arcade.exit()

    def _play_pv_video(self) -> None:
        import os, sys, subprocess
        from pathlib import Path
        pv_path = Path("vimana_wars_pv_final.mp4").resolve()
        if not pv_path.exists():
            return
        try:
            if sys.platform == "win32":
                os.startfile(str(pv_path))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(pv_path)])
            else:
                subprocess.Popen(["xdg-open", str(pv_path)])
        except Exception:
            pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)
        self._hovered_deploy = self._btn_deploy.contains(x, y)

        new_hovered_mode = -1
        for i, (btn, _) in enumerate(self._mode_buttons):
            if btn.contains(x, y):
                new_hovered_mode = i
                break
        if new_hovered_mode != self._hovered_mode and new_hovered_mode >= 0:
            self.sound_manager.play_ui_click(volume=0.20)
        self._hovered_mode = new_hovered_mode

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Check nav rail first
        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            return

        # Check primary deploy button
        if self._btn_deploy.contains(x, y):
            self._activate("play")
            return

        # Check mode buttons
        for btn, action in self._mode_buttons:
            if btn.contains(x, y):
                self._activate(action)
                return

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._activate("play")
        elif key in (arcade.key.H, arcade.key.R):
            self._activate("arsenal")
        elif key == arcade.key.M:
            self._activate("map")
        elif key == arcade.key.N:
            self._activate("multiplayer")
        elif key == arcade.key.L:
            self._activate("leaderboard")
        elif key == arcade.key.C:
            self._activate("codex")
        elif key == arcade.key.T:
            self._activate("stats")
        elif key == arcade.key.A:
            self._activate("achievements")
        elif key == arcade.key.O:
            self._activate("settings")
        elif key == arcade.key.P:
            self._activate("account")
        elif key == arcade.key.V:
            self._play_pv_video()
        elif key == arcade.key.ESCAPE:
            arcade.exit()
