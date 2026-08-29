"""
game/ui/parallax_bg.py
Four-layer dynamic parallax starfield that shifts with the player's position
and morphs visual theme & palettes per Mythological Realm (Swarga, Kshira Sagara, Dandaka, Lanka).
"""
import random
import arcade
from constants import WIDTH, HEIGHT, get_realm_for_wave


class ParallaxBackground:
    def __init__(self, seed: int = 42):
        rng = random.Random(seed)

        def rand_pos(margin=0):
            return (rng.randint(margin, WIDTH - margin),
                    rng.randint(margin, HEIGHT - margin))

        # Layer 0 — far tiny stars
        self._l0 = [
            (*rand_pos(), rng.uniform(0.5, 1.2), rng.randint(50, 140))
            for _ in range(150)
        ]

        # Layer 1 — cosmic nebula blobs
        self._nebulas = [
            (*rand_pos(60), rng.randint(45, 110), rng.randint(0, 2))
            for _ in range(8)
        ]

        # Layer 2 — medium stars
        self._l2 = [
            (*rand_pos(), rng.uniform(1.0, 2.2), rng.randint(100, 220))
            for _ in range(60)
        ]

        # Layer 3 — near celestial dust & glowing sparks
        self._l3 = [
            (*rand_pos(), rng.uniform(1.6, 3.2), rng.randint(180, 255))
            for _ in range(22)
        ]

    def draw(self, player_x: float, player_y: float, wave_num: int = 1) -> None:
        """Draws the dynamic realm backdrop with parallax motion."""
        realm = get_realm_for_wave(wave_num)
        nebula_colors = realm["nebula_palette"]
        accent = realm["accent_color"]

        cx, cy = WIDTH / 2, HEIGHT / 2
        nx = (player_x - cx) / cx
        ny = (player_y - cy) / cy

        # Draw deep realm atmosphere tint
        bg_r, bg_g, bg_b = realm["bg_color"]
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (bg_r, bg_g, bg_b))

        # ── 1. Nebulas ────────────────────────────────────────────────
        for bx, by, br, color_idx in self._nebulas:
            ox = nx * 18
            oy = ny * 18
            rx = (bx + ox) % WIDTH
            ry = (by + oy) % HEIGHT
            col = nebula_colors[color_idx % len(nebula_colors)]
            arcade.draw_circle_filled(rx, ry, br, (*col, 40))

        # ── 2. Layer 0 — Far Stars ────────────────────────────────────
        for sx, sy, sr, sb in self._l0:
            ox, oy = nx * 10, ny * 10
            rx = (sx + ox) % WIDTH
            ry = (sy + oy) % HEIGHT
            arcade.draw_circle_filled(rx, ry, sr, (sb, sb, sb))

        # ── 3. Layer 2 — Medium Stars (Realm Tinted) ───────────────────
        for sx, sy, sr, sb in self._l2:
            ox, oy = nx * 28, ny * 28
            rx = (sx + ox) % WIDTH
            ry = (sy + oy) % HEIGHT
            ar, ag, ab = accent
            # Blend star brightness with realm accent
            sr_val = int((sb + ar) * 0.5)
            sg_val = int((sb + ag) * 0.5)
            sb_val = int((sb + ab) * 0.5)
            arcade.draw_circle_filled(rx, ry, sr, (sr_val, sg_val, sb_val))

        # ── 4. Layer 3 — Foreground Cosmic Dust ────────────────────────
        for sx, sy, sr, sb in self._l3:
            ox, oy = nx * 50, ny * 50
            rx = (sx + ox) % WIDTH
            ry = (sy + oy) % HEIGHT
            arcade.draw_circle_filled(rx, ry, sr, (*accent, min(255, sb)))
