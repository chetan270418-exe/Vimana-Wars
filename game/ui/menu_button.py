"""
Small animated button primitive shared by front-end views.
"""
import arcade
from game.ui.vedic_theme import GOLD, SURFACE_LOW, draw_chamfered_panel


class MenuButton:
    def __init__(self, label: str, center_x: float, center_y: float,
                 width: float, height: float, accent: tuple):
        self.label = label
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.accent = accent
        self.hover_amount = 0.0
        self._text = arcade.Text(
            label, center_x, center_y, (210, 220, 240, 255),
            font_size=12, bold=True, anchor_x="center", anchor_y="center",
        )

    def contains(self, x: float, y: float) -> bool:
        return (
            self.center_x - self.width / 2 <= x <= self.center_x + self.width / 2
            and self.center_y - self.height / 2 <= y <= self.center_y + self.height / 2
        )

    def update(self, delta_time: float, hovered: bool) -> None:
        target = 1.0 if hovered else 0.0
        self.hover_amount += (target - self.hover_amount) * min(1.0, delta_time * 14.0)

    def draw(self) -> None:
        scale = 1.0 + 0.035 * self.hover_amount
        width = self.width * scale
        height = self.height * scale
        left = self.center_x - width / 2
        right = self.center_x + width / 2
        bottom = self.center_y - height / 2
        top = self.center_y + height / 2
        r, g, b = self.accent

        fill = tuple(int(base + (target - base) * self.hover_amount)
                     for base, target in zip(SURFACE_LOW, (45, 52, 72)))
        draw_chamfered_panel(
            left, right, bottom, top,
            (r, g, b), fill=fill, alpha=245,
            border_width=1, selected=self.hover_amount > 0.1, cut=7,
        )
        self._text.position = (self.center_x, self.center_y)
        self._text.color = (r, g, b, 255) if self.hover_amount > 0.1 else (210, 220, 240, 255)
        self._text.font_size = int(12 + self.hover_amount)
        self._text.draw()
