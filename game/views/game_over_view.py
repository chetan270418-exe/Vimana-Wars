"""
game/views/game_over_view.py
Game-over screen — shows stats, high score, and difficulty played.
Uses arcade.Text objects (no draw_text calls).
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system


class GameOverView(arcade.View):
    def __init__(self, score: int, wave: int, kills: int,
                 highest_combo: int, high_score: int = 0, difficulty: str = "normal"):
        super().__init__()
        self._pulse = 0.0
        self.difficulty = difficulty
        is_new_record = score >= high_score and score > 0

        # ── Title ────────────────────────────────────────────────────
        self._title = arcade.Text(
            "GAME OVER",
            WIDTH // 2, int(HEIGHT * 0.82),
            (220, 30, 30), font_size=52, bold=True,
            anchor_x="center", anchor_y="center",
        )

        # ── New record banner ────────────────────────────────────────
        self._record_banner = arcade.Text(
            "★  NEW HIGH SCORE  ★" if is_new_record else "",
            WIDTH // 2, int(HEIGHT * 0.72),
            (255, 220, 50), font_size=14, bold=True,
            anchor_x="center", anchor_y="center",
        )

        # ── Stats table ──────────────────────────────────────────────
        diff_colors = {"easy": (60, 220, 100), "normal": (220, 200, 60), "hard": (220, 60, 60)}
        stats = [
            ("SCORE",          f"{score:,}",         COLOR_SCORE),
            ("HIGH SCORE",     f"{high_score:,}",    (200, 200, 200)),
            ("DIFFICULTY",     difficulty.upper(),   diff_colors.get(difficulty, COLOR_WHITE)),
            ("WAVES SURVIVED", f"{wave}",            COLOR_WHITE),
            ("ENEMIES SLAIN",  f"{kills}",           COLOR_WHITE),
            ("HIGHEST COMBO",  f"×{highest_combo}",  COLOR_WHITE),
        ]
        self._stat_labels = []
        self._stat_values = []
        for i, (label, value, val_color) in enumerate(stats):
            y = int(HEIGHT * 0.60) - i * 30
            self._stat_labels.append(arcade.Text(
                label, WIDTH // 2 - 140, y,
                (140, 140, 170), font_size=12,
            ))
            self._stat_values.append(arcade.Text(
                value, WIDTH // 2 + 140, y,
                val_color, font_size=13, bold=True,
                anchor_x="right",
            ))

        # ── Prompt ───────────────────────────────────────────────────
        self._prompt = arcade.Text(
            "R — Quick Restart   •   L — Leaderboard   •   ESC — Main Menu",
            WIDTH // 2, int(HEIGHT * 0.08),
            COLOR_WHITE, font_size=13, bold=True,
            anchor_x="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color((10, 0, 5))
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time
        alpha = max(0, min(255, int(200 + 55 * math.sin(self._pulse * 2.5))))
        self._prompt.color = (*COLOR_WHITE, alpha)

    def on_draw(self) -> None:
        self.clear()
        self._title.draw()
        self._record_banner.draw()
        for lbl, val in zip(self._stat_labels, self._stat_values):
            lbl.draw()
            val.draw()
        self._prompt.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.R:
            from game.views.game_view import GameView
            self.window.show_view(GameView(difficulty=self.difficulty))
        elif key == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            self.window.show_view(LeaderboardView(return_view=self))
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())
