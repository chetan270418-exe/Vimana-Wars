#pragma once
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

    void resolve_combat(
        Player& player,
        std::vector<Enemy>& enemies,
        Boss* current_boss,
        std::vector<Bullet>& bullets,
        std::vector<Powerup>& powerups,
        ParticleSystem& particles,
        int& out_prana_earned
    ) {
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

            // Check Boss first if active
            if (current_boss && current_boss->active) {
                if (Vector2Distance(b.pos, current_boss->pos) < (b.radius + current_boss->radius)) {
                    current_boss->take_damage(b.damage);
                    player.total_damage_dealt += b.damage;
                    particles.emit_explosion(b.pos, COLOR_GOLD_BRIGHT, 6, 90.0f);
                    particles.add_floating_text(b.pos, std::to_string(b.damage), COLOR_GOLD_BRIGHT);
                    SoundSystem::instance().play_sfx("hit.wav", 0.4f);

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
                    // 1. Critical Hit Calculation
                    bool is_crit = (std::rand() % 100) < static_cast<int>(CRIT_CHANCE * 100.0f);
                    int final_dmg = b.damage;
                    if (is_crit) {
                        final_dmg = static_cast<int>(final_dmg * CRIT_MULTIPLIER);
                    }

                    // 2. Critical hit execution with Yama boon or baseline execute threshold
                    if (player.has_boon(BoonType::YAMA_FATAL_DECREE) && enemy.hp < enemy.max_hp * 0.4f) {
                        final_dmg = static_cast<int>(final_dmg * 1.6f);
                        particles.add_floating_text(enemy.pos, "FATAL DECREE!", COLOR_PURPLE_BRIGHT);
                    } else if (enemy.hp <= enemy.max_hp * EXECUTE_THRESHOLD) {
                        final_dmg = static_cast<int>(final_dmg * EXECUTE_BONUS);
                        particles.add_floating_text(enemy.pos, "EXECUTE!", COLOR_RED_BRIGHT);
                    }

                    if (is_crit) {
                        particles.add_floating_text({ enemy.pos.x, enemy.pos.y - 12.0f }, "+CRIT!", COLOR_GOLD_BRIGHT);
                        player.score += SCORE_CRIT_BONUS;
                    }

                    enemy.hp -= final_dmg;
                    enemy.hit_flash = 0.15f;
                    player.total_damage_dealt += final_dmg;
                    particles.emit_explosion(b.pos, is_crit ? COLOR_GOLD_BRIGHT : b.color, is_crit ? 10 : 5, is_crit ? 130.0f : 80.0f);
                    particles.add_floating_text(enemy.pos, std::to_string(final_dmg), is_crit ? COLOR_GOLD_BRIGHT : b.color);
                    SoundSystem::instance().play_sfx("hit.wav", is_crit ? 0.6f : 0.35f);

                    // Chain lightning on hit (Indra boon)
                    if (player.has_boon(BoonType::INDRA_VAJRA_THUNDER) && (std::rand() % 100 < 35)) {
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
                        player.kills++;
                        player.add_combo();
                        int kill_score = (enemy.is_elite ? enemy.score_value * 2 : enemy.score_value) * player.combo;
                        player.score += kill_score;
                        int prana_drop = enemy.is_elite ? 8 : 2;
                        out_prana_earned += prana_drop;

                        if (enemy.is_elite) {
                            particles.add_floating_text(enemy.pos, "ELITE SLAIN +8 PRANA", COLOR_GOLD_BRIGHT);
                        }

                        particles.emit_explosion(enemy.pos, enemy.is_elite ? COLOR_GOLD_BRIGHT : COLOR_ORANGE_BRIGHT, enemy.is_elite ? 35 : 22, 220.0f);
                        SoundSystem::instance().play_sfx("explosion.wav", 0.6f);

                        // Drop Astral Ability Cube / Amrita (22% chance, 50% for elite)
                        int drop_chance = enemy.is_elite ? 50 : 22;
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

        // 3. Enemy Bullets vs Player
        for (auto& b : bullets) {
            if (!b.active || !b.is_enemy) continue;
            if (Vector2Distance(b.pos, player.pos) < (b.radius + player.radius)) {
                player.take_damage(b.damage);
                particles.emit_explosion(b.pos, COLOR_RED_BRIGHT, 10, 110.0f);
                particles.trigger_screen_shake(7.0f, 0.25f);
                SoundSystem::instance().play_sfx("hit.wav", 0.8f);
                b.active = false;
            }
        }

        // 4. Player vs Enemies (Contact damage)
        m_grid.query(player.pos, player.radius + 20.0f, candidate_indices);
        for (int idx : candidate_indices) {
            if (idx < 0 || idx >= static_cast<int>(enemies.size())) continue;
            Enemy& enemy = enemies[idx];
            if (!enemy.active) continue;

            if (Vector2Distance(player.pos, enemy.pos) < (player.radius + enemy.radius)) {
                player.take_damage(PLAYER_CONTACT_DAMAGE);
                enemy.hp -= 30; // Contact recoil damage
                particles.trigger_screen_shake(8.0f, 0.3f);
                if (enemy.hp <= 0) {
                    enemy.active = false;
                    player.kills++;
                    particles.emit_explosion(enemy.pos, COLOR_ORANGE_BRIGHT, 20, 180.0f);
                }
            }
        }

        // 5. Player vs Astral Cubes
        for (auto& p : powerups) {
            if (!p.active) continue;
            if (Vector2Distance(p.pos, player.pos) < (p.radius + player.radius + 10.0f)) {
                p.active = false;
                SoundSystem::instance().play_sfx("powerup.wav", 0.7f);
                particles.emit_explosion(p.pos, COLOR_CYAN_BRIGHT, 15, 140.0f);

                switch (p.type) {
                    case PowerupType::KAVACH_SHIELD:
                        player.has_kavach_shield = true;
                        player.kavach_timer = 8.0f;
                        particles.add_floating_text(player.pos, "KAVACH SHIELD!", COLOR_CYAN_BRIGHT);
                        break;
                    case PowerupType::AGNEYASTRA_SPREAD:
                        player.buff_agneyastra_timer = 10.0f;
                        particles.add_floating_text(player.pos, "AGNEYASTRA SPREAD!", COLOR_RED_BRIGHT);
                        break;
                    case PowerupType::VAYAVYASTRA_SPEED:
                        player.buff_speed_timer = 10.0f;
                        player.dash_charges = player.max_dash_charges;
                        particles.add_floating_text(player.pos, "VAYU SURGE!", COLOR_GREEN_BRIGHT);
                        break;
                    case PowerupType::AMRITA_HEAL:
                        player.hp = std::min(player.max_hp, player.hp + 35);
                        particles.add_floating_text(player.pos, "+35 HP AMRITA", { 80, 240, 180, 255 });
                        break;
                    case PowerupType::BRAHMASTRA_BOMB:
                        player.brahmastra_bombs++;
                        particles.add_floating_text(player.pos, "+1 BRAHMASTRA BOMB", COLOR_GOLD_BRIGHT);
                        break;
                    case PowerupType::ASTRA_OVERDRIVE:
                        player.buff_overdrive_timer = 8.0f;
                        particles.add_floating_text(player.pos, "ASTRA OVERDRIVE!", COLOR_PURPLE_BRIGHT);
                        break;
                }
            }
        }
    }

private:
    DSA::SpatialGrid m_grid;
};

} // namespace Vimana
