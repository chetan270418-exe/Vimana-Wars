#pragma once
#include <vector>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "entities/enemy.hpp"
#include "entities/player.hpp"

namespace Vimana {

enum class SquadTactic {
    SWARM,       // Converge and orbit in tight pack
    PINCER,      // Flank from two opposing angles
    SCREEN,      // Tanks form frontline shield, ranged units stay behind
    FOCUS_FIRE,  // Target lowest-HP player (co-op peeling pressure)
    ESCORT       // Guard Healers / Carriers behind frontliners
};

struct EnemySquad {
    SquadTactic tactic = SquadTactic::SWARM;
    std::vector<int> member_indices;
    float retask_timer = 4.0f;
    Vector2 anchor = { SCREEN_WIDTH * 0.5f, 140.0f };
    int target_player_id = 0;
};

class SquadFormationSystem {
public:
    static SquadFormationSystem& instance() {
        static SquadFormationSystem s_inst;
        return s_inst;
    }

    void clear() {
        m_squads.clear();
        m_formation_tick_timer = 0.0f;
    }

    // Automatically organises active unassigned enemies into tactical squads
    void rebuild_squads(const std::vector<Enemy>& enemies, int wave_num, size_t coop_players) {
        m_squads.clear();
        if (enemies.empty()) return;

        std::vector<bool> assigned(enemies.size(), false);

        // Gather indices of living non-miniboss enemies
        std::vector<int> living;
        for (size_t i = 0; i < enemies.size(); ++i) {
            if (enemies[i].active && !enemies[i].is_miniboss) {
                living.push_back(static_cast<int>(i));
            }
        }

        // Form squads of 3-5 enemies
        size_t cursor = 0;
        int squad_count = 0;
        while (cursor < living.size()) {
            size_t batch_size = std::min<size_t>(4, living.size() - cursor);
            if (batch_size < 2) break; // Leave singletons

            EnemySquad sq;
            sq.retask_timer = 3.5f + (squad_count % 3) * 0.5f;

            // Pick tactic based on composition & wave
            bool has_tank = false;
            bool has_healer = false;
            bool has_carrier = false;
            for (size_t b = 0; b < batch_size; ++b) {
                int idx = living[cursor + b];
                sq.member_indices.push_back(idx);
                if (enemies[idx].type == EnemyType::ASURA_TANK) has_tank = true;
                if (enemies[idx].type == EnemyType::ASURA_HEALER) has_healer = true;
                if (enemies[idx].type == EnemyType::ASURA_CARRIER) has_carrier = true;
            }

            if (has_healer || has_carrier) {
                sq.tactic = SquadTactic::ESCORT;
            } else if (has_tank && batch_size >= 3) {
                sq.tactic = SquadTactic::SCREEN;
            } else if (coop_players > 1 && (squad_count % 2 == 0)) {
                sq.tactic = SquadTactic::FOCUS_FIRE;
            } else if (squad_count % 2 == 1) {
                sq.tactic = SquadTactic::PINCER;
            } else {
                sq.tactic = SquadTactic::SWARM;
            }

            m_squads.push_back(sq);
            cursor += batch_size;
            squad_count++;
        }
    }

