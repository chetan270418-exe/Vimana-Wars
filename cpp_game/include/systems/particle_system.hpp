#pragma once
#include <vector>
#include <string>
#include <cmath>
#include <array>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/dsa/object_pool.hpp"
#include "core/dsa/ring_buffer.hpp"

namespace Vimana {

struct Particle {
    bool active = false;
    Vector2 pos = { 0, 0 };
    Vector2 vel = { 0, 0 };
    Color color = COLOR_GOLD_BRIGHT;
    float size = 3.0f;
    float lifetime = 0.0f;
    float max_lifetime = 0.5f;

    void update(float dt) {
        if (!active) return;
        pos.x += vel.x * dt;
        pos.y += vel.y * dt;
        lifetime += dt;
        if (lifetime >= max_lifetime) {
            active = false;
        }
    }

    void draw() const {
        if (!active) return;
        float progress = lifetime / max_lifetime;
        Color c = color;
        c.a = static_cast<unsigned char>((1.0f - progress) * 255);
        float sz = size * (1.0f - progress * 0.5f);
        DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), sz, c);
    }
};

struct FloatingText {
    bool active = false;
    std::string text = "";
    Vector2 pos = { 0, 0 };
    Color color = COLOR_GOLD_BRIGHT;
    float lifetime = 0.0f;
    float max_lifetime = 0.8f;

    void update(float dt) {
        if (!active) return;
        pos.y -= 45.0f * dt;
        lifetime += dt;
        if (lifetime >= max_lifetime) {
            active = false;
        }
    }

    void draw() const {
        if (!active) return;
        float progress = lifetime / max_lifetime;
        Color c = color;
        c.a = static_cast<unsigned char>((1.0f - progress) * 255);
        DrawText(text.c_str(), static_cast<int>(pos.x), static_cast<int>(pos.y), 16, c);
    }
};

struct DashGhost {
    bool active = false;
    Vector2 pos = { 0, 0 };
    std::string sprite_key = "";
    float rotation = 0.0f;
    Color color = COLOR_CYAN_BRIGHT;
    float lifetime = 0.0f;
    float max_lifetime = 0.22f;

    void update(float dt) {
        if (!active) return;
        lifetime += dt;
        if (lifetime >= max_lifetime) active = false;
    }

    void draw() const {
        if (!active) return;
        float progress = lifetime / max_lifetime;
        Color c = color;
        c.a = static_cast<unsigned char>((1.0f - progress) * 160);

        Texture2D tex = AssetManager::instance().get_texture(sprite_key);
        if (tex.id > 0) {
            Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { pos.x, pos.y, 48.0f, 48.0f };
            Vector2 origin = { 24.0f, 24.0f };
            DrawTexturePro(tex, src, dest, origin, rotation, c);
        }
    }
};

struct ShieldRipple {
    bool active = false;
    Vector2 pos = { 0, 0 };
    float current_r = 10.0f;
    float max_r = 50.0f;
    Color color = COLOR_CYAN_BRIGHT;
    float lifetime = 0.0f;
    float max_lifetime = 0.35f;

    void update(float dt) {
        if (!active) return;
        lifetime += dt;
        current_r = 10.0f + (max_r - 10.0f) * (lifetime / max_lifetime);
        if (lifetime >= max_lifetime) active = false;
    }

    void draw() const {
        if (!active) return;
        float progress = lifetime / max_lifetime;
        Color c = color;
        c.a = static_cast<unsigned char>((1.0f - progress) * 200);
        DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), current_r, c);
        c.a = static_cast<unsigned char>((1.0f - progress) * 80);
        DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), current_r * 0.8f, c);
    }
};

struct CoopAstraVFX {
    bool active = false;
    Vector2 p1 = { 0, 0 };
    Vector2 p2 = { 0, 0 };
    Color col1 = COLOR_GOLD_BRIGHT;
    Color col2 = COLOR_CYAN_BRIGHT;
    float timer = 0.0f;
    float duration = 1.2f;

    void update(float dt) {
        if (!active) return;
        timer += dt;
        if (timer >= duration) active = false;
    }

    void draw() const {
        if (!active) return;
        float progress = timer / duration;
        Vector2 center = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT / 2.0f };

        // Dual energy conduit beams from ships to center
        if (progress < 0.6f) {
            float beam_a = (1.0f - (progress / 0.6f)) * 255.0f;
            DrawLineEx(p1, center, 4.0f, ColorAlpha(col1, beam_a / 255.0f));
            DrawLineEx(p2, center, 4.0f, ColorAlpha(col2, beam_a / 255.0f));
        }

