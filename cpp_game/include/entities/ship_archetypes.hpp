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

inline const std::array<ShipArchetype, 12> SHIP_FLEET = {{
    { "pushpaka", "Pushpaka", "Celestial Cruiser", "Balanced", 100, 300.0f, 0.15f, 25, 2, 1.6f, 0, 0, "pushpaka.png", COLOR_GOLD },
    { "tripura", "Tripura", "Iron Dreadnought", "Heavy Assault", 160, 240.0f, 0.20f, 38, 1, 2.2f, 0, 0, "tripura.png", COLOR_ORANGE_BRIGHT },
    { "garuda", "Garuda", "Sky Predator", "High Agility", 80, 380.0f, 0.11f, 18, 3, 1.1f, 0, 0, "garuda.png", COLOR_CYAN_BRIGHT },
    { "vajra", "Vajra Spear", "Thunder Interceptor", "Burst", 90, 340.0f, 0.14f, 28, 2, 1.4f, 4, 400, "vajra.png", COLOR_CYAN },
    { "naga", "Naga Coil", "Venom Infiltrator", "Piercing", 95, 320.0f, 0.13f, 26, 2, 1.5f, 7, 450, "naga.png", COLOR_GREEN_BRIGHT },
    { "agneyastra", "Agneyastra", "Flame Chariot", "Burn DPS", 110, 290.0f, 0.16f, 32, 2, 1.7f, 10, 500, "agneyastra.png", COLOR_RED_BRIGHT },
    { "soma", "Soma Ark", "Lunar Sanctuary", "Shielding", 125, 270.0f, 0.18f, 24, 2, 1.8f, 13, 550, "soma.png", COLOR_PURPLE_BRIGHT },
    { "kubera", "Kubera Galleon", "Treasury Citadel", "Wealth & Armor", 140, 250.0f, 0.19f, 34, 1, 2.0f, 16, 600, "kubera.png", COLOR_GOLD_BRIGHT },
    { "surya", "Surya Flare", "Solar Vanguard", "Radiant Beam", 105, 330.0f, 0.14f, 30, 2, 1.5f, 20, 700, "surya.png", COLOR_GOLD_BRIGHT },
    // ── NEW SHIPS ───────────────────────────────────────────────────────────
    { "airavata", "Airavata", "Indra's Celestial Elephant", "Tank Bastion", 300, 200.0f, 0.22f, 48, 1, 2.8f, 22, 750, "tripura.png", { 180, 210, 255, 255 } },
    { "kamadhenu", "Kamadhenu", "Divine Sustenance Vessel", "Support / Sustain", 130, 290.0f, 0.17f, 22, 2, 1.6f, 26, 800, "soma.png", { 130, 255, 190, 255 } },
    { "narasimha", "Narasimha", "Avatar of Ferocious Righteousness", "Ultimate Berserker", 150, 360.0f, 0.09f, 55, 3, 0.9f, 30, 1200, "garuda.png", { 255, 90, 30, 255 } }
}};

inline const ShipArchetype* GetShipArchetype(const std::string& id) {
    for (const auto& ship : SHIP_FLEET) {
        if (ship.id == id) return &ship;
    }
    return &SHIP_FLEET[0];
}

} // namespace Vimana
