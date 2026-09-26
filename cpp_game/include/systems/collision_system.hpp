#pragma once
#include <algorithm>
#include <cmath>
#include <vector>
#include <iostream>
#include "core/types.hpp"
#include "core/constants.hpp"
#include "core/dsa/spatial_grid.hpp"
#include "entities/player.hpp"
#include "entities/enemy.hpp"
#include "entities/boss.hpp"
#include "entities/bullet.hpp"
#include "entities/powerup.hpp"
#include "systems/particle_system.hpp"
#include "systems/sound_system.hpp"

namespace Vimana {

class CollisionSystem {
public:
    CollisionSystem() : m_grid(SCREEN_WIDTH, SCREEN_HEIGHT, 80.0f) {}

    void resolve_combat_ptrs(
        const std::vector<Player*>& squad,
        std::vector<Enemy>& enemies,
        Boss* current_boss,
        std::vector<Bullet>& bullets,
        std::vector<Powerup>& powerups,
        ParticleSystem& particles,
        int& out_prana_earned,
        float player_damage_multiplier = 1.0f
    ) {
        if (squad.empty()) return;
        const auto emit_player_hit_feedback = [&particles](Player& player, int hp_before) {
            const int hp_lost = std::max(0, hp_before - player.hp);
            const bool shielded = hp_lost == 0;
            particles.emit_explosion(player.pos, shielded ? COLOR_CYAN_BRIGHT : COLOR_RED_BRIGHT,
                                     shielded ? 8 : 14, shielded ? 95.0f : 155.0f);
            particles.add_floating_text(player.pos,
                shielded ? "DAMAGE BLOCKED" : "-" + std::to_string(hp_lost) + " HP",
                shielded ? COLOR_CYAN_BRIGHT : COLOR_RED_BRIGHT);
            if (g_screen_shake_enabled) {
                particles.trigger_screen_shake(shielded ? 3.0f : 8.0f, shielded ? 0.12f : 0.25f);
            }
        };
        m_grid.clear();

        // 1. Insert active enemies into SpatialGrid
        for (size_t i = 0; i < enemies.size(); ++i) {
            if (enemies[i].active) {
                m_grid.insert(static_cast<int>(i), enemies[i].pos, enemies[i].radius);
            }
        }

        std::vector<int> candidate_indices;

        // 2. Player Bullets vs Enemies
        for (auto& b : bullets) {
            if (!b.active || b.is_enemy) continue;

            // Find bullet owner
            Player* owner = nullptr;
            for (auto* p : squad) {
                if (p && p->player_id == b.owner_player_id) {
                    owner = p;
                    break;
                }
            }
            if (!owner) owner = squad[0];

            // Check Boss first if active
            if (current_boss && current_boss->active) {
                if (Vector2Distance(b.pos, current_boss->pos) < (b.radius + current_boss->radius)) {
                    const int scaled_damage = static_cast<int>(std::round(b.damage * player_damage_multiplier));
                    const int applied_damage = current_boss->take_damage(std::max(1, scaled_damage));
                    if (owner) {
                        owner->shots_hit++;
                        owner->total_damage_dealt += applied_damage;
                    }
                    if (applied_damage > 0) {
                        particles.emit_explosion(b.pos, COLOR_GOLD_BRIGHT, 6, 90.0f);
                        particles.add_floating_text(b.pos, std::to_string(applied_damage), COLOR_GOLD_BRIGHT);
                        if (g_screen_shake_enabled) particles.trigger_screen_shake(2.0f, 0.06f);
                        SoundSystem::instance().play_sfx("hit.wav", 0.4f);
                    } else {
                        particles.emit_explosion(b.pos, COLOR_CYAN_BRIGHT, 4, 65.0f);
                        particles.add_floating_text(b.pos, "SHIELDED", COLOR_CYAN_BRIGHT);
                    }

                    if (b.pierce_remaining > 0) {
                        b.pierce_remaining--;
                    } else {
                        b.active = false;
                    }
                    continue;
                }
            }

            // Query spatial grid for nearby enemies
            m_grid.query(b.pos, b.radius + 15.0f, candidate_indices);
            for (int idx : candidate_indices) {
                if (idx < 0 || idx >= static_cast<int>(enemies.size())) continue;
                Enemy& enemy = enemies[idx];
                if (!enemy.active) continue;

                if (Vector2Distance(b.pos, enemy.pos) < (b.radius + enemy.radius)) {
                    if (owner) {
                        owner->shots_hit++;
                    }

                    // 1. Critical Hit Calculation
                    bool is_crit = (std::rand() % 100) < static_cast<int>(CRIT_CHANCE * 100.0f);
                    int final_dmg = std::max(1, static_cast<int>(std::round(b.damage * player_damage_multiplier)));
                    if (is_crit) {
                        final_dmg = static_cast<int>(final_dmg * CRIT_MULTIPLIER);
                    }

                    // 2. Critical hit execution with Yama boon or baseline execute threshold
                    if (owner && owner->has_boon(BoonType::YAMA_FATAL_DECREE) && enemy.hp < enemy.max_hp * 0.4f) {
                        final_dmg = static_cast<int>(final_dmg * 1.6f);
                        particles.add_floating_text(enemy.pos, "FATAL DECREE!", COLOR_PURPLE_BRIGHT);
                    } else if (enemy.hp <= enemy.max_hp * EXECUTE_THRESHOLD) {
                        final_dmg = static_cast<int>(final_dmg * EXECUTE_BONUS);
                        particles.add_floating_text(enemy.pos, "EXECUTE!", COLOR_RED_BRIGHT);
                    }

                    if (is_crit) {
                        particles.add_floating_text({ enemy.pos.x, enemy.pos.y - 12.0f }, "+CRIT!", COLOR_GOLD_BRIGHT);
                        if (owner) owner->score += SCORE_CRIT_BONUS;
                    }

                    enemy.hp -= final_dmg;
                    enemy.hit_flash = 0.15f;
                    if (owner) owner->total_damage_dealt += final_dmg;

                    particles.emit_explosion(b.pos, is_crit ? COLOR_GOLD_BRIGHT : b.color, is_crit ? 10 : 5, is_crit ? 130.0f : 80.0f);
                    particles.add_floating_text(enemy.pos, std::to_string(final_dmg), is_crit ? COLOR_GOLD_BRIGHT : b.color);
                    if (g_screen_shake_enabled) particles.trigger_screen_shake(is_crit ? 4.0f : 1.5f, is_crit ? 0.14f : 0.05f);
                    SoundSystem::instance().play_sfx("hit.wav", is_crit ? 0.6f : 0.35f);

                    // Chain lightning on hit (Indra boon)
                    if (owner && owner->has_boon(BoonType::INDRA_VAJRA_THUNDER) && (std::rand() % 100 < 35)) {
                        for (auto& other_e : enemies) {
                            if (other_e.active && &other_e != &enemy && Vector2Distance(enemy.pos, other_e.pos) < 160.0f) {
                                other_e.hp -= 20;
                                other_e.hit_flash = 0.2f;
                                particles.emit_explosion(other_e.pos, COLOR_CYAN_BRIGHT, 8, 120.0f);
                                break;
                            }
                        }
                    }

                    // Enemy death
                    if (enemy.hp <= 0) {
                        enemy.active = false;
                        if (owner) {
                            owner->kills++;
                            owner->add_combo();
                            int elite_multiplier = enemy.is_miniboss ? 1 : enemy.is_elite ? 2 : 1;
                            int kill_score = enemy.score_value * elite_multiplier * owner->combo;
                            owner->score += kill_score;
                        }
                        int prana_drop = enemy.is_miniboss ? 50 : enemy.is_elite ? 8 : 2;
                        out_prana_earned += prana_drop;

                        if (enemy.is_elite) {
                            particles.add_floating_text(enemy.pos,
                                enemy.is_miniboss ? "MINI-BOSS SLAIN +50 PRANA" : "ELITE SLAIN +8 PRANA",
                                enemy.is_miniboss ? COLOR_RED_BRIGHT : COLOR_GOLD_BRIGHT);
                        }

                        const int explosion_particles = enemy.is_miniboss ? 65 : enemy.is_elite ? 35 : 22;
                        const float shake_strength = enemy.is_miniboss ? 13.0f : enemy.is_elite ? 9.0f : 5.0f;
                        particles.emit_explosion(enemy.pos,
                            enemy.is_miniboss ? COLOR_RED_BRIGHT : enemy.is_elite ? COLOR_GOLD_BRIGHT : COLOR_ORANGE_BRIGHT,
                            explosion_particles, 260.0f);
                        if (g_screen_shake_enabled) particles.trigger_screen_shake(shake_strength, enemy.is_miniboss ? 0.32f : enemy.is_elite ? 0.24f : 0.12f);
                        SoundSystem::instance().play_sfx("explosion.wav", 0.6f);

                        // Mini-bosses guarantee a supply drop; elites have a better chance.
                        int drop_chance = enemy.is_miniboss ? 100 : enemy.is_elite ? 50 : 22;
                        if ((std::rand() % 100) < drop_chance) {
                            Powerup p;
                            p.active = true;
                            p.pos = enemy.pos;
                            int type_roll = std::rand() % 6;
                            p.type = static_cast<PowerupType>(type_roll);
                            powerups.push_back(p);
                        }
                    }

                    if (b.pierce_remaining > 0) {
                        b.pierce_remaining--;
                    } else {
                        b.active = false;
                        break;
                    }
                }
            }
        }

        // 3. Enemy Bullets vs Squad Members
        for (auto& b : bullets) {
            if (!b.active || !b.is_enemy) continue;
            for (auto* p : squad) {
                if (!p || p->is_downed) continue;
                if (Vector2Distance(b.pos, p->pos) < (b.radius + p->radius)) {
                    const int hp_before = p->hp;
                    if (p->take_damage(b.damage, b.damage_source)) {
                        emit_player_hit_feedback(*p, hp_before);
                    }
                    b.active = false;
                    break;
                }
            }
        }

        // 4. Squad Members vs Enemies (Contact damage)
        for (auto* p : squad) {
            if (!p || p->is_downed) continue;
            m_grid.query(p->pos, p->radius + 20.0f, candidate_indices);
            for (int idx : candidate_indices) {
                if (idx < 0 || idx >= static_cast<int>(enemies.size())) continue;
                Enemy& enemy = enemies[idx];
                if (!enemy.active) continue;

                if (Vector2Distance(p->pos, enemy.pos) < (p->radius + enemy.radius)) {
                    const int hp_before = p->hp;
                    bool damaged = p->take_damage(PLAYER_CONTACT_DAMAGE, enemy.damage_source_name());
                    enemy.hp -= 30; // Contact recoil damage
                    if (damaged) emit_player_hit_feedback(*p, hp_before);
                    if (enemy.hp <= 0) {
                        enemy.active = false;
                        p->kills++;
                        particles.emit_explosion(enemy.pos, COLOR_ORANGE_BRIGHT, 20, 180.0f);
                    }
                }
            }
        }

        // 5. Squad Members vs Astral Cubes
        for (auto& pw : powerups) {
            if (!pw.active) continue;
            for (auto* p : squad) {
                if (!p || p->is_downed) continue;
                if (Vector2Distance(pw.pos, p->pos) < (pw.radius + p->radius + 10.0f)) {
                    pw.active = false;
                    SoundSystem::instance().play_sfx("powerup.wav", 0.7f);
                    particles.emit_explosion(pw.pos, COLOR_CYAN_BRIGHT, 15, 140.0f);

                    switch (pw.type) {
                        case PowerupType::KAVACH_SHIELD:
                            p->has_kavach_shield = true;
                            p->kavach_timer = 8.0f;
                            particles.add_floating_text(p->pos, "KAVACH SHIELD!", COLOR_CYAN_BRIGHT);
                            break;
                        case PowerupType::AGNEYASTRA_SPREAD:
                            p->buff_agneyastra_timer = 10.0f;
                            particles.add_floating_text(p->pos, "AGNEYASTRA SPREAD!", COLOR_RED_BRIGHT);
                            break;
                        case PowerupType::VAYAVYASTRA_SPEED:
                            p->buff_speed_timer = 10.0f;
                            p->dash_charges = p->max_dash_charges;
                            particles.add_floating_text(p->pos, "VAYU SURGE!", COLOR_GREEN_BRIGHT);
                            break;
                        case PowerupType::AMRITA_HEAL:
                            p->hp = std::min(p->max_hp, p->hp + 35);
                            particles.add_floating_text(p->pos, "+35 HP AMRITA", { 80, 240, 180, 255 });
                            break;
                        case PowerupType::BRAHMASTRA_BOMB:
                            p->brahmastra_bombs++;
                            particles.add_floating_text(p->pos, "+1 BRAHMASTRA BOMB", COLOR_GOLD_BRIGHT);
                            break;
                        case PowerupType::ASTRA_OVERDRIVE:
                            p->buff_overdrive_timer = 8.0f;
                            particles.add_floating_text(p->pos, "ASTRA OVERDRIVE!", COLOR_PURPLE_BRIGHT);
                            break;
                    }
                    break;
                }
            }
        }
    }

    void resolve_combat(
        std::vector<Player>& squad,
        std::vector<Enemy>& enemies,
        Boss* current_boss,
        std::vector<Bullet>& bullets,
        std::vector<Powerup>& powerups,
        ParticleSystem& particles,
        int& out_prana_earned,
        float player_damage_multiplier = 1.0f
    ) {
        std::vector<Player*> ptrs;
        ptrs.reserve(squad.size());
        for (auto& p : squad) ptrs.push_back(&p);
        resolve_combat_ptrs(ptrs, enemies, current_boss, bullets, powerups, particles,
                            out_prana_earned, player_damage_multiplier);
    }

    void resolve_combat(
        Player& player,
        std::vector<Enemy>& enemies,
        Boss* current_boss,
        std::vector<Bullet>& bullets,
        std::vector<Powerup>& powerups,
        ParticleSystem& particles,
        int& out_prana_earned,
        float player_damage_multiplier = 1.0f
    ) {
        std::vector<Player*> ptrs = { &player };
        resolve_combat_ptrs(ptrs, enemies, current_boss, bullets, powerups, particles,
                            out_prana_earned, player_damage_multiplier);
    }

private:
    DSA::SpatialGrid m_grid;
};

} // namespace Vimana
