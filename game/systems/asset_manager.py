"""Small, fault-tolerant cache for optional visual assets."""
from pathlib import Path
import arcade


_IMAGE_ROOT = Path(__file__).resolve().parents[2] / "assets" / "images"
_CACHE = {}


class AssetManager:
    """Load an image once and return ``None`` when it cannot be used."""

    @staticmethod
    def texture(name: str):
        if name in _CACHE:
            return _CACHE[name]
        path = _IMAGE_ROOT / name
        if path.suffix.lower() != ".png":
            path = path.with_suffix(".png")
        texture = None
        try:
            if path.is_file():
                texture = arcade.load_texture(str(path))
        except Exception:
            texture = None
        _CACHE[name] = texture
        return texture

    @staticmethod
    def draw(texture, x: float, y: float, width: float, height: float,
             angle: float = 0.0, color=(255, 255, 255, 255)) -> bool:
        """Draw a cached texture in Arcade 3.x; return whether it was drawn."""
        if texture is None:
            return False
        try:
            arcade.draw_texture_rect(
                texture,
                arcade.LBWH(x - width / 2, y - height / 2, width, height),
                angle=angle,
                color=color,
            )
            return True
        except Exception:
            return False
