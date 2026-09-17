"""
game/views/loading_screen.py
Cinematic Loading and Prologue Screen for Vimana Wars: "The Reclamation of Dharma".
Displays high-tech Vedic-punk visuals, narrative crawl, and asset initialization
telemetry after the automatic launch cinematic has finished.
"""
import math
import arcade

from constants import WIDTH, HEIGHT
from game.systems.asset_manager import AssetManager
from game.systems.sound_manager import SoundManager
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, GOLD, GOLD_BRIGHT, CYAN, CYAN_BRIGHT,
    PARCHMENT, MUTED, draw_chamfered_panel, draw_corner_etching,
    draw_segmented_bar, draw_scanlines, draw_telemetry_ticks, pulse_alpha,
    FONT_CEREMONIAL, FONT_TELEMETRY, FONT_INTERFACE
)
from game.ui.easing import ease_out_cubic, clamp


_STORY_LINES = [
    "Dharma is not a place. It is a balance — and it is breaking.",
    "Ravana has broken his exile. The celestial realms are falling under his shadow.",
    "You are the last Vimana pilot the Celestial Order could spare.",
    "Fly. Reclaim what is falling. End this at Lanka, or don't come back.",
]

_SYS_STEPS = [
    (0.15, "INITIALIZING VIMANA POWER CORE..."),
    (0.40, "ATTUNING OJAS AND PRANA TELEMETRY..."),
    (0.65, "CALIBRATING ASTRAL CANNONS AND SHIELDS..."),
    (0.85, "CONNECTING TO AKASHIC CHRONICLES..."),
    (1.00, "COMMAND CONSOLE READY"),
]


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self._elapsed = 0.0
        self._progress = 0.0
        self._ready_to_advance = False
        self._advance_requested = False
        self.sound_manager = SoundManager()

        # Cached text labels
        self._title = arcade.Text(
            "VIMANA WARS", WIDTH // 2, HEIGHT - 75,
            GOLD_BRIGHT, font_size=32, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_CEREMONIAL[0],
        )
        self._subtitle = arcade.Text(
            "THE RECLAMATION OF DHARMA // CELESTIAL PROLOGUE", WIDTH // 2, HEIGHT - 110,
            CYAN_BRIGHT, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        self._status_label = arcade.Text(
            "INITIALIZING SYSTEMS...", WIDTH // 2, 115,
            GOLD, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        self._prompt = arcade.Text(
            "PRESS SPACE OR ENTER TO ENGAGE COMMAND CONSOLE", WIDTH // 2, 45,
            GOLD_BRIGHT, font_size=12, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        # Starfield
        self._stars = [
            (
                (i * 73 + 19) % WIDTH,
                (i * 127 + 41) % HEIGHT,
                0.8 + ((i % 5) * 0.25),
                80 + (i % 120),
            )
            for i in range(110)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._elapsed += delta_time

        # Smooth loading progress over ~2.6 seconds
        target_progress = min(1.0, self._elapsed / 2.6)
        self._progress = clamp(ease_out_cubic(target_progress), 0.0, 1.0)

        # Status text update
        current_status = "INITIALIZING SYSTEMS..."
        for threshold, text in _SYS_STEPS:
            if self._progress >= threshold:
                current_status = text
        self._status_text_str = current_status
        try:
            self._status_label.text = current_status
        except Exception:
            pass

        if self._progress >= 1.0:
            self._ready_to_advance = True
            # Loading is now a real boot phase: once the systems are ready,
            # continue automatically instead of waiting for a key press.
            if self._elapsed >= 3.25:
                self._advance_to_menu()

    def on_draw(self) -> None:
        self.clear()

        # 1. Parallax deep space background
        for x, y, size, alpha in self._stars:
            twinkle = int(alpha + 30 * math.sin(self._elapsed * 2.5 + x * 0.05))
            twinkle = max(40, min(255, twinkle))
            arcade.draw_circle_filled(x, y, size, (180, 210, 255, twinkle))

        # 2. Hero illustration backdrop
        hero = AssetManager.texture("hero_vimana_wars.png")
        if hero:
            hero_alpha = int(clamp(self._elapsed * 45, 0, 110))
            AssetManager.draw(hero, WIDTH // 2, HEIGHT // 2 + 10, 680, 450, color=(255, 255, 255, hero_alpha))

        # 3. Holographic frame and scanlines
        draw_scanlines(20, WIDTH - 20, 20, HEIGHT - 20, CYAN, spacing=24, alpha=6)
        draw_chamfered_panel(40, WIDTH - 40, 30, HEIGHT - 30, GOLD, fill=OBSIDIAN, alpha=185, cut=18)
        draw_corner_etching(40, WIDTH - 40, 30, HEIGHT - 30, GOLD, length=28, alpha=140)
        draw_telemetry_ticks(60, WIDTH - 60, HEIGHT - 130, CYAN, count=25, height=4, alpha=70)
        draw_telemetry_ticks(60, WIDTH - 60, 150, GOLD, count=25, height=4, alpha=70)

        # 4. Logo and Title
        logo = AssetManager.texture("vimana_wars_logo.png")
        if logo:
            logo_y = HEIGHT - 75
            AssetManager.draw(logo, WIDTH // 2 - 165, logo_y, 48, 48)
            AssetManager.draw(logo, WIDTH // 2 + 165, logo_y, 48, 48)

        self._title.draw()
        self._subtitle.draw()

        # 5. Narrative Prologue Crawl
        box_top = HEIGHT - 160
        line_height = 36
        for idx, line in enumerate(_STORY_LINES):
            line_delay = 0.3 + idx * 0.55
            fade = clamp((self._elapsed - line_delay) / 0.8, 0.0, 1.0)
            if fade > 0.0:
                alpha = int(255 * ease_out_cubic(fade))
                color = GOLD_BRIGHT if idx in (0, 3) else PARCHMENT
                arcade.draw_text(
                    line,
                    WIDTH // 2, box_top - idx * line_height,
                    (*color[:3], alpha),
                    font_size=11, bold=(idx == 0 or idx == 3),
                    anchor_x="center", anchor_y="center",
                    font_name=FONT_INTERFACE[0]
                )

        # 6. Segmented Telemetry Progress Bar
        bar_w = 460
        bar_left = (WIDTH - bar_w) // 2
        bar_right = bar_left + bar_w
        draw_segmented_bar(bar_left, bar_right, 126, 138, self._progress, color=CYAN_BRIGHT, segments=18, gap=4)
        pct = int(self._progress * 100)
        arcade.draw_text(f"{pct}%", bar_right + 12, 132, CYAN, font_size=9, bold=True, anchor_y="center")

        self._status_label.draw()

        # 7. Automatic hand-off prompt
        if self._ready_to_advance:
            p_alpha = pulse_alpha(self._elapsed, 160, 255, 3.5)
            self._prompt.text = "COMMAND CONSOLE READY // ENTERING..."
            self._prompt.color = (*GOLD_BRIGHT[:3], p_alpha)
            self._prompt.draw()
        else:
            skip_hint = "LOADING CELESTIAL SYSTEMS..."
            arcade.draw_text(skip_hint, WIDTH // 2, 45, MUTED, font_size=10, anchor_x="center", anchor_y="center")

        TransitionOverlay.draw()

    def _advance_to_menu(self) -> None:
        if self._advance_requested or TransitionOverlay.is_active:
            return
        self._advance_requested = True
        self.sound_manager.play_ui_click()
        # Give first-time pilots a skippable narrative briefing.  Returning
        # players go straight to the command console, so the story never
        # becomes startup friction.
        from game.systems import save_system
        if not save_system.load().get("story_intro_seen", False):
            from game.views.story_briefing_view import StoryBriefingView
            transition_to(self.window, StoryBriefingView())
        else:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self._ready_to_advance:
            self._advance_to_menu()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.SPACE, arcade.key.ENTER, arcade.key.ESCAPE):
            self._advance_to_menu()
