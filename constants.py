# ─────────────────────────────────────────────
#  Vimana Wars — constants.py
#  All magic numbers live here. Tweak freely.
# ─────────────────────────────────────────────

# Screen
WIDTH = 900
HEIGHT = 600
SCREEN_TITLE = "Vimana Wars"
FPS = 60

# ── Backend & Network ─────────────────────────────────────────────────────────
LEADERBOARD_API_URL = "http://127.0.0.1:5000"
NETWORK_TIMEOUT = 2.5  # seconds before fallback to offline mode

# ── Difficulty multipliers ────────────────────────────────────────────────────
# Applied by GameView to scale HP, damage, enemy speed, and spawn counts.
DIFFICULTY_SETTINGS = {
    #              player_hp_mult  damage_taken_mult  enemy_speed_mult  spawn_mult
    "easy":   dict(player_hp=1.5, dmg_in=0.6,  enemy_spd=0.8, spawn=0.7),
    "normal": dict(player_hp=1.0, dmg_in=1.0,  enemy_spd=1.0, spawn=1.0),
    "hard":   dict(player_hp=0.7, dmg_in=1.4,  enemy_spd=1.25, spawn=1.3),
}

def get_difficulty_mults(level: str = "normal") -> dict:
    """Return the multiplier dict for the given difficulty level."""
    return DIFFICULTY_SETTINGS.get(level, DIFFICULTY_SETTINGS["normal"])


# ── Themed Mythological Realms ────────────────────────────────────────────────
REALMS = {
    1: {
        "name": "Swarga",
        "subtitle": "The Heavenly Celestial Realm",
        "waves": (1, 2, 3),
        "bg_color": (5, 8, 26),
        "nebula_palette": [(30, 40, 90), (10, 50, 100), (50, 40, 110)],
        "accent_color": (120, 200, 255),
    },
    2: {
        "name": "Kshira Sagara",
        "subtitle": "The Cosmic Ocean of Milk",
        "waves": (4, 5, 6),
        "bg_color": (4, 18, 28),
        "nebula_palette": [(10, 70, 90), (0, 90, 80), (20, 110, 100)],
        "accent_color": (80, 240, 220),
    },
    3: {
        "name": "Dandaka Void",
        "subtitle": "The Mystical Astral Forest",
        "waves": (7, 8, 9),
        "bg_color": (14, 5, 24),
        "nebula_palette": [(70, 10, 80), (30, 80, 40), (90, 20, 90)],
        "accent_color": (210, 100, 255),
    },
    4: {
        "name": "Lanka",
        "subtitle": "The Molten Rift of Ravana",
        "waves": (10, 11, 12),
        "bg_color": (22, 4, 10),
        "nebula_palette": [(110, 15, 25), (140, 40, 10), (80, 0, 40)],
        "accent_color": (255, 70, 70),
    },
    5: {
        "name": "Setu Expanse",
        "subtitle": "The Bridge Between Celestial Worlds",
        "waves": (13, 14, 15),
        "bg_color": (9, 12, 30),
        "nebula_palette": [(35, 45, 120), (100, 35, 90), (30, 90, 130)],
        "accent_color": (255, 150, 80),
    },
    6: {
        "name": "Naraka Forge",
        "subtitle": "The Burning Foundry of Asura Warships",
        "waves": (16, 17, 18),
        "bg_color": (25, 7, 5),
        "nebula_palette": [(150, 35, 10), (100, 10, 30), (180, 65, 5)],
        "accent_color": (255, 100, 40),
    },
    7: {
        "name": "Mahayuddha Citadel",
        "subtitle": "The Final Astral Battlefield",
        "waves": (19, 20),
        "bg_color": (18, 4, 24),
        "nebula_palette": [(120, 15, 120), (70, 10, 80), (180, 30, 100)],
        "accent_color": (255, 80, 190),
    },
}

def get_realm_for_wave(wave_num: int) -> dict:
    effective_wave = ((wave_num - 1) % 20) + 1
    if effective_wave <= 3:
        return REALMS[1]
    elif effective_wave <= 6:
        return REALMS[2]
    elif effective_wave <= 9:
        return REALMS[3]
    elif effective_wave <= 12:
        return REALMS[4]
    elif effective_wave <= 15:
        return REALMS[5]
    elif effective_wave <= 18:
        return REALMS[6]
    return REALMS[7]


# Player
PLAYER_SPEED = 5.0
PLAYER_SPEED_BOOSTED = 8.0
PLAYER_SHOOT_COOLDOWN = 0.15   # seconds between shots (hold-to-fire)
PLAYER_MAX_HP = 100
PLAYER_RADIUS = 20
PLAYER_INVINCIBILITY_TIME = 0.5  # seconds of i-frames after being hit
PLAYER_CONTACT_DAMAGE = 15       # damage taken from touching an enemy

# Bullets
PLAYER_BULLET_SPEED = 13
PLAYER_BULLET_RADIUS = 5
PLAYER_BULLET_DAMAGE = 25
ENEMY_BULLET_SPEED = 6
ENEMY_BULLET_RADIUS = 5
ENEMY_BULLET_DAMAGE = 12

