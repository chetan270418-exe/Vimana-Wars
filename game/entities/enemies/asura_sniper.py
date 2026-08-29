"""
game/entities/enemies/asura_sniper.py
Asura Void Sniper — Keeps maximum range, paints target with a red aiming laser,
and fires an ultra-high-velocity piercing beam bullet with clear audio/visual telegraphs.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_WHITE
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet


class AsuraSniper(BaseEnemy):
    def __init__(self, safe_player_x: float = WIDTH / 2, safe_player_y: float = HEIGHT / 2):
        x, y = BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y, hp=40, speed=1.2, score_value=220, radius=16)
        self._charge_timer = 2.8
        self._is_aiming = False
        self._aim_angle = 0.0

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        # Stay at long range (~320px)
        dist = math.hypot(player_x - self.x, player_y - self.y)
        if dist < 260:
            # Back up
            self._move_toward(self.x - (player_x - self.x), self.y - (player_y - self.y), delta_time)
        elif dist > 380:
            self._move_toward(player_x, player_y, delta_time)

        self._aim_angle = self._angle_to_player(player_x, player_y)
        self._charge_timer -= delta_time

        bullets = []
        # Aiming telegraph during last 1.0s before firing
        if self._charge_timer <= 1.0:
            self._is_aiming = True

        if self._charge_timer <= 0:
            self._charge_timer = 3.0
            self._is_aiming = False
            # Fire high speed sniper beam
            b = EnemyBullet(self.x, self.y, self._aim_angle, speed=13.0, damage=22, radius=6, color=(255, 40, 90))
            bullets.append(b)

        return bullets

    def draw(self) -> None:
        self._draw_elite_aura()
        flash = self._hit_flash > 0
        body_col = COLOR_WHITE if flash else (180, 40, 100)

        # Draw red laser aiming telegraph line
        if self._is_aiming:
            rad = math.radians(self._aim_angle)
            end_x = self.x + math.cos(rad) * 600
            end_y = self.y + math.sin(rad) * 600
            arcade.draw_line(self.x, self.y, end_x, end_y, (255, 30, 70, 180), 2)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 4, (255, 60, 100, 90))

        # Diamond Sniper Chassis
        rad = math.radians(self._aim_angle)
        tip_x = self.x + math.cos(rad) * (self.radius + 10)
        tip_y = self.y + math.sin(rad) * (self.radius + 10)

        arcade.draw_circle_filled(self.x, self.y, self.radius, body_col)
        arcade.draw_line(self.x, self.y, tip_x, tip_y, (255, 80, 120), 4)
        arcade.draw_circle_filled(self.x, self.y, 4, (255, 255, 255))
        self._draw_hp_bar()
