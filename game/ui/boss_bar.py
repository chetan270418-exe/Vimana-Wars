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

        boss_name = getattr(boss, "name", "RAVANA")

        # Background
        arcade.draw_lrbt_rectangle_filled(bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, (30, 10, 10))

        # Fill — color shifts by phase or boss type
        if boss_name == "KUMBHAKARNA":
            fill_color = (210, 140, 20) if frac > 0.4 else (230, 60, 20)
        else:
            phase_fills = [(200, 0, 60), (255, 80, 0), (220, 0, 200)]
            fill_color = phase_fills[getattr(boss, "phase", 1) - 1]

        if frac > 0:
            arcade.draw_lrbt_rectangle_filled(
                bar_x, bar_x + bar_w * frac, bar_y, bar_y + bar_h, fill_color)

        # Threshold markers for Ravana
        if boss_name == "RAVANA":
            for threshold in (0.66, 0.33):
                mx = bar_x + bar_w * threshold
                arcade.draw_line(mx, bar_y, mx, bar_y + bar_h, COLOR_WHITE, 1)

        # Border
        arcade.draw_lrbt_rectangle_outline(
            bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, COLOR_WHITE, 2)

        # Label formatting
        if boss_name == "RAVANA":
            phase_labels = ["Phase I", "Phase II", "Phase III"]
            p_idx = getattr(boss, "phase", 1) - 1
            self._label_name.text = f"RAVANA  —  {phase_labels[p_idx]}"
        else:
            self._label_name.text = f"MINI-BOSS: {boss_name}  (THE ARMORED TITAN)"

        self._label_hp.text = f"{max(0, boss.hp):,} / {boss.max_hp:,}"
        self._label_name.draw()
        self._label_hp.draw()
