#pragma once
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "entities/player.hpp"
#include "entities/enemy.hpp"
#include "entities/boss.hpp"
#include "entities/bullet.hpp"
#include "entities/powerup.hpp"
#include "systems/wave_manager.hpp"
#include "systems/collision_system.hpp"
#include "systems/particle_system.hpp"
#include "systems/sound_system.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "ui/hud.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class GameView : public IView {
public:
    GameView() 
        : m_next_view(ViewType::GAMEPLAY), 
          m_is_paused(false),
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

        if (!m_player.archetype) {
            m_player.init(&SHIP_FLEET[0]);
        }

        m_wave_mgr.start_campaign(1);
        m_wave_start_hp = m_player.hp;
        m_wave_kills = 0;
        m_milestone_text = "";
        m_milestone_timer = 0.0f;
        m_last_milestone = 0;

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

    void start_with_ship(const ShipArchetype* ship, const ConsumableInventory& pre_inv, int starting_wave = 1) {
        m_player.init(ship);
        m_player.inventory = pre_inv;
        m_bullets.clear();
        m_enemies.clear();
        m_powerups.clear();
        m_wave_mgr.start_campaign(starting_wave);
        m_wave_start_hp = m_player.hp;
        m_wave_kills = 0;
        m_is_paused = false;
        m_next_view = ViewType::GAMEPLAY;
        m_milestone_text = "";
        m_milestone_timer = 0.0f;
        m_last_milestone = 0;
    }

    void apply_boon_and_resume(BoonType boon) {
        m_player.apply_boon(boon);
        m_next_view = ViewType::GAMEPLAY;

        // Advance to next wave
        int next_w = m_wave_mgr.current_wave() + 1;
        if (next_w > 30) {
            m_next_view = ViewType::VICTORY;
        } else {
            m_bullets.clear();
            m_enemies.clear();
            m_wave_mgr.prepare_wave(next_w);
            m_wave_start_hp = m_player.hp;
            m_wave_kills = 0;
        }
    }

    const WaveResult& latest_wave_result() const { return m_last_wave_result; }

    void update(float dt, Vector2 mouse_pos) override {
        if (IsKeyPressed(KEY_ESCAPE)) {
            m_is_paused = !m_is_paused;
        }

        if (m_is_paused) {
            if (m_btn_resume.update(mouse_pos)) m_is_paused = false;
            if (m_btn_restart_wave.update(mouse_pos)) {
                m_bullets.clear();
                m_enemies.clear();
                m_wave_mgr.prepare_wave(m_wave_mgr.current_wave());
                m_player.hp = m_player.max_hp;
                m_wave_start_hp = m_player.hp;
                m_is_paused = false;
            }
            if (m_btn_exit.update(mouse_pos)) m_next_view = ViewType::CAMPAIGN_MAP;
            return;
        }

        // ── 1. Brahmastra Screen Nuke (F Key) ────────────────────────────────────
        if (IsKeyPressed(KEY_F) && m_player.brahmastra_bombs > 0) {
            m_player.brahmastra_bombs--;
            SoundSystem::instance().play_sfx("explosion.wav", 1.0f);
            m_particles.trigger_screen_shake(18.0f, 0.7f);

            for (auto& b : m_bullets) {
                if (b.is_enemy) b.active = false;
            }
            for (auto& e : m_enemies) {
                if (e.active) {
                    e.hp -= 280;
                    m_particles.emit_explosion(e.pos, COLOR_GOLD_BRIGHT, 15, 180.0f);
                }
            }
            if (m_wave_mgr.is_boss_wave() && m_wave_mgr.get_boss().active) {
                m_wave_mgr.get_boss().take_damage(400);
            }
            m_particles.add_floating_text({ SCREEN_WIDTH / 2.0f - 110.0f, SCREEN_HEIGHT / 2.0f }, "BRAHMASTRA DETONATION!", COLOR_GOLD_BRIGHT);
        }

        // ── 2. Parallax Stars ───────────────────────────────────────────────────
        for (auto& s : m_stars) {
            s.y += s.z * 30.0f * dt;
            if (s.y > SCREEN_HEIGHT) {
                s.y = 0;
                s.x = static_cast<float>(std::rand() % SCREEN_WIDTH);
            }
        }

        // ── 3. Player Update & Thruster ─────────────────────────────────────────
        m_player.handle_input(dt, mouse_pos, m_bullets, false);
        m_player.update(dt);

        float rad = (m_player.angle + 180.0f) * (3.14159f / 180.0f);
        Vector2 engine_pos = { m_player.pos.x + std::cos(rad) * m_player.radius, m_player.pos.y + std::sin(rad) * m_player.radius };
        m_particles.emit_thrust(engine_pos, { std::cos(rad), std::sin(rad) }, COLOR_CYAN_BRIGHT);

        // ── 4. Near-Miss Graze Detection ────────────────────────────────────────
        for (auto& b : m_bullets) {
            if (b.active && b.is_enemy && !b.grazed) {
                float dist = Vector2Distance(b.pos, m_player.pos);
                if (dist < m_player.radius + PLAYER_GRAZE_RADIUS && dist > m_player.radius + 2.0f) {
                    b.grazed = true;
                    m_player.score += SCORE_NEAR_MISS;
                    m_particles.add_floating_text({ m_player.pos.x - 30.0f, m_player.pos.y - 20.0f }, "NEAR MISS +25", COLOR_CYAN_BRIGHT);
                    m_particles.trigger_screen_shake(2.0f, 0.08f);
                    SoundSystem::instance().play_sfx("ui_click.wav", 0.4f);
                }
            }
        }

        // ── 5. Combo Milestone Announcements ────────────────────────────────────
        if (m_player.combo >= 50 && m_last_milestone < 50) {
            m_last_milestone = 50;
            m_milestone_text = "★ x50 TRANSCENDENCE: MAHAYUDDHA SUPREME! ★";
            m_milestone_timer = 2.2f;
            SoundSystem::instance().play_sfx("wave_clear.wav");
        } else if (m_player.combo >= 30 && m_last_milestone < 30) {
            m_last_milestone = 30;
            m_milestone_text = "★ x30 DIVINE TRANSCENDENCE! ★";
            m_milestone_timer = 2.0f;
            SoundSystem::instance().play_sfx("ui_click.wav");
        } else if (m_player.combo >= 20 && m_last_milestone < 20) {
            m_last_milestone = 20;
            m_milestone_text = "x20 ASHVIN FURY!";
            m_milestone_timer = 1.8f;
        } else if (m_player.combo >= 10 && m_last_milestone < 10) {
            m_last_milestone = 10;
            m_milestone_text = "x10 CELESTIAL RHYTHM!";
            m_milestone_timer = 1.5f;
        }

        if (m_milestone_timer > 0) m_milestone_timer -= dt;
        if (m_player.combo <= 1) m_last_milestone = 0;

        // ── 6. Update Bullets ───────────────────────────────────────────────────
        for (auto& b : m_bullets) {
            b.update(dt);
        }

        // ── 7. Wave Manager & Enemies ───────────────────────────────────────────
        m_wave_mgr.update(dt, m_enemies, m_bullets, m_player.pos);

        for (auto& e : m_enemies) {
            e.update(dt, m_player.pos, m_bullets, m_enemies);
        }

        // ── 8. Astral Cubes & Magnetism ─────────────────────────────────────────
        float magnet_radius = m_player.has_boon(BoonType::GARUDA_CELESTIAL_MAGNET) ? 350.0f : 120.0f;
        for (auto& p : m_powerups) {
            p.update(dt, m_player.pos, magnet_radius);
        }

        // ── 9. Combat Collisions ────────────────────────────────────────────────
        int prana_earned = 0;
        int pre_kills = m_player.kills;
        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;
        m_collisions.resolve_combat(m_player, m_enemies, boss_ptr, m_bullets, m_powerups, m_particles, prana_earned);
        if (prana_earned > 0) {
            CurrencySystem::instance().add_prana_shards(prana_earned);
        }
        m_wave_kills += (m_player.kills - pre_kills);

        // ── 10. Particles ───────────────────────────────────────────────────────
        m_particles.update(dt);

        // ── 12. Check Player Defeat ─────────────────────────────────────────────
        if (m_player.hp <= 0) {
            SoundSystem::instance().play_sfx("game_over.wav");
            m_next_view = ViewType::GAME_OVER;
            return;
        }

        // ── 13. Check Wave Cleared ──────────────────────────────────────────────
        if (m_wave_mgr.is_wave_cleared()) {
            int dmg_taken = std::max(0, m_wave_start_hp - m_player.hp);
            bool no_dmg = (dmg_taken == 0);
            bool perfect = (no_dmg && m_player.max_combo >= 10);

            // Determine Rank
            PerformanceRank rank = PerformanceRank::B_RANK;
            if (no_dmg || m_player.max_combo >= 15) {
                rank = PerformanceRank::S_RANK;
            } else if (dmg_taken <= 25 || m_player.max_combo >= 8) {
                rank = PerformanceRank::A_RANK;
            } else if (dmg_taken > 60) {
                rank = PerformanceRank::C_RANK;
            }

            int wave_score = 500 + m_player.max_combo * 35;
            int wave_prana = PRANA_REWARD_WAVE_CLEAR + (no_dmg ? BONUS_NO_DEATH : 0);

            CurrencySystem::instance().add_prana_shards(wave_prana);
            DBSystem::instance().update_max_wave(m_wave_mgr.current_wave());

            m_last_wave_result = {
                m_wave_mgr.current_wave(),
                m_wave_kills,
                dmg_taken,
                m_player.max_combo,
                88, // Accuracy
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
        ClearBackground(realm.bg_color);

        // Parallax stars
        for (const auto& s : m_stars) {
            DrawCircle(static_cast<int>(s.x), static_cast<int>(s.y), s.z, realm.accent_color);
        }

        // Screen Shake offset
        Vector2 shake = m_particles.get_shake_offset();
        BeginMode2D({ { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT / 2.0f }, { SCREEN_WIDTH / 2.0f + shake.x, SCREEN_HEIGHT / 2.0f + shake.y }, 0.0f, 1.0f });

        // Draw Astral Cubes
        for (const auto& p : m_powerups) {
            p.draw();
        }

        // Draw Bullets
        for (const auto& b : m_bullets) {
            b.draw();
        }

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

        // Draw Player
        std::string p_sprite = m_player.archetype ? m_player.archetype->sprite_file : "pushpaka.png";
        Texture2D p_tex = AssetManager::instance().get_texture(p_sprite);
        m_player.draw(p_tex);

        // Draw Particles
        m_particles.draw();

        EndMode2D();

        Font font = AssetManager::instance().font();

        // Cockpit HUD
        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;
        UI::HUD::draw(m_player, m_wave_mgr.current_wave(), realm, boss_ptr, m_enemies, font);

        // ── Boss Attack Telegraph Warning Banner ───────────────────────────────
        if (boss_ptr && boss_ptr->active && boss_ptr->is_telegraphing) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 18.0f);
            Rectangle warn_bar = { SCREEN_WIDTH / 2.0f - 240, 110, 480, 36 };
            UI::DrawChamferedPanel(warn_bar, COLOR_RED_BRIGHT, ColorAlpha(COLOR_RED_BRIGHT, 0.25f + 0.3f * pulse), 4.0f);
            std::string warn_msg = "⚠ WARNING: TITAN CHARGING [" + boss_ptr->telegraph_warning + "] ⚠";
            Vector2 w_sz = MeasureTextEx(font, warn_msg.c_str(), 13, 1.0f);
            DrawTextEx(font, warn_msg.c_str(), { (SCREEN_WIDTH - w_sz.x) / 2.0f, warn_bar.y + 10 }, 13, 1.0f, WHITE);
        }

        // ── Combo Milestone Banner ──────────────────────────────────────────────
        if (m_milestone_timer > 0) {
            float m_alpha = std::min(1.0f, m_milestone_timer / 0.4f);
            Vector2 m_sz = MeasureTextEx(font, m_milestone_text.c_str(), 20, 1.0f);
            Rectangle m_box = { (SCREEN_WIDTH - m_sz.x) / 2.0f - 20, 155, m_sz.x + 40, 38 };
            UI::DrawChamferedPanel(m_box, COLOR_GOLD_BRIGHT, ColorAlpha(COLOR_SURFACE_HIGH, 0.9f * m_alpha), 5.0f);
            DrawTextEx(font, m_milestone_text.c_str(), { (SCREEN_WIDTH - m_sz.x) / 2.0f, m_box.y + 9 }, 20, 1.0f, ColorAlpha(COLOR_GOLD_BRIGHT, m_alpha));
        }

        // ── Low-HP Vignette & Critical Warning ──────────────────────────────────
        if (m_player.hp <= 35) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
            DrawRectangleLinesEx({ 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT }, 10.0f, ColorAlpha(COLOR_RED_BRIGHT, 0.2f + 0.4f * pulse));
            DrawText("⚠ HULL INTEGRITY CRITICAL // USE SOMA [C] ⚠", SCREEN_WIDTH / 2 - 170, SCREEN_HEIGHT - 45, 12, ColorAlpha(COLOR_RED_BRIGHT, 0.8f + 0.2f * pulse));
        }

        // Story Transmission or Realm Banner
        if (m_wave_mgr.banner_timer() > 0) {
            std::string story = m_wave_mgr.get_story_transmission();
            if (!story.empty()) {
                UI::DrawChamferedPanel({ 100, 150, 700, 46 }, COLOR_CYAN_BRIGHT, { 5, 15, 30, 240 }, 6.0f);
                DrawText(story.c_str(), 120, 166, 12, COLOR_CYAN_BRIGHT);
            }
        }

        // ── Enhanced Pause Menu with Controls Cheatsheet ────────────────────────
        if (m_is_paused) {
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 0, 0, 0, 195 });
            Rectangle pause_box = { SCREEN_WIDTH / 2.0f - 220, 150, 440, 310 };
            UI::DrawChamferedPanel(pause_box, COLOR_GOLD, COLOR_SURFACE_HIGH, 8.0f);

            DrawTextEx(font, "COMBAT SUSPENDED // PAUSE", { SCREEN_WIDTH / 2.0f - 120, pause_box.y + 20 }, 18, 1.0f, COLOR_GOLD_BRIGHT);

            // Controls Cheatsheet inside Pause
            Rectangle info_rec = { pause_box.x + 20, pause_box.y + 55, pause_box.width - 40, 75 };
            UI::DrawChamferedPanel(info_rec, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
            DrawText("PILOT FLIGHT CONTROLS:", static_cast<int>(info_rec.x + 10), static_cast<int>(info_rec.y + 8), 10, COLOR_MUTED);
            DrawText("[WASD] Movement  •  [L-Click] Fire  •  [SPACE] Warp Dash", static_cast<int>(info_rec.x + 10), static_cast<int>(info_rec.y + 24), 11, COLOR_GOLD_BRIGHT);
            DrawText("[Q/E] Chakram  •  [F] Brahmastra Nuke  •  [C] Soma  •  [V] Vajra", static_cast<int>(info_rec.x + 10), static_cast<int>(info_rec.y + 42), 11, COLOR_CYAN_BRIGHT);

            m_btn_resume.draw(font);
            m_btn_restart_wave.draw(font);
            m_btn_exit.draw(font);
        }

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::GAMEPLAY; }
    const Player& player() const { return m_player; }
    int current_wave() const { return m_wave_mgr.current_wave(); }

private:
    struct Star { float x, y, z; };
    ViewType m_next_view;
    bool m_is_paused;
    std::vector<Star> m_stars;

    Player m_player;
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
