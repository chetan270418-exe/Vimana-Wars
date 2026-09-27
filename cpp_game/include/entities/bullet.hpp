#pragma once
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

struct Bullet {
    bool active = false;
    Vector2 pos = { 0, 0 };
    Vector2 vel = { 0, 0 };
    float radius = 5.0f;
    int damage = 25;
    bool is_enemy = false;
    const char* damage_source = "Unknown hostile";
    uint8_t owner_player_id = 0;
    bool is_player_owned = true;
    bool grazed = false;
    BulletType type = BulletType::PLAYER_BASIC;
    int pierce_remaining = 0;
    float lifetime = 0.0f;
    float max_lifetime = 3.5f;
    float rotation = 0.0f;
    Color color = COLOR_GOLD_BRIGHT;

    void update(float dt) {
        if (!active) return;
        pos.x += vel.x * dt;
        pos.y += vel.y * dt;
        lifetime += dt;
        rotation += 450.0f * dt;

        if (lifetime >= max_lifetime || pos.x < -40 || pos.x > SCREEN_WIDTH + 40 ||
            pos.y < -40 || pos.y > SCREEN_HEIGHT + 40) {
            active = false;
        }
    }

    void draw() const {
        if (!active) return;
        const bool hostile = is_enemy || !is_player_owned;
        const Color shot_color = accessible_projectile_color(color, hostile);
        if (g_colorblind_mode) {
            // Shape plus luminance contrast avoids relying on red/green alone.
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 2.0f, WHITE);
            if (hostile) {
                DrawPoly(pos, 4, radius * 1.5f, 45.0f, shot_color);
                DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 0.35f, WHITE);
            } else {
                DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, shot_color);
                DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 0.35f, WHITE);
            }
            return;
        }
        if (type == BulletType::CHAKRAM) {
            // Draw rotating spinning blade chakram
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, COLOR_GOLD_BRIGHT);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 0.6f, COLOR_CYAN_BRIGHT);
            // 4 rotating blades
            for (int i = 0; i < 4; ++i) {
                float angle = (rotation + i * 90.0f) * (3.14159f / 180.0f);
                Vector2 tip = { pos.x + std::cos(angle) * (radius + 4.0f), pos.y + std::sin(angle) * (radius + 4.0f) };
                DrawLineEx(pos, tip, 2.5f, COLOR_GOLD);
            }
        } else if (type == BulletType::NARASIMHA_CLAW) {
            // Golden slash wave
            DrawCircleGradient(pos, radius * 1.5f, Color{ 255, 120, 30, 240 }, Color{ 255, 60, 0, 0 });
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, Color{ 255, 230, 150, 255 });
        } else if (type == BulletType::CARRIER_SPAWN_SIGNAL) {
            // Signal beacon handled immediately by game_view, do not draw
            return;
        } else if (type == BulletType::ENEMY_PROXIMITY_MINE) {
            // Proximity mine: pulsating spikes, warning beep glow ring
            float pulse = 0.5f + 0.5f * std::sin(lifetime * 8.0f);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * (1.3f + 0.4f * pulse), ColorAlpha(COLOR_RED_BRIGHT, 0.7f * pulse));
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, COLOR_ORANGE_BRIGHT);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 0.5f, COLOR_RED_BRIGHT);
            for (int i = 0; i < 4; ++i) {
                float a = (rotation + i * 90.0f) * (3.14159f / 180.0f);
                Vector2 spk = { pos.x + std::cos(a) * (radius + 3.0f), pos.y + std::sin(a) * (radius + 3.0f) };
                DrawLineEx(pos, spk, 2.0f, COLOR_GOLD_BRIGHT);
            }
        } else {
            // Basic & Spread laser slug
            Color glow = shot_color;
            glow.a = 70;
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.8f, glow);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, shot_color);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 0.4f, WHITE);
        }
    }
};

} // namespace Vimana
