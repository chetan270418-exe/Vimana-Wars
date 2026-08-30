"""
game/views/game_over_view.py
Game-over screen — shows stats, high score, and difficulty played.
Uses arcade.Text objects (no draw_text calls).
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_SCORE, COLOR_WHITE
from game.ui.easing import ease_out_cubic, ease_in_out_cubic, clamp
from game.ui.tween import TweenManager, Tween
from game.ui.transitions import transition_to, TransitionOverlay


class GameOverView(arcade.View):
    def __init__(self, score: int, wave: int, kills: int,
                 highest_combo: int, high_score: int = 0, difficulty: str = "normal",
                 ship_class: str = "pushpaka", stats: dict = None,
                 start_wave: int = 1, is_endless: bool = False):
        super().__init__()
        self._pulse = 0.0
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.start_wave = start_wave
        self.is_endless = is_endless
        self.stats = stats or {}
        is_new_record = score >= high_score and score > 0

        self._tweens = TweenManager()
        self._title_chars = 0.0
        self._displayed_score = 0.0
        self._final_score = score
        
        # ── Particles ────────────────────────────────────────────────
        self._embers = []
        
        # ── Title ────────────────────────────────────────────────────
        self._title_text_str = "GAME OVER"
        self._title = arcade.Text(
            self._title_text_str,
            WIDTH // 2, int(HEIGHT * 0.82),
            (220, 30, 30), font_size=52, bold=True,
            anchor_x="center", anchor_y="center",
        )

        # ── New record banner ────────────────────────────────────────
        self._is_new_record = is_new_record
        self._record_banner = arcade.Text(
            "★  NEW HIGH SCORE  ★" if is_new_record else "",
            WIDTH // 2, int(HEIGHT * 0.72),
            (255, 220, 50), font_size=14, bold=True,
            anchor_x="center", anchor_y="center",
        )

        # ── Stats table ──────────────────────────────────────────────
        diff_colors = {"easy": (60, 220, 100), "normal": (220, 200, 60), "hard": (220, 60, 60)}
        total_dmg = self.stats.get("total_damage", 0)
        perf_dodges = self.stats.get("perfect_dodges", 0)
        syn_list = self.stats.get("synergies_activated", [])
        syn_str = ", ".join(s[:10] for s in syn_list) if syn_list else "None"

        self._stat_rows_data = [
            ("SCORE",           0,                    COLOR_SCORE),
            ("HIGH SCORE",      f"{high_score:,}",    (200, 200, 200)),
            ("DIFFICULTY",      difficulty.upper(),   diff_colors.get(difficulty, COLOR_WHITE)),
            ("WAVES SURVIVED",  f"{wave}",            COLOR_WHITE),
            ("ENEMIES SLAIN",   f"{kills}",           COLOR_WHITE),
            ("HIGHEST COMBO",   f"×{highest_combo}",  COLOR_WHITE),
            ("TOTAL DAMAGE",    f"{total_dmg:,}",     (255, 160, 60)),
            ("PERFECT DODGES",  f"{perf_dodges}",     (100, 255, 200)),
            ("DEVA SYNERGIES",  syn_str,              (255, 120, 220)),
        ]
        
        num_rows = len(self._stat_rows_data)
        self._stat_labels = []
        self._stat_values = []
        self._row_alphas = [0.0] * num_rows

        for i, (label, value, val_color) in enumerate(self._stat_rows_data):
            y = int(HEIGHT * 0.62) - i * 22
            self._stat_labels.append(arcade.Text(
                label, WIDTH // 2 - 160, y,
                (140, 140, 170, 0), font_size=10, bold=True,
            ))
            val_str = str(value)
            self._stat_values.append(arcade.Text(
                val_str, WIDTH // 2 + 160, y,
                (*val_color[:3], 0), font_size=11, bold=True,
                anchor_x="right",
            ))

        # ── Prompt ───────────────────────────────────────────────────
        self._prompt = arcade.Text(
            "R — Quick Restart   •   L — Leaderboard   •   S — Stats   •   ESC — Main Menu",
            WIDTH // 2, int(HEIGHT * 0.06),
            COLOR_WHITE, font_size=12, bold=True,
            anchor_x="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color((15, 2, 5))
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()
        
        # Start tweens
        self._tweens.cancel_all()
        
        # 1. Title typewriter
        self._tweens.tween(
            self, "_title_chars",
            end=len(self._title_text_str),
            duration=0.8,
            ease=ease_out_cubic,
            start=0.0
        )
        
        # 2. Score count up (starting at 0.5s)
        self._tweens.tween(
            self, "_displayed_score",
            end=self._final_score,
            duration=1.0, 
            delay=0.5,
            ease=ease_out_cubic,
            start=0.0
        )
        
        # 3. Staggered row reveals
        class FloatRef:
            def __init__(self):
                self.val = 0.0
                
        self._alpha_refs = [FloatRef() for _ in range(len(self._row_alphas))]
        for i, ref in enumerate(self._alpha_refs):
            self._tweens.tween(
                ref, "val",
                end=255.0,
                duration=0.5, 
                delay=1.0 + i * 0.15,
                ease=ease_out_cubic,
                start=0.0
            )

    def on_update(self, delta_time: float) -> None:
        self._tweens.update(delta_time)
        TransitionOverlay.update(delta_time)

        # Sync row alphas from refs
        if hasattr(self, "_alpha_refs"):
            for i, ref in enumerate(self._alpha_refs):
                self._row_alphas[i] = ref.val

        # Prompt uses ease_in_out_cubic pulse
        self._pulse += delta_time
        cycle = (self._pulse % 2.0)
        t = cycle if cycle <= 1.0 else 2.0 - cycle
        eased_t = ease_in_out_cubic(t)
        alpha = int(100 + 155 * eased_t)
        p_c = self._prompt.color
        self._prompt.color = (p_c[0], p_c[1], p_c[2], alpha)

        # Update dynamic score text
        self._stat_values[0].text = f"{int(self._displayed_score):,}"

        # Apply alphas to stat rows
        for i, a in enumerate(self._row_alphas):
            a_int = int(clamp(a, 0, 255))
            lbl_color = self._stat_labels[i].color
            val_color = self._stat_values[i].color
            self._stat_labels[i].color = (lbl_color[0], lbl_color[1], lbl_color[2], a_int)
            self._stat_values[i].color = (val_color[0], val_color[1], val_color[2], a_int)

        # Embers logic
        for _ in range(2):
            self._embers.append({
                "x": random.uniform(0, WIDTH),
                "y": HEIGHT + 10,
                "vy": random.uniform(-60, -20),
                "size": random.uniform(1, 3),
                "life": random.uniform(2.0, 5.0),
                "max_life": 5.0,
                "color": random.choice([(255, 100, 50), (255, 150, 0), (200, 50, 50)])
            })
            
        for e in self._embers[:]:
            e["y"] += e["vy"] * delta_time
            e["life"] -= delta_time
            if e["life"] <= 0 or e["y"] < -10:
                self._embers.remove(e)

    def on_draw(self) -> None:
        self.clear()
        
        # Draw embers
        for e in self._embers:
            alpha = int(255 * clamp(e["life"] / e["max_life"], 0.0, 1.0))
            color = (*e["color"], alpha)
            arcade.draw_circle_filled(e["x"], e["y"], e["size"], color)
            
        # Draw title
        chars = int(self._title_chars)
        if chars > 0:
            self._title.text = self._title_text_str[:chars]
            self._title.draw()

        if self._is_new_record:
            self._record_banner.draw()

        # Draw stats
        for lbl, val in zip(self._stat_labels, self._stat_values):
            lbl.draw()
            val.draw()

        self._prompt.draw()
        
        TransitionOverlay.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.R:
            from game.views.game_view import GameView
            transition_to(
                self.window,
                GameView(
                    difficulty=self.difficulty,
                    ship_class=self.ship_class,
                    start_wave=self.start_wave,
                    is_endless=self.is_endless,
                ),
            )
        elif key == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            transition_to(self.window, LeaderboardView(return_view=self))
        elif key == arcade.key.S:
            from game.views.stats_view import StatsView
            transition_to(self.window, StatsView(return_view=self))
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())
