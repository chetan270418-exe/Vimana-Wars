"""
game/systems/boon_system.py
Roguelite Deva Boon & Blessing System.
Provides 8 distinct mythological upgrade cards offered between waves.
"""
import random

BOONS_DATABASE = [
    {
        "id": "agni_fury",
        "name": "Agni's Solar Fury",
        "deva": "AGNI (GOD OF FIRE)",
        "desc": "Bullets ignite enemies with burning DoT for 3 seconds. Defeated burning foes explode.",
        "color": (255, 120, 30),
        "icon": "🔥",
    },
    {
        "id": "indra_thunder",
        "name": "Indra's Vajra Thunderbolt",
        "deva": "INDRA (KING OF HEAVENS)",
        "desc": "25% chance on bullet impact to trigger chain lightning zapping up to 3 nearby enemies.",
        "color": (120, 220, 255),
        "icon": "⚡",
    },
    {
        "id": "vayu_tempest",
        "name": "Vayu's Gale Tempest",
        "deva": "VAYU (LORD OF WINDS)",
        "desc": "Reduces Dash cooldown by 35% and leaves a damaging wind cyclone behind you on dash.",
        "color": (100, 255, 180),
        "icon": "🌪️",
    },
    {
        "id": "garuda_magnet",
        "name": "Garuda's Celestial Magnet",
        "deva": "GARUDA (DIVINE EAGLE)",
        "desc": "Magnetically pulls Astras, Power-ups, and healing drops toward your ship from across the arena.",
        "color": (255, 215, 60),
        "icon": "🦅",
    },
    {
        "id": "varuna_ward",
        "name": "Varuna's Oceanic Ward",
        "deva": "VARUNA (LORD OF WATERS)",
        "desc": "+35 Maximum HP and passive celestial rejuvenation restoring 6 HP every 7 seconds.",
        "color": (60, 180, 255),
        "icon": "🌊",
    },
    {
        "id": "sudarshana_keen",
        "name": "Sudarshana Keen Edge",
        "deva": "VISHNU (THE PRESERVER)",
        "desc": "Chakram size +30%, damage +40%, and reduces Chakram throw cooldown by 2.0s.",
        "color": (255, 230, 80),
        "icon": "🪓",
    },
    {
        "id": "yama_execution",
        "name": "Yama's Fatal Decree",
        "deva": "YAMA (LORD OF JUSTICE)",
        "desc": "Deal +60% Critical Damage to all enemy targets below 45% remaining health.",
        "color": (220, 50, 80),
        "icon": "💀",
    },
    {
        "id": "surya_beam",
        "name": "Surya's Radiant Pierce",
        "deva": "SURYA (THE SUN GOD)",
        "desc": "Every 7th shot fires an amplified golden Solar slug that pierces through all enemies.",
        "color": (255, 240, 140),
        "icon": "☀️",
    },
]


class BoonManager:
    def __init__(self):
        self.active_boons: dict[str, int] = {}
        self.shot_counter = 0
        self.regen_timer = 0.0

    def has_boon(self, boon_id: str) -> bool:
        return boon_id in self.active_boons

    def get_boon_level(self, boon_id: str) -> int:
        return self.active_boons.get(boon_id, 0)

    def add_boon(self, boon_id: str) -> None:
        if boon_id in self.active_boons:
            self.active_boons[boon_id] += 1
        else:
            self.active_boons[boon_id] = 1

    def get_random_choices(self, count: int = 3) -> list[dict]:
        # Filter available boons not yet maxed out (max level 3)
        pool = [b for b in BOONS_DATABASE if self.get_boon_level(b["id"]) < 3]
        return random.sample(pool, min(count, len(pool)))

    def update_passives(self, delta_time: float, player) -> None:
        # Varuna Ward passive regeneration
        if self.has_boon("varuna_ward") and player.alive:
            self.regen_timer += delta_time
            if self.regen_timer >= 7.0:
                self.regen_timer = 0.0
                heal_amt = 6 * self.get_boon_level("varuna_ward")
                player.heal(heal_amt)
