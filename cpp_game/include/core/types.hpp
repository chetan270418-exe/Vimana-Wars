#pragma once
#include <string>
#include <vector>
#include <cmath>
#include <cstdint>
#include "raylib.h"

namespace Vimana {

inline constexpr int SAVE_SCHEMA_VERSION = 6;

// ── Math Helpers ─────────────────────────────────────────────────────────────
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

// ── View State Machine ────────────────────────────────────────────────────────
enum class ViewType {
    BOOT,               // 2s animated splash
    TITLE,              // Title card — PRESS SPACE
    PILOT_SETUP,        // First-launch name entry
    MENU,               // Pilot dashboard
    CAMPAIGN_MAP,       // 10-act campaign map
    SHIP_SELECT,        // Vimana Hangar
    LOADOUT,            // Pre-mission loadout
    DIFFICULTY_SELECT,  // 4-tier difficulty picker
    GAMEPLAY,           // Live combat
    WAVE_CLEAR,         // Post-wave tally S/A/B/C
    DUEL,               // Local 1v1 / training
    BOON_SELECT,        // Boon draft after wave
    LEADERBOARD,        // Hall of Valor
    MULTIPLAYER_LOBBY,  // Room create / join
    MULTIPLAYER_RESULT, // Post-match co-op/PvP result
    PROFILE,            // Pilot profile + match history
    ACHIEVEMENTS,       // Browsable trophy gallery
    CODEX,              // Bestiary / lore / synergy reference
    SETTINGS,           // Audio / Controls / Accessibility
    AUTH,               // Online Account Login / Registration
    VICTORY,            // Campaign victory
    GAME_OVER,          // Defeat screen
    QUIT                // Safe exit request (main loop handles teardown)
};

// ── Performance Rank ──────────────────────────────────────────────────────────
enum class PerformanceRank {
    S_RANK,
    A_RANK,
    B_RANK,
    C_RANK
};

// ── Wave Result (post-wave tally) ─────────────────────────────────────────────
struct WaveResult {
    int wave_num           = 1;
    int enemies_destroyed  = 0;
    int damage_taken       = 0;
    int max_combo          = 1;
    int accuracy_pct       = 100;
    int score_earned       = 0;
    int prana_earned       = 50;
    bool no_damage         = false;
    bool perfect_wave      = false;
    PerformanceRank rank   = PerformanceRank::A_RANK;
    std::string rank_reason = "";
    std::string boss_ship_unlocked = "";
};

// ── Match Record (persisted in DB for match history) ─────────────────────────
struct MatchRecord {
    int   wave          = 1;
    int   score         = 0;
    int   kills         = 0;
    int   assists       = 0;
    int   revives       = 0;
    int   total_damage  = 0;
    float duration_sec  = 0.0f;
    PerformanceRank rank = PerformanceRank::B_RANK;
    std::string ship_id  = "pushpaka";
    std::string created_at = "";
};

// ── Boon System ───────────────────────────────────────────────────────────────
// IMPORTANT: BoonType MUST appear before BoonSynergy
enum class BoonType {
    AGNI_SOLAR_FURY,         // Burning dot & explosive death
    INDRA_VAJRA_THUNDER,     // Chain lightning on hit
    VAYU_GALE_TEMPEST,       // Dash cdr & cyclone wakes
    GARUDA_CELESTIAL_MAGNET, // Magnetic pickup radius
    VARUNA_OCEANIC_WARD,     // Max HP + passive regeneration
    SUDARSHANA_KEEN_EDGE,    // Larger Chakram + reduced cooldown
    YAMA_FATAL_DECREE,       // Execute bonus on weakened targets
    SURYA_RADIANT_PIERCE,    // 7th shot piercing golden slug
    NARASIMHA_BERSERK_MIGHT  // Low HP massive damage amplification
};

struct UpgradeChoice {
    std::string id;
    std::string name;
    std::string description;
    int cost;
    bool purchased;
};

// ── Combat & Damage Events ───────────────────────────────────────────────────
struct DamageEvent {
    uint8_t source_player_id = 0;
    int damage_amount        = 0;
    bool is_crit             = false;
    bool is_fatal            = false;
    Vector2 hit_position     = { 0.0f, 0.0f };
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

// ── Ship Mastery ───────────────────────────────────────────────────────────────
struct ShipMastery {
    int kills            = 0;
    int waves_cleared    = 0;
    int bosses_defeated  = 0;
    int mastery_level    = 1;  // 1–20
};

// ── Game Modes ─────────────────────────────────────────────────────────────────
enum class GameMode {
    CAMPAIGN,
    ENDLESS,
    DUEL_PVP,
    DUEL_TRAINING,
    CO_OP_PVE,    // 2–4 player cooperative
    BOSS_RUSH,    // Boss-only gauntlet
    DAILY_CHALLENGE
};

// Co-op failure rules. These are persisted as small integer values; keep the
// explicit values stable so older/newer saves remain readable.
enum class CoopRule : uint8_t {
    REVIVE_MODE = 0, // Existing individual lives + down/revive loop
    SQUAD_LIVES = 1, // Shared pool spent when a downed pilot bleeds out
    HARDCORE = 2     // No downed state or revives
};

// ── Difficulty (4-tier) ───────────────────────────────────────────────────────
enum class Difficulty {
    NOVICE,        // Initiated — fights with honor
    KSHATRIYA,     // Warrior's path — baseline
    ASURA_SLAYER,  // Army of Asuras fights without mercy
    CHAKRAVYUHA    // Inescapable formation — no mercy
};

struct DifficultyProfile {
    Difficulty   tier;
    const char*  name;
    const char*  flavor;
    float        enemy_hp_mult;
    float        bullet_speed_mult;
    float        elite_chance_bonus;  // added on top of base elite chance
    int          min_enemies_bonus;   // extra enemies per wave
};

// ── Bot Difficulty ────────────────────────────────────────────────────────────
enum class BotDifficulty {
    NOVICE,
    SKILLED,
    ASURA_MASTER
};

// ── Bullet & Powerup Types ────────────────────────────────────────────────────
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
    KAVACH_SHIELD,     // Invulnerability shield
    AGNEYASTRA_SPREAD, // 3-way spread shots
    VAYAVYASTRA_SPEED, // Speed boost & dash refund
    AMRITA_HEAL,       // Instant HP recovery
    BRAHMASTRA_BOMB,   // Celestial nuke item
    ASTRA_OVERDRIVE    // Hyper rapid fire
};

// ── Threat Level (aggro system) ───────────────────────────────────────────────
enum class ThreatLevel {
    NONE,
    LOW,
    MEDIUM,
    HIGH,
    TAUNTED  // Max priority — overrides everything
};

// ── Consumables & Currency ────────────────────────────────────────────────────
struct ConsumableInventory {
    int prana_shards    = 200;
    int kavach_charges  = 0;   // auto death-defiance barrier
    int soma_vials      = 1;   // usable via 'C' hotkey
    int vajra_flares    = 1;   // usable via 'V' hotkey
};

// ── High Score Entry ──────────────────────────────────────────────────────────
struct ScoreEntry {
    int         id              = 0;
    std::string player_name     = "Warrior";
    int         score           = 0;
    int         level_reached   = 1;
    std::string difficulty      = "normal";
    std::string ship_class      = "pushpaka";
    std::string game_id         = "";
    int         kills           = 0;
    int         total_damage    = 0;
    float       duration_seconds= 0.0f;
    std::string death_cause     = "";
    std::string created_at      = "";
};

// ── Networking ────────────────────────────────────────────────────────────────
enum class NetworkRole {
    OFFLINE,    // Single-player, no networking
    HOST,       // This client is the authoritative host
    CLIENT,     // Connected to a remote host
    DEDICATED   // Headless server (future)
};

// Compact per-player state broadcast in every snapshot
struct PlayerNetState {
    uint8_t  player_id  = 0;
    float    pos_x      = 450.0f;
    float    pos_y      = 500.0f;
    float    vel_x      = 0.0f;
    float    vel_y      = 0.0f;
    float    angle      = 0.0f;
    int      hp         = 100;
    int      combo      = 0;
    int      score      = 0;
    bool     is_downed  = false;
    bool     is_firing  = false;
    bool     is_dashing = false;
    char     ship_id[16]= "pushpaka";
};

// Client → Host every frame
struct InputPacket {
    uint32_t seq       = 0;
    uint32_t timestamp = 0;    // milliseconds since match start
    float    move_x    = 0.0f;
    float    move_y    = 0.0f;
    float    aim_x     = 0.0f;
    float    aim_y     = 0.0f;
    bool     fire      = false;
    bool     dash      = false;
    bool     astra     = false;
    bool     use_soma  = false;
    bool     use_vajra = false;
    bool     taunt     = false;
    bool     ping_wheel= false;
    uint8_t  ping_type = 0;   // 0=Attack 1=Help 2=Defend 3=Boss
};

// Host → all clients every tick
struct EnemyNetState {
    uint16_t enemy_id  = 0;
    float    pos_x     = 0.0f;
    float    pos_y     = 0.0f;
    int      hp        = 100;
    bool     active    = true;
    bool     is_elite  = false;
};

struct SnapshotPacket {
    uint32_t       tick           = 0;
    PlayerNetState players[4];
    EnemyNetState  enemies[50];
    float          boss_hp        = 0.0f;
    int            boss_phase     = 1;
    int            wave_number    = 1;
    int            team_combo     = 0;
    bool           wave_cleared   = false;
    bool           boss_wave      = false;
};

// Lobby messaging (reliable)
struct LobbyMessage {
    enum class Type : uint8_t {
        JOIN, LEAVE, READY, UNREADY, KICK,
        SHIP_SELECT, START_COUNTDOWN, START_MATCH,
        CHAT, PING_UPDATE
    } type = Type::JOIN;
    uint8_t player_id   = 0;
    char    player_name[32] = {};
    char    ship_id[16]     = {};
    bool    is_ready        = false;
    uint8_t ping_ms         = 0;
    char    room_code[8]    = {};
};

// ── Co-op Astra Types ─────────────────────────────────────────────────────────
enum class CoOpAstraType {
    NONE,
    THUNDER_TEMPEST,  // GARUDA + VAJRA — chain lightning storm
    DIVINE_BARRIER,   // KAMADHENU + TRIPURA — team shield 5s
    SOLAR_INFERNO,    // AGNEYASTRA + SURYA — burning AoE 4s
    STORM_CYCLONE     // INDRA + VAYU — homing tornado 3s
};

// ── Ping Wheel Types ──────────────────────────────────────────────────────────
enum class PingType : uint8_t {
    ATTACK = 0,
    HELP   = 1,
    DEFEND = 2,
    BOSS   = 3,
    FOLLOW = 4,
    WAIT   = 5
};

} // namespace Vimana
