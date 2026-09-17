"""
game/entities/enemies/boss_hiranyakashipu.py
New Boss — Hiranyakashipu.
"""
import math
import random
import arcade
from constants import (
    WIDTH, HEIGHT,
    COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet

class BossHiranyakashipu(BaseEnemy):
    name = "HIRANYAKASHIPU"
    boss_id = "hiranyakashipu"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + 60,
                         hp=4500, speed=0.8,
                         score_value=20000, radius=50)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.75

        self._fire_timer = 2.0
        self._summon_timer = 6.0
        
        self._drift_dir = 1
        self._drift_timer = 0.0
        
        # Phase 3 specific
        self._invincibility_timer = 5.0
        self._is_invincible = False

        self.current_attack_name = "WRATH OF THE TYRANT"

    def _update_phase(self) -> None:
        frac = self.hp / self.max_hp
        if frac <= 0.33:
            if self.phase != 3:
                self.phase = 3
                self.speed = 1.8
        elif frac <= 0.66:
            if self.phase != 2:
                self.phase = 2
                self.speed = 1.3
        else:
            self.phase = 1

    def take_damage(self, amount: int) -> None:
        if getattr(self, '_is_invincible', False):
            return
        super().take_damage(amount)

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

        # Movement
        self._drift_timer += delta_time
        drift_period = 3.0 if self.phase < 3 else 1.5
        self.x += self._drift_dir * self.speed * 35.0 * delta_time
        if self._drift_timer >= drift_period:
            self._drift_dir *= -1
            self._drift_timer = 0.0
        self.x = max(self.radius + 20, min(WIDTH - self.radius - 20, self.x))

        aim_angle = math.degrees(math.atan2(player_y - self.y, player_x - self.x))

        # Attacking logic based on phase
        self._fire_timer -= delta_time
        if self._fire_timer <= 0:
            if self.phase == 1:
                self._fire_timer = 2.0
                self.current_attack_name = "SPREAD BARRAGE"
                spread = [-30, -15, 0, 15, 30]
                for offset in spread:
                    bullets.append(EnemyBullet(self.x, self.y, aim_angle + offset, speed=5.5, radius=7))
            elif self.phase == 2:
                self._fire_timer = 1.2
                self.current_attack_name = "PILLAR SLAM"
                # Triple spread
                spread = [-45, -20, 0, 20, 45, -10, 10]
                for offset in spread:
                    bullets.append(EnemyBullet(self.x, self.y, aim_angle + offset, speed=6.5, radius=8))
            elif self.phase == 3:
                self._fire_timer = 0.4
                self.current_attack_name = "RAPID ASSAULT"
                bullets.append(EnemyBullet(self.x, self.y, aim_angle + random.uniform(-10, 10), speed=8.0, radius=5))

        # Summoning logic phase 1
        summons = []
        if self.phase == 1:
            self._summon_timer -= delta_time
            if self._summon_timer <= 0:
                self._summon_timer = 6.0
                self.current_attack_name = "ASURA COLUMNS"
                from game.entities.enemies.asura_fast import AsuraFast
                for _ in range(3):
                    summons.append(AsuraFast(self.x + random.uniform(-60, 60), self.y + random.uniform(20, 60)))

        if summons:
            self._pending_summons = summons

        # Phase 3 Invincibility mechanics
        if self.phase == 3:
            self._invincibility_timer -= delta_time
            if self._is_invincible and self._invincibility_timer <= 0:
                self._is_invincible = False
                self._invincibility_timer = 5.0 # Vulnerable for 5s
            elif not self._is_invincible and self._invincibility_timer <= 0:
                self._is_invincible = True
                self._invincibility_timer = 3.0 # Invincible for 3s
            
            if self._is_invincible:
                self.current_attack_name = "IMMORTAL BOON"

        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        r = self.radius

        # Draw glowing circle in phase 3 if invincible
        if self.phase == 3 and getattr(self, '_is_invincible', False):
            arcade.draw_circle_filled(self.x, self.y, r + 20, (255, 255, 255, 100))
        elif self.phase == 3:
            # Pulsing white glow underneath
            arcade.draw_circle_filled(self.x, self.y, r + 10, (255, 255, 255, 40))

        # Body - Large red diamond
        body_color = COLOR_WHITE if flash else (180, 20, 20)
        points = [
            (self.x, self.y + r),
            (self.x + r, self.y),
            (self.x, self.y - r),
            (self.x - r, self.y)
        ]
        arcade.draw_polygon_filled(points, body_color)

        # 4 Arms N/S/E/W - thin gold rectangles
        arm_color = COLOR_WHITE if flash else (255, 215, 0)
        # N
        arcade.draw_rectangle_filled(self.x, self.y + r + 10, 8, 30, arm_color)
        # S
        arcade.draw_rectangle_filled(self.x, self.y - r - 10, 8, 30, arm_color)
        # E
        arcade.draw_rectangle_filled(self.x + r + 10, self.y, 30, 8, arm_color)
        # W
        arcade.draw_rectangle_filled(self.x - r - 10, self.y, 30, 8, arm_color)

        # Crown - 10 small gold triangles in a semicircle above
        for i in range(10):
            ang = math.radians(i * 18 + 180) # Semicircle over the top
            cx = self.x + math.cos(ang) * (r + 15)
            cy = self.y - math.sin(ang) * (r + 15) # negate sin for upper half
            
            # Triangle pointing outwards
            t_points = [
                (cx, cy),
                (cx + math.cos(ang + 1.5) * 8, cy - math.sin(ang + 1.5) * 8),
                (cx + math.cos(ang - 1.5) * 8, cy - math.sin(ang - 1.5) * 8)
            ]
            arcade.draw_polygon_filled(t_points, arm_color)
            
        # Demonic Red Optics in the middle
        eye_color = COLOR_WHITE if not flash else (255, 0, 0)
        arcade.draw_circle_filled(self.x - 10, self.y + 10, 5, eye_color)
        arcade.draw_circle_filled(self.x + 10, self.y + 10, 5, eye_color)

        # Attack name tag
        arcade.draw_text(self.current_attack_name, self.x, self.y - r - 30, (255, 200, 50), font_size=9, bold=True, anchor_x="center")

    @property
    def pending_summons(self) -> list:
        summons = getattr(self, '_pending_summons', [])
        self._pending_summons = []
        return summons
