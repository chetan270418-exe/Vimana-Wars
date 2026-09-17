"""
game/ui/modal.py
Canonical modal dialog with dim scrim, Tier 2 chamfered glass container, and focus trapping.
Used for Pause & Abandon Sortie confirmation per Section 5 and Section 7.8.
"""
import arcade
from constants import WIDTH, HEIGHT
from game.ui.vedic_theme import (
    SURFACE_HIGH, GOLD, CYAN_BRIGHT,
    ASTRA_RED, GREY, PARCHMENT,
    FONT_INTERFACE, FONT_TELEMETRY, draw_chamfered_panel, draw_corner_etching,
)
from game.ui.menu_button import MenuButton


class Modal:
    """Canonical modal dialog overlay."""

    def __init__(self, title: str, subtitle: str = "",
                 body: list[str] | None = None,
                 actions: list[tuple[str, str, str]] | None = None,
                 width: float = 460.0, height: float = 280.0,
                 accent=GOLD):
        """
        :param actions: list of (label, action_key, variant) where variant is 'celestial', 'metallic', or 'danger'.
        """
        self.title = title
        self.subtitle = subtitle
        self.body = body or []
        self.width = width
        self.height = height
        self.accent = accent
        self.is_open = False
        self._hovered_btn = -1
        self._buttons: list[tuple[MenuButton, str]] = []

        self._rebuild_buttons(actions or [])

    def _rebuild_buttons(self, actions: list[tuple[str, str, str]]) -> None:
        self._buttons.clear()
        if not actions:
            return

        btn_w = min(180.0, (self.width - 40 - (len(actions) - 1) * 16) / len(actions))
        btn_h = 36.0
        start_x = WIDTH // 2 - ((len(actions) - 1) * (btn_w + 16)) / 2
        btn_y = HEIGHT // 2 - self.height // 2 + 45.0

        for i, (label, key, variant) in enumerate(actions):
            bx = start_x + i * (btn_w + 16)
            btn = MenuButton(label, bx, btn_y, btn_w, btn_h,
                             accent=ASTRA_RED if variant == "danger" else (GOLD if variant == "celestial" else GREY),
                             variant=variant)
            self._buttons.append((btn, key))

    def set_content(self, title: str, subtitle: str = "",
                    body: list[str] | None = None,
                    actions: list[tuple[str, str, str]] | None = None,
                    accent=GOLD) -> None:
        self.title = title
        self.subtitle = subtitle
        self.body = body or []
        self.accent = accent
        if actions is not None:
            self._rebuild_buttons(actions)

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    def update(self, delta_time: float) -> None:
        if not self.is_open:
            return
        for i, (btn, _) in enumerate(self._buttons):
            btn.update(delta_time, i == self._hovered_btn)

    def on_mouse_motion(self, x: float, y: float) -> None:
        if not self.is_open:
            return
        self._hovered_btn = -1
        for i, (btn, _) in enumerate(self._buttons):
            if btn.contains(x, y):
                self._hovered_btn = i
                break

    def on_mouse_press(self, x: float, y: float) -> str | None:
        if not self.is_open:
            return None
        for i, (btn, key) in enumerate(self._buttons):
            if btn.contains(x, y):
                return key
        return None

    def on_key_press(self, key: int, modifiers: int) -> str | None:
        if not self.is_open:
            return None
        if key == arcade.key.ESCAPE:
            self.close()
            return "cancel"
        elif key == arcade.key.ENTER:
            # Activate first celestial or metallic button, or cancel if danger
            for btn, act_key in self._buttons:
                if act_key in ("resume", "cancel"):
                    return act_key
            if self._buttons:
                return self._buttons[0][1]
        return None

    def draw(self) -> None:
        if not self.is_open:
            return

        # 70% dim scrim over entire viewport
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (0, 0, 0, 180))

        # Centered Tier 2 chamfered dialog
        left = WIDTH // 2 - self.width // 2
        right = WIDTH // 2 + self.width // 2
        bottom = HEIGHT // 2 - self.height // 2
        top = HEIGHT // 2 + self.height // 2

        draw_chamfered_panel(left, right, bottom, top, self.accent,
                             fill=SURFACE_HIGH, alpha=245, border_width=2,
                             selected=True, cut=10.0, scanlines=True)
        draw_corner_etching(left, right, bottom, top, self.accent, length=16.0, alpha=140)

        # Title
        arcade.draw_text(self.title, WIDTH // 2, top - 32,
                         self.accent, font_size=16, bold=True,
                         anchor_x="center", font_name=FONT_INTERFACE)
        if self.subtitle:
            arcade.draw_text(self.subtitle, WIDTH // 2, top - 52,
                             CYAN_BRIGHT, font_size=9, bold=True,
                             anchor_x="center", font_name=FONT_TELEMETRY)

        arcade.draw_line(left + 24, top - 62, right - 24, top - 62, (*self.accent[:3], 60), 1)

        # Body copy lines
        body_y = top - 86
        for line in self.body:
            arcade.draw_text(line, WIDTH // 2, body_y,
                             PARCHMENT, font_size=10,
                             anchor_x="center", font_name=FONT_INTERFACE)
            body_y -= 18

        # Buttons
        for btn, _ in self._buttons:
            btn.draw()
