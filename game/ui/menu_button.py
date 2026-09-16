"""
game/ui/menu_button.py
Canonical Vedic-Punk Button Component with Celestial, Metallic, and Danger variants.
Supports smooth 120ms ease-out hover scale (+3.5%), breathing glow, and font fallbacks.
"""
import math
import arcade
from game.ui.vedic_theme import (
    GOLD, GOLD_BRIGHT, CYAN, CYAN_BRIGHT, GREY, OBSIDIAN, SURFACE_LOW,
    ASTRA_RED, ASTRA_RED_BRIGHT, FONT_INTERFACE, draw_chamfered_panel,
)


class MenuButton:
    def __init__(self, label: str, center_x: float, center_y: float,
                 width: float = 200.0, height: float = 40.0,
                 accent: tuple = GOLD, variant: str = "metallic"):
        self.label = label
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.variant = variant  # 'celestial', 'metallic', 'danger'
        self.accent = accent
        self.hover_amount = 0.0
        self._pulse_timer = 0.0

        # Resolve colors by variant
        if variant == "celestial" or accent == GOLD:
            self._base_border = GOLD
            self._hover_border = GOLD_BRIGHT
            self._base_text = GOLD_BRIGHT
            self._hover_text = (255, 255, 255)
            self._fill = OBSIDIAN
            self._border_w = 2
        elif variant == "danger" or accent == ASTRA_RED:
            self._base_border = ASTRA_RED
            self._hover_border = ASTRA_RED_BRIGHT
            self._base_text = ASTRA_RED_BRIGHT
            self._hover_text = (255, 255, 255)
            self._fill = (34, 8, 18)
            self._border_w = 2
        else:
            self._base_border = GREY if accent == GREY else accent
            self._hover_border = CYAN
            self._base_text = (210, 220, 240)
            self._hover_text = CYAN_BRIGHT
            self._fill = SURFACE_LOW
            self._border_w = 1

        self._text = arcade.Text(
            label, center_x, center_y, (*self._base_text, 255),
            font_size=12, bold=True, anchor_x="center", anchor_y="center",
            font_name=FONT_INTERFACE,
        )

    def contains(self, x: float, y: float) -> bool:
        return (
            self.center_x - self.width / 2 <= x <= self.center_x + self.width / 2
            and self.center_y - self.height / 2 <= y <= self.center_y + self.height / 2
        )

    def update(self, delta_time: float, hovered: bool) -> None:
        target = 1.0 if hovered else 0.0
        self.hover_amount += (target - self.hover_amount) * min(1.0, delta_time * 14.0)
        self._pulse_timer += delta_time

    def draw(self) -> None:
        scale = 1.0 + 0.035 * self.hover_amount
        width = self.width * scale
        height = self.height * scale
        left = self.center_x - width / 2
        right = self.center_x + width / 2
        bottom = self.center_y - height / 2
        top = self.center_y + height / 2

        # Interpolate border color
        r = int(self._base_border[0] + (self._hover_border[0] - self._base_border[0]) * self.hover_amount)
        g = int(self._base_border[1] + (self._hover_border[1] - self._base_border[1]) * self.hover_amount)
        b = int(self._base_border[2] + (self._hover_border[2] - self._base_border[2]) * self.hover_amount)

        # Hover fill brightening
        fill = tuple(int(base + (target - base) * self.hover_amount)
                     for base, target in zip(self._fill, (45, 52, 72)))

        border_width = self._border_w if self.hover_amount < 0.2 else self._border_w + 1

        draw_chamfered_panel(
            left, right, bottom, top,
            (r, g, b), fill=fill, alpha=245,
            border_width=border_width,
            selected=self.hover_amount > 0.1,
            cut=8.0,
        )

        # Update text position, color, and size
        tr = int(self._base_text[0] + (self._hover_text[0] - self._base_text[0]) * self.hover_amount)
        tg = int(self._base_text[1] + (self._hover_text[1] - self._base_text[1]) * self.hover_amount)
        tb = int(self._base_text[2] + (self._hover_text[2] - self._base_text[2]) * self.hover_amount)
        self._text.position = (self.center_x, self.center_y)
        self._text.color = (tr, tg, tb, 255)
        self._text.font_size = int(12 + self.hover_amount)
        self._text.draw()
