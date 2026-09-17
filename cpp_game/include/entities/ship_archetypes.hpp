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
};

inline const std::array<ShipArchetype, 18> SHIP_FLEET = {{
    { "pushpaka", "Pushpaka", "Celestial Cruiser", "Balanced", 100, 300.0f, 0.15f, 25, 2, 1.6f, 0, 0, "pushpaka.png", COLOR_GOLD },
    { "tripura", "Tripura", "Iron Dreadnought", "Heavy Assault", 160, 240.0f, 0.20f, 38, 1, 2.2f, 0, 0, "tripura.png", COLOR_ORANGE_BRIGHT },
    { "garuda", "Garuda", "Sky Predator", "High Agility", 80, 380.0f, 0.11f, 18, 3, 1.1f, 0, 0, "garuda.png", COLOR_CYAN_BRIGHT },
    { "vajra", "Vajra Spear", "Thunder Interceptor", "Burst", 90, 340.0f, 0.14f, 28, 2, 1.4f, 4, 400, "vajra.png", COLOR_CYAN },
    { "naga", "Naga Coil", "Venom Infiltrator", "Piercing", 95, 320.0f, 0.13f, 26, 2, 1.5f, 7, 450, "naga.png", COLOR_GREEN_BRIGHT },
    { "agneyastra", "Agneyastra", "Flame Chariot", "Burn DPS", 110, 290.0f, 0.16f, 32, 2, 1.7f, 10, 500, "agneyastra.png", COLOR_RED_BRIGHT },
    { "soma", "Soma Ark", "Lunar Sanctuary", "Shielding", 125, 270.0f, 0.18f, 24, 2, 1.8f, 13, 550, "soma.png", COLOR_PURPLE_BRIGHT },
    { "kubera", "Kubera Galleon", "Treasury Citadel", "Wealth & Armor", 140, 250.0f, 0.19f, 34, 1, 2.0f, 16, 600, "kubera.png", COLOR_GOLD_BRIGHT },
    { "surya", "Surya Flare", "Solar Vanguard", "Radiant Beam", 105, 330.0f, 0.14f, 30, 2, 1.5f, 20, 700, "surya.png", COLOR_GOLD_BRIGHT },
    { "airavata", "Airavata", "Indra's Celestial Elephant", "Tank Bastion", 300, 200.0f, 0.22f, 48, 1, 2.8f, 22, 750, "airavata.png", { 180, 210, 255, 255 } },
    { "kamadhenu", "Kamadhenu", "Divine Sustenance Vessel", "Support / Sustain", 130, 290.0f, 0.17f, 22, 2, 1.6f, 26, 800, "kamadhenu.png", { 130, 255, 190, 255 } },
    { "narasimha", "Narasimha", "Avatar of Ferocious Righteousness", "Ultimate Berserker", 150, 360.0f, 0.09f, 55, 3, 0.9f, 30, 1200, "narasimha.png", { 255, 90, 30, 255 } },
    // ── MODERN FLEET: AIRPLANES, INTERCEPTORS & AIRSHIPS ───────────────────
    { "garuda_prime", "Garuda Prime", "Supersonic Astral Interceptor", "Hypersonic Strike", 95, 410.0f, 0.10f, 26, 3, 1.0f, 5, 500, "phase8_wisedawn_shaded_ship_0.png", { 70, 220, 255, 255 } },
    { "tripura_mk2", "Tripura Dread-Assault", "Twin-Hull Heavy Gunship", "Heavy Barrage", 220, 250.0f, 0.16f, 42, 2, 1.9f, 12, 650, "phase8_wisedawn_shaded_ship_1.png", { 255, 140, 40, 255 } },
    { "varuna_void", "Varuna Stealth Cruiser", "Forward-Swept Wing Infiltrator", "Stealth & Criticals", 120, 350.0f, 0.12f, 34, 3, 1.2f, 18, 750, "phase8_wisedawn_shaded_ship_2.png", { 150, 110, 255, 255 } },
    { "brahma_ark", "Brahma Sky Leviathan", "Vedic Capital Airship", "Titan Airship", 350, 210.0f, 0.18f, 50, 1, 2.5f, 24, 900, "phase8_wisedawn_shaded_ship_3.png", { 255, 215, 60, 255 } },
    { "rudra_bomber", "Rudra Plasma Striker", "Delta-Wing Astral Bomber", "Plasma Demolition", 140, 310.0f, 0.14f, 38, 2, 1.5f, 28, 1000, "phase8_wisedawn_shaded_ship_4.png", { 255, 60, 80, 255 } },
    { "sudarshana_neo", "Sudarshana Cyber-Vimana", "Advanced Cybernetic Flagship", "Omni-Vanguard", 180, 370.0f, 0.08f, 48, 4, 0.9f, 30, 1500, "phase8_wisedawn_shaded_ship_5.png", { 0, 255, 210, 255 } }
}};

inline const ShipArchetype* GetShipArchetype(const std::string& id) {
    for (const auto& ship : SHIP_FLEET) {
        if (ship.id == id) return &ship;
    }
    return &SHIP_FLEET[0];
}

} // namespace Vimana
