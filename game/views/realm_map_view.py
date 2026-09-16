"""
game/views/realm_map_view.py
Celestial Campaign Sector Map.
Follows Section 7.3 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, 7-node curved trajectory, state badges
(Cleared gold tick, Available cyan pulse, Locked brass lock), boss chevrons,
and direct briefing/sortie launch.
"""
import math
import random
import arcade

from constants import WIDTH, HEIGHT, REALMS
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.ui.nav_rail import NavRail
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    VOID, OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, BRASS, ASTRA_RED, ASTRA_RED_BRIGHT, PARCHMENT,
    STARLIGHT, GREY, MUTED, WELL,
    FONT_CEREMONIAL, FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
    pulse_alpha, draw_state_badge,
)


REALM_ORDER = (1, 2, 3, 4, 5, 6, 7)
REALM_START_WAVES = {1: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19}
BOSS_REALMS = {2: "Kumbhakarna", 4: "Ravana", 7: "Vritra"}

# Curved trajectory coordinates across x=240 to 880 space
_NODE_POS = {
    1: (280, 360),
    2: (375, 430),
    3: (470, 340),
    4: (570, 440),
    5: (670, 350),
    6: (765, 430),
    7: (845, 330),
}


def realm_is_unlocked(realm_id: int, last_wave: int) -> bool:
    return realm_id == 1 or last_wave >= REALM_START_WAVES[realm_id]


