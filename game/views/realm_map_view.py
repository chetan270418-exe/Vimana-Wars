"""
Campaign realm map. Realms unlock from saved campaign progress.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WHITE, REALMS
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import draw_menu_backdrop, draw_focus_panel


REALM_ORDER = (1, 2, 3, 4, 5, 6, 7)
REALM_START_WAVES = {1: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19}
_NODE_POS = {
    1: (120, 365), 2: (340, 365), 3: (560, 365), 4: (780, 365),
    5: (230, 275), 6: (450, 275), 7: (670, 275),
}


def realm_is_unlocked(realm_id: int, last_wave: int) -> bool:
    return realm_id == 1 or last_wave >= REALM_START_WAVES[realm_id]


class RealmMapView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        self._hovered = -1
        self._selected = 1
        self._unlock_banner_timer = 0.0
        self._new_realm_name = ""
        self.sound_manager = SoundManager()
        self._stars = [
            (random.randrange(WIDTH), random.randrange(HEIGHT), random.uniform(0.5, 1.5))
            for _ in range(100)
        ]

        saved = save_system.load()
        self.last_wave = max(0, int(saved.get("last_wave", 0)))
        self._unlocked = [
            realm_id for realm_id in REALM_ORDER
            if realm_is_unlocked(realm_id, self.last_wave)
        ]
        last_realm = int(saved.get("last_realm", 1))
        if last_realm in self._unlocked:
            self._selected = last_realm

        # Show a newly reached realm once, the next time the map is opened.
        seen = set(saved.get("realm_unlock_seen", []))
        new_realms = [r for r in self._unlocked if r != 1 and r not in seen]
        if new_realms:
            self._new_realm_name = REALMS[new_realms[-1]]["name"]
            self._unlock_banner_timer = 3.0
            seen.update(new_realms)
            saved["realm_unlock_seen"] = sorted(seen)
            save_system.save(saved)
            self.sound_manager.play_powerup()

        self._title = arcade.Text(
            "CAMPAIGN REALM MAP", WIDTH // 2, 535,
            COLOR_SCORE, font_size=30, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "Choose an unlocked chapter to begin at its opening wave",
            WIDTH // 2, 500, COLOR_WHITE, font_size=11,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "← → / A D: Select   •   ENTER / Click: Enter Realm   •   ESC: Back",
            WIDTH // 2, 32, (150, 165, 195), font_size=10,
            anchor_x="center", anchor_y="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self._unlock_banner_timer = max(0.0, self._unlock_banner_timer - delta_time)

    def on_draw(self) -> None:
        draw_menu_backdrop("CAMPAIGN REALM MAP", "CONNECTED ROUTE // SELECT AN UNLOCKED CHAPTER", COLOR_SCORE, pulse=self._pulse)
        for x, y, radius in self._stars:
            sx = (x + self._pulse * 3.0) % WIDTH
            brightness = int(100 + 35 * math.sin(self._pulse + x * 0.03))
            arcade.draw_circle_filled(sx, y, radius, (brightness, brightness, brightness + 15))

        self._title.draw()
        self._subtitle.draw()

        # Connected campaign path.
        for left, right in zip(REALM_ORDER, REALM_ORDER[1:]):
            unlocked = left in self._unlocked and right in self._unlocked
            color = REALMS[right]["accent_color"] if unlocked else (65, 70, 95)
            lx, ly = _NODE_POS[left]
            rx, ry = _NODE_POS[right]
            arcade.draw_line(lx, ly, rx, ry, color, 4)
            arcade.draw_line(lx, ly + 5, rx, ry + 5, (20, 25, 45), 2)

        for realm_id in REALM_ORDER:
            realm = REALMS[realm_id]
            unlocked = realm_id in self._unlocked
            active = realm_id == self._selected
            hovered = realm_id == self._hovered
            x, y = _NODE_POS[realm_id]
            radius = 35 + (4 if active or hovered else 0)
            if unlocked:
                glow = int(25 + 20 * (math.sin(self._pulse * 3.0) + 1))
                arcade.draw_circle_filled(x, y, radius + 12, (*realm["accent_color"], glow))
                arcade.draw_circle_filled(x, y, radius, (20, 30, 60))
                if active:
                    arcade.draw_circle_outline(x, y, radius + 18, (*realm["accent_color"], 150), 2)
                arcade.draw_circle_outline(x, y, radius, realm["accent_color"], 3 if active else 2)
                arcade.draw_text(str(realm_id), x, y, realm["accent_color"],
                                 font_size=20, bold=True, anchor_x="center", anchor_y="center")
            else:
                arcade.draw_circle_filled(x, y, radius, (35, 38, 55))
                arcade.draw_circle_outline(x, y, radius, (80, 85, 105), 2)
                arcade.draw_text("🔒", x, y, (145, 150, 170),
                                 font_size=18, anchor_x="center", anchor_y="center")

            arcade.draw_text(
                realm["name"], x, y - 62,
                realm["accent_color"] if unlocked else (115, 120, 140),
                font_size=11, bold=True, anchor_x="center",
            )
            wave_label = f"Waves {realm['waves'][0]}–{realm['waves'][-1]}"
            arcade.draw_text(
                wave_label if unlocked else f"Unlock at Wave {REALM_START_WAVES[realm_id]}",
                x, y - 80, (175, 180, 200) if unlocked else (95, 100, 120),
                font_size=8, anchor_x="center",
            )
            if active and unlocked:
                arcade.draw_text("SELECTED", x, y + 58, COLOR_SCORE,
                                 font_size=8, bold=True, anchor_x="center")

        realm = REALMS[self._selected]
        unlocked_count = len(self._unlocked)
        draw_focus_panel(155, WIDTH - 155, 115, 205, realm["accent_color"], selected=True)
        arcade.draw_text(
            f"{realm['name']}  •  {realm['subtitle']}", WIDTH // 2, 182,
            realm["accent_color"], font_size=14, bold=True, anchor_x="center",
        )
        arcade.draw_text(
            f"Chapter opening: Wave {REALM_START_WAVES[self._selected]}    •    Realms unlocked: {unlocked_count}/7",
            WIDTH // 2, 157, COLOR_WHITE, font_size=10, anchor_x="center",
        )
        arcade.draw_text(
            "Select this realm to choose difficulty and your Vimana.",
            WIDTH // 2, 135, (160, 175, 205), font_size=9, anchor_x="center",
        )

        if self._unlock_banner_timer > 0:
            alpha = min(255, int(255 * min(1.0, self._unlock_banner_timer)))
            arcade.draw_lrbt_rectangle_filled(230, WIDTH - 230, 435, 470, (40, 30, 12, alpha))
            arcade.draw_text(
                f"✦ NEW REALM UNLOCKED: {self._new_realm_name.upper()} ✦",
                WIDTH // 2, 452, (255, 220, 80, alpha), font_size=13,
                bold=True, anchor_x="center", anchor_y="center",
            )

        self._hint.draw()
        TransitionOverlay.draw()

    def _realm_at(self, x: float, y: float) -> int:
        for realm_id in REALM_ORDER:
            nx, ny = _NODE_POS[realm_id]
            if math.hypot(x - nx, y - ny) <= 48:
                return realm_id
        return -1

    def _select(self, realm_id: int) -> None:
        if realm_id not in self._unlocked:
            return
        if realm_id != self._selected:
            self.sound_manager.play_ui_click(volume=0.35)
        self._selected = realm_id

    def _confirm(self) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()
        saved = save_system.load()
        saved["last_realm"] = self._selected
        save_system.save(saved)
        from game.views.difficulty_view import DifficultyView
        transition_to(
            self.window,
            DifficultyView(
                start_wave=REALM_START_WAVES[self._selected],
                realm_id=self._selected,
            ),
            style="wipe",
        )

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        realm_id = self._realm_at(x, y)
        if realm_id != self._hovered and realm_id in self._unlocked:
            self.sound_manager.play_ui_click(volume=0.20)
        self._hovered = realm_id
        if realm_id in self._unlocked:
            self._select(realm_id)

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        realm_id = self._realm_at(x, y)
        if realm_id in self._unlocked:
            if realm_id == self._selected:
                self._confirm()
            else:
                self._select(realm_id)

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            choices = list(self._unlocked)
            self._select(choices[(choices.index(self._selected) - 1) % len(choices)])
        elif key in (arcade.key.RIGHT, arcade.key.D):
            choices = list(self._unlocked)
            self._select(choices[(choices.index(self._selected) + 1) % len(choices)])
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._confirm()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        choices = list(self._unlocked)
        if hat_x < 0:
            self._select(choices[(choices.index(self._selected) - 1) % len(choices)])
        elif hat_x > 0:
            self._select(choices[(choices.index(self._selected) + 1) % len(choices)])
