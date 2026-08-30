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
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay


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

        self._title = arcade.Text(
            "VIMANA WARS", WIDTH // 2, 515,
            COLOR_SCORE, font_size=52, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "Defend the Realm — Defeat the Asuras", WIDTH // 2, 477,
            COLOR_WAVE, font_size=15,
            anchor_x="center", anchor_y="center",
        )
        self._high_score = arcade.Text(
            f"LOCAL BEST  {high_score:,}   •   LAST MODE  {last_diff}",
            245, 410, (160, 220, 160), font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._progress = arcade.Text(
            f"CAMPAIGN PROGRESS   {unlocked}/7 REALMS UNLOCKED",
            245, 382, (190, 200, 230), font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._ship_label = arcade.Text(
            f"LAST VIMANA  •  {last_ship_data['name']}",
            245, 265, last_ship_data["color"], font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "Mouse / D-pad: Navigate   •   ENTER: Confirm   •   ESC: Quit",
            WIDTH // 2, 28, (130, 145, 180), font_size=10,
            anchor_x="center", anchor_y="center",
        )
        self._version = arcade.Text(
            "v0.5 Celestial Frontend", WIDTH - 10, 8,
            (90, 100, 130), font_size=9, anchor_x="right",
        )

        button_x = 690
        button_y = 400
        button_gap = 45
        button_data = [
            ("PLAY", "play", COLOR_SCORE),
            ("CAMPAIGN MAP", "map", (120, 210, 255)),
            ("LEADERBOARDS", "leaderboard", (170, 130, 255)),
            ("LIFETIME STATS", "stats", (255, 200, 100)),
            ("ACHIEVEMENTS", "achievements", (255, 170, 80)),
            ("CODEX", "codex", (100, 240, 190)),
            ("SETTINGS", "settings", (190, 200, 220)),
            ("QUIT", "quit", (255, 90, 100)),
        ]
        self._buttons = [
            (MenuButton(label, button_x, button_y - i * button_gap, 300, 38, color), action)
            for i, (label, action, color) in enumerate(button_data)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        for i, (button, _) in enumerate(self._buttons):
            button.update(delta_time, i == self._hovered)

    def on_draw(self) -> None:
        self.clear()

        # Slow parallax drift keeps the menu alive without distracting from controls.
        for sx, sy, radius, base, speed in _STARS:
            x = (sx + self._pulse * speed * 5.0) % WIDTH
            y = (sy + self._pulse * speed * 1.5) % HEIGHT
            brightness = int(base + 18 * math.sin(self._pulse * 0.8 + sx * 0.01))
            arcade.draw_circle_filled(x, y, radius, (brightness, brightness, min(255, brightness + 15)))

        # Subtle rotating celestial rings behind the title.
        ring_angle = self._pulse * 12.0
        for radius, alpha in ((125, 24), (155, 14)):
            arcade.draw_arc_outline(WIDTH // 2, 500, radius * 2, radius * 0.55,
                                    (100, 180, 255, alpha), ring_angle, ring_angle + 250, 2)

        self._title.draw()
        self._subtitle.draw()

        arcade.draw_lrbt_rectangle_filled(70, 420, 330, 445, (12, 18, 42, 210))
        arcade.draw_lrbt_rectangle_outline(70, 420, 330, 445, (55, 85, 135, 180), 1)
        self._high_score.draw()
        self._progress.draw()

        # Last ship mini-preview.
        ship_data = SHIP_CLASSES.get(self._last_ship_id, SHIP_CLASSES["pushpaka"])
        arcade.draw_triangle_filled(245, 315, 225, 275, 265, 275, ship_data["color"])
        arcade.draw_circle_filled(245, 284, 5, ship_data["accent"])
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
        elif key == arcade.key.ESCAPE:
            arcade.exit()

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y > 0:
            self._hovered = (self._hovered - 1) % len(self._buttons)
            self.sound_manager.play_ui_click(volume=0.22)
        elif hat_y < 0:
            self._hovered = (self._hovered + 1) % len(self._buttons)
            self.sound_manager.play_ui_click(volume=0.22)
