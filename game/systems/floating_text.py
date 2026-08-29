"""
game/systems/floating_text.py
Floating combat numbers and battle popup notifications.
Renders rising damage numbers, combo milestone tags, and ability ready popups.
"""
import random
import arcade


class FloatingNumber:
    __slots__ = ("text", "x", "y", "vx", "vy", "life", "max_life", "color", "font_size", "scale")

    def __init__(self, text: str, x: float, y: float, color: tuple,
                 life: float = 0.65, font_size: int = 12, is_crit: bool = False):
        self.text = text
        self.x = x + random.uniform(-8, 8)
        self.y = y + random.uniform(-4, 4)
        self.vx = random.uniform(-15, 15)
        self.vy = random.uniform(40, 75) if not is_crit else random.uniform(60, 95)
        self.life = life
        self.max_life = life
        self.color = color
        self.font_size = font_size if not is_crit else font_size + 4
        self.scale = 1.3 if is_crit else 1.0

    def update(self, delta_time: float) -> bool:
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.vy *= 0.94
        self.life -= delta_time
        return self.life > 0

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        frac = max(0.0, self.life / self.max_life)
        alpha = int(255 * min(1.0, frac * 1.5))
        r, g, b = self.color[:3]
        arcade.draw_text(
            self.text,
            self.x + ox, self.y + oy,
            (r, g, b, alpha),
            font_size=self.font_size,
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )


class FloatingTextManager:
    def __init__(self):
        self.numbers: list[FloatingNumber] = []

    def update(self, delta_time: float) -> None:
        self.numbers = [n for n in self.numbers if n.update(delta_time)]

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        for n in self.numbers:
            n.draw(ox, oy)

    def spawn_damage(self, x: float, y: float, amount: int, is_crit: bool = False,
                     color: tuple = None) -> None:
        if color is None:
            color = (255, 220, 50) if is_crit else (255, 160, 60)
        text = f"{amount}" if not is_crit else f"★ {amount}!"
        self.numbers.append(FloatingNumber(text, x, y, color=color, is_crit=is_crit))

    def spawn_combo(self, x: float, y: float, combo: int) -> None:
        if combo >= 3:
            self.numbers.append(FloatingNumber(
                f"×{combo} COMBO!", x, y + 16,
                color=(255, 100, 220), life=0.8, font_size=13, is_crit=True
            ))

    def spawn_notification(self, x: float, y: float, text: str, color: tuple = (100, 220, 255)) -> None:
        self.numbers.append(FloatingNumber(text, x, y, color=color, life=0.9, font_size=12, is_crit=True))
