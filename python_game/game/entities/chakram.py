"""
game/entities/chakram.py
Sudarshana Chakram — Spinning divine razor blade ability.
Flies outwards in facing direction, deflects enemy bullets, slices enemies, and returns to player.
"""
import math
import arcade
from constants import WIDTH, HEIGHT


class Chakram:
    def __init__(self, start_x: float, start_y: float, angle_deg: float):
        self.x = start_x
        self.y = start_y
        self.radius = 16
        self.damage = 55
        self.alive = True
        self.angle_deg = angle_deg
        self.spin_angle = 0.0

        # Flight dynamics: Outward phase -> Return phase
        self._state = "OUTWARD"
        self._speed = 12.0
        self._distance_traveled = 0.0
        self._max_distance = 280.0
        self._hit_cooldowns: dict = {}  # enemy_id -> cooldown

    def update(self, delta_time: float, player_x: float, player_y: float) -> None:
        self.spin_angle += 720.0 * delta_time  # 2 full rotations per second

        # Decrement hit cooldowns so it doesn't hit 60 times a second on the same enemy
        for eid in list(self._hit_cooldowns.keys()):
            self._hit_cooldowns[eid] -= delta_time
            if self._hit_cooldowns[eid] <= 0:
                del self._hit_cooldowns[eid]

        speed_step = self._speed * 60.0 * delta_time

        if self._state == "OUTWARD":
            rad = math.radians(self.angle_deg)
            self.x += math.cos(rad) * speed_step
            self.y += math.sin(rad) * speed_step
            self._distance_traveled += speed_step

            if self._distance_traveled >= self._max_distance or not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
                self._state = "RETURNING"

        elif self._state == "RETURNING":
            dx = player_x - self.x
            dy = player_y - self.y
            dist = math.hypot(dx, dy)

            if dist < 22:
                self.alive = False  # Caught back by player!
                return

            return_speed_step = 14.0 * 60.0 * delta_time
            self.x += (dx / dist) * return_speed_step
            self.y += (dy / dist) * return_speed_step

    def can_damage(self, enemy) -> bool:
        eid = id(enemy)
        if eid in self._hit_cooldowns:
            return False
        self._hit_cooldowns[eid] = 0.25  # 250ms hit cooldown per enemy
        return True

    def draw(self) -> None:
        # Golden core
        arcade.draw_circle_filled(self.x, self.y, self.radius, (255, 220, 50))
        arcade.draw_circle_filled(self.x, self.y, self.radius * 0.45, (255, 255, 255))

        # Spinning razor teeth (8 blades)
        for i in range(8):
            rad = math.radians(self.spin_angle + i * 45)
            tx = self.x + math.cos(rad) * (self.radius + 6)
            ty = self.y + math.sin(rad) * (self.radius + 6)
            arcade.draw_triangle_filled(
                self.x, self.y,
                tx, ty,
                self.x + math.cos(rad + 0.3) * (self.radius + 2),
                self.y + math.sin(rad + 0.3) * (self.radius + 2),
                (255, 160, 20)
            )

        # Outer plasma glow
        arcade.draw_circle_outline(self.x, self.y, self.radius + 8, (255, 240, 100, 180), 2)
