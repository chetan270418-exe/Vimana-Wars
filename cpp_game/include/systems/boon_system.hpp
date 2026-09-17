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
    { BoonType::SURYA_RADIANT_PIERCE, "Surya's Radiant Pierce", "Deity: Surya", "Every 7th shot unleashes a golden piercing solar slug.", COLOR_ORANGE_BRIGHT },
    { BoonType::NARASIMHA_BERSERK_MIGHT, "Narasimha's Berserk Might", "Deity: Narasimha", "When Hull HP drops below 35%, weapon damage amplifies by +40%.", COLOR_ORANGE_BRIGHT }
};

inline const std::vector<BoonSynergy> ALL_SYNERGIES = {
    { "solar_inferno", "Solar Inferno", "Agni + Surya", "Slain foes detonate in radiant solar flames piercing nearby armadas.", BoonType::AGNI_SOLAR_FURY, BoonType::SURYA_RADIANT_PIERCE, COLOR_ORANGE_BRIGHT },
    { "tempest_drive", "Tempest Drive", "Vayu + Garuda", "Vayu Dash leaves a crushing vacuum vortex pulling and shredding enemies.", BoonType::VAYU_GALE_TEMPEST, BoonType::GARUDA_CELESTIAL_MAGNET, COLOR_GREEN_BRIGHT },
    { "reaper_chakram", "Reaper Chakram", "Yama + Sudarshana", "Spinning blade instantly decapitates any Asura below 35% HP.", BoonType::YAMA_FATAL_DECREE, BoonType::SUDARSHANA_KEEN_EDGE, COLOR_PURPLE_BRIGHT },
    { "oceanic_burn", "Oceanic Firestorm", "Varuna + Agni", "Passive hull regeneration speed doubled and emits fiery shockwaves.", BoonType::VARUNA_OCEANIC_WARD, BoonType::AGNI_SOLAR_FURY, { 80, 240, 220, 255 } },
    { "berserk_decree", "Wrath of Narasimha", "Narasimha + Yama", "Berserk state triggers at 50% HP and grants guaranteed critical hits.", BoonType::NARASIMHA_BERSERK_MIGHT, BoonType::YAMA_FATAL_DECREE, COLOR_RED_BRIGHT }
};

class BoonSystem {
public:
    static std::vector<BoonInfo> generate_draft(const std::vector<BoonType>& current_boons) {
        std::vector<BoonInfo> available;
        for (const auto& b : ALL_BOONS) {
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

    static bool check_synergy_unlocked(const std::vector<BoonType>& boons, BoonType newly_added, BoonSynergy& out_synergy) {
        for (const auto& syn : ALL_SYNERGIES) {
            if (syn.req1 == newly_added || syn.req2 == newly_added) {
                BoonType other = (syn.req1 == newly_added) ? syn.req2 : syn.req1;
                if (std::find(boons.begin(), boons.end(), other) != boons.end()) {
                    out_synergy = syn;
                    return true;
                }
            }
        }
        return false;
    }

    static bool has_synergy(const std::vector<BoonType>& boons, const std::string& syn_id) {
        for (const auto& syn : ALL_SYNERGIES) {
            if (syn.id == syn_id) {
                bool has1 = (std::find(boons.begin(), boons.end(), syn.req1) != boons.end());
                bool has2 = (std::find(boons.begin(), boons.end(), syn.req2) != boons.end());
                return (has1 && has2);
            }
        }
        return false;
    }
};

} // namespace Vimana
