"""
game/views/ship_select_view.py
Fleet Hangar & Astra Armory Selection Screen.
Follows Section 7.5 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, 3 paginated cards per page with counter-rotating halos,
5 real telemetry stats, lock silhouettes, detailed pilot dossier, and celestial deploy action.
"""
import math
import arcade

from constants import WIDTH, HEIGHT
from game.entities.ship_classes import SHIP_CLASSES
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.ui.nav_rail import NavRail
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, BRASS, PARCHMENT,
    STARLIGHT, GREY, MUTED, WELL,
    FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_segmented_bar,
    draw_scanlines, pulse_alpha, draw_state_badge,
)


_SHIPS = list(SHIP_CLASSES.keys())
_PAGE_SIZE = 3

def _draw_ship_silhouette(cx, cy, ship_id, color, size=32):
    if ship_id == "pushpaka":
        points = ((cx-size*0.8, cy-size*0.6), (cx+size*0.8, cy-size*0.6), (cx+size*0.5, cy+size*0.6), (cx-size*0.5, cy+size*0.6))
    elif ship_id == "tripura":
        points = ((cx-size*0.6, cy-size*0.8), (cx+size*0.6, cy-size*0.8), (cx, cy+size*0.8))
    elif ship_id == "garuda":
        points = ((cx, cy+size*0.8), (cx+size*0.8, cy-size*0.4), (cx+size*0.2, cy-size*0.2), (cx, cy-size*0.8), (cx-size*0.2, cy-size*0.2), (cx-size*0.8, cy-size*0.4))
    elif ship_id == "vajra":
        points = ((cx, cy+size*0.8), (cx+size*0.3, cy), (cx, cy-size*0.8), (cx-size*0.3, cy))
    elif ship_id == "naga":
        points = ((cx-size*0.4, cy-size*0.6), (cx+size*0.6, cy-size*0.2), (cx-size*0.6, cy+size*0.2), (cx+size*0.4, cy+size*0.6))
    elif ship_id == "agneyastra":
        arcade.draw_circle_filled(cx, cy, size*0.4, color)
        points = ((cx-size*0.8, cy), (cx, cy+size*0.8), (cx+size*0.8, cy), (cx, cy-size*0.8))
    elif ship_id == "soma":
        arcade.draw_circle_filled(cx, cy, size*0.6, color)
        arcade.draw_circle_filled(cx+size*0.2, cy+size*0.2, size*0.6, OBSIDIAN)
        points = ()
    elif ship_id == "kubera":
        points = ((cx-size*0.6, cy-size*0.5), (cx+size*0.6, cy-size*0.5), (cx+size*0.6, cy+size*0.5), (cx-size*0.6, cy+size*0.5))
    elif ship_id == "surya":
        arcade.draw_circle_filled(cx, cy, size*0.5, color)
        points = ((cx-size*0.9, cy-size*0.2), (cx-size*0.9, cy+size*0.2), (cx+size*0.9, cy+size*0.2), (cx+size*0.9, cy-size*0.2))
    else:
        points = ((cx, cy+size), (cx+size, cy), (cx, cy-size), (cx-size, cy))
    
    if points:
        arcade.draw_polygon_filled(points, color)


