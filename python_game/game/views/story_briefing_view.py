"""
game/views/story_briefing_view.py
Canonical Story Transmission Briefing Screen.
Follows Section 7.4 of the authoritative specification.
Implements the 6-Act narrative spine across all 7 campaign realms:
Act I (Swarga), Act II (Kshira Sagara), Act III (Dandaka Void),
Act IV (Lanka), Act V (The Long Pursuit), Act VI (Mahayuddha).
"""
import arcade
from constants import WIDTH, HEIGHT
from game.systems import save_system
from game.systems.asset_manager import AssetManager
from game.systems.sound_manager import SoundManager
from game.ui.transitions import TransitionOverlay, transition_to
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, ASTRA_RED, STARLIGHT, GREY, MUTED,
    FONT_CEREMONIAL, FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
)


_ACT_BRIEFINGS = {
    1: {
        "act_num": "ACT I",
        "title": "SWARGA INCURSION",
        "realm": "SWARGA OUTER WARDS",
        "waves": "WAVES 01–03",
        "pages": [
            {
                "speaker": "AKASHIC ARCHIVIST // TRANSMISSION 01.1",
                "headline": "THE CRACK IN THE HEAVENS",
                "text": "Dharma is not a territory; it is the universal balance that sustains every realm. "
                        "The golden wards of Swarga have been breached. Ravana has shattered his ancient cosmic exile "
                        "and siphons celestial Prana into dark resonance.",
                "accent": GOLD,
            },
            {
                "speaker": "COMMANDER ILA // CELESTIAL ORDER",
                "headline": "LAST FLIGHT PATH",
                "text": "The outer bastions of Indra are crumbling into the void. You are piloting the last commissioned "
                        "Vimana of the Celestial Order. Your flight corridor leads through four hostile realms to the molten gates of Lanka.",
                "accent": CYAN_BRIGHT,
            },
            {
                "speaker": "COMMANDER ILA // SORTIE DIRECTIVE",
                "headline": "RECLAIM DHARMA",
                "text": "Take flight. Harmonize with the divine Astras bestowed by the Devas. "
                        "Purge the Asura vanguard from Swarga's golden spires and ignite the path back to order.",
                "accent": GOLD_BRIGHT,
            },
        ],
    },
    2: {
        "act_num": "ACT II",
        "title": "KSHIRA SAGARA",
        "realm": "COSMIC OCEAN OF MILK",
        "waves": "WAVES 04–06",
        "pages": [
            {
                "speaker": "COMMANDER ILA // TACTICAL TRANSMISSION",
                "headline": "POISON IN THE MILK",
                "text": "We have crossed the threshold into Kshira Sagara, the primordial cosmic ocean. "
                        "Its waters of immortality have been corrupted by Asura toxic bio-munitions, turning luminescence into venomous black bile.",
                "accent": CYAN,
            },
            {
                "speaker": "AKASHIC ARCHIVIST // THREAT ANALYSIS",
                "headline": "THE TITAN AWAKENS",
                "text": "Deep beneath the gravitational eddies, Kumbhakarna stirs. The colossal brother of Ravana "
                        "has been awakened from his millennia of slumber to crush our corridor before we reach the outer reefs.",
                "accent": ASTRA_RED,
            },
            {
                "speaker": "COMMANDER ILA // COMBAT ORDERS",
                "headline": "PIERCE THE DEPTHS",
                "text": "Keep maximum thruster output. Do not linger in corrosive wakes. Fulfill the rites of the Devas, "
                        "fell Kumbhakarna, and breach the threshold of the deep astral forest.",
                "accent": GOLD_BRIGHT,
            },
        ],
    },
    3: {
        "act_num": "ACT III",
        "title": "DANDAKA VOID",
        "realm": "HAUNTED ASTRAL NEBULA",
        "waves": "WAVES 07–09",
        "pages": [
            {
                "speaker": "AKASHIC ARCHIVIST // SECTOR WARNING",
                "headline": "WHERE REALITY DISSOLVES",
                "text": "You are entering the Dandaka Void. Here, the boundaries of space fold like dead leaves. "
                        "Ancient feral Asuras nest within the grav-roots of shattered celestial archipelagos.",
                "accent": (180, 130, 255),
            },
            {
                "speaker": "COMMANDER ILA // TELEMETRY REPORT",
                "headline": "GHOST SIGNATURES",
                "text": "Sensors are catching hundreds of phantom targets. The void twists weapons telemetry and "
                        "hides sniper legions within dimensional rifts. Trust your manual crosshairs and intuition.",
                "accent": CYAN_BRIGHT,
            },
            {
                "speaker": "COMMANDER ILA // MISSION DIRECTIVE",
                "headline": "CLEANSE THE SHADOWS",
                "text": "Beyond this haunted sector lies Lanka. Burn a clean incandescent line through Dandaka. "
                        "Leave no Asura warship behind to ambush your rear flank.",
                "accent": GOLD,
            },
        ],
    },
    4: {
        "act_num": "ACT IV",
        "title": "LANKA SIEGE",
        "realm": "MOLTEN FORTRESS OF RAVANA",
        "waves": "WAVES 10–12",
        "pages": [
            {
                "speaker": "COMMANDER ILA // URGENT COMMAND",
                "headline": "THE CITADEL OF BRASS AND GOLD",
                "text": "Lanka orbital fortress is in visual range. A monstrous war sphere forged of celestial gold "
                        "and demon blood. Ravana's ten manifold heads govern ten independent fire-control networks.",
                "accent": ASTRA_RED,
            },
            {
                "speaker": "AKASHIC ARCHIVIST // SACRED CHRONICLE",
                "headline": "THE TEN MANIFOLDS",
                "text": "Ravana believes himself immortal. His pride has unknotted the cosmic laws of life and rebirth. "
                        "Channel the Sudarshana and Brahmastra Astras to shatter his ten-fold armor and reclaim the throne.",
                "accent": GOLD_BRIGHT,
            },
            {
                "speaker": "COMMANDER ILA // FINAL ENGAGEMENT",
                "headline": "BREAK THE TYRANT",
                "text": "All auxiliary squadrons have been intercepted. It is just you and the flagship. "
                        "End Ravana's reign over Lanka. For Dharma. For the heavens.",
                "accent": GOLD,
            },
        ],
    },
    5: {
        "act_num": "ACT V",
        "title": "THE LONG PURSUIT",
        "realm": "SETU EXPANSE & NARAKA FORGE",
        "waves": "WAVES 13–18",
        "pages": [
            {
                "speaker": "COMMANDER ILA // AFTERMATH TELEMETRY",
                "headline": "THE SHATTERED HEIRS",
                "text": "Ravana has fallen at Lanka, but his destruction did not end the war — it fractured his armada. "
                        "His rogue generals have retreated across the Setu causeway to the subterranean hell-foundry of Naraka.",
                "accent": (255, 140, 60),
            },
            {
                "speaker": "AKASHIC ARCHIVIST // INTEL REPORT",
                "headline": "THE FORGE OF NAMUCI",
                "text": "In Naraka, demon artificers are mass-producing automated Asura juggernauts powered by molten core fire. "
                        "Mahishasura and Namuci lead the counter-siege from iron dreadnoughts.",
                "accent": ASTRA_RED,
            },
            {
                "speaker": "COMMANDER ILA // PURSUIT SORTIE",
                "headline": "EXTINGUISH THE FURNACE",
                "text": "We cannot allow the Asura war machine to rebuild. Cross the Setu void bridge, enter the forge, "
                        "and destroy the production cauldrons before they swarm the galaxy anew.",
                "accent": GOLD_BRIGHT,
            },
        ],
    },
    6: {
        "act_num": "ACT VI",
        "title": "MAHAYUDDHA",
        "realm": "CITADEL AT THE EDGE OF CREATION",
        "waves": "WAVES 19–20",
        "pages": [
            {
                "speaker": "AKASHIC ARCHIVIST // COSMIC HORIZON",
                "headline": "THE EDGE OF CREATION",
                "text": "You have flown beyond the boundaries of known stars into the Mahayuddha Citadel. "
                        "Here at the cosmic horizon, the great serpent Vritra has coiled around the pillars of creation.",
                "accent": (160, 100, 255),
            },
            {
                "speaker": "COMMANDER ILA // FINAL WARNS",
                "headline": "VRITRA THE STORM SERPENT",
                "text": "Vritra was never Ravana's servant — he was the eternal warden waiting for Dharma to break. "
                        "His storm bolts swallow stars whole. Only the purest Astra resonance can pierce his scales.",
                "accent": ASTRA_RED,
            },
            {
                "speaker": "COMMANDER ILA // THE TRANSCENDENT SORTIE",
                "headline": "RESTORE THE UNIVERSE",
                "text": "Pilot, this is the final flight of the Celestial Order. Slay the serpent. "
                        "Reclaim Dharma across all seven realms. Achieve Karmic Transcendence.",
                "accent": GOLD_BRIGHT,
            },
        ],
    },
}


