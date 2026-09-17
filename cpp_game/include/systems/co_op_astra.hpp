#pragma once
#include <string>
#include <vector>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

struct CoOpAstraDefinition {
    CoOpAstraType type;
    std::string name;
    std::string formula;
    std::string description;
    float duration;
    Color theme_color;
};

class CoOpAstraSystem {
public:
    static const std::vector<CoOpAstraDefinition>& all_definitions() {
        static const std::vector<CoOpAstraDefinition> defs = {
            {
                CoOpAstraType::THUNDER_TEMPEST,
                "THUNDER TEMPEST",
                "GARUDA + VAJRA",
                "Fierce celestial storm strikes all active enemies with multi-branching chain lightning.",
                3.5f,
                COLOR_CYAN_BRIGHT
            },
            {
                CoOpAstraType::DIVINE_BARRIER,
                "DIVINE BARRIER",
                "KAMADHENU + TRIPURA",
                "Impenetrable sacred mandala protects the entire squadron from all damage for 5 seconds.",
                5.0f,
                COLOR_GOLD_BRIGHT
            },
            {
                CoOpAstraType::SOLAR_INFERNO,
                "SOLAR INFERNO",
                "AGNEYASTRA + SURYA",
                "Blinding solar eruption ignites the astral void, inflicting massive burning devastation.",
                4.0f,
                COLOR_ORANGE_BRIGHT
            },
            {
                CoOpAstraType::STORM_CYCLONE,
                "STORM CYCLONE",
                "INDRA + VAYU",
                "Whirling hurricane pulls enemies into the central vortex and reflects hostile fire.",
                4.5f,
                COLOR_GREEN_BRIGHT
            }
        };
        return defs;
    }

    static CoOpAstraType evaluate_combination(const std::string& ship1, const std::string& ship2) {
        if ((ship1 == "garuda" && ship2 == "vajra") || (ship1 == "vajra" && ship2 == "garuda")) {
            return CoOpAstraType::THUNDER_TEMPEST;
        }
        if ((ship1 == "kamadhenu" && ship2 == "tripura") || (ship1 == "tripura" && ship2 == "kamadhenu")) {
            return CoOpAstraType::DIVINE_BARRIER;
        }
        if ((ship1 == "agneyastra" && ship2 == "surya") || (ship1 == "surya" && ship2 == "agneyastra")) {
            return CoOpAstraType::SOLAR_INFERNO;
        }
        if ((ship1 == "indra" && ship2 == "vayu") || (ship1 == "vayu" && ship2 == "indra")) {
            return CoOpAstraType::STORM_CYCLONE;
        }
        // Generic fallback team astra
        return CoOpAstraType::THUNDER_TEMPEST;
    }

    static const CoOpAstraDefinition* get_definition(CoOpAstraType type) {
        for (const auto& d : all_definitions()) {
            if (d.type == type) return &d;
        }
        return &all_definitions()[0];
    }
};

} // namespace Vimana