class ShipSelectView(arcade.View):
    def __init__(self, difficulty: str = "normal", start_wave: int = 1,
                 realm_id: int | None = None):
        super().__init__()
        self.difficulty = difficulty
        self.start_wave = max(1, int(start_wave))
        self.realm_id = realm_id

        self.sound_manager = SoundManager()
        self.nav_rail = NavRail("hangar")

        saved = save_system.load()
        self._last_ship = saved.get("last_ship", "pushpaka")
        self._last_wave = max(0, int(saved.get("last_wave", 0)))
        self._reduced_flashes = bool(saved.get("reduced_flashes", False))

        self._selected = _SHIPS.index(self._last_ship) if self._last_ship in _SHIPS else 0
        self._hovered = -1
        self._pulse = 0.0
        self._newly_unlocked: set = set()

        # Primary deploy button
        self._btn_deploy = MenuButton(
            "COMMENCE SORTIE  ▶", 755, 96,
            width=210, height=40, accent=GOLD, variant="celestial"
        )
        self._hovered_deploy = False

    def _is_unlocked(self, ship_id: str) -> bool:
        from game.systems.save_system import get_unlocked_ships
        return ship_id in get_unlocked_ships()

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()
        saved = save_system.load()
        self._last_wave = max(0, int(saved.get("last_wave", 0)))

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)
        self._btn_deploy.update(delta_time, self._hovered_deploy)

    def on_draw(self) -> None:
        self.clear()

        # Background scanlines
        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        arcade.draw_text("FLEET HANGAR // VIMANA SPECIFICATION", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        page_num = (self._selected // _PAGE_SIZE) + 1
        total_pages = (len(_SHIPS) + _PAGE_SIZE - 1) // _PAGE_SIZE
        arcade.draw_text(f"ARMORY SQUADRON  •  PAGE {page_num}/{total_pages}  •  SORTIE WAVE {self.start_wave:02d}",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Page indicator chips
        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        visible_ships = _SHIPS[page_start:page_start + _PAGE_SIZE]

        # ── Three Paginated Ship Cards (y=190 to 535) ────────────────────────
        card_w = 200.0
        card_h = 325.0
        spacing = 215.0
        start_x = 240.0 + card_w / 2

        for local_i, ship_id in enumerate(visible_ships):
            idx = page_start + local_i
            sdata = SHIP_CLASSES[ship_id]
            unlocked = self._is_unlocked(ship_id)
            selected = (idx == self._selected)
            hovered = (local_i == self._hovered)

            cx = start_x + local_i * spacing
            cy = 365.0

            left = cx - card_w / 2
            right = cx + card_w / 2
            bottom = cy - card_h / 2
            top = cy + card_h / 2

            # Card Container — selected > hovered > default
            if selected:
                accent_col = GOLD
            elif hovered and unlocked:
                accent_col = CYAN_BRIGHT   # distinct hover: brighter than unselected
            elif hovered:
                accent_col = BRASS         # hover on locked card
            elif unlocked:
                accent_col = CYAN
            else:
                accent_col = BRASS
            fill_col = SURFACE_HIGH if (selected or hovered) else SURFACE_LOW
            draw_chamfered_panel(left, right, bottom, top, accent_col,
                                 fill=fill_col, alpha=235, border_width=2 if selected else (2 if hovered else 1),
                                 selected=selected, cut=10.0)
            if selected:
                draw_corner_etching(left, right, bottom, top, GOLD, length=12.0, alpha=130)

            # Hologram Viewport with counter-rotating halos
            holo_cy = top - 80.0
            arcade.draw_circle_filled(cx, holo_cy, 48.0, (*WELL, 200))
            if selected and not self._reduced_flashes:
                halo_a = pulse_alpha(self._pulse, 30, 90, 2.0)
                arcade.draw_arc_outline(cx, holo_cy, 100, 100, (*CYAN, halo_a),
                                        self._pulse * 18.0, self._pulse * 18.0 + 240, 1.5)
                arcade.draw_arc_outline(cx, holo_cy, 114, 114, (*GOLD, halo_a // 2),
                                        -self._pulse * 14.0, -self._pulse * 14.0 + 200, 1.0)

            # Ship sprite replaced by silhouette
            drift = 0.0 if self._reduced_flashes or not selected else math.sin(self._pulse * 1.5) * 3.0
            if unlocked:
                _draw_ship_silhouette(cx, holo_cy + drift, ship_id, accent_col, size=32)
            else:
                _draw_ship_silhouette(cx, holo_cy, ship_id, (80, 85, 95, 65), size=32)
                draw_state_badge(cx, holo_cy, f"WAVE {sdata.get('unlock_wave', 0):02d}", BRASS, width=78)

            # Card Header Text
            arcade.draw_text(sdata["name"].upper(), cx, top - 142,
                             GOLD_BRIGHT if selected else (STARLIGHT if unlocked else GREY),
                             font_size=11, bold=True, anchor_x="center", font_name=FONT_INTERFACE)
            arcade.draw_text(sdata.get("subtitle", "").upper(), cx, top - 156,
                             CYAN if unlocked else (*GREY, 120),
                             font_size=7, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

            arcade.draw_line(left + 16, top - 168, right - 16, top - 168, (*accent_col, 45), 1)

            # 5 Canonical Telemetry Bars
            bar_labels = [
                ("HULL", sdata["hp"] / 190.0, sdata["hp"]),
                ("FIREPOWER", sdata["bullet_damage"] / 65.0, sdata["bullet_damage"]),
                ("SPEED", sdata["speed"] / 7.2, round(sdata["speed"], 1)),
                ("DASH", 1.0 - (sdata["dash_cooldown"] - 1.2) / 2.2, round(sdata["dash_cooldown"], 1)),
                ("ASTRA", sdata.get("astra_power", 75) / 100.0, sdata.get("astra_power", 75)),
            ]

            by = top - 188
            for blabel, bfrac, bval in bar_labels:
                arcade.draw_text(blabel, left + 16, by + 2, (*GREY, 200),
                                 font_size=7, bold=True, font_name=FONT_TELEMETRY)
                draw_segmented_bar(left + 76, right - 28, by, by + 12,
                                   bfrac, color=GOLD if selected else CYAN, segments=8, gap=2.0)
                arcade.draw_text(f"{bval}", right - 10, by + 2, (*GREY, 200),
                                 font_size=6, bold=True, anchor_x="right", font_name=FONT_TELEMETRY)
                by -= 24

            if not unlocked:
                # Lock indicator banner at bottom of card
                arcade.draw_text(f"UNLOCK AT WAVE {sdata.get('unlock_wave', 0):02d}",
                                 cx, bottom + 26, BRASS,
                                 font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)
                unlock_w = sdata.get("unlock_wave", 0)
                last_w = self._last_wave
                progress = min(1.0, last_w / max(1, unlock_w))
                arcade.draw_lrbt_rectangle_filled(cx - 50, cx + 50, bottom + 12, bottom + 16, SURFACE_HIGH)
                arcade.draw_lrbt_rectangle_filled(cx - 50, cx - 50 + 100 * progress, bottom + 12, bottom + 16, BRASS)
                arcade.draw_text(f"WAVE {last_w}/{unlock_w}", cx, bottom + 2, BRASS,
                                 font_size=6, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)
            elif selected:
                arcade.draw_text("SELECTED VESSEL", cx, bottom + 16, GOLD,
                                 font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Page indicator dots
        total_pages = (len(_SHIPS) + _PAGE_SIZE - 1) // _PAGE_SIZE
        current_page = self._selected // _PAGE_SIZE
        dot_spacing = 20
        dots_width = (total_pages - 1) * dot_spacing
        dot_start_x = 560 - dots_width / 2
        for p in range(total_pages):
            dot_x = dot_start_x + p * dot_spacing
            if p == current_page:
                arcade.draw_text("●", dot_x, 195, GOLD, font_size=12, anchor_x="center", anchor_y="center")
            else:
                arcade.draw_text("○", dot_x, 195, MUTED, font_size=12, anchor_x="center", anchor_y="center")

        # ── Lower Focused Ship Dossier (x=240 to 880, y=42 to 180) ───────────
        draw_chamfered_panel(240, 880, 42, 180, GOLD, fill=SURFACE_LOW, alpha=235, cut=10.0)
        draw_corner_etching(240, 880, 42, 180, GOLD, length=12.0, alpha=100)

        sel_ship = SHIP_CLASSES[_SHIPS[self._selected]]
        sel_unlocked = self._is_unlocked(_SHIPS[self._selected])

        # Header with weapon & ability loadout
        arcade.draw_text(sel_ship["name"].upper(), 256, 156, GOLD_BRIGHT,
                         font_size=14, bold=True, font_name=FONT_INTERFACE)
        draw_state_badge(450, 156, sel_ship.get("subtitle", "VESSEL").upper(), CYAN, width=120)

        arcade.draw_text(f"PRIMARY WEAPON: {sel_ship.get('weapon', 'Brahmastra Cannon')}",
                         600, 156, STARLIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_text(f"DIVINE ABILITY: {sel_ship.get('ability', 'Divine Barrier')}",
                         600, 142, CYAN_BRIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        arcade.draw_line(256, 134, 864, 134, (*GOLD, 40), 1)

        # Lore narrative body
        lore = sel_ship.get("desc", "Celestial craft forged for cosmic warfare.")
        arcade.draw_text(lore, 256, 114, PARCHMENT, font_size=9, font_name=FONT_INTERFACE)

        # Deploy Sortie or Unlock Banner
        if sel_unlocked:
            self._btn_deploy.draw()
        else:
            arcade.draw_text(f"HULL SECURED // SURVIVE TO WAVE {sel_ship.get('unlock_wave', 0):02d} TO COMMISSION",
                             755, 96, BRASS, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Pagination & Controls Hint
        arcade.draw_text(
            "← → / A D: PREV/NEXT VESSEL   •   Q / E: FLIP PAGE   •   ENTER: COMMENCE SORTIE   •   ESC: BACK",
            560, 22, MUTED, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY
        )

        # Draw Nav Rail
        self.nav_rail.draw()

        # Transition
        TransitionOverlay.draw()

    def _deploy_focused_ship(self) -> None:
        ship_id = _SHIPS[self._selected]
        if not self._is_unlocked(ship_id) or TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        # Save selected ship
        saved = save_system.load()
        saved["last_ship"] = ship_id
        save_system.save(saved)

        # Launch directly into GameView or DifficultyView
        from game.views.game_view import GameView
        game_view = GameView(difficulty=self.difficulty, start_wave=self.start_wave,
                             ship_class=ship_id, realm_id=self.realm_id)
        self.window.show_view(game_view)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)
        self._hovered_deploy = self._btn_deploy.contains(x, y)

        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        self._hovered = -1
        card_w, card_h = 200.0, 325.0
        start_x, spacing = 240.0 + card_w / 2, 215.0

        for local_i in range(min(_PAGE_SIZE, len(_SHIPS) - page_start)):
            cx = start_x + local_i * spacing
            cy = 365.0
            if cx - card_w / 2 <= x <= cx + card_w / 2 and cy - card_h / 2 <= y <= cy + card_h / 2:
                self._hovered = local_i
                break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            return

        if self._btn_deploy.contains(x, y):
            self._deploy_focused_ship()
            return

        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        card_w, card_h = 200.0, 325.0
        start_x, spacing = 240.0 + card_w / 2, 215.0

        for local_i in range(min(_PAGE_SIZE, len(_SHIPS) - page_start)):
            cx = start_x + local_i * spacing
            cy = 365.0
            if cx - card_w / 2 <= x <= cx + card_w / 2 and cy - card_h / 2 <= y <= cy + card_h / 2:
                self._selected = page_start + local_i
                self.sound_manager.play_ui_click(volume=0.25)
                return

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            self._selected = (self._selected - 1) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._selected = (self._selected + 1) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.Q, arcade.key.PAGEUP):
            self._selected = (self._selected - _PAGE_SIZE) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.E, arcade.key.PAGEDOWN):
            self._selected = (self._selected + _PAGE_SIZE) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._deploy_focused_ship()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())
