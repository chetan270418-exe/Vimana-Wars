#pragma once
#include <string>
#include <vector>
#include <array>
#include <algorithm>
#include <limits>
#include "raylib.h"
#include "core/constants.hpp"

namespace Vimana {

enum class ShipAbilityType {
    NONE,
    // ── Passive modifiers (applied each frame / on event) ─────────────────────
    DASH_QUICKDRAW,      // Next shot after dash deals +25% dmg
    CADENCE_PIERCE,      // Every Nth shot pierces extra targets
    DASH_DAMAGE,         // Primary shots deal +% dmg while dashing
    PROJECTILE_SPEED,    // Primary shot speed multiplier
    EXTRA_BRAHMASTRA,    // Start with +1 Brahmastra charge
    COMBO_CADENCE,       // Kills extend combo window, add steps
    PRANA_BONUS,         // +% wave-clear prana reward
    // ── Active abilities (triggered on Q, have a cooldown) ─────────────────────
    OVERDRIVE,           // +80% fire rate for 4s
    AEGIS,               // 2-second Kavach invuln bubble
    BLINK,               // Teleport 160px toward crosshair
    NOVA,                // Radial knockback pulse + AoE damage
    REPAIR_AURA,         // Regenerate 30 HP over 4s
    NULL_FIELD,          // Slow all enemy bullets 50% for 5s
    BERSERK,             // Damage scales with missing HP, 5s duration
};

// Passive descriptor (applied by gameplay systems each frame/event)
struct ShipAbility {
    ShipAbilityType type = ShipAbilityType::NONE;
    float magnitude = 0.0f;  // strength / multiplier
    int   cadence   = 0;     // every-N trigger count
    float duration  = 0.0f;  // buff duration for timed effects
};

// Active ability descriptor (key Q, per-ship cooldown)
struct ActiveAbility {
    ShipAbilityType type    = ShipAbilityType::NONE;
    float cooldown          = 0.0f;   // seconds between uses
    float magnitude         = 0.0f;   // strength scalar
    float duration          = 0.0f;   // effect duration in seconds
    std::string name        = {};
    std::string description = {};
};

struct ShipArchetype {
    std::string id;
    std::string name;
    std::string subtitle;
    std::string role;
    int max_hp;
    float speed;
    float shoot_cooldown;
    int bullet_damage;
    int dash_charges;
    float dash_cooldown;
    int unlock_wave;
    int prana_cost;
    std::string sprite_file;
    Color accent_color;
    std::string boss_unlock_id = {};
    std::string boss_unlock_name = {};
    std::string gun_type = "STANDARD"; // STANDARD, BURST, PIERCE, BURN
    std::string ability_name = {};
    std::string ability_description = {};
    ShipAbility ability = {};           // passive ability (always active)
    ActiveAbility active_ability = {}; // active ability (Q key, cooldown)
};

inline int ShipWavePranaReward(const ShipArchetype& ship, int amount) {
    if (amount <= 0) return amount;
    const int bonus_percent = (ship.id == "kubera" || ship.id == "kubera_vault") ? 20 :
        (ship.ability.type == ShipAbilityType::PRANA_BONUS ? static_cast<int>(ship.ability.magnitude) : 0);
    const long long reward = amount + static_cast<long long>(amount) * bonus_percent / 100;
    return static_cast<int>(std::min<long long>(reward, std::numeric_limits<int>::max()));
}

inline const std::array<ShipArchetype, 62> SHIP_FLEET = {{
    // ── TIER 1: STARTER FLEET (Wave 0 — always unlocked) ─────────────────────
    // Pushpaka: balanced — NOVA (small AoE pulse, teaches active mechanic)
    { "pushpaka", "Pushpaka", "Celestial Cruiser", "Balanced", 100, 300.0f, 0.15f, 25, 2, 1.6f, 0, 0, "pushpaka.png", COLOR_GOLD,
      {}, {}, "STANDARD", {}, {},  {},
      { ShipAbilityType::NOVA, 12.0f, 0.6f, 0.0f, "Dharmic Pulse", "Releases a radial energy pulse that damages and knocks back nearby enemies." }
    },
    // Tripura: heavy tank — AEGIS (shield fits the dreadnought archetype)
    { "tripura", "Tripura", "Iron Dreadnought", "Heavy Assault", 160, 240.0f, 0.20f, 38, 1, 2.2f, 0, 0, "tripura.png", COLOR_ORANGE_BRIGHT,
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::AEGIS, 14.0f, 1.0f, 2.0f, "Iron Ward", "Raises an invulnerable Kavach shield for 2 seconds." }
    },
    // Garuda: high agility — OVERDRIVE (speed build, reward fast play)
    { "garuda", "Garuda", "Sky Predator", "High Agility", 80, 380.0f, 0.11f, 18, 3, 1.1f, 0, 0, "garuda.png", COLOR_CYAN_BRIGHT,
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::OVERDRIVE, 12.0f, 1.8f, 4.0f, "Raptor Burst", "+80% fire rate for 4 seconds — unleash the sky predator." }
    },

