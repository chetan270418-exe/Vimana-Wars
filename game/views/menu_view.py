"""
Vimana Wars main menu with mouse/controller-friendly navigation.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_WAVE, COLOR_SCORE, COLOR_WHITE
from game.entities.ship_classes import SHIP_CLASSES
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, GOLD, GOLD_BRIGHT, CYAN, CYAN_BRIGHT,
    PARCHMENT, MUTED, draw_chamfered_panel, draw_corner_etching,
    draw_segmented_bar,
)


_RNG = random.Random(42)
_STARS = [
    (_RNG.randint(0, WIDTH), _RNG.randint(0, HEIGHT),
     _RNG.uniform(0.5, 1.7), _RNG.randint(80, 200), _RNG.uniform(0.4, 1.4))
    for _ in range(140)
]


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        self._hovered = -1
        self.sound_manager = SoundManager()

        saved = save_system.load()
        high_score = saved.get("high_score", 0)
        last_diff = saved.get("difficulty", "normal").upper()
        last_ship = saved.get("last_ship", "pushpaka")
        last_ship_data = SHIP_CLASSES.get(last_ship, SHIP_CLASSES["pushpaka"])
        self._last_ship_id = last_ship
        last_wave = max(0, int(saved.get("last_wave", 0)))
        unlocked = sum(1 for start in (1, 4, 7, 10, 13, 16, 19) if last_wave >= start)
        unlocked = max(1, unlocked)
        self._unlocked_realms = unlocked

        self._title = arcade.Text(
            "VIMANA WARS", 274, 558,
            GOLD_BRIGHT, font_size=28, bold=True,
            anchor_x="left", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "CELESTIAL WAR COMMAND CONSOLE", 255, 485,
            CYAN_BRIGHT, font_size=12, bold=True,
            anchor_x="left", anchor_y="center",
        )
        self._high_score = arcade.Text(
            f"LOCAL BEST  {high_score:,}   •   LAST MODE  {last_diff}",
            255, 455, (160, 220, 160), font_size=10, bold=True,
            anchor_x="left", anchor_y="center",
        )
        self._progress = arcade.Text(
            f"CAMPAIGN PROGRESS   {unlocked}/7 REALMS UNLOCKED",
            255, 432, PARCHMENT, font_size=10, bold=True,
            anchor_x="left", anchor_y="center",
        )
        self._ship_label = arcade.Text(
            f"LAST VIMANA  •  {last_ship_data['name']}",
            744, 110, last_ship_data["color"], font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "MOUSE / D-PAD: NAVIGATE   •   ENTER: CONFIRM   •   ESC: QUIT",
            560, 28, MUTED, font_size=9,
            anchor_x="center", anchor_y="center",
        )
        self._version = arcade.Text(
            "VIMANA WARS // ASTRAL SYNC ONLINE", WIDTH - 12, 570,
            (120, 130, 150), font_size=8, bold=True, anchor_x="right",
        )
        self._section = arcade.Text(
            "MISSION CONTROL", 255, 520, GOLD, font_size=9, bold=True,
            anchor_x="left", anchor_y="center",
        )
        self._vitals = arcade.Text(
            "VIMANA VITALS", 24, 535, GOLD_BRIGHT, font_size=10, bold=True,
            anchor_x="left", anchor_y="center",
        )
        account_label = saved.get("game_id")
        sync_text = f"ACCOUNT LINKED\n{account_label}" if account_label else "GUEST MODE\nOFFLINE"
        self._sync = arcade.Text(
            sync_text, 820, 557, CYAN_BRIGHT if account_label else MUTED, font_size=8,
            bold=True, anchor_x="right", anchor_y="center",
        )

        button_x = 108
        button_y = 405
        button_gap = 39
        button_data = [
            ("PLAY", "play", COLOR_SCORE),
            ("CAMPAIGN MAP", "map", (120, 210, 255)),
            ("LEADERBOARDS", "leaderboard", (170, 130, 255)),
            ("LIFETIME STATS", "stats", (255, 200, 100)),
            ("ACHIEVEMENTS", "achievements", (255, 170, 80)),
            ("CODEX", "codex", (100, 240, 190)),
            ("ACCOUNT", "account", (116, 245, 255)),
            ("SETTINGS", "settings", (190, 200, 220)),
            ("QUIT", "quit", (255, 90, 100)),
        ]
        self._buttons = [
            (MenuButton(label, button_x, button_y - i * button_gap, 190, 32, color), action)
            for i, (label, action, color) in enumerate(button_data)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        SoundManager.stop_music()
        saved = save_system.load()
        game_id = saved.get("game_id")
        self._sync.text = f"ACCOUNT LINKED\n{game_id}" if game_id else "GUEST MODE\nOFFLINE"
        self._sync.color = CYAN_BRIGHT if game_id else MUTED
        self._high_score.text = (
            f"LOCAL BEST  {saved.get('high_score', 0):,}   •   LAST MODE  "
            f"{saved.get('difficulty', 'normal').upper()}"
        )

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        for i, (button, _) in enumerate(self._buttons):
            button.update(delta_time, i == self._hovered)

    def on_draw(self) -> None:
        self.clear()

        # Stitch-inspired command rail and holographic content frame.
        arcade.draw_lrbt_rectangle_filled(0, 220, 0, HEIGHT, (14, 16, 22, 255))
        arcade.draw_line(220, 0, 220, HEIGHT, (233, 196, 0, 75), 1)
        arcade.draw_line(220, 548, WIDTH, 548, (233, 196, 0, 80), 1)

        # Slow parallax drift keeps the menu alive without distracting from controls.
        for sx, sy, radius, base, speed in _STARS:
            x = 220 + ((sx + self._pulse * speed * 5.0) % (WIDTH - 220))
            y = (sy + self._pulse * speed * 1.5) % HEIGHT
            brightness = int(base + 18 * math.sin(self._pulse * 0.8 + sx * 0.01))
            arcade.draw_circle_filled(x, y, radius, (brightness, brightness, min(255, brightness + 15)))

        # Hero illustration from the supplied Stitch mockup, with a dark glass
        # scrim so menu text remains readable on every monitor.
        hero = AssetManager.texture("hero_vimana_wars.png")
        AssetManager.draw(hero, 570, 315, 620, 414, color=(255, 255, 255, 100))
        draw_chamfered_panel(235, 880, 145, 475, CYAN, fill=(9, 14, 25), alpha=145, cut=14)
        draw_corner_etching(235, 880, 145, 475, GOLD, length=18, alpha=120)

        # Subtle rotating celestial rings behind the hero.
        ring_angle = self._pulse * 12.0
        for radius, alpha in ((125, 24), (155, 14)):
            arcade.draw_arc_outline(570, 315, radius * 2, radius * 0.55,
                                    (100, 180, 255, alpha), ring_angle, ring_angle + 250, 2)

        self._title.draw()
        self._subtitle.draw()
        self._section.draw()
        self._sync.draw()
        logo = AssetManager.texture("vimana_wars_logo.png")
        AssetManager.draw(logo, 245, 558, 34, 34)

        # Vitals rail.
        self._vitals.draw()
        arcade.draw_text("PRANA", 24, 505, CYAN_BRIGHT, font_size=8, bold=True)
        arcade.draw_text("108/108", 194, 505, PARCHMENT, font_size=8, bold=True, anchor_x="right")
        draw_segmented_bar(24, 194, 493, 499, 1.0, CYAN, segments=8, gap=3)
        arcade.draw_text("MANTRA", 24, 466, GOLD, font_size=8, bold=True)
        arcade.draw_text(f"{min(100, self._unlocked_realms * 14)}%", 194, 466, PARCHMENT, font_size=8, bold=True, anchor_x="right")
        draw_segmented_bar(24, 194, 454, 460, min(1.0, self._unlocked_realms / 7), GOLD, segments=8, gap=3)

        self._high_score.draw()
        self._progress.draw()

        # Last ship mini-preview.
        ship_data = SHIP_CLASSES.get(self._last_ship_id, SHIP_CLASSES["pushpaka"])
        last_texture = AssetManager.texture(ship_data.get("sprite", "pushpaka.png"))
        if not AssetManager.draw(last_texture, 744, 155, 74, 74):
            arcade.draw_triangle_filled(744, 185, 724, 145, 764, 145, ship_data["color"])
            arcade.draw_circle_filled(744, 154, 5, ship_data["accent"])
        self._ship_label.draw()

        for button, _ in self._buttons:
            button.draw()
        self._hint.draw()
        self._version.draw()
        TransitionOverlay.draw()

    def _activate(self, action: str) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()
        if action == "play":
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView())
        elif action == "map":
            from game.views.realm_map_view import RealmMapView
            transition_to(self.window, RealmMapView())
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

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        new_hovered = -1
        for i, (button, _) in enumerate(self._buttons):
            if button.contains(x, y):
                new_hovered = i
                break
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.22)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        for i, (menu_button, action) in enumerate(self._buttons):
            if menu_button.contains(x, y):
                self._hovered = i
                self._activate(action)
                return

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._hovered = (self._hovered - 1) % len(self._buttons)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._hovered = (self._hovered + 1) % len(self._buttons)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            index = self._hovered if self._hovered >= 0 else 0
            self._activate(self._buttons[index][1])
        elif key == arcade.key.M:
            self._activate("map")
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
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y > 0:
            self._hovered = (self._hovered - 1) % len(self._buttons)
            self.sound_manager.play_ui_click(volume=0.22)
        elif hat_y < 0:
            self._hovered = (self._hovered + 1) % len(self._buttons)
            self.sound_manager.play_ui_click(volume=0.22)
