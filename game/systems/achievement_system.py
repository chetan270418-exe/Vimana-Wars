"""
game/systems/achievement_system.py
In-game achievements and trophy tracker with animated popup notifications.
Persists unlocked trophies in save.json.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_SCORE, COLOR_WHITE
from game.systems import save_system


ACHIEVEMENTS_LIST = [
    {
        "id": "first_blood",
        "name": "First Blood",
        "desc": "Slay your first Asura in defense of the realm.",
        "icon": "⚔️",
    },
    {
        "id": "chakram_master",
        "name": "Sudarshana Mastery",
        "desc": "Defeat 3+ enemies with a single Chakram throw.",
        "icon": "🪓",
    },
    {
        "id": "dash_phantom",
        "name": "Untouchable Phantom",
        "desc": "Execute 8 Vayu Dashes in a single run.",
        "icon": "💨",
    },
    {
        "id": "combo_god",
        "name": "Combo Maestro",
        "desc": "Reach a maximum ×8 combo multiplier.",
        "icon": "⚡",
    },
    {
        "id": "kumbhakarna_bane",
        "name": "Giant Slayer",
        "desc": "Defeat the Armored Titan Kumbhakarna on Wave 5.",
        "icon": "🛡️",
    },
    {
        "id": "ravana_vanquisher",
        "name": "Slayer of Lanka",
        "desc": "Vanquish the Ten-Headed Ravana on Wave 10.",
        "icon": "👑",
    },
    {
        "id": "hardcore_hero",
        "name": "Immortal Warrior",
        "desc": "Complete the entire campaign on Hard difficulty.",
        "icon": "🔥",
    },
    {
        "id": "bomb_annihilator",
        "name": "Brahmastra Unleashed",
        "desc": "Vaporize 8+ enemies with a single Brahmastra detonation.",
        "icon": "💥",
    },
    {
        "id": "boon_collector",
        "name": "Blessed by the Devas",
        "desc": "Attain 4 Divine Astral Boons in a single run.",
        "icon": "✨",
    },
    {
        "id": "high_scorer",
        "name": "Legend of the Realm",
        "desc": "Achieve a final score exceeding 25,000 points.",
        "icon": "🏆",
    },
]


class AchievementManager:
    def __init__(self):
        saved = save_system.load()
        self.unlocked: set[str] = set(saved.get("achievements", []))
        self.active_popups: list[dict] = []

    def check_unlock(self, ach_id: str) -> bool:
        if ach_id in self.unlocked:
            return False

        ach_data = next((a for a in ACHIEVEMENTS_LIST if a["id"] == ach_id), None)
        if not ach_data:
            return False

        self.unlocked.add(ach_id)

        # Save immediately
        saved = save_system.load()
        saved["achievements"] = list(self.unlocked)
        save_system.save(saved)

        # Trigger popup banner
        self.active_popups.append({
            "name": ach_data["name"],
            "desc": ach_data["desc"],
            "icon": ach_data["icon"],
            "timer": 3.5,
            "max_timer": 3.5,
        })
        return True

    def update(self, delta_time: float) -> None:
        for p in self.active_popups:
            p["timer"] -= delta_time
        self.active_popups = [p for p in self.active_popups if p["timer"] > 0]

    def draw(self) -> None:
        for i, p in enumerate(self.active_popups):
            frac = p["timer"] / p["max_timer"]
            # Slide in from top
            slide = min(1.0, (1.0 - frac) * 5.0) if frac > 0.8 else min(1.0, frac * 4.0)
            target_y = HEIGHT - 55 - i * 55
            cur_y = HEIGHT + 40 - (HEIGHT + 40 - target_y) * slide

            # Banner Background
            bx1, bx2 = WIDTH // 2 - 180, WIDTH // 2 + 180
            by1, by2 = cur_y - 20, cur_y + 20
            arcade.draw_lrbt_rectangle_filled(bx1, bx2, by1, by2, (20, 25, 45, 230))
            arcade.draw_lrbt_rectangle_outline(bx1, bx2, by1, by2, COLOR_SCORE, 2)

            # Icon & Text
            arcade.draw_text(
                "★ TROPHY UNLOCKED ★",
                WIDTH // 2, cur_y + 6,
                COLOR_SCORE, font_size=9, bold=True, anchor_x="center"
            )
            arcade.draw_text(
                f"{p['name']} — {p['desc']}",
                WIDTH // 2, cur_y - 10,
                COLOR_WHITE, font_size=10, bold=True, anchor_x="center"
            )
