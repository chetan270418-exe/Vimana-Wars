"""
game/ui/button.py
Reusable clickable button widget for menus, pause overlay, and stat screens.

Renders as a rounded-style rectangle with a centered label. Has three visual
states (idle / hover / pressed) driven by mouse position and click, with a
small pulse on hover and a brief scale-down on press for tactile feedback.

Uses arcade.Text objects for the label + hotkey hint (instead of draw_text)
to avoid the per-frame PerformanceWarning spam.
"""
import arcade
from game.ui.easing import clamp, ease_out_cubic


class Button:
    """
    A clickable rectangular button.

    Usage:
        btn = Button(x, y, w, h, label="RESUME", on_click=self._resume)
        # in on_update: btn.update(dt, mouse_x, mouse_y)
        # in on_draw:   btn.draw()
        # in on_mouse_press: if btn.hit_test(x, y): btn.press()
        # in on_mouse_release: if btn.was_pressed: btn.release()
    """

    # Default palette — easy to override per-instance
    DEFAULT_IDLE_FILL    = (28, 32, 60)
    DEFAULT_IDLE_BORDER  = (90, 110, 150)
    DEFAULT_HOVER_FILL   = (48, 58, 100)
    DEFAULT_HOVER_BORDER = (255, 220, 80)
    DEFAULT_PRESS_FILL   = (70, 85, 140)
    DEFAULT_PRESS_BORDER = (255, 240, 150)
    DEFAULT_LABEL_COLOR  = (220, 225, 245)
    DEFAULT_HOT_COLOR    = (255, 220, 80)

    def __init__(self, cx: float, cy: float, width: float, height: float,
                 label: str, on_click=None,
                 hotkey: str = None,
                 idle_fill: tuple = None, hover_fill: tuple = None,
                 press_fill: tuple = None,
                 idle_border: tuple = None, hover_border: tuple = None,
                 label_color: tuple = None,
                 font_size: int = 14, accent_color: tuple = None):
        self.cx = cx
        self.cy = cy
        self.w = width
        self.h = height
        self.label = label
        self.on_click = on_click
        self.hotkey = hotkey  # shown as a small hint next to the label

        # Allow per-instance color overrides, fall back to defaults
        self.idle_fill    = idle_fill    or self.DEFAULT_IDLE_FILL
        self.hover_fill   = hover_fill   or self.DEFAULT_HOVER_FILL
        self.press_fill   = press_fill   or self.DEFAULT_PRESS_FILL
        self.idle_border  = idle_border  or self.DEFAULT_IDLE_BORDER
        self.hover_border = hover_border or self.DEFAULT_HOVER_BORDER
        self.label_color  = label_color  or self.DEFAULT_LABEL_COLOR
        self.accent_color = accent_color or self.DEFAULT_HOT_COLOR
        self.font_size = font_size

        # State
        self.hovered = False
        self.pressed = False       # mouse held down on this button
        self.was_pressed = False    # edge-trigger for click detection
        self._press_anim = 0.0     # 0..1 visual press feedback (eases out)
        self._hover_anim = 0.0     # 0..1 hover lerp (eases out)

        # Cached Text objects — colors update in-place, no per-frame rebuild.
        self._text_label = arcade.Text(
            label, cx, cy, self.label_color, font_size=font_size, bold=True,
            anchor_x="center", anchor_y="center",
        )
        if hotkey:
            self._text_hot = arcade.Text(
                f"[{hotkey}]",
                cx + (width / 2) - 22, cy,
                (*self.accent_color, 220),
                font_size=10, bold=True,
                anchor_x="right", anchor_y="center",
            )
        else:
            self._text_hot = None

    # ── Geometry ──────────────────────────────────────────────────────

    @property
    def left(self) -> float:   return self.cx - self.w / 2
    @property
    def right(self) -> float:  return self.cx + self.w / 2
    @property
    def bottom(self) -> float: return self.cy - self.h / 2
    @property
    def top(self) -> float:    return self.cy + self.h / 2

    def hit_test(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    # ── Input events ──────────────────────────────────────────────────

    def press(self) -> None:
        """Call from on_mouse_press when this button is clicked."""
        self.pressed = True
        self.was_pressed = True
        self._press_anim = 1.0

    def release(self) -> bool:
        """
        Call from on_mouse_release. Returns True if this release is a real
        click (mouse was over us when released), False otherwise.
        """
        was_over = self.pressed and self.hovered
        self.pressed = False
        self.was_pressed = False
        if was_over and self.on_click:
            self.on_click()
        return was_over

    def cancel_press(self) -> None:
        """If the user dragged off the button before releasing, swallow it."""
        self.pressed = False

    def activate(self) -> None:
        """Activate from keyboard/gamepad without requiring mouse hover."""
        self._press_anim = 1.0
        if self.on_click:
            self.on_click()

    # ── Per-frame ─────────────────────────────────────────────────────

    def update(self, dt: float, mouse_x: float, mouse_y: float) -> None:
        # Hover state from mouse position
        new_hovered = self.hit_test(mouse_x, mouse_y)
        if new_hovered != self.hovered:
            self.hovered = new_hovered
        # Smooth the hover anim
        target = 1.0 if self.hovered else 0.0
        # Critically-damped lerp: ~10 = 100ms to converge
        self._hover_anim += (target - self._hover_anim) * min(1.0, 12.0 * dt)
        # Decay press anim
        if self._press_anim > 0:
            self._press_anim = max(0.0, self._press_anim - dt * 3.5)

    def draw(self) -> None:
        # Choose colors based on state, with a smooth blend for hover
        hov = clamp(self._hover_anim)
        # Press anim makes the button briefly sink in
        press_offset = ease_out_cubic(self._press_anim) * 4.0
        # Subtle scale on hover (1.0 -> 1.04)
        scale = 1.0 + 0.04 * hov
        w = self.w * scale
        h = self.h * scale

        # Fill: blend idle -> hover
        fill = _lerp_color(self.idle_fill, self.hover_fill, hov)
        if self.pressed:
            fill = self.press_fill
        # Border: same blend, brighter
        border = _lerp_color(self.idle_border, self.hover_border, hov)
        border_w = 2 if not self.hovered else 3

        cy = self.cy - press_offset

        # Background panel
        arcade.draw_lrbt_rectangle_filled(
            self.cx - w / 2, self.cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*fill, 230),
        )
        # Border
        arcade.draw_lrbt_rectangle_outline(
            self.cx - w / 2, self.cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*border, 255), border_w,
        )
        # Soft glow when hovered
        if hov > 0.05:
            glow_alpha = int(40 * hov)
            arcade.draw_lrbt_rectangle_filled(
                self.cx - w / 2 - 4, self.cx + w / 2 + 4,
                cy - h / 2 - 4, cy + h / 2 + 4,
                (*self.accent_color, glow_alpha),
            )

        # Label (with optional hotkey hint on the right) — use cached Text
        # objects so we don't trip arcade's per-frame draw_text performance warning.
        self._text_label.position = (self.cx, cy)
        self._text_label.color = (*self.label_color, 255)
        self._text_label.draw()
        if self._text_hot is not None:
            self._text_hot.position = (self.cx + (self.w / 2) - 22, cy)
            self._text_hot.draw()


def _lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1[:3], c2[:3]))
