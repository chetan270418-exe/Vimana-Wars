#pragma once
#include <vector>
#include <string>
#include <queue>
#include <array>
#include <cmath>
#include <algorithm>
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

enum class WavePattern { PATROL, INTERCEPTOR_SWARM, SIEGE_LINE, ELITE_HUNT, RIFT_AMBUSH, BOSS_DUEL };

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
        m_wave_timer = 0.0f;
        m_is_wave_in_progress = true;
        m_banner_timer = 2.5f;
        while (!m_spawn_queue.empty()) m_spawn_queue.pop();

        const int act = CampaignActForWave(wave);
        const int act_wave = CampaignWaveWithinAct(wave);
        switch (act_wave % 6) {
            case 2: m_wave_pattern = WavePattern::INTERCEPTOR_SWARM; break;
            case 3: m_wave_pattern = WavePattern::SIEGE_LINE; break;
            case 4: m_wave_pattern = WavePattern::ELITE_HUNT; break;
            case 0: m_wave_pattern = WavePattern::RIFT_AMBUSH; break;
            default: m_wave_pattern = WavePattern::PATROL; break;
        }
        if (act_wave % 5 == 0) {
            m_wave_pattern = WavePattern::BOSS_DUEL;
            m_boss_active = true;
            static constexpr std::array<BossID, 8> boss_rotation = {
                BossID::KUMBHAKARNA, BossID::RAVANA, BossID::MAHISHASURA,
                BossID::MAKARA, BossID::INDRAJIT, BossID::HIRANYAKASHIPU,
                BossID::MEGHNADA, BossID::VRITRA
            };
            const int boss_slot = act_wave / 5 - 1;
            const int boss_index = (boss_slot + act - 1) % static_cast<int>(boss_rotation.size());
            m_current_boss.init(boss_rotation[boss_index]);
            m_current_boss.scale_for_act(act, m_difficulty_profile.enemy_hp_mult, m_difficulty_profile.bullet_speed_mult);

            // Boss waves are fleet encounters too: the boss enters with a coordinated escort wing.
            const int escort_count = 5 + std::min(5, (act - 1) / 2);
            m_wave_enemy_goal = escort_count;
            for (int i = 0; i < escort_count; ++i) {
                EnemyType type = (i % 4 == 0) ? EnemyType::ASURA_SHOOTER :
                                 (i % 3 == 0) ? EnemyType::ASURA_TANK : EnemyType::ASURA_CHASER;
                const float x = 90.0f + (SCREEN_WIDTH - 180.0f) * (i + 0.5f) / escort_count;
                const Vector2 spawn_pos = { x, -35.0f - (i % 2) * 28.0f };
                m_spawn_queue.push({ type, 0.75f + (i / 5) * 0.45f + (i % 5) * 0.025f,
                                     spawn_pos, i == 2 || (act >= 4 && i % 4 == 0) });
            }
            return;
        }

        m_boss_active = false;
        m_current_boss.active = false;

        // Tutorial beats: Act 1 Waves 1-5 staged (chasers -> tanks -> shooters -> mixed -> mini-elite)
        if (act == 1 && act_wave >= 1 && act_wave <= 5) {
            struct Beat { EnemyType t; float d; };
            std::vector<Beat> beats;
            if (act_wave == 1) {
                for (int i = 0; i < 8; ++i) beats.push_back({EnemyType::ASURA_CHASER, 0.5f + i * 0.8f});
            } else if (act_wave == 2) {
                for (int i = 0; i < 6; ++i) beats.push_back({EnemyType::ASURA_CHASER, 0.5f + i * 0.7f});
                for (int i = 0; i < 2; ++i) beats.push_back({EnemyType::ASURA_TANK, 3.0f + i * 1.5f});
            } else if (act_wave == 3) {
                for (int i = 0; i < 5; ++i) beats.push_back({EnemyType::ASURA_CHASER, 0.5f + i * 0.6f});
                for (int i = 0; i < 3; ++i) beats.push_back({EnemyType::ASURA_SHOOTER, 2.5f + i * 1.0f});
                beats.push_back({EnemyType::ASURA_TANK, 5.0f});
            } else if (act_wave == 4) {
                for (int i = 0; i < 4; ++i) beats.push_back({EnemyType::ASURA_CHASER, 0.5f + i * 0.5f});
                for (int i = 0; i < 2; ++i) beats.push_back({EnemyType::ASURA_KAMIKAZE, 2.0f + i * 0.9f});
                for (int i = 0; i < 2; ++i) beats.push_back({EnemyType::ASURA_SHOOTER, 3.5f + i * 1.0f});
                beats.push_back({EnemyType::ASURA_TANK, 5.5f});
            } else {
                for (int i = 0; i < 5; ++i) beats.push_back({EnemyType::ASURA_CHASER, 0.5f + i * 0.5f});
                beats.push_back({EnemyType::ASURA_TANK, 3.0f});
                beats.push_back({EnemyType::ASURA_SHOOTER, 3.8f});
                beats.push_back({EnemyType::ASURA_KAMIKAZE, 4.5f});
                beats.push_back({EnemyType::ASURA_HEALER, 6.0f});
            }
            m_wave_enemy_goal = (int)beats.size();
            for (auto &b : beats) {
                float sx = 70.0f + static_cast<float>(std::rand() % (SCREEN_WIDTH - 140));
                m_spawn_queue.push({b.t, b.d, {sx, -30.0f}, act_wave == 5 && b.t == EnemyType::ASURA_TANK});
            }
            return;
        }

        // Act I's first post-tutorial beats are authored formations rather than
        // the procedural composition used later in the campaign. Wave 10 is
        // intentionally handled above as a boss-and-escort fleet encounter.
        if (act == 1 && act_wave >= 6 && act_wave <= 9) {
            struct FormationBeat { EnemyType type; int count; float first_delay; float spacing; bool elite; };
            std::vector<FormationBeat> formation;
            switch (act_wave) {
                case 6: formation = {
                    { EnemyType::ASURA_CHASER, 8, 0.35f, 0.28f, false },
                    { EnemyType::ASURA_KAMIKAZE, 4, 1.2f, 0.48f, false },
                    { EnemyType::ASURA_SHOOTER, 3, 2.0f, 0.65f, false }
                }; break;
                case 7: formation = {
                    { EnemyType::ASURA_TANK, 4, 0.4f, 0.72f, false },
                    { EnemyType::ASURA_SHOOTER, 6, 0.8f, 0.42f, false },
                    { EnemyType::ASURA_CHASER, 5, 2.4f, 0.38f, false }
                }; break;
                case 8: formation = {
                    { EnemyType::ASURA_SNIPER, 3, 0.5f, 1.0f, false },
                    { EnemyType::ASURA_HEALER, 3, 1.1f, 0.9f, false },
                    { EnemyType::ASURA_CHASER, 8, 1.4f, 0.32f, false }
                }; break;
                default: formation = {
                    { EnemyType::ASURA_KAMIKAZE, 5, 0.35f, 0.45f, false },
                    { EnemyType::ASURA_TANK, 3, 1.0f, 0.85f, true },
                    { EnemyType::ASURA_SNIPER, 3, 1.8f, 0.8f, false },
                    { EnemyType::ASURA_CHASER, 7, 2.0f, 0.34f, false }
                }; break;
            }
            m_wave_pattern = (act_wave == 6) ? WavePattern::INTERCEPTOR_SWARM :
                             (act_wave == 7) ? WavePattern::SIEGE_LINE :
                             (act_wave == 8) ? WavePattern::RIFT_AMBUSH : WavePattern::ELITE_HUNT;
            m_wave_enemy_goal = 0;
            std::vector<SpawnInstruction> staged_spawns;
            for (const auto& group : formation) {
                for (int i = 0; i < group.count; ++i) {
                    const float lane = static_cast<float>((i * 2 + group.count) % 9) / 8.0f;
                    const float x = 70.0f + lane * (SCREEN_WIDTH - 140.0f);
                    const float y = -30.0f - static_cast<float>(i % 3) * 22.0f;
                    staged_spawns.push_back({ group.type, group.first_delay + i * group.spacing, { x, y }, group.elite });
                    ++m_wave_enemy_goal;
                }
            }
            std::stable_sort(staged_spawns.begin(), staged_spawns.end(),
                [](const SpawnInstruction& lhs, const SpawnInstruction& rhs) { return lhs.delay < rhs.delay; });
            for (const auto& spawn : staged_spawns) m_spawn_queue.push(spawn);
            return;
        }

        // Generate standard wave composition with scaling
        const float act_pressure = std::sqrt(static_cast<float>(act - 1));
        // Boosted enemy counts so each wave is a real fight, not a trickle.
        // Acts 1-2: ~12-20 enemies; mid-game: 30-50; late-game: 80-120.
        int base_enemies = 12 + act_wave * 3 + m_difficulty_profile.min_enemies_bonus + static_cast<int>(act_pressure * 6.0f);
        if (m_wave_pattern == WavePattern::INTERCEPTOR_SWARM || m_wave_pattern == WavePattern::RIFT_AMBUSH) base_enemies = static_cast<int>(base_enemies * 1.35f);
        if (m_wave_pattern == WavePattern::SIEGE_LINE || m_wave_pattern == WavePattern::ELITE_HUNT) base_enemies = static_cast<int>(base_enemies * 0.9f);
        // Co-op enemy count scaling: EnemyCount = BaseCount * (1 + 0.35 * (Players - 1))
        int total_enemies = std::clamp(static_cast<int>(base_enemies * (1.0f + CO_OP_ENEMY_SCALE_PER_PLAYER * (m_player_count - 1))), 12, 180);
        m_wave_enemy_goal = total_enemies;
        float current_delay = 0.35f;
        int spawned = 0;

        while (spawned < total_enemies) {
            // Bigger squads: 5-10 enemies arrive together (was 3-6).
            // Creates the "swarm" feel - many ships attacking at once, not one-by-one.
            const int squad_size = std::min(total_enemies - spawned, 5 + std::rand() % 6);
            const float squad_center_x = 70.0f + static_cast<float>(std::rand() % (SCREEN_WIDTH - 140));
            for (int member = 0; member < squad_size; ++member, ++spawned) {
            EnemyType type = EnemyType::ASURA_CHASER;
            int roll = std::rand() % 100;

            if (m_wave_pattern == WavePattern::INTERCEPTOR_SWARM) {
                // Swarm: 60% fast chasers + kamikazes, 25% shooters for support fire
                type = roll < 60 ? EnemyType::ASURA_CHASER : roll < 80 ? EnemyType::ASURA_KAMIKAZE : EnemyType::ASURA_SHOOTER;
            } else if (m_wave_pattern == WavePattern::SIEGE_LINE) {
                // Siege: tanks anchor the line, shooters+snipers fire from behind, healers keep them alive
                type = roll < 35 ? EnemyType::ASURA_TANK : roll < 60 ? EnemyType::ASURA_SHOOTER
                       : roll < 80 ? EnemyType::ASURA_HEALER : EnemyType::ASURA_SNIPER;
            } else if (m_wave_pattern == WavePattern::ELITE_HUNT) {
                // Elite: all dangerous, mixed - tanks + snipers + shooters + kamikazes together
                type = roll < 30 ? EnemyType::ASURA_TANK : roll < 55 ? EnemyType::ASURA_SNIPER
                       : roll < 78 ? EnemyType::ASURA_SHOOTER : EnemyType::ASURA_KAMIKAZE;
            } else if (m_wave_pattern == WavePattern::RIFT_AMBUSH) {
                // Ambush: snipers in back, kamikazes rush in, healers patch them up
                type = roll < 30 ? EnemyType::ASURA_SNIPER : roll < 60 ? EnemyType::ASURA_KAMIKAZE
                       : roll < 80 ? EnemyType::ASURA_HEALER : EnemyType::ASURA_CHASER;
            } else if (act_wave >= 22) {
                // Late-act mixed assault: ALL 6 types in coordinated wave
                type = roll < 22 ? EnemyType::ASURA_SNIPER : roll < 42 ? EnemyType::ASURA_KAMIKAZE
                       : roll < 60 ? EnemyType::ASURA_HEALER : roll < 75 ? EnemyType::ASURA_SHOOTER
                       : roll < 90 ? EnemyType::ASURA_TANK : EnemyType::ASURA_CHASER;
            } else if (act_wave >= 15) {
                // Mid-late: 4 types together
                type = roll < 28 ? EnemyType::ASURA_SNIPER : roll < 52 ? EnemyType::ASURA_KAMIKAZE
                       : roll < 74 ? EnemyType::ASURA_HEALER : roll < 90 ? EnemyType::ASURA_SHOOTER : EnemyType::ASURA_TANK;
            } else if (act_wave >= 9) {
                type = roll < 22 ? EnemyType::ASURA_SNIPER : roll < 42 ? EnemyType::ASURA_HEALER
                       : roll < 64 ? EnemyType::ASURA_KAMIKAZE : roll < 84 ? EnemyType::ASURA_SHOOTER : EnemyType::ASURA_TANK;
            } else if (act_wave >= 5) {
                type = roll < 25 ? EnemyType::ASURA_HEALER : roll < 55 ? EnemyType::ASURA_KAMIKAZE
                       : roll < 78 ? EnemyType::ASURA_SHOOTER : EnemyType::ASURA_TANK;
            } else if (act_wave >= 3) {
                type = roll < 30 ? EnemyType::ASURA_SHOOTER : roll < 60 ? EnemyType::ASURA_KAMIKAZE : EnemyType::ASURA_TANK;
            } else if (act_wave >= 2) {
                type = roll < 40 ? EnemyType::ASURA_TANK : EnemyType::ASURA_CHASER;
            }
            // else: act_wave 1 stays chasers-only (tutorial)

            const int formation_column = member % 5;
            const int formation_row = member / 5;
            const float formation_x = (formation_column - 2) * 32.0f + (formation_row == 1 ? 16.0f : 0.0f);
            Vector2 pos = { std::clamp(squad_center_x + formation_x, 35.0f, SCREEN_WIDTH - 35.0f),
                            -30.0f - formation_row * 30.0f };
            bool guaranteed_elite = (m_wave_pattern == WavePattern::ELITE_HUNT && spawned % 3 == 0) ||
                                    (act_wave % ELITE_SPAWN_EVERY_N_WAVES == 0 && spawned % 6 == 0);
            float act_elite_bonus = std::min(0.40f, 0.03f * act_pressure);
            if (m_wave_pattern == WavePattern::ELITE_HUNT) act_elite_bonus += 0.20f;
            if (m_wave_pattern == WavePattern::RIFT_AMBUSH) act_elite_bonus += 0.08f;
            float elite_chance = std::min(0.82f, m_difficulty_profile.elite_chance_bonus + 0.04f * (m_player_count - 1) + act_elite_bonus);
            bool chance_elite = (std::rand() % 100) < static_cast<int>(elite_chance * 100.0f);
            // Members of a squadron arrive together; the queue spreads them over only a few frames.
            m_spawn_queue.push({ type, current_delay + member * 0.02f, pos, guaranteed_elite || chance_elite });
            }
            const float formation_delay = m_wave_pattern == WavePattern::INTERCEPTOR_SWARM ? 0.85f :
                                          m_wave_pattern == WavePattern::SIEGE_LINE ? 1.35f :
                                          m_wave_pattern == WavePattern::ELITE_HUNT ? 1.20f : 1.05f;
            current_delay += formation_delay + (std::rand() % 4) * 0.10f;
        }
    }

    void update(float dt, std::vector<Enemy>& enemies, std::vector<Bullet>& bullets, Vector2 player_pos) {
        m_banner_timer = std::max(0.0f, m_banner_timer - dt);

        m_wave_timer += dt;
        if (!m_spawn_queue.empty()) {
            const auto& next_spawn = m_spawn_queue.front();
            if (m_wave_timer >= next_spawn.delay) {
                Enemy enemy;
                const int act = CampaignActForWave(m_current_wave);
                const int act_wave = CampaignWaveWithinAct(m_current_wave);
                const float act_pressure = std::sqrt(static_cast<float>(act - 1));
                float spd_mult = (1.0f + act_wave * 0.02f + std::min(0.8f, act_pressure * 0.06f)) * m_difficulty_profile.bullet_speed_mult;
                float hp_mult = (1.0f + act_wave * 0.05f + act_pressure * 0.24f) * m_difficulty_profile.enemy_hp_mult;

                enemy.init(next_spawn.type, next_spawn.spawn_pos, spd_mult, hp_mult, next_spawn.elite);
                enemies.push_back(enemy);
                m_spawn_queue.pop();
            }
        }

        if (m_boss_active && m_current_boss.active) {
            m_current_boss.update(dt, player_pos, bullets);
        }

        // A boss wave only clears after both its boss and escort fleet are defeated.
        bool any_alive = false;
        for (const auto& e : enemies) {
            if (e.active) { any_alive = true; break; }
        }
        if (m_spawn_queue.empty() && !any_alive && (!m_boss_active || !m_current_boss.active)) {
            m_boss_active = false;
            m_is_wave_in_progress = false;
        }
    }

    bool is_wave_cleared() const {
        return !m_is_wave_in_progress && m_banner_timer <= 0.0f;
    }

    int current_wave() const { return m_current_wave; }
    size_t queued_spawn_count() const { return m_spawn_queue.size(); }
    int wave_enemy_goal() const { return m_wave_enemy_goal; }
    bool is_boss_wave() const { return m_boss_active; }
    Boss& get_boss() { return m_current_boss; }
    const Boss& get_boss() const { return m_current_boss; }
    float banner_timer() const { return m_banner_timer; }
    const CampaignRealm& get_realm_data() const { return GetCampaignRealmForWave(m_current_wave); }
    WavePattern wave_pattern() const { return m_wave_pattern; }

    const char* wave_pattern_name() const {
        switch (m_wave_pattern) {
            case WavePattern::INTERCEPTOR_SWARM: return "INTERCEPTOR SWARM";
            case WavePattern::SIEGE_LINE: return "SIEGE LINE";
            case WavePattern::ELITE_HUNT: return "ELITE HUNT";
            case WavePattern::RIFT_AMBUSH: return "RIFT AMBUSH";
            case WavePattern::BOSS_DUEL: return "BOSS DUEL";
            default: return "SCOUT PATROL";
        }
    }

    std::string get_story_transmission() const {
        const int act = CampaignActForWave(m_current_wave);
        const int act_wave = CampaignWaveWithinAct(m_current_wave);
        if (act_wave == 1 && act > 1) {
            return "ACT " + std::to_string(act) + " // NEW ARMADA: HOSTILE ARMOR AND ATTACK SPEED INCREASED.";
        }
        if (act == 1 && act_wave == 11) {
            return "TRANSMISSION // VIBHISHANA: 'I defect from Lanka's tyranny. Ravana's citadel harnesses void portals. Seek the celestial astras.'";
        } else if (act == 1 && act_wave == 25) {
            return "WARNING // CONQUEROR INDRAJIT HAS ENGAGED. BEWARE ILLUSORY CLONES AND SERPENT ARROWS.";
        } else if (act == 1 && act_wave == 30) {
            return "FINAL APOTHEOSIS // EMPEROR HIRANYAKASHIPU INVOKES HIS IMMORTAL PACT. STRIKE AT THE THRESHOLD TO SUMMON NARASIMHA!";
        }
        if (m_boss_active) {
            return "ACT " + std::to_string(act) + " BOSS FLEET // " + m_current_boss.name + " + " +
                   std::to_string(m_wave_enemy_goal) + " ESCORT SHIPS.";
        }
        return std::string("WAVE FORMATION // ") + wave_pattern_name() + " // PURGE " + std::to_string(m_wave_enemy_goal) + " HOSTILES IN SQUADRONS.";
    }

private:
    int m_current_wave;
    float m_wave_timer;
    float m_banner_timer = 0.0f;
    bool m_is_wave_in_progress;
    bool m_boss_active;
    WavePattern m_wave_pattern = WavePattern::PATROL;
    Boss m_current_boss;
    std::queue<SpawnInstruction> m_spawn_queue;
    DifficultyProfile m_difficulty_profile;
    int m_player_count = 1;
    int m_wave_enemy_goal = 0;
};

} // namespace Vimana
