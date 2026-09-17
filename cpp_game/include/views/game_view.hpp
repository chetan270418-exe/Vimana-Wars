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
#include "ui/hud.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class GameView : public IView {
public:
    GameView() 
        : m_next_view(ViewType::GAMEPLAY), 
          m_is_paused(false),
          m_is_coop_mode(false),
          m_team_combo(1),
          m_team_transcendence_timer(0.0f),
          m_total_team_score(0),
          m_net_snapshot_timer(0.0f),
          m_btn_resume({ SCREEN_WIDTH / 2.0f - 130, 250, 260, 36 }, "RESUME COMBAT", COLOR_GOLD_BRIGHT),
          m_btn_restart_wave({ SCREEN_WIDTH / 2.0f - 130, 300, 260, 36 }, "RESTART WAVE", COLOR_CYAN_BRIGHT),
          m_btn_exit({ SCREEN_WIDTH / 2.0f - 130, 350, 260, 36 }, "ABORT TO CAMPAIGN", COLOR_RED_BRIGHT)
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
        m_wave_mgr.start_campaign(1, Difficulty::KSHATRIYA, 1);
        m_wave_start_hp = m_squad[0].hp;
        m_wave_kills = 0;
        m_team_combo = 1;
        m_team_transcendence_timer = 0.0f;
        m_total_team_score = 0;
        m_milestone_text = "";
        m_milestone_timer = 0.0f;
        m_last_milestone = 0;
        CoOpAstraSystem::instance().reset();

        // Ambient stars
        m_stars.clear();
        for (int i = 0; i < 120; ++i) {
            m_stars.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                0.5f + (std::rand() % 20) / 10.0f
            });
        }

        SoundSystem::instance().play_music("combat_loop.mp3");
    }

    void start_with_ship(
        const ShipArchetype* ship,
        const ConsumableInventory& pre_inv,
        int starting_wave = 1,
        Difficulty diff = Difficulty::KSHATRIYA,
        int squad_size = 1
    ) {
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
        }
    }

    const WaveResult& latest_wave_result() const { return m_last_wave_result; }
    const std::vector<Player>& squad() const { return m_squad; }
    bool is_coop_mode() const { return m_is_coop_mode; }
    int total_team_score() const { return m_total_team_score; }

    void update(float dt, Vector2 mouse_pos) override {
        NetworkManager::instance().update(dt);
        CoOpAstraSystem::instance().update(dt);

        if (IsKeyPressed(KEY_ESCAPE)) {
            m_is_paused = !m_is_paused;
        }

        if (m_is_paused) {
            if (m_btn_resume.update(mouse_pos)) m_is_paused = false;
            if (m_btn_restart_wave.update(mouse_pos)) {
                m_bullets.clear();
                m_enemies.clear();
                m_wave_mgr.prepare_wave(m_wave_mgr.current_wave());
                for (auto& p : m_squad) {
                    p.hp = p.max_hp;
                    p.is_downed = false;
                }
                m_wave_start_hp = m_squad[0].hp;
                m_is_paused = false;
            }
            if (m_btn_exit.update(mouse_pos)) {
                if (m_is_coop_mode) NetworkManager::instance().leave_session();
                m_next_view = ViewType::CAMPAIGN_MAP;
            }
            return;
        }

        // Team Transcendence countdown
        if (m_team_transcendence_timer > 0) m_team_transcendence_timer -= dt;

        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;

        // -- 1. Brahmastra / Co-op Dual Astra (F Key) ----------------------------
        if (IsKeyPressed(KEY_F) && m_squad[0].brahmastra_bombs > 0) {
            m_squad[0].brahmastra_bombs--;
            bool synced = CoOpAstraSystem::instance().register_astra_invocation(
                0, m_squad, m_bullets, m_enemies, boss_ptr, m_particles
            );

            if (!synced) {
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

        // -- 4. Downed & Revive Status Handling ----------------------------------
        int alive_count = 0;
        for (auto& p : m_squad) {
            if (p.is_downed) {
                p.downed_timer -= dt;
                if (p.downed_timer <= 0) {
                    p.hp = 0; // Hull permanent failure for this wave
                }
            } else if (p.hp <= 0) {
                if (m_is_coop_mode && m_squad.size() > 1) {
                    p.is_downed = true;
                    p.downed_timer = DOWNED_TIMER;
                    p.downed_count++;
                    p.hp = 0;
                    m_particles.add_floating_text(p.pos, "? SQUAD PILOT DOWNED!", COLOR_RED_BRIGHT);
                    SoundSystem::instance().play_sfx("hit.wav", 1.0f);
                } else {
                    // Single player fatal
                    SoundSystem::instance().play_sfx("game_over.wav");
                    m_next_view = ViewType::GAME_OVER;
                    return;
                }
            } else {
                alive_count++;
            }
        }

        // Squadron wipe check
        if (alive_count == 0) {
            SoundSystem::instance().play_sfx("game_over.wav");
            m_next_view = m_is_coop_mode ? ViewType::MULTIPLAYER_RESULT : ViewType::GAME_OVER;
            return;
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
            m_milestone_text = "? x50 MAHAYUDDHA SUPREME TRANSCENDENCE! ?";
            m_milestone_timer = 2.4f;
            m_team_transcendence_timer = 8.0f;
            SoundSystem::instance().play_sfx("wave_clear.wav");
        } else if (m_team_combo >= 25 && m_last_milestone < 25) {
            m_last_milestone = 25;
            m_milestone_text = "? x25 SANGHA TRANSCENDENCE (+20% DMG)! ?";
            m_milestone_timer = 2.0f;
            m_team_transcendence_timer = 8.0f;
            SoundSystem::instance().play_sfx("ui_click.wav");
        } else if (m_team_combo >= 10 && m_last_milestone < 10) {
            m_last_milestone = 10;
            m_milestone_text = "x10 SQUAD RHYTHM!";
            m_milestone_timer = 1.6f;
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
        ClearBackground(COLOR_OBSIDIAN);

        // Parallax stars
        for (const auto& s : m_stars) {
            DrawCircle(static_cast<int>(s.x), static_cast<int>(s.y), s.z, realm.accent_color);
        }

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

        // Draw Particles
        m_particles.draw();

        EndMode2D();

        Font font = AssetManager::instance().font();

        // Cockpit HUD
        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;
        UI::HUD::draw(m_squad[0], m_wave_mgr.current_wave(), realm, boss_ptr, m_enemies, font);

        // -- Co-op Squadron Wingman Status Widget (Top Right) --------------------
        if (m_is_coop_mode && m_squad.size() > 1) {
            float sx = SCREEN_WIDTH - 230.0f;
            float sy = 70.0f;
            for (size_t i = 1; i < m_squad.size(); ++i) {
                const auto& mate = m_squad[i];
                Rectangle mate_bar = { sx, sy, 210, 26 };
                UI::DrawChamferedPanel(mate_bar, mate.is_downed ? COLOR_RED_BRIGHT : COLOR_SURFACE_HIGH, COLOR_SURFACE_LOW, 3.0f);

                DrawText(mate.callsign.c_str(), static_cast<int>(sx + 6), static_cast<int>(sy + 4), 10, COLOR_PARCHMENT);
                if (mate.is_downed) {
                    DrawText("? DOWNED", static_cast<int>(sx + 130), static_cast<int>(sy + 4), 10, COLOR_RED_BRIGHT);
                } else {
                    float hp_pct = std::clamp((float)mate.hp / mate.max_hp, 0.0f, 1.0f);
                    Rectangle hp_f = { sx + 100, sy + 6, 95 * hp_pct, 12 };
                    DrawRectangleRec(hp_f, COLOR_GREEN_BRIGHT);
                    DrawRectangleLinesEx({ sx + 100, sy + 6, 95, 12 }, 1.0f, COLOR_SURFACE_HIGH);
                }
                sy += 30.0f;
            }
        }

        // -- Boss Attack Telegraph Warning Banner -------------------------------
        if (boss_ptr && boss_ptr->active && boss_ptr->is_telegraphing) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 18.0f);
            Rectangle warn_bar = { SCREEN_WIDTH / 2.0f - 240, 110, 480, 36 };
            UI::DrawChamferedPanel(warn_bar, COLOR_RED_BRIGHT, ColorAlpha(COLOR_RED_BRIGHT, 0.25f + 0.3f * pulse), 4.0f);
            std::string warn_msg = "? WARNING: TITAN CHARGING [" + boss_ptr->telegraph_warning + "] ?";
            Vector2 w_sz = MeasureTextEx(font, warn_msg.c_str(), 13, 1.0f);
            DrawTextEx(font, warn_msg.c_str(), { (SCREEN_WIDTH - w_sz.x) / 2.0f, warn_bar.y + 10 }, 13, 1.0f, WHITE);
        }

        // -- Combo Milestone Banner ----------------------------------------------
        if (m_milestone_timer > 0) {
            float m_alpha = std::min(1.0f, m_milestone_timer / 0.4f);
            Vector2 m_sz = MeasureTextEx(font, m_milestone_text.c_str(), 20, 1.0f);
            Rectangle m_box = { (SCREEN_WIDTH - m_sz.x) / 2.0f - 20, 155, m_sz.x + 40, 38 };
            UI::DrawChamferedPanel(m_box, COLOR_GOLD_BRIGHT, ColorAlpha(COLOR_SURFACE_HIGH, 0.9f * m_alpha), 5.0f);
            DrawTextEx(font, m_milestone_text.c_str(), { (SCREEN_WIDTH - m_sz.x) / 2.0f, m_box.y + 9 }, 20, 1.0f, ColorAlpha(COLOR_GOLD_BRIGHT, m_alpha));
        }

        // -- Team Transcendence Banner -------------------------------------------
        if (m_team_transcendence_timer > 0) {
            float t_pulse = 0.5f + 0.5f * std::sin(GetTime() * 12.0f);
            DrawText("? TEAM TRANSCENDENCE ACTIVE: +20% DMG, +10% SPD ?", SCREEN_WIDTH / 2 - 200, 52, 12, ColorAlpha(COLOR_GOLD_BRIGHT, 0.7f + 0.3f * t_pulse));
        }

        // -- Low-HP Vignette & Critical Warning ----------------------------------
        if (m_squad[0].hp <= 35 && !m_squad[0].is_downed) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
            DrawRectangleLinesEx({ 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT }, 10.0f, ColorAlpha(COLOR_RED_BRIGHT, 0.2f + 0.4f * pulse));
            DrawText("? HULL INTEGRITY CRITICAL // USE SOMA [C] ?", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT - 45, 12, ColorAlpha(COLOR_RED_BRIGHT, 0.8f + 0.2f * pulse));
        }

        // Story Transmission
        if (m_wave_mgr.banner_timer() > 0) {
            std::string story = m_wave_mgr.get_story_transmission();
            if (!story.empty()) {
                UI::DrawChamferedPanel({ 100, 150, 700, 46 }, COLOR_CYAN_BRIGHT, { 5, 15, 30, 240 }, 6.0f);
                DrawText(story.c_str(), 120, 166, 12, COLOR_CYAN_BRIGHT);
            }
        }

        // -- Pause Menu with Controls Cheatsheet ---------------------------------
        if (m_is_paused) {
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 0, 0, 0, 195 });
            Rectangle pause_box = { SCREEN_WIDTH / 2.0f - 220, 150, 440, 310 };
            UI::DrawChamferedPanel(pause_box, COLOR_GOLD, COLOR_SURFACE_HIGH, 8.0f);

            DrawTextEx(font, "COMBAT SUSPENDED // PAUSE", { SCREEN_WIDTH / 2.0f - 120, pause_box.y + 20 }, 18, 1.0f, COLOR_GOLD_BRIGHT);

            Rectangle info_rec = { pause_box.x + 20, pause_box.y + 55, pause_box.width - 40, 75 };
            UI::DrawChamferedPanel(info_rec, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
            DrawText("PILOT FLIGHT CONTROLS:", static_cast<int>(info_rec.x + 10), static_cast<int>(info_rec.y + 8), 10, COLOR_MUTED);
            DrawText("[WASD] Movement  •  [L-Click] Fire  •  [SPACE] Warp Dash", static_cast<int>(info_rec.x + 10), static_cast<int>(info_rec.y + 24), 11, COLOR_GOLD_BRIGHT);
            DrawText("[Q/E] Chakram  •  [F] Brahmastra / Astra  •  [C] Soma  •  [V] Vajra", static_cast<int>(info_rec.x + 10), static_cast<int>(info_rec.y + 42), 11, COLOR_CYAN_BRIGHT);

            m_btn_resume.draw(font);
            m_btn_restart_wave.draw(font);
            m_btn_exit.draw(font);
        }

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::GAMEPLAY; }
    const Player& player() const { return m_squad[0]; }
    Player& player() { return m_squad[0]; }
    int current_wave() const { return m_wave_mgr.current_wave(); }

private:
    struct Star { float x, y, z; };
    ViewType m_next_view;
    bool m_is_paused;
    bool m_is_coop_mode;
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

    UI::Button m_btn_resume;
    UI::Button m_btn_restart_wave;
    UI::Button m_btn_exit;
};

} // namespace Vimana