        // Expanding Celestial Yantra Mandala Shockwave
        float ring_r = progress * (SCREEN_WIDTH * 0.7f);
        float ring_a = (1.0f - progress) * 240.0f;
        Color mand_col = COLOR_GOLD_BRIGHT;
        mand_col.a = static_cast<unsigned char>(ring_a);

        DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), ring_r, mand_col);
        mand_col.a = static_cast<unsigned char>(ring_a * 0.5f);
        DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), ring_r * 0.75f, mand_col);
    }
};

struct BossPhaseVFX {
    bool active = false;
    Vector2 center = { 0, 0 };
    Color color = COLOR_GOLD_BRIGHT;
    int phase = 2;
    float timer = 0.0f;
    float duration = 1.15f;

    void update(float dt) {
        if (!active) return;
        timer += dt;
        if (timer >= duration) active = false;
    }

    void draw() const {
        if (!active) return;
        float progress = std::clamp(timer / duration, 0.0f, 1.0f);
        float radius = 34.0f + progress * 95.0f;
        Color ring = color;
        ring.a = static_cast<unsigned char>((1.0f - progress) * 220.0f);
        DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), radius, ring);
        DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), radius * 0.72f, ColorAlpha(ring, 0.55f));
        for (int i = 0; i < 8; ++i) {
            float angle = (i * 45.0f + timer * 110.0f) * (3.14159f / 180.0f);
            Vector2 a = { center.x + std::cos(angle) * radius * 0.72f, center.y + std::sin(angle) * radius * 0.72f };
            Vector2 b = { center.x + std::cos(angle) * radius, center.y + std::sin(angle) * radius };
            DrawLineEx(a, b, 2.0f, ring);
        }
    }
};

class ParticleSystem {
public:
    ParticleSystem() = default;

    void emit_explosion(Vector2 pos, Color color, int count = 25, float speed = 180.0f) {
        for (int i = 0; i < count; ++i) {
            Particle* p = m_particle_pool.acquire();
            if (!p) break;
            p->active = true;
            p->pos = pos;
            float angle = (std::rand() % 360) * (3.14159f / 180.0f);
            float spd = speed * (0.4f + 0.6f * ((std::rand() % 100) / 100.0f));
            p->vel = { std::cos(angle) * spd, std::sin(angle) * spd };
            p->color = color;
            p->size = 3.5f + (std::rand() % 30) / 10.0f;
            p->lifetime = 0.0f;
            p->max_lifetime = 0.35f + (std::rand() % 25) / 100.0f;
        }
    }

    void emit_thrust(Vector2 pos, Vector2 direction, Color color) {
        Particle* p = m_particle_pool.acquire();
        if (!p) return;
        p->active = true;
        p->pos = pos;
        float spread = ((std::rand() % 40) - 20) * (3.14159f / 180.0f);
        float spd = 120.0f + (std::rand() % 60);
        p->vel = { direction.x * spd + std::sin(spread) * 20.0f, direction.y * spd + std::cos(spread) * 20.0f };
        p->color = color;
        p->size = 2.5f;
        p->lifetime = 0.0f;
        p->max_lifetime = 0.22f;
    }

    void emit_muzzle_flash(Vector2 pos, Vector2 direction, Color color) {
        for (int i = 0; i < 6; ++i) {
            Particle* p = m_particle_pool.acquire();
            if (!p) break;
            p->active = true;
            p->pos = pos;
            float angle = std::atan2(direction.y, direction.x) + ((std::rand() % 30) - 15) * (3.14159f / 180.0f);
            float spd = 180.0f + (std::rand() % 100);
            p->vel = { std::cos(angle) * spd, std::sin(angle) * spd };
            p->color = color;
            p->size = 3.0f;
            p->lifetime = 0.0f;
            p->max_lifetime = 0.12f;
        }
    }

    void emit_dash_ghost(Vector2 pos, const std::string& sprite_key, float rot, Color color) {
        for (auto& g : m_dash_ghosts) {
            if (!g.active) {
                g.active = true;
                g.pos = pos;
                g.sprite_key = sprite_key;
                g.rotation = rot;
                g.color = color;
                g.lifetime = 0.0f;
                g.max_lifetime = 0.20f;
                break;
            }
        }
    }

    void emit_shield_ripple(Vector2 pos, float max_r, Color color) {
        for (auto& r : m_shield_ripples) {
            if (!r.active) {
                r.active = true;
                r.pos = pos;
                r.current_r = 10.0f;
                r.max_r = max_r;
                r.color = color;
                r.lifetime = 0.0f;
                r.max_lifetime = 0.30f;
                break;
            }
        }
    }