# Asura Fast (Chaser)
ASURA_FAST_HP = 30
ASURA_FAST_SPEED = 3.5
ASURA_FAST_SCORE = 100
ASURA_FAST_RADIUS = 14

# Asura Tank (Brute)
ASURA_TANK_HP = 150
ASURA_TANK_SPEED = 1.0
ASURA_TANK_SCORE = 300
ASURA_TANK_RADIUS = 28
ASURA_TANK_CONTACT_DAMAGE = 25

# Asura Ranged (Shooter)
ASURA_RANGED_HP = 60
ASURA_RANGED_SPEED = 1.5
ASURA_RANGED_SCORE = 200
ASURA_RANGED_RADIUS = 16
ASURA_RANGED_FIRE_RATE = 2.0     # seconds between shots
ASURA_RANGED_PREFERRED_DIST = 250

# Asura Kamikaze
ASURA_KAMIKAZE_HP = 20
ASURA_KAMIKAZE_SPEED = 5.5
ASURA_KAMIKAZE_SCORE = 150
ASURA_KAMIKAZE_RADIUS = 10
ASURA_KAMIKAZE_EXPLOSION_RADIUS = 70
ASURA_KAMIKAZE_EXPLOSION_DAMAGE = 40

# Mini-Boss — Kumbhakarna (Wave 5)
KUMBHAKARNA_HP = 750
KUMBHAKARNA_RADIUS = 38
KUMBHAKARNA_SPEED = 1.8
KUMBHAKARNA_SCORE = 2500
KUMBHAKARNA_SLAM_RATE = 4.0

# Boss — Ravana (Wave 10)
RAVANA_HP = 1500
RAVANA_RADIUS = 46
RAVANA_SPEED = 1.2
RAVANA_SCORE = 5000
RAVANA_PHASE2_HP = 0.66   # fraction of max HP where phase 2 begins
RAVANA_PHASE3_HP = 0.33   # fraction of max HP where phase 3 begins
RAVANA_FIRE_RATE_P1 = 1.5
RAVANA_FIRE_RATE_P2 = 1.0
RAVANA_FIRE_RATE_P3 = 0.7
RAVANA_SPIRAL_RATE = 0.08  # seconds between spiral shots
RAVANA_SUMMON_RATE = 5.0   # seconds between summons in phase 3

# Additional campaign bosses (Waves 15 and 20)
MAHISHASURA_HP = 2200
MAHISHASURA_RADIUS = 50
MAHISHASURA_SPEED = 1.1
MAHISHASURA_SCORE = 7000

VRITRA_HP = 3000
VRITRA_RADIUS = 56
VRITRA_SPEED = 0.9
VRITRA_SCORE = 10000

# Power-ups
POWERUP_RADIUS = 14
SHIELD_MAX_HITS = 3
SHIELD_DURATION = 10.0
SPREAD_DURATION = 8.0
SPEED_DURATION = 6.0
HEALTH_RESTORE = 30
MAX_POWERUPS_ACTIVE = 2       # max collectables on map at once

# Wave manager
WAVE_ANNOUNCE_DURATION = 2.5  # seconds the "Wave X!" banner shows
WAVE_CLEAR_DELAY = 3.0        # seconds between last kill and next wave
BOSS_WAVE_NUMBER = 10
CAMPAIGN_FINAL_WAVE = 20
CAMPAIGN_BOSS_WAVES = (10, 20)
CAMPAIGN_MINI_BOSS_WAVES = (5, 15)
POWERUP_SPAWN_EVERY_N_WAVES = 2

# Score / combo
COMBO_WINDOW = 2.0   # seconds to chain kills for a multiplier
MAX_COMBO = 10

# Colours (RGB tuples)
COLOR_BG           = (5, 5, 20)
COLOR_PLAYER       = (200, 210, 255)
COLOR_BULLET_PLAYER = (255, 230, 60)
COLOR_BULLET_ENEMY  = (255, 80, 80)

COLOR_ASURA_FAST      = (230, 120, 30)
COLOR_ASURA_TANK      = (140, 20, 20)
COLOR_ASURA_RANGED    = (150, 40, 210)
COLOR_ASURA_KAMIKAZE  = (255, 60, 60)
COLOR_KUMBHAKARNA     = (180, 110, 20)
COLOR_RAVANA          = (180, 0, 80)

COLOR_HP_BG    = (80, 0, 0)
COLOR_HP_GREEN = (30, 200, 70)
COLOR_HP_LOW   = (220, 60, 0)
COLOR_SHIELD   = (60, 160, 255)
COLOR_SCORE    = (255, 220, 50)
COLOR_WAVE     = (100, 210, 255)
COLOR_BOSS_BAR = (200, 0, 60)
COLOR_WHITE    = (255, 255, 255)
COLOR_BLACK    = (0, 0, 0)

COLOR_POWERUP_SHIELD  = (60, 160, 255)
COLOR_POWERUP_SPREAD  = (255, 150, 30)
COLOR_POWERUP_SPEED   = (50, 230, 100)
COLOR_POWERUP_HEALTH  = (230, 50, 50)
COLOR_POWERUP_BOMB    = (200, 50, 220)
COLOR_POWERUP_OVERDRIVE = (255, 70, 220)
