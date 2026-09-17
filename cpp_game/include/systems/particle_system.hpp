#pragma once
#include <vector>
#include <string>
#include <cmath>
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

        for (size_t i = 0; i < m_text_buffer.size(); ++i) {
            if (m_text_buffer[i].active) {
                m_text_buffer[i].update(dt);
            }
        }
    }

    void draw() const {
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
    float m_shake_intensity = 0.0f;
    float m_shake_duration = 0.0f;
    float m_shake_timer = 0.0f;
};

} // namespace Vimana
