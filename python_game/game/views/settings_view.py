"""
game/views/settings_view.py
Console Settings & Accessibility View.
Follows Section 7.11 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, tabbed sections (Audio, Display, Accessibility, Controls),
diamond toggles, sliders with diamond thumbs, and conflict-safe keybind reference.
"""
import arcade

from constants import WIDTH, HEIGHT
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, BRASS, PARCHMENT,
    STARLIGHT, GREY, MUTED, WELL,
    FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
    draw_state_badge,
)


_TABS = ["AUDIO", "DISPLAY", "ACCESSIBILITY", "CONTROLS"]

_SHAKE_OPTIONS = ["full", "low", "off"]
_PARTICLE_OPTIONS = ["high", "low"]
_COLORBLIND_OPTIONS = ["off", "protan", "deutan", "tritan"]

_KEYBINDINGS = [
    ("MOVE UP", "W  /  UP ARROW", "Movement"),
    ("MOVE DOWN", "S  /  DOWN ARROW", "Movement"),
    ("MOVE LEFT", "A  /  LEFT ARROW", "Movement"),
    ("MOVE RIGHT", "D  /  RIGHT ARROW", "Movement"),
    ("PRIMARY FIRE", "SPACE  /  LEFT CLICK", "Combat"),
    ("DIVINE DASH / ABILITY", "SHIFT", "Combat"),
    ("PAUSE / ABANDON", "ESC", "System"),
    ("CINEMATIC TRAILER (PV)", "V", "System"),
    ("ARMORY SHORTCUT", "H  /  R", "System"),
]


