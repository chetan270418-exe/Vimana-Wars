"""
game/entities/enemies/asura_ranged.py
Asura Shooter — keeps its distance and fires enemy bullets at the player.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    ASURA_RANGED_HP, ASURA_RANGED_SPEED, ASURA_RANGED_SCORE, ASURA_RANGED_RADIUS,
    ASURA_RANGED_FIRE_RATE, ASURA_RANGED_PREFERRED_DIST,
    COLOR_ASURA_RANGED, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet


class AsuraRanged(BaseEnemy):
    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_RANGED_HP, speed=ASURA_RANGED_SPEED,
                         score_value=ASURA_RANGED_SCORE, radius=ASURA_RANGED_RADIUS)
        self._fire_timer = ASURA_RANGED_FIRE_RATE  # wait before first shot

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        # Maintain preferred distance — move closer if too far, back off if too close
        dist = math.hypot(player_x - self.x, player_y - self.y)
        if dist < ASURA_RANGED_PREFERRED_DIST - 40:
            # Too close — strafe sideways and backwards
            angle = self._angle_to_player(player_x, player_y) + 180
            rad = math.radians(angle)
            step = self.speed * 60.0 * delta_time
            self.x += math.cos(rad) * step
            self.y += math.sin(rad) * step
        elif dist > ASURA_RANGED_PREFERRED_DIST + 40:
            self._move_toward(player_x, player_y, delta_time)

        # Fire
        self._fire_timer -= delta_time
        if self._fire_timer <= 0:
            self._fire_timer = ASURA_RANGED_FIRE_RATE
            angle = self._angle_to_player(player_x, player_y)
            return [EnemyBullet(self.x, self.y, angle)]

        return []

    def draw(self) -> None:
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_RANGED
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        # A small 'barrel' pointing at the last known player direction
        arcade.draw_circle_filled(self.x, self.y + self.radius - 4, 4, (80, 0, 130))
        self._draw_hp_bar()
