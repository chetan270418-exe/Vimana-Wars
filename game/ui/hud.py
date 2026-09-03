"""
game/ui/hud.py
Comprehensive HUD — reactive HP bar with ghost trail and color crossfade,
score count-up animation, combo burst particles, ability countdown rings,
off-screen threat radar arrows, wave objectives, and low-health vignette.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    COLOR_HP_BG, COLOR_HP_GREEN, COLOR_HP_LOW,
    COLOR_SCORE, COLOR_WAVE, COLOR_WHITE,
    COLOR_POWERUP_SHIELD, COLOR_POWERUP_SPREAD,
    COLOR_POWERUP_SPEED, COLOR_POWERUP_HEALTH, COLOR_POWERUP_BOMB,
    COLOR_POWERUP_OVERDRIVE,
)
from game.ui.easing import ease_out_cubic, ease_in_out_cubic, lerp, lerp_color, clamp
from game.ui.vedic_theme import (
    CYAN, GOLD, CYAN_BRIGHT, MUTED, RED_BRIGHT,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
    draw_telemetry_ticks, draw_segmented_bar,
)

_POWERUP_COLORS = {
    "SHIELD": COLOR_POWERUP_SHIELD,
    "SPREAD": COLOR_POWERUP_SPREAD,
    "SPEED":  COLOR_POWERUP_SPEED,
    "HEALTH": COLOR_POWERUP_HEALTH,
    "BOMB":   COLOR_POWERUP_BOMB,
    "OVERDRIVE": COLOR_POWERUP_OVERDRIVE,
}
_POWERUP_NAMES = {
    "SHIELD": "Kavach",
    "SPREAD": "Agneyastra",
    "SPEED":  "Vayavyastra",
    "HEALTH": "Amrita",
    "BOMB": "Brahmastra",
    "OVERDRIVE": "Astra Overdrive",
}

_BAR_X, _BAR_Y, _BAR_W, _BAR_H = 16, HEIGHT - 32, 220, 20

# HP bar color thresholds
_HP_COLOR_HIGH   = (30, 200, 70)     # green > 60%
_HP_COLOR_MID    = (220, 200, 40)    # amber 30-60%
_HP_COLOR_LOW    = (220, 60, 0)      # red < 30%


class HUD:
    def __init__(self):
        from game.systems import save_system
        settings = save_system.load()
        self.colorblind_mode = settings.get("colorblind_mode", "off")
        self.reduced_flashes = bool(settings.get("reduced_flashes", False))
        self._displayed_hp = 100.0
        self._ghost_hp = 100.0       # slower-decaying ghost trail
        self._pulse_timer = 0.0

        # Score count-up animation
        self._displayed_score = 0.0
        self._target_score = 0
        self._score_flash = 0.0      # brief scale/flash on big score changes

        # Combo burst state
        self._combo_scale = 1.0
        self._last_combo = 0

        # HP hit flash (red vignette on damage)
        self._hp_hit_flash = 0.0
        self._last_hp = 100

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

        # Smooth HP bar transition (eased approach)
        hp_diff = player.hp - self._displayed_hp
        self._displayed_hp += hp_diff * min(1.0, 12.0 * delta_time)

        # Ghost HP trail (decays slower — shows damage taken)
        ghost_diff = player.hp - self._ghost_hp
        if ghost_diff < 0:
            # HP decreased — ghost stays high then slowly catches up
            self._ghost_hp += ghost_diff * min(1.0, 2.5 * delta_time)
        else:
            # HP increased (heal) — ghost snaps to match
            self._ghost_hp = self._displayed_hp

        # HP hit flash on damage
        if player.hp < self._last_hp:
            self._hp_hit_flash = 1.0
        self._last_hp = player.hp
        if self._hp_hit_flash > 0:
            self._hp_hit_flash = max(0.0, self._hp_hit_flash - delta_time * 5.0)

        # Score count-up animation
        self._target_score = getattr(player, '_score_ref', self._target_score)
        score_diff = self._target_score - self._displayed_score
        if abs(score_diff) > 0.5:
            self._displayed_score += score_diff * min(1.0, 8.0 * delta_time)
        else:
            self._displayed_score = self._target_score

        # Score flash decay
        if self._score_flash > 0:
            self._score_flash = max(0.0, self._score_flash - delta_time * 4.0)

        # Combo burst scale decay
        if self._combo_scale > 1.0:
            self._combo_scale = max(1.0, self._combo_scale - delta_time * 6.0)

    def draw(self, player, score_system, wave_manager, enemies: list, powerups: list, boon_manager) -> None:
        self._draw_cockpit_frame()
        # Update score target from score_system
        if score_system.score != self._target_score:
            score_change = score_system.score - self._target_score
            if score_change > 500:
                self._score_flash = 1.0
            self._target_score = score_system.score

        # Combo burst detection
        if score_system.combo > self._last_combo and score_system.combo >= 3:
            self._combo_scale = 1.35
        self._last_combo = score_system.combo

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

    def _draw_cockpit_frame(self) -> None:
        draw_corner_etching(10, WIDTH - 10, 10, HEIGHT - 10, CYAN, length=28, alpha=62)
        draw_scanlines(218, WIDTH - 218, HEIGHT - 88, HEIGHT - 70, CYAN, spacing=6, alpha=10)
        draw_telemetry_ticks(245, WIDTH - 245, HEIGHT - 70, GOLD, count=17, height=3, alpha=54)
        draw_telemetry_ticks(230, WIDTH - 230, 70, CYAN, count=19, height=3, alpha=42)
        arcade.draw_line(215, 70, 215, HEIGHT - 88, (*CYAN, 28), 1)
        arcade.draw_text("PRANA TELEMETRY", 226, HEIGHT - 84, CYAN_BRIGHT, font_size=7, bold=True)
        arcade.draw_text("ASTRA CONTROL // LIVE", WIDTH - 226, HEIGHT - 84, MUTED, font_size=7, bold=True, anchor_x="right")

    def _draw_hp_bar(self, player) -> None:
        draw_chamfered_panel(12, _BAR_X + _BAR_W + 8, _BAR_Y - 5, _BAR_Y + _BAR_H + 7,
                             (220, 80, 80) if player.hp / player.max_hp < 0.3 else CYAN,
                             fill=(10, 16, 28), alpha=220, cut=7)
        arcade.draw_text("PRANA / HULL INTEGRITY", _BAR_X + 6, _BAR_Y + _BAR_H + 9,
                         MUTED, font_size=7, bold=True)
        draw_telemetry_ticks(_BAR_X, _BAR_X + _BAR_W, _BAR_Y - 3, CYAN, count=9, height=2, alpha=55)
        frac_actual = clamp(player.hp / player.max_hp)
        frac_display = clamp(self._displayed_hp / player.max_hp)
        frac_ghost = clamp(self._ghost_hp / player.max_hp)

        # Color crossfade: green > 60%, amber 30-60%, red < 30%
        palette = {
            "off": (_HP_COLOR_HIGH, _HP_COLOR_MID, _HP_COLOR_LOW),
            "protan": ((0, 114, 178), (230, 159, 0), (86, 180, 233)),
            "deutan": ((0, 114, 178), (230, 159, 0), (213, 94, 0)),
            "tritan": ((0, 158, 115), (230, 159, 0), (213, 94, 0)),
        }.get(self.colorblind_mode, (_HP_COLOR_HIGH, _HP_COLOR_MID, _HP_COLOR_LOW))
        high_color, mid_color, low_color = palette
        if frac_actual > 0.6:
            fill_color = high_color
        elif frac_actual > 0.3:
            t = clamp((frac_actual - 0.3) / 0.3)
            fill_color = lerp_color(mid_color, high_color, ease_out_cubic(t))
        else:
            t = clamp(frac_actual / 0.3)
            fill_color = lerp_color(low_color, mid_color, ease_out_cubic(t))

        # Background
        arcade.draw_lrbt_rectangle_filled(_BAR_X, _BAR_X + _BAR_W, _BAR_Y, _BAR_Y + _BAR_H, COLOR_HP_BG)

        # Ghost trail (red damage indicator — slower decay)
        if frac_ghost > frac_display:
            arcade.draw_lrbt_rectangle_filled(
                _BAR_X, _BAR_X + _BAR_W * frac_ghost,
                _BAR_Y, _BAR_Y + _BAR_H, (220, 40, 40, 160))

        # Actual HP fill
        if frac_display > 0:
            draw_segmented_bar(_BAR_X, _BAR_X + _BAR_W, _BAR_Y,
                               _BAR_Y + _BAR_H, frac_display, fill_color,
                               segments=10, gap=3)

        # Low-HP pulsing bar border
        if frac_actual < 0.28 and player.alive:
            pulse_t = ease_in_out_cubic(clamp((math.sin(self._pulse_timer * 5.0) + 1.0) * 0.5))
            pulse_a = int(lerp(100, 255, pulse_t))
            arcade.draw_lrbt_rectangle_outline(
                _BAR_X - 1, _BAR_X + _BAR_W + 1,
                _BAR_Y - 1, _BAR_Y + _BAR_H + 1,
                (255, 50, 50, pulse_a), 2)
        else:
            arcade.draw_lrbt_rectangle_outline(
                _BAR_X, _BAR_X + _BAR_W,
                _BAR_Y, _BAR_Y + _BAR_H, COLOR_WHITE, 1)

        # HP hit flash — red screen-edge vignette on damage
        if self._hp_hit_flash > 0:
            flash_a = int(60 * ease_out_cubic(self._hp_hit_flash) * (0.35 if self.reduced_flashes else 1.0))
            arcade.draw_lrbt_rectangle_filled(
                _BAR_X, _BAR_X + _BAR_W,
                _BAR_Y, _BAR_Y + _BAR_H, (255, 30, 30, flash_a))

        # HP number — flashes when low
        hp_text = f"{max(0, player.hp)}/{player.max_hp}"
        hp_col = COLOR_WHITE
        if frac_actual < 0.28 and player.alive:
            pulse_t = ease_in_out_cubic(clamp((math.sin(self._pulse_timer * 5.0) + 1.0) * 0.5))
            hp_col = lerp_color((255, 100, 80), (255, 255, 255), pulse_t)

        self._label_hp.text = hp_text
        self._label_hp.color = hp_col
        self._label_vimana.draw()
        self._label_hp.draw()

    def _draw_score(self, score_system) -> None:
        # Animated score count-up
        displayed = int(self._displayed_score)
        self._label_score.text = f"{displayed:,}"

        # Flash effect on big score changes
        if self._score_flash > 0:
            flash_scale = 1.0 + (0.06 if self.reduced_flashes else 0.15) * ease_out_cubic(self._score_flash)
            self._label_score.font_size = int(18 * flash_scale)
            glow_a = int((24 if self.reduced_flashes else 80) * self._score_flash)
            arcade.draw_lrbt_rectangle_filled(
                WIDTH - 200, WIDTH - 8,
                HEIGHT - 32, HEIGHT - 8,
                (255, 220, 50, glow_a))
        else:
            self._label_score.font_size = 18

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

            # Combo text with burst scale
            combo_size = int(11 * self._combo_scale)
            self._label_combo.text = f"×{combo} COMBO"
            self._label_combo.color = col
            self._label_combo.font_size = combo_size
            self._label_combo.draw()

            # Combo burst ring on increment
            if self._combo_scale > 1.05:
                ring_r = int(15 * self._combo_scale)
                ring_a = int(120 * (self._combo_scale - 1.0) / 0.35)
                cx = WIDTH - 55
                cy = HEIGHT - 50
                arcade.draw_circle_outline(cx, cy, ring_r, (*col, ring_a), 2)

            # Combo timer bar
            bar_w = 90
            bar_h = 3
            bx = WIDTH - 16 - bar_w
            by = HEIGHT - 64
            frac = clamp(score_system.combo_timer / score_system.combo_timeout)
            arcade.draw_lrbt_rectangle_filled(bx, bx + bar_w, by, by + bar_h, (40, 20, 20))
            if frac > 0:
                arcade.draw_lrbt_rectangle_filled(bx, bx + bar_w * frac, by, by + bar_h, col)

    def _draw_wave_and_objective(self, wave_manager, enemy_count: int) -> None:
        if wave_manager.wave_number == 0:
            return

        from constants import get_realm_for_wave
        realm = get_realm_for_wave(wave_manager.wave_number)
        effective_wave = ((wave_manager.wave_number - 1) % 20) + 1
        realm_index = (
            1 if effective_wave <= 3 else
            2 if effective_wave <= 6 else
            3 if effective_wave <= 9 else
            4 if effective_wave <= 12 else
            5 if effective_wave <= 15 else
            6 if effective_wave <= 18 else 7
        )
        breadcrumb = (
            f"MAHAYUDDHA  •  WAVE {wave_manager.wave_number}"
            if getattr(wave_manager, "is_endless", False)
            else f"REALM {realm_index}/7  •  {realm['name']}  •  WAVE {wave_manager.wave_number}"
        )
        if wave_manager.is_boss_wave:
            w_text = f"{breadcrumb}  —  EMPEROR RAVANA"
        elif wave_manager.is_mini_boss_wave:
            w_text = f"{breadcrumb}  —  MINI-BOSS"
        else:
            w_text = breadcrumb

        self._label_wave.text = w_text
        self._label_wave.draw()

        if wave_manager.is_fighting:
            self._label_objective.text = f"OBJECTIVE: {wave_manager.current_objective}"
            self._label_objective.draw()
            total = max(enemy_count, getattr(wave_manager, "total_wave_enemies", enemy_count))
            self._label_enemy_count.text = f"ENEMIES REMAINING: {enemy_count} / {total}"
            self._label_enemy_count.draw()

    def _draw_boons_row(self, boon_manager) -> None:
        if not boon_manager.active_boons:
            return
        start_x = _BAR_X
        start_y = _BAR_Y - 24
        from game.systems.boon_system import BOONS_DATABASE, SYNERGIES_DATABASE
        
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

        # ── Synergy Badges Row ─────────────────────────────────────────
        if hasattr(boon_manager, "active_synergies") and boon_manager.active_synergies:
            syn_y = start_y - 24
            for j, sid in enumerate(boon_manager.active_synergies):
                sdata = next((s for s in SYNERGIES_DATABASE if s["id"] == sid), None)
                if not sdata: continue
                sx = start_x + j * 75
                # Glowing synergy capsule
                pulse = (math.sin(self._pulse_timer * 4.0) + 1.0) * 0.5
                border_col = (*sdata["color"][:3], int(180 + 75 * pulse))
                arcade.draw_lrbt_rectangle_filled(sx, sx + 70, syn_y - 8, syn_y + 9, (25, 18, 45))
                arcade.draw_lrbt_rectangle_outline(sx, sx + 70, syn_y - 8, syn_y + 9, border_col, 2)
                arcade.draw_text(sdata["name"][:9].upper(), sx + 35, syn_y - 4, sdata["color"], font_size=7, bold=True, anchor_x="center")

    def _draw_ability_meters(self, player) -> None:
        draw_chamfered_panel(12, 190, 8, 66, CYAN, fill=(10, 16, 28),
                             alpha=220, cut=8)
        arcade.draw_line(200, 12, WIDTH - 184, 12, (*CYAN, 42), 1)
        arcade.draw_text("ASTRA CONTROL", 202, 51, CYAN_BRIGHT, font_size=7, bold=True)
        arcade.draw_text("COOLDOWN / CHARGE TELEMETRY", 202, 40, MUTED, font_size=7, bold=True)
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
        dash_state = "READY" if player.dash_ready else f"{max(0.0, player.dash_cooldown_timer):.1f}s"
        arcade.draw_text("◆", cx1, cy1 - 5, COLOR_WHITE, font_size=10, bold=True, anchor_x="center")
        arcade.draw_text("SPACE", cx1, cy1 - 21, COLOR_WHITE, font_size=6, bold=True, anchor_x="center")
        arcade.draw_text(f"{dash_label} {dash_state}", cx1, cy1 - 31, ready_col, font_size=6, bold=True, anchor_x="center")

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

        chk_state = "READY" if player.chakram_ready else f"{max(0.0, player.chakram_cooldown_timer):.1f}s"
        arcade.draw_text("◈", cx2, cy2 - 5, COLOR_WHITE, font_size=10, bold=True, anchor_x="center")
        arcade.draw_text("Q", cx2, cy2 - 21, COLOR_WHITE, font_size=6, bold=True, anchor_x="center")
        arcade.draw_text(f"CHAKRAM {chk_state}", cx2, cy2 - 31, chk_col, font_size=6, bold=True, anchor_x="center")

        # Bomb [F]
        if player.bomb_count > 0:
            cx3, cy3 = 145, 32
            arcade.draw_circle_filled(cx3, cy3, 16, (45, 15, 50))
            arcade.draw_circle_outline(cx3, cy3, 16, COLOR_POWERUP_BOMB, 2)
            arcade.draw_text("✦", cx3, cy3 - 5, COLOR_WHITE, font_size=10, bold=True, anchor_x="center")
            arcade.draw_text(f"F ×{player.bomb_count}", cx3, cy3 - 21, COLOR_WHITE, font_size=6, bold=True, anchor_x="center")
            arcade.draw_text("BOMB READY", cx3, cy3 - 31, COLOR_POWERUP_BOMB, font_size=6, bold=True, anchor_x="center")

    def _draw_offscreen_radar(self, player, enemies: list, powerups: list) -> None:
        """Draws glowing directional threat arrows along screen edges for off-screen enemies and power-ups."""
        margin = 22
        living = sum(1 for enemy in enemies if enemy.alive)
        offscreen = sum(1 for enemy in enemies if enemy.alive and not (0 <= enemy.x <= WIDTH and 0 <= enemy.y <= HEIGHT))
        radar_col = RED_BRIGHT if offscreen else CYAN_BRIGHT
        arcade.draw_text("RADAR", WIDTH - 112, 54, MUTED, font_size=7, bold=True)
        arcade.draw_text(f"THREATS {living:02d}", WIDTH - 112, 40, radar_col, font_size=8, bold=True)
        if offscreen:
            arcade.draw_text(f"OFF-SCREEN {offscreen:02d}", WIDTH - 112, 27, RED_BRIGHT, font_size=7, bold=True)

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
            # Smooth eased pulse instead of raw sin()
            pulse_t = ease_in_out_cubic(clamp((math.sin(self._pulse_timer * 5.0) + 1.0) * 0.5))
            alpha = int(lerp(12, 36, pulse_t)) if self.reduced_flashes else int(lerp(30, 90, pulse_t))
            # Red screen border vignette — thicker at lower HP
            border_w = int(lerp(4, 12, 1.0 - frac / 0.28))
            arcade.draw_lrbt_rectangle_outline(
                4, WIDTH - 4, 4, HEIGHT - 4,
                (255, 30, 30, alpha), border_w)

            # Corner vignette glow for extra urgency
            corner_a = int(lerp(10, 40, pulse_t))
            for cx, cy in [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]:
                arcade.draw_circle_filled(cx, cy, 120, (180, 0, 0, corner_a))

        # Damage hit flash (from _hp_hit_flash)
        if self._hp_hit_flash > 0:
            edge_a = int(15 * ease_out_cubic(self._hp_hit_flash)) if self.reduced_flashes else int(50 * ease_out_cubic(self._hp_hit_flash))
            arcade.draw_lrbt_rectangle_outline(
                2, WIDTH - 2, 2, HEIGHT - 2,
                (255, 60, 40, edge_a), 6)

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