    void emit_crit_hit(Vector2 pos, int damage) {
        emit_explosion(pos, COLOR_GOLD_BRIGHT, 18, 160.0f);
        add_floating_text(pos, "CRIT! " + std::to_string(damage), COLOR_GOLD_BRIGHT);
    }

    void emit_coop_astra_sequence(Vector2 p1, Vector2 p2, Color col1, Color col2) {
        m_coop_astra.active = true;
        m_coop_astra.p1 = p1;
        m_coop_astra.p2 = p2;
        m_coop_astra.col1 = col1;
        m_coop_astra.col2 = col2;
        m_coop_astra.timer = 0.0f;
        m_coop_astra.duration = 1.2f;
        trigger_screen_shake(9.0f, 0.6f);
    }

    void add_floating_text(Vector2 pos, const std::string& text, Color color) {
        FloatingText ft;
        ft.active = true;
        ft.text = text;
        ft.pos = pos;
        ft.color = color;
        ft.lifetime = 0.0f;
        ft.max_lifetime = 0.75f;
        m_text_buffer.push(ft);
    }

    void emit_boss_phase_transition(Vector2 pos, Color color, int phase) {
        m_boss_phase_vfx.active = true;
        m_boss_phase_vfx.center = pos;
        m_boss_phase_vfx.color = color;
        m_boss_phase_vfx.phase = phase;
        m_boss_phase_vfx.timer = 0.0f;
        m_boss_phase_vfx.duration = 1.15f;
        add_floating_text({ pos.x - 72.0f, pos.y - 72.0f }, "PHASE " + std::to_string(phase) + " AWAKENED", COLOR_GOLD_BRIGHT);
        trigger_screen_shake(12.0f, 0.45f);
    }

    void trigger_screen_shake(float intensity, float duration) {
        m_shake_intensity = intensity;
        m_shake_duration = duration;
        m_shake_timer = duration;
    }

    Vector2 get_shake_offset() const {
        if (m_shake_timer <= 0) return { 0, 0 };
        float progress = m_shake_timer / m_shake_duration;
        float curr_int = m_shake_intensity * progress;
        float ox = ((std::rand() % 200) - 100) / 100.0f * curr_int;
        float oy = ((std::rand() % 200) - 100) / 100.0f * curr_int;
        return { ox, oy };
    }

    void update(float dt) {
        if (m_shake_timer > 0) {
            m_shake_timer -= dt;
        }

        auto& pool = m_particle_pool.raw_storage();
        for (auto& p : pool) {
            if (p.active) {
                p.update(dt);
                if (!p.active) {
                    m_particle_pool.release(&p);
                }
            }
        }

        for (auto& g : m_dash_ghosts) {
            if (g.active) g.update(dt);
        }

        for (auto& r : m_shield_ripples) {
            if (r.active) r.update(dt);
        }

        if (m_coop_astra.active) {
            m_coop_astra.update(dt);
        }

        m_boss_phase_vfx.update(dt);

        for (size_t i = 0; i < m_text_buffer.size(); ++i) {
            if (m_text_buffer[i].active) {
                m_text_buffer[i].update(dt);
            }
        }
    }

    void draw() const {
        // Draw ghosts
        for (const auto& g : m_dash_ghosts) {
            if (g.active) g.draw();
        }

        // Draw shield ripples
        for (const auto& r : m_shield_ripples) {
            if (r.active) r.draw();
        }

        // Draw Coop Astra
        if (m_coop_astra.active) {
            m_coop_astra.draw();
        }

        m_boss_phase_vfx.draw();

        // Draw particles
        const auto& pool = m_particle_pool.raw_storage();
        for (const auto& p : pool) {
            if (p.active) p.draw();
        }

        for (size_t i = 0; i < m_text_buffer.size(); ++i) {
            if (m_text_buffer[i].active) m_text_buffer[i].draw();
        }
    }

private:
    DSA::ObjectPool<Particle, 1024> m_particle_pool;
    DSA::RingBuffer<FloatingText, 64> m_text_buffer;
    std::array<DashGhost, 16> m_dash_ghosts;
    std::array<ShieldRipple, 16> m_shield_ripples;
    CoopAstraVFX m_coop_astra;
    BossPhaseVFX m_boss_phase_vfx;
    float m_shake_intensity = 0.0f;
    float m_shake_duration = 0.0f;
    float m_shake_timer = 0.0f;
};

} // namespace Vimana