    // ── TIER 2: EARLY CAMPAIGN (Wave 1-8) ────────────────────────────────────
    { "vajra", "Vajra Spear", "Thunder Interceptor", "Burst", 90, 340.0f, 0.14f, 28, 4, 1.4f, 2, 350, "phase9_commander_ship_01.png", COLOR_CYAN,
      {}, {}, "BURST", {}, {}, {},
      { ShipAbilityType::OVERDRIVE, 11.0f, 1.8f, 4.0f, "Thunder Surge", "Overdrives weapon fire rate by 80% for 4 seconds." }
    },
    { "naga", "Naga Coil", "Venom Infiltrator", "Piercing", 95, 320.0f, 0.13f, 26, 3, 1.5f, 3, 380, "phase9_commander_ship_02.png", COLOR_GREEN_BRIGHT,
      {}, {}, "PIERCE", {}, {}, {},
      { ShipAbilityType::BLINK, 10.0f, 160.0f, 0.0f, "Venom Step", "Instantly teleports 160px toward the crosshair — impossible to track." }
    },
    { "agneyastra", "Agneyastra", "Flame Chariot", "Burn DPS", 110, 290.0f, 0.16f, 32, 2, 1.7f, 4, 420, "phase9_commander_ship_03.png", COLOR_RED_BRIGHT,
      {}, {}, "BURN", {}, {}, {},
      { ShipAbilityType::BERSERK, 11.0f, 1.6f, 5.0f, "Flame Rage", "Damage scales with missing hull — deadlier the more damage you absorb." }
    },
    { "soma", "Soma Ark", "Lunar Sanctuary", "Shielding", 125, 270.0f, 0.18f, 24, 2, 1.8f, 5, 450, "phase9_commander_ship_04.png", COLOR_PURPLE_BRIGHT,
      {}, {}, "STANDARD", "Lunar Aegis", "Automatically raises a brief Kavach shield every fifteen seconds.", {},
      { ShipAbilityType::REPAIR_AURA, 13.0f, 30.0f, 4.0f, "Soma Infusion", "Restores 30 hull integrity over 4 seconds." }
    },
    { "garuda_prime", "Garuda Prime", "Supersonic Astral Interceptor", "Hypersonic Strike", 95, 410.0f, 0.10f, 26, 3, 1.0f, 5, 500, "phase8_wisedawn_shaded_ship_0.png", { 70, 220, 255, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::BLINK, 9.0f, 180.0f, 0.0f, "Hypersonic Step", "Teleports 180px toward the crosshair in a burst of supersonic speed." }
    },
    { "kubera", "Kubera Galleon", "Treasury Citadel", "Wealth & Armor", 140, 250.0f, 0.19f, 34, 1, 2.0f, 6, 480, "phase9_commander_ship_05.png", COLOR_GOLD_BRIGHT,
      {}, {}, "STANDARD", "Divine Treasury", "Earns 20% more Prana from wave-clear rewards.", { ShipAbilityType::PRANA_BONUS, 20.0f },
      { ShipAbilityType::AEGIS, 12.0f, 1.0f, 2.0f, "Vault Shield", "Deploys a 2-second Kavach shield — wealth protects." }
    },
    { "marut", "Marut Striker", "Wind-God Interceptor", "Speed Burst", 85, 420.0f, 0.09f, 20, 4, 0.9f, 7, 520, "phase9_commander_ship_06.png", { 200, 240, 255, 255 },
      {}, {}, "STANDARD", "Gale Launch", "Dashes travel 25% farther.", {},
      { ShipAbilityType::OVERDRIVE, 10.0f, 1.8f, 4.0f, "Gale Overcharge", "80% fire rate burst for 4s — the Wind-God's tempest." }
    },
    { "kinnara", "Kinnara Scout", "Celestial Recon Skiff", "Recon & Evade", 78, 400.0f, 0.12f, 22, 3, 1.1f, 8, 540, "phase9_commander_ship_07.png", { 230, 200, 255, 255 },
      {}, {}, "STANDARD", "Slipstream Veil", "Dashes grant an extra 0.25 seconds of invulnerability.", {},
      { ShipAbilityType::BLINK, 10.0f, 160.0f, 0.0f, "Ghost Step", "Phase-steps 160px instantly — the scout vanishes before reappearing." }
    },

