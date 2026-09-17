#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "entities/player.hpp"
#include "entities/bullet.hpp"
#include "entities/enemy.hpp"
#include "entities/boss.hpp"
#include "systems/particle_system.hpp"
#include "systems/sound_system.hpp"

namespace Vimana {

class CoOpAstraSystem {
public:
    static CoOpAstraSystem& instance() {
        static CoOpAstraSystem sys;
        return sys;
    }

    void reset() {
        m_last_trigger_player = -1;
        m_trigger_window_timer = 0.0f;
        m_cooldown_timer = 0.0f;
        m_synergy_active_timer = 0.0f;
    }

    void update(float dt) {
        if (m_trigger_window_timer > 0) m_trigger_window_timer -= dt;
        if (m_cooldown_timer > 0) m_cooldown_timer -= dt;
        if (m_synergy_active_timer > 0) m_synergy_active_timer -= dt;
    }

    bool register_astra_invocation(
        int player_idx,
        std::vector<Player>& squad,
        std::vector<Bullet>& bullets,
        std::vector<Enemy>& enemies,
        Boss* boss,
        ParticleSystem& particles
    ) {
        if (m_cooldown_timer > 0) return false;

        if (m_trigger_window_timer > 0 && m_last_trigger_player != player_idx && m_last_trigger_player >= 0) {
            execute_dual_astra(m_last_trigger_player, player_idx, squad, bullets, enemies, boss, particles);
            m_trigger_window_timer = 0.0f;
            m_last_trigger_player = -1;
            m_cooldown_timer = CO_OP_ASTRA_COOLDOWN;
            return true;
        }

        m_last_trigger_player = player_idx;
        m_trigger_window_timer = CO_OP_ASTRA_SYNC_WIN;
        return false;
    }

    bool is_synergy_active() const { return m_synergy_active_timer > 0; }

private:
    CoOpAstraSystem() 
        : m_last_trigger_player(-1), m_trigger_window_timer(0.0f), 
          m_cooldown_timer(0.0f), m_synergy_active_timer(0.0f) {}

    void execute_dual_astra(
        int p1_idx,
        int p2_idx,
        std::vector<Player>& squad,
        std::vector<Bullet>& bullets,
        std::vector<Enemy>& enemies,
        Boss* boss,
        ParticleSystem& particles
    ) {
        m_synergy_active_timer = 4.0f;
        SoundSystem::instance().play_sfx("wave_clear.wav", 1.0f);
        if (g_screen_shake_enabled) particles.trigger_screen_shake(20.0f, 0.8f);

        particles.add_floating_text({ SCREEN_WIDTH / 2.0f - 140.0f, SCREEN_HEIGHT / 2.0f - 30.0f }, "? SANGHA DUAL ASTRA SYNERGY! ?", COLOR_GOLD_BRIGHT);

        for (auto& p : squad) {
            p.invincibility_timer = 5.0f;
            p.has_kavach_shield = true;
            p.kavach_timer = 5.0f;
        }

        for (auto& b : bullets) {
            if (b.is_enemy) b.active = false;
        }

        for (auto& e : enemies) {
            if (e.active) {
                e.hp -= 450;
                particles.emit_explosion(e.pos, COLOR_CYAN_BRIGHT, 18, 160.0f);
            }
        }

        if (boss && boss->active) {
            boss->take_damage(600);
            particles.emit_explosion(boss->pos, COLOR_GOLD_BRIGHT, 25, 200.0f);
        }

        for (int i = 0; i < 32; ++i) {
            float rad = (i * (360.0f / 32.0f)) * (3.14159f / 180.0f);
            Bullet b;
            b.active = true;
            b.pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT / 2.0f };
            b.vel = { std::cos(rad) * 600.0f, std::sin(rad) * 600.0f };
            b.damage = 120;
            b.radius = 8.0f;
            b.color = COLOR_GOLD_BRIGHT;
            b.pierce_remaining = 5;
            b.owner_player_id = static_cast<uint8_t>(p1_idx);
            b.is_player_owned = true;
            bullets.push_back(b);
        }
    }

    int m_last_trigger_player;
    float m_trigger_window_timer;
    float m_cooldown_timer;
    float m_synergy_active_timer;
};

} // namespace Vimana
