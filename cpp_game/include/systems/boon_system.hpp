#pragma once
#include <string>
#include <vector>
#include <algorithm>
#include <random>
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

struct BoonInfo {
    BoonType type;
    std::string name;
    std::string deity;
    std::string description;
    Color color;
};

inline const std::vector<BoonInfo> ALL_BOONS = {
    { BoonType::AGNI_SOLAR_FURY, "Agni's Solar Fury", "Deity: Agni", "Defeated enemies detonate in fiery explosions inflicting AOE burn.", COLOR_RED_BRIGHT },
    { BoonType::INDRA_VAJRA_THUNDER, "Indra's Vajra Thunderbolt", "Deity: Indra", "35% chance on hit to discharge chain lightning to nearby Asuras.", COLOR_CYAN_BRIGHT },
    { BoonType::VAYU_GALE_TEMPEST, "Vayu's Gale Tempest", "Deity: Vayu", "35% Dash cooldown reduction; leaves damaging gale currents.", COLOR_GREEN_BRIGHT },
    { BoonType::GARUDA_CELESTIAL_MAGNET, "Garuda's Celestial Magnet", "Deity: Garuda", "Pulls powerups and Amrita drops magnetically from 3x distance.", COLOR_GOLD_BRIGHT },
    { BoonType::VARUNA_OCEANIC_WARD, "Varuna's Oceanic Ward", "Deity: Varuna", "+30 Maximum Hull HP and passive celestial hull self-regeneration.", { 80, 220, 255, 255 } },
    { BoonType::SUDARSHANA_KEEN_EDGE, "Sudarshana Keen Edge", "Deity: Vishnu", "Sudarshana Chakram damage and size doubled, cooldown reduced by 30%.", COLOR_GOLD },
    { BoonType::YAMA_FATAL_DECREE, "Yama's Fatal Decree", "Deity: Yama", "+60% critical execution damage against targets below 40% HP.", COLOR_PURPLE_BRIGHT },
    { BoonType::SURYA_RADIANT_PIERCE, "Surya's Radiant Pierce", "Deity: Surya", "Every 7th shot unleashes a golden piercing solar slug.", COLOR_ORANGE_BRIGHT }
};

class BoonSystem {
public:
    static std::vector<BoonInfo> generate_draft(const std::vector<BoonType>& current_boons) {
        std::vector<BoonInfo> available;
        for (const auto& b : ALL_BOONS) {
            // Can offer upgrades or new boons
            available.push_back(b);
        }

        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(available.begin(), available.end(), g);

        std::vector<BoonInfo> draft;
        for (size_t i = 0; i < std::min<size_t>(3, available.size()); ++i) {
            draft.push_back(available[i]);
        }
        return draft;
    }
};

} // namespace Vimana
