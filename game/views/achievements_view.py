"""Browsable trophy cabinet for every achievement in the campaign."""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WHITE
from game.systems import save_system
from game.systems.achievement_system import ACHIEVEMENTS_LIST
from game.ui.transitions import TransitionOverlay, transition_to
from game.ui.vedic_theme import draw_menu_backdrop, draw_focus_panel


class AchievementsView(arcade.View):
    PER_PAGE = 8

    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._page = 0
        self._selected = 0
        self._unlocked = set(save_system.load().get("achievements") or [])
        self._title = arcade.Text("ACHIEVEMENT HALL", WIDTH // 2, HEIGHT - 48,
                                  COLOR_SCORE, font_size=28, bold=True,
                                  anchor_x="center", anchor_y="center")
        self._hint = arcade.Text(
            "↑ ↓: Select   •   ← →: Page   •   ENTER: Details   •   ESC: Back",
            WIDTH // 2, 28, (150, 165, 195), font_size=10,
            anchor_x="center", anchor_y="center")
        self._detail = ""

    @property
    def page_count(self):
        return max(1, (len(ACHIEVEMENTS_LIST) + self.PER_PAGE - 1) // self.PER_PAGE)

    def on_show_view(self):
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time):
        TransitionOverlay.update(delta_time)

    def on_draw(self):
        draw_menu_backdrop("ACHIEVEMENT HALL", "CAMPAIGN RECORDS // SELECT A TROPHY FOR DETAILS", COLOR_SCORE)
        unlocked_count = len(self._unlocked.intersection({a["id"] for a in ACHIEVEMENTS_LIST}))
        self._title.text = f"ACHIEVEMENT HALL  •  {unlocked_count}/{len(ACHIEVEMENTS_LIST)} UNLOCKED"
        self._title.draw()

        start = self._page * self.PER_PAGE
        page_items = ACHIEVEMENTS_LIST[start:start + self.PER_PAGE]
        for index, achievement in enumerate(page_items):
            col = index // 4
            row = index % 4
            cx = 250 + col * 400
            cy = 430 - row * 88
            absolute_index = start + index
            is_unlocked = achievement["id"] in self._unlocked
            is_selected = index == self._selected
            accent = COLOR_SCORE if is_unlocked else (85, 95, 125)
            if is_selected:
                accent = (120, 220, 255)
            draw_focus_panel(cx - 180, cx + 180, cy - 32, cy + 32, accent, selected=is_selected)

            icon = achievement["icon"] if is_unlocked else "🔒"
            arcade.draw_text(icon, cx - 158, cy, COLOR_WHITE if is_unlocked else (110, 115, 140),
                             font_size=18, anchor_x="center", anchor_y="center")
            arcade.draw_text(achievement["name"], cx - 132, cy + 12,
                             accent, font_size=11, bold=True)
            arcade.draw_text(achievement["desc"], cx - 132, cy - 10,
                             (205, 210, 230) if is_unlocked else (110, 118, 140),
                             font_size=8)

        arcade.draw_text(f"PAGE {self._page + 1}/{self.page_count}", WIDTH // 2, 80,
                         (140, 155, 190), font_size=10, bold=True,
                         anchor_x="center")
        if self._detail:
            arcade.draw_text(self._detail, WIDTH // 2, 58, COLOR_SCORE,
                             font_size=9, anchor_x="center")
        self._hint.draw()
        TransitionOverlay.draw()

    def _activate_selected(self):
        start = self._page * self.PER_PAGE
        items = ACHIEVEMENTS_LIST[start:start + self.PER_PAGE]
        if items:
            achievement = items[self._selected]
            status = "UNLOCKED" if achievement["id"] in self._unlocked else "LOCKED"
            self._detail = f"{status}  •  {achievement['name']}  •  {achievement['desc']}"

    def _item_at(self, x, y):
        start = self._page * self.PER_PAGE
        items = ACHIEVEMENTS_LIST[start:start + self.PER_PAGE]
        for index in range(len(items)):
            col = index // 4
            row = index % 4
            cx = 250 + col * 400
            cy = 430 - row * 88
            if cx - 180 <= x <= cx + 180 and cy - 32 <= y <= cy + 32:
                return index
        return -1

    def on_mouse_motion(self, x, y, dx, dy):
        index = self._item_at(x, y)
        if index >= 0:
            self._selected = index

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            index = self._item_at(x, y)
            if index >= 0:
                self._selected = index
                self._activate_selected()

    def on_key_press(self, key, modifiers):
        start = self._page * self.PER_PAGE
        count = len(ACHIEVEMENTS_LIST[start:start + self.PER_PAGE])
        if key in (arcade.key.UP, arcade.key.W):
            self._selected = (self._selected - 1) % max(1, count)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected = (self._selected + 1) % max(1, count)
        elif key in (arcade.key.LEFT, arcade.key.A):
            self._page = (self._page - 1) % self.page_count
            self._selected = 0
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._page = (self._page + 1) % self.page_count
            self._selected = 0
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            self._activate_selected()
        elif key == arcade.key.ESCAPE:
            if self.return_view:
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())
