#pragma once
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/bullet.hpp"

namespace Vimana {

enum class BossID {
    KUMBHAKARNA,    // Wave 5
    RAVANA,         // Wave 10
    MAHISHASURA,    // Wave 15
    INDRAJIT,       // Wave 25 (NEW)
    HIRANYAKASHIPU  // Wave 30 (NEW)
};

struct Boss {
    bool active = false;
    BossID id = BossID::KUMBHAKARNA;
    std::string name = "TITAN KUMBHAKARNA";
    std::string title = "The Slumbering Mountain";
    Vector2 pos = { SCREEN_WIDTH / 2.0f, -80.0f };
    float target_y = 130.0f;
    float radius = 55.0f;
    int hp = 1500;
    int max_hp = 1500;
    float speed = 70.0f;
    int phase = 1;
    float hit_flash = 0.0f;
    float attack_timer = 2.0f;
    float special_timer = 5.0f;
    float move_timer = 0.0f;
    int move_dir = 1;
    bool is_invincible = false;
    float invincibility_timer = 0.0f;
    std::string attack_name = "SEISMIC SHOCKWAVE";
    bool is_telegraphing = false;
    float telegraph_timer = 0.0f;
    Vector2 telegraph_target = { 0, 0 };
    std::string telegraph_warning = "";
    std::string sprite_key = "boss_kumbhakarna.png";
    Color theme_color = COLOR_ORANGE_BRIGHT;

    void init(BossID boss_type) {
        active = true;
        id = boss_type;
        pos = { SCREEN_WIDTH / 2.0f, -80.0f };
        target_y = 120.0f;
        hit_flash = 0.0f;
        phase = 1;
        is_invincible = false;
        invincibility_timer = 0.0f;

        switch (id) {
            case BossID::KUMBHAKARNA:
                name = "TITAN KUMBHAKARNA";
                title = "The Slumbering Colossus";
                max_hp = 1800;
                radius = 56.0f;
                speed = 60.0f;
                attack_name = "SEISMIC STOMP";
                sprite_key = "boss_kumbhakarna.png";
                theme_color = COLOR_ORANGE_BRIGHT;
                break;

            case BossID::RAVANA:
                name = "EMPEROR RAVANA";
                title = "Lord of the Ten Realms";
                max_hp = 3200;
                radius = 62.0f;
                speed = 75.0f;
                attack_name = "VOID SPIRAL";
                sprite_key = "boss_ravana.png";
                theme_color = COLOR_RED_BRIGHT;
                break;

            case BossID::MAHISHASURA:
                name = "WARLORD MAHISHASURA";
                title = "The Unyielding Buffalo King";
                max_hp = 2600;
                radius = 58.0f;
                speed = 95.0f;
                attack_name = "BRUTAL GORE CHARGE";
                sprite_key = "boss_mahishasura.png";
                theme_color = { 240, 100, 50, 255 };
                break;

            case BossID::INDRAJIT:
                name = "CONQUEROR INDRAJIT";
                title = "Master of Illusions & Celestial Astras";
                max_hp = 3500;
                radius = 50.0f;
                speed = 120.0f;
                attack_name = "MIRAGE CLOAK & SERPENT ARROW";
                sprite_key = "boss_indrajit.png";
                theme_color = COLOR_PURPLE_BRIGHT;
                break;

            case BossID::HIRANYAKASHIPU:
                name = "TYRANT HIRANYAKASHIPU";
                title = "Immortal Demon Sovereign";
                max_hp = 4500;
                radius = 65.0f;
                speed = 85.0f;
                attack_name = "WRATH OF THE TYRANT";
                sprite_key = "boss_hiranyakashipu.png";
                theme_color = COLOR_GOLD_BRIGHT;
                break;
        }
        hp = max_hp;
        attack_timer = 2.0f;
        special_timer = 6.0f;
    }

    void update(float dt, Vector2 player_pos, std::vector<Bullet>& out_bullets) {
        if (!active) return;
        if (hit_flash > 0) hit_flash -= dt;

        // Entrance slide down
        if (pos.y < target_y) {
            pos.y += 120.0f * dt;
            return;
        }

        // Phase update
        float hp_ratio = static_cast<float>(hp) / max_hp;
        if (hp_ratio < 0.35f && phase < 3) {
            phase = 3;
            speed *= 1.35f;
        } else if (hp_ratio < 0.70f && phase < 2) {
            phase = 2;
            speed *= 1.2f;
        }

        // Horizontal sway
        move_timer += dt;
        pos.x += move_dir * speed * dt;
        if (pos.x < radius + 40.0f) {
            pos.x = radius + 40.0f;
            move_dir = 1;
        } else if (pos.x > SCREEN_WIDTH - radius - 40.0f) {
            pos.x = SCREEN_WIDTH - radius - 40.0f;
            move_dir = -1;
        }

        // Invincibility handling (Hiranyakashipu / Indrajit cloak)
        if (is_invincible) {
            invincibility_timer -= dt;
            if (invincibility_timer <= 0) {
                is_invincible = false;
            }
        }

        // Attack patterns
        attack_timer -= dt;
        special_timer -= dt;

        if (special_timer <= 1.2f && special_timer > 0.0f) {
            is_telegraphing = true;
            telegraph_timer = special_timer;
            telegraph_target = player_pos;
            telegraph_warning = attack_name;
        } else {
            is_telegraphing = false;
        }

        if (attack_timer <= 0) {
            execute_basic_attack(out_bullets, player_pos);
        }

        if (special_timer <= 0) {
            execute_special_attack(out_bullets, player_pos);
        }
    }

