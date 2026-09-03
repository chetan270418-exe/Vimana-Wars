"""
game/views/codex_view.py
The Realm Archives & Mythological Lore Codex.
Provides in-depth lore, vector illustrations, and tactical guides for Vimanas, Astras, Asuras, and Realms.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import draw_menu_backdrop, draw_focus_panel


CODEX_ENTRIES = [
    {
        "category": "CHRONICLES",
        "title": "Act I — Swarga",
        "subtitle": "The Heavenly Realm (Waves 1-3)",
        "color": (255, 235, 100),
        "lore": "The war begins in heaven itself. Asura scouts and corrupted guardians breach Swarga's outer wards. The player learns the ropes while watching a realm once thought untouchable begin to crack.",
        "tip": "Maintain spatial awareness and prioritize fast chaser scouts before they flank your vessel."
    },
    {
        "category": "CHRONICLES",
        "title": "Act II — Kshira Sagara",
        "subtitle": "The Cosmic Ocean of Milk (Waves 4-6)",
        "color": (100, 220, 255),
        "lore": "The corruption spreads to the primordial ocean from which the gods churned immortality. At wave 5, Kumbhakarna — Ravana's slumbering titan brother — rises from the depths to guard the deep expanse.",
        "tip": "Defeating Kumbhakarna proves Ravana's inner circle can bleed. Dodge his sweeping flails."
    },
    {
        "category": "CHRONICLES",
        "title": "Act III — Dandaka Void",
        "subtitle": "The Mystical Astral Forest (Waves 7-9)",
        "color": (120, 255, 170),
        "lore": "Cutting into enemy territory where reality grows thin. Hostile, disorienting astral fauna and feral Asura fleets strike in dense formations as you approach the point of no return.",
        "tip": "Equip piercing Astras to punch clean flight corridors through dense swarm formations."
    },
    {
        "category": "CHRONICLES",
        "title": "Act IV — Lanka",
        "subtitle": "The Molten Rift of Ravana (Wave 10)",
        "color": (255, 60, 90),
        "lore": "The molten fortress heart of Ravana. Every system, Astra, and evasive reflex learned across the campaign is tested simultaneously. Break his tenfold grip or Dharma is extinguished forever.",
        "tip": "Save your Brahmastra bomb for Phase 3 when his summon swarms and spiral barrages peak."
    },
    {
        "category": "VIMANAS",
        "title": "Pushpaka Mk-I",
        "subtitle": "The Flagship Celestial Chariot",
        "color": (255, 215, 60),
        "lore": "Named for the legendary flying chariot of kings and gods. A balanced, dependable vessel favored by pilots who value steady endurance across a full campaign rather than fleeting burst.",
        "tip": "Balanced handling suitable for all combat scenarios. Ideal for pilots mastering the astral plane."
    },
    {
        "category": "VIMANAS",
        "title": "Tripura Destroyer",
        "subtitle": "The Three-Fortress Juggernaut",
        "color": (255, 140, 60),
        "lore": "Named for the myth of the three cities destroyed in a single divine strike. Heavy, armored, and built to withstand direct cosmic fire and return with devastating railgun volleys.",
        "tip": "High hull durability and single-shot damage. Use predictive aiming to compensate for lower cruising speed."
    },
    {
        "category": "VIMANAS",
        "title": "Garuda Interceptor",
        "subtitle": "The High-Speed Void Striker",
        "color": (120, 240, 255),
        "lore": "Named for Vishnu's celestial mount, the fastest creature in the cosmos. Trades heavy plating for supreme agility, rapid twin needle blasters, and dual-charge tactical dashes.",
        "tip": "Never stand still. Use your rapid dash recharge to slip through bullet hell patterns unscathed."
    },
    {
        "category": "ASTRAS",
        "title": "Brahmastra",
        "subtitle": "The Ultimate Annihilation Astra",
        "color": (255, 60, 220),
        "lore": "Created by Lord Brahma. A divine weapon of supreme finality whose activation unleashes a screen-clearing supernova flash that vaporizes every enemy projectile and hostile vessel.",
        "tip": "Press [F] when overwhelmed by swarms or to instantly wipe boss summons."
    },
    {
        "category": "ASTRAS",
        "title": "Sudarshana Chakram",
        "subtitle": "The Discus of Divine Order",
        "color": (255, 220, 50),
        "lore": "The spinning 108-serrated razor discus of Lord Vishnu. Slices through demon hulls, annihilates projectile walls, and returns unerringly to your Vimana's magnetic core.",
        "tip": "Press [Q] to carve safe flight channels through oncoming bullet waves."
    },
    {
        "category": "ASTRAS",
        "title": "Deva Elemental Astras",
        "subtitle": "Agni, Vayu, and Indra Blessings",
        "color": (255, 170, 60),
        "lore": "Fragments of celestial weapons lent to the lone pilot by the surviving Devas: Agni's blazing fury burns foes over time, Vayu's tempest grants evasive speed cyclones, and Indra's Vajra arcs lightning through armada ranks.",
        "tip": "Combine complementary Deva Astras between waves to awaken catastrophic Divine Synergies."
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
        "lore": "Master of all ten cosmic directions and breaker of divine exile. Commands the corrupted celestial fleet, deploying multi-stage spread lasers, bullet spirals, and demonic reinforcements.",
        "tip": "Save your Brahmastra bomb for Phase 3 when his summon swarms and spiral attacks intensify."
    },
    {
        "category": "ASURAS",
        "title": "Mahishasura",
        "subtitle": "The Warlord of the Setu Expanse (Wave 15 Mini-Boss)",
        "color": (255, 120, 40),
        "lore": "A shape-shifting warlord whose shockwave roars scatter celestial formations. When wounded, Mahishasura calls fast assault vessels into the breach.",
        "tip": "Keep moving through the radial shockwave and save your dash for the phase-two barrage."
    },
    {
        "category": "ASURAS",
        "title": "Vritra",
        "subtitle": "The Storm Serpent of the Final Citadel (Wave 20 Boss)",
        "color": (190, 80, 255),
        "lore": "The primordial drought serpent coiled around the Mahayuddha Citadel. Its celestial lightning barrages accelerate exponentially across each health phase.",
        "tip": "Read the attack line, circle the arena, and keep the Brahmastra for the final phase."
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
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time

    def on_draw(self) -> None:
        draw_menu_backdrop("THE REALM ARCHIVES & CODEX", "TACTICAL RECORDS // VIMANAS, ASTRAS, ASURAS", COLOR_SCORE, pulse=self._pulse)
        self._title.draw()

        # Left Sidebar (Entries List)
        sidebar_x = 70
        sidebar_w = 260
        start_y = HEIGHT - 95

        for i, entry in enumerate(CODEX_ENTRIES):
            y = start_y - i * 52
            is_sel = (i == self._selected)

            if is_sel:
                draw_focus_panel(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, entry["color"], selected=True)
            else:
                draw_focus_panel(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, entry["color"])

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
        TransitionOverlay.draw()

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
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())
