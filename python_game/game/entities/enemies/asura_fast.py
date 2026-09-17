"""
game/entities/enemies/asura_fast.py
Asura Chaser — fast, weak, beelines straight at the player.
"""
import arcade
from constants import (
    WIDTH, HEIGHT,
    ASURA_FAST_HP, ASURA_FAST_SPEED, ASURA_FAST_SCORE, ASURA_FAST_RADIUS,
    COLOR_ASURA_FAST, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraFast(BaseEnemy):
    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_FAST_HP, speed=ASURA_FAST_SPEED,
                         score_value=ASURA_FAST_SCORE, radius=ASURA_FAST_RADIUS)
        self.texture = AssetManager.texture("asura_fast.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        self._move_toward(player_x, player_y, delta_time)
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        return []   # no projectiles

    def draw(self) -> None:
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_FAST
        if self._draw_sprite(color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            self._draw_hp_bar()
            return
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        # Pupils — two small dots to give it a face
        arcade.draw_circle_filled(self.x - 4, self.y + 3, 2, COLOR_WHITE)
        arcade.draw_circle_filled(self.x + 4, self.y + 3, 2, COLOR_WHITE)
        self._draw_hp_bar()
