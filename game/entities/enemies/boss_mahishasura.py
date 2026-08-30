"""Mahishasura — Wave 15 warlord with a two-phase shock assault."""
import math
import arcade
from constants import (
    WIDTH, HEIGHT, MAHISHASURA_HP, MAHISHASURA_RADIUS,
    MAHISHASURA_SPEED, MAHISHASURA_SCORE, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossMahishasura(BaseEnemy):
    name = "MAHISHASURA"
    boss_id = "mahishasura"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + MAHISHASURA_RADIUS + 10,
                         hp=MAHISHASURA_HP, speed=MAHISHASURA_SPEED,
                         score_value=MAHISHASURA_SCORE,
                         radius=MAHISHASURA_RADIUS)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.76
        self._attack_timer = 2.0
        self._drift = 1
        self._drift_timer = 0.0
        self._aim = 0.0
        self._pending_summons = []
        self.texture = AssetManager.texture("boss_mahishasura.png")
        self.current_attack_name = "SHOCKWAVE ROAR"

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        frac = self.hp / self.max_hp
        self.phase = 2 if frac <= 0.5 else 1
        if not self._entered:
            self.y = max(self._target_y, self.y - self.speed * 80 * delta_time)
            self._entered = self.y <= self._target_y
            return []

        self._drift_timer += delta_time
        self.x += self._drift * self.speed * 28 * delta_time
        if self._drift_timer >= 2.3:
            self._drift *= -1
            self._drift_timer = 0.0
        self.x = max(self.radius + 20, min(WIDTH - self.radius - 20, self.x))

        self._aim = self._angle_to_player(player_x, player_y)
        self._attack_timer -= delta_time
        if self._attack_timer > 0:
            return []
        self._attack_timer = 1.9 if self.phase == 2 else 2.5
        bullets = []
        if self.phase == 1:
            self.current_attack_name = "SHOCKWAVE ROAR!"
            for i in range(14):
                bullets.append(EnemyBullet(self.x, self.y, i * (360 / 14), speed=4.8, radius=5, color=(255, 140, 40)))
        else:
            self.current_attack_name = "WARLORD'S BARRAGE!"
            for offset in (-32, -16, 0, 16, 32):
                bullets.append(EnemyBullet(self.x, self.y, self._aim + offset, speed=7.0, radius=6, color=(255, 60, 60)))
            from game.entities.enemies.asura_fast import AsuraFast
            self._pending_summons = [AsuraFast(self.x - 45, self.y), AsuraFast(self.x + 45, self.y)]
        return bullets

    @property
    def pending_summons(self) -> list:
        summons, self._pending_summons = self._pending_summons, []
        return summons

    def draw(self) -> None:
        flash = self._hit_flash > 0
        if self._attack_timer < 0.35:
            rad = math.radians(self._aim)
            arcade.draw_line(self.x, self.y, self.x + math.cos(rad) * 500,
                             self.y + math.sin(rad) * 500, (255, 60, 40, 150), 3)
        if self._draw_sprite(width=self.radius * 2.5, height=self.radius * 2.5,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            ring = (255, 180, 40) if self.phase == 1 else (255, 50, 50)
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, ring, 3)
        else:
            body = COLOR_WHITE if flash else (190, 60, 30)
            arcade.draw_circle_filled(self.x, self.y, self.radius, body)
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, (255, 180, 40), 3)
        arcade.draw_text(self.current_attack_name, self.x,
                         self.y - self.radius - 18, (255, 140, 50),
                         font_size=9, bold=True, anchor_x="center")
