#pragma once
#include <cmath>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

struct Powerup {
    bool active = false;
    Vector2 pos = { 0, 0 };
    Vector2 vel = { 0, 0 };
    PowerupType type = PowerupType::AMRITA_HEAL;
    float radius = 16.0f;
    float lifetime = 0.0f;
    float max_lifetime = 14.0f;
    float rotation = 0.0f;

    void update(float dt, Vector2 player_pos, float magnet_radius) {
        if (!active) return;
        lifetime += dt;
        rotation += 90.0f * dt;

        // Magnet attraction
        float dist = Vector2Distance(pos, player_pos);
        if (dist < magnet_radius && dist > 1.0f) {
            Vector2 dir = Vector2Normalize(Vector2Subtract(player_pos, pos));
            float pull = (magnet_radius - dist) * 2.5f + 120.0f;
            pos.x += dir.x * pull * dt;
            pos.y += dir.y * pull * dt;
        } else {
            // Gentle drift down
            pos.y += 35.0f * dt;
        }

        if (lifetime >= max_lifetime || pos.y > SCREEN_HEIGHT + 50) {
            active = false;
        }
    }

    void draw() const {
        if (!active) return;

        Color primary = COLOR_GOLD;
        const char* label = "+";
        switch (type) {
            case PowerupType::KAVACH_SHIELD: primary = COLOR_CYAN_BRIGHT; label = "S"; break;
            case PowerupType::AGNEYASTRA_SPREAD: primary = COLOR_RED_BRIGHT; label = "A"; break;
            case PowerupType::VAYAVYASTRA_SPEED: primary = COLOR_GREEN_BRIGHT; label = "V"; break;
            case PowerupType::AMRITA_HEAL: primary = { 80, 240, 180, 255 }; label = "+"; break;
            case PowerupType::BRAHMASTRA_BOMB: primary = COLOR_GOLD_BRIGHT; label = "B"; break;
            case PowerupType::ASTRA_OVERDRIVE: primary = COLOR_PURPLE_BRIGHT; label = "O"; break;
        }

        // Pulsing outer aura and a gentle hover make cubes readable against
        // busy realm backgrounds before the magnet effect begins.
        float pulse = 1.0f + 0.18f * std::sin(lifetime * 6.0f);
        float bob = std::sin(lifetime * 4.0f) * 2.5f;
        float draw_y = pos.y + bob;
        Color aura = primary;
        aura.a = 72;
        DrawCircle(static_cast<int>(pos.x), static_cast<int>(draw_y), radius * pulse * 1.65f, aura);
        DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(draw_y), radius * pulse * 1.9f, ColorAlpha(primary, 0.42f));

        // 3D Isometric Astral Cube effect
        float size = radius * 0.9f;
        float rad = rotation * (3.14159f / 180.0f);
        float cos_r = std::cos(rad) * size;
        float sin_r = std::sin(rad) * size;

        Vector2 top = { pos.x, draw_y - size };
        Vector2 right = { pos.x + cos_r, draw_y + sin_r * 0.5f };
        Vector2 bottom = { pos.x, draw_y + size };
        Vector2 left = { pos.x - cos_r, draw_y - sin_r * 0.5f };
        Vector2 center = { pos.x, draw_y };

        DrawTriangle(top, right, center, primary);
        DrawTriangle(top, center, left, ColorAlpha(primary, 0.7f));
        DrawTriangle(left, center, bottom, ColorAlpha(primary, 0.5f));
        DrawTriangle(center, right, bottom, ColorAlpha(primary, 0.85f));

        DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(draw_y), radius, COLOR_PARCHMENT);
        DrawText(label, static_cast<int>(pos.x - 4), static_cast<int>(draw_y - 6), 12, COLOR_OBSIDIAN);
    }
};

} // namespace Vimana
