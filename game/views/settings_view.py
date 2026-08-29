"""
game/views/settings_view.py
In-game Settings & Configuration view.
Allows players to configure Audio Volume, Screen Shake, Particles, and Display Mode.
Saves settings automatically to ~/.vimana_wars/save.json.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system


_VOLUME_STEPS = [0, 20, 40, 60, 80, 100]
_SHAKE_OPTIONS = ["full", "low", "off"]
_PARTICLE_OPTIONS = ["high", "low"]


class SettingsView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._selected_row = 0

        # Load current settings
        data = save_system.load()
        self.volume = data.get("volume", 80)
        self.sfx_volume = data.get("sfx_volume", data.get("volume", 80))
        self.music_volume = data.get("music_volume", data.get("volume", 80))
        self.screen_shake = data.get("screen_shake", "full")
        self.particles = data.get("particles", "high")
        self.fullscreen = data.get("fullscreen", False)

        # ── UI Texts ─────────────────────────────────────────────────
        self._title = arcade.Text(
            "SETTINGS & OPTIONS",
            WIDTH // 2, HEIGHT - 65,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "↑ ↓ : Select   •   ← → / ENTER : Change   •   ESC : Save & Return",
            WIDTH // 2, 35,
            (160, 160, 190), font_size=12, bold=True,
            anchor_x="center"
        )

        self._row_labels = [
            "SFX VOLUME",
            "MUSIC VOLUME",
            "SCREEN SHAKE",
            "PARTICLE QUALITY",
            "DISPLAY MODE",
        ]

    def _save_and_apply(self) -> None:
        data = save_system.load()
        data["volume"] = self.sfx_volume
        data["sfx_volume"] = self.sfx_volume
        data["music_volume"] = self.music_volume
        data["screen_shake"] = self.screen_shake
        data["particles"] = self.particles
        data["fullscreen"] = self.fullscreen
        save_system.save(data)

        # Dynamically reload active view subsystems immediately
        target = self.return_view
        if hasattr(target, "game_view"):  # If returning to PauseView
            target = target.game_view
        if target:
            if hasattr(target, "particles") and hasattr(target.particles, "reload_settings"):
                target.particles.reload_settings()
            if hasattr(target, "sound_manager") and hasattr(target.sound_manager, "reload_volume"):
                target.sound_manager.reload_volume()
            if hasattr(target, "shake_setting"):
                target.shake_setting = self.screen_shake

        # Apply fullscreen to active window
        if self.window:
            if self.window.fullscreen != self.fullscreen:
                self.window.set_fullscreen(self.fullscreen)

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_draw(self) -> None:
        self.clear()

        self._title.draw()

        start_y = HEIGHT - 145
        row_height = 54

        for i, label in enumerate(self._row_labels):
            y = start_y - i * row_height
            is_selected = (i == self._selected_row)

            # Row background highlight
            if is_selected:
                arcade.draw_lrbt_rectangle_filled(
                    WIDTH // 2 - 260, WIDTH // 2 + 260,
                    y - 16, y + 22,
                    (30, 40, 75)
                )
                arcade.draw_lrbt_rectangle_outline(
                    WIDTH // 2 - 260, WIDTH // 2 + 260,
                    y - 16, y + 22,
                    COLOR_SCORE, 2
                )
                label_col = COLOR_SCORE
            else:
                label_col = (180, 190, 210)

            # Setting Label
            arcade.draw_text(label, WIDTH // 2 - 230, y - 2, label_col, font_size=13, bold=True)

            # Setting Value
            val_str = ""
            if i == 0:
                val_str = f"«  {self.sfx_volume}%  »"
            elif i == 1:
                val_str = f"«  {self.music_volume}%  »"
            elif i == 2:
                val_str = f"«  {self.screen_shake.upper()}  »"
            elif i == 3:
                val_str = f"«  {self.particles.upper()}  »"
            elif i == 4:
                val_str = "«  FULLSCREEN  »" if self.fullscreen else "«  WINDOWED  »"

            arcade.draw_text(
                val_str, WIDTH // 2 + 230, y - 2,
                COLOR_WHITE if is_selected else (150, 160, 180),
                font_size=13, bold=True, anchor_x="right"
            )

        # Cheatsheet panel at bottom
        arcade.draw_lrbt_rectangle_filled(WIDTH // 2 - 260, WIDTH // 2 + 260, 75, 140, (15, 18, 35))
        arcade.draw_text(
            "CONTROLS: WASD/Arrows to Move  •  Hold LMB to Shoot  •  F for Brahmastra Bomb",
            WIDTH // 2, 115, (140, 170, 220), font_size=10, bold=True, anchor_x="center"
        )
        arcade.draw_text(
            "GAMEPAD: Left Stick (Fly)  •  Right Stick (Aim 360°)  •  RT (Shoot)  •  X / LT (Bomb)",
            WIDTH // 2, 92, (120, 220, 180), font_size=10, bold=True, anchor_x="center"
        )

        self._hint.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._selected_row = (self._selected_row - 1) % len(self._row_labels)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected_row = (self._selected_row + 1) % len(self._row_labels)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self._adjust_option(-1)
        elif key in (arcade.key.RIGHT, arcade.key.D, arcade.key.ENTER, arcade.key.RETURN):
            self._adjust_option(1)
        elif key in (arcade.key.ESCAPE, arcade.key.BACKSPACE):
            self._save_and_apply()
            if self.return_view:
                self.window.show_view(self.return_view)
            else:
                from game.views.menu_view import MenuView
                self.window.show_view(MenuView())

    def _adjust_option(self, direction: int) -> None:
        if self._selected_row == 0:  # SFX Volume
            curr_idx = _VOLUME_STEPS.index(self.sfx_volume) if self.sfx_volume in _VOLUME_STEPS else 4
            new_idx = (curr_idx + direction) % len(_VOLUME_STEPS)
            self.sfx_volume = _VOLUME_STEPS[new_idx]

        elif self._selected_row == 1:  # Music Volume
            curr_idx = _VOLUME_STEPS.index(self.music_volume) if self.music_volume in _VOLUME_STEPS else 4
            new_idx = (curr_idx + direction) % len(_VOLUME_STEPS)
            self.music_volume = _VOLUME_STEPS[new_idx]

        elif self._selected_row == 2:  # Screen shake
            curr_idx = _SHAKE_OPTIONS.index(self.screen_shake)
            new_idx = (curr_idx + direction) % len(_SHAKE_OPTIONS)
            self.screen_shake = _SHAKE_OPTIONS[new_idx]

        elif self._selected_row == 3:  # Particles
            curr_idx = _PARTICLE_OPTIONS.index(self.particles)
            new_idx = (curr_idx + direction) % len(_PARTICLE_OPTIONS)
            self.particles = _PARTICLE_OPTIONS[new_idx]

        elif self._selected_row == 4:  # Fullscreen
            self.fullscreen = not self.fullscreen
