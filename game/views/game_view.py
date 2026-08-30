"""
game/views/game_view.py
Main gameplay loop — owns all entities, calls all systems, handles keyboard, mouse & gamepad input.
Features full ship archetypes, difficulty scaling, near-miss/perfect dodge feedback,
Deva Boons, and instant run restarts.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, get_difficulty_mults
from game.entities.player import Player
from game.entities.bullet import PlayerBullet
from game.entities.chakram import Chakram
from game.entities.ship_classes import SHIP_CLASSES
from game.systems.wave_manager import WaveManager
from game.systems.score_system import ScoreSystem
from game.systems.sound_manager import SoundManager
from game.systems.particles import ParticleManager
from game.systems.floating_text import FloatingTextManager
from game.systems.boon_system import BoonManager
from game.systems.achievement_system import AchievementManager
from game.systems.environmental_hazards import EnvironmentalHazardManager
from game.systems import collision as collision_sys
from game.systems import save_system
from game.ui.hud import HUD
from game.ui.boss_bar import BossBar
from game.ui.parallax_bg import ParallaxBackground
from game.ui.transitions import TransitionOverlay, transition_to
from game.ui.tween import TweenManager, Tween
from game.ui.easing import ease_out_cubic, ease_out_elastic, ease_out_back, ease_in_out_cubic, lerp, clamp


class GameView(arcade.View):
    def __init__(self, difficulty: str = "normal", ship_class: str = "pushpaka", is_endless: bool = False):
        super().__init__()
        self._difficulty = difficulty
        self._ship_class_id = ship_class
        self.is_endless = is_endless
        self._mults = get_difficulty_mults(difficulty)

        sdata = SHIP_CLASSES.get(ship_class, SHIP_CLASSES["pushpaka"])

        # ── Entity lists ────────────────────────────────────────────────
        self.player = Player()
        self.player.apply_ship_class(sdata)
        self.player.dmg_taken_mult = self._mults["dmg_in"]
        self.player.max_hp = max(1, int(self.player.max_hp * self._mults["player_hp"]))
        self.player.hp = self.player.max_hp
        self._bullet_dmg = sdata["bullet_damage"]

        self.enemies: list = []
        self.player_bullets: list = []
        self.enemy_bullets: list = []
        self.powerups: list = []
        self.chakrams: list[Chakram] = []

        # ── Systems ─────────────────────────────────────────────────────
        self.wave_manager = WaveManager(
            spawn_mult=self._mults["spawn"],
            enemy_spd_mult=self._mults["enemy_spd"],
            is_endless=is_endless
        )
        self.score_system = ScoreSystem()
        self.sound_manager = SoundManager()
        self.particles = ParticleManager()
        self.floating_texts = FloatingTextManager()
        self.boon_manager = BoonManager()
        self.achievement_manager = AchievementManager()
        self.hazard_manager = EnvironmentalHazardManager()

        # ── Combat Breakdown Stats ──────────────────────────────────────
        self.combat_stats = {
            "total_damage": 0,
            "perfect_dodges": 0,
            "near_misses": 0,
            "bombs_used": 0,
            "synergies_activated": [],
        }

        # ── Boss Cinematic Intro State ──────────────────────────────────
        self._cinematic_timer = 0.0
        self._cinematic_title = ""
        self._cinematic_subtitle = ""
        self._cinematic_color = (255, 215, 60)

        # ── UI & Background ─────────────────────────────────────────────
        self.hud = HUD()
        self.boss_bar = BossBar()
        self.bg = ParallaxBackground()

        # Pause text objects
        self._pause_title = arcade.Text(
            "GAME PAUSED", WIDTH // 2, HEIGHT // 2 + 50,
            (200, 200, 255), font_size=36, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._pause_hint = arcade.Text(
            "ESC : Resume   •   R : Restart Run   •   O : Settings   •   M : Menu",
            WIDTH // 2, HEIGHT // 2 - 40,
            (160, 180, 220), font_size=13, bold=True,
            anchor_x="center",
        )

        # ── State & Juice ───────────────────────────────────────────────
        self.paused = False
        self._boss = None
        self._boss_announced = False
        self._was_clearing = False
        self._screen_shake = 0.0
        self._shake_intensity = 0.0
        self._hit_stop = 0.0
        self._boon_awarded_waves: set[int] = set()

        # ── Tween & Animation ───────────────────────────────────────────
        self._tweens = TweenManager()

        # ── Death Sequence State ────────────────────────────────────────
        self._death_phase = None       # None | "slowmo" | "freeze" | "fadeout"
        self._death_timer = 0.0
        self._death_time_scale = 1.0   # slows to 0.15 during death
        self._death_desat = 0.0        # 0.0 → 1.0 desaturation overlay
        self._death_fade = 0.0         # 0.0 → 1.0 fade to dark red

        saved = save_system.load()
        self.shake_setting = saved.get("screen_shake", "full")

        # ── Gamepad Setup ───────────────────────────────────────────────
        self.right_stick_x = 0.0
        self.right_stick_y = 0.0
        try:
            gamepads = arcade.get_gamepads()
            if gamepads:
                self.gamepad = gamepads[0]
                self.gamepad.open()
                self.gamepad.push_handlers(self)
        except Exception:
            pass

    # ── Arcade callbacks ────────────────────────────────────────────────

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        saved = save_system.load()
        self.shake_setting = saved.get("screen_shake", "full")
        self.sound_manager.start_music()

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            return

        if self.paused:
            if key == arcade.key.R:
                self.window.show_view(GameView(difficulty=self._difficulty, ship_class=self._ship_class_id))
            elif key == arcade.key.O:
                from game.views.settings_view import SettingsView
                self.window.show_view(SettingsView(return_view=self))
            elif key == arcade.key.M:
                from game.views.menu_view import MenuView
                self.window.show_view(MenuView())
            return

        if key in (arcade.key.SPACE, arcade.key.LSHIFT, arcade.key.RSHIFT):
            self._trigger_dash()
        elif key in (arcade.key.Q, arcade.key.E):
            self._trigger_chakram()
        elif key == arcade.key.F:
            if self.player.use_bomb():
                self._activate_bomb()

        self.player.keys_pressed.add(key)

    def on_key_release(self, key, modifiers) -> None:
        self.player.keys_pressed.discard(key)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.player.mouse_x = x
        self.player.mouse_y = y
        self.player.joy_aim_angle = None

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.mouse_held = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self._trigger_dash()
        elif button == arcade.MOUSE_BUTTON_MIDDLE:
            self._trigger_chakram()

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player.mouse_held = False

    def on_joybutton_press(self, joystick, button) -> None:
        if button in (0, 5):
            self.player.mouse_held = True
        elif button in (1, 4):
            self._trigger_dash()
        elif button in (3,):
            self._trigger_chakram()
        elif button in (2, 8):
            if self.player.use_bomb():
                self._activate_bomb()
        elif button in (6, 7, 9):
            self.paused = not self.paused

    def on_joybutton_release(self, joystick, button) -> None:
        if button in (0, 5):
            self.player.mouse_held = False

    def on_joyaxis_motion(self, joystick, axis, value) -> None:
        if axis == "x":
            self.player.joy_dx = value if abs(value) > 0.15 else 0.0
        elif axis == "y":
            self.player.joy_dy = -value if abs(value) > 0.15 else 0.0
        elif axis in ("rx", "z"):
            self.right_stick_x = value
        elif axis in ("ry", "rz"):
            self.right_stick_y = -value

        if math.hypot(self.right_stick_x, self.right_stick_y) > 0.25:
            self.player.joy_aim_angle = math.degrees(
                math.atan2(self.right_stick_y, self.right_stick_x)
            )

    # ── Ability Triggers ────────────────────────────────────────────────

    def _trigger_dash(self) -> None:
        if self.player.trigger_dash():
            self.sound_manager.play_dash()
            self.particles.spawn_dash_flash(self.player.x, self.player.y)
            self.floating_texts.spawn_notification(self.player.x, self.player.y + 20, "VAYU DASH!", (100, 230, 255))
            if self.boon_manager.has_boon("vayu_tempest"):
                self.particles.spawn_explosion(self.player.x, self.player.y, radius=28, count=18, base_color=(100, 255, 180))
                # Damaging cyclone
                level = self.boon_manager.get_boon_level("vayu_tempest")
                dmg = 40 * level
                for enemy in self.enemies:
                    if enemy.alive and math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < 120:
                        enemy.take_damage(dmg)
                        self.combat_stats["total_damage"] += dmg
                        self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=5, color=(100, 255, 180))
                        if enemy.is_dead():
                            self.score_system.register_kill(enemy.score_value)
                            self.player.enemies_killed += 1
                            self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius, count=22)

            if self.boon_manager.has_synergy("solar_cyclone"):
                self.particles.spawn_explosion(self.player.x, self.player.y, radius=38, count=24, base_color=(255, 200, 40))
                for enemy in self.enemies:
                    if enemy.alive and math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < 150:
                        enemy.take_damage(60)
                        enemy._burning = 3.0
                        self.combat_stats["total_damage"] += 60
                        self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=6, color=(255, 200, 40))
                        if enemy.is_dead():
                            self.score_system.register_kill(enemy.score_value)
                            self.player.enemies_killed += 1
                            self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius, count=22)

    def _trigger_chakram(self) -> None:
        if self.player.trigger_chakram():
            self.sound_manager.play_shoot()
            chk = Chakram(self.player.x, self.player.y, self.player.angle)
            if self.boon_manager.has_boon("sudarshana_keen"):
                chk.damage = int(chk.damage * 1.4)
                chk.radius = int(chk.radius * 1.3)
            self.chakrams.append(chk)
            tag = "YAMA'S EXECUTIONER DISC!" if self.boon_manager.has_synergy("executioner_disc") else "SUDARSHANA!"
            self.floating_texts.spawn_notification(self.player.x, self.player.y + 20, tag, (255, 220, 60))

    def apply_boon(self, boon_data: dict) -> None:
        bid = boon_data["id"]
        new_syns = self.boon_manager.add_boon(bid)
        self.sound_manager.play_powerup()
        
        level = self.boon_manager.get_boon_level(bid)
        lvl_str = f" (Lv.{level})" if level > 1 else ""
        self.floating_texts.spawn_notification(self.player.x, self.player.y + 30, f"+ {boon_data['name']}{lvl_str}", boon_data["color"])
        
        if bid == "varuna_ward":
            self.player.max_hp += 35
            self.player.heal(35)
        elif bid == "vayu_tempest":
            self.player.dash_cooldown_max *= 0.65
            self.player.dash_cooldown_timer = min(self.player.dash_cooldown_timer, self.player.dash_cooldown_max)
        elif bid == "sudarshana_keen":
            self.player.chakram_cooldown_max = max(1.0, self.player.chakram_cooldown_max - 2.0)
            self.player.chakram_cooldown_timer = min(self.player.chakram_cooldown_timer, self.player.chakram_cooldown_max)

        for syn in new_syns:
            self.sound_manager.play_synergy()
            self.floating_texts.spawn_notification(self.player.x, self.player.y + 50, f"★ SYNERGY: {syn['name'].upper()}! ★", syn["color"])
            self.particles.spawn_explosion(self.player.x, self.player.y, radius=45, count=32, base_color=syn["color"])
            self.combat_stats["synergies_activated"].append(syn["name"])

        if len(self.boon_manager.active_boons) >= 4:
            self.achievement_manager.check_unlock("boon_collector")

    # ── Update ──────────────────────────────────────────────────────────

    def on_update(self, delta_time: float) -> None:
        # Always update transitions and tweens even when paused
        TransitionOverlay.update(delta_time)
        self._tweens.update(delta_time)

        if self.paused:
            return

        # ── Death Sequence ──────────────────────────────────────────────
        if self._death_phase is not None:
            self._death_timer += delta_time
            if self._death_phase == "slowmo":
                # Slow-mo for 0.5s, then freeze
                if self._death_timer >= 0.5:
                    self._death_phase = "freeze"
                    self._death_timer = 0.0
                else:
                    # Run game at reduced speed for visual drama
                    scaled_dt = delta_time * 0.15
                    self.particles.update(scaled_dt)
                    self.floating_texts.update(scaled_dt)
                    self._death_desat = clamp(self._death_timer / 0.5)
            elif self._death_phase == "freeze":
                # Hold freeze for 0.4s
                if self._death_timer >= 0.4:
                    self._death_phase = "fadeout"
                    self._death_timer = 0.0
            elif self._death_phase == "fadeout":
                # Fade to dark red over 0.6s, then transition
                self._death_fade = clamp(self._death_timer / 0.6)
                if self._death_timer >= 0.7:
                    self._death_phase = None
                    self._finish_game_over()
            return

        if self._cinematic_timer > 0:
            self._cinematic_timer -= delta_time

        if self._hit_stop > 0:
            self._hit_stop -= delta_time
            return

        was_dashing = getattr(self, "_was_dashing", False)

        # Player & Passives
        self.player.update(delta_time)
        self.boon_manager.update_passives(delta_time, self.player)
        self.hud.update(delta_time, self.player)

        if was_dashing and not self.player.is_dashing:
            self.particles.spawn_dash_shockwave(self.player.x, self.player.y)
        self._was_dashing = self.player.is_dashing

        if (self.player.keys_pressed or abs(self.player.joy_dx) > 0.1 or abs(self.player.joy_dy) > 0.1) and self.player.alive:
            self.particles.spawn_engine_trail(self.player.x, self.player.y, self.player.angle)

        # Garuda Magnet Boon (delta_time scaled)
        if self.boon_manager.has_boon("garuda_magnet"):
            for pu in self.powerups:
                dx = self.player.x - pu.x
                dy = self.player.y - pu.y
                dist = math.hypot(dx, dy)
                if 0 < dist < 350:
                    mag_step = 480.0 * delta_time
                    pu.x += (dx / dist) * mag_step
                    pu.y += (dy / dist) * mag_step

        # Shooting
        bullets_fired = self.player.get_bullets_to_fire()
        if bullets_fired:
            self.sound_manager.play_shoot()
            self.boon_manager.shot_counter += 1
            for angle in bullets_fired:
                b = PlayerBullet(self.player.x, self.player.y, angle)
                b.damage = self._bullet_dmg
                if self.boon_manager.has_boon("surya_beam"):
                    level = self.boon_manager.get_boon_level("surya_beam")
                    shots_req = max(2, 7 - level + 1)
                    if self.boon_manager.shot_counter % shots_req == 0:
                        b.damage = int(self._bullet_dmg * (2.0 + level * 0.2))
                        b.radius = 8
                        b.is_piercing = True
                self.player_bullets.append(b)

        # Near Miss & Perfect Dodge Checks (single reward per projectile)
        for eb in self.enemy_bullets:
            if not eb.alive: continue
            if getattr(eb, "_rewarded", False): continue
            dist = math.hypot(eb.x - self.player.x, eb.y - self.player.y)
            if self.player.is_dashing and dist < 32:
                eb._rewarded = True
                self.floating_texts.spawn_notification(self.player.x, self.player.y + 24, "PERFECT DODGE! +100", (100, 255, 200))
                self.score_system.score += 100
                self.combat_stats["perfect_dodges"] += 1
                self.sound_manager.play_dodge_chime()
                self.particles.spawn_hit_sparks(self.player.x, self.player.y, count=4, color=(100, 255, 200))
            elif not self.player.is_dashing and 15 < dist < 26:
                eb._rewarded = True
                self.floating_texts.spawn_notification(self.player.x, self.player.y + 15, "NEAR MISS! +50", (255, 230, 100))
                self.score_system.score += 50
                self.combat_stats["near_misses"] += 1
                self.sound_manager.play_dodge_chime(0.4)

        # Chakram mechanics
        for chk in self.chakrams:
            chk.update(delta_time, self.player.x, self.player.y)
            for eb in self.enemy_bullets[:]:
                if math.hypot(chk.x - eb.x, chk.y - eb.y) < chk.radius + eb.radius + 6:
                    eb.alive = False
                    self.particles.spawn_hit_sparks(eb.x, eb.y, count=4, color=(255, 220, 80))

            for enemy in self.enemies:
                if enemy.alive and math.hypot(chk.x - enemy.x, chk.y - enemy.y) < chk.radius + enemy.radius:
                    if chk.can_damage(enemy):
                        dmg = chk.damage
                        if self.boon_manager.has_boon("yama_execution") and enemy.max_hp > 0 and (enemy.hp / enemy.max_hp) < 0.45:
                            dmg = int(dmg * 1.6)
                        if self.boon_manager.has_synergy("executioner_disc") and enemy.max_hp > 0 and (enemy.hp / enemy.max_hp) < 0.25 and not getattr(enemy, "is_boss", False):
                            dmg = enemy.hp
                            self.floating_texts.spawn_notification(enemy.x, enemy.y + 15, "EXECUTED!", (255, 60, 100))

                        enemy.take_damage(dmg)
                        self.combat_stats["total_damage"] += dmg
                        self.floating_texts.spawn_damage(enemy.x, enemy.y, dmg, is_crit=True)
                        self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=7, color=(255, 215, 60))
                        if enemy.is_dead():
                            self.score_system.register_kill(enemy.score_value)
                            self.player.enemies_killed += 1
                            self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius, count=22)

        self.chakrams = [c for c in self.chakrams if c.alive]

        # Enemy updates & Burning DoT
        new_enemy_bullets = []
        for enemy in self.enemies:
            fired = enemy.update(delta_time, self.player.x, self.player.y)
            new_enemy_bullets.extend(fired)
            if hasattr(enemy, "pending_summons") and enemy.pending_summons:
                self.enemies.extend(enemy.pending_summons)

            # Healer pulse logic
            if hasattr(enemy, "perform_heal_pulse"):
                if enemy.perform_heal_pulse(self.enemies):
                    self.particles.spawn_powerup_sparkle(enemy.x, enemy.y, color=(40, 240, 140))

            # Agni Burning DoT
            if getattr(enemy, "_burning", 0) > 0:
                enemy._burning -= delta_time
                level = self.boon_manager.get_boon_level("agni_fury")
                burn_dps = 24.0 * max(1, level)
                enemy._burn_accum = getattr(enemy, "_burn_accum", 0.0) + burn_dps * delta_time
                if enemy._burn_accum >= 1.0:
                    dmg = int(enemy._burn_accum)
                    enemy._burn_accum -= dmg
                    enemy.take_damage(dmg)
                    self.combat_stats["total_damage"] += dmg
                    self.floating_texts.spawn_damage(enemy.x, enemy.y, dmg, color=(255, 120, 30))
                    self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=2, color=(255, 100, 20))
                    if enemy.is_dead():
                        self.score_system.register_kill(enemy.score_value)
                        self.player.enemies_killed += 1
                        self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius * 1.5, count=22, base_color=(255, 120, 30))

        self.enemy_bullets.extend(new_enemy_bullets)

        for b in self.player_bullets: b.update(delta_time)
        for b in self.enemy_bullets: b.update(delta_time)
        for pu in self.powerups: pu.update(delta_time)

        # Systems
        self.particles.update(delta_time)
        self.floating_texts.update(delta_time)
        self.achievement_manager.update(delta_time)
        self.hazard_manager.update(delta_time, self.wave_manager.wave_number, self.player, self.enemies, self.player_bullets + self.enemy_bullets)
        self.wave_manager.update(delta_time, self.enemies, self.powerups, self.player)
        self.score_system.update(delta_time)

        # Inter-Wave Boon Card Trigger
        if self.wave_manager.is_clearing:
            wn = self.wave_manager.wave_number
            if wn in (1, 3, 5, 7, 9) and wn not in self._boon_awarded_waves:
                self._boon_awarded_waves.add(wn)
                from game.views.boon_select_view import BoonSelectView
                choices = self.boon_manager.get_random_choices(3)
                if choices:
                    self.window.show_view(BoonSelectView(self, choices))
                    return

        if self.wave_manager.is_clearing and not self._was_clearing:
            self.sound_manager.play_wave_clear()
        self._was_clearing = self.wave_manager.is_clearing

        # Collision System
        summary = collision_sys.check_all(
            self.player, self.enemies, self.player_bullets,
            self.enemy_bullets, self.powerups, self.score_system,
            self.boon_manager
        )

        for sx, sy, scol in summary.get("hit_sparks", []):
            self.particles.spawn_hit_sparks(sx, sy, count=6, color=scol)
            self.floating_texts.spawn_damage(sx, sy, self._bullet_dmg)
            self.combat_stats["total_damage"] += self._bullet_dmg

        # Indra Chain Lightning & Plasma Storm Synergy
        if self.boon_manager.has_boon("indra_thunder"):
            for bx, by, struck_enemy in summary.get("bullet_hits", []):
                if random.random() < 0.25:
                    # Find up to 3 nearest other living enemies
                    nearby_enemies = sorted(
                        [e for e in self.enemies if e.alive and e is not struck_enemy],
                        key=lambda e: math.hypot(e.x - bx, e.y - by)
                    )[:3]
                    for nearby in nearby_enemies:
                        if math.hypot(nearby.x - bx, nearby.y - by) < 320:
                            l_dmg = 28
                            nearby.take_damage(l_dmg)
                            self.combat_stats["total_damage"] += l_dmg
                            self.particles.spawn_hit_sparks(nearby.x, nearby.y, count=5, color=(120, 220, 255))
                            
                            if self.boon_manager.has_synergy("plasma_storm"):
                                nearby.take_damage(20)
                                nearby._burning = 3.0
                                self.combat_stats["total_damage"] += 20
                                self.particles.spawn_explosion(nearby.x, nearby.y, radius=24, count=16, base_color=(255, 120, 240))

                            if nearby.is_dead():
                                self.score_system.register_kill(nearby.score_value)
                                self.player.enemies_killed += 1
                                self.particles.spawn_explosion(nearby.x, nearby.y, radius=nearby.radius, count=22)

        for ex, ey, erad, ecol in summary.get("explosions", []):
            self.particles.spawn_explosion(ex, ey, radius=erad, count=22, base_color=ecol)
            self.achievement_manager.check_unlock("first_blood")
            if self.score_system.combo >= 3:
                self.floating_texts.spawn_combo(ex, ey, self.score_system.combo)
            if self.score_system.combo >= 8:
                self.achievement_manager.check_unlock("combo_god")

        if self.score_system.score >= 25000:
            self.achievement_manager.check_unlock("high_scorer")

        for px, py, pcol in summary.get("powerup_auras", []):
            self.particles.spawn_powerup_sparkle(px, py, color=pcol)

        if summary["player_hit"]:
            self.sound_manager.play_hit()
            self._hit_stop = 0.04
            if self.shake_setting != "off":
                self._screen_shake = 0.25
                self._shake_intensity = 6.0 * (0.4 if self.shake_setting == "low" else 1.0)

        if summary["kills"] > 0 or summary.get("kamikaze_exploded"):
            self.sound_manager.play_explosion()

        if summary.get("kamikaze_exploded"):
            if self.shake_setting != "off":
                self._screen_shake = 0.40
                self._shake_intensity = 10.0 * (0.4 if self.shake_setting == "low" else 1.0)

        if summary["powerup_picked"]:
            self.sound_manager.play_powerup()
            if self.boon_manager.has_synergy("oceanic_surge"):
                self.player.heal(15)
                self.floating_texts.spawn_notification(self.player.x, self.player.y + 25, "+15 HP OCEANIC SURGE!", (80, 240, 255))
                self.particles.spawn_powerup_sparkle(self.player.x, self.player.y, color=(80, 240, 255))
                for eb in self.enemy_bullets[:]:
                    if math.hypot(eb.x - self.player.x, eb.y - self.player.y) < 250:
                        eb.alive = False
                        self.particles.spawn_hit_sparks(eb.x, eb.y, count=3, color=(80, 240, 255))

        if self._screen_shake > 0:
            self._screen_shake -= delta_time

        self.enemies        = [e for e in self.enemies        if e.alive]
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemy_bullets  = [b for b in self.enemy_bullets  if b.alive]
        self.powerups       = [p for p in self.powerups       if p.alive]

        # Boss Tracking & Achievements
        from game.entities.enemies.boss_ravana import BossRavana
        from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
        prev_boss = self._boss
        self._boss = next(
            (e for e in self.enemies if isinstance(e, (BossRavana, BossKumbhakarna))), None
        )
        if self._boss and not self._boss_announced:
            self._cinematic_timer = 2.4
            self.sound_manager.play_warning_siren()
            self.sound_manager.play_boss_roar()
            if isinstance(self._boss, BossRavana):
                self._cinematic_title = "👑 LANKAPATI RAVANA"
                self._cinematic_subtitle = "LORD OF THE TEN HEADS — DEMON EMPEROR OF LANKA"
                self._cinematic_color = (255, 60, 80)
            else:
                self._cinematic_title = "🛡️ TITAN KUMBHAKARNA"
                self._cinematic_subtitle = "THE GIGANTIC ARMORED TITAN AWAKENS"
                self._cinematic_color = (255, 180, 40)
            self._boss_announced = True
        elif not self._boss:
            if isinstance(prev_boss, BossKumbhakarna):
                self.achievement_manager.check_unlock("kumbhakarna_bane")
            self._boss_announced = False

        if self.wave_manager.boss_wave_cleared and not self.is_endless:
            self.achievement_manager.check_unlock("ravana_vanquisher")
            if self._difficulty == "hard":
                self.achievement_manager.check_unlock("hardcore_hero")
            self._go_to_victory()
            return

        if not self.player.alive and self._death_phase is None:
            self._start_death_sequence()

    # ── Draw ────────────────────────────────────────────────────────────

    def on_draw(self) -> None:
        import random
        self.clear()

        ox, oy = 0.0, 0.0
        if self._screen_shake > 0 and self.shake_setting != "off":
            ox = random.uniform(-self._shake_intensity, self._shake_intensity)
            oy = random.uniform(-self._shake_intensity, self._shake_intensity)

        # Background & Hazards
        self.bg.draw(self.player.x + ox, self.player.y + oy, wave_num=self.wave_manager.wave_number)
        self.hazard_manager.draw(ox, oy)

        # Aim Laser Tracer
        aim_rad = math.radians(self.player.angle)
        aim_end_x = self.player.x + math.cos(aim_rad) * 140
        aim_end_y = self.player.y + math.sin(aim_rad) * 140
        arcade.draw_line(self.player.x + ox, self.player.y + oy, aim_end_x + ox, aim_end_y + oy, (100, 200, 255, 60), 1)

        # Particles & Collectables
        self.particles.draw(ox, oy)
        for pu in self.powerups:
            pu.x += ox; pu.y += oy; pu.draw(); pu.x -= ox; pu.y -= oy
        for chk in self.chakrams:
            chk.x += ox; chk.y += oy; chk.draw(); chk.x -= ox; chk.y -= oy
        for enemy in self.enemies:
            enemy.x += ox; enemy.y += oy; enemy.draw(); enemy.x -= ox; enemy.y -= oy
        for b in self.enemy_bullets:
            b.x += ox; b.y += oy; b.draw(); b.x -= ox; b.y -= oy
        for b in self.player_bullets:
            b.x += ox; b.y += oy; b.draw(); b.x -= ox; b.y -= oy

        # Player Vimana
        self.player.x += ox; self.player.y += oy
        self.player.draw()
        self.player.x -= ox; self.player.y -= oy

        # Floating Texts & HUD
        self.floating_texts.draw(ox, oy)
        self.hud.draw(self.player, self.score_system, self.wave_manager, self.enemies, self.powerups, self.boon_manager)
        self.boss_bar.draw(self._boss)
        self.achievement_manager.draw()

        # Boss Entrance Cinematic Overlay
        if self._cinematic_timer > 0:
            self._draw_boss_cinematic()

        # Death sequence overlays
        if self._death_phase is not None:
            self._draw_death_overlay()

        if self.paused:
            self._draw_pause()

        # View transition overlay (always last)
        TransitionOverlay.draw()

    def _draw_boss_cinematic(self) -> None:
        # Widescreen cinematic letterbox bars
        bar_height = 65
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, HEIGHT - bar_height, HEIGHT, (5, 5, 12, 240))
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, bar_height, (5, 5, 12, 240))
        arcade.draw_line(0, HEIGHT - bar_height, WIDTH, HEIGHT - bar_height, self._cinematic_color, 2)
        arcade.draw_line(0, bar_height, WIDTH, bar_height, self._cinematic_color, 2)

        # Title slam with elastic easing
        cy = HEIGHT // 2 + 10
        # Progress 0→1 over the first 0.8s of the cinematic
        intro_t = clamp(1.0 - (self._cinematic_timer - 1.4) / 0.8) if self._cinematic_timer > 1.4 else 1.0
        title_scale = ease_out_elastic(intro_t) if intro_t < 1.0 else 1.0
        title_y_offset = int((1.0 - title_scale) * 80)

        # Pulsing glow
        pulse_t = clamp((math.sin(self._cinematic_timer * 6.0) + 1.0) * 0.5)
        glow_a = int(lerp(160, 255, ease_out_cubic(pulse_t)))

        # Scan line wipe (first 0.6s)
        if self._cinematic_timer > 1.8:
            scan_t = clamp(1.0 - (self._cinematic_timer - 1.8) / 0.6)
            scan_y = int(HEIGHT * ease_out_cubic(scan_t))
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, scan_y - 2, scan_y + 3, (255, 255, 255, 60))

        arcade.draw_lrbt_rectangle_filled(WIDTH // 2 - 300, WIDTH // 2 + 300, cy - 35 - title_y_offset, cy + 45 - title_y_offset, (15, 10, 25, 210))
        arcade.draw_lrbt_rectangle_outline(WIDTH // 2 - 300, WIDTH // 2 + 300, cy - 35 - title_y_offset, cy + 45 - title_y_offset, (*self._cinematic_color, glow_a), 2)

        arcade.draw_text(self._cinematic_title, WIDTH // 2, cy + 12 - title_y_offset, (*self._cinematic_color, glow_a), font_size=22, bold=True, anchor_x="center", anchor_y="center")

        # Subtitle fades in 0.3s after title
        sub_alpha = int(255 * clamp((1.0 - self._cinematic_timer / 1.8) * 3.0)) if self._cinematic_timer < 1.8 else 0
        if sub_alpha > 0:
            arcade.draw_text(self._cinematic_subtitle, WIDTH // 2, cy - 18 - title_y_offset, (220, 230, 255, sub_alpha), font_size=10, bold=True, anchor_x="center", anchor_y="center")

    def _draw_death_overlay(self) -> None:
        """Cinematic death overlay: desaturation → freeze flash → fade to dark red."""
        if self._death_desat > 0:
            # Grey desaturation overlay
            a = int(120 * self._death_desat)
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (80, 80, 80, a))

        if self._death_phase == "freeze":
            # Brief white flash at start of freeze
            flash = max(0, 1.0 - self._death_timer * 5.0)
            if flash > 0:
                arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (255, 255, 255, int(80 * flash)))
            # Full desaturation hold
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (80, 80, 80, 100))

        if self._death_fade > 0:
            # Fade to dark red
            a = int(255 * ease_out_cubic(self._death_fade))
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (25, 5, 8, a))

    def _draw_pause(self) -> None:
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (0, 0, 0, 170))
        self._pause_title.draw()
        self._pause_hint.draw()

    # ── Helpers ─────────────────────────────────────────────────────────

    def _activate_bomb(self) -> None:
        self.sound_manager.play_explosion(volume=1.0)
        self.combat_stats["bombs_used"] += 1
        killed_count = 0
        for enemy in self.enemies:
            if enemy.alive:
                enemy.alive = False
                self.score_system.register_kill(enemy.score_value)
                self.player.enemies_killed += 1
                killed_count += 1
                self.combat_stats["total_damage"] += 999
                self.particles.spawn_explosion(enemy.x, enemy.y, radius=35, count=35, base_color=(255, 60, 220))
                self.floating_texts.spawn_damage(enemy.x, enemy.y, 999, is_crit=True)
        self.enemy_bullets.clear()
        if killed_count >= 8:
            self.achievement_manager.check_unlock("bomb_annihilator")

        if self.shake_setting != "off":
            self._screen_shake = 0.6
            self._shake_intensity = 14.0 if self.shake_setting == "full" else 6.0

    def _go_to_victory(self) -> None:
        SoundManager.stop_music()
        self.sound_manager.play_victory()
        from game.views.name_entry_view import NameEntryView
        transition_to(self.window, NameEntryView(
            score=self.score_system.score,
            wave=self.wave_manager.wave_number,
            kills=self.player.enemies_killed,
            highest_combo=self.score_system.highest_combo,
            difficulty=self._difficulty,
            is_victory=True,
            stats=self.combat_stats,
        ), duration=0.5, style="wipe")

    def _start_death_sequence(self) -> None:
        """Begin the cinematic death: slow-mo → freeze → fade → game over."""
        self._death_phase = "slowmo"
        self._death_timer = 0.0
        self._death_desat = 0.0
        self._death_fade = 0.0
        self.sound_manager.play_game_over()
        # Dramatic particle burst at death position
        self.particles.spawn_explosion(self.player.x, self.player.y,
                                       radius=50, count=40,
                                       base_color=(255, 60, 60))
        if self.shake_setting != "off":
            self._screen_shake = 0.5
            self._shake_intensity = 10.0

    def _finish_game_over(self) -> None:
        """Called after death sequence completes — transition to game over screen."""
        SoundManager.stop_music()
        from game.views.name_entry_view import NameEntryView
        self.window.show_view(NameEntryView(
            score=self.score_system.score,
            wave=self.wave_manager.wave_number,
            kills=self.player.enemies_killed,
            highest_combo=self.score_system.highest_combo,
            difficulty=self._difficulty,
            is_victory=False,
            stats=self.combat_stats,
        ))