    // ── TIER 3: MID CAMPAIGN (Wave 9-15) ─────────────────────────────────────
    { "surya", "Surya Flare", "Solar Vanguard", "Radiant Beam", 105, 330.0f, 0.14f, 30, 2, 1.5f, 9, 560, "phase9_commander_ship_08.png", COLOR_GOLD_BRIGHT,
      {}, {}, "STANDARD", "Radiant Pierce", "Every seventh primary shot pierces hostile craft.", {},
      { ShipAbilityType::OVERDRIVE, 11.0f, 1.8f, 4.0f, "Solar Flare Burst", "Solar overcharge doubles fire rate for 4 seconds." }
    },
    { "agni_mk2", "Agni Mk-II", "Inferno Chariot", "Heavy Burn", 130, 280.0f, 0.17f, 36, 2, 1.6f, 10, 580, "phase9_commander_ship_09.png", { 255, 80, 0, 255 },
      {}, {}, "BURN", "Furnace Array", "Fires a twin-shot flame spread.", {},
      { ShipAbilityType::BERSERK, 10.0f, 1.7f, 5.0f, "Inferno Rage", "Hull damage boosts weapon power — burns hotter when hit." }
    },
    { "varuna_void", "Varuna Stealth", "Forward-Swept Wing Infiltrator", "Stealth Criticals", 120, 350.0f, 0.12f, 34, 3, 1.2f, 10, 600, "phase8_wisedawn_shaded_ship_2.png", { 150, 110, 255, 255 },
      {}, {}, "STANDARD", "Eclipse Thread", "Every fifth primary shot pierces through three additional targets.", { ShipAbilityType::CADENCE_PIERCE, 3.0f, 5 },
      { ShipAbilityType::NULL_FIELD, 12.0f, 0.5f, 5.0f, "Void Shroud", "Slows all enemy projectiles by 50% for 5 seconds." }
    },
    { "tripura_mk2", "Tripura Dread-Assault", "Twin-Hull Heavy Gunship", "Heavy Barrage", 220, 250.0f, 0.16f, 42, 2, 1.9f, 11, 640, "phase8_wisedawn_shaded_ship_1.png", { 255, 140, 40, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::AEGIS, 12.0f, 1.0f, 2.5f, "Dread Ward", "Twin-hull raises a reinforced Kavach shield for 2.5 seconds." }
    },
    { "vata", "Vata Skyrider", "Storm-God Light Fighter", "Agile Striker", 88, 395.0f, 0.11f, 24, 3, 1.0f, 11, 620, "phase9_commander_ship_10.png", { 180, 230, 255, 255 },
      {}, {}, "STANDARD", "Skyline Quickdraw", "Dashing primes your next primary shot for 25% bonus damage.", { ShipAbilityType::DASH_QUICKDRAW, 1.25f },
      { ShipAbilityType::BLINK, 9.0f, 160.0f, 0.0f, "Storm Step", "Blinks 160px toward target — the storm-god moves like lightning." }
    },
    { "yamaduta", "Yamaduta", "Death-Messenger Gunship", "Execute", 115, 305.0f, 0.15f, 33, 2, 1.5f, 12, 660, "phase9_commander_ship_11.png", { 140, 40, 200, 255 },
      {}, {}, "STANDARD", "Final Decree", "Every fifth primary shot deals 45% bonus damage.", {},
      { ShipAbilityType::BERSERK, 10.0f, 1.8f, 5.0f, "Death Sentence", "Weapon damage amplified by missing hull — the messenger delivers final judgment." }
    },
    { "airavata", "Airavata", "Indra's Celestial Elephant", "Tank Bastion", 300, 200.0f, 0.22f, 48, 1, 2.8f, 12, 700, "airavata.png", { 180, 210, 255, 255 },
      {}, {}, "STANDARD", "Thunderhead Bastion", "Reduces incoming hull damage by 15%.", {},
      { ShipAbilityType::AEGIS, 13.0f, 1.0f, 3.0f, "Elephant Aegis", "Raises a 3-second Kavach shield — the elephant's hide is impenetrable." }
    },
    { "dhanvantari", "Dhanvantari", "Divine Physician Ark", "Sustain Support", 135, 275.0f, 0.18f, 22, 2, 1.7f, 13, 680, "phase9_commander_ship_12.png", { 100, 255, 160, 255 },
      {}, {}, "STANDARD", "Healing Current", "Restores 4 hull integrity per second while damaged.", {},
      { ShipAbilityType::REPAIR_AURA, 11.0f, 40.0f, 4.0f, "Divine Infusion", "Restores 40 hull instantly over 4 seconds — the physician heals in battle." }
    },
    { "indra_rider", "Indra's Chariot", "Thousand-Eyed War Platform", "AoE Dominance", 145, 285.0f, 0.16f, 35, 2, 1.6f, 13, 720, "phase9_commander_ship_13.png", { 100, 180, 255, 255 },
      {}, {}, "STANDARD", "Sudarshana Orbitals", "Chakrams split into three lower-damage orbitals.", {},
      { ShipAbilityType::NOVA, 11.0f, 0.8f, 0.0f, "Indra's Thunder", "A thunderous radial pulse blasts enemies in all directions." }
    },
    { "varaha", "Varaha Boar", "Earth-Upheaval Siege Ship", "Slam & Shield", 175, 245.0f, 0.20f, 44, 1, 2.3f, 14, 740, "phase9_commander_ship_14.png", { 140, 200, 80, 255 },
      {}, {}, "STANDARD", "Earth-Upheaval Dash", "Each successful dash grants a brief Kavach shield.", {},
      { ShipAbilityType::NOVA, 10.0f, 1.0f, 0.0f, "Tusk Slam", "A massive earth-shattering shockwave knocks back and damages all nearby enemies." }
    },
    { "matsya", "Matsya Leviathan", "World-Flood Cruiser", "Flood Suppression", 150, 270.0f, 0.17f, 38, 2, 1.8f, 15, 760, "phase9_commander_ship_15.png", { 0, 160, 220, 255 },
      {}, {}, "STANDARD", "Leviathan's Wake", "Slowly restores hull and launches a heavier Chakram.", { ShipAbilityType::PROJECTILE_SPEED, 1.3f, 0, 0.0f },
      { ShipAbilityType::REPAIR_AURA, 12.0f, 35.0f, 4.0f, "Flood Heal", "Tidal energies restore 35 hull integrity over 4 seconds." }
    },

