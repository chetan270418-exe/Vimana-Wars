"""
game/ui/hud.py
Comprehensive HUD — animated smooth HP bar, active boons row, ability countdown rings,
off-screen threat radar arrows, wave objectives, enemy counts, and low-health vignette.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    COLOR_HP_BG, COLOR_HP_GREEN, COLOR_HP_LOW,
    COLOR_SCORE, COLOR_WAVE, COLOR_WHITE,
    COLOR_POWERUP_SHIELD, COLOR_POWERUP_SPREAD,
    COLOR_POWERUP_SPEED, COLOR_POWERUP_HEALTH, COLOR_POWERUP_BOMB,
)

_POWERUP_COLORS = {
    "SHIELD": COLOR_POWERUP_SHIELD,
    "SPREAD": COLOR_POWERUP_SPREAD,
    "SPEED":  COLOR_POWERUP_SPEED,
    "HEALTH": COLOR_POWERUP_HEALTH,
    "BOMB":   COLOR_POWERUP_BOMB,
}
_POWERUP_NAMES = {
    "SHIELD": "Kavach",
    "SPREAD": "Agneyastra",
    "SPEED":  "Vayavyastra",
}

_BAR_X, _BAR_Y, _BAR_W, _BAR_H = 16, HEIGHT - 32, 220, 20


class HUD:
    def __init__(self):
        self._displayed_hp = 100.0
        self._pulse_timer = 0.0

        # HP bar labels
        self._label_vimana = arcade.Text(
            "VIMANA", _BAR_X + 6, _BAR_Y + 4,
            COLOR_WHITE, font_size=9, bold=True,
        )
        self._label_hp = arcade.Text(
            "100/100", _BAR_X + _BAR_W - 65, _BAR_Y + 4,
            COLOR_WHITE, font_size=9, bold=True,
        )

        # Score & Combo
        self._label_score = arcade.Text(
            "0", WIDTH - 16, HEIGHT - 18,
            COLOR_SCORE, font_size=18, bold=True,
            anchor_x="right", anchor_y="top",
        )
        self._label_combo = arcade.Text(
            "", WIDTH - 16, HEIGHT - 44,
            (255, 150, 30), font_size=11, bold=True,
            anchor_x="right", anchor_y="top",
        )

        # Wave & Objective Info
        self._label_wave = arcade.Text(
            "", WIDTH // 2, HEIGHT - 16,
            COLOR_WAVE, font_size=13, bold=True,
            anchor_x="center", anchor_y="top",
        )
        self._label_objective = arcade.Text(
            "", WIDTH // 2, HEIGHT - 36,
            (180, 200, 240), font_size=10, bold=True,
            anchor_x="center", anchor_y="top",
        )
        self._label_enemy_count = arcade.Text(
            "", WIDTH // 2, HEIGHT - 52,
            (255, 120, 120), font_size=9, bold=True,
            anchor_x="center", anchor_y="top",
        )

        # Wave countdown banner
        self._label_announce = arcade.Text(
            "", WIDTH // 2, HEIGHT // 2 + 20,
            COLOR_WAVE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._label_announce_sub = arcade.Text(
            "Prepare yourself!", WIDTH // 2, HEIGHT // 2 - 20,
            COLOR_WHITE, font_size=14,
            anchor_x="center", anchor_y="center",
        )

        # Wave clear banner
        self._label_clear = arcade.Text(
            "WAVE CLEARED", WIDTH // 2, HEIGHT // 2 + 10,
            (50, 230, 120), font_size=28, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._label_clear_sub = arcade.Text(
            "Next wave incoming...", WIDTH // 2, HEIGHT // 2 - 22,
            (180, 240, 200), font_size=13,
            anchor_x="center", anchor_y="center",
        )

        # Tutorial hint
        self._label_tutorial = arcade.Text(
            "WASD: Move  •  LMB: Shoot  •  SPACE: Dash  •  Q: Chakram  •  F: Bomb",
            WIDTH // 2, 45,
            (200, 220, 255, 190), font_size=10, bold=True,
            anchor_x="center",
        )

        # Powerup text
        self._label_pu_name  = arcade.Text("", 56, 18, COLOR_WHITE, font_size=8, bold=True, anchor_x="center")
        self._label_pu_timer = arcade.Text("", 30, 44, COLOR_WHITE, font_size=9, bold=True, anchor_x="center")

    def update(self, delta_time: float, player) -> None:
        self._pulse_timer += delta_time
        # Smooth HP bar transition
        self._displayed_hp += (player.hp - self._displayed_hp) * min(1.0, 10.0 * delta_time)

    def draw(self, player, score_system, wave_manager, enemies: list, powerups: list, boon_manager) -> None:
        self._draw_hp_bar(player)
        self._draw_score(score_system)
        self._draw_wave_and_objective(wave_manager, len(enemies))
        self._draw_boons_row(boon_manager)
        self._draw_powerup(player)
        self._draw_ability_meters(player)
        self._draw_offscreen_radar(player, enemies, powerups)
        self._draw_low_health_vignette(player)

        if wave_manager.is_announcing:
            self._draw_announce(wave_manager)
        elif wave_manager.is_clearing:
            self._draw_clearing()

        if wave_manager.wave_number == 1 and wave_manager.is_fighting:
            self._label_tutorial.draw()

    def _draw_hp_bar(self, player) -> None:
        frac_actual = max(0.0, player.hp / player.max_hp)
        frac_ghost = max(0.0, self._displayed_hp / player.max_hp)

        fill_color = COLOR_HP_GREEN if frac_actual > 0.35 else COLOR_HP_LOW

        # Background
        arcade.draw_lrbt_rectangle_filled(_BAR_X, _BAR_X + _BAR_W, _BAR_Y, _BAR_Y + _BAR_H, COLOR_HP_BG)
        # Red damage ghosting trail
        if frac_ghost > frac_actual:
            arcade.draw_lrbt_rectangle_filled(_BAR_X, _BAR_X + _BAR_W * frac_ghost, _BAR_Y, _BAR_Y + _BAR_H, (220, 40, 40, 180))
        # Actual green fill
        if frac_actual > 0:
            arcade.draw_lrbt_rectangle_filled(_BAR_X, _BAR_X + _BAR_W * frac_actual, _BAR_Y, _BAR_Y + _BAR_H, fill_color)
        arcade.draw_lrbt_rectangle_outline(_BAR_X, _BAR_X + _BAR_W, _BAR_Y, _BAR_Y + _BAR_H, COLOR_WHITE, 1)

        self._label_hp.text = f"{max(0, player.hp)}/{player.max_hp}"
        self._label_vimana.draw()
        self._label_hp.draw()

    def _draw_score(self, score_system) -> None:
        self._label_score.text = f"{score_system.score:,}"
        self._label_score.draw()

        if score_system.combo_active:
            combo = score_system.combo
            if combo >= 10:
                col = (0, 240, 255)      # Cyan Godlike
            elif combo >= 6:
                col = (255, 80, 220)     # Magenta Epic
            elif combo >= 3:
                col = (255, 215, 60)     # Golden Frenzy
            else:
                col = (255, 140, 30)     # Orange Warmup

            self._label_combo.text = f"×{combo} COMBO"
            self._label_combo.color = col
            self._label_combo.draw()

            # Combo timer bar
            bar_w = 90
            bar_h = 3
            bx = WIDTH - 16 - bar_w
            by = HEIGHT - 64
            frac = max(0.0, score_system.combo_timer / score_system.combo_timeout)
            arcade.draw_lrbt_rectangle_filled(bx, bx + bar_w, by, by + bar_h, (40, 20, 20))
            if frac > 0:
                arcade.draw_lrbt_rectangle_filled(bx, bx + bar_w * frac, by, by + bar_h, col)

    def _draw_wave_and_objective(self, wave_manager, enemy_count: int) -> None:
        if wave_manager.wave_number == 0:
            return

        if wave_manager.is_boss_wave:
            w_text = "BOSS WAVE — EMPEROR RAVANA"
        elif wave_manager.is_mini_boss_wave:
            w_text = f"Wave {wave_manager.wave_number} — MINI-BOSS"
        else:
            w_text = f"Wave {wave_manager.wave_number}"

        self._label_wave.text = w_text
        self._label_wave.draw()

        if wave_manager.is_fighting:
            self._label_objective.text = f"OBJECTIVE: {wave_manager.current_objective}"
            self._label_objective.draw()
            self._label_enemy_count.text = f"ENEMIES REMAINING: {enemy_count}"
            self._label_enemy_count.draw()

    def _draw_boons_row(self, boon_manager) -> None:
        if not boon_manager.active_boons:
            return
        start_x = _BAR_X
        start_y = _BAR_Y - 24
        from game.systems.boon_system import BOONS_DATABASE
        
        rune_abbr = {
            "agni_fury": "AG",
            "indra_thunder": "IN",
            "vayu_tempest": "VA",
            "garuda_magnet": "GA",
            "varuna_ward": "VR",
            "sudarshana_keen": "SU",
            "yama_execution": "YA",
            "surya_beam": "SY",
        }

        for i, (bid, lvl) in enumerate(boon_manager.active_boons.items()):
            bdata = next((b for b in BOONS_DATABASE if b["id"] == bid), None)
            if not bdata: continue
            bx = start_x + i * 28
            arcade.draw_circle_filled(bx + 10, start_y, 11, (20, 25, 45))
            arcade.draw_circle_outline(bx + 10, start_y, 11, bdata["color"], 2)
            
            abbr = rune_abbr.get(bid, bdata["name"][:2].upper())
            arcade.draw_text(abbr, bx + 10, start_y - 4, bdata["color"], font_size=7, bold=True, anchor_x="center")

            # Stack level badge
            if lvl > 1:
                arcade.draw_circle_filled(bx + 19, start_y + 8, 5, (255, 215, 60))
                arcade.draw_text(str(lvl), bx + 19, start_y + 4, (10, 10, 10), font_size=7, bold=True, anchor_x="center")

    def _draw_ability_meters(self, player) -> None:
        # Dash [SPACE]
        cx1, cy1, r1 = 38, 32, 16
        dash_ratio = player.dash_ratio
        ready_col = (60, 230, 255) if player.dash_ready else (60, 100, 140)

        arcade.draw_circle_filled(cx1, cy1, r1, (15, 25, 45))
        arcade.draw_circle_outline(cx1, cy1, r1, ready_col, 2)
        if dash_ratio > 0:
            steps = max(1, int(30 * dash_ratio))
            for i in range(1, steps + 1):
                a = math.radians(90 - (360 * dash_ratio) * (i / 30))
                arcade.draw_line(cx1, cy1, cx1 + math.cos(a) * r1, cy1 + math.sin(a) * r1, ready_col, 2)

        dash_label = f"DASH ({player.dash_charges})" if player.dash_charges_max > 1 else "DASH"
        arcade.draw_text("SPACE", cx1, cy1 - 4, COLOR_WHITE, font_size=7, bold=True, anchor_x="center")
        arcade.draw_text(dash_label, cx1, cy1 - 22, ready_col, font_size=7, bold=True, anchor_x="center")

        # Chakram [Q]
        cx2, cy2, r2 = 88, 32, 16
        chk_ratio = player.chakram_ratio
        chk_col = (255, 215, 60) if player.chakram_ready else (120, 100, 40)

        arcade.draw_circle_filled(cx2, cy2, r2, (35, 30, 15))
        arcade.draw_circle_outline(cx2, cy2, r2, chk_col, 2)
        if chk_ratio > 0:
            steps = max(1, int(30 * chk_ratio))
            for i in range(1, steps + 1):
                a = math.radians(90 - (360 * chk_ratio) * (i / 30))
                arcade.draw_line(cx2, cy2, cx2 + math.cos(a) * r2, cy2 + math.sin(a) * r2, chk_col, 2)

        arcade.draw_text("Q", cx2, cy2 - 4, COLOR_WHITE, font_size=8, bold=True, anchor_x="center")
        arcade.draw_text("CHAKRAM", cx2, cy2 - 22, chk_col, font_size=7, bold=True, anchor_x="center")

        # Bomb [F]
        if player.bomb_count > 0:
            cx3, cy3 = 145, 32
            arcade.draw_circle_filled(cx3, cy3, 16, (45, 15, 50))
            arcade.draw_circle_outline(cx3, cy3, 16, COLOR_POWERUP_BOMB, 2)
            arcade.draw_text(f"F ×{player.bomb_count}", cx3, cy3 - 4, COLOR_WHITE, font_size=8, bold=True, anchor_x="center")
            arcade.draw_text("BOMB", cx3, cy3 - 22, COLOR_POWERUP_BOMB, font_size=7, bold=True, anchor_x="center")

    def _draw_offscreen_radar(self, player, enemies: list, powerups: list) -> None:
        """Draws glowing directional threat arrows along screen edges for off-screen enemies and power-ups."""
        margin = 22

        # 1. Off-screen enemies (red chevrons / pointer triangles)
        for e in enemies:
            if not e.alive: continue
            if not (0 <= e.x <= WIDTH and 0 <= e.y <= HEIGHT):
                ex = max(margin, min(WIDTH - margin, e.x))
                ey = max(margin, min(HEIGHT - margin, e.y))
                ang = math.atan2(e.y - player.y, e.x - player.x)
                
                # Draw pointer triangle pointing towards enemy
                tx1 = ex + math.cos(ang) * 8
                ty1 = ey + math.sin(ang) * 8
                tx2 = ex + math.cos(ang + 2.4) * 6
                ty2 = ey + math.sin(ang + 2.4) * 6
                tx3 = ex + math.cos(ang - 2.4) * 6
                ty3 = ey + math.sin(ang - 2.4) * 6
                arcade.draw_triangle_filled(tx1, ty1, tx2, ty2, tx3, ty3, (255, 50, 50))
                arcade.draw_circle_outline(ex, ey, 7, (255, 100, 100, 150), 1)

        # 2. Off-screen powerups (golden/cyan diamond pointers)
        for pu in powerups:
            if not pu.alive: continue
            if not (0 <= pu.x <= WIDTH and 0 <= pu.y <= HEIGHT):
                px = max(margin, min(WIDTH - margin, pu.x))
                py = max(margin, min(HEIGHT - margin, pu.y))
                pcol = getattr(pu, "_color", (255, 215, 60))
                arcade.draw_circle_filled(px, py, 6, pcol)
                arcade.draw_circle_outline(px, py, 8, COLOR_WHITE, 1)

    def _draw_low_health_vignette(self, player) -> None:
        frac = player.hp / player.max_hp
        if frac < 0.28 and player.alive:
            pulse = (math.sin(self._pulse_timer * 6) + 1.0) * 0.5
            alpha = int(70 * pulse)
            # Red screen border vignette
            arcade.draw_lrbt_rectangle_outline(4, WIDTH - 4, 4, HEIGHT - 4, (255, 30, 30, alpha), 8)

    def _draw_powerup(self, player) -> None:
        if not player.active_powerup or player.active_powerup.expired:
            return

        pu = player.active_powerup
        pname = pu.type.name
        label_str = _POWERUP_NAMES.get(pname, pname)
        color = _POWERUP_COLORS.get(pname, COLOR_WHITE)

        cx, cy, r = 38, 92, 18
        frac = pu.fraction

        arcade.draw_circle_outline(cx, cy, r, (60, 60, 60), 3)
        if frac > 0:
            steps = max(1, int(40 * frac))
            for i in range(1, steps + 1):
                a = math.radians(90 - (360 * frac) * (i / 40))
                arcade.draw_line(cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r, (*color, 180), 2)

        arcade.draw_circle_filled(cx, cy, r - 3, (*color, 100))
        self._label_pu_name.x = cx
        self._label_pu_name.y = cy - 28
        self._label_pu_name.text = label_str
        self._label_pu_name.color = color
        self._label_pu_timer.x = cx
        self._label_pu_timer.y = cy - 4
        self._label_pu_timer.text = f"{pu.remaining:.1f}s"
        self._label_pu_name.draw()
        self._label_pu_timer.draw()

    def _draw_announce(self, wave_manager) -> None:
        alpha = max(0, min(255, wave_manager.announce_alpha))
        r, g, b = COLOR_WAVE
        self._label_announce.text = f"{wave_manager.announce_text} — {wave_manager.countdown_val}"
        self._label_announce.color = (r, g, b, alpha)
        if wave_manager.announce_subtitle:
            self._label_announce_sub.text = wave_manager.announce_subtitle
        self._label_announce_sub.color = (*COLOR_WHITE, alpha)
        self._label_announce.draw()
        self._label_announce_sub.draw()

    def _draw_clearing(self) -> None:
        self._label_clear.draw()
        self._label_clear_sub.draw()
