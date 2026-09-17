# ==============================================================================
# VIMANA WARS — CONSOLIDATED ALL-IN-ONE PYTHON CODE ARCHIVE
# Celestial Astral Combat Arcade Edition
# Contains all original Python modules, entities, systems, UI, views, and backend.
# ==============================================================================

# Total Consolidated Modules: 77

# ── TABLE OF CONTENTS ──────────────────────────────────────────────
# 01. constants.py
# 02. main.py
# 03. build_exe.py
# 04. game/__init__.py
# 05. game/window.py
# 06. game/entities/__init__.py
# 07. game/entities/bullet.py
# 08. game/entities/chakram.py
# 09. game/entities/player.py
# 10. game/entities/powerup.py
# 11. game/entities/ship_classes.py
# 12. game/entities/enemies/__init__.py
# 13. game/entities/enemies/asura_fast.py
# 14. game/entities/enemies/asura_healer.py
# 15. game/entities/enemies/asura_kamikaze.py
# 16. game/entities/enemies/asura_ranged.py
# 17. game/entities/enemies/asura_sniper.py
# 18. game/entities/enemies/asura_tank.py
# 19. game/entities/enemies/base_enemy.py
# 20. game/entities/enemies/boss_hiranyakashipu.py
# 21. game/entities/enemies/boss_kumbhakarna.py
# 22. game/entities/enemies/boss_mahishasura.py
# 23. game/entities/enemies/boss_ravana.py
# 24. game/entities/enemies/boss_vritra.py
# 25. game/systems/__init__.py
# 26. game/systems/achievement_system.py
# 27. game/systems/asset_manager.py
# 28. game/systems/audio_synthesizer.py
# 29. game/systems/boon_system.py
# 30. game/systems/collision.py
# 31. game/systems/duel_client.py
# 32. game/systems/environmental_hazards.py
# 33. game/systems/floating_text.py
# 34. game/systems/leaderboard_client.py
# 35. game/systems/particles.py
# 36. game/systems/save_system.py
# 37. game/systems/score_system.py
# 38. game/systems/sound_manager.py
# 39. game/systems/wave_manager.py
# 40. game/ui/__init__.py
# 41. game/ui/boss_bar.py
# 42. game/ui/button.py
# 43. game/ui/easing.py
# 44. game/ui/hud.py
# 45. game/ui/menu_button.py
# 46. game/ui/modal.py
# 47. game/ui/nav_rail.py
# 48. game/ui/parallax_bg.py
# 49. game/ui/radial_gauge.py
# 50. game/ui/transitions.py
# 51. game/ui/tween.py
# 52. game/ui/vedic_theme.py
# 53. game/views/__init__.py
# 54. game/views/account_view.py
# 55. game/views/achievements_view.py
# 56. game/views/boon_select_view.py
# 57. game/views/codex_view.py
# 58. game/views/difficulty_view.py
# 59. game/views/game_over_view.py
# 60. game/views/game_view.py
# 61. game/views/intro_video_view.py
# 62. game/views/leaderboard_view.py
# 63. game/views/loading_screen.py
# 64. game/views/menu_view.py
# 65. game/views/multiplayer_view.py
# 66. game/views/name_entry_view.py
# 67. game/views/realm_map_view.py
# 68. game/views/settings_view.py
# 69. game/views/ship_select_view.py
# 70. game/views/stats_view.py
# 71. game/views/story_briefing_view.py
# 72. game/views/victory_view.py
# 73. backend/app.py
# 74. backend/firebase_service.py
# 75. tests/test_backend.py
# 76. tests/test_entities.py
# 77. tests/test_systems.py
# ───────────────────────────────────────────────────────────────────



# ==============================================================================
# [01/77] MODULE: constants.py
# ==============================================================================
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
import os

LEADERBOARD_API_URL = os.environ.get("VIMANA_API_URL", "https://vimana-wars.onrender.com").rstrip("/")
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
    8: {
        "name": "Patala Depths",
        "subtitle": "The Serpent Kingdom Below",
        "waves": (21, 22, 23),
        "bg_color": (3, 12, 18),
        "nebula_palette": [(0, 60, 50), (10, 80, 40), (0, 100, 60)],
        "accent_color": (60, 255, 180),
    },
    9: {
        "name": "Brahmaloka Summit",
        "subtitle": "The Creator's Divine Citadel",
        "waves": (24, 25, 26),
        "bg_color": (20, 18, 30),
        "nebula_palette": [(80, 60, 120), (100, 80, 140), (60, 40, 100)],
        "accent_color": (200, 170, 255),
    },
    10: {
        "name": "Vaikuntha Gate",
        "subtitle": "The Eternal Threshold of Vishnu",
        "waves": (27, 28, 29, 30),
        "bg_color": (10, 5, 20),
        "nebula_palette": [(80, 20, 80), (100, 10, 60), (120, 30, 100)],
        "accent_color": (255, 150, 255),
    },
}

def get_realm_for_wave(wave_num: int) -> dict:
    effective_wave = ((wave_num - 1) % 30) + 1
    if effective_wave <= 3:   return REALMS[1]
    elif effective_wave <= 6: return REALMS[2]
    elif effective_wave <= 9: return REALMS[3]
    elif effective_wave <= 12: return REALMS[4]
    elif effective_wave <= 15: return REALMS[5]
    elif effective_wave <= 18: return REALMS[6]
    elif effective_wave <= 20: return REALMS[7]
    elif effective_wave <= 23: return REALMS[8]
    elif effective_wave <= 26: return REALMS[9]
    return REALMS[10]


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
CAMPAIGN_FINAL_WAVE = 30
CAMPAIGN_BOSS_WAVES = (10, 20, 30)
CAMPAIGN_MINI_BOSS_WAVES = (5, 15, 25)
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


# ==============================================================================
# [02/77] MODULE: main.py
# ==============================================================================
"""
Vimana Wars — main entry point
Run this file to start the game.
"""
import arcade
from game.window import create_window


def main():
    create_window()
    arcade.run()


if __name__ == "__main__":
    main()


# ==============================================================================
# [03/77] MODULE: build_exe.py
# ==============================================================================
"""
build_exe.py
Automated script to bundle Vimana Wars into a standalone Windows/Mac/Linux executable.
Ready for publishing on itch.io or Steam.

Usage:
  python build_exe.py
"""
import os
import subprocess
import sys
from pathlib import Path


def build():
    print("==================================================")
    print("   Vimana Wars — Standalone Executable Builder    ")
    print("==================================================")

    # Check if pyinstaller is installed
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("\nInstalling PyInstaller in virtualenv...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    dist_dir = Path("dist")
    sep = os.pathsep

    # Command arguments for PyInstaller
    # Bundles assets, sounds, fonts, and dependencies into a clean release folder
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onedir",             # directory distribution (fast startup, easy modding)
        "--windowed",           # hide black console window
        "--name=VimanaWars",
        f"--add-data=assets{sep}assets",
        f"--add-data=constants.py{sep}.",
        f"--add-data=CREDITS.md{sep}.",
        f"--add-data=README.md{sep}.",
        f"--add-data=vimana_wars_pv_final.mp4{sep}.",
        "--collect-all=cv2",
        "main.py",
    ]

    print(f"\nRunning PyInstaller build command:\n{' '.join(cmd)}\n")
    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("🎉 BUILD SUCCESSFUL!")
        print("Your game executable is ready in:")
        print(f"  {dist_dir.resolve() / 'VimanaWars'}")
        print("To test: run dist/VimanaWars/VimanaWars.exe")
        print("To publish: zip the 'dist/VimanaWars' folder and upload to itch.io!")
        print("=" * 50)
    else:
        print("\n❌ Build failed. Please check error logs above.")


if __name__ == "__main__":
    build()


# ==============================================================================
# [04/77] MODULE: game/__init__.py
# ==============================================================================
# game/__init__.py


# ==============================================================================
# [05/77] MODULE: game/window.py
# ==============================================================================
"""Window creation and logical-resolution handling for Vimana Wars."""
import arcade
from pyglet.math import Mat4
from constants import WIDTH, HEIGHT, SCREEN_TITLE
from game.systems import save_system


class VimanaWindow(arcade.Window):
    """Arcade window that keeps the game's 900x600 layout in fullscreen.

    The game coordinates are intentionally designed around WIDTH/HEIGHT.
    Arcade changes the physical window size when entering fullscreen, so we
    use a centered, aspect-preserving viewport and a fixed logical projection.
    Mouse events are converted back into those logical coordinates before
    views receive them.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from pyglet.window import key, mouse
        self.keyboard = key.KeyStateHandler()
        self.mouse = mouse.MouseStateHandler()
        self.push_handlers(self.keyboard, self.mouse)

    def _apply_logical_viewport(self) -> None:
        physical_w = max(1, int(self.width))
        physical_h = max(1, int(self.height))
        scale = max(0.001, min(physical_w / WIDTH, physical_h / HEIGHT))
        view_w = max(1, int(WIDTH * scale))
        view_h = max(1, int(HEIGHT * scale))
        offset_x = (physical_w - view_w) // 2
        offset_y = (physical_h - view_h) // 2

        # Keep all existing draw code in the game's logical coordinate space.
        self.viewport = (offset_x, offset_y, view_w, view_h)
        self.projection = Mat4.orthogonal_projection(
            0, WIDTH, 0, HEIGHT, -1, 1
        )
        self._logical_scale = scale
        self._logical_offset = (offset_x, offset_y)

    def show_view(self, new_view) -> None:
        super().show_view(new_view)
        self._apply_logical_viewport()

    def on_resize(self, width: int, height: int) -> None:
        self._apply_logical_viewport()

    def _logical_point(self, x: float, y: float) -> tuple[float, float]:
        scale = getattr(self, "_logical_scale", 1.0)
        if scale <= 0:
            scale = 1.0
        offset_x, offset_y = getattr(self, "_logical_offset", (0, 0))
        return ((x - offset_x) / scale, (y - offset_y) / scale)

    def dispatch_event(self, event_type, *args):
        """Translate pointer events from physical pixels to game pixels."""
        scale = getattr(self, "_logical_scale", 1.0)
        if scale <= 0:
            scale = 1.0
        if event_type in ("on_mouse_motion", "on_mouse_drag") and len(args) >= 4:
            x, y = self._logical_point(args[0], args[1])
            args = (x, y, args[2] / scale, args[3] / scale, *args[4:])
        elif event_type in ("on_mouse_press", "on_mouse_release") and len(args) >= 2:
            x, y = self._logical_point(args[0], args[1])
            args = (x, y, *args[2:])
        return super().dispatch_event(event_type, *args)


def load_game_fonts() -> None:
    """Load bundled OFL fonts (Cinzel, Space Grotesk, JetBrains Mono) if available."""
    from pathlib import Path
    fonts_dir = Path(__file__).resolve().parent.parent / "assets" / "fonts"
    if not fonts_dir.exists():
        fonts_dir = Path(__file__).resolve().parent.parent.parent / "assets" / "fonts"
    if fonts_dir.exists():
        for font_file in fonts_dir.glob("*.ttf"):
            try:
                arcade.load_font(str(font_file))
            except Exception:
                pass


def create_window() -> arcade.Window:
    load_game_fonts()
    saved = save_system.load()
    fullscreen = bool(saved.get("fullscreen", False))
    window = VimanaWindow(
        WIDTH, HEIGHT, SCREEN_TITLE,
        fullscreen=fullscreen,
        resizable=True,
        center_window=not fullscreen,
    )
    from game.views.intro_video_view import IntroVideoView
    window.show_view(IntroVideoView())
    return window


# ==============================================================================
# [06/77] MODULE: game/entities/__init__.py
# ==============================================================================
# game/entities/__init__.py


# ==============================================================================
# [07/77] MODULE: game/entities/bullet.py
# ==============================================================================
"""
game/entities/bullet.py
Player and enemy projectiles with delta_time frame-rate independent movement,
muzzle flash support, and glowing trailing particle tails.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    PLAYER_BULLET_SPEED, PLAYER_BULLET_RADIUS, PLAYER_BULLET_DAMAGE,
    ENEMY_BULLET_SPEED, ENEMY_BULLET_RADIUS, ENEMY_BULLET_DAMAGE,
    COLOR_BULLET_PLAYER, COLOR_BULLET_ENEMY,
)


class PlayerBullet:
    """Fired by the player vimana, travels with glowing energy trail."""

    def __init__(self, x: float, y: float, angle: float, speed: float = PLAYER_BULLET_SPEED,
                 damage: int = PLAYER_BULLET_DAMAGE, radius: float = PLAYER_BULLET_RADIUS,
                 color: tuple = COLOR_BULLET_PLAYER, is_piercing: bool = False):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = radius
        self.damage = damage
        self.color = color
        self.is_piercing = is_piercing
        self.alive = True
        self.trail: list[tuple[float, float, float]] = []  # [(x, y, alpha)]
        self.pierce_count = 0

    def update(self, delta_time: float) -> None:
        step = self.speed * 60.0 * delta_time
        rad = math.radians(self.angle)

        # Store trail position
        self.trail.append((self.x, self.y, 220))
        if len(self.trail) > 5:
            self.trail.pop(0)

        self.x += math.cos(rad) * step
        self.y += math.sin(rad) * step

        # Age trails
        self.trail = [(tx, ty, max(0, a - int(500 * delta_time))) for tx, ty, a in self.trail if a > 10]

        if not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
            self.alive = False

    def draw(self) -> None:
        r, g, b = self.color[:3]
        # Draw fading energy trail
        for tx, ty, alpha in self.trail:
            arcade.draw_circle_filled(tx, ty, self.radius * 0.75, (r, g, b, alpha // 2))

        # Core
        arcade.draw_circle_filled(self.x, self.y, self.radius, (255, 255, 255))
        arcade.draw_circle_filled(self.x, self.y, self.radius * 0.8, self.color)
        # Glow halo
        arcade.draw_circle_filled(self.x, self.y, self.radius + 3, (r, g, b, 70))


class EnemyBullet:
    """Fired by enemies and bosses, aimed at the player with crimson trails."""

    def __init__(self, x: float, y: float, angle: float, speed: float = ENEMY_BULLET_SPEED,
                 damage: int = ENEMY_BULLET_DAMAGE, radius: float = ENEMY_BULLET_RADIUS,
                 color: tuple = COLOR_BULLET_ENEMY):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.radius = radius
        self.damage = damage
        self.color = color
        self.alive = True
        self.trail: list[tuple[float, float, float]] = []

    def update(self, delta_time: float) -> None:
        step = self.speed * 60.0 * delta_time
        rad = math.radians(self.angle)

        self.trail.append((self.x, self.y, 200))
        if len(self.trail) > 4:
            self.trail.pop(0)

        self.x += math.cos(rad) * step
        self.y += math.sin(rad) * step

        self.trail = [(tx, ty, max(0, a - int(600 * delta_time))) for tx, ty, a in self.trail if a > 10]

        if not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
            self.alive = False

    def draw(self) -> None:
        r, g, b = self.color[:3]
        for tx, ty, alpha in self.trail:
            arcade.draw_circle_filled(tx, ty, self.radius * 0.65, (r, g, b, alpha // 2))

        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        arcade.draw_circle_filled(self.x, self.y, self.radius + 2, (r, g, b, 90))


# ==============================================================================
# [08/77] MODULE: game/entities/chakram.py
# ==============================================================================
"""
game/entities/chakram.py
Sudarshana Chakram — Spinning divine razor blade ability.
Flies outwards in facing direction, deflects enemy bullets, slices enemies, and returns to player.
"""
import math
import arcade
from constants import WIDTH, HEIGHT


class Chakram:
    def __init__(self, start_x: float, start_y: float, angle_deg: float):
        self.x = start_x
        self.y = start_y
        self.radius = 16
        self.damage = 55
        self.alive = True
        self.angle_deg = angle_deg
        self.spin_angle = 0.0

        # Flight dynamics: Outward phase -> Return phase
        self._state = "OUTWARD"
        self._speed = 12.0
        self._distance_traveled = 0.0
        self._max_distance = 280.0
        self._hit_cooldowns: dict = {}  # enemy_id -> cooldown

    def update(self, delta_time: float, player_x: float, player_y: float) -> None:
        self.spin_angle += 720.0 * delta_time  # 2 full rotations per second

        # Decrement hit cooldowns so it doesn't hit 60 times a second on the same enemy
        for eid in list(self._hit_cooldowns.keys()):
            self._hit_cooldowns[eid] -= delta_time
            if self._hit_cooldowns[eid] <= 0:
                del self._hit_cooldowns[eid]

        speed_step = self._speed * 60.0 * delta_time

        if self._state == "OUTWARD":
            rad = math.radians(self.angle_deg)
            self.x += math.cos(rad) * speed_step
            self.y += math.sin(rad) * speed_step
            self._distance_traveled += speed_step

            if self._distance_traveled >= self._max_distance or not (0 < self.x < WIDTH and 0 < self.y < HEIGHT):
                self._state = "RETURNING"

        elif self._state == "RETURNING":
            dx = player_x - self.x
            dy = player_y - self.y
            dist = math.hypot(dx, dy)

            if dist < 22:
                self.alive = False  # Caught back by player!
                return

            return_speed_step = 14.0 * 60.0 * delta_time
            self.x += (dx / dist) * return_speed_step
            self.y += (dy / dist) * return_speed_step

    def can_damage(self, enemy) -> bool:
        eid = id(enemy)
        if eid in self._hit_cooldowns:
            return False
        self._hit_cooldowns[eid] = 0.25  # 250ms hit cooldown per enemy
        return True

    def draw(self) -> None:
        # Golden core
        arcade.draw_circle_filled(self.x, self.y, self.radius, (255, 220, 50))
        arcade.draw_circle_filled(self.x, self.y, self.radius * 0.45, (255, 255, 255))

        # Spinning razor teeth (8 blades)
        for i in range(8):
            rad = math.radians(self.spin_angle + i * 45)
            tx = self.x + math.cos(rad) * (self.radius + 6)
            ty = self.y + math.sin(rad) * (self.radius + 6)
            arcade.draw_triangle_filled(
                self.x, self.y,
                tx, ty,
                self.x + math.cos(rad + 0.3) * (self.radius + 2),
                self.y + math.sin(rad + 0.3) * (self.radius + 2),
                (255, 160, 20)
            )

        # Outer plasma glow
        arcade.draw_circle_outline(self.x, self.y, self.radius + 8, (255, 240, 100, 180), 2)


# ==============================================================================
# [09/77] MODULE: game/entities/player.py
# ==============================================================================
"""
game/entities/player.py
The player's Vimana — enhanced with delta_time physics, velocity smoothing,
banking lean, ship archetype stats, multiple dash charges, and combat juice.
"""
import math
import time
import arcade
from constants import (
    WIDTH, HEIGHT,
    PLAYER_MAX_HP, PLAYER_RADIUS,
    PLAYER_INVINCIBILITY_TIME, SHIELD_MAX_HITS, HEALTH_RESTORE,
    COLOR_SHIELD, COLOR_WHITE,
)
from game.systems.asset_manager import AssetManager


class Player:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = 0.0
        self.vy = 0.0
        self.angle = 0.0
        self.bank_tilt = 0.0
        self.radius = PLAYER_RADIUS
        self.hp = PLAYER_MAX_HP
        self.max_hp = PLAYER_MAX_HP
        self.alive = True

        # Ship class & difficulty tunings
        self.speed_stat = 320.0       # pixels / second
        self.fire_rate_stat = 0.15    # seconds per shot
        self.dash_charges_max = 1
        self.dash_charges = 1
        self.dash_cooldown_max = 2.2
        self.dash_cooldown_timer = 0.0
        self.dmg_taken_mult = 1.0     # Scaled by difficulty setting

        # Input
        self.keys_pressed: set = set()
        self.mouse_x = WIDTH / 2
        self.mouse_y = HEIGHT / 2
        self.mouse_held = False
        self.joy_dx = 0.0
        self.joy_dy = 0.0
        self.joy_aim_angle: float | None = None

        # Shooting & Recoil
        self._shoot_timer = 0.0
        self._recoil_dist = 0.0
        self.muzzle_flash_timer = 0.0

        # Dash state
        self.is_dashing = False
        self._dash_duration = 0.0
        self._dash_vx = 0.0
        self._dash_vy = 0.0
        self.afterimages: list[dict] = []

        # Ability 2 (Chakram)
        self.chakram_cooldown_max = 6.0
        self.chakram_cooldown_timer = 0.0

        # I-frames & flash
        self.invincible_timer = 0.0
        self._flash_timer = 0.0

        # Power-up state
        self.active_powerup = None
        self.shield_hits = 0
        self.spread_active = False
        self.speed_boosted = False
        self.overdrive_active = False
        self.bomb_count = 0

        # Stats
        self.enemies_killed = 0
        self.total_score = 0
        self.sprite_name = "pushpaka.png"
        self.texture = AssetManager.texture(self.sprite_name)

    def reset_input_state(self) -> None:
        """Release all transient controls when changing overlays/views.

        Arcade can change the active view while a key, mouse button, or
        joystick axis is still physically held.  In that case the matching
        release event may be delivered to the new view, leaving the player
        moving or firing forever.  Treat every view transition as a fresh
        input boundary.
        """
        self.keys_pressed.clear()
        self.mouse_held = False
        self.joy_dx = 0.0
        self.joy_dy = 0.0
        self.joy_aim_angle = None
        self.vx = 0.0
        self.vy = 0.0
        self.is_dashing = False
        self._dash_duration = 0.0
        self._dash_vx = 0.0
        self._dash_vy = 0.0
        self._shoot_timer = 0.0

    def apply_ship_class(self, sdata: dict) -> None:
        self.max_hp = sdata["hp"]
        self.hp = self.max_hp
        self.speed_stat = sdata["speed"] * 60.0
        self.fire_rate_stat = sdata["fire_rate"]
        self.dash_cooldown_max = sdata["dash_cooldown"]
        if sdata["id"] == "garuda":
            self.dash_charges_max = 2
            self.dash_charges = 2
        else:
            self.dash_charges_max = 1
            self.dash_charges = 1
        self.sprite_name = sdata.get("sprite", "pushpaka.png")
        self.texture = AssetManager.texture(self.sprite_name)

    # ── Per-frame update with delta_time physics ─────────────────────────

    def update(self, delta_time: float, keyboard_state=None) -> None:
        if not self.alive:
            return

        self._update_movement(delta_time, keyboard_state=keyboard_state)
        self._update_aim()
        self._update_timers(delta_time)
        self._update_afterimages(delta_time)

    def _update_movement(self, delta_time: float, keyboard_state=None) -> None:
        # Dash state physics
        if self.is_dashing:
            self.x += self._dash_vx * delta_time
            self.y += self._dash_vy * delta_time
            self._dash_duration -= delta_time

            self.afterimages.append({
                "x": self.x, "y": self.y, "angle": self.angle, "life": 0.22, "max_life": 0.22
            })

            if self._dash_duration <= 0:
                self.is_dashing = False

            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
            return

        # Target input direction
        inp_x, inp_y = 0.0, 0.0
        k = self.keys_pressed
        
        def _is_down(key):
            if key in k:
                return True
            if keyboard_state:
                try:
                    return bool(keyboard_state[key])
                except Exception:
                    pass
            return False

        if _is_down(arcade.key.W) or _is_down(arcade.key.UP):    inp_y += 1
        if _is_down(arcade.key.S) or _is_down(arcade.key.DOWN):  inp_y -= 1
        if _is_down(arcade.key.A) or _is_down(arcade.key.LEFT):  inp_x -= 1
        if _is_down(arcade.key.D) or _is_down(arcade.key.RIGHT): inp_x += 1

        if abs(self.joy_dx) > 0.15: inp_x += self.joy_dx
        if abs(self.joy_dy) > 0.15: inp_y += self.joy_dy

        length = math.hypot(inp_x, inp_y)
        if length > 1.0:
            inp_x /= length
            inp_y /= length

        target_speed = self.speed_stat * (1.5 if self.speed_boosted else 1.0)
        target_vx = inp_x * target_speed
        target_vy = inp_y * target_speed

        # Smooth acceleration and drag
        accel = 16.0
        self.vx += (target_vx - self.vx) * min(1.0, accel * delta_time)
        self.vy += (target_vy - self.vy) * min(1.0, accel * delta_time)

        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        # Bank lean smoothing
        target_tilt = -self.vx * 0.06
        self.bank_tilt += (target_tilt - self.bank_tilt) * min(1.0, 12.0 * delta_time)

        # Screen clamp
        self.x = max(self.radius, min(WIDTH  - self.radius, self.x))
        self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def _update_aim(self) -> None:
        if self.joy_aim_angle is not None:
            self.angle = self.joy_aim_angle
        else:
            dx = self.mouse_x - self.x
            dy = self.mouse_y - self.y
            if abs(dx) > 0.1 or abs(dy) > 0.1:
                self.angle = math.degrees(math.atan2(dy, dx))

    def _update_timers(self, delta_time: float) -> None:
        if self._shoot_timer > 0:
            self._shoot_timer -= delta_time
        if self.muzzle_flash_timer > 0:
            self.muzzle_flash_timer -= delta_time

        # Dash charge recharge
        if self.dash_charges < self.dash_charges_max:
            self.dash_cooldown_timer -= delta_time
            if self.dash_cooldown_timer <= 0:
                self.dash_charges += 1
                if self.dash_charges < self.dash_charges_max:
                    self.dash_cooldown_timer = self.dash_cooldown_max
                else:
                    self.dash_cooldown_timer = 0.0

        if self.chakram_cooldown_timer > 0:
            self.chakram_cooldown_timer -= delta_time
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time
        if self._flash_timer > 0:
            self._flash_timer -= delta_time
        if self._recoil_dist > 0:
            self._recoil_dist = max(0.0, self._recoil_dist - delta_time * 28)

        if self.active_powerup:
            self.active_powerup.update(delta_time)
            if self.active_powerup.expired:
                self._expire_powerup()

    def _update_afterimages(self, delta_time: float) -> None:
        for ghost in self.afterimages:
            ghost["life"] -= delta_time
        self.afterimages = [g for g in self.afterimages if g["life"] > 0]

    # ── Active Abilities ─────────────────────────────────────────────────

    def trigger_dash(self) -> bool:
        if self.dash_charges <= 0 or not self.alive:
            return False

        self.dash_charges -= 1
        if self.dash_cooldown_timer <= 0:
            self.dash_cooldown_timer = self.dash_cooldown_max

        self.is_dashing = True
        self._dash_duration = 0.22
        self.invincible_timer = 0.28

        # Direction from velocity or facing angle
        dx, dy = self.vx, self.vy
        if math.hypot(dx, dy) < 10:
            rad = math.radians(self.angle)
            dx = math.cos(rad)
            dy = math.sin(rad)

        dist = math.hypot(dx, dy)
        dash_speed = 780.0
        self._dash_vx = (dx / dist) * dash_speed
        self._dash_vy = (dy / dist) * dash_speed
        return True

    def trigger_chakram(self) -> bool:
        if self.chakram_cooldown_timer > 0 or not self.alive:
            return False
        self.chakram_cooldown_timer = self.chakram_cooldown_max
        return True

    @property
    def dash_ready(self) -> bool:
        return self.dash_charges > 0

    @property
    def dash_ratio(self) -> float:
        if self.dash_charges == self.dash_charges_max:
            return 1.0
        return max(0.0, 1.0 - (self.dash_cooldown_timer / self.dash_cooldown_max))

    @property
    def chakram_ready(self) -> bool:
        return self.chakram_cooldown_timer <= 0

    @property
    def chakram_ratio(self) -> float:
        return max(0.0, 1.0 - (self.chakram_cooldown_timer / self.chakram_cooldown_max))

    # ── Shooting ─────────────────────────────────────────────────────────

    def get_bullets_to_fire(self) -> list:
        if not self.mouse_held or self._shoot_timer > 0 or not self.alive or self.is_dashing:
            return []

        self._shoot_timer = self.fire_rate_stat * (0.55 if self.overdrive_active else 1.0)
        self._recoil_dist = 4.0
        self.muzzle_flash_timer = 0.06

        if self.spread_active:
            return [self.angle - 15.0, self.angle, self.angle + 15.0]
        return [self.angle]

    # ── Damage & Healing ─────────────────────────────────────────────────

    def take_damage(self, amount: int) -> bool:
        if not self.alive or self.invincible_timer > 0:
            return False

        if self.shield_hits > 0:
            self.shield_hits -= 1
            self.invincible_timer = 0.25
            if self.shield_hits == 0 and self.active_powerup:
                self._expire_powerup()
            return False

        effective_damage = max(1, int(amount * self.dmg_taken_mult))
        self.hp -= effective_damage
        self._flash_timer = 0.12
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME

        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        return True

    def heal(self, amount: int) -> None:
        self.hp = min(self.max_hp, self.hp + amount)

    # ── Power-ups ────────────────────────────────────────────────────────

    def apply_powerup(self, ptype) -> None:
        from game.entities.powerup import PowerUpType, PowerUpEffect

        if ptype == PowerUpType.HEALTH:
            self.heal(HEALTH_RESTORE)
            return
        if ptype == PowerUpType.BOMB:
            self.bomb_count += 1
            return

        if self.active_powerup and not self.active_powerup.expired:
            self._expire_powerup()

        self.active_powerup = PowerUpEffect(ptype)
        if ptype == PowerUpType.SHIELD:
            self.shield_hits = SHIELD_MAX_HITS
        elif ptype == PowerUpType.SPREAD:
            self.spread_active = True
        elif ptype == PowerUpType.SPEED:
            self.speed_boosted = True
        elif ptype == PowerUpType.OVERDRIVE:
            self.overdrive_active = True

    def _expire_powerup(self) -> None:
        from game.entities.powerup import PowerUpType
        if self.active_powerup:
            t = self.active_powerup.type
            if t == PowerUpType.SHIELD:
                self.shield_hits = 0
            elif t == PowerUpType.SPREAD:
                self.spread_active = False
            elif t == PowerUpType.SPEED:
                self.speed_boosted = False
            elif t == PowerUpType.OVERDRIVE:
                self.overdrive_active = False
        self.active_powerup = None

    def use_bomb(self) -> bool:
        if self.bomb_count > 0:
            self.bomb_count -= 1
            return True
        return False

    # ── Render with Muzzle Flash & Dynamic Exhaust ───────────────────────

    def draw(self) -> None:
        if not self.alive:
            return

        # 1. Afterimage ghost trails
        for ghost in self.afterimages:
            g_alpha = int(130 * (ghost["life"] / ghost["max_life"]))
            self._draw_ship_body(ghost["x"], ghost["y"], ghost["angle"], (100, 200, 255, g_alpha))

        # 2. Blink during i-frames
        if self.invincible_timer > 0 and self._flash_timer <= 0 and not self.is_dashing:
            if int(time.time() * 12) % 2 == 0:
                return

        # 3. Position with recoil
        rad = math.radians(self.angle)
        draw_x = self.x - math.cos(rad) * self._recoil_dist
        draw_y = self.y - math.sin(rad) * self._recoil_dist

        color = COLOR_WHITE if self._flash_timer > 0 else (255, 215, 80) if self.spread_active else (210, 225, 255)
        self._draw_ship_body(draw_x, draw_y, self.angle + self.bank_tilt, color)

        # 4. Muzzle Flash on gun tip
        if self.muzzle_flash_timer > 0:
            tip_x = self.x + math.cos(rad) * (self.radius + 16)
            tip_y = self.y + math.sin(rad) * (self.radius + 16)
            arcade.draw_circle_filled(tip_x, tip_y, 7, (255, 240, 150))
            arcade.draw_circle_filled(tip_x, tip_y, 4, (255, 255, 255))

        # 5. Shield aura
        if self.shield_hits > 0:
            arcade.draw_circle_outline(self.x, self.y, self.radius + 12, COLOR_SHIELD, 2)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 12, (60, 160, 255, 35))

        # Overdrive reads as a hot-pink energy ring while active, making the
        # temporary fire-rate boost obvious without covering the ship.
        if self.overdrive_active:
            pulse = 1.0 + 0.12 * math.sin(time.time() * 12.0)
            arcade.draw_circle_outline(self.x, self.y, (self.radius + 15) * pulse,
                                       (255, 70, 220, 210), 2)

    def _draw_ship_body(self, sx: float, sy: float, angle_deg: float, main_color: tuple) -> None:
        if AssetManager.draw(self.texture, sx, sy, self.radius * 3.0,
                             self.radius * 3.0, angle=angle_deg - 90):
            return
        r = self.radius
        angle_rad = math.radians(angle_deg)

        # Main Forward Nose
        tip_x = sx + math.cos(angle_rad) * r * 1.9
        tip_y = sy + math.sin(angle_rad) * r * 1.9

        # Swept-Back Wings
        wing_l_rad = angle_rad + math.radians(140)
        wing_r_rad = angle_rad - math.radians(140)
        wing_l_x = sx + math.cos(wing_l_rad) * r * 1.3
        wing_l_y = sy + math.sin(wing_l_rad) * r * 1.3
        wing_r_x = sx + math.cos(wing_r_rad) * r * 1.3
        wing_r_y = sy + math.sin(wing_r_rad) * r * 1.3

        # Inner Chassis
        arcade.draw_triangle_filled(tip_x, tip_y, wing_l_x, wing_l_y, wing_r_x, wing_r_y, main_color)
        arcade.draw_line(tip_x, tip_y, wing_l_x, wing_l_y, (255, 215, 60), 2)
        arcade.draw_line(tip_x, tip_y, wing_r_x, wing_r_y, (255, 215, 60), 2)

        # Cockpit Canopy
        cockpit_x = sx + math.cos(angle_rad) * r * 0.5
        cockpit_y = sy + math.sin(angle_rad) * r * 0.5
        arcade.draw_circle_filled(cockpit_x, cockpit_y, 4.5, (100, 240, 255))
        arcade.draw_circle_filled(cockpit_x, cockpit_y, 2.5, (255, 255, 255))

        # Dynamic Dual Plasma Thrusters
        rear_l_rad = angle_rad + math.radians(165)
        rear_r_rad = angle_rad - math.radians(165)
        t_l_x = sx + math.cos(rear_l_rad) * r * 0.7
        t_l_y = sy + math.sin(rear_l_rad) * r * 0.7
        t_r_x = sx + math.cos(rear_r_rad) * r * 0.7
        t_r_y = sy + math.sin(rear_r_rad) * r * 0.7

        cur_speed_len = math.hypot(self.vx, self.vy)
        flame_len = 5 + (cur_speed_len / 400.0) * 8
        thruster_col = (255, 160, 40) if self.speed_boosted or self.is_dashing else (100, 180, 255)

        # Jet flares
        jet_rad = angle_rad + math.pi
        arcade.draw_line(t_l_x, t_l_y, t_l_x + math.cos(jet_rad) * flame_len, t_l_y + math.sin(jet_rad) * flame_len, thruster_col, 3)
        arcade.draw_line(t_r_x, t_r_y, t_r_x + math.cos(jet_rad) * flame_len, t_r_y + math.sin(jet_rad) * flame_len, thruster_col, 3)
        arcade.draw_circle_filled(t_l_x, t_l_y, 3.5, (255, 255, 255))
        arcade.draw_circle_filled(t_r_x, t_r_y, 3.5, (255, 255, 255))


# ==============================================================================
# [10/77] MODULE: game/entities/powerup.py
# ==============================================================================
"""
game/entities/powerup.py
Collectables that spawn on the map and give the player timed or instant effects.
"""
import math
import random
import arcade
from enum import Enum, auto
from constants import (
    WIDTH, HEIGHT,
    POWERUP_RADIUS,
    SHIELD_DURATION, SPREAD_DURATION, SPEED_DURATION,
    COLOR_POWERUP_SHIELD, COLOR_POWERUP_SPREAD, COLOR_POWERUP_SPEED,
    COLOR_POWERUP_HEALTH, COLOR_POWERUP_BOMB, COLOR_POWERUP_OVERDRIVE,
    COLOR_WHITE,
)


class PowerUpType(Enum):
    SHIELD = auto()   # Kavach  — absorbs 3 hits for 10s
    SPREAD = auto()   # Agneyastra — 3-bullet spread for 8s
    SPEED  = auto()   # Vayavyastra — +60% speed for 6s
    HEALTH = auto()   # Amrita — instant +30 HP
    BOMB   = auto()   # Brahmastra — clear all enemies on screen
    OVERDRIVE = auto()  # Astra Overdrive — rapid fire for 8s


# Duration in seconds for each timed type (instant types use 0)
_DURATIONS = {
    PowerUpType.SHIELD: SHIELD_DURATION,
    PowerUpType.SPREAD: SPREAD_DURATION,
    PowerUpType.SPEED:  SPEED_DURATION,
    PowerUpType.HEALTH: 0.0,
    PowerUpType.BOMB:   0.0,
    PowerUpType.OVERDRIVE: 8.0,
}

_COLORS = {
    PowerUpType.SHIELD: COLOR_POWERUP_SHIELD,
    PowerUpType.SPREAD: COLOR_POWERUP_SPREAD,
    PowerUpType.SPEED:  COLOR_POWERUP_SPEED,
    PowerUpType.HEALTH: COLOR_POWERUP_HEALTH,
    PowerUpType.BOMB:   COLOR_POWERUP_BOMB,
    PowerUpType.OVERDRIVE: COLOR_POWERUP_OVERDRIVE,
}

_LABELS = {
    PowerUpType.SHIELD: "KVH",   # Kavach
    PowerUpType.SPREAD: "AGN",   # Agneyastra
    PowerUpType.SPEED:  "VAY",   # Vayavyastra
    PowerUpType.HEALTH: "AMR",   # Amrita
    PowerUpType.BOMB:   "BRM",   # Brahmastra
    PowerUpType.OVERDRIVE: "OVR",  # Astra Overdrive
}


class PowerUpEffect:
    """
    Tracks a timed power-up effect that is active on the player.
    Instant effects (HEALTH, BOMB) should never be stored here.
    """
    def __init__(self, ptype: PowerUpType):
        self.type = ptype
        self.duration = _DURATIONS[ptype]
        self.remaining = self.duration
        self.expired = False

    def update(self, delta_time: float) -> None:
        if self.expired:
            return
        self.remaining -= delta_time
        if self.remaining <= 0:
            self.remaining = 0
            self.expired = True

    @property
    def fraction(self) -> float:
        """0.0 (expired) → 1.0 (full)"""
        if self.duration <= 0:
            return 0.0
        return max(0.0, self.remaining / self.duration)


class PowerUp:
    """
    A collectable that lives on the game map until the player touches it.
    Spawns at a random edge position, pulses visually.
    """

    def __init__(self, ptype: PowerUpType = None):
        self.type = ptype or random.choice(list(PowerUpType))
        self.radius = POWERUP_RADIUS
        self.x, self.y = self._random_position()
        self.alive = True
        self._pulse_timer = 0.0
        self._color = _COLORS[self.type]
        self._label = _LABELS[self.type]

    @staticmethod
    def _random_position():
        margin = POWERUP_RADIUS + 30
        side = random.randint(0, 3)
        if side == 0:   # top
            return random.uniform(margin, WIDTH - margin), HEIGHT - margin
        elif side == 1: # bottom
            return random.uniform(margin, WIDTH - margin), margin
        elif side == 2: # left
            return margin, random.uniform(margin, HEIGHT - margin)
        else:           # right
            return WIDTH - margin, random.uniform(margin, HEIGHT - margin)

    def update(self, delta_time: float) -> None:
        self._pulse_timer += delta_time

    def draw(self) -> None:
        r, g, b = self._color
        pulse = 0.5 + 0.5 * math.sin(self._pulse_timer * 4)

        # 1. Upward Celestial Light Beacon Beam
        beam_alpha = int(40 + 35 * pulse)
        arcade.draw_line(self.x, self.y, self.x, self.y + 100, (r, g, b, beam_alpha), 4)
        arcade.draw_line(self.x, self.y, self.x, self.y + 60, (255, 255, 255, beam_alpha + 30), 2)

        # 2. Pulsing outer glow
        glow_r = self.radius + 6 + pulse * 6
        arcade.draw_circle_filled(self.x, self.y, glow_r, (r, g, b, 60))

        # 3. Rotating Diamond Orbit Ring
        rot = self._pulse_timer * 60.0  # degrees
        for i in range(4):
            ang = math.radians(rot + i * 90)
            dx = self.x + math.cos(ang) * (self.radius + 8)
            dy = self.y + math.sin(ang) * (self.radius + 8)
            arcade.draw_circle_filled(dx, dy, 2.5, (255, 255, 255, 200))

        # 4. Rotating 3D-looking astral cube. The faces make pickups readable
        # even in a busy bullet field and give every ability a collectible,
        # game-like silhouette instead of another plain orb.
        half = self.radius * 0.72
        depth = 7.0
        front_center = (self.x, self.y)
        back_center = (self.x + depth * 0.75, self.y + depth * 0.55)
        angle = math.radians(rot)

        def diamond(center, size):
            cx, cy = center
            return [
                (cx + math.cos(angle + math.pi / 2) * size,
                 cy + math.sin(angle + math.pi / 2) * size),
                (cx + math.cos(angle) * size,
                 cy + math.sin(angle) * size),
                (cx + math.cos(angle - math.pi / 2) * size,
                 cy + math.sin(angle - math.pi / 2) * size),
                (cx + math.cos(angle + math.pi) * size,
                 cy + math.sin(angle + math.pi) * size),
            ]

        front = diamond(front_center, half)
        back = diamond(back_center, half * 0.88)
        face_colors = (
            (min(255, r + 35), min(255, g + 35), min(255, b + 35), 235),
            (max(0, r - 25), max(0, g - 25), max(0, b - 25), 235),
            (max(0, r - 45), max(0, g - 45), max(0, b - 45), 235),
            (min(255, r + 15), min(255, g + 15), min(255, b + 15), 235),
        )
        for i in range(4):
            arcade.draw_polygon_filled([front[i], front[(i + 1) % 4],
                                        back[(i + 1) % 4], back[i]], face_colors[i])
        arcade.draw_polygon_filled(front, (*self._color, 245))
        for i in range(4):
            arcade.draw_line(front[i][0], front[i][1], back[i][0], back[i][1], COLOR_WHITE, 1)
            arcade.draw_line(front[i][0], front[i][1], front[(i + 1) % 4][0], front[(i + 1) % 4][1], COLOR_WHITE, 1)

        arcade.draw_text(
            self._label,
            self.x - 12, self.y - 5,
            COLOR_WHITE,
            font_size=8,
            bold=True,
        )


# ==============================================================================
# [11/77] MODULE: game/entities/ship_classes.py
# ==============================================================================
"""
game/entities/ship_classes.py
Vimana Ship Class definitions with distinct archetypes, stats, weapons, and special traits.
Follows the authoritative Vimana Wars specification.
"""

SHIP_CLASSES = {
    "pushpaka": {
        "id": "pushpaka",
        "name": "Pushpaka Mk-I",
        "subtitle": "Celestial Carrier",
        "hp": 100,
        "speed": 5.0,
        "fire_rate": 0.15,
        "bullet_damage": 25,
        "dash_cooldown": 2.2,
        "astra_power": 75,
        "weapon": "Brahmastra Cannon",
        "ability": "Divine Barrier",
        "color": (210, 225, 255),
        "accent": (233, 196, 0),
        "sprite": "pushpaka.png",
        "unlock_wave": 0,
        "desc": "The legendary flying chariot of kings and gods gifted by Vishwakarma. A balanced, enduring flagship built for sustained campaigns across all celestial realms.",
    },
    "tripura": {
        "id": "tripura",
        "name": "Tripura Destroyer",
        "subtitle": "Siege Platform",
        "hp": 160,
        "speed": 3.8,
        "fire_rate": 0.24,
        "bullet_damage": 48,
        "dash_cooldown": 3.0,
        "astra_power": 90,
        "weapon": "Triple Agni Mortars",
        "ability": "Triple Convergence",
        "color": (255, 140, 60),
        "accent": (255, 107, 114),
        "sprite": "tripura.png",
        "unlock_wave": 0,
        "desc": "Replicates the three flying fortresses annihilated by Shiva. Unmatched frontal armor and devastating sustained fire built to break Asura dreadnought lines.",
    },
    "garuda": {
        "id": "garuda",
        "name": "Garuda Interceptor",
        "subtitle": "Aerial Assault",
        "hp": 75,
        "speed": 6.8,
        "fire_rate": 0.11,
        "bullet_damage": 18,
        "dash_cooldown": 1.4,
        "astra_power": 80,
        "weapon": "Solar Lance Array",
        "ability": "Gale Dive",
        "color": (120, 240, 255),
        "accent": (116, 245, 255),
        "sprite": "garuda.png",
        "unlock_wave": 0,
        "desc": "Modeled after the divine eagle of Vishnu. Trades durability for supreme velocity and piercing solar bolts that dissolve enemy formations before return fire.",
    },
    "vajra": {
        "id": "vajra",
        "name": "Vajra Spear",
        "subtitle": "Storm Striker",
        "hp": 110,
        "speed": 5.5,
        "fire_rate": 0.13,
        "bullet_damage": 30,
        "dash_cooldown": 1.8,
        "astra_power": 85,
        "weapon": "Thunderbolt Cannon",
        "ability": "Storm Cascade",
        "color": (255, 235, 90),
        "accent": (120, 220, 255),
        "sprite": "vajra.png",
        "unlock_wave": 5,
        "desc": "Forged from the sacrifice of Sage Dadhichi. Indra's own lightning scaled for void dogfights, rewarding forward momentum with chaining electrical arcs.",
    },
    "naga": {
        "id": "naga",
        "name": "Naga Coil",
        "subtitle": "Venom Stalker",
        "hp": 130,
        "speed": 4.5,
        "fire_rate": 0.18,
        "bullet_damage": 38,
        "dash_cooldown": 2.4,
        "astra_power": 70,
        "weapon": "Venom Torpedoes",
        "ability": "Serpent Coil",
        "color": (100, 230, 180),
        "accent": (100, 255, 180),
        "sprite": "naga.png",
        "unlock_wave": 8,
        "desc": "Engineered from the scales of the primordial serpent Vasuki. Toxic astral payload systems erode enemy shields and hold critical tactical corridors.",
    },
    "agneyastra": {
        "id": "agneyastra",
        "name": "Agneyastra",
        "subtitle": "Solar Burst Frigate",
        "hp": 90,
        "speed": 5.8,
        "fire_rate": 0.10,
        "bullet_damage": 24,
        "dash_cooldown": 1.8,
        "astra_power": 88,
        "weapon": "Solar Burst Flak",
        "ability": "Prominence Surge",
        "color": (255, 130, 50),
        "accent": (255, 120, 30),
        "sprite": "agneyastra.png",
        "unlock_wave": 10,
        "desc": "Rapid-firing solar flak built to clear dense Asura swarms before they encircle the player, leaving trails of superheated cosmic plasma.",
    },
    "soma": {
        "id": "soma",
        "name": "Soma Ark",
        "subtitle": "Support Carrier",
        "hp": 115,
        "speed": 5.2,
        "fire_rate": 0.14,
        "bullet_damage": 32,
        "dash_cooldown": 2.0,
        "astra_power": 92,
        "weapon": "Amrita Projector",
        "ability": "Lunar Renewal",
        "color": (150, 210, 255),
        "accent": (170, 80, 255),
        "sprite": "soma.png",
        "unlock_wave": 13,
        "desc": "Named for the nectar of immortality and the moon deity. Equipped with regenerative Amrita field capacitors and balanced astral defenses.",
    },
    "kubera": {
        "id": "kubera",
        "name": "Kubera Galleon",
        "subtitle": "Heavy Fortress",
        "hp": 190,
        "speed": 3.4,
        "fire_rate": 0.30,
        "bullet_damage": 65,
        "dash_cooldown": 3.4,
        "astra_power": 95,
        "weapon": "Ratna Siege Gun",
        "ability": "Fortress Mode",
        "color": (255, 190, 70),
        "accent": (233, 196, 0),
        "sprite": "kubera.png",
        "unlock_wave": 15,
        "desc": "The celestial treasury rendered as an orbital fortress. Heavy gold-plated hull plating with overwhelming single-volley kinetic yield.",
    },
    "surya": {
        "id": "surya",
        "name": "Surya Flare",
        "subtitle": "Solar Radiant",
        "hp": 85,
        "speed": 7.2,
        "fire_rate": 0.09,
        "bullet_damage": 20,
        "dash_cooldown": 1.2,
        "astra_power": 98,
        "weapon": "Solar Flare Burst",
        "ability": "Radiance Surge",
        "color": (255, 220, 80),
        "accent": (255, 215, 0),
        "sprite": "surya.png",
        "unlock_wave": 20,
        "desc": "The ultimate high-velocity strike craft: fragile, radiant, and delivering devastating point-blank bursts in the hands of master pilots.",
    },
}


# ==============================================================================
# [12/77] MODULE: game/entities/enemies/__init__.py
# ==============================================================================
# game/entities/enemies/__init__.py


# ==============================================================================
# [13/77] MODULE: game/entities/enemies/asura_fast.py
# ==============================================================================
"""
game/entities/enemies/asura_fast.py
Asura Chaser — fast, weak, beelines straight at the player.
"""
import arcade
from constants import (
    WIDTH, HEIGHT,
    ASURA_FAST_HP, ASURA_FAST_SPEED, ASURA_FAST_SCORE, ASURA_FAST_RADIUS,
    COLOR_ASURA_FAST, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraFast(BaseEnemy):
    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_FAST_HP, speed=ASURA_FAST_SPEED,
                         score_value=ASURA_FAST_SCORE, radius=ASURA_FAST_RADIUS)
        self.texture = AssetManager.texture("asura_fast.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        self._move_toward(player_x, player_y, delta_time)
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        return []   # no projectiles

    def draw(self) -> None:
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_FAST
        if self._draw_sprite(color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            self._draw_hp_bar()
            return
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        # Pupils — two small dots to give it a face
        arcade.draw_circle_filled(self.x - 4, self.y + 3, 2, COLOR_WHITE)
        arcade.draw_circle_filled(self.x + 4, self.y + 3, 2, COLOR_WHITE)
        self._draw_hp_bar()


# ==============================================================================
# [14/77] MODULE: game/entities/enemies/asura_healer.py
# ==============================================================================
"""
game/entities/enemies/asura_healer.py
Asura Healer — Priest vessel that pulses healing restorative waves to nearby damaged Asuras.
Priority target for player.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_WHITE
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraHealer(BaseEnemy):
    def __init__(self, safe_player_x: float = WIDTH / 2, safe_player_y: float = HEIGHT / 2):
        x, y = BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y, hp=45, speed=1.6, score_value=250, radius=18)
        self._heal_timer = 2.5
        self._pulse_anim = 0.0
        self.texture = AssetManager.texture("asura_healer.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        self._pulse_anim += delta_time
        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        # Stays at mid distance
        dist = math.hypot(player_x - self.x, player_y - self.y)
        if dist < 220:
            self._move_toward(self.x - (player_x - self.x), self.y - (player_y - self.y), delta_time, speed_override=self.speed * 0.8)
        else:
            self._move_toward(player_x, player_y, delta_time)

        self._heal_timer -= delta_time
        return []

    def perform_heal_pulse(self, enemies: list) -> bool:
        if self._heal_timer <= 0:
            self._heal_timer = 2.8
            for e in enemies:
                if e is not self and e.alive and math.hypot(e.x - self.x, e.y - self.y) < 180:
                    e.hp = min(e.max_hp, e.hp + 20)
            return True
        return False

    def draw(self) -> None:
        self._draw_elite_aura()
        flash = self._hit_flash > 0
        body_col = COLOR_WHITE if flash else (40, 210, 140)

        if self._draw_sprite(width=self.radius * 2.3, height=self.radius * 2.3,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            pulse_r = self.radius + 6 + math.sin(self._pulse_anim * 4) * 3
            arcade.draw_circle_outline(self.x, self.y, pulse_r, (50, 240, 150, 160), 2)
            self._draw_hp_bar()
            return

        # Emerald Core
        arcade.draw_circle_filled(self.x, self.y, self.radius, body_col)
        arcade.draw_circle_filled(self.x, self.y, self.radius * 0.5, (200, 255, 220))

        # Healing Cross Emblem
        arcade.draw_line(self.x - 7, self.y, self.x + 7, self.y, (255, 255, 255), 3)
        arcade.draw_line(self.x, self.y - 7, self.x, self.y + 7, (255, 255, 255), 3)

        # Pulsing Healing Aura Ring
        pulse_r = self.radius + 6 + math.sin(self._pulse_anim * 4) * 3
        arcade.draw_circle_outline(self.x, self.y, pulse_r, (50, 240, 150, 160), 2)
        self._draw_hp_bar()


# ==============================================================================
# [15/77] MODULE: game/entities/enemies/asura_kamikaze.py
# ==============================================================================
"""
game/entities/enemies/asura_kamikaze.py
Asura Kamikaze — tiny, very fast, explodes on contact dealing AOE damage.
Flashes faster the closer it gets to the player.
"""
import math
import arcade
from constants import (
    ASURA_KAMIKAZE_HP, ASURA_KAMIKAZE_SPEED, ASURA_KAMIKAZE_SCORE,
    ASURA_KAMIKAZE_RADIUS, ASURA_KAMIKAZE_EXPLOSION_RADIUS,
    ASURA_KAMIKAZE_EXPLOSION_DAMAGE,
    COLOR_ASURA_KAMIKAZE, COLOR_WHITE,
    WIDTH, HEIGHT,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraKamikaze(BaseEnemy):
    """
    On player contact the collision system checks self.exploded,
    which triggers AOE damage to the player and kills this enemy.
    """

    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_KAMIKAZE_HP, speed=ASURA_KAMIKAZE_SPEED,
                         score_value=ASURA_KAMIKAZE_SCORE, radius=ASURA_KAMIKAZE_RADIUS)
        self.exploded = False
        self.explosion_radius = ASURA_KAMIKAZE_EXPLOSION_RADIUS
        self.explosion_damage = ASURA_KAMIKAZE_EXPLOSION_DAMAGE
        self._flash_cycle = 0.0
        self._visible = True
        self.texture = AssetManager.texture("asura_kamikaze.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        self._move_toward(player_x, player_y, delta_time)

        # Flash rate proportional to distance — panicky near the player
        dist = math.hypot(player_x - self.x, player_y - self.y)
        flash_rate = max(3.0, 18.0 - dist * 0.06)
        self._flash_cycle += delta_time * flash_rate
        self._visible = int(self._flash_cycle) % 2 == 0

        return []

    def explode(self) -> None:
        """Call this (from collision system) to trigger the explosion."""
        self.exploded = True
        self.alive = False

    def draw(self) -> None:
        if not self._visible:
            return
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_KAMIKAZE
        if self._draw_sprite(width=self.radius * 2.2, height=self.radius * 2.2,
                             color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            return
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        # No HP bar — it dies in one hit anyway; bar would clutter the tiny sprite


# ==============================================================================
# [16/77] MODULE: game/entities/enemies/asura_ranged.py
# ==============================================================================
"""
game/entities/enemies/asura_ranged.py
Asura Shooter — keeps its distance and fires enemy bullets at the player.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    ASURA_RANGED_HP, ASURA_RANGED_SPEED, ASURA_RANGED_SCORE, ASURA_RANGED_RADIUS,
    ASURA_RANGED_FIRE_RATE, ASURA_RANGED_PREFERRED_DIST,
    COLOR_ASURA_RANGED, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class AsuraRanged(BaseEnemy):
    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_RANGED_HP, speed=ASURA_RANGED_SPEED,
                         score_value=ASURA_RANGED_SCORE, radius=ASURA_RANGED_RADIUS)
        self._fire_timer = ASURA_RANGED_FIRE_RATE  # wait before first shot
        self.texture = AssetManager.texture("asura_ranged.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        # Maintain preferred distance — move closer if too far, back off if too close
        dist = math.hypot(player_x - self.x, player_y - self.y)
        if dist < ASURA_RANGED_PREFERRED_DIST - 40:
            # Too close — strafe sideways and backwards
            angle = self._angle_to_player(player_x, player_y) + 180
            rad = math.radians(angle)
            step = self.speed * 60.0 * delta_time
            self.x += math.cos(rad) * step
            self.y += math.sin(rad) * step
        elif dist > ASURA_RANGED_PREFERRED_DIST + 40:
            self._move_toward(player_x, player_y, delta_time)

        # Fire
        self._fire_timer -= delta_time
        if self._fire_timer <= 0:
            self._fire_timer = ASURA_RANGED_FIRE_RATE
            angle = self._angle_to_player(player_x, player_y)
            return [EnemyBullet(self.x, self.y, angle)]

        return []

    def draw(self) -> None:
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_RANGED
        if self._draw_sprite(color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            self._draw_hp_bar()
            return
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        # A small 'barrel' pointing at the last known player direction
        arcade.draw_circle_filled(self.x, self.y + self.radius - 4, 4, (80, 0, 130))
        self._draw_hp_bar()


# ==============================================================================
# [17/77] MODULE: game/entities/enemies/asura_sniper.py
# ==============================================================================
"""
game/entities/enemies/asura_sniper.py
Asura Void Sniper — Keeps maximum range, paints target with a red aiming laser,
and fires an ultra-high-velocity piercing beam bullet with clear audio/visual telegraphs.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_WHITE
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class AsuraSniper(BaseEnemy):
    def __init__(self, safe_player_x: float = WIDTH / 2, safe_player_y: float = HEIGHT / 2):
        x, y = BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y, hp=40, speed=1.2, score_value=220, radius=16)
        self._charge_timer = 2.8
        self._is_aiming = False
        self._aim_angle = 0.0
        self.texture = AssetManager.texture("asura_sniper.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        # Stay at long range (~320px)
        dist = math.hypot(player_x - self.x, player_y - self.y)
        if dist < 260:
            # Back up
            self._move_toward(self.x - (player_x - self.x), self.y - (player_y - self.y), delta_time)
        elif dist > 380:
            self._move_toward(player_x, player_y, delta_time)

        self._aim_angle = self._angle_to_player(player_x, player_y)
        self._charge_timer -= delta_time

        bullets = []
        # Aiming telegraph during last 1.0s before firing
        if self._charge_timer <= 1.0:
            self._is_aiming = True

        if self._charge_timer <= 0:
            self._charge_timer = 3.0
            self._is_aiming = False
            # Fire high speed sniper beam
            b = EnemyBullet(self.x, self.y, self._aim_angle, speed=13.0, damage=22, radius=6, color=(255, 40, 90))
            bullets.append(b)

        return bullets

    def draw(self) -> None:
        self._draw_elite_aura()
        flash = self._hit_flash > 0
        body_col = COLOR_WHITE if flash else (180, 40, 100)

        # Draw red laser aiming telegraph line
        if self._is_aiming:
            rad = math.radians(self._aim_angle)
            end_x = self.x + math.cos(rad) * 600
            end_y = self.y + math.sin(rad) * 600
            arcade.draw_line(self.x, self.y, end_x, end_y, (255, 30, 70, 180), 2)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 4, (255, 60, 100, 90))

        if self._draw_sprite(width=self.radius * 2.3, height=self.radius * 2.3,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            self._draw_hp_bar()
            return

        # Diamond Sniper Chassis
        rad = math.radians(self._aim_angle)
        tip_x = self.x + math.cos(rad) * (self.radius + 10)
        tip_y = self.y + math.sin(rad) * (self.radius + 10)

        arcade.draw_circle_filled(self.x, self.y, self.radius, body_col)
        arcade.draw_line(self.x, self.y, tip_x, tip_y, (255, 80, 120), 4)
        arcade.draw_circle_filled(self.x, self.y, 4, (255, 255, 255))
        self._draw_hp_bar()


# ==============================================================================
# [18/77] MODULE: game/entities/enemies/asura_tank.py
# ==============================================================================
"""
game/entities/enemies/asura_tank.py
Asura Brute — slow, very tanky, deals heavy contact damage.
"""
import arcade
from constants import (
    WIDTH, HEIGHT,
    ASURA_TANK_HP, ASURA_TANK_SPEED, ASURA_TANK_SCORE, ASURA_TANK_RADIUS,
    ASURA_TANK_CONTACT_DAMAGE,
    COLOR_ASURA_TANK, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.systems.asset_manager import AssetManager


class AsuraTank(BaseEnemy):
    """Contact damage is higher — collision.py checks this attribute."""

    def __init__(self, start_x=None, start_y=None, safe_player_x=WIDTH / 2, safe_player_y=HEIGHT / 2):
        x, y = (start_x, start_y) if start_x is not None else BaseEnemy.spawn_at_edge(safe_player_x=safe_player_x, safe_player_y=safe_player_y)
        super().__init__(x, y,
                         hp=ASURA_TANK_HP, speed=ASURA_TANK_SPEED,
                         score_value=ASURA_TANK_SCORE, radius=ASURA_TANK_RADIUS)
        self.contact_damage = ASURA_TANK_CONTACT_DAMAGE
        self.texture = AssetManager.texture("asura_tank.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        self._move_toward(player_x, player_y, delta_time)
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        return []

    def draw(self) -> None:
        self._draw_elite_aura()
        color = COLOR_WHITE if self._hit_flash > 0 else COLOR_ASURA_TANK
        if self._draw_sprite(width=self.radius * 2.4, height=self.radius * 2.4,
                             color=COLOR_WHITE if self._hit_flash > 0 else (255, 255, 255, 255)):
            self._draw_hp_bar(bar_w=self.radius * 2.5)
            return
        # Large body
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)
        
        hp_frac = self.hp / self.max_hp
        import math

        # Spiky outline to signal tanky-ness (outer spikes break off below 50% HP)
        active_spikes = 8 if hp_frac > 0.5 else 4
        for i in range(active_spikes):
            ang = math.radians(i * (360 / active_spikes))
            sx = self.x + math.cos(ang) * (self.radius + 7)
            sy = self.y + math.sin(ang) * (self.radius + 7)
            arcade.draw_circle_filled(sx, sy, 4, COLOR_ASURA_TANK)

        # Draw glowing armor crack lines when damaged
        if hp_frac < 0.70:
            arcade.draw_line(self.x - 8, self.y + 6, self.x + 4, self.y - 2, (255, 100, 30), 2)
        if hp_frac < 0.40:
            arcade.draw_line(self.x + 4, self.y - 2, self.x + 10, self.y - 9, (255, 60, 20), 2)
            arcade.draw_line(self.x - 3, self.y - 8, self.x + 2, self.y + 7, (255, 200, 50), 2)

        self._draw_hp_bar(bar_w=self.radius * 2.5)


# ==============================================================================
# [19/77] MODULE: game/entities/enemies/base_enemy.py
# ==============================================================================
"""
game/entities/enemies/base_enemy.py
Abstract base class for all enemy types with delta_time frame-rate independence,
hit stagger physics, safe spawning algorithms, and animated HP bars.
"""
import math
import random
import arcade
from abc import ABC, abstractmethod
from constants import WIDTH, HEIGHT
from game.systems.asset_manager import AssetManager


class BaseEnemy(ABC):
    def __init__(self, x: float, y: float, hp: int, speed: float,
                 score_value: int, radius: float):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.score_value = score_value
        self.radius = radius
        self.alive = True
        self._hit_flash = 0.0
        self._stagger_vx = 0.0
        self._stagger_vy = 0.0
        self._burning = 0.0
        self.texture = None

    @abstractmethod
    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    def take_damage(self, amount: int, knockback_angle: float | None = None) -> None:
        self.hp -= amount
        self._hit_flash = 0.12
        if knockback_angle is not None:
            rad = math.radians(knockback_angle)
            self._stagger_vx += math.cos(rad) * 120.0
            self._stagger_vy += math.sin(rad) * 120.0

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def is_dead(self) -> bool:
        return not self.alive

    def _angle_to_player(self, player_x: float, player_y: float) -> float:
        dx = player_x - self.x
        dy = player_y - self.y
        return math.degrees(math.atan2(dy, dx))

    def _move_toward(self, target_x: float, target_y: float,
                     delta_time: float, speed_override: float = None) -> None:
        # Apply stagger recovery
        if abs(self._stagger_vx) > 1 or abs(self._stagger_vy) > 1:
            self.x += self._stagger_vx * delta_time
            self.y += self._stagger_vy * delta_time
            self._stagger_vx *= 0.88
            self._stagger_vy *= 0.88

        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 1:
            return
        spd = speed_override if speed_override is not None else self.speed
        step = spd * 60.0 * delta_time
        self.x += (dx / dist) * step
        self.y += (dy / dist) * step

    def _draw_hp_bar(self, bar_w: float = None, bar_h: float = 4,
                     y_offset: float = None) -> None:
        bar_w = bar_w or self.radius * 2.2
        y_offset = y_offset or self.radius + 6
        bg_x = self.x - bar_w / 2
        bg_y = self.y + y_offset
        frac = max(0.0, self.hp / self.max_hp)
        arcade.draw_lrbt_rectangle_filled(
            bg_x, bg_x + bar_w,
            bg_y, bg_y + bar_h,
            (80, 0, 0)
        )
        if frac > 0:
            color = (30, 200, 70) if frac > 0.35 else (220, 60, 0)
            arcade.draw_lrbt_rectangle_filled(
                bg_x, bg_x + bar_w * frac,
                bg_y, bg_y + bar_h,
                color
            )

    def _draw_sprite(self, width: float = None, height: float = None,
                     angle: float = 0.0,
                     color=(255, 255, 255, 255)) -> bool:
        width = width or self.radius * 2.2
        height = height or self.radius * 2.2
        return AssetManager.draw(self.texture, self.x, self.y, width, height,
                                 angle=angle, color=color)

    def _draw_elite_aura(self) -> None:
        if getattr(self, "is_elite", False):
            import time
            rot = time.time() * 90.0  # 90 degrees/sec
            arcade.draw_circle_outline(self.x, self.y, self.radius + 6, (255, 215, 0), 2)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 6, (255, 200, 0, 45))
            for i in range(4):
                rad = math.radians(rot + i * 90)
                px = self.x + math.cos(rad) * (self.radius + 9)
                py = self.y + math.sin(rad) * (self.radius + 9)
                arcade.draw_circle_filled(px, py, 3, (255, 230, 80))

    @staticmethod
    def spawn_at_edge(margin: float = 40, safe_player_x: float = WIDTH / 2, safe_player_y: float = HEIGHT / 2):
        """Return (x, y) guaranteed outside the visible screen and far from player."""
        for _ in range(10):
            side = random.randint(0, 3)
            if side == 0:
                x, y = random.uniform(margin, WIDTH - margin), HEIGHT + margin
            elif side == 1:
                x, y = random.uniform(margin, WIDTH - margin), -margin
            elif side == 2:
                x, y = -margin, random.uniform(margin, HEIGHT - margin)
            else:
                x, y = WIDTH + margin, random.uniform(margin, HEIGHT - margin)

            if math.hypot(x - safe_player_x, y - safe_player_y) > 200:
                return x, y
        return x, y


# ==============================================================================
# [20/77] MODULE: game/entities/enemies/boss_hiranyakashipu.py
# ==============================================================================
"""
game/entities/enemies/boss_hiranyakashipu.py
New Boss — Hiranyakashipu.
"""
import math
import random
import arcade
from constants import (
    WIDTH, HEIGHT,
    COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet

class BossHiranyakashipu(BaseEnemy):
    name = "HIRANYAKASHIPU"
    boss_id = "hiranyakashipu"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + 60,
                         hp=4500, speed=0.8,
                         score_value=20000, radius=50)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.75

        self._fire_timer = 2.0
        self._summon_timer = 6.0
        
        self._drift_dir = 1
        self._drift_timer = 0.0
        
        # Phase 3 specific
        self._invincibility_timer = 5.0
        self._is_invincible = False

        self.current_attack_name = "WRATH OF THE TYRANT"

    def _update_phase(self) -> None:
        frac = self.hp / self.max_hp
        if frac <= 0.33:
            if self.phase != 3:
                self.phase = 3
                self.speed = 1.8
        elif frac <= 0.66:
            if self.phase != 2:
                self.phase = 2
                self.speed = 1.3
        else:
            self.phase = 1

    def take_damage(self, amount: int) -> None:
        if getattr(self, '_is_invincible', False):
            return
        super().take_damage(amount)

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        self._update_phase()

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        bullets = []

        if not self._entered:
            if self.y > self._target_y:
                self.y -= self.speed * 100.0 * delta_time
            else:
                self._entered = True
            return bullets

        # Movement
        self._drift_timer += delta_time
        drift_period = 3.0 if self.phase < 3 else 1.5
        self.x += self._drift_dir * self.speed * 35.0 * delta_time
        if self._drift_timer >= drift_period:
            self._drift_dir *= -1
            self._drift_timer = 0.0
        self.x = max(self.radius + 20, min(WIDTH - self.radius - 20, self.x))

        aim_angle = math.degrees(math.atan2(player_y - self.y, player_x - self.x))

        # Attacking logic based on phase
        self._fire_timer -= delta_time
        if self._fire_timer <= 0:
            if self.phase == 1:
                self._fire_timer = 2.0
                self.current_attack_name = "SPREAD BARRAGE"
                spread = [-30, -15, 0, 15, 30]
                for offset in spread:
                    bullets.append(EnemyBullet(self.x, self.y, aim_angle + offset, speed=5.5, radius=7))
            elif self.phase == 2:
                self._fire_timer = 1.2
                self.current_attack_name = "PILLAR SLAM"
                # Triple spread
                spread = [-45, -20, 0, 20, 45, -10, 10]
                for offset in spread:
                    bullets.append(EnemyBullet(self.x, self.y, aim_angle + offset, speed=6.5, radius=8))
            elif self.phase == 3:
                self._fire_timer = 0.4
                self.current_attack_name = "RAPID ASSAULT"
                bullets.append(EnemyBullet(self.x, self.y, aim_angle + random.uniform(-10, 10), speed=8.0, radius=5))

        # Summoning logic phase 1
        summons = []
        if self.phase == 1:
            self._summon_timer -= delta_time
            if self._summon_timer <= 0:
                self._summon_timer = 6.0
                self.current_attack_name = "ASURA COLUMNS"
                from game.entities.enemies.asura_fast import AsuraFast
                for _ in range(3):
                    summons.append(AsuraFast(self.x + random.uniform(-60, 60), self.y + random.uniform(20, 60)))

        if summons:
            self._pending_summons = summons

        # Phase 3 Invincibility mechanics
        if self.phase == 3:
            self._invincibility_timer -= delta_time
            if self._is_invincible and self._invincibility_timer <= 0:
                self._is_invincible = False
                self._invincibility_timer = 5.0 # Vulnerable for 5s
            elif not self._is_invincible and self._invincibility_timer <= 0:
                self._is_invincible = True
                self._invincibility_timer = 3.0 # Invincible for 3s
            
            if self._is_invincible:
                self.current_attack_name = "IMMORTAL BOON"

        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        r = self.radius

        # Draw glowing circle in phase 3 if invincible
        if self.phase == 3 and getattr(self, '_is_invincible', False):
            arcade.draw_circle_filled(self.x, self.y, r + 20, (255, 255, 255, 100))
        elif self.phase == 3:
            # Pulsing white glow underneath
            arcade.draw_circle_filled(self.x, self.y, r + 10, (255, 255, 255, 40))

        # Body - Large red diamond
        body_color = COLOR_WHITE if flash else (180, 20, 20)
        points = [
            (self.x, self.y + r),
            (self.x + r, self.y),
            (self.x, self.y - r),
            (self.x - r, self.y)
        ]
        arcade.draw_polygon_filled(points, body_color)

        # 4 Arms N/S/E/W - thin gold rectangles
        arm_color = COLOR_WHITE if flash else (255, 215, 0)
        # N
        arcade.draw_rectangle_filled(self.x, self.y + r + 10, 8, 30, arm_color)
        # S
        arcade.draw_rectangle_filled(self.x, self.y - r - 10, 8, 30, arm_color)
        # E
        arcade.draw_rectangle_filled(self.x + r + 10, self.y, 30, 8, arm_color)
        # W
        arcade.draw_rectangle_filled(self.x - r - 10, self.y, 30, 8, arm_color)

        # Crown - 10 small gold triangles in a semicircle above
        for i in range(10):
            ang = math.radians(i * 18 + 180) # Semicircle over the top
            cx = self.x + math.cos(ang) * (r + 15)
            cy = self.y - math.sin(ang) * (r + 15) # negate sin for upper half
            
            # Triangle pointing outwards
            t_points = [
                (cx, cy),
                (cx + math.cos(ang + 1.5) * 8, cy - math.sin(ang + 1.5) * 8),
                (cx + math.cos(ang - 1.5) * 8, cy - math.sin(ang - 1.5) * 8)
            ]
            arcade.draw_polygon_filled(t_points, arm_color)
            
        # Demonic Red Optics in the middle
        eye_color = COLOR_WHITE if not flash else (255, 0, 0)
        arcade.draw_circle_filled(self.x - 10, self.y + 10, 5, eye_color)
        arcade.draw_circle_filled(self.x + 10, self.y + 10, 5, eye_color)

        # Attack name tag
        arcade.draw_text(self.current_attack_name, self.x, self.y - r - 30, (255, 200, 50), font_size=9, bold=True, anchor_x="center")

    @property
    def pending_summons(self) -> list:
        summons = getattr(self, '_pending_summons', [])
        self._pending_summons = []
        return summons


# ==============================================================================
# [21/77] MODULE: game/entities/enemies/boss_kumbhakarna.py
# ==============================================================================
"""
game/entities/enemies/boss_kumbhakarna.py
Mini-Boss — Kumbhakarna (Wave 5 Armored Titan).
Features charging telegraph cones, shockwave tremor rings, and mace flurries.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    KUMBHAKARNA_HP, KUMBHAKARNA_RADIUS, KUMBHAKARNA_SPEED, KUMBHAKARNA_SCORE,
    COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossKumbhakarna(BaseEnemy):
    name = "KUMBHAKARNA"
    boss_id = "kumbhakarna"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + KUMBHAKARNA_RADIUS + 10,
                         hp=KUMBHAKARNA_HP, speed=KUMBHAKARNA_SPEED,
                         score_value=KUMBHAKARNA_SCORE, radius=KUMBHAKARNA_RADIUS)
        self._target_y = HEIGHT * 0.75
        self._entered = False

        self._attack_timer = 2.0
        self._attack_mode = 0  # 0: Radial Mace, 1: Tremor 5-way, 2: Charge Dash
        self._charge_vx = 0.0
        self._charge_vy = 0.0
        self._charge_duration = 0.0
        self._charge_telegraph_timer = 0.0
        self._charge_aim = 0.0
        self._is_charging = False
        self.current_attack_name = "RADIAL MACE"
        self.texture = AssetManager.texture("boss_kumbhakarna.png")

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        bullets = []

        if not self._entered:
            if self.y > self._target_y:
                self.y -= self.speed * 80.0 * delta_time
            else:
                self._entered = True
            return bullets

        # Charge Telegraph Phase (locked warning before dashing)
        if self._charge_telegraph_timer > 0:
            self._charge_telegraph_timer -= delta_time
            self.current_attack_name = "⚠ CHARGE INCOMING!"
            self._charge_aim = self._angle_to_player(player_x, player_y)
            if self._charge_telegraph_timer <= 0:
                rad = math.radians(self._charge_aim)
                charge_speed = 620.0
                self._charge_vx = math.cos(rad) * charge_speed
                self._charge_vy = math.sin(rad) * charge_speed
                self._charge_duration = 0.65
                self._is_charging = True
                self.current_attack_name = "TITAN CHARGE!"
            return bullets

        # Charge Dash Execution
        if self._is_charging:
            self.x += self._charge_vx * delta_time
            self.y += self._charge_vy * delta_time
            self._charge_duration -= delta_time
            if self._charge_duration <= 0:
                self._is_charging = False
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))
            return bullets

        # Normal tracking movement
        self._move_toward(player_x, self._target_y, delta_time)

        self._attack_timer -= delta_time
        if self._attack_timer <= 0:
            self._attack_timer = 3.4
            self._attack_mode = (self._attack_mode + 1) % 3

            if self._attack_mode == 0:
                # Radial Mace Burst
                self.current_attack_name = "MACE BURST!"
                for i in range(12):
                    ang = i * 30
                    bullets.append(EnemyBullet(self.x, self.y, ang, speed=4.5, radius=5, color=(255, 140, 30)))

            elif self._attack_mode == 1:
                # Tremor 5-way aimed blast
                self.current_attack_name = "TREMOR SHOCK!"
                aim = self._angle_to_player(player_x, player_y)
                for offset in (-30, -15, 0, 15, 30):
                    bullets.append(EnemyBullet(self.x, self.y, aim + offset, speed=6.0, radius=6, color=(255, 60, 40)))

            elif self._attack_mode == 2:
                # Enter Charge Telegraph
                self._charge_telegraph_timer = 0.9
                self._charge_aim = self._angle_to_player(player_x, player_y)
                self.current_attack_name = "⚠ CHARGE INCOMING!"

        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        body_col = COLOR_WHITE if flash else (180, 100, 20)

        # Draw Clear Red Danger Line & Warning Cone when telegraphing charge
        if self._charge_telegraph_timer > 0:
            rad = math.radians(self._charge_aim)
            end_x = self.x + math.cos(rad) * 600
            end_y = self.y + math.sin(rad) * 600
            arcade.draw_line(self.x, self.y, end_x, end_y, (255, 40, 40, 190), 4)
            arcade.draw_circle_filled(self.x, self.y, self.radius + 20, (255, 40, 40, 90))
            arcade.draw_circle_outline(self.x, self.y, self.radius + 22, (255, 80, 80), 2)

        if self._draw_sprite(width=self.radius * 2.5, height=self.radius * 2.5,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            arcade.draw_circle_outline(self.x, self.y, self.radius + 4, (255, 200, 60), 3)
            arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 160, 40), font_size=9, bold=True, anchor_x="center")
            return

        # Heavy Armored Titan Hull
        arcade.draw_circle_filled(self.x, self.y, self.radius, body_col)
        arcade.draw_circle_outline(self.x, self.y, self.radius + 4, (255, 200, 60), 3)

        # Armored Mace Spikes
        for i in range(8):
            ang = math.radians(i * 45)
            sx = self.x + math.cos(ang) * (self.radius + 8)
            sy = self.y + math.sin(ang) * (self.radius + 8)
            arcade.draw_circle_filled(sx, sy, 6, (120, 70, 20))

        arcade.draw_circle_filled(self.x, self.y, 8, (255, 180, 40))
        arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 160, 40), font_size=9, bold=True, anchor_x="center")


# ==============================================================================
# [22/77] MODULE: game/entities/enemies/boss_mahishasura.py
# ==============================================================================
"""Mahishasura — Wave 15 warlord with a two-phase shock assault."""
import math
import arcade
from constants import (
    WIDTH, HEIGHT, MAHISHASURA_HP, MAHISHASURA_RADIUS,
    MAHISHASURA_SPEED, MAHISHASURA_SCORE, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossMahishasura(BaseEnemy):
    name = "MAHISHASURA"
    boss_id = "mahishasura"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + MAHISHASURA_RADIUS + 10,
                         hp=MAHISHASURA_HP, speed=MAHISHASURA_SPEED,
                         score_value=MAHISHASURA_SCORE,
                         radius=MAHISHASURA_RADIUS)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.76
        self._attack_timer = 2.0
        self._drift = 1
        self._drift_timer = 0.0
        self._aim = 0.0
        self._pending_summons = []
        self.texture = AssetManager.texture("boss_mahishasura.png")
        self.current_attack_name = "SHOCKWAVE ROAR"

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        frac = self.hp / self.max_hp
        self.phase = 2 if frac <= 0.5 else 1
        if not self._entered:
            self.y = max(self._target_y, self.y - self.speed * 80 * delta_time)
            self._entered = self.y <= self._target_y
            return []

        self._drift_timer += delta_time
        self.x += self._drift * self.speed * 28 * delta_time
        if self._drift_timer >= 2.3:
            self._drift *= -1
            self._drift_timer = 0.0
        self.x = max(self.radius + 20, min(WIDTH - self.radius - 20, self.x))

        self._aim = self._angle_to_player(player_x, player_y)
        self._attack_timer -= delta_time
        if self._attack_timer > 0:
            return []
        self._attack_timer = 1.9 if self.phase == 2 else 2.5
        bullets = []
        if self.phase == 1:
            self.current_attack_name = "SHOCKWAVE ROAR!"
            for i in range(14):
                bullets.append(EnemyBullet(self.x, self.y, i * (360 / 14), speed=4.8, radius=5, color=(255, 140, 40)))
        else:
            self.current_attack_name = "WARLORD'S BARRAGE!"
            for offset in (-32, -16, 0, 16, 32):
                bullets.append(EnemyBullet(self.x, self.y, self._aim + offset, speed=7.0, radius=6, color=(255, 60, 60)))
            from game.entities.enemies.asura_fast import AsuraFast
            self._pending_summons = [AsuraFast(self.x - 45, self.y), AsuraFast(self.x + 45, self.y)]
        return bullets

    @property
    def pending_summons(self) -> list:
        summons, self._pending_summons = self._pending_summons, []
        return summons

    def draw(self) -> None:
        flash = self._hit_flash > 0
        if self._attack_timer < 0.35:
            rad = math.radians(self._aim)
            arcade.draw_line(self.x, self.y, self.x + math.cos(rad) * 500,
                             self.y + math.sin(rad) * 500, (255, 60, 40, 150), 3)
        if self._draw_sprite(width=self.radius * 2.5, height=self.radius * 2.5,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            ring = (255, 180, 40) if self.phase == 1 else (255, 50, 50)
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, ring, 3)
        else:
            body = COLOR_WHITE if flash else (190, 60, 30)
            arcade.draw_circle_filled(self.x, self.y, self.radius, body)
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, (255, 180, 40), 3)
        arcade.draw_text(self.current_attack_name, self.x,
                         self.y - self.radius - 18, (255, 140, 50),
                         font_size=9, bold=True, anchor_x="center")


# ==============================================================================
# [23/77] MODULE: game/entities/enemies/boss_ravana.py
# ==============================================================================
"""
game/entities/enemies/boss_ravana.py
Boss — Ravana. Three-phase mythological emperor fight with attack telegraphs,
red danger cones, destructible energy plates, and attack announcements.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    RAVANA_HP, RAVANA_RADIUS, RAVANA_SPEED, RAVANA_SCORE,
    RAVANA_PHASE2_HP, RAVANA_PHASE3_HP,
    RAVANA_FIRE_RATE_P1, RAVANA_FIRE_RATE_P2, RAVANA_FIRE_RATE_P3,
    RAVANA_SPIRAL_RATE, RAVANA_SUMMON_RATE,
    COLOR_RAVANA, COLOR_WHITE,
)
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossRavana(BaseEnemy):
    name = "RAVANA"
    boss_id = "ravana"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + RAVANA_RADIUS + 10,
                         hp=RAVANA_HP, speed=RAVANA_SPEED,
                         score_value=RAVANA_SCORE, radius=RAVANA_RADIUS)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.78

        self._fire_timer = RAVANA_FIRE_RATE_P1
        self._spiral_timer = 0.0
        self._spiral_angle = 0.0
        self._summon_timer = RAVANA_SUMMON_RATE

        self._drift_dir = 1
        self._drift_timer = 0.0
        self._telegraph_timer = 0.0
        self.current_attack_name = "SPREAD BARRAGE"
        self._telegraph_aim = 0.0
        self.texture = AssetManager.texture("boss_ravana.png")

    def _update_phase(self) -> None:
        frac = self.hp / self.max_hp
        if frac <= RAVANA_PHASE3_HP:
            self.phase = 3
        elif frac <= RAVANA_PHASE2_HP:
            self.phase = 2
        else:
            self.phase = 1

    def _current_fire_rate(self) -> float:
        return {1: RAVANA_FIRE_RATE_P1,
                2: RAVANA_FIRE_RATE_P2,
                3: RAVANA_FIRE_RATE_P3}[self.phase]

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []

        self._update_phase()

        if self._hit_flash > 0:
            self._hit_flash -= delta_time

        bullets = []

        if not self._entered:
            if self.y > self._target_y:
                self.y -= self.speed * 100.0 * delta_time
            else:
                self._entered = True
            return bullets

        # Lateral drift with delta_time
        self._drift_timer += delta_time
        drift_period = 4.0 if self.phase < 3 else 2.5
        self.x += self._drift_dir * self.speed * 25.0 * delta_time
        if self._drift_timer >= drift_period:
            self._drift_dir *= -1
            self._drift_timer = 0.0
        self.x = max(self.radius + 20, min(WIDTH - self.radius - 20, self.x))

        self._telegraph_aim = math.degrees(math.atan2(player_y - self.y, player_x - self.x))

        # Main Spread Shot with 0.5s Telegraph
        self._fire_timer -= delta_time
        if self._fire_timer <= 0:
            self._fire_timer = self._current_fire_rate()
            self.current_attack_name = "SPREAD ASTRA!"
            spread = [-20, 0, 20] if self.phase == 1 else [-28, -14, 0, 14, 28]
            for offset in spread:
                bullets.append(EnemyBullet(self.x, self.y, self._telegraph_aim + offset, speed=6.0, radius=6))

        # Phase 2+ Spiral Attack
        if self.phase >= 2:
            self._spiral_timer -= delta_time
            if self._spiral_timer <= 0:
                self._spiral_timer = RAVANA_SPIRAL_RATE
                self.current_attack_name = "SPIRAL VOID!"
                self._spiral_angle += 22.0
                for arm in range(4):
                    a = self._spiral_angle + arm * 90
                    bullets.append(EnemyBullet(self.x, self.y, a, speed=4.5, radius=5))

        # Phase 3 Summons
        summons = []
        if self.phase == 3:
            self._summon_timer -= delta_time
            if self._summon_timer <= 0:
                self._summon_timer = RAVANA_SUMMON_RATE
                self.current_attack_name = "SUMMON FLEET!"
                from game.entities.enemies.asura_fast import AsuraFast
                from game.entities.enemies.asura_kamikaze import AsuraKamikaze
                summons = [AsuraFast(self.x - 40, self.y), AsuraKamikaze(self.x + 40, self.y)]

        if summons:
            self._pending_summons = summons

        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        color = COLOR_WHITE if flash else COLOR_RAVANA
        r = self.radius

        # Attack Telegraph Aim Line
        if self._fire_timer < 0.5:
            rad = math.radians(self._telegraph_aim)
            end_x = self.x + math.cos(rad) * 450
            end_y = self.y + math.sin(rad) * 450
            arcade.draw_line(self.x, self.y, end_x, end_y, (255, 30, 50, 160), 2)
            arcade.draw_circle_outline(self.x, self.y, r + 16, (255, 50, 50, 140), 2)

        if self._draw_sprite(width=r * 2.5, height=r * 2.5,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            phase_colors = [(255, 200, 0), (255, 100, 0), (255, 0, 50)]
            arcade.draw_circle_outline(self.x, self.y, r + 4, phase_colors[self.phase - 1], 3)
            arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 80, 80), font_size=9, bold=True, anchor_x="center")
            return

        # 10 Golden Crown Spikes
        for i in range(10):
            ang = math.radians(i * 36 - 90)
            sx = self.x + math.cos(ang) * (r + 18)
            sy = self.y + math.sin(ang) * (r + 18)
            arcade.draw_circle_filled(sx, sy, 5, (255, 215, 60))

        # Main Fortress Hull
        arcade.draw_circle_filled(self.x, self.y, r, color)

        # Demonic Red Optics
        eye_color = COLOR_WHITE if not flash else COLOR_RAVANA
        arcade.draw_circle_filled(self.x - 14, self.y + 8, 6, eye_color)
        arcade.draw_circle_filled(self.x + 14, self.y + 8, 6, eye_color)
        arcade.draw_circle_filled(self.x - 14, self.y + 8, 2.5, (255, 255, 255))
        arcade.draw_circle_filled(self.x + 14, self.y + 8, 2.5, (255, 255, 255))

        # Phase indicator ring
        phase_colors = [(255, 200, 0), (255, 100, 0), (255, 0, 50)]
        ring_color = phase_colors[self.phase - 1]
        arcade.draw_circle_outline(self.x, self.y, r + 4, ring_color, 3)

        # Attack name tag
        arcade.draw_text(self.current_attack_name, self.x, self.y - self.radius - 18, (255, 80, 80), font_size=9, bold=True, anchor_x="center")

    @property
    def pending_summons(self) -> list:
        summons = getattr(self, '_pending_summons', [])
        self._pending_summons = []
        return summons


# ==============================================================================
# [24/77] MODULE: game/entities/enemies/boss_vritra.py
# ==============================================================================
"""Vritra — the Wave 20 campaign finale, a storm-serpent fortress."""
import math
import arcade
from constants import WIDTH, HEIGHT, VRITRA_HP, VRITRA_RADIUS, VRITRA_SPEED, VRITRA_SCORE, COLOR_WHITE
from game.entities.enemies.base_enemy import BaseEnemy
from game.entities.bullet import EnemyBullet
from game.systems.asset_manager import AssetManager


class BossVritra(BaseEnemy):
    name = "VRITRA"
    boss_id = "vritra"
    is_boss = True

    def __init__(self):
        super().__init__(WIDTH / 2, HEIGHT + VRITRA_RADIUS + 10,
                         hp=VRITRA_HP, speed=VRITRA_SPEED,
                         score_value=VRITRA_SCORE, radius=VRITRA_RADIUS)
        self.phase = 1
        self._entered = False
        self._target_y = HEIGHT * 0.74
        self._attack_timer = 1.6
        self._angle = 0.0
        self._aim = 0.0
        self.texture = AssetManager.texture("boss_vritra.png")
        self.current_attack_name = "STORM COIL"

    def update(self, delta_time: float, player_x: float, player_y: float) -> list:
        if not self.alive:
            return []
        if self._hit_flash > 0:
            self._hit_flash -= delta_time
        frac = self.hp / self.max_hp
        self.phase = 3 if frac <= 0.33 else 2 if frac <= 0.66 else 1
        if not self._entered:
            self.y = max(self._target_y, self.y - self.speed * 90 * delta_time)
            self._entered = self.y <= self._target_y
            return []

        self._angle += delta_time * (80 if self.phase == 3 else 45)
        self.x = WIDTH / 2 + math.sin(self._angle * 0.02) * (180 if self.phase >= 2 else 120)
        self._aim = self._angle_to_player(player_x, player_y)
        self._attack_timer -= delta_time
        if self._attack_timer > 0:
            return []
        self._attack_timer = max(0.8, 1.8 - self.phase * 0.25)
        bullets = []
        self.current_attack_name = "ASTRAL STORM!" if self.phase < 3 else "VRITRA UNLEASHED!"
        count = 10 + self.phase * 2
        for i in range(count):
            angle = self._angle + i * (360 / count)
            bullets.append(EnemyBullet(self.x, self.y, angle, speed=4.2 + self.phase * 0.5, radius=5, color=(180, 70, 255)))
        if self.phase == 3:
            for offset in (-18, 18):
                bullets.append(EnemyBullet(self.x, self.y, self._aim + offset, speed=8.0, radius=6, color=(255, 40, 140)))
        return bullets

    def draw(self) -> None:
        flash = self._hit_flash > 0
        rad = math.radians(self._aim)
        if self._attack_timer < 0.35:
            arcade.draw_line(self.x, self.y, self.x + math.cos(rad) * 520,
                             self.y + math.sin(rad) * 520, (190, 80, 255, 150), 3)
        if self._draw_sprite(width=self.radius * 2.55, height=self.radius * 2.55,
                             color=COLOR_WHITE if flash else (255, 255, 255, 255)):
            ring = [(100, 220, 255), (180, 80, 255), (255, 40, 140)][self.phase - 1]
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, ring, 3)
        else:
            arcade.draw_circle_filled(self.x, self.y, self.radius, COLOR_WHITE if flash else (100, 40, 180))
            arcade.draw_circle_outline(self.x, self.y, self.radius + 5, (180, 80, 255), 3)
        arcade.draw_text(self.current_attack_name, self.x,
                         self.y - self.radius - 18, (210, 100, 255),
                         font_size=9, bold=True, anchor_x="center")


# ==============================================================================
# [25/77] MODULE: game/systems/__init__.py
# ==============================================================================
# game/systems/__init__.py


# ==============================================================================
# [26/77] MODULE: game/systems/achievement_system.py
# ==============================================================================
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
        "id": "wave_5_veteran",
        "name": "Into the Deep",
        "desc": "Reach Wave 5 and awaken your first campaign boss.",
        "icon": "🌊",
    },
    {
        "id": "wave_10_breaker",
        "name": "Break Lanka's Gate",
        "desc": "Reach Wave 10 and enter the second half of the campaign.",
        "icon": "🚪",
    },
    {
        "id": "mahishasura_bane",
        "name": "Warlord Breaker",
        "desc": "Defeat Mahishasura in the Setu Expanse.",
        "icon": "🐂",
    },
    {
        "id": "wave_15_conqueror",
        "name": "Forge Walker",
        "desc": "Reach Wave 15 in the final half of the campaign.",
        "icon": "🔥",
    },
    {
        "id": "vritra_vanquisher",
        "name": "Storm Breaker",
        "desc": "Defeat Vritra at the Mahayuddha Citadel.",
        "icon": "⚡",
    },
    {
        "id": "boss_collector",
        "name": "Four Thrones Fall",
        "desc": "Defeat all four campaign bosses across your runs.",
        "icon": "👑",
    },
    {
        "id": "campaign_conqueror",
        "name": "Conqueror of the Mahayuddha",
        "desc": "Clear all 20 campaign waves and defeat the final boss.",
        "icon": "🏅",
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
    {
        "id": "cube_collector",
        "name": "Astral Arsenal",
        "desc": "Collect 10 ability cubes in a single run.",
        "icon": "🔷",
    },
    {
        "id": "overdrive_online",
        "name": "Overdrive Online",
        "desc": "Collect an Astra Overdrive cube and unleash rapid fire.",
        "icon": "💗",
    },
]


def get_all() -> list[dict]:
    """Return all achievements with an 'unlocked' key reflecting save state.

    Each element is a copy of the achievement dict from ACHIEVEMENTS_LIST
    with an extra ``unlocked: bool`` key so callers don't need to
    instantiate AchievementManager just to render the trophy page.
    """
    saved = save_system.load()
    unlocked_ids: set[str] = set(saved.get("achievements", []))
    return [
        {**a, "unlocked": a["id"] in unlocked_ids}
        for a in ACHIEVEMENTS_LIST
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


# ==============================================================================
# [27/77] MODULE: game/systems/asset_manager.py
# ==============================================================================
"""Small, fault-tolerant cache for optional visual assets."""
from pathlib import Path
import arcade


_IMAGE_ROOT = Path(__file__).resolve().parents[2] / "assets" / "images"
if not _IMAGE_ROOT.exists():
    _IMAGE_ROOT = Path(__file__).resolve().parents[3] / "assets" / "images"
_CACHE = {}


class AssetManager:
    """Load an image once and return ``None`` when it cannot be used."""

    @staticmethod
    def texture(name: str):
        if name in _CACHE:
            return _CACHE[name]
        path = _IMAGE_ROOT / name
        if path.suffix.lower() != ".png":
            path = path.with_suffix(".png")
        texture = None
        try:
            if path.is_file():
                texture = arcade.load_texture(str(path))
        except Exception:
            texture = None
        _CACHE[name] = texture
        return texture

    @staticmethod
    def draw(texture, x: float, y: float, width: float, height: float,
             angle: float = 0.0, color=(255, 255, 255, 255)) -> bool:
        """Draw a cached texture in Arcade 3.x; return whether it was drawn."""
        if texture is None:
            return False
        try:
            arcade.draw_texture_rect(
                texture,
                arcade.LBWH(x - width / 2, y - height / 2, width, height),
                angle=angle,
                color=color,
            )
            return True
        except Exception:
            return False


# ==============================================================================
# [28/77] MODULE: game/systems/audio_synthesizer.py
# ==============================================================================
"""
game/systems/audio_synthesizer.py
Pure-Python Procedural Sound Generator using standard library `wave`, `math`, and `struct`.
Generates crisp, retro-sci-fi 16-bit sound effects directly into assets/sounds/
so audio works out of the box with zero external downloads!
"""
import math
import random
import struct
import wave
from pathlib import Path


# Resolve from the source file instead of the process working directory.  This
# matters when the game is launched from a desktop shortcut, an IDE, or a
SOUND_DIR = Path(__file__).resolve().parents[2] / "assets" / "sounds"
if not SOUND_DIR.exists():
    SOUND_DIR = Path(__file__).resolve().parents[3] / "assets" / "sounds"


def _write_wav(filename: str, samples: list[float], sample_rate: int = 22050) -> None:
    SOUND_DIR.mkdir(parents=True, exist_ok=True)
    filepath = SOUND_DIR / filename
    if filepath.exists():
        return  # Don't overwrite existing files

    with wave.open(str(filepath), "wb") as wav_file:
        wav_file.setnchannels(1)       # Mono
        wav_file.setsampwidth(2)       # 16-bit
        wav_file.setframerate(sample_rate)

        # Convert float (-1.0 to 1.0) to 16-bit signed integer (-32767 to 32767)
        raw_frames = bytearray()
        for sample in samples:
            clamped = max(-1.0, min(1.0, sample))
            val = int(clamped * 32760)
            raw_frames.extend(struct.pack("<h", val))

        wav_file.writeframes(raw_frames)


def generate_all_sounds() -> None:
    """Generates all 8 core sound effects if missing."""
    sample_rate = 22050

    # 1. shoot.wav — Punchy high-frequency laser sweep
    samples = []
    dur = 0.12
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 880 - (t / dur) * 600
        vol = (1.0 - (t / dur)) ** 1.5
        sample = math.sin(2 * math.pi * freq * t) * vol
        samples.append(sample)
    _write_wav("shoot.wav", samples, sample_rate)

    # 2. dash.wav — Swift wind warp whoosh
    samples = []
    dur = 0.18
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 300 + math.sin(t * 30) * 150 + (t / dur) * 400
        noise = (random.random() * 2 - 1) * 0.35
        vol = math.sin(math.pi * (t / dur)) * 0.9
        sample = (math.sin(2 * math.pi * freq * t) * 0.65 + noise) * vol
        samples.append(sample)
    _write_wav("dash.wav", samples, sample_rate)

    # 3. hit.wav — Crisp metallic kinetic thud
    samples = []
    dur = 0.10
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 240 - (t / dur) * 160
        noise = (random.random() * 2 - 1) * 0.4
        vol = (1.0 - (t / dur)) ** 2
        sample = (math.sin(2 * math.pi * freq * t) * 0.6 + noise) * vol
        samples.append(sample)
    _write_wav("hit.wav", samples, sample_rate)

    # 4. explosion.wav — Heavy crunching blast with low-end rumble
    samples = []
    dur = 0.35
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 120 * (1.0 - (t / dur) * 0.7)
        noise = (random.random() * 2 - 1) * 0.75
        vol = (1.0 - (t / dur)) ** 1.2
        sample = (math.sin(2 * math.pi * freq * t) * 0.35 + noise * 0.65) * vol
        samples.append(sample)
    _write_wav("explosion.wav", samples, sample_rate)

    # 5. powerup.wav — Ascending celestial golden chime
    samples = []
    dur = 0.30
    total_samples = int(sample_rate * dur)
    notes = [440, 554.37, 659.25, 880]  # A Major chord arpeggio
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur)) * 0.85
        sample = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)) * vol
        samples.append(sample)
    _write_wav("powerup.wav", samples, sample_rate)

    # 6. boss_roar.wav — Deep terrifying sub-bass growl
    samples = []
    dur = 0.80
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 70 + math.sin(t * 24) * 35 - (t / dur) * 30
        noise = (random.random() * 2 - 1) * 0.4
        vol = math.sin(math.pi * (t / dur)) * 0.95
        sample = (math.sin(2 * math.pi * freq * t) * 0.7 + noise) * vol
        samples.append(sample)
    _write_wav("boss_roar.wav", samples, sample_rate)

    # 7. wave_clear.wav — Bright positive victory stinger
    samples = []
    dur = 0.40
    total_samples = int(sample_rate * dur)
    notes = [523.25, 659.25, 783.99, 1046.50]  # C Major fanfare
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur)) * 0.8
        sample = math.sin(2 * math.pi * freq * t) * vol
        samples.append(sample)
    _write_wav("wave_clear.wav", samples, sample_rate)

    # 8. victory.wav — Grand celebratory fanfare
    samples = []
    dur = 1.0
    total_samples = int(sample_rate * dur)
    melody = [(523.25, 0.2), (659.25, 0.2), (783.99, 0.2), (1046.50, 0.4)]
    for freq, note_dur in melody:
        note_samples = int(sample_rate * note_dur)
        for i in range(note_samples):
            t = i / sample_rate
            vol = (1.0 - (t / note_dur)) * 0.85
            sample = (math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(4 * math.pi * freq * t)) * vol
            samples.append(sample)
    _write_wav("victory.wav", samples, sample_rate)

    # 9. game_over.wav — Descending minor collapse tone
    samples = []
    dur = 0.6
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 300 - (t / dur) * 220
        vol = (1.0 - (t / dur)) * 0.8
        sample = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * (freq * 0.5) * t)) * vol
        samples.append(sample)
    _write_wav("game_over.wav", samples, sample_rate)

    # 10. ui_click.wav — Crisp gentle UI selection click
    samples = []
    dur = 0.05
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 1200 - (t / dur) * 700
        vol = (1.0 - (t / dur)) ** 3
        sample = math.sin(2 * math.pi * freq * t) * vol * 0.7
        samples.append(sample)
    _write_wav("ui_click.wav", samples, sample_rate)

    # 11. warning_siren.wav — Pulsing danger klaxon for boss warning
    samples = []
    dur = 0.55
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 600 + math.sin(t * 28) * 250
        vol = math.sin(math.pi * (t / dur)) * 0.85
        sample = math.sin(2 * math.pi * freq * t) * vol
        samples.append(sample)
    _write_wav("warning_siren.wav", samples, sample_rate)

    # 12. dodge_chime.wav — Sparkling high chime for perfect dodge / near miss
    samples = []
    dur = 0.22
    total_samples = int(sample_rate * dur)
    notes = [1046.50, 1318.51, 1567.98]  # High C Major
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur)) * 0.75
        sample = (math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(4 * math.pi * freq * t)) * vol
        samples.append(sample)
    _write_wav("dodge_chime.wav", samples, sample_rate)

    # 13. synergy.wav — Grand harmonic resonance for Deva Boon Fusion
    samples = []
    dur = 0.85
    total_samples = int(sample_rate * dur)
    notes = [523.25, 659.25, 783.99, 1046.50, 1318.51]  # Full ascending arpeggio with shimmering harmonics
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur) * 0.8) * 0.9
        sample = (math.sin(2 * math.pi * freq * t) * 0.6 +
                  math.sin(2 * math.pi * (freq * 1.5) * t) * 0.25 +
                  math.sin(4 * math.pi * freq * t) * 0.15) * vol
        samples.append(sample)
    _write_wav("synergy.wav", samples, sample_rate)


# ==============================================================================
# [29/77] MODULE: game/systems/boon_system.py
# ==============================================================================
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
        "desc": "Fires an amplified piercing Solar slug on recurring shots (7th shot at Lv.1, scaling down with level).",
        "color": (255, 240, 140),
        "icon": "☀️",
    },
]


SYNERGIES_DATABASE = [
    {
        "id": "plasma_storm",
        "name": "Celestial Plasma Storm",
        "parents": ("agni_fury", "indra_thunder"),
        "desc": "Chain lightning strikes detonate blazing plasma explosions on all struck enemies.",
        "color": (255, 160, 240),
        "icon": "⚡🔥",
    },
    {
        "id": "solar_cyclone",
        "name": "Solar Flare Cyclone",
        "parents": ("vayu_tempest", "surya_beam"),
        "desc": "Vayu dashes leave behind a persistent fiery solar tornado that incinerates enemies.",
        "color": (255, 215, 60),
        "icon": "🌪️☀️",
    },
    {
        "id": "oceanic_surge",
        "name": "Oceanic Amrita Surge",
        "parents": ("varuna_ward", "garuda_magnet"),
        "desc": "Collecting magnetized power-ups releases a holy wave restoring 15 HP and clearing nearby bullets.",
        "color": (80, 240, 255),
        "icon": "🌊🦅",
    },
    {
        "id": "executioner_disc",
        "name": "Yama's Executioner Disc",
        "parents": ("sudarshana_keen", "yama_execution"),
        "desc": "Sudarshana Chakram instantly executes non-boss enemies below 25% HP with double critical score.",
        "color": (255, 60, 100),
        "icon": "🪓💀",
    },
]


class BoonManager:
    def __init__(self):
        self.active_boons: dict[str, int] = {}
        self.active_synergies: set[str] = set()
        self.newly_unlocked_synergies: list[dict] = []
        self.shot_counter = 0
        self.regen_timer = 0.0

    def has_boon(self, boon_id: str) -> bool:
        return boon_id in self.active_boons

    def get_boon_level(self, boon_id: str) -> int:
        return self.active_boons.get(boon_id, 0)

    def has_synergy(self, synergy_id: str) -> bool:
        return synergy_id in self.active_synergies

    def add_boon(self, boon_id: str) -> list[dict]:
        """Add a boon level and check if any new synergy was unlocked."""
        if boon_id in self.active_boons:
            self.active_boons[boon_id] += 1
        else:
            self.active_boons[boon_id] = 1

        newly_formed = []
        for syn in SYNERGIES_DATABASE:
            sid = syn["id"]
            if sid not in self.active_synergies:
                p1, p2 = syn["parents"]
                if self.has_boon(p1) and self.has_boon(p2):
                    self.active_synergies.add(sid)
                    newly_formed.append(syn)
                    self.newly_unlocked_synergies.append(syn)
        return newly_formed

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


# ==============================================================================
# [30/77] MODULE: game/systems/collision.py
# ==============================================================================
"""
game/systems/collision.py
Centralised circle-circle collision detection.
Runs all checks in one place so game_view stays clean.
"""
import math
from constants import PLAYER_CONTACT_DAMAGE


def _circles_overlap(ax, ay, ar, bx, by, br) -> bool:
    return math.hypot(ax - bx, ay - by) < ar + br


def check_all(
    player,
    enemies: list,
    player_bullets: list,
    enemy_bullets: list,
    powerups: list,
    score_system,
    boon_manager,
) -> dict:
    """
    Run every collision pair. Mutates entity lists and player state in place.
    Returns a summary dict with event coordinates for particles and SFX.
    """
    summary = {
        "kills": 0,
        "player_hit": False,
        "powerup_picked": [],
        "kamikaze_exploded": False,
        "hit_sparks": [],      # [(x, y, color)]
        "explosions": [],      # [(x, y, radius, color)]
        "powerup_auras": [],   # [(x, y, color)]
        "bullet_hits": [],     # [(x, y, enemy)]
    }

    px, py, pr = player.x, player.y, player.radius

    # ── 1. Player bullets ↔ enemies ──────────────────────────────────────
    for bullet in player_bullets[:]:
        if not bullet.alive:
            continue
        for enemy in enemies:
            if not enemy.alive:
                continue
            
            is_piercing = getattr(bullet, "is_piercing", False)
            if is_piercing:
                if not hasattr(bullet, "hit_enemies"):
                    bullet.hit_enemies = set()
                if enemy in bullet.hit_enemies:
                    continue

            if _circles_overlap(bullet.x, bullet.y, bullet.radius,
                                 enemy.x, enemy.y, enemy.radius):
                dmg = bullet.damage
                is_crit = False
                if boon_manager.has_boon("yama_execution") and enemy.max_hp > 0 and (enemy.hp / enemy.max_hp) < 0.45:
                    dmg = int(dmg * 1.6)
                    is_crit = True
                enemy.take_damage(dmg)
                summary["hit_sparks"].append((bullet.x, bullet.y, (255, 240, 100) if not is_crit else (255, 80, 80)))
                summary["bullet_hits"].append((bullet.x, bullet.y, enemy))

                if boon_manager.has_boon("agni_fury"):
                    enemy._burning = 3.0

                if enemy.is_dead():
                    summary["kills"] += 1
                    score_system.register_kill(enemy.score_value)
                    player.enemies_killed += 1
                    base_col = getattr(enemy, "_color", (255, 120, 30))
                    
                    if boon_manager.has_boon("agni_fury") and getattr(enemy, "_burning", 0) > 0:
                        summary["explosions"].append((enemy.x, enemy.y, enemy.radius * 1.5, (255, 120, 30)))
                        for other in enemies:
                            if other is not enemy and other.alive:
                                if _circles_overlap(enemy.x, enemy.y, enemy.radius * 2, other.x, other.y, other.radius):
                                    other.take_damage(25)
                                    if other.is_dead():
                                        summary["kills"] += 1
                                        score_system.register_kill(other.score_value)
                                        player.enemies_killed += 1
                                        summary["explosions"].append((other.x, other.y, other.radius, (255, 120, 30)))
                    else:
                        summary["explosions"].append((enemy.x, enemy.y, enemy.radius, base_col))
                
                if is_piercing:
                    bullet.hit_enemies.add(enemy)
                else:
                    bullet.alive = False
                    break   # one bullet hits one enemy

    # ── 2. Enemy bullets ↔ player ────────────────────────────────────────
    for bullet in enemy_bullets[:]:
        if not bullet.alive:
            continue
        if _circles_overlap(bullet.x, bullet.y, bullet.radius, px, py, pr):
            hit = player.take_damage(bullet.damage)
            bullet.alive = False
            summary["hit_sparks"].append((bullet.x, bullet.y, (255, 80, 80)))
            if hit:
                summary["player_hit"] = True

    # ── 3. Enemy contact ↔ player ────────────────────────────────────────
    for enemy in enemies:
        if not enemy.alive:
            continue
        if _circles_overlap(enemy.x, enemy.y, enemy.radius, px, py, pr):
            # Kamikaze: AOE explosion
            from game.entities.enemies.asura_kamikaze import AsuraKamikaze
            if isinstance(enemy, AsuraKamikaze) and not enemy.exploded:
                enemy.explode()
                hit = player.take_damage(enemy.explosion_damage)
                summary["kamikaze_exploded"] = True
                summary["explosions"].append((enemy.x, enemy.y, enemy.explosion_radius, (255, 60, 60)))
                if hit:
                    summary["player_hit"] = True
                # AOE: also hurt nearby enemies with the shockwave
                for other in enemies:
                    if other is not enemy and other.alive:
                        if _circles_overlap(enemy.x, enemy.y,
                                            enemy.explosion_radius,
                                            other.x, other.y, other.radius):
                            other.take_damage(20)
                            if other.is_dead():
                                summary["kills"] += 1
                                score_system.register_kill(other.score_value)
                                player.enemies_killed += 1
                                summary["explosions"].append((other.x, other.y, other.radius, (255, 120, 30)))
            else:
                # Normal contact damage
                contact_dmg = getattr(enemy, "contact_damage", PLAYER_CONTACT_DAMAGE)
                hit = player.take_damage(contact_dmg)
                if hit:
                    summary["player_hit"] = True
                    summary["hit_sparks"].append((player.x, player.y, (255, 100, 100)))

    # ── 4. Player ↔ power-ups ─────────────────────────────────────────────
    for pu in powerups[:]:
        if not pu.alive:
            continue
        if _circles_overlap(pu.x, pu.y, pu.radius, px, py, pr):
            player.apply_powerup(pu.type)
            summary["powerup_picked"].append(pu.type)
            summary["powerup_auras"].append((pu.x, pu.y, getattr(pu, "_color", (255, 220, 60))))
            pu.alive = False

    return summary


# ==============================================================================
# [31/77] MODULE: game/systems/duel_client.py
# ==============================================================================
"""
game/systems/duel_client.py
Background-thread SocketIO client for online 1v1 duels.
Sends local player inputs at 20Hz, receives opponent state.
"""
import threading
import time
from dataclasses import dataclass, field
from typing import Optional, Callable

@dataclass
class PlayerState:
    game_id: str = ""
    x: float = 450.0
    y: float = 300.0
    dx: float = 0.0
    dy: float = 0.0
    hp: int = 100
    max_hp: int = 100
    firing: bool = False
    dash: bool = False
    last_updated: float = 0.0

@dataclass  
class DuelState:
    local: PlayerState = field(default_factory=PlayerState)
    opponent: PlayerState = field(default_factory=PlayerState)
    connected: bool = False
    opponent_connected: bool = False
    duel_ended: bool = False
    winner_game_id: str = ""
    error: str = ""

class DuelClient:
    """Thread-safe SocketIO client. Create once, call connect(), then use send_input() each frame."""
    
    def __init__(self, api_url: str, token: str, room_code: str, game_id: str, ship_class: str):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.room_code = room_code
        self.game_id = game_id
        self.ship_class = ship_class
        self.state = DuelState()
        self.state.local.game_id = game_id
        self._sio = None
        self._thread: Optional[threading.Thread] = None
        self._last_send = 0.0
        self._lock = threading.Lock()
        self._on_duel_end: Optional[Callable] = None

    def connect(self, on_duel_end: Optional[Callable] = None) -> None:
        self._on_duel_end = on_duel_end
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        try:
            import socketio as sio_lib
            self._sio = sio_lib.Client(reconnection=True, reconnection_attempts=5)
            
            @self._sio.event
            def connect():
                with self._lock:
                    self.state.connected = True
                self._sio.emit("join_duel", {
                    "token": self.token,
                    "room_code": self.room_code,
                    "game_id": self.game_id,
                    "ship_class": self.ship_class,
                })

            @self._sio.event
            def disconnect():
                with self._lock:
                    self.state.connected = False

            @self._sio.on("player_joined")
            def on_player_joined(data):
                if data.get("game_id") != self.game_id:
                    with self._lock:
                        self.state.opponent.game_id = data.get("game_id", "")
                        self.state.opponent_connected = True

            @self._sio.on("opponent_state")
            def on_opponent_state(data):
                with self._lock:
                    op = self.state.opponent
                    op.x = float(data.get("x", op.x))
                    op.y = float(data.get("y", op.y))
                    op.dx = float(data.get("dx", 0))
                    op.dy = float(data.get("dy", 0))
                    op.firing = bool(data.get("firing", False))
                    op.dash = bool(data.get("dash", False))
                    op.last_updated = time.time()

            @self._sio.on("hp_update")
            def on_hp_update(data):
                with self._lock:
                    for entry in data.get("players", []):
                        if entry["game_id"] == self.game_id:
                            self.state.local.hp = entry["hp"]
                        else:
                            self.state.opponent.hp = entry["hp"]

            @self._sio.on("duel_end")
            def on_duel_end(data):
                with self._lock:
                    self.state.duel_ended = True
                    self.state.winner_game_id = data.get("winner_game_id", "")
                if self._on_duel_end:
                    self._on_duel_end(data)

            @self._sio.on("duel_pong")
            def on_pong(data):
                pass  # latency measurement placeholder

            self._sio.connect(self.api_url, transports=["websocket", "polling"])
            self._sio.wait()
        except Exception as exc:
            with self._lock:
                self.state.error = str(exc)
                self.state.connected = False

    def send_input(self, x: float, y: float, dx: float, dy: float, firing: bool, dash: bool) -> None:
        """Call from game loop — throttled to 20 sends/second."""
        now = time.time()
        if now - self._last_send < 0.05:
            return
        self._last_send = now
        with self._lock:
            self.state.local.x = x
            self.state.local.y = y
        if self._sio and self._sio.connected:
            try:
                self._sio.emit("player_input", {
                    "x": round(x, 1),
                    "y": round(y, 1),
                    "dx": round(dx, 2),
                    "dy": round(dy, 2),
                    "firing": firing,
                    "dash": dash,
                })
            except Exception:
                pass

    def report_hit(self, damage: int) -> None:
        """Call when local player's bullet hits the opponent."""
        with self._lock:
            opponent_id = self.state.opponent.game_id
        if self._sio and self._sio.connected and opponent_id:
            try:
                self._sio.emit("hit_registered", {
                    "target_game_id": opponent_id,
                    "damage": min(50, max(1, int(damage))),
                })
            except Exception:
                pass

    def get_state(self) -> DuelState:
        with self._lock:
            import copy
            return copy.deepcopy(self.state)

    def disconnect(self) -> None:
        if self._sio:
            try:
                self._sio.disconnect()
            except Exception:
                pass


# ==============================================================================
# [32/77] MODULE: game/systems/environmental_hazards.py
# ==============================================================================
"""
game/systems/environmental_hazards.py
Dynamic realm-specific cosmic hazards and environmental anomalies.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT


class EnvironmentalHazardManager:
    def __init__(self):
        self.asteroids: list[dict] = []
        self.solar_beams: list[dict] = []
        self.spawn_timer = 0.0

    def update(self, delta_time: float, wave_num: int, player, enemies: list, bullets: list) -> None:
        realm_id = ((wave_num - 1) % 20) + 1
        self.spawn_timer += delta_time

        # ── Dandaka Void (Waves 7–9): Astral Crystal Asteroids ─────────
        if 7 <= realm_id <= 9:
            if self.spawn_timer >= 3.5 and len(self.asteroids) < 4:
                self.spawn_timer = 0.0
                self.asteroids.append({
                    "x": random.uniform(100, WIDTH - 100),
                    "y": HEIGHT + 40,
                    "vx": random.uniform(-15, 15),
                    "vy": random.uniform(-25, -45),
                    "radius": random.uniform(22, 36),
                    "hp": 60,
                    "rot": 0.0,
                })

        for ast in self.asteroids:
            ast["x"] += ast["vx"] * delta_time
            ast["y"] += ast["vy"] * delta_time
            ast["rot"] += 20 * delta_time

            # Bullet collisions with asteroids (acts as tactical cover)
            for b in bullets:
                if b.alive and math.hypot(b.x - ast["x"], b.y - ast["y"]) < b.radius + ast["radius"]:
                    b.alive = False
                    ast["hp"] -= 20

        self.asteroids = [a for a in self.asteroids if a["hp"] > 0 and a["y"] > -50]

        # ── Swarga (Waves 1–3): Celestial Solar Rays ───────────────────
        if 1 <= realm_id <= 3:
            if self.spawn_timer >= 5.5 and len(self.solar_beams) < 2:
                self.spawn_timer = 0.0
                self.solar_beams.append({
                    "x": random.uniform(150, WIDTH - 150),
                    "w": 35,
                    "timer": 2.2,
                    "warning": True,
                })

        for beam in self.solar_beams:
            beam["timer"] -= delta_time
            if beam["timer"] < 1.0:
                beam["warning"] = False
                # Damage anything inside active solar ray
                if abs(player.x - beam["x"]) < beam["w"] and not player.is_dashing:
                    player.take_damage(1)  # Light continuous burn

        self.solar_beams = [b for b in self.solar_beams if b["timer"] > 0]

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        # Draw Asteroids
        for ast in self.asteroids:
            arcade.draw_circle_filled(ast["x"] + ox, ast["y"] + oy, ast["radius"], (70, 45, 95))
            arcade.draw_circle_outline(ast["x"] + ox, ast["y"] + oy, ast["radius"], (140, 90, 190), 2)
            arcade.draw_circle_filled(ast["x"] + ox - 4, ast["y"] + oy + 4, ast["radius"] * 0.4, (95, 65, 130))

        # Draw Solar Beams
        for beam in self.solar_beams:
            bx = beam["x"] + ox
            bw = beam["w"]
            if beam["warning"]:
                arcade.draw_lrbt_rectangle_filled(bx - bw // 2, bx + bw // 2, 0, HEIGHT, (255, 220, 100, 35))
                arcade.draw_line(bx, 0, bx, HEIGHT, (255, 240, 150, 120), 1)
            else:
                arcade.draw_lrbt_rectangle_filled(bx - bw // 2, bx + bw // 2, 0, HEIGHT, (255, 235, 120, 160))
                arcade.draw_lrbt_rectangle_filled(bx - bw // 4, bx + bw // 4, 0, HEIGHT, (255, 255, 255, 220))


# ==============================================================================
# [33/77] MODULE: game/systems/floating_text.py
# ==============================================================================
"""
game/systems/floating_text.py
Floating combat numbers and battle popup notifications.
Renders rising damage numbers, combo milestone tags, and ability ready popups.
"""
import random
import arcade


class FloatingNumber:
    __slots__ = ("text", "x", "y", "vx", "vy", "life", "max_life", "color", "font_size", "scale")

    def __init__(self, text: str, x: float, y: float, color: tuple,
                 life: float = 0.65, font_size: int = 12, is_crit: bool = False):
        self.text = text
        self.x = x + random.uniform(-8, 8)
        self.y = y + random.uniform(-4, 4)
        self.vx = random.uniform(-15, 15)
        self.vy = random.uniform(40, 75) if not is_crit else random.uniform(60, 95)
        self.life = life
        self.max_life = life
        self.color = color
        self.font_size = font_size if not is_crit else font_size + 4
        self.scale = 1.3 if is_crit else 1.0

    def update(self, delta_time: float) -> bool:
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.vy *= 0.94
        self.life -= delta_time
        return self.life > 0

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        frac = max(0.0, self.life / self.max_life)
        alpha = int(255 * min(1.0, frac * 1.5))
        r, g, b = self.color[:3]
        arcade.draw_text(
            self.text,
            self.x + ox, self.y + oy,
            (r, g, b, alpha),
            font_size=self.font_size,
            bold=True,
            anchor_x="center",
            anchor_y="center"
        )


class FloatingTextManager:
    def __init__(self):
        self.numbers: list[FloatingNumber] = []

    def update(self, delta_time: float) -> None:
        self.numbers = [n for n in self.numbers if n.update(delta_time)]

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        for n in self.numbers:
            n.draw(ox, oy)

    def spawn_damage(self, x: float, y: float, amount: int, is_crit: bool = False,
                     color: tuple = None) -> None:
        if color is None:
            color = (255, 220, 50) if is_crit else (255, 160, 60)
        text = f"{amount}" if not is_crit else f"★ {amount}!"
        self.numbers.append(FloatingNumber(text, x, y, color=color, is_crit=is_crit))

    def spawn_combo(self, x: float, y: float, combo: int) -> None:
        if combo >= 3:
            self.numbers.append(FloatingNumber(
                f"×{combo} COMBO!", x, y + 16,
                color=(255, 100, 220), life=0.8, font_size=13, is_crit=True
            ))

    def spawn_notification(self, x: float, y: float, text: str, color: tuple = (100, 220, 255)) -> None:
        self.numbers.append(FloatingNumber(text, x, y, color=color, life=0.9, font_size=12, is_crit=True))


# ==============================================================================
# [34/77] MODULE: game/systems/leaderboard_client.py
# ==============================================================================
"""
game/systems/leaderboard_client.py
Asynchronous network client for the Vimana Wars Leaderboard API.
Executes all HTTP calls on background daemon threads so the game thread
never drops frames or freezes on network latency/offline mode.
"""
import threading
import requests
from constants import LEADERBOARD_API_URL, NETWORK_TIMEOUT


class LeaderboardClient:
    """
    Non-blocking client for online score submissions and queries.
    """

    def __init__(self, api_url: str = LEADERBOARD_API_URL):
        self.api_url = api_url.rstrip("/")
        self._lock = threading.Lock()
        self.is_loading = False
        self.last_error: str | None = None
        # The menu reads this state every frame.  Keep it separate from
        # ``last_error`` so a previous failed request cannot make a later
        # successful health check look offline (and so the menu does not need
        # to perform network I/O during drawing).
        self._online = False
        self.top_scores: list[dict] = []
        self.submission_success = False

    def is_online(self) -> bool:
        """Return the last known API reachability without doing network I/O."""
        with self._lock:
            return self._online

    def _set_online(self, online: bool) -> None:
        with self._lock:
            self._online = bool(online)

    def check_health(self, on_complete=None) -> None:
        """Check the API asynchronously for the menu's online/offline badge."""
        def _worker():
            online = False
            error = None
            try:
                resp = requests.get(self.api_url, timeout=NETWORK_TIMEOUT)
                online = resp.status_code == 200
                if not online:
                    error = f"API returned {resp.status_code}"
            except requests.exceptions.RequestException:
                error = "API offline"
            self._set_online(online)
            if on_complete:
                on_complete(online, error)

        threading.Thread(target=_worker, daemon=True).start()

    @staticmethod
    def _auth_headers() -> dict:
        from game.systems import save_system
        token = save_system.load().get("auth_token", "")
        return {"Authorization": f"Bearer {token}"} if token else {}

    @staticmethod
    def _merge_profile(profile: dict) -> None:
        from game.systems import save_system
        if not isinstance(profile, dict):
            return
        data = save_system.load()
        max_keys = {
            "high_score", "last_wave", "last_realm", "total_kills", "games_played",
            "total_damage", "best_combo", "total_boons", "playtime_seconds",
            "endless_high_wave", "endless_high_score",
        }
        union_keys = {"realm_unlock_seen", "bosses_defeated", "ships_mastered", "achievements"}
        for key in save_system.profile_for_sync().keys():
            if key in profile:
                if key in max_keys:
                    try:
                        data[key] = max(data.get(key, 0), profile[key])
                    except (TypeError, ValueError):
                        pass
                elif key in union_keys:
                    data[key] = sorted(set(data.get(key) or []) | set(profile[key] or []))
                else:
                    data[key] = profile[key]
        save_system.save(data)

    @staticmethod
    def _save_account(token: str, user: dict) -> None:
        from game.systems import save_system
        data = save_system.load()
        data["auth_token"] = token
        data["game_id"] = user.get("game_id", "")
        data["account_email"] = user.get("email", "")
        if user.get("player_name"):
            data["player_name"] = user["player_name"]
        save_system.save(data)

    @staticmethod
    def current_account() -> dict | None:
        from game.systems import save_system
        data = save_system.load()
        if not data.get("auth_token") or not data.get("game_id"):
            return None
        return {
            "game_id": data.get("game_id", ""),
            "email": data.get("account_email", ""),
            "player_name": data.get("player_name", "Warrior"),
        }

    def _account_request(self, endpoint: str, payload: dict, on_complete=None) -> None:
        """Run register/login without blocking the Arcade render thread."""
        with self._lock:
            self.is_loading = True
            self.last_error = None

        def _worker():
            success = False
            error = None
            user = None
            try:
                resp = requests.post(
                    f"{self.api_url}{endpoint}",
                    json=payload,
                    timeout=NETWORK_TIMEOUT,
                )
                body = resp.json() if resp.content else {}
                if resp.status_code in (200, 201) and body.get("success"):
                    success = True
                    self._set_online(True)
                    user = body.get("user") or {}
                    user["verification_required"] = bool(body.get("verification_required"))
                    if body.get("verification_token"):
                        user["verification_token"] = body["verification_token"]
                    if body.get("token"):
                        self._save_account(body["token"], user)
                        # Pull cloud progression after authentication. This runs
                        # independently so login remains fast when the profile is empty.
                        self.sync_profile()
                else:
                    self._set_online(True)
                    error = body.get("error", f"Account request failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                self._set_online(False)
                error = "Account server offline — guest mode is still available"
            finally:
                with self._lock:
                    self.last_error = error
                    self.is_loading = False
                if on_complete:
                    on_complete(success, error, user)

        threading.Thread(target=_worker, daemon=True).start()

    def register(self, email: str, password: str, player_name: str,
                 on_complete=None) -> None:
        self._account_request(
            "/auth/register",
            {"email": email, "password": password, "player_name": player_name},
            on_complete,
        )

    def login(self, email: str, password: str, on_complete=None) -> None:
        self._account_request(
            "/auth/login", {"email": email, "password": password}, on_complete
        )

    def _action_request(self, endpoint: str, payload: dict, on_complete=None) -> None:
        """Run verification/reset calls without blocking the game thread."""
        def _worker():
            success, error, body = False, None, {}
            try:
                resp = requests.post(f"{self.api_url}{endpoint}", json=payload, timeout=NETWORK_TIMEOUT)
                body = resp.json() if resp.content else {}
                if resp.status_code == 200 and body.get("success"):
                    success = True
                    self._set_online(True)
                    if body.get("token") and body.get("user"):
                        self._save_account(body["token"], body["user"])
                else:
                    self._set_online(True)
                    error = body.get("error", f"Account action failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                self._set_online(False)
                error = "Account server offline"
            if on_complete:
                on_complete(success, error, body)

        threading.Thread(target=_worker, daemon=True).start()

    def verify_email(self, token: str, on_complete=None) -> None:
        self._action_request("/auth/verify-email", {"token": token}, on_complete)

    def request_password_reset(self, email: str, on_complete=None) -> None:
        self._action_request("/auth/request-password-reset", {"email": email}, on_complete)

    def reset_password(self, token: str, password: str, on_complete=None) -> None:
        self._action_request(
            "/auth/reset-password", {"token": token, "password": password}, on_complete
        )

    def _multiplayer_request(self, method: str, endpoint: str,
                             payload: dict | None = None, on_complete=None) -> None:
        """Run lobby requests without blocking the Arcade render loop."""
        headers = self._auth_headers()

        def _worker():
            success, error, body = False, None, {}
            try:
                resp = requests.request(
                    method, f"{self.api_url}{endpoint}", json=payload,
                    headers=headers, timeout=NETWORK_TIMEOUT,
                )
                body = resp.json() if resp.content else {}
                if resp.status_code in (200, 201):
                    success = True
                    self._set_online(True)
                else:
                    self._set_online(True)
                    error = body.get("error", f"Multiplayer request failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                self._set_online(False)
                error = "Multiplayer server offline — campaign remains available"
            if on_complete:
                on_complete(success, error, body)

        threading.Thread(target=_worker, daemon=True).start()

    def list_lobbies(self, on_complete=None) -> None:
        self._multiplayer_request("GET", "/multiplayer/lobbies", on_complete=on_complete)

    def create_lobby(self, mode="campaign", max_players=2,
                     ship_class="pushpaka", on_complete=None) -> None:
        self._multiplayer_request(
            "POST", "/multiplayer/lobbies",
            {"mode": mode, "max_players": max_players, "ship_class": ship_class},
            on_complete,
        )

    def get_lobby(self, code: str, on_complete=None) -> None:
        self._multiplayer_request("GET", f"/multiplayer/lobbies/{code}", on_complete=on_complete)

    def join_lobby(self, code: str, ship_class="pushpaka", on_complete=None) -> None:
        self._multiplayer_request(
            "POST", f"/multiplayer/lobbies/{code}/join",
            {"ship_class": ship_class}, on_complete,
        )

    def set_lobby_ready(self, code: str, ready=True, on_complete=None) -> None:
        self._multiplayer_request(
            "POST", f"/multiplayer/lobbies/{code}/ready",
            {"ready": ready}, on_complete,
        )

    def start_lobby(self, code: str, on_complete=None) -> None:
        self._multiplayer_request("POST", f"/multiplayer/lobbies/{code}/start", on_complete=on_complete)

    def leave_lobby(self, code: str, on_complete=None) -> None:
        self._multiplayer_request("POST", f"/multiplayer/lobbies/{code}/leave", on_complete=on_complete)

    def logout(self, on_complete=None) -> None:
        """Clear the local session even if the server is unreachable."""
        from game.systems import save_system
        headers = self._auth_headers()
        data = save_system.load()
        data["auth_token"] = ""
        data["game_id"] = ""
        data["account_email"] = ""
        save_system.save(data)

        def _worker():
            error = None
            try:
                requests.post(f"{self.api_url}/auth/logout", headers=headers, timeout=NETWORK_TIMEOUT)
            except requests.exceptions.RequestException:
                error = "Signed out locally"
            if on_complete:
                on_complete(error)
        threading.Thread(target=_worker, daemon=True).start()

    def sync_profile(self, on_complete=None) -> None:
        """Pull authenticated progression/achievements into the local save."""
        headers = self._auth_headers()
        if not headers:
            if on_complete:
                on_complete(False, "Not signed in", None)
            return

        def _worker():
            success, error, profile = False, None, None
            try:
                resp = requests.get(f"{self.api_url}/account/profile", headers=headers, timeout=NETWORK_TIMEOUT)
                body = resp.json() if resp.content else {}
                if resp.status_code == 200:
                    profile = body.get("profile") or {}
                    self._merge_profile(profile)
                    success = True
                    self._set_online(True)
                else:
                    self._set_online(True)
                    error = body.get("error", f"Profile sync failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                self._set_online(False)
                error = "Cloud profile unavailable — local progress is safe"
            if on_complete:
                on_complete(success, error, profile)

        threading.Thread(target=_worker, daemon=True).start()

    def push_profile(self, on_complete=None) -> None:
        """Push the local gameplay profile to the authenticated account."""
        headers = self._auth_headers()
        if not headers:
            if on_complete:
                on_complete(False, "Not signed in")
            return
        from game.systems import save_system
        payload = {"profile": save_system.profile_for_sync()}

        def _worker():
            success, error = False, None
            try:
                resp = requests.put(
                    f"{self.api_url}/account/profile", json=payload,
                    headers=headers, timeout=NETWORK_TIMEOUT,
                )
                body = resp.json() if resp.content else {}
                if resp.status_code == 200:
                    success = True
                    self._set_online(True)
                else:
                    self._set_online(True)
                    error = body.get("error", f"Profile sync failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                self._set_online(False)
                error = "Cloud profile unavailable — local progress is safe"
            if on_complete:
                on_complete(success, error)

        threading.Thread(target=_worker, daemon=True).start()

    def fetch_account_stats(self, on_complete=None) -> None:
        """Fetch server-calculated stats for the signed-in account."""
        headers = self._auth_headers()
        if not headers:
            if on_complete:
                on_complete(None, "Not signed in")
            return

        def _worker():
            stats, error = None, None
            try:
                resp = requests.get(f"{self.api_url}/account/stats", headers=headers, timeout=NETWORK_TIMEOUT)
                body = resp.json() if resp.content else {}
                if resp.status_code == 200:
                    stats = body
                    self._set_online(True)
                else:
                    self._set_online(True)
                    error = body.get("error", f"Stats request failed ({resp.status_code})")
            except (requests.exceptions.RequestException, ValueError):
                self._set_online(False)
                error = "Online stats unavailable"
            if on_complete:
                on_complete(stats, error)

        threading.Thread(target=_worker, daemon=True).start()

    def fetch_top(self, limit: int = 10, difficulty: str | None = None, on_complete=None) -> None:
        """
        Fetch top leaderboard records asynchronously.
        """
        with self._lock:
            self.is_loading = True
            self.last_error = None

        def _worker():
            scores = []
            err = None
            try:
                params = {"limit": limit}
                if difficulty:
                    params["difficulty"] = difficulty

                resp = requests.get(
                    f"{self.api_url}/scores/top",
                    params=params,
                    timeout=NETWORK_TIMEOUT
                )
                if resp.status_code == 200:
                    data = resp.json()
                    scores = list(data.get("leaderboard", []))
                    err = None
                    self._set_online(True)
                else:
                    self._set_online(True)
                    err = f"Server returned {resp.status_code}"
            except requests.exceptions.RequestException:
                self._set_online(False)
                err = "Leaderboard offline (Could not connect to server)"
                scores = []
            finally:
                with self._lock:
                    self.top_scores = list(scores)
                    self.last_error = err
                    self.is_loading = False
                if on_complete:
                    on_complete(scores, err)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()

    def submit_score(self, player_name: str, score: int, level_reached: int,
                     difficulty: str = "normal", ship_class: str = "pushpaka",
                     stats: dict | None = None,
                     on_complete=None) -> None:
        """
        Submit a score record asynchronously.
        """
        with self._lock:
            self.is_loading = True
            self.last_error = None
            self.submission_success = False

        def _worker():
            success = False
            err = None
            try:
                payload = {
                    "player_name": player_name,
                    "score": score,
                    "level_reached": level_reached,
                    "difficulty": difficulty,
                    "ship_class": ship_class,
                }
                run_stats = stats or {}
                payload["kills"] = max(0, int(run_stats.get("kills", 0)))
                payload["total_damage"] = max(0, int(run_stats.get("total_damage", 0)))
                payload["duration_seconds"] = max(0.0, float(run_stats.get("duration_seconds", 0)))
                resp = requests.post(
                    f"{self.api_url}/scores",
                    json=payload,
                    headers=self._auth_headers(),
                    timeout=NETWORK_TIMEOUT
                )
                if resp.status_code == 201:
                    success = True
                    err = None
                    self._set_online(True)
                else:
                    success = False
                    self._set_online(True)
                    try:
                        err = resp.json().get("error", f"Submission error {resp.status_code}")
                    except ValueError:
                        err = f"Submission error {resp.status_code}"
            except requests.exceptions.RequestException:
                self._set_online(False)
                success = False
                err = "Server offline — score saved locally"
            finally:
                with self._lock:
                    self.submission_success = success
                    self.last_error = err
                    self.is_loading = False
                if on_complete:
                    on_complete(success, err)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()


# Global singleton instance for easy access
leaderboard_client = LeaderboardClient()


# ==============================================================================
# [35/77] MODULE: game/systems/particles.py
# ==============================================================================
"""
game/systems/particles.py
High-performance procedural particle system for arcade visual juice.
Handles engine trails, bullet hit sparks, explosions, and powerup auras.
"""
import math
import random
import arcade


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "radius", "color", "decay_rate")

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 life: float, radius: float, color: tuple[int, int, int],
                 decay_rate: float = 0.96):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.radius = radius
        self.color = color
        self.decay_rate = decay_rate

    def update(self, delta_time: float) -> bool:
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
        self.vx *= self.decay_rate
        self.vy *= self.decay_rate
        self.life -= delta_time
        return self.life > 0

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        frac = max(0.0, self.life / self.max_life)
        alpha = int(255 * frac)
        r, g, b = self.color
        arcade.draw_circle_filled(self.x + ox, self.y + oy, self.radius * frac, (r, g, b, alpha))


class ParticleManager:
    def __init__(self):
        self.particles: list[Particle] = []
        self._trail_timer = 0.0
        self.quality_multiplier = 1.0
        self.reduced_flashes = False
        self.reload_settings()

    def reload_settings(self) -> None:
        try:
            from game.systems import save_system
            settings = save_system.load()
            q = settings.get("particles", "high")
            self.reduced_flashes = bool(settings.get("reduced_flashes", False))
            if q == "low":
                self.quality_multiplier = 0.4
            elif q == "off":
                self.quality_multiplier = 0.0
            else:
                self.quality_multiplier = 1.0
        except Exception:
            self.quality_multiplier = 1.0
            self.reduced_flashes = False

    def _flash_count(self, count: int, minimum: int = 1) -> int:
        if self.quality_multiplier <= 0:
            return 0
        flash_scale = 0.45 if self.reduced_flashes else 1.0
        return max(minimum, int(count * self.quality_multiplier * flash_scale))

    def update(self, delta_time: float) -> None:
        self.particles = [p for p in self.particles if p.update(delta_time)]

    def draw(self, ox: float = 0.0, oy: float = 0.0) -> None:
        for p in self.particles:
            p.draw(ox, oy)

    def spawn_engine_trail(self, x: float, y: float, angle_deg: float) -> None:
        """Spawns glowing propulsion sparks behind the player vimana."""
        if self.quality_multiplier <= 0.0:
            return
        if self.quality_multiplier < 1.0 and random.random() > self.quality_multiplier:
            return
        rad = math.radians(angle_deg + 180 + random.uniform(-25, 25))
        speed = random.uniform(30, 90)
        color = random.choice([
            (100, 180, 255),  # blue plasma
            (255, 200, 80),   # golden ignition
            (255, 120, 30),   # orange flare
        ])
        self.particles.append(Particle(
            x=x, y=y,
            vx=math.cos(rad) * speed,
            vy=math.sin(rad) * speed,
            life=random.uniform(0.15, 0.35),
            radius=random.uniform(2.5, 4.5),
            color=color,
            decay_rate=0.92
        ))

    def spawn_hit_sparks(self, x: float, y: float, count: int = 5,
                         color: tuple = (255, 240, 100)) -> None:
        """Spawns sharp sparks upon bullet impacts."""
        adj_count = self._flash_count(count)
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 220)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.10, 0.25),
                radius=random.uniform(1.8, 3.2),
                color=color,
                decay_rate=0.88
            ))

    def spawn_explosion(self, x: float, y: float, radius: float = 20, count: int = 24,
                        base_color: tuple = (255, 120, 30)) -> None:
        """Spawns an energetic burst of fiery debris and shockwave particles."""
        adj_count = self._flash_count(count, minimum=2)
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            dist_factor = random.uniform(0.5, 1.8)
            speed = random.uniform(40, 160) * dist_factor
            palette = [
                base_color,
                (255, 230, 70),   # bright yellow
                (255, 60, 20),    # deep fiery red
                (180, 180, 180),  # smoke
            ]
            self.particles.append(Particle(
                x=x + random.uniform(-5, 5),
                y=y + random.uniform(-5, 5),
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.3, 0.65),
                radius=random.uniform(3.0, radius * 0.45),
                color=random.choice(palette),
                decay_rate=0.93
            ))

    def spawn_powerup_sparkle(self, x: float, y: float, color: tuple) -> None:
        """Spawns celestial aura sparkles when picking up an Astra."""
        adj_count = self._flash_count(30, minimum=4)
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(60, 200)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.4, 0.8),
                radius=random.uniform(2.5, 5.0),
                color=color,
                decay_rate=0.90
            ))

    def spawn_dash_flash(self, x: float, y: float, color: tuple = (140, 220, 255)) -> None:
        """Spawns a radiant flare burst at the start of a dash."""
        adj_count = self._flash_count(18, minimum=4)
        for _ in range(adj_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(120, 340)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.18, 0.35),
                radius=random.uniform(3.0, 6.0),
                color=color,
                decay_rate=0.85
            ))

    def spawn_dash_shockwave(self, x: float, y: float, color: tuple = (200, 240, 255)) -> None:
        """Spawns a ring-expanding deceleration shockwave at the end of a dash."""
        adj_count = self._flash_count(22, minimum=6)
        for i in range(adj_count):
            angle = (i / max(1, adj_count)) * 2 * math.pi
            speed = random.uniform(70, 150)
            self.particles.append(Particle(
                x=x, y=y,
                vx=math.cos(angle) * speed,
                vy=math.sin(angle) * speed,
                life=random.uniform(0.2, 0.4),
                radius=random.uniform(2.5, 4.5),
                color=color,
                decay_rate=0.88
            ))


# ==============================================================================
# [36/77] MODULE: game/systems/save_system.py
# ==============================================================================
"""
game/systems/save_system.py
Local save/load using a JSON file in the user's app data directory.
Saves: high score, settings (volume, screen shake, particles, fullscreen, difficulty).
"""
import json
import os
from pathlib import Path

# Save file lives in user home directory under ~/.vimana_wars/
_SAVE_DIR  = Path(os.path.expanduser("~")) / ".vimana_wars"
_SAVE_FILE = _SAVE_DIR / "save.json"

_DEFAULTS = {
    "player_name":   "Warrior",
    "high_score":    0,
    "last_wave":     0,
    "difficulty":    "normal",   # "easy" | "normal" | "hard" | "endless"
    "last_ship":     "pushpaka",
    # Online identity is optional; guest play remains available offline.
    "auth_token":    "",
    "game_id":       "",
    "account_email": "",
    "last_realm":    1,
    "story_intro_seen": False,
    "realm_unlock_seen": [],
    "total_kills":   0,
    "games_played":  0,
    "total_damage":      0,            # lifetime damage dealt
    "best_combo":        1,            # highest single-run combo ever
    "total_boons":       0,            # total boons claimed across all runs
    "bosses_defeated":   [],           # list of boss ids the player has beaten
    "playtime_seconds":  0,            # total in-game time across sessions
    "ships_mastered":    [],           # ship ids used to clear campaign
    "volume":             80,         # 0 - 100 (master/legacy)
    "sfx_volume":         80,         # 0 - 100
    "music_volume":       80,         # 0 - 100
    "screen_shake":       "full",     # "full" | "low" | "off"
    "particles":          "high",     # "high" | "low"
    "reduced_flashes":    False,      # True | False (accessibility)
    "colorblind_mode":    "off",      # "off" | "protan" | "deutan" | "tritan"
    "fullscreen":         False,
    "endless_high_wave":  0,
    "endless_high_score": 0,
    "unlocked_ships":     ["pushpaka", "tripura", "garuda"],
}

_SYNC_KEYS = (
    "player_name", "high_score", "last_wave", "difficulty", "last_ship",
    "last_realm", "story_intro_seen", "realm_unlock_seen", "total_kills", "games_played",
    "total_damage", "best_combo", "total_boons", "bosses_defeated",
    "playtime_seconds", "ships_mastered", "achievements", "endless_high_wave",
    "endless_high_score",
)


def _ensure_dir() -> None:
    _SAVE_DIR.mkdir(parents=True, exist_ok=True)


def load() -> dict:
    """Return save data, falling back to defaults if the file doesn't exist."""
    _ensure_dir()
    if not _SAVE_FILE.exists():
        return dict(_DEFAULTS)
    try:
        with open(_SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, default in _DEFAULTS.items():
            data.setdefault(key, default)
        return data
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULTS)


def save(data: dict) -> None:
    """Write data dict to disk."""
    _ensure_dir()
    try:
        with open(_SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass   # graceful degradation — never crash over a save failure


def unlock_ship(ship_id: str) -> bool:
    """Unlock a ship by ID. Returns True if newly unlocked, False if already unlocked."""
    data = load()
    unlocked = data.get("unlocked_ships", ["pushpaka", "tripura", "garuda"])
    if ship_id in unlocked:
        return False
    unlocked.append(ship_id)
    data["unlocked_ships"] = unlocked
    save(data)
    return True

def get_unlocked_ships() -> list:
    data = load()
    return data.get("unlocked_ships", ["pushpaka", "tripura", "garuda"])


def profile_for_sync(data: dict = None) -> dict:
    """Return only safe gameplay state for authenticated cloud synchronization."""
    source = data if data is not None else load()
    return {key: source.get(key, _DEFAULTS.get(key)) for key in _SYNC_KEYS}


def update_after_game(score: int, wave: int, kills: int,
                      *, highest_combo: int = 1,
                      total_damage: int = 0,
                      boons_claimed: int = 0,
                      bosses_defeated: list = None,
                      ship_class: str = None,
                      campaign_cleared: bool = False) -> dict:
    """
    Convenience: load, update lifetime stats, save, return updated data.
    All new args are optional for backward compatibility.
    """
    data = load()
    data["high_score"]   = max(data["high_score"], score)
    data["last_wave"]    = max(data["last_wave"], wave)
    data["total_kills"] += kills
    data["games_played"] += 1
    data["total_damage"] += max(0, total_damage)
    data["best_combo"]   = max(data["best_combo"], max(1, highest_combo))
    data["total_boons"]  += max(0, boons_claimed)
    if bosses_defeated:
        existing = set(data.get("bosses_defeated") or [])
        for bid in bosses_defeated:
            existing.add(bid)
        data["bosses_defeated"] = sorted(existing)
    if ship_class and campaign_cleared:
        mastered = set(data.get("ships_mastered") or [])
        mastered.add(ship_class)
        data["ships_mastered"] = sorted(mastered)
    save(data)
    return data


def add_playtime(seconds: float) -> dict:
    """Accumulate playtime (called each frame from the active game view)."""
    if seconds <= 0:
        return load()
    data = load()
    data["playtime_seconds"] = float(data.get("playtime_seconds", 0)) + seconds
    save(data)
    return data


def get_difficulty() -> str:
    return load().get("difficulty", "normal")


def set_difficulty(level: str) -> None:
    assert level in ("easy", "normal", "hard", "endless"), f"Unknown difficulty: {level}"
    data = load()
    data["difficulty"] = level
    save(data)


# ==============================================================================
# [37/77] MODULE: game/systems/score_system.py
# ==============================================================================
"""
game/systems/score_system.py
Score tracking with combo multiplier.
Kills within COMBO_WINDOW seconds of each other chain the multiplier.
"""
from constants import COMBO_WINDOW, MAX_COMBO


class ScoreSystem:
    def __init__(self):
        self.score = 0
        self.combo = 1          # current multiplier
        self._combo_timer = 0.0  # counts down; reset on each kill
        self.highest_combo = 1

    def register_kill(self, base_score: int) -> int:
        """
        Call when an enemy dies. Returns the actual points awarded.
        """
        if self._combo_timer > 0:
            # Chain! Increment combo (cap at MAX_COMBO)
            self.combo = min(self.combo + 1, MAX_COMBO)
        else:
            # Reset to x1 for the first kill after a gap
            self.combo = 1

        self._combo_timer = COMBO_WINDOW
        self.highest_combo = max(self.highest_combo, self.combo)

        earned = base_score * self.combo
        self.score += earned
        return earned

    def update(self, delta_time: float) -> None:
        if self._combo_timer > 0:
            self._combo_timer -= delta_time
            if self._combo_timer <= 0:
                self._combo_timer = 0
                self.combo = 1   # combo expired

    @property
    def combo_active(self) -> bool:
        return self.combo > 1

    @property
    def combo_timer(self) -> float:
        return self._combo_timer

    @property
    def combo_timeout(self) -> float:
        return COMBO_WINDOW


# ==============================================================================
# [38/77] MODULE: game/systems/sound_manager.py
# ==============================================================================
"""
game/systems/sound_manager.py
Wraps arcade.Sound — silently skips missing files so the game never crashes
if a sound file hasn't been dropped in yet.

HOW TO ADD SOUNDS
─────────────────
1. Download free CC0 files from a reputable asset source and verify the license
2. Save them as WAV (preferred) or OGG into  assets/sounds/
3. Name them to match the keys in _SOUND_FILES below
4. Restart the game — they load automatically

Suggested search terms on Freesound:
  shoot.wav    → "laser shoot 8bit"
  hit.wav      → "damage hit player"
  explosion.wav→ "explosion arcade"
  powerup.wav  → "item pickup"
  boss_roar.wav→ "monster roar"
  victory.wav  → "fanfare win"
  game_over.wav→ "game over sting"
  wave_clear.wav → "stage clear jingle"
"""
import arcade
_ASSETS = Path(__file__).resolve().parent.parent.parent / "assets" / "sounds"
if not _ASSETS.exists():
    _ASSETS = Path(__file__).resolve().parent.parent.parent.parent / "assets" / "sounds"

_SOUND_FILES: dict[str, str] = {
    "shoot":         "shoot.wav",
    "dash":          "dash.wav",
    "hit":           "hit.wav",
    "explosion":     "explosion.wav",
    "powerup":       "powerup.wav",
    "boss_roar":     "boss_roar.wav",
    "victory":       "victory.wav",
    "game_over":     "game_over.wav",
    "wave_clear":    "wave_clear.wav",
    "ui_click":      "ui_click.wav",
    "warning_siren": "warning_siren.wav",
    "dodge_chime":   "dodge_chime.wav",
    "synergy":       "synergy.wav",
    # Optional CC0 Kenney variations.  The generated WAVs remain fallbacks.
    "shoot_online":  "online_laser_small.ogg",
    "hit_online":    "online_impact_metal.ogg",
    "explosion_online": "online_explosion_crunch.ogg",
    "dash_online":   "online_thruster_fire.ogg",
}
_MUSIC_FILE = _ASSETS / "combat_loop.mp3"


class SoundManager:
    """
    Create one instance (e.g. in GameView.__init__).
    Call play_*(volume) methods anywhere in the game.
    Auto-synthesizes clean procedural sounds if sound files are missing.
    """

    _music_player = None

    def __init__(self):
        try:
            from game.systems.audio_synthesizer import generate_all_sounds
            generate_all_sounds()
        except Exception:
            pass

        self._sounds: dict[str, arcade.Sound | None] = {}
        for key, filename in _SOUND_FILES.items():
            path = _ASSETS / filename
            try:
                self._sounds[key] = arcade.load_sound(str(path))
            except Exception:
                self._sounds[key] = None

        try:
            self._music = arcade.load_sound(str(_MUSIC_FILE), streaming=True)
        except Exception:
            self._music = None

        self.master_vol = 0.8
        self.sfx_vol = 0.8
        self.music_vol = 0.8
        self.reload_volume()

    def reload_volume(self) -> None:
        try:
            from game.systems import save_system
            data = save_system.load()
            self.master_vol = data.get("volume", 80) / 100.0
            self.sfx_vol = data.get("sfx_volume", data.get("volume", 80)) / 100.0
            self.music_vol = data.get("music_volume", data.get("volume", 80)) / 100.0
        except Exception:
            self.master_vol = 0.8
            self.sfx_vol = 0.8
            self.music_vol = 0.8

        if SoundManager._music_player is not None:
            try:
                SoundManager._music_player.volume = max(0.0, min(1.0, 0.24 * self.music_vol))
            except Exception:
                pass

    def start_music(self, volume: float = 0.24) -> None:
        """Start the looping combat bed once for the current application."""
        if self._music is None or SoundManager._music_player is not None:
            return
        final_vol = max(0.0, min(1.0, volume * self.music_vol))
        if final_vol <= 0.01:
            return
        try:
            SoundManager._music_player = arcade.play_sound(
                self._music, volume=final_vol, loop=True
            )
        except Exception:
            SoundManager._music_player = None

    @classmethod
    def stop_music(cls) -> None:
        """Stop the shared music player when leaving gameplay."""
        if cls._music_player is None:
            return
        try:
            arcade.stop_sound(cls._music_player)
        except Exception:
            pass
        finally:
            cls._music_player = None

    def _play(self, key: str, volume: float = 1.0) -> None:
        final_vol = max(0.0, min(1.0, volume * self.sfx_vol))
        sound = self._sounds.get(key)
        if sound is not None and final_vol > 0.01:
            try:
                arcade.play_sound(sound, volume=final_vol)
            except Exception:
                pass

    def _play_any(self, keys: tuple[str, ...], volume: float = 1.0) -> None:
        """Play the first loaded variant, keeping generated audio as fallback."""
        final_vol = max(0.0, min(1.0, volume * self.sfx_vol))
        if final_vol <= 0.01:
            return
        for key in keys:
            sound = self._sounds.get(key)
            if sound is None:
                continue
            try:
                arcade.play_sound(sound, volume=final_vol)
            except Exception:
                pass
            return

    def play_dash(self, volume: float = 0.55) -> None: self._play_any(("dash_online", "dash"), volume)

    # ── Convenience methods ──────────────────────────────────────────
    def play_shoot(self,         volume: float = 0.35) -> None: self._play_any(("shoot_online", "shoot"), volume)
    def play_hit(self,           volume: float = 0.70) -> None: self._play_any(("hit_online", "hit"), volume)
    def play_explosion(self,     volume: float = 0.80) -> None: self._play_any(("explosion_online", "explosion"), volume)
    def play_powerup(self,       volume: float = 1.00) -> None: self._play("powerup",       volume)
    def play_boss_roar(self,     volume: float = 1.00) -> None: self._play("boss_roar",     volume)
    def play_victory(self,       volume: float = 1.00) -> None: self._play("victory",       volume)
    def play_game_over(self,     volume: float = 0.90) -> None: self._play("game_over",     volume)
    def play_wave_clear(self,    volume: float = 0.70) -> None: self._play("wave_clear",    volume)
    def play_ui_click(self,      volume: float = 0.60) -> None: self._play("ui_click",      volume)
    def play_warning_siren(self, volume: float = 0.85) -> None: self._play("warning_siren", volume)
    def play_dodge_chime(self,   volume: float = 0.75) -> None: self._play("dodge_chime",   volume)
    def play_synergy(self,       volume: float = 1.00) -> None: self._play("synergy",       volume)


# ==============================================================================
# [39/77] MODULE: game/systems/wave_manager.py
# ==============================================================================
"""
game/systems/wave_manager.py
Controls wave progression, 3-2-1 countdowns, wave objectives, and diverse enemy fleet spawns.
"""
import random
from constants import (
    WAVE_CLEAR_DELAY,
    CAMPAIGN_FINAL_WAVE, CAMPAIGN_BOSS_WAVES,
    CAMPAIGN_MINI_BOSS_WAVES, POWERUP_SPAWN_EVERY_N_WAVES,
    MAX_POWERUPS_ACTIVE, get_realm_for_wave,
)


def _wave_config(wave_num: int) -> dict:
    effective = ((wave_num - 1) % CAMPAIGN_FINAL_WAVE) + 1

    if effective == 30:
        return {"boss": "hiranyakashipu"}
    elif effective == 25:
        return {"mini_boss": "hiranyakashipu_herald", "fast": 5, "tank": 2}
    elif effective == 20:
        return {"boss": "vritra"}
    elif effective == 15:
        return {"mini_boss": "mahishasura", "fast": 4, "tank": 1}
    elif effective == 10:
        return {"boss": "ravana"}
    elif effective == 5:
        return {"mini_boss": True, "fast": 3, "kamikaze": 2}

    configs = [
        {"fast": 5},                                          # 1
        {"fast": 6, "healer": 1},                             # 2
        {"fast": 6, "kamikaze": 3},                           # 3
        {"fast": 4, "tank": 2, "sniper": 1},                  # 4
        {"mini_boss": True, "fast": 3},                       # 5
        {"fast": 5, "tank": 2, "healer": 1, "kamikaze": 3},   # 6
        {"fast": 4, "ranged": 3, "sniper": 2},                # 7
        {"fast": 5, "tank": 3, "ranged": 2, "healer": 1},     # 8
        {"fast": 6, "tank": 3, "sniper": 2, "kamikaze": 4},   # 9
        {"boss": "ravana"},                                   # 10
        {"fast": 7, "ranged": 2, "kamikaze": 4},              # 11
        {"fast": 5, "tank": 3, "healer": 2, "sniper": 2},     # 12
        {"fast": 7, "ranged": 4, "sniper": 2, "kamikaze": 4}, # 13
        {"fast": 5, "tank": 4, "healer": 2, "sniper": 3},     # 14
        {"mini_boss": "mahishasura", "fast": 4, "tank": 1},   # 15
        {"fast": 8, "ranged": 4, "kamikaze": 5},              # 16
        {"fast": 6, "tank": 4, "healer": 2, "sniper": 3},     # 17
        {"fast": 8, "tank": 4, "ranged": 4, "kamikaze": 5},   # 18
        {"fast": 10, "ranged": 4, "sniper": 4, "healer": 2},  # 19
        {"boss": "vritra"},                                   # 20
        {"fast": 8, "ranged": 4, "kamikaze": 5},              # 21
        {"fast": 6, "tank": 4, "healer": 3, "sniper": 3},     # 22
        {"fast": 8, "tank": 4, "ranged": 4, "kamikaze": 6},   # 23
        {"fast": 10, "ranged": 5, "sniper": 4, "healer": 2},  # 24
        {"mini_boss": "hiranyakashipu_herald", "fast": 5, "tank": 2}, # 25
        {"fast": 9, "tank": 5, "ranged": 5, "kamikaze": 6, "healer": 3}, # 26
        {"fast": 10, "ranged": 6, "sniper": 5, "kamikaze": 6}, # 27
        {"fast": 8, "tank": 6, "healer": 4, "sniper": 5},     # 28
        {"fast": 12, "tank": 6, "ranged": 6, "kamikaze": 8, "sniper": 4}, # 29
        {"boss": "hiranyakashipu"},                           # 30
    ]
    return configs[effective - 1]


class WaveManager:
    def __init__(self, spawn_mult: float = 1.0, enemy_spd_mult: float = 1.0,
                 is_endless: bool = False, start_wave: int = 1):
        self.wave_number = max(0, int(start_wave) - 1)
        self.boss_alive = False
        self.boss_wave_cleared = False
        self._difficulty_mult = spawn_mult
        self.enemy_speed_mult = enemy_spd_mult
        self.is_endless = is_endless

        # State machine: CLEAR_PAUSE -> COUNTDOWN -> SPAWNING -> FIGHTING
        self._state = "CLEAR_PAUSE"
        self._timer = WAVE_CLEAR_DELAY
        self.announce_text = ""
        self.announce_subtitle = ""
        self.announce_alpha = 0
        self.countdown_val = 3

        # Objective & Enemy tracking
        self.current_objective = "Defeat all Asuras"
        self.total_wave_enemies = 0
        self.wave_time = 0.0
        self.took_damage_this_wave = False

        # Power-up spawning
        self._waves_since_powerup = 0

    def update(self, delta_time: float, enemies: list, powerups: list, player=None) -> None:
        if self._state == "COUNTDOWN":
            self._timer -= delta_time
            self.countdown_val = max(1, int(self._timer + 1))
            self.announce_alpha = max(0, min(255, int(255 * (self._timer / 2.0))))

            if self._timer <= 0:
                self._state = "SPAWNING"

        elif self._state == "SPAWNING":
            self._spawn_wave(enemies, player)
            self.total_wave_enemies = len(enemies)
            self._state = "FIGHTING"
            self.wave_time = 0.0
            self.took_damage_this_wave = False

        elif self._state == "FIGHTING":
            self.wave_time += delta_time
            all_dead = (len(enemies) == 0) or all(not e.alive for e in enemies)
            if all_dead:
                if self.boss_alive:
                    self.boss_alive = False
                    self._waves_since_powerup += 1
                    self._maybe_spawn_powerup(powerups)
                    if self.wave_number == CAMPAIGN_FINAL_WAVE and not self.is_endless:
                        self.boss_wave_cleared = True
                        return
                self._state = "CLEAR_PAUSE"
                self._timer = WAVE_CLEAR_DELAY

        elif self._state == "CLEAR_PAUSE":
            self._timer -= delta_time
            if self._timer <= 0:
                self._advance_wave()

    def _advance_wave(self) -> None:
        self.wave_number += 1
        realm = get_realm_for_wave(self.wave_number)

        if self.wave_number > CAMPAIGN_FINAL_WAVE:
            loops = (self.wave_number - 1) // CAMPAIGN_FINAL_WAVE
            self._difficulty_mult = 1.0 + loops * 0.3

        self._waves_since_powerup += 1

        wave_objectives = {
            1: "Eliminate Asura Chaser scouts [5 vessels]",
            2: "Priority Target: Eliminate the Support Healer!",
            3: "Evasive Action: Evade and destroy Kamikaze swarm",
            4: "Armor Piercing: Crack 2 Heavy Brutes & Snipers",
            5: "Defeat the Armored Titan Kumbhakarna",
            6: "Survive Crossfire: Clear mixed Asura armada",
            7: "Long-Range Threat: Neutralize backline Snipers",
            8: "Break the Phalanx: Dismantle Heavy Battlefleet",
            9: "Armageddon Swarm: Annihilate vanguard assault fleet",
            10: "Vanquish the Ten-Headed Demon King Ravana",
            11: "Break the Lanka blockade",
            12: "Survive the molten counterattack",
            13: "Cross the Setu Expanse under fire",
            14: "Crack the warlord escort fleet",
            15: "Defeat the buffalo-demon warlord Mahishasura",
            16: "Enter the Naraka Forge",
            17: "Destroy the foundry guardians",
            18: "Endure the forge armada",
            19: "Prepare the final astral assault",
            20: "Vanquish the storm-serpent Vritra",
            21: "Descend into Patala — Survive the Naga serpent vanguard",
            22: "The Naga War Corps — Break the serpent battle formation",
            23: "Vasuki's Guard — Defeat the Serpent King's elite defenders",
            24: "Brahmaloka Defenders — Breach the Creator's celestial fortress",
            25: "Herald of Hiranyakashipu — Defeat the Tyrant's advance herald",
            26: "Summit Assault — Storm the divine citadel battlements",
            27: "Vaikuntha Approach — Endure the final threshold guardians",
            28: "Gate Guardian Corps — Shatter the eternal gate defenses",
            29: "The Final Armada — Annihilate the Asura supreme fleet",
            30: "Vanquish the Indestructible Tyrant-Demon Hiranyakashipu",
        }

        effective = ((self.wave_number - 1) % CAMPAIGN_FINAL_WAVE) + 1
        self.current_objective = wave_objectives.get(effective, "Eliminate all incoming Asura vessels")

        if effective in (10, 20, 30):
            if effective == 30:
                self.announce_text = "FINAL BOSS — HIRANYAKASHIPU RISES!"
            elif effective == 20:
                self.announce_text = "BOSS WAVE — VRITRA RISES!"
            else:
                self.announce_text = "BOSS WAVE — RAVANA APPROACHES!"
            self.announce_subtitle = f"Realm of {realm['name']} • {realm['subtitle']}"
        elif effective in (5, 15, 25):
            if effective == 25:
                self.announce_text = "MINI-BOSS — HERALD OF THE TYRANT!"
            elif effective == 15:
                self.announce_text = "MINI-BOSS — MAHISHASURA CHARGES!"
            else:
                self.announce_text = "MINI-BOSS — KUMBHAKARNA AWAKENS!"
            self.announce_subtitle = f"Realm of {realm['name']} • {realm['subtitle']}"
        else:
            self.announce_text = f"Wave {self.wave_number}"
            self.announce_subtitle = f"Realm: {realm['name']} — {realm['subtitle']}"

        self._timer = 2.4
        self._state = "COUNTDOWN"

    def _spawn_wave(self, enemies: list, player=None) -> None:
        config = _wave_config(self.wave_number)

        if config.get("boss"):
            if config["boss"] == "hiranyakashipu":
                from game.entities.enemies.boss_hiranyakashipu import BossHiranyakashipu
                boss = BossHiranyakashipu()
            elif config["boss"] == "vritra":
                from game.entities.enemies.boss_vritra import BossVritra
                boss = BossVritra()
            else:
                from game.entities.enemies.boss_ravana import BossRavana
                boss = BossRavana()
            boss.speed *= self.enemy_speed_mult
            enemies.append(boss)
            self.boss_alive = True
            return

        if config.get("mini_boss"):
            if config["mini_boss"] == "hiranyakashipu_herald":
                from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
                mini = BossKumbhakarna()
                mini.hp *= 2.5
                mini.max_hp = mini.hp
            elif config["mini_boss"] == "mahishasura":
                from game.entities.enemies.boss_mahishasura import BossMahishasura
                mini = BossMahishasura()
            else:
                from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
                mini = BossKumbhakarna()
            mini.speed *= self.enemy_speed_mult
            enemies.append(mini)
            self.boss_alive = True

        mult = self._difficulty_mult
        from constants import WIDTH, HEIGHT
        px = player.x if player else WIDTH / 2
        py = player.y if player else HEIGHT / 2

        def add(cls, n):
            for _ in range(max(1, int(n * mult))):
                try:
                    e = cls(safe_player_x=px, safe_player_y=py)
                except TypeError:
                    e = cls()
                e.speed *= self.enemy_speed_mult
                if self.wave_number >= 3 and random.random() < 0.15:
                    e.hp *= 2
                    e.max_hp = e.hp
                    e.score_value *= 2
                    setattr(e, "is_elite", True)
                enemies.append(e)

        from game.entities.enemies.asura_fast     import AsuraFast
        from game.entities.enemies.asura_tank     import AsuraTank
        from game.entities.enemies.asura_ranged   import AsuraRanged
        from game.entities.enemies.asura_kamikaze import AsuraKamikaze
        from game.entities.enemies.asura_healer   import AsuraHealer
        from game.entities.enemies.asura_sniper   import AsuraSniper

        if config.get("fast"):     add(AsuraFast,     config["fast"])
        if config.get("tank"):     add(AsuraTank,     config["tank"])
        if config.get("ranged"):   add(AsuraRanged,   config["ranged"])
        if config.get("kamikaze"): add(AsuraKamikaze, config["kamikaze"])
        if config.get("healer"):   add(AsuraHealer,   config["healer"])
        if config.get("sniper"):   add(AsuraSniper,   config["sniper"])

    def _maybe_spawn_powerup(self, powerups: list) -> None:
        if len(powerups) >= MAX_POWERUPS_ACTIVE:
            return
        if self._waves_since_powerup >= POWERUP_SPAWN_EVERY_N_WAVES:
            from game.entities.powerup import PowerUp
            powerups.append(PowerUp())
            self._waves_since_powerup = 0

    @property
    def is_boss_wave(self) -> bool:
        effective = ((self.wave_number - 1) % CAMPAIGN_FINAL_WAVE) + 1
        return effective in CAMPAIGN_BOSS_WAVES

    @property
    def is_mini_boss_wave(self) -> bool:
        effective = ((self.wave_number - 1) % CAMPAIGN_FINAL_WAVE) + 1
        return effective in CAMPAIGN_MINI_BOSS_WAVES

    @property
    def is_announcing(self) -> bool:
        return self._state == "COUNTDOWN"

    @property
    def is_clearing(self) -> bool:
        return self._state == "CLEAR_PAUSE" and self.wave_number > 0

    @property
    def is_fighting(self) -> bool:
        return self._state == "FIGHTING"


# ==============================================================================
# [40/77] MODULE: game/ui/__init__.py
# ==============================================================================
# game/ui/__init__.py


# ==============================================================================
# [41/77] MODULE: game/ui/boss_bar.py
# ==============================================================================
"""
game/ui/boss_bar.py
BossBar class — full-width bar at the bottom of the screen while a Boss / Mini-Boss is alive.
Uses arcade.Text objects (no draw_text calls).
"""
import math
import arcade
from constants import WIDTH, COLOR_WHITE
from game.ui.vedic_theme import (
    RED, RED_BRIGHT, GOLD, MUTED, draw_chamfered_panel, draw_telemetry_ticks, draw_segmented_bar,
)


class BossBar:
    def __init__(self):
        self._label_name = arcade.Text(
            "", WIDTH // 2, 16,
            COLOR_WHITE, font_size=10, bold=True,
            anchor_x="center",
        )
        self._label_hp = arcade.Text(
            "", 18, 16,
            COLOR_WHITE, font_size=9,
        )

    def draw(self, boss) -> None:
        if not boss or not boss.alive:
            return

        bar_x, bar_y = 20, 14
        bar_w, bar_h = WIDTH - 40, 20
        frac = max(0.0, boss.hp / boss.max_hp)

        boss_name = getattr(boss, "name", "BOSS").upper()

        draw_chamfered_panel(bar_x - 6, bar_x + bar_w + 6, bar_y - 7,
                             bar_y + bar_h + 9, RED, fill=(22, 8, 18),
                             alpha=225, border_width=1, cut=6)
        draw_telemetry_ticks(bar_x, bar_x + bar_w, bar_y + bar_h + 5,
                             GOLD, count=19, height=3, alpha=65)
        arcade.draw_lrbt_rectangle_filled(bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, (30, 10, 10))

        # Fill — color shifts by phase or boss type
        if boss_name == "KUMBHAKARNA":
            fill_color = (210, 140, 20) if frac > 0.4 else (230, 60, 20)
        elif boss_name == "MAHISHASURA":
            fill_color = (200, 70, 30) if frac > 0.4 else (255, 30, 80)
        elif boss_name == "VRITRA":
            phase_fills = [(100, 220, 255), (180, 80, 255), (255, 40, 140)]
            fill_color = phase_fills[min(2, max(0, getattr(boss, "phase", 1) - 1))]
        else:
            phase_fills = [(200, 0, 60), (255, 80, 0), (220, 0, 200)]
            fill_color = phase_fills[getattr(boss, "phase", 1) - 1]

        if frac > 0:
            # Ghost trail — slightly wider semi-transparent version of fill
            arcade.draw_lrbt_rectangle_filled(
                bar_x - 2, bar_x + bar_w * frac + 2,
                bar_y, bar_y + bar_h,
                (*fill_color[:3], 60))
            # Segmented fill with 20 segments
            draw_segmented_bar(bar_x, bar_x + bar_w, bar_y, bar_y + bar_h,
                               frac, fill_color, segments=20, gap=2)

        phase = max(1, int(getattr(boss, "phase", 1)))
        phase_count = 3 if boss_name in ("RAVANA", "VRITRA") else 2
        phase_count = max(phase_count, phase)
        phase_width = bar_w / phase_count
        for phase_index in range(phase_count):
            phase_left = bar_x + phase_index * phase_width
            phase_right = phase_left + phase_width - 3
            phase_color = GOLD if phase_index < phase else (*MUTED, 120)
            arcade.draw_lrbt_rectangle_outline(
                phase_left, phase_right, bar_y - 5, bar_y + bar_h + 5,
                phase_color, 1)

        thresholds = ((0.66, "P2"), (0.33, "P3"))
        for threshold, p_tag in thresholds:
            mx = bar_x + bar_w * threshold
            marker_col = GOLD if frac > threshold else (*MUTED, 180)
            arcade.draw_line(mx, bar_y - 2, mx, bar_y + bar_h + 2, marker_col, 2)
            arcade.draw_triangle_filled(mx, bar_y + bar_h + 6, mx - 4, bar_y + bar_h, mx + 4, bar_y + bar_h, marker_col)
            arcade.draw_text(p_tag, mx, bar_y + bar_h + 10, marker_col, font_size=7, bold=True, anchor_x="center")

        # Enraged outline pulsing when boss is below 33% HP
        border_col = COLOR_WHITE
        if frac < 0.33:
            import time
            pulse = int(180 + 75 * ((math.sin(time.time() * 6.0) + 1.0) * 0.5))
            border_col = (*RED_BRIGHT, pulse)

        # Border
        arcade.draw_lrbt_rectangle_outline(
            bar_x, bar_x + bar_w, bar_y, bar_y + bar_h, border_col, 2)

        # Label formatting
        phase = max(1, int(getattr(boss, "phase", 1)))
        phase_text = f"PHASE {phase}"
        if boss_name == "RAVANA":
            phase_text = ("PHASE I / SPREAD", "PHASE II / SPIRAL VOID", "PHASE III / FLEET SUMMONS")[min(2, phase - 1)]
            title = "EMPEROR RAVANA"
        elif boss_name == "MAHISHASURA":
            title = "WARLORD MAHISHASURA"
        elif boss_name == "VRITRA":
            title = "STORM SERPENT VRITRA"
        else:
            title = f"MINI-BOSS: {boss_name}"
        attack = getattr(boss, "current_attack_name", "")
        self._label_name.text = f"{title}  —  {phase_text}"
        self._label_hp.text = f"{max(0, boss.hp):,} / {boss.max_hp:,}"
        self._label_name.draw()
        self._label_hp.draw()
        status = "BOSS ALERT" if phase == 1 else "PHASE BREAK" if frac > 0.30 else "FINAL PHASE"
        status_color = RED_BRIGHT if phase > 1 else GOLD
        arcade.draw_text(status, bar_x + 4, bar_y + bar_h + 22, status_color,
                         font_size=8, bold=True)
        if attack:
            arcade.draw_text(attack, WIDTH - 18, 16, RED_BRIGHT if frac < 0.33 else GOLD,
                             font_size=8, bold=True, anchor_x="right")
        if phase > 1:
            arcade.draw_text("PHASE BREAK", WIDTH // 2, 43, RED_BRIGHT, font_size=8, bold=True, anchor_x="center")


# ==============================================================================
# [42/77] MODULE: game/ui/button.py
# ==============================================================================
"""
game/ui/button.py
Reusable clickable button widget for menus, pause overlay, and stat screens.

Renders as a rounded-style rectangle with a centered label. Has three visual
states (idle / hover / pressed) driven by mouse position and click, with a
small pulse on hover and a brief scale-down on press for tactile feedback.

Uses arcade.Text objects for the label + hotkey hint (instead of draw_text)
to avoid the per-frame PerformanceWarning spam.
"""
import arcade
from game.ui.easing import clamp, ease_out_cubic


class Button:
    """
    A clickable rectangular button.

    Usage:
        btn = Button(x, y, w, h, label="RESUME", on_click=self._resume)
        # in on_update: btn.update(dt, mouse_x, mouse_y)
        # in on_draw:   btn.draw()
        # in on_mouse_press: if btn.hit_test(x, y): btn.press()
        # in on_mouse_release: if btn.was_pressed: btn.release()
    """

    # Default palette — easy to override per-instance
    DEFAULT_IDLE_FILL    = (28, 32, 60)
    DEFAULT_IDLE_BORDER  = (90, 110, 150)
    DEFAULT_HOVER_FILL   = (48, 58, 100)
    DEFAULT_HOVER_BORDER = (255, 220, 80)
    DEFAULT_PRESS_FILL   = (70, 85, 140)
    DEFAULT_PRESS_BORDER = (255, 240, 150)
    DEFAULT_LABEL_COLOR  = (220, 225, 245)
    DEFAULT_HOT_COLOR    = (255, 220, 80)

    def __init__(self, cx: float, cy: float, width: float, height: float,
                 label: str, on_click=None,
                 hotkey: str = None,
                 idle_fill: tuple = None, hover_fill: tuple = None,
                 press_fill: tuple = None,
                 idle_border: tuple = None, hover_border: tuple = None,
                 label_color: tuple = None,
                 font_size: int = 14, accent_color: tuple = None):
        self.cx = cx
        self.cy = cy
        self.w = width
        self.h = height
        self.label = label
        self.on_click = on_click
        self.hotkey = hotkey  # shown as a small hint next to the label

        # Allow per-instance color overrides, fall back to defaults
        self.idle_fill    = idle_fill    or self.DEFAULT_IDLE_FILL
        self.hover_fill   = hover_fill   or self.DEFAULT_HOVER_FILL
        self.press_fill   = press_fill   or self.DEFAULT_PRESS_FILL
        self.idle_border  = idle_border  or self.DEFAULT_IDLE_BORDER
        self.hover_border = hover_border or self.DEFAULT_HOVER_BORDER
        self.label_color  = label_color  or self.DEFAULT_LABEL_COLOR
        self.accent_color = accent_color or self.DEFAULT_HOT_COLOR
        self.font_size = font_size

        # State
        self.hovered = False
        self.pressed = False       # mouse held down on this button
        self.was_pressed = False    # edge-trigger for click detection
        self._press_anim = 0.0     # 0..1 visual press feedback (eases out)
        self._hover_anim = 0.0     # 0..1 hover lerp (eases out)

        # Cached Text objects — colors update in-place, no per-frame rebuild.
        self._text_label = arcade.Text(
            label, cx, cy, self.label_color, font_size=font_size, bold=True,
            anchor_x="center", anchor_y="center",
        )
        if hotkey:
            self._text_hot = arcade.Text(
                f"[{hotkey}]",
                cx + (width / 2) - 22, cy,
                (*self.accent_color, 220),
                font_size=10, bold=True,
                anchor_x="right", anchor_y="center",
            )
        else:
            self._text_hot = None

    # ── Geometry ──────────────────────────────────────────────────────

    @property
    def left(self) -> float:   return self.cx - self.w / 2
    @property
    def right(self) -> float:  return self.cx + self.w / 2
    @property
    def bottom(self) -> float: return self.cy - self.h / 2
    @property
    def top(self) -> float:    return self.cy + self.h / 2

    def hit_test(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    # ── Input events ──────────────────────────────────────────────────

    def press(self) -> None:
        """Call from on_mouse_press when this button is clicked."""
        self.pressed = True
        self.was_pressed = True
        self._press_anim = 1.0

    def release(self) -> bool:
        """
        Call from on_mouse_release. Returns True if this release is a real
        click (mouse was over us when released), False otherwise.
        """
        was_over = self.pressed and self.hovered
        self.pressed = False
        self.was_pressed = False
        if was_over and self.on_click:
            self.on_click()
        return was_over

    def cancel_press(self) -> None:
        """If the user dragged off the button before releasing, swallow it."""
        self.pressed = False

    def activate(self) -> None:
        """Activate from keyboard/gamepad without requiring mouse hover."""
        self._press_anim = 1.0
        if self.on_click:
            self.on_click()

    # ── Per-frame ─────────────────────────────────────────────────────

    def update(self, dt: float, mouse_x: float, mouse_y: float) -> None:
        # Hover state from mouse position
        new_hovered = self.hit_test(mouse_x, mouse_y)
        if new_hovered != self.hovered:
            self.hovered = new_hovered
        # Smooth the hover anim
        target = 1.0 if self.hovered else 0.0
        # Critically-damped lerp: ~10 = 100ms to converge
        self._hover_anim += (target - self._hover_anim) * min(1.0, 12.0 * dt)
        # Decay press anim
        if self._press_anim > 0:
            self._press_anim = max(0.0, self._press_anim - dt * 3.5)

    def draw(self) -> None:
        # Choose colors based on state, with a smooth blend for hover
        hov = clamp(self._hover_anim)
        # Press anim makes the button briefly sink in
        press_offset = ease_out_cubic(self._press_anim) * 4.0
        # Subtle scale on hover (1.0 -> 1.04)
        scale = 1.0 + 0.04 * hov
        w = self.w * scale
        h = self.h * scale

        # Fill: blend idle -> hover
        fill = _lerp_color(self.idle_fill, self.hover_fill, hov)
        if self.pressed:
            fill = self.press_fill
        # Border: same blend, brighter
        border = _lerp_color(self.idle_border, self.hover_border, hov)
        border_w = 2 if not self.hovered else 3

        cy = self.cy - press_offset

        # Background panel
        arcade.draw_lrbt_rectangle_filled(
            self.cx - w / 2, self.cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*fill, 230),
        )
        # Border
        arcade.draw_lrbt_rectangle_outline(
            self.cx - w / 2, self.cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*border, 255), border_w,
        )
        # Soft glow when hovered
        if hov > 0.05:
            glow_alpha = int(40 * hov)
            arcade.draw_lrbt_rectangle_filled(
                self.cx - w / 2 - 4, self.cx + w / 2 + 4,
                cy - h / 2 - 4, cy + h / 2 + 4,
                (*self.accent_color, glow_alpha),
            )

        # Label (with optional hotkey hint on the right) — use cached Text
        # objects so we don't trip arcade's per-frame draw_text performance warning.
        self._text_label.position = (self.cx, cy)
        self._text_label.color = (*self.label_color, 255)
        self._text_label.draw()
        if self._text_hot is not None:
            self._text_hot.position = (self.cx + (self.w / 2) - 22, cy)
            self._text_hot.draw()


def _lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1[:3], c2[:3]))


# ==============================================================================
# [43/77] MODULE: game/ui/easing.py
# ==============================================================================
"""
game/ui/easing.py
Easing curves for smooth UI animations.
Premium-indie motion grammar — every value transition should flow through one of these.
"""
import math


# ── Linear ──────────────────────────────────────────────────────────────

def linear(t: float) -> float:
    return t


# ── Cubic ───────────────────────────────────────────────────────────────

def ease_in_cubic(t: float) -> float:
    return t * t * t


def ease_out_cubic(t: float) -> float:
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t: float) -> float:
    return 4.0 * t * t * t if t < 0.5 else 1.0 - (-2.0 * t + 2.0) ** 3 / 2.0


# ── Quart ───────────────────────────────────────────────────────────────

def ease_out_quart(t: float) -> float:
    return 1.0 - (1.0 - t) ** 4


def ease_in_out_quart(t: float) -> float:
    return 8.0 * t * t * t * t if t < 0.5 else 1.0 - (-2.0 * t + 2.0) ** 4 / 2.0


# ── Back (overshoot) ───────────────────────────────────────────────────

def ease_out_back(t: float, s: float = 1.70158) -> float:
    return 1.0 + (s + 1.0) * (t - 1.0) ** 3 + s * (t - 1.0) ** 2


def ease_in_back(t: float, s: float = 1.70158) -> float:
    return (s + 1.0) * t * t * t - s * t * t


# ── Elastic (spring) ───────────────────────────────────────────────────

def ease_out_elastic(t: float) -> float:
    if t == 0.0 or t == 1.0:
        return t
    return math.pow(2.0, -10.0 * t) * math.sin((t * 10.0 - 0.75) * 2.094) + 1.0


def ease_in_elastic(t: float) -> float:
    if t == 0.0 or t == 1.0:
        return t
    return -math.pow(2.0, 10.0 * t - 10.0) * math.sin((t * 10.0 - 10.75) * 2.094)


# ── Bounce ──────────────────────────────────────────────────────────────

def ease_out_bounce(t: float) -> float:
    if t < 1.0 / 2.75:
        return 7.5625 * t * t
    elif t < 2.0 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375


# ── Expo ────────────────────────────────────────────────────────────────

def ease_out_expo(t: float) -> float:
    return 1.0 if t == 1.0 else 1.0 - math.pow(2.0, -10.0 * t)


# ── Utility helpers ─────────────────────────────────────────────────────

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation from a to b by t (0..1)."""
    return a + (b - a) * t


def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    """Linearly interpolate between two RGB or RGBA color tuples."""
    return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def approach(current: float, target: float, step: float) -> float:
    """Move current toward target by at most step."""
    if abs(current - target) <= step:
        return target
    return current + math.copysign(step, target - current)


def inverse_lerp(a: float, b: float, v: float) -> float:
    """Returns t such that lerp(a, b, t) == v. Returns 0 if a == b."""
    if abs(b - a) < 1e-9:
        return 0.0
    return clamp((v - a) / (b - a))


def remap(v: float, in_lo: float, in_hi: float, out_lo: float, out_hi: float) -> float:
    """Map value v from [in_lo, in_hi] to [out_lo, out_hi]."""
    t = inverse_lerp(in_lo, in_hi, v)
    return lerp(out_lo, out_hi, t)


# ==============================================================================
# [44/77] MODULE: game/ui/hud.py
# ==============================================================================
"""
game/ui/hud.py
Comprehensive HUD — reactive HP bar with ghost trail and color crossfade,
score count-up animation, combo burst particles, ability countdown rings,
off-screen threat radar arrows, wave objectives, and low-health vignette.
"""
import math
import arcade
from constants import (
    WIDTH, HEIGHT,
    COLOR_HP_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE,
    COLOR_POWERUP_SHIELD, COLOR_POWERUP_SPREAD,
    COLOR_POWERUP_SPEED, COLOR_POWERUP_HEALTH, COLOR_POWERUP_BOMB,
    COLOR_POWERUP_OVERDRIVE,
)
from game.ui.easing import ease_out_cubic, ease_in_out_cubic, lerp, lerp_color, clamp
from game.ui.vedic_theme import (
    CYAN, GOLD, CYAN_BRIGHT, MUTED, RED_BRIGHT, ASTRA_RED,
    JADE, AMBER,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
    draw_telemetry_ticks, draw_segmented_bar,
)
from game.ui.radial_gauge import draw_radial_gauge

_POWERUP_COLORS = {
    "SHIELD": COLOR_POWERUP_SHIELD,
    "SPREAD": COLOR_POWERUP_SPREAD,
    "SPEED":  COLOR_POWERUP_SPEED,
    "HEALTH": COLOR_POWERUP_HEALTH,
    "BOMB":   COLOR_POWERUP_BOMB,
    "OVERDRIVE": COLOR_POWERUP_OVERDRIVE,
}
_POWERUP_NAMES = {
    "SHIELD": "Kavach",
    "SPREAD": "Agneyastra",
    "SPEED":  "Vayavyastra",
    "HEALTH": "Amrita",
    "BOMB": "Brahmastra",
    "OVERDRIVE": "Astra Overdrive",
}

_BAR_X, _BAR_Y, _BAR_W, _BAR_H = 16, HEIGHT - 32, 220, 20

# HP bar color thresholds
_HP_COLOR_HIGH   = (30, 200, 70)     # green > 60%
_HP_COLOR_MID    = (220, 200, 40)    # amber 30-60%
_HP_COLOR_LOW    = (220, 60, 0)      # red < 30%


class HUD:
    def __init__(self):
        from game.systems import save_system
        settings = save_system.load()
        self.colorblind_mode = settings.get("colorblind_mode", "off")
        self.reduced_flashes = bool(settings.get("reduced_flashes", False))
        self._displayed_hp = 100.0
        self._ghost_hp = 100.0       # slower-decaying ghost trail
        self._pulse_timer = 0.0

        # Score count-up animation
        self._displayed_score = 0.0
        self._target_score = 0
        self._score_flash = 0.0      # brief scale/flash on big score changes

        # Combo burst state
        self._combo_scale = 1.0
        self._last_combo = 0

        # HP hit flash (red vignette on damage)
        self._hp_hit_flash = 0.0
        self._last_hp = 100

        # HP bar labels
        self._label_vimana = arcade.Text(
            "VIMANA", _BAR_X + 6, _BAR_Y + 4,
            COLOR_WHITE, font_size=9, bold=True,
        )
        self._label_hp = arcade.Text(
            "100/100", _BAR_X + _BAR_W - 65, _BAR_Y + 4,
            COLOR_WHITE, font_size=9, bold=True,
        )

        # Score & Combo
        self._label_score = arcade.Text(
            "0", WIDTH - 16, HEIGHT - 18,
            COLOR_SCORE, font_size=18, bold=True,
            anchor_x="right", anchor_y="top",
        )
        self._label_combo = arcade.Text(
            "", WIDTH - 16, HEIGHT - 44,
            (255, 150, 30), font_size=11, bold=True,
            anchor_x="right", anchor_y="top",
        )

        # Wave & Objective Info
        self._label_wave = arcade.Text(
            "", WIDTH // 2, HEIGHT - 16,
            COLOR_WAVE, font_size=13, bold=True,
            anchor_x="center", anchor_y="top",
        )
        self._label_objective = arcade.Text(
            "", WIDTH // 2, HEIGHT - 36,
            (180, 200, 240), font_size=10, bold=True,
            anchor_x="center", anchor_y="top",
        )
        self._label_enemy_count = arcade.Text(
            "", WIDTH // 2, HEIGHT - 52,
            (255, 120, 120), font_size=9, bold=True,
            anchor_x="center", anchor_y="top",
        )

        # Wave countdown banner
        self._label_announce = arcade.Text(
            "", WIDTH // 2, HEIGHT // 2 + 20,
            COLOR_WAVE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._label_announce_sub = arcade.Text(
            "Prepare yourself!", WIDTH // 2, HEIGHT // 2 - 20,
            COLOR_WHITE, font_size=14,
            anchor_x="center", anchor_y="center",
        )

        # Wave clear banner
        self._label_clear = arcade.Text(
            "WAVE CLEARED", WIDTH // 2, HEIGHT // 2 + 10,
            (50, 230, 120), font_size=28, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._label_clear_sub = arcade.Text(
            "Next wave incoming...", WIDTH // 2, HEIGHT // 2 - 22,
            (180, 240, 200), font_size=13,
            anchor_x="center", anchor_y="center",
        )

        # Tutorial hint
        self._label_tutorial = arcade.Text(
            "WASD: Move  •  LMB: Shoot  •  SPACE: Dash  •  Q: Chakram  •  F: Bomb",
            WIDTH // 2, 45,
            (200, 220, 255, 190), font_size=10, bold=True,
            anchor_x="center",
        )

        # Powerup text
        self._label_pu_name  = arcade.Text("", 56, 18, COLOR_WHITE, font_size=8, bold=True, anchor_x="center")
        self._label_pu_timer = arcade.Text("", 30, 44, COLOR_WHITE, font_size=9, bold=True, anchor_x="center")

    def update(self, delta_time: float, player) -> None:
        self._pulse_timer += delta_time

        # Smooth HP bar transition (eased approach)
        hp_diff = player.hp - self._displayed_hp
        self._displayed_hp += hp_diff * min(1.0, 12.0 * delta_time)

        # Ghost HP trail (decays slower — shows damage taken)
        ghost_diff = player.hp - self._ghost_hp
        if ghost_diff < 0:
            # HP decreased — ghost stays high then slowly catches up
            self._ghost_hp += ghost_diff * min(1.0, 2.5 * delta_time)
        else:
            # HP increased (heal) — ghost snaps to match
            self._ghost_hp = self._displayed_hp

        # HP hit flash on damage
        if player.hp < self._last_hp:
            self._hp_hit_flash = 1.0
        self._last_hp = player.hp
        if self._hp_hit_flash > 0:
            self._hp_hit_flash = max(0.0, self._hp_hit_flash - delta_time * 5.0)

        # Score count-up animation
        self._target_score = getattr(player, '_score_ref', self._target_score)
        score_diff = self._target_score - self._displayed_score
        if abs(score_diff) > 0.5:
            self._displayed_score += score_diff * min(1.0, 8.0 * delta_time)
        else:
            self._displayed_score = self._target_score

        # Score flash decay
        if self._score_flash > 0:
            self._score_flash = max(0.0, self._score_flash - delta_time * 4.0)

        # Combo burst scale decay
        if self._combo_scale > 1.0:
            self._combo_scale = max(1.0, self._combo_scale - delta_time * 6.0)

    def draw(self, player, score_system, wave_manager, enemies: list, powerups: list, boon_manager) -> None:
        self._draw_cockpit_frame()
        # Update score target from score_system
        if score_system.score != self._target_score:
            score_change = score_system.score - self._target_score
            if score_change > 500:
                self._score_flash = 1.0
            self._target_score = score_system.score

        # Combo burst detection
        if score_system.combo > self._last_combo and score_system.combo >= 3:
            self._combo_scale = 1.35
        self._last_combo = score_system.combo

        self._draw_hp_bar(player)
        self._draw_score(score_system)
        self._draw_wave_and_objective(wave_manager, len(enemies))
        self._draw_boons_row(boon_manager)
        self._draw_powerup(player)
        self._draw_ability_meters(player)
        self._draw_offscreen_radar(player, enemies, powerups)
        self._draw_low_health_vignette(player)

        if wave_manager.is_announcing:
            self._draw_announce(wave_manager)
        elif wave_manager.is_clearing:
            self._draw_clearing()

        if wave_manager.wave_number == 1 and wave_manager.is_fighting:
            self._label_tutorial.draw()

    def _draw_cockpit_frame(self) -> None:
        draw_corner_etching(10, WIDTH - 10, 10, HEIGHT - 10, CYAN, length=28, alpha=62)
        draw_scanlines(218, WIDTH - 218, HEIGHT - 88, HEIGHT - 70, CYAN, spacing=6, alpha=10)
        draw_telemetry_ticks(245, WIDTH - 245, HEIGHT - 70, GOLD, count=17, height=3, alpha=54)
        draw_telemetry_ticks(230, WIDTH - 230, 70, CYAN, count=19, height=3, alpha=42)
        arcade.draw_line(215, 70, 215, HEIGHT - 88, (*CYAN, 28), 1)
        arcade.draw_text("PRANA TELEMETRY", 226, HEIGHT - 84, CYAN_BRIGHT, font_size=7, bold=True)
        arcade.draw_text("ASTRA CONTROL // LIVE", WIDTH - 226, HEIGHT - 84, MUTED, font_size=7, bold=True, anchor_x="right")
        # 12px chamfered cockpit border inset (border only, no fill)
        draw_chamfered_panel(10, WIDTH - 10, 10, HEIGHT - 10, CYAN,
                             fill=(0, 0, 0), alpha=0, border_width=1, cut=12)

    def _draw_hp_bar(self, player) -> None:
        draw_chamfered_panel(12, _BAR_X + _BAR_W + 8, _BAR_Y - 5, _BAR_Y + _BAR_H + 7,
                             (220, 80, 80) if player.hp / player.max_hp < 0.3 else CYAN,
                             fill=(10, 16, 28), alpha=220, cut=7)
        arcade.draw_text("PRANA / HULL INTEGRITY", _BAR_X + 6, _BAR_Y + _BAR_H + 9,
                         MUTED, font_size=7, bold=True)
        draw_telemetry_ticks(_BAR_X, _BAR_X + _BAR_W, _BAR_Y - 3, CYAN, count=9, height=2, alpha=55)
        frac_actual = clamp(player.hp / player.max_hp)
        frac_display = clamp(self._displayed_hp / player.max_hp)
        frac_ghost = clamp(self._ghost_hp / player.max_hp)

        # Color crossfade: green > 60%, amber 30-60%, red < 30%
        palette = {
            "off": (_HP_COLOR_HIGH, _HP_COLOR_MID, _HP_COLOR_LOW),
            "protan": ((0, 114, 178), (230, 159, 0), (86, 180, 233)),
            "deutan": ((0, 114, 178), (230, 159, 0), (213, 94, 0)),
            "tritan": ((0, 158, 115), (230, 159, 0), (213, 94, 0)),
        }.get(self.colorblind_mode, (_HP_COLOR_HIGH, _HP_COLOR_MID, _HP_COLOR_LOW))
        high_color, mid_color, low_color = palette
        if frac_actual > 0.6:
            fill_color = high_color
        elif frac_actual > 0.3:
            t = clamp((frac_actual - 0.3) / 0.3)
            fill_color = lerp_color(mid_color, high_color, ease_out_cubic(t))
        else:
            t = clamp(frac_actual / 0.3)
            fill_color = lerp_color(low_color, mid_color, ease_out_cubic(t))

        # Background
        arcade.draw_lrbt_rectangle_filled(_BAR_X, _BAR_X + _BAR_W, _BAR_Y, _BAR_Y + _BAR_H, COLOR_HP_BG)

        # Ghost trail (red damage indicator — slower decay)
        if frac_ghost > frac_display:
            arcade.draw_lrbt_rectangle_filled(
                _BAR_X, _BAR_X + _BAR_W * frac_ghost,
                _BAR_Y, _BAR_Y + _BAR_H, (220, 40, 40, 160))

        # Actual HP fill
        if frac_display > 0:
            draw_segmented_bar(_BAR_X, _BAR_X + _BAR_W, _BAR_Y,
                               _BAR_Y + _BAR_H, frac_display, fill_color,
                               segments=10, gap=3)

        # Low-HP pulsing bar border
        if frac_actual < 0.28 and player.alive:
            pulse_t = ease_in_out_cubic(clamp((math.sin(self._pulse_timer * 5.0) + 1.0) * 0.5))
            pulse_a = int(lerp(100, 255, pulse_t))
            arcade.draw_lrbt_rectangle_outline(
                _BAR_X - 1, _BAR_X + _BAR_W + 1,
                _BAR_Y - 1, _BAR_Y + _BAR_H + 1,
                (255, 50, 50, pulse_a), 2)
        else:
            arcade.draw_lrbt_rectangle_outline(
                _BAR_X, _BAR_X + _BAR_W,
                _BAR_Y, _BAR_Y + _BAR_H, COLOR_WHITE, 1)

        # HP hit flash — red screen-edge vignette on damage
        if self._hp_hit_flash > 0:
            flash_a = int(60 * ease_out_cubic(self._hp_hit_flash) * (0.35 if self.reduced_flashes else 1.0))
            arcade.draw_lrbt_rectangle_filled(
                _BAR_X, _BAR_X + _BAR_W,
                _BAR_Y, _BAR_Y + _BAR_H, (255, 30, 30, flash_a))

        # HP number — flashes when low
        hp_text = f"{max(0, player.hp)}/{player.max_hp}"
        hp_col = COLOR_WHITE
        if frac_actual < 0.28 and player.alive:
            pulse_t = ease_in_out_cubic(clamp((math.sin(self._pulse_timer * 5.0) + 1.0) * 0.5))
            hp_col = lerp_color((255, 100, 80), (255, 255, 255), pulse_t)

        self._label_hp.text = hp_text
        self._label_hp.color = hp_col
        self._label_vimana.draw()
        self._label_hp.draw()

    def _draw_score(self, score_system) -> None:
        # Animated score count-up
        displayed = int(self._displayed_score)
        self._label_score.text = f"{displayed:,}"

        # Flash effect on big score changes
        if self._score_flash > 0:
            flash_scale = 1.0 + (0.06 if self.reduced_flashes else 0.15) * ease_out_cubic(self._score_flash)
            self._label_score.font_size = int(18 * flash_scale)
            glow_a = int((24 if self.reduced_flashes else 80) * self._score_flash)
            arcade.draw_lrbt_rectangle_filled(
                WIDTH - 200, WIDTH - 8,
                HEIGHT - 32, HEIGHT - 8,
                (255, 220, 50, glow_a))
        else:
            self._label_score.font_size = 18

        self._label_score.draw()

        if score_system.combo_active:
            combo = score_system.combo
            if combo >= 10:
                col = (0, 240, 255)      # Cyan Godlike
            elif combo >= 6:
                col = (255, 80, 220)     # Magenta Epic
            elif combo >= 3:
                col = (255, 215, 60)     # Golden Frenzy
            else:
                col = (255, 140, 30)     # Orange Warmup

            # Combo text with burst scale
            combo_size = int(11 * self._combo_scale)
            self._label_combo.text = f"×{combo} COMBO"
            self._label_combo.color = col
            self._label_combo.font_size = combo_size
            self._label_combo.draw()

            # Combo burst ring on increment
            if self._combo_scale > 1.05:
                ring_r = int(15 * self._combo_scale)
                ring_a = int(120 * (self._combo_scale - 1.0) / 0.35)
                cx = WIDTH - 55
                cy = HEIGHT - 50
                arcade.draw_circle_outline(cx, cy, ring_r, (*col, ring_a), 2)

            # Combo timer bar
            bar_w = 90
            bar_h = 3
            bx = WIDTH - 16 - bar_w
            by = HEIGHT - 64
            frac = clamp(score_system.combo_timer / score_system.combo_timeout)
            arcade.draw_lrbt_rectangle_filled(bx, bx + bar_w, by, by + bar_h, (40, 20, 20))
            if frac > 0:
                arcade.draw_lrbt_rectangle_filled(bx, bx + bar_w * frac, by, by + bar_h, col)

    def _draw_wave_and_objective(self, wave_manager, enemy_count: int) -> None:
        if wave_manager.wave_number == 0:
            return

        from constants import get_realm_for_wave
        realm = get_realm_for_wave(wave_manager.wave_number)
        effective_wave = ((wave_manager.wave_number - 1) % 20) + 1
        realm_index = (
            1 if effective_wave <= 3 else
            2 if effective_wave <= 6 else
            3 if effective_wave <= 9 else
            4 if effective_wave <= 12 else
            5 if effective_wave <= 15 else
            6 if effective_wave <= 18 else 7
        )
        breadcrumb = (
            f"MAHAYUDDHA  •  WAVE {wave_manager.wave_number}"
            if getattr(wave_manager, "is_endless", False)
            else f"REALM {realm_index}/7  •  {realm['name']}  •  WAVE {wave_manager.wave_number}"
        )
        if wave_manager.is_boss_wave:
            w_text = f"{breadcrumb}  —  EMPEROR RAVANA"
        elif wave_manager.is_mini_boss_wave:
            w_text = f"{breadcrumb}  —  MINI-BOSS"
        else:
            w_text = breadcrumb

        self._label_wave.text = w_text
        self._label_wave.draw()

        if wave_manager.is_fighting:
            self._label_objective.text = f"OBJECTIVE: {wave_manager.current_objective}"
            self._label_objective.draw()
            total = max(enemy_count, getattr(wave_manager, "total_wave_enemies", enemy_count))
            self._label_enemy_count.text = f"ENEMIES REMAINING: {enemy_count} / {total}"
            self._label_enemy_count.draw()

    def _draw_boons_row(self, boon_manager) -> None:
        if not boon_manager.active_boons:
            return
        start_x = _BAR_X
        start_y = _BAR_Y - 24
        from game.systems.boon_system import BOONS_DATABASE, SYNERGIES_DATABASE
        
        rune_abbr = {
            "agni_fury": "AG",
            "indra_thunder": "IN",
            "vayu_tempest": "VA",
            "garuda_magnet": "GA",
            "varuna_ward": "VR",
            "sudarshana_keen": "SU",
            "yama_execution": "YA",
            "surya_beam": "SY",
        }

        from game.ui.vedic_theme import BOON_ACCENTS
        for i, (bid, lvl) in enumerate(boon_manager.active_boons.items()):
            bdata = next((b for b in BOONS_DATABASE if b["id"] == bid), None)
            if not bdata: continue
            bx = start_x + i * 28
            # Use BOON_ACCENTS keyed by deity prefix (e.g. "agni_fury" → "Agni")
            deity_key = bid.split("_")[0].capitalize()
            chip_color = BOON_ACCENTS.get(deity_key, bdata["color"])
            arcade.draw_circle_filled(bx + 10, start_y, 11, (20, 25, 45))
            arcade.draw_circle_outline(bx + 10, start_y, 11, chip_color, 2)

            abbr = rune_abbr.get(bid, bdata["name"][:2].upper())
            arcade.draw_text(abbr, bx + 10, start_y - 4, chip_color, font_size=7, bold=True, anchor_x="center")

            # Stack level badge
            if lvl > 1:
                arcade.draw_circle_filled(bx + 19, start_y + 8, 5, (255, 215, 60))
                arcade.draw_text(str(lvl), bx + 19, start_y + 4, (10, 10, 10), font_size=7, bold=True, anchor_x="center")

        # ── Synergy Badges Row ─────────────────────────────────────────
        if hasattr(boon_manager, "active_synergies") and boon_manager.active_synergies:
            syn_y = start_y - 24
            for j, sid in enumerate(boon_manager.active_synergies):
                sdata = next((s for s in SYNERGIES_DATABASE if s["id"] == sid), None)
                if not sdata: continue
                sx = start_x + j * 75
                # Glowing synergy capsule
                pulse = (math.sin(self._pulse_timer * 4.0) + 1.0) * 0.5
                border_col = (*sdata["color"][:3], int(180 + 75 * pulse))
                arcade.draw_lrbt_rectangle_filled(sx, sx + 70, syn_y - 8, syn_y + 9, (25, 18, 45))
                arcade.draw_lrbt_rectangle_outline(sx, sx + 70, syn_y - 8, syn_y + 9, border_col, 2)
                arcade.draw_text(sdata["name"][:9].upper(), sx + 35, syn_y - 4, sdata["color"], font_size=7, bold=True, anchor_x="center")

    def _draw_ability_meters(self, player) -> None:
        draw_chamfered_panel(12, 190, 8, 66, CYAN, fill=(10, 16, 28),
                             alpha=220, cut=8)
        arcade.draw_line(200, 12, WIDTH - 184, 12, (*CYAN, 42), 1)
        arcade.draw_text("ASTRA CONTROL", 202, 51, CYAN_BRIGHT, font_size=7, bold=True)
        arcade.draw_text("COOLDOWN / CHARGE TELEMETRY", 202, 40, MUTED, font_size=7, bold=True)

        # Dash [SPACE] — JADE when ready
        dash_label = f"DASH ({player.dash_charges})" if player.dash_charges_max > 1 else "DASH"
        draw_radial_gauge(
            38, 32, 16,
            player.dash_ratio,
            JADE,
            dash_label,
            "SPACE",
            player.dash_ready,
        )

        # Chakram [Q] — AMBER when ready
        draw_radial_gauge(
            88, 32, 16,
            player.chakram_ratio,
            AMBER,
            "CHAKRAM",
            "Q",
            player.chakram_ready,
        )

        # Bomb [F] — ASTRA_RED
        if player.bomb_count > 0:
            draw_radial_gauge(
                145, 32, 16,
                1.0,
                ASTRA_RED,
                f"BOMB ×{player.bomb_count}",
                "F",
                True,
            )

    def _draw_offscreen_radar(self, player, enemies: list, powerups: list) -> None:
        """Draws glowing directional threat arrows along screen edges for off-screen enemies and power-ups."""
        margin = 22
        living = sum(1 for enemy in enemies if enemy.alive)
        offscreen = sum(1 for enemy in enemies if enemy.alive and not (0 <= enemy.x <= WIDTH and 0 <= enemy.y <= HEIGHT))
        radar_col = RED_BRIGHT if offscreen else CYAN_BRIGHT
        arcade.draw_text("RADAR", WIDTH - 112, 54, MUTED, font_size=7, bold=True)
        arcade.draw_text(f"THREATS {living:02d}", WIDTH - 112, 40, radar_col, font_size=8, bold=True)
        if offscreen:
            arcade.draw_text(f"OFF-SCREEN {offscreen:02d}", WIDTH - 112, 27, RED_BRIGHT, font_size=7, bold=True)

        # 1. Off-screen enemies (red chevrons / pointer triangles)
        for e in enemies:
            if not e.alive: continue
            if not (0 <= e.x <= WIDTH and 0 <= e.y <= HEIGHT):
                ex = max(margin, min(WIDTH - margin, e.x))
                ey = max(margin, min(HEIGHT - margin, e.y))
                ang = math.atan2(e.y - player.y, e.x - player.x)
                
                # Draw pointer triangle pointing towards enemy
                tx1 = ex + math.cos(ang) * 8
                ty1 = ey + math.sin(ang) * 8
                tx2 = ex + math.cos(ang + 2.4) * 6
                ty2 = ey + math.sin(ang + 2.4) * 6
                tx3 = ex + math.cos(ang - 2.4) * 6
                ty3 = ey + math.sin(ang - 2.4) * 6
                arcade.draw_triangle_filled(tx1, ty1, tx2, ty2, tx3, ty3, (255, 50, 50))
                arcade.draw_circle_outline(ex, ey, 7, (255, 100, 100, 150), 1)

        # 2. Off-screen powerups (golden/cyan diamond pointers)
        for pu in powerups:
            if not pu.alive: continue
            if not (0 <= pu.x <= WIDTH and 0 <= pu.y <= HEIGHT):
                px = max(margin, min(WIDTH - margin, pu.x))
                py = max(margin, min(HEIGHT - margin, pu.y))
                pcol = getattr(pu, "_color", (255, 215, 60))
                arcade.draw_circle_filled(px, py, 6, pcol)
                arcade.draw_circle_outline(px, py, 8, COLOR_WHITE, 1)

    def _draw_low_health_vignette(self, player) -> None:
        frac = player.hp / player.max_hp
        if frac < 0.28 and player.alive:
            # Smooth eased pulse instead of raw sin()
            pulse_t = ease_in_out_cubic(clamp((math.sin(self._pulse_timer * 5.0) + 1.0) * 0.5))
            alpha = int(lerp(12, 36, pulse_t)) if self.reduced_flashes else int(lerp(30, 90, pulse_t))
            # Red screen border vignette — thicker at lower HP
            border_w = int(lerp(4, 12, 1.0 - frac / 0.28))
            arcade.draw_lrbt_rectangle_outline(
                4, WIDTH - 4, 4, HEIGHT - 4,
                (255, 30, 30, alpha), border_w)

            # Corner vignette glow for extra urgency
            corner_a = int(lerp(10, 40, pulse_t))
            for cx, cy in [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]:
                arcade.draw_circle_filled(cx, cy, 120, (180, 0, 0, corner_a))

        # Damage hit flash (from _hp_hit_flash)
        if self._hp_hit_flash > 0:
            edge_a = int(15 * ease_out_cubic(self._hp_hit_flash)) if self.reduced_flashes else int(50 * ease_out_cubic(self._hp_hit_flash))
            arcade.draw_lrbt_rectangle_outline(
                2, WIDTH - 2, 2, HEIGHT - 2,
                (255, 60, 40, edge_a), 6)

    def _draw_powerup(self, player) -> None:
        if not player.active_powerup or player.active_powerup.expired:
            return

        pu = player.active_powerup
        pname = pu.type.name
        label_str = _POWERUP_NAMES.get(pname, pname)
        color = _POWERUP_COLORS.get(pname, COLOR_WHITE)

        cx, cy, r = 38, 92, 18
        frac = pu.fraction

        arcade.draw_circle_outline(cx, cy, r, (60, 60, 60), 3)
        if frac > 0:
            steps = max(1, int(40 * frac))
            for i in range(1, steps + 1):
                a = math.radians(90 - (360 * frac) * (i / 40))
                arcade.draw_line(cx, cy, cx + math.cos(a) * r, cy + math.sin(a) * r, (*color, 180), 2)

        arcade.draw_circle_filled(cx, cy, r - 3, (*color, 100))
        self._label_pu_name.x = cx
        self._label_pu_name.y = cy - 28
        self._label_pu_name.text = label_str
        self._label_pu_name.color = color
        self._label_pu_timer.x = cx
        self._label_pu_timer.y = cy - 4
        self._label_pu_timer.text = f"{pu.remaining:.1f}s"
        self._label_pu_name.draw()
        self._label_pu_timer.draw()

    def _draw_announce(self, wave_manager) -> None:
        alpha = max(0, min(255, wave_manager.announce_alpha))
        r, g, b = COLOR_WAVE
        self._label_announce.text = f"{wave_manager.announce_text} — {wave_manager.countdown_val}"
        self._label_announce.color = (r, g, b, alpha)
        if wave_manager.announce_subtitle:
            self._label_announce_sub.text = wave_manager.announce_subtitle
        self._label_announce_sub.color = (*COLOR_WHITE, alpha)
        self._label_announce.draw()
        self._label_announce_sub.draw()

    def _draw_clearing(self) -> None:
        self._label_clear.draw()
        self._label_clear_sub.draw()


# ==============================================================================
# [45/77] MODULE: game/ui/menu_button.py
# ==============================================================================
"""
game/ui/menu_button.py
Canonical Vedic-Punk Button Component with Celestial, Metallic, and Danger variants.
Supports smooth 120ms ease-out hover scale (+3.5%), breathing glow, and font fallbacks.
"""
import arcade
from game.ui.vedic_theme import (
    GOLD, GOLD_BRIGHT, CYAN, CYAN_BRIGHT, GREY, OBSIDIAN, SURFACE_LOW,
    ASTRA_RED, ASTRA_RED_BRIGHT, FONT_INTERFACE, draw_chamfered_panel,
)


class MenuButton:
    def __init__(self, label: str, center_x: float, center_y: float,
                 width: float = 200.0, height: float = 40.0,
                 accent: tuple = GOLD, variant: str = "metallic"):
        self.label = label
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height
        self.variant = variant  # 'celestial', 'metallic', 'danger'
        self.accent = accent
        self.hover_amount = 0.0
        self._pulse_timer = 0.0

        # Resolve colors by variant
        if variant == "celestial" or accent == GOLD:
            self._base_border = GOLD
            self._hover_border = GOLD_BRIGHT
            self._base_text = GOLD_BRIGHT
            self._hover_text = (255, 255, 255)
            self._fill = OBSIDIAN
            self._border_w = 2
        elif variant == "danger" or accent == ASTRA_RED:
            self._base_border = ASTRA_RED
            self._hover_border = ASTRA_RED_BRIGHT
            self._base_text = ASTRA_RED_BRIGHT
            self._hover_text = (255, 255, 255)
            self._fill = (34, 8, 18)
            self._border_w = 2
        else:
            self._base_border = GREY if accent == GREY else accent
            self._hover_border = CYAN
            self._base_text = (210, 220, 240)
            self._hover_text = CYAN_BRIGHT
            self._fill = SURFACE_LOW
            self._border_w = 1

        self._text = arcade.Text(
            label, center_x, center_y, (*self._base_text, 255),
            font_size=12, bold=True, anchor_x="center", anchor_y="center",
            font_name=FONT_INTERFACE,
        )

    def contains(self, x: float, y: float) -> bool:
        return (
            self.center_x - self.width / 2 <= x <= self.center_x + self.width / 2
            and self.center_y - self.height / 2 <= y <= self.center_y + self.height / 2
        )

    def update(self, delta_time: float, hovered: bool) -> None:
        target = 1.0 if hovered else 0.0
        self.hover_amount += (target - self.hover_amount) * min(1.0, delta_time * 14.0)
        self._pulse_timer += delta_time

    def draw(self) -> None:
        scale = 1.0 + 0.035 * self.hover_amount
        width = self.width * scale
        height = self.height * scale
        left = self.center_x - width / 2
        right = self.center_x + width / 2
        bottom = self.center_y - height / 2
        top = self.center_y + height / 2

        # Interpolate border color
        r = int(self._base_border[0] + (self._hover_border[0] - self._base_border[0]) * self.hover_amount)
        g = int(self._base_border[1] + (self._hover_border[1] - self._base_border[1]) * self.hover_amount)
        b = int(self._base_border[2] + (self._hover_border[2] - self._base_border[2]) * self.hover_amount)

        # Hover fill brightening
        fill = tuple(int(base + (target - base) * self.hover_amount)
                     for base, target in zip(self._fill, (45, 52, 72)))

        border_width = self._border_w if self.hover_amount < 0.2 else self._border_w + 1

        draw_chamfered_panel(
            left, right, bottom, top,
            (r, g, b), fill=fill, alpha=245,
            border_width=border_width,
            selected=self.hover_amount > 0.1,
            cut=8.0,
        )

        # Update text position, color, and size
        tr = int(self._base_text[0] + (self._hover_text[0] - self._base_text[0]) * self.hover_amount)
        tg = int(self._base_text[1] + (self._hover_text[1] - self._base_text[1]) * self.hover_amount)
        tb = int(self._base_text[2] + (self._hover_text[2] - self._base_text[2]) * self.hover_amount)
        self._text.position = (self.center_x, self.center_y)
        self._text.color = (tr, tg, tb, 255)
        self._text.font_size = int(12 + self.hover_amount)
        self._text.draw()


# ==============================================================================
# [46/77] MODULE: game/ui/modal.py
# ==============================================================================
"""
game/ui/modal.py
Canonical modal dialog with dim scrim, Tier 2 chamfered glass container, and focus trapping.
Used for Pause & Abandon Sortie confirmation per Section 5 and Section 7.8.
"""
import arcade
from constants import WIDTH, HEIGHT
from game.ui.vedic_theme import (
    SURFACE_HIGH, GOLD, CYAN_BRIGHT,
    ASTRA_RED, GREY, PARCHMENT,
    FONT_INTERFACE, FONT_TELEMETRY, draw_chamfered_panel, draw_corner_etching,
)
from game.ui.menu_button import MenuButton


class Modal:
    """Canonical modal dialog overlay."""

    def __init__(self, title: str, subtitle: str = "",
                 body: list[str] | None = None,
                 actions: list[tuple[str, str, str]] | None = None,
                 width: float = 460.0, height: float = 280.0,
                 accent=GOLD):
        """
        :param actions: list of (label, action_key, variant) where variant is 'celestial', 'metallic', or 'danger'.
        """
        self.title = title
        self.subtitle = subtitle
        self.body = body or []
        self.width = width
        self.height = height
        self.accent = accent
        self.is_open = False
        self._hovered_btn = -1
        self._buttons: list[tuple[MenuButton, str]] = []

        self._rebuild_buttons(actions or [])

    def _rebuild_buttons(self, actions: list[tuple[str, str, str]]) -> None:
        self._buttons.clear()
        if not actions:
            return

        btn_w = min(180.0, (self.width - 40 - (len(actions) - 1) * 16) / len(actions))
        btn_h = 36.0
        start_x = WIDTH // 2 - ((len(actions) - 1) * (btn_w + 16)) / 2
        btn_y = HEIGHT // 2 - self.height // 2 + 45.0

        for i, (label, key, variant) in enumerate(actions):
            bx = start_x + i * (btn_w + 16)
            btn = MenuButton(label, bx, btn_y, btn_w, btn_h,
                             accent=ASTRA_RED if variant == "danger" else (GOLD if variant == "celestial" else GREY),
                             variant=variant)
            self._buttons.append((btn, key))

    def set_content(self, title: str, subtitle: str = "",
                    body: list[str] | None = None,
                    actions: list[tuple[str, str, str]] | None = None,
                    accent=GOLD) -> None:
        self.title = title
        self.subtitle = subtitle
        self.body = body or []
        self.accent = accent
        if actions is not None:
            self._rebuild_buttons(actions)

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    def update(self, delta_time: float) -> None:
        if not self.is_open:
            return
        for i, (btn, _) in enumerate(self._buttons):
            btn.update(delta_time, i == self._hovered_btn)

    def on_mouse_motion(self, x: float, y: float) -> None:
        if not self.is_open:
            return
        self._hovered_btn = -1
        for i, (btn, _) in enumerate(self._buttons):
            if btn.contains(x, y):
                self._hovered_btn = i
                break

    def on_mouse_press(self, x: float, y: float) -> str | None:
        if not self.is_open:
            return None
        for i, (btn, key) in enumerate(self._buttons):
            if btn.contains(x, y):
                return key
        return None

    def on_key_press(self, key: int, modifiers: int) -> str | None:
        if not self.is_open:
            return None
        if key == arcade.key.ESCAPE:
            self.close()
            return "cancel"
        elif key == arcade.key.ENTER:
            # Activate first celestial or metallic button, or cancel if danger
            for btn, act_key in self._buttons:
                if act_key in ("resume", "cancel"):
                    return act_key
            if self._buttons:
                return self._buttons[0][1]
        return None

    def draw(self) -> None:
        if not self.is_open:
            return

        # 70% dim scrim over entire viewport
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (0, 0, 0, 180))

        # Centered Tier 2 chamfered dialog
        left = WIDTH // 2 - self.width // 2
        right = WIDTH // 2 + self.width // 2
        bottom = HEIGHT // 2 - self.height // 2
        top = HEIGHT // 2 + self.height // 2

        draw_chamfered_panel(left, right, bottom, top, self.accent,
                             fill=SURFACE_HIGH, alpha=245, border_width=2,
                             selected=True, cut=10.0, scanlines=True)
        draw_corner_etching(left, right, bottom, top, self.accent, length=16.0, alpha=140)

        # Title
        arcade.draw_text(self.title, WIDTH // 2, top - 32,
                         self.accent, font_size=16, bold=True,
                         anchor_x="center", font_name=FONT_INTERFACE)
        if self.subtitle:
            arcade.draw_text(self.subtitle, WIDTH // 2, top - 52,
                             CYAN_BRIGHT, font_size=9, bold=True,
                             anchor_x="center", font_name=FONT_TELEMETRY)

        arcade.draw_line(left + 24, top - 62, right - 24, top - 62, (*self.accent[:3], 60), 1)

        # Body copy lines
        body_y = top - 86
        for line in self.body:
            arcade.draw_text(line, WIDTH // 2, body_y,
                             PARCHMENT, font_size=10,
                             anchor_x="center", font_name=FONT_INTERFACE)
            body_y -= 18

        # Buttons
        for btn, _ in self._buttons:
            btn.draw()


# ==============================================================================
# [47/77] MODULE: game/ui/nav_rail.py
# ==============================================================================
"""
game/ui/nav_rail.py
Standardized 220px left navigation rail for front-end console views.
Follows the canonical Section 5 and Section 7.1 specification.
"""
import arcade
from constants import HEIGHT
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, GREY, FONT_INTERFACE, FONT_TELEMETRY,
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


# ==============================================================================
# [48/77] MODULE: game/ui/parallax_bg.py
# ==============================================================================
"""
game/ui/parallax_bg.py
Four-layer dynamic parallax starfield that shifts with the player's position
and morphs visual theme & palettes per Mythological Realm (Swarga, Kshira Sagara, Dandaka, Lanka).
"""
import random
import arcade
from constants import WIDTH, HEIGHT, get_realm_for_wave


class ParallaxBackground:
    def __init__(self, seed: int = 42):
        rng = random.Random(seed)

        def rand_pos(margin=0):
            return (rng.randint(margin, WIDTH - margin),
                    rng.randint(margin, HEIGHT - margin))

        # Layer 0 — far tiny stars
        self._l0 = [
            (*rand_pos(), rng.uniform(0.5, 1.2), rng.randint(50, 140))
            for _ in range(150)
        ]

        # Layer 1 — cosmic nebula blobs
        self._nebulas = [
            (*rand_pos(60), rng.randint(45, 110), rng.randint(0, 2))
            for _ in range(8)
        ]

        # Layer 2 — medium stars
        self._l2 = [
            (*rand_pos(), rng.uniform(1.0, 2.2), rng.randint(100, 220))
            for _ in range(60)
        ]

        # Layer 3 — near celestial dust & glowing sparks
        self._l3 = [
            (*rand_pos(), rng.uniform(1.6, 3.2), rng.randint(180, 255))
            for _ in range(22)
        ]

    def draw(self, player_x: float, player_y: float, wave_num: int = 1) -> None:
        """Draws the dynamic realm backdrop with parallax motion."""
        realm = get_realm_for_wave(wave_num)
        nebula_colors = realm["nebula_palette"]
        accent = realm["accent_color"]

        cx, cy = WIDTH / 2, HEIGHT / 2
        nx = (player_x - cx) / cx
        ny = (player_y - cy) / cy

        # Draw deep realm atmosphere tint
        bg_r, bg_g, bg_b = realm["bg_color"]
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (bg_r, bg_g, bg_b))

        # ── 1. Nebulas ────────────────────────────────────────────────
        for bx, by, br, color_idx in self._nebulas:
            ox = nx * 18
            oy = ny * 18
            rx = (bx + ox) % WIDTH
            ry = (by + oy) % HEIGHT
            col = nebula_colors[color_idx % len(nebula_colors)]
            arcade.draw_circle_filled(rx, ry, br, (*col, 40))

        # ── 2. Layer 0 — Far Stars ────────────────────────────────────
        for sx, sy, sr, sb in self._l0:
            ox, oy = nx * 10, ny * 10
            rx = (sx + ox) % WIDTH
            ry = (sy + oy) % HEIGHT
            arcade.draw_circle_filled(rx, ry, sr, (sb, sb, sb))

        # ── 3. Layer 2 — Medium Stars (Realm Tinted) ───────────────────
        for sx, sy, sr, sb in self._l2:
            ox, oy = nx * 28, ny * 28
            rx = (sx + ox) % WIDTH
            ry = (sy + oy) % HEIGHT
            ar, ag, ab = accent
            # Blend star brightness with realm accent
            sr_val = int((sb + ar) * 0.5)
            sg_val = int((sb + ag) * 0.5)
            sb_val = int((sb + ab) * 0.5)
            arcade.draw_circle_filled(rx, ry, sr, (sr_val, sg_val, sb_val))

        # ── 4. Layer 3 — Foreground Cosmic Dust ────────────────────────
        for sx, sy, sr, sb in self._l3:
            ox, oy = nx * 50, ny * 50
            rx = (sx + ox) % WIDTH
            ry = (sy + oy) % HEIGHT
            arcade.draw_circle_filled(rx, ry, sr, (*accent, min(255, sb)))


# ==============================================================================
# [49/77] MODULE: game/ui/radial_gauge.py
# ==============================================================================
"""
game/ui/radial_gauge.py
Circular cooldown and readiness dial for Dash, Chakram, and Brahmastra.
Renders an authentic 32px diameter gauge with sweep indicator, readiness pulse, and keybind tag.
"""
import arcade
from game.ui.vedic_theme import (
    CYAN, GOLD, GOLD_BRIGHT, WELL, GREY,
    FONT_TELEMETRY, draw_state_badge,
)


def draw_radial_gauge(center_x: float, center_y: float, radius: float = 16.0,
                      fraction: float = 1.0, color=CYAN, label: str = "",
                      keybind: str = "", ready: bool = True) -> None:
    """
    Draw a circular dial representing ability readiness / cooldown fraction.
    :param fraction: 0.0 (empty/cooling) to 1.0 (fully charged/ready).
    """
    fraction = max(0.0, min(1.0, fraction))
    is_ready = fraction >= 0.999 or ready

    # Outer well ring
    arcade.draw_circle_filled(center_x, center_y, radius, (*WELL[:3], 230))
    arcade.draw_circle_outline(center_x, center_y, radius, (*GREY[:3], 80), 1)

    # Sweep arc (clockwise from top: 90 deg down)
    sweep_angle = fraction * 360.0
    if sweep_angle > 0.0:
        fill_color = GOLD if is_ready else color
        # Draw arc from 90 deg backwards by sweep_angle
        start_angle = 90.0 - sweep_angle
        arcade.draw_arc_outline(center_x, center_y, radius * 2 - 3, radius * 2 - 3,
                                (*fill_color[:3], 240), start_angle, 90.0, 3)

    # Inner core dot
    core_color = GOLD_BRIGHT if is_ready else (*color[:3], 160)
    core_radius = 4.0 if is_ready else 2.5
    arcade.draw_circle_filled(center_x, center_y, core_radius, core_color)

    # Keybind badge underneath
    if keybind:
        badge_y = center_y - radius - 10
        draw_state_badge(center_x, badge_y, keybind, GOLD if is_ready else GREY, width=38)

    # Label text
    if label:
        text_y = center_y - radius - 24 if keybind else center_y - radius - 12
        arcade.draw_text(
            label, center_x, text_y,
            GOLD_BRIGHT if is_ready else GREY,
            font_size=8, bold=True, anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY,
        )


# ==============================================================================
# [50/77] MODULE: game/ui/transitions.py
# ==============================================================================
"""
game/ui/transitions.py
View-transition overlays — smooth crossfade between arcade Views.
Supports fade-to-black, slide-up, and custom wipe patterns.
"""
import arcade
from constants import WIDTH, HEIGHT
from game.ui.easing import ease_in_out_cubic, ease_out_cubic, clamp


class TransitionOverlay:
    """
    Singleton-ish overlay drawn on top of the active view.
    Call TransitionOverlay.start(...) to begin a transition;
    the overlay handles the mid-swap and fade-in automatically.

    Usage:
        Instead of:
            self.window.show_view(NextView())
        Do:
            TransitionOverlay.start(self.window, NextView(), duration=0.4)

    The overlay must be drawn by the window's active view — see the
    `draw_transition()` helper which views should call at the end of on_draw().
    """

    # Class-level state (one transition at a time)
    _active = False
    _phase = "idle"       # "fade_out" | "swap" | "fade_in" | "idle"
    _elapsed = 0.0
    _duration = 0.4
    _half = 0.2
    _window = None
    _new_view = None
    _color = (0, 0, 0)   # transition overlay color
    _style = "fade"       # "fade" | "slide_up" | "wipe"

    @classmethod
    def start(cls, window, new_view, duration: float = 0.4,
              color: tuple = (0, 0, 0), style: str = "fade") -> None:
        """Begin a transition to new_view."""
        cls._active = True
        cls._phase = "fade_out"
        cls._elapsed = 0.0
        cls._duration = duration
        cls._half = duration / 2.0
        cls._window = window
        cls._new_view = new_view
        cls._color = color
        cls._style = style

    @classmethod
    def update(cls, dt: float) -> None:
        if not cls._active:
            return
        cls._elapsed += dt

        if cls._phase == "fade_out":
            if cls._elapsed >= cls._half:
                # Swap view at the midpoint (screen is fully covered)
                cls._phase = "fade_in"
                cls._elapsed = 0.0
                if cls._window and cls._new_view:
                    cls._window.show_view(cls._new_view)
                    cls._new_view = None

        elif cls._phase == "fade_in":
            if cls._elapsed >= cls._half:
                cls._active = False
                cls._phase = "idle"

    @classmethod
    def draw(cls) -> None:
        """Draw the transition overlay. Call at the END of on_draw()."""
        if not cls._active:
            return

        if cls._style == "fade":
            cls._draw_fade()
        elif cls._style == "slide_up":
            cls._draw_slide_up()
        elif cls._style == "wipe":
            cls._draw_wipe()

    @classmethod
    def _draw_fade(cls) -> None:
        if cls._phase == "fade_out":
            t = clamp(cls._elapsed / cls._half)
            alpha = int(255 * ease_in_out_cubic(t))
        else:  # fade_in
            t = clamp(cls._elapsed / cls._half)
            alpha = int(255 * (1.0 - ease_out_cubic(t)))
        r, g, b = cls._color[:3]
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (r, g, b, alpha))

    @classmethod
    def _draw_slide_up(cls) -> None:
        if cls._phase == "fade_out":
            t = clamp(cls._elapsed / cls._half)
            y_off = int(HEIGHT * ease_in_out_cubic(t))
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, y_off, (r, g, b, 255))
        else:
            t = clamp(cls._elapsed / cls._half)
            y_off = int(HEIGHT * (1.0 - ease_out_cubic(t)))
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, HEIGHT - y_off, HEIGHT, (r, g, b, 255))

    @classmethod
    def _draw_wipe(cls) -> None:
        """Horizontal scan-line wipe from top to bottom."""
        if cls._phase == "fade_out":
            t = clamp(cls._elapsed / cls._half)
            eased = ease_in_out_cubic(t)
            # Fill from top downward
            fill_h = int(HEIGHT * eased)
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, HEIGHT - fill_h, HEIGHT, (r, g, b, 255))
            # Scan line at leading edge
            line_y = HEIGHT - fill_h
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, line_y - 3, line_y + 1, (255, 255, 255, 80))
        else:
            t = clamp(cls._elapsed / cls._half)
            eased = ease_out_cubic(t)
            fill_h = int(HEIGHT * (1.0 - eased))
            r, g, b = cls._color[:3]
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, fill_h, (r, g, b, 255))
            line_y = fill_h
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, line_y - 1, line_y + 3, (255, 255, 255, 80))

    @classmethod
    @property
    def is_active(cls) -> bool:
        return cls._active


def transition_to(window, new_view, duration: float = 0.4,
                  color: tuple = (0, 0, 0), style: str = "fade") -> None:
    """
    Convenience function — call this instead of window.show_view() for
    a smooth animated transition.
    """
    TransitionOverlay.start(window, new_view, duration=duration,
                            color=color, style=style)


# ==============================================================================
# [51/77] MODULE: game/ui/tween.py
# ==============================================================================
"""
game/ui/tween.py
Lightweight tween manager for animating any numeric attribute over time.
Used by HUD, menus, boon cards, boss intros, and death sequences.
"""
from game.ui.easing import ease_out_cubic, lerp, clamp


class Tween:
    """Animate a single attribute on a target object from start → end."""
    __slots__ = ("_target", "_attr", "start", "end", "duration",
                 "elapsed", "ease", "on_done", "delay", "_started")

    def __init__(self, target, attr: str, end: float, duration: float,
                 ease=ease_out_cubic, on_done=None, delay: float = 0.0,
                 start=None):
        self._target = target
        self._attr = attr
        self.start = start if start is not None else getattr(target, attr, 0.0)
        self.end = end
        self.duration = max(0.001, duration)
        self.elapsed = 0.0
        self.ease = ease
        self.on_done = on_done
        self.delay = delay
        self._started = delay <= 0

    @property
    def done(self) -> bool:
        return self._started and self.elapsed >= self.duration

    @property
    def progress(self) -> float:
        if not self._started:
            return 0.0
        return clamp(self.elapsed / self.duration)

    def update(self, dt: float) -> None:
        if not self._started:
            self.delay -= dt
            if self.delay <= 0:
                self._started = True
                # Re-read start value at the moment the tween actually begins
                if self.start is None:
                    self.start = getattr(self._target, self._attr, 0.0)
            else:
                return

        self.elapsed += dt
        t = clamp(self.elapsed / self.duration)
        eased = self.ease(t)
        val = lerp(self.start, self.end, eased)
        setattr(self._target, self._attr, val)

        if t >= 1.0 and self.on_done:
            cb = self.on_done
            self.on_done = None  # prevent double-fire
            cb()


class TweenSequence:
    """Run a list of tweens one after another on the same target."""
    __slots__ = ("tweens", "_index")

    def __init__(self, tweens: list):
        self.tweens = tweens
        self._index = 0

    @property
    def done(self) -> bool:
        return self._index >= len(self.tweens)

    def update(self, dt: float) -> None:
        if self.done:
            return
        tw = self.tweens[self._index]
        tw.update(dt)
        if tw.done:
            self._index += 1


class TweenManager:
    """Manages a pool of active tweens, automatically pruning completed ones."""
    def __init__(self):
        self.tweens: list = []

    def add(self, tween) -> None:
        """Add a Tween or TweenSequence."""
        self.tweens.append(tween)
        return tween

    def tween(self, target, attr: str, end: float, duration: float,
              ease=ease_out_cubic, on_done=None, delay: float = 0.0,
              start=None):
        """Convenience: create and add a Tween in one call."""
        t = Tween(target, attr, end, duration, ease=ease, on_done=on_done,
                  delay=delay, start=start)
        self.tweens.append(t)
        return t

    def cancel_all(self) -> None:
        self.tweens.clear()

    def update(self, dt: float) -> None:
        for t in self.tweens:
            t.update(dt)
        self.tweens = [t for t in self.tweens if not t.done]

    @property
    def active(self) -> bool:
        return len(self.tweens) > 0


# ==============================================================================
# [52/77] MODULE: game/ui/vedic_theme.py
# ==============================================================================
"""
Canonical design tokens and drawing primitives for Vimana Wars.
Follows the authoritative Vimana Wars UI Redesign & Platform Design Document.
Single source of truth for all colours, typography fallbacks, chamfers, and gauges.
"""
import math
import arcade
from constants import WIDTH, HEIGHT


# ── Canonical Colours (Section 4.1) ──────────────────────────────────────────
VOID              = (7, 10, 19)          # Deepest background, starfield ground (#070A13)
OBSIDIAN          = (11, 13, 18)         # Window base, view background (#0B0D12)
WELL              = (14, 19, 32)         # Recessed insets behind bars & inputs (#0E1320)
SURFACE_LOW       = (20, 26, 40)         # Base RGB for low-tier glass (#141A28)
SURFACE_HIGH      = (32, 42, 61)         # Base RGB for high-tier glass (#202A3D)
GLASS_LOW         = (20, 26, 40, 217)    # Default panels and cards (85% opacity)
GLASS_HIGH        = (32, 42, 61, 235)    # Hovered / selected / focal panels (92% opacity)
GOLD              = (233, 196, 0)        # Primary action & current selection only (#E9C400)
GOLD_BRIGHT       = (255, 246, 223)      # Text on gold, victory headline (#FFF6DF)
CYAN              = (0, 219, 231)        # Operational: shields, ready states, links, sync (#00DBE7)
CYAN_BRIGHT       = (116, 245, 255)      # Cyan emphasis, warp lines (#74F5FF)
BRASS             = (197, 160, 89)       # Hardware plates, dividers, locked tiers (#C5A059)
ASTRA_RED         = (191, 0, 54)         # Danger, bosses, destructive confirm (#BF0036)
ASTRA_RED_BRIGHT  = (255, 107, 114)      # Red text, breach alarm (#FF6B72)
PARCHMENT         = (208, 198, 171)      # Lore and secondary body copy (#D0C6AB)
STARLIGHT         = (240, 237, 230)      # Primary body copy (#F0EDE6)
GREY              = (143, 152, 168)      # Hints, inactive data, disabled (#8F98A8)

# Aliases for backward-compatibility with existing views
MUTED        = GREY
RED          = ASTRA_RED
RED_BRIGHT   = ASTRA_RED_BRIGHT
HAIRLINE_GOLD = (*GOLD, 72)
HAIRLINE_CYAN = (*CYAN, 58)

# ── Gauge Color Ramp (Section 4.1) ───────────────────────────────────────────
JADE        = (30, 200, 70)     # > 0.60 (#1EC846)
AMBER       = (220, 200, 40)    # 0.30 - 0.60 (#DCC828)
CRIMSON     = (220, 60, 0)      # < 0.30 (#DC3C00)
GHOST_TRAIL = (220, 40, 40)     # Decays over 600ms (#DC2828)


def get_gauge_color(fraction: float) -> tuple[int, int, int]:
    """Return the canonical gauge color for a normalized 0.0-1.0 fraction."""
    if fraction > 0.60:
        return JADE
    if fraction >= 0.30:
        return AMBER
    return CRIMSON


# ── Boon Elemental Accents (Section 4.1) ─────────────────────────────────────
BOON_ACCENTS = {
    "Agni":       (255, 120, 30),   # #FF781E
    "Indra":      (120, 220, 255),  # #78DCFF
    "Vayu":       (100, 255, 180),  # #64FFB4
    "Yama":       (170, 80, 255),   # #AA50FF
    "Varuna":     (0, 160, 200),    # #00A0C8
    "Garuda":     (233, 196, 0),    # #E9C400
    "Sudarshana": (116, 245, 255),  # #74F5FF
    "Surya":      (255, 215, 0),    # #FFD700
}


# ── Canonical Typography Roles (Section 4.2) ─────────────────────────────────
FONT_CEREMONIAL = ("Cinzel", "Times New Roman", "serif")
FONT_INTERFACE   = ("Space Grotesk", "Arial", "sans-serif")
FONT_TELEMETRY   = ("JetBrains Mono", "Consolas", "monospace")


# ── Motion & Animation Helpers (Section 4.4) ─────────────────────────────────
def pulse_alpha(elapsed: float, low: int = 90, high: int = 190,
                speed: float = 3.0, reduced: bool = False) -> int:
    """Return a pulsing alpha value, honoring the player's reduced motion setting."""
    if reduced:
        return low
    phase = (math.sin(elapsed * speed) + 1.0) * 0.5
    return int(low + (high - low) * phase)


# ── Drawing Primitives (Section 4.3 & 5) ──────────────────────────────────────
def _chamfer_points(left: float, right: float, bottom: float, top: float, cut: float = 8.0):
    """Calculate the 8 vertices of an octagonally chamfered box."""
    cut = min(cut, max(1.0, (right - left) / 3.0), max(1.0, (top - bottom) / 3.0))
    return [
        (left + cut, bottom), (right - cut, bottom),
        (right, bottom + cut), (right, top - cut),
        (right - cut, top), (left + cut, top),
        (left, top - cut), (left, bottom + cut),
    ]


def draw_chamfered_panel(left: float, right: float, bottom: float, top: float,
                         accent=GOLD, *, fill=SURFACE_LOW, alpha: int = 225,
                         border_width: int = 1, selected: bool = False,
                         cut: float = 8.0, scanlines: bool = False) -> None:
    """Draw an authentic Tier 1-3 chamfered glass panel with luminous border."""
    points = _chamfer_points(left, right, bottom, top, cut)
    arcade.draw_polygon_filled(points, (*fill[:3], alpha))

    border_alpha = min(255, alpha + 25 if selected else alpha)
    width = max(border_width, 2 if selected else border_width)
    for i, point in enumerate(points):
        nxt = points[(i + 1) % len(points)]
        arcade.draw_line(point[0], point[1], nxt[0], nxt[1],
                         (*accent[:3], border_alpha), width)

    # Accent hairline near top edge
    if top - bottom > 18:
        arcade.draw_line(left + cut + 6, top - 3, right - cut - 6, top - 3,
                         (*accent[:3], min(110, border_alpha)), 1)

    if scanlines and top - bottom > 20:
        draw_scanlines(left + 2, right - 2, bottom + 2, top - 2, CYAN, spacing=16, alpha=6)


def draw_corner_etching(left: float, right: float, bottom: float, top: float,
                        color=GOLD, length: float = 12.0, alpha: int = 90) -> None:
    """Draw four cockpit-style L-bracket etchings around a focal panel."""
    c = (*color[:3], alpha)
    arcade.draw_line(left, top, left + length, top, c, 1)
    arcade.draw_line(left, top, left, top - length, c, 1)
    arcade.draw_line(right, top, right - length, top, c, 1)
    arcade.draw_line(right, top, right, top - length, c, 1)
    arcade.draw_line(left, bottom, left + length, bottom, c, 1)
    arcade.draw_line(left, bottom, left, bottom + length, c, 1)
    arcade.draw_line(right, bottom, right - length, bottom, c, 1)
    arcade.draw_line(right, bottom, right, bottom + length, c, 1)


def draw_segmented_bar(left: float, right: float, bottom: float, top: float,
                       fraction: float, color=CYAN, segments: int = 10,
                       background=WELL, gap: float = 3.0,
                       ghost_fraction: float = 0.0) -> None:
    """Render a canonical 10-segment telemetry bar with optional ghost trail."""
    fraction = max(0.0, min(1.0, fraction))
    ghost_fraction = max(fraction, min(1.0, ghost_fraction))
    width = right - left
    segment_width = (width - gap * (segments - 1)) / segments

    for i in range(segments):
        x1 = left + i * (segment_width + gap)
        x2 = x1 + segment_width
        filled = fraction >= (i + 1) / segments
        partial = max(0.0, min(1.0, fraction * segments - i))

        # Base background well
        arcade.draw_lrbt_rectangle_filled(x1, x2, bottom, top, (*background[:3], 220))

        # Ghost decay trail
        if ghost_fraction > fraction:
            g_partial = max(0.0, min(1.0, ghost_fraction * segments - i))
            if g_partial > 0:
                arcade.draw_lrbt_rectangle_filled(
                    x1, x1 + segment_width * g_partial, bottom, top,
                    (*GHOST_TRAIL, 180)
                )

        # Active fill
        if filled or partial > 0:
            arcade.draw_lrbt_rectangle_filled(
                x1, x1 + segment_width * partial, bottom, top,
                (*color[:3], 240),
            )


def draw_scanlines(left: float, right: float, bottom: float, top: float,
                   color=CYAN, spacing: int = 18, alpha: int = 8) -> None:
    """Draw subtle vertical or horizontal holographic scanline mesh."""
    y = bottom + spacing
    while y < top:
        arcade.draw_line(left, y, right, y, (*color[:3], alpha), 1)
        y += spacing


def draw_telemetry_ticks(left: float, right: float, y: float, color=CYAN,
                         count: int = 12, height: float = 5, alpha: int = 80) -> None:
    """Draw horizontal tick marks for cockpit dials and frame boundaries."""
    if count < 2:
        return
    step = (right - left) / (count - 1)
    arcade.draw_line(left, y, right, y, (*color[:3], alpha // 2), 1)
    for index in range(count):
        tick_height = height * (1.5 if index in (0, count - 1) else 1.0)
        x = left + index * step
        arcade.draw_line(x, y - tick_height, x, y + tick_height, (*color[:3], alpha), 1)


def draw_menu_backdrop(title: str, subtitle: str = "", accent=GOLD,
                       *, pulse: float = 0.0, reduced: bool = False) -> None:
    """Draw standard command-console backdrop used by front-end screens."""
    arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, OBSIDIAN)
    arcade.draw_lrbt_rectangle_filled(24, WIDTH - 24, 74, HEIGHT - 74, (*SURFACE_LOW, 175))
    arcade.draw_lrbt_rectangle_filled(24, WIDTH - 24, 74, 170, (*VOID, 125))

    for index in range(42):
        sx = 38 + ((index * 137) % (WIDTH - 76))
        sy = 92 + ((index * 71) % (HEIGHT - 184))
        drift = 0.0 if reduced else (pulse * (0.8 + (index % 3) * 0.22))
        x = 28 + ((sx + drift) % (WIDTH - 56))
        twinkle = 70 + ((index * 17) % 70)
        arcade.draw_circle_filled(x, sy, 0.7 + (index % 2) * 0.45,
                                  (110, 180, 220, twinkle))

    draw_scanlines(24, WIDTH - 24, 58, HEIGHT - 58, CYAN, spacing=24, alpha=6)
    draw_corner_etching(24, WIDTH - 24, 24, HEIGHT - 24, accent, length=22, alpha=105)
    arcade.draw_line(24, HEIGHT - 74, WIDTH - 24, HEIGHT - 74, (*accent, 105), 1)
    arcade.draw_line(24, 74, WIDTH - 24, 74, (*CYAN, 48), 1)

    arcade.draw_text(title, 42, HEIGHT - 52, accent, font_size=22, bold=True,
                     font_name=FONT_INTERFACE)
    if subtitle:
        arcade.draw_text(subtitle, 42, HEIGHT - 68, MUTED, font_size=8, bold=True,
                         font_name=FONT_TELEMETRY)
    draw_back_navigation()
    if not reduced:
        alpha = pulse_alpha(pulse, 12, 30, 1.7)
        arcade.draw_circle_outline(WIDTH - 100, HEIGHT - 50, 28, (*accent, alpha), 1)
        arcade.draw_line(WIDTH - 132, HEIGHT - 50, WIDTH - 68, HEIGHT - 50, (*accent, alpha), 1)
        arcade.draw_line(WIDTH - 100, HEIGHT - 82, WIDTH - 100, HEIGHT - 18, (*accent, alpha), 1)
    arcade.draw_text("AKASHIC LINK  //  LOCAL CONSOLE", WIDTH - 30, 38,
                     (*MUTED, 190), font_size=7, bold=True, anchor_x="right",
                     font_name=FONT_TELEMETRY)


def draw_focus_panel(left: float, right: float, bottom: float, top: float,
                     accent=CYAN, *, selected: bool = False) -> None:
    """Draw a highlighted Tier 2 focus panel."""
    draw_chamfered_panel(left, right, bottom, top, accent,
                         fill=SURFACE_HIGH if selected else SURFACE_LOW,
                         alpha=238, border_width=2 if selected else 1,
                         selected=selected, cut=10)


def draw_back_navigation(label: str = "ESC  BACK") -> None:
    """Standardized top-right back button hint."""
    arcade.draw_text(label, WIDTH - 30, HEIGHT - 52, MUTED, font_size=8,
                     bold=True, anchor_x="right", anchor_y="center",
                     font_name=FONT_TELEMETRY)


def draw_state_badge(x: float, y: float, label: str, color=CYAN, *, width: float = 92) -> None:
    """Draw a small chamfered status badge (e.g. READY, LOCKED, CLEARED)."""
    draw_chamfered_panel(x - width / 2, x + width / 2, y - 10, y + 10,
                         color, fill=WELL, alpha=225, border_width=1, cut=4)
    arcade.draw_text(label, x, y - 3, color, font_size=8, bold=True,
                     anchor_x="center", font_name=FONT_TELEMETRY)


# ==============================================================================
# [53/77] MODULE: game/views/__init__.py
# ==============================================================================
# game/views/__init__.py


# ==============================================================================
# [54/77] MODULE: game/views/account_view.py
# ==============================================================================
"""Account and stable Game ID screen.

The game remains playable as a guest, but this view lets a player link a
stable Vimana Wars identity to online leaderboard submissions. Network work
is delegated to ``LeaderboardClient`` so the Arcade render thread never
blocks while a server is unavailable.
"""
import arcade

from constants import WIDTH, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.systems.sound_manager import SoundManager
from game.ui.menu_button import MenuButton
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT, CYAN,
    CYAN_BRIGHT, PARCHMENT, MUTED, RED_BRIGHT,
    draw_chamfered_panel, draw_corner_etching,
)


class AccountView(arcade.View):
    """Email account registration/login and local profile display."""

    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self.sound_manager = SoundManager()
        saved = save_system.load()
        self._email = saved.get("account_email", "")
        self._password = ""
        self._player_name = saved.get("player_name", "Warrior")
        self._mode = "login"
        self._reset_token = ""
        self._verify_token = ""
        self._selected_field = 0
        self._submitting = False
        self._pending_result = None
        self._pending_logout = None
        self._pending_stats = None
        self._pending_action = None
        self._account_stats = None
        self._status_msg = ""
        self._status_color = MUTED
        self._hovered = -1
        self._pulse = 0.0
        self._nav_rail = NavRail(current_screen="account")

        self._title = arcade.Text(
            "ACCOUNT // ASTRAL IDENTITY", WIDTH // 2, 548,
            GOLD_BRIGHT, font_size=25, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "LINK YOUR WARSHIP TO A PERMANENT VIMANA WARS GAME ID",
            WIDTH // 2, 516, CYAN_BRIGHT, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, 105, MUTED, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "TAB / ↑↓ : FIELD   •   ENTER : CONFIRM   •   ESC : BACK",
            WIDTH // 2, 32, MUTED, font_size=10,
            anchor_x="center", anchor_y="center",
        )

        self._buttons = self._build_buttons()

    def _build_buttons(self):
        cx = (240 + WIDTH - 90) // 2  # 525
        if leaderboard_client.current_account():
            data = [
                ("SIGN OUT OF ASTRAL NETWORK", "logout", RED_BRIGHT, 300, 38, 145),
                ("BACK TO COMMAND DECK", "back", CYAN, 240, 32, 100),
            ]
        elif self._mode == "reset_request":
            data = [
                ("SEND RECOVERY TOKEN  ▶", "submit", GOLD, 290, 38, 140),
                ("RETURN TO SIGN IN", "login", CYAN, 250, 32, 95),
            ]
        elif self._mode == "reset_password":
            data = [
                ("UPDATE PASSWORD  ▶", "submit", GOLD, 290, 38, 140),
                ("RETURN TO SIGN IN", "login", CYAN, 250, 32, 95),
            ]
        elif self._mode == "verify":
            data = [
                ("CONFIRM VERIFICATION  ▶", "submit", CYAN, 290, 38, 140),
                ("RETURN TO SIGN IN", "login", MUTED, 250, 32, 95),
            ]
        elif self._mode == "register":
            data = [
                ("CREATE ASTRAL IDENTITY  ▶", "submit", GOLD, 310, 38, 145),
                ("ALREADY REGISTERED? SIGN IN", "login", CYAN, 280, 32, 100),
            ]
        else:  # login
            data = [
                ("SIGN IN TO WARSHIP  ▶", "submit", GOLD, 290, 38, 145),
                ("NEED AN ACCOUNT? CREATE ONE", "register", CYAN, 290, 32, 100),
                ("FORGOT PASSWORD / RECOVERY", "reset_request", MUTED, 240, 26, 62),
            ]

        buttons = []
        for label, action, color, w, h, y in data:
            buttons.append((MenuButton(label, cx, y, w, h, color), action))
        return buttons

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        self._buttons = self._build_buttons()
        self._hovered = -1
        self._account_stats = None
        if leaderboard_client.current_account():
            def on_stats(stats, error):
                self._pending_stats = (stats, error)
            leaderboard_client.fetch_account_stats(on_stats)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._nav_rail.update(delta_time)
        self._pulse += delta_time
        for i, (button, _) in enumerate(self._buttons):
            button.update(delta_time, i == self._hovered)
        if self._pending_result is not None:
            result = self._pending_result
            self._pending_result = None
            self._submitting = False
            success, error, user = result
            if success and user:
                self._password = ""
                if user.get("verification_required") and not leaderboard_client.current_account():
                    self._mode = "verify"
                    self._selected_field = 0
                    self._verify_token = user.get("verification_token", "")
                    self._status_msg = "ACCOUNT CREATED — ENTER THE VERIFICATION TOKEN FROM YOUR EMAIL"
                    if user.get("verification_token"):
                        self._status_msg += f"  •  DEV TOKEN {user['verification_token']}"
                else:
                    self._status_msg = f"ACCOUNT LINKED  •  GAME ID {user.get('game_id', '')}"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            else:
                self._status_msg = error or "Account request failed"
                self._status_color = RED_BRIGHT
        if self._pending_logout is not None:
            (error,) = self._pending_logout
            self._pending_logout = None
            self._submitting = False
            self._status_msg = error or "SIGNED OUT — guest mode active"
            self._status_color = MUTED if error else CYAN_BRIGHT
            self._buttons = self._build_buttons()
        if self._pending_stats is not None:
            stats, error = self._pending_stats
            self._pending_stats = None
            self._account_stats = stats or {}
            if error and not self._status_msg:
                self._status_msg = error
                self._status_color = MUTED
        if self._pending_action is not None:
            success, error, body = self._pending_action
            self._pending_action = None
            self._submitting = False
            if success and self._mode == "reset_request":
                self._mode = "reset_password"
                self._selected_field = 2
                if body.get("reset_token"):
                    self._reset_token = body["reset_token"]
                    self._status_msg = "RESET CODE READY — set a new password below"
                else:
                    self._status_msg = "RESET INSTRUCTIONS CREATED — check your email"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            elif success and self._mode == "reset_password":
                self._mode = "login"
                self._password = ""
                self._reset_token = ""
                self._selected_field = 1
                self._status_msg = "PASSWORD UPDATED — sign in with your new password"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            elif success and self._mode == "verify":
                self._mode = "login"
                self._selected_field = 1
                self._status_msg = "EMAIL VERIFIED — ACCOUNT LINKED"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            elif not success:
                self._status_msg = error or "Account action failed"
                self._status_color = RED_BRIGHT

    def _draw_background(self) -> None:
        self.clear()
        arcade.draw_lrbt_rectangle_filled(240, WIDTH - 90, 50, 490, (9, 14, 25, 240))
        draw_chamfered_panel(240, WIDTH - 90, 50, 490, CYAN,
                             fill=OBSIDIAN, alpha=240, border_width=1, cut=16)
        draw_corner_etching(240, WIDTH - 90, 50, 490, GOLD, length=20, alpha=130)
        # Slow scan line gives the account console a little life.
        scan_y = 65 + ((self._pulse * 24) % 410)
        arcade.draw_lrbt_rectangle_filled(265, WIDTH - 115, scan_y, scan_y + 1, (80, 210, 255, 30))

    def _draw_tabs(self) -> None:
        tabs = [("SIGN IN", "login"), ("CREATE ACCOUNT", "register"), ("RECOVERY", "reset_request"), ("PILOT CARD", "profile")]
        cx = (240 + WIDTH - 90) // 2
        tab_start_x = cx - 180
        for i, (t_label, t_mode) in enumerate(tabs):
            tx = tab_start_x + i * 120
            if leaderboard_client.current_account():
                active = (t_mode == "profile")
            else:
                active = (self._mode == t_mode or (t_mode == "login" and self._mode not in ("register", "reset_request", "reset_password", "verify", "profile")))
            col = GOLD_BRIGHT if active else MUTED
            arcade.draw_text(t_label, tx, 452, col, font_size=10, bold=True, anchor_x="center", font_name=FONT_INTERFACE)
            if active:
                arcade.draw_line(tx - 35, 442, tx + 35, 442, GOLD, 2)

    def _get_fields(self):
        cx = (240 + WIDTH - 90) // 2  # 525
        w = 420
        left = cx - w // 2
        right = cx + w // 2

        if self._mode == "register":
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 370, 404), False, "Used to link your permanent Game ID"),
                (1, "PASSWORD (MIN 8 CHARS)", "•" * len(self._password) if self._password else "", (left, right, 305, 339), True, "Secured on celestial server"),
                (2, "WARRIOR CALLSIGN", self._player_name, (left, right, 240, 274), False, "Displayed on the global leaderboard"),
            ]
        elif self._mode == "reset_request":
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 340, 376), False, "A reset token will be delivered to your inbox"),
            ]
        elif self._mode == "reset_password":
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 370, 404), False, "Registered email address"),
                (1, "RESET TOKEN", self._reset_token, (left, right, 305, 339), False, "Paste token received in email"),
                (2, "NEW PASSWORD", "•" * len(self._password) if self._password else "", (left, right, 240, 274), True, "Minimum 8 characters"),
            ]
        elif self._mode == "verify":
            return [
                (0, "VERIFICATION TOKEN", self._verify_token, (left, right, 340, 376), False, "Enter token delivered by email"),
            ]
        else:  # login
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 350, 386), False, "Registered pilot email"),
                (1, "PASSWORD", "•" * len(self._password) if self._password else "", (left, right, 270, 306), True, "Account password"),
            ]

    def _draw_profile(self, account: dict) -> None:
        draw_chamfered_panel(540, 840, 160, 410, GOLD, fill=SURFACE_LOW, alpha=245, cut=9)
        draw_corner_etching(540, 840, 160, 410, GOLD, length=12, alpha=100)
        
        arcade.draw_text("PILOT CARD", 690, 380, GOLD_BRIGHT, font_size=14, bold=True, anchor_x="center")
        arcade.draw_text("WARRIOR DESIGNATION", 690, 340, MUTED, font_size=8, bold=True, anchor_x="center")
        arcade.draw_text(account.get("player_name", "Warrior").upper(), 690, 315, PARCHMENT, font_size=16, bold=True, anchor_x="center")
        
        arcade.draw_text("GAME ID", 690, 270, MUTED, font_size=8, bold=True, anchor_x="center")
        arcade.draw_text(account.get("game_id", "—"), 690, 245, CYAN_BRIGHT, font_size=20, bold=True, anchor_x="center")
        
        stats = self._account_stats or {}
        score = int(stats.get('best_score', 0))
        arcade.draw_text(f"TOTAL SCORE: {score:,}", 690, 190, GOLD, font_size=10, bold=True, anchor_x="center")

        arcade.draw_text("ASTRAL IDENTITY ACTIVE", 390, 300, CYAN_BRIGHT, font_size=14, bold=True, anchor_x="center")

    def _draw_form(self) -> None:
        fields = self._get_fields()
        for i, label, value, (left, right, bottom, top), is_pwd, hint in fields:
            selected = self._selected_field == i
            accent = CYAN_BRIGHT if selected else (65, 90, 125)
            fill = SURFACE_HIGH if selected else SURFACE_LOW
            arcade.draw_text(label, left, top + 5, accent, font_size=8, bold=True)
            draw_chamfered_panel(left, right, bottom, top, accent,
                                 fill=fill, alpha=245, border_width=2 if selected else 1, cut=6)
            shown = value or "TYPE HERE"
            shown_color = PARCHMENT if value else MUTED
            arcade.draw_text(shown, left + 14, bottom + 10, shown_color, font_size=11)
            if selected and hint:
                arcade.draw_text(hint, left, bottom - 14, (110, 135, 165), font_size=7)

    def on_draw(self) -> None:
        self._draw_background()
        self._title.draw()
        self._subtitle.draw()
        self._draw_tabs()
        account = leaderboard_client.current_account()
        if account:
            self._draw_profile(account)
        else:
            self._draw_form()
        if self._status_msg:
            msg_lower = self._status_msg.lower()
            if "error" in msg_lower or "fail" in msg_lower or "required" in msg_lower:
                pill_color = (220, 50, 50)
            elif "success" in msg_lower or "registered" in msg_lower or "signed in" in msg_lower or "secured" in msg_lower or "linked" in msg_lower or "verified" in msg_lower or "ready" in msg_lower:
                pill_color = (50, 200, 100)
            else:
                pill_color = (200, 180, 50)
            
            w = len(self._status_msg) * 6.5 + 40
            cx, cy = (240 + WIDTH - 90) // 2, 195
            draw_chamfered_panel(cx - w//2, cx + w//2, cy - 12, cy + 12, pill_color, fill=(*pill_color[:3], 40), alpha=255, cut=6)
            
            self._status_text.text = self._status_msg
            self._status_text.color = pill_color
            self._status_text.x = cx
            self._status_text.y = cy
            self._status_text.draw()
        for button, _ in self._buttons:
            button.draw()
        self._hint.draw()
        self._nav_rail.draw()
        TransitionOverlay.draw()

    def _back(self) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()
        target = self.return_view
        if target is None:
            from game.views.menu_view import MenuView
            target = MenuView()
        transition_to(self.window, target)

    def _submit(self) -> None:
        if self._submitting:
            return
        email = self._email.strip()
        password = self._password
        if self._mode == "verify":
            if not self._verify_token:
                self._status_msg = "Verification token is required"
                self._status_color = RED_BRIGHT
                return
        elif self._mode == "reset_request":
            if not email:
                self._status_msg = "Email is required"
                self._status_color = RED_BRIGHT
                return
        elif self._mode == "reset_password":
            if not self._reset_token or not password:
                self._status_msg = "Reset token and new password are required"
                self._status_color = RED_BRIGHT
                return
            if len(password) < 8:
                self._status_msg = "Password must be at least 8 characters"
                self._status_color = RED_BRIGHT
                return
        elif not email or not password:
            self._status_msg = "Email and password are required"
            self._status_color = RED_BRIGHT
            return
        if self._mode == "register" and len(password) < 8:
            self._status_msg = "Password must be at least 8 characters"
            self._status_color = RED_BRIGHT
            return
        self._submitting = True
        self._status_msg = "CONTACTING ASTRAL IDENTITY SERVER..."
        self._status_color = CYAN_BRIGHT

        def on_done(success, error, user):
            self._pending_result = (success, error, user)

        def on_action_done(success, error, body):
            # Only queue data here; on_update owns all visible UI changes.
            self._pending_action = (success, error, body)

        if self._mode == "register":
            leaderboard_client.register(email, password, self._player_name.strip() or "Warrior", on_done)
        elif self._mode == "login":
            leaderboard_client.login(email, password, on_done)
        elif self._mode == "reset_request":
            leaderboard_client.request_password_reset(email, on_action_done)
        elif self._mode == "reset_password":
            leaderboard_client.reset_password(self._reset_token, password, on_action_done)
        elif self._mode == "verify":
            leaderboard_client.verify_email(self._verify_token, on_action_done)

    def _activate(self, action: str) -> None:
        if action == "back":
            self._back()
        elif action == "submit":
            self._submit()
        elif action in ("login", "switch_login"):
            self._mode = "login"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action in ("register", "switch_register"):
            self._mode = "register"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action in ("reset_request", "switch_reset"):
            self._mode = "reset_request"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action == "reset_password":
            self._mode = "reset_password"
            self._selected_field = 1
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action == "verify":
            self._mode = "verify"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action == "logout":
            self._submitting = True
            self._status_msg = "SIGNING OUT..."
            self._status_color = MUTED

            def on_done(error):
                self._pending_logout = (error,)

            leaderboard_client.logout(on_done)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)
        new_hovered = -1
        for i, (button, _) in enumerate(self._buttons):
            if button.contains(x, y):
                new_hovered = i
                break
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.18)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT or self._submitting:
            return
        nav = self._nav_rail.on_mouse_press(x, y, self.window)
        if nav:
            return
        
        # Tab selection
        if 430 <= y <= 475:
            cx = (240 + WIDTH - 90) // 2
            tab_start_x = cx - 180
            for i, t_mode in enumerate(["login", "register", "reset_request", "profile"]):
                tx = tab_start_x + i * 120
                if tx - 55 <= x <= tx + 55:
                    if t_mode in ("login", "register", "reset_request"):
                        self.sound_manager.play_ui_click()
                        self._activate(t_mode)
                    return
                    
        account = leaderboard_client.current_account()
        if not account:
            for i, label, value, (left, right, bottom, top), is_pwd, hint in self._get_fields():
                if left <= x <= right and bottom <= y <= top:
                    self._selected_field = i
                    self.sound_manager.play_ui_click(volume=0.2)
                    return

        for i, (menu_button, action) in enumerate(self._buttons):
            if menu_button.contains(x, y):
                self._hovered = i
                self.sound_manager.play_ui_click()
                self._activate(action)
                return

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            self._back()
            return
        if self._submitting or leaderboard_client.current_account():
            return
        fields = self._get_fields()
        num_fields = len(fields) if fields else 1
        if key in (arcade.key.TAB, arcade.key.DOWN):
            self._selected_field = (self._selected_field + 1) % num_fields
        elif key in (arcade.key.UP,):
            self._selected_field = (self._selected_field - 1) % num_fields
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            self._submit()
        elif key == arcade.key.F1:
            self._activate("login")
        elif key == arcade.key.F2:
            self._activate("register")
        elif key == arcade.key.BACKSPACE:
            self._delete_character()

    def _delete_character(self) -> None:
        if self._selected_field == 0:
            if self._mode == "verify":
                self._verify_token = self._verify_token[:-1]
            else:
                self._email = self._email[:-1]
        elif self._selected_field == 1:
            if self._mode == "reset_password":
                self._reset_token = self._reset_token[:-1]
            else:
                self._password = self._password[:-1]
        elif self._selected_field == 2:
            if self._mode == "reset_password":
                self._password = self._password[:-1]
            else:
                self._player_name = self._player_name[:-1]

    def on_text(self, text: str) -> None:
        if self._submitting or leaderboard_client.current_account() or not text.isprintable():
            return
        if self._selected_field == 0:
            if self._mode == "verify" and len(self._verify_token) < 128:
                self._verify_token += text
            elif self._mode != "verify" and len(self._email) < 254:
                self._email += text
        elif self._selected_field == 1 and len(self._password) < 128:
            if self._mode == "reset_password":
                self._reset_token += text
            else:
                self._password += text
        elif self._selected_field == 2:
            if self._mode == "reset_password" and len(self._password) < 128:
                self._password += text
            elif self._mode != "reset_password" and len(self._player_name) < 20:
                self._player_name += text

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y or hat_x:
            self.on_key_press(arcade.key.DOWN if (hat_y < 0 or hat_x > 0) else arcade.key.UP, 0)

    def on_joybutton_press(self, joystick, button) -> None:
        if button == 0:
            self._submit()
        elif button in (1, 4):
            self._back()


# ==============================================================================
# [55/77] MODULE: game/views/achievements_view.py
# ==============================================================================
"""Browsable trophy cabinet for every achievement in the campaign."""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WHITE
from game.systems import save_system
from game.systems.achievement_system import ACHIEVEMENTS_LIST
from game.ui.nav_rail import NavRail
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

        # Nav Rail
        self._nav_rail = NavRail(current_screen="codex")

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
        self._nav_rail.update(delta_time)

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
            # Shift columns right by 170px to clear the 220px nav rail
            cx = 420 + col * 400
            cy = 430 - row * 88
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
        self._nav_rail.draw()
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
            cx = 420 + col * 400
            cy = 430 - row * 88
            if cx - 180 <= x <= cx + 180 and cy - 32 <= y <= cy + 32:
                return index
        return -1

    def on_mouse_motion(self, x, y, dx, dy):
        self._nav_rail.on_mouse_motion(x, y)
        index = self._item_at(x, y)
        if index >= 0:
            self._selected = index

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            nav = self._nav_rail.on_mouse_press(x, y, self.window)
            if nav:
                return
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


# ==============================================================================
# [56/77] MODULE: game/views/boon_select_view.py
# ==============================================================================
"""
game/views/boon_select_view.py
3-Card Roguelite Deva Blessing selection screen between waves.
Presented during wave transitions so the player can choose an astral upgrade.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE
from game.ui.easing import ease_out_back, ease_out_cubic, lerp, clamp
from game.ui.tween import TweenManager
from game.ui.transitions import TransitionOverlay
from game.systems.sound_manager import SoundManager
from game.ui.vedic_theme import draw_chamfered_panel, draw_corner_etching
from arcade import draw_rect_filled, LRBT


class CardState:
    def __init__(self):
        self.flip_progress = 0.0
        self.lift = 0.0
        self.scale = 1.0
        self.alpha = 255.0
        self.fly_text_y = 0.0
        self.fly_text_alpha = 0.0
        # Cached Text objects — content/position/alpha updated per frame.
        # Using Text (not draw_text) avoids the slow-draw silent-failure path
        # that was making the cards invisible in the user's screenshot.
        self._text_deva = arcade.Text("", 0, 0, (255, 255, 255, 255),
                                      font_size=9, bold=True,
                                      anchor_x="center", anchor_y="center")
        self._text_name = arcade.Text("", 0, 0, (255, 255, 255, 255),
                                      font_size=13, bold=True,
                                      anchor_x="center", anchor_y="center")
        self._text_num  = arcade.Text("", 0, 0, (255, 255, 255, 255),
                                      font_size=18, bold=True,
                                      anchor_x="center", anchor_y="center")
        # 4 description lines is enough for our 24-char wrapped boons
        self._text_desc = [arcade.Text("", 0, 0, (210, 215, 230, 255),
                                        font_size=10, bold=True,
                                        anchor_x="center", anchor_y="center")
                           for _ in range(4)]
        self._text_claim = arcade.Text("", 0, 0, (255, 220, 50, 255),
                                       font_size=9, bold=True,
                                       anchor_x="center", anchor_y="center")
        self._text_fly = arcade.Text("", 0, 0, (255, 215, 0, 255),
                                     font_size=16, bold=True,
                                     anchor_x="center", anchor_y="center")


class BoonSelectView(arcade.View):
    def __init__(self, game_view, choices: list[dict]):
        super().__init__()
        self.game_view = game_view
        self.choices = choices
        self._selected_card = 0
        self._pulse = 0.0

        self.sound_manager = SoundManager()
        self._tweens = TweenManager()
        
        self._pick_phase = False
        self._pick_timer = 0.0
        self._transition_started = False
        
        self._cards = [CardState() for _ in range(len(self.choices))]
        
        # Background Particles
        self._particles = []
        for _ in range(20):
            self._particles.append({
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(0, HEIGHT),
                "speed": random.uniform(10, 30),
                "wobble_offset": random.uniform(0, math.pi * 2),
                "wobble_speed": random.uniform(1, 3),
                "wobble_amp": random.uniform(5, 15)
            })

        # UI Text Objects
        self._title = arcade.Text(
            "BLESSING OF THE DEVAS",
            WIDTH // 2, HEIGHT - 70,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._sub = arcade.Text(
            "Choose a Divine Astral Boon to empower your Vimana",
            WIDTH // 2, HEIGHT - 110,
            COLOR_WAVE, font_size=14,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "1, 2, 3 or ← → : Select   •   ENTER / Click : Claim Boon",
            WIDTH // 2, 35,
            (160, 170, 200), font_size=12, bold=True,
            anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        
        if hasattr(self.game_view, "player"):
            self.game_view.player.reset_input_state()
        
        for i, card in enumerate(self._cards):
            card.flip_progress = 0.0
            card.lift = 0.0
            card.scale = 1.0
            card.alpha = 255.0
            card.fly_text_y = 0.0
            card.fly_text_alpha = 0.0
            
            self._tweens.tween(
                target=card,
                attr="flip_progress",
                end=1.0,
                duration=0.4,
                ease=ease_out_back,
                delay=i * 0.15
            )

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time
        self._tweens.update(delta_time)
        TransitionOverlay.update(delta_time)
        
        # Update particles
        for p in self._particles:
            p["y"] += p["speed"] * delta_time
            if p["y"] > HEIGHT + 20:
                p["y"] = -20
                p["x"] = random.uniform(0, WIDTH)

        # Handle smooth hover states if not picked
        if not self._pick_phase:
            for i, card in enumerate(self._cards):
                is_sel = (i == self._selected_card)
                target_lift = 12.0 if is_sel else 0.0
                target_scale = 1.05 if is_sel else 1.0
                target_alpha = 255.0 if is_sel else 153.0
                
                card.lift = lerp(card.lift, target_lift, delta_time * 10)
                card.scale = lerp(card.scale, target_scale, delta_time * 10)
                card.alpha = lerp(card.alpha, target_alpha, delta_time * 10)
        else:
            self._pick_timer -= delta_time
            if self._pick_timer <= 0 and not self._transition_started:
                self._transition_started = True
                if hasattr(self.game_view, "player"):
                    self.game_view.player.reset_input_state()
                self.window.show_view(self.game_view)

    def on_draw(self) -> None:
        self.clear()

        # Draw background particles
        chosen = self.choices[self._selected_card]
        p_color = chosen["color"]
        for p in self._particles:
            px = p["x"] + math.sin(p["wobble_offset"] + self._pulse * p["wobble_speed"]) * p["wobble_amp"]
            py = p["y"]
            arcade.draw_circle_filled(px, py, 2, (p_color[0], p_color[1], p_color[2], 100))

        self._title.draw()
        self._sub.draw()

        card_w = 230
        card_h = 320
        start_x = WIDTH // 2 - 270
        spacing = 270
        cy = HEIGHT // 2 - 20

        for i, boon in enumerate(self.choices):
            card = self._cards[i]
            is_sel = (i == self._selected_card)

            # Draw Face Down Back
            if card.flip_progress <= 0.0:
                cx = start_x + i * spacing
                # Direct low-level call: avoids the convenience-layer alpha
                # parsing that has caused "invisible cards" regressions before.
                draw_rect_filled(LRBT(
                    cx - card_w // 2, cx + card_w // 2,
                    cy - card_h // 2, cy + card_h // 2,
                ), (20, 25, 45, 255))
                # Rotating glow rings
                arcade.draw_arc_outline(
                    cx, cy, 80, 80, (100, 120, 200, 150),
                    0, 270, border_width=4, tilt_angle=math.degrees(self._pulse * 3)
                )
                arcade.draw_arc_outline(
                    cx, cy, 50, 50, (80, 100, 180, 100),
                    0, 180, border_width=2, tilt_angle=math.degrees(-self._pulse * 4)
                )
                continue

            width_scale = card.flip_progress
            cx = start_x + i * spacing
            cy_lifted = cy + card.lift

            w = card_w * width_scale * card.scale
            h = card_h * card.scale

            alpha = int(clamp(card.alpha, 0.0, 255.0))

            # Card Background & Glowing Chamfered Border (Vedic-Punk theme)
            l = cx - int(w / 2)
            r = cx + int(w / 2)
            b = cy_lifted - int(h / 2)
            t = cy_lifted + int(h / 2)

            if is_sel:
                pulse_t = (math.sin(self._pulse * 4) + 1.0) / 2.0
                pulse_val = int(200 + 55 * ease_out_cubic(pulse_t))
                border_col = (boon["color"][0], boon["color"][1], boon["color"][2], min(alpha, pulse_val))
                border_w = max(2, int(3 * card.scale))
                fill_col = (35, 45, 80)
            else:
                border_col = (70, 80, 110, alpha)
                border_w = max(1, int(1 * card.scale))
                fill_col = (20, 26, 40)

            draw_chamfered_panel(l, r, b, t, accent=border_col, fill=fill_col,
                                 alpha=alpha, border_width=border_w, selected=is_sel, cut=12)
            draw_corner_etching(l + 4, r - 4, b + 4, t - 4, color=boon["color"],
                                length=14, alpha=int(min(140, alpha * 0.75)))

            text_alpha = int(alpha * clamp(width_scale, 0.0, 1.0))
            if text_alpha <= 0:
                continue

            # God Name Header
            arcade.draw_text(
                boon["deva"],
                cx, cy_lifted + 125 * card.scale,
                (200, 210, 240, text_alpha), font_size=int(9 * card.scale), bold=True, anchor_x="center"
            )

            # Boon Name
            b_col = boon["color"]
            arcade.draw_text(
                boon["name"],
                cx, cy_lifted + 90 * card.scale,
                (b_col[0], b_col[1], b_col[2], text_alpha), font_size=int(13 * card.scale), bold=True, anchor_x="center"
            )

            # Decorative Emblem
            arcade.draw_circle_filled(cx, cy_lifted + 20 * card.scale, 36 * card.scale, (15, 20, 35, alpha))
            arcade.draw_circle_outline(cx, cy_lifted + 20 * card.scale, 36 * card.scale, (b_col[0], b_col[1], b_col[2], alpha), int(2 * card.scale))
            arcade.draw_text(
                f"[{i + 1}]",
                cx, cy_lifted + 12 * card.scale,
                (255, 255, 255, text_alpha), font_size=int(18 * card.scale), bold=True, anchor_x="center"
            )

            # Description (Wrapped)
            desc_lines = self._wrap_text(boon["desc"], 24)
            for l_idx, line in enumerate(desc_lines):
                arcade.draw_text(
                    line,
                    cx, cy_lifted - 45 * card.scale - l_idx * 18 * card.scale,
                    (210, 215, 230, text_alpha), font_size=int(10 * card.scale), bold=True, anchor_x="center"
                )

            # Selection Tag
            if is_sel and not self._pick_phase:
                t2 = (math.sin(self._pulse * 4) + 1.0) / 2.0
                pulse_val2 = int(200 + 55 * ease_out_cubic(t2))
                arcade.draw_text(
                    "★ PRESS ENTER TO CLAIM ★",
                    cx, cy_lifted - 135 * card.scale,
                    (255, 220, 50, pulse_val2), font_size=int(9 * card.scale), bold=True, anchor_x="center"
                )
                
            # Picked Fly Text
            if card.fly_text_alpha > 0:
                arcade.draw_text(
                    "+1 BOON OBTAINED",
                    cx, cy_lifted + card.fly_text_y,
                    (255, 215, 0, int(card.fly_text_alpha)), font_size=16, bold=True, anchor_x="center"
                )

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
        if self._pick_phase:
            return
            
        old_sel = self._selected_card
        
        if key in (arcade.key.LEFT, arcade.key.A):
            self._selected_card = (self._selected_card - 1) % len(self.choices)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._selected_card = (self._selected_card + 1) % len(self.choices)
        elif key == arcade.key.KEY_1 and len(self.choices) >= 1:
            self._selected_card = 0
            self._claim_selected()
        elif key == arcade.key.KEY_2 and len(self.choices) >= 2:
            self._selected_card = 1
            self._claim_selected()
        elif key == arcade.key.KEY_3 and len(self.choices) >= 3:
            self._selected_card = 2
            self._claim_selected()
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._claim_selected()
            
        if self._selected_card != old_sel:
            self.sound_manager.play_ui_click()

    def on_key_release(self, key, modifiers) -> None:
        if hasattr(self.game_view, "player"):
            self.game_view.player.keys_pressed.discard(key)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        if hasattr(self.game_view, "player"):
            self.game_view.player.mouse_x = x
            self.game_view.player.mouse_y = y
            self.game_view.player.mouse_held = False
        if not self._pick_phase:
            card_w = 230
            card_h = 320
            start_x = WIDTH // 2 - 270
            spacing = 270
            cy = HEIGHT // 2 - 20
            for i in range(len(self.choices)):
                cx = start_x + i * spacing
                if cx - card_w // 2 <= x <= cx + card_w // 2 and cy - card_h // 2 <= y <= cy + card_h // 2:
                    if self._selected_card != i:
                        self._selected_card = i
                        self.sound_manager.play_ui_click(volume=0.20)
                    break

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if self._pick_phase:
            return
            
        if hasattr(self.game_view, "player"):
            self.game_view.player.mouse_x = x
            self.game_view.player.mouse_y = y
            self.game_view.player.mouse_held = False

        card_w = 230
        card_h = 320
        start_x = WIDTH // 2 - 270
        spacing = 270
        cy = HEIGHT // 2 - 20

        for i in range(len(self.choices)):
            cx = start_x + i * spacing
            if cx - card_w // 2 <= x <= cx + card_w // 2 and cy - card_h // 2 <= y <= cy + card_h // 2:
                old_sel = self._selected_card
                self._selected_card = i
                if old_sel != i:
                    self.sound_manager.play_ui_click()
                self._claim_selected()
                break

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        if hasattr(self.game_view, "player"):
            self.game_view.player.mouse_held = False

    def _claim_selected(self) -> None:
        if self._pick_phase:
            return
            
        self._pick_phase = True
        self._pick_timer = 0.6
        self._transition_started = False
        
        chosen = self.choices[self._selected_card]
        self.game_view.apply_boon(chosen)
        
        for i, card in enumerate(self._cards):
            if i == self._selected_card:
                self._tweens.tween(card, "scale", 1.3, 0.3, ease=ease_out_back)
                self._tweens.tween(card, "fly_text_y", 40.0, 0.5, ease=ease_out_cubic)
                card.fly_text_alpha = 255.0
                self._tweens.tween(card, "fly_text_alpha", 0.0, 0.5, ease=ease_out_cubic, delay=0.2)
            else:
                self._tweens.tween(card, "alpha", 76.5, 0.2, ease=ease_out_cubic)


# ==============================================================================
# [57/77] MODULE: game/views/codex_view.py
# ==============================================================================
"""
game/views/codex_view.py
The Realm Archives & Mythological Lore Codex.
Provides in-depth lore, vector illustrations, and tactical guides for Vimanas, Astras, Asuras, and Realms.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import draw_menu_backdrop, draw_focus_panel, CYAN_BRIGHT, MUTED


CODEX_ENTRIES = [
    {
        "category": "TRANSMISSION",
        "title": "The Reclamation of Dharma",
        "subtitle": "Opening Briefing // The Celestial Order",
        "color": (255, 246, 223),
        "lore": "Dharma is unraveling. Ravana has broken his exile and is draining Prana from the celestial realms to rebuild his tenfold power. The last Vimana pilot must cut a corridor through four falling heavens and reach Lanka before the balance is extinguished.",
        "tip": "Begin with Swarga. Learn the flight path, collect Deva Astras, and keep moving when the warning telemetry turns red.",
        "speaker": "AKASHIC ARCHIVIST // COMMAND BRIEFING",
    },
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
        self._page = 0
        self._page_size = 7
        self._pulse = 0.0

        # Nav Rail
        self._nav_rail = NavRail(current_screen="codex")

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
        self._nav_rail.update(delta_time)

    def on_draw(self) -> None:
        draw_menu_backdrop("THE REALM ARCHIVES & CODEX", "TACTICAL RECORDS // VIMANAS, ASTRAS, ASURAS", COLOR_SCORE, pulse=self._pulse)
        self._title.draw()

        # Left Sidebar (Entries List) — shifted right to clear 220px nav rail
        sidebar_x = 240
        sidebar_w = 260
        start_y = HEIGHT - 95

        page_count = (len(CODEX_ENTRIES) + self._page_size - 1) // self._page_size
        page_start = self._page * self._page_size
        visible_entries = CODEX_ENTRIES[page_start:page_start + self._page_size]
        for local_i, entry in enumerate(visible_entries):
            i = page_start + local_i
            y = start_y - local_i * 52
            is_sel = (i == self._selected)

            if is_sel:
                draw_focus_panel(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, entry["color"], selected=True)
            else:
                draw_focus_panel(sidebar_x, sidebar_x + sidebar_w, y - 18, y + 26, entry["color"])

            arcade.draw_text(f"[{entry['category']}]", sidebar_x + 14, y + 10, (140, 150, 180), font_size=8, bold=True)
            arcade.draw_text(entry["title"], sidebar_x + 14, y - 8, entry["color"] if is_sel else (200, 205, 220), font_size=12, bold=True)

        arcade.draw_text(
            f"ARCHIVE PAGE {self._page + 1}/{page_count}",
            sidebar_x, 92, MUTED, font_size=8, bold=True,
        )
        arcade.draw_text(
            "Q / E  PAGE   •   CLICK AN ENTRY",
            sidebar_x + sidebar_w, 92, MUTED, font_size=8, bold=True,
            anchor_x="right",
        )

        # Right Detail Panel
        detail_x = 530
        detail_w = WIDTH - detail_x - 30
        detail_y = HEIGHT - 100
        detail_h = 420

        arcade.draw_lrbt_rectangle_filled(detail_x, detail_x + detail_w, detail_y - detail_h, detail_y, (22, 26, 48))
        cur = CODEX_ENTRIES[self._selected]
        arcade.draw_lrbt_rectangle_outline(detail_x, detail_x + detail_w, detail_y - detail_h, detail_y, cur["color"], 2)

        # Header Details
        arcade.draw_text(cur["title"].upper(), detail_x + 30, detail_y - 45, cur["color"], font_size=22, bold=True)
        arcade.draw_text(cur["subtitle"], detail_x + 30, detail_y - 75, (170, 185, 215), font_size=12, bold=True)
        arcade.draw_line(detail_x + 30, detail_y - 90, detail_x + detail_w - 30, detail_y - 90, (60, 70, 100), 1)

        if cur.get("speaker"):
            arcade.draw_text(cur["speaker"], detail_x + 30, detail_y - 105,
                             CYAN_BRIGHT, font_size=8, bold=True)

        # Lore Paragraph
        lore_top = detail_y - (142 if cur.get("speaker") else 125)
        arcade.draw_text("MYTHOLOGICAL RECORD:", detail_x + 30, lore_top, COLOR_SCORE, font_size=11, bold=True)
        lore_lines = self._wrap_text(cur["lore"], 40)
        for l_idx, line in enumerate(lore_lines):
            arcade.draw_text(line, detail_x + 30, lore_top - 30 - l_idx * 22, (220, 225, 240), font_size=11)

        # Tactical Tip Box
        tip_y = detail_y - 300
        arcade.draw_lrbt_rectangle_filled(detail_x + 30, detail_x + detail_w - 30, tip_y - 60, tip_y + 10, (15, 18, 32))
        arcade.draw_lrbt_rectangle_outline(detail_x + 30, detail_x + detail_w - 30, tip_y - 60, tip_y + 10, (80, 140, 200), 1)
        arcade.draw_text("TACTICAL DOCTRINE:", detail_x + 45, tip_y - 12, (100, 220, 255), font_size=9, bold=True)
        tip_lines = self._wrap_text(cur["tip"], 38)
        for t_idx, line in enumerate(tip_lines):
            arcade.draw_text(line, detail_x + 45, tip_y - 32 - t_idx * 18, (190, 200, 220), font_size=9)

        self._hint.draw()
        self._nav_rail.draw()
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
            self._page = self._selected // self._page_size
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected = (self._selected + 1) % len(CODEX_ENTRIES)
            self._page = self._selected // self._page_size
        elif key in (arcade.key.Q, arcade.key.LEFT):
            page_count = (len(CODEX_ENTRIES) + self._page_size - 1) // self._page_size
            self._page = (self._page - 1) % page_count
            self._selected = self._page * self._page_size
        elif key in (arcade.key.E, arcade.key.RIGHT):
            page_count = (len(CODEX_ENTRIES) + self._page_size - 1) // self._page_size
            self._page = (self._page + 1) % page_count
            self._selected = self._page * self._page_size
        elif key == arcade.key.ESCAPE:
            if self.return_view:
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)

        # The list remains keyboard-friendly, but pointer selection now works
        # consistently with the rest of the front-end.
        sidebar_x = 240
        sidebar_w = 260
        start_y = HEIGHT - 95
        if sidebar_x <= x <= sidebar_x + sidebar_w:
            for local_i in range(self._page_size):
                y_pos = start_y - local_i * 52
                if y_pos - 18 <= y <= y_pos + 26:
                    index = self._page * self._page_size + local_i
                    if index < len(CODEX_ENTRIES):
                        self._selected = index
                    break

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        nav = self._nav_rail.on_mouse_press(x, y, self.window)
        if nav:
            return
        self.on_mouse_motion(x, y, 0, 0)


# ==============================================================================
# [58/77] MODULE: game/views/difficulty_view.py
# ==============================================================================
"""
game/views/difficulty_view.py
Difficulty selection screen shown before the game starts.
Reads/writes via save_system so the choice persists between sessions.
"""
import math
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_WAVE, COLOR_WHITE
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import draw_menu_backdrop, draw_focus_panel


_OPTIONS = ["easy", "normal", "hard", "endless"]
_DESCRIPTIONS = {
    "easy":    "More HP  ·  Less damage  ·  Fewer enemies",
    "normal":  "The intended mythological campaign",
    "hard":    "Less HP  ·  More damage  ·  Elite foes",
    "endless": "Mahayuddha: Infinite scaling waves & continuous boss encounters",
}
_COLORS = {
    "easy":    (60, 220, 100),
    "normal":  (220, 200, 60),
    "hard":    (220, 60, 60),
    "endless": (220, 90, 255),
}


class DifficultyView(arcade.View):
    def __init__(self, start_wave: int = 1, realm_id: int | None = None, initial_difficulty: str | None = None):
        super().__init__()
        self.start_wave = max(1, int(start_wave))
        self.realm_id = realm_id
        saved = save_system.load()
        chosen = initial_difficulty or saved.get("difficulty", "normal")
        self._selected = _OPTIONS.index(chosen) if chosen in _OPTIONS else 1
        self._hovered = -1
        self._pulse = 0.0
        self.sound_manager = SoundManager()

        # Nav Rail
        self._nav_rail = NavRail(current_screen="campaign")

        # ── Static text ──────────────────────────────────────────────
        self._title = arcade.Text(
            "SELECT GAMEPLAY MODE",
            WIDTH // 2, int(HEIGHT * 0.86),
            COLOR_WAVE, font_size=26, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._option_texts = [
            arcade.Text(
                opt.upper() if opt != "endless" else "ENDLESS MAHAYUDDHA",
                WIDTH // 2, int(HEIGHT * 0.68) - i * 62,
                _COLORS[opt], font_size=18, bold=True,
                anchor_x="center", anchor_y="center",
            )
            for i, opt in enumerate(_OPTIONS)
        ]
        self._desc_texts = [
            arcade.Text(
                _DESCRIPTIONS[opt],
                WIDTH // 2, int(HEIGHT * 0.68) - i * 62 - 20,
                (160, 160, 180), font_size=9,
                anchor_x="center", anchor_y="center",
            )
            for i, opt in enumerate(_OPTIONS)
        ]
        self._hint = arcade.Text(
            "↑ ↓ to choose   ENTER to confirm   ESC to go back",
            WIDTH // 2, int(HEIGHT * 0.08),
            (130, 130, 160), font_size=11,
            anchor_x="center",
        )
        # Cursor arrow (updated in draw)
        self._cursor = arcade.Text(
            "▶", 0, 0,
            COLOR_WHITE, font_size=18, bold=True,
            anchor_x="right", anchor_y="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self._nav_rail.update(delta_time)


    def on_draw(self) -> None:
        draw_menu_backdrop("SELECT GAMEPLAY MODE", "CHOOSE A SORTIE PROFILE", COLOR_WAVE, pulse=self._pulse)
        self._title.draw()

        for i, (opt, txt, desc) in enumerate(
            zip(_OPTIONS, self._option_texts, self._desc_texts)
        ):
            # Highlight the selected option
            if i == self._selected or i == self._hovered:
                pulse = 0.85 + 0.15 * math.sin(self._pulse * 4)
                r, g, b = _COLORS[opt]
                txt.color = (int(r * pulse), int(g * pulse), int(b * pulse))

                # Draw selection box
                cy = int(HEIGHT * 0.68) - i * 62
                draw_focus_panel(WIDTH // 2 - 210, WIDTH // 2 + 210, cy - 26, cy + 26, _COLORS[opt], selected=i == self._selected)
                if i == self._selected:
                    # Cursor
                    self._cursor.x = WIDTH // 2 - 220
                    self._cursor.y = cy
                    self._cursor.draw()
            else:
                r, g, b = _COLORS[opt]
                txt.color = (r // 2, g // 2, b // 2)   # dimmed when not selected

            txt.draw()
            desc.draw()

        self._hint.draw()
        self._nav_rail.draw()
        TransitionOverlay.draw()

    def _row_at(self, x: float, y: float) -> int:
        if not WIDTH // 2 - 230 <= x <= WIDTH // 2 + 230:
            return -1
        for i in range(len(_OPTIONS)):
            cy = int(HEIGHT * 0.68) - i * 62
            if cy - 30 <= y <= cy + 30:
                return i
        return -1

    def _confirm(self) -> None:
        if TransitionOverlay.is_active:
            return
        chosen = _OPTIONS[self._selected]
        save_system.set_difficulty(chosen)
        self.sound_manager.play_ui_click()
        from game.views.ship_select_view import ShipSelectView
        transition_to(
            self.window,
            ShipSelectView(
                difficulty=chosen,
                start_wave=self.start_wave,
                realm_id=self.realm_id,
            ),
        )

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)
        new_hovered = self._row_at(x, y)
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.20)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        nav = self._nav_rail.on_mouse_press(x, y, self.window)
        if nav:
            return
        row = self._row_at(x, y)
        if row < 0:
            return
        if row == self._selected:
            self._confirm()
        else:
            self._selected = row
            self.sound_manager.play_ui_click(volume=0.35)


    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._selected = (self._selected - 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._selected = (self._selected + 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            self._confirm()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y > 0:
            self._selected = (self._selected - 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif hat_y < 0:
            self._selected = (self._selected + 1) % len(_OPTIONS)
            self.sound_manager.play_ui_click(volume=0.25)


# ==============================================================================
# [59/77] MODULE: game/views/game_over_view.py
# ==============================================================================
"""
game/views/game_over_view.py
Game-over screen — shows stats, high score, and difficulty played.
Uses arcade.Text objects (no draw_text calls).
"""
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_SCORE, COLOR_WHITE
from game.systems import save_system
from game.ui.easing import ease_out_cubic, ease_in_out_cubic, clamp
from game.ui.tween import TweenManager
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    draw_menu_backdrop, draw_focus_panel,
    ASTRA_RED, ASTRA_RED_BRIGHT, STARLIGHT, GREY, FONT_CEREMONIAL, FONT_INTERFACE,
)


class GameOverView(arcade.View):
    def __init__(self, score: int, wave: int, kills: int,
                 highest_combo: int, high_score: int = 0, difficulty: str = "normal",
                 ship_class: str = "pushpaka", stats: dict = None,
                 start_wave: int = 1, is_endless: bool = False):
        super().__init__()
        self._pulse = 0.0
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.start_wave = start_wave
        self.is_endless = is_endless
        self.stats = stats or {}
        is_new_record = score >= high_score and score > 0

        self._tweens = TweenManager()
        self._title_chars = 0.0
        self._displayed_score = 0.0
        self._final_score = score
        
        # ── Particles ────────────────────────────────────────────────
        self._embers = []
        
        # ── Title ────────────────────────────────────────────────────
        self._title_text_str = "GAME OVER"
        self._title = arcade.Text(
            self._title_text_str,
            WIDTH // 2, int(HEIGHT * 0.82),
            (220, 30, 30), font_size=52, bold=True,
            font_name=FONT_CEREMONIAL[0],
            anchor_x="center", anchor_y="center",
        )

        # Subtitle lore line below title
        self._t_subtitle = arcade.Text(
            "VESSEL DESTROYED  \u2022  KARMA PRESERVED",
            WIDTH // 2, int(HEIGHT * 0.82) - 36,
            (*ASTRA_RED_BRIGHT[:3], 180), font_size=11, bold=True,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )

        # ── New record banner ────────────────────────────────────────
        self._is_new_record = is_new_record
        self._record_banner = arcade.Text(
            "★  NEW HIGH SCORE  ★" if is_new_record else "",
            WIDTH // 2, int(HEIGHT * 0.72),
            (255, 220, 50), font_size=14, bold=True,
            anchor_x="center", anchor_y="center",
        )

        # ── Stats table ──────────────────────────────────────────────
        diff_colors = {"easy": (60, 220, 100), "normal": (220, 200, 60), "hard": (220, 60, 60)}
        total_dmg = self.stats.get("total_damage", 0)
        perf_dodges = self.stats.get("perfect_dodges", 0)
        syn_list = self.stats.get("synergies_activated", [])
        syn_str = ", ".join(s[:10] for s in syn_list) if syn_list else "None"

        self._stat_rows_data = [
            ("SCORE",           0,                    COLOR_SCORE),
            ("HIGH SCORE",      f"{high_score:,}",    (200, 200, 200)),
            ("DIFFICULTY",      difficulty.upper(),   diff_colors.get(difficulty, COLOR_WHITE)),
            ("WAVES SURVIVED",  f"{wave}",            COLOR_WHITE),
            ("ENEMIES SLAIN",   f"{kills}",           COLOR_WHITE),
            ("HIGHEST COMBO",   f"×{highest_combo}",  COLOR_WHITE),
            ("TOTAL DAMAGE",    f"{total_dmg:,}",     (255, 160, 60)),
            ("PERFECT DODGES",  f"{perf_dodges}",     (100, 255, 200)),
            ("DEVA SYNERGIES",  syn_str,              (255, 120, 220)),
        ]
        
        num_rows = len(self._stat_rows_data)
        self._stat_labels = []
        self._stat_values = []
        self._row_alphas = [0.0] * num_rows

        for i, (label, value, val_color) in enumerate(self._stat_rows_data):
            y = int(HEIGHT * 0.62) - i * 22
            self._stat_labels.append(arcade.Text(
                label, WIDTH // 2 - 160, y,
                (*GREY[:3], 0), font_size=10, bold=True,
                font_name=FONT_INTERFACE[0],
            ))
            val_str = str(value)
            self._stat_values.append(arcade.Text(
                val_str, WIDTH // 2 + 160, y,
                (*val_color[:3], 0), font_size=11, bold=True,
                font_name=FONT_INTERFACE[0],
                anchor_x="right",
            ))

        # ── Prompt ───────────────────────────────────────────────────
        self._prompt = arcade.Text(
            "R \u2014 REINCARNATE (RETRY)   \u2022   A \u2014 ARSENAL   \u2022   L \u2014 AKASHIC RECORDS   \u2022   ESC \u2014 RETURN TO SOURCE",
            WIDTH // 2, int(HEIGHT * 0.06),
            STARLIGHT, font_size=11, bold=True,
            font_name=FONT_INTERFACE[0],
            anchor_x="center",
        )

    def on_show_view(self) -> None:
        arcade.set_background_color((15, 2, 5))
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()
        
        # Start tweens
        self._tweens.cancel_all()
        
        # 1. Title typewriter
        self._tweens.tween(
            self, "_title_chars",
            end=len(self._title_text_str),
            duration=0.8,
            ease=ease_out_cubic,
            start=0.0
        )
        
        # 2. Score count up (starting at 0.5s)
        self._tweens.tween(
            self, "_displayed_score",
            end=self._final_score,
            duration=1.0, 
            delay=0.5,
            ease=ease_out_cubic,
            start=0.0
        )
        
        # 3. Staggered row reveals
        class FloatRef:
            def __init__(self):
                self.val = 0.0
                
        self._alpha_refs = [FloatRef() for _ in range(len(self._row_alphas))]
        for i, ref in enumerate(self._alpha_refs):
            self._tweens.tween(
                ref, "val",
                end=255.0,
                duration=0.5, 
                delay=1.0 + i * 0.15,
                ease=ease_out_cubic,
                start=0.0
            )

    def on_update(self, delta_time: float) -> None:
        self._tweens.update(delta_time)
        TransitionOverlay.update(delta_time)

        # Sync row alphas from refs
        if hasattr(self, "_alpha_refs"):
            for i, ref in enumerate(self._alpha_refs):
                self._row_alphas[i] = ref.val

        # Prompt uses ease_in_out_cubic pulse
        self._pulse += delta_time
        cycle = (self._pulse % 2.0)
        t = cycle if cycle <= 1.0 else 2.0 - cycle
        eased_t = ease_in_out_cubic(t)
        alpha = int(100 + 155 * eased_t)
        p_c = self._prompt.color
        self._prompt.color = (p_c[0], p_c[1], p_c[2], alpha)

        # Update dynamic score text
        self._stat_values[0].text = f"{int(self._displayed_score):,}"

        # Apply alphas to stat rows
        for i, a in enumerate(self._row_alphas):
            a_int = int(clamp(a, 0, 255))
            lbl_color = self._stat_labels[i].color
            val_color = self._stat_values[i].color
            self._stat_labels[i].color = (lbl_color[0], lbl_color[1], lbl_color[2], a_int)
            self._stat_values[i].color = (val_color[0], val_color[1], val_color[2], a_int)

        # Embers logic
        for _ in range(2):
            self._embers.append({
                "x": random.uniform(0, WIDTH),
                "y": HEIGHT + 10,
                "vy": random.uniform(-60, -20),
                "size": random.uniform(1, 3),
                "life": random.uniform(2.0, 5.0),
                "max_life": 5.0,
                "color": random.choice([(255, 100, 50), (255, 150, 0), (200, 50, 50)])
            })
            
        for e in self._embers[:]:
            e["y"] += e["vy"] * delta_time
            e["life"] -= delta_time
            if e["life"] <= 0 or e["y"] < -10:
                self._embers.remove(e)

    def on_draw(self) -> None:
        reduced = bool(save_system.load().get("reduced_flashes", False))
        draw_menu_backdrop("DHARMIC REBIRTH", "PHYSICAL VESSEL LOST // KARMA RECORDED IN AKASHIC CHRONICLES", ASTRA_RED, pulse=self._pulse, reduced=reduced)
        draw_focus_panel(WIDTH // 2 - 230, WIDTH // 2 + 230, HEIGHT * 0.08, HEIGHT * 0.68, ASTRA_RED, selected=True)

        # Draw embers
        for e in self._embers:
            alpha = int(255 * clamp(e["life"] / e["max_life"], 0.0, 1.0))
            color = (*e["color"], alpha)
            arcade.draw_circle_filled(e["x"], e["y"], e["size"], color)

        # Draw title (typewriter effect)
        chars = int(self._title_chars)
        if chars > 0:
            self._title.text = self._title_text_str[:chars]
            self._title.draw()
            # Subtitle fades in once title is fully revealed
            if chars >= len(self._title_text_str):
                self._t_subtitle.draw()

        if self._is_new_record:
            self._record_banner.draw()

        # Draw stats
        for lbl, val in zip(self._stat_labels, self._stat_values):
            lbl.draw()
            val.draw()

        self._prompt.draw()

        TransitionOverlay.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.R:
            from game.views.game_view import GameView
            transition_to(
                self.window,
                GameView(
                    difficulty=self.difficulty,
                    ship_class=self.ship_class,
                    start_wave=self.start_wave,
                    is_endless=self.is_endless,
                ),
            )
        elif key == arcade.key.A:
            from game.views.ship_select_view import ShipSelectView
            transition_to(self.window, ShipSelectView(difficulty=self.difficulty, start_wave=self.start_wave))
        elif key == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            transition_to(self.window, LeaderboardView(return_view=self))
        elif key == arcade.key.S:
            from game.views.stats_view import StatsView
            transition_to(self.window, StatsView(return_view=self))
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())


# ==============================================================================
# [60/77] MODULE: game/views/game_view.py
# ==============================================================================
"""
game/views/game_view.py
Main gameplay loop — owns all entities, calls all systems, handles keyboard, mouse & gamepad input.
Features full ship archetypes, difficulty scaling, near-miss/perfect dodge feedback,
Deva Boons, and instant run restarts.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, get_difficulty_mults
from game.entities.player import Player
from game.entities.bullet import PlayerBullet
from game.entities.chakram import Chakram
from game.entities.ship_classes import SHIP_CLASSES
from game.systems.wave_manager import WaveManager
from game.systems.score_system import ScoreSystem
from game.systems.sound_manager import SoundManager
from game.systems.particles import ParticleManager
from game.systems.floating_text import FloatingTextManager
from game.systems.boon_system import BoonManager
from game.systems.achievement_system import AchievementManager
from game.systems.environmental_hazards import EnvironmentalHazardManager
from game.systems import collision as collision_sys
from game.systems import save_system
from game.ui.hud import HUD
from game.ui.boss_bar import BossBar
from game.ui.parallax_bg import ParallaxBackground
from game.ui.transitions import TransitionOverlay, transition_to
from game.ui.vedic_theme import (
    GOLD, CYAN, CYAN_BRIGHT, MUTED, SURFACE_HIGH, FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching,
)
from game.ui.tween import TweenManager
from game.ui.easing import ease_out_cubic, ease_out_elastic, lerp, clamp


class GameView(arcade.View):
    def __init__(self, difficulty: str = "normal", ship_class: str = "pushpaka",
                 is_endless: bool = False, start_wave: int = 1,
                 realm_id: int | None = None):
        super().__init__()
        self._difficulty = difficulty
        self._ship_class_id = ship_class
        self.is_endless = is_endless
        self.start_wave = max(1, int(start_wave))
        # ShipSelectView carries the selected realm through the flow.  Keep it
        # optional for older restart/game-over callers, deriving it from the
        # starting wave when they do not provide one.
        derived_realm = ((self.start_wave - 1) // 3) + 1
        self.realm_id = max(1, int(realm_id)) if realm_id is not None else min(7, derived_realm)
        self._mults = get_difficulty_mults(difficulty)

        sdata = SHIP_CLASSES.get(ship_class, SHIP_CLASSES["pushpaka"])

        # ── Entity lists ────────────────────────────────────────────────
        self.player = Player()
        self.player.apply_ship_class(sdata)
        self.player.dmg_taken_mult = self._mults["dmg_in"]
        self.player.max_hp = max(1, int(self.player.max_hp * self._mults["player_hp"]))
        self.player.hp = self.player.max_hp
        self._bullet_dmg = sdata["bullet_damage"]

        self.enemies: list = []
        self.player_bullets: list = []
        self.enemy_bullets: list = []
        self.powerups: list = []
        self.chakrams: list[Chakram] = []

        # ── Systems ─────────────────────────────────────────────────────
        self.wave_manager = WaveManager(
            spawn_mult=self._mults["spawn"],
            enemy_spd_mult=self._mults["enemy_spd"],
            is_endless=is_endless,
            start_wave=self.start_wave,
        )
        self.score_system = ScoreSystem()
        self.sound_manager = SoundManager()
        self.particles = ParticleManager()
        self.floating_texts = FloatingTextManager()
        self.boon_manager = BoonManager()
        self.achievement_manager = AchievementManager()
        self.hazard_manager = EnvironmentalHazardManager()

        # ── Combat Breakdown Stats ──────────────────────────────────────
        self.combat_stats = {
            "total_damage": 0,
            "perfect_dodges": 0,
            "near_misses": 0,
            "bombs_used": 0,
            "boons_claimed": 0,
            "powerups_collected": 0,
            "synergies_activated": [],
            "bosses_defeated": [],
        }

        # ── Boss Cinematic Intro State ──────────────────────────────────
        self._cinematic_timer = 0.0
        self._cinematic_title = ""
        self._cinematic_subtitle = ""
        self._cinematic_color = (255, 215, 60)

        # ── UI & Background ─────────────────────────────────────────────
        self.hud = HUD()
        self.boss_bar = BossBar()
        self.bg = ParallaxBackground()

        # Pause text objects
        self._pause_title = arcade.Text(
            "SORTIE SUSPENDED", WIDTH // 2, int(HEIGHT * 0.76),
            GOLD, font_size=28, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_INTERFACE,
        )
        self._pause_hint = arcade.Text(
            "ESC  RESUME   •   R  RESTART   •   O  SETTINGS   •   M  MENU",
            WIDTH // 2, int(HEIGHT * 0.235),
            MUTED, font_size=10, bold=True,
            anchor_x="center",
            font_name=FONT_TELEMETRY,
        )

        # ── Pause menu buttons (replaces the old key-hint overlay) ──────
        self._mouse_x = 0.0
        self._mouse_y = 0.0
        self._init_pause_buttons()

        # Playtime accumulator for lifetime stats
        self._run_playtime = 0.0
        self._playtime_save_every = 30.0  # flush to save every 30s of play

        # ── State & Juice ───────────────────────────────────────────────
        self.paused = False
        self._boss = None
        self._boss_announced = False
        self._last_boss_roar_time: float = 0.0
        self._boss_death_timer: float = 0.0
        self._was_clearing = False
        self._screen_shake = 0.0
        self._shake_intensity = 0.0
        self._hit_stop = 0.0
        self._boon_awarded_waves: set[int] = set()

        # ── Tween & Animation ───────────────────────────────────────────
        self._tweens = TweenManager()

        # ── Death Sequence State ────────────────────────────────────────
        self._death_phase = None       # None | "slowmo" | "freeze" | "fadeout"
        self._death_timer = 0.0
        self._death_time_scale = 1.0   # slows to 0.15 during death
        self._death_desat = 0.0        # 0.0 → 1.0 desaturation overlay
        self._death_fade = 0.0         # 0.0 → 1.0 fade to dark red

        saved = save_system.load()
        self.shake_setting = saved.get("screen_shake", "full")
        self.reduced_flashes = bool(saved.get("reduced_flashes", False))
        self.colorblind_mode = saved.get("colorblind_mode", "off")
        self.hud.colorblind_mode = self.colorblind_mode
        self.hud.reduced_flashes = self.reduced_flashes

        # ── Gamepad Setup ───────────────────────────────────────────────
        self.right_stick_x = 0.0
        self.right_stick_y = 0.0
        try:
            gamepads = arcade.get_gamepads()
            if gamepads:
                self.gamepad = gamepads[0]
                self.gamepad.open()
                self.gamepad.push_handlers(self)
        except Exception:
            pass

    # ── Arcade callbacks ────────────────────────────────────────────────

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        saved = save_system.load()
        self.shake_setting = saved.get("screen_shake", "full")
        self.reduced_flashes = bool(saved.get("reduced_flashes", False))
        self.colorblind_mode = saved.get("colorblind_mode", "off")
        self.hud.colorblind_mode = self.colorblind_mode
        self.hud.reduced_flashes = self.reduced_flashes
        saved["last_ship"] = self._ship_class_id
        saved["last_realm"] = self.realm_id
        save_system.save(saved)
        self.sound_manager.start_music()
        
        # Reset keys and mouse state to prevent getting stuck moving or firing after view switch
        self.player.reset_input_state()
        try:
            if hasattr(self.window, "_mouse_x") and self.window._mouse_x is not None:
                self.player.mouse_x = self.window._mouse_x
                self.player.mouse_y = self.window._mouse_y
        except Exception:
            pass

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            self.player.reset_input_state()
            return

        if self.paused:
            # Keyboard navigation of pause menu
            if key in (arcade.key.UP, arcade.key.W):
                self._pause_selected = (self._pause_selected - 1) % len(self._pause_buttons)
            elif key in (arcade.key.DOWN, arcade.key.S):
                self._pause_selected = (self._pause_selected + 1) % len(self._pause_buttons)
            elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
                self._pause_buttons[self._pause_selected].activate()
            elif key == arcade.key.R:
                self._pause_restart()
            elif key == arcade.key.O:
                self._pause_settings()
            elif key == arcade.key.M:
                self._pause_quit()
            return

        if key in (arcade.key.SPACE, arcade.key.LSHIFT, arcade.key.RSHIFT):
            self._trigger_dash()
        elif key in (arcade.key.Q, arcade.key.E):
            self._trigger_chakram()
        elif key == arcade.key.F:
            if self.player.use_bomb():
                self._activate_bomb()

        self.player.keys_pressed.add(key)

    def on_key_release(self, key, modifiers) -> None:
        self.player.keys_pressed.discard(key)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self.player.mouse_x = x
        self.player.mouse_y = y
        self.player.joy_aim_angle = None
        # Track for pause-menu hover detection
        self._mouse_x = x
        self._mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            # If paused, route click to pause menu buttons first
            if self.paused:
                for btn in self._pause_buttons:
                    if btn.hit_test(x, y):
                        btn.press()
                return

            # Check if clicked on HUD ability meters at bottom-left
            if math.hypot(x - 38, y - 32) <= 24:
                self._trigger_dash()
                return
            elif math.hypot(x - 88, y - 32) <= 24:
                self._trigger_chakram()
                return
            elif math.hypot(x - 145, y - 32) <= 24:
                if self.player.use_bomb():
                    self._activate_bomb()
                return

            self.player.mouse_held = True
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self._trigger_dash()
        elif button == arcade.MOUSE_BUTTON_MIDDLE:
            self._trigger_chakram()

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.paused:
                for btn in self._pause_buttons:
                    if btn.was_pressed:
                        btn.release()  # calls on_click if still hovered
                return
            self.player.mouse_held = False

    def on_joybutton_press(self, joystick, button) -> None:
        if self.paused:
            if button in (0, 5):
                self._pause_buttons[self._pause_selected].activate()
            elif button in (1, 4):
                self._pause_resume()
            elif button in (6, 7, 9):
                self._pause_resume()
            return
        if button in (0, 5):
            self.player.mouse_held = True
        elif button in (1, 4):
            self._trigger_dash()
        elif button in (3,):
            self._trigger_chakram()
        elif button in (2, 8):
            if self.player.use_bomb():
                self._activate_bomb()
        elif button in (6, 7, 9):
            self.paused = not self.paused

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if not self.paused:
            return
        if hat_y > 0:
            self._pause_selected = (self._pause_selected - 1) % len(self._pause_buttons)
        elif hat_y < 0:
            self._pause_selected = (self._pause_selected + 1) % len(self._pause_buttons)

    def on_joybutton_release(self, joystick, button) -> None:
        if button in (0, 5):
            self.player.mouse_held = False

    def on_joyaxis_motion(self, joystick, axis, value) -> None:
        if axis == "x":
            self.player.joy_dx = value if abs(value) > 0.15 else 0.0
        elif axis == "y":
            self.player.joy_dy = -value if abs(value) > 0.15 else 0.0
        elif axis in ("rx", "z"):
            self.right_stick_x = value
        elif axis in ("ry", "rz"):
            self.right_stick_y = -value

        if math.hypot(self.right_stick_x, self.right_stick_y) > 0.25:
            self.player.joy_aim_angle = math.degrees(
                math.atan2(self.right_stick_y, self.right_stick_x)
            )

    # ── Ability Triggers ────────────────────────────────────────────────

    def _trigger_dash(self) -> None:
        if self.player.trigger_dash():
            self.sound_manager.play_dash()
            self.particles.spawn_dash_flash(self.player.x, self.player.y)
            self.floating_texts.spawn_notification(self.player.x, self.player.y + 20, "VAYU DASH!", (100, 230, 255))
            if self.boon_manager.has_boon("vayu_tempest"):
                self.particles.spawn_explosion(self.player.x, self.player.y, radius=28, count=18, base_color=(100, 255, 180))
                # Damaging cyclone
                level = self.boon_manager.get_boon_level("vayu_tempest")
                dmg = 40 * level
                for enemy in self.enemies:
                    if enemy.alive and math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < 120:
                        enemy.take_damage(dmg)
                        self.combat_stats["total_damage"] += dmg
                        self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=5, color=(100, 255, 180))
                        if enemy.is_dead():
                            self.score_system.register_kill(enemy.score_value)
                            self.player.enemies_killed += 1
                            self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius, count=22)

            if self.boon_manager.has_synergy("solar_cyclone"):
                self.particles.spawn_explosion(self.player.x, self.player.y, radius=38, count=24, base_color=(255, 200, 40))
                for enemy in self.enemies:
                    if enemy.alive and math.hypot(enemy.x - self.player.x, enemy.y - self.player.y) < 150:
                        enemy.take_damage(60)
                        enemy._burning = 3.0
                        self.combat_stats["total_damage"] += 60
                        self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=6, color=(255, 200, 40))
                        if enemy.is_dead():
                            self.score_system.register_kill(enemy.score_value)
                            self.player.enemies_killed += 1
                            self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius, count=22)

    def _trigger_chakram(self) -> None:
        if self.player.trigger_chakram():
            self.sound_manager.play_shoot()
            chk = Chakram(self.player.x, self.player.y, self.player.angle)
            if self.boon_manager.has_boon("sudarshana_keen"):
                chk.damage = int(chk.damage * 1.4)
                chk.radius = int(chk.radius * 1.3)
            self.chakrams.append(chk)
            tag = "YAMA'S EXECUTIONER DISC!" if self.boon_manager.has_synergy("executioner_disc") else "SUDARSHANA!"
            self.floating_texts.spawn_notification(self.player.x, self.player.y + 20, tag, (255, 220, 60))

    def apply_boon(self, boon_data: dict) -> None:
        bid = boon_data["id"]
        new_syns = self.boon_manager.add_boon(bid)
        self.combat_stats["boons_claimed"] += 1
        self.sound_manager.play_powerup()
        
        level = self.boon_manager.get_boon_level(bid)
        lvl_str = f" (Lv.{level})" if level > 1 else ""
        self.floating_texts.spawn_notification(self.player.x, self.player.y + 30, f"+ {boon_data['name']}{lvl_str}", boon_data["color"])
        
        if bid == "varuna_ward":
            self.player.max_hp += 35
            self.player.heal(35)
        elif bid == "vayu_tempest":
            self.player.dash_cooldown_max *= 0.65
            self.player.dash_cooldown_timer = min(self.player.dash_cooldown_timer, self.player.dash_cooldown_max)
        elif bid == "sudarshana_keen":
            self.player.chakram_cooldown_max = max(1.0, self.player.chakram_cooldown_max - 2.0)
            self.player.chakram_cooldown_timer = min(self.player.chakram_cooldown_timer, self.player.chakram_cooldown_max)

        for syn in new_syns:
            self.sound_manager.play_synergy()
            self.floating_texts.spawn_notification(self.player.x, self.player.y + 50, f"★ SYNERGY: {syn['name'].upper()}! ★", syn["color"])
            self.particles.spawn_explosion(self.player.x, self.player.y, radius=45, count=32, base_color=syn["color"])
            self.combat_stats["synergies_activated"].append(syn["name"])

        if len(self.boon_manager.active_boons) >= 4:
            self.achievement_manager.check_unlock("boon_collector")

    # ── Update ──────────────────────────────────────────────────────────

    def on_update(self, delta_time: float) -> None:
        # Always update transitions and tweens even when paused
        TransitionOverlay.update(delta_time)
        self._tweens.update(delta_time)

        if self.paused:
            # Keep the pause-menu buttons responsive (hover anim, pulse).
            self._update_pause_buttons(delta_time)
            return

        # Track playtime for lifetime stats (not when paused or in death seq)
        if self._death_phase is None:
            self._run_playtime += delta_time
            if self._run_playtime >= self._playtime_save_every:
                try:
                    save_system.add_playtime(self._run_playtime)
                except Exception:
                    pass
                self._run_playtime = 0.0

        # ── Death Sequence ──────────────────────────────────────────────
        if self._death_phase is not None:
            self._death_timer += delta_time
            if self._death_phase == "slowmo":
                # Slow-mo for 0.5s, then freeze
                if self._death_timer >= 0.5:
                    self._death_phase = "freeze"
                    self._death_timer = 0.0
                else:
                    # Run game at reduced speed for visual drama
                    scaled_dt = delta_time * 0.15
                    self.particles.update(scaled_dt)
                    self.floating_texts.update(scaled_dt)
                    self._death_desat = clamp(self._death_timer / 0.5)
            elif self._death_phase == "freeze":
                # Hold freeze for 0.4s
                if self._death_timer >= 0.4:
                    self._death_phase = "fadeout"
                    self._death_timer = 0.0
            elif self._death_phase == "fadeout":
                # Fade to dark red over 0.6s, then transition
                self._death_fade = clamp(self._death_timer / 0.6)
                if self._death_timer >= 0.7:
                    self._death_phase = None
                    self._finish_game_over()
            return

        if self._cinematic_timer > 0:
            self._cinematic_timer -= delta_time

        if self._hit_stop > 0:
            self._hit_stop -= delta_time
            return

        was_dashing = getattr(self, "_was_dashing", False)

        # Hardware mouse safety check to eliminate stuck firing
        try:
            if hasattr(self.window, "mouse") and self.window.mouse:
                if not bool(self.window.mouse[arcade.MOUSE_BUTTON_LEFT]):
                    self.player.mouse_held = False
        except Exception:
            pass

        # Player & Passives
        kb = getattr(self.window, "keyboard", None)
        self.player.update(delta_time, keyboard_state=kb)
        self.boon_manager.update_passives(delta_time, self.player)
        self.hud.update(delta_time, self.player)

        if was_dashing and not self.player.is_dashing:
            self.particles.spawn_dash_shockwave(self.player.x, self.player.y)
        self._was_dashing = self.player.is_dashing

        if (self.player.keys_pressed or abs(self.player.joy_dx) > 0.1 or abs(self.player.joy_dy) > 0.1) and self.player.alive:
            self.particles.spawn_engine_trail(self.player.x, self.player.y, self.player.angle)

        # Garuda Magnet Boon (delta_time scaled)
        if self.boon_manager.has_boon("garuda_magnet"):
            for pu in self.powerups:
                dx = self.player.x - pu.x
                dy = self.player.y - pu.y
                dist = math.hypot(dx, dy)
                if 0 < dist < 350:
                    mag_step = 480.0 * delta_time
                    pu.x += (dx / dist) * mag_step
                    pu.y += (dy / dist) * mag_step

        # Shooting
        bullets_fired = self.player.get_bullets_to_fire()
        if bullets_fired:
            self.sound_manager.play_shoot()
            self.boon_manager.shot_counter += 1
            for angle in bullets_fired:
                b = PlayerBullet(self.player.x, self.player.y, angle)
                b.damage = self._bullet_dmg
                if self.boon_manager.has_boon("surya_beam"):
                    level = self.boon_manager.get_boon_level("surya_beam")
                    shots_req = max(2, 7 - level + 1)
                    if self.boon_manager.shot_counter % shots_req == 0:
                        b.damage = int(self._bullet_dmg * (2.0 + level * 0.2))
                        b.radius = 8
                        b.is_piercing = True
                self.player_bullets.append(b)

        # Near Miss & Perfect Dodge Checks (single reward per projectile)
        for eb in self.enemy_bullets:
            if not eb.alive: continue
            if getattr(eb, "_rewarded", False): continue
            dist = math.hypot(eb.x - self.player.x, eb.y - self.player.y)
            if self.player.is_dashing and dist < 32:
                eb._rewarded = True
                self.floating_texts.spawn_notification(self.player.x, self.player.y + 24, "PERFECT DODGE! +100", (100, 255, 200))
                self.score_system.score += 100
                self.combat_stats["perfect_dodges"] += 1
                self.sound_manager.play_dodge_chime()
                self.particles.spawn_hit_sparks(self.player.x, self.player.y, count=4, color=(100, 255, 200))
            elif not self.player.is_dashing and 15 < dist < 26:
                eb._rewarded = True
                self.floating_texts.spawn_notification(self.player.x, self.player.y + 15, "NEAR MISS! +50", (255, 230, 100))
                self.score_system.score += 50
                self.combat_stats["near_misses"] += 1
                self.sound_manager.play_dodge_chime(0.4)

        # Chakram mechanics
        for chk in self.chakrams:
            chk.update(delta_time, self.player.x, self.player.y)
            for eb in self.enemy_bullets[:]:
                if math.hypot(chk.x - eb.x, chk.y - eb.y) < chk.radius + eb.radius + 6:
                    eb.alive = False
                    self.particles.spawn_hit_sparks(eb.x, eb.y, count=4, color=(255, 220, 80))

            for enemy in self.enemies:
                if enemy.alive and math.hypot(chk.x - enemy.x, chk.y - enemy.y) < chk.radius + enemy.radius:
                    if chk.can_damage(enemy):
                        dmg = chk.damage
                        if self.boon_manager.has_boon("yama_execution") and enemy.max_hp > 0 and (enemy.hp / enemy.max_hp) < 0.45:
                            dmg = int(dmg * 1.6)
                        if self.boon_manager.has_synergy("executioner_disc") and enemy.max_hp > 0 and (enemy.hp / enemy.max_hp) < 0.25 and not getattr(enemy, "is_boss", False):
                            dmg = enemy.hp
                            self.floating_texts.spawn_notification(enemy.x, enemy.y + 15, "EXECUTED!", (255, 60, 100))

                        enemy.take_damage(dmg)
                        self.combat_stats["total_damage"] += dmg
                        self.floating_texts.spawn_damage(enemy.x, enemy.y, dmg, is_crit=True)
                        self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=7, color=(255, 215, 60))
                        if enemy.is_dead():
                            self.score_system.register_kill(enemy.score_value)
                            self.player.enemies_killed += 1
                            self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius, count=22)

        self.chakrams = [c for c in self.chakrams if c.alive]

        # Enemy updates & Burning DoT
        new_enemy_bullets = []
        for enemy in self.enemies:
            fired = enemy.update(delta_time, self.player.x, self.player.y)
            new_enemy_bullets.extend(fired)
            if hasattr(enemy, "pending_summons"):
                summons = enemy.pending_summons
                if summons:
                    self.enemies.extend(summons)

            # Healer pulse logic
            if hasattr(enemy, "perform_heal_pulse"):
                if enemy.perform_heal_pulse(self.enemies):
                    self.particles.spawn_powerup_sparkle(enemy.x, enemy.y, color=(40, 240, 140))

            # Agni Burning DoT
            if getattr(enemy, "_burning", 0) > 0:
                enemy._burning -= delta_time
                level = self.boon_manager.get_boon_level("agni_fury")
                burn_dps = 24.0 * max(1, level)
                enemy._burn_accum = getattr(enemy, "_burn_accum", 0.0) + burn_dps * delta_time
                if enemy._burn_accum >= 1.0:
                    dmg = int(enemy._burn_accum)
                    enemy._burn_accum -= dmg
                    enemy.take_damage(dmg)
                    self.combat_stats["total_damage"] += dmg
                    self.floating_texts.spawn_damage(enemy.x, enemy.y, dmg, color=(255, 120, 30))
                    self.particles.spawn_hit_sparks(enemy.x, enemy.y, count=2, color=(255, 100, 20))
                    if enemy.is_dead():
                        self.score_system.register_kill(enemy.score_value)
                        self.player.enemies_killed += 1
                        self.particles.spawn_explosion(enemy.x, enemy.y, radius=enemy.radius * 1.5, count=22, base_color=(255, 120, 30))

        self.enemy_bullets.extend(new_enemy_bullets)

        for b in self.player_bullets: b.update(delta_time)
        for b in self.enemy_bullets: b.update(delta_time)
        for pu in self.powerups: pu.update(delta_time)

        # Systems
        self.particles.update(delta_time)
        self.floating_texts.update(delta_time)
        self.achievement_manager.update(delta_time)
        self.hazard_manager.update(delta_time, self.wave_manager.wave_number, self.player, self.enemies, self.player_bullets + self.enemy_bullets)
        self.wave_manager.update(delta_time, self.enemies, self.powerups, self.player)
        self.score_system.update(delta_time)

        # Campaign milestone trophies are checked at wave start and persist
        # across runs through AchievementManager.
        wave_trophies = {
            5: "wave_5_veteran",
            10: "wave_10_breaker",
            15: "wave_15_conqueror",
        }
        trophy_id = wave_trophies.get(self.wave_manager.wave_number)
        if trophy_id:
            self.achievement_manager.check_unlock(trophy_id)

        # Inter-Wave Boon Card Trigger
        if self.wave_manager.is_clearing:
            wn = self.wave_manager.wave_number
            if wn in (1, 3, 5, 7, 9) and wn not in self._boon_awarded_waves:
                self._boon_awarded_waves.add(wn)
                from game.views.boon_select_view import BoonSelectView
                choices = self.boon_manager.get_random_choices(3)
                if choices:
                    self.player.reset_input_state()
                    self.window.show_view(BoonSelectView(self, choices))
                    return

        if self.wave_manager.is_clearing and not self._was_clearing:
            self.sound_manager.play_wave_clear()
            from game.systems import save_system as _ss
            from game.entities.ship_classes import SHIP_CLASSES as _SC
            _wave = self.wave_manager.wave_number
            for _sid, _sdata in _SC.items():
                _uw = _sdata.get("unlock_wave", 0)
                if _uw > 0 and _wave >= _uw:
                    if _ss.unlock_ship(_sid):  # Returns True if newly unlocked
                        self.floating_texts.spawn_notification(
                            self.player.x, self.player.y + 60,
                            f"⚡ {_sdata['name']} UNLOCKED!",
                            (233, 196, 0)
                        )
        self._was_clearing = self.wave_manager.is_clearing

        # Collision System
        summary = collision_sys.check_all(
            self.player, self.enemies, self.player_bullets,
            self.enemy_bullets, self.powerups, self.score_system,
            self.boon_manager
        )

        for sx, sy, scol in summary.get("hit_sparks", []):
            self.particles.spawn_hit_sparks(sx, sy, count=6, color=scol)
            self.floating_texts.spawn_damage(sx, sy, self._bullet_dmg)
            self.combat_stats["total_damage"] += self._bullet_dmg

        # Indra Chain Lightning & Plasma Storm Synergy
        if self.boon_manager.has_boon("indra_thunder"):
            for bx, by, struck_enemy in summary.get("bullet_hits", []):
                if random.random() < 0.25:
                    # Find up to 3 nearest other living enemies
                    nearby_enemies = sorted(
                        [e for e in self.enemies if e.alive and e is not struck_enemy],
                        key=lambda e: math.hypot(e.x - bx, e.y - by)
                    )[:3]
                    for nearby in nearby_enemies:
                        if math.hypot(nearby.x - bx, nearby.y - by) < 320:
                            l_dmg = 28
                            nearby.take_damage(l_dmg)
                            self.combat_stats["total_damage"] += l_dmg
                            self.particles.spawn_hit_sparks(nearby.x, nearby.y, count=5, color=(120, 220, 255))
                            
                            if self.boon_manager.has_synergy("plasma_storm"):
                                nearby.take_damage(20)
                                nearby._burning = 3.0
                                self.combat_stats["total_damage"] += 20
                                self.particles.spawn_explosion(nearby.x, nearby.y, radius=24, count=16, base_color=(255, 120, 240))

                            if nearby.is_dead():
                                self.score_system.register_kill(nearby.score_value)
                                self.player.enemies_killed += 1
                                self.particles.spawn_explosion(nearby.x, nearby.y, radius=nearby.radius, count=22)

        for ex, ey, erad, ecol in summary.get("explosions", []):
            self.particles.spawn_explosion(ex, ey, radius=erad, count=22, base_color=ecol)
            self.achievement_manager.check_unlock("first_blood")
            if self.score_system.combo >= 3:
                self.floating_texts.spawn_combo(ex, ey, self.score_system.combo)
            if self.score_system.combo >= 8:
                self.achievement_manager.check_unlock("combo_god")

        if self.score_system.score >= 25000:
            self.achievement_manager.check_unlock("high_scorer")

        for px, py, pcol in summary.get("powerup_auras", []):
            self.particles.spawn_powerup_sparkle(px, py, color=pcol)

        if summary["player_hit"]:
            self.sound_manager.play_hit()
            self._hit_stop = 0.04
            if self.shake_setting != "off":
                self._screen_shake = 0.25
                self._shake_intensity = 6.0 * (0.4 if self.shake_setting == "low" else 1.0)

        if summary["kills"] > 0 or summary.get("kamikaze_exploded"):
            self.sound_manager.play_explosion()

        if summary.get("kamikaze_exploded"):
            if self.shake_setting != "off":
                self._screen_shake = 0.40
                self._shake_intensity = 10.0 * (0.4 if self.shake_setting == "low" else 1.0)

        if summary["powerup_picked"]:
            self.sound_manager.play_powerup()
            for index, ptype in enumerate(summary["powerup_picked"]):
                self.combat_stats["powerups_collected"] += 1
                name = getattr(ptype, "name", "ABILITY")
                aura = summary.get("powerup_auras", [])
                color = aura[index][2] if index < len(aura) else (255, 220, 80)
                self.floating_texts.spawn_notification(
                    self.player.x, self.player.y + 34,
                    f"{name} BOOST!", color,
                )
                if self.combat_stats["powerups_collected"] >= 10:
                    self.achievement_manager.check_unlock("cube_collector")
                if name == "OVERDRIVE":
                    self.achievement_manager.check_unlock("overdrive_online")
            if self.boon_manager.has_synergy("oceanic_surge"):
                self.player.heal(15)
                self.floating_texts.spawn_notification(self.player.x, self.player.y + 25, "+15 HP OCEANIC SURGE!", (80, 240, 255))
                self.particles.spawn_powerup_sparkle(self.player.x, self.player.y, color=(80, 240, 255))
                for eb in self.enemy_bullets[:]:
                    if math.hypot(eb.x - self.player.x, eb.y - self.player.y) < 250:
                        eb.alive = False
                        self.particles.spawn_hit_sparks(eb.x, eb.y, count=3, color=(80, 240, 255))

        if self._screen_shake > 0:
            self._screen_shake -= delta_time
            
        if self._boss_death_timer > 0:
            self._boss_death_timer -= delta_time
            if self._boss_death_timer <= 0:
                self._boss_announced = False

        self.enemies        = [e for e in self.enemies        if e.alive]
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemy_bullets  = [b for b in self.enemy_bullets  if b.alive]
        self.powerups       = [p for p in self.powerups       if p.alive]

        # Boss Tracking & Achievements
        from game.entities.enemies.boss_ravana import BossRavana
        from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
        from game.entities.enemies.boss_mahishasura import BossMahishasura
        from game.entities.enemies.boss_vritra import BossVritra
        from game.entities.enemies.boss_hiranyakashipu import BossHiranyakashipu
        boss_types = (BossRavana, BossKumbhakarna, BossMahishasura, BossVritra, BossHiranyakashipu)
        prev_boss = self._boss
        self._boss = next(
            (e for e in self.enemies if isinstance(e, boss_types)), None
        )
        if self._boss and not self._boss_announced:
            import time as _time
            now = _time.monotonic()
            if now - self._last_boss_roar_time > 3.0:
                self._cinematic_timer = 2.4
                self.sound_manager.play_warning_siren()
                self.sound_manager.play_boss_roar()
                self._last_boss_roar_time = now
                boss_intro = {
                    "ravana": ("👑 LANKAPATI RAVANA", "LORD OF THE TEN HEADS — DEMON EMPEROR OF LANKA", (255, 60, 80)),
                    "kumbhakarna": ("🛡️ TITAN KUMBHAKARNA", "THE GIGANTIC ARMORED TITAN AWAKENS", (255, 180, 40)),
                    "mahishasura": ("🐂 WARLORD MAHISHASURA", "THE BUFFALO-DEMON WARLORD CHARGES", (255, 120, 40)),
                    "vritra": ("⚡ STORM SERPENT VRITRA", "THE FINAL SKY-BLOCKING DRAGON RISES", (190, 80, 255)),
                    "hiranyakashipu": ("👑 TYRANT HIRANYAKASHIPU", "THE INDESTRUCTIBLE DEMON LORD RISES", (255, 200, 50)),
                }
                title, subtitle, color = boss_intro.get(getattr(self._boss, "boss_id", ""), ("⚔️ BOSS INCOMING", "THE ASURA WARLORD APPROACHES", (255, 80, 100)))
                self._cinematic_title = title
                self._cinematic_subtitle = subtitle
                self._cinematic_color = color
                self._boss_announced = True
        elif not self._boss:
            if prev_boss is not None:
                boss_id = getattr(prev_boss, "boss_id", None)
                if boss_id and boss_id not in self.combat_stats["bosses_defeated"]:
                    self.combat_stats["bosses_defeated"].append(boss_id)
                    # Record boss clears immediately so a player can collect
                    # all four across separate runs, including a run that
                    # ends before the final score screen.
                    saved_bosses = save_system.load()
                    defeated = set(saved_bosses.get("bosses_defeated") or [])
                    defeated.add(boss_id)
                    saved_bosses["bosses_defeated"] = sorted(defeated)
                    save_system.save(saved_bosses)
                    self.achievement_manager.check_unlock({
                        "kumbhakarna": "kumbhakarna_bane",
                        "ravana": "ravana_vanquisher",
                        "mahishasura": "mahishasura_bane",
                        "vritra": "vritra_vanquisher",
                    }.get(boss_id, ""))
                    if len(defeated) >= 4:
                        self.achievement_manager.check_unlock("boss_collector")
            self._boss_death_timer = 1.0

        if self.wave_manager.boss_wave_cleared and not self.is_endless:
            self.achievement_manager.check_unlock("campaign_conqueror")
            if self._difficulty == "hard":
                self.achievement_manager.check_unlock("hardcore_hero")
            from game.systems import save_system as _ss
            from game.entities.ship_classes import SHIP_CLASSES as _SC
            _wave = self.wave_manager.wave_number
            for _sid, _sdata in _SC.items():
                _uw = _sdata.get("unlock_wave", 0)
                if _uw > 0 and _wave >= _uw:
                    if _ss.unlock_ship(_sid):  # Returns True if newly unlocked
                        self.floating_texts.spawn_notification(
                            self.player.x, self.player.y + 60,
                            f"⚡ {_sdata['name']} UNLOCKED!",
                            (233, 196, 0)
                        )
            self._go_to_victory()
            return

        if not self.player.alive and self._death_phase is None:
            self._start_death_sequence()

    # ── Draw ────────────────────────────────────────────────────────────

    def on_draw(self) -> None:
        import random
        self.clear()

        ox, oy = 0.0, 0.0
        if self._screen_shake > 0 and self.shake_setting != "off":
            ox = random.uniform(-self._shake_intensity, self._shake_intensity)
            oy = random.uniform(-self._shake_intensity, self._shake_intensity)

        # Background & Hazards
        self.bg.draw(self.player.x + ox, self.player.y + oy, wave_num=self.wave_manager.wave_number)
        self.hazard_manager.draw(ox, oy)

        # Aim Laser Tracer
        aim_rad = math.radians(self.player.angle)
        aim_end_x = self.player.x + math.cos(aim_rad) * 140
        aim_end_y = self.player.y + math.sin(aim_rad) * 140
        arcade.draw_line(self.player.x + ox, self.player.y + oy, aim_end_x + ox, aim_end_y + oy, (100, 200, 255, 60), 1)

        # Particles & Collectables
        self.particles.draw(ox, oy)
        for pu in self.powerups:
            pu.x += ox; pu.y += oy
            try:
                pu.draw()
            finally:
                pu.x -= ox; pu.y -= oy
        for chk in self.chakrams:
            chk.x += ox; chk.y += oy
            try:
                chk.draw()
            finally:
                chk.x -= ox; chk.y -= oy
        for enemy in self.enemies:
            enemy.x += ox; enemy.y += oy
            try:
                enemy.draw()
            finally:
                enemy.x -= ox; enemy.y -= oy
        for b in self.enemy_bullets:
            b.x += ox; b.y += oy
            try:
                b.draw()
            finally:
                b.x -= ox; b.y -= oy
        for b in self.player_bullets:
            b.x += ox; b.y += oy
            try:
                b.draw()
            finally:
                b.x -= ox; b.y -= oy

        # Player Vimana
        self.player.x += ox; self.player.y += oy
        try:
            self.player.draw()
        finally:
            self.player.x -= ox; self.player.y -= oy

        # Floating Texts & HUD
        self.floating_texts.draw(ox, oy)
        self.hud.draw(self.player, self.score_system, self.wave_manager, self.enemies, self.powerups, self.boon_manager)
        self.boss_bar.draw(self._boss)
        self.achievement_manager.draw()

        # Boss Entrance Cinematic Overlay
        if self._cinematic_timer > 0:
            self._draw_boss_cinematic()

        # Death sequence overlays
        if self._death_phase is not None:
            self._draw_death_overlay()

        if self.paused:
            self._draw_pause()

        # View transition overlay (always last)
        TransitionOverlay.draw()

    def _draw_boss_cinematic(self) -> None:
        flash_factor = 0.25 if self.reduced_flashes else 1.0
        # Widescreen cinematic letterbox bars
        bar_height = 65
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, HEIGHT - bar_height, HEIGHT, (5, 5, 12, 240))
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, bar_height, (5, 5, 12, 240))
        arcade.draw_line(0, HEIGHT - bar_height, WIDTH, HEIGHT - bar_height, self._cinematic_color, 2)
        arcade.draw_line(0, bar_height, WIDTH, bar_height, self._cinematic_color, 2)

        # Title slam with elastic easing
        cy = HEIGHT // 2 + 10
        # Progress 0→1 over the first 0.8s of the cinematic
        intro_t = clamp(1.0 - (self._cinematic_timer - 1.4) / 0.8) if self._cinematic_timer > 1.4 else 1.0
        title_scale = ease_out_elastic(intro_t) if intro_t < 1.0 else 1.0
        title_y_offset = int((1.0 - title_scale) * 80)

        # Pulsing glow
        pulse_t = clamp((math.sin(self._cinematic_timer * 6.0) + 1.0) * 0.5)
        glow_a = int(lerp(160, 255, ease_out_cubic(pulse_t)))

        # Scan line wipe (first 0.6s)
        if self._cinematic_timer > 1.8:
            scan_t = clamp(1.0 - (self._cinematic_timer - 1.8) / 0.6)
            scan_y = int(HEIGHT * ease_out_cubic(scan_t))
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, scan_y - 2, scan_y + 3, (255, 255, 255, int(60 * flash_factor)))

        arcade.draw_lrbt_rectangle_filled(WIDTH // 2 - 300, WIDTH // 2 + 300, cy - 35 - title_y_offset, cy + 45 - title_y_offset, (15, 10, 25, 210))
        arcade.draw_lrbt_rectangle_outline(WIDTH // 2 - 300, WIDTH // 2 + 300, cy - 35 - title_y_offset, cy + 45 - title_y_offset, (*self._cinematic_color, int(glow_a * flash_factor)), 2)

        arcade.draw_text(self._cinematic_title, WIDTH // 2, cy + 12 - title_y_offset, (*self._cinematic_color, int(glow_a * flash_factor)), font_size=22, bold=True, anchor_x="center", anchor_y="center")

        # Subtitle fades in 0.3s after title
        sub_alpha = int(255 * clamp((1.0 - self._cinematic_timer / 1.8) * 3.0)) if self._cinematic_timer < 1.8 else 0
        if sub_alpha > 0:
            arcade.draw_text(self._cinematic_subtitle, WIDTH // 2, cy - 18 - title_y_offset, (220, 230, 255, int(sub_alpha * flash_factor)), font_size=10, bold=True, anchor_x="center", anchor_y="center")

    def _draw_death_overlay(self) -> None:
        """Cinematic death overlay: desaturation → freeze flash → fade to dark red."""
        flash_factor = 0.25 if self.reduced_flashes else 1.0
        if self._death_desat > 0:
            # Grey desaturation overlay
            a = int(120 * self._death_desat)
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (80, 80, 80, a))

        if self._death_phase == "freeze":
            # Brief white flash at start of freeze
            flash = max(0, 1.0 - self._death_timer * 5.0)
            if flash > 0:
                arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (255, 255, 255, int(80 * flash * flash_factor)))
            # Full desaturation hold
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (80, 80, 80, 100))

        if self._death_fade > 0:
            # Fade to dark red
            a = int(255 * ease_out_cubic(self._death_fade))
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (25, 5, 8, a))

    # ── Pause menu ─────────────────────────────────────────────────────

    def _init_pause_buttons(self) -> None:
        """Build the four clickable buttons in the pause overlay."""
        from game.ui.button import Button
        bx = WIDTH // 2
        btn_w, btn_h = 240, 42
        gap = 14
        # First button starts at HEIGHT//2 + 30, stack downward
        start_y = HEIGHT // 2 + 30
        # Order: Resume, Restart, Settings, Quit to Menu
        self._pause_buttons = [
            Button(bx, start_y,            btn_w, btn_h,
                   "RESUME",       hotkey="ESC",
                   on_click=self._pause_resume),
            Button(bx, start_y - (btn_h + gap),       btn_w, btn_h,
                   "RESTART RUN",  hotkey="R",
                   on_click=self._pause_restart),
            Button(bx, start_y - 2 * (btn_h + gap),   btn_w, btn_h,
                   "SETTINGS",     hotkey="O",
                   on_click=self._pause_settings),
            Button(bx, start_y - 3 * (btn_h + gap),   btn_w, btn_h,
                   "QUIT TO MENU", hotkey="M",
                   on_click=self._pause_quit),
        ]
        # Index of currently-highlighted button (for keyboard nav)
        self._pause_selected = 0

    def _pause_resume(self) -> None:
        self.paused = False

    def _pause_restart(self) -> None:
        from game.ui.transitions import transition_to
        transition_to(self.window, GameView(
            difficulty=self._difficulty,
            ship_class=self._ship_class_id,
            is_endless=self.is_endless,
            start_wave=self.start_wave,
        ))

    def _pause_settings(self) -> None:
        from game.views.settings_view import SettingsView
        from game.ui.transitions import transition_to
        transition_to(self.window, SettingsView(return_view=self))

    def _pause_quit(self) -> None:
        from game.views.menu_view import MenuView
        from game.ui.transitions import transition_to
        # Flush playtime before leaving
        try:
            save_system.add_playtime(self._run_playtime)
        except Exception:
            pass
        self._run_playtime = 0.0
        transition_to(self.window, MenuView())

    def _update_pause_buttons(self, dt: float) -> None:
        for btn in self._pause_buttons:
            btn.update(dt, self._mouse_x, self._mouse_y)

    def _draw_pause(self) -> None:
        # 70% dim scrim
        arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, (0, 0, 0, 179))

        # Canonical Tier 2 chamfered panel
        pw, ph = 460, 340
        pl = WIDTH // 2 - pw // 2
        pr = WIDTH // 2 + pw // 2
        pb = HEIGHT // 2 - ph // 2
        pt = HEIGHT // 2 + ph // 2
        draw_chamfered_panel(pl, pr, pb, pt, GOLD,
                             fill=SURFACE_HIGH, alpha=245, border_width=2,
                             selected=True, cut=12.0, scanlines=True)
        draw_corner_etching(pl, pr, pb, pt, GOLD, length=18, alpha=130)

        # Title
        self._pause_title.draw()

        # Mini-stats panel above buttons
        self._draw_pause_mini_stats()

        # Buttons
        for btn in self._pause_buttons:
            btn.draw()

        self._pause_hint.draw()

    def _draw_pause_mini_stats(self) -> None:
        """Compact in-pause summary: wave, score, HP, boons, time-in-run."""

        cx = WIDTH // 2
        # Panel position: between title and buttons
        panel_y = HEIGHT // 2 + 105
        panel_w, panel_h = 390, 64
        draw_chamfered_panel(
            cx - panel_w / 2, cx + panel_w / 2,
            panel_y - panel_h / 2, panel_y + panel_h / 2,
            CYAN, fill=(10, 16, 28), alpha=210, border_width=1, cut=8
        )

        # Two rows of stats
        wave = self.wave_manager.wave_number
        score = self.score_system.score
        hp = self.player.hp
        max_hp = self.player.max_hp
        boons = len(self.boon_manager.active_boons)
        mins = int(self._run_playtime // 60)
        secs = int(self._run_playtime % 60)

        # Row 1: WAVE  SCORE  HP
        row1 = f"WAVE  {wave:<3}     SCORE  {score:>7,}     HP  {int(hp):>3}/{int(max_hp):<3}"
        arcade.draw_text(
            row1, cx, panel_y + 12,
            CYAN_BRIGHT, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY,
        )
        # Row 2: BOONS  TIME
        row2 = f"BOONS  {boons:<2}     TIME  {mins:02d}:{secs:02d}"
        arcade.draw_text(
            row2, cx, panel_y - 12,
            GOLD, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY,
        )


    # ── Helpers ─────────────────────────────────────────────────────────

    def _activate_bomb(self) -> None:
        self.sound_manager.play_explosion(volume=1.0)
        self.combat_stats["bombs_used"] += 1
        killed_count = 0
        for enemy in self.enemies:
            if enemy.alive:
                enemy.alive = False
                self.score_system.register_kill(enemy.score_value)
                self.player.enemies_killed += 1
                killed_count += 1
                self.combat_stats["total_damage"] += 999
                self.particles.spawn_explosion(enemy.x, enemy.y, radius=35, count=35, base_color=(255, 60, 220))
                self.floating_texts.spawn_damage(enemy.x, enemy.y, 999, is_crit=True)
        self.enemy_bullets.clear()
        if killed_count >= 8:
            self.achievement_manager.check_unlock("bomb_annihilator")

        if self.shake_setting != "off":
            self._screen_shake = 0.6
            self._shake_intensity = 14.0 if self.shake_setting == "full" else 6.0

    def _go_to_victory(self) -> None:
        SoundManager.stop_music()
        self.sound_manager.play_victory()
        
        # Save game progress
        updated = save_system.update_after_game(
            score=self.score_system.score,
            wave=self.wave_manager.wave_number,
            kills=self.player.enemies_killed,
            highest_combo=self.score_system.highest_combo,
            total_damage=self.combat_stats.get("total_damage", 0),
            boons_claimed=self.combat_stats.get("boons_claimed", 0),
            bosses_defeated=self.combat_stats.get("bosses_defeated", []),
            ship_class=self._ship_class_id,
            campaign_cleared=True,
        )
        
        saved = save_system.load()
        pilot_name = saved.get("player_name", "Warrior")
        from game.systems.leaderboard_client import leaderboard_client
        leaderboard_client.submit_score(
            player_name=pilot_name,
            score=self.score_system.score,
            level_reached=self.wave_manager.wave_number,
            difficulty=self._difficulty,
            ship_class=self._ship_class_id,
            stats={**self.combat_stats, "kills": self.player.enemies_killed},
        )
        leaderboard_client.push_profile()

        from game.views.victory_view import VictoryView
        transition_to(self.window, VictoryView(
            score=self.score_system.score,
            kills=self.player.enemies_killed,
            highest_combo=self.score_system.highest_combo,
            difficulty=self._difficulty,
            ship_class=self._ship_class_id,
            wave=self.wave_manager.wave_number,
            stats=self.combat_stats,
        ), duration=0.5, style="wipe")

    def _start_death_sequence(self) -> None:
        """Begin the cinematic death: slow-mo → freeze → fade → game over."""
        self._death_phase = "slowmo"
        self._death_timer = 0.0
        self._death_desat = 0.0
        self._death_fade = 0.0
        self.sound_manager.play_game_over()
        # Dramatic particle burst at death position
        self.particles.spawn_explosion(self.player.x, self.player.y,
                                       radius=50, count=40,
                                       base_color=(255, 60, 60))
        if self.shake_setting != "off":
            self._screen_shake = 0.5
            self._shake_intensity = 10.0

    def _finish_game_over(self) -> None:
        """Called after death sequence completes — transition directly to cinematic game over screen."""
        SoundManager.stop_music()
        
        # Save game progress and update high score
        updated = save_system.update_after_game(
            score=self.score_system.score,
            wave=self.wave_manager.wave_number,
            kills=self.player.enemies_killed,
            highest_combo=self.score_system.highest_combo,
            total_damage=self.combat_stats.get("total_damage", 0),
            boons_claimed=self.combat_stats.get("boons_claimed", 0),
            bosses_defeated=self.combat_stats.get("bosses_defeated", []),
            ship_class=self._ship_class_id,
            campaign_cleared=False,
        )
        
        # Submit score in background
        saved = save_system.load()
        pilot_name = saved.get("player_name", "Warrior")
        from game.systems.leaderboard_client import leaderboard_client
        leaderboard_client.submit_score(
            player_name=pilot_name,
            score=self.score_system.score,
            level_reached=self.wave_manager.wave_number,
            difficulty=self._difficulty,
            ship_class=self._ship_class_id,
            stats={**self.combat_stats, "kills": self.player.enemies_killed},
        )
        leaderboard_client.push_profile()

        # Direct transition to cinematic GameOverView
        from game.views.game_over_view import GameOverView
        transition_to(self.window, GameOverView(
            score=self.score_system.score,
            wave=self.wave_manager.wave_number,
            kills=self.player.enemies_killed,
            highest_combo=self.score_system.highest_combo,
            high_score=updated.get("high_score", self.score_system.score),
            difficulty=self._difficulty,
            ship_class=self._ship_class_id,
            stats=self.combat_stats,
            start_wave=self.start_wave,
            is_endless=self.is_endless,
        ), duration=0.4, style="fade")


# ==============================================================================
# [61/77] MODULE: game/views/intro_video_view.py
# ==============================================================================
"""Automatic launch cinematic shown before the loading screen.

The game deliberately keeps the cinematic inside the Arcade window instead of
opening a second media-player window.  OpenCV is used only for decoding video
frames; it is imported lazily so a missing optional decoder can never prevent
the game from starting.  In that case the view shows a short branded fallback
and continues to the normal loading screen.
"""
from __future__ import annotations

import threading
import time
from pathlib import Path

import arcade

from constants import HEIGHT, WIDTH
from game.systems.sound_manager import SoundManager
from game.ui.transitions import TransitionOverlay, transition_to
from game.ui.vedic_theme import (
    CYAN,
    CYAN_BRIGHT,
    GOLD,
    GOLD_BRIGHT,
    MUTED,
    OBSIDIAN,
    FONT_CEREMONIAL,
    FONT_TELEMETRY,
    draw_scanlines,
)
from game.ui.easing import clamp


class IntroVideoView(arcade.View):
    """Play the launch PV automatically, then hand off to ``LoadingView``."""

    def __init__(self) -> None:
        super().__init__()
        self._elapsed = 0.0
        self._duration = 1.0
        self._fallback = False
        self._fallback_message = "PREPARING CELESTIAL ORDER SYSTEMS..."
        self._finished = False
        self._eof = False
        self._reader_thread: threading.Thread | None = None
        self._stop_reader = threading.Event()
        self._frame_lock = threading.Lock()
        self._pending_frame = None
        self._texture: arcade.Texture | None = None
        self._frame_number = 0
        self._frame_size = (16, 9)

        self._title = arcade.Text(
            "VIMANA WARS",
            WIDTH // 2,
            48,
            GOLD_BRIGHT,
            font_size=16,
            bold=True,
            anchor_x="center",
            anchor_y="center",
            font_name=FONT_CEREMONIAL[0],
        )
        self._status = arcade.Text(
            "CELESTIAL ORDER // THE RECLAMATION OF DHARMA",
            WIDTH // 2,
            25,
            CYAN_BRIGHT,
            font_size=8,
            bold=True,
            anchor_x="center",
            anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )

    @property
    def _video_path(self) -> Path:
        return Path(__file__).resolve().parents[2] / "vimana_wars_pv_final.mp4"

    def on_show_view(self) -> None:
        arcade.set_background_color((0, 0, 0))
        # Arcade's built-in media backend does not decode MP4 audio, so use
        # the bundled CC0 combat bed as a reliable cinematic audio bed.  The
        # loading screen stops it before the main UI appears.
        self.sound_manager = SoundManager()
        self.sound_manager.start_music(volume=0.18)
        self._start_video_reader()

    def on_hide_view(self) -> None:
        self._stop_video_reader()

    def _start_video_reader(self) -> None:
        path = self._video_path
        if not path.exists():
            self._use_fallback("LAUNCH CINEMATIC NOT FOUND — CONTINUING...", 0.9)
            return

        try:
            import cv2
            from PIL import Image
        except ImportError:
            self._use_fallback("VIDEO DECODER NOT INSTALLED — CONTINUING...", 0.9)
            return

        capture = cv2.VideoCapture(str(path))
        if not capture.isOpened():
            capture.release()
            self._use_fallback("CINEMATIC COULD NOT BE OPENED — CONTINUING...", 0.9)
            return

        fps = float(capture.get(cv2.CAP_PROP_FPS) or 24.0)
        fps = max(1.0, min(60.0, fps))
        frame_count = float(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0)
        self._duration = max(1.0, frame_count / fps) if frame_count else 12.0
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 16)
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 9)
        self._frame_size = (max(1, frame_width), max(1, frame_height))
        self._reader_thread = threading.Thread(
            target=self._read_frames,
            args=(capture, cv2, Image, fps),
            name="vimana-intro-video",
            daemon=True,
        )
        self._reader_thread.start()

    def _use_fallback(self, message: str, duration: float) -> None:
        self._fallback = True
        self._fallback_message = message
        self._duration = duration

    def _read_frames(self, capture, cv2, image_cls, fps: float) -> None:
        """Decode at real-time speed and keep only the newest frame."""
        frame_interval = 1.0 / fps
        next_frame_at = time.monotonic()
        try:
            while not self._stop_reader.is_set():
                ok, frame = capture.read()
                if not ok:
                    break

                # The source is 2560x1440.  1280x720 is more than enough for
                # the game's logical 900x600 viewport and greatly reduces
                # texture upload cost during the intro.
                height, width = frame.shape[:2]
                if width > 1280:
                    scale = 1280.0 / width
                    frame = cv2.resize(
                        frame,
                        (1280, max(1, int(height * scale))),
                        interpolation=cv2.INTER_AREA,
                    )
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Arcade's texture hitbox path requires an RGBA image.
                image = image_cls.fromarray(frame).convert("RGBA")
                with self._frame_lock:
                    self._pending_frame = image

                next_frame_at += frame_interval
                wait = next_frame_at - time.monotonic()
                if wait > 0:
                    self._stop_reader.wait(wait)
                elif wait < -frame_interval * 2:
                    next_frame_at = time.monotonic()
        finally:
            capture.release()
            self._eof = True

    def _stop_video_reader(self) -> None:
        self._stop_reader.set()
        thread = self._reader_thread
        if thread and thread.is_alive():
            thread.join(timeout=0.25)
        self._reader_thread = None

    def _consume_pending_frame(self) -> None:
        with self._frame_lock:
            image = self._pending_frame
            self._pending_frame = None
        if image is None:
            return

        self._frame_number += 1
        # A unique hash prevents Arcade's texture cache from confusing two
        # different video frames that share the same dimensions.
        self._texture = arcade.Texture(
            image,
            hash=f"vimana-intro-frame-{self._frame_number}",
        )
        self._frame_size = (image.width, image.height)

    def _go_to_loading(self) -> None:
        if self._finished or not self.window or TransitionOverlay.is_active:
            return
        self._finished = True
        self._stop_video_reader()
        from game.views.loading_screen import LoadingView
        transition_to(self.window, LoadingView(), duration=0.45, style="fade")

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        if self._finished:
            return
        self._elapsed += max(0.0, delta_time)
        self._consume_pending_frame()

        if self._fallback:
            if self._elapsed >= self._duration:
                self._go_to_loading()
            return

        if self._eof and self._elapsed >= self._duration:
            self._go_to_loading()

    def on_draw(self) -> None:
        self.clear()
        if self._texture:
            frame_w, frame_h = self._frame_size
            scale = min(WIDTH / frame_w, HEIGHT / frame_h)
            draw_w = frame_w * scale
            draw_h = frame_h * scale
            rect = arcade.rect.LBWH(
                (WIDTH - draw_w) / 2,
                (HEIGHT - draw_h) / 2,
                draw_w,
                draw_h,
            )
            arcade.draw_texture_rect(self._texture, rect)
        else:
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, OBSIDIAN)

        # Minimal branded chrome keeps the transition intentional while the
        # first decoded frame arrives, without covering the cinematic.
        draw_scanlines(0, WIDTH, 0, HEIGHT, CYAN, spacing=36, alpha=3)
        progress = clamp(self._elapsed / max(0.1, self._duration))
        arcade.draw_lrbt_rectangle_filled(0, WIDTH * progress, 0, 3, GOLD)
        self._title.draw()
        self._status.text = self._fallback_message if self._fallback else self._status.text
        self._status.color = MUTED if self._fallback else CYAN_BRIGHT
        self._status.draw()
        arcade.draw_text(
            "PRESS ESC TO SKIP TO LOADING",
            WIDTH - 18,
            HEIGHT - 20,
            (*MUTED[:3], 190),
            font_size=8,
            anchor_x="right",
            anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        TransitionOverlay.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.ESCAPE, arcade.key.SPACE, arcade.key.ENTER):
            self._go_to_loading()


# ==============================================================================
# [62/77] MODULE: game/views/leaderboard_view.py
# ==============================================================================
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems.leaderboard_client import leaderboard_client
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import MUTED, CYAN_BRIGHT, draw_menu_backdrop, draw_focus_panel


_FILTERS = ["all", "easy", "normal", "hard", "endless"]
_FILTER_LABELS = {
    "all":    "ALL DIFFICULTIES",
    "easy":   "EASY",
    "normal": "NORMAL",
    "hard":   "HARD",
    "endless": "ENDLESS MAHAYUDDHA",
}


class LeaderboardView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._filter_index = 0
        self._pulse = 0.0

        # Nav Rail
        self._nav_rail = NavRail(current_screen="sangha")

        # UI Text elements
        self._title = arcade.Text(
            "GLOBAL LEADERBOARD",
            WIDTH // 2, HEIGHT - 50,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._tab_hint = arcade.Text(
            "TAB / ← → : Filter   •   R : Refresh   •   ESC : Back",
            WIDTH // 2, 28,
            (160, 160, 190), font_size=11, bold=True,
            anchor_x="center",
        )
        self._status_text = arcade.Text(
            "Loading scores...", WIDTH // 2, HEIGHT // 2,
            COLOR_WHITE, font_size=14,
            anchor_x="center", anchor_y="center",
        )

        # Pre-built rows text cache
        self._row_texts: list[list[arcade.Text]] = []
        self._current_filter_text = arcade.Text(
            "", WIDTH // 2, HEIGHT - 95,
            COLOR_WAVE, font_size=13, bold=True,
            anchor_x="center",
        )

        # Trigger initial fetch
        self._refresh()


    def _refresh(self) -> None:
        selected_diff = _FILTERS[self._filter_index]
        diff_arg = None if selected_diff == "all" else selected_diff
        self._status_text.text = "Contacting realm archive..."
        self._current_filter_text.text = f"«  {_FILTER_LABELS[selected_diff]}  »"
        
        leaderboard_client.fetch_top(
            limit=10,
            difficulty=diff_arg,
            on_complete=self._on_fetch_complete
        )

    def _on_fetch_complete(self, scores: list[dict], error: str | None) -> None:
        # Save raw data thread-safely; build Arcade OpenGL Text on the main thread in on_update
        self._pending_data = (scores, error)

    def _apply_fetch_results(self, scores: list[dict], error: str | None) -> None:
        self._row_texts.clear()

        if error:
            self._status_text.text = f"{error}\n(Run 'python backend/app.py' to host online server)"
            return

        if not scores:
            self._status_text.text = "No heroic deeds recorded yet in this category."
            return

        self._status_text.text = ""

        # Build table rows
        rank_colors = [
            (255, 215, 0),   # 1st Gold
            (210, 215, 230), # 2nd Silver
            (205, 127, 50),  # 3rd Bronze
        ]

        start_y = HEIGHT - 150
        row_height = 36

        for i, row in enumerate(scores):
            y = start_y - i * row_height
            rank_color = rank_colors[i] if i < 3 else (180, 180, 200)
            
            rank_str = f"#{row['rank']}"
            name_str = row['player_name']
            game_id_str = row.get('game_id') or "GUEST"
            score_str = f"{row['score']:,}"
            wave_str = f"W{row['level_reached']}"
            diff_str = row.get('difficulty', 'normal').upper()

            t_rank = arcade.Text(rank_str, 90, y, rank_color, font_size=13, bold=True)
            t_name = arcade.Text(name_str, 160, y + 6, COLOR_WHITE, font_size=12, bold=(i < 3))
            t_game_id = arcade.Text(game_id_str, 160, y - 8,
                                    CYAN_BRIGHT if game_id_str != "GUEST" else MUTED,
                                    font_size=8, bold=game_id_str != "GUEST")
            t_score = arcade.Text(score_str, WIDTH - 260, y, COLOR_SCORE, font_size=13, bold=True, anchor_x="right")
            t_wave = arcade.Text(wave_str, WIDTH - 160, y, (120, 200, 255), font_size=12, anchor_x="center")
            t_diff = arcade.Text(diff_str, WIDTH - 80, y, (160, 160, 170), font_size=11, anchor_x="right")

            self._row_texts.append([t_rank, t_name, t_game_id, t_score, t_wave, t_diff])

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self._nav_rail.update(delta_time)
        pending = getattr(self, "_pending_data", None)
        if pending is not None:
            self._pending_data = None
            scores, error = pending
            self._apply_fetch_results(scores, error)

    def on_draw(self) -> None:
        draw_menu_backdrop("GLOBAL LEADERBOARD", "ONLINE ARCHIVE // LOCAL PLAY REMAINS AVAILABLE OFFLINE", COLOR_SCORE, pulse=self._pulse)
        self._title.draw()
        self._current_filter_text.draw()

        # Header bar — offset right to clear nav rail
        header_y = HEIGHT - 122
        draw_focus_panel(240, WIDTH - 30, header_y - 6, header_y + 18, COLOR_WAVE)
        arcade.draw_text("RANK", 260, header_y, (120, 140, 180), font_size=10, bold=True)
        arcade.draw_text("WARRIOR / GAME ID", 330, header_y, (120, 140, 180), font_size=10, bold=True)
        arcade.draw_text("SCORE", WIDTH - 260, header_y, (120, 140, 180), font_size=10, bold=True, anchor_x="right")
        arcade.draw_text("WAVE", WIDTH - 160, header_y, (120, 140, 180), font_size=10, bold=True, anchor_x="center")
        arcade.draw_text("DIFFICULTY", WIDTH - 80, header_y, (120, 140, 180), font_size=10, bold=True, anchor_x="right")

        # Table rows or status
        if self._status_text.text:
            self._status_text.draw()
        else:
            for i, row in enumerate(self._row_texts):
                row_y = HEIGHT - 150 - i * 36
                if i % 2 == 1:
                    arcade.draw_lrbt_rectangle_filled(240, WIDTH - 30, row_y - 8, row_y + 20, (12, 12, 30, 80))
                for cell in row:
                    cell.draw()

        self._tab_hint.draw()
        self._nav_rail.draw()
        TransitionOverlay.draw()

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button == arcade.MOUSE_BUTTON_LEFT:
            nav = self._nav_rail.on_mouse_press(x, y, self.window)
            if nav:
                return

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.TAB, arcade.key.RIGHT, arcade.key.D):
            self._filter_index = (self._filter_index + 1) % len(_FILTERS)
            self._refresh()
        elif key in (arcade.key.LEFT, arcade.key.A):
            self._filter_index = (self._filter_index - 1) % len(_FILTERS)
            self._refresh()
        elif key == arcade.key.R:
            self._refresh()
        elif key == arcade.key.ESCAPE:
            if self.return_view:
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())



# ==============================================================================
# [63/77] MODULE: game/views/loading_screen.py
# ==============================================================================
"""
game/views/loading_screen.py
Cinematic Loading and Prologue Screen for Vimana Wars: "The Reclamation of Dharma".
Displays high-tech Vedic-punk visuals, narrative crawl, and asset initialization
telemetry after the automatic launch cinematic has finished.
"""
import math
import arcade

from constants import WIDTH, HEIGHT
from game.systems.asset_manager import AssetManager
from game.systems.sound_manager import SoundManager
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, GOLD, GOLD_BRIGHT, CYAN, CYAN_BRIGHT,
    PARCHMENT, MUTED, draw_chamfered_panel, draw_corner_etching,
    draw_segmented_bar, draw_scanlines, draw_telemetry_ticks, pulse_alpha,
    FONT_CEREMONIAL, FONT_TELEMETRY, FONT_INTERFACE
)
from game.ui.easing import ease_out_cubic, clamp


_STORY_LINES = [
    "Dharma is not a place. It is a balance — and it is breaking.",
    "Ravana has broken his exile. The celestial realms are falling under his shadow.",
    "You are the last Vimana pilot the Celestial Order could spare.",
    "Fly. Reclaim what is falling. End this at Lanka, or don't come back.",
]

_SYS_STEPS = [
    (0.15, "INITIALIZING VIMANA POWER CORE..."),
    (0.40, "ATTUNING OJAS AND PRANA TELEMETRY..."),
    (0.65, "CALIBRATING ASTRAL CANNONS AND SHIELDS..."),
    (0.85, "CONNECTING TO AKASHIC CHRONICLES..."),
    (1.00, "COMMAND CONSOLE READY"),
]


class LoadingView(arcade.View):
    def __init__(self):
        super().__init__()
        self._elapsed = 0.0
        self._progress = 0.0
        self._ready_to_advance = False
        self._advance_requested = False
        self.sound_manager = SoundManager()

        # Cached text labels
        self._title = arcade.Text(
            "VIMANA WARS", WIDTH // 2, HEIGHT - 75,
            GOLD_BRIGHT, font_size=32, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_CEREMONIAL[0],
        )
        self._subtitle = arcade.Text(
            "THE RECLAMATION OF DHARMA // CELESTIAL PROLOGUE", WIDTH // 2, HEIGHT - 110,
            CYAN_BRIGHT, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        self._status_label = arcade.Text(
            "INITIALIZING SYSTEMS...", WIDTH // 2, 115,
            GOLD, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        self._prompt = arcade.Text(
            "PRESS SPACE OR ENTER TO ENGAGE COMMAND CONSOLE", WIDTH // 2, 45,
            GOLD_BRIGHT, font_size=12, bold=True,
            anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        # Starfield
        self._stars = [
            (
                (i * 73 + 19) % WIDTH,
                (i * 127 + 41) % HEIGHT,
                0.8 + ((i % 5) * 0.25),
                80 + (i % 120),
            )
            for i in range(110)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._elapsed += delta_time

        # Smooth loading progress over ~2.6 seconds
        target_progress = min(1.0, self._elapsed / 2.6)
        self._progress = clamp(ease_out_cubic(target_progress), 0.0, 1.0)

        # Status text update
        current_status = "INITIALIZING SYSTEMS..."
        for threshold, text in _SYS_STEPS:
            if self._progress >= threshold:
                current_status = text
        self._status_text_str = current_status
        try:
            self._status_label.text = current_status
        except Exception:
            pass

        if self._progress >= 1.0:
            self._ready_to_advance = True
            # Loading is now a real boot phase: once the systems are ready,
            # continue automatically instead of waiting for a key press.
            if self._elapsed >= 3.25:
                self._advance_to_menu()

    def on_draw(self) -> None:
        self.clear()

        # 1. Parallax deep space background
        for x, y, size, alpha in self._stars:
            twinkle = int(alpha + 30 * math.sin(self._elapsed * 2.5 + x * 0.05))
            twinkle = max(40, min(255, twinkle))
            arcade.draw_circle_filled(x, y, size, (180, 210, 255, twinkle))

        # 2. Hero illustration backdrop
        hero = AssetManager.texture("hero_vimana_wars.png")
        if hero:
            hero_alpha = int(clamp(self._elapsed * 45, 0, 110))
            AssetManager.draw(hero, WIDTH // 2, HEIGHT // 2 + 10, 680, 450, color=(255, 255, 255, hero_alpha))

        # 3. Holographic frame and scanlines
        draw_scanlines(20, WIDTH - 20, 20, HEIGHT - 20, CYAN, spacing=24, alpha=6)
        draw_chamfered_panel(40, WIDTH - 40, 30, HEIGHT - 30, GOLD, fill=OBSIDIAN, alpha=185, cut=18)
        draw_corner_etching(40, WIDTH - 40, 30, HEIGHT - 30, GOLD, length=28, alpha=140)
        draw_telemetry_ticks(60, WIDTH - 60, HEIGHT - 130, CYAN, count=25, height=4, alpha=70)
        draw_telemetry_ticks(60, WIDTH - 60, 150, GOLD, count=25, height=4, alpha=70)

        # 4. Logo and Title
        logo = AssetManager.texture("vimana_wars_logo.png")
        if logo:
            logo_y = HEIGHT - 75
            AssetManager.draw(logo, WIDTH // 2 - 165, logo_y, 48, 48)
            AssetManager.draw(logo, WIDTH // 2 + 165, logo_y, 48, 48)

        self._title.draw()
        self._subtitle.draw()

        # 5. Narrative Prologue Crawl
        box_top = HEIGHT - 160
        line_height = 36
        for idx, line in enumerate(_STORY_LINES):
            line_delay = 0.3 + idx * 0.55
            fade = clamp((self._elapsed - line_delay) / 0.8, 0.0, 1.0)
            if fade > 0.0:
                alpha = int(255 * ease_out_cubic(fade))
                color = GOLD_BRIGHT if idx in (0, 3) else PARCHMENT
                arcade.draw_text(
                    line,
                    WIDTH // 2, box_top - idx * line_height,
                    (*color[:3], alpha),
                    font_size=11, bold=(idx == 0 or idx == 3),
                    anchor_x="center", anchor_y="center",
                    font_name=FONT_INTERFACE[0]
                )

        # 6. Segmented Telemetry Progress Bar
        bar_w = 460
        bar_left = (WIDTH - bar_w) // 2
        bar_right = bar_left + bar_w
        draw_segmented_bar(bar_left, bar_right, 126, 138, self._progress, color=CYAN_BRIGHT, segments=18, gap=4)
        pct = int(self._progress * 100)
        arcade.draw_text(f"{pct}%", bar_right + 12, 132, CYAN, font_size=9, bold=True, anchor_y="center")

        self._status_label.draw()

        # 7. Automatic hand-off prompt
        if self._ready_to_advance:
            p_alpha = pulse_alpha(self._elapsed, 160, 255, 3.5)
            self._prompt.text = "COMMAND CONSOLE READY // ENTERING..."
            self._prompt.color = (*GOLD_BRIGHT[:3], p_alpha)
            self._prompt.draw()
        else:
            skip_hint = "LOADING CELESTIAL SYSTEMS..."
            arcade.draw_text(skip_hint, WIDTH // 2, 45, MUTED, font_size=10, anchor_x="center", anchor_y="center")

        TransitionOverlay.draw()

    def _advance_to_menu(self) -> None:
        if self._advance_requested or TransitionOverlay.is_active:
            return
        self._advance_requested = True
        self.sound_manager.play_ui_click()
        # Give first-time pilots a skippable narrative briefing.  Returning
        # players go straight to the command console, so the story never
        # becomes startup friction.
        from game.systems import save_system
        if not save_system.load().get("story_intro_seen", False):
            from game.views.story_briefing_view import StoryBriefingView
            transition_to(self.window, StoryBriefingView())
        else:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        if self._ready_to_advance:
            self._advance_to_menu()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.SPACE, arcade.key.ENTER, arcade.key.ESCAPE):
            self._advance_to_menu()


# ==============================================================================
# [64/77] MODULE: game/views/menu_view.py
# ==============================================================================
"""
Vimana Wars Command Deck — Main Menu View.
Reskinned per Section 7.1 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, Hero Vimana hologram panel, real Pilot Record dossier,
primary Celestial Gold [ DEPLOY SORTIE ] button, and three-card mode row.
"""
import math
import random
import arcade

from constants import WIDTH, HEIGHT, REALMS
from game.entities.ship_classes import SHIP_CLASSES
from game.systems import save_system, achievement_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.systems.leaderboard_client import leaderboard_client
from game.ui.nav_rail import NavRail
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, PARCHMENT, STARLIGHT, GREY, MUTED, ASTRA_RED,
    FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_segmented_bar,
    draw_scanlines, pulse_alpha, draw_state_badge,
)


_RNG = random.Random(42)
_STARS = [
    (_RNG.randint(220, WIDTH), _RNG.randint(0, HEIGHT),
     _RNG.uniform(0.6, 1.8), _RNG.randint(80, 210), _RNG.uniform(0.5, 1.5))
    for _ in range(80)
]


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        self.sound_manager = SoundManager()
        self.nav_rail = NavRail("menu")

        # Load real game state
        saved = save_system.load()
        self._reduced_flashes = bool(saved.get("reduced_flashes", False))
        self._high_score = saved.get("high_score", 0)
        self._last_diff = saved.get("difficulty", "normal").upper()
        self._last_ship_id = saved.get("last_ship", "pushpaka")
        self._last_wave = max(0, int(saved.get("last_wave", 0)))

        # Calculate real unlocked realms
        unlocked = sum(1 for start in (1, 4, 7, 10, 13, 16, 19) if self._last_wave >= start)
        self._unlocked_realms = max(1, unlocked)

        # Calculate real ships unlocked
        self._unlocked_ships = sum(
            1 for s in SHIP_CLASSES.values()
            if self._last_wave >= s.get("unlock_wave", 0)
        )

        # Calculate real trophies
        achievements = achievement_system.get_all()
        self._unlocked_trophies = sum(1 for a in achievements if a.get("unlocked", False))
        self._total_trophies = len(achievements)

        # Current realm name
        realm_id = min(7, max(1, self._unlocked_realms))
        self._current_realm_name = REALMS.get(realm_id, {}).get("name", "Swarga")

        # Primary Sortie Action Button (Celestial Gold)
        self._btn_deploy = MenuButton(
            "DEPLOY SORTIE  ▶", 560, 168,
            width=620, height=44, accent=GOLD, variant="celestial"
        )

        # Mode row buttons (Metallic)
        self._mode_buttons = [
            (MenuButton("CAMPAIGN MAP", 320, 102, 145, 34, accent=CYAN, variant="metallic"), "map"),
            (MenuButton("ENDLESS VOID", 480, 102, 145, 34, accent=(180, 140, 255), variant="metallic"), "endless"),
            (MenuButton("MULTIPLAYER ⚔", 640, 102, 145, 34, accent=ASTRA_RED, variant="metallic"), "multiplayer"),
            (MenuButton("LEADERBOARDS", 800, 102, 145, 34, accent=GOLD, variant="metallic"), "leaderboard"),
        ]

        self._hovered_mode = -1
        self._hovered_deploy = False

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()
        # Refresh dynamic state
        saved = save_system.load()
        self._last_wave = max(0, int(saved.get("last_wave", 0)))
        self._high_score = saved.get("high_score", 0)
        self._last_ship_id = saved.get("last_ship", "pushpaka")
        self._game_id = saved.get("game_id", "")
        # Refresh the connection badge without blocking the render thread.
        leaderboard_client.check_health()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)

        self._btn_deploy.update(delta_time, self._hovered_deploy)
        for i, (btn, _) in enumerate(self._mode_buttons):
            btn.update(delta_time, i == self._hovered_mode)

    def on_draw(self) -> None:
        self.clear()

        # ── Background Parallax Drift (x=220 to WIDTH) ───────────────────────
        for sx, sy, radius, base, speed in _STARS:
            x = 220 + ((sx - 220 + self._pulse * speed * 6.0) % (WIDTH - 220))
            y = (sy + self._pulse * speed * 1.5) % HEIGHT
            brightness = int(base + 20 * math.sin(self._pulse * 0.8 + sx * 0.01))
            arcade.draw_circle_filled(x, y, radius, (brightness, brightness, min(255, brightness + 20)))

        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        # Wordmark & Context
        arcade.draw_text("COMMAND DECK // BRIDGE CONSOLE", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(f"CURRENT THEATER: {self._current_realm_name.upper()} // WAVE {self._last_wave:02d}",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Online Sync Badge
        sync_label = f"VMN-{self._game_id[-6:]}" if self._game_id else "LOCAL GUEST"
        is_online = leaderboard_client.is_online()
        sync_color = CYAN_BRIGHT if is_online else GREY

        draw_state_badge(WIDTH - 70, 574, "ONLINE" if is_online else "OFFLINE", sync_color, width=74)
        arcade.draw_text(sync_label, WIDTH - 120, 574, STARLIGHT,
                         font_size=9, bold=True, anchor_x="right", anchor_y="center",
                         font_name=FONT_TELEMETRY)

        # ── Left Hero Vimana Panel (x=240 to 550, y=225 to 530) ─────────────
        draw_chamfered_panel(240, 550, 225, 530, CYAN, fill=SURFACE_LOW, alpha=225, cut=10.0)
        draw_corner_etching(240, 550, 225, 530, GOLD, length=14.0, alpha=110)

        arcade.draw_text("ACTIVE VIMANA CRAFT", 256, 508, CYAN_BRIGHT,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)

        ship_data = SHIP_CLASSES.get(self._last_ship_id, SHIP_CLASSES["pushpaka"])
        arcade.draw_text(ship_data["name"].upper(), 256, 488, GOLD_BRIGHT,
                         font_size=16, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(ship_data.get("subtitle", "Celestial Flagship"), 256, 472, PARCHMENT,
                         font_size=8, bold=True, font_name=FONT_INTERFACE)

        # Counter-rotating hologram halo rings
        cx, cy = 395, 355
        ring_angle = 0.0 if self._reduced_flashes else self._pulse * 14.0
        ring_alpha = pulse_alpha(self._pulse, 20, 55, 1.8, self._reduced_flashes)
        arcade.draw_circle_outline(cx, cy, 65, (*GOLD, 40), 1)
        arcade.draw_arc_outline(cx, cy, 140, 140, (*CYAN, ring_alpha),
                                ring_angle, ring_angle + 240, 2)
        arcade.draw_arc_outline(cx, cy, 175, 175, (*GOLD, max(15, ring_alpha // 2)),
                                -ring_angle, -ring_angle + 200, 1)

        # Hero ship sprite
        hero_tex = AssetManager.texture(ship_data.get("sprite", "pushpaka.png"))
        float_y = 0.0 if self._reduced_flashes else math.sin(self._pulse * 1.2) * 4.0
        if not AssetManager.draw(hero_tex, cx, cy + float_y, 110, 110):
            arcade.draw_triangle_filled(cx, cy + 50 + float_y, cx - 40, cy - 40 + float_y,
                                        cx + 40, cy - 40 + float_y, ship_data["color"])

        # Reticle crosshair
        arcade.draw_line(cx - 18, cy + float_y, cx + 18, cy + float_y, (*CYAN, 75), 1)
        arcade.draw_line(cx, cy - 18 + float_y, cx, cy + 18 + float_y, (*CYAN, 75), 1)

        # Weapon loadout strip
        arcade.draw_line(256, 260, 534, 260, (*CYAN, 55), 1)
        arcade.draw_text("SYSTEMS ARMED // READY FOR SORTIE", 256, 242, (*CYAN, 190),
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # ── Right Pilot Record Dossier (x=570 to 880, y=225 to 530) ─────────
        draw_chamfered_panel(570, 880, 225, 530, GOLD, fill=SURFACE_LOW, alpha=225, cut=10.0)
        draw_corner_etching(570, 880, 225, 530, CYAN, length=14.0, alpha=110)

        arcade.draw_text("PILOT DOSSIER // CAMPAIGN RECORD", 586, 508, GOLD,
                         font_size=8, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_text("AKASHIC CHRONICLES", 586, 488, GOLD_BRIGHT,
                         font_size=16, bold=True, font_name=FONT_INTERFACE)

        # Campaign Progress Bar
        arcade.draw_text("CAMPAIGN RESONANCE", 586, 452, STARLIGHT,
                         font_size=9, bold=True, font_name=FONT_INTERFACE)
        prog_pct = int((self._unlocked_realms / 7.0) * 100)
        arcade.draw_text(f"{prog_pct}%  ({self._unlocked_realms}/7 REALMS)", 864, 452, GOLD_BRIGHT,
                         font_size=9, bold=True, anchor_x="right", font_name=FONT_TELEMETRY)
        draw_segmented_bar(586, 864, 436, 444, self._unlocked_realms / 7.0,
                           color=GOLD, segments=7, gap=4.0)

        # Real Statistics Grid
        stat_rows = [
            ("HIGHEST WAVE REACHED", f"WAVE {self._last_wave:02d} / 20", CYAN_BRIGHT),
            ("VESSELS COMMISSIONED", f"{self._unlocked_ships} / 9 SHIPS", STARLIGHT),
            ("HONORIFIC TROPHIES", f"{self._unlocked_trophies} / {self._total_trophies} UNLOCKED", GOLD_BRIGHT),
            ("COMBAT DIFFICULTY", f"{self._last_diff}", PARCHMENT),
            ("LIFETIME HIGH SCORE", f"{self._high_score:,}", GOLD_BRIGHT),
        ]

        sy = 398
        for label, val, val_col in stat_rows:
            arcade.draw_text(label, 586, sy, GREY, font_size=8, bold=True, font_name=FONT_TELEMETRY)
            arcade.draw_text(val, 864, sy, val_col, font_size=9, bold=True, anchor_x="right", font_name=FONT_TELEMETRY)
            arcade.draw_line(586, sy - 6, 864, sy - 6, (*GREY, 35), 1)
            sy -= 32

        # ── Primary Deploy Sortie Button ─────────────────────────────────────
        self._btn_deploy.draw()

        # ── Three-Card Mode Row ──────────────────────────────────────────────
        for btn, _ in self._mode_buttons:
            btn.draw()

        # ── Bottom Command Hints ─────────────────────────────────────────────
        arcade.draw_text(
            "SPACE / ENTER: DEPLOY SORTIE   •   V: TRAILER (PV)   •   ESC: QUIT",
            560, 32, MUTED, font_size=9, bold=True, anchor_x="center", anchor_y="center",
            font_name=FONT_TELEMETRY
        )

        # ── Draw 220px Navigation Rail ───────────────────────────────────────
        self.nav_rail.draw()

        # Transition Wipe
        TransitionOverlay.draw()

    def _activate(self, action: str) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        if action == "play":
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView())
        elif action == "arsenal":
            from game.views.ship_select_view import ShipSelectView
            transition_to(self.window, ShipSelectView())
        elif action == "map":
            from game.views.realm_map_view import RealmMapView
            transition_to(self.window, RealmMapView())
        elif action == "endless":
            from game.views.difficulty_view import DifficultyView
            transition_to(self.window, DifficultyView(initial_difficulty="endless"))
        elif action == "multiplayer":
            from game.views.multiplayer_view import MultiplayerView
            transition_to(self.window, MultiplayerView(return_view=self))
        elif action == "leaderboard":
            from game.views.leaderboard_view import LeaderboardView
            transition_to(self.window, LeaderboardView(return_view=self))
        elif action == "codex":
            from game.views.codex_view import CodexView
            transition_to(self.window, CodexView(return_view=self))
        elif action == "account":
            from game.views.account_view import AccountView
            transition_to(self.window, AccountView(return_view=self))
        elif action == "stats":
            from game.views.stats_view import StatsView
            transition_to(self.window, StatsView(return_view=self))
        elif action == "achievements":
            from game.views.achievements_view import AchievementsView
            transition_to(self.window, AchievementsView(return_view=self))
        elif action == "settings":
            from game.views.settings_view import SettingsView
            transition_to(self.window, SettingsView(return_view=self))
        elif action == "quit":
            arcade.exit()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)
        self._hovered_deploy = self._btn_deploy.contains(x, y)

        new_hovered_mode = -1
        for i, (btn, _) in enumerate(self._mode_buttons):
            if btn.contains(x, y):
                new_hovered_mode = i
                break
        if new_hovered_mode != self._hovered_mode and new_hovered_mode >= 0:
            self.sound_manager.play_ui_click(volume=0.20)
        self._hovered_mode = new_hovered_mode

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Check nav rail first
        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            return

        # Check primary deploy button
        if self._btn_deploy.contains(x, y):
            self._activate("play")
            return

        # Check mode buttons
        for btn, action in self._mode_buttons:
            if btn.contains(x, y):
                self._activate(action)
                return

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._activate("play")
        elif key in (arcade.key.H, arcade.key.R):
            self._activate("arsenal")
        elif key == arcade.key.M:
            self._activate("map")
        elif key == arcade.key.N:
            self._activate("multiplayer")
        elif key == arcade.key.L:
            self._activate("leaderboard")
        elif key == arcade.key.C:
            self._activate("codex")
        elif key == arcade.key.T:
            self._activate("stats")
        elif key == arcade.key.A:
            self._activate("achievements")
        elif key == arcade.key.O:
            self._activate("settings")
        elif key == arcade.key.P:
            self._activate("account")
        elif key == arcade.key.ESCAPE:
            arcade.exit()


# ==============================================================================
# [65/77] MODULE: game/views/multiplayer_view.py
# ==============================================================================
"""Authenticated multiplayer lobby browser.

This screen implements the pre-match layer: create, browse, join, ready,
start, and leave. Combat itself remains authoritative to a future real-time
game session and is intentionally not faked with local-only state.
"""
import math
import random
import arcade

from constants import WIDTH, HEIGHT, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.systems.asset_manager import AssetManager
from game.systems.sound_manager import SoundManager
from game.ui.menu_button import MenuButton
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT, CYAN,
    CYAN_BRIGHT, PARCHMENT, MUTED, RED_BRIGHT,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
)


_RNG = random.Random(77)
_STARS = [(_RNG.randrange(40, WIDTH - 40), _RNG.randrange(30, HEIGHT), _RNG.uniform(0.5, 1.8)) for _ in range(85)]


class MultiplayerView(arcade.View):
    """A network lobby screen backed by the Flask multiplayer API."""

    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self.sound_manager = SoundManager()
        saved = save_system.load()
        self._ship_class = saved.get("last_ship", "pushpaka")
        self._mode = "campaign"
        self._code = ""
        self._lobbies = []
        self._current_lobby = None
        self._selected_lobby = -1
        self._hovered = -1
        self._pulse = 0.0
        self._poll_timer = 0.0
        self._network_busy = False
        self._pending = None
        self._status = ""
        self._status_color = MUTED
        self._api_status = "CONNECTED"
        self._nav_rail = NavRail(current_screen="sangha")

        self._title = arcade.Text(
            "MULTIPLAYER // SANGHA NETWORK", WIDTH // 2, 550,
            GOLD_BRIGHT, font_size=25, bold=True, anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "FORM A VIMANA WING • READY TOGETHER • ENTER THE MAHAYUDDHA",
            WIDTH // 2, 518, CYAN_BRIGHT, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "CLICK A LOBBY TO SELECT   •   TYPE A CODE   •   ESC: BACK",
            WIDTH // 2, 28, MUTED, font_size=9, anchor_x="center", anchor_y="center",
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, 75, MUTED, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._buttons = self._build_buttons()

    def _build_buttons(self):
        data = [
            ("CREATE LOBBY", "create", GOLD),
            ("JOIN CODE", "join", CYAN),
            ("READY / UNREADY", "ready", (100, 240, 190)),
            ("START MATCH", "start", (255, 150, 80)),
            ("LEAVE LOBBY", "leave", RED_BRIGHT),
            ("REFRESH", "refresh", MUTED),
            ("BACK", "back", MUTED),
            ("⚔ LOCAL 1V1 DUEL", "local_duel", GOLD_BRIGHT),
        ]
        ys = (455, 410, 310, 265, 220, 175, 130, 85)
        return [
            (MenuButton(label, 730, ys[i], 205, 31, color), action)
            for i, (label, action, color) in enumerate(data)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        self._buttons = self._build_buttons()
        self._hovered = -1
        self._refresh_lobbies()
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._nav_rail.update(delta_time)
        self._pulse += delta_time
        self._poll_timer += delta_time
        for i, (button, _) in enumerate(self._buttons):
            button.update(delta_time, i == self._hovered)
        if self._current_lobby and self._poll_timer >= 2.0 and not self._network_busy:
            self._poll_timer = 0.0
            self._get_current_lobby()
        if self._pending is not None:
            kind, success, error, body = self._pending
            self._pending = None
            self._network_busy = False
            self._apply_result(kind, success, error, body)

    def _queue_request(self, kind, request_fn) -> None:
        if self._network_busy:
            return
        self._network_busy = True
        self._api_status = "RECONNECTING"
        request_fn(lambda success, error, body: setattr(self, "_pending", (kind, success, error, body)))

    def _refresh_lobbies(self) -> None:
        self._status = "SCANNING ACTIVE LOBBIES..."
        self._status_color = CYAN_BRIGHT
        self._queue_request("list", leaderboard_client.list_lobbies)

    def _get_current_lobby(self) -> None:
        if self._current_lobby:
            self._queue_request("get", lambda done: leaderboard_client.get_lobby(self._current_lobby["code"], done))

    def _apply_result(self, kind, success, error, body) -> None:
        if not success:
            self._api_status = "OFFLINE"
            self._status = error or "Multiplayer request failed"
            self._status_color = RED_BRIGHT
            if kind == "get":
                self._current_lobby = None
            return
        
        self._api_status = "CONNECTED"
        if kind == "list":
            self._lobbies = body.get("lobbies", [])
            self._status = f"{len(self._lobbies)} ACTIVE LOBBY" + ("S" if len(self._lobbies) != 1 else "")
            self._status_color = CYAN_BRIGHT
        elif kind in ("create", "join", "get", "ready", "start"):
            self._current_lobby = body.get("lobby") or self._current_lobby
            if self._current_lobby:
                self._code = self._current_lobby["code"]
                self._status = f"LOBBY {self._code} • {self._current_lobby['status'].upper()}"
                self._status_color = CYAN_BRIGHT
        elif kind == "leave":
            self._current_lobby = None
            self._status = "LEFT LOBBY — READY FOR ANOTHER SORTIE"
            self._status_color = MUTED
            self._refresh_lobbies()

    def _draw_background(self) -> None:
        self.clear()
        for x, y, speed in _STARS:
            sx = (x + self._pulse * speed * 3) % WIDTH
            alpha = int(55 + 35 * math.sin(self._pulse + x * 0.02))
            arcade.draw_circle_filled(sx, y, 1.2, (120, 190, 255, alpha))
        draw_scanlines(0, WIDTH, 0, HEIGHT, CYAN, spacing=20, alpha=5)
        draw_chamfered_panel(265, 585, 95, 485, CYAN, fill=OBSIDIAN, alpha=235, cut=14)
        draw_corner_etching(265, 585, 95, 485, GOLD, length=18, alpha=125)
        draw_chamfered_panel(610, 850, 95, 485, GOLD, fill=OBSIDIAN, alpha=235, cut=14)
        draw_corner_etching(610, 850, 95, 485, CYAN, length=18, alpha=115)

    def _draw_lobby_list(self) -> None:
        arcade.draw_text("OPEN WINGS", 285, 450, GOLD, font_size=11, bold=True)
        if not self._lobbies:
            arcade.draw_text("No open lobbies yet.", 425, 320, MUTED, font_size=12, anchor_x="center")
            arcade.draw_text("Create one and invite another Game ID.", 425, 295, PARCHMENT, font_size=9, anchor_x="center")
            return
        for i, lobby in enumerate(self._lobbies[:7]):
            y = 415 - i * 45
            selected = i == self._selected_lobby
            color = GOLD_BRIGHT if selected else (75, 100, 140)
            fill = SURFACE_HIGH if selected else SURFACE_LOW
            draw_chamfered_panel(280, 570, y - 16, y + 17, color, fill=fill, alpha=240, cut=6)
            players = lobby.get("players", [])
            arcade.draw_text(lobby.get("code", "------"), 298, y, color, font_size=14, bold=True, font_name="Courier New", anchor_y="center")
            
            mode = lobby.get("mode", "campaign").upper()
            mode_icon = "⚔" if mode == "DUEL" else ("🤝" if mode == "CO-OP" else "∞")
            arcade.draw_text(f"{mode_icon} {mode}", 390, y + 6, PARCHMENT, font_size=8, bold=True)
            
            max_p = lobby.get('max_players', 2)
            dots = ""
            for p_idx in range(max_p):
                dots += "● " if p_idx < len(players) else "○ "
            arcade.draw_text(dots.strip(), 390, y - 6, MUTED, font_size=7)
            
            st = lobby.get("status", "waiting").upper()
            st_color = CYAN if st == "WAITING" else (GOLD if st == "FULL" else RED_BRIGHT)
            from game.ui.vedic_theme import draw_state_badge
            draw_state_badge(525, y, st, st_color, width=50)

    def _draw_current_lobby(self) -> None:
        account = leaderboard_client.current_account()
        arcade.draw_text("YOUR GAME ID", 635, 450, MUTED, font_size=8, bold=True)
        arcade.draw_text(account["game_id"] if account else "SIGN IN REQUIRED", 635, 428,
                         CYAN_BRIGHT if account else RED_BRIGHT, font_size=14, bold=True)
        
        # Mode Tabs
        for i, (mode_label, mode_val) in enumerate([("⚔ DUEL", "duel"), ("🤝 CO-OP", "coop"), ("∞ ENDLESS", "endless")]):
            tx = 630 + i * 65
            selected = self._mode == mode_val
            color = GOLD if selected else MUTED
            draw_chamfered_panel(tx, tx + 60, 350, 380, color, fill=SURFACE_LOW, alpha=245, border_width=2 if selected else 1, cut=4)
            arcade.draw_text(mode_label, tx + 30, 365, color, font_size=7, bold=True, anchor_x="center", anchor_y="center")

        arcade.draw_text("LOBBY CODE", 635, 205, MUTED, font_size=8, bold=True)
        draw_chamfered_panel(635, 825, 165, 195, GOLD, fill=SURFACE_LOW, alpha=245, cut=6,
                             selected=True)
        arcade.draw_text(self._code or "TYPE CODE", 730, 180,
                         GOLD_BRIGHT if self._code else MUTED, font_size=20, bold=True, anchor_x="center", anchor_y="center")
        if self._current_lobby:
            lobby = self._current_lobby
            arcade.draw_text(f"{lobby.get('mode', 'campaign').upper()} • {lobby['status'].upper()}", 635, 145,
                             PARCHMENT, font_size=9, bold=True)
            for i in range(lobby.get('max_players', 2)):
                if i < len(lobby.get("players", [])):
                    player = lobby.get("players")[i]
                    is_ready = player.get("ready")
                    host = "HOST" if player.get("host") else "WING"
                    player_name = player.get("game_id", "—")
                    color = CYAN_BRIGHT if is_ready else PARCHMENT
                    cy = 118 - i * 22
                    arcade.draw_polygon_filled(((635, cy+6), (645, cy), (635, cy-6)), color)
                    arcade.draw_text(f"{host}  {player_name}", 655, cy, color, font_size=8, anchor_y="center")
                    if is_ready:
                        pulse = 155 + int(100 * math.sin(self._pulse * 8))
                        arcade.draw_circle_filled(815, cy, 3, (50, 255, 150, pulse))
                        arcade.draw_text("READY", 805, cy, CYAN_BRIGHT, font_size=8, anchor_x="right", anchor_y="center")
                    else:
                        arcade.draw_circle_filled(815, cy, 3, MUTED)
                        arcade.draw_text("STANDBY", 805, cy, MUTED, font_size=8, anchor_x="right", anchor_y="center")
                else:
                    cy = 118 - i * 22
                    arcade.draw_text("WAITING FOR PILOT...", 635, cy, MUTED, font_size=8, anchor_y="center")
        else:
            arcade.draw_text("Select a lobby or create one.", 730, 125, MUTED, font_size=9, anchor_x="center")
            if self._mode == "duel":
                arcade.draw_text("COMING SOON — ONLINE DUEL LAUNCHING SOON", 730, 105, (255, 150, 50), font_size=7, bold=True, anchor_x="center")

    def on_draw(self) -> None:
        self._draw_background()
        logo = AssetManager.texture("vimana_wars_logo.png")
        AssetManager.draw(logo, 75, 535, 30, 30)
        self._title.draw()
        self._subtitle.draw()
        
        if self._api_status == "CONNECTED":
            dot_color = (50, 200, 100)
        elif self._api_status == "RECONNECTING":
            dot_color = (200, 180, 50)
        else:
            dot_color = RED_BRIGHT
        arcade.draw_text(f"● {self._api_status}", WIDTH - 30, 565, dot_color, font_size=8, bold=True, anchor_x="right")

        self._draw_lobby_list()
        self._draw_current_lobby()
        if self._status:
            self._status_text.text = self._status
            self._status_text.color = self._status_color
            self._status_text.draw()
        for button, _ in self._buttons:
            button.draw()
        self._hint.draw()
        self._nav_rail.draw()
        TransitionOverlay.draw()

    def _selected_code(self) -> str:
        if self._code.strip():
            return self._code.strip().upper()
        if 0 <= self._selected_lobby < len(self._lobbies):
            return self._lobbies[self._selected_lobby].get("code", "").upper()
        return ""

    def _require_account(self) -> bool:
        if leaderboard_client.current_account():
            return True
        self._status = "SIGN IN FROM ACCOUNT BEFORE JOINING A MULTIPLAYER WING"
        self._status_color = RED_BRIGHT
        return False

    def _activate(self, action: str) -> None:
        if action == "back":
            target = self.return_view
            if target is None:
                from game.views.menu_view import MenuView
                target = MenuView()
            transition_to(self.window, target)
            return
        if action == "refresh":
            self._refresh_lobbies()
            return
        if action == "local_duel":
            from game.views.difficulty_view import DifficultyView
            # You can route to GameView with 2 players or any Duel view if it exists.
            # Using DifficultyView or similar if "on_local_duel" is mentioned.
            # We can also just transition to game view directly for local duel.
            from game.views.game_view import GameView
            transition_to(self.window, GameView(difficulty="normal", ship_class=self._ship_class))
            return
        if not self._require_account():
            return
        if action == "create":
            self._queue_request("create", lambda done: leaderboard_client.create_lobby(
                self._mode, 2, self._ship_class, done))
        elif action == "join":
            code = self._selected_code()
            if not code:
                self._status = "SELECT A LOBBY OR TYPE ITS SIX-CHARACTER CODE"
                self._status_color = RED_BRIGHT
                return
            self._queue_request("join", lambda done: leaderboard_client.join_lobby(code, self._ship_class, done))
        elif action == "ready":
            if not self._current_lobby:
                self._status = "JOIN OR CREATE A LOBBY FIRST"
                self._status_color = RED_BRIGHT
                return
            account = leaderboard_client.current_account()
            mine = next((p for p in self._current_lobby.get("players", []) if p.get("game_id") == account["game_id"]), {})
            self._queue_request("ready", lambda done: leaderboard_client.set_lobby_ready(
                self._current_lobby["code"], not mine.get("ready", False), done))
        elif action == "start":
            if self._current_lobby:
                self._queue_request("start", lambda done: leaderboard_client.start_lobby(self._current_lobby["code"], done))
            else:
                self._status = "JOIN OR CREATE A LOBBY FIRST"
                self._status_color = RED_BRIGHT
        elif action == "leave":
            if self._current_lobby:
                self._queue_request("leave", lambda done: leaderboard_client.leave_lobby(self._current_lobby["code"], done))

    def _handle_nav(self, key: str) -> None:
        """Delegate navigation from the rail to the appropriate view."""
        self._nav_rail.navigate_to(key, self.window)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)
        new_hovered = -1
        for i, (button, _) in enumerate(self._buttons):
            if button.contains(x, y):
                new_hovered = i
                break
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.18)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        nav = self._nav_rail.on_mouse_press(x, y, self.window)
        if nav:
            self._handle_nav(nav)
            return
        
        # Mode tabs click
        if 350 <= y <= 380:
            for i, mode_val in enumerate(["duel", "coop", "endless"]):
                if 630 + i * 65 <= x <= 690 + i * 65:
                    self._mode = mode_val
                    self.sound_manager.play_ui_click()
                    return

        if 635 <= x <= 825 and 165 <= y <= 195:
            self._code = ""
            return
        for i, lobby in enumerate(self._lobbies[:7]):
            row_y = 415 - i * 45
            if 280 <= x <= 570 and row_y - 16 <= y <= row_y + 17:
                self._selected_lobby = i
                self._code = lobby.get("code", "")
                return
        for i, (menu_button, action) in enumerate(self._buttons):
            if menu_button.contains(x, y):
                self._hovered = i
                self.sound_manager.play_ui_click()
                self._activate(action)
                return

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            self._activate("back")
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            if self._hovered >= 0:
                self._activate(self._buttons[self._hovered][1])
            else:
                self._activate("join")
        elif key == arcade.key.BACKSPACE:
            self._code = self._code[:-1]
        elif key in (arcade.key.UP, arcade.key.W):
            self._hovered = (self._hovered - 1) % len(self._buttons)
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._hovered = (self._hovered + 1) % len(self._buttons)

    def on_text(self, text: str) -> None:
        if text.isalnum() and len(self._code) < 6:
            self._code += text.upper()


# ==============================================================================
# [66/77] MODULE: game/views/name_entry_view.py
# ==============================================================================
"""
game/views/name_entry_view.py
Name Entry Screen displayed after game over or victory.
Allows player to type their warrior name and submit to the online leaderboard.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT, CYAN,
    CYAN_BRIGHT, PARCHMENT, STARLIGHT, MUTED, ASTRA_RED,
    FONT_CEREMONIAL, FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
)


class NameEntryView(arcade.View):
    def __init__(self, score: int, wave: int, kills: int, highest_combo: int,
                 difficulty: str = "normal", ship_class: str = "pushpaka",
                 is_victory: bool = False, stats: dict = None,
                 start_wave: int = 1, is_endless: bool = False):
        super().__init__()
        self.score = score
        self.wave = wave
        self.kills = kills
        self.highest_combo = highest_combo
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.is_victory = is_victory
        self.stats = stats or {}
        self.start_wave = start_wave
        self.is_endless = is_endless

        saved = save_system.load()
        self.player_name = saved.get("player_name", "Warrior")
        self._cursor_timer = 0.0
        self._submitting = False
        self._status_msg = ""

        # UI Text Objects
        header_str = "CELESTIAL VICTORY" if is_victory else "DHARMIC REBIRTH"
        self._title = arcade.Text(
            header_str, WIDTH // 2, int(HEIGHT * 0.78),
            GOLD_BRIGHT if is_victory else ASTRA_RED,
            font_size=32, bold=True, font_name=FONT_CEREMONIAL[0],
            anchor_x="center", anchor_y="center"
        )
        self._sub = arcade.Text(
            f"SCORE: {score:,}   •   WAVE: {wave:02d}   •   DIFFICULTY: {difficulty.upper()}",
            WIDTH // 2, int(HEIGHT * 0.70),
            CYAN_BRIGHT, font_size=11, bold=True, font_name=FONT_TELEMETRY[0],
            anchor_x="center", anchor_y="center"
        )
        self._prompt = arcade.Text(
            "COMMISSION PILOT RECORD INTO AKASHIC ARCHIVES",
            WIDTH // 2, int(HEIGHT * 0.58),
            PARCHMENT, font_size=10, bold=True, font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center"
        )
        self._name_display = arcade.Text(
            "", WIDTH // 2, int(HEIGHT * 0.46),
            GOLD_BRIGHT, font_size=24, bold=True, font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center"
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, int(HEIGHT * 0.34),
            CYAN, font_size=11, bold=True, font_name=FONT_TELEMETRY[0],
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "ENTER : TRANSMIT RECORD   •   ESC : SKIP TO DEBRIEF",
            WIDTH // 2, int(HEIGHT * 0.16),
            MUTED, font_size=10, bold=True, font_name=FONT_TELEMETRY[0],
            anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._cursor_timer += delta_time
        pending = getattr(self, "_pending_result", None)
        if pending is not None:
            self._pending_result = None
            self._proceed_to_results()

    def on_draw(self) -> None:
        self.clear()
        
        # Backdrop console panel
        draw_chamfered_panel(WIDTH // 2 - 260, WIDTH // 2 + 260, 60, HEIGHT - 60, CYAN,
                             fill=OBSIDIAN, alpha=240, border_width=1, cut=16)
        draw_corner_etching(WIDTH // 2 - 260, WIDTH // 2 + 260, 60, HEIGHT - 60, GOLD, length=18, alpha=140)
        draw_scanlines(WIDTH // 2 - 250, WIDTH // 2 + 250, 70, HEIGHT - 70, CYAN, spacing=24, alpha=4)

        self._title.draw()
        self._sub.draw()
        self._prompt.draw()

        # Input box with chamfered panel
        box_y = int(HEIGHT * 0.46)
        draw_chamfered_panel(WIDTH // 2 - 180, WIDTH // 2 + 180, box_y - 24, box_y + 24, CYAN_BRIGHT,
                             fill=SURFACE_HIGH, alpha=245, border_width=2, cut=8)

        # Blinking cursor
        show_cursor = (int(self._cursor_timer * 2.5) % 2 == 0) and not self._submitting
        cursor_char = "_" if show_cursor else " "
        self._name_display.text = f"{self.player_name}{cursor_char}"
        self._name_display.draw()

        if self._status_msg:
            self._status_text.text = self._status_msg
            self._status_text.draw()

        self._hint.draw()
        TransitionOverlay.draw()

    def on_key_press(self, key, modifiers) -> None:
        if self._submitting:
            return

        if key in (arcade.key.ENTER, arcade.key.RETURN):
            self._submit_and_proceed()
        elif key == arcade.key.ESCAPE:
            self._proceed_to_results()
        elif key == arcade.key.BACKSPACE:
            if len(self.player_name) > 0:
                self.player_name = self.player_name[:-1]

    def on_text(self, text: str) -> None:
        if self._submitting:
            return
        if text.isprintable() and len(self.player_name) < 16:
            self.player_name += text

    def _submit_and_proceed(self) -> None:
        final_name = self.player_name.strip() or "Anonymous"
        
        # Persist name for next time
        saved = save_system.load()
        saved["player_name"] = final_name
        save_system.save(saved)

        self._submitting = True
        self._status_msg = "Transmitting record to online leaderboard..."

        def _on_done(success: bool, error: str | None):
            # Network callbacks run on a worker thread. Defer the view change
            # to on_update so Arcade/OpenGL state is touched only on the UI thread.
            self._pending_result = (success, error)

        leaderboard_client.submit_score(
            player_name=final_name,
            score=self.score,
            level_reached=self.wave,
            difficulty=self.difficulty,
            ship_class=self.ship_class,
            stats={**self.stats, "kills": self.kills},
            on_complete=_on_done
        )

    def _proceed_to_results(self) -> None:
        if self.is_victory:
            from game.views.victory_view import VictoryView
            transition_to(self.window, VictoryView(
                score=self.score,
                kills=self.kills,
                highest_combo=self.highest_combo,
                difficulty=self.difficulty,
                ship_class=self.ship_class,
                wave=self.wave,
                stats=self.stats,
            ))
        else:
            from game.views.game_over_view import GameOverView
            updated = save_system.update_after_game(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
                highest_combo=self.highest_combo,
                total_damage=self.stats.get("total_damage", 0),
                boons_claimed=self.stats.get("boons_claimed", 0),
                bosses_defeated=self.stats.get("bosses_defeated", []),
                ship_class=self.ship_class,
                campaign_cleared=self.is_victory,
            )
            from game.systems.leaderboard_client import leaderboard_client
            leaderboard_client.push_profile()
            transition_to(self.window, GameOverView(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
                highest_combo=self.highest_combo,
                high_score=updated["high_score"],
                difficulty=self.difficulty,
                ship_class=self.ship_class,
                stats=self.stats,
                start_wave=self.start_wave,
                is_endless=self.is_endless,
            ))


# ==============================================================================
# [67/77] MODULE: game/views/realm_map_view.py
# ==============================================================================
"""
game/views/realm_map_view.py
Celestial Campaign Sector Map.
Follows Section 7.3 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, 7-node curved trajectory, state badges
(Cleared gold tick, Available cyan pulse, Locked brass lock), boss chevrons,
and direct briefing/sortie launch.
"""
import math
import random
import arcade

from constants import WIDTH, HEIGHT, REALMS
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.ui.nav_rail import NavRail
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, BRASS, ASTRA_RED, ASTRA_RED_BRIGHT, PARCHMENT,
    STARLIGHT, GREY, MUTED, WELL,
    FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
    pulse_alpha, draw_state_badge,
)


REALM_ORDER = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
REALM_START_WAVES = {1: 1, 2: 4, 3: 7, 4: 10, 5: 13, 6: 16, 7: 19, 8: 21, 9: 24, 10: 27}
BOSS_REALMS = {2: "Kumbhakarna", 4: "Ravana", 7: "Vritra", 10: "Hiranyakashipu"}

REALM_LORE = {
    1: "Swarga, the Celestial Heaven — home of the Devas and the first line of defense against the Asura uprising. The golden gates are falling. You are the last Vimana standing between the invasion and the mortal world.",
    2: "Kshira Sagara, the Cosmic Ocean of Milk — the birthplace of Amrita, the nectar of immortality. The Asuras seek to corrupt it. Kumbhakarna, the sleeping titan, has been roused by dark sorcery.",
    3: "Dandaka Void, the Mystical Astral Forest — a dimension between worlds where Asura hunters stalk the debris of shattered planets. Navigate the phantom nebulae and eliminate the ambush fleet.",
    4: "Lanka, the Molten Rift — Ravana's fortress realm, forged from volcanic celestial matter. The ten-headed Demon King commands his final legions here. Break his war machine before it reaches Earth.",
    5: "Setu Expanse, the Bridge Between Worlds — the ancient Rama Setu reborn as an astral highway. Mahishasura, the buffalo warlord, has blockaded this corridor with his armored columns.",
    6: "Naraka Forge, the Burning Foundry — where the Asuras manufacture their warships from captured celestial metals. Destroy the factory fleet before the next armada launches.",
    7: "Mahayuddha Citadel, the Final Astral Battlefield — where the great war between Devas and Asuras reaches its crescendo. Vritra, the storm-serpent who swallows the sky, makes his last stand.",
    8: "Patala Depths, the Serpent Kingdom Below — the subterranean astral ocean ruled by Vasuki and the Nagas. The Asuras have enlisted them as shock troops. Plunge into the deep and shatter their alliance.",
    9: "Brahmaloka Summit, the Creator's Divine Citadel — the highest realm of Lord Brahma. The Asura tyrant Hiranyakashipu has besieged even this sacred place, believing himself indestructible.",
    10: "Vaikuntha Gate, the Eternal Threshold of Vishnu — the final door between creation and dissolution. Hiranyakashipu, who cannot be killed by man or beast, day or night, inside or outside — you must find the moment of vulnerability and strike.",
}

# Curved trajectory coordinates across x=240 to 880 space
_NODE_POS = {
    1: (260, 380),
    2: (330, 380),
    3: (420, 380),
    4: (510, 380),
    5: (590, 380),
    6: (590, 250),
    7: (510, 250),
    8: (420, 250),
    9: (330, 250),
    10: (260, 250),
}


def realm_is_unlocked(realm_id: int, last_wave: int) -> bool:
    return realm_id == 1 or last_wave >= REALM_START_WAVES[realm_id]


class RealmMapView(arcade.View):
    def __init__(self):
        super().__init__()
        self._pulse = 0.0
        self._hovered = -1
        self._selected = 1
        self.sound_manager = SoundManager()
        self.nav_rail = NavRail("campaign")

        saved = save_system.load()
        self._reduced_flashes = bool(saved.get("reduced_flashes", False))
        self.last_wave = max(0, int(saved.get("last_wave", 0)))
        self._unlocked = [
            r for r in REALM_ORDER
            if realm_is_unlocked(r, self.last_wave)
        ]
        last_realm = int(saved.get("last_realm", 1))
        if last_realm in self._unlocked:
            self._selected = last_realm
        else:
            self._selected = self._unlocked[-1] if self._unlocked else 1

        self._stars = [
            (random.randrange(220, WIDTH), random.randrange(HEIGHT), random.uniform(0.6, 1.8))
            for _ in range(70)
        ]

        self._btn_enter = MenuButton(
            "ENTER SORTIE  ▶", 755, 110,
            width=210, height=42, accent=GOLD, variant="celestial"
        )
        self._hovered_enter = False

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()
        saved = save_system.load()
        self.last_wave = max(0, int(saved.get("last_wave", 0)))
        self._unlocked = [
            r for r in REALM_ORDER
            if realm_is_unlocked(r, self.last_wave)
        ]

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)
        self._btn_enter.update(delta_time, self._hovered_enter)

    def on_draw(self) -> None:
        self.clear()

        # Starfield
        for sx, sy, radius in self._stars:
            drift_x = 220 + ((sx - 220 + self._pulse * 4.0) % (WIDTH - 220))
            twinkle = int(120 + 40 * math.sin(self._pulse * 1.5 + sx * 0.02))
            arcade.draw_circle_filled(drift_x, sy, radius, (twinkle, twinkle, min(255, twinkle + 20)))

        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        arcade.draw_text("CELESTIAL CAMPAIGN MAP // REALM TRAJECTORY", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        cleared_count = max(0, len(self._unlocked) - 1)
        arcade.draw_text(f"CAMPAIGN STATUS: {cleared_count}/7 REALMS LIBERATED // MAX REACHED: WAVE {self.last_wave:02d}",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # ── Connective Trajectory Lines ──────────────────────────────────────
        for left_id, right_id in zip(REALM_ORDER, REALM_ORDER[1:]):
            lx, ly = _NODE_POS[left_id]
            rx, ry = _NODE_POS[right_id]
            left_unlocked = left_id in self._unlocked
            right_unlocked = right_id in self._unlocked

            if left_unlocked and right_unlocked:
                # Active liberated/current path
                arcade.draw_line(lx, ly, rx, ry, (*GOLD, 180), 3)
                arcade.draw_line(lx, ly, rx, ry, (*GOLD_BRIGHT, 90), 1)
            elif left_unlocked and not right_unlocked:
                # Warp conduit to next unlock
                pulse_a = pulse_alpha(self._pulse, 60, 200, 3.0, self._reduced_flashes)
                arcade.draw_line(lx, ly, rx, ry, (*CYAN, pulse_a), 2)
            else:
                # Locked segment
                arcade.draw_line(lx, ly, rx, ry, (*BRASS, 60), 1)

        # ── Realm Nodes ──────────────────────────────────────────────────────
        for realm_id in REALM_ORDER:
            x, y = _NODE_POS[realm_id]
            unlocked = realm_id in self._unlocked
            selected = (realm_id == self._selected)
            hovered = (realm_id == self._hovered)

            node_radius = 24.0 if not selected else 28.0
            # Expand radius slightly on hover for feedback
            if hovered and not selected:
                node_radius += 3.0

            # Background well
            arcade.draw_circle_filled(x, y, node_radius, (*WELL, 240))

            if unlocked:
                # Check if cleared (not the latest unlocked unless all 7 done)
                is_cleared = (realm_id < len(self._unlocked))
                if is_cleared:
                    arcade.draw_circle_filled(x, y, node_radius, (*GOLD, 45))
                    arcade.draw_circle_outline(x, y, node_radius, GOLD, 2)
                    arcade.draw_text("✓", x, y, GOLD_BRIGHT, font_size=16, bold=True,
                                     anchor_x="center", anchor_y="center")
                else:
                    # Current available realm
                    pulse_ring = pulse_alpha(self._pulse, 120, 255, 2.5, self._reduced_flashes)
                    arcade.draw_circle_outline(x, y, node_radius + 4, (*CYAN_BRIGHT, pulse_ring), 2)
                    arcade.draw_circle_outline(x, y, node_radius, CYAN, 2)
                    arcade.draw_text("◈", x, y, CYAN_BRIGHT, font_size=16, bold=True,
                                     anchor_x="center", anchor_y="center")
            else:
                # Locked node
                arcade.draw_circle_outline(x, y, node_radius, (*BRASS, 140), 1)
                arcade.draw_text("⊘", x, y, GREY, font_size=14, bold=True,
                                 anchor_x="center", anchor_y="center")

            # Hover ring — drawn on top of node outline for clear feedback
            if hovered and not selected:
                arcade.draw_circle_outline(x, y, node_radius + 5, (*STARLIGHT, 160), 1)

            # Boss chevron indicator
            if realm_id in BOSS_REALMS:
                arcade.draw_text("▲", x, y + node_radius + 6, ASTRA_RED, font_size=10, bold=True,
                                 anchor_x="center", anchor_y="center")

            # Node label underneath — brighten on hover
            realm_info = REALMS.get(realm_id, {})
            name_col = GOLD_BRIGHT if selected else (STARLIGHT if (hovered or unlocked) else GREY)
            arcade.draw_text(realm_info.get("name", "").upper(), x, y - node_radius - 14,
                             name_col, font_size=8, bold=True, anchor_x="center",
                             font_name=FONT_INTERFACE)
            waves_info = f"W{realm_info.get('waves', [1])[0]}–{realm_info.get('waves', [1])[-1]}"
            arcade.draw_text(waves_info, x, y - node_radius - 26,
                             CYAN if unlocked else (*GREY, 120), font_size=7, bold=True,
                             anchor_x="center", font_name=FONT_TELEMETRY)

        # ── Lower Sector Dossier Panel (x=240 to 880, y=48 to 220) ───────────
        draw_chamfered_panel(240, 880, 48, 220, GOLD if self._selected in self._unlocked else BRASS,
                             fill=SURFACE_LOW, alpha=235, cut=10.0)
        draw_corner_etching(240, 880, 48, 220, GOLD, length=12.0, alpha=110)

        sel_info = REALMS.get(self._selected, {})
        sel_unlocked = self._selected in self._unlocked
        waves_span = f"WAVES {sel_info.get('waves', [1])[0]:02d}–{sel_info.get('waves', [1])[-1]:02d}"

        # Status badge
        status_text = "CLEARED" if (self._selected < len(self._unlocked)) else ("CURRENT ACTIVE" if sel_unlocked else "LOCKED SECTOR")
        status_col = GOLD if status_text == "CLEARED" else (CYAN if sel_unlocked else GREY)
        draw_state_badge(310, 196, status_text, status_col, width=100)

        # Title & waves
        arcade.draw_text(sel_info.get("name", "").upper(), 375, 196, GOLD_BRIGHT,
                         font_size=16, bold=True, anchor_y="center", font_name=FONT_INTERFACE)
        arcade.draw_text(waves_span, 590, 196, CYAN_BRIGHT,
                         font_size=10, bold=True, anchor_y="center", font_name=FONT_TELEMETRY)

        arcade.draw_line(256, 178, 864, 178, (*GOLD, 50), 1)

        # Realm Lore Description
        lore = REALM_LORE.get(self._selected, "Celestial battle theater facing Asura vanguard.")
        arcade.draw_text(lore, 260, 155, PARCHMENT, font_size=9, font_name=FONT_INTERFACE,
                         width=600, multiline=True, align="left", anchor_y="top")

        # Boss threat summary
        if self._selected in BOSS_REALMS:
            boss_name = BOSS_REALMS[self._selected]
            arcade.draw_text(f"THREAT INTELLIGENCE: BOSS OVERLORD {boss_name.upper()}",
                             260, 110, ASTRA_RED_BRIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)
        else:
            arcade.draw_text("THREAT INTELLIGENCE: ASURA FRONTLINE SQUADRONS",
                             260, 110, (*GREY, 180), font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Unlock condition or Sortie button
        if sel_unlocked:
            self._btn_enter.draw()
        else:
            req_wave = REALM_START_WAVES.get(self._selected, 1)
            arcade.draw_text(f"LOCKED // CLEAR WAVE {req_wave - 1:02d} IN CAMPAIGN TO ACCESS",
                             755, 110, GREY, font_size=9, bold=True,
                             anchor_x="center", anchor_y="center", font_name=FONT_TELEMETRY)

        # Keyboard & Navigation Hints
        arcade.draw_text("← → / A D: SELECT REALM   •   ENTER: COMMENCE SORTIE   •   ESC: BACK",
                         560, 24, MUTED, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Draw Nav Rail
        self.nav_rail.draw()

        # Transition
        TransitionOverlay.draw()

    def _enter_selected_realm(self) -> None:
        if self._selected not in self._unlocked or TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        # Save selected starting realm
        saved = save_system.load()
        saved["last_realm"] = self._selected
        save_system.save(saved)

        start_wave = REALM_START_WAVES.get(self._selected, 1)

        # Open story briefing if needed, else difficulty view
        from game.views.story_briefing_view import StoryBriefingView
        briefing = StoryBriefingView(realm_id=self._selected, start_wave=start_wave)
        transition_to(self.window, briefing)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)
        self._hovered_enter = self._btn_enter.contains(x, y)

        self._hovered = -1
        for realm_id, (nx, ny) in _NODE_POS.items():
            if (x - nx) ** 2 + (y - ny) ** 2 <= 28 ** 2:
                self._hovered = realm_id
                break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            return

        if self._btn_enter.contains(x, y):
            self._enter_selected_realm()
            return

        for realm_id, (nx, ny) in _NODE_POS.items():
            if (x - nx) ** 2 + (y - ny) ** 2 <= 30 ** 2:
                self._selected = realm_id
                self.sound_manager.play_ui_click(volume=0.25)
                return

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            curr_idx = REALM_ORDER.index(self._selected)
            self._selected = REALM_ORDER[(curr_idx - 1) % len(REALM_ORDER)]
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            curr_idx = REALM_ORDER.index(self._selected)
            self._selected = REALM_ORDER[(curr_idx + 1) % len(REALM_ORDER)]
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._enter_selected_realm()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())


# ==============================================================================
# [68/77] MODULE: game/views/settings_view.py
# ==============================================================================
"""
game/views/settings_view.py
Console Settings & Accessibility View.
Follows Section 7.11 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, tabbed sections (Audio, Display, Accessibility, Controls),
diamond toggles, sliders with diamond thumbs, and conflict-safe keybind reference.
"""
import arcade

from constants import WIDTH, HEIGHT
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.ui.nav_rail import NavRail
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, BRASS, PARCHMENT,
    STARLIGHT, GREY, MUTED, WELL,
    FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
    draw_state_badge,
)


_TABS = ["AUDIO", "DISPLAY", "ACCESSIBILITY", "CONTROLS"]

_SHAKE_OPTIONS = ["full", "low", "off"]
_PARTICLE_OPTIONS = ["high", "low"]
_COLORBLIND_OPTIONS = ["off", "protan", "deutan", "tritan"]

_KEYBINDINGS = [
    ("MOVE UP", "W  /  UP ARROW", "Movement"),
    ("MOVE DOWN", "S  /  DOWN ARROW", "Movement"),
    ("MOVE LEFT", "A  /  LEFT ARROW", "Movement"),
    ("MOVE RIGHT", "D  /  RIGHT ARROW", "Movement"),
    ("PRIMARY FIRE", "SPACE  /  LEFT CLICK", "Combat"),
    ("DIVINE DASH / ABILITY", "SHIFT", "Combat"),
    ("PAUSE / ABANDON", "ESC", "System"),
    ("CINEMATIC TRAILER (PV)", "V", "System"),
    ("ARMORY SHORTCUT", "H  /  R", "System"),
]


class SettingsView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self.nav_rail = NavRail("settings")

        data = save_system.load()
        self.sfx_volume = data.get("sfx_volume", data.get("volume", 80))
        self.music_volume = data.get("music_volume", data.get("volume", 80))
        self.screen_shake = data.get("screen_shake", "full")
        self.particles = data.get("particles", "high")
        self.reduced_flashes = bool(data.get("reduced_flashes", False))
        self.colorblind_mode = data.get("colorblind_mode", "off")
        self.fullscreen = bool(data.get("fullscreen", False))

        self.sound_manager = SoundManager()

        self._active_tab = 0
        self._hovered_tab = -1
        self._pulse = 0.0
        self._dragging_slider = None  # 'sfx' or 'music'

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)

    def _save_and_apply(self) -> None:
        data = save_system.load()
        data["volume"] = self.sfx_volume
        data["sfx_volume"] = self.sfx_volume
        data["music_volume"] = self.music_volume
        data["screen_shake"] = self.screen_shake
        data["particles"] = self.particles
        data["reduced_flashes"] = self.reduced_flashes
        data["colorblind_mode"] = self.colorblind_mode
        data["fullscreen"] = self.fullscreen
        save_system.save(data)

        target = self.return_view
        if hasattr(target, "game_view"):
            target = target.game_view
        if target:
            if hasattr(target, "particles") and hasattr(target.particles, "reload_settings"):
                target.particles.reload_settings()
            if hasattr(target, "sound_manager") and hasattr(target.sound_manager, "reload_volume"):
                target.sound_manager.reload_volume()
            if hasattr(target, "shake_setting"):
                target.shake_setting = self.screen_shake
            if hasattr(target, "reduced_flashes"):
                target.reduced_flashes = self.reduced_flashes
            if hasattr(target, "colorblind_mode"):
                target.colorblind_mode = self.colorblind_mode
            if hasattr(target, "hud"):
                target.hud.colorblind_mode = self.colorblind_mode
                target.hud.reduced_flashes = self.reduced_flashes

        # Apply fullscreen if changed
        if self.window and self.window.fullscreen != self.fullscreen:
            self.window.set_fullscreen(self.fullscreen)

    def on_draw(self) -> None:
        self.clear()

        # Background scanlines
        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        arcade.draw_text("CONSOLE SETTINGS // CALIBRATION", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("AUDIO • DISPLAY • ACCESSIBILITY • KEYBINDINGS",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # ── Tab Switcher Strip (y=500 to 536) ────────────────────────────────
        tab_w = 145.0
        start_x = 240.0
        for i, tname in enumerate(_TABS):
            tx = start_x + i * (tab_w + 10)
            is_active = (i == self._active_tab)
            is_hov = (i == self._hovered_tab)

            fill_col = SURFACE_HIGH if is_active else (SURFACE_LOW if is_hov else WELL)
            border_col = GOLD if is_active else (CYAN if is_hov else GREY)

            draw_chamfered_panel(tx, tx + tab_w, 502, 536, border_col,
                                 fill=fill_col, alpha=230, border_width=2 if is_active else 1,
                                 cut=6.0)

            tcolor = GOLD_BRIGHT if is_active else (CYAN_BRIGHT if is_hov else GREY)
            arcade.draw_text(tname, tx + tab_w / 2, 519, tcolor,
                             font_size=9, bold=is_active, anchor_x="center", anchor_y="center",
                             font_name=FONT_INTERFACE)

        # ── Active Tab Panel Container (x=240 to 880, y=55 to 490) ───────────
        draw_chamfered_panel(240, 880, 55, 490, GOLD, fill=SURFACE_LOW, alpha=240, cut=10.0)
        draw_corner_etching(240, 880, 55, 490, GOLD, length=14.0, alpha=110)

        # Render Active Tab Content
        if self._active_tab == 0:
            self._draw_audio_tab()
        elif self._active_tab == 1:
            self._draw_display_tab()
        elif self._active_tab == 2:
            self._draw_accessibility_tab()
        elif self._active_tab == 3:
            self._draw_controls_tab()

        # Bottom save & return hint
        arcade.draw_text("TAB / 1-4: SWITCH SECTIONS   •   CLICK: ADJUST SETTINGS   •   ESC: SAVE & EXIT",
                         560, 24, MUTED, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Draw Nav Rail
        self.nav_rail.draw()

        # Transition
        TransitionOverlay.draw()

    def _draw_audio_tab(self) -> None:
        arcade.draw_text("AUDIO MIXER CALIBRATION", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Adjust master volume levels and sound balance", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # SFX Slider
        self._draw_slider(270, 360, 520, "SOUND EFFECTS (SFX)", self.sfx_volume, "sfx")

        # Music Slider
        self._draw_slider(270, 280, 520, "CELESTIAL MUSIC", self.music_volume, "music")

        # Volume guide text
        arcade.draw_text("Sound telemetry adjustments apply dynamically in real time.",
                         270, 180, GREY, font_size=9, font_name=FONT_INTERFACE)

    def _draw_display_tab(self) -> None:
        arcade.draw_text("DISPLAY & GRAPHICS CALIBRATION", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Configure viewport presentation and particle rendering", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # Fullscreen Toggle
        self._draw_toggle(270, 360, "DISPLAY MODE", "Fullscreen (Aspect-Preserving)",
                          "Windowed (900x600)", self.fullscreen)

        # Particle Quality
        self._draw_segmented_selector(270, 280, "PARTICLE QUALITY", ["HIGH", "LOW"],
                                      0 if self.particles == "high" else 1)

        # Screen Shake
        curr_shake_idx = _SHAKE_OPTIONS.index(self.screen_shake) if self.screen_shake in _SHAKE_OPTIONS else 0
        self._draw_segmented_selector(270, 200, "SCREEN SHAKE IMPULSE", ["FULL", "LOW", "OFF"],
                                      curr_shake_idx)

    def _draw_accessibility_tab(self) -> None:
        arcade.draw_text("ACCESSIBILITY & COMFORT", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Visual comfort filters and photosensitivity toggles", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # Reduced Flashes Toggle
        self._draw_diamond_toggle(270, 360, "REDUCED FLASHES",
                                  "Suppresses bright screen flashes, shield strobes, and intense weapon blooms",
                                  self.reduced_flashes)

        # Colorblind Filter
        curr_cb_idx = _COLORBLIND_OPTIONS.index(self.colorblind_mode) if self.colorblind_mode in _COLORBLIND_OPTIONS else 0
        self._draw_segmented_selector(270, 260, "COLORBLIND CORRECTION",
                                      ["OFF", "PROTAN", "DEUTAN", "TRITAN"], curr_cb_idx)

        # UI Scale indicator
        arcade.draw_text("LOGICAL RESOLUTION SCALE", 270, 160, STARLIGHT,
                         font_size=10, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("900x600 Canonical (Automatically aspect-scaled with zero letterbox distortion)",
                         270, 142, CYAN_BRIGHT, font_size=9, font_name=FONT_TELEMETRY)

    def _draw_controls_tab(self) -> None:
        arcade.draw_text("KEYBOARD & MOUSE CALIBRATION", 270, 452, GOLD_BRIGHT,
                         font_size=13, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text("Vimana cockpit tactical control scheme", 270, 436, PARCHMENT,
                         font_size=9, font_name=FONT_INTERFACE)

        arcade.draw_line(270, 420, 850, 420, (*GOLD, 45), 1)

        # Keybindings 2-column grid
        start_y = 390
        row_h = 32
        for i, (action, bind_key, category) in enumerate(_KEYBINDINGS):
            col_x = 270 if i < 5 else 570
            row_y = start_y - (i % 5) * row_h

            arcade.draw_text(action, col_x, row_y, STARLIGHT,
                             font_size=9, bold=True, anchor_y="center", font_name=FONT_INTERFACE)

            # Keybind badge
            draw_state_badge(col_x + 200, row_y, bind_key, GOLD if "Combat" in category else CYAN, width=130)

    def _draw_slider(self, x: float, y: float, width: float, label: str, value: int, key: str) -> None:
        arcade.draw_text(label, x, y + 22, STARLIGHT, font_size=10, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(f"{value}%", x + width, y + 22, GOLD_BRIGHT, font_size=10, bold=True,
                         anchor_x="right", font_name=FONT_TELEMETRY)

        # Track well
        track_h = 6.0
        arcade.draw_lrbt_rectangle_filled(x, x + width, y - track_h / 2, y + track_h / 2, (*WELL, 240))
        arcade.draw_line(x, y, x + width, y, (*GREY, 70), 1)

        # Filled track
        frac = max(0.0, min(1.0, value / 100.0))
        fill_w = width * frac
        arcade.draw_lrbt_rectangle_filled(x, x + fill_w, y - track_h / 2, y + track_h / 2, (*GOLD, 230))

        # Diamond thumb (14x14 rotated square)
        tx = x + fill_w
        diamond = [(tx, y + 8.5), (tx + 8.5, y), (tx, y - 8.5), (tx - 8.5, y)]
        arcade.draw_polygon_filled(diamond, GOLD_BRIGHT)
        arcade.draw_polygon_outline(diamond, OBSIDIAN, 1.5)

    def _draw_toggle(self, x: float, y: float, label: str, on_text: str, off_text: str, state: bool) -> None:
        arcade.draw_text(label, x, y + 20, STARLIGHT, font_size=10, bold=True, font_name=FONT_INTERFACE)

        # Switch box
        sw_w = 260.0
        sw_h = 32.0
        draw_chamfered_panel(x, x + sw_w, y - sw_h / 2, y + sw_h / 2, GOLD if state else GREY,
                             fill=WELL, alpha=230, cut=6.0)

        tlabel = on_text if state else off_text
        arcade.draw_text(tlabel, x + sw_w / 2, y, GOLD_BRIGHT if state else GREY,
                         font_size=9, bold=True, anchor_x="center", anchor_y="center",
                         font_name=FONT_INTERFACE)

    def _draw_diamond_toggle(self, x: float, y: float, label: str, desc: str, state: bool) -> None:
        # 16x16 rotated square diamond toggle per Section 7.11
        cx, cy = x + 12, y + 6
        diamond = [(cx, cy + 11.5), (cx + 11.5, cy), (cx, cy - 11.5), (cx - 11.5, cy)]
        arcade.draw_polygon_filled(diamond, GOLD if state else WELL)
        arcade.draw_polygon_outline(diamond, BRASS, 1.5)
        if state:
            arcade.draw_text("✓", x + 12, y + 6, OBSIDIAN, font_size=10, bold=True,
                             anchor_x="center", anchor_y="center")

        arcade.draw_text(label, x + 36, y + 14, GOLD_BRIGHT if state else STARLIGHT,
                         font_size=10, bold=True, font_name=FONT_INTERFACE)
        arcade.draw_text(desc, x + 36, y - 2, PARCHMENT, font_size=8, font_name=FONT_INTERFACE)

    def _draw_segmented_selector(self, x: float, y: float, label: str, options: list[str], selected_idx: int) -> None:
        arcade.draw_text(label, x, y + 22, STARLIGHT, font_size=10, bold=True, font_name=FONT_INTERFACE)

        btn_w = 90.0
        btn_h = 28.0
        for i, opt in enumerate(options):
            bx = x + i * (btn_w + 8)
            is_sel = (i == selected_idx)
            draw_chamfered_panel(bx, bx + btn_w, y - btn_h / 2, y + btn_h / 2,
                                 GOLD if is_sel else GREY,
                                 fill=SURFACE_HIGH if is_sel else WELL,
                                 alpha=230, cut=5.0)
            if is_sel:
                # Cyan underline indicator
                arcade.draw_line(bx + 6, y - btn_h / 2 + 2, bx + btn_w - 6, y - btn_h / 2 + 2, CYAN_BRIGHT, 2)

            arcade.draw_text(opt, bx + btn_w / 2, y, GOLD_BRIGHT if is_sel else GREY,
                             font_size=8, bold=True, anchor_x="center", anchor_y="center",
                             font_name=FONT_TELEMETRY)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)

        # Tab hover
        self._hovered_tab = -1
        tab_w = 145.0
        for i in range(len(_TABS)):
            tx = 240.0 + i * (tab_w + 10)
            if tx <= x <= tx + tab_w and 502 <= y <= 536:
                self._hovered_tab = i
                break

        # Slider drag
        if self._dragging_slider:
            slider_x = 270.0
            slider_w = 520.0
            new_val = int(max(0, min(100, (x - slider_x) / slider_w * 100)))
            if self._dragging_slider == "sfx":
                self.sfx_volume = new_val
            elif self._dragging_slider == "music":
                self.music_volume = new_val
            self._save_and_apply()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            self._save_and_apply()
            return

        # Check tab clicks
        tab_w = 145.0
        for i in range(len(_TABS)):
            tx = 240.0 + i * (tab_w + 10)
            if tx <= x <= tx + tab_w and 502 <= y <= 536:
                self._active_tab = i
                self.sound_manager.play_ui_click(volume=0.25)
                return

        # Handle tab-specific clicks
        if self._active_tab == 0:
            # SFX slider (y=360)
            if 270 <= x <= 790 and 345 <= y <= 375:
                self._dragging_slider = "sfx"
                self.sfx_volume = int((x - 270) / 520 * 100)
                self._save_and_apply()
            # Music slider (y=280)
            elif 270 <= x <= 790 and 265 <= y <= 295:
                self._dragging_slider = "music"
                self.music_volume = int((x - 270) / 520 * 100)
                self._save_and_apply()

        elif self._active_tab == 1:
            # Fullscreen toggle (y=360)
            if 270 <= x <= 530 and 340 <= y <= 380:
                self.fullscreen = not self.fullscreen
                self.sound_manager.play_ui_click(volume=0.25)
                self._save_and_apply()
            # Particle selector (y=280)
            elif 240 <= y <= 300:
                for i in range(len(_PARTICLE_OPTIONS)):
                    bx = 270 + i * 98
                    if bx <= x <= bx + 90:
                        self.particles = _PARTICLE_OPTIONS[i]
                        self.sound_manager.play_ui_click(volume=0.25)
                        self._save_and_apply()
            # Screen shake (y=200)
            elif 180 <= y <= 220:
                for i in range(len(_SHAKE_OPTIONS)):
                    bx = 270 + i * 98
                    if bx <= x <= bx + 90:
                        self.screen_shake = _SHAKE_OPTIONS[i]
                        self.sound_manager.play_ui_click(volume=0.25)
                        self._save_and_apply()

        elif self._active_tab == 2:
            # Reduced flashes diamond toggle (y=360)
            if 270 <= x <= 800 and 340 <= y <= 385:
                self.reduced_flashes = not self.reduced_flashes
                self.sound_manager.play_ui_click(volume=0.25)
                self._save_and_apply()
            # Colorblind selector (y=260)
            elif 240 <= y <= 280:
                for i in range(len(_COLORBLIND_OPTIONS)):
                    bx = 270 + i * 98
                    if bx <= x <= bx + 90:
                        self.colorblind_mode = _COLORBLIND_OPTIONS[i]
                        self.sound_manager.play_ui_click(volume=0.25)
                        self._save_and_apply()

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        self._dragging_slider = None

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.TAB:
            self._active_tab = (self._active_tab + 1) % len(_TABS)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.KEY_1, arcade.key.NUM_1):
            self._active_tab = 0
        elif key in (arcade.key.KEY_2, arcade.key.NUM_2):
            self._active_tab = 1
        elif key in (arcade.key.KEY_3, arcade.key.NUM_3):
            self._active_tab = 2
        elif key in (arcade.key.KEY_4, arcade.key.NUM_4):
            self._active_tab = 3
        elif key == arcade.key.ESCAPE:
            self._save_and_apply()
            if self.return_view:
                self.window.show_view(self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())


# ==============================================================================
# [69/77] MODULE: game/views/ship_select_view.py
# ==============================================================================
"""
game/views/ship_select_view.py
Fleet Hangar & Astra Armory Selection Screen.
Follows Section 7.5 and Section 9 of the authoritative specification.
Features canonical 220px nav rail, 3 paginated cards per page with counter-rotating halos,
5 real telemetry stats, lock silhouettes, detailed pilot dossier, and celestial deploy action.
"""
import math
import arcade

from constants import WIDTH, HEIGHT
from game.entities.ship_classes import SHIP_CLASSES
from game.systems import save_system
from game.systems.sound_manager import SoundManager
from game.systems.asset_manager import AssetManager
from game.ui.nav_rail import NavRail
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT,
    CYAN, CYAN_BRIGHT, BRASS, PARCHMENT,
    STARLIGHT, GREY, MUTED, WELL,
    FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_segmented_bar,
    draw_scanlines, pulse_alpha, draw_state_badge,
)


_SHIPS = list(SHIP_CLASSES.keys())
_PAGE_SIZE = 3

def _draw_ship_silhouette(cx, cy, ship_id, color, size=32):
    if ship_id == "pushpaka":
        points = ((cx-size*0.8, cy-size*0.6), (cx+size*0.8, cy-size*0.6), (cx+size*0.5, cy+size*0.6), (cx-size*0.5, cy+size*0.6))
    elif ship_id == "tripura":
        points = ((cx-size*0.6, cy-size*0.8), (cx+size*0.6, cy-size*0.8), (cx, cy+size*0.8))
    elif ship_id == "garuda":
        points = ((cx, cy+size*0.8), (cx+size*0.8, cy-size*0.4), (cx+size*0.2, cy-size*0.2), (cx, cy-size*0.8), (cx-size*0.2, cy-size*0.2), (cx-size*0.8, cy-size*0.4))
    elif ship_id == "vajra":
        points = ((cx, cy+size*0.8), (cx+size*0.3, cy), (cx, cy-size*0.8), (cx-size*0.3, cy))
    elif ship_id == "naga":
        points = ((cx-size*0.4, cy-size*0.6), (cx+size*0.6, cy-size*0.2), (cx-size*0.6, cy+size*0.2), (cx+size*0.4, cy+size*0.6))
    elif ship_id == "agneyastra":
        arcade.draw_circle_filled(cx, cy, size*0.4, color)
        points = ((cx-size*0.8, cy), (cx, cy+size*0.8), (cx+size*0.8, cy), (cx, cy-size*0.8))
    elif ship_id == "soma":
        arcade.draw_circle_filled(cx, cy, size*0.6, color)
        arcade.draw_circle_filled(cx+size*0.2, cy+size*0.2, size*0.6, OBSIDIAN)
        points = ()
    elif ship_id == "kubera":
        points = ((cx-size*0.6, cy-size*0.5), (cx+size*0.6, cy-size*0.5), (cx+size*0.6, cy+size*0.5), (cx-size*0.6, cy+size*0.5))
    elif ship_id == "surya":
        arcade.draw_circle_filled(cx, cy, size*0.5, color)
        points = ((cx-size*0.9, cy-size*0.2), (cx-size*0.9, cy+size*0.2), (cx+size*0.9, cy+size*0.2), (cx+size*0.9, cy-size*0.2))
    else:
        points = ((cx, cy+size), (cx+size, cy), (cx, cy-size), (cx-size, cy))
    
    if points:
        arcade.draw_polygon_filled(points, color)


class ShipSelectView(arcade.View):
    def __init__(self, difficulty: str = "normal", start_wave: int = 1,
                 realm_id: int | None = None):
        super().__init__()
        self.difficulty = difficulty
        self.start_wave = max(1, int(start_wave))
        self.realm_id = realm_id

        self.sound_manager = SoundManager()
        self.nav_rail = NavRail("hangar")

        saved = save_system.load()
        self._last_ship = saved.get("last_ship", "pushpaka")
        self._last_wave = max(0, int(saved.get("last_wave", 0)))
        self._reduced_flashes = bool(saved.get("reduced_flashes", False))

        self._selected = _SHIPS.index(self._last_ship) if self._last_ship in _SHIPS else 0
        self._hovered = -1
        self._pulse = 0.0
        self._newly_unlocked: set = set()

        # Primary deploy button
        self._btn_deploy = MenuButton(
            "COMMENCE SORTIE  ▶", 755, 96,
            width=210, height=40, accent=GOLD, variant="celestial"
        )
        self._hovered_deploy = False

    def _is_unlocked(self, ship_id: str) -> bool:
        from game.systems.save_system import get_unlocked_ships
        return ship_id in get_unlocked_ships()

    def on_show_view(self) -> None:
        arcade.set_background_color(OBSIDIAN)
        SoundManager.stop_music()
        saved = save_system.load()
        self._last_wave = max(0, int(saved.get("last_wave", 0)))

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        self.nav_rail.update(delta_time)
        self._btn_deploy.update(delta_time, self._hovered_deploy)

    def on_draw(self) -> None:
        self.clear()

        # Background scanlines
        draw_scanlines(220, WIDTH, 0, HEIGHT, CYAN, spacing=24, alpha=4)

        # ── Top Header Bar (y=548 to 600) ────────────────────────────────────
        arcade.draw_lrbt_rectangle_filled(220, WIDTH, 548, HEIGHT, (*SURFACE_LOW, 220))
        arcade.draw_line(220, 548, WIDTH, 548, (*GOLD, 85), 1)

        arcade.draw_text("FLEET HANGAR // VIMANA SPECIFICATION", 240, 574, GOLD_BRIGHT,
                         font_size=15, bold=True, font_name=FONT_INTERFACE)
        page_num = (self._selected // _PAGE_SIZE) + 1
        total_pages = (len(_SHIPS) + _PAGE_SIZE - 1) // _PAGE_SIZE
        arcade.draw_text(f"ARMORY SQUADRON  •  PAGE {page_num}/{total_pages}  •  SORTIE WAVE {self.start_wave:02d}",
                         240, 558, CYAN, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        # Page indicator chips
        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        visible_ships = _SHIPS[page_start:page_start + _PAGE_SIZE]

        # ── Three Paginated Ship Cards (y=190 to 535) ────────────────────────
        card_w = 200.0
        card_h = 325.0
        spacing = 215.0
        start_x = 240.0 + card_w / 2

        for local_i, ship_id in enumerate(visible_ships):
            idx = page_start + local_i
            sdata = SHIP_CLASSES[ship_id]
            unlocked = self._is_unlocked(ship_id)
            selected = (idx == self._selected)
            hovered = (local_i == self._hovered)

            cx = start_x + local_i * spacing
            cy = 365.0

            left = cx - card_w / 2
            right = cx + card_w / 2
            bottom = cy - card_h / 2
            top = cy + card_h / 2

            # Card Container — selected > hovered > default
            if selected:
                accent_col = GOLD
            elif hovered and unlocked:
                accent_col = CYAN_BRIGHT   # distinct hover: brighter than unselected
            elif hovered:
                accent_col = BRASS         # hover on locked card
            elif unlocked:
                accent_col = CYAN
            else:
                accent_col = BRASS
            fill_col = SURFACE_HIGH if (selected or hovered) else SURFACE_LOW
            draw_chamfered_panel(left, right, bottom, top, accent_col,
                                 fill=fill_col, alpha=235, border_width=2 if selected else (2 if hovered else 1),
                                 selected=selected, cut=10.0)
            if selected:
                draw_corner_etching(left, right, bottom, top, GOLD, length=12.0, alpha=130)

            # Hologram Viewport with counter-rotating halos
            holo_cy = top - 80.0
            arcade.draw_circle_filled(cx, holo_cy, 48.0, (*WELL, 200))
            if selected and not self._reduced_flashes:
                halo_a = pulse_alpha(self._pulse, 30, 90, 2.0)
                arcade.draw_arc_outline(cx, holo_cy, 100, 100, (*CYAN, halo_a),
                                        self._pulse * 18.0, self._pulse * 18.0 + 240, 1.5)
                arcade.draw_arc_outline(cx, holo_cy, 114, 114, (*GOLD, halo_a // 2),
                                        -self._pulse * 14.0, -self._pulse * 14.0 + 200, 1.0)

            # Ship sprite replaced by silhouette
            drift = 0.0 if self._reduced_flashes or not selected else math.sin(self._pulse * 1.5) * 3.0
            if unlocked:
                _draw_ship_silhouette(cx, holo_cy + drift, ship_id, accent_col, size=32)
            else:
                _draw_ship_silhouette(cx, holo_cy, ship_id, (80, 85, 95, 65), size=32)
                draw_state_badge(cx, holo_cy, f"WAVE {sdata.get('unlock_wave', 0):02d}", BRASS, width=78)

            # Card Header Text
            arcade.draw_text(sdata["name"].upper(), cx, top - 142,
                             GOLD_BRIGHT if selected else (STARLIGHT if unlocked else GREY),
                             font_size=11, bold=True, anchor_x="center", font_name=FONT_INTERFACE)
            arcade.draw_text(sdata.get("subtitle", "").upper(), cx, top - 156,
                             CYAN if unlocked else (*GREY, 120),
                             font_size=7, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

            arcade.draw_line(left + 16, top - 168, right - 16, top - 168, (*accent_col, 45), 1)

            # 5 Canonical Telemetry Bars
            bar_labels = [
                ("HULL", sdata["hp"] / 190.0, sdata["hp"]),
                ("FIREPOWER", sdata["bullet_damage"] / 65.0, sdata["bullet_damage"]),
                ("SPEED", sdata["speed"] / 7.2, round(sdata["speed"], 1)),
                ("DASH", 1.0 - (sdata["dash_cooldown"] - 1.2) / 2.2, round(sdata["dash_cooldown"], 1)),
                ("ASTRA", sdata.get("astra_power", 75) / 100.0, sdata.get("astra_power", 75)),
            ]

            by = top - 188
            for blabel, bfrac, bval in bar_labels:
                arcade.draw_text(blabel, left + 16, by + 2, (*GREY, 200),
                                 font_size=7, bold=True, font_name=FONT_TELEMETRY)
                draw_segmented_bar(left + 76, right - 28, by, by + 12,
                                   bfrac, color=GOLD if selected else CYAN, segments=8, gap=2.0)
                arcade.draw_text(f"{bval}", right - 10, by + 2, (*GREY, 200),
                                 font_size=6, bold=True, anchor_x="right", font_name=FONT_TELEMETRY)
                by -= 24

            if not unlocked:
                # Lock indicator banner at bottom of card
                arcade.draw_text(f"UNLOCK AT WAVE {sdata.get('unlock_wave', 0):02d}",
                                 cx, bottom + 26, BRASS,
                                 font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)
                unlock_w = sdata.get("unlock_wave", 0)
                last_w = self._last_wave
                progress = min(1.0, last_w / max(1, unlock_w))
                arcade.draw_lrbt_rectangle_filled(cx - 50, cx + 50, bottom + 12, bottom + 16, SURFACE_HIGH)
                arcade.draw_lrbt_rectangle_filled(cx - 50, cx - 50 + 100 * progress, bottom + 12, bottom + 16, BRASS)
                arcade.draw_text(f"WAVE {last_w}/{unlock_w}", cx, bottom + 2, BRASS,
                                 font_size=6, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)
            elif selected:
                arcade.draw_text("SELECTED VESSEL", cx, bottom + 16, GOLD,
                                 font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Page indicator dots
        total_pages = (len(_SHIPS) + _PAGE_SIZE - 1) // _PAGE_SIZE
        current_page = self._selected // _PAGE_SIZE
        dot_spacing = 20
        dots_width = (total_pages - 1) * dot_spacing
        dot_start_x = 560 - dots_width / 2
        for p in range(total_pages):
            dot_x = dot_start_x + p * dot_spacing
            if p == current_page:
                arcade.draw_text("●", dot_x, 195, GOLD, font_size=12, anchor_x="center", anchor_y="center")
            else:
                arcade.draw_text("○", dot_x, 195, MUTED, font_size=12, anchor_x="center", anchor_y="center")

        # ── Lower Focused Ship Dossier (x=240 to 880, y=42 to 180) ───────────
        draw_chamfered_panel(240, 880, 42, 180, GOLD, fill=SURFACE_LOW, alpha=235, cut=10.0)
        draw_corner_etching(240, 880, 42, 180, GOLD, length=12.0, alpha=100)

        sel_ship = SHIP_CLASSES[_SHIPS[self._selected]]
        sel_unlocked = self._is_unlocked(_SHIPS[self._selected])

        # Header with weapon & ability loadout
        arcade.draw_text(sel_ship["name"].upper(), 256, 156, GOLD_BRIGHT,
                         font_size=14, bold=True, font_name=FONT_INTERFACE)
        draw_state_badge(450, 156, sel_ship.get("subtitle", "VESSEL").upper(), CYAN, width=120)

        arcade.draw_text(f"PRIMARY WEAPON: {sel_ship.get('weapon', 'Brahmastra Cannon')}",
                         600, 156, STARLIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)
        arcade.draw_text(f"DIVINE ABILITY: {sel_ship.get('ability', 'Divine Barrier')}",
                         600, 142, CYAN_BRIGHT, font_size=8, bold=True, font_name=FONT_TELEMETRY)

        arcade.draw_line(256, 134, 864, 134, (*GOLD, 40), 1)

        # Lore narrative body
        lore = sel_ship.get("desc", "Celestial craft forged for cosmic warfare.")
        arcade.draw_text(lore, 256, 114, PARCHMENT, font_size=9, font_name=FONT_INTERFACE)

        # Deploy Sortie or Unlock Banner
        if sel_unlocked:
            self._btn_deploy.draw()
        else:
            arcade.draw_text(f"HULL SECURED // SURVIVE TO WAVE {sel_ship.get('unlock_wave', 0):02d} TO COMMISSION",
                             755, 96, BRASS, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY)

        # Pagination & Controls Hint
        arcade.draw_text(
            "← → / A D: PREV/NEXT VESSEL   •   Q / E: FLIP PAGE   •   ENTER: COMMENCE SORTIE   •   ESC: BACK",
            560, 22, MUTED, font_size=8, bold=True, anchor_x="center", font_name=FONT_TELEMETRY
        )

        # Draw Nav Rail
        self.nav_rail.draw()

        # Transition
        TransitionOverlay.draw()

    def _deploy_focused_ship(self) -> None:
        ship_id = _SHIPS[self._selected]
        if not self._is_unlocked(ship_id) or TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()

        # Save selected ship
        saved = save_system.load()
        saved["last_ship"] = ship_id
        save_system.save(saved)

        # Launch directly into GameView or DifficultyView
        from game.views.game_view import GameView
        game_view = GameView(difficulty=self.difficulty, start_wave=self.start_wave,
                             ship_class=ship_id, realm_id=self.realm_id)
        self.window.show_view(game_view)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.nav_rail.on_mouse_motion(x, y)
        self._hovered_deploy = self._btn_deploy.contains(x, y)

        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        self._hovered = -1
        card_w, card_h = 200.0, 325.0
        start_x, spacing = 240.0 + card_w / 2, 215.0

        for local_i in range(min(_PAGE_SIZE, len(_SHIPS) - page_start)):
            cx = start_x + local_i * spacing
            cy = 365.0
            if cx - card_w / 2 <= x <= cx + card_w / 2 and cy - card_h / 2 <= y <= cy + card_h / 2:
                self._hovered = local_i
                break

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        rail_action = self.nav_rail.on_mouse_press(x, y, self.window)
        if rail_action:
            return

        if self._btn_deploy.contains(x, y):
            self._deploy_focused_ship()
            return

        page_start = (self._selected // _PAGE_SIZE) * _PAGE_SIZE
        card_w, card_h = 200.0, 325.0
        start_x, spacing = 240.0 + card_w / 2, 215.0

        for local_i in range(min(_PAGE_SIZE, len(_SHIPS) - page_start)):
            cx = start_x + local_i * spacing
            cy = 365.0
            if cx - card_w / 2 <= x <= cx + card_w / 2 and cy - card_h / 2 <= y <= cy + card_h / 2:
                self._selected = page_start + local_i
                self.sound_manager.play_ui_click(volume=0.25)
                return

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.LEFT, arcade.key.A):
            self._selected = (self._selected - 1) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._selected = (self._selected + 1) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.22)
        elif key in (arcade.key.Q, arcade.key.PAGEUP):
            self._selected = (self._selected - _PAGE_SIZE) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.E, arcade.key.PAGEDOWN):
            self._selected = (self._selected + _PAGE_SIZE) % len(_SHIPS)
            self.sound_manager.play_ui_click(volume=0.25)
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._deploy_focused_ship()
        elif key == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())


# ==============================================================================
# [70/77] MODULE: game/views/stats_view.py
# ==============================================================================
"""
game/views/stats_view.py
Lifetime stats screen — surfaces save.json progress across all runs.
Bento-grid layout with sections for Core / Per-Difficulty / Per-Ship /
Mastery / Collection.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE
from game.systems import save_system
from game.ui.easing import clamp
from game.ui.tween import TweenManager
from game.ui.transitions import TransitionOverlay
from game.systems.achievement_system import ACHIEVEMENTS_LIST


# ── Helpers ──────────────────────────────────────────────────────────

def _fmt_hms(seconds: float) -> str:
    """Format seconds as 'Xh Ym' or 'Ym Zs' — never shows seconds when hours are present."""
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s"

def _fmt_int(n: int) -> str:
    return f"{n:,}"


# ── Bento panel primitive ────────────────────────────────────────────

class StatPanel:
    """A single bento card — title + 2-3 stat lines, with hover lift."""
    def __init__(self, cx, cy, w, h, title, accent=(120, 180, 255)):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.title = title
        self.accent = accent
        self.lines: list[tuple] = []  # (label, value, value_color)
        self.hover_anim = 0.0
        self.appear_delay = 0.0
        self.appear_anim = 0.0  # 0..1, driven by TweenManager

        # Cached Text objects (per panel) — content/alpha/position update in-place.
        # Max 6 line pairs per panel is more than enough for our 2-3 line panels.
        self._title_text = arcade.Text(
            title.upper(), cx - w / 2 + 14, cy + h / 2 - 14,
            (*accent, 230), font_size=9, bold=True,
        )
        self._label_texts: list[arcade.Text] = []
        self._value_texts: list[arcade.Text] = []
        for _ in range(6):
            self._append_line_text_pair()

    def _append_line_text_pair(self) -> None:
        self._label_texts.append(arcade.Text(
            "", self.cx - self.w / 2 + 14, 0,
            (140, 150, 180, 200), font_size=9, bold=True,
        ))
        self._value_texts.append(arcade.Text(
            "", self.cx + self.w / 2 - 14, 0,
            (220, 230, 250, 240), font_size=11, bold=True,
            anchor_x="right",
        ))

    def _ensure_line_capacity(self, count: int) -> None:
        while len(self._label_texts) < count:
            self._append_line_text_pair()

    def _visible_lines(self) -> list[tuple]:
        """Keep dense panels readable while retaining a useful overflow summary."""
        max_visible = max(1, int((self.h - 30) // 16))
        if len(self.lines) <= max_visible:
            return self.lines
        kept = max(1, max_visible - 1)
        return list(self.lines[:kept]) + [
            ("More", f"+{len(self.lines) - kept} tracked", (160, 200, 240))
        ]

    def _sync_line_text(self, idx, label, value, vcol, alpha):
        """Update one cached Text pair with current label/value/alpha."""
        lt = self._label_texts[idx]
        vt = self._value_texts[idx]
        lt.text = label
        vt.text = value
        lt.color = (140, 150, 180, int(200 * alpha))
        vt.color = (*vcol, int(240 * alpha))

    @property
    def left(self):   return self.cx - self.w / 2
    @property
    def right(self):  return self.cx + self.w / 2
    @property
    def bottom(self): return self.cy - self.h / 2
    @property
    def top(self):    return self.cy + self.h / 2

    def hit_test(self, x, y):
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    def update(self, dt, mouse_x, mouse_y):
        target = 1.0 if self.hit_test(mouse_x, mouse_y) else 0.0
        self.hover_anim += (target - self.hover_anim) * min(1.0, 12.0 * dt)
        # Drive appear anim
        if self.appear_delay > 0:
            self.appear_delay -= dt
        else:
            self.appear_anim = min(1.0, self.appear_anim + dt * 2.5)

    def draw(self):
        if self.appear_anim <= 0.0:
            return
        a = clamp(self.appear_anim)
        scale = 0.92 + 0.08 * a + 0.02 * self.hover_anim
        cx = self.cx
        cy = self.cy - (1.0 - a) * 12  # rise-in
        w = self.w * scale
        h = self.h * scale

        # Background — blend with hover
        idle = (18, 24, 46)
        hov  = (28, 38, 72)
        bg = _lerp(idle, hov, self.hover_anim)
        arcade.draw_lrbt_rectangle_filled(
            cx - w / 2, cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*bg, int(220 * a)),
        )
        # Accent stripe on the left
        arcade.draw_lrbt_rectangle_filled(
            cx - w / 2, cx - w / 2 + 4,
            cy - h / 2, cy + h / 2,
            (*self.accent, int(220 * a)),
        )
        # Border
        border = (90, 110, 150) if self.hover_anim < 0.5 else self.accent
        arcade.draw_lrbt_rectangle_outline(
            cx - w / 2, cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*border, int(220 * a)), 2 if self.hover_anim > 0.5 else 1,
        )

        # Title — cached Text, position + color update per frame.
        self._title_text.position = (cx - w / 2 + 14, cy + h / 2 - 14)
        self._title_text.color = (*self.accent, int(230 * a))
        self._title_text.draw()

        # Stat lines — cached Text pairs, no per-frame arcade.draw_text.
        visible_lines = self._visible_lines()
        self._ensure_line_capacity(len(visible_lines))
        line_y = cy + h / 2 - 30
        for idx, (label, value, vcol) in enumerate(visible_lines):
            self._sync_line_text(idx, label, value, vcol, a)
            self._label_texts[idx].position = (cx - w / 2 + 14, line_y)
            self._value_texts[idx].position = (cx + w / 2 - 14, line_y)
            self._label_texts[idx].draw()
            self._value_texts[idx].draw()
            line_y -= 16


def _lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1[:3], c2[:3]))


# ── Main view ────────────────────────────────────────────────────────

class StatsView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._mouse_x = 0.0
        self._mouse_y = 0.0
        self._pulse = 0.0
        self._tweens = TweenManager()

        # Title text
        self._title = arcade.Text(
            "WARRIOR ARCHIVES — LIFETIME STATS",
            WIDTH // 2, HEIGHT - 50,
            COLOR_SCORE, font_size=24, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "ESC : Back",
            WIDTH // 2, 30,
            (160, 160, 190), font_size=11, bold=True,
            anchor_x="center",
        )
        # Empty-state notice (shown when nothing has been recorded yet)
        self._empty = arcade.Text(
            "No runs yet — defeat some Asuras to fill this archive!",
            WIDTH // 2, HEIGHT // 2,
            (180, 180, 210), font_size=13,
            anchor_x="center", anchor_y="center",
        )
        self._show_empty = False

        # Build the panels
        self._panels: list[StatPanel] = []
        self._build_panels()

    # ── Panel layout ───────────────────────────────────────────────────

    def _build_panels(self) -> None:
        data = save_system.load()
        played = data["games_played"] > 0

        # Panel size + spacing
        pw, ph = 240, 110
        gap_x, gap_y = 20, 20
        # 3 columns × 2 rows
        cols = 3
        col_w = pw
        total_w = cols * col_w + (cols - 1) * gap_x
        start_x = WIDTH // 2 - total_w / 2 + col_w / 2
        # Vertically centered with title above
        row_h = ph
        start_y = HEIGHT // 2 + 30

        def pos(c, r):
            return (start_x + c * (col_w + gap_x),
                    start_y - r * (row_h + gap_y))

        def make_panel(c, r, title, accent):
            p = StatPanel(*pos(c, r), pw, ph, title, accent=accent)
            return p

        # ── Row 0 ──────────────────────────────────────────────────────
        # Core
        p = make_panel(0, 0, "Core Records", (255, 215, 60))
        p.lines = [
            ("High Score",  _fmt_int(data["high_score"]),  (255, 220, 50)),
            ("Best Wave",   f"{data['last_wave']}",        (200, 230, 255)),
            ("Total Kills", _fmt_int(data["total_kills"]), (255, 100, 100)),
        ]
        self._panels.append(p)

        # Playtime
        p = make_panel(1, 0, "Time in Combat", (100, 220, 200))
        p.lines = [
            ("Lifetime",    _fmt_hms(data["playtime_seconds"]), (100, 230, 200)),
            ("Runs Played", f"{data['games_played']}",          (220, 230, 255)),
            ("Best Combo",  f"×{max(1, data['best_combo'])}",   (255, 150, 30)),
        ]
        self._panels.append(p)

        # Damage & Boons
        p = make_panel(2, 0, "Damage & Boons", (220, 100, 220))
        p.lines = [
            ("Total Damage",  _fmt_int(data["total_damage"]), (255, 160, 60)),
            ("Boons Claimed", f"{data['total_boons']}",       (255, 100, 220)),
            ("Endless Best",  f"W{data['endless_high_wave']}  {_fmt_int(data['endless_high_score'])} pts",
                                                              (160, 220, 255)),
        ]
        self._panels.append(p)

        # ── Row 1 ──────────────────────────────────────────────────────
        # Achievements (collection)
        unlocked = set(data.get("achievements") or [])
        total = len(ACHIEVEMENTS_LIST)
        pct = (len(unlocked) / total * 100) if total else 0
        p = make_panel(0, 1, "Trophy Collection", (255, 200, 100))
        p.lines = [
            ("Unlocked",     f"{len(unlocked)} / {total}",  (255, 230, 60)),
            ("Completion",   f"{pct:.0f}%",                 (200, 220, 255)),
            ("Last Trophy",  self._last_unlocked_name(unlocked) or "—",
                                                              (160, 200, 240)),
        ]
        self._panels.append(p)

        # Bosses
        bosses = data.get("bosses_defeated") or []
        p = make_panel(1, 1, "Bosses Vanquished", (220, 60, 100))
        p.lines = [
            ("Total",       f"{len(bosses)} / 4",          (255, 100, 130)),
            ("Kumbhakarna", "✓" if "kumbhakarna" in bosses else "—",
                                                            (210, 140, 20)),
            ("Ravana",      "✓" if "ravana"      in bosses else "—",
                                                            (220, 0, 80)),
            ("Mahishasura", "✓" if "mahishasura" in bosses else "—",
                                                            (255, 120, 40)),
            ("Vritra",      "✓" if "vritra"      in bosses else "—",
                                                            (190, 80, 255)),
        ]
        self._panels.append(p)

        # Ships mastered
        from game.entities.ship_classes import SHIP_CLASSES
        mastered = set(data.get("ships_mastered") or [])
        p = make_panel(2, 1, "Vimana Mastery", (120, 240, 255))
        ship_lines = []
        for sid, sdata in SHIP_CLASSES.items():
            mark = "✓" if sid in mastered else "—"
            ship_lines.append((sdata["name"], mark,
                               sdata["color"] if sid in mastered else (120, 130, 150)))
        p.lines = ship_lines
        self._panels.append(p)

        # Stagger the panel appearances for a nice cascade
        for i, panel in enumerate(self._panels):
            panel.appear_anim = 0.0
            panel.appear_delay = i * 0.06

        # Show empty state if the player has never finished a run
        self._show_empty = not played

    def _last_unlocked_name(self, unlocked: set) -> str | None:
        if not unlocked:
            return None
        # ACHIEVEMENTS_LIST is in declared order; last is most-recent visually
        for ach in reversed(ACHIEVEMENTS_LIST):
            if ach["id"] in unlocked:
                return ach["name"]
        return None

    # ── Lifecycle ──────────────────────────────────────────────────────

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time
        for panel in self._panels:
            panel.update(delta_time, self._mouse_x, self._mouse_y)

    def on_draw(self) -> None:
        self.clear()
        self._title.draw()
        if self._show_empty:
            self._empty.draw()
        else:
            for panel in self._panels:
                panel.draw()
        self._hint.draw()
        TransitionOverlay.draw()

    # ── Input ──────────────────────────────────────────────────────────

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._mouse_x = x
        self._mouse_y = y

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            if self.return_view:
                from game.ui.transitions import transition_to
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                from game.ui.transitions import transition_to
                transition_to(self.window, MenuView())


# ==============================================================================
# [71/77] MODULE: game/views/story_briefing_view.py
# ==============================================================================
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


# ==============================================================================
# [72/77] MODULE: game/views/victory_view.py
# ==============================================================================
import math
import random
import arcade
from constants import WIDTH, HEIGHT
from game.systems import save_system
from game.ui.easing import ease_out_cubic, ease_out_elastic, ease_in_out_cubic, clamp
from game.ui.tween import TweenManager
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    draw_menu_backdrop, draw_focus_panel,
    GOLD, CYAN, CYAN_BRIGHT, STARLIGHT, GREY,
    FONT_CEREMONIAL, FONT_INTERFACE,
)
try:
    from game.systems.sound_manager import SoundManager
except ImportError:
    SoundManager = None


class _FloatRef:
    """Mutable float holder so we can tween list-element 'alpha' values.
    Lists don't support setattr(list, idx, val) so we wrap each alpha."""
    __slots__ = ("val",)
    def __init__(self, val: float = 0.0):
        self.val = val

class ConfettiParticle:
    def __init__(self, x, y, dx, dy, color):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.color = color
        self.life = 2.0
        self.max_life = 2.0
        self.angle = random.uniform(0, 360)
        self.d_angle = random.uniform(-100, 100)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        self.dy -= 300 * dt  # gravity
        self.angle += self.d_angle * dt
        self.life -= dt

    def draw(self):
        if self.life > 0:
            # Eased alpha
            t = 1.0 - (self.life / self.max_life)
            alpha_t = ease_out_cubic(1.0 - t)
            alpha = int(255 * alpha_t)
            c = self.color[:3] + (alpha,)
            arcade.draw_rect_filled(arcade.XYWH(self.x, self.y, 8, 8), c, self.angle)

class VictoryView(arcade.View):
    def __init__(self, score, kills, highest_combo, difficulty='normal',
                 ship_class='pushpaka', wave=10, stats=None):
        super().__init__()
        self.score = score
        self.kills = kills
        self.highest_combo = highest_combo
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.wave = wave
        self.stats = stats or {}
        
        self.time_elapsed = 0.0
        self._tweens = TweenManager()
        
        self._title_y = HEIGHT + 100.0
        self._displayed_score = 0.0
        # Wrapped float refs so each row alpha can be independently tweened.
        self._alpha_refs = [_FloatRef(0.0) for _ in range(5)]
        # Mirror list kept for the on_draw reads (avoids changing the draw code).
        self._row_alphas = [ref.val for ref in self._alpha_refs]
        
        self.particles = []
        self.particle_timer = 0.0
        
        # Glow pulse state
        self._glow_pulse = 0.0

        # ── Pre-built arcade.Text objects ────────────────────────────────────
        # Title — position is animated; y updated each frame in on_draw
        self._t_title = arcade.Text(
            "VICTORY!",
            WIDTH // 2, int(self._title_y),
            GOLD, font_size=52,
            font_name=FONT_CEREMONIAL[0],
            anchor_x="center", anchor_y="center",
        )

        # Subtitle lore line (y set relative to title_y in on_draw)
        self._t_subtitle = arcade.Text(
            "KARMIC TRANSCENDENCE  \u2022  DHARMA RESTORED",
            WIDTH // 2, 0,
            CYAN_BRIGHT, font_size=11, bold=True,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )

        # Stat rows — content and color updated each frame in on_draw
        _cx   = WIDTH // 2
        _base = int(HEIGHT * 0.58)
        _sp   = 46

        self._t_score_row = arcade.Text(
            "", _cx, _base,
            (*GOLD[:3], 0), font_size=22,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
        self._t_kills_row = arcade.Text(
            "", _cx, _base - _sp,
            (*STARLIGHT[:3], 0), font_size=18,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
        self._t_combo_row = arcade.Text(
            "", _cx, _base - _sp * 2,
            (*CYAN[:3], 0), font_size=18,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
        self._t_diff_row = arcade.Text(
            "", _cx, _base - _sp * 3,
            (*STARLIGHT[:3], 0), font_size=18,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
        self._t_breakdown = arcade.Text(
            "", _cx, _base - _sp * 4,
            (255, 170, 80, 0), font_size=14,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )

        # Bottom prompts
        _prompt_y = int(HEIGHT * 0.14)
        self._t_prompt_enter = arcade.Text(
            "ENTER  \u2014  NEXT REALM / SORTIE",
            _cx, _prompt_y + 30,
            (*GOLD[:3], 0), font_size=14, bold=True,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
        self._t_prompt_l = arcade.Text(
            "L  \u2014  AKASHIC RECORDS",
            _cx, _prompt_y,
            (*CYAN[:3], 0), font_size=14, bold=True,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
        self._t_prompt_esc = arcade.Text(
            "ESC  \u2014  RETURN TO SOURCE",
            _cx, _prompt_y - 30,
            (*GREY[:3], 0), font_size=14,
            font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center",
        )
    def on_show_view(self):
        if SoundManager:
            SoundManager.stop_music()

        arcade.set_background_color((5, 8, 20))
        self._reduced_flashes = bool(save_system.load().get("reduced_flashes", False))

        # Reset animation state for repeat visits.
        self._title_y = HEIGHT + 100.0
        self._displayed_score = 0.0
        for ref in self._alpha_refs:
            ref.val = 0.0
        self._row_alphas = [ref.val for ref in self._alpha_refs]

        self._tweens.cancel_all()

        # Title slam-in
        self._tweens.tween(
            target=self,
            attr='_title_y',
            end=HEIGHT * 0.82,
            duration=0.8,
            ease=ease_out_elastic,
            start=HEIGHT + 100.0,
        )

        # Score count-up
        self._tweens.tween(
            target=self,
            attr='_displayed_score',
            end=float(self.score),
            duration=1.2,
            delay=0.5,
            ease=ease_out_cubic,
            start=0.0,
        )

        # Staggered stat reveal — tween each FloatRef's .val (lists don't support attr-by-index).
        for i, ref in enumerate(self._alpha_refs):
            self._tweens.tween(
                target=ref,
                attr='val',
                end=255.0,
                duration=0.5,
                delay=1.0 + i * 0.15,
                ease=ease_out_cubic,
                start=0.0,
            )

        try:
            save_system.update_after_game(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
                highest_combo=self.highest_combo,
                total_damage=self.stats.get("total_damage", 0),
                boons_claimed=self.stats.get("boons_claimed", 0),
                bosses_defeated=self.stats.get("bosses_defeated", []),
                ship_class=self.ship_class,
                campaign_cleared=True,
            )
            from game.systems.leaderboard_client import leaderboard_client
            leaderboard_client.push_profile()
        except Exception:
            pass
        
    def on_update(self, dt):
        self.time_elapsed += dt
        self._tweens.update(dt)
        TransitionOverlay.update(dt)

        # Sync the alpha mirror from the tweenable refs (draw code reads the list).
        for i, ref in enumerate(self._alpha_refs):
            self._row_alphas[i] = ref.val
        
        # Pulse for glow
        self._glow_pulse = ease_in_out_cubic((math.sin(self.time_elapsed * 3.0) + 1.0) / 2.0)
        
        # Confetti spawn
        self.particle_timer += dt
        if self.particle_timer > 0.05:
            self.particle_timer = 0.0
            colors = [
                (255, 215, 0),   # Gold
                (255, 223, 0),   # Yellow
                (0, 255, 255),   # Cyan
                (255, 0, 255)    # Magenta
            ]
            for _ in range(4):
                x = random.uniform(0, WIDTH)
                y = HEIGHT + 20
                dx = random.uniform(-100, 100)
                dy = random.uniform(-150, 50)
                c = random.choices(colors, weights=[0.6, 0.2, 0.1, 0.1])[0]
                self.particles.append(ConfettiParticle(x, y, dx, dy, c))
                
        # Update particles
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]
        
    def on_draw(self):
        reduced = getattr(self, "_reduced_flashes", False)
        draw_menu_backdrop("MISSION COMPLETE", "CAMPAIGN RESULT // REWARDS AND RECORDS", GOLD, pulse=self.time_elapsed, reduced=reduced)
        draw_focus_panel(WIDTH // 2 - 240, WIDTH // 2 + 240, HEIGHT * 0.12, HEIGHT * 0.66, GOLD, selected=True)
        # Draw particles
        for p in self.particles:
            p.draw()

        # Draw Title with glow
        title_y = int(self._title_y)

        # Pulse glow
        glow_radius_1 = 60 + 20 * self._glow_pulse
        glow_radius_2 = 100 + 30 * self._glow_pulse

        arcade.draw_circle_filled(WIDTH // 2, title_y, glow_radius_2, (255, 215, 0, 20))
        arcade.draw_circle_filled(WIDTH // 2, title_y, glow_radius_1, (255, 215, 0, 40))

        # Title (animated y position)
        self._t_title.y = title_y
        self._t_title.draw()

        # Subtitle lore line — 36px below title centre
        self._t_subtitle.y = title_y - 36
        self._t_subtitle.draw()

        # Draw Stats
        # Score
        alpha0 = int(clamp(self._row_alphas[0], 0, 255))
        self._t_score_row.text = f"Dharmic Karma Reclaimed: {int(self._displayed_score):,}"
        self._t_score_row.color = (*GOLD[:3], alpha0)
        self._t_score_row.draw()

        # Kills
        alpha1 = int(clamp(self._row_alphas[1], 0, 255))
        self._t_kills_row.text = f"Asura Legion Purged: {self.kills}"
        self._t_kills_row.color = (*STARLIGHT[:3], alpha1)
        self._t_kills_row.draw()

        # Combo
        alpha2 = int(clamp(self._row_alphas[2], 0, 255))
        self._t_combo_row.text = f"Highest Battle Flow: {self.highest_combo}"
        self._t_combo_row.color = (*CYAN[:3], alpha2)
        self._t_combo_row.draw()

        # Difficulty
        alpha3 = int(clamp(self._row_alphas[3], 0, 255))
        self._t_diff_row.text = f"Difficulty: {self.difficulty.capitalize()}"
        self._t_diff_row.color = (*STARLIGHT[:3], alpha3)
        self._t_diff_row.draw()

        # Compact combat breakdown
        alpha4 = int(clamp(self._row_alphas[4], 0, 255))
        total_damage = int(self.stats.get("total_damage", 0))
        perfect_dodges = int(self.stats.get("perfect_dodges", 0))
        self._t_breakdown.text = f"Total Damage: {total_damage:,}  \u2022  Perfect Dodges: {perfect_dodges}"
        self._t_breakdown.color = (255, 170, 80, alpha4)
        self._t_breakdown.draw()

        # Prompts (gold / cyan / muted)
        self._t_prompt_enter.color = (*GOLD[:3], alpha4)
        self._t_prompt_enter.draw()

        self._t_prompt_l.color = (*CYAN[:3], alpha4)
        self._t_prompt_l.draw()

        self._t_prompt_esc.color = (*GREY[:3], alpha4)
        self._t_prompt_esc.draw()

        TransitionOverlay.draw()

    def on_key_press(self, symbol, modifiers):
        if TransitionOverlay.is_active:
            return
            
        if symbol == arcade.key.ENTER:
            from game.views.realm_map_view import RealmMapView
            transition_to(self.window, RealmMapView())
        elif symbol == arcade.key.L:
            from game.views.leaderboard_view import LeaderboardView
            transition_to(self.window, LeaderboardView())
        elif symbol == arcade.key.ESCAPE:
            from game.views.menu_view import MenuView
            transition_to(self.window, MenuView())


# ==============================================================================
# [73/77] MODULE: backend/app.py
# ==============================================================================
"""
backend/app.py
Flask REST API for Vimana Wars Online Leaderboard.
Uses SQLite for zero-config persistence.
"""
import sqlite3
import os
import logging
import hashlib
import hmac
import json
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from pathlib import Path
from flask import Flask, request, jsonify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("VimanaWarsBackend")

app = Flask(__name__)
from flask_socketio import SocketIO, join_room, leave_room, emit
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

try:
    from backend.firebase_service import (
        save_user_to_firebase, save_score_to_firebase,
        save_cloud_save_to_firebase, get_firebase_status,
    )
except ImportError:
    from firebase_service import (
        save_user_to_firebase, save_score_to_firebase,
        save_cloud_save_to_firebase, get_firebase_status,
    )

DB_PATH = Path(os.environ.get("DATABASE_PATH", "leaderboard.db"))
if not DB_PATH.exists() and (Path(__file__).resolve().parent.parent / "leaderboard.db").exists():
    DB_PATH = Path(__file__).resolve().parent.parent / "leaderboard.db"
elif not DB_PATH.exists() and (Path(__file__).resolve().parent.parent.parent / "leaderboard.db").exists():
    DB_PATH = Path(__file__).resolve().parent.parent.parent / "leaderboard.db"
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
SESSION_TTL_SECONDS = 30 * 24 * 60 * 60
ACTION_TOKEN_TTL_SECONDS = 30 * 60
REQUIRE_EMAIL_VERIFICATION = os.environ.get("REQUIRE_EMAIL_VERIFICATION", "0").lower() in ("1", "true", "yes")
SHOW_DEV_AUTH_TOKENS = os.environ.get("SHOW_DEV_AUTH_TOKENS", "0").lower() in ("1", "true", "yes")
# Browser clients need explicit CORS origins when the React site is hosted on
# a different Render domain.  Keep this allow-list based instead of using '*'
# so bearer tokens are never exposed to arbitrary origins.
_CORS_ORIGINS = {
    origin.strip().rstrip("/")
    for origin in os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:5173,http://localhost:4173,http://localhost:8443",
    ).split(",")
    if origin.strip()
}
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_SHIP_IDS = (
    "pushpaka", "tripura", "garuda", "vajra", "naga",
    "agneyastra", "soma", "kubera", "surya",
)
_RATE_LIMITS = {
    "register": (5, 60),
    "login": (10, 60),
    "verify": (10, 60),
    "reset_request": (5, 60),
    "reset_password": (10, 60),
    "score": (60, 60),
}
_rate_state = defaultdict(deque)
_rate_lock = threading.Lock()
_PROFILE_KEYS = {
    "player_name", "high_score", "last_wave", "difficulty", "last_ship",
    "last_realm", "realm_unlock_seen", "total_kills", "games_played",
    "total_damage", "best_combo", "total_boons", "bosses_defeated",
    "playtime_seconds", "ships_mastered", "achievements", "endless_high_wave",
    "endless_high_score",
}


def get_db():
    if DATABASE_URL:
        try:
            import psycopg
            from psycopg.rows import dict_row
        except ImportError as exc:
            raise RuntimeError("DATABASE_URL is set but psycopg is not installed") from exc
        connection = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        return _PostgresConnection(connection)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class _PostgresConnection:
    """Tiny compatibility wrapper for the existing parameterized queries."""
    is_postgres = True

    def __init__(self, connection):
        self._connection = connection

    def execute(self, statement, params=()):
        return self._connection.execute(statement.replace("?", "%s"), params)

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self._connection.close()


def _is_postgres() -> bool:
    return bool(DATABASE_URL)


def _is_integrity_error(exc: Exception) -> bool:
    return isinstance(exc, sqlite3.IntegrityError) or (
        _is_postgres() and getattr(exc, "sqlstate", None) == "23505"
    )


def init_db():
    with get_db() as conn:
        id_definition = (
            "INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY"
            if _is_postgres() else "INTEGER PRIMARY KEY AUTOINCREMENT"
        )
        email_definition = "email TEXT NOT NULL UNIQUE" if _is_postgres() else "email TEXT NOT NULL UNIQUE COLLATE NOCASE"
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id %s,
                game_id TEXT NOT NULL UNIQUE,
                %s,
                player_name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                email_verified INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ % (id_definition, email_definition))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS auth_tokens (
                token_hash TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                purpose TEXT NOT NULL,
                expires_at INTEGER NOT NULL,
                consumed_at INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                user_id INTEGER PRIMARY KEY,
                profile_json TEXT NOT NULL DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id %s,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                difficulty TEXT DEFAULT 'normal',
                ship_class TEXT DEFAULT 'pushpaka',
                user_id INTEGER,
                game_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """ % id_definition)
        # Safe migrations for databases created by earlier versions.
        migration_columns = (
            "ALTER TABLE users ADD COLUMN email_verified INTEGER NOT NULL DEFAULT 0",
            "ALTER TABLE scores ADD COLUMN ship_class TEXT DEFAULT 'pushpaka'",
            "ALTER TABLE scores ADD COLUMN user_id INTEGER",
            "ALTER TABLE scores ADD COLUMN game_id TEXT",
            "ALTER TABLE scores ADD COLUMN kills INTEGER DEFAULT 0",
            "ALTER TABLE scores ADD COLUMN total_damage INTEGER DEFAULT 0",
            "ALTER TABLE scores ADD COLUMN duration_seconds REAL DEFAULT 0",
        )
        statements = tuple(
            statement.replace("ADD COLUMN ", "ADD COLUMN IF NOT EXISTS ")
            for statement in migration_columns
        ) if _is_postgres() else migration_columns
        for statement in statements:
            try:
                conn.execute(statement)
            except Exception as exc:
                # SQLite and PostgreSQL both report duplicate columns here;
                # preserve real connection/schema errors.
                duplicate_column = (
                    isinstance(exc, sqlite3.OperationalError)
                    or (_is_postgres() and getattr(exc, "sqlstate", None) == "42701")
                )
                if not duplicate_column:
                    raise
        conn.commit()


# Initialize database table on startup
init_db()


@app.after_request
def add_cors_headers(response):
    """Allow the separately hosted React frontend to call this API."""
    origin = request.headers.get("Origin", "").rstrip("/")
    if origin in _CORS_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
        response.headers["Access-Control-Max-Age"] = "600"
        response.headers.add("Vary", "Origin")
    return response


@app.route("/<path:_path>", methods=["OPTIONS"])
def cors_preflight(_path):
    return ("", 204)


@app.route("/", methods=["GET", "OPTIONS"])
def index():
    if request.method == "OPTIONS":
        return ("", 204)
    logger.info("API Root status checked from %s", request.remote_addr)
    return jsonify({
        "game": "Vimana Wars API",
        "status": "online",
        "firebase_gsa": get_firebase_status(),
        "endpoints": {
            "GET /health": "Server health and database/GSA status",
            "GET /scores/top": "Get top leaderboard entries (?limit=10&difficulty=normal)",
            "POST /scores": "Submit a score (Bearer token optional for guest submissions)",
            "POST /auth/register": "Create an email account and receive a stable Game ID",
            "POST /auth/login": "Sign in with email and password",
            "POST /auth/verify-email": "Verify an email address with its one-time token",
            "POST /auth/request-password-reset": "Request a password reset token",
            "POST /auth/reset-password": "Set a new password with a reset token",
            "GET /auth/me": "Get the signed-in player profile",
            "GET /account/profile": "Get cloud-synced progression and achievements",
            "PUT /account/profile": "Sync cloud-saved progression and achievements",
            "GET /account/stats": "Get personal online gameplay statistics",
            "GET /multiplayer/lobbies": "Browse active multiplayer lobbies",
            "POST /multiplayer/lobbies": "Create a multiplayer lobby",
            "GET /scores/stats": "Global gameplay metrics",
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Vimana Wars Backend",
        "database": "postgresql" if DATABASE_URL else "sqlite",
        "firebase_gsa": get_firebase_status(),
        "timestamp": time.time(),
    })


def _rate_limit(action: str):
    """Small process-local guard; production deployments should use Redis."""
    limit, window = _RATE_LIMITS[action]
    now = time.monotonic()
    key = (action, request.remote_addr or "unknown")
    with _rate_lock:
        calls = _rate_state[key]
        while calls and now - calls[0] >= window:
            calls.popleft()
        if len(calls) >= limit:
            retry_after = max(1, int(window - (now - calls[0])))
            return jsonify({"error": "Too many requests. Please try again shortly."}), 429, {
                "Retry-After": str(retry_after)
            }
        calls.append(now)
    return None


def _new_action_token(conn, user_id: int, purpose: str) -> str:
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO auth_tokens (token_hash, user_id, purpose, expires_at) VALUES (?, ?, ?, ?)",
        (hashlib.sha256(token.encode("utf-8")).hexdigest(), user_id, purpose,
         int(time.time()) + ACTION_TOKEN_TTL_SECONDS),
    )
    return token


def _default_profile() -> dict:
    return {
        "player_name": "Warrior", "high_score": 0, "last_wave": 0,
        "difficulty": "normal", "last_ship": "pushpaka", "last_realm": 1,
        "realm_unlock_seen": [], "total_kills": 0, "games_played": 0,
        "total_damage": 0, "best_combo": 1, "total_boons": 0,
        "bosses_defeated": [], "playtime_seconds": 0, "ships_mastered": [],
        "achievements": [], "endless_high_wave": 0, "endless_high_score": 0,
    }


def _profile_from_payload(value) -> dict:
    if not isinstance(value, dict):
        return {}
    profile = {}
    for key in _PROFILE_KEYS:
        if key in value:
            profile[key] = value[key]
    # Prevent a malformed client from creating unbounded profile data.
    encoded = json.dumps(profile, separators=(",", ":"))
    return profile if len(encoded) <= 100_000 else {}


# Multiplayer lobby state is intentionally ephemeral. It is suitable for a
# first lobby/matchmaking layer; live combat state belongs in a WebSocket or
# dedicated game server and should not be stored in this request database.
_lobbies = {}
_lobbies_lock = threading.Lock()


def _new_lobby_code() -> str:
    with _lobbies_lock:
        while True:
            code = secrets.token_hex(3).upper()
            if code not in _lobbies:
                return code


def _lobby_payload(lobby: dict) -> dict:
    return {
        "code": lobby["code"],
        "mode": lobby["mode"],
        "max_players": lobby["max_players"],
        "status": lobby["status"],
        "host_game_id": lobby["host_game_id"],
        "players": list(lobby["players"].values()),
        "created_at": lobby["created_at"],
        "rules": lobby.get("rules", {"health": 100, "win_condition": "first pilot to reduce the opponent to 0 HP"}),
    }


def _password_hash(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 210_000)
    return f"pbkdf2_sha256$210000${salt.hex()}${digest.hex()}"


def _password_matches(password: str, encoded: str) -> bool:
    try:
        algorithm, rounds, salt_hex, digest_hex = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        expected = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(rounds)
        ).hex()
        return hmac.compare_digest(expected, digest_hex)
    except (TypeError, ValueError):
        return False


def _new_game_id(conn) -> str:
    while True:
        game_id = f"VMN-{secrets.token_hex(4).upper()}"
        if conn.execute("SELECT 1 FROM users WHERE game_id = ?", (game_id,)).fetchone() is None:
            return game_id


def _user_payload(row) -> dict:
    return {
        "game_id": row["game_id"],
        "email": row["email"],
        "player_name": row["player_name"],
        "email_verified": bool(row["email_verified"]) if "email_verified" in row.keys() else False,
    }


def _current_user():
    """Resolve an opaque bearer token without exposing password data."""
    header = request.headers.get("Authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    token = header[7:].strip()
    if not token:
        return None
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.game_id, u.email, u.player_name, u.email_verified
            FROM sessions s JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ? AND s.expires_at > ?
            """, (token_hash, now)
        ).fetchone()
    return row


@app.route("/auth/register", methods=["POST"])
def register():
    limited = _rate_limit("register")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    player_name = str(data.get("player_name", "Warrior")).strip()[:20] or "Warrior"
    if not _EMAIL_RE.match(email) or len(email) > 254:
        return jsonify({"error": "Enter a valid email address"}), 400
    if len(password) < 8 or len(password) > 128:
        return jsonify({"error": "Password must be 8 to 128 characters"}), 400

    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with get_db() as conn:
        try:
            game_id = _new_game_id(conn)
            _reg_sql = """
                INSERT INTO users (game_id, email, player_name, password_hash, email_verified)
                VALUES (?, ?, ?, ?, ?)
                """
            if _is_postgres():
                _reg_sql += " RETURNING id"
            cursor = conn.execute(
                _reg_sql, (game_id, email, player_name, _password_hash(password),
                      0 if REQUIRE_EMAIL_VERIFICATION else 1)
            )
            if _is_postgres():
                _urow = cursor.fetchone()
                user_id = (_urow[0] if isinstance(_urow, (tuple, list)) else _urow["id"]) if _urow else None
            else:
                user_id = cursor.lastrowid
            verification_token = _new_action_token(conn, user_id, "verify_email")
            conn.execute(
                "INSERT INTO profiles (user_id, profile_json) VALUES (?, ?)",
                (user_id, json.dumps(_default_profile(), separators=(",", ":"))),
            )
            session_token = None
            if not REQUIRE_EMAIL_VERIFICATION:
                session_token = token
            else:
                # A new account must verify its email before a session is issued.
                token = None
            if session_token:
                conn.execute(
                    "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
                    (token_hash, user_id, int(time.time()) + SESSION_TTL_SECONDS)
                )
            row = conn.execute(
                "SELECT game_id, email, player_name, email_verified FROM users WHERE id = ?", (user_id,)
            ).fetchone()
            conn.commit()
            if row:
                save_user_to_firebase({
                    "game_id": row["game_id"],
                    "email": row["email"],
                    "player_name": row["player_name"],
                    "email_verified": bool(row["email_verified"]),
                })
        except Exception as exc:
            if not _is_integrity_error(exc):
                raise
            if _is_postgres():
                conn.rollback()
            return jsonify({"error": "An account with that email already exists"}), 409
    response = {
        "success": True,
        "token": token,
        "verification_required": REQUIRE_EMAIL_VERIFICATION,
        "user": _user_payload(row),
    }
    if REQUIRE_EMAIL_VERIFICATION and SHOW_DEV_AUTH_TOKENS:
        response["verification_token"] = verification_token
    return jsonify(response), 201


@app.route("/auth/login", methods=["POST"])
def login():
    limited = _rate_limit("login")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, game_id, email, player_name, password_hash, email_verified FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        if row is None or not _password_matches(password, row["password_hash"]):
            return jsonify({"error": "Email or password is incorrect"}), 401
        if REQUIRE_EMAIL_VERIFICATION and not row["email_verified"]:
            return jsonify({
                "error": "Please verify your email before signing in",
                "verification_required": True,
            }), 403
        token = secrets.token_urlsafe(32)
        conn.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (hashlib.sha256(token.encode("utf-8")).hexdigest(), row["id"], int(time.time()) + SESSION_TTL_SECONDS)
        )
        conn.commit()
    return jsonify({"success": True, "token": token, "user": _user_payload(row)}), 200


@app.route("/auth/me", methods=["GET"])
def me():
    user = _current_user()
    if user is None:
        return jsonify({"error": "Authentication required"}), 401
    return jsonify({"user": _user_payload(user)})


@app.route("/auth/verify-email", methods=["POST"])
def verify_email():
    limited = _rate_limit("verify")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    raw_token = str(data.get("token", "")).strip()
    if not raw_token:
        return jsonify({"error": "Verification token is required"}), 400
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.game_id, u.email, u.player_name, u.email_verified
            FROM auth_tokens t JOIN users u ON u.id = t.user_id
            WHERE t.token_hash = ? AND t.purpose = 'verify_email'
              AND t.consumed_at IS NULL AND t.expires_at > ?
            """, (token_hash, now)
        ).fetchone()
        if row is None:
            return jsonify({"error": "Verification token is invalid or expired"}), 400
        conn.execute("UPDATE users SET email_verified = 1 WHERE id = ?", (row["id"],))
        conn.execute("UPDATE auth_tokens SET consumed_at = ? WHERE token_hash = ?", (now, token_hash))
        session_token = secrets.token_urlsafe(32)
        conn.execute(
            "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (hashlib.sha256(session_token.encode("utf-8")).hexdigest(), row["id"], now + SESSION_TTL_SECONDS),
        )
        conn.commit()
    return jsonify({"success": True, "token": session_token,
                    "user": {**_user_payload(row), "email_verified": True}})


@app.route("/auth/request-password-reset", methods=["POST"])
def request_password_reset():
    limited = _rate_limit("reset_request")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    response = {"success": True, "message": "If that email exists, reset instructions have been created."}
    with get_db() as conn:
        row = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if row is not None:
            reset_token = _new_action_token(conn, row["id"], "reset_password")
            conn.commit()
            if SHOW_DEV_AUTH_TOKENS:
                response["reset_token"] = reset_token
    return jsonify(response)


@app.route("/auth/reset-password", methods=["POST"])
def reset_password():
    limited = _rate_limit("reset_password")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    raw_token = str(data.get("token", "")).strip()
    password = str(data.get("password", ""))
    if len(password) < 8 or len(password) > 128:
        return jsonify({"error": "Password must be 8 to 128 characters"}), 400
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT user_id FROM auth_tokens
            WHERE token_hash = ? AND purpose = 'reset_password'
              AND consumed_at IS NULL AND expires_at > ?
            """, (token_hash, now)
        ).fetchone()
        if row is None:
            return jsonify({"error": "Reset token is invalid or expired"}), 400
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (_password_hash(password), row["user_id"]))
        conn.execute("DELETE FROM sessions WHERE user_id = ?", (row["user_id"],))
        conn.execute("UPDATE auth_tokens SET consumed_at = ? WHERE token_hash = ?", (now, token_hash))
        conn.commit()
    return jsonify({"success": True, "message": "Password updated. Please sign in again."})


@app.route("/auth/logout", methods=["POST"])
def logout():
    header = request.headers.get("Authorization", "")
    token = header[7:].strip() if header.lower().startswith("bearer ") else ""
    if token:
        with get_db() as conn:
            conn.execute(
                "DELETE FROM sessions WHERE token_hash = ?",
                (hashlib.sha256(token.encode("utf-8")).hexdigest(),)
            )
            conn.commit()
    return jsonify({"success": True})


def _require_user():
    user = _current_user()
    if user is None:
        return None, (jsonify({"error": "Authentication required"}), 401)
    return user, None


def _lobby_player(user, ship_class="pushpaka", ready=False, host=False):
    return {
        "game_id": user["game_id"],
        "player_name": user["player_name"],
        "ship_class": ship_class if ship_class in _SHIP_IDS else "pushpaka",
        "ready": bool(ready),
        "host": bool(host),
        # These are match rules/initial values for the future authoritative
        # duel server. HTTP lobby state is not trusted for combat results.
        "health": 100,
        "max_health": 100,
    }


def _cleanup_lobbies() -> None:
    cutoff = time.time() - 30 * 60
    expired = [code for code, lobby in _lobbies.items() if lobby["created_at"] < cutoff]
    for code in expired:
        _lobbies.pop(code, None)


@app.route("/multiplayer/lobbies", methods=["GET", "POST"])
def multiplayer_lobbies():
    if request.method == "GET":
        with _lobbies_lock:
            _cleanup_lobbies()
            return jsonify({"lobbies": [_lobby_payload(lobby) for lobby in _lobbies.values()]})

    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    mode = str(data.get("mode", "campaign")).lower()
    if mode not in ("campaign", "endless", "duel"):
        mode = "campaign"
    try:
        max_players = min(4, max(2, int(data.get("max_players", 2))))
    except (TypeError, ValueError):
        max_players = 2
    if mode == "duel":
        max_players = 2
    ship_class = str(data.get("ship_class", "pushpaka")).lower()
    code = _new_lobby_code()
    host = _lobby_player(user, ship_class, ready=False, host=True)
    lobby = {
        "code": code, "mode": mode, "max_players": max_players,
        "status": "waiting", "host_game_id": user["game_id"],
        "players": {user["game_id"]: host}, "created_at": time.time(),
        "rules": {
            "health": 100,
            "win_condition": "first pilot to reduce the opponent to 0 HP",
        } if mode == "duel" else {
            "health": 100,
            "win_condition": "complete the selected wave set",
        },
    }
    with _lobbies_lock:
        _lobbies[code] = lobby
    return jsonify({"lobby": _lobby_payload(lobby)}), 201


@app.route("/multiplayer/lobbies/<code>", methods=["GET"])
def get_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"error": "Lobby not found or expired"}), 404
        if user["game_id"] not in lobby["players"]:
            return jsonify({"error": "Join this lobby to view its private status"}), 403
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/join", methods=["POST"])
def join_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    ship_class = str(data.get("ship_class", "pushpaka")).lower()
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"error": "Lobby not found or expired"}), 404
        if lobby["status"] != "waiting":
            return jsonify({"error": "Lobby has already started"}), 409
        if user["game_id"] not in lobby["players"] and len(lobby["players"]) >= lobby["max_players"]:
            return jsonify({"error": "Lobby is full"}), 409
        lobby["players"][user["game_id"]] = _lobby_player(user, ship_class)
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/ready", methods=["POST"])
def ready_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None or user["game_id"] not in lobby["players"]:
            return jsonify({"error": "You are not in this lobby"}), 404
        player = lobby["players"][user["game_id"]]
        player["ready"] = bool(data.get("ready", not player["ready"]))
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/start", methods=["POST"])
def start_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"error": "Lobby not found or expired"}), 404
        if lobby["host_game_id"] != user["game_id"]:
            return jsonify({"error": "Only the lobby host can start the match"}), 403
        if len(lobby["players"]) < 2:
            return jsonify({"error": "At least two players are required"}), 409
        if not all(player["ready"] for player in lobby["players"].values()):
            return jsonify({"error": "Every player must be ready"}), 409
        lobby["status"] = "running"
        return jsonify({"lobby": _lobby_payload(lobby)})


@app.route("/multiplayer/lobbies/<code>/leave", methods=["POST"])
def leave_multiplayer_lobby(code):
    user, error = _require_user()
    if error:
        return error
    with _lobbies_lock:
        lobby = _lobbies.get(code.upper())
        if lobby is None:
            return jsonify({"success": True})
        lobby["players"].pop(user["game_id"], None)
        if not lobby["players"]:
            _lobbies.pop(code.upper(), None)
        elif lobby["host_game_id"] == user["game_id"]:
            new_host_id = next(iter(lobby["players"]))
            lobby["host_game_id"] = new_host_id
            for game_id, player in lobby["players"].items():
                player["host"] = game_id == new_host_id
        return jsonify({"success": True, "lobby": _lobby_payload(lobby) if lobby["players"] else None})


@app.route("/account/profile", methods=["GET"])
def get_profile():
    user, error = _require_user()
    if error:
        return error
    with get_db() as conn:
        row = conn.execute("SELECT profile_json, updated_at FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
    try:
        profile = json.loads(row["profile_json"]) if row else _default_profile()
    except (TypeError, ValueError):
        profile = _default_profile()
    return jsonify({"profile": profile, "updated_at": row["updated_at"] if row else None})


@app.route("/account/profile", methods=["PUT"])
def update_profile():
    user, error = _require_user()
    if error:
        return error
    data = request.get_json(silent=True) or {}
    incoming = _profile_from_payload(data.get("profile", data))
    if not incoming:
        return jsonify({"error": "A valid profile object is required"}), 400
    with get_db() as conn:
        row = conn.execute("SELECT profile_json FROM profiles WHERE user_id = ?", (user["id"],)).fetchone()
        try:
            current = json.loads(row["profile_json"]) if row else _default_profile()
        except (TypeError, ValueError):
            current = _default_profile()
        current.update(incoming)
        if "player_name" in current:
            current["player_name"] = str(current["player_name"]).strip()[:20] or "Warrior"
        encoded = json.dumps(current, separators=(",", ":"))
        if len(encoded) > 100_000:
            return jsonify({"error": "Profile is too large"}), 413
        conn.execute(
            """
            INSERT INTO profiles (user_id, profile_json, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET profile_json = excluded.profile_json,
                                               updated_at = CURRENT_TIMESTAMP
            """, (user["id"], encoded)
        )
        if current.get("player_name"):
            conn.execute("UPDATE users SET player_name = ? WHERE id = ?", (current["player_name"], user["id"]))
        conn.commit()
    return jsonify({"success": True, "profile": current})


@app.route("/account/stats", methods=["GET"])
def get_account_stats():
    user, error = _require_user()
    if error:
        return error
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT COUNT(*) AS games, COALESCE(MAX(score), 0) AS best_score,
                   COALESCE(SUM(score), 0) AS total_score,
                   COALESCE(MAX(level_reached), 0) AS best_wave,
                   COALESCE(SUM(kills), 0) AS total_kills,
                   COALESCE(SUM(total_damage), 0) AS total_damage
            FROM scores WHERE user_id = ?
            """, (user["id"],)
        ).fetchone()
        achievements = conn.execute(
            "SELECT profile_json FROM profiles WHERE user_id = ?", (user["id"],)
        ).fetchone()
    unlocked = 0
    if achievements:
        try:
            unlocked = len(json.loads(achievements["profile_json"]).get("achievements", []))
        except (TypeError, ValueError):
            unlocked = 0
    return jsonify({
        "game_id": user["game_id"], "games": row["games"],
        "best_score": row["best_score"], "total_score": row["total_score"],
        "best_wave": row["best_wave"], "total_kills": row["total_kills"],
        "total_damage": row["total_damage"], "achievements_unlocked": unlocked,
    })


@app.route("/scores", methods=["POST"])
def submit_score():
    limited = _rate_limit("score")
    if limited:
        return limited
    data = request.get_json(silent=True) or {}
    user = _current_user()
    player_name = str(data.get("player_name", "Anonymous")).strip()[:20] or "Anonymous"
    
    try:
        score = int(data.get("score", 0))
        level_reached = int(data.get("level_reached", 1))
        kills = int(data.get("kills", 0))
        total_damage = int(data.get("total_damage", 0))
        duration_seconds = float(data.get("duration_seconds", 0))
    except (ValueError, TypeError):
        logger.warning("Invalid score/level submission from %s: %s", request.remote_addr, data)
        return jsonify({"error": "Invalid score or level format"}), 400

    difficulty = str(data.get("difficulty", "normal")).lower()
    if difficulty not in ("easy", "normal", "hard", "endless"):
        difficulty = "normal"

    ship_class = str(data.get("ship_class", "pushpaka")).lower()
    if ship_class not in _SHIP_IDS:
        ship_class = "pushpaka"

    # These are deliberately generous sanity limits. They stop accidental or
    # obviously forged payloads while leaving room for future balance changes.
    max_wave = 10000 if difficulty == "endless" else 20
    max_score = max(250_000, level_reached * 250_000)
    if level_reached < 1 or level_reached > max_wave:
        return jsonify({"error": "Invalid wave value"}), 422
    if score < 0 or score > max_score or kills < 0 or kills > level_reached * 1000:
        logger.warning("Negative score rejected from %s: %s", request.remote_addr, score)
        return jsonify({"error": "Score failed sanity validation"}), 422
    if total_damage < 0 or duration_seconds < 0 or duration_seconds > 24 * 60 * 60:
        return jsonify({"error": "Run statistics failed sanity validation"}), 422

    with get_db() as conn:
        _insert_sql = """
                INSERT INTO scores (player_name, score, level_reached, difficulty, ship_class,
                                    user_id, game_id, kills, total_damage, duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        if _is_postgres():
            _insert_sql += " RETURNING id"
        cursor = conn.execute(
            _insert_sql,
            (
                user["player_name"] if user else player_name,
                score, level_reached, difficulty, ship_class,
                user["id"] if user else None,
                user["game_id"] if user else None,
                kills, total_damage, duration_seconds,
            )
        )
        # Fetch RETURNING row BEFORE commit (commit closes the cursor on SQLite)
        if _is_postgres():
            _srow = cursor.fetchone()
            inserted_id = (_srow[0] if isinstance(_srow, (tuple, list)) else _srow["id"]) if _srow else None
        else:
            inserted_id = cursor.lastrowid
        conn.commit()
        save_score_to_firebase({
            "player_name": user["player_name"] if user else player_name,
            "game_id": user["game_id"] if user else "",
            "score": score,
            "level_reached": level_reached,
            "difficulty": difficulty,
            "ship_class": ship_class,
            "kills": kills,
        })

    stored_name = user["player_name"] if user else player_name
    logger.info(
        "🏆 Score Recorded [ID=%s]: Warrior='%s' | Ship='%s' | Score=%s | Wave=%s | Diff='%s'",
        inserted_id, stored_name, ship_class.upper(), score, level_reached, difficulty.upper()
    )

    return jsonify({
        "success": True,
        "message": "Score recorded successfully",
        "id": inserted_id,
        "player_name": stored_name,
        "game_id": user["game_id"] if user else None,
        "ship_class": ship_class,
        "score": score,
        "level_reached": level_reached,
        "difficulty": difficulty,
        "kills": kills,
        "total_damage": total_damage,
        "duration_seconds": duration_seconds,
    }), 201


@app.route("/scores/top", methods=["GET"])
def get_top_scores():
    try:
        limit = min(max(1, int(request.args.get("limit", 10))), 50)
    except ValueError:
        limit = 10

    difficulty = request.args.get("difficulty")
    logger.info("Fetching leaderboard: limit=%s, difficulty=%s", limit, difficulty)

    with get_db() as conn:
        if difficulty and difficulty in ("easy", "normal", "hard", "endless"):
            rows = conn.execute(
                """
                SELECT id, player_name, score, level_reached, difficulty, ship_class, game_id, created_at
                FROM scores
                WHERE difficulty = ?
                ORDER BY score DESC, created_at ASC
                LIMIT ?
                """,
                (difficulty, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT id, player_name, score, level_reached, difficulty, ship_class, game_id, created_at
                FROM scores
                ORDER BY score DESC, created_at ASC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

    leaderboard = [
        {
            "rank": i + 1,
            "player_name": row["player_name"],
            "game_id": row["game_id"],
            "score": row["score"],
            "level_reached": row["level_reached"],
            "difficulty": row["difficulty"],
            "ship_class": row["ship_class"] or "pushpaka",
            "created_at": row["created_at"],
        }
        for i, row in enumerate(rows)
    ]

    return jsonify({
        "count": len(leaderboard),
        "leaderboard": leaderboard
    })


@app.route("/scores/stats", methods=["GET"])
def get_stats():
    with get_db() as conn:
        def _scalar(cur):
            r = cur.fetchone()
            if not r:
                return 0
            if isinstance(r, (tuple, list)):
                return r[0]
            if isinstance(r, dict):
                return next(iter(r.values()))
            try:
                return r[0]
            except Exception:
                return 0

        total_games = _scalar(conn.execute("SELECT COUNT(*) FROM scores")) or 0
        total_players = _scalar(conn.execute("SELECT COUNT(*) FROM users")) or 0
        max_score = _scalar(conn.execute("SELECT MAX(score) FROM scores")) or 0
        avg_score = _scalar(conn.execute("SELECT AVG(score) FROM scores")) or 0

    logger.info("Global stats queried: total_games=%s, max_score=%s", total_games, max_score)
    return jsonify({
        "total_games_submitted": total_games,
        "highest_score": max_score,
        "average_score": round(float(avg_score), 1),
        "registered_players": total_players,
    })

_duel_state = {}
_sid_to_player = {}

@socketio.on("join_duel")
def handle_join_duel(data):
    token = data.get("token")
    room_code = data.get("room_code")
    game_id = data.get("game_id")
    ship_class = data.get("ship_class", "pushpaka")

    if not token or not room_code or not game_id:
        emit("error", {"message": "Invalid join data"})
        return

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    now = int(time.time())
    with get_db() as conn:
        row = conn.execute(
            """
            SELECT u.id, u.game_id
            FROM sessions s JOIN users u ON u.id = s.user_id
            WHERE s.token_hash = ? AND s.expires_at > ?
            """, (token_hash, now)
        ).fetchone()

    if not row or row["game_id"] != game_id:
        emit("error", {"message": "Unauthorized"})
        return

    join_room(room_code)
    _sid_to_player[request.sid] = {"room_code": room_code, "game_id": game_id}

    if room_code not in _duel_state:
        _duel_state[room_code] = {}

    _duel_state[room_code][game_id] = {
        "game_id": game_id,
        "hp": 100,
        "max_hp": 100
    }

    emit("player_joined", {"game_id": game_id, "ship_class": ship_class}, to=room_code)


@socketio.on("player_input")
def handle_player_input(data):
    player = _sid_to_player.get(request.sid)
    if not player:
        return
    emit("opponent_state", data, to=player["room_code"], include_self=False)


@socketio.on("hit_registered")
def handle_hit_registered(data):
    player = _sid_to_player.get(request.sid)
    if not player:
        return

    room_code = player["room_code"]
    target_id = data.get("target_game_id")
    damage = min(50, max(0, int(data.get("damage", 0))))

    room_state = _duel_state.get(room_code)
    if not room_state or target_id not in room_state:
        return

    target = room_state[target_id]
    target["hp"] = max(0, target["hp"] - damage)

    players_list = [{"game_id": k, "hp": v["hp"], "max_hp": v["max_hp"]} for k, v in room_state.items()]
    emit("hp_update", {"players": players_list}, to=room_code)

    if target["hp"] == 0:
        emit("duel_end", {"winner_game_id": player["game_id"]}, to=room_code)


@socketio.on("disconnect")
def handle_disconnect():
    player = _sid_to_player.pop(request.sid, None)
    if player:
        room_code = player["room_code"]
        game_id = player["game_id"]
        emit("player_left", {"game_id": game_id}, to=room_code)
        
        room_state = _duel_state.get(room_code)
        if room_state and game_id in room_state:
            del room_state[game_id]
            if not room_state:
                del _duel_state[room_code]


@socketio.on("duel_ping")
def handle_duel_ping(data):
    emit("duel_pong", data)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Vimana Wars Leaderboard Server on port {port}...")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)


# ==============================================================================
# [74/77] MODULE: backend/firebase_service.py
# ==============================================================================
"""
backend/firebase_service.py
Google Service Account (GSA) & Firebase Admin Integration for Vimana Wars.

Supports:
- Firebase Firestore NoSQL Database for Users, Leaderboards, Match History, and Cloud Saves.
- Authenticates using Google Service Account (GSA) credentials:
  1. File path: `serviceAccountKey.json` in backend/ or repository root.
  2. Environment variable: `GOOGLE_APPLICATION_CREDENTIALS` path.
  3. Environment variable: `FIREBASE_SERVICE_ACCOUNT_JSON` containing inline JSON string.
- Dual-mode architecture: seamlessly synchronizes when GSA is present,
  gracefully operates in local mode when awaiting GSA key.
"""
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger("vimana.firebase")

_firebase_app = None
_firestore_db = None
_initialized = False
_init_error: Optional[str] = None


def get_gsa_credential_path() -> Optional[Path]:
    """Locate Google Service Account key file if present."""
    # 1. Check standard Google env var
    env_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    # 2. Check local backend directory
    backend_dir = Path(__file__).resolve().parent
    candidates = [
        backend_dir / "serviceAccountKey.json",
        backend_dir / "firebase-service-account.json",
        backend_dir / "gsa_key.json",
        backend_dir.parent / "serviceAccountKey.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    return None


def init_firebase() -> bool:
    """Initialize Firebase Admin SDK using Google Service Account (GSA)."""
    global _firebase_app, _firestore_db, _initialized, _init_error

    if _initialized:
        return _firestore_db is not None

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError:
        _init_error = "firebase-admin library not installed. Run: pip install firebase-admin"
        logger.info(_init_error)
        _initialized = True
        return False

    try:
        # Check for inline JSON credentials in environment variable
        raw_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")
        cred = None

        if raw_json:
            try:
                cert_dict = json.loads(raw_json)
                cred = credentials.Certificate(cert_dict)
                logger.info("Loaded GSA credentials from FIREBASE_SERVICE_ACCOUNT_JSON")
            except Exception as e:
                logger.warning("Failed to parse FIREBASE_SERVICE_ACCOUNT_JSON: %s", e)

        if cred is None:
            key_path = get_gsa_credential_path()
            if key_path:
                cred = credentials.Certificate(str(key_path))
                logger.info("Loaded GSA credentials from file: %s", key_path)

        if cred is None:
            _init_error = (
                "Google Service Account (GSA) key not found. "
                "Place serviceAccountKey.json in backend/ or set GOOGLE_APPLICATION_CREDENTIALS."
            )
            logger.info("Firebase: %s (operating in SQLite/Postgres mode)", _init_error)
            _initialized = True
            return False

        if not firebase_admin._apps:
            _firebase_app = firebase_admin.initialize_app(cred)
        else:
            _firebase_app = firebase_admin.get_app()

        _firestore_db = firestore.client()
        _initialized = True
        logger.info("Firebase Firestore connected successfully via Google Service Account!")
        return True

    except Exception as exc:
        _init_error = f"Firebase initialization failed: {exc}"
        logger.warning(_init_error)
        _initialized = True
        return False


def is_firebase_active() -> bool:
    """Check if Firebase Firestore is active and ready."""
    if not _initialized:
        init_firebase()
    return _firestore_db is not None


def get_firebase_status() -> Dict[str, Any]:
    """Return current Firebase GSA connection status for system health reports."""
    if not _initialized:
        init_firebase()
    return {
        "active": _firestore_db is not None,
        "gsa_key_detected": get_gsa_credential_path() is not None or bool(os.getenv("FIREBASE_SERVICE_ACCOUNT_JSON")),
        "error": _init_error,
    }


# ── Firestore Synchronization Operations ──────────────────────────────────────

def save_user_to_firebase(user_dict: Dict[str, Any]) -> bool:
    """Save or update user record in Firestore 'users' collection."""
    if not is_firebase_active():
        return False
    try:
        from google.cloud import firestore as gc_firestore
        game_id = user_dict.get("game_id")
        if not game_id:
            return False
        doc_ref = _firestore_db.collection("users").document(game_id)
        payload = {
            "game_id": game_id,
            "email": user_dict.get("email", ""),
            "player_name": user_dict.get("player_name", "Warrior"),
            "email_verified": bool(user_dict.get("email_verified", False)),
            "updated_at": gc_firestore.SERVER_TIMESTAMP,
        }
        doc_ref.set(payload, merge=True)
        return True
    except Exception as exc:
        logger.error("Error saving user to Firestore: %s", exc)
        return False


def save_score_to_firebase(score_dict: Dict[str, Any]) -> bool:
    """Record high score entry in Firestore 'leaderboard' collection."""
    if not is_firebase_active():
        return False
    try:
        from google.cloud import firestore as gc_firestore
        doc_ref = _firestore_db.collection("leaderboard").document()
        payload = {
            "player_name": score_dict.get("player_name", "Warrior"),
            "game_id": score_dict.get("game_id", ""),
            "score": int(score_dict.get("score", 0)),
            "wave": int(score_dict.get("level_reached", score_dict.get("wave", 1))),
            "difficulty": str(score_dict.get("difficulty", "normal")).lower(),
            "ship_class": str(score_dict.get("ship_class", "pushpaka")),
            "kills": int(score_dict.get("kills", 0)),
            "created_at": gc_firestore.SERVER_TIMESTAMP,
        }
        doc_ref.set(payload)
        return True
    except Exception as exc:
        logger.error("Error saving score to Firestore: %s", exc)
        return False


def get_firebase_leaderboard(limit: int = 50) -> List[Dict[str, Any]]:
    """Query top scores from Firestore."""
    if not is_firebase_active():
        return []
    try:
        from google.cloud import firestore as gc_firestore
        scores_ref = (
            _firestore_db.collection("leaderboard")
            .order_by("score", direction=gc_firestore.Query.DESCENDING)
            .limit(limit)
        )
        results = []
        for rank, doc in enumerate(scores_ref.stream(), 1):
            data = doc.to_dict()
            results.append({
                "rank": rank,
                "player_name": data.get("player_name", "Warrior"),
                "game_id": data.get("game_id", ""),
                "score": data.get("score", 0),
                "wave": data.get("wave", 1),
                "difficulty": data.get("difficulty", "normal"),
                "ship_class": data.get("ship_class", "pushpaka"),
            })
        return results
    except Exception as exc:
        logger.error("Error fetching Firestore leaderboard: %s", exc)
        return []


def save_cloud_save_to_firebase(game_id: str, save_data: Dict[str, Any]) -> bool:
    """Save persistent player progression to Firestore 'cloud_saves' collection."""
    if not is_firebase_active():
        return False
    try:
        from google.cloud import firestore as gc_firestore
        doc_ref = _firestore_db.collection("cloud_saves").document(game_id)
        payload = {
            "game_id": game_id,
            "save_data": save_data,
            "updated_at": gc_firestore.SERVER_TIMESTAMP,
        }
        doc_ref.set(payload, merge=True)
        return True
    except Exception as exc:
        logger.error("Error saving cloud save to Firestore: %s", exc)
        return False


def get_cloud_save_from_firebase(game_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve player cloud save from Firestore."""
    if not is_firebase_active():
        return None
    try:
        doc = _firestore_db.collection("cloud_saves").document(game_id).get()
        if doc.exists:
            data = doc.to_dict()
            return data.get("save_data")
        return None
    except Exception as exc:
        logger.error("Error retrieving cloud save from Firestore: %s", exc)
        return None



# ==============================================================================
# [75/77] MODULE: tests/test_backend.py
# ==============================================================================
"""
tests/test_backend.py
Unit tests for the Flask Leaderboard REST API.
"""
import pytest
from backend.app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_leaderboard.db"
    monkeypatch.setattr("backend.app.DB_PATH", db_file)
    from backend import app as backend_app
    backend_app._rate_state.clear()
    backend_app._lobbies.clear()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client


def test_index_route(client):
    res = client.get("/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "online"


def test_submit_and_get_scores(client):
    payload = {
        "player_name": "Arjuna",
        "score": 50000,
        "level_reached": 10,
        "difficulty": "hard",
        "ship_class": "garuda",
    }
    res = client.post("/scores", json=payload)
    assert res.status_code == 201
    res_data = res.get_json()
    assert res_data["success"] is True
    assert res_data["ship_class"] == "garuda"

    # Retrieve top scores
    res_top = client.get("/scores/top")
    assert res_top.status_code == 200
    top_data = res_top.get_json()
    assert top_data["count"] == 1
    assert top_data["leaderboard"][0]["player_name"] == "Arjuna"
    assert top_data["leaderboard"][0]["score"] == 50000
    assert top_data["leaderboard"][0]["ship_class"] == "garuda"


def test_stats_route(client):
    client.post("/scores", json={"player_name": "Hero", "score": 10000, "level_reached": 5, "difficulty": "normal"})
    res = client.get("/scores/stats")
    assert res.status_code == 200
    stats = res.get_json()
    assert stats["total_games_submitted"] == 1
    assert stats["highest_score"] == 10000


def test_account_lifecycle_and_authenticated_score(client):
    register = client.post("/auth/register", json={
        "email": "arjuna@example.com",
        "password": "celestial123",
        "player_name": "Arjuna",
    })
    assert register.status_code == 201
    account = register.get_json()
    assert account["success"] is True
    assert account["user"]["game_id"].startswith("VMN-")
    token = account["token"]

    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.get_json()["user"]["game_id"] == account["user"]["game_id"]

    duplicate = client.post("/auth/register", json={
        "email": "ARJUNA@example.com",
        "password": "another123",
        "player_name": "Other",
    })
    assert duplicate.status_code == 409

    bad_login = client.post("/auth/login", json={
        "email": "arjuna@example.com", "password": "wrongpass"
    })
    assert bad_login.status_code == 401

    score = client.post("/scores", headers={"Authorization": f"Bearer {token}"}, json={
        "player_name": "Spoofed Name",
        "score": 777,
        "level_reached": 4,
        "difficulty": "normal",
        "ship_class": "garuda",
    })
    assert score.status_code == 201
    assert score.get_json()["player_name"] == "Arjuna"
    assert score.get_json()["game_id"] == account["user"]["game_id"]

    top = client.get("/scores/top").get_json()["leaderboard"][0]
    assert top["game_id"] == account["user"]["game_id"]

    logout = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout.status_code == 200
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_cloud_profile_and_personal_stats(client):
    register = client.post("/auth/register", json={
        "email": "profile@example.com",
        "password": "celestial123",
        "player_name": "Profile Hero",
    }).get_json()
    headers = {"Authorization": f"Bearer {register['token']}"}

    profile = client.put("/account/profile", headers=headers, json={
        "profile": {
            "player_name": "Profile Hero",
            "achievements": ["first_blood", "high_scorer"],
            "last_wave": 12,
            "unknown_secret": "must not be stored",
        }
    })
    assert profile.status_code == 200
    assert "unknown_secret" not in profile.get_json()["profile"]

    client.post("/scores", headers=headers, json={
        "score": 1200, "level_reached": 4, "difficulty": "normal",
        "kills": 6, "total_damage": 900,
    })
    stats = client.get("/account/stats", headers=headers)
    assert stats.status_code == 200
    assert stats.get_json()["games"] == 1
    assert stats.get_json()["best_score"] == 1200
    assert stats.get_json()["total_kills"] == 6
    assert stats.get_json()["achievements_unlocked"] == 2


def test_password_reset_token_flow(client, monkeypatch):
    monkeypatch.setattr("backend.app.SHOW_DEV_AUTH_TOKENS", True)
    client.post("/auth/register", json={
        "email": "reset@example.com",
        "password": "oldpassword",
        "player_name": "Reset Hero",
    })
    request_reset = client.post("/auth/request-password-reset", json={
        "email": "reset@example.com",
    })
    assert request_reset.status_code == 200
    reset_token = request_reset.get_json()["reset_token"]

    reset = client.post("/auth/reset-password", json={
        "token": reset_token, "password": "newpassword",
    })
    assert reset.status_code == 200
    assert client.post("/auth/login", json={
        "email": "reset@example.com", "password": "oldpassword",
    }).status_code == 401
    assert client.post("/auth/login", json={
        "email": "reset@example.com", "password": "newpassword",
    }).status_code == 200


def test_required_email_verification_flow(client, monkeypatch):
    monkeypatch.setattr("backend.app.REQUIRE_EMAIL_VERIFICATION", True)
    monkeypatch.setattr("backend.app.SHOW_DEV_AUTH_TOKENS", True)
    register = client.post("/auth/register", json={
        "email": "verify@example.com",
        "password": "celestial123",
        "player_name": "Verified Hero",
    })
    assert register.status_code == 201
    body = register.get_json()
    assert body["verification_required"] is True
    assert "token" not in body or body["token"] is None
    assert client.post("/auth/login", json={
        "email": "verify@example.com", "password": "celestial123",
    }).status_code == 403

    verified = client.post("/auth/verify-email", json={"token": body["verification_token"]})
    assert verified.status_code == 200
    assert client.post("/auth/login", json={
        "email": "verify@example.com", "password": "celestial123",
    }).status_code == 200


def test_score_sanity_validation(client):
    negative = client.post("/scores", json={
        "score": -1, "level_reached": 1,
    })
    assert negative.status_code == 422

    impossible_wave = client.post("/scores", json={
        "score": 100, "level_reached": 21, "difficulty": "normal",
    })
    assert impossible_wave.status_code == 422

    impossible_stats = client.post("/scores", json={
        "score": 100, "level_reached": 1, "kills": -2,
    })
    assert impossible_stats.status_code == 422


def test_multiplayer_lobby_lifecycle(client):
    first = client.post("/auth/register", json={
        "email": "host@example.com", "password": "celestial123", "player_name": "Host"
    }).get_json()
    second = client.post("/auth/register", json={
        "email": "guest@example.com", "password": "celestial123", "player_name": "Wingman"
    }).get_json()
    host_headers = {"Authorization": f"Bearer {first['token']}"}
    guest_headers = {"Authorization": f"Bearer {second['token']}"}

    created = client.post("/multiplayer/lobbies", headers=host_headers, json={
        "mode": "campaign", "max_players": 2, "ship_class": "garuda"
    })
    assert created.status_code == 201
    lobby = created.get_json()["lobby"]
    code = lobby["code"]
    assert len(lobby["players"]) == 1

    joined = client.post(f"/multiplayer/lobbies/{code}/join", headers=guest_headers, json={
        "ship_class": "vajra"
    })
    assert joined.status_code == 200
    assert len(joined.get_json()["lobby"]["players"]) == 2

    assert client.post(f"/multiplayer/lobbies/{code}/ready", headers=host_headers,
                       json={"ready": True}).status_code == 200
    assert client.post(f"/multiplayer/lobbies/{code}/ready", headers=guest_headers,
                       json={"ready": True}).status_code == 200
    started = client.post(f"/multiplayer/lobbies/{code}/start", headers=host_headers)
    assert started.status_code == 200
    assert started.get_json()["lobby"]["status"] == "running"


def test_duel_lobby_has_two_slots_and_health_rules(client):
    account = client.post("/auth/register", json={
        "email": "duelist@example.com", "password": "celestial123", "player_name": "Duelist"
    }).get_json()
    headers = {"Authorization": f"Bearer {account['token']}"}

    response = client.post("/multiplayer/lobbies", headers=headers, json={
        "mode": "duel", "max_players": 4, "ship_class": "surya"
    })
    assert response.status_code == 201
    lobby = response.get_json()["lobby"]
    assert lobby["mode"] == "duel"
    assert lobby["max_players"] == 2
    assert lobby["rules"]["health"] == 100
    assert lobby["players"][0]["health"] == 100


# ==============================================================================
# [76/77] MODULE: tests/test_entities.py
# ==============================================================================
"""
tests/test_entities.py
Unit tests for all game entities.
"""
from constants import (
    WIDTH, HEIGHT,
    PLAYER_MAX_HP,
    PLAYER_BULLET_DAMAGE,
    ASURA_FAST_HP,
    ASURA_TANK_HP,
    ASURA_RANGED_HP,
    ASURA_KAMIKAZE_HP,
    KUMBHAKARNA_HP,
    RAVANA_HP,
)
from game.entities.player import Player
from game.entities.bullet import PlayerBullet, EnemyBullet
from game.entities.chakram import Chakram
from game.entities.powerup import PowerUp, PowerUpType, PowerUpEffect
from game.entities.ship_classes import SHIP_CLASSES
from game.entities.enemies.asura_fast import AsuraFast
from game.entities.enemies.asura_tank import AsuraTank
from game.entities.enemies.asura_ranged import AsuraRanged
from game.entities.enemies.asura_kamikaze import AsuraKamikaze
from game.entities.enemies.asura_healer import AsuraHealer
from game.entities.enemies.asura_sniper import AsuraSniper
from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
from game.entities.enemies.boss_ravana import BossRavana


class TestPlayer:
    def test_player_init(self):
        p = Player()
        assert p.hp == PLAYER_MAX_HP
        assert p.alive is True
        assert p.x == WIDTH / 2
        assert p.y == HEIGHT / 2
        assert p.dash_charges >= 1

    def test_player_take_damage(self):
        p = Player()
        initial_hp = p.hp
        hit = p.take_damage(20)
        assert hit is True
        assert p.hp == initial_hp - 20

    def test_player_heal(self):
        p = Player()
        p.take_damage(40)
        p.heal(25)
        assert p.hp == PLAYER_MAX_HP - 15
        p.heal(100)
        assert p.hp == p.max_hp

    def test_player_shield_powerup(self):
        p = Player()
        p.apply_powerup(PowerUpType.SHIELD)
        assert p.shield_hits > 0
        initial_hp = p.hp
        hit = p.take_damage(30)
        assert hit is False  # absorbed by shield
        assert p.hp == initial_hp

    def test_player_dash(self):
        p = Player()
        assert p.dash_ready is True
        dashed = p.trigger_dash()
        assert dashed is True
        assert p.is_dashing is True

    def test_ship_classes(self):
        for sid, sdata in SHIP_CLASSES.items():
            p = Player()
            p.apply_ship_class(sdata)
            assert p.max_hp == sdata["hp"]
            assert p.hp == sdata["hp"]
            assert p.fire_rate_stat == sdata["fire_rate"]
            if sid == "garuda":
                assert p.dash_charges_max == 2


class TestBulletsAndAbilities:
    def test_player_bullet(self):
        b = PlayerBullet(100, 100, 90)
        assert b.damage == PLAYER_BULLET_DAMAGE
        assert b.alive is True
        b.update(0.016)
        assert b.y > 100

    def test_enemy_bullet(self):
        eb = EnemyBullet(200, 200, 0)
        assert eb.alive is True
        eb.update(0.016)
        assert eb.x > 200

    def test_chakram(self):
        chk = Chakram(300, 300, 45)
        assert chk.alive is True
        chk.update(0.016, 300, 300)
        assert chk.alive is True


class TestPowerups:
    def test_powerup_creation(self):
        for ptype in PowerUpType:
            pu = PowerUp(ptype)
            assert pu.type == ptype
            assert pu.alive is True

    def test_powerup_effect_expiration(self):
        eff = PowerUpEffect(PowerUpType.SPEED)
        assert eff.expired is False
        eff.update(eff.duration + 1.0)
        assert eff.expired is True


class TestEnemies:
    def test_asura_fast(self):
        e = AsuraFast()
        assert e.hp == ASURA_FAST_HP
        assert e.alive is True
        e.update(0.016, 100, 100)

    def test_asura_tank(self):
        e = AsuraTank()
        assert e.hp == ASURA_TANK_HP
        assert e.alive is True

    def test_asura_ranged(self):
        e = AsuraRanged()
        assert e.hp == ASURA_RANGED_HP
        bullets = e.update(0.016, 100, 100)
        assert isinstance(bullets, list)

    def test_asura_kamikaze(self):
        e = AsuraKamikaze()
        assert e.hp == ASURA_KAMIKAZE_HP
        e.explode()
        assert e.exploded is True
        assert e.is_dead() is True

    def test_asura_healer(self):
        e = AsuraHealer()
        assert e.alive is True
        ally = AsuraFast()
        ally.x = e.x + 50
        ally.y = e.y + 50
        ally.hp = 10
        e._heal_timer = 0.0
        healed = e.perform_heal_pulse([ally])
        assert healed is True
        assert ally.hp > 10

    def test_asura_sniper(self):
        e = AsuraSniper()
        assert e.alive is True

    def test_boss_kumbhakarna(self):
        boss = BossKumbhakarna()
        assert boss.hp == KUMBHAKARNA_HP
        assert boss.alive is True

    def test_boss_ravana(self):
        boss = BossRavana()
        assert boss.hp == RAVANA_HP
        assert boss.phase == 1
        boss.take_damage(int(RAVANA_HP * 0.4))
        boss._update_phase()
        assert boss.phase == 2

    def test_boss_ravana_summons(self):
        boss = BossRavana()
        # Trigger fleet summon in phase 3
        boss._entered = True
        boss.hp = int(RAVANA_HP * 0.2)
        boss._update_phase()
        assert boss.phase == 3
        boss._summon_timer = 0.0
        boss.update(0.1, 450, 300)
        # Summons should be produced and cleanly read
        summons = boss.pending_summons
        assert len(summons) >= 2
        # Second read should be empty
        assert len(boss.pending_summons) == 0

    def test_ship_class_dash_charges_reset(self):
        p = Player()
        p.apply_ship_class(SHIP_CLASSES["garuda"])
        assert p.dash_charges_max == 2
        # Switch to pushpaka
        p.apply_ship_class(SHIP_CLASSES["pushpaka"])
        assert p.dash_charges_max == 1
        assert p.dash_charges == 1


# ==============================================================================
# [77/77] MODULE: tests/test_systems.py
# ==============================================================================
"""
tests/test_systems.py
Unit tests for all core gameplay systems.
"""
from game.entities.player import Player
from game.entities.bullet import PlayerBullet
from game.entities.powerup import PowerUp, PowerUpType
from game.entities.enemies.asura_fast import AsuraFast
from game.systems.score_system import ScoreSystem
from game.systems.boon_system import BoonManager
from game.systems.wave_manager import WaveManager
from game.systems.floating_text import FloatingTextManager
from game.systems.particles import ParticleManager
from game.systems.achievement_system import AchievementManager
from game.systems import collision as collision_sys
from game.systems import save_system
from constants import WIDTH, HEIGHT


class TestScoreSystem:
    def test_score_and_combo(self):
        ss = ScoreSystem()
        assert ss.score == 0
        assert ss.combo == 1
        ss.register_kill(100)
        assert ss.score == 100
        assert ss.combo == 1
        ss.register_kill(100)
        assert ss.score == 100 + 100 * 2
        assert ss.combo == 2

    def test_combo_decay(self):
        ss = ScoreSystem()
        ss.register_kill(100)
        ss.register_kill(100)
        assert ss.combo_active is True
        ss.update(ss.combo_timeout + 1.0)
        assert ss.combo == 1
        assert ss.combo_active is False


class TestBoonSystem:
    def test_boon_manager(self):
        bm = BoonManager()
        assert bm.has_boon("agni_fury") is False
        bm.add_boon("agni_fury")
        assert bm.has_boon("agni_fury") is True
        assert bm.get_boon_level("agni_fury") == 1
        bm.add_boon("agni_fury")
        assert bm.get_boon_level("agni_fury") == 2

    def test_get_random_choices(self):
        bm = BoonManager()
        choices = bm.get_random_choices(3)
        assert len(choices) <= 3
        # Max out one boon
        for _ in range(3):
            bm.add_boon("agni_fury")
        choices2 = bm.get_random_choices(8)
        assert not any(c["id"] == "agni_fury" for c in choices2)


class TestWaveManager:
    def test_wave_manager_progression(self):
        wm = WaveManager()
        assert wm.wave_number == 0
        enemies = []
        powerups = []
        player = Player()
        # Progress from initial clear pause to countdown
        wm.update(3.5, enemies, powerups, player)
        assert wm.is_announcing is True
        # Progress through countdown to spawning
        wm.update(2.5, enemies, powerups, player)
        assert wm._state == "SPAWNING"
        # Tick to spawn wave and enter fighting
        wm.update(0.016, enemies, powerups, player)
        assert wm.is_fighting is True
        assert len(enemies) > 0

    def test_extended_campaign_boss_schedule(self):
        from game.systems.wave_manager import _wave_config
        from constants import get_realm_for_wave
        assert _wave_config(10)["boss"] == "ravana"
        assert _wave_config(15)["mini_boss"] == "mahishasura"
        assert _wave_config(20)["boss"] == "vritra"
        assert get_realm_for_wave(13)["name"] == "Setu Expanse"
        assert get_realm_for_wave(20)["name"] == "Mahayuddha Citadel"

    def test_extended_boss_entities_have_unique_identity(self):
        from game.entities.enemies.boss_mahishasura import BossMahishasura
        from game.entities.enemies.boss_vritra import BossVritra
        assert BossMahishasura().boss_id == "mahishasura"
        assert BossVritra().boss_id == "vritra"

    def test_extended_boss_schedule_spawns_expected_entities(self):
        from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
        from game.entities.enemies.boss_ravana import BossRavana
        from game.entities.enemies.boss_mahishasura import BossMahishasura
        from game.entities.enemies.boss_vritra import BossVritra
        expected = ((5, BossKumbhakarna), (10, BossRavana),
                    (15, BossMahishasura), (20, BossVritra))
        for wave, boss_type in expected:
            wm = WaveManager(start_wave=wave)
            wm._advance_wave()
            enemies = []
            wm._spawn_wave(enemies, Player())
            assert any(isinstance(enemy, boss_type) for enemy in enemies)


class TestCollisionSystem:
    def test_bullet_enemy_collision(self):
        p = Player()
        enemy = AsuraFast()
        enemy.x = 200
        enemy.y = 200
        bullet = PlayerBullet(200, 200, 0)
        bullets = [bullet]
        enemies = [enemy]
        ss = ScoreSystem()
        bm = BoonManager()

        summary = collision_sys.check_all(p, enemies, bullets, [], [], ss, bm)
        assert len(summary["hit_sparks"]) > 0
        assert enemy.hp < enemy.max_hp

    def test_player_powerup_collision(self):
        p = Player()
        pu = PowerUp(PowerUpType.HEALTH)
        pu.x = p.x
        pu.y = p.y
        powerups = [pu]
        ss = ScoreSystem()
        bm = BoonManager()

        summary = collision_sys.check_all(p, [], [], [], powerups, ss, bm)
        assert PowerUpType.HEALTH in summary["powerup_picked"]
        assert pu.alive is False


class TestParticlesAndFloatingTexts:
    def test_floating_texts(self):
        ft = FloatingTextManager()
        ft.spawn_damage(100, 100, 25)
        ft.spawn_damage(100, 100, 50, is_crit=True)
        ft.spawn_damage(100, 100, 15, color=(255, 120, 30))
        ft.spawn_combo(100, 100, 5)
        ft.spawn_notification(100, 100, "TEST")
        assert len(ft.numbers) == 5
        ft.update(0.016)

    def test_particles(self):
        pm = ParticleManager()
        pm.spawn_hit_sparks(100, 100)
        pm.spawn_explosion(100, 100)
        pm.spawn_dash_flash(100, 100)
        pm.spawn_dash_shockwave(100, 100)
        assert len(pm.particles) > 0
        pm.update(0.016)


class TestAchievementsAndSave:
    def test_achievement_system(self, tmp_path, monkeypatch):
        test_file = tmp_path / "save.json"
        monkeypatch.setattr(save_system, "_SAVE_FILE", test_file)
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)

        am = AchievementManager()
        unlocked = am.check_unlock("first_blood")
        assert unlocked is True
        # Second time should not unlock again
        unlocked_again = am.check_unlock("first_blood")
        assert unlocked_again is False

    def test_save_system_roundtrip(self, tmp_path, monkeypatch):
        test_file = tmp_path / "save.json"
        monkeypatch.setattr(save_system, "_SAVE_FILE", test_file)
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)

        data = save_system.load()
        data["high_score"] = 12345
        data["sfx_volume"] = 60
        data["music_volume"] = 40
        save_system.save(data)

        loaded = save_system.load()
        assert loaded["high_score"] == 12345
        assert loaded["sfx_volume"] == 60
        assert loaded["music_volume"] == 40


class TestEasingSystem:
    def test_ease_out_cubic_bounds(self):
        from game.ui.easing import ease_out_cubic, clamp, lerp, lerp_color
        assert ease_out_cubic(0.0) == 0.0
        assert ease_out_cubic(1.0) == 1.0
        assert 0.0 < ease_out_cubic(0.5) < 1.0
        # Should be past midpoint (easing out is fast then slow)
        assert ease_out_cubic(0.5) > 0.5

    def test_lerp(self):
        from game.ui.easing import lerp
        assert lerp(0, 100, 0.0) == 0
        assert lerp(0, 100, 1.0) == 100
        assert lerp(0, 100, 0.5) == 50

    def test_lerp_color(self):
        from game.ui.easing import lerp_color
        c = lerp_color((0, 0, 0), (255, 255, 255), 0.5)
        assert c == (127, 127, 127)

    def test_clamp(self):
        from game.ui.easing import clamp
        assert clamp(-0.5) == 0.0
        assert clamp(1.5) == 1.0
        assert clamp(0.5) == 0.5

    def test_ease_out_elastic(self):
        from game.ui.easing import ease_out_elastic
        assert ease_out_elastic(0.0) == 0.0
        assert ease_out_elastic(1.0) == 1.0
        # Elastic can overshoot > 1.0 briefly
        assert ease_out_elastic(0.5) > 0.5


class TestTweenSystem:
    def test_tween_basic(self):
        from game.ui.tween import Tween, TweenManager

        class Target:
            value = 0.0

        t = Target()
        tw = Tween(t, "value", end=100.0, duration=1.0)
        tw.update(0.5)
        assert 0 < t.value < 100
        tw.update(0.6)
        assert t.value == 100.0
        assert tw.done

    def test_tween_manager(self):
        from game.ui.tween import TweenManager

        class Target:
            x = 0.0
            y = 0.0

        t = Target()
        tm = TweenManager()
        tm.tween(t, "x", 50.0, 0.5)
        tm.tween(t, "y", 100.0, 1.0)
        assert tm.active
        tm.update(0.6)
        assert t.x == 50.0  # completed
        assert 0 < t.y < 100  # still running
        tm.update(0.5)
        assert t.y == 100.0
        assert not tm.active

    def test_tween_with_delay(self):
        from game.ui.tween import Tween

        class Target:
            value = 0.0

        t = Target()
        tw = Tween(t, "value", end=10.0, duration=0.5, delay=0.3)
        tw.update(0.2)
        assert t.value == 0.0  # still in delay
        tw.update(0.2)  # delay ends, 0.1s into tween
        assert t.value > 0.0
        tw.update(0.5)
        assert t.value == 10.0

    def test_tween_callback(self):
        from game.ui.tween import Tween

        class Target:
            value = 0.0

        t = Target()
        callback_called = []
        tw = Tween(t, "value", end=5.0, duration=0.1, on_done=lambda: callback_called.append(True))
        tw.update(0.2)
        assert len(callback_called) == 1


class TestSynergySystem:
    def test_synergy_unlock(self):
        from game.systems.boon_system import BoonManager
        bm = BoonManager()
        # Add first half of plasma_storm pair
        result1 = bm.add_boon("agni_fury")
        assert len(result1) == 0  # no synergy yet

        # Add second half
        result2 = bm.add_boon("indra_thunder")
        assert len(result2) == 1
        assert result2[0]["id"] == "plasma_storm"
        assert bm.has_synergy("plasma_storm")

    def test_no_duplicate_synergy(self):
        from game.systems.boon_system import BoonManager
        bm = BoonManager()
        bm.add_boon("agni_fury")
        result = bm.add_boon("indra_thunder")
        assert len(result) == 1
        # Adding same boons again should not re-unlock
        result2 = bm.add_boon("agni_fury")
        assert len(result2) == 0


class TestVictoryViewTweenAPI:
    """Regression for a runtime TypeError that crashed the game on boss clear:
    victory_view called TweenManager.add(obj=..., easing=...) which doesn't
    exist on the new tween API. Verify the view constructs and its on_show_view
    path schedules only the tween() convenience method."""

    def test_victory_view_constructs(self, monkeypatch):
        # arcade.View.__init__ requires a real window; bypass it.
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.victory_view import VictoryView
        v = VictoryView(score=12345, kills=42, highest_combo=8,
                        difficulty='hard', ship_class='garuda', wave=10,
                        stats={'total_damage': 5000})
        assert v.score == 12345
        assert v.wave == 10
        assert v.ship_class == 'garuda'
        # Animation entry state: title off-screen, score zero, alphas zero.
        assert v._title_y > HEIGHT
        assert v._displayed_score == 0.0
        assert all(a == 0.0 for a in v._row_alphas)
        # 5 alpha refs (Score, Kills, Combo, Difficulty, Prompts).
        assert len(v._alpha_refs) == 5

    def test_victory_view_tweens_finish(self, monkeypatch, tmp_path):
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views import victory_view as vv_mod
        # Redirect save to tmp so we don't pollute the real one.
        monkeypatch.setattr(vv_mod.save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(vv_mod.save_system, "_SAVE_DIR", tmp_path)

        from game.views.victory_view import VictoryView
        v = VictoryView(score=1000, kills=10, highest_combo=5,
                        difficulty='normal', wave=10)
        # Mirror the tween setup from on_show_view (without needing a window).
        from game.ui.easing import ease_out_elastic, ease_out_cubic
        v._tweens.tween(target=v, attr='_title_y', end=HEIGHT * 0.82,
                        duration=0.8, ease=ease_out_elastic,
                        start=HEIGHT + 100.0)
        v._tweens.tween(target=v, attr='_displayed_score', end=1000.0,
                        duration=1.2, delay=0.5, ease=ease_out_cubic, start=0.0)
        for i, ref in enumerate(v._alpha_refs):
            v._tweens.tween(target=ref, attr='val', end=255.0,
                            duration=0.5, delay=1.0 + i * 0.15,
                            ease=ease_out_cubic, start=0.0)

        # Step well past the longest delay (1.6s) + duration (1.2s).
        for _ in range(200):
            v._tweens.update(0.05)
            for i, ref in enumerate(v._alpha_refs):
                v._row_alphas[i] = ref.val

        # All anims should be at their final values.
        assert v._title_y == HEIGHT * 0.82
        assert v._displayed_score == 1000.0
        assert all(abs(a - 255.0) < 1e-6 for a in v._row_alphas)

    def test_transition_overlay_is_active_is_a_property(self):
        """Victory view uses TransitionOverlay.is_active as a property, not method."""
        from game.ui.transitions import TransitionOverlay
        # Must be accessible without parens and return a bool.
        val = TransitionOverlay.is_active
        assert isinstance(val, bool)
        # And calling it with parens (the old wrong usage) should fail clearly.
        raised = False
        try:
            TransitionOverlay.is_active()
        except TypeError:
            raised = True
        assert raised, "is_active() with parens should raise TypeError"


class TestButton:
    """Cover the reusable button widget used by the pause menu."""

    def test_hit_test(self):
        from game.ui.button import Button
        b = Button(cx=100, cy=200, width=80, height=40, label="OK")
        assert b.hit_test(100, 200) is True
        assert b.hit_test(60, 200) is True   # left edge
        assert b.hit_test(140, 200) is True  # right edge
        assert b.hit_test(50, 200) is False  # outside left
        assert b.hit_test(150, 200) is False # outside right
        assert b.hit_test(100, 170) is False # above
        assert b.hit_test(100, 230) is False # below

    def test_click_fires_on_release_over_button(self):
        from game.ui.button import Button
        calls = []
        b = Button(cx=100, cy=200, width=80, height=40, label="OK",
                   on_click=lambda: calls.append(1))
        b.update(0.016, 100, 200)   # mouse hovers
        assert b.hovered is True
        b.press()
        assert b.was_pressed is True
        clicked = b.release()
        assert clicked is True
        assert calls == [1]
        assert b.was_pressed is False

    def test_drag_off_cancels_click(self):
        from game.ui.button import Button
        calls = []
        b = Button(cx=100, cy=200, width=80, height=40, label="OK",
                   on_click=lambda: calls.append(1))
        b.update(0.016, 100, 200)   # hover over
        b.press()
        b.update(0.016, 400, 400)   # drag off
        clicked = b.release()
        assert clicked is False
        assert calls == []

    def test_hover_anim_decays_when_mouse_leaves(self):
        from game.ui.button import Button
        b = Button(cx=100, cy=200, width=80, height=40, label="OK")
        b.update(0.016, 100, 200)  # hover
        hov_peak = b._hover_anim
        # First frame: target=1.0, dt=0.016, factor=12*dt=0.192 → ~0.192
        # Step a few more times so the lerp climbs well past 0.3
        for _ in range(10):
            b.update(0.05, 100, 200)
        assert b._hover_anim > 0.5
        for _ in range(60):
            b.update(0.05, 500, 500)  # far away
        assert b._hover_anim < 0.05
        assert b.hovered is False

    def test_press_anim_decays(self):
        from game.ui.button import Button
        b = Button(cx=100, cy=200, width=80, height=40, label="OK")
        b.press()
        assert b._press_anim == 1.0
        for _ in range(60):
            b.update(0.05, 500, 500)
        assert b._press_anim == 0.0

    def test_keyboard_activation_does_not_require_mouse_hover(self):
        from game.ui.button import Button
        calls = []
        b = Button(cx=100, cy=200, width=80, height=40, label="OK",
                   on_click=lambda: calls.append(True))
        b.activate()
        assert calls == [True]


class TestOptionalAssets:
    def test_visual_assets_load_with_fallback_manager(self):
        from game.systems.asset_manager import AssetManager
        for name in ("pushpaka.png", "tripura.png", "garuda.png",
                     "boss_kumbhakarna.png", "boss_ravana.png"):
            assert AssetManager.texture(name) is not None


class TestSaveLifetimeStats:
    """Cover the new lifetime stat fields and the extended update_after_game."""

    def test_defaults_include_lifetime_fields(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        data = save_system.load()
        for key in ("total_damage", "best_combo", "total_boons",
                    "bosses_defeated", "playtime_seconds", "ships_mastered"):
            assert key in data, f"missing default for {key}"

    def test_update_after_game_persists_lifetime(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)

        save_system.update_after_game(
            score=15000, wave=10, kills=200,
            highest_combo=9, total_damage=45000,
            boons_claimed=4, bosses_defeated=["kumbhakarna"],
            ship_class="tripura", campaign_cleared=False,
        )
        data = save_system.load()
        assert data["high_score"] == 15000
        assert data["total_kills"] == 200
        assert data["best_combo"] == 9
        assert data["total_damage"] == 45000
        assert data["total_boons"] == 4
        assert data["bosses_defeated"] == ["kumbhakarna"]
        assert "tripura" not in data["ships_mastered"]  # not cleared

        # Second run with campaign clear and Ravana kill
        save_system.update_after_game(
            score=99999, wave=10, kills=400,
            highest_combo=10, total_damage=90000,
            boons_claimed=8, bosses_defeated=["ravana", "kumbhakarna"],
            ship_class="tripura", campaign_cleared=True,
        )
        data = save_system.load()
        assert data["high_score"] == 99999
        assert data["best_combo"] == 10
        assert data["total_damage"] == 135000   # 45k + 90k
        assert data["bosses_defeated"] == ["kumbhakarna", "ravana"]
        assert "tripura" in data["ships_mastered"]

    def test_bosses_dedup_across_runs(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.update_after_game(score=100, wave=5, kills=10,
                                      bosses_defeated=["kumbhakarna"])
        save_system.update_after_game(score=200, wave=5, kills=20,
                                      bosses_defeated=["kumbhakarna"])
        data = save_system.load()
        assert data["bosses_defeated"] == ["kumbhakarna"]
        assert data["games_played"] == 2

    def test_add_playtime_accumulates(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.add_playtime(12.5)
        save_system.add_playtime(7.5)
        data = save_system.load()
        assert abs(data["playtime_seconds"] - 20.0) < 1e-6

    def test_add_playtime_ignores_zero_and_negative(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.add_playtime(0)
        save_system.add_playtime(-5)
        data = save_system.load()
        assert data["playtime_seconds"] == 0


class TestStatsView:
    """Cover the lifetime stats screen — construction, panel layout, empty state."""

    def test_stats_view_constructs_with_panels(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.stats_view import StatsView
        v = StatsView(return_view=None)
        # 6 panels: Core, Playtime, Damage&Boons, Achievements, Bosses, Ships
        assert len(v._panels) == 6
        # Empty state visible when no runs have been played
        assert v._show_empty is True

    def test_stats_view_hides_empty_after_runs(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        # Seed a run
        save_system.update_after_game(score=100, wave=3, kills=5)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.stats_view import StatsView
        v = StatsView()
        assert v._show_empty is False

    def test_stats_view_panels_have_lines(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.update_after_game(
            score=12345, wave=8, kills=150,
            highest_combo=7, total_damage=50000,
            boons_claimed=5, bosses_defeated=["kumbhakarna"],
            ship_class="garuda", campaign_cleared=False,
        )
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.stats_view import StatsView
        v = StatsView()
        # Every panel must have at least one line
        for panel in v._panels:
            assert panel.title
            assert len(panel.lines) >= 1
            # Each line: (label, value, color)
            for line in panel.lines:
                assert len(line) == 3
                assert isinstance(line[0], str)
                assert isinstance(line[1], str)

    def test_fmt_hms(self):
        from game.views.stats_view import _fmt_hms
        assert _fmt_hms(0) == "0m 00s"
        assert _fmt_hms(59) == "0m 59s"
        assert _fmt_hms(60) == "1m 00s"
        assert _fmt_hms(3599) == "59m 59s"
        assert _fmt_hms(3600) == "1h 00m"
        assert _fmt_hms(7325) == "2h 02m"


class TestAchievementsView:
    def test_achievement_hall_pages_all_trophies(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.achievements_view import AchievementsView
        view = AchievementsView()
        assert view.page_count >= 2
        assert view.PER_PAGE == 8


class TestGameViewPauseButtons:
    """Verify the new pause-menu button list is wired into GameView.__init__."""

    def test_pause_buttons_initialized(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        # Stub the heavy systems so we don't actually open a window / play sound
        from game.views import game_view as gv_mod
        # Build a GameView by calling __init__; we need to mock everything it touches.
        # Simplest: construct via type with __new__ and set just the attrs the test cares about.
        gv = gv_mod.GameView.__new__(gv_mod.GameView)
        gv._init_pause_buttons()
        assert len(gv._pause_buttons) == 4
        labels = [b.label for b in gv._pause_buttons]
        assert labels == ["RESUME", "RESTART RUN", "SETTINGS", "QUIT TO MENU"]
        # Each button has a hotkey hint
        for b in gv._pause_buttons:
            assert b.hotkey is not None
        # Hit-test one of them
        assert gv._pause_buttons[0].hit_test(WIDTH // 2, HEIGHT // 2 + 30) is True


class TestLoadingView:
    def test_loading_view_constructs_and_updates(self, monkeypatch):
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.loading_screen import LoadingView
        lv = LoadingView()
        assert lv._progress == 0.0
        assert lv._ready_to_advance is False
        # Update by 3.0 seconds
        lv.on_update(3.0)
        assert lv._progress >= 1.0
        assert lv._ready_to_advance is True
        assert "READY" in lv._status_text_str


class TestStoryBriefingView:
    def test_story_briefing_pages_and_completion_state(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        class _TextStub:
            def __init__(self, text, *args, **kwargs):
                self.text = text
                self.color = kwargs.get("color", (255, 255, 255))
            def draw(self):
                return None
        monkeypatch.setattr(arcade, "Text", _TextStub)
        from game.views.story_briefing_view import StoryBriefingView

        view = StoryBriefingView()
        assert view.page == 0
        view._set_page(2)
        assert view._button.text == "BEGIN SORTIE"

        data = save_system.load()
        data["story_intro_seen"] = True
        save_system.save(data)
        assert save_system.load()["story_intro_seen"] is True


class TestCanonicalTokensAndComponents:
    def test_canonical_tokens(self):
        from game.ui.vedic_theme import (
            VOID, OBSIDIAN, WELL, GOLD, GOLD_BRIGHT, CYAN, CYAN_BRIGHT,
            BRASS, ASTRA_RED, ASTRA_RED_BRIGHT, PARCHMENT, STARLIGHT, GREY,
            JADE, AMBER, CRIMSON, get_gauge_color, BOON_ACCENTS
        )
        assert VOID == (7, 10, 19)
        assert OBSIDIAN == (11, 13, 18)
        assert GOLD == (233, 196, 0)
        assert CYAN == (0, 219, 231)
        assert ASTRA_RED == (191, 0, 54)
        assert get_gauge_color(0.8) == JADE
        assert get_gauge_color(0.5) == AMBER
        assert get_gauge_color(0.2) == CRIMSON
        assert "Agni" in BOON_ACCENTS

    def test_nav_rail(self):
        from game.ui.nav_rail import NavRail, NAV_ITEMS
        rail = NavRail(current_screen="menu")
        assert rail.current_screen == "menu"
        assert len(NAV_ITEMS) == 7
        rail.on_mouse_motion(100, 460)
        assert rail.hovered_index == 0

    def test_modal(self):
        from game.ui.modal import Modal
        m = Modal("PAUSE", "SORTIE SUSPENDED", body=["Mission is paused"],
                  actions=[("RESUME", "resume", "celestial"), ("ABANDON", "abandon", "danger")])
        assert not m.is_open
        m.open()
        assert m.is_open
        assert len(m._buttons) == 2
        # Test key press
        import arcade
        assert m.on_key_press(arcade.key.ESCAPE, 0) == "cancel"
        assert not m.is_open

