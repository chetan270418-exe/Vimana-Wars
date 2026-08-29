"""
game/views/difficulty_view.py
Difficulty selection screen shown before the game starts.
Reads/writes via save_system so the choice persists between sessions.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system

_OPTIONS = ["easy", "normal", "hard"]
_DESCRIPTIONS = {
    "easy":   "More HP  ·  Less damage  ·  Fewer enemies",
    "normal": "The intended experience",
    "hard":   "Less HP  ·  More damage  ·  More enemies",
}
_COLORS = {
    "easy":   (60, 220, 100),
    "normal": (220, 200, 60),
    "hard":   (220, 60, 60),
}


class DifficultyView(arcade.View):
    def __init__(self):
        super().__init__()
        saved = save_system.load()
        self._selected = _OPTIONS.index(saved.get("difficulty", "normal"))
        self._pulse = 0.0

        # ── Static text ──────────────────────────────────────────────
        self._title = arcade.Text(
            "SELECT DIFFICULTY",
            WIDTH // 2, int(HEIGHT * 0.80),
            COLOR_WAVE, font_size=28, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._option_texts = [
            arcade.Text(
                opt.upper(),
                WIDTH // 2, int(HEIGHT * 0.60) - i * 70,
                _COLORS[opt], font_size=22, bold=True,
                anchor_x="center", anchor_y="center",
            )
            for i, opt in enumerate(_OPTIONS)
        ]
        self._desc_texts = [
            arcade.Text(
                _DESCRIPTIONS[opt],
                WIDTH // 2, int(HEIGHT * 0.60) - i * 70 - 24,
                (160, 160, 180), font_size=10,
                anchor_x="center", anchor_y="center",
            )
            for i, opt in enumerate(_OPTIONS)
        ]
        self._hint = arcade.Text(
            "↑ ↓ to choose   ENTER to confirm   ESC to go back",
            WIDTH // 2, int(HEIGHT * 0.10),
            (130, 130, 160), font_size=11,
            anchor_x="center",
        )
        # Cursor arrow (updated in draw)
        self._cursor = arcade.Text(
            "▶", 0, 0,
            COLOR_WHITE, font_size=22, bold=True,
            anchor_x="right", anchor_y="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time

    def on_draw(self) -> None:
        self.clear()

        self._title.draw()

        for i, (opt, txt, desc) in enumerate(
            zip(_OPTIONS, self._option_texts, self._desc_texts)
        ):
            # Highlight the selected option
            if i == self._selected:
                pulse = 0.85 + 0.15 * math.sin(self._pulse * 4)
                r, g, b = _COLORS[opt]
                txt.color = (int(r * pulse), int(g * pulse), int(b * pulse))

                # Draw selection box
                cy = int(HEIGHT * 0.60) - i * 70
                arcade.draw_lrbt_rectangle_outline(
                    WIDTH // 2 - 200, WIDTH // 2 + 200,
                    cy - 32, cy + 32,
                    (*_COLORS[opt], 180), 2,
                )
                # Cursor
                self._cursor.x = WIDTH // 2 - 210
                self._cursor.y = cy
                self._cursor.draw()
            else:
                r, g, b = _COLORS[opt]
                txt.color = (r // 2, g // 2, b // 2)   # dimmed when not selected

            txt.draw()
            desc.draw()

        self._hint.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._selected = (self._selected - 1) % len(_OPTIONS)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected = (self._selected + 1) % len(_OPTIONS)
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            chosen = _OPTIONS[self._selected]
            save_system.set_difficulty(chosen)
            from game.views.ship_select_view import ShipSelectView
            self.window.show_view(ShipSelectView(difficulty=chosen))
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            self.window.show_view(MenuView())

