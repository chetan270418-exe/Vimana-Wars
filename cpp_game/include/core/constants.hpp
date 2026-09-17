#pragma once
#include <string>
#include <vector>
#include <array>
#include "raylib.h"

namespace Vimana {

// ── Screen & Display ────────────────────────────────────────────────────────
constexpr int SCREEN_WIDTH = 900;
constexpr int SCREEN_HEIGHT = 600;
constexpr const char* WINDOW_TITLE = "Vimana Wars // Celestial Combat";
constexpr int TARGET_FPS = 60;

// ── Combat & Physics ────────────────────────────────────────────────────────
constexpr float PLAYER_DEFAULT_SPEED = 300.0f;
constexpr float PLAYER_BOOSTED_SPEED = 480.0f;
constexpr float PLAYER_SHOOT_COOLDOWN = 0.15f;
constexpr int PLAYER_DEFAULT_MAX_HP = 100;
constexpr float PLAYER_DEFAULT_RADIUS = 20.0f;
constexpr float PLAYER_GRAZE_RADIUS = 36.0f;
constexpr float PLAYER_INVINCIBILITY_TIME = 0.6f;
constexpr int PLAYER_CONTACT_DAMAGE = 15;

constexpr int SCORE_NEAR_MISS = 25;
constexpr int BONUS_NO_DEATH = 100;
constexpr int BONUS_PERFECT_WAVE = 75;

constexpr float DASH_SPEED_BURST = 750.0f;
constexpr float DASH_DURATION = 0.22f;
constexpr float DASH_COOLDOWN = 1.6f;
constexpr int DASH_MAX_CHARGES = 2;

constexpr float PLAYER_BULLET_SPEED = 780.0f;
constexpr float PLAYER_BULLET_RADIUS = 5.0f;
constexpr int PLAYER_BULLET_DAMAGE = 25;

constexpr float ENEMY_BULLET_SPEED = 360.0f;
constexpr float ENEMY_BULLET_RADIUS = 5.0f;
constexpr int ENEMY_BULLET_DAMAGE = 12;

constexpr float CHAKRAM_ORBIT_RADIUS = 120.0f;
constexpr float CHAKRAM_ROTATION_SPEED = 540.0f;
constexpr int CHAKRAM_DAMAGE = 45;
constexpr float CHAKRAM_COOLDOWN = 6.0f;

// ── Vedic Cyberpunk Color Palette ───────────────────────────────────────────
inline const Color COLOR_OBSIDIAN     = { 5, 8, 16, 255 };
inline const Color COLOR_SURFACE_LOW  = { 12, 18, 30, 240 };
inline const Color COLOR_SURFACE_MID  = { 16, 24, 38, 245 };
inline const Color COLOR_SURFACE_HIGH = { 20, 28, 48, 255 };
inline const Color COLOR_GOLD         = { 220, 180, 50, 255 };
inline const Color COLOR_GOLD_BRIGHT  = { 255, 225, 90, 255 };
inline const Color COLOR_CYAN         = { 40, 200, 220, 255 };
inline const Color COLOR_CYAN_BRIGHT  = { 120, 240, 255, 255 };
inline const Color COLOR_PARCHMENT    = { 235, 225, 210, 255 };
inline const Color COLOR_MUTED        = { 120, 130, 150, 255 };
inline const Color COLOR_RED_BRIGHT   = { 255, 60, 60, 255 };
inline const Color COLOR_GREEN_BRIGHT = { 50, 240, 120, 255 };
inline const Color COLOR_ORANGE_BRIGHT= { 255, 140, 40, 255 };
inline const Color COLOR_PURPLE_BRIGHT= { 210, 90, 255, 255 };

// ── Realm Metadata ──────────────────────────────────────────────────────────
struct RealmData {
    int id;
    const char* name;
    const char* subtitle;
    int start_wave;
    int end_wave;
    Color bg_color;
    Color accent_color;
};

inline const std::array<RealmData, 10> REALMS = {{
    { 1, "Swarga", "The Heavenly Celestial Realm", 1, 3, { 5, 8, 26, 255 }, { 120, 200, 255, 255 } },
    { 2, "Kshira Sagara", "The Cosmic Ocean of Milk", 4, 6, { 4, 18, 28, 255 }, { 80, 240, 220, 255 } },
    { 3, "Dandaka Void", "The Mystical Astral Forest", 7, 9, { 14, 5, 24, 255 }, { 210, 100, 255, 255 } },
    { 4, "Lanka", "The Molten Rift of Ravana", 10, 12, { 22, 4, 10, 255 }, { 255, 70, 70, 255 } },
    { 5, "Setu Expanse", "The Bridge Between Celestial Worlds", 13, 15, { 9, 12, 30, 255 }, { 255, 150, 80, 255 } },
    { 6, "Naraka Forge", "The Burning Foundry of Asura Warships", 16, 18, { 25, 7, 5, 255 }, { 255, 100, 40, 255 } },
    { 7, "Mahayuddha Citadel", "The Final Astral Battlefield", 19, 20, { 18, 4, 24, 255 }, { 255, 80, 190, 255 } },
    { 8, "Patala Depths", "The Serpent Kingdom Below", 21, 23, { 3, 12, 18, 255 }, { 60, 255, 180, 255 } },
    { 9, "Brahmaloka Summit", "The Creator's Divine Citadel", 24, 26, { 20, 18, 30, 255 }, { 200, 170, 255, 255 } },
    { 10, "Vaikuntha Gate", "The Eternal Threshold of Vishnu", 27, 30, { 10, 5, 20, 255 }, { 255, 150, 255, 255 } }
}};

inline const RealmData& GetRealmForWave(int wave) {
    int effective = ((wave - 1) % 30) + 1;
    for (const auto& realm : REALMS) {
        if (effective >= realm.start_wave && effective <= realm.end_wave) {
            return realm;
        }
    }
    return REALMS[9];
}

// ── Currency & Armory ───────────────────────────────────────────────────────
constexpr int PRANA_REWARD_WAVE_CLEAR = 50;
constexpr int PRANA_REWARD_BOSS_DEFEAT = 250;
constexpr int PRANA_REWARD_DUEL_WIN = 150;

constexpr int COST_KAVACH_SHIELD = 120;
constexpr int COST_SOMA_VIAL = 100;
constexpr int COST_VAJRA_FLARE = 80;

constexpr int COST_EARLY_SHIP_UNLOCK = 600;

// ── Networking Defaults ─────────────────────────────────────────────────────
constexpr const char* DEFAULT_API_URL = "http://127.0.0.1:5000";
constexpr const char* CLOUD_API_URL = "https://vimana-wars.onrender.com";

} // namespace Vimana