class RealmMapView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        self._hovered = -1
        self._selected = 1
        self.sound_manager = SoundManager()
        self.nav_rail = NavRail("campaign")

        saved = save_system.load()
        self._reduced_flashes = bool(saved.get("reduced_flashes", False))
        self.last_wave = max(0, int(saved.get("last_wave", 0)))
        self._unlocked = [
            r for r in REALM_ORDER
            if realm_is_unlocked(r, self.last_wave)
        ]
        last_realm = int(saved.get("last_realm", 1))
        if last_realm in self._unlocked:
            self._selected = last_realm
        else:
            self._selected = self._unlocked[-1] if self._unlocked else 1

        self._stars = [
            (random.randrange(220, WIDTH), random.randrange(HEIGHT), random.uniform(0.6, 1.8))
            for _ in range(70)
        ]

        self._btn_enter = MenuButton(
            "ENTER SORTIE  ▶", 755, 110,
            width=210, height=42, accent=GOLD, variant="celestial"
        )
        self._hovered_enter = False

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()
        saved = save_system.load()
        self.last_wave = max(0, int(saved.get("last_wave", 0)))
        self._unlocked = [
            r for r in REALM_ORDER
            if realm_is_unlocked(r, self.last_wave)
        ]

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)
        self._btn_enter.update(delta_time, self._hovered_enter)

    def on_draw(self) -> None:
        self.clear()

        # Starfield
        for sx, sy, radius in self._stars:
            drift_x = 220 + ((sx - 220 + self._pulse * 4.0) % (WIDTH - 220))
            twinkle = int(120 + 40 * math.sin(self._pulse * 1.5 + sx * 0.02))
            arcade.draw_circle_filled(drift_x, sy, radius, (twinkle, twinkle, min(255, twinkle + 20)))

        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        arcade.draw_text("CELESTIAL CAMPAIGN MAP // REALM TRAJECTORY", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        cleared_count = max(0, len(self._unlocked) - 1)
        arcade.draw_text(f"CAMPAIGN STATUS: {cleared_count}/7 REALMS LIBERATED // MAX REACHED: WAVE {self.last_wave:02d}",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # ── Connective Trajectory Lines ──────────────────────────────────────
        for left_id, right_id in zip(REALM_ORDER, REALM_ORDER[1:]):
            lx, ly = _NODE_POS[left_id]
            rx, ry = _NODE_POS[right_id]
            left_unlocked = left_id in self._unlocked
            right_unlocked = right_id in self._unlocked

            if left_unlocked and right_unlocked:
                # Active liberated/current path
                arcade.draw_line(lx, ly, rx, ry, (*GOLD, 180), 3)
                arcade.draw_line(lx, ly, rx, ry, (*GOLD_BRIGHT, 90), 1)
            elif left_unlocked and not right_unlocked:
                # Warp conduit to next unlock
                pulse_a = pulse_alpha(self._pulse, 60, 200, 3.0, self._reduced_flashes)
                arcade.draw_line(lx, ly, rx, ry, (*CYAN, pulse_a), 2)
            else:
                # Locked segment
                arcade.draw_line(lx, ly, rx, ry, (*BRASS, 60), 1)

        # ── Realm Nodes ──────────────────────────────────────────────────────
        for realm_id in REALM_ORDER:
            x, y = _NODE_POS[realm_id]
            unlocked = realm_id in self._unlocked
            selected = (realm_id == self._selected)
            hovered = (realm_id == self._hovered)

            node_radius = 24.0 if not selected else 28.0

            # Background well
            arcade.draw_circle_filled(x, y, node_radius, (*WELL, 240))

            if unlocked:
                # Check if cleared (not the latest unlocked unless all 7 done)
                is_cleared = (realm_id < len(self._unlocked))
                if is_cleared:
                    arcade.draw_circle_filled(x, y, node_radius, (*GOLD, 45))
                    arcade.draw_circle_outline(x, y, node_radius, GOLD, 2)
                    arcade.draw_text("✓", x, y, GOLD_BRIGHT, font_size=16, bold=True,
                                     anchor_x="center", anchor_y="center")
                else:
                    # Current available realm
                    pulse_ring = pulse_alpha(self._pulse, 120, 255, 2.5, self._reduced_flashes)
                    arcade.draw_circle_outline(x, y, node_radius + 4, (*CYAN_BRIGHT, pulse_ring), 2)
                    arcade.draw_circle_outline(x, y, node_radius, CYAN, 2)
                    arcade.draw_text("◈", x, y, CYAN_BRIGHT, font_size=16, bold=True,
                                     anchor_x="center", anchor_y="center")
            else:
                # Locked node
                arcade.draw_circle_outline(x, y, node_radius, (*BRASS, 140), 1)
                arcade.draw_text("⊘", x, y, GREY, font_size=14, bold=True,
                                 anchor_x="center", anchor_y="center")

            # Boss chevron indicator
            if realm_id in BOSS_REALMS:
                arcade.draw_text("▲", x, y + node_radius + 6, ASTRA_RED, font_size=10, bold=True,
                                 anchor_x="center", anchor_y="center")

            # Node label underneath
            realm_info = REALMS.get(realm_id, {})
            name_col = GOLD_BRIGHT if selected else (STARLIGHT if unlocked else GREY)
            arcade.draw_text(realm_info.get("name", "").upper(), x, y - node_radius - 14,
                             name_col, font_size=8, bold=True, anchor_x="center",
                             font_name=FONT_INTERFACE)
            waves_info = f"W{realm_info.get('waves', [1])[0]}–{realm_info.get('waves', [1])[-1]}"
            arcade.draw_text(waves_info, x, y - node_radius - 26,
                             CYAN if unlocked else (*GREY, 120), font_size=7, bold=True,
                             anchor_x="center", font_name=FONT_TELEMETRY)

        # ── Lower Sector Dossier Panel (x=240 to 880, y=48 to 220) ───────────
        draw_chamfered_panel(240, 880, 48, 220, GOLD if self._selected in self._unlocked else BRASS,
                             fill=SURFACE_LOW, alpha=235, cut=10.0)
        draw_corner_etching(240, 880, 48, 220, GOLD, length=12.0, alpha=110)

        sel_info = REALMS.get(self._selected, {})
        sel_unlocked = self._selected in self._unlocked
        waves_span = f"WAVES {sel_info.get('waves', [1])[0]:02d}–{sel_info.get('waves', [1])[-1]:02d}"

        # Status badge
        status_text = "CLEARED" if (self._selected < len(self._unlocked)) else ("CURRENT ACTIVE" if sel_unlocked else "LOCKED SECTOR")
        status_col = GOLD if status_text == "CLEARED" else (CYAN if sel_unlocked else GREY)
        draw_state_badge(310, 196, status_text, status_col, width=100)

        # Title & waves
        arcade.draw_text(sel_info.get("name", "").upper(), 375, 196, GOLD_BRIGHT,
                         font_size=16, bold=True, anchor_y="center", font_name=FONT_INTERFACE)
        arcade.draw_text(waves_span, 590, 196, CYAN_BRIGHT,
                         font_size=10, bold=True, anchor_y="center", font_name=FONT_TELEMETRY)

        arcade.draw_line(256, 178, 864, 178, (*GOLD, 50), 1)

        # Realm Lore Description
        lore = sel_info.get("desc", "Celestial battle theater facing Asura vanguard.")
        arcade.draw_text(lore, 260, 148, PARCHMENT, font_size=9, font_name=FONT_INTERFACE)

        # Boss threat summary
        if self._selected in BOSS_REALMS:
            boss_name = BOSS_REALMS[self._selected]
            arcade.draw_text(f"THREAT INTELLIGENCE: BOSS OVERLORD {boss_name.upper()}",
                             260, 110, ASTRA_RED_BRIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)
        else:
            arcade.draw_text("THREAT INTELLIGENCE: ASURA FRONTLINE SQUADRONS",
                             260, 110, (*GREY, 180), font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Unlock condition or Sortie button
        if sel_unlocked:
            self._btn_enter.draw()
        else:
            req_wave = REALM_START_WAVES.get(self._selected, 1)
            arcade.draw_text(f"LOCKED // CLEAR WAVE {req_wave - 1:02d} IN CAMPAIGN TO ACCESS",
                             755, 110, GREY, font_size=9, bold=True,
                             anchor_x="center", anchor_y="center", font_name=FONT_TELEMETRY)

        # Keyboard & Navigation Hints
        arcade.draw_text("← → / A D: SELECT REALM   •   ENTER: COMMENCE SORTIE   •   ESC: BACK",
                         560, 24, MUTED, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Draw Nav Rail
        self.nav_rail.draw()

        # Transition
        TransitionOverlay.draw()

    def _enter_selected_realm(self) -> None:
        if self._selected not in self._unlocked or TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        # Save selected starting realm
        saved = save_system.load()
        saved["last_realm"] = self._selected
        save_system.save(saved)

        start_wave = REALM_START_WAVES.get(self._selected, 1)

        # Open story briefing if needed, else difficulty view
        from game.views.story_briefing_view import StoryBriefingView
        briefing = StoryBriefingView(realm_id=self._selected, start_wave=start_wave)
        transition_to(self.window, briefing)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)
        self._hovered_enter = self._btn_enter.contains(x, y)

        self._hovered = -1
        for realm_id, (nx, ny) in _NODE_POS.items():
            if (x - nx) ** 2 + (y - ny) ** 2 <= 28 ** 2:
                self._hovered = realm_id
                break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            return

        if self._btn_enter.contains(x, y):
            self._enter_selected_realm()
            return

        for realm_id, (nx, ny) in _NODE_POS.items():
            if (x - nx) ** 2 + (y - ny) ** 2 <= 30 ** 2:
                self._selected = realm_id
                self.sound_manager.play_ui_click(volume=0.25)
                return

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            curr_idx = REALM_ORDER.index(self._selected)
            self._selected = REALM_ORDER[(curr_idx - 1) % len(REALM_ORDER)]
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            curr_idx = REALM_ORDER.index(self._selected)
            self._selected = REALM_ORDER[(curr_idx + 1) % len(REALM_ORDER)]
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._enter_selected_realm()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())
