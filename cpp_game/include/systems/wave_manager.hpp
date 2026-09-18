#pragma once
#include <vector>
#include <string>
#include <queue>
#include <iostream>
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/enemy.hpp"
#include "entities/boss.hpp"

namespace Vimana {

struct SpawnInstruction {
    EnemyType type;
    float delay;
    Vector2 spawn_pos;
    bool elite = false;
};

class WaveManager {
public:
    WaveManager() 
        : m_current_wave(1), m_wave_timer(0.0f), m_is_wave_in_progress(false), m_boss_active(false),
          m_difficulty_profile(DIFFICULTY_PROFILES[1]), m_player_count(1) {}

    void set_difficulty(Difficulty diff) {
        for (const auto& dp : DIFFICULTY_PROFILES) {
            if (dp.tier == diff) {
                m_difficulty_profile = dp;
                break;
            }
        }
    }

    void set_player_count(int count) {
        m_player_count = std::max(1, count);
    }

    void start_campaign(int start_wave = 1, Difficulty diff = Difficulty::KSHATRIYA, int players = 1) {
        m_current_wave = start_wave;
        set_difficulty(diff);
        m_player_count = players;
        m_is_wave_in_progress = false;
        m_boss_active = false;
        m_banner_timer = 2.5f;
        prepare_wave(m_current_wave);
    }

    void prepare_wave(int wave) {
        m_current_wave = wave;
        m_is_wave_in_progress = true;
        m_banner_timer = 2.5f;
        while (!m_spawn_queue.empty()) m_spawn_queue.pop();

        // Check for Boss Wave
        if (wave == 5) {
            m_boss_active = true;
            m_current_boss.init(BossID::KUMBHAKARNA);
            return;
        } else if (wave == 10) {
            m_boss_active = true;
            m_current_boss.init(BossID::RAVANA);
            return;
        } else if (wave == 15) {
            m_boss_active = true;
            m_current_boss.init(BossID::MAHISHASURA);
            return;
        } else if (wave == 25) {
            m_boss_active = true;
            m_current_boss.init(BossID::INDRAJIT);
            return;
        } else if (wave == 30) {
            m_boss_active = true;
            m_current_boss.init(BossID::HIRANYAKASHIPU);
            return;
        }

        m_boss_active = false;

        // Generate standard wave composition with scaling
        int base_enemies = 8 + wave * 2 + m_difficulty_profile.min_enemies_bonus;
        // Co-op enemy count scaling: EnemyCount = BaseCount * (1 + 0.35 * (Players - 1))
        int total_enemies = static_cast<int>(base_enemies * (1.0f + CO_OP_ENEMY_SCALE_PER_PLAYER * (m_player_count - 1)));
        float current_delay = 0.5f;

        for (int i = 0; i < total_enemies; ++i) {
            EnemyType type = EnemyType::ASURA_CHASER;
            int roll = std::rand() % 100;

            if (wave >= 12 && roll < 20) {
                type = EnemyType::ASURA_SNIPER;
            } else if (wave >= 8 && roll < 40) {
                type = EnemyType::ASURA_HEALER;
            } else if (wave >= 6 && roll < 60) {
                type = EnemyType::ASURA_KAMIKAZE;
            } else if (wave >= 3 && roll < 80) {
                type = EnemyType::ASURA_SHOOTER;
            } else if (wave >= 2 && roll < 90) {
                type = EnemyType::ASURA_TANK;
            }

            float spawn_x = 40.0f + static_cast<float>(std::rand() % (SCREEN_WIDTH - 80));
            Vector2 pos = { spawn_x, -30.0f };
            bool guaranteed_elite = (wave % ELITE_SPAWN_EVERY_N_WAVES == 0) && (i % 6 == 0);
            bool chance_elite = (std::rand() % 100) < static_cast<int>((m_difficulty_profile.elite_chance_bonus + 0.04f * (m_player_count - 1)) * 100.0f);
            m_spawn_queue.push({ type, current_delay, pos, guaranteed_elite || chance_elite });
            current_delay += 0.7f + (std::rand() % 7) / 10.0f;
        }
    }

    void update(float dt, std::vector<Enemy>& enemies, std::vector<Bullet>& bullets, Vector2 player_pos) {
        if (m_banner_timer > 0) m_banner_timer -= dt;

        if (m_boss_active) {
            if (m_current_boss.active) {
                m_current_boss.update(dt, player_pos, bullets);
            } else {
                // Boss defeated!
                m_boss_active = false;
                m_is_wave_in_progress = false;
            }
            return;
        }

        // Spawn timer
        m_wave_timer += dt;
        if (!m_spawn_queue.empty()) {
            const auto& next_spawn = m_spawn_queue.front();
            if (m_wave_timer >= next_spawn.delay) {
                Enemy enemy;
                float spd_mult = (1.0f + (m_current_wave * 0.02f)) * m_difficulty_profile.bullet_speed_mult;
                float hp_mult = (1.0f + (m_current_wave * 0.05f)) * m_difficulty_profile.enemy_hp_mult;

                enemy.init(next_spawn.type, next_spawn.spawn_pos, spd_mult, hp_mult, next_spawn.elite);
                enemies.push_back(enemy);
                m_spawn_queue.pop();
            }
        } else {
            // Check if all enemies in the wave are defeated
            bool any_alive = false;
            for (const auto& e : enemies) {
                if (e.active) {
                    any_alive = true;
                    break;
                }
            }
            if (!any_alive) {
                m_is_wave_in_progress = false;
            }
        }
    }

    bool is_wave_cleared() const {
        return !m_is_wave_in_progress && (!m_boss_active || !m_current_boss.active);
    }

    int current_wave() const { return m_current_wave; }
    bool is_boss_wave() const { return m_boss_active; }
    Boss& get_boss() { return m_current_boss; }
    const Boss& get_boss() const { return m_current_boss; }
    float banner_timer() const { return m_banner_timer; }
    const CampaignRealm& get_realm_data() const { return GetCampaignRealmForWave(m_current_wave); }

    std::string get_story_transmission() const {
        if (m_current_wave == 11) {
            return "TRANSMISSION // VIBHISHANA: 'I defect from Lanka's tyranny. Ravana's citadel harnesses void portals. Seek the celestial astras.'";
        } else if (m_current_wave == 25) {
            return "WARNING // CONQUEROR INDRAJIT HAS ENGAGED. BEWARE ILLUSORY CLONES AND SERPENT ARROWS.";
        } else if (m_current_wave == 30) {
            return "FINAL APOTHEOSIS // EMPEROR HIRANYAKASHIPU INVOKES HIS IMMORTAL PACT. STRIKE AT THE THRESHOLD TO SUMMON NARASIMHA!";
        }
        if (m_boss_active) {
            return "BOSS ENGAGEMENT // BREAK THE GUARDIAN'S PHASES TO ADVANCE.";
        }
        int goal = 8 + m_current_wave * 2 + m_difficulty_profile.min_enemies_bonus;
        return "MISSION GOAL // PURGE " + std::to_string(goal) + " HOSTILES TO ADVANCE.";
    }

private:
    int m_current_wave;
    float m_wave_timer;
    float m_banner_timer = 0.0f;
    bool m_is_wave_in_progress;
    bool m_boss_active;
    Boss m_current_boss;
    std::queue<SpawnInstruction> m_spawn_queue;
    DifficultyProfile m_difficulty_profile;
    int m_player_count = 1;
};

} // namespace Vimana
