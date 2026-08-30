"""Small Arcade-native visual primitives for the Vedic-punk interface."""
import arcade


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
