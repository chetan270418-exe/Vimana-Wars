#pragma once
#include <string>
#include <vector>
#include <cmath>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/bullet.hpp"

namespace Vimana {

enum class EnemyType {
    ASURA_CHASER,
    ASURA_TANK,
    ASURA_SHOOTER,
    ASURA_KAMIKAZE,
    ASURA_HEALER,
    ASURA_SNIPER
};

struct Enemy {
    bool active = false;
    EnemyType type = EnemyType::ASURA_CHASER;
    Vector2 pos = { 0, 0 };
    Vector2 vel = { 0, 0 };
    float radius = 16.0f;
    int hp = 30;
    int max_hp = 30;
    float speed = 180.0f;
    int score_value = 100;
    float shoot_timer = 1.5f;
    float shoot_interval = 2.0f;
    float hit_flash = 0.0f;
    float angle = 0.0f;
    std::string sprite_key = "asura_fast.png";

    // Type specific mechanics
    float special_timer = 0.0f;
    bool is_charging = false;

    void init(EnemyType t, Vector2 spawn_pos, float speed_mult = 1.0f, float hp_mult = 1.0f) {
        active = true;
        type = t;
        pos = spawn_pos;
        hit_flash = 0.0f;
        is_charging = false;
        special_timer = 0.0f;

        switch (type) {
            case EnemyType::ASURA_CHASER:
                radius = 16.0f;
                max_hp = static_cast<int>(30 * hp_mult);
                speed = 210.0f * speed_mult;
                score_value = 100;
                shoot_interval = 999.0f; // Pure melee chaser
                sprite_key = "asura_fast.png";
                break;
            case EnemyType::ASURA_TANK:
                radius = 28.0f;
                max_hp = static_cast<int>(150 * hp_mult);
                speed = 80.0f * speed_mult;
                score_value = 300;
                shoot_interval = 3.0f;
                sprite_key = "asura_tank.png";
                break;
            case EnemyType::ASURA_SHOOTER:
                radius = 20.0f;
                max_hp = static_cast<int>(60 * hp_mult);
                speed = 130.0f * speed_mult;
                score_value = 200;
                shoot_interval = 2.2f;
                sprite_key = "asura_ranged.png";
                break;
            case EnemyType::ASURA_KAMIKAZE:
                radius = 18.0f;
                max_hp = static_cast<int>(40 * hp_mult);
                speed = 240.0f * speed_mult;
                score_value = 180;
                shoot_interval = 999.0f;
                sprite_key = "asura_kamikaze.png";
                break;
            case EnemyType::ASURA_HEALER:
                radius = 22.0f;
                max_hp = static_cast<int>(80 * hp_mult);
                speed = 100.0f * speed_mult;
                score_value = 250;
                shoot_interval = 4.0f; // Healing pulse timer
                sprite_key = "asura_healer.png";
                break;
            case EnemyType::ASURA_SNIPER:
                radius = 20.0f;
                max_hp = static_cast<int>(50 * hp_mult);
                speed = 90.0f * speed_mult;
                score_value = 280;
                shoot_interval = 3.5f;
                sprite_key = "asura_sniper.png";
                break;
        }
        hp = max_hp;
        shoot_timer = ((std::rand() % 100) / 100.0f) * shoot_interval;
    }

