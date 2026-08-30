"""
game/entities/enemies/boss_kumbhakarna.py
Mini-Boss — Kumbhakarna (Wave 5 Armored Titan).
Features charging telegraph cones, shockwave tremor rings, and mace flurries.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    KUMBHAKARNA_HP, KUMBHAKARNA_RADIUS, KUMBHAKARNA_SPEED, KUMBHAKARNA_SCORE,
    COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossKumbhakarna(BaseEnemy):
    name = "KUMBHAKARNA"
    boss_id = "kumbhakarna"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + KUMBHAKARNA_RADIUS + 10,
                         hp=KUMBHAKARNA_HP, speed=KUMBHAKARNA_SPEED,
                         score_value=KUMBHAKARNA_SCORE, radius=KUMBHAKARNA_RADIUS)
        self._target_y = HEIGHT * 0.75
        self._entered = False

        self._attack_timer = 2.0
        self._attack_mode = 0  # 0: Radial Mace, 1: Tremor 5-way, 2: Charge Dash
        self._charge_vx = 0.0
        self._charge_vy = 0.0
        self._charge_duration = 0.0
        self._charge_telegraph_timer = 0.0
        self._charge_aim = 0.0
        self._is_charging = False
        self.current_attack_name = "RADIAL MACE"
        self.texture = AssetManager.texture("boss_kumbhakarna.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        bullets = []

        if not self._entered:
            if self.y > self._target_y:
                self.y -= self.speed * 80.0 * delta_time
            else:
                self._entered = True
            return bullets

        # Charge Telegraph Phase (locked warning before dashing)
        if self._charge_telegraph_timer > 0:
            self._charge_telegraph_timer -= delta_time
            self.current_attack_name = "⚠ CHARGE INCOMING!"
            self._charge_aim = self._angle_to_player(player_x, player_y)
            if self._charge_telegraph_timer <= 0:
                rad = math.radians(self._charge_aim)
                charge_speed = 620.0
                self._charge_vx = math.cos(rad) * charge_speed
                self._charge_vy = math.sin(rad) * charge_speed
                self._charge_duration = 0.65
                self._is_charging = True
                self.current_attack_name = "TITAN CHARGE!"
            return bullets

        # Charge Dash Execution
        if self._is_charging:
            self.x += self._charge_vx * delta_time
            self.y += self._charge_vy * delta_time
            self._charge_duration -= delta_time
            if self._charge_duration <= 0:
                self._is_charging = False
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
            return bullets

        # Normal tracking movement
        self._move_toward(player_x, self._target_y, delta_time)

        self._attack_timer -= delta_time
        if self._attack_timer <= 0:
            self._attack_timer = 3.4
            self._attack_mode = (self._attack_mode + 1) % 3

            if self._attack_mode == 0:
                # Radial Mace Burst
                self.current_attack_name = "MACE BURST!"
                for i in range(12):
                    ang = i * 30
                    bullets.append(EnemyBullet(self.x, self.y, ang, speed=4.5, radius=5, color=(255, 140, 30)))

            elif self._attack_mode == 1:
                # Tremor 5-way aimed blast
                self.current_attack_name = "TREMOR SHOCK!"
                aim = self._angle_to_player(player_x, player_y)
                for offset in (-30, -15, 0, 15, 30):
                    bullets.append(EnemyBullet(self.x, self.y, aim + offset, speed=6.0, radius=6, color=(255, 60, 40)))

            elif self._attack_mode == 2:
                # Enter Charge Telegraph
                self._charge_telegraph_timer = 0.9
                self._charge_aim = self._angle_to_player(player_x, player_y)
                self.current_attack_name = "⚠ CHARGE INCOMING!"

        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        body_col = COLOR_WHITE if flash else (180, 100, 20)

        # Draw Clear Red Danger Line & Warning Cone when telegraphing charge
        if self._charge_telegraph_timer > 0:
            rad = math.radians(self._charge_aim)
            end_x = self.x + math.cos(rad) * 600
            end_y = self.y + math.sin(rad) * 600
            arcade.draw_line(self.x, self.y, end_x, end_y, (255, 40, 40, 190), 4)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 20, (255, 40, 40, 90))
            arcade.draw_circle_outline(self.x, self.y, self.radius + 22, (255, 80, 80), 2)

        if self._draw_sprite(width=self.radius * 2.5, height=self.radius * 2.5,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            arcade.draw_circle_outline(self.x, self.y, self.radius + 4, (255, 200, 60), 3)
            arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 160, 40), font_size=9, bold=True, anchor_x="center")
            return

        # Heavy Armored Titan Hull
        arcade.draw_circle_filled(self.x, self.y, self.radius, body_col)
        arcade.draw_circle_outline(self.x, self.y, self.radius + 4, (255, 200, 60), 3)

        # Armored Mace Spikes
        for i in range(8):
            ang = math.radians(i * 45)
            sx = self.x + math.cos(ang) * (self.radius + 8)
            sy = self.y + math.sin(ang) * (self.radius + 8)
            arcade.draw_circle_filled(sx, sy, 6, (120, 70, 20))

        arcade.draw_circle_filled(self.x, self.y, 8, (255, 180, 40))
        arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 160, 40), font_size=9, bold=True, anchor_x="center")