def _get_act_for_realm(realm_id: int) -> int:
    if realm_id <= 1:
        return 1
    elif realm_id == 2:
        return 2
    elif realm_id == 3:
        return 3
    elif realm_id == 4:
        return 4
    elif realm_id in (5, 6):
        return 5
    else:
        return 6


class StoryBriefingView(arcade.View):
    """6-Act skippable transmission terminal introducing the campaign."""

    def __init__(self, realm_id: int = 1, start_wave: int = 1, difficulty: str = "normal",
                 return_to_menu: bool = False):
        super().__init__()
        self.realm_id = realm_id
        self.start_wave = start_wave
        self.difficulty = difficulty
        self._return_to_menu = return_to_menu
        self.sound_manager = SoundManager()

        self.act_idx = _get_act_for_realm(realm_id)
        self.act_data = _ACT_BRIEFINGS.get(self.act_idx, _ACT_BRIEFINGS[1])

        self.page = 0
        self.elapsed = 0.0
        self._button = arcade.Text("NEXT TRANSMISSION", 0, 0)
        self._set_page(0)

    def _set_page(self, page: int) -> None:
        self.page = max(0, min(len(self.act_data["pages"]) - 1, page))
        is_last = (self.page == len(self.act_data["pages"]) - 1)
        self._button.text = "BEGIN SORTIE" if is_last else "NEXT TRANSMISSION"

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self.elapsed += delta_time

    def on_draw(self) -> None:
        self.clear()

        # Background subtle scanlines
        draw_scanlines(0, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # 40% opacity hero / realm graphic on the right
        hero_tex = AssetManager.texture("hero_vimana_wars.png")
        AssetManager.draw(hero_tex, 680, 290, 420, 420, color=(255, 255, 255, 95))

        # ── Left Transmission Panel (x=36 to 540, 56% width) ─────────────────
        left, right = 36.0, 540.0
        bottom, top = 48.0, HEIGHT - 48.0

        page_record = self.act_data["pages"][self.page]
        accent_col = page_record["accent"]

        draw_chamfered_panel(left, right, bottom, top, accent_col,
                             fill=SURFACE_HIGH, alpha=245, border_width=2,
                             selected=True, cut=12.0, scanlines=True)
        draw_corner_etching(left, right, bottom, top, GOLD, length=16.0, alpha=130)

        # Header Act Banner
        arcade.draw_text(f"{self.act_data['act_num']}  //  {self.act_data['title']}",
                         left + 24, top - 32, GOLD_BRIGHT,
                         font_size=16, bold=True, font_name=FONT_CEREMONIAL)
        arcade.draw_text(f"{self.act_data['realm']}  •  {self.act_data['waves']}",
                         left + 24, top - 52, CYAN,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)

        arcade.draw_line(left + 24, top - 64, right - 24, top - 64, (*GOLD, 60), 1)

        # Speaker & Title
        arcade.draw_text(page_record["speaker"], left + 24, top - 92,
                         CYAN_BRIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_text(page_record["headline"], left + 24, top - 114,
                         accent_col, font_size=14, bold=True, font_name=FONT_INTERFACE)

        # Body text (word-wrapped to <= 72 chars per line)
        words = page_record["text"].split()
        lines = []
        cur_line = []
        cur_len = 0
        for w in words:
            if cur_len + len(w) + 1 <= 54:
                cur_line.append(w)
                cur_len += len(w) + 1
            else:
                lines.append(" ".join(cur_line))
                cur_line = [w]
                cur_len = len(w)
        if cur_line:
            lines.append(" ".join(cur_line))

        body_y = top - 150
        for line in lines:
            arcade.draw_text(line, left + 24, body_y,
                             STARLIGHT, font_size=10, font_name=FONT_INTERFACE)
            body_y -= 22

        # Page Dots (Bottom Left)
        dot_start_x = left + 28
        for i in range(len(self.act_data["pages"])):
            dx = dot_start_x + i * 16
            is_active = (i == self.page)
            arcade.draw_circle_filled(dx, bottom + 32, 4 if is_active else 2.5,
                                      GOLD if is_active else GREY)

        # Advance / Sortie Action Hint
        is_last_page = (self.page == len(self.act_data["pages"]) - 1)
        action_label = "[ ENTER / SPACE : LAUNCH SORTIE ▶ ]" if is_last_page else "[ ENTER / SPACE : NEXT TRANSMISSION ▶ ]"
        arcade.draw_text(action_label, right - 24, bottom + 32,
                         GOLD_BRIGHT if is_last_page else CYAN_BRIGHT,
                         font_size=9, bold=True, anchor_x="right", anchor_y="center",
                         font_name=FONT_INTERFACE)

        # Skip hint (Bottom Right of screen)
        arcade.draw_text("ESC : SKIP BRIEFING", WIDTH - 48, 32,
                         MUTED, font_size=9, bold=True, anchor_x="right",
                         font_name=FONT_TELEMETRY)

        # Transition Wipe
        TransitionOverlay.draw()

    def _advance_or_start(self) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        if self.page < len(self.act_data["pages"]) - 1:
            self.page += 1
        else:
            self._start_game()

    def _start_game(self) -> None:
        saved = save_system.load()
        saved_seen = set(saved.get("seen_briefings", []))
        saved_seen.add(self.act_idx)
        saved["seen_briefings"] = sorted(saved_seen)
        save_system.save(saved)

        # Launch into DifficultyView or directly into ShipSelectView
        from game.views.difficulty_view import DifficultyView
        difficulty_view = DifficultyView(start_wave=self.start_wave, realm_id=self.realm_id)
        transition_to(self.window, difficulty_view)

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._advance_or_start()
        elif key == arcade.key.LEFT and self.page > 0:
            self.page -= 1
            self.sound_manager.play_ui_click(volume=0.2)
        elif key == arcade.key.RIGHT:
            self._advance_or_start()
        elif key == arcade.key.ESCAPE:
            self._start_game()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if 36 <= x <= 540 and 48 <= y <= HEIGHT - 48:
                self._advance_or_start()
            elif x >= WIDTH - 180 and y <= 60:
                self._start_game()
