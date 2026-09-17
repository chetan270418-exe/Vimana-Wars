"""
game/entities/bullet.py
Player and enemy projectiles with delta_time frame-rate independent movement,
muzzle flash support, and glowing trailing particle tails.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    PLAYER_BULLET_SPEED, PLAYER_BULLET_RADIUS, PLAYER_BULLET_DAMAGE,
    ENEMY_BULLET_SPEED, ENEMY_BULLET_RADIUS, ENEMY_BULLET_DAMAGE,
    COLOR_BULLET_PLAYER, COLOR_BULLET_ENEMY,
)


class PlayerBullet:
    """Fired by the player vimana, travels with glowing energy trail."""

    def __init__(self, x: float, y: float, angle: float, speed: float = PLAYER_BULLET_SPEED,
                 damage: int = PLAYER_BULLET_DAMAGE, radius: float = PLAYER_BULLET_RADIUS,
                 color: tuple = COLOR_BULLET_PLAYER, is_piercing: bool = False):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = radius
        self.damage = damage
        self.color = color
        self.is_piercing = is_piercing
        self.alive = True
        self.trail: list[tuple[float, float, float]] = []  # [(x, y, alpha)]
        self.pierce_count = 0

    def update(self, delta_time: float) -> None:
        step = self.speed * 60.0 * delta_time
        rad = math.radians(self.angle)

        # Store trail position
        self.trail.append((self.x, self.y, 220))
        if len(self.trail) > 5:
            self.trail.pop(0)

        self.x += math.cos(rad) * step
        self.y += math.sin(rad) * step

        # Age trails
        self.trail = [(tx, ty, max(0, a - int(500 * delta_time))) for tx, ty, a in self.trail if a > 10]

        if not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
            self.alive = False

    def draw(self) -> None:
        r, g, b = self.color[:3]
        # Draw fading energy trail
        for tx, ty, alpha in self.trail:
            arcade.draw_circle_filled(tx, ty, self.radius * 0.75, (r, g, b, alpha // 2))

        # Core
        arcade.draw_circle_filled(self.x, self.y, self.radius, (255, 255, 255))
        arcade.draw_circle_filled(self.x, self.y, self.radius * 0.8, self.color)
        # Glow halo
        arcade.draw_circle_filled(self.x, self.y, self.radius + 3, (r, g, b, 70))


class EnemyBullet:
    """Fired by enemies and bosses, aimed at the player with crimson trails."""

    def __init__(self, x: float, y: float, angle: float, speed: float = ENEMY_BULLET_SPEED,
                 damage: int = ENEMY_BULLET_DAMAGE, radius: float = ENEMY_BULLET_RADIUS,
                 color: tuple = COLOR_BULLET_ENEMY):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = radius
        self.damage = damage
        self.color = color
        self.alive = True
        self.trail: list[tuple[float, float, float]] = []

    def update(self, delta_time: float) -> None:
        step = self.speed * 60.0 * delta_time
        rad = math.radians(self.angle)

        self.trail.append((self.x, self.y, 200))
        if len(self.trail) > 4:
            self.trail.pop(0)

        self.x += math.cos(rad) * step
        self.y += math.sin(rad) * step

        self.trail = [(tx, ty, max(0, a - int(600 * delta_time))) for tx, ty, a in self.trail if a > 10]

        if not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
            self.alive = False

    def draw(self) -> None:
        r, g, b = self.color[:3]
        for tx, ty, alpha in self.trail:
            arcade.draw_circle_filled(tx, ty, self.radius * 0.65, (r, g, b, alpha // 2))

        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        arcade.draw_circle_filled(self.x, self.y, self.radius + 2, (r, g, b, 90))
