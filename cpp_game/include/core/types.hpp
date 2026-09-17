#pragma once
#include <string>
#include <vector>
#include <cmath>
#include "raylib.h"

namespace Vimana {

// ── Math Helpers ────────────────────────────────────────────────────────────
inline Vector2 Vector2Zero() { return { 0.0f, 0.0f }; }
inline Vector2 Vector2Add(Vector2 a, Vector2 b) { return { a.x + b.x, a.y + b.y }; }
inline Vector2 Vector2Subtract(Vector2 a, Vector2 b) { return { a.x - b.x, a.y - b.y }; }
inline Vector2 Vector2Scale(Vector2 v, float s) { return { v.x * s, v.y * s }; }
inline float Vector2Length(Vector2 v) { return std::sqrt(v.x * v.x + v.y * v.y); }
inline Vector2 Vector2Normalize(Vector2 v) {
    float len = Vector2Length(v);
    if (len > 0.0001f) return { v.x / len, v.y / len };
    return { 0.0f, 0.0f };
}
inline float Vector2Distance(Vector2 a, Vector2 b) {
    float dx = a.x - b.x;
    float dy = a.y - b.y;
    return std::sqrt(dx * dx + dy * dy);
}
inline float Vector2AngleDeg(Vector2 from, Vector2 to) {
    return std::atan2(to.y - from.y, to.x - from.x) * (180.0f / 3.1415926535f);
}

// ── Enums ───────────────────────────────────────────────────────────────────
enum class ViewType {
    MENU,
    CAMPAIGN_MAP,
    SHIP_SELECT,
    LOADOUT,
    DIFFICULTY_SELECT,
    GAMEPLAY,
    WAVE_CLEAR,
    DUEL,
    BOON_SELECT,
    LEADERBOARD,
    MULTIPLAYER_LOBBY,
    CODEX,
    SETTINGS,
    VICTORY,
    GAME_OVER
};

enum class PerformanceRank {
    S_RANK,
    A_RANK,
    B_RANK,
    C_RANK
};

struct WaveResult {
    int wave_num = 1;
    int enemies_destroyed = 0;
    int damage_taken = 0;
    int max_combo = 1;
    int accuracy_pct = 88;
    int score_earned = 0;
    int prana_earned = 50;
    bool no_damage = false;
    bool perfect_wave = false;
    PerformanceRank rank = PerformanceRank::A_RANK;
};

enum class BoonType {
    AGNI_SOLAR_FURY,        // Burning dot & explosive death
    INDRA_VAJRA_THUNDER,    // Chain lightning on hit
    VAYU_GALE_TEMPEST,      // Dash cdr & cyclone wakes
    GARUDA_CELESTIAL_MAGNET,// Magnetic pickup radius
    VARUNA_OCEANIC_WARD,    // Max HP + passive regeneration
    SUDARSHANA_KEEN_EDGE,   // Larger Chakram + reduced cooldown
    YAMA_FATAL_DECREE,      // Execute bonus on weakened targets
    SURYA_RADIANT_PIERCE,   // 7th shot piercing golden slug
    NARASIMHA_BERSERK_MIGHT // Low HP massive damage amplification
};

struct BoonSynergy {
    std::string id;
    std::string name;
    std::string formula;
    std::string description;
    BoonType req1;
    BoonType req2;
    Color color;
};

struct ShipMastery {
    int kills = 0;
    int waves_cleared = 0;
    int bosses_defeated = 0;
    int mastery_level = 1;
};

enum class GameMode {
    CAMPAIGN,
    ENDLESS,
    DUEL_PVP,
    DUEL_TRAINING
};

enum class Difficulty {
    EASY,
    NORMAL,
    HARD
};

enum class BotDifficulty {
    NOVICE,
    SKILLED,
    ASURA_MASTER
};

enum class BulletType {
    PLAYER_BASIC,
    PLAYER_PIERCING,
    PLAYER_SPREAD,
    CHAKRAM,
    NARASIMHA_CLAW,
    ENEMY_BASIC,
    ENEMY_SPREAD,
    ENEMY_SNIPER_BEAM,
    ENEMY_SEEKING,
    BOSS_VOID_ORB,
    BOSS_LIGHTNING_STORM
};

enum class PowerupType {
    KAVACH_SHIELD,      // Invulnerability shield
    AGNEYASTRA_SPREAD,  // 3-way spread shots
    VAYAVYASTRA_SPEED,  // Speed boost & dash refund
    AMRITA_HEAL,        // Instant HP recovery
    BRAHMASTRA_BOMB,    // Celestial nuke item
    ASTRA_OVERDRIVE     // Hyper rapid fire
};

// ── Player Consumables & Currency ───────────────────────────────────────────
struct ConsumableInventory {
    int prana_shards = 200;
    int kavach_charges = 0;  // 1-time auto death defiance / barrier
    int soma_vials = 1;      // Usable via 'C' hotkey
    int vajra_flares = 1;    // Usable via 'V' hotkey
};

// ── High Score Entry ────────────────────────────────────────────────────────
struct ScoreEntry {
    int id = 0;
    std::string player_name = "Warrior";
    int score = 0;
    int level_reached = 1;
    std::string difficulty = "normal";
    std::string ship_class = "pushpaka";
    std::string game_id = "";
    int kills = 0;
    int total_damage = 0;
    float duration_seconds = 0.0f;
    std::string created_at = "";
};

} // namespace Vimana
