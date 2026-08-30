"""
game/entities/enemies/asura_kamikaze.py
Asura Kamikaze — tiny, very fast, explodes on contact dealing AOE damage.
Flashes faster the closer it gets to the player.
"""
import math
import arcade
from constants import (
    ASURA_KAMIKAZE_HP, ASURA_KAMIKAZE_SPEED, ASURA_KAMIKAZE_SCORE,
    ASURA_KAMIKAZE_RADIUS, ASURA_KAMIKAZE_EXPLOSION_RADIUS,
    ASURA_KAMIKAZE_EXPLOSION_DAMAGE,
    COLOR_ASURA_KAMIKAZE, COLOR_WHITE,
    WIDTH, HEIGHT,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraKamikaze(BaseEnemy):
    """
    On player contact the collision system checks self.exploded,
    which triggers AOE damage to the player and kills this enemy.
    """

    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_KAMIKAZE_HP, speed=ASURA_KAMIKAZE_SPEED,
                         score_value=ASURA_KAMIKAZE_SCORE, radius=ASURA_KAMIKAZE_RADIUS)
        self.exploded = False
        self.explosion_radius = ASURA_KAMIKAZE_EXPLOSION_RADIUS
        self.explosion_damage = ASURA_KAMIKAZE_EXPLOSION_DAMAGE
        self._flash_cycle = 0.0
        self._visible = True
        self.texture = AssetManager.texture("asura_kamikaze.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        self._move_toward(player_x, player_y, delta_time)

        # Flash rate proportional to distance — panicky near the player
        dist = math.hypot(player_x - self.x, player_y - self.y)
        flash_rate = max(3.0, 18.0 - dist * 0.06)
        self._flash_cycle += delta_time * flash_rate
        self._visible = int(self._flash_cycle) % 2 == 0

        return []

    def explode(self) -> None:
        """Call this (from collision system) to trigger the explosion."""
        self.exploded = True
        self.alive = False

    def draw(self) -> None:
        if not self._visible:
            return
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_KAMIKAZE
        if self._draw_sprite(width=self.radius * 2.2, height=self.radius * 2.2,
                             color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            return
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        # No HP bar — it dies in one hit anyway; bar would clutter the tiny sprite
