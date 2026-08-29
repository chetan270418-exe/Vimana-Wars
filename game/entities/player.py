"""
game/entities/player.py
The player's Vimana — enhanced with delta_time physics, velocity smoothing,
banking lean, ship archetype stats, multiple dash charges, and combat juice.
"""
import math
import time
import arcade
from constants import (
    WIDTH, HEIGHT,
    PLAYER_MAX_HP, PLAYER_RADIUS,
    PLAYER_INVINCIBILITY_TIME, SHIELD_MAX_HITS,
    COLOR_SHIELD, COLOR_WHITE,
)


class Player:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.0
        self.bank_tilt = 0.0
        self.radius = PLAYER_RADIUS
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.alive = True

        # Ship class & difficulty tunings
        self.speed_stat = 320.0       # pixels / second
        self.fire_rate_stat = 0.15    # seconds per shot
        self.dash_charges_max = 1
        self.dash_charges = 1
        self.dash_cooldown_max = 2.2
        self.dash_cooldown_timer = 0.0
        self.dmg_taken_mult = 1.0     # Scaled by difficulty setting

        # Input
        self.keys_pressed: set = set()
        self.mouse_x = WIDTH / 2
        self.mouse_y = HEIGHT / 2
        self.mouse_held = False
        self.joy_dx = 0.0
        self.joy_dy = 0.0
        self.joy_aim_angle: float | None = None

        # Shooting & Recoil
        self._shoot_timer = 0.0
        self._recoil_dist = 0.0
        self.muzzle_flash_timer = 0.0

        # Dash state
        self.is_dashing = False
        self._dash_duration = 0.0
        self._dash_vx = 0.0
        self._dash_vy = 0.0
        self.afterimages: list[dict] = []

        # Ability 2 (Chakram)
        self.chakram_cooldown_max = 6.0
        self.chakram_cooldown_timer = 0.0

        # I-frames & flash
        self.invincible_timer = 0.0
        self._flash_timer = 0.0

        # Power-up state
        self.active_powerup = None
        self.shield_hits = 0
        self.spread_active = False
        self.speed_boosted = False
        self.bomb_count = 0

        # Stats
        self.enemies_killed = 0
        self.total_score = 0

    def apply_ship_class(self, sdata: dict) -> None:
        self.max_hp = sdata["hp"]
        self.hp = self.max_hp
        self.speed_stat = sdata["speed"] * 60.0
        self.fire_rate_stat = sdata["fire_rate"]
        self.dash_cooldown_max = sdata["dash_cooldown"]
        if sdata["id"] == "garuda":
            self.dash_charges_max = 2
            self.dash_charges = 2

    # ── Per-frame update with delta_time physics ─────────────────────────

    def update(self, delta_time: float) -> None:
        if not self.alive:
            return

        self._update_movement(delta_time)
        self._update_aim()
        self._update_timers(delta_time)
        self._update_afterimages(delta_time)

    def _update_movement(self, delta_time: float) -> None:
        # Dash state physics
        if self.is_dashing:
            self.x += self._dash_vx * delta_time
            self.y += self._dash_vy * delta_time
            self._dash_duration -= delta_time

            self.afterimages.append({
                "x": self.x, "y": self.y, "angle": self.angle, "life": 0.22, "max_life": 0.22
            })

            if self._dash_duration <= 0:
                self.is_dashing = False

            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
            return

        # Target input direction
        inp_x, inp_y = 0.0, 0.0
        k = self.keys_pressed
        if arcade.key.W in k or arcade.key.UP    in k: inp_y += 1
        if arcade.key.S in k or arcade.key.DOWN  in k: inp_y -= 1
        if arcade.key.A in k or arcade.key.LEFT  in k: inp_x -= 1
        if arcade.key.D in k or arcade.key.RIGHT in k: inp_x += 1

        if abs(self.joy_dx) > 0.15: inp_x += self.joy_dx
        if abs(self.joy_dy) > 0.15: inp_y += self.joy_dy

        length = math.hypot(inp_x, inp_y)
        if length > 1.0:
            inp_x /= length
            inp_y /= length

        target_speed = self.speed_stat * (1.5 if self.speed_boosted else 1.0)
        target_vx = inp_x * target_speed
        target_vy = inp_y * target_speed

        # Smooth acceleration and drag
        accel = 16.0
        self.vx += (target_vx - self.vx) * min(1.0, accel * delta_time)
        self.vy += (target_vy - self.vy) * min(1.0, accel * delta_time)

        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        # Bank lean smoothing
        target_tilt = -self.vx * 0.06
        self.bank_tilt += (target_tilt - self.bank_tilt) * min(1.0, 12.0 * delta_time)

        # Screen clamp
        self.x = max(self.radius, min(WIDTH  - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def _update_aim(self) -> None:
        if self.joy_aim_angle is not None:
            self.angle = self.joy_aim_angle
        else:
            dx = self.mouse_x - self.x
            dy = self.mouse_y - self.y
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.angle = math.degrees(math.atan2(dy, dx))

    def _update_timers(self, delta_time: float) -> None:
        if self._shoot_timer > 0:
            self._shoot_timer -= delta_time
        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= delta_time

        # Dash charge recharge
        if self.dash_charges < self.dash_charges_max:
            self.dash_cooldown_timer -= delta_time
            if self.dash_cooldown_timer <= 0:
                self.dash_charges += 1
                if self.dash_charges < self.dash_charges_max:
                    self.dash_cooldown_timer = self.dash_cooldown_max
                else:
                    self.dash_cooldown_timer = 0.0

        if self.chakram_cooldown_timer > 0:
            self.chakram_cooldown_timer -= delta_time
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time
        if self._flash_timer > 0:
            self._flash_timer -= delta_time
        if self._recoil_dist > 0:
            self._recoil_dist = max(0.0, self._recoil_dist - delta_time * 28)

        if self.active_powerup:
            self.active_powerup.update(delta_time)
            if self.active_powerup.expired:
                self._expire_powerup()

    def _update_afterimages(self, delta_time: float) -> None:
        for ghost in self.afterimages:
            ghost["life"] -= delta_time
        self.afterimages = [g for g in self.afterimages if g["life"] > 0]

    # ── Active Abilities ─────────────────────────────────────────────────

    def trigger_dash(self) -> bool:
        if self.dash_charges <= 0 or not self.alive:
            return False

        self.dash_charges -= 1
        if self.dash_cooldown_timer <= 0:
            self.dash_cooldown_timer = self.dash_cooldown_max

        self.is_dashing = True
        self._dash_duration = 0.22
        self.invincible_timer = 0.28

        # Direction from velocity or facing angle
        dx, dy = self.vx, self.vy
        if math.hypot(dx, dy) < 10:
            rad = math.radians(self.angle)
            dx = math.cos(rad)
            dy = math.sin(rad)

        dist = math.hypot(dx, dy)
        dash_speed = 780.0
        self._dash_vx = (dx / dist) * dash_speed
        self._dash_vy = (dy / dist) * dash_speed
        return True

    def trigger_chakram(self) -> bool:
        if self.chakram_cooldown_timer > 0 or not self.alive:
            return False
        self.chakram_cooldown_timer = self.chakram_cooldown_max
        return True

    @property
    def dash_ready(self) -> bool:
        return self.dash_charges > 0

    @property
    def dash_ratio(self) -> float:
        if self.dash_charges == self.dash_charges_max:
            return 1.0
        return max(0.0, 1.0 - (self.dash_cooldown_timer / self.dash_cooldown_max))

    @property
    def chakram_ready(self) -> bool:
        return self.chakram_cooldown_timer <= 0

    @property
    def chakram_ratio(self) -> float:
        return max(0.0, 1.0 - (self.chakram_cooldown_timer / self.chakram_cooldown_max))

    # ── Shooting ─────────────────────────────────────────────────────────

    def get_bullets_to_fire(self) -> list:
        if not self.mouse_held or self._shoot_timer > 0 or not self.alive or self.is_dashing:
            return []

        self._shoot_timer = self.fire_rate_stat
        self._recoil_dist = 4.0
        self.muzzle_flash_timer = 0.06

        if self.spread_active:
            return [self.angle - 15.0, self.angle, self.angle + 15.0]
        return [self.angle]

    # ── Damage & Healing ─────────────────────────────────────────────────

    def take_damage(self, amount: int) -> bool:
        if not self.alive or self.invincible_timer > 0:
            return False

        if self.shield_hits > 0:
            self.shield_hits -= 1
            self.invincible_timer = 0.25
            if self.shield_hits == 0 and self.active_powerup:
                self._expire_powerup()
            return False

        effective_damage = max(1, int(amount * self.dmg_taken_mult))
        self.hp -= effective_damage
        self._flash_timer = 0.12
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME

        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        return True

    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    # ── Power-ups ────────────────────────────────────────────────────────

    def apply_powerup(self, ptype) -> None:
        from game.entities.powerup import PowerUpType, PowerUpEffect

        if ptype == PowerUpType.HEALTH:
            self.heal(35)
            return
        if ptype == PowerUpType.BOMB:
            self.bomb_count += 1
            return

        if self.active_powerup and not self.active_powerup.expired:
            self._expire_powerup()

        self.active_powerup = PowerUpEffect(ptype)
        if ptype == PowerUpType.SHIELD:
            self.shield_hits = SHIELD_MAX_HITS
        elif ptype == PowerUpType.SPREAD:
            self.spread_active = True
        elif ptype == PowerUpType.SPEED:
            self.speed_boosted = True

    def _expire_powerup(self) -> None:
        from game.entities.powerup import PowerUpType
        if self.active_powerup:
            t = self.active_powerup.type
            if t == PowerUpType.SHIELD:
                self.shield_hits = 0
            elif t == PowerUpType.SPREAD:
                self.spread_active = False
            elif t == PowerUpType.SPEED:
                self.speed_boosted = False
        self.active_powerup = None

    def use_bomb(self) -> bool:
        if self.bomb_count > 0:
            self.bomb_count -= 1
            return True
        return False

    # ── Render with Muzzle Flash & Dynamic Exhaust ───────────────────────

    def draw(self) -> None:
        if not self.alive:
            return

        # 1. Afterimage ghost trails
        for ghost in self.afterimages:
            g_alpha = int(130 * (ghost["life"] / ghost["max_life"]))
            self._draw_ship_body(ghost["x"], ghost["y"], ghost["angle"], (100, 200, 255, g_alpha))

        # 2. Blink during i-frames
        if self.invincible_timer > 0 and self._flash_timer <= 0 and not self.is_dashing:
            if int(time.time() * 12) % 2 == 0:
                return

        # 3. Position with recoil
        rad = math.radians(self.angle)
        draw_x = self.x - math.cos(rad) * self._recoil_dist
        draw_y = self.y - math.sin(rad) * self._recoil_dist

        color = COLOR_WHITE if self._flash_timer > 0 else (255, 215, 80) if self.spread_active else (210, 225, 255)
        self._draw_ship_body(draw_x, draw_y, self.angle + self.bank_tilt, color)

        # 4. Muzzle Flash on gun tip
        if self.muzzle_flash_timer > 0:
            tip_x = self.x + math.cos(rad) * (self.radius + 16)
            tip_y = self.y + math.sin(rad) * (self.radius + 16)
            arcade.draw_circle_filled(tip_x, tip_y, 7, (255, 240, 150))
            arcade.draw_circle_filled(tip_x, tip_y, 4, (255, 255, 255))

        # 5. Shield aura
        if self.shield_hits > 0:
            arcade.draw_circle_outline(self.x, self.y, self.radius + 12, COLOR_SHIELD, 2)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 12, (60, 160, 255, 35))

    def _draw_ship_body(self, sx: float, sy: float, angle_deg: float, main_color: tuple) -> None:
        r = self.radius
        angle_rad = math.radians(angle_deg)

        # Main Forward Nose
        tip_x = sx + math.cos(angle_rad) * r * 1.9
        tip_y = sy + math.sin(angle_rad) * r * 1.9

        # Swept-Back Wings
        wing_l_rad = angle_rad + math.radians(140)
        wing_r_rad = angle_rad - math.radians(140)
        wing_l_x = sx + math.cos(wing_l_rad) * r * 1.3
        wing_l_y = sy + math.sin(wing_l_rad) * r * 1.3
        wing_r_x = sx + math.cos(wing_r_rad) * r * 1.3
        wing_r_y = sy + math.sin(wing_r_rad) * r * 1.3

        # Inner Chassis
        arcade.draw_triangle_filled(tip_x, tip_y, wing_l_x, wing_l_y, wing_r_x, wing_r_y, main_color)
        arcade.draw_line(tip_x, tip_y, wing_l_x, wing_l_y, (255, 215, 60), 2)
        arcade.draw_line(tip_x, tip_y, wing_r_x, wing_r_y, (255, 215, 60), 2)

        # Cockpit Canopy
        cockpit_x = sx + math.cos(angle_rad) * r * 0.5
        cockpit_y = sy + math.sin(angle_rad) * r * 0.5
        arcade.draw_circle_filled(cockpit_x, cockpit_y, 4.5, (100, 240, 255))
        arcade.draw_circle_filled(cockpit_x, cockpit_y, 2.5, (255, 255, 255))

        # Dynamic Dual Plasma Thrusters
        rear_l_rad = angle_rad + math.radians(165)
        rear_r_rad = angle_rad - math.radians(165)
        t_l_x = sx + math.cos(rear_l_rad) * r * 0.7
        t_l_y = sy + math.sin(rear_l_rad) * r * 0.7
        t_r_x = sx + math.cos(rear_r_rad) * r * 0.7
        t_r_y = sy + math.sin(rear_r_rad) * r * 0.7

        cur_speed_len = math.hypot(self.vx, self.vy)
        flame_len = 5 + (cur_speed_len / 400.0) * 8
        thruster_col = (255, 160, 40) if self.speed_boosted or self.is_dashing else (100, 180, 255)

        # Jet flares
        jet_rad = angle_rad + math.pi
        arcade.draw_line(t_l_x, t_l_y, t_l_x + math.cos(jet_rad) * flame_len, t_l_y + math.sin(jet_rad) * flame_len, thruster_col, 3)
        arcade.draw_line(t_r_x, t_r_y, t_r_x + math.cos(jet_rad) * flame_len, t_r_y + math.sin(jet_rad) * flame_len, thruster_col, 3)
        arcade.draw_circle_filled(t_l_x, t_l_y, 3.5, (255, 255, 255))
        arcade.draw_circle_filled(t_r_x, t_r_y, 3.5, (255, 255, 255))
