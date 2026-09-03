"""
game/views/settings_view.py
In-game Settings & Configuration view.
Allows players to configure Audio Volume, Screen Shake, Particles, and Display Mode.
Saves settings automatically to ~/.vimana_wars/save.json.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WHITE
from game.systems import save_system
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import draw_menu_backdrop, draw_focus_panel


_VOLUME_STEPS = [0, 20, 40, 60, 80, 100]
_SHAKE_OPTIONS = ["full", "low", "off"]
_PARTICLE_OPTIONS = ["high", "low"]
_COLORBLIND_OPTIONS = ["off", "protan", "deutan", "tritan"]


class SettingsView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._selected_row = 0

        # Load current settings
        data = save_system.load()
        self.sfx_volume = data.get("sfx_volume", data.get("volume", 80))
        self.music_volume = data.get("music_volume", data.get("volume", 80))
        self.screen_shake = data.get("screen_shake", "full")
        self.particles = data.get("particles", "high")
        self.reduced_flashes = data.get("reduced_flashes", False)
        self.colorblind_mode = data.get("colorblind_mode", "off")
        self.fullscreen = data.get("fullscreen", False)

        from game.systems.sound_manager import SoundManager
        self.sound_manager = SoundManager()

        # ── UI Texts ─────────────────────────────────────────────────
        self._title = arcade.Text(
            "SETTINGS & ACCESSIBILITY",
            WIDTH // 2, HEIGHT - 55,
            COLOR_SCORE, font_size=28, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "↑ ↓ : Select   •   ← → / ENTER : Change   •   ESC : Save & Return",
            WIDTH // 2, 35,
            (160, 160, 190), font_size=11, bold=True,
            anchor_x="center"
        )

        self._row_labels = [
            "SFX VOLUME",
            "MUSIC VOLUME",
            "SCREEN SHAKE",
            "PARTICLE QUALITY",
            "REDUCED FLASHES",
            "COLORBLIND MODE",
            "DISPLAY MODE",
        ]

    def _save_and_apply(self) -> None:
        data = save_system.load()
        data["volume"] = self.sfx_volume
        data["sfx_volume"] = self.sfx_volume
        data["music_volume"] = self.music_volume
        data["screen_shake"] = self.screen_shake
        data["particles"] = self.particles
        data["reduced_flashes"] = self.reduced_flashes
        data["colorblind_mode"] = self.colorblind_mode
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
            if hasattr(target, "reduced_flashes"):
                target.reduced_flashes = self.reduced_flashes
            if hasattr(target, "colorblind_mode"):
                target.colorblind_mode = self.colorblind_mode
            if hasattr(target, "hud"):
                target.hud.colorblind_mode = self.colorblind_mode
                target.hud.reduced_flashes = self.reduced_flashes

        # Apply fullscreen to active window
        self._apply_fullscreen()

    def _apply_fullscreen(self) -> None:
        """Apply the display mode immediately and keep logical coordinates."""
        if not self.window:
            return
        desired_fullscreen = bool(self.fullscreen)
        try:
            if self.window.fullscreen != desired_fullscreen:
                self.window.set_fullscreen(desired_fullscreen)
            # VimanaWindow reapplies this automatically; the fallback keeps
            # the setting correct if another Arcade Window implementation is
            # used by a test harness or packaged build.
            apply_viewport = getattr(self.window, "_apply_logical_viewport", None)
            if apply_viewport:
                apply_viewport()
        except Exception:
            # Do not leave the UI claiming fullscreen if the OS rejects the
            # mode switch (for example, a monitor with no usable mode).
            self.fullscreen = bool(getattr(self.window, "fullscreen", False))

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)

    def on_draw(self) -> None:
        draw_menu_backdrop("SETTINGS & ACCESSIBILITY", "LOCAL CONFIGURATION // CHANGES APPLY IMMEDIATELY", COLOR_SCORE, reduced=self.reduced_flashes)
        self._title.draw()

        start_y = HEIGHT - 115
        row_height = 42

        for i, label in enumerate(self._row_labels):
            y = start_y - i * row_height
            is_selected = (i == self._selected_row)

            # Row background highlight
            if is_selected:
                draw_focus_panel(WIDTH // 2 - 260, WIDTH // 2 + 260, y - 12, y + 16, COLOR_SCORE, selected=True)
                label_col = COLOR_SCORE
            else:
                label_col = (180, 190, 210)

            # Setting Label
            arcade.draw_text(label, WIDTH // 2 - 230, y - 2, label_col, font_size=12, bold=True)

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
                val_str = "«  ON  »" if self.reduced_flashes else "«  OFF  »"
            elif i == 5:
                val_str = f"«  {self.colorblind_mode.upper()}  »"
            elif i == 6:
                val_str = "«  FULLSCREEN  »" if self.fullscreen else "«  WINDOWED  »"

            arcade.draw_text(
                val_str, WIDTH // 2 + 230, y - 2,
                COLOR_WHITE if is_selected else (150, 160, 180),
                font_size=12, bold=True, anchor_x="right"
            )

        # Cheatsheet panel at bottom
        arcade.draw_lrbt_rectangle_filled(WIDTH // 2 - 260, WIDTH // 2 + 260, 70, 130, (15, 18, 35))
        arcade.draw_text(
            "CONTROLS: WASD/Arrows to Move  •  Hold LMB to Shoot  •  F for Brahmastra Bomb",
            WIDTH // 2, 106, (140, 170, 220), font_size=10, bold=True, anchor_x="center"
        )
        arcade.draw_text(
            "GAMEPAD: Left Stick (Fly)  •  Right Stick (Aim 360°)  •  RT (Shoot)  •  X / LT (Bomb)",
            WIDTH // 2, 84, (120, 220, 180), font_size=10, bold=True, anchor_x="center"
        )

        self._hint.draw()
        TransitionOverlay.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._selected_row = (self._selected_row - 1) % len(self._row_labels)
            self.sound_manager.play_ui_click()
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected_row = (self._selected_row + 1) % len(self._row_labels)
            self.sound_manager.play_ui_click()
        elif key in (arcade.key.LEFT, arcade.key.A):
            self._adjust_option(-1)
            self.sound_manager.play_ui_click()
        elif key in (arcade.key.RIGHT, arcade.key.D, arcade.key.ENTER, arcade.key.RETURN):
            self._adjust_option(1)
            self.sound_manager.play_ui_click()
        elif key in (arcade.key.ESCAPE, arcade.key.BACKSPACE):
            self._save_and_apply()
            if self.return_view:
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())

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

        elif self._selected_row == 4:  # Reduced Flashes
            self.reduced_flashes = not self.reduced_flashes

        elif self._selected_row == 5:  # Colorblind Mode
            curr_idx = _COLORBLIND_OPTIONS.index(self.colorblind_mode) if self.colorblind_mode in _COLORBLIND_OPTIONS else 0
            new_idx = (curr_idx + direction) % len(_COLORBLIND_OPTIONS)
            self.colorblind_mode = _COLORBLIND_OPTIONS[new_idx]

        elif self._selected_row == 6:  # Fullscreen
            self.fullscreen = not self.fullscreen
            self._apply_fullscreen()

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y > 0:
            self._selected_row = (self._selected_row - 1) % len(self._row_labels)
        elif hat_y < 0:
            self._selected_row = (self._selected_row + 1) % len(self._row_labels)
        if hat_x < 0:
            self._adjust_option(-1)
        elif hat_x > 0:
            self._adjust_option(1)

    def on_joybutton_press(self, joystick, button) -> None:
        # A / Cross changes the selected option; B / Circle saves and exits.
        if button == 0:
            self._adjust_option(1)
        elif button in (1, 4):
            self._save_and_apply()
            if self.return_view:
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())
