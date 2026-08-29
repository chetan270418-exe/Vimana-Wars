"""
game/entities/ship_classes.py
Vimana Ship Class definitions with distinct archetypes, stats, weapons, and special traits.
"""

SHIP_CLASSES = {
    "pushpaka": {
        "id": "pushpaka",
        "name": "Pushpaka Mk-I",
        "subtitle": "Celestial Balanced Cruiser",
        "hp": 100,
        "speed": 5.0,
        "fire_rate": 0.15,
        "bullet_damage": 25,
        "dash_cooldown": 2.2,
        "color": (210, 225, 255),
        "accent": (255, 215, 60),
        "desc": "The legendary golden chariot of the gods. Perfect balance of speed, firepower, and defense.",
    },
    "tripura": {
        "id": "tripura",
        "name": "Tripura Destroyer",
        "subtitle": "Heavy Armored Fortress",
        "hp": 160,
        "speed": 3.8,
        "fire_rate": 0.24,
        "bullet_damage": 48,
        "dash_cooldown": 3.0,
        "color": (255, 140, 60),
        "accent": (220, 60, 40),
        "desc": "Forged in cosmic celestial fires. Tremendous armor plating and heavy piercing railgun cannons.",
    },
    "garuda": {
        "id": "garuda",
        "name": "Garuda Interceptor",
        "subtitle": "High-Speed Void Striker",
        "hp": 75,
        "speed": 6.8,
        "fire_rate": 0.11,
        "bullet_damage": 18,
        "dash_cooldown": 1.4,
        "color": (120, 240, 255),
        "accent": (50, 255, 180),
        "desc": "Swift as thought itself. Devastating rapid-fire needle blasters and rapid twin-burst dashes.",
    },
}