    // ── TIER 4: LATE CAMPAIGN (Wave 16-22) ───────────────────────────────────
    { "kamadhenu", "Kamadhenu", "Divine Sustenance Vessel", "Support Sustain", 130, 290.0f, 0.17f, 22, 2, 1.6f, 16, 780, "kamadhenu.png", { 130, 255, 190, 255 },
      {}, {}, "STANDARD", "Sustenance Field", "Repairs hull integrity gradually during combat.", {},
      { ShipAbilityType::REPAIR_AURA, 10.0f, 45.0f, 4.0f, "Wish-Cow Blessing", "Fully restores 45 HP over 4 seconds — Kamadhenu grants wishes." }
    },
    { "kurma", "Kurma Shell", "World-Turtle Fortress", "Fortress Tank", 320, 195.0f, 0.23f, 50, 1, 2.9f, 16, 800, "phase9_commander_ship_16.png", { 80, 160, 100, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::AEGIS, 11.0f, 1.0f, 3.5f, "Turtle Shell", "Retracts into a 3.5-second impenetrable Kavach shield." }
    },
    { "vimana_mk3", "Vimana Mk-III", "Third-Eye Combat Cruiser", "Versatile Elite", 160, 310.0f, 0.14f, 38, 2, 1.5f, 17, 820, "phase9_commander_ship_17.png", { 255, 200, 60, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::OVERDRIVE, 10.0f, 1.8f, 4.0f, "Combat Surge", "Elite overcharge grants 80% fire rate for 4 seconds." }
    },
    { "brahma_ark", "Brahma Leviathan", "Vedic Capital Airship", "Titan Airship", 350, 210.0f, 0.18f, 50, 1, 2.5f, 18, 860, "phase8_wisedawn_shaded_ship_3.png", { 255, 215, 60, 255 },
      {}, {}, "STANDARD", "Creation's Arsenal", "Deploys with one additional Brahmastra charge.", { ShipAbilityType::EXTRA_BRAHMASTRA, 1.0f },
      { ShipAbilityType::NOVA, 10.0f, 1.2f, 0.0f, "Brahma's Wrath", "The Creator unleashes a world-shattering radial pulse." }
    },
    { "chakravyuha", "Chakravyuha", "Inescapable Formation Ship", "Tactical Lock", 165, 295.0f, 0.15f, 36, 2, 1.6f, 18, 880, "phase9_commander_ship_18.png", { 255, 130, 200, 255 },
      {}, {}, "STANDARD", "Convergence Volley", "Every fifth primary shot releases a three-way convergence volley.", {},
      { ShipAbilityType::NULL_FIELD, 11.0f, 0.5f, 5.0f, "Formation Lock", "All enemy projectiles slowed 50% for 5 seconds — the formation holds." }
    },
    { "ketu_shadow", "Ketu Shadow", "Descending Node Phantom", "Shadow Strike", 110, 365.0f, 0.11f, 32, 3, 1.2f, 19, 900, "phase9_commander_ship_19.png", { 80, 60, 160, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::BLINK, 8.0f, 200.0f, 0.0f, "Shadow Phase", "Phases 200px toward crosshair — the descending node cannot be caught." }
    },
    { "rahu_devour", "Rahu Devourer", "Ascending Eclipse Destroyer", "Null-Field", 200, 265.0f, 0.16f, 42, 2, 1.7f, 19, 920, "phase9_commander_ship_20.png", { 40, 20, 100, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::NULL_FIELD, 10.0f, 0.5f, 6.0f, "Eclipse Null-Field", "Rahu devours all enemy bullets — slows projectiles 50% for 6 seconds." }
    },
    { "ananta", "Ananta Serpent", "Cosmic Serpent Dreadnought", "Infinite Fury", 190, 275.0f, 0.15f, 44, 2, 1.7f, 20, 940, "phase9_commander_ship_21.png", { 60, 200, 120, 255 },
      {}, {}, "STANDARD", "Endless Cadence", "Kills add two combo steps and extend the combo window to four seconds.", { ShipAbilityType::COMBO_CADENCE, 1.0f, 0, 4.0f },
      { ShipAbilityType::BERSERK, 10.0f, 1.9f, 5.0f, "Serpent's Fury", "Infinite serpent rage — damage rises to 90% boost at low hull." }
    },
    { "garuda_apex", "Garuda Apex", "Apex Predator Warbird", "Terminal Strike", 105, 430.0f, 0.09f, 30, 4, 0.8f, 20, 960, "phase9_commander_ship_22.png", { 0, 255, 240, 255 },
      {}, {}, "STANDARD", "Predator's Pass", "Piercing shots pass through additional hostile craft.", {},
      { ShipAbilityType::OVERDRIVE, 9.0f, 1.8f, 4.0f, "Apex Predator", "Terminal overcharge — 80% fire rate for 4 seconds at the kill zone." }
    },
    { "kalki_vimana", "Kalki Vimana", "Tenth Avatar Warship", "Prophetic Blade", 120, 380.0f, 0.12f, 36, 3, 1.2f, 21, 980, "phase9_commander_ship_23.png", { 255, 255, 200, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::BLINK, 9.0f, 180.0f, 0.0f, "Avatar's Leap", "The tenth avatar leaps 180px to deliver the prophetic strike." }
    },
    { "vishnu_disc", "Vishnu Disc", "Sudarshana Orbital Platform", "Orbital Strike", 155, 320.0f, 0.13f, 40, 2, 1.5f, 21, 1000, "phase9_commander_ship_24.png", { 60, 130, 255, 255 },
      {}, {}, "STANDARD", "Sudarshana Orbitals", "Chakrams split into three lower-damage orbitals.", {},
      { ShipAbilityType::NOVA, 10.0f, 1.0f, 0.0f, "Sudarshana Spin", "The Sudarshana Chakra spins outward — radial damage blast." }
    },
    { "shiva_eye", "Shiva's Eye", "Third-Eye Annihilator", "Destruction Nova", 145, 330.0f, 0.12f, 42, 2, 1.4f, 22, 1050, "phase9_commander_ship_25.png", { 200, 60, 60, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::NOVA, 9.0f, 1.5f, 0.0f, "Third Eye Opens", "Shiva's third eye unleashes a devastating radial annihilation wave." }
    },