class SettingsView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self.nav_rail = NavRail("settings")

        data = save_system.load()
        self.sfx_volume = data.get("sfx_volume", data.get("volume", 80))
        self.music_volume = data.get("music_volume", data.get("volume", 80))
        self.screen_shake = data.get("screen_shake", "full")
        self.particles = data.get("particles", "high")
        self.reduced_flashes = bool(data.get("reduced_flashes", False))
        self.colorblind_mode = data.get("colorblind_mode", "off")
        self.fullscreen = bool(data.get("fullscreen", False))

        self.sound_manager = SoundManager()

        self._active_tab = 0
        self._hovered_tab = -1
        self._pulse = 0.0
        self._dragging_slider = None  # 'sfx' or 'music'

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)

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

        target = self.return_view
        if hasattr(target, "game_view"):
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

        # Apply fullscreen if changed
        if self.window and self.window.fullscreen != self.fullscreen:
            self.window.set_fullscreen(self.fullscreen)

    def on_draw(self) -> None:
        self.clear()

        # Background scanlines
        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        arcade.draw_text("CONSOLE SETTINGS // CALIBRATION", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("AUDIO • DISPLAY • ACCESSIBILITY • KEYBINDINGS",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # ── Tab Switcher Strip (y=500 to 536) ────────────────────────────────
        tab_w = 145.0
        start_x = 240.0
        for i, tname in enumerate(_TABS):
            tx = start_x + i * (tab_w + 10)
            is_active = (i == self._active_tab)
            is_hov = (i == self._hovered_tab)

            fill_col = SURFACE_HIGH if is_active else (SURFACE_LOW if is_hov else WELL)
            border_col = GOLD if is_active else (CYAN if is_hov else GREY)

            draw_chamfered_panel(tx, tx + tab_w, 502, 536, border_col,
                                 fill=fill_col, alpha=230, border_width=2 if is_active else 1,
                                 cut=6.0)

            tcolor = GOLD_BRIGHT if is_active else (CYAN_BRIGHT if is_hov else GREY)
            arcade.draw_text(tname, tx + tab_w / 2, 519, tcolor,
                             font_size=9, bold=is_active, anchor_x="center", anchor_y="center",
                             font_name=FONT_INTERFACE)

        # ── Active Tab Panel Container (x=240 to 880, y=55 to 490) ───────────
        draw_chamfered_panel(240, 880, 55, 490, GOLD, fill=SURFACE_LOW, alpha=240, cut=10.0)
        draw_corner_etching(240, 880, 55, 490, GOLD, length=14.0, alpha=110)

        # Render Active Tab Content
        if self._active_tab == 0:
            self._draw_audio_tab()
        elif self._active_tab == 1:
            self._draw_display_tab()
        elif self._active_tab == 2:
            self._draw_accessibility_tab()
        elif self._active_tab == 3:
            self._draw_controls_tab()

        # Bottom save & return hint
        arcade.draw_text("TAB / 1-4: SWITCH SECTIONS   •   CLICK: ADJUST SETTINGS   •   ESC: SAVE & EXIT",
                         560, 24, MUTED, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Draw Nav Rail
        self.nav_rail.draw()

        # Transition
        TransitionOverlay.draw()

    def _draw_audio_tab(self) -> None:
        arcade.draw_text("AUDIO MIXER CALIBRATION", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Adjust master volume levels and sound balance", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # SFX Slider
        self._draw_slider(270, 360, 520, "SOUND EFFECTS (SFX)", self.sfx_volume, "sfx")

        # Music Slider
        self._draw_slider(270, 280, 520, "CELESTIAL MUSIC", self.music_volume, "music")

        # Volume guide text
        arcade.draw_text("Sound telemetry adjustments apply dynamically in real time.",
                         270, 180, GREY, font_size=9, font_name=FONT_INTERFACE)

    def _draw_display_tab(self) -> None:
        arcade.draw_text("DISPLAY & GRAPHICS CALIBRATION", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Configure viewport presentation and particle rendering", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # Fullscreen Toggle
        self._draw_toggle(270, 360, "DISPLAY MODE", "Fullscreen (Aspect-Preserving)",
                          "Windowed (900x600)", self.fullscreen)

        # Particle Quality
        self._draw_segmented_selector(270, 280, "PARTICLE QUALITY", ["HIGH", "LOW"],
                                      0 if self.particles == "high" else 1)

        # Screen Shake
        curr_shake_idx = _SHAKE_OPTIONS.index(self.screen_shake) if self.screen_shake in _SHAKE_OPTIONS else 0
        self._draw_segmented_selector(270, 200, "SCREEN SHAKE IMPULSE", ["FULL", "LOW", "OFF"],
                                      curr_shake_idx)

    def _draw_accessibility_tab(self) -> None:
        arcade.draw_text("ACCESSIBILITY & COMFORT", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Visual comfort filters and photosensitivity toggles", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # Reduced Flashes Toggle
        self._draw_diamond_toggle(270, 360, "REDUCED FLASHES",
                                  "Suppresses bright screen flashes, shield strobes, and intense weapon blooms",
                                  self.reduced_flashes)

        # Colorblind Filter
        curr_cb_idx = _COLORBLIND_OPTIONS.index(self.colorblind_mode) if self.colorblind_mode in _COLORBLIND_OPTIONS else 0
        self._draw_segmented_selector(270, 260, "COLORBLIND CORRECTION",
                                      ["OFF", "PROTAN", "DEUTAN", "TRITAN"], curr_cb_idx)

        # UI Scale indicator
        arcade.draw_text("LOGICAL RESOLUTION SCALE", 270, 160, STARLIGHT,
                         font_size=10, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("900x600 Canonical (Automatically aspect-scaled with zero letterbox distortion)",
                         270, 142, CYAN_BRIGHT, font_size=9, font_name=FONT_TELEMETRY)

    def _draw_controls_tab(self) -> None:
        arcade.draw_text("KEYBOARD & MOUSE CALIBRATION", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Vimana cockpit tactical control scheme", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # Keybindings 2-column grid
        start_y = 390
        row_h = 32
        for i, (action, bind_key, category) in enumerate(_KEYBINDINGS):
            col_x = 270 if i < 5 else 570
            row_y = start_y - (i % 5) * row_h

            arcade.draw_text(action, col_x, row_y, STARLIGHT,
                             font_size=9, bold=True, anchor_y="center", font_name=FONT_INTERFACE)

            # Keybind badge
            draw_state_badge(col_x + 200, row_y, bind_key, GOLD if "Combat" in category else CYAN, width=130)

    def _draw_slider(self, x: float, y: float, width: float, label: str, value: int, key: str) -> None:
        arcade.draw_text(label, x, y + 22, STARLIGHT, font_size=10, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(f"{value}%", x + width, y + 22, GOLD_BRIGHT, font_size=10, bold=True,
                         anchor_x="right", font_name=FONT_TELEMETRY)

        # Track well
        track_h = 6.0
        arcade.draw_lrbt_rectangle_filled(x, x + width, y - track_h / 2, y + track_h / 2, (*WELL, 240))
        arcade.draw_line(x, y, x + width, y, (*GREY, 70), 1)

        # Filled track
        frac = max(0.0, min(1.0, value / 100.0))
        fill_w = width * frac
        arcade.draw_lrbt_rectangle_filled(x, x + fill_w, y - track_h / 2, y + track_h / 2, (*GOLD, 230))

        # Diamond thumb (14x14 rotated square)
        tx = x + fill_w
        diamond = [(tx, y + 8.5), (tx + 8.5, y), (tx, y - 8.5), (tx - 8.5, y)]
        arcade.draw_polygon_filled(diamond, GOLD_BRIGHT)
        arcade.draw_polygon_outline(diamond, OBSIDIAN, 1.5)

    def _draw_toggle(self, x: float, y: float, label: str, on_text: str, off_text: str, state: bool) -> None:
        arcade.draw_text(label, x, y + 20, STARLIGHT, font_size=10, bold=True, font_name=FONT_INTERFACE)

        # Switch box
        sw_w = 260.0
        sw_h = 32.0
        draw_chamfered_panel(x, x + sw_w, y - sw_h / 2, y + sw_h / 2, GOLD if state else GREY,
                             fill=WELL, alpha=230, cut=6.0)

        tlabel = on_text if state else off_text
        arcade.draw_text(tlabel, x + sw_w / 2, y, GOLD_BRIGHT if state else GREY,
                         font_size=9, bold=True, anchor_x="center", anchor_y="center",
                         font_name=FONT_INTERFACE)

    def _draw_diamond_toggle(self, x: float, y: float, label: str, desc: str, state: bool) -> None:
        # 16x16 rotated square diamond toggle per Section 7.11
        cx, cy = x + 12, y + 6
        diamond = [(cx, cy + 11.5), (cx + 11.5, cy), (cx, cy - 11.5), (cx - 11.5, cy)]
        arcade.draw_polygon_filled(diamond, GOLD if state else WELL)
        arcade.draw_polygon_outline(diamond, BRASS, 1.5)
        if state:
            arcade.draw_text("✓", x + 12, y + 6, OBSIDIAN, font_size=10, bold=True,
                             anchor_x="center", anchor_y="center")

        arcade.draw_text(label, x + 36, y + 14, GOLD_BRIGHT if state else STARLIGHT,
                         font_size=10, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(desc, x + 36, y - 2, PARCHMENT, font_size=8, font_name=FONT_INTERFACE)

    def _draw_segmented_selector(self, x: float, y: float, label: str, options: list[str], selected_idx: int) -> None:
        arcade.draw_text(label, x, y + 22, STARLIGHT, font_size=10, bold=True, font_name=FONT_INTERFACE)

        btn_w = 90.0
        btn_h = 28.0
        for i, opt in enumerate(options):
            bx = x + i * (btn_w + 8)
            is_sel = (i == selected_idx)
            draw_chamfered_panel(bx, bx + btn_w, y - btn_h / 2, y + btn_h / 2,
                                 GOLD if is_sel else GREY,
                                 fill=SURFACE_HIGH if is_sel else WELL,
                                 alpha=230, cut=5.0)
            if is_sel:
                # Cyan underline indicator
                arcade.draw_line(bx + 6, y - btn_h / 2 + 2, bx + btn_w - 6, y - btn_h / 2 + 2, CYAN_BRIGHT, 2)

            arcade.draw_text(opt, bx + btn_w / 2, y, GOLD_BRIGHT if is_sel else GREY,
                             font_size=8, bold=True, anchor_x="center", anchor_y="center",
                             font_name=FONT_TELEMETRY)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)

        # Tab hover
        self._hovered_tab = -1
        tab_w = 145.0
        for i in range(len(_TABS)):
            tx = 240.0 + i * (tab_w + 10)
            if tx <= x <= tx + tab_w and 502 <= y <= 536:
                self._hovered_tab = i
                break

        # Slider drag
        if self._dragging_slider:
            slider_x = 270.0
            slider_w = 520.0
            new_val = int(max(0, min(100, (x - slider_x) / slider_w * 100)))
            if self._dragging_slider == "sfx":
                self.sfx_volume = new_val
            elif self._dragging_slider == "music":
                self.music_volume = new_val
            self._save_and_apply()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            self._save_and_apply()
            return

        # Check tab clicks
        tab_w = 145.0
        for i in range(len(_TABS)):
            tx = 240.0 + i * (tab_w + 10)
            if tx <= x <= tx + tab_w and 502 <= y <= 536:
                self._active_tab = i
                self.sound_manager.play_ui_click(volume=0.25)
                return

        # Handle tab-specific clicks
        if self._active_tab == 0:
            # SFX slider (y=360)
            if 270 <= x <= 790 and 345 <= y <= 375:
                self._dragging_slider = "sfx"
                self.sfx_volume = int((x - 270) / 520 * 100)
                self._save_and_apply()
            # Music slider (y=280)
            elif 270 <= x <= 790 and 265 <= y <= 295:
                self._dragging_slider = "music"
                self.music_volume = int((x - 270) / 520 * 100)
                self._save_and_apply()

        elif self._active_tab == 1:
            # Fullscreen toggle (y=360)
            if 270 <= x <= 530 and 340 <= y <= 380:
                self.fullscreen = not self.fullscreen
                self.sound_manager.play_ui_click(volume=0.25)
                self._save_and_apply()
            # Particle selector (y=280)
            elif 240 <= y <= 300:
                for i in range(len(_PARTICLE_OPTIONS)):
                    bx = 270 + i * 98
                    if bx <= x <= bx + 90:
                        self.particles = _PARTICLE_OPTIONS[i]
                        self.sound_manager.play_ui_click(volume=0.25)
                        self._save_and_apply()
            # Screen shake (y=200)
            elif 180 <= y <= 220:
                for i in range(len(_SHAKE_OPTIONS)):
                    bx = 270 + i * 98
                    if bx <= x <= bx + 90:
                        self.screen_shake = _SHAKE_OPTIONS[i]
                        self.sound_manager.play_ui_click(volume=0.25)
                        self._save_and_apply()

        elif self._active_tab == 2:
            # Reduced flashes diamond toggle (y=360)
            if 270 <= x <= 800 and 340 <= y <= 385:
                self.reduced_flashes = not self.reduced_flashes
                self.sound_manager.play_ui_click(volume=0.25)
                self._save_and_apply()
            # Colorblind selector (y=260)
            elif 240 <= y <= 280:
                for i in range(len(_COLORBLIND_OPTIONS)):
                    bx = 270 + i * 98
                    if bx <= x <= bx + 90:
                        self.colorblind_mode = _COLORBLIND_OPTIONS[i]
                        self.sound_manager.play_ui_click(volume=0.25)
                        self._save_and_apply()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        self._dragging_slider = None

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.TAB:
            self._active_tab = (self._active_tab + 1) % len(_TABS)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.KEY_1, arcade.key.NUM_1):
            self._active_tab = 0
        elif key in (arcade.key.KEY_2, arcade.key.NUM_2):
            self._active_tab = 1
        elif key in (arcade.key.KEY_3, arcade.key.NUM_3):
            self._active_tab = 2
        elif key in (arcade.key.KEY_4, arcade.key.NUM_4):
            self._active_tab = 3
        elif key == arcade.key.ESCAPE:
            self._save_and_apply()
            if self.return_view:
                self.window.show_view(self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())
