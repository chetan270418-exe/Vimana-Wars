"""Small Arcade-native visual primitives for the Vedic-punk interface."""
import math
import arcade
from constants import WIDTH, HEIGHT


OBSIDIAN = (11, 13, 18)
SURFACE_LOW = (20, 26, 40)
SURFACE_HIGH = (31, 41, 60)
GOLD = (233, 196, 0)
GOLD_BRIGHT = (255, 246, 223)
CYAN = (0, 219, 231)
CYAN_BRIGHT = (116, 245, 255)
RED = (191, 0, 54)
RED_BRIGHT = (255, 107, 114)
PARCHMENT = (208, 198, 171)
MUTED = (143, 152, 168)
GLASS_LOW = (*SURFACE_LOW, 217)
GLASS_HIGH = (*SURFACE_HIGH, 235)
HAIRLINE_GOLD = (*GOLD, 72)
HAIRLINE_CYAN = (*CYAN, 58)


def pulse_alpha(elapsed: float, low: int = 90, high: int = 190,
                speed: float = 3.0, reduced: bool = False) -> int:
    if reduced:
        return low
    phase = (math.sin(elapsed * speed) + 1.0) * 0.5
    return int(low + (high - low) * phase)


def _chamfer_points(left, right, bottom, top, cut=10):
    cut = min(cut, max(1, (right - left) / 3), max(1, (top - bottom) / 3))
    return [
        (left + cut, bottom), (right - cut, bottom),
        (right, bottom + cut), (right, top - cut),
        (right - cut, top), (left + cut, top),
        (left, top - cut), (left, bottom + cut),
    ]


def draw_chamfered_panel(left, right, bottom, top, accent=GOLD,
                         *, fill=SURFACE_LOW, alpha=225, border_width=1,
                         selected=False, cut=10) -> None:
    """Draw a sharp glass panel with a restrained luminous border."""
    points = _chamfer_points(left, right, bottom, top, cut)
    arcade.draw_polygon_filled(points, (*fill[:3], alpha))
    border_alpha = min(255, alpha + 25 if selected else alpha)
    width = max(border_width, 2 if selected else border_width)
    for i, point in enumerate(points):
        nxt = points[(i + 1) % len(points)]
        arcade.draw_line(point[0], point[1], nxt[0], nxt[1],
                         (*accent[:3], border_alpha), width)
    if top - bottom > 18:
        arcade.draw_line(left + cut + 6, top - 3, right - cut - 6, top - 3,
                         (*accent[:3], min(110, border_alpha)), 1)


def draw_corner_etching(left, right, bottom, top, color=GOLD, length=22,
                        alpha=90) -> None:
    """Draw four cockpit-style corner brackets around a content area."""
    c = (*color[:3], alpha)
    arcade.draw_line(left, top, left + length, top, c, 1)
    arcade.draw_line(left, top, left, top - length, c, 1)
    arcade.draw_line(right, top, right - length, top, c, 1)
    arcade.draw_line(right, top, right, top - length, c, 1)
    arcade.draw_line(left, bottom, left + length, bottom, c, 1)
    arcade.draw_line(left, bottom, left, bottom + length, c, 1)
    arcade.draw_line(right, bottom, right - length, bottom, c, 1)
    arcade.draw_line(right, bottom, right, bottom + length, c, 1)


def draw_segmented_bar(left, right, bottom, top, fraction, color=CYAN,
                       segments=9, background=(53, 57, 60), gap=3) -> None:
    """Render a compact segmented telemetry bar used by vitals and HUD."""
    fraction = max(0.0, min(1.0, fraction))
    width = right - left
    segment_width = (width - gap * (segments - 1)) / segments
    for i in range(segments):
        x1 = left + i * (segment_width + gap)
        x2 = x1 + segment_width
        filled = fraction >= (i + 1) / segments
        partial = max(0.0, min(1.0, fraction * segments - i))
        arcade.draw_lrbt_rectangle_filled(x1, x2, bottom, top,
                                           (*background[:3], 220))
        if filled or partial > 0:
            arcade.draw_lrbt_rectangle_filled(
                x1, x1 + segment_width * partial, bottom, top,
                (*color[:3], 240),
            )


def draw_scanlines(left: float, right: float, bottom: float, top: float,
                   color=CYAN, spacing: int = 18, alpha: int = 12) -> None:
    y = bottom + spacing
    while y < top:
        arcade.draw_line(left, y, right, y, (*color[:3], alpha), 1)
        y += spacing


def draw_telemetry_ticks(left: float, right: float, y: float, color=CYAN,
                         count: int = 12, height: float = 5,
                         alpha: int = 80) -> None:
    if count < 2:
        return
    step = (right - left) / (count - 1)
    arcade.draw_line(left, y, right, y, (*color[:3], alpha // 2), 1)
    for index in range(count):
        tick_height = height * (1.5 if index in (0, count - 1) else 1.0)
        x = left + index * step
        arcade.draw_line(x, y - tick_height, x, y + tick_height,
                         (*color[:3], alpha), 1)


def draw_menu_backdrop(title: str, subtitle: str = "", accent=GOLD,
                       *, pulse: float = 0.0, reduced: bool = False) -> None:
    arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, OBSIDIAN)
    draw_scanlines(24, WIDTH - 24, 58, HEIGHT - 58, CYAN, spacing=24, alpha=6)
    draw_corner_etching(24, WIDTH - 24, 24, HEIGHT - 24, accent, length=22, alpha=105)
    arcade.draw_line(24, HEIGHT - 74, WIDTH - 24, HEIGHT - 74, (*accent, 105), 1)
    arcade.draw_text(title, 42, HEIGHT - 52, accent, font_size=22, bold=True)
    if subtitle:
        arcade.draw_text(subtitle, 42, HEIGHT - 68, MUTED, font_size=8, bold=True)
    draw_back_navigation()
    if not reduced:
        alpha = pulse_alpha(pulse, 12, 30, 1.7)
        arcade.draw_circle_outline(WIDTH - 100, HEIGHT - 50, 28, (*accent, alpha), 1)
        arcade.draw_line(WIDTH - 132, HEIGHT - 50, WIDTH - 68, HEIGHT - 50, (*accent, alpha), 1)


def draw_focus_panel(left: float, right: float, bottom: float, top: float,
                     accent=CYAN, *, selected: bool = False) -> None:
    draw_chamfered_panel(left, right, bottom, top, accent,
                         fill=SURFACE_HIGH if selected else SURFACE_LOW,
                         alpha=238, border_width=2 if selected else 1,
                         selected=selected, cut=10)


def draw_back_navigation(label: str = "ESC  BACK") -> None:
    arcade.draw_text(label, WIDTH - 30, HEIGHT - 52, MUTED, font_size=8,
                     bold=True, anchor_x="right", anchor_y="center")


def draw_state_badge(x: float, y: float, label: str, color, *, width: float = 92) -> None:
    draw_chamfered_panel(x - width / 2, x + width / 2, y - 10, y + 10,
                         color, fill=(12, 18, 30), alpha=225, border_width=1, cut=5)
    arcade.draw_text(label, x, y - 3, color, font_size=8, bold=True,
                     anchor_x="center")
