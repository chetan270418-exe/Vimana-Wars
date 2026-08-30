import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system
from game.ui.easing import ease_out_cubic, ease_out_elastic, ease_in_out_cubic, clamp
from game.ui.tween import TweenManager
from game.ui.transitions import transition_to, TransitionOverlay
try:
    from game.systems.sound_manager import SoundManager
except ImportError:
    SoundManager = None


class _FloatRef:
    """Mutable float holder so we can tween list-element 'alpha' values.
    Lists don't support setattr(list, idx, val) so we wrap each alpha."""
    __slots__ = ("val",)
    def __init__(self, val: float = 0.0):
        self.val = val

class ConfettiParticle:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.life = 2.0
        self.max_life = 2.0
        self.angle = random.uniform(0, 360)
        self.d_angle = random.uniform(-100, 100)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dy -= 300 * dt  # gravity
        self.angle += self.d_angle * dt
        self.life -= dt

    def draw(self):
        if self.life > 0:
            # Eased alpha
            t = 1.0 - (self.life / self.max_life)
            alpha_t = ease_out_cubic(1.0 - t)
            alpha = int(255 * alpha_t)
            c = self.color[:3] + (alpha,)
            arcade.draw_rect_filled(arcade.XYWH(self.x, self.y, 8, 8), c, self.angle)

