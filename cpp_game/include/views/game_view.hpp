#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
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

namespace Vimana {

class GameView : public IView {
public:
    GameView() : m_next_view(ViewType::GAMEPLAY), m_is_paused(false) {
        init();
    }

    void init() override {
        m_next_view = ViewType::GAMEPLAY;
        m_is_paused = false;
        m_bullets.clear();
        m_enemies.clear();
        m_powerups.clear();

        // Default to Pushpaka if not set
        if (!m_player.archetype) {
            m_player.init(&SHIP_FLEET[0]);
        }

        m_wave_mgr.start_campaign(1);
        m_btn_resume = UI::Button({ SCREEN_WIDTH / 2.0f - 110, 260, 220, 38 }, "RESUME", COLOR_GOLD_BRIGHT);
        m_btn_exit = UI::Button({ SCREEN_WIDTH / 2.0f - 110, 320, 220, 38 }, "ABORT MISSION", COLOR_RED_BRIGHT);

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

    void start_with_ship(const ShipArchetype* ship, const ConsumableInventory& pre_inv) {
        m_player.init(ship);
        m_player.inventory = pre_inv;
        m_bullets.clear();
        m_enemies.clear();
        m_powerups.clear();
        m_wave_mgr.start_campaign(1);
        m_is_paused = false;
        m_next_view = ViewType::GAMEPLAY;
    }

    void apply_boon_and_resume(BoonType boon) {
        m_player.apply_boon(boon);
        m_next_view = ViewType::GAMEPLAY;

        // Advance to next wave
        int next_w = m_wave_mgr.current_wave() + 1;
        if (next_w > 30) {
            // Victory!
            m_next_view = ViewType::VICTORY;
        } else {
            m_wave_mgr.prepare_wave(next_w);
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (IsKeyPressed(KEY_ESCAPE)) {
            m_is_paused = !m_is_paused;
        }

        if (m_is_paused) {
            if (m_btn_resume.update(mouse_pos)) m_is_paused = false;
            if (m_btn_exit.update(mouse_pos)) m_next_view = ViewType::MENU;
            return;
        }

        // Brahmastra Screen Nuke Key (F)
        if (IsKeyPressed(KEY_F) && m_player.brahmastra_bombs > 0) {
            m_player.brahmastra_bombs--;
            SoundSystem::instance().play_sfx("explosion.wav", 1.0f);
            m_particles.trigger_screen_shake(15.0f, 0.6f);

            // Wipe all enemy bullets
            for (auto& b : m_bullets) {
                if (b.is_enemy) b.active = false;
            }
            // Heavily damage all non-boss enemies
            for (auto& e : m_enemies) {
                if (e.active) {
                    e.hp -= 250;
                    m_particles.emit_explosion(e.pos, COLOR_GOLD_BRIGHT, 15, 180.0f);
                }
            }
            // Damage boss
            if (m_wave_mgr.is_boss_wave() && m_wave_mgr.get_boss().active) {
                m_wave_mgr.get_boss().take_damage(350);
            }
        }

        // Update Stars
        for (auto& s : m_stars) {
            s.y += s.z * 30.0f * dt;
            if (s.y > SCREEN_HEIGHT) {
                s.y = 0;
                s.x = static_cast<float>(std::rand() % SCREEN_WIDTH);
            }
        }

        // Update Player
        m_player.handle_input(dt, mouse_pos, m_bullets, false);
        m_player.update(dt);

        // Player Thruster Particle
        float rad = (m_player.angle + 180.0f) * (3.14159f / 180.0f);
        Vector2 engine_pos = { m_player.pos.x + std::cos(rad) * m_player.radius, m_player.pos.y + std::sin(rad) * m_player.radius };
        m_particles.emit_thrust(engine_pos, { std::cos(rad), std::sin(rad) }, COLOR_CYAN_BRIGHT);

        // Update Bullets
        for (auto& b : m_bullets) {
            b.update(dt);
        }

        // Update Wave Manager & Boss
        m_wave_mgr.update(dt, m_enemies, m_bullets, m_player.pos);

        // Update Enemies
        for (auto& e : m_enemies) {
            e.update(dt, m_player.pos, m_bullets, m_enemies);
        }

        // Update Astral Cubes
        float magnet_radius = m_player.has_boon(BoonType::GARUDA_CELESTIAL_MAGNET) ? 350.0f : 120.0f;
        for (auto& p : m_powerups) {
            p.update(dt, m_player.pos, magnet_radius);
        }

        // Collision Resolution
        int prana_earned = 0;
        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;
        m_collisions.resolve_combat(m_player, m_enemies, boss_ptr, m_bullets, m_powerups, m_particles, prana_earned);
        if (prana_earned > 0) {
            CurrencySystem::instance().add_prana_shards(prana_earned);
        }

        // Update Particles
        m_particles.update(dt);

        // Check Player Death
        if (m_player.hp <= 0) {
            SoundSystem::instance().play_sfx("game_over.wav");
            m_next_view = ViewType::GAME_OVER;
            return;
        }

        // Check Wave Cleared
        if (m_wave_mgr.is_wave_cleared()) {
            CurrencySystem::instance().add_prana_shards(PRANA_REWARD_WAVE_CLEAR);
            DBSystem::instance().update_max_wave(m_wave_mgr.current_wave());
            SoundSystem::instance().play_sfx("wave_clear.wav");

            if (m_wave_mgr.current_wave() == 30) {
                // Defeated Hiranyakashipu at Wave 30 -> Unlock Narasimha!
                CurrencySystem::instance().try_unlock_ship_with_prana("narasimha");
                m_next_view = ViewType::VICTORY;
            } else {
                m_next_view = ViewType::BOON_SELECT;
            }
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

        // Cockpit HUD
        Boss* boss_ptr = m_wave_mgr.is_boss_wave() ? &m_wave_mgr.get_boss() : nullptr;
        Font font = AssetManager::instance().font();
        UI::HUD::draw(m_player, m_wave_mgr.current_wave(), realm, boss_ptr, m_enemies, font);

        // Story Transmission or Realm Banner
        if (m_wave_mgr.banner_timer() > 0) {
            std::string story = m_wave_mgr.get_story_transmission();
            if (!story.empty()) {
                UI::DrawChamferedPanel({ 100, 160, 700, 50 }, COLOR_CYAN_BRIGHT, { 5, 15, 30, 240 }, 6.0f);
                DrawText(story.c_str(), 120, 178, 11, COLOR_CYAN_BRIGHT);
            }
        }

        // Pause Menu
        if (m_is_paused) {
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 0, 0, 0, 180 });
            UI::DrawChamferedPanel({ SCREEN_WIDTH / 2.0f - 150, 200, 300, 200 }, COLOR_GOLD, COLOR_SURFACE_HIGH, 6.0f);
            DrawText("PAUSED", SCREEN_WIDTH / 2 - 40, 220, 20, COLOR_GOLD_BRIGHT);
            m_btn_resume.draw(font);
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

    UI::Button m_btn_resume;
    UI::Button m_btn_exit;
};

} // namespace Vimana