    void update(float dt, Vector2 player_pos, std::vector<Bullet>& out_bullets, std::vector<Enemy>& all_enemies) {
        if (!active) return;
        if (hit_flash > 0) hit_flash -= dt;

        Vector2 to_player = Vector2Subtract(player_pos, pos);
        float dist = Vector2Length(to_player);
        Vector2 dir = Vector2Normalize(to_player);
        angle = Vector2AngleDeg(pos, player_pos);

        // AI Behaviors
        switch (type) {
            case EnemyType::ASURA_CHASER:
                pos.x += dir.x * speed * dt;
                pos.y += dir.y * speed * dt;
                break;

            case EnemyType::ASURA_TANK:
                // Slow relentless march toward player
                pos.x += dir.x * speed * dt;
                pos.y += dir.y * speed * dt;
                shoot_timer -= dt;
                if (shoot_timer <= 0) {
                    shoot_timer = shoot_interval;
                    // Fire 3-spread shot
                    for (int offset : { -20, 0, 20 }) {
                        float rad = (angle + offset) * (3.14159f / 180.0f);
                        Bullet b;
                        b.active = true;
                        b.is_enemy = true;
                        b.pos = pos;
                        b.vel = { std::cos(rad) * ENEMY_BULLET_SPEED, std::sin(rad) * ENEMY_BULLET_SPEED };
                        b.damage = 14;
                        b.radius = 6.0f;
                        b.color = COLOR_ORANGE_BRIGHT;
                        out_bullets.push_back(b);
                    }
                }
                break;

            case EnemyType::ASURA_SHOOTER:
                // Strafe at medium range
                if (dist > 280.0f) {
                    pos.x += dir.x * speed * dt;
                    pos.y += dir.y * speed * dt;
                } else if (dist < 180.0f) {
                    pos.x -= dir.x * speed * 0.8f * dt;
                    pos.y -= dir.y * speed * 0.8f * dt;
                } else {
                    // Strafe tangentially
                    pos.x += -dir.y * speed * dt;
                    pos.y += dir.x * speed * dt;
                }
                shoot_timer -= dt;
                if (shoot_timer <= 0) {
                    shoot_timer = shoot_interval;
                    Bullet b;
                    b.active = true;
                    b.is_enemy = true;
                    b.pos = pos;
                    b.vel = Vector2Scale(dir, ENEMY_BULLET_SPEED * 1.1f);
                    b.damage = 12;
                    b.color = COLOR_RED_BRIGHT;
                    out_bullets.push_back(b);
                }
                break;

            case EnemyType::ASURA_KAMIKAZE:
                // Charge aggressively
                pos.x += dir.x * speed * 1.3f * dt;
                pos.y += dir.y * speed * 1.3f * dt;
                break;

            case EnemyType::ASURA_HEALER:
                // Follow allies and emit healing wave
                pos.y += speed * 0.4f * dt;
                shoot_timer -= dt;
                if (shoot_timer <= 0) {
                    shoot_timer = shoot_interval;
                    for (auto& ally : all_enemies) {
                        if (ally.active && Vector2Distance(pos, ally.pos) < 180.0f) {
                            ally.hp = std::min(ally.max_hp, ally.hp + 25);
                            ally.hit_flash = 0.2f;
                        }
                    }
                }
                break;

            case EnemyType::ASURA_SNIPER:
                // Keep far distance and telegraph sniper beam
                if (dist < 350.0f) {
                    pos.x -= dir.x * speed * dt;
                    pos.y -= dir.y * speed * dt;
                }
                shoot_timer -= dt;
                if (shoot_timer <= 0.8f) {
                    is_charging = true;
                }
                if (shoot_timer <= 0) {
                    shoot_timer = shoot_interval;
                    is_charging = false;
                    Bullet b;
                    b.active = true;
                    b.is_enemy = true;
                    b.pos = pos;
                    b.vel = Vector2Scale(dir, ENEMY_BULLET_SPEED * 2.2f);
                    b.damage = 30;
                    b.radius = 7.0f;
                    b.type = BulletType::ENEMY_SNIPER_BEAM;
                    b.color = COLOR_CYAN_BRIGHT;
                    out_bullets.push_back(b);
                }
                break;
        }

        // Clamp inside screen bounds
        pos.x = std::max(radius, std::min(SCREEN_WIDTH - radius, pos.x));
        pos.y = std::max(radius, std::min(SCREEN_HEIGHT - radius, pos.y));
    }

    void draw(Texture2D tex) const {
        if (!active) return;

        // Sniper telegraph laser
        if (type == EnemyType::ASURA_SNIPER && is_charging) {
            float rad = angle * (3.14159f / 180.0f);
            Vector2 aim_end = { pos.x + std::cos(rad) * 600.0f, pos.y + std::sin(rad) * 600.0f };
            DrawLineEx(pos, aim_end, 1.5f, ColorAlpha(COLOR_RED_BRIGHT, 0.45f));
        }

        Color tint = (hit_flash > 0) ? WHITE : COLOR_PARCHMENT;
        if (type == EnemyType::ASURA_KAMIKAZE) {
            // Pulsing red kamikaze
            tint = ColorAlpha(COLOR_RED_BRIGHT, 0.85f + 0.15f * std::sin(GetTime() * 16.0f));
        }

        if (tex.id > 0) {
            Rectangle src = { 0.0f, 0.0f, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { pos.x, pos.y, radius * 2.2f, radius * 2.2f };
            Vector2 origin = { dest.width / 2.0f, dest.height / 2.0f };
            DrawTexturePro(tex, src, dest, origin, angle + 90.0f, tint);
        } else {
            // Procedural geometric fallback
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, tint);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, COLOR_RED_BRIGHT);
        }

        // Mini HP Bar for Tanks & Healers
        if (hp < max_hp) {
            float bar_w = radius * 2.0f;
            float bar_h = 3.0f;
            float hp_ratio = static_cast<float>(hp) / max_hp;
            DrawRectangle(static_cast<int>(pos.x - bar_w / 2), static_cast<int>(pos.y - radius - 8), static_cast<int>(bar_w), static_cast<int>(bar_h), { 30, 30, 30, 200 });
            DrawRectangle(static_cast<int>(pos.x - bar_w / 2), static_cast<int>(pos.y - radius - 8), static_cast<int>(bar_w * hp_ratio), static_cast<int>(bar_h), COLOR_RED_BRIGHT);
        }
    }
};

} // namespace Vimana
