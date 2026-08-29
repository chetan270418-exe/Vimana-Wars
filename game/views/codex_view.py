"""
game/views/codex_view.py
The Realm Archives & Mythological Lore Codex.
Provides in-depth lore, vector illustrations, and tactical guides for Vimanas, Astras, Asuras, and Realms.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE


CODEX_ENTRIES = [
    {
        "category": "VIMANAS",
        "title": "Pushpaka Vimana",
        "subtitle": "The Flagship Celestial Chariot",
        "color": (255, 215, 60),
        "lore": "Engineered by Vishwakarma, the divine architect. Capable of moving at the speed of thought and navigating both cosmic skies and interstellar dimensions with complete agility.",
        "tip": "Balanced handling suitable for all combat scenarios. Ideal for beginners and veterans alike."
    },
    {
        "category": "VIMANAS",
        "title": "Tripura Destroyer",
        "subtitle": "The Three-Fortress Juggernaut",
        "color": (255, 140, 60),
        "lore": "Constructed from the indestructible remnants of the three celestial cities of Tripura. Boasts reinforced impenetrable plating and high-caliber railgun cannons.",
        "tip": "High health and single-shot damage, but requires careful positioning due to lower cruising speed."
    },
    {
        "category": "ASTRAS",
        "title": "Brahmastra",
        "subtitle": "The Ultimate Annihilation Astra",
        "color": (255, 60, 220),
        "lore": "Created by Lord Brahma. A weapon of supreme finality whose activation unleashes a screen-clearing supernova flash that vaporizes every enemy vessel in the vicinity.",
        "tip": "Press [F] when overwhelmed by swarms or to instantly wipe boss summons."
    },
    {
        "category": "ASTRAS",
        "title": "Sudarshana Chakram",
        "subtitle": "The Discus of Divine Order",
        "color": (255, 220, 50),
        "lore": "The spinning 108-serrated razor discus of Lord Vishnu. Slices through ranks of demon fleets, shatters incoming projectiles into sparks, and returns unerringly to the wielder.",
        "tip": "Press [Q] to throw in front of dangerous projectile walls to clear a path."
    },
    {
        "category": "ASURAS",
        "title": "Kumbhakarna",
        "subtitle": "The Sleeping Titan (Wave 5 Mini-Boss)",
        "color": (210, 140, 20),
        "lore": "Brother of Ravana, cursed to sleep for six months but possessing apocalyptic brute strength when awakened. Charges across battle lines wielding heavy radial mace flails.",
        "tip": "Maintain distance during his charge attack and use Vayu Dash to slip behind his armor."
    },
    {
        "category": "ASURAS",
        "title": "Ravana",
        "subtitle": "King of Lanka & Ten-Headed Emperor (Wave 10 Boss)",
        "color": (220, 0, 80),
        "lore": "Master of all ten cosmic directions and ruler of the underworld. Commands the celestial Pushpaka fleet, deploying multi-stage spread lasers, bullet spirals, and demonic reinforcements.",
        "tip": "Save your Brahmastra bomb for Phase 3 when his summon swarms and spiral attacks intensify."
    },
]


class CodexView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._selected = 0
        self._pulse = 0.0

        # UI Texts
        self._title = arcade.Text(
            "THE REALM ARCHIVES & CODEX",
            WIDTH // 2, HEIGHT - 55,
            COLOR_SCORE, font_size=30, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "↑ ↓ : Select Entry   •   ESC : Return to Main Menu",
            WIDTH // 2, 30,
            (160, 170, 200), font_size=11, bold=True,
            anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time

    def on_draw(self) -> None:
        self.clear()

        self._title.draw()

        # Left Sidebar (Entries List)
        sidebar_x = 70
        sidebar_w = 260
        start_y = HEIGHT - 120

        for i, entry in enumerate(CODEX_ENTRIES):
            y = start_y - i * 65
            is_sel = (i == self._selected)

            if is_sel:
                arcade.draw_lrbt_rectangle_filled(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, (35, 45, 80))
                arcade.draw_lrbt_rectangle_outline(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, entry["color"], 2)
            else:
                arcade.draw_lrbt_rectangle_filled(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, (20, 24, 40))

            arcade.draw_text(f"[{entry['category']}]", sidebar_x + 14, y + 10, (140, 150, 180), font_size=8, bold=True)
            arcade.draw_text(entry["title"], sidebar_x + 14, y - 8, entry["color"] if is_sel else (200, 205, 220), font_size=12, bold=True)

        # Right Detail Panel
        detail_x = 360
        detail_w = WIDTH - detail_x - 70
        detail_y = HEIGHT - 100
        detail_h = 420

        arcade.draw_lrbt_rectangle_filled(detail_x, detail_x + detail_w, detail_y - detail_h, detail_y, (22, 26, 48))
        cur = CODEX_ENTRIES[self._selected]
        arcade.draw_lrbt_rectangle_outline(detail_x, detail_x + detail_w, detail_y - detail_h, detail_y, cur["color"], 2)

        # Header Details
        arcade.draw_text(cur["title"].upper(), detail_x + 30, detail_y - 45, cur["color"], font_size=24, bold=True)
        arcade.draw_text(cur["subtitle"], detail_x + 30, detail_y - 75, (170, 185, 215), font_size=12, bold=True)
        arcade.draw_line(detail_x + 30, detail_y - 90, detail_x + detail_w - 30, detail_y - 90, (60, 70, 100), 1)

        # Lore Paragraph
        arcade.draw_text("MYTHOLOGICAL RECORD:", detail_x + 30, detail_y - 125, COLOR_SCORE, font_size=11, bold=True)
        lore_lines = self._wrap_text(cur["lore"], 46)
        for l_idx, line in enumerate(lore_lines):
            arcade.draw_text(line, detail_x + 30, detail_y - 155 - l_idx * 22, (220, 225, 240), font_size=11)

        # Tactical Tip Box
        tip_y = detail_y - 300
        arcade.draw_lrbt_rectangle_filled(detail_x + 30, detail_x + detail_w - 30, tip_y - 60, tip_y + 10, (15, 18, 32))
        arcade.draw_lrbt_rectangle_outline(detail_x + 30, detail_x + detail_w - 30, tip_y - 60, tip_y + 10, (80, 140, 200), 1)
        arcade.draw_text("TACTICAL DOCTRINE:", detail_x + 45, tip_y - 12, (100, 220, 255), font_size=9, bold=True)
        tip_lines = self._wrap_text(cur["tip"], 44)
        for t_idx, line in enumerate(tip_lines):
            arcade.draw_text(line, detail_x + 45, tip_y - 32 - t_idx * 18, (190, 200, 220), font_size=9)

        self._hint.draw()

    def _wrap_text(self, text: str, max_chars: int) -> list[str]:
        words = text.split()
        lines = []
        cur = []
        cur_len = 0
        for w in words:
            if cur_len + len(w) + 1 > max_chars:
                lines.append(" ".join(cur))
                cur = [w]
                cur_len = len(w)
            else:
                cur.append(w)
                cur_len += len(w) + 1
        if cur:
            lines.append(" ".join(cur))
        return lines

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._selected = (self._selected - 1) % len(CODEX_ENTRIES)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected = (self._selected + 1) % len(CODEX_ENTRIES)
        elif key == arcade.key.ESCAPE:
            if self.return_view:
                self.window.show_view(self.return_view)
            else:
                from game.views.menu_view import MenuView
                self.window.show_view(MenuView())
