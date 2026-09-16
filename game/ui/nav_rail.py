"""
game/ui/nav_rail.py
Standardized 220px left navigation rail for front-end console views.
Follows the canonical Section 5 and Section 7.1 specification.
"""
import arcade
from constants import WIDTH, HEIGHT
from game.ui.vedic_theme import (
    VOID, OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, GREY, MUTED, FONT_INTERFACE, FONT_TELEMETRY,
    draw_scanlines,
)
from game.ui.transitions import transition_to


NAV_ITEMS = [
    ("COMMAND DECK", "menu", "01"),
    ("CAMPAIGN MAP", "campaign", "02"),
    ("FLEET HANGAR", "hangar", "03"),
    ("DHARMIC CODEX", "codex", "04"),
    ("SANGHA NETWORK", "sangha", "05"),
    ("ACCOUNT INTEL", "account", "06"),
    ("CONSOLE SETTINGS", "settings", "07"),
]

RAIL_WIDTH = 220.0
ITEM_HEIGHT = 44.0
START_Y = 460.0


class NavRail:
    """Standardized 220px left navigation rail across front-end views."""

    def __init__(self, current_screen: str):
        self.current_screen = current_screen
        self.hovered_index = -1
        self._pulse = 0.0

    def update(self, delta_time: float) -> None:
        self._pulse += delta_time

    def on_mouse_motion(self, x: float, y: float) -> None:
        self.hovered_index = -1
        if 0 <= x <= RAIL_WIDTH:
            for i in range(len(NAV_ITEMS)):
                item_y = START_Y - i * ITEM_HEIGHT
                if item_y - ITEM_HEIGHT / 2 <= y <= item_y + ITEM_HEIGHT / 2:
                    self.hovered_index = i
                    break

    def on_mouse_press(self, x: float, y: float, window: arcade.Window) -> str | None:
        """Handle click on rail item and transition to corresponding view."""
        if 0 <= x <= RAIL_WIDTH:
            for i, (label, key, num) in enumerate(NAV_ITEMS):
                item_y = START_Y - i * ITEM_HEIGHT
                if item_y - ITEM_HEIGHT / 2 <= y <= item_y + ITEM_HEIGHT / 2:
                    if key != self.current_screen:
                        self.navigate_to(key, window)
                        return key
        return None

    def navigate_to(self, key: str, window: arcade.Window) -> None:
        """Navigate to target view."""
        if key == "menu":
            from game.views.menu_view import MenuView
            transition_to(window, MenuView())
        elif key == "campaign":
            from game.views.realm_map_view import RealmMapView
            transition_to(window, RealmMapView())
        elif key == "hangar":
            from game.views.ship_select_view import ShipSelectView
            transition_to(window, ShipSelectView())
        elif key == "codex":
            from game.views.codex_view import CodexView
            transition_to(window, CodexView())
        elif key == "sangha":
            from game.views.multiplayer_view import MultiplayerView
            transition_to(window, MultiplayerView())
        elif key == "account":
            from game.views.account_view import AccountView
            transition_to(window, AccountView())
        elif key == "settings":
            from game.views.settings_view import SettingsView
            transition_to(window, SettingsView())

    def draw(self) -> None:
        # Base rail panel (220px)
        arcade.draw_lrbt_rectangle_filled(0, RAIL_WIDTH, 0, HEIGHT, (*OBSIDIAN, 250))
        arcade.draw_line(RAIL_WIDTH, 0, RAIL_WIDTH, HEIGHT, (*GOLD, 75), 1)

        # Subtle scanlines in rail
        draw_scanlines(0, RAIL_WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # Header branding
        arcade.draw_text("VIMANA WARS", 24, HEIGHT - 38, GOLD,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("CELESTIAL WAR CONSOLE", 24, HEIGHT - 52, CYAN,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_line(24, HEIGHT - 62, RAIL_WIDTH - 24, HEIGHT - 62, (*CYAN, 50), 1)

        arcade.draw_text("CORE SYSTEMS", 24, START_Y + 30, GREY,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Nav items
        for i, (label, key, num) in enumerate(NAV_ITEMS):
            item_y = START_Y - i * ITEM_HEIGHT
            is_active = (key == self.current_screen)
            is_hovered = (i == self.hovered_index)

            # Highlight background on active/hover
            if is_active:
                arcade.draw_lrbt_rectangle_filled(
                    8, RAIL_WIDTH - 8,
                    item_y - ITEM_HEIGHT / 2 + 4, item_y + ITEM_HEIGHT / 2 - 4,
                    (*SURFACE_HIGH, 240)
                )
                # 3px Gold active indicator bar
                arcade.draw_lrbt_rectangle_filled(
                    8, 12,
                    item_y - ITEM_HEIGHT / 2 + 4, item_y + ITEM_HEIGHT / 2 - 4,
                    (*GOLD, 255)
                )
            elif is_hovered:
                arcade.draw_lrbt_rectangle_filled(
                    8, RAIL_WIDTH - 8,
                    item_y - ITEM_HEIGHT / 2 + 4, item_y + ITEM_HEIGHT / 2 - 4,
                    (*SURFACE_LOW, 180)
                )
                # 2px Dim cyan hover indicator bar
                arcade.draw_lrbt_rectangle_filled(
                    8, 11,
                    item_y - ITEM_HEIGHT / 2 + 4, item_y + ITEM_HEIGHT / 2 - 4,
                    (*CYAN, 180)
                )

            # Item label
            text_color = GOLD_BRIGHT if is_active else (CYAN_BRIGHT if is_hovered else GREY)
            arcade.draw_text(
                label, 26, item_y, text_color,
                font_size=10, bold=is_active, anchor_y="center",
                font_name=FONT_INTERFACE,
            )

            # Item index number
            num_color = GOLD if is_active else (CYAN if is_hovered else (*GREY[:3], 120))
            arcade.draw_text(
                num, RAIL_WIDTH - 20, item_y, num_color,
                font_size=8, bold=True, anchor_x="right", anchor_y="center",
                font_name=FONT_TELEMETRY,
            )

        # Bottom telemetry summary
        arcade.draw_line(24, 60, RAIL_WIDTH - 24, 60, (*GOLD, 50), 1)
        arcade.draw_text("SYSTEM STATUS // ONLINE", 24, 40, (*CYAN, 180),
                         font_size=7, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_text("BUILD 2026.09 // PY3.11", 24, 26, (*GREY, 140),
                         font_size=7, font_name=FONT_TELEMETRY)
