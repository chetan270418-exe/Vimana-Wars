"""
game/ui/boss_bar.py
BossBar class — full-width bar at the bottom of the screen while a Boss / Mini-Boss is alive.
Uses arcade.Text objects (no draw_text calls).
"""
import math
import arcade
from constants import WIDTH, COLOR_WHITE
from game.ui.vedic_theme import RED, RED_BRIGHT, GOLD, MUTED, draw_chamfered_panel, draw_telemetry_ticks


class BossBar:
    def __init__(self):
        self._label_name = arcade.Text(
            "", WIDTH // 2, 16,
            COLOR_WHITE, font_size=10, bold=True,
            anchor_x="center",
        )
        self._label_hp = arcade.Text(
            "", 18, 16,
            COLOR_WHITE, font_size=9,
        )

    def draw(self, boss) -> None:
        if not boss or not boss.alive:
            return

        bar_x, bar_y = 20, 14
        bar_w, bar_h = WIDTH - 40, 20
        frac = max(0.0, boss.hp / boss.max_hp)

        boss_name = getattr(boss, "name", "BOSS").upper()

        draw_chamfered_panel(bar_x - 6, bar_x + bar_w + 6, bar_y - 7,
                             bar_y + bar_h + 9, RED, fill=(22, 8, 18),
                             alpha=225, border_width=1, cut=6)
        draw_telemetry_ticks(bar_x, bar_x + bar_w, bar_y + bar_h + 5,
                             GOLD, count=19, height=3, alpha=65)
        arcade.draw_lrbt_rectangle_filled(bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, (30, 10, 10))

        # Fill — color shifts by phase or boss type
        if boss_name == "KUMBHAKARNA":
            fill_color = (210, 140, 20) if frac > 0.4 else (230, 60, 20)
        elif boss_name == "MAHISHASURA":
            fill_color = (200, 70, 30) if frac > 0.4 else (255, 30, 80)
        elif boss_name == "VRITRA":
            phase_fills = [(100, 220, 255), (180, 80, 255), (255, 40, 140)]
            fill_color = phase_fills[min(2, max(0, getattr(boss, "phase", 1) - 1))]
        else:
            phase_fills = [(200, 0, 60), (255, 80, 0), (220, 0, 200)]
            fill_color = phase_fills[getattr(boss, "phase", 1) - 1]

        if frac > 0:
            arcade.draw_lrbt_rectangle_filled(
                bar_x, bar_x + bar_w * frac, bar_y, bar_y + bar_h, fill_color)

        phase = max(1, int(getattr(boss, "phase", 1)))
        phase_count = 3 if boss_name in ("RAVANA", "VRITRA") else 2
        phase_count = max(phase_count, phase)
        phase_width = bar_w / phase_count
        for phase_index in range(phase_count):
            phase_left = bar_x + phase_index * phase_width
            phase_right = phase_left + phase_width - 3
            phase_color = GOLD if phase_index < phase else (*MUTED, 120)
            arcade.draw_lrbt_rectangle_outline(
                phase_left, phase_right, bar_y - 5, bar_y + bar_h + 5,
                phase_color, 1)

        thresholds = ((0.66, "P2"), (0.33, "P3"))
        for threshold, p_tag in thresholds:
            mx = bar_x + bar_w * threshold
            marker_col = GOLD if frac > threshold else (*MUTED, 180)
            arcade.draw_line(mx, bar_y - 2, mx, bar_y + bar_h + 2, marker_col, 2)
            arcade.draw_triangle_filled(mx, bar_y + bar_h + 6, mx - 4, bar_y + bar_h, mx + 4, bar_y + bar_h, marker_col)
            arcade.draw_text(p_tag, mx, bar_y + bar_h + 10, marker_col, font_size=7, bold=True, anchor_x="center")

        # Enraged outline pulsing when boss is below 33% HP
        border_col = COLOR_WHITE
        if frac < 0.33:
            import time
            pulse = int(180 + 75 * ((math.sin(time.time() * 6.0) + 1.0) * 0.5))
            border_col = (*RED_BRIGHT, pulse)

        # Border
        arcade.draw_lrbt_rectangle_outline(
            bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, border_col, 2)

        # Label formatting
        phase = max(1, int(getattr(boss, "phase", 1)))
        phase_text = f"PHASE {phase}"
        if boss_name == "RAVANA":
            phase_text = ("PHASE I / SPREAD", "PHASE II / SPIRAL VOID", "PHASE III / FLEET SUMMONS")[min(2, phase - 1)]
            title = "EMPEROR RAVANA"
        elif boss_name == "MAHISHASURA":
            title = "WARLORD MAHISHASURA"
        elif boss_name == "VRITRA":
            title = "STORM SERPENT VRITRA"
        else:
            title = f"MINI-BOSS: {boss_name}"
        attack = getattr(boss, "current_attack_name", "")
        self._label_name.text = f"{title}  —  {phase_text}"
        self._label_hp.text = f"{max(0, boss.hp):,} / {boss.max_hp:,}"
        self._label_name.draw()
        self._label_hp.draw()
        status = "BOSS ALERT" if phase == 1 else "PHASE BREAK" if frac > 0.30 else "FINAL PHASE"
        status_color = RED_BRIGHT if phase > 1 else GOLD
        arcade.draw_text(status, bar_x + 4, bar_y + bar_h + 22, status_color,
                         font_size=8, bold=True)
        if attack:
            arcade.draw_text(attack, WIDTH - 18, 16, RED_BRIGHT if frac < 0.33 else GOLD,
                             font_size=8, bold=True, anchor_x="right")
        if phase > 1:
            arcade.draw_text("PHASE BREAK", WIDTH // 2, 43, RED_BRIGHT, font_size=8, bold=True, anchor_x="center")
