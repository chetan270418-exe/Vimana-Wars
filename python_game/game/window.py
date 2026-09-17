"""Window creation and logical-resolution handling for Vimana Wars."""
import arcade
from pyglet.math import Mat4
from constants import WIDTH, HEIGHT, SCREEN_TITLE
from game.systems import save_system


class VimanaWindow(arcade.Window):
    """Arcade window that keeps the game's 900x600 layout in fullscreen.

    The game coordinates are intentionally designed around WIDTH/HEIGHT.
    Arcade changes the physical window size when entering fullscreen, so we
    use a centered, aspect-preserving viewport and a fixed logical projection.
    Mouse events are converted back into those logical coordinates before
    views receive them.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from pyglet.window import key, mouse
        self.keyboard = key.KeyStateHandler()
        self.mouse = mouse.MouseStateHandler()
        self.push_handlers(self.keyboard, self.mouse)

    def _apply_logical_viewport(self) -> None:
        physical_w = max(1, int(self.width))
        physical_h = max(1, int(self.height))
        scale = max(0.001, min(physical_w / WIDTH, physical_h / HEIGHT))
        view_w = max(1, int(WIDTH * scale))
        view_h = max(1, int(HEIGHT * scale))
        offset_x = (physical_w - view_w) // 2
        offset_y = (physical_h - view_h) // 2

        # Keep all existing draw code in the game's logical coordinate space.
        self.viewport = (offset_x, offset_y, view_w, view_h)
        self.projection = Mat4.orthogonal_projection(
            0, WIDTH, 0, HEIGHT, -1, 1
        )
        self._logical_scale = scale
        self._logical_offset = (offset_x, offset_y)

    def show_view(self, new_view) -> None:
        super().show_view(new_view)
        self._apply_logical_viewport()

    def on_resize(self, width: int, height: int) -> None:
        self._apply_logical_viewport()

    def _logical_point(self, x: float, y: float) -> tuple[float, float]:
        scale = getattr(self, "_logical_scale", 1.0)
        if scale <= 0:
            scale = 1.0
        offset_x, offset_y = getattr(self, "_logical_offset", (0, 0))
        return ((x - offset_x) / scale, (y - offset_y) / scale)

    def dispatch_event(self, event_type, *args):
        """Translate pointer events from physical pixels to game pixels."""
        scale = getattr(self, "_logical_scale", 1.0)
        if scale <= 0:
            scale = 1.0
        if event_type in ("on_mouse_motion", "on_mouse_drag") and len(args) >= 4:
            x, y = self._logical_point(args[0], args[1])
            args = (x, y, args[2] / scale, args[3] / scale, *args[4:])
        elif event_type in ("on_mouse_press", "on_mouse_release") and len(args) >= 2:
            x, y = self._logical_point(args[0], args[1])
            args = (x, y, *args[2:])
        return super().dispatch_event(event_type, *args)


def load_game_fonts() -> None:
    """Load bundled OFL fonts (Cinzel, Space Grotesk, JetBrains Mono) if available."""
    from pathlib import Path
    fonts_dir = Path(__file__).resolve().parent.parent / "assets" / "fonts"
    if not fonts_dir.exists():
        fonts_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "fonts"
    if fonts_dir.exists():
        for font_file in fonts_dir.glob("*.ttf"):
            try:
                arcade.load_font(str(font_file))
            except Exception:
                pass


def create_window() -> arcade.Window:
    load_game_fonts()
    saved = save_system.load()
    fullscreen = bool(saved.get("fullscreen", False))
    window = VimanaWindow(
        WIDTH, HEIGHT, SCREEN_TITLE,
        fullscreen=fullscreen,
        resizable=True,
        center_window=not fullscreen,
    )
    from game.views.intro_video_view import IntroVideoView
    window.show_view(IntroVideoView())
    return window
