"""
game/entities/enemies/asura_tank.py
Asura Brute — slow, very tanky, deals heavy contact damage.
"""
import arcade
from constants import (
    WIDTH, HEIGHT,
    ASURA_TANK_HP, ASURA_TANK_SPEED, ASURA_TANK_SCORE, ASURA_TANK_RADIUS,
    ASURA_TANK_CONTACT_DAMAGE,
    COLOR_ASURA_TANK, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraTank(BaseEnemy):
    """Contact damage is higher — collision.py checks this attribute."""

    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_TANK_HP, speed=ASURA_TANK_SPEED,
                         score_value=ASURA_TANK_SCORE, radius=ASURA_TANK_RADIUS)
        self.contact_damage = ASURA_TANK_CONTACT_DAMAGE
        self.texture = AssetManager.texture("asura_tank.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        self._move_toward(player_x, player_y, delta_time)
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        return []

    def draw(self) -> None:
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_TANK
        if self._draw_sprite(width=self.radius * 2.4, height=self.radius * 2.4,
                             color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            self._draw_hp_bar(bar_w=self.radius * 2.5)
            return
        # Large body
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        
        hp_frac = self.hp / self.max_hp
        import math

        # Spiky outline to signal tanky-ness (outer spikes break off below 50% HP)
        active_spikes = 8 if hp_frac > 0.5 else 4
        for i in range(active_spikes):
            ang = math.radians(i * (360 / active_spikes))
            sx = self.x + math.cos(ang) * (self.radius + 7)
            sy = self.y + math.sin(ang) * (self.radius + 7)
            arcade.draw_circle_filled(sx, sy, 4, COLOR_ASURA_TANK)

        # Draw glowing armor crack lines when damaged
        if hp_frac < 0.70:
            arcade.draw_line(self.x - 8, self.y + 6, self.x + 4, self.y - 2, (255, 100, 30), 2)
        if hp_frac < 0.40:
            arcade.draw_line(self.x + 4, self.y - 2, self.x + 10, self.y - 9, (255, 60, 20), 2)
            arcade.draw_line(self.x - 3, self.y - 8, self.x + 2, self.y + 7, (255, 200, 50), 2)

        self._draw_hp_bar(bar_w=self.radius * 2.5)
