"""
game/systems/environmental_hazards.py
Dynamic realm-specific cosmic hazards and environmental anomalies.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT


class EnvironmentalHazardManager:
    def __init__(self):
        self.asteroids: list[dict] = []
        self.solar_beams: list[dict] = []
        self.spawn_timer = 0.0

    def update(self, delta_time: float, wave_num: int, player, enemies: list, bullets: list) -> None:
        realm_id = ((wave_num - 1) % 10) + 1
        self.spawn_timer += delta_time

        # ── Dandaka Void (Waves 7–9): Astral Crystal Asteroids ─────────
        if 7 <= realm_id <= 9:
            if self.spawn_timer >= 3.5 and len(self.asteroids) < 4:
                self.spawn_timer = 0.0
                self.asteroids.append({
                    "x": random.uniform(100, WIDTH - 100),
                    "y": HEIGHT + 40,
                    "vx": random.uniform(-15, 15),
                    "vy": random.uniform(-25, -45),
                    "radius": random.uniform(22, 36),
                    "hp": 60,
                    "rot": 0.0,
                })

        for ast in self.asteroids:
            ast["x"] += ast["vx"] * delta_time
            ast["y"] += ast["vy"] * delta_time
            ast["rot"] += 20 * delta_time

            # Bullet collisions with asteroids (acts as tactical cover)
            for b in bullets:
                if b.alive and math.hypot(b.x - ast["x"], b.y - ast["y"]) < b.radius + ast["radius"]:
                    b.alive = False
                    ast["hp"] -= 20

        self.asteroids = [a for a in self.asteroids if a["hp"] > 0 and a["y"] > -50]

        # ── Swarga (Waves 1–3): Celestial Solar Rays ───────────────────
        if 1 <= realm_id <= 3:
            if self.spawn_timer >= 5.5 and len(self.solar_beams) < 2:
                self.spawn_timer = 0.0
                self.solar_beams.append({
                    "x": random.uniform(150, WIDTH - 150),
                    "w": 35,
                    "timer": 2.2,
                    "warning": True,
                })

        for beam in self.solar_beams:
            beam["timer"] -= delta_time
            if beam["timer"] < 1.0:
                beam["warning"] = False
                # Damage anything inside active solar ray
                if abs(player.x - beam["x"]) < beam["w"] and not player.is_dashing:
                    player.take_damage(1)  # Light continuous burn

        self.solar_beams = [b for b in self.solar_beams if b["timer"] > 0]

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        # Draw Asteroids
        for ast in self.asteroids:
            arcade.draw_circle_filled(ast["x"] + ox, ast["y"] + oy, ast["radius"], (70, 45, 95))
            arcade.draw_circle_outline(ast["x"] + ox, ast["y"] + oy, ast["radius"], (140, 90, 190), 2)
            arcade.draw_circle_filled(ast["x"] + ox - 4, ast["y"] + oy + 4, ast["radius"] * 0.4, (95, 65, 130))

        # Draw Solar Beams
        for beam in self.solar_beams:
            bx = beam["x"] + ox
            bw = beam["w"]
            if beam["warning"]:
                arcade.draw_lrbt_rectangle_filled(bx - bw // 2, bx + bw // 2, 0, HEIGHT, (255, 220, 100, 35))
                arcade.draw_line(bx, 0, bx, HEIGHT, (255, 240, 150, 120), 1)
            else:
                arcade.draw_lrbt_rectangle_filled(bx - bw // 2, bx + bw // 2, 0, HEIGHT, (255, 235, 120, 160))
                arcade.draw_lrbt_rectangle_filled(bx - bw // 4, bx + bw // 4, 0, HEIGHT, (255, 255, 255, 220))
