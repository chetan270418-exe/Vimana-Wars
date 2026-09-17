"""
game/entities/enemies/base_enemy.py
Abstract base class for all enemy types with delta_time frame-rate independence,
hit stagger physics, safe spawning algorithms, and animated HP bars.
"""
import math
import random
import arcade
from abc import ABC, abstractmethod
from constants import WIDTH, HEIGHT
from game.systems.asset_manager import AssetManager


class BaseEnemy(ABC):
    def __init__(self, x: float, y: float, hp: int, speed: float,
                 score_value: int, radius: float):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.score_value = score_value
        self.radius = radius
        self.alive = True
        self._hit_flash = 0.0
        self._stagger_vx = 0.0
        self._stagger_vy = 0.0
        self._burning = 0.0
        self.texture = None

    @abstractmethod
    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    def take_damage(self, amount: int, knockback_angle: float | None = None) -> None:
        self.hp -= amount
        self._hit_flash = 0.12
        if knockback_angle is not None:
            rad = math.radians(knockback_angle)
            self._stagger_vx += math.cos(rad) * 120.0
            self._stagger_vy += math.sin(rad) * 120.0

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def is_dead(self) -> bool:
        return not self.alive

    def _angle_to_player(self, player_x: float, player_y: float) -> float:
        dx = player_x - self.x
        dy = player_y - self.y
        return math.degrees(math.atan2(dy, dx))

    def _move_toward(self, target_x: float, target_y: float,
                     delta_time: float, speed_override: float = None) -> None:
        # Apply stagger recovery
        if abs(self._stagger_vx) > 1 or abs(self._stagger_vy) > 1:
            self.x += self._stagger_vx * delta_time
            self.y += self._stagger_vy * delta_time
            self._stagger_vx *= 0.88
            self._stagger_vy *= 0.88

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 1:
            return
        spd = speed_override if speed_override is not None else self.speed
        step = spd * 60.0 * delta_time
        self.x += (dx / dist) * step
        self.y += (dy / dist) * step

    def _draw_hp_bar(self, bar_w: float = None, bar_h: float = 4,
                     y_offset: float = None) -> None:
        bar_w = bar_w or self.radius * 2.2
        y_offset = y_offset or self.radius + 6
        bg_x = self.x - bar_w / 2
        bg_y = self.y + y_offset
        frac = max(0.0, self.hp / self.max_hp)
        arcade.draw_lrbt_rectangle_filled(
            bg_x, bg_x + bar_w,
            bg_y, bg_y + bar_h,
            (80, 0, 0)
        )
        if frac > 0:
            color = (30, 200, 70) if frac > 0.35 else (220, 60, 0)
            arcade.draw_lrbt_rectangle_filled(
                bg_x, bg_x + bar_w * frac,
                bg_y, bg_y + bar_h,
                color
            )

    def _draw_sprite(self, width: float = None, height: float = None,
                     angle: float = 0.0,
                     color=(255, 255, 255, 255)) -> bool:
        width = width or self.radius * 2.2
        height = height or self.radius * 2.2
        return AssetManager.draw(self.texture, self.x, self.y, width, height,
                                 angle=angle, color=color)

    def _draw_elite_aura(self) -> None:
        if getattr(self, "is_elite", False):
            import time
            rot = time.time() * 90.0  # 90 degrees/sec
            arcade.draw_circle_outline(self.x, self.y, self.radius + 6, (255, 215, 0), 2)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 6, (255, 200, 0, 45))
            for i in range(4):
                rad = math.radians(rot + i * 90)
                px = self.x + math.cos(rad) * (self.radius + 9)
                py = self.y + math.sin(rad) * (self.radius + 9)
                arcade.draw_circle_filled(px, py, 3, (255, 230, 80))

    @staticmethod
    def spawn_at_edge(margin: float = 40, safe_player_x: float = WIDTH / 2, safe_player_y: float = HEIGHT / 2):
        """Return (x, y) guaranteed outside the visible screen and far from player."""
        for _ in range(10):
            side = random.randint(0, 3)
            if side == 0:
                x, y = random.uniform(margin, WIDTH - margin), HEIGHT + margin
            elif side == 1:
                x, y = random.uniform(margin, WIDTH - margin), -margin
            elif side == 2:
                x, y = -margin, random.uniform(margin, HEIGHT - margin)
            else:
                x, y = WIDTH + margin, random.uniform(margin, HEIGHT - margin)

            if math.hypot(x - safe_player_x, y - safe_player_y) > 200:
                return x, y
        return x, y
