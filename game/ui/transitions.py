"""
game/ui/transitions.py
View-transition overlays — smooth crossfade between arcade Views.
Supports fade-to-black, slide-up, and custom wipe patterns.
"""
import math
import arcade
from constants import WIDTH, HEIGHT
from game.ui.easing import ease_in_out_cubic, ease_out_cubic, clamp


class TransitionOverlay:
    """
    Singleton-ish overlay drawn on top of the active view.
    Call TransitionOverlay.start(...) to begin a transition;
    the overlay handles the mid-swap and fade-in automatically.

    Usage:
        Instead of:
            self.window.show_view(NextView())
        Do:
            TransitionOverlay.start(self.window, NextView(), duration=0.4)

    The overlay must be drawn by the window's active view — see the
    `draw_transition()` helper which views should call at the end of on_draw().
    """

    # Class-level state (one transition at a time)
    _active = False
    _phase = "idle"       # "fade_out" | "swap" | "fade_in" | "idle"
    _elapsed = 0.0
    _duration = 0.4
    _half = 0.2
    _window = None
    _new_view = None
    _color = (0, 0, 0)   # transition overlay color
    _style = "fade"       # "fade" | "slide_up" | "wipe"

    @classmethod
    def start(cls, window, new_view, duration: float = 0.4,
              color: tuple = (0, 0, 0), style: str = "fade") -> None:
        """Begin a transition to new_view."""
        cls._active = True
        cls._phase = "fade_out"
        cls._elapsed = 0.0
        cls._duration = duration
        cls._half = duration / 2.0
        cls._window = window
        cls._new_view = new_view
        cls._color = color
        cls._style = style

    @classmethod
    def update(cls, dt: float) -> None:
        if not cls._active:
            return
        cls._elapsed += dt

        if cls._phase == "fade_out":
            if cls._elapsed >= cls._half:
                # Swap view at the midpoint (screen is fully covered)
                cls._phase = "fade_in"
                cls._elapsed = 0.0
                if cls._window and cls._new_view:
                    cls._window.show_view(cls._new_view)
                    cls._new_view = None

        elif cls._phase == "fade_in":
            if cls._elapsed >= cls._half:
                cls._active = False
                cls._phase = "idle"

    @classmethod
    def draw(cls) -> None:
        """Draw the transition overlay. Call at the END of on_draw()."""
        if not cls._active:
            return

        if cls._style == "fade":
            cls._draw_fade()
        elif cls._style == "slide_up":
            cls._draw_slide_up()
        elif cls._style == "wipe":
            cls._draw_wipe()

    @classmethod
    def _draw_fade(cls) -> None:
        if cls._phase == "fade_out":
            t = clamp(cls._elapsed / cls._half)
            alpha = int(255 * ease_in_out_cubic(t))
        else:  # fade_in
            t = clamp(cls._elapsed / cls._half)
            alpha = int(255 * (1.0 - ease_out_cubic(t)))
        r, g, b = cls._color[:3]
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (r, g, b, alpha))

    @classmethod
    def _draw_slide_up(cls) -> None:
        if cls._phase == "fade_out":
            t = clamp(cls._elapsed / cls._half)
            y_off = int(HEIGHT * ease_in_out_cubic(t))
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, y_off, (r, g, b, 255))
        else:
            t = clamp(cls._elapsed / cls._half)
            y_off = int(HEIGHT * (1.0 - ease_out_cubic(t)))
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, HEIGHT - y_off, HEIGHT, (r, g, b, 255))

    @classmethod
    def _draw_wipe(cls) -> None:
        """Horizontal scan-line wipe from top to bottom."""
        if cls._phase == "fade_out":
            t = clamp(cls._elapsed / cls._half)
            eased = ease_in_out_cubic(t)
            # Fill from top downward
            fill_h = int(HEIGHT * eased)
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, HEIGHT - fill_h, HEIGHT, (r, g, b, 255))
            # Scan line at leading edge
            line_y = HEIGHT - fill_h
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, line_y - 3, line_y + 1, (255, 255, 255, 80))
        else:
            t = clamp(cls._elapsed / cls._half)
            eased = ease_out_cubic(t)
            fill_h = int(HEIGHT * (1.0 - eased))
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, fill_h, (r, g, b, 255))
            line_y = fill_h
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, line_y - 1, line_y + 3, (255, 255, 255, 80))

    @classmethod
    @property
    def is_active(cls) -> bool:
        return cls._active


def transition_to(window, new_view, duration: float = 0.4,
                  color: tuple = (0, 0, 0), style: str = "fade") -> None:
    """
    Convenience function — call this instead of window.show_view() for
    a smooth animated transition.
    """
    TransitionOverlay.start(window, new_view, duration=duration,
                            color=color, style=style)
