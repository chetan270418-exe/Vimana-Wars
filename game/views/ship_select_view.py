"""
game/views/ship_select_view.py
Vimana Flagship Selection Screen shown before entering battle.
Displays detailed stats, vector preview, and unique ship class descriptions.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE
from game.entities.ship_classes import SHIP_CLASSES
from game.ui.transitions import transition_to, TransitionOverlay


_SHIPS = ["pushpaka", "tripura", "garuda"]


class ShipSelectView(arcade.View):
    def __init__(self, difficulty: str = "normal"):
        super().__init__()
        self.difficulty = difficulty
        self._selected = 0
        self._pulse = 0.0

        # UI Texts
        self._title = arcade.Text(
            "SELECT YOUR VIMANA",
            WIDTH // 2, HEIGHT - 65,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "← → or A / D : Select   •   ENTER / SPACE : Launch Vimana   •   ESC : Back",
            WIDTH // 2, 35,
            (160, 170, 200), font_size=12, bold=True,
            anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time

    def on_draw(self) -> None:
        self.clear()

        self._title.draw()

        card_w = 250
        card_h = 390
        start_x = WIDTH // 2 - 280
        spacing = 280
        cy = HEIGHT // 2 - 15

        for i, ship_id in enumerate(_SHIPS):
            sdata = SHIP_CLASSES[ship_id]
            cx = start_x + i * spacing
            is_sel = (i == self._selected)

            # Card Background
            bg_col = (28, 32, 60) if not is_sel else (38, 48, 88)
            arcade.draw_lrbt_rectangle_filled(
                cx - card_w // 2, cx + card_w // 2,
                cy - card_h // 2, cy + card_h // 2,
                bg_col
            )

            # Border
            border_col = sdata["accent"] if is_sel else (70, 80, 110)
            border_w = 3 if is_sel else 1
            arcade.draw_lrbt_rectangle_outline(
                cx - card_w // 2, cx + card_w // 2,
                cy - card_h // 2, cy + card_h // 2,
                border_col, border_w
            )

            # Ship Title
            arcade.draw_text(
                sdata["name"],
                cx, cy + 160,
                sdata["color"], font_size=15, bold=True, anchor_x="center"
            )
            arcade.draw_text(
                sdata["subtitle"],
                cx, cy + 140,
                (170, 180, 210), font_size=9, bold=True, anchor_x="center"
            )

            # Vector Ship Preview
            preview_y = cy + 75
            self._draw_ship_preview(cx, preview_y, ship_id, sdata["color"], sdata["accent"])

            # Stat Bars
            self._draw_stat_bar("ARMOR / HP", sdata["hp"] / 160.0, cx, cy - 5, (220, 60, 60))
            self._draw_stat_bar("SPEED", sdata["speed"] / 7.0, cx, cy - 35, (60, 220, 100))
            self._draw_stat_bar("FIREPOWER", sdata["bullet_damage"] / 50.0, cx, cy - 65, (255, 200, 50))

            # Description (Wrapped)
            desc_lines = self._wrap_text(sdata["desc"], 27)
            for l_idx, line in enumerate(desc_lines):
                arcade.draw_text(
                    line,
                    cx, cy - 110 - l_idx * 16,
                    (200, 205, 220), font_size=9, anchor_x="center"
                )

            # Ready indicator
            if is_sel:
                pulse_val = int(200 + 55 * math.sin(self._pulse * 4))
                arcade.draw_text(
                    "▶ READY FOR LAUNCH ◀",
                    cx, cy - 170,
                    (255, 220, 50, pulse_val), font_size=10, bold=True, anchor_x="center"
                )

        self._hint.draw()
        TransitionOverlay.draw()

    def _draw_stat_bar(self, label: str, frac: float, cx: float, cy: float, col: tuple) -> None:
        arcade.draw_text(label, cx - 100, cy, (160, 170, 190), font_size=8, bold=True)
        bar_w = 90
        arcade.draw_lrbt_rectangle_filled(cx + 10, cx + 10 + bar_w, cy - 1, cy + 7, (20, 20, 35))
        arcade.draw_lrbt_rectangle_filled(cx + 10, cx + 10 + bar_w * min(1.0, frac), cy - 1, cy + 7, col)
        arcade.draw_lrbt_rectangle_outline(cx + 10, cx + 10 + bar_w, cy - 1, cy + 7, (80, 90, 110), 1)

    def _draw_ship_preview(self, cx: float, cy: float, ship_id: str, col: tuple, acc: tuple) -> None:
        r = 24
        # Draw rotating/hovering ship preview
        tilt = math.sin(self._pulse * 2.5) * 5.0
        angle_rad = math.radians(90 + tilt)

        tip_x = cx + math.cos(angle_rad) * r * 1.8
        tip_y = cy + math.sin(angle_rad) * r * 1.8

        if ship_id == "tripura":
            # Bulky Fortress Shape
            w_l_x = cx + math.cos(angle_rad + 2.4) * r * 1.5
            w_l_y = cy + math.sin(angle_rad + 2.4) * r * 1.5
            w_r_x = cx + math.cos(angle_rad - 2.4) * r * 1.5
            w_r_y = cy + math.sin(angle_rad - 2.4) * r * 1.5
            arcade.draw_triangle_filled(tip_x, tip_y, w_l_x, w_l_y, w_r_x, w_r_y, col)
            arcade.draw_circle_filled(cx, cy - 4, 14, acc)
        elif ship_id == "garuda":
            # Sharp Needle Interceptor
            w_l_x = cx + math.cos(angle_rad + 2.6) * r * 1.4
            w_l_y = cy + math.sin(angle_rad + 2.6) * r * 1.4
            w_r_x = cx + math.cos(angle_rad - 2.6) * r * 1.4
            w_r_y = cy + math.sin(angle_rad - 2.6) * r * 1.4
            arcade.draw_triangle_filled(tip_x, tip_y, w_l_x, w_l_y, w_r_x, w_r_y, col)
            arcade.draw_line(tip_x, tip_y, w_l_x, w_l_y, acc, 2)
            arcade.draw_line(tip_x, tip_y, w_r_x, w_r_y, acc, 2)
        else:
            # Pushpaka Celestial Cruiser
            w_l_x = cx + math.cos(angle_rad + 2.5) * r * 1.3
            w_l_y = cy + math.sin(angle_rad + 2.5) * r * 1.3
            w_r_x = cx + math.cos(angle_rad - 2.5) * r * 1.3
            w_r_y = cy + math.sin(angle_rad - 2.5) * r * 1.3
            arcade.draw_triangle_filled(tip_x, tip_y, w_l_x, w_l_y, w_r_x, w_r_y, col)
            arcade.draw_circle_filled(cx, cy + 2, 5, (100, 240, 255))

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
            self._selected = (self._selected - 1) % len(_SHIPS)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._selected = (self._selected + 1) % len(_SHIPS)
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            chosen_ship = _SHIPS[self._selected]
            is_endless = (self.difficulty == "endless")
            eff_diff = "normal" if is_endless else self.difficulty
            from game.views.game_view import GameView
            self.window.show_view(GameView(difficulty=eff_diff, ship_class=chosen_ship, is_endless=is_endless))
        elif key == arcade.key.ESCAPE:
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView())
