#pragma once
#include <unordered_map>
#include <vector>
#include <algorithm>
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

// ── AI Threat Table (DSA HashMap + Priority Evaluation) ───────────────────────
// Tracks aggregate threat generated per active player (damage dealt, distance, taunt).
class AIThreatTable {
public:
    AIThreatTable() = default;

    void reset() {
        m_threat_map.clear();
        m_taunted_player = -1;
    }

    void add_threat(int player_id, float amount) {
        m_threat_map[player_id] += amount;
    }

    void apply_taunt(int player_id, float duration = 4.0f) {
        m_taunted_player = player_id;
        m_taunt_timer = duration;
        m_threat_map[player_id] += 500.0f; // Massive threat spike
    }

    void update(float dt) {
        if (m_taunt_timer > 0.0f) {
            m_taunt_timer -= dt;
            if (m_taunt_timer <= 0.0f) {
                m_taunted_player = -1;
            }
        }
        // Threat decay over time
        for (auto& pair : m_threat_map) {
            pair.second = std::max(0.0f, pair.second - 2.0f * dt);
        }
    }

    // Evaluates which player an enemy or boss should prioritize targeting
    int select_target(const std::vector<PlayerNetState>& players, Vector2 enemy_pos) const {
        if (players.empty()) return 0;
        if (m_taunted_player >= 0) return m_taunted_player;

        int best_id = 0;
        float best_score = -99999.0f;

        for (const auto& p : players) {
            if (p.is_downed) continue; // Do not prioritize downed players

            float dist = Vector2Distance({ p.pos_x, p.pos_y }, enemy_pos);
            float threat = 0.0f;
            auto it = m_threat_map.find(p.player_id);
            if (it != m_threat_map.end()) threat = it->second;

            // Score formula: Threat * 0.7 - Distance * 0.3
            float eval_score = threat - (dist * 0.25f);
            if (eval_score > best_score) {
                best_score = eval_score;
                best_id = p.player_id;
            }
        }
        return best_id;
    }

    float get_threat(int player_id) const {
        auto it = m_threat_map.find(player_id);
        return (it != m_threat_map.end()) ? it->second : 0.0f;
    }

private:
    std::unordered_map<int, float> m_threat_map;
    int m_taunted_player = -1;
    float m_taunt_timer = 0.0f;
};

} // namespace Vimana
