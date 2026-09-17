"""
game/entities/powerup.py
Collectables that spawn on the map and give the player timed or instant effects.
"""
import math
import random
import arcade
from enum import Enum, auto
from constants import (
    WIDTH, HEIGHT,
    POWERUP_RADIUS,
    SHIELD_DURATION, SPREAD_DURATION, SPEED_DURATION,
    COLOR_POWERUP_SHIELD, COLOR_POWERUP_SPREAD, COLOR_POWERUP_SPEED,
    COLOR_POWERUP_HEALTH, COLOR_POWERUP_BOMB, COLOR_POWERUP_OVERDRIVE,
    COLOR_WHITE,
)


class PowerUpType(Enum):
    SHIELD = auto()   # Kavach  — absorbs 3 hits for 10s
    SPREAD = auto()   # Agneyastra — 3-bullet spread for 8s
    SPEED  = auto()   # Vayavyastra — +60% speed for 6s
    HEALTH = auto()   # Amrita — instant +30 HP
    BOMB   = auto()   # Brahmastra — clear all enemies on screen
    OVERDRIVE = auto()  # Astra Overdrive — rapid fire for 8s


# Duration in seconds for each timed type (instant types use 0)
_DURATIONS = {
    PowerUpType.SHIELD: SHIELD_DURATION,
    PowerUpType.SPREAD: SPREAD_DURATION,
    PowerUpType.SPEED:  SPEED_DURATION,
    PowerUpType.HEALTH: 0.0,
    PowerUpType.BOMB:   0.0,
    PowerUpType.OVERDRIVE: 8.0,
}

_COLORS = {
    PowerUpType.SHIELD: COLOR_POWERUP_SHIELD,
    PowerUpType.SPREAD: COLOR_POWERUP_SPREAD,
    PowerUpType.SPEED:  COLOR_POWERUP_SPEED,
    PowerUpType.HEALTH: COLOR_POWERUP_HEALTH,
    PowerUpType.BOMB:   COLOR_POWERUP_BOMB,
    PowerUpType.OVERDRIVE: COLOR_POWERUP_OVERDRIVE,
}

_LABELS = {
    PowerUpType.SHIELD: "KVH",   # Kavach
    PowerUpType.SPREAD: "AGN",   # Agneyastra
    PowerUpType.SPEED:  "VAY",   # Vayavyastra
    PowerUpType.HEALTH: "AMR",   # Amrita
    PowerUpType.BOMB:   "BRM",   # Brahmastra
    PowerUpType.OVERDRIVE: "OVR",  # Astra Overdrive
}


class PowerUpEffect:
    """
    Tracks a timed power-up effect that is active on the player.
    Instant effects (HEALTH, BOMB) should never be stored here.
    """
    def __init__(self, ptype: PowerUpType):
        self.type = ptype
        self.duration = _DURATIONS[ptype]
        self.remaining = self.duration
        self.expired = False

    def update(self, delta_time: float) -> None:
        if self.expired:
            return
        self.remaining -= delta_time
        if self.remaining <= 0:
            self.remaining = 0
            self.expired = True

    @property
    def fraction(self) -> float:
        """0.0 (expired) → 1.0 (full)"""
        if self.duration <= 0:
            return 0.0
        return max(0.0, self.remaining / self.duration)


class PowerUp:
    """
    A collectable that lives on the game map until the player touches it.
    Spawns at a random edge position, pulses visually.
    """

    def __init__(self, ptype: PowerUpType = None):
        self.type = ptype or random.choice(list(PowerUpType))
        self.radius = POWERUP_RADIUS
        self.x, self.y = self._random_position()
        self.alive = True
        self._pulse_timer = 0.0
        self._color = _COLORS[self.type]
        self._label = _LABELS[self.type]

    @staticmethod
    def _random_position():
        margin = POWERUP_RADIUS + 30
        side = random.randint(0, 3)
        if side == 0:   # top
            return random.uniform(margin, WIDTH - margin), HEIGHT - margin
        elif side == 1: # bottom
            return random.uniform(margin, WIDTH - margin), margin
        elif side == 2: # left
            return margin, random.uniform(margin, HEIGHT - margin)
        else:           # right
            return WIDTH - margin, random.uniform(margin, HEIGHT - margin)

    def update(self, delta_time: float) -> None:
        self._pulse_timer += delta_time

    def draw(self) -> None:
        r, g, b = self._color
        pulse = 0.5 + 0.5 * math.sin(self._pulse_timer * 4)

        # 1. Upward Celestial Light Beacon Beam
        beam_alpha = int(40 + 35 * pulse)
        arcade.draw_line(self.x, self.y, self.x, self.y + 100, (r, g, b, beam_alpha), 4)
        arcade.draw_line(self.x, self.y, self.x, self.y + 60, (255, 255, 255, beam_alpha + 30), 2)

        # 2. Pulsing outer glow
        glow_r = self.radius + 6 + pulse * 6
        arcade.draw_circle_filled(self.x, self.y, glow_r, (r, g, b, 60))

        # 3. Rotating Diamond Orbit Ring
        rot = self._pulse_timer * 60.0  # degrees
        for i in range(4):
            ang = math.radians(rot + i * 90)
            dx = self.x + math.cos(ang) * (self.radius + 8)
            dy = self.y + math.sin(ang) * (self.radius + 8)
            arcade.draw_circle_filled(dx, dy, 2.5, (255, 255, 255, 200))

        # 4. Rotating 3D-looking astral cube. The faces make pickups readable
        # even in a busy bullet field and give every ability a collectible,
        # game-like silhouette instead of another plain orb.
        half = self.radius * 0.72
        depth = 7.0
        front_center = (self.x, self.y)
        back_center = (self.x + depth * 0.75, self.y + depth * 0.55)
        angle = math.radians(rot)

        def diamond(center, size):
            cx, cy = center
            return [
                (cx + math.cos(angle + math.pi / 2) * size,
                 cy + math.sin(angle + math.pi / 2) * size),
                (cx + math.cos(angle) * size,
                 cy + math.sin(angle) * size),
                (cx + math.cos(angle - math.pi / 2) * size,
                 cy + math.sin(angle - math.pi / 2) * size),
                (cx + math.cos(angle + math.pi) * size,
                 cy + math.sin(angle + math.pi) * size),
            ]

        front = diamond(front_center, half)
        back = diamond(back_center, half * 0.88)
        face_colors = (
            (min(255, r + 35), min(255, g + 35), min(255, b + 35), 235),
            (max(0, r - 25), max(0, g - 25), max(0, b - 25), 235),
            (max(0, r - 45), max(0, g - 45), max(0, b - 45), 235),
            (min(255, r + 15), min(255, g + 15), min(255, b + 15), 235),
        )
        for i in range(4):
            arcade.draw_polygon_filled([front[i], front[(i + 1) % 4],
                                        back[(i + 1) % 4], back[i]], face_colors[i])
        arcade.draw_polygon_filled(front, (*self._color, 245))
        for i in range(4):
            arcade.draw_line(front[i][0], front[i][1], back[i][0], back[i][1], COLOR_WHITE, 1)
            arcade.draw_line(front[i][0], front[i][1], front[(i + 1) % 4][0], front[(i + 1) % 4][1], COLOR_WHITE, 1)

        arcade.draw_text(
            self._label,
            self.x - 12, self.y - 5,
            COLOR_WHITE,
            font_size=8,
            bold=True,
        )
