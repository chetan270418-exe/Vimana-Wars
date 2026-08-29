"""
game/views/victory_view.py
Shown when the player defeats Ravana (boss wave cleared).
Celebrates with animated gold particles and a stats summary.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system


class VictoryView(arcade.View):
    def __init__(self, score: int, kills: int, highest_combo: int,
                 difficulty: str = "normal"):
        super().__init__()
        self._pulse = 0.0
        self._particles: list[dict] = []
        self._spawn_timer = 0.0

        # Save results
        updated = save_system.update_after_game(
            score=score, wave=10, kills=kills
        )
        is_record = score >= updated["high_score"] and score > 0

        # ── Text objects ─────────────────────────────────────────────
        self._title = arcade.Text(
            "VICTORY!",
            WIDTH // 2, int(HEIGHT * 0.80),
            (255, 210, 30), font_size=60, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._sub = arcade.Text(
            "Ravana has been defeated. The realm is safe.",
            WIDTH // 2, int(HEIGHT * 0.69),
            (200, 180, 100), font_size=14,
            anchor_x="center", anchor_y="center",
        )
        self._record = arcade.Text(
            "★  NEW HIGH SCORE  ★" if is_record else "",
            WIDTH // 2, int(HEIGHT * 0.61),
            (255, 230, 60), font_size=13, bold=True,
            anchor_x="center", anchor_y="center",
        )

        diff_colors = {
            "easy":   (60, 220, 100),
            "normal": (220, 200, 60),
            "hard":   (220, 60, 60),
        }
        stats = [
            ("FINAL SCORE",   f"{score:,}",          COLOR_SCORE),
            ("HIGH SCORE",    f"{updated['high_score']:,}", (200, 200, 200)),
            ("DIFFICULTY",    difficulty.upper(),     diff_colors.get(difficulty, COLOR_WHITE)),
            ("ENEMIES SLAIN", f"{kills}",             COLOR_WHITE),
            ("HIGHEST COMBO", f"×{highest_combo}",   COLOR_WHITE),
        ]
        self._stat_labels = []
        self._stat_values = []
        for i, (label, value, vc) in enumerate(stats):
            y = int(HEIGHT * 0.54) - i * 30
            self._stat_labels.append(arcade.Text(
                label, WIDTH // 2 - 140, y,
                (140, 140, 170), font_size=12,
            ))
            self._stat_values.append(arcade.Text(
                value, WIDTH // 2 + 140, y,
                vc, font_size=13, bold=True, anchor_x="right",
            ))

        self._prompt = arcade.Text(
            "ENTER — Play Again   •   L — Leaderboard   •   ESC — Main Menu",
            WIDTH // 2, int(HEIGHT * 0.07),
            COLOR_WHITE, font_size=13, bold=True,
            anchor_x="center",
        )

    # ── Lifecycle ───────────────────────────────────────────────────────

    def on_show_view(self) -> None:
        arcade.set_background_color((5, 8, 20))
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time

        # Pulsing prompt
        alpha = max(0, min(255, int(200 + 55 * math.sin(self._pulse * 2.5))))
        self._prompt.color = (*COLOR_WHITE, alpha)

        # Spawn gold celebration particles
        self._spawn_timer -= delta_time
        if self._spawn_timer <= 0:
            self._spawn_timer = 0.05
            for _ in range(3):
                self._particles.append({
                    "x":     random.uniform(0, WIDTH),
                    "y":     random.uniform(HEIGHT * 0.5, HEIGHT * 1.1),
                    "vx":    random.uniform(-30, 30),
                    "vy":    random.uniform(40, 120),
                    "life":  random.uniform(1.5, 3.0),
                    "max_life": 3.0,
                    "r":    random.uniform(2, 5),
                    "color": random.choice([
                        (255, 210, 30),   # gold
                        (255, 160, 20),   # amber
                        (255, 255, 180),  # pale gold
                        (100, 220, 255),  # cyan accent
                    ]),
                })

        # Update particles
        for p in self._particles:
            p["x"]    += p["vx"]  * delta_time
            p["y"]    += p["vy"]  * delta_time
            p["vy"]   -= 60 * delta_time   # gravity
            p["life"] -= delta_time

        # Prune dead particles
        self._particles = [p for p in self._particles if p["life"] > 0]

    def on_draw(self) -> None:
        self.clear()

        # Draw particles
        for p in self._particles:
            frac = max(0.0, p["life"] / p["max_life"])
            alpha = int(255 * frac)
            r, g, b = p["color"]
            arcade.draw_circle_filled(p["x"], p["y"], p["r"] * frac, (r, g, b, alpha))

        # Glow behind title
        for radius in range(80, 10, -12):
            alpha = int(18 * (1 - radius / 80))
            arcade.draw_circle_filled(
                WIDTH // 2, int(HEIGHT * 0.80),
                radius, (255, 200, 30, alpha)
            )

        self._title.draw()
        self._sub.draw()
        self._record.draw()

        for lbl, val in zip(self._stat_labels, self._stat_values):
            lbl.draw()
            val.draw()

        self._prompt.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.ENTER, arcade.key.RETURN):
            from game.views.difficulty_view import DifficultyView
            self.window.show_view(DifficultyView())
        elif key == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            self.window.show_view(LeaderboardView(return_view=self))
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())
