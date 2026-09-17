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
};

class WaveManager {
public:
    WaveManager() : m_current_wave(1), m_wave_timer(0.0f), m_is_wave_in_progress(false), m_boss_active(false) {}

    void start_campaign(int start_wave = 1) {
        m_current_wave = start_wave;
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

        // Generate standard wave composition
        int total_enemies = 8 + wave * 2;
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
            m_spawn_queue.push({ type, current_delay, pos });
            current_delay += 0.8f + (std::rand() % 8) / 10.0f;
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
                float spd_mult = 1.0f + (m_current_wave * 0.02f);
                float hp_mult = 1.0f + (m_current_wave * 0.05f);
                enemy.init(next_spawn.type, next_spawn.spawn_pos, spd_mult, hp_mult);
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

    std::string get_story_transmission() const {
        if (m_current_wave == 11) {
            return "TRANSMISSION // VIBHISHANA: 'I defect from Lanka's tyranny. Ravana's citadel harnesses void portals. Seek the celestial astras.'";
        } else if (m_current_wave == 25) {
            return "WARNING // CONQUEROR INDRAJIT HAS ENGAGED. BEWARE ILLUSORY CLONES AND SERPENT ARROWS.";
        } else if (m_current_wave == 30) {
            return "FINAL APOTHEOSIS // EMPEROR HIRANYAKASHIPU INVOKES HIS IMMORTAL PACT. STRIKE AT THE THRESHOLD TO SUMMON NARASIMHA!";
        }
        return "";
    }

private:
    int m_current_wave;
    float m_wave_timer;
    float m_banner_timer = 0.0f;
    bool m_is_wave_in_progress;
    bool m_boss_active;
    Boss m_current_boss;
    std::queue<SpawnInstruction> m_spawn_queue;
};

} // namespace Vimana
