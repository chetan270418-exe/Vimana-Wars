"""
game/entities/enemies/boss_ravana.py
Boss — Ravana. Three-phase mythological emperor fight with attack telegraphs,
red danger cones, destructible energy plates, and attack announcements.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    RAVANA_HP, RAVANA_RADIUS, RAVANA_SPEED, RAVANA_SCORE,
    RAVANA_PHASE2_HP, RAVANA_PHASE3_HP,
    RAVANA_FIRE_RATE_P1, RAVANA_FIRE_RATE_P2, RAVANA_FIRE_RATE_P3,
    RAVANA_SPIRAL_RATE, RAVANA_SUMMON_RATE,
    COLOR_RAVANA, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet


class BossRavana(BaseEnemy):
    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + RAVANA_RADIUS + 10,
                         hp=RAVANA_HP, speed=RAVANA_SPEED,
                         score_value=RAVANA_SCORE, radius=RAVANA_RADIUS)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.78

        self._fire_timer = RAVANA_FIRE_RATE_P1
        self._spiral_timer = 0.0
        self._spiral_angle = 0.0
        self._summon_timer = RAVANA_SUMMON_RATE

        self._drift_dir = 1
        self._drift_timer = 0.0
        self._telegraph_timer = 0.0
        self.current_attack_name = "SPREAD BARRAGE"
        self._telegraph_aim = 0.0

    def _update_phase(self) -> None:
        frac = self.hp / self.max_hp
        if frac <= RAVANA_PHASE3_HP:
            self.phase = 3
        elif frac <= RAVANA_PHASE2_HP:
            self.phase = 2
        else:
            self.phase = 1

    def _current_fire_rate(self) -> float:
        return {1: RAVANA_FIRE_RATE_P1,
                2: RAVANA_FIRE_RATE_P2,
                3: RAVANA_FIRE_RATE_P3}[self.phase]

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        self._update_phase()

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        bullets = []

        if not self._entered:
            if self.y > self._target_y:
                self.y -= self.speed * 100.0 * delta_time
            else:
                self._entered = True
            return bullets

        # Lateral drift with delta_time
        self._drift_timer += delta_time
        drift_period = 4.0 if self.phase < 3 else 2.5
        self.x += self._drift_dir * self.speed * 25.0 * delta_time
        if self._drift_timer >= drift_period:
            self._drift_dir *= -1
            self._drift_timer = 0.0
        self.x = max(self.radius + 20, min(WIDTH - self.radius - 20, self.x))

        self._telegraph_aim = math.degrees(math.atan2(player_y - self.y, player_x - self.x))

        # Main Spread Shot with 0.5s Telegraph
        self._fire_timer -= delta_time
        if self._fire_timer <= 0:
            self._fire_timer = self._current_fire_rate()
            self.current_attack_name = "SPREAD ASTRA!"
            spread = [-20, 0, 20] if self.phase == 1 else [-28, -14, 0, 14, 28]
            for offset in spread:
                bullets.append(EnemyBullet(self.x, self.y, self._telegraph_aim + offset, speed=6.0, radius=6))

        # Phase 2+ Spiral Attack
        if self.phase >= 2:
            self._spiral_timer -= delta_time
            if self._spiral_timer <= 0:
                self._spiral_timer = RAVANA_SPIRAL_RATE
                self.current_attack_name = "SPIRAL VOID!"
                self._spiral_angle += 22.0
                for arm in range(4):
                    a = self._spiral_angle + arm * 90
                    bullets.append(EnemyBullet(self.x, self.y, a, speed=4.5, radius=5))

        # Phase 3 Summons
        summons = []
        if self.phase == 3:
            self._summon_timer -= delta_time
            if self._summon_timer <= 0:
                self._summon_timer = RAVANA_SUMMON_RATE
                self.current_attack_name = "SUMMON FLEET!"
                from game.entities.enemies.asura_fast import AsuraFast
                from game.entities.enemies.asura_kamikaze import AsuraKamikaze
                summons = [AsuraFast(self.x - 40, self.y), AsuraKamikaze(self.x + 40, self.y)]

        if summons:
            self._pending_summons = summons

        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        color = COLOR_WHITE if flash else COLOR_RAVANA
        r = self.radius

        # Attack Telegraph Aim Line
        if self._fire_timer < 0.5:
            rad = math.radians(self._telegraph_aim)
            end_x = self.x + math.cos(rad) * 450
            end_y = self.y + math.sin(rad) * 450
            arcade.draw_line(self.x, self.y, end_x, end_y, (255, 30, 50, 160), 2)
            arcade.draw_circle_outline(self.x, self.y, r + 16, (255, 50, 50, 140), 2)

        # 10 Golden Crown Spikes
        for i in range(10):
            ang = math.radians(i * 36 - 90)
            sx = self.x + math.cos(ang) * (r + 18)
            sy = self.y + math.sin(ang) * (r + 18)
            arcade.draw_circle_filled(sx, sy, 5, (255, 215, 60))

        # Main Fortress Hull
        arcade.draw_circle_filled(self.x, self.y, r, color)

        # Demonic Red Optics
        eye_color = COLOR_WHITE if not flash else COLOR_RAVANA
        arcade.draw_circle_filled(self.x - 14, self.y + 8, 6, eye_color)
        arcade.draw_circle_filled(self.x + 14, self.y + 8, 6, eye_color)
        arcade.draw_circle_filled(self.x - 14, self.y + 8, 2.5, (255, 255, 255))
        arcade.draw_circle_filled(self.x + 14, self.y + 8, 2.5, (255, 255, 255))

        # Phase indicator ring
        phase_colors = [(255, 200, 0), (255, 100, 0), (255, 0, 50)]
        ring_color = phase_colors[self.phase - 1]
        arcade.draw_circle_outline(self.x, self.y, r + 4, ring_color, 3)

        # Attack name tag
        arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 80, 80), font_size=9, bold=True, anchor_x="center")

    @property
    def pending_summons(self) -> list:
        summons = getattr(self, '_pending_summons', [])
        self._pending_summons = []
        return summons
