"""
game/ui/radial_gauge.py
Circular cooldown and readiness dial for Dash, Chakram, and Brahmastra.
Renders an authentic 32px diameter gauge with sweep indicator, readiness pulse, and keybind tag.
"""
import math
import arcade
from game.ui.vedic_theme import (
    CYAN, CYAN_BRIGHT, GOLD, GOLD_BRIGHT, WELL, GREY,
    FONT_TELEMETRY, FONT_INTERFACE, draw_state_badge,
)


def draw_radial_gauge(center_x: float, center_y: float, radius: float = 16.0,
                      fraction: float = 1.0, color=CYAN, label: str = "",
                      keybind: str = "", ready: bool = True) -> None:
    """
    Draw a circular dial representing ability readiness / cooldown fraction.
    :param fraction: 0.0 (empty/cooling) to 1.0 (fully charged/ready).
    """
    fraction = max(0.0, min(1.0, fraction))
    is_ready = fraction >= 0.999 or ready

    # Outer well ring
    arcade.draw_circle_filled(center_x, center_y, radius, (*WELL[:3], 230))
    arcade.draw_circle_outline(center_x, center_y, radius, (*GREY[:3], 80), 1)

    # Sweep arc (clockwise from top: 90 deg down)
    sweep_angle = fraction * 360.0
    if sweep_angle > 0.0:
        fill_color = GOLD if is_ready else color
        # Draw arc from 90 deg backwards by sweep_angle
        start_angle = 90.0 - sweep_angle
        arcade.draw_arc_outline(center_x, center_y, radius * 2 - 3, radius * 2 - 3,
                                (*fill_color[:3], 240), start_angle, 90.0, 3)

    # Inner core dot
    core_color = GOLD_BRIGHT if is_ready else (*color[:3], 160)
    core_radius = 4.0 if is_ready else 2.5
    arcade.draw_circle_filled(center_x, center_y, core_radius, core_color)

    # Keybind badge underneath
    if keybind:
        badge_y = center_y - radius - 10
        draw_state_badge(center_x, badge_y, keybind, GOLD if is_ready else GREY, width=38)

    # Label text
    if label:
        text_y = center_y - radius - 24 if keybind else center_y - radius - 12
        arcade.draw_text(
            label, center_x, text_y,
            GOLD_BRIGHT if is_ready else GREY,
            font_size=8, bold=True, anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY,
        )
