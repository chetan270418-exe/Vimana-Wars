#pragma once
#include <string>
#include <vector>
#include <array>
#include "raylib.h"
#include "core/constants.hpp"

namespace Vimana {

struct ShipArchetype {
    std::string id;
    std::string name;
    std::string subtitle;
    std::string role; // Balanced, Tank, Vanguard, Piercing, Support, Ultimate
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
};

inline const std::array<ShipArchetype, 60> SHIP_FLEET = {{
    // ── TIER 1: STARTER FLEET (Wave 0 — always unlocked) ─────────────────────
    { "pushpaka",    "Pushpaka",      "Celestial Cruiser",             "Balanced",        100, 300.0f, 0.15f, 25, 2, 1.6f,  0, 0,    "pushpaka.png",                    COLOR_GOLD },
    { "tripura",     "Tripura",       "Iron Dreadnought",              "Heavy Assault",   160, 240.0f, 0.20f, 38, 1, 2.2f,  0, 0,    "tripura.png",                     COLOR_ORANGE_BRIGHT },
    { "garuda",      "Garuda",        "Sky Predator",                  "High Agility",     80, 380.0f, 0.11f, 18, 3, 1.1f,  0, 0,    "garuda.png",                      COLOR_CYAN_BRIGHT },

    // ── TIER 2: EARLY CAMPAIGN (Wave 1-8) ────────────────────────────────────
    { "vajra",       "Vajra Spear",   "Thunder Interceptor",           "Burst",            90, 340.0f, 0.14f, 28, 2, 1.4f,  2, 350,  "phase9_commander_ship_01.png",    COLOR_CYAN },
    { "naga",        "Naga Coil",     "Venom Infiltrator",             "Piercing",         95, 320.0f, 0.13f, 26, 2, 1.5f,  3, 380,  "phase9_commander_ship_02.png",    COLOR_GREEN_BRIGHT },
    { "agneyastra",  "Agneyastra",    "Flame Chariot",                 "Burn DPS",        110, 290.0f, 0.16f, 32, 2, 1.7f,  4, 420,  "phase9_commander_ship_03.png",    COLOR_RED_BRIGHT },
    { "soma",        "Soma Ark",      "Lunar Sanctuary",               "Shielding",       125, 270.0f, 0.18f, 24, 2, 1.8f,  5, 450,  "phase9_commander_ship_04.png",    COLOR_PURPLE_BRIGHT },
    { "garuda_prime","Garuda Prime",  "Supersonic Astral Interceptor", "Hypersonic Strike", 95, 410.0f, 0.10f, 26, 3, 1.0f, 5, 500,  "phase8_wisedawn_shaded_ship_0.png",{ 70, 220, 255, 255 } },
    { "kubera",      "Kubera Galleon","Treasury Citadel",              "Wealth & Armor",  140, 250.0f, 0.19f, 34, 1, 2.0f,  6, 480,  "phase9_commander_ship_05.png",    COLOR_GOLD_BRIGHT },
    { "marut",       "Marut Striker", "Wind-God Interceptor",          "Speed Burst",      85, 420.0f, 0.09f, 20, 4, 0.9f,  7, 520,  "phase9_commander_ship_06.png",    { 200, 240, 255, 255 } },
    { "kinnara",     "Kinnara Scout", "Celestial Recon Skiff",         "Recon & Evade",    78, 400.0f, 0.12f, 22, 3, 1.1f,  8, 540,  "phase9_commander_ship_07.png",    { 230, 200, 255, 255 } },

    // ── TIER 3: MID CAMPAIGN (Wave 9-15) ─────────────────────────────────────
    { "surya",       "Surya Flare",   "Solar Vanguard",                "Radiant Beam",    105, 330.0f, 0.14f, 30, 2, 1.5f,  9, 560,  "phase9_commander_ship_08.png",    COLOR_GOLD_BRIGHT },
    { "agni_mk2",    "Agni Mk-II",    "Inferno Chariot",               "Heavy Burn",      130, 280.0f, 0.17f, 36, 2, 1.6f, 10, 580,  "phase9_commander_ship_09.png",    { 255, 80, 0, 255 } },
    { "varuna_void", "Varuna Stealth","Forward-Swept Wing Infiltrator","Stealth Criticals",120, 350.0f, 0.12f, 34, 3, 1.2f, 10, 600,  "phase8_wisedawn_shaded_ship_2.png",{ 150, 110, 255, 255 } },
    { "tripura_mk2", "Tripura Dread-Assault","Twin-Hull Heavy Gunship","Heavy Barrage",   220, 250.0f, 0.16f, 42, 2, 1.9f, 11, 640,  "phase8_wisedawn_shaded_ship_1.png",{ 255, 140, 40, 255 } },
    { "vata",        "Vata Skyrider", "Storm-God Light Fighter",       "Agile Striker",    88, 395.0f, 0.11f, 24, 3, 1.0f, 11, 620,  "phase9_commander_ship_10.png",    { 180, 230, 255, 255 } },
    { "yamaduta",    "Yamaduta",      "Death-Messenger Gunship",       "Execute",         115, 305.0f, 0.15f, 33, 2, 1.5f, 12, 660,  "phase9_commander_ship_11.png",    { 140, 40, 200, 255 } },
    { "airavata",    "Airavata",      "Indra's Celestial Elephant",    "Tank Bastion",    300, 200.0f, 0.22f, 48, 1, 2.8f, 12, 700,  "airavata.png",                    { 180, 210, 255, 255 } },
    { "dhanvantari", "Dhanvantari",   "Divine Physician Ark",          "Sustain Support", 135, 275.0f, 0.18f, 22, 2, 1.7f, 13, 680,  "phase9_commander_ship_12.png",    { 100, 255, 160, 255 } },
    { "indra_rider", "Indra's Chariot","Thousand-Eyed War Platform",   "AoE Dominance",   145, 285.0f, 0.16f, 35, 2, 1.6f, 13, 720,  "phase9_commander_ship_13.png",    { 100, 180, 255, 255 } },
    { "varaha",      "Varaha Boar",   "Earth-Upheaval Siege Ship",     "Slam & Shield",   175, 245.0f, 0.20f, 44, 1, 2.3f, 14, 740,  "phase9_commander_ship_14.png",    { 140, 200, 80, 255 } },
    { "matsya",      "Matsya Leviathan","World-Flood Cruiser",         "Flood Suppression",150, 270.0f, 0.17f, 38, 2, 1.8f, 15, 760, "phase9_commander_ship_15.png",    { 0, 160, 220, 255 } },

    // ── TIER 4: LATE CAMPAIGN (Wave 16-22) ───────────────────────────────────
    { "kamadhenu",   "Kamadhenu",     "Divine Sustenance Vessel",      "Support Sustain", 130, 290.0f, 0.17f, 22, 2, 1.6f, 16, 780,  "kamadhenu.png",                   { 130, 255, 190, 255 } },
    { "kurma",       "Kurma Shell",   "World-Turtle Fortress",         "Fortress Tank",   320, 195.0f, 0.23f, 50, 1, 2.9f, 16, 800,  "phase9_commander_ship_16.png",    { 80, 160, 100, 255 } },
    { "vimana_mk3",  "Vimana Mk-III", "Third-Eye Combat Cruiser",      "Versatile Elite", 160, 310.0f, 0.14f, 38, 2, 1.5f, 17, 820,  "phase9_commander_ship_17.png",    { 255, 200, 60, 255 } },
    { "brahma_ark",  "Brahma Leviathan","Vedic Capital Airship",       "Titan Airship",   350, 210.0f, 0.18f, 50, 1, 2.5f, 18, 860,  "phase8_wisedawn_shaded_ship_3.png",{ 255, 215, 60, 255 } },
    { "chakravyuha", "Chakravyuha",   "Inescapable Formation Ship",    "Tactical Lock",   165, 295.0f, 0.15f, 36, 2, 1.6f, 18, 880,  "phase9_commander_ship_18.png",    { 255, 130, 200, 255 } },
    { "ketu_shadow", "Ketu Shadow",   "Descending Node Phantom",       "Shadow Strike",   110, 365.0f, 0.11f, 32, 3, 1.2f, 19, 900,  "phase9_commander_ship_19.png",    { 80, 60, 160, 255 } },
    { "rahu_devour", "Rahu Devourer", "Ascending Eclipse Destroyer",   "Null-Field",      200, 265.0f, 0.16f, 42, 2, 1.7f, 19, 920,  "phase9_commander_ship_20.png",    { 40, 20, 100, 255 } },
    { "ananta",      "Ananta Serpent","Cosmic Serpent Dreadnought",    "Infinite Fury",   190, 275.0f, 0.15f, 44, 2, 1.7f, 20, 940,  "phase9_commander_ship_21.png",    { 60, 200, 120, 255 } },
    { "garuda_apex", "Garuda Apex",   "Apex Predator Warbird",         "Terminal Strike", 105, 430.0f, 0.09f, 30, 4, 0.8f, 20, 960,  "phase9_commander_ship_22.png",    { 0, 255, 240, 255 } },
    { "kalki_vimana","Kalki Vimana",  "Tenth Avatar Warship",          "Prophetic Blade",  120, 380.0f, 0.12f, 36, 3, 1.2f, 21, 980, "phase9_commander_ship_23.png",    { 255, 255, 200, 255 } },
    { "vishnu_disc", "Vishnu Disc",   "Sudarshana Orbital Platform",   "Orbital Strike",  155, 320.0f, 0.13f, 40, 2, 1.5f, 21, 1000,"phase9_commander_ship_24.png",    { 60, 130, 255, 255 } },
    { "shiva_eye",   "Shiva's Eye",   "Third-Eye Annihilator",         "Destruction Nova",145, 330.0f, 0.12f, 42, 2, 1.4f, 22, 1050,"phase9_commander_ship_25.png",    { 200, 60, 60, 255 } },

    // ── TIER 5: ENDGAME FLEET (Wave 23-28) ───────────────────────────────────
    { "rudra_bomber","Rudra Striker", "Delta-Wing Astral Bomber",      "Plasma Demolition",140, 310.0f, 0.14f, 38, 2, 1.5f, 23, 1100,"phase8_wisedawn_shaded_ship_4.png",{ 255, 60, 80, 255 } },
    { "skanda_lance","Skanda Lance",  "War-God Six-Faced Speeder",     "Multi-Pierce",    115, 375.0f, 0.11f, 35, 3, 1.1f, 23, 1100,"phase9_commander_ship_26.png",    { 255, 200, 80, 255 } },
    { "durga_fortress","Durga Fortress","Nine-Power Siege Platform",   "Nine-Aspect Wall",250, 230.0f, 0.19f, 52, 1, 2.5f, 24, 1150,"phase9_commander_ship_27.png",    { 255, 140, 60, 255 } },
    { "lakshmi_grace","Lakshmi Grace","Prosperity Aura Cruiser",       "Wealth Shield",   170, 280.0f, 0.17f, 30, 2, 1.7f, 24, 1150,"phase9_commander_ship_28.png",    { 255, 220, 150, 255 } },
    { "hanuman_fist","Hanuman Fist",  "Devotion Strike Warship",       "Raging Loyalty",  210, 300.0f, 0.14f, 48, 2, 1.5f, 25, 1200,"phase9_commander_ship_29.png",    { 255, 140, 0, 255 } },
    { "saraswati_arc","Saraswati Arc","Knowledge-Current Resonator",   "Resonance Burst", 130, 335.0f, 0.12f, 34, 3, 1.3f, 25, 1200,"phase9_commander_ship_30.png",    { 200, 180, 255, 255 } },
    { "kali_storm",  "Kali Storm",    "Time-Destroyer Battlerider",    "Chaos Cascade",   160, 360.0f, 0.10f, 46, 3, 1.0f, 26, 1250,"phase9_commander_ship_31.png",    { 80, 0, 120, 255 } },
    { "yama_throne", "Yama Throne",   "Death-God Judgment Carrier",    "Judgment Beam",   230, 245.0f, 0.18f, 55, 1, 2.2f, 26, 1250,"phase9_commander_ship_32.png",    { 60, 0, 80, 255 } },
    { "kubera_vault","Kubera Vault",  "Celestial Treasury Titan",      "Hoard & Barrage", 280, 220.0f, 0.20f, 52, 1, 2.3f, 27, 1300,"phase9_commander_ship_33.png",    { 220, 180, 0, 255 } },
    { "vayu_cyclone","Vayu Cyclone",  "Wind-Storm Hypercruiser",       "Vortex Control",  140, 400.0f, 0.10f, 32, 4, 0.9f, 27, 1300,"phase9_commander_ship_34.png",    { 180, 255, 240, 255 } },
    { "brahmastra_mk1","Brahmastra Mk-I","Celestial Weapon Platform",  "Cosmic Nuke",     190, 290.0f, 0.15f, 50, 2, 1.5f, 28, 1350,"phase9_commander_ship_35.png",    { 255, 240, 100, 255 } },

    // ── TIER 6: ULTIMATE FLEET (Wave 29-30 & Secret) ─────────────────────────
    { "narasimha",   "Narasimha",     "Avatar of Ferocious Righteousness","Ultimate Berserker",150, 360.0f, 0.09f, 55, 3, 0.9f, 29, 1400,"narasimha.png",                { 255, 90, 30, 255 } },
    { "sudarshana_neo","Sudarshana Neo","Advanced Cybernetic Flagship", "Omni-Vanguard",   180, 370.0f, 0.08f, 48, 4, 0.9f, 29, 1400,"phase8_wisedawn_shaded_ship_5.png",{ 0, 255, 210, 255 } },
    { "parasurama",  "Parashurama",   "Axe-God Destroyer",             "Warrior Avatar",  200, 340.0f, 0.11f, 58, 2, 1.3f, 30, 1500,"phase9_commander_ship_36.png",    { 180, 100, 0, 255 } },
    { "rama_vimana", "Rama Vimana",   "Righteous King's Warship",      "Honor Blade",     175, 345.0f, 0.11f, 52, 3, 1.1f, 30, 1500,"phase9_commander_ship_37.png",    { 60, 200, 80, 255 } },
    { "krishna_disc","Krishna Disc",  "Flute-Song Battle Platform",    "Divine Play",     185, 355.0f, 0.10f, 54, 3, 1.0f, 30, 1500,"phase9_commander_ship_38.png",    { 50, 80, 200, 255 } },
    { "vishnu_prime","Vishnu Prime",  "Preserver's Ultimate Form",     "Cosmic Preservation",220, 330.0f, 0.10f, 60, 2, 1.2f, 30, 1600,"phase9_commander_ship_39.png",  { 40, 120, 255, 255 } },
    { "shiva_ultimate","Shiva Ultimate","Destroyer's Transcendent Form","Tandava Annihilation",240, 340.0f, 0.09f, 65, 3, 1.0f, 30, 1600,"phase9_commander_ship_40.png", { 220, 50, 50, 255 } },

    // ── TIER 7: BOSS-SALVAGED SIGNATURE FLEET ────────────────────────────────
    { "kumbha_titan", "Kumbha Titan", "Siege hull forged from the Slumbering Colossus", "Boss Breaker / Heavy", 390, 205.0f, 0.19f, 61, 1, 2.4f, 999999, 0, "phase9_commander_ship_41.png", { 255, 145, 70, 255 }, "KUMBHAKARNA", "TITAN KUMBHAKARNA" },
    { "ravana_dasha", "Dasha Vimana", "Tenfold imperial weapons platform", "Boss Breaker / Barrage", 250, 315.0f, 0.12f, 51, 2, 1.4f, 999999, 0, "phase9_commander_ship_42.png", { 255, 65, 80, 255 }, "RAVANA", "EMPEROR RAVANA" },
    { "mahisha_rush", "Mahisha Ram", "Armored charge interceptor", "Boss Breaker / Assault", 310, 285.0f, 0.15f, 58, 2, 1.7f, 999999, 0, "phase9_commander_ship_43.png", { 255, 115, 60, 255 }, "MAHISHASURA", "WARLORD MAHISHASURA" },
    { "makara_abyss", "Makara Abyssal", "Tidal shield cruiser recovered from the deep", "Boss Breaker / Sustain", 330, 260.0f, 0.17f, 45, 2, 1.6f, 999999, 0, "phase9_commander_ship_44.png", { 60, 225, 255, 255 }, "MAKARA", "MAKARA, ABYSSAL LEVIATHAN" },
    { "indra_mirage", "Indrajit's Mirage", "Phase-shift strike craft", "Boss Breaker / Evasion", 205, 390.0f, 0.095f, 42, 4, 0.85f, 999999, 0, "phase9_commander_ship_45.png", { 190, 100, 255, 255 }, "INDRAJIT", "CONQUEROR INDRAJIT" },
    { "hiranya_aegis", "Hiranya Aegis", "Immortal pact fortress vessel", "Boss Breaker / Aegis", 430, 225.0f, 0.18f, 58, 1, 2.3f, 999999, 0, "phase9_commander_ship_46.png", { 255, 220, 85, 255 }, "HIRANYAKASHIPU", "TYRANT HIRANYAKASHIPU" },
    { "megha_tempest", "Meghnada Tempest", "Lightning grid assault carrier", "Boss Breaker / Storm", 260, 360.0f, 0.105f, 50, 3, 1.1f, 999999, 0, "phase9_commander_ship_47.png", { 180, 120, 255, 255 }, "MEGHNADA", "MEGHNADA, STORM ILLUSIONIST" },
    { "vritra_skyseal", "Vritra Skyseal", "Storm-severing bastion fighter", "Boss Breaker / Control", 360, 275.0f, 0.16f, 56, 2, 1.8f, 999999, 0, "phase9_commander_ship_48.png", { 75, 220, 235, 255 }, "VRITRA", "VRITRA, SKY-SEALING SERPENT" }
}};

inline const ShipArchetype* GetShipArchetype(const std::string& id) {
    for (const auto& ship : SHIP_FLEET) {
        if (ship.id == id) return &ship;
    }
    return &SHIP_FLEET[0];
}

} // namespace Vimana
