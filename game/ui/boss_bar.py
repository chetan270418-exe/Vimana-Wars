"""
game/ui/boss_bar.py
BossBar class — full-width bar at the bottom of the screen while a Boss / Mini-Boss is alive.
Uses arcade.Text objects (no draw_text calls).
"""
import arcade
from constants import WIDTH, COLOR_WHITE


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

        # Background
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

        # Threshold markers for Boss phases (Phase 2 at 66%, Phase 3 at 33%)
        for threshold, p_tag in ((0.66, "P2"), (0.33, "P3")):
            mx = bar_x + bar_w * threshold
            arcade.draw_line(mx, bar_y - 2, mx, bar_y + bar_h + 2, (255, 220, 80), 2)
            arcade.draw_triangle_filled(mx, bar_y + bar_h + 6, mx - 4, bar_y + bar_h, mx + 4, bar_y + bar_h, (255, 220, 80))

        # Enraged outline pulsing when boss is below 33% HP
        border_col = COLOR_WHITE
        if frac < 0.33:
            import time
            pulse = int(180 + 75 * (time.time() * 6 % 1.0))
            border_col = (255, 50, 50, pulse)

        # Border
        arcade.draw_lrbt_rectangle_outline(
            bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, border_col, 2)

        # Label formatting
        if boss_name == "RAVANA":
            phase_labels = ["Phase I (Spread)", "Phase II (Spiral Void)", "Phase III (Fleet Summons)"]
            p_idx = getattr(boss, "phase", 1) - 1
            self._label_name.text = f"👑 EMPEROR RAVANA  —  {phase_labels[p_idx]}"
        elif boss_name == "MAHISHASURA":
            self._label_name.text = f"🐂 WARLORD MAHISHASURA  —  PHASE {getattr(boss, 'phase', 1)}"
        elif boss_name == "VRITRA":
            self._label_name.text = f"⚡ STORM SERPENT VRITRA  —  PHASE {getattr(boss, 'phase', 1)}"
        else:
            self._label_name.text = f"🛡️ MINI-BOSS: {boss_name}"

        self._label_hp.text = f"{max(0, boss.hp):,} / {boss.max_hp:,}"
        self._label_name.draw()
        self._label_hp.draw()
