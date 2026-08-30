"""
game/views/ship_select_view.py
Vimana Flagship Selection Screen shown before entering battle.
Displays detailed stats, vector preview, and unique ship class descriptions.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE
from game.entities.ship_classes import SHIP_CLASSES
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.ui.transitions import transition_to, TransitionOverlay


_SHIPS = list(SHIP_CLASSES.keys())
_PAGE_SIZE = 3


class ShipSelectView(arcade.View):
    def __init__(self, difficulty: str = "normal", start_wave: int = 1,
                 realm_id: int | None = None):
        super().__init__()
        self.difficulty = difficulty
        self.start_wave = max(1, int(start_wave))
        self.realm_id = realm_id
        saved = save_system.load()
        last_ship = saved.get("last_ship", "pushpaka")
        self._last_ship = last_ship
        self._last_wave = max(0, int(saved.get("last_wave", 0)))
        self._selected = _SHIPS.index(last_ship) if last_ship in _SHIPS and self._is_unlocked(last_ship) else 0
        self._hovered = -1
        self._pulse = 0.0
        self.sound_manager = SoundManager()

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

        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        visible_ships = _SHIPS[page_start:page_start + _PAGE_SIZE]
        arcade.draw_text(
            f"ARMORY PAGE {page_start // _PAGE_SIZE + 1}/{(len(_SHIPS) + _PAGE_SIZE - 1) // _PAGE_SIZE}",
            WIDTH // 2, HEIGHT - 95, (140, 155, 190), font_size=9,
            bold=True, anchor_x="center",
        )

        for local_i, ship_id in enumerate(visible_ships):
            i = page_start + local_i
            sdata = SHIP_CLASSES[ship_id]
            cx = start_x + local_i * spacing
            is_sel = (i == self._selected)
            is_hovered = (i == self._hovered)
            unlocked = self._is_unlocked(ship_id)

            # Card Background
            bg_col = ((34, 40, 72) if is_hovered and not is_sel else ((38, 48, 88) if is_sel else (28, 32, 60))) if unlocked else (18, 20, 32)
            arcade.draw_lrbt_rectangle_filled(
                cx - card_w // 2, cx + card_w // 2,
                cy - card_h // 2, cy + card_h // 2,
                bg_col
            )

            # Border
            border_col = sdata["accent"] if unlocked and (is_sel or is_hovered) else (70, 80, 110)
            border_w = 3 if is_sel else (2 if is_hovered else 1)
            arcade.draw_lrbt_rectangle_outline(
                cx - card_w // 2, cx + card_w // 2,
                cy - card_h // 2, cy + card_h // 2,
                border_col, border_w
            )

            # Ship Title
            arcade.draw_text(
                sdata["name"] if unlocked else "LOCKED VIMANA",
                cx, cy + 160,
                sdata["color"] if unlocked else (105, 110, 135), font_size=15, bold=True, anchor_x="center"
            )
            arcade.draw_text(
                sdata["subtitle"] if unlocked else f"Unlock at Wave {sdata['unlock_wave']}",
                cx, cy + 140,
                (170, 180, 210), font_size=9, bold=True, anchor_x="center"
            )
            if self._last_ship == ship_id and unlocked:
                arcade.draw_text(
                    "LAST USED", cx, cy + 120, (255, 220, 80),
                    font_size=8, bold=True, anchor_x="center",
                )

            # Vector Ship Preview
            preview_y = cy + 75
            if unlocked:
                self._draw_ship_preview(cx, preview_y, ship_id, sdata["color"], sdata["accent"])
            else:
                arcade.draw_text("🔒", cx, preview_y, (120, 125, 150), font_size=28,
                                 anchor_x="center", anchor_y="center")

            # Stat Bars
            self._draw_stat_bar("ARMOR / HP", sdata["hp"] / 160.0, cx, cy - 5, (220, 60, 60))
            self._draw_stat_bar("SPEED", sdata["speed"] / 7.0, cx, cy - 35, (60, 220, 100))
            self._draw_stat_bar("FIREPOWER", sdata["bullet_damage"] / 50.0, cx, cy - 65, (255, 200, 50))

            # Description (Wrapped)
            desc_lines = self._wrap_text(sdata["desc"], 27)
            for l_idx, line in enumerate(desc_lines if unlocked else ["Complete more campaign waves", "to unlock this warship."]):
                arcade.draw_text(
                    line,
                    cx, cy - 110 - l_idx * 16,
                    (200, 205, 220), font_size=9, anchor_x="center"
                )

            # Ready indicator
            if is_sel and unlocked:
                pulse_val = int(200 + 55 * math.sin(self._pulse * 4))
                arcade.draw_text(
                    "▶ READY FOR LAUNCH ◀",
                    cx, cy - 170,
                    (255, 220, 50, pulse_val), font_size=10, bold=True, anchor_x="center"
                )

        self._hint.draw()
        TransitionOverlay.draw()

    def _card_at(self, x: float, y: float) -> int:
        card_w = 250
        card_h = 390
        start_x = WIDTH // 2 - 280
        spacing = 280
        cy = HEIGHT // 2 - 15
        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        visible_ships = _SHIPS[page_start:page_start + _PAGE_SIZE]
        for local_i in range(len(visible_ships)):
            i = page_start + local_i
            cx = start_x + local_i * spacing
            if (cx - card_w / 2 <= x <= cx + card_w / 2
                    and cy - card_h / 2 <= y <= cy + card_h / 2):
                return i
        return -1

    def _is_unlocked(self, ship_id: str) -> bool:
        return self._last_wave >= SHIP_CLASSES[ship_id].get("unlock_wave", 1)

    def _select(self, index: int) -> None:
        if index < 0 or index >= len(_SHIPS):
            return
        if index != self._selected:
            self.sound_manager.play_ui_click(volume=0.35)
        self._selected = index

    def _confirm(self) -> None:
        if TransitionOverlay.is_active:
            return
        chosen_ship = _SHIPS[self._selected]
        if not self._is_unlocked(chosen_ship):
            self.sound_manager.play_ui_click(volume=0.25)
            return
        saved = save_system.load()
        saved["last_ship"] = chosen_ship
        self._last_ship = chosen_ship
        if self.realm_id is not None:
            saved["last_realm"] = self.realm_id
        save_system.save(saved)
        self.sound_manager.play_ui_click()
        is_endless = self.difficulty == "endless"
        eff_diff = "normal" if is_endless else self.difficulty
        from game.views.game_view import GameView
        transition_to(
            self.window,
            GameView(
                difficulty=eff_diff,
                ship_class=chosen_ship,
                is_endless=is_endless,
                start_wave=1 if is_endless else self.start_wave,
            ),
            style="wipe",
        )

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        new_hovered = self._card_at(x, y)
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.20)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        index = self._card_at(x, y)
        if index < 0:
            return
        if index == self._selected:
            self._confirm()
        else:
            self._select(index)

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

        if AssetManager.draw(AssetManager.texture(SHIP_CLASSES[ship_id].get("sprite", "pushpaka.png")),
                             cx, cy, 72, 72, angle=-tilt):
            return

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
            self._select((self._selected - 1) % len(_SHIPS))
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._select((self._selected + 1) % len(_SHIPS))
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._confirm()
        elif key == arcade.key.ESCAPE:
            from game.views.difficulty_view import DifficultyView
            transition_to(
                self.window,
                DifficultyView(start_wave=self.start_wave, realm_id=self.realm_id),
            )

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_x < 0:
            self._select((self._selected - 1) % len(_SHIPS))
        elif hat_x > 0:
            self._select((self._selected + 1) % len(_SHIPS))