    // ── TIER 5: ENDGAME FLEET (Wave 23-28) ───────────────────────────────────
    { "rudra_bomber", "Rudra Striker", "Delta-Wing Astral Bomber", "Plasma Demolition", 140, 310.0f, 0.14f, 38, 2, 1.5f, 23, 1100, "phase8_wisedawn_shaded_ship_4.png", { 255, 60, 80, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::NOVA, 9.0f, 1.3f, 0.0f, "Plasma Detonation", "Drops a radial plasma bomb that demolishes grouped enemies." }
    },
    { "skanda_lance", "Skanda Lance", "War-God Six-Faced Speeder", "Multi-Pierce", 115, 375.0f, 0.11f, 35, 3, 1.1f, 23, 1100, "phase9_commander_ship_26.png", { 255, 200, 80, 255 },
      {}, {}, "PIERCE", {}, {}, {},
      { ShipAbilityType::OVERDRIVE, 9.0f, 1.8f, 4.0f, "Six-Faced Barrage", "War-God fires on six fronts — 80% fire rate for 4 seconds." }
    },
    { "durga_fortress", "Durga Fortress", "Nine-Power Siege Platform", "Nine-Aspect Wall", 250, 230.0f, 0.19f, 52, 1, 2.5f, 24, 1150, "phase9_commander_ship_27.png", { 255, 140, 60, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::AEGIS, 10.0f, 1.0f, 3.0f, "Nine-Aspect Shield", "Durga's nine-fold power raises a 3-second Kavach fortress." }
    },
    { "lakshmi_grace", "Lakshmi Grace", "Prosperity Aura Cruiser", "Wealth Shield", 170, 280.0f, 0.17f, 30, 2, 1.7f, 24, 1150, "phase9_commander_ship_28.png", { 255, 220, 150, 255 },
      {}, {}, "STANDARD", "Fortune's Grace", "Earns 15% more Prana from wave-clear rewards.", { ShipAbilityType::PRANA_BONUS, 15.0f },
      { ShipAbilityType::REPAIR_AURA, 10.0f, 45.0f, 4.0f, "Lakshmi's Blessing", "Prosperity heals the ship — 45 HP restored over 4 seconds." }
    },
    { "hanuman_fist", "Hanuman Fist", "Devotion Strike Warship", "Raging Loyalty", 210, 300.0f, 0.14f, 48, 2, 1.5f, 25, 1200, "phase9_commander_ship_29.png", { 255, 140, 0, 255 },
      {}, {}, "STANDARD", "Devotion Surge", "Primary shots deal 35% more damage while dashing.", { ShipAbilityType::DASH_DAMAGE, 1.35f },
      { ShipAbilityType::BERSERK, 9.0f, 2.0f, 5.0f, "Devotion Rage", "Hanuman's rage amplifies damage 100% at zero hull — unstoppable." }
    },
    { "saraswati_arc", "Saraswati Arc", "Knowledge-Current Resonator", "Resonance Burst", 130, 335.0f, 0.12f, 34, 3, 1.3f, 25, 1200, "phase9_commander_ship_30.png", { 200, 180, 255, 255 },
      {}, {}, "STANDARD", "Resonant Velocity", "Primary shots travel 30% faster.", { ShipAbilityType::PROJECTILE_SPEED, 1.3f },
      { ShipAbilityType::NULL_FIELD, 10.0f, 0.5f, 5.0f, "Knowledge Disruption", "Saraswati's knowledge field unravels enemy projectile logic for 5 seconds." }
    },
    { "kali_storm", "Kali Storm", "Time-Destroyer Battlerider", "Chaos Cascade", 160, 360.0f, 0.10f, 46, 3, 1.0f, 26, 1250, "phase9_commander_ship_31.png", { 80, 0, 120, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::BERSERK, 9.0f, 2.0f, 5.0f, "Kali's Fury", "Time-destroyer mode — damage amplified 100% at critical hull." }
    },
    { "yama_throne", "Yama Throne", "Death-God Judgment Carrier", "Judgment Beam", 230, 245.0f, 0.18f, 55, 1, 2.2f, 26, 1250, "phase9_commander_ship_32.png", { 60, 0, 80, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::NOVA, 9.0f, 1.4f, 0.0f, "Judgment Decree", "Death's judgment radiates outward — all nearby enemies are condemned." }
    },
    { "kubera_vault", "Kubera Vault", "Celestial Treasury Titan", "Hoard & Barrage", 280, 220.0f, 0.20f, 52, 1, 2.3f, 27, 1300, "phase9_commander_ship_33.png", { 220, 180, 0, 255 },
      {}, {}, "STANDARD", "Divine Treasury", "Earns 20% more Prana from wave-clear rewards.", { ShipAbilityType::PRANA_BONUS, 20.0f },
      { ShipAbilityType::AEGIS, 11.0f, 1.0f, 3.0f, "Vault Lockdown", "The treasury vault locks — impenetrable Kavach shield for 3 seconds." }
    },
    { "vayu_cyclone", "Vayu Cyclone", "Wind-Storm Hypercruiser", "Vortex Control", 140, 400.0f, 0.10f, 32, 4, 0.9f, 27, 1300, "phase9_commander_ship_34.png", { 180, 255, 240, 255 },
      {}, {}, "STANDARD", "Cyclone Cadence", "Every fourth primary shot releases a three-way wind burst.", {},
      { ShipAbilityType::BLINK, 8.0f, 200.0f, 0.0f, "Cyclone Dash", "Vayu's cyclone carries the ship 200px in a vortex blink." }
    },
    { "brahmastra_mk1", "Brahmastra Mk-I", "Celestial Weapon Platform", "Cosmic Nuke", 190, 290.0f, 0.15f, 50, 2, 1.5f, 28, 1350, "phase9_commander_ship_35.png", { 255, 240, 100, 255 },
      {}, {}, "STANDARD", "Creation's Arsenal", "Deploys with one additional Brahmastra charge.", { ShipAbilityType::EXTRA_BRAHMASTRA, 1.0f },
      { ShipAbilityType::OVERDRIVE, 9.0f, 1.8f, 4.0f, "Brahma Weapon Online", "The celestial weapon platform fires at maximum capacity for 4 seconds." }
    },

