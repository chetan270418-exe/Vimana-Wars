"""
game/views/boon_select_view.py
3-Card Roguelite Deva Blessing selection screen between waves.
Presented during wave transitions so the player can choose an astral upgrade.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE


class BoonSelectView(arcade.View):
    def __init__(self, game_view, choices: list[dict]):
        super().__init__()
        self.game_view = game_view
        self.choices = choices
        self._selected_card = 0
        self._pulse = 0.0

        # UI Text Objects
        self._title = arcade.Text(
            "BLESSING OF THE DEVAS",
            WIDTH // 2, HEIGHT - 70,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._sub = arcade.Text(
            "Choose a Divine Astral Boon to empower your Vimana",
            WIDTH // 2, HEIGHT - 110,
            COLOR_WAVE, font_size=14,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "1, 2, 3 or ← → : Select   •   ENTER / Click : Claim Boon",
            WIDTH // 2, 35,
            (160, 170, 200), font_size=12, bold=True,
            anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time

    def on_draw(self) -> None:
        self.clear()

        # Render frozen game view in the background with a dark overlay
        self._title.draw()
        self._sub.draw()

        card_w = 230
        card_h = 320
        start_x = WIDTH // 2 - 270
        spacing = 270
        cy = HEIGHT // 2 - 20

        for i, boon in enumerate(self.choices):
            cx = start_x + i * spacing
            is_sel = (i == self._selected_card)

            # Card Background
            bg_color = (25, 30, 55) if not is_sel else (35, 45, 80)
            arcade.draw_lrbt_rectangle_filled(
                cx - card_w // 2, cx + card_w // 2,
                cy - card_h // 2, cy + card_h // 2,
                bg_color
            )

            # Golden glowing card border
            border_col = boon["color"] if is_sel else (70, 80, 110)
            border_width = 3 if is_sel else 1
            arcade.draw_lrbt_rectangle_outline(
                cx - card_w // 2, cx + card_w // 2,
                cy - card_h // 2, cy + card_h // 2,
                border_col, border_width
            )

            # Card Header (God Name)
            arcade.draw_text(
                boon["deva"],
                cx, cy + 125,
                (200, 210, 240), font_size=9, bold=True, anchor_x="center"
            )

            # Boon Name
            arcade.draw_text(
                boon["name"],
                cx, cy + 90,
                boon["color"], font_size=13, bold=True, anchor_x="center"
            )

            # Card Decorative Emblem Box
            arcade.draw_circle_filled(cx, cy + 20, 36, (15, 20, 35))
            arcade.draw_circle_outline(cx, cy + 20, 36, boon["color"], 2)
            arcade.draw_text(
                f"[{i + 1}]",
                cx, cy + 12,
                COLOR_WHITE, font_size=18, bold=True, anchor_x="center"
            )

            # Boon Description Text (Wrapped)
            desc_lines = self._wrap_text(boon["desc"], 24)
            for l_idx, line in enumerate(desc_lines):
                arcade.draw_text(
                    line,
                    cx, cy - 45 - l_idx * 18,
                    (210, 215, 230), font_size=10, bold=True, anchor_x="center"
                )

            # Selection Tag
            if is_sel:
                pulse_val = int(200 + 55 * math.sin(self._pulse * 4))
                arcade.draw_text(
                    "★ PRESS ENTER TO CLAIM ★",
                    cx, cy - 135,
                    (255, 220, 50, pulse_val), font_size=9, bold=True, anchor_x="center"
                )

        self._hint.draw()

    def _wrap_text(self, text: str, max_chars: int) -> list[str]:
        words = text.split()
        lines = []
        cur = []
        cur_len = 0
        for w in words:
            if cur_len + len(w) + 1 > max_chars:
                lines.append(" ".join(cur))
                cur = [w]
                cur_len = len(w)
            else:
                cur.append(w)
                cur_len += len(w) + 1
        if cur:
            lines.append(" ".join(cur))
        return lines

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            self._selected_card = (self._selected_card - 1) % len(self.choices)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._selected_card = (self._selected_card + 1) % len(self.choices)
        elif key == arcade.key.KEY_1 and len(self.choices) >= 1:
            self._selected_card = 0
            self._claim_selected()
        elif key == arcade.key.KEY_2 and len(self.choices) >= 2:
            self._selected_card = 1
            self._claim_selected()
        elif key == arcade.key.KEY_3 and len(self.choices) >= 3:
            self._selected_card = 2
            self._claim_selected()
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._claim_selected()

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        card_w = 230
        card_h = 320
        start_x = WIDTH // 2 - 270
        spacing = 270
        cy = HEIGHT // 2 - 20

        for i in range(len(self.choices)):
            cx = start_x + i * spacing
            if cx - card_w // 2 <= x <= cx + card_w // 2 and cy - card_h // 2 <= y <= cy + card_h // 2:
                self._selected_card = i
                self._claim_selected()
                break

    def _claim_selected(self) -> None:
        chosen = self.choices[self._selected_card]
        self.game_view.apply_boon(chosen)
        self.window.show_view(self.game_view)
