"""
game/entities/enemies/asura_healer.py
Asura Healer — Priest vessel that pulses healing restorative waves to nearby damaged Asuras.
Priority target for player.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_WHITE
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraHealer(BaseEnemy):
    def __init__(self, safe_player_x: float = WIDTH / 2, safe_player_y: float = HEIGHT / 2):
        x, y = BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y, hp=45, speed=1.6, score_value=250, radius=18)
        self._heal_timer = 2.5
        self._pulse_anim = 0.0
        self.texture = AssetManager.texture("asura_healer.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        self._pulse_anim += delta_time
        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        # Stays at mid distance
        dist = math.hypot(player_x - self.x, player_y - self.y)
        if dist < 220:
            self._move_toward(self.x - (player_x - self.x), self.y - (player_y - self.y), delta_time, speed_override=self.speed * 0.8)
        else:
            self._move_toward(player_x, player_y, delta_time)

        self._heal_timer -= delta_time
        return []

    def perform_heal_pulse(self, enemies: list) -> bool:
        if self._heal_timer <= 0:
            self._heal_timer = 2.8
            for e in enemies:
                if e is not self and e.alive and math.hypot(e.x - self.x, e.y - self.y) < 180:
                    e.hp = min(e.max_hp, e.hp + 20)
            return True
        return False

    def draw(self) -> None:
        self._draw_elite_aura()
        flash = self._hit_flash > 0
        body_col = COLOR_WHITE if flash else (40, 210, 140)

        if self._draw_sprite(width=self.radius * 2.3, height=self.radius * 2.3,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            pulse_r = self.radius + 6 + math.sin(self._pulse_anim * 4) * 3
            arcade.draw_circle_outline(self.x, self.y, pulse_r, (50, 240, 150, 160), 2)
            self._draw_hp_bar()
            return

        # Emerald Core
        arcade.draw_circle_filled(self.x, self.y, self.radius, body_col)
        arcade.draw_circle_filled(self.x, self.y, self.radius * 0.5, (200, 255, 220))

        # Healing Cross Emblem
        arcade.draw_line(self.x - 7, self.y, self.x + 7, self.y, (255, 255, 255), 3)
        arcade.draw_line(self.x, self.y - 7, self.x, self.y + 7, (255, 255, 255), 3)

        # Pulsing Healing Aura Ring
        pulse_r = self.radius + 6 + math.sin(self._pulse_anim * 4) * 3
        arcade.draw_circle_outline(self.x, self.y, pulse_r, (50, 240, 150, 160), 2)
        self._draw_hp_bar()