    // ── TIER 6: ULTIMATE FLEET (Wave 29-30 & Secret) ─────────────────────────
    { "narasimha", "Narasimha", "Avatar of Ferocious Righteousness", "Ultimate Berserker", 150, 360.0f, 0.09f, 55, 3, 0.9f, 29, 1400, "narasimha.png", { 255, 90, 30, 255 },
      {}, {}, "STANDARD", "Righteous Fury", "Weapon damage rises as hull integrity falls.", {},
      { ShipAbilityType::BERSERK, 8.0f, 2.0f, 5.0f, "Avatar Berserker", "At zero hull: damage doubles — Narasimha cannot be contained." }
    },
    { "sudarshana_neo", "Sudarshana Neo", "Advanced Cybernetic Flagship", "Omni-Vanguard", 180, 370.0f, 0.08f, 48, 4, 0.9f, 29, 1400, "phase8_wisedawn_shaded_ship_5.png", { 0, 255, 210, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::OVERDRIVE, 8.0f, 1.8f, 5.0f, "Neo Overcharge", "The cybernetic flagship pushes all weapons to maximum for 5 seconds." }
    },
    { "parasurama", "Parashurama", "Axe-God Destroyer", "Warrior Avatar", 200, 340.0f, 0.11f, 58, 2, 1.3f, 30, 1500, "phase9_commander_ship_36.png", { 180, 100, 0, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::BERSERK, 8.0f, 2.0f, 5.0f, "Axe Rage", "The destroyer's axe fuels berserker rage — max damage at low hull." }
    },
    { "rama_vimana", "Rama Vimana", "Righteous King's Warship", "Honor Blade", 175, 345.0f, 0.11f, 52, 3, 1.1f, 30, 1500, "phase9_commander_ship_37.png", { 60, 200, 80, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::AEGIS, 9.0f, 1.0f, 3.0f, "Dharma Shield", "Rama's righteousness manifests as a 3-second divine shield." }
    },
    { "krishna_disc", "Krishna Disc", "Flute-Song Battle Platform", "Divine Play", 185, 355.0f, 0.10f, 54, 3, 1.0f, 30, 1500, "phase9_commander_ship_38.png", { 50, 80, 200, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::BLINK, 8.0f, 200.0f, 0.0f, "Lila Step", "Krishna's divine play — blinks 200px to where the enemy least expects." }
    },
    { "vishnu_prime", "Vishnu Prime", "Preserver's Ultimate Form", "Cosmic Preservation", 220, 330.0f, 0.10f, 60, 2, 1.2f, 30, 1600, "phase9_commander_ship_39.png", { 40, 120, 255, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::REPAIR_AURA, 9.0f, 60.0f, 4.0f, "Cosmic Preservation", "Vishnu preserves — restores 60 hull integrity over 4 seconds." }
    },
    { "shiva_ultimate", "Shiva Ultimate", "Destroyer's Transcendent Form", "Tandava Annihilation", 240, 340.0f, 0.09f, 65, 3, 1.0f, 30, 1600, "phase9_commander_ship_40.png", { 220, 50, 50, 255 },
      {}, {}, "STANDARD", {}, {}, {},
      { ShipAbilityType::NOVA, 8.0f, 2.0f, 0.0f, "Tandava Dance", "Shiva's cosmic dance unleashes the most powerful radial annihilation in the fleet." }
    },