    void execute_basic_attack(std::vector<Bullet>& out_bullets, Vector2 player_pos) {
        attack_timer = (phase == 3) ? 1.1f : (phase == 2 ? 1.6f : 2.2f);
        Vector2 to_p = Vector2Normalize(Vector2Subtract(player_pos, pos));
        float base_ang = std::atan2(to_p.y, to_p.x) * (180.0f / 3.14159f);

        if (id == BossID::RAVANA) {
            // Spiral void ring
            int count = (phase == 3) ? 14 : 10;
            for (int i = 0; i < count; ++i) {
                float ang = (i * (360.0f / count) + GetTime() * 40.0f) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.is_enemy = true;
                b.pos = pos;
                b.vel = { std::cos(ang) * ENEMY_BULLET_SPEED * 0.9f, std::sin(ang) * ENEMY_BULLET_SPEED * 0.9f };
                b.damage = 18;
                b.color = COLOR_RED_BRIGHT;
                b.radius = 6.0f;
                out_bullets.push_back(b);
            }
        } else if (id == BossID::HIRANYAKASHIPU) {
            // Pillar Barrage
            int count = 7;
            for (int i = -3; i <= 3; ++i) {
                float ang = (base_ang + i * 16.0f) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.is_enemy = true;
                b.pos = pos;
                b.vel = { std::cos(ang) * ENEMY_BULLET_SPEED * 1.1f, std::sin(ang) * ENEMY_BULLET_SPEED * 1.1f };
                b.damage = 22;
                b.color = COLOR_GOLD_BRIGHT;
                b.radius = 7.0f;
                out_bullets.push_back(b);
            }
        } else {
            // Standard multi-arc
            for (int off : { -24, -8, 8, 24 }) {
                float ang = (base_ang + off) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.is_enemy = true;
                b.pos = pos;
                b.vel = { std::cos(ang) * ENEMY_BULLET_SPEED, std::sin(ang) * ENEMY_BULLET_SPEED };
                b.damage = 16;
                b.color = theme_color;
                out_bullets.push_back(b);
            }
        }
    }

    void execute_special_attack(std::vector<Bullet>& out_bullets, Vector2 player_pos) {
        special_timer = (phase == 3) ? 4.5f : 6.5f;

        if (id == BossID::HIRANYAKASHIPU) {
            // Phase 3 Invulnerability + Void Rift
            if (phase == 3) {
                is_invincible = true;
                invincibility_timer = 2.5f;
            }
            // Double burst cross
            for (int i = 0; i < 16; ++i) {
                float ang = (i * 22.5f) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.is_enemy = true;
                b.pos = pos;
                b.vel = { std::cos(ang) * 320.0f, std::sin(ang) * 320.0f };
                b.damage = 25;
                b.color = COLOR_ORANGE_BRIGHT;
                b.radius = 8.0f;
                out_bullets.push_back(b);
            }
        } else if (id == BossID::INDRAJIT) {
            // Mirage Illusion: Teleport and serpent homing arrows
            pos.x = 150.0f + static_cast<float>(std::rand() % (SCREEN_WIDTH - 300));
            for (int i = 0; i < 6; ++i) {
                Vector2 to_p = Vector2Normalize(Vector2Subtract(player_pos, pos));
                float ang = (std::atan2(to_p.y, to_p.x) * (180.0f / 3.14159f) + (i - 2.5f) * 20.0f) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.is_enemy = true;
                b.pos = pos;
                b.vel = { std::cos(ang) * 440.0f, std::sin(ang) * 440.0f };
                b.damage = 22;
                b.color = COLOR_PURPLE_BRIGHT;
                b.radius = 7.0f;
                out_bullets.push_back(b);
            }
        } else {
            // Radial Shockwave
            for (int i = 0; i < 18; ++i) {
                float ang = (i * 20.0f) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.is_enemy = true;
                b.pos = pos;
                b.vel = { std::cos(ang) * 280.0f, std::sin(ang) * 280.0f };
                b.damage = 20;
                b.color = theme_color;
                out_bullets.push_back(b);
            }
        }
    }

    void take_damage(int amount) {
        if (!active || amount <= 0) return;
        if (is_invincible || invincibility_timer > 0.0f) return;
        hp = std::max(0, hp - amount);
        hit_flash = 0.15f;
        if (hp <= 0) {
            active = false;
        }
    }

    void draw(Texture2D tex) const {
        if (!active) return;

        // Invulnerability golden barrier
        if (is_invincible) {
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.35f, COLOR_GOLD_BRIGHT);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.3f, ColorAlpha(COLOR_GOLD, 0.25f));
        }

        // Telegraph laser line to target
        if (is_telegraphing) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 16.0f);
            Color beam_col = ColorAlpha(COLOR_RED_BRIGHT, 0.4f + 0.4f * pulse);
            DrawLineEx(pos, telegraph_target, 2.5f, beam_col);
            DrawCircleLines(static_cast<int>(telegraph_target.x), static_cast<int>(telegraph_target.y), 16.0f * (1.0f + 0.3f * pulse), COLOR_RED_BRIGHT);
            DrawCircle(static_cast<int>(telegraph_target.x), static_cast<int>(telegraph_target.y), 5.0f, COLOR_RED_BRIGHT);
        }

        Color tint = (hit_flash > 0) ? WHITE : COLOR_PARCHMENT;
        if (tex.id > 0) {
            Rectangle src = { 0.0f, 0.0f, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { pos.x, pos.y, radius * 2.3f, radius * 2.3f };
            Vector2 origin = { dest.width / 2.0f, dest.height / 2.0f };
            DrawTexturePro(tex, src, dest, origin, 180.0f, tint);
        } else {
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, theme_color);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, COLOR_GOLD);
        }
    }
};

} // namespace Vimana
