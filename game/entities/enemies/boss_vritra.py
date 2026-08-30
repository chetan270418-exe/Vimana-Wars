"""Vritra — the Wave 20 campaign finale, a storm-serpent fortress."""
import math
import arcade
from constants import WIDTH, HEIGHT, VRITRA_HP, VRITRA_RADIUS, VRITRA_SPEED, VRITRA_SCORE, COLOR_WHITE
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossVritra(BaseEnemy):
    name = "VRITRA"
    boss_id = "vritra"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + VRITRA_RADIUS + 10,
                         hp=VRITRA_HP, speed=VRITRA_SPEED,
                         score_value=VRITRA_SCORE, radius=VRITRA_RADIUS)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.74
        self._attack_timer = 1.6
        self._angle = 0.0
        self._aim = 0.0
        self.texture = AssetManager.texture("boss_vritra.png")
        self.current_attack_name = "STORM COIL"

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        frac = self.hp / self.max_hp
        self.phase = 3 if frac <= 0.33 else 2 if frac <= 0.66 else 1
        if not self._entered:
            self.y = max(self._target_y, self.y - self.speed * 90 * delta_time)
            self._entered = self.y <= self._target_y
            return []

        self._angle += delta_time * (80 if self.phase == 3 else 45)
        self.x = WIDTH / 2 + math.sin(self._angle * 0.02) * (180 if self.phase >= 2 else 120)
        self._aim = self._angle_to_player(player_x, player_y)
        self._attack_timer -= delta_time
        if self._attack_timer > 0:
            return []
        self._attack_timer = max(0.8, 1.8 - self.phase * 0.25)
        bullets = []
        self.current_attack_name = "ASTRAL STORM!" if self.phase < 3 else "VRITRA UNLEASHED!"
        count = 10 + self.phase * 2
        for i in range(count):
            angle = self._angle + i * (360 / count)
            bullets.append(EnemyBullet(self.x, self.y, angle, speed=4.2 + self.phase * 0.5, radius=5, color=(180, 70, 255)))
        if self.phase == 3:
            for offset in (-18, 18):
                bullets.append(EnemyBullet(self.x, self.y, self._aim + offset, speed=8.0, radius=6, color=(255, 40, 140)))
        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        rad = math.radians(self._aim)
        if self._attack_timer < 0.35:
            arcade.draw_line(self.x, self.y, self.x + math.cos(rad) * 520,
                             self.y + math.sin(rad) * 520, (190, 80, 255, 150), 3)
        if self._draw_sprite(width=self.radius * 2.55, height=self.radius * 2.55,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            ring = [(100, 220, 255), (180, 80, 255), (255, 40, 140)][self.phase - 1]
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, ring, 3)
        else:
            arcade.draw_circle_filled(self.x, self.y, self.radius, COLOR_WHITE if flash else (100, 40, 180))
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, (180, 80, 255), 3)
        arcade.draw_text(self.current_attack_name, self.x,
                         self.y - self.radius - 18, (210, 100, 255),
                         font_size=9, bold=True, anchor_x="center")