    // ── TIER 7: LATE-ACT COMMISSIONED FLEET (Wave 35+) ──────────────────────
    { "amogha_lancer", "Amogha Lancer", "Long-range astral interceptor", "Precision Piercing", 155, 355.0f, 0.11f, 48, 3, 1.05f, 35, 1750, "phase9_commander_ship_49.png", COLOR_CYAN_BRIGHT,
      {}, {}, "PIERCE", "Needle Thread", "Every fifth primary shot gains bonus damage and pierces up to eight targets.", { ShipAbilityType::CADENCE_PIERCE, 8.0f, 5 },
      { ShipAbilityType::OVERDRIVE, 9.0f, 1.8f, 4.0f, "Amogha Overcharge", "Long-range overcharge — 80% fire rate at maximum precision." }
    },
    { "nandi_aegis", "Nandi Aegis", "Armored command escort", "Heavy Burst", 300, 235.0f, 0.18f, 52, 1, 2.1f, 50, 1950, "phase9_commander_ship_50.png", COLOR_GOLD_BRIGHT,
      {}, {}, "BURST", "Living Aegis", "Automatically raises a Kavach shield for two seconds every ten seconds.", {},
      { ShipAbilityType::AEGIS, 10.0f, 1.0f, 3.5f, "Sacred Aegis", "Nandi's sacred armor — raises an impenetrable 3.5-second Kavach shield." }
    },

    // ── TIER 8: BOSS-SALVAGED SIGNATURE FLEET ────────────────────────────────
    { "kumbha_titan", "Kumbha Titan", "Siege hull forged from the Slumbering Colossus", "Boss Breaker / Heavy", 390, 205.0f, 0.19f, 61, 1, 2.4f, 999999, 0, "phase9_commander_ship_41.png", { 255, 145, 70, 255 },
      "KUMBHAKARNA", "TITAN KUMBHAKARNA", "STANDARD", {}, {}, {},
      { ShipAbilityType::BERSERK, 8.0f, 2.0f, 5.0f, "Colossus Rampage", "The titan's hull fuels fury — maximum damage boost at critical integrity." }
    },
    { "ravana_dasha", "Dasha Vimana", "Tenfold imperial weapons platform", "Boss Breaker / Barrage", 250, 315.0f, 0.12f, 51, 2, 1.4f, 999999, 0, "phase9_commander_ship_42.png", { 255, 65, 80, 255 },
      "RAVANA", "EMPEROR RAVANA", "STANDARD", {}, {}, {},
      { ShipAbilityType::OVERDRIVE, 8.0f, 1.8f, 5.0f, "Ten-Head Barrage", "Ten heads fire simultaneously — 80% fire rate for 5 seconds." }
    },
    { "mahisha_rush", "Mahisha Ram", "Armored charge interceptor", "Boss Breaker / Assault", 310, 285.0f, 0.15f, 58, 2, 1.7f, 999999, 0, "phase9_commander_ship_43.png", { 255, 115, 60, 255 },
      "MAHISHASURA", "WARLORD MAHISHASURA", "STANDARD", {}, {}, {},
      { ShipAbilityType::NOVA, 8.0f, 1.8f, 0.0f, "Bull Charge", "Mahisha charges — an armored shockwave destroys everything in range." }
    },
    { "makara_abyss", "Makara Abyssal", "Tidal shield cruiser recovered from the deep", "Boss Breaker / Sustain", 330, 260.0f, 0.17f, 45, 2, 1.6f, 999999, 0, "phase9_commander_ship_44.png", { 60, 225, 255, 255 },
      "MAKARA", "MAKARA, ABYSSAL LEVIATHAN", "STANDARD", {}, {}, {},
      { ShipAbilityType::REPAIR_AURA, 9.0f, 80.0f, 4.0f, "Abyssal Regeneration", "Tidal energies restore 80 hull integrity over 4 seconds." }
    },
    { "indra_mirage", "Indrajit's Mirage", "Phase-shift strike craft", "Boss Breaker / Evasion", 205, 390.0f, 0.095f, 42, 4, 0.85f, 999999, 0, "phase9_commander_ship_45.png", { 190, 100, 255, 255 },
      "INDRAJIT", "CONQUEROR INDRAJIT", "STANDARD", {}, {}, {},
      { ShipAbilityType::BLINK, 7.0f, 240.0f, 0.0f, "Vanish & Strike", "Indrajit vanishes and reappears 240px away — impossible to track." }
    },
    { "hiranya_aegis", "Hiranya Aegis", "Immortal pact fortress vessel", "Boss Breaker / Aegis", 430, 225.0f, 0.18f, 58, 1, 2.3f, 999999, 0, "phase9_commander_ship_46.png", { 255, 220, 85, 255 },
      "HIRANYAKASHIPU", "TYRANT HIRANYAKASHIPU", "STANDARD", {}, {}, {},
      { ShipAbilityType::AEGIS, 9.0f, 1.0f, 4.0f, "Immortal Pact", "Hiranyakashipu's pact — a 4-second invulnerability boon." }
    },
    { "megha_tempest", "Meghnada Tempest", "Lightning grid assault carrier", "Boss Breaker / Storm", 260, 360.0f, 0.105f, 50, 3, 1.1f, 999999, 0, "phase9_commander_ship_47.png", { 180, 120, 255, 255 },
      "MEGHNADA", "MEGHNADA, STORM ILLUSIONIST", "STANDARD", {}, {}, {},
      { ShipAbilityType::NULL_FIELD, 9.0f, 0.5f, 6.0f, "Lightning Null", "Storm energy nullifies enemy projectiles — slowed 50% for 6 seconds." }
    },
    { "vritra_skyseal", "Vritra Skyseal", "Storm-severing bastion fighter", "Boss Breaker / Control", 360, 275.0f, 0.16f, 56, 2, 1.8f, 999999, 0, "phase9_commander_ship_48.png", { 75, 220, 235, 255 },
      "VRITRA", "VRITRA, SKY-SEALING SERPENT", "STANDARD", {}, {}, {},
      { ShipAbilityType::NULL_FIELD, 9.0f, 0.5f, 7.0f, "Sky Seal", "Vritra seals the sky — enemy projectiles slowed 50% for 7 seconds." }
    }
}};


