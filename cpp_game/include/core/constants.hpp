#pragma once
#include <string>
#include <vector>
#include <array>
#include "raylib.h"
#include "core/types.hpp"

namespace Vimana {

// ── Screen & Display ──────────────────────────────────────────────────────────
constexpr int SCREEN_WIDTH  = 900;
constexpr int SCREEN_HEIGHT = 600;
constexpr const char* WINDOW_TITLE = "Vimana Wars // Celestial Combat";
constexpr int TARGET_FPS = 60;

// ── Pilot Identity ────────────────────────────────────────────────────────────
constexpr const char* PILOT_ID       = "VMN-7704";
constexpr const char* PILOT_NAME     = "CHETAN";
constexpr const char* PILOT_SQUADRON = "ARJUNA CELESTIAL ACE";

// ── Combat & Physics ──────────────────────────────────────────────────────────
constexpr float PLAYER_DEFAULT_SPEED     = 300.0f;
constexpr float PLAYER_BOOSTED_SPEED     = 480.0f;
constexpr float PLAYER_SHOOT_COOLDOWN    = 0.15f;
constexpr int   PLAYER_DEFAULT_MAX_HP    = 100;
constexpr float PLAYER_DEFAULT_RADIUS    = 20.0f;
constexpr float PLAYER_GRAZE_RADIUS      = 36.0f;
constexpr float PLAYER_INVINCIBILITY_TIME= 0.6f;
constexpr int   PLAYER_CONTACT_DAMAGE    = 15;

// ── Scoring ───────────────────────────────────────────────────────────────────
constexpr int SCORE_NEAR_MISS    = 25;
constexpr int SCORE_KILL_BASE    = 100;
constexpr int SCORE_ASSIST       = 20;
constexpr int SCORE_CRIT_BONUS   = 50;
constexpr int SCORE_EXECUTE_BONUS= 75;
constexpr int BONUS_NO_DEATH     = 100;
constexpr int BONUS_PERFECT_WAVE = 75;

// ── Dash & Movement ───────────────────────────────────────────────────────────
constexpr float DASH_SPEED_BURST  = 750.0f;
constexpr float DASH_DURATION     = 0.22f;
constexpr float DASH_COOLDOWN     = 1.6f;
constexpr int   DASH_MAX_CHARGES  = 2;

// ── Bullets ───────────────────────────────────────────────────────────────────
constexpr float PLAYER_BULLET_SPEED  = 780.0f;
constexpr float PLAYER_BULLET_RADIUS = 5.0f;
constexpr int   PLAYER_BULLET_DAMAGE = 25;

constexpr float ENEMY_BULLET_SPEED  = 360.0f;
constexpr float ENEMY_BULLET_RADIUS = 5.0f;
constexpr int   ENEMY_BULLET_DAMAGE = 12;

// ── Chakram ───────────────────────────────────────────────────────────────────
constexpr float CHAKRAM_ORBIT_RADIUS  = 120.0f;
constexpr float CHAKRAM_ROTATION_SPEED= 540.0f;
constexpr int   CHAKRAM_DAMAGE        = 45;
constexpr float CHAKRAM_COOLDOWN      = 6.0f;

// ── Critical Hits & Execute ───────────────────────────────────────────────────
constexpr float CRIT_CHANCE          = 0.15f;   // 15% per shot
constexpr float CRIT_MULTIPLIER      = 2.0f;    // 2x damage on crit
constexpr float EXECUTE_THRESHOLD    = 0.20f;   // enemy HP < 20% → execute window
constexpr float EXECUTE_BONUS        = 1.25f;   // +25% damage during execute

// ── Elite Enemies ─────────────────────────────────────────────────────────────
constexpr int   ELITE_SPAWN_EVERY_N_WAVES = 5;  // elite appears every N waves
constexpr float ELITE_HP_MULT            = 1.5f;
constexpr float ELITE_DAMAGE_MULT        = 1.25f;
constexpr float ELITE_SPEED_MULT         = 1.15f;

// ── Co-op: Downed & Revive ────────────────────────────────────────────────────
constexpr float REVIVE_TIME          = 3.5f;   // 3.5 seconds to fully revive
constexpr float REVIVE_RANGE         = 80.0f;  // pixels — must be this close
constexpr float DOWNED_TIMER         = 15.0f;  // seconds before eliminated

// ── Co-op: Team Combo ─────────────────────────────────────────────────────────
constexpr float TEAM_COMBO_BUFF_DAMAGE = 1.20f;  // +20% team damage
constexpr float TEAM_COMBO_BUFF_SPEED  = 1.10f;  // +10% team move speed
constexpr float TEAM_COMBO_BUFF_DUR    = 8.0f;   // seconds the buff lasts

// ── Co-op: Cooperative Astra Cooldown ────────────────────────────────────────
constexpr float CO_OP_ASTRA_COOLDOWN   = 30.0f;  // 30 second shared cooldown
constexpr float CO_OP_ASTRA_SYNC_WIN   = 1.5f;   // 1.5 second coordination window

// ── Co-op: Player Scaling ─────────────────────────────────────────────────────
// EnemyCount = BaseCount * (1 + 0.35 * (Players - 1))
constexpr float CO_OP_ENEMY_SCALE_PER_PLAYER = 0.35f;
constexpr float CO_OP_BOSS_HP_SCALE           = 0.50f;  // +50% boss HP per extra player
constexpr float CO_OP_ELITE_CHANCE_SCALE      = 0.08f;  // +8% elite chance per extra player

// ── Networking ────────────────────────────────────────────────────────────────
constexpr int   MAX_CO_OP_PLAYERS      = 4;
constexpr int   SERVER_TICK_RATE       = 60;
constexpr int   DEFAULT_HOST_PORT      = 7704;    // VMN-7704 reference
constexpr int   DEFAULT_SIGNALING_PORT = 7705;
constexpr float NET_RECONNECT_WINDOW   = 15.0f;   // seconds before AI takeover
constexpr float NET_INTERP_DELAY       = 0.033f;  // 2-frame interpolation buffer
constexpr float NET_RECONCILE_THRESHOLD= 8.0f;    // pixels — force correction above this

// ── Networking URLs ───────────────────────────────────────────────────────────
constexpr const char* DEFAULT_API_URL  = "http://127.0.0.1:5000";
constexpr const char* CLOUD_API_URL    = "https://vimana-wars.onrender.com";

// ── Vedic Cyberpunk Color Palette ─────────────────────────────────────────────
inline const Color COLOR_OBSIDIAN      = {  5,   8,  16, 255 };
inline const Color COLOR_SURFACE_LOW   = { 12,  18,  30, 240 };
inline const Color COLOR_SURFACE_MID   = { 16,  24,  38, 245 };
inline const Color COLOR_SURFACE_HIGH  = { 20,  28,  48, 255 };
inline const Color COLOR_GOLD          = { 220, 180,  50, 255 };
inline const Color COLOR_GOLD_BRIGHT   = { 255, 225,  90, 255 };
inline const Color COLOR_CYAN          = {  40, 200, 220, 255 };
inline const Color COLOR_CYAN_BRIGHT   = { 120, 240, 255, 255 };
inline const Color COLOR_PARCHMENT     = { 235, 225, 210, 255 };
inline const Color COLOR_MUTED         = { 120, 130, 150, 255 };
inline const Color COLOR_RED_BRIGHT    = { 255,  60,  60, 255 };
inline const Color COLOR_GREEN_BRIGHT  = {  50, 240, 120, 255 };
inline const Color COLOR_ORANGE_BRIGHT = { 255, 140,  40, 255 };
inline const Color COLOR_PURPLE_BRIGHT = { 210,  90, 255, 255 };

// Accessibility overrides
inline Color COLOR_CB_ACCENT_1        = { 255, 255, 255, 255 };
inline Color COLOR_CB_ACCENT_2        = { 255, 230,  50, 255 };
inline bool  g_colorblind_mode        = false;
inline bool  g_screen_shake_enabled   = true;
inline bool  g_scanlines_enabled      = true;

// ── Difficulty Profiles ───────────────────────────────────────────────────────
inline const std::array<DifficultyProfile, 4> DIFFICULTY_PROFILES = {{
    {
        Difficulty::NOVICE,
        "NOVICE",
        "For the initiated — enemies fight with honor",
        0.70f,   // enemy HP × 0.70
        0.85f,   // bullet speed × 0.85
        0.00f,   // no extra elite chance
        0        // no extra enemies
    },
    {
        Difficulty::KSHATRIYA,
        "KSHATRIYA",
        "The warrior's path — balanced and true",
        1.00f, 1.00f, 0.00f, 0
    },
    {
        Difficulty::ASURA_SLAYER,
        "ASURA SLAYER",
        "The army of Asuras fights without mercy",
        1.35f, 1.20f, 0.15f, 2
    },
    {
        Difficulty::CHAKRAVYUHA,
        "CHAKRAVYUHA",
        "The inescapable formation — no shield, no mercy",
        1.70f, 1.50f, 0.40f, 4
    }
}};

// ── Campaign Realms & Boss Single Source of Truth ─────────────────────────────
enum class RealmModifierType {
    NONE,
    SWARGA_AETHER,      // +15% player thruster agility
    KSHIRA_VORTEX,      // vortex currents & projectile drift
    DANDAKA_JAMMING,    // sensor/radar jamming & short telegraphs
    LANKA_MOLTEN_FIRE,  // +15% void fire damage
    SETU_DRIFT,         // +20% dash distance
    NARAKA_FLAK,        // extra flak shrapnel from shooter enemies
    MAHAYUDDHA_DISTORT  // reality distortion rift events
};

struct CampaignRealm {
    int               id;
    const char*       name;
    const char*       sanskrit_title;
    int               start_wave;
    int               end_wave;
    int               boss_wave;
    const char*       boss_name;
    RealmModifierType modifier_type;
    const char*       modifier_desc;
    const char*       description;
    Vector2           map_pos;
    Color             accent_color;
};

inline const std::array<CampaignRealm, 7> CAMPAIGN_REALMS = {{
    { 1, "Swarga Outpost",     "Gate of Indra",                 1,  3,  0, "None",                   RealmModifierType::SWARGA_AETHER,     "Celestial Aether (+15% Speed)",       "Outer orbital sanctuary guarding the celestial gateway. Light Asura reconnaissance forces.", { 140, 420 }, COLOR_CYAN_BRIGHT },
    { 2, "Kshira Sagara",      "Ocean of Celestial Nectar",     4,  6,  5, "Titan Kumbhakarna",      RealmModifierType::KSHIRA_VORTEX,     "Vortex Currents & Drift",             "Astral sea of luminescent nebulae. Beware the awakened Slumbering Mountain at wave 5.",        { 250, 310 }, { 100, 220, 255, 255 } },
    { 3, "Dandaka Void",       "Forest of Eternal Shadows",     7,  9,  0, "None",                   RealmModifierType::DANDAKA_JAMMING,   "Sensor Jamming & Stealth",            "Perilous asteroid expanse infested with cloaked Rakshasa raiders and plasma minefields.",      { 390, 360 }, COLOR_PURPLE_BRIGHT },
    { 4, "Lanka Approach",     "The Molten Bastion",           10, 12, 10, "Emperor Ravana",         RealmModifierType::LANKA_MOLTEN_FIRE, "Molten Void Fire (+15% Dmg)",        "Outer planetary defense network surrounding the demon fortress. Emperor Ravana commands wave 10.", { 510, 260 }, COLOR_GOLD_BRIGHT },
    { 5, "Setu Expanse",       "Bridge of Floating Spheres",   13, 15, 15, "Warlord Mahishasura",    RealmModifierType::SETU_DRIFT,        "Hyperlane Drift (+20% Dash)",         "Cosmic bridge of magnetized meteors. Guarded by the unyielding Buffalo Warlord at wave 15.",    { 630, 330 }, COLOR_GREEN_BRIGHT },
    { 6, "Naraka Forge",       "Foundry of Asura Warships",    16, 25, 25, "Conqueror Indrajit",     RealmModifierType::NARAKA_FLAK,       "Heavy Flak Shrapnel",                 "Volcanic underworld foundry where demon dreadnoughts are forged. Conqueror Indrajit strikes at wave 25.", { 730, 220 }, COLOR_RED_BRIGHT },
    { 7, "Mahayuddha Citadel", "Throne of the Demon Sovereign",26, 30, 30, "Tyrant Hiranyakashipu", RealmModifierType::MAHAYUDDHA_DISTORT, "Reality Distortion Field",            "Epicenter of the Asura Dominion. Confront the immortal tyrant Hiranyakashipu in the final wave 30 clash.", { 820, 140 }, COLOR_ORANGE_BRIGHT }
}};

inline const CampaignRealm& GetCampaignRealmForWave(int wave) {
    int effective = ((wave - 1) % 30) + 1;
    for (const auto& realm : CAMPAIGN_REALMS) {
        if (effective >= realm.start_wave && effective <= realm.end_wave) return realm;
    }
    return CAMPAIGN_REALMS[6];
}

// Backward-compatibility alias for legacy code
using RealmData = CampaignRealm;
inline const std::array<CampaignRealm, 7>& REALMS = CAMPAIGN_REALMS;
inline const CampaignRealm& GetRealmForWave(int wave) { return GetCampaignRealmForWave(wave); }

// ── Currency & Armory ─────────────────────────────────────────────────────────
constexpr int PRANA_REWARD_WAVE_CLEAR   = 50;
constexpr int PRANA_REWARD_BOSS_DEFEAT  = 250;
constexpr int PRANA_REWARD_DUEL_WIN     = 150;
constexpr int PRANA_REWARD_CO_OP_WIN    = 200;
constexpr int PRANA_REWARD_REVIVE       = 30;  // bonus for reviving teammate

constexpr int COST_KAVACH_SHIELD        = 120;
constexpr int COST_SOMA_VIAL            = 100;
constexpr int COST_VAJRA_FLARE          = 80;
constexpr int COST_EARLY_SHIP_UNLOCK    = 600;

// ── Mini-Event Types ──────────────────────────────────────────────────────────
enum class MiniEventType {
    NONE,
    ASTRAL_STORM,       // Reduced visibility + debris bullets
    ELITE_INVASION,     // 3 elites spawn mid-wave
    TREASURE_SHIP,      // Destroy for 300 Prana
    VOID_RIFT,          // Gravity well pulls bullets
    RESCUE_MISSION,     // Escort friendly Vimana to safe zone
    DEFEND_ASTRAL_CORE  // Survive 20s protecting core
};

} // namespace Vimana
