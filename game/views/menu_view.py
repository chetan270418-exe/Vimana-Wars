"""
game/views/menu_view.py
Main menu — uses arcade.Text objects (no draw_text calls).
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_WAVE, COLOR_SCORE, COLOR_WHITE
from game.systems import save_system

# Static star field — seeded so it never changes
_RNG = random.Random(42)
_STARS = [
    (_RNG.randint(0, WIDTH), _RNG.randint(0, HEIGHT),
     _RNG.uniform(0.5, 1.5), _RNG.randint(80, 200))
    for _ in range(120)
]


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        saved = save_system.load()
        high_score = saved.get("high_score", 0)
        last_diff  = saved.get("difficulty", "normal").upper()

        # ── Static text objects ──────────────────────────────────────
        self._title = arcade.Text(
            "VIMANA WARS",
            WIDTH // 2, int(HEIGHT * 0.67),
            COLOR_SCORE, font_size=52, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "Defend the Realm — Defeat the Asuras",
            WIDTH // 2, int(HEIGHT * 0.57),
            COLOR_WAVE, font_size=16,
            anchor_x="center", anchor_y="center",
        )
        self._prompt = arcade.Text(
            "Press  ENTER  to Play",
            WIDTH // 2, int(HEIGHT * 0.43),
            COLOR_WHITE, font_size=18, bold=True,
            anchor_x="center", anchor_y="center",
        )
        # High score line
        hs_text = f"Local Best: {high_score:,}  [{last_diff}]" if high_score > 0 else ""
        self._high_score = arcade.Text(
            hs_text,
            WIDTH // 2, int(HEIGHT * 0.36),
            (160, 220, 160), font_size=12,
            anchor_x="center",
        )
        ctrl_lines = [
            "WASD / Arrows — Move    •    Mouse Aim + Hold LMB — Shoot",
            "SPACE — Vayu Dash    •    Q — Sudarshana Chakram    •    F — Bomb",
            "L — Leaderboards    •    C — Lore Codex    •    O — Settings",
        ]
        self._ctrl_texts = [
            arcade.Text(
                line, WIDTH // 2, int(HEIGHT * 0.25) - i * 22,
                (160, 170, 200) if i < 2 else (255, 215, 100),
                font_size=11, bold=(i == 2),
                anchor_x="center",
            )
            for i, line in enumerate(ctrl_lines)
        ]
        self._version = arcade.Text(
            "v0.4 Celestial Master Edition", WIDTH - 8, 8,
            (90, 100, 130), font_size=9,
            anchor_x="right",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time
        alpha = max(0, min(255, int(200 + 55 * math.sin(self._pulse * 2.5))))
        self._prompt.color = (*COLOR_WHITE, alpha)

    def on_draw(self) -> None:
        self.clear()
        for sx, sy, sr, sbr in _STARS:
            arcade.draw_circle_filled(sx, sy, sr, (sbr, sbr, sbr))
        self._title.draw()
        self._subtitle.draw()
        self._prompt.draw()
        self._high_score.draw()
        for t in self._ctrl_texts:
            t.draw()
        self._version.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.ENTER, arcade.key.RETURN):
            from game.views.difficulty_view import DifficultyView
            self.window.show_view(DifficultyView())
        elif key == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            self.window.show_view(LeaderboardView(return_view=self))
        elif key == arcade.key.C:
            from game.views.codex_view import CodexView
            self.window.show_view(CodexView(return_view=self))
        elif key == arcade.key.O:
            from game.views.settings_view import SettingsView
            self.window.show_view(SettingsView(return_view=self))
        elif key == arcade.key.ESCAPE:
            arcade.exit()