inline const ShipArchetype* GetShipArchetype(const std::string& id) {
    for (const auto& ship : SHIP_FLEET) {
        if (ship.id == id) return &ship;
    }
    return &SHIP_FLEET[0];
}

inline std::string ShipSignatureName(const ShipArchetype& ship) {
    if (!ship.ability_name.empty()) return ship.ability_name;
    if (ship.id == "pushpaka") return "Kavach Ward";
    if (ship.id == "kamadhenu") return "Sustenance Field";
    if (ship.id == "dhanvantari") return "Healing Current";
    if (ship.id == "soma") return "Lunar Aegis";
    if (ship.id == "surya") return "Radiant Pierce";
    if (ship.id == "varaha") return "Earth-Upheaval Dash";
    if (ship.id == "kubera" || ship.id == "kubera_vault") return "Divine Treasury";
    if (ship.id == "narasimha") return "Righteous Fury";
    if (ship.id == "tripura") return "Dreadnought Salvo";
    if (ship.id == "garuda" || ship.id == "garuda_prime" || ship.id == "garuda_apex") return "Predator's Pass";
    if (ship.id == "marut") return "Gale Launch";
    if (ship.id == "kinnara") return "Slipstream Veil";
    if (ship.id == "airavata") return "Thunderhead Bastion";
    if (ship.id == "yamaduta") return "Final Decree";
    if (ship.id == "matsya") return "Leviathan's Wake";
    if (ship.id == "vishnu_disc") return "Sudarshana Orbitals";
    if (ship.id == "chakravyuha") return "Convergence Volley";
    if (ship.id == "vayu_cyclone") return "Cyclone Cadence";
    if (ship.id == "agni_mk2") return "Furnace Array";
    if (ship.gun_type == "BURST") return "Storm Salvo";
    if (ship.gun_type == "PIERCE") return "Astral Lance";
    if (ship.gun_type == "BURN") return "Agni Fan";
    return ship.role + " Doctrine";
}

inline std::string ShipSignatureDescription(const ShipArchetype& ship) {
    if (!ship.ability_description.empty()) return ship.ability_description;
    if (ship.id == "pushpaka") return "Periodically generates a short-lived automatic Kavach shield.";
    if (ship.id == "kamadhenu") return "Repairs hull integrity gradually during combat.";
    if (ship.id == "dhanvantari") return "Restores 4 hull integrity per second while damaged.";
    if (ship.id == "soma") return "Automatically raises a brief Kavach shield every fifteen seconds.";
    if (ship.id == "surya") return "Every seventh primary shot pierces hostile craft.";
    if (ship.id == "varaha") return "Each successful dash grants a brief Kavach shield.";
    if (ship.id == "kubera" || ship.id == "kubera_vault") return "Earns 20% more Prana from wave-clear rewards.";
    if (ship.id == "narasimha") return "Weapon damage rises as hull integrity falls.";
    if (ship.id == "tripura") return "Fires a three-projectile heavy spread.";
    if (ship.id == "garuda" || ship.id == "garuda_prime" || ship.id == "garuda_apex") return "Piercing shots pass through additional hostile craft.";
    if (ship.id == "marut") return "Dashes travel 25% farther.";
    if (ship.id == "kinnara") return "Dashes grant an extra 0.25 seconds of invulnerability.";
    if (ship.id == "airavata") return "Reduces incoming hull damage by 15%.";
    if (ship.id == "yamaduta") return "Every fifth primary shot deals 45% bonus damage.";
    if (ship.id == "matsya") return "Slowly restores hull and launches a heavier Chakram.";
    if (ship.id == "vishnu_disc") return "Chakrams split into three lower-damage orbitals.";
    if (ship.id == "chakravyuha") return "Every fifth primary shot releases a three-way convergence volley.";
    if (ship.id == "vayu_cyclone") return "Every fourth primary shot releases a three-way wind burst.";
    if (ship.id == "agni_mk2") return "Fires a twin-shot flame spread.";
    if (ship.gun_type == "BURST") return "Fires a tight four-shot burst.";
    if (ship.gun_type == "PIERCE") return "Fires a fast, long-range penetrating shot.";
    if (ship.gun_type == "BURN") return "Fires a twin-shot flame spread.";
    return "A role-tuned hull, speed, and weapon profile.";
}

} // namespace Vimana
