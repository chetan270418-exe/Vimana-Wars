"""
game/views/difficulty_view.py
Difficulty selection screen shown before the game starts.
Reads/writes via save_system so the choice persists between sessions.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.ui.transitions import transition_to, TransitionOverlay

_OPTIONS = ["easy", "normal", "hard", "endless"]
_DESCRIPTIONS = {
    "easy":    "More HP  ·  Less damage  ·  Fewer enemies",
    "normal":  "The intended mythological campaign",
    "hard":    "Less HP  ·  More damage  ·  Elite foes",
    "endless": "Mahayuddha: Infinite scaling waves & continuous boss encounters",
}
_COLORS = {
    "easy":    (60, 220, 100),
    "normal":  (220, 200, 60),
    "hard":    (220, 60, 60),
    "endless": (220, 90, 255),
}


class DifficultyView(arcade.View):
    def __init__(self, start_wave: int = 1, realm_id: int | None = None):
        super().__init__()
        self.start_wave = max(1, int(start_wave))
        self.realm_id = realm_id
        saved = save_system.load()
        last_diff = saved.get("difficulty", "normal")
        self._selected = _OPTIONS.index(last_diff) if last_diff in _OPTIONS else 1
        self._hovered = -1
        self._pulse = 0.0
        self.sound_manager = SoundManager()

        # ── Static text ──────────────────────────────────────────────
        self._title = arcade.Text(
            "SELECT GAMEPLAY MODE",
            WIDTH // 2, int(HEIGHT * 0.86),
            COLOR_WAVE, font_size=26, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._option_texts = [
            arcade.Text(
                opt.upper() if opt != "endless" else "ENDLESS MAHAYUDDHA",
                WIDTH // 2, int(HEIGHT * 0.68) - i * 62,
                _COLORS[opt], font_size=18, bold=True,
                anchor_x="center", anchor_y="center",
            )
            for i, opt in enumerate(_OPTIONS)
        ]
        self._desc_texts = [
            arcade.Text(
                _DESCRIPTIONS[opt],
                WIDTH // 2, int(HEIGHT * 0.68) - i * 62 - 20,
                (160, 160, 180), font_size=9,
                anchor_x="center", anchor_y="center",
            )
            for i, opt in enumerate(_OPTIONS)
        ]
        self._hint = arcade.Text(
            "↑ ↓ to choose   ENTER to confirm   ESC to go back",
            WIDTH // 2, int(HEIGHT * 0.08),
            (130, 130, 160), font_size=11,
            anchor_x="center",
        )
        # Cursor arrow (updated in draw)
        self._cursor = arcade.Text(
            "▶", 0, 0,
            COLOR_WHITE, font_size=18, bold=True,
            anchor_x="right", anchor_y="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time

    def on_draw(self) -> None:
        self.clear()

        self._title.draw()

        for i, (opt, txt, desc) in enumerate(
            zip(_OPTIONS, self._option_texts, self._desc_texts)
        ):
            # Highlight the selected option
            if i == self._selected or i == self._hovered:
                pulse = 0.85 + 0.15 * math.sin(self._pulse * 4)
                r, g, b = _COLORS[opt]
                txt.color = (int(r * pulse), int(g * pulse), int(b * pulse))

                # Draw selection box
                cy = int(HEIGHT * 0.68) - i * 62
                arcade.draw_lrbt_rectangle_outline(
                    WIDTH // 2 - 210, WIDTH // 2 + 210,
                    cy - 26, cy + 26,
                    (*_COLORS[opt], 220 if i == self._selected else 120),
                    2 if i == self._selected else 1,
                )
                if i == self._selected:
                    # Cursor
                    self._cursor.x = WIDTH // 2 - 220
                    self._cursor.y = cy
                    self._cursor.draw()
            else:
                r, g, b = _COLORS[opt]
                txt.color = (r // 2, g // 2, b // 2)   # dimmed when not selected

            txt.draw()
            desc.draw()

        self._hint.draw()
        TransitionOverlay.draw()

    def _row_at(self, x: float, y: float) -> int:
        if not WIDTH // 2 - 230 <= x <= WIDTH // 2 + 230:
            return -1
        for i in range(len(_OPTIONS)):
            cy = int(HEIGHT * 0.68) - i * 62
            if cy - 30 <= y <= cy + 30:
                return i
        return -1

    def _confirm(self) -> None:
        if TransitionOverlay.is_active:
            return
        chosen = _OPTIONS[self._selected]
        save_system.set_difficulty(chosen)
        self.sound_manager.play_ui_click()
        from game.views.ship_select_view import ShipSelectView
        transition_to(
            self.window,
            ShipSelectView(
                difficulty=chosen,
                start_wave=self.start_wave,
                realm_id=self.realm_id,
            ),
        )

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        new_hovered = self._row_at(x, y)
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.20)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        row = self._row_at(x, y)
        if row < 0:
            return
        if row == self._selected:
            self._confirm()
        else:
            self._selected = row
            self.sound_manager.play_ui_click(volume=0.35)

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._selected = (self._selected - 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected = (self._selected + 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            self._confirm()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y > 0:
            self._selected = (self._selected - 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif hat_y < 0:
            self._selected = (self._selected + 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