class VictoryView(arcade.View):
    def __init__(self, score, kills, highest_combo, difficulty='normal',
                 ship_class='pushpaka', wave=10, stats=None):
        super().__init__()
        self.score = score
        self.kills = kills
        self.highest_combo = highest_combo
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.wave = wave
        self.stats = stats or {}
        
        self.time_elapsed = 0.0
        self._tweens = TweenManager()
        
        self._title_y = HEIGHT + 100.0
        self._displayed_score = 0.0
        # Wrapped float refs so each row alpha can be independently tweened.
        self._alpha_refs = [_FloatRef(0.0) for _ in range(5)]
        # Mirror list kept for the on_draw reads (avoids changing the draw code).
        self._row_alphas = [ref.val for ref in self._alpha_refs]
        
        self.particles = []
        self.particle_timer = 0.0
        
        # Glow pulse state
        self._glow_pulse = 0.0
        
    def on_show_view(self):
        if SoundManager:
            SoundManager.stop_music()

        arcade.set_background_color((5, 8, 20))

        # Reset animation state for repeat visits.
        self._title_y = HEIGHT + 100.0
        self._displayed_score = 0.0
        for ref in self._alpha_refs:
            ref.val = 0.0
        self._row_alphas = [ref.val for ref in self._alpha_refs]

        self._tweens.cancel_all()

        # Title slam-in
        self._tweens.tween(
            target=self,
            attr='_title_y',
            end=HEIGHT * 0.82,
            duration=0.8,
            ease=ease_out_elastic,
            start=HEIGHT + 100.0,
        )

        # Score count-up
        self._tweens.tween(
            target=self,
            attr='_displayed_score',
            end=float(self.score),
            duration=1.2,
            delay=0.5,
            ease=ease_out_cubic,
            start=0.0,
        )

        # Staggered stat reveal — tween each FloatRef's .val (lists don't support attr-by-index).
        for i, ref in enumerate(self._alpha_refs):
            self._tweens.tween(
                target=ref,
                attr='val',
                end=255.0,
                duration=0.5,
                delay=1.0 + i * 0.15,
                ease=ease_out_cubic,
                start=0.0,
            )

        try:
            save_system.update_after_game(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
                highest_combo=self.highest_combo,
                total_damage=self.stats.get("total_damage", 0),
                boons_claimed=self.stats.get("boons_claimed", 0),
                bosses_defeated=self.stats.get("bosses_defeated", []),
                ship_class=self.ship_class,
                campaign_cleared=True,
            )
            from game.systems.leaderboard_client import leaderboard_client
            leaderboard_client.push_profile()
        except Exception:
            pass
        
    def on_update(self, dt):
        self.time_elapsed += dt
        self._tweens.update(dt)
        TransitionOverlay.update(dt)

        # Sync the alpha mirror from the tweenable refs (draw code reads the list).
        for i, ref in enumerate(self._alpha_refs):
            self._row_alphas[i] = ref.val
        
        # Pulse for glow
        self._glow_pulse = ease_in_out_cubic((math.sin(self.time_elapsed * 3.0) + 1.0) / 2.0)
        
        # Confetti spawn
        self.particle_timer += dt
        if self.particle_timer > 0.05:
            self.particle_timer = 0.0
            colors = [
                (255, 215, 0),   # Gold
                (255, 223, 0),   # Yellow
                (0, 255, 255),   # Cyan
                (255, 0, 255)    # Magenta
            ]
            for _ in range(4):
                x = random.uniform(0, WIDTH)
                y = HEIGHT + 20
                dx = random.uniform(-100, 100)
                dy = random.uniform(-150, 50)
                c = random.choices(colors, weights=[0.6, 0.2, 0.1, 0.1])[0]
                self.particles.append(ConfettiParticle(x, y, dx, dy, c))
                
        # Update particles
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]
        
    def on_draw(self):
        self.clear()
        
        # Draw particles
        for p in self.particles:
            p.draw()
            
        # Draw Title with glow
        title_y = int(self._title_y)
        
        # Pulse glow
        glow_radius_1 = 60 + 20 * self._glow_pulse
        glow_radius_2 = 100 + 30 * self._glow_pulse
        
        arcade.draw_circle_filled(WIDTH // 2, title_y, glow_radius_2, (255, 215, 0, 20))
        arcade.draw_circle_filled(WIDTH // 2, title_y, glow_radius_1, (255, 215, 0, 40))
        
        arcade.draw_text(
            "VICTORY!",
            WIDTH // 2,
            title_y,
            arcade.color.GOLD,
            font_size=54,
            font_name="Kenney Future",
            anchor_x="center",
            anchor_y="center"
        )
        
        # Draw Stats
        base_y = int(HEIGHT * 0.6)
        spacing = 50
        
        # Score
        alpha0 = int(clamp(self._row_alphas[0], 0, 255))
        arcade.draw_text(f"Final Score: {int(self._displayed_score):,}", WIDTH // 2, base_y, COLOR_SCORE[:3] + (alpha0,), font_size=24, font_name="Kenney Future", anchor_x="center", anchor_y="center")
        
        # Kills
        alpha1 = int(clamp(self._row_alphas[1], 0, 255))
        arcade.draw_text(f"Enemies Destroyed: {self.kills}", WIDTH // 2, base_y - spacing, COLOR_WHITE[:3] + (alpha1,), font_size=20, font_name="Kenney Future", anchor_x="center", anchor_y="center")
        
        # Combo
        alpha2 = int(clamp(self._row_alphas[2], 0, 255))
        arcade.draw_text(f"Highest Combo: {self.highest_combo}", WIDTH // 2, base_y - spacing * 2, COLOR_WAVE[:3] + (alpha2,), font_size=20, font_name="Kenney Future", anchor_x="center", anchor_y="center")
        
        # Difficulty
        alpha3 = int(clamp(self._row_alphas[3], 0, 255))
        arcade.draw_text(f"Difficulty: {self.difficulty.capitalize()}", WIDTH // 2, base_y - spacing * 3, COLOR_WHITE[:3] + (alpha3,), font_size=20, font_name="Kenney Future", anchor_x="center", anchor_y="center")

        # Compact combat breakdown
        alpha4 = int(clamp(self._row_alphas[4], 0, 255))
        total_damage = int(self.stats.get("total_damage", 0))
        perfect_dodges = int(self.stats.get("perfect_dodges", 0))
        arcade.draw_text(
            f"Total Damage: {total_damage:,}  •  Perfect Dodges: {perfect_dodges}",
            WIDTH // 2, base_y - spacing * 4,
            (255, 170, 80, alpha4), font_size=15,
            font_name="Kenney Future", anchor_x="center", anchor_y="center",
        )
        
        # Prompts
        prompt_y = int(HEIGHT * 0.15)
        arcade.draw_text("Press ENTER to Continue", WIDTH // 2, prompt_y + 30, COLOR_WHITE[:3] + (alpha4,), font_size=16, font_name="Kenney Future", anchor_x="center", anchor_y="center")
        arcade.draw_text("Press L for Leaderboard", WIDTH // 2, prompt_y, COLOR_WHITE[:3] + (alpha4,), font_size=16, font_name="Kenney Future", anchor_x="center", anchor_y="center")
        arcade.draw_text("Press ESC for Main Menu", WIDTH // 2, prompt_y - 30, COLOR_WHITE[:3] + (alpha4,), font_size=16, font_name="Kenney Future", anchor_x="center", anchor_y="center")
        
        TransitionOverlay.draw()

    def on_key_press(self, symbol, modifiers):
        if TransitionOverlay.is_active:
            return
            
        if symbol == arcade.key.ENTER:
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView())
        elif symbol == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            transition_to(self.window, LeaderboardView())
        elif symbol == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())