    void update(float dt, std::vector<Enemy>& enemies, const std::vector<Player>& squad_players) {
        if (enemies.empty() || squad_players.empty()) return;

        m_formation_tick_timer -= dt;
        if (m_formation_tick_timer <= 0.0f) {
            m_formation_tick_timer = 2.0f; // Refresh squad memberships periodically
            rebuild_squads(enemies, 1, squad_players.size());
        }

        // Find lowest-HP player for FOCUS_FIRE
        const Player* lowest_hp_player = &squad_players[0];
        int min_hp = 999999;
        for (const auto& p : squad_players) {
            if (!p.is_downed && !p.is_spectator && p.hp < min_hp) {
                min_hp = p.hp;
                lowest_hp_player = &p;
            }
        }

        for (auto& sq : m_squads) {
            sq.retask_timer -= dt;

            // Remove inactive members
            sq.member_indices.erase(
                std::remove_if(sq.member_indices.begin(), sq.member_indices.end(),
                    [&enemies](int idx) {
                        return idx < 0 || idx >= static_cast<int>(enemies.size()) || !enemies[idx].active;
                    }),
                sq.member_indices.end()
            );

            if (sq.member_indices.empty()) continue;

            const size_t count = sq.member_indices.size();

            switch (sq.tactic) {
                case SquadTactic::SCREEN: {
                    // Tanks line up at y=130 horizontally, shooters/snipers stay behind at y=70
                    int tank_slot = 0;
                    int back_slot = 0;
                    for (int idx : sq.member_indices) {
                        auto& e = enemies[idx];
                        if (e.type == EnemyType::ASURA_TANK) {
                            float target_x = 200.0f + (tank_slot * 250.0f);
                            e.pos.x += (target_x - e.pos.x) * 1.5f * dt;
                            if (e.pos.y > 150.0f) e.pos.y -= 30.0f * dt;
                            tank_slot++;
                        } else {
                            // Backline support
                            float target_x = 220.0f + (back_slot * 220.0f);
                            e.pos.x += (target_x - e.pos.x) * 1.2f * dt;
                            if (e.pos.y > 90.0f) e.pos.y -= 40.0f * dt;
                            back_slot++;
                        }
                    }
                    break;
                }

                case SquadTactic::PINCER: {
                    // Half approach from left angle, half from right
                    for (size_t i = 0; i < count; ++i) {
                        int idx = sq.member_indices[i];
                        auto& e = enemies[idx];
                        bool left_wing = (i % 2 == 0);
                        float flank_target_x = left_wing ? (lowest_hp_player->pos.x - 180.0f)
                                                         : (lowest_hp_player->pos.x + 180.0f);
                        flank_target_x = std::clamp(flank_target_x, 40.0f, SCREEN_WIDTH - 40.0f);
                        // Steer toward flank position
                        e.pos.x += (flank_target_x - e.pos.x) * 0.8f * dt;
                    }
                    break;
                }

                case SquadTactic::FOCUS_FIRE: {
                    // All ranged squad members concentrate aim and accelerate toward lowest HP player
                    for (int idx : sq.member_indices) {
                        auto& e = enemies[idx];
                        Vector2 to_target = Vector2Subtract(lowest_hp_player->pos, e.pos);
                        e.angle = Vector2AngleDeg(e.pos, lowest_hp_player->pos);
                        if (Vector2Length(to_target) > 200.0f) {
                            Vector2 dir = Vector2Normalize(to_target);
                            e.pos.x += dir.x * e.speed * 0.25f * dt;
                            e.pos.y += dir.y * e.speed * 0.25f * dt;
                        }
                    }
                    break;
                }

                case SquadTactic::ESCORT: {
                    // Keep Healer/Carrier behind guardians
                    Vector2 front_center = { 0, 0 };
                    int front_count = 0;
                    for (int idx : sq.member_indices) {
                        const auto& e = enemies[idx];
                        if (e.type != EnemyType::ASURA_HEALER && e.type != EnemyType::ASURA_CARRIER) {
                            front_center.x += e.pos.x;
                            front_center.y += e.pos.y;
                            front_count++;
                        }
                    }
                    if (front_count > 0) {
                        front_center.x /= front_count;
                        front_center.y /= front_count;
                        // Tuck VIP behind front center
                        for (int idx : sq.member_indices) {
                            auto& e = enemies[idx];
                            if (e.type == EnemyType::ASURA_HEALER || e.type == EnemyType::ASURA_CARRIER) {
                                float desired_y = std::max(60.0f, front_center.y - 70.0f);
                                e.pos.x += (front_center.x - e.pos.x) * 1.5f * dt;
                                e.pos.y += (desired_y - e.pos.y) * 1.5f * dt;
                            }
                        }
                    }
                    break;
                }

                case SquadTactic::SWARM:
                default: {
                    // Coordinated orbiting flock: slight cohesion force
                    Vector2 center = { 0, 0 };
                    for (int idx : sq.member_indices) {
                        center.x += enemies[idx].pos.x;
                        center.y += enemies[idx].pos.y;
                    }
                    center.x /= count;
                    center.y /= count;
                    for (int idx : sq.member_indices) {
                        auto& e = enemies[idx];
                        // Nudge toward flock center for cohesion
                        e.pos.x += (center.x - e.pos.x) * 0.35f * dt;
                    }
                    break;
                }
            }
        }
    }

private:
    SquadFormationSystem() = default;
    std::vector<EnemySquad> m_squads;
    float m_formation_tick_timer = 0.0f;
};

} // namespace Vimana
