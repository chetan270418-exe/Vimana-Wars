"""
game/systems/particles.py
High-performance procedural particle system for arcade visual juice.
Handles engine trails, bullet hit sparks, explosions, and powerup auras.
"""
import math
import random
import arcade


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "radius", "color", "decay_rate")

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 life: float, radius: float, color: tuple[int, int, int],
                 decay_rate: float = 0.96):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.radius = radius
        self.color = color
        self.decay_rate = decay_rate

    def update(self, delta_time: float) -> bool:
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.vx *= self.decay_rate
        self.vy *= self.decay_rate
        self.life -= delta_time
        return self.life > 0

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        frac = max(0.0, self.life / self.max_life)
        alpha = int(255 * frac)
        r, g, b = self.color
        arcade.draw_circle_filled(self.x + ox, self.y + oy, self.radius * frac, (r, g, b, alpha))


class ParticleManager:
    def __init__(self):
        self.particles: list[Particle] = []
        self._trail_timer = 0.0
        self.quality_multiplier = 1.0
        self.reload_settings()

    def reload_settings(self) -> None:
        try:
            from game.systems import save_system
            q = save_system.load().get("particles", "high")
            if q == "low":
                self.quality_multiplier = 0.4
            elif q == "off":
                self.quality_multiplier = 0.0
            else:
                self.quality_multiplier = 1.0
        except Exception:
            self.quality_multiplier = 1.0

    def update(self, delta_time: float) -> None:
        self.particles = [p for p in self.particles if p.update(delta_time)]

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        for p in self.particles:
            p.draw(ox, oy)

    def spawn_engine_trail(self, x: float, y: float, angle_deg: float) -> None:
        """Spawns glowing propulsion sparks behind the player vimana."""
        if self.quality_multiplier <= 0.0:
            return
        if self.quality_multiplier < 1.0 and random.random() > self.quality_multiplier:
            return
        rad = math.radians(angle_deg + 180 + random.uniform(-25, 25))
        speed = random.uniform(30, 90)
        color = random.choice([
            (100, 180, 255),  # blue plasma
            (255, 200, 80),   # golden ignition
            (255, 120, 30),   # orange flare
        ])
        self.particles.append(Particle(
            x=x, y=y,
            vx=math.cos(rad) * speed,
            vy=math.sin(rad) * speed,
            life=random.uniform(0.15, 0.35),
            radius=random.uniform(2.5, 4.5),
            color=color,
            decay_rate=0.92
        ))

    def spawn_hit_sparks(self, x: float, y: float, count: int = 5,
                         color: tuple = (255, 240, 100)) -> None:
        """Spawns sharp sparks upon bullet impacts."""
        adj_count = max(1, int(count * self.quality_multiplier)) if self.quality_multiplier > 0 else 0
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 220)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.10, 0.25),
                radius=random.uniform(1.8, 3.2),
                color=color,
                decay_rate=0.88
            ))

    def spawn_explosion(self, x: float, y: float, radius: float = 20, count: int = 24,
                        base_color: tuple = (255, 120, 30)) -> None:
        """Spawns an energetic burst of fiery debris and shockwave particles."""
        adj_count = max(2, int(count * self.quality_multiplier)) if self.quality_multiplier > 0 else 0
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            dist_factor = random.uniform(0.5, 1.8)
            speed = random.uniform(40, 160) * dist_factor
            palette = [
                base_color,
                (255, 230, 70),   # bright yellow
                (255, 60, 20),    # deep fiery red
                (180, 180, 180),  # smoke
            ]
            self.particles.append(Particle(
                x=x + random.uniform(-5, 5),
                y=y + random.uniform(-5, 5),
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.3, 0.65),
                radius=random.uniform(3.0, radius * 0.45),
                color=random.choice(palette),
                decay_rate=0.93
            ))

    def spawn_powerup_sparkle(self, x: float, y: float, color: tuple) -> None:
        """Spawns celestial aura sparkles when picking up an Astra."""
        adj_count = max(4, int(30 * self.quality_multiplier)) if self.quality_multiplier > 0 else 0
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(60, 200)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.4, 0.8),
                radius=random.uniform(2.5, 5.0),
                color=color,
                decay_rate=0.90
            ))

    def spawn_dash_flash(self, x: float, y: float, color: tuple = (140, 220, 255)) -> None:
        """Spawns a radiant flare burst at the start of a dash."""
        adj_count = max(4, int(18 * self.quality_multiplier)) if self.quality_multiplier > 0 else 0
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(120, 340)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.18, 0.35),
                radius=random.uniform(3.0, 6.0),
                color=color,
                decay_rate=0.85
            ))

    def spawn_dash_shockwave(self, x: float, y: float, color: tuple = (200, 240, 255)) -> None:
        """Spawns a ring-expanding deceleration shockwave at the end of a dash."""
        adj_count = max(6, int(22 * self.quality_multiplier)) if self.quality_multiplier > 0 else 0
        for i in range(adj_count):
            angle = (i / max(1, adj_count)) * 2 * math.pi
            speed = random.uniform(70, 150)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.2, 0.4),
                radius=random.uniform(2.5, 4.5),
                color=color,
                decay_rate=0.88
            ))
