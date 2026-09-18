#pragma once
#include <vector>
#include <memory>
#include <string>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "entities/ship_archetypes.hpp"
#include "entities/player.hpp"
#include "entities/player_controller.hpp"
#include "entities/enemy.hpp"
#include "entities/boss.hpp"
#include "entities/bullet.hpp"
#include "entities/powerup.hpp"
#include "systems/wave_manager.hpp"
#include "systems/collision_system.hpp"
#include "systems/particle_system.hpp"
#include "systems/sound_system.hpp"
#include "systems/currency_system.hpp"
#include "systems/asset_manager.hpp"
#include "systems/db_system.hpp"
#include "systems/realm_modifier_system.hpp"
#include "systems/co_op_astra_system.hpp"
#include "systems/ai_threat_table.hpp"
#include "systems/network_manager.hpp"
#include "systems/parallax_background.hpp"
#include "systems/achievement_system.hpp"
#include "ui/hud.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class GameView : public IView {
public:
    GameView() 
        : m_next_view(ViewType::GAMEPLAY), 
          m_is_paused(false),
          m_confirm_abort(false),
          m_is_coop_mode(false),
          m_team_combo(1),
          m_team_transcendence_timer(0.0f),
          m_total_team_score(0),
          m_net_snapshot_timer(0.0f),
          m_btn_resume(      { SCREEN_WIDTH / 2.0f - 130, 242, 260, 34 }, "RESUME COMBAT",       COLOR_GOLD_BRIGHT),
          m_btn_restart_wave({ SCREEN_WIDTH / 2.0f - 130, 284, 260, 34 }, "RESTART WAVE",        COLOR_CYAN_BRIGHT),
          m_btn_exit(        { SCREEN_WIDTH / 2.0f - 130, 326, 260, 34 }, "ABORT TO CAMPAIGN",   COLOR_RED_BRIGHT),
          m_btn_quit_title(  { SCREEN_WIDTH / 2.0f - 130, 368, 260, 34 }, "QUIT TO TITLE",       COLOR_ORANGE_BRIGHT),
          m_btn_quit_desktop({ SCREEN_WIDTH / 2.0f - 130, 410, 260, 34 }, "QUIT TO DESKTOP",     COLOR_MUTED),
          m_btn_confirm_abort({ SCREEN_WIDTH / 2.0f - 135, 340, 130, 32 }, "CONFIRM",            COLOR_RED_BRIGHT),
          m_btn_cancel_abort( { SCREEN_WIDTH / 2.0f +   5, 340, 130, 32 }, "CANCEL",             COLOR_CYAN_BRIGHT)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::GAMEPLAY;
        m_is_paused = false;
        m_bullets.clear();
        m_enemies.clear();
        m_powerups.clear();

        m_squad.clear();
        m_squad.resize(1);
        m_squad[0].init(&SHIP_FLEET[0]);
        m_squad[0].player_id = 0;
        m_squad[0].callsign = DBSystem::instance().player_name();

        m_controllers.clear();
        m_controllers.push_back(std::make_unique<HumanController>(0));

        m_is_coop_mode = false;
        m_difficulty = Difficulty::KSHATRIYA;
        m_run_duration = 0.0f;
        m_wave_mgr.start_campaign(1, Difficulty::KSHATRIYA, 1);
        m_wave_start_hp = m_squad[0].hp;
        m_wave_kills = 0;
        m_team_combo = 1;
        m_team_transcendence_timer = 0.0f;
        m_total_team_score = 0;
        m_milestone_text = "";
        m_milestone_timer = 0.0f;
        m_last_milestone = 0;
        m_last_boss_phase = 1;
        m_boss_phase_flash_timer = 0.0f;
        CoOpAstraSystem::instance().reset();
        ParallaxBackground::instance().init();

        SoundSystem::instance().play_music("combat_loop.mp3");
    }

    void start_with_ship(
        const ShipArchetype* ship,
        const ConsumableInventory& pre_inv,
        int starting_wave = 1,
        Difficulty diff = Difficulty::KSHATRIYA,
        int squad_size = 1
    ) {
        m_difficulty = diff;
        if (starting_wave <= 1) {
            m_run_duration = 0.0f;
        }
        m_is_coop_mode = (squad_size > 1 || NetworkManager::instance().role() != NetworkRole::OFFLINE);
        int num_players = m_is_coop_mode ? std::max(squad_size, (int)NetworkManager::instance().players().size()) : 1;
        if (num_players < 1) num_players = 1;

        m_squad.clear();
        m_squad.resize(num_players);
        m_controllers.clear();

        // Slot 0: Primary local player
        m_squad[0].init(ship);
        m_squad[0].inventory = pre_inv;
        m_squad[0].player_id = 0;
        m_squad[0].callsign = DBSystem::instance().player_name();
        m_controllers.push_back(std::make_unique<HumanController>(0));

        // Slots 1..num_players-1: Teammates / Wingmen
        for (int i = 1; i < num_players; ++i) {
            m_squad[i].player_id = static_cast<uint8_t>(i);
            const ShipArchetype* mate_arch = &SHIP_FLEET[i % SHIP_FLEET.size()];
            m_squad[i].init(mate_arch);
            m_squad[i].callsign = "WINGMAN-0" + std::to_string(i + 1);

            if (NetworkManager::instance().role() == NetworkRole::HOST) {
                const auto& peers = NetworkManager::instance().peers();
                bool is_remote = false;
                for (const auto& peer : peers) {
                    if (peer.player_id == i && peer.is_connected && !peer.is_ai_takeover) {
                        is_remote = true;
                        break;
                    }
                }
                if (is_remote) {
                    m_controllers.push_back(std::make_unique<NetworkController>(i));
                } else {
                    m_controllers.push_back(std::make_unique<AIController>(i));
                }
            } else {
                m_controllers.push_back(std::make_unique<AIController>(i));
            }
        }

        m_bullets.clear();
        m_enemies.clear();
        m_powerups.clear();
        m_wave_mgr.start_campaign(starting_wave, diff, num_players);
        ParallaxBackground::instance().set_realm(m_wave_mgr.get_realm_data());

        // Scale boss HP if starting on boss wave
        if (m_wave_mgr.is_boss_wave() && m_wave_mgr.get_boss().active) {
            m_wave_mgr.get_boss().max_hp = static_cast<int>(m_wave_mgr.get_boss().max_hp * (1.0f + 0.50f * (num_players - 1)));
            m_wave_mgr.get_boss().hp = m_wave_mgr.get_boss().max_hp;
        }

        m_wave_start_hp = m_squad[0].hp;
        m_wave_kills = 0;
        m_team_combo = 1;
        m_team_transcendence_timer = 0.0f;
        m_total_team_score = 0;
        m_is_paused = false;
        m_next_view = ViewType::GAMEPLAY;
        m_milestone_text = "";
        m_milestone_timer = 0.0f;
        m_last_milestone = 0;
        m_last_boss_phase = 1;
        m_boss_phase_flash_timer = 0.0f;
        CoOpAstraSystem::instance().reset();
    }

    void apply_boon_and_resume(BoonType boon) {
        m_squad[0].apply_boon(boon);
        m_next_view = ViewType::GAMEPLAY;

        int next_w = m_wave_mgr.current_wave() + 1;
        if (next_w > 30) {
            m_next_view = m_is_coop_mode ? ViewType::MULTIPLAYER_RESULT : ViewType::VICTORY;
        } else {
            m_bullets.clear();
            m_enemies.clear();
            m_wave_mgr.prepare_wave(next_w);

            // Boss scaling for co-op
            if (m_wave_mgr.is_boss_wave() && m_wave_mgr.get_boss().active && m_squad.size() > 1) {
                m_wave_mgr.get_boss().max_hp = static_cast<int>(m_wave_mgr.get_boss().max_hp * (1.0f + 0.50f * (m_squad.size() - 1)));
                m_wave_mgr.get_boss().hp = m_wave_mgr.get_boss().max_hp;
            }

            m_wave_start_hp = m_squad[0].hp;
            m_wave_kills = 0;
            m_last_boss_phase = 1;
            m_boss_phase_flash_timer = 0.0f;
        }
    }

    const WaveResult& latest_wave_result() const { return m_last_wave_result; }
    const std::vector<Player>& squad() const { return m_squad; }
    bool is_coop_mode() const { return m_is_coop_mode; }
    int total_team_score() const { return m_total_team_score; }

    void update(float dt, Vector2 mouse_pos) override {
        m_aim_pos = mouse_pos;
        NetworkManager::instance().update(dt);
        CoOpAstraSystem::instance().update(dt);

        // Pause toggle: ESC, P, or Enter — multiple keys so a flaky focus
        // or non-US keyboard layout doesn't leave the player stuck in combat.
        if (IsKeyPressed(KEY_ESCAPE) || IsKeyPressed(KEY_P) || IsKeyPressed(KEY_ENTER)) {
            m_is_paused = !m_is_paused;
            m_confirm_abort = false; // reset confirm state on any toggle
        }

        if (m_is_paused) {
            if (!m_confirm_abort) {
                // Normal pause menu
                if (m_btn_resume.update(mouse_pos)) {
                    m_is_paused = false;
                    m_confirm_abort = false;
                }
                if (m_btn_restart_wave.update(mouse_pos)) {
                    m_bullets.clear();
                    m_enemies.clear();
                    m_wave_mgr.prepare_wave(m_wave_mgr.current_wave());
                    for (auto& p : m_squad) {
                        p.hp = p.max_hp;
                        p.is_downed = false;
                        p.lives = 3;
                        p.is_spectator = false;
                    }
                    m_wave_start_hp = m_squad[0].hp;
                    m_is_paused = false;
                }
                if (m_btn_exit.update(mouse_pos)) {
                    m_confirm_abort = true; // Show confirmation panel
                }
                if (m_btn_quit_title.update(mouse_pos)) {
                    if (m_is_coop_mode) NetworkManager::instance().leave_session();
                    m_next_view = ViewType::TITLE;
                }
                if (m_btn_quit_desktop.update(mouse_pos)) {
                    if (m_is_coop_mode) NetworkManager::instance().leave_session();
                    CloseWindow(); // Graceful desktop quit
                }
            } else {
                // ARE YOU SURE? confirmation sub-panel
                if (m_btn_confirm_abort.update(mouse_pos)) {
                    if (m_is_coop_mode) NetworkManager::instance().leave_session();
                    m_next_view = ViewType::CAMPAIGN_MAP;
                }
                if (m_btn_cancel_abort.update(mouse_pos)) {
                    m_confirm_abort = false;
                }
            }
            return;
        }

        m_run_duration += dt;

        // ── LIFE TOKENS + SPECTATOR + SELF-REVIVE ───────────────────────────
        int alive_count = 0;
        for (auto& p : m_squad) {
            if (!p.is_spectator && !p.is_downed) alive_count++;
        }

        for (size_t i = 0; i < m_squad.size(); ++i) {
            auto& p = m_squad[i];
            if (p.is_spectator) continue;

            if (p.is_downed) {
                // Spectator camera: WASD free-fly (handled in draw via offset)
                if (i == 0) {
                    float spd = 200.0f * dt;
                    if (IsKeyDown(KEY_W)) p.pos.y -= spd;
                    if (IsKeyDown(KEY_S)) p.pos.y += spd;
                    if (IsKeyDown(KEY_A)) p.pos.x -= spd;
                    if (IsKeyDown(KEY_D)) p.pos.x += spd;
                    p.pos.x = std::clamp(p.pos.x, 0.0f, (float)SCREEN_WIDTH);
                    p.pos.y = std::clamp(p.pos.y, 0.0f, (float)SCREEN_HEIGHT);
                }

                // Self-revive (solo only): hold R for 30s
                if (i == 0 && IsKeyDown(KEY_R)) {
                    p.self_revive_timer += dt;
                    if (p.self_revive_timer >= 30.0f) {
                        p.is_downed = false;
                        p.hp = static_cast<int>(p.max_hp * 0.30f);
                        p.invincibility_timer = 2.0f;
                        p.self_revive_timer = 0.0f;
                        SoundSystem::instance().play_revive_complete();
                        m_particles.add_floating_text(p.pos, "SELF-REVIVED!", COLOR_GREEN_BRIGHT);
                    }
                } else {
                    p.self_revive_timer = 0.0f;
                }

                // Last-standing auto-revive: 1 live player, auto-revive in 20s
                if (alive_count == 1 && m_squad.size() > 1) {
                    p.downed_timer += dt;
                    if (p.downed_timer >= 20.0f) {
                        p.is_downed = false;
                        p.hp = static_cast<int>(p.max_hp * 0.30f);
                        p.invincibility_timer = 2.0f;
                        p.downed_timer = 0.0f;
                        SoundSystem::instance().play_revive_complete();
                        m_particles.add_floating_text(p.pos, "EMERGENCY REVIVE!", COLOR_CYAN_BRIGHT);
                    }
                }

                // Bleed-out: downed_timer expires → lose a life
                p.downed_timer += dt;
                if (p.downed_timer >= 15.0f) {
                    p.downed_timer = 0.0f;
                    p.lives--;
                    if (p.lives > 0) {
                        // Respawn at 25% HP with 2s invincibility
                        p.is_downed = false;
                        p.hp = static_cast<int>(p.max_hp * 0.25f);
                        p.invincibility_timer = 2.0f;
                        p.pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT * 0.78f };
                        SoundSystem::instance().play_sfx("powerup.wav", 0.8f);
                        m_particles.add_floating_text(p.pos,
                            "LIFE LOST — " + std::to_string(p.lives) + " REMAINING", COLOR_RED_BRIGHT);
                    } else {
                        // No lives left → become spectator
                        p.is_spectator = true;
                        SoundSystem::instance().play_downed_alert();
                        m_particles.add_floating_text(p.pos, "ELIMINATED // SPECTATING", COLOR_MUTED);
                    }
                }
            }
        }

        // Squad wipe check: all players are spectators → game over
        bool any_alive = false;
        for (auto& p : m_squad) { if (!p.is_spectator) { any_alive = true; break; } }
        if (!any_alive) {
            m_next_view = ViewType::GAME_OVER;
            return;
        }


        // Team Transcendence countdown
        if (m_team_transcendence_timer > 0) m_team_transcendence_timer -= dt;
        if (m_boss_phase_flash_timer > 0.0f) m_boss_phase_flash_timer -= dt;

        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;

        // Update Parallax Background responding to flagship movement
        ParallaxBackground::instance().update(dt, m_squad.empty() ? Vector2{ 0, 0 } : m_squad[0].vel);

        // Dynamic Boss Music Escalation
        if (boss_ptr && boss_ptr->active) {
            SoundSystem::instance().set_boss_phase(boss_ptr->phase);
        }

        // Emit Dash Ghost silhouettes
        for (const auto& p : m_squad) {
            if (p.is_dashing) {
                m_particles.emit_dash_ghost(p.pos, p.archetype ? p.archetype->sprite_file : "pushpaka.png", p.angle + 90.0f, p.archetype ? p.archetype->accent_color : COLOR_CYAN_BRIGHT);
            }
        }

        // -- 1. Brahmastra / Co-op Dual Astra (F Key) ----------------------------
        if (IsKeyPressed(KEY_F) && m_squad[0].brahmastra_bombs > 0) {
            m_squad[0].brahmastra_bombs--;
            AchievementSystem::instance().check_and_award("BRAHMASTRA");

            bool synced = CoOpAstraSystem::instance().register_astra_invocation(
                0, m_squad, m_bullets, m_enemies, boss_ptr, m_particles
            );

            if (synced) {
                AchievementSystem::instance().check_and_award("COOP_DUAL_ASTRA");
            } else {
                // Solo detonation
                SoundSystem::instance().play_sfx("explosion.wav", 1.0f);
                if (g_screen_shake_enabled) m_particles.trigger_screen_shake(18.0f, 0.7f);

                for (auto& b : m_bullets) {
                    if (b.is_enemy) b.active = false;
                }
                for (auto& e : m_enemies) {
                    if (e.active) {
                        e.hp -= 280;
                        m_particles.emit_explosion(e.pos, COLOR_GOLD_BRIGHT, 15, 180.0f);
                    }
                }
                if (boss_ptr && boss_ptr->active) {
                    boss_ptr->take_damage(400);
                }
                m_particles.add_floating_text({ SCREEN_WIDTH / 2.0f - 110.0f, SCREEN_HEIGHT / 2.0f }, "BRAHMASTRA DETONATION!", COLOR_GOLD_BRIGHT);
            }
        }

        // -- 2. Parallax Stars ---------------------------------------------------
        for (auto& s : m_stars) {
            s.y += s.z * 30.0f * dt;
            if (s.y > SCREEN_HEIGHT) {
                s.y = 0;
                s.x = static_cast<float>(std::rand() % SCREEN_WIDTH);
            }
        }

        // -- 3. Squad Controllers & Physics --------------------------------------
        // Apply Realm Modifiers to speed
        const auto& realm = GetCampaignRealmForWave(m_wave_mgr.current_wave());
        float realm_spd_mult = RealmModifierSystem::player_speed_mult(m_wave_mgr.current_wave());

        for (size_t i = 0; i < m_squad.size(); ++i) {
            auto& p = m_squad[i];
            p.current_speed = p.base_speed * realm_spd_mult;
            if (m_team_transcendence_timer > 0) p.current_speed *= 1.10f; // Team Transcendence buff

            if (i < m_controllers.size()) {
                m_controllers[i]->update(dt, p, m_bullets, mouse_pos, m_squad, m_enemies, boss_ptr);
            }
            p.update(dt);

            // Thruster trail for active ships
            if (!p.is_downed) {
                float rad = (p.angle + 180.0f) * (3.14159f / 180.0f);
                Vector2 eng_pos = { p.pos.x + std::cos(rad) * p.radius, p.pos.y + std::sin(rad) * p.radius };
                Color th_col = p.archetype ? p.archetype->accent_color : COLOR_CYAN_BRIGHT;
                m_particles.emit_thrust(eng_pos, { std::cos(rad), std::sin(rad) }, th_col);
            }
        }

        // -- 4. Downed & Revive Status Transition --------------------------------
        for (auto& p : m_squad) {
            if (!p.is_spectator && !p.is_downed && p.hp <= 0) {
                p.is_downed = true;
                p.downed_timer = 0.0f;
                p.self_revive_timer = 0.0f;
                p.downed_count++;
                p.hp = 0;
                m_particles.add_floating_text(p.pos, "PILOT DOWNED // HOLD R TO REVIVE!", COLOR_RED_BRIGHT);
                SoundSystem::instance().play_downed_alert();
            }
        }

        // -- 5. Near-Miss Graze Detection (P0) -----------------------------------
        for (auto& b : m_bullets) {
            if (b.active && b.is_enemy && !b.grazed) {
                float dist = Vector2Distance(b.pos, m_squad[0].pos);
                if (dist < m_squad[0].radius + PLAYER_GRAZE_RADIUS && dist > m_squad[0].radius + 2.0f) {
                    b.grazed = true;
                    m_squad[0].score += SCORE_NEAR_MISS;
                    m_particles.add_floating_text({ m_squad[0].pos.x - 30.0f, m_squad[0].pos.y - 20.0f }, "NEAR MISS +25", COLOR_CYAN_BRIGHT);
                    if (g_screen_shake_enabled) m_particles.trigger_screen_shake(2.0f, 0.08f);
                    SoundSystem::instance().play_sfx("ui_click.wav", 0.4f);
                }
            }
        }

        // -- 6. Team Combo & Transcendence ---------------------------------------
        int max_squad_combo = 1;
        for (const auto& p : m_squad) {
            max_squad_combo = std::max(max_squad_combo, p.combo);
        }
        m_team_combo = max_squad_combo;

        if (m_team_combo >= 50 && m_last_milestone < 50) {
            m_last_milestone = 50;
            m_milestone_text = "x50 MAHAYUDDHA SUPREME TRANSCENDENCE";
            m_milestone_timer = 2.4f;
            m_team_transcendence_timer = 8.0f;
            SoundSystem::instance().play_transcendence();
            AchievementSystem::instance().check_and_award("COMBO_50");
        } else if (m_team_combo >= 25 && m_last_milestone < 25) {
            m_last_milestone = 25;
            m_milestone_text = "x25 SANGHA TRANSCENDENCE  //  +20% DMG";
            m_milestone_timer = 2.0f;
            m_team_transcendence_timer = 8.0f;
            SoundSystem::instance().play_ui_confirm();
            AchievementSystem::instance().check_and_award("COMBO_25");
        } else if (m_team_combo >= 10 && m_last_milestone < 10) {
            m_last_milestone = 10;
            m_milestone_text = "x10 SQUAD RHYTHM!";
            m_milestone_timer = 1.6f;
            SoundSystem::instance().play_ui_confirm();
        } else if (m_team_combo >= 5 && m_last_milestone < 5) {
            m_last_milestone = 5;
            m_milestone_text = "x5 COMBAT RHYTHM";
            m_milestone_timer = 1.2f;
            SoundSystem::instance().play_telemetry_chime();
        }

        if (m_milestone_timer > 0) m_milestone_timer -= dt;
        if (m_team_combo <= 1) m_last_milestone = 0;

        // -- 7. Bullets Update ---------------------------------------------------
        for (auto& b : m_bullets) {
            b.update(dt);
        }

        // -- 8. Wave Manager & Threat-targeted Enemies ---------------------------
        m_wave_mgr.update(dt, m_enemies, m_bullets, m_squad[0].pos);

        for (auto& e : m_enemies) {
            Vector2 target_pos = AIThreatTable::get_highest_threat_target(e.pos, m_squad);
            e.update(dt, target_pos, m_bullets, m_enemies);
        }

        if (boss_ptr && boss_ptr->active) {
            Vector2 target_pos = AIThreatTable::get_highest_threat_target(boss_ptr->pos, m_squad);
            boss_ptr->update(dt, target_pos, m_bullets);
            if (boss_ptr->phase != m_last_boss_phase) {
                m_last_boss_phase = boss_ptr->phase;
                m_boss_phase_flash_timer = 1.4f;
                m_particles.emit_boss_phase_transition(boss_ptr->pos, boss_ptr->theme_color, boss_ptr->phase);
                SoundSystem::instance().set_boss_phase(boss_ptr->phase);
            }
        } else {
            m_last_boss_phase = 1;
        }

        // -- 9. Powerups & Magnetism ---------------------------------------------
        float magnet_radius = m_squad[0].has_boon(BoonType::GARUDA_CELESTIAL_MAGNET) ? 350.0f : 120.0f;
        for (auto& p : m_powerups) {
            p.update(dt, m_squad[0].pos, magnet_radius);
        }

        // -- 10. Combat Collisions with Squad Attribution ------------------------
        int prana_earned = 0;
        int pre_kills = m_squad[0].kills;
        m_collisions.resolve_combat(m_squad, m_enemies, boss_ptr, m_bullets, m_powerups, m_particles, prana_earned);

        if (prana_earned > 0) {
            CurrencySystem::instance().add_prana_shards(prana_earned);
        }
        m_wave_kills += (m_squad[0].kills - pre_kills);
        if (m_squad[0].kills > 0) {
            AchievementSystem::instance().check_and_award("FIRST_BLOOD");
        }

        // Sum squad scores
        m_total_team_score = 0;
        for (const auto& p : m_squad) m_total_team_score += p.score;

        // -- 11. Particles -------------------------------------------------------
        m_particles.update(dt);

        // -- 12. Check Wave Cleared ----------------------------------------------
        if (m_wave_mgr.is_wave_cleared()) {
            int dmg_taken = std::max(0, m_wave_start_hp - m_squad[0].hp);
            bool no_dmg = (dmg_taken == 0);
            bool perfect = (no_dmg && m_squad[0].max_combo >= 10);

            // Award Wave Achievements
            if (no_dmg) AchievementSystem::instance().check_and_award("PERFECT_WAVE");
            if (m_wave_mgr.current_wave() >= 5)  AchievementSystem::instance().check_and_award("WAVE_5");
            if (m_wave_mgr.current_wave() >= 15) AchievementSystem::instance().check_and_award("WAVE_15");
            if (m_wave_mgr.current_wave() >= 30) AchievementSystem::instance().check_and_award("WAVE_30");
            if (m_wave_mgr.is_boss_wave()) {
                if (m_wave_mgr.current_wave() <= 6)  AchievementSystem::instance().check_and_award("BOSS_1");
                if (m_wave_mgr.current_wave() >= 25) AchievementSystem::instance().check_and_award("BOSS_5");
            }

            PerformanceRank rank = PerformanceRank::B_RANK;
            if (no_dmg || m_squad[0].max_combo >= 15) {
                rank = PerformanceRank::S_RANK;
            } else if (dmg_taken <= 25 || m_squad[0].max_combo >= 8) {
                rank = PerformanceRank::A_RANK;
            } else if (dmg_taken > 60) {
                rank = PerformanceRank::C_RANK;
            }

            int wave_score = 500 + m_squad[0].max_combo * 35;
            int wave_prana = PRANA_REWARD_WAVE_CLEAR + (no_dmg ? BONUS_NO_DEATH : 0);

            CurrencySystem::instance().add_prana_shards(wave_prana);
            DBSystem::instance().update_max_wave(m_wave_mgr.current_wave());

            // Projectile-based Dynamic Accuracy calculation
            int acc = (m_squad[0].shots_fired > 0) ? static_cast<int>((m_squad[0].shots_hit * 100) / m_squad[0].shots_fired) : 100;
            acc = std::clamp(acc, 0, 100);

            m_last_wave_result = {
                m_wave_mgr.current_wave(),
                m_wave_kills,
                dmg_taken,
                m_squad[0].max_combo,
                acc,
                wave_score,
                wave_prana,
                no_dmg,
                perfect,
                rank
            };

            m_next_view = ViewType::WAVE_CLEAR;
        }
    }

    void draw() override {
        const auto& realm = GetRealmForWave(m_wave_mgr.current_wave());

        // 5-Layer Layered Parallax Background
        ParallaxBackground::instance().draw();

        // Screen Shake offset (respects accessibility setting)
        Vector2 shake = g_screen_shake_enabled ? m_particles.get_shake_offset() : Vector2{ 0.0f, 0.0f };
        BeginMode2D({ { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT / 2.0f }, { SCREEN_WIDTH / 2.0f + shake.x, SCREEN_HEIGHT / 2.0f + shake.y }, 0.0f, 1.0f });

        // Draw Powerups
        for (const auto& p : m_powerups) p.draw();

        // Draw Bullets
        for (const auto& b : m_bullets) b.draw();

        // Draw Enemies
        for (const auto& e : m_enemies) {
            Texture2D tex = AssetManager::instance().get_texture(e.sprite_key);
            e.draw(tex);
        }

        // Draw Boss
        if (m_wave_mgr.is_boss_wave() && m_wave_mgr.get_boss().active) {
            Texture2D b_tex = AssetManager::instance().get_texture(m_wave_mgr.get_boss().sprite_key);
            m_wave_mgr.get_boss().draw(b_tex);
        }

        // Draw All Squad Players
        for (const auto& p : m_squad) {
            std::string p_sprite = p.archetype ? p.archetype->sprite_file : "pushpaka.png";
            Texture2D p_tex = AssetManager::instance().get_texture(p_sprite);
            p.draw(p_tex);
        }

        // Lightweight aim tracer: communicates the current firing direction
        // without adding a permanent reticle over the cockpit HUD.
        if (!m_squad.empty() && !m_squad[0].is_downed && !m_squad[0].is_spectator) {
            Vector2 aim = Vector2Subtract(m_aim_pos, m_squad[0].pos);
            if (Vector2Length(aim) > 1.0f) {
                aim = Vector2Normalize(aim);
                Vector2 start = Vector2Add(m_squad[0].pos, Vector2Scale(aim, m_squad[0].radius * 0.8f));
                Vector2 end = Vector2Add(start, Vector2Scale(aim, 34.0f));
                DrawLineEx(start, end, 2.0f, ColorAlpha(m_squad[0].archetype ? m_squad[0].archetype->accent_color : COLOR_CYAN_BRIGHT, 0.65f));
                DrawCircleV(end, 2.5f, COLOR_PARCHMENT);
            }
        }

        // Draw Particles
        m_particles.draw();

        EndMode2D();

        Font title_f = AssetManager::instance().title_font();
        Font body_f = AssetManager::instance().body_font();

        // Cockpit HUD (Squadron status, boss bar, combo meter, instruments, radar)
        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;
        UI::HUD::draw(m_squad, m_wave_mgr.current_wave(), realm, boss_ptr, m_enemies, m_team_combo, m_team_transcendence_timer, title_f, body_f);

        // Persistent [ESC] PAUSE reminder — always visible during active gameplay
        // so pilots know how to suspend the run.
        Rectangle esc_hint = { SCREEN_WIDTH - 130.0f, 8.0f, 122.0f, 18.0f };
        DrawRectangleRec(esc_hint, ColorAlpha(COLOR_SURFACE_HIGH, 0.55f));
        DrawRectangleLinesEx(esc_hint, 1.0f, ColorAlpha(COLOR_GOLD, 0.5f));
        DrawText("[ESC] PAUSE", static_cast<int>(esc_hint.x + 12), static_cast<int>(esc_hint.y + 3), 11, COLOR_GOLD_BRIGHT);

        // Pulsing PAUSED banner at top-center — guaranteed visibility even if
        // the pause panel below somehow fails to render.
        if (m_is_paused) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 4.0f);
            Rectangle banner = { SCREEN_WIDTH / 2.0f - 90.0f, 14.0f, 180.0f, 28.0f };
            DrawRectangleRec(banner, ColorAlpha(COLOR_RED_BRIGHT, 0.25f + 0.20f * pulse));
            DrawRectangleLinesEx(banner, 2.0f, COLOR_RED_BRIGHT);
            const char* txt = "|| PAUSED ||";
            Vector2 sz = MeasureTextEx(title_f, txt, 16, 1.0f);
            DrawTextEx(title_f, txt, { SCREEN_WIDTH / 2.0f - sz.x / 2.0f, banner.y + 5 }, 16, 1.0f, COLOR_GOLD_BRIGHT);
        }

        // -- Boss Attack Telegraph Warning Banner -------------------------------
        if (boss_ptr && boss_ptr->active && boss_ptr->is_telegraphing) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 18.0f);
            Rectangle warn_bar = { SCREEN_WIDTH / 2.0f - 240, 110, 480, 36 };
            UI::DrawChamferedPanel(warn_bar, COLOR_RED_BRIGHT, ColorAlpha(COLOR_RED_BRIGHT, 0.25f + 0.3f * pulse), 4.0f);
            std::string warn_msg = "[!] WARNING: TITAN CHARGING [" + boss_ptr->telegraph_warning + "] [!]";
            Vector2 w_sz = MeasureTextEx(title_f, warn_msg.c_str(), 13, 1.0f);
            DrawTextEx(title_f, warn_msg.c_str(), { (SCREEN_WIDTH - w_sz.x) / 2.0f, warn_bar.y + 10 }, 13, 1.0f, WHITE);
        }

        if (boss_ptr && boss_ptr->active && m_boss_phase_flash_timer > 0.0f) {
            float pulse = 0.65f + 0.35f * std::sin(GetTime() * 14.0f);
            float alpha = std::clamp(m_boss_phase_flash_timer / 0.45f, 0.0f, 1.0f);
            Rectangle phase_box = { SCREEN_WIDTH / 2.0f - 210, 148, 420, 34 };
            UI::DrawYantraPanel(phase_box, boss_ptr->theme_color, ColorAlpha(boss_ptr->theme_color, 0.18f + 0.20f * pulse), 4.0f, true);
            std::string phase_msg = "BOSS PHASE " + std::to_string(boss_ptr->phase) + " // THREAT ESCALATED";
            Vector2 phase_sz = MeasureTextEx(title_f, phase_msg.c_str(), 13, 1.0f);
            DrawTextEx(title_f, phase_msg.c_str(), { (SCREEN_WIDTH - phase_sz.x) / 2.0f, phase_box.y + 10 }, 13, 1.0f, ColorAlpha(COLOR_GOLD_BRIGHT, alpha));
        }

        // -- Combo Milestone Banner ----------------------------------------------
        if (m_milestone_timer > 0) {
            float m_alpha = std::min(1.0f, m_milestone_timer / 0.4f);
            Vector2 m_sz = MeasureTextEx(title_f, m_milestone_text.c_str(), 18, 1.0f);
            Rectangle m_box = { (SCREEN_WIDTH - m_sz.x) / 2.0f - 20, 155, m_sz.x + 40, 38 };
            UI::DrawYantraPanel(m_box, COLOR_GOLD_BRIGHT, ColorAlpha(COLOR_SURFACE_HIGH, 0.9f * m_alpha), 5.0f, true);
            DrawTextEx(title_f, m_milestone_text.c_str(), { (SCREEN_WIDTH - m_sz.x) / 2.0f, m_box.y + 9 }, 18, 1.0f, ColorAlpha(COLOR_GOLD_BRIGHT, m_alpha));
        }

        // -- Team Transcendence Banner -------------------------------------------
        if (m_team_transcendence_timer > 0) {
            float t_pulse = 0.5f + 0.5f * std::sin(GetTime() * 12.0f);
            DrawText("TEAM TRANSCENDENCE ACTIVE: +20% DMG, +10% SPD", SCREEN_WIDTH / 2 - 180, 52, 12, ColorAlpha(COLOR_GOLD_BRIGHT, 0.7f + 0.3f * t_pulse));
        }

        // -- Low-HP Vignette & Critical Warning ----------------------------------
        if (m_squad[0].hp <= 35 && !m_squad[0].is_downed) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
            DrawRectangleLinesEx({ 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT }, 10.0f, ColorAlpha(COLOR_RED_BRIGHT, 0.2f + 0.4f * pulse));
            DrawText("[!] HULL INTEGRITY CRITICAL // USE SOMA [C] [!]", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT - 45, 12, ColorAlpha(COLOR_RED_BRIGHT, 0.8f + 0.2f * pulse));
        }

        // Story Transmission
        if (m_wave_mgr.banner_timer() > 0) {
            std::string story = m_wave_mgr.get_story_transmission();
            if (!story.empty()) {
                UI::DrawChamferedPanel({ 100, 150, 700, 46 }, COLOR_CYAN_BRIGHT, { 5, 15, 30, 240 }, 6.0f);
                DrawText(story.c_str(), 120, 166, 12, COLOR_CYAN_BRIGHT);
            }
        }

        // -- Pause Menu with Controls Cheatsheet & Quit Confirmation ------------
        if (m_is_paused) {
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 0, 0, 0, 205 });

            if (!m_confirm_abort) {
                Rectangle pause_box = { SCREEN_WIDTH / 2.0f - 230, 95, 460, 365 };
                UI::DrawChamferedPanel(pause_box, COLOR_GOLD, COLOR_SURFACE_HIGH, 8.0f);

                DrawTextEx(title_f, "COMBAT SUSPENDED // PAUSE", { SCREEN_WIDTH / 2.0f - 130, pause_box.y + 16 }, 18, 1.0f, COLOR_GOLD_BRIGHT);

                Rectangle info_rec = { pause_box.x + 20, pause_box.y + 44, pause_box.width - 40, 68 };
                UI::DrawChamferedPanel(info_rec, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
                DrawTextEx(body_f, "PILOT FLIGHT CONTROLS:", { info_rec.x + 10, info_rec.y + 6 }, 10, 1.0f, COLOR_MUTED);
                DrawTextEx(body_f, "[WASD] Movement  -  [L-Click] Fire  -  [SPACE] Warp Dash", { info_rec.x + 10, info_rec.y + 22 }, 11, 1.0f, COLOR_GOLD_BRIGHT);
                DrawTextEx(body_f, "[Q/E] Chakram  -  [F] Brahmastra  -  [C] Soma  -  [V] Vajra", { info_rec.x + 10, info_rec.y + 38 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

                if (m_is_coop_mode) {
                    std::string ping_str = "LAN CO-OP ONLINE // PING: " + std::to_string(NetworkManager::instance().ping_ms()) + "ms";
                    DrawText(ping_str.c_str(), static_cast<int>(pause_box.x + 25), static_cast<int>(pause_box.y + 118), 10, COLOR_GREEN_BRIGHT);
                }

                m_btn_resume.draw(title_f);
                m_btn_restart_wave.draw(title_f);
                m_btn_exit.draw(title_f);
                m_btn_quit_title.draw(title_f);
                m_btn_quit_desktop.draw(title_f);
            } else {
                // Inline Confirmation Panel
                Rectangle conf_box = { SCREEN_WIDTH / 2.0f - 190, 180, 380, 200 };
                UI::DrawYantraPanel(conf_box, COLOR_RED_BRIGHT, COLOR_SURFACE_HIGH, 8.0f, true);

                DrawTextEx(title_f, "ABORT MISSION?", { SCREEN_WIDTH / 2.0f - 85, conf_box.y + 25 }, 18, 1.0f, COLOR_RED_BRIGHT);
                DrawText("Are you sure you want to abandon this sortie?", static_cast<int>(SCREEN_WIDTH / 2.0f - 140), static_cast<int>(conf_box.y + 65), 12, COLOR_PARCHMENT);
                DrawText("Unsaved wave progression will be forfeited.", static_cast<int>(SCREEN_WIDTH / 2.0f - 130), static_cast<int>(conf_box.y + 90), 11, COLOR_MUTED);

                m_btn_confirm_abort.draw(title_f);
                m_btn_cancel_abort.draw(title_f);
            }
        }

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::GAMEPLAY; }
    const Player& player() const { return m_squad[0]; }
    Player& player() { return m_squad[0]; }
    int current_wave() const { return m_wave_mgr.current_wave(); }
    float run_duration() const { return m_run_duration; }
    Difficulty difficulty() const { return m_difficulty; }
    std::string difficulty_string() const {
        switch (m_difficulty) {
            case Difficulty::NOVICE: return "easy";
            case Difficulty::KSHATRIYA: return "normal";
            case Difficulty::ASURA_SLAYER: return "hard";
            case Difficulty::CHAKRAVYUHA: return "endless";
            default: return "normal";
        }
    }

private:
    struct Star { float x, y, z; };
    ViewType m_next_view;
    bool m_is_paused;
    bool m_confirm_abort;
    bool m_is_coop_mode;
    Difficulty m_difficulty = Difficulty::KSHATRIYA;
    float m_run_duration = 0.0f;
    int m_team_combo;
    float m_team_transcendence_timer;
    int m_total_team_score;
    float m_net_snapshot_timer;
    std::vector<Star> m_stars;

    std::vector<Player> m_squad;
    std::vector<std::unique_ptr<IPlayerController>> m_controllers;
    std::vector<Bullet> m_bullets;
    std::vector<Enemy> m_enemies;
    std::vector<Powerup> m_powerups;

    WaveManager m_wave_mgr;
    CollisionSystem m_collisions;
    ParticleSystem m_particles;

    int m_wave_start_hp = 100;
    int m_wave_kills = 0;
    WaveResult m_last_wave_result;

    std::string m_milestone_text;
    float m_milestone_timer = 0.0f;
    int m_last_milestone = 0;
    int m_last_boss_phase = 1;
    float m_boss_phase_flash_timer = 0.0f;
    Vector2 m_aim_pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT / 2.0f };

    UI::Button m_btn_resume;
    UI::Button m_btn_restart_wave;
    UI::Button m_btn_exit;
    UI::Button m_btn_quit_title;
    UI::Button m_btn_quit_desktop;
    UI::Button m_btn_confirm_abort;
    UI::Button m_btn_cancel_abort;
};

} // namespace Vimana

