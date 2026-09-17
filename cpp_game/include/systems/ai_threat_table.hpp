#pragma once
#include <vector>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "entities/player.hpp"

namespace Vimana {

class AIThreatTable {
public:
    static Vector2 get_highest_threat_target(Vector2 enemy_pos, const std::vector<Player>& squad) {
        if (squad.empty()) return { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT * 0.75f };

        float highest_threat = -1.0f;
        int target_idx = -1;

        for (size_t i = 0; i < squad.size(); ++i) {
            const auto& p = squad[i];
            if (p.is_downed) continue; // Downed players generate 0 threat

            float dist = Vector2Distance(enemy_pos, p.pos);
            float proximity_score = 1500.0f / (dist + 50.0f);
            float damage_score = p.total_damage_dealt * 0.04f;
            float combo_score = p.combo * 8.0f;

            float total_threat = proximity_score + damage_score + combo_score;
            if (total_threat > highest_threat) {
                highest_threat = total_threat;
                target_idx = static_cast<int>(i);
            }
        }

        if (target_idx >= 0 && target_idx < static_cast<int>(squad.size())) {
            return squad[target_idx].pos;
        }

        // Fallback to first player or center
        return squad[0].pos;
    }
};

} // namespace Vimana
