#pragma once
#include <string>
#include <vector>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/ship_archetypes.hpp"
#include "entities/bullet.hpp"

namespace Vimana {

struct Player {
    Vector2 pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT * 0.75f };
    Vector2 vel = { 0, 0 };
    float radius = 20.0f;
    int hp = 100;
    int max_hp = 100;
    float base_speed = 300.0f;
    float current_speed = 300.0f;
    float angle = -90.0f; // Pointing upwards

    // Weapon & Cooldowns
    float shoot_cooldown = 0.15f;
    float shoot_timer = 0.0f;
    int bullet_damage = 25;
    int shot_counter = 0; // For Surya 7th shot pierce

    // Vayu Dash
    int dash_charges = 2;
    int max_dash_charges = 2;
    float dash_cooldown = 1.6f;
    float dash_timer = 0.0f;
    float dash_duration_timer = 0.0f;
    bool is_dashing = false;

    // Defense & Invincibility
    float invincibility_timer = 0.0f;
    bool has_kavach_shield = false;
    float kavach_timer = 0.0f;

    // Chakram & Brahmastra
    float chakram_cooldown = CHAKRAM_COOLDOWN;
    float chakram_timer = 0.0f;
    int brahmastra_bombs = 1;

    // Astral Cube active buff timers
    float buff_agneyastra_timer = 0.0f;
    float buff_speed_timer = 0.0f;
    float buff_overdrive_timer = 0.0f;

    // Archetype & Consumables
    const ShipArchetype* archetype = nullptr;
    ConsumableInventory inventory;
    std::vector<BoonType> boons;

    // Identification
    uint8_t player_id = 0;
    std::string callsign = "Warrior";

    // Statistics for current run
    int score = 0;
    int combo = 1;
    int max_combo = 1;
    float combo_timer = 0.0f;
    int kills = 0;
    int total_damage_dealt = 0;
    long long shots_fired = 0;
    long long shots_hit = 0;
    int downed_count = 0;
    int revives_given = 0;

    // Co-op Downed & Lives System
    bool is_downed = false;
    float downed_timer = 0.0f;
    float self_revive_timer = 0.0f;
    int lives = 3;
    bool is_spectator = false;

    void init(const ShipArchetype* ship_arch) {
        archetype = ship_arch ? ship_arch : &SHIP_FLEET[0];
        radius = 20.0f;
        max_hp = archetype->max_hp;
        hp = max_hp;
        base_speed = archetype->speed;
        current_speed = base_speed;
        bullet_damage = archetype->bullet_damage;
        shoot_cooldown = archetype->shoot_cooldown;
        max_dash_charges = archetype->dash_charges;
        dash_charges = max_dash_charges;
        dash_cooldown = archetype->dash_cooldown;

        pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT * 0.78f };
        vel = { 0, 0 };
        is_dashing = false;
        dash_duration_timer = 0.0f;
        dash_timer = 0.0f;
        invincibility_timer = 0.0f;
        has_kavach_shield = false;
        kavach_timer = 0.0f;
        chakram_timer = 0.0f;
        brahmastra_bombs = 1;
        buff_agneyastra_timer = 0.0f;
        buff_speed_timer = 0.0f;
        buff_overdrive_timer = 0.0f;
        shot_counter = 0;
        score = 0;
        combo = 1;
        combo_timer = 0.0f;
        kills = 0;
        total_damage_dealt = 0;
        shots_fired = 0;
        shots_hit = 0;
        downed_count = 0;
        revives_given = 0;
        is_downed = false;
        downed_timer = 0.0f;
        self_revive_timer = 0.0f;
        lives = 3;
        is_spectator = false;
        boons.clear();
    }

    bool has_boon(BoonType boon) const {
        return std::find(boons.begin(), boons.end(), boon) != boons.end();
    }

    void apply_boon(BoonType boon) {
        boons.push_back(boon);
        if (boon == BoonType::VARUNA_OCEANIC_WARD) {
            max_hp += 30;
            hp = std::min(max_hp, hp + 30);
        } else if (boon == BoonType::VAYU_GALE_TEMPEST) {
            dash_cooldown *= 0.65f;
        } else if (boon == BoonType::SUDARSHANA_KEEN_EDGE) {
            chakram_cooldown *= 0.7f;
        }
    }

    void update(float dt) {
        // Timers
        if (shoot_timer > 0) shoot_timer -= dt;
        if (invincibility_timer > 0) invincibility_timer -= dt;
        if (chakram_timer > 0) chakram_timer -= dt;

        // Buff countdowns
        if (has_kavach_shield) {
            kavach_timer -= dt;
            if (kavach_timer <= 0) has_kavach_shield = false;
        }
        if (buff_agneyastra_timer > 0) buff_agneyastra_timer -= dt;
        if (buff_overdrive_timer > 0) buff_overdrive_timer -= dt;
        if (buff_speed_timer > 0) {
            buff_speed_timer -= dt;
            current_speed = base_speed * 1.4f;
        } else {
            current_speed = base_speed;
        }

        // Kamadhenu & Varuna passive HP regen
        if (archetype && archetype->id == "kamadhenu") {
            hp = std::min(max_hp, hp + static_cast<int>(3.0f * dt));
        }
        if (has_boon(BoonType::VARUNA_OCEANIC_WARD)) {
            hp = std::min(max_hp, hp + static_cast<int>(2.0f * dt));
        }

        // Dash recharge
        if (dash_charges < max_dash_charges) {
            dash_timer += dt;
            if (dash_timer >= dash_cooldown) {
                dash_charges++;
                dash_timer = 0.0f;
            }
        }

        // Dash movement execution
        if (is_dashing) {
            dash_duration_timer -= dt;
            if (dash_duration_timer <= 0) {
                is_dashing = false;
            }
        }

        // Combo decay
        if (combo > 1) {
            combo_timer -= dt;
            if (combo_timer <= 0) {
                combo = 1;
            }
        }

        // Integrate velocity with inertia damping
        pos.x += vel.x * dt;
        pos.y += vel.y * dt;
        if (!is_dashing) {
            vel.x *= 0.85f;
            vel.y *= 0.85f;
        }

        // Clamp inside screen bounds
        pos.x = std::max(radius, std::min(SCREEN_WIDTH - radius, pos.x));
        pos.y = std::max(radius, std::min(SCREEN_HEIGHT - radius, pos.y));
    }

    void handle_input(float dt, Vector2 mouse_pos, std::vector<Bullet>& out_bullets, bool is_p2 = false) {
        Vector2 input_dir = { 0, 0 };

        if (!is_p2) {
            // Player 1: WASD
            if (IsKeyDown(KEY_W)) input_dir.y -= 1.0f;
            if (IsKeyDown(KEY_S)) input_dir.y += 1.0f;
            if (IsKeyDown(KEY_A)) input_dir.x -= 1.0f;
            if (IsKeyDown(KEY_D)) input_dir.x += 1.0f;

            // Aim towards mouse
            angle = Vector2AngleDeg(pos, mouse_pos);

            // Fire
            if (IsMouseButtonDown(MOUSE_BUTTON_LEFT) || IsKeyDown(KEY_SPACE)) {
                try_shoot(out_bullets);
            }

            // Dash
            if (IsKeyPressed(KEY_LEFT_SHIFT) || IsMouseButtonPressed(MOUSE_BUTTON_RIGHT)) {
                try_dash(input_dir);
            }

            // Sudarshana Chakram
            if (IsKeyPressed(KEY_Q) || IsKeyPressed(KEY_E)) {
                try_chakram(out_bullets);
            }

            // Consumables: Soma Vial (C) and Vajra Flare (V)
            if (IsKeyPressed(KEY_C)) {
                use_soma_vial();
            }
            if (IsKeyPressed(KEY_V)) {
                use_vajra_flare(out_bullets);
            }
        } else {
            // Player 2: Arrow keys + Enter + Slash (for Local Duel)
            if (IsKeyDown(KEY_UP)) input_dir.y -= 1.0f;
            if (IsKeyDown(KEY_DOWN)) input_dir.y += 1.0f;
            if (IsKeyDown(KEY_LEFT)) input_dir.x -= 1.0f;
            if (IsKeyDown(KEY_RIGHT)) input_dir.x += 1.0f;

            if (Vector2Length(input_dir) > 0.1f) {
                angle = std::atan2(input_dir.y, input_dir.x) * (180.0f / 3.14159f);
            }

            if (IsKeyDown(KEY_ENTER) || IsKeyDown(KEY_RIGHT_CONTROL)) {
                try_shoot(out_bullets);
            }
            if (IsKeyPressed(KEY_SLASH) || IsKeyPressed(KEY_RIGHT_SHIFT)) {
                try_dash(input_dir);
            }
        }

        input_dir = Vector2Normalize(input_dir);
        float spd = is_dashing ? DASH_SPEED_BURST : current_speed;
        vel.x = input_dir.x * spd;
        vel.y = input_dir.y * spd;
    }

    void try_shoot(std::vector<Bullet>& out_bullets) {
        float cd = (buff_overdrive_timer > 0) ? shoot_cooldown * 0.45f : shoot_cooldown;
        if (shoot_timer > 0) return;
        shoot_timer = cd;
        shot_counter++;

        float rad = angle * (3.14159f / 180.0f);
        Vector2 nose = { pos.x + std::cos(rad) * radius, pos.y + std::sin(rad) * radius };

        // Damage calculation
        int dmg = bullet_damage;
        // Narasimha Archetype trait: low HP scaling
        if (archetype && archetype->id == "narasimha") {
            float missing_hp = 1.0f - (static_cast<float>(hp) / max_hp);
            dmg += static_cast<int>(missing_hp * 25);
        }
        // Narasimha 9th Boon: +40% damage when HP < 35%
        if (has_boon(BoonType::NARASIMHA_BERSERK_MIGHT) && (static_cast<float>(hp) / max_hp) < 0.35f) {
            dmg = static_cast<int>(dmg * 1.4f);
        }

        bool is_pierce = (has_boon(BoonType::SURYA_RADIANT_PIERCE) && (shot_counter % 7 == 0));

        if (buff_agneyastra_timer > 0) {
            // 3-way spread fire
            shots_fired += 3;
            for (int off : { -16, 0, 16 }) {
                float a = (angle + off) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.pos = nose;
                b.vel = { std::cos(a) * PLAYER_BULLET_SPEED, std::sin(a) * PLAYER_BULLET_SPEED };
                b.damage = dmg;
                b.radius = 6.0f;
                b.color = COLOR_RED_BRIGHT;
                b.pierce_remaining = is_pierce ? 3 : 0;
                b.owner_player_id = player_id;
                b.is_player_owned = true;
                out_bullets.push_back(b);
            }
        } else {
            shots_fired += 1;
            Bullet b;
            b.active = true;
            b.pos = nose;
            b.vel = { std::cos(rad) * PLAYER_BULLET_SPEED, std::sin(rad) * PLAYER_BULLET_SPEED };
            b.damage = dmg;
            b.radius = is_pierce ? 8.0f : PLAYER_BULLET_RADIUS;
            b.color = is_pierce ? COLOR_GOLD_BRIGHT : (archetype ? archetype->accent_color : COLOR_GOLD);
            b.pierce_remaining = is_pierce ? 4 : 0;
            b.owner_player_id = player_id;
            b.is_player_owned = true;
            if (archetype && archetype->id == "narasimha") {
                b.type = BulletType::NARASIMHA_CLAW;
            }
            out_bullets.push_back(b);
        }
    }

    void try_dash(Vector2 dir) {
        if (dash_charges <= 0 || is_dashing) return;
        dash_charges--;
        is_dashing = true;
        dash_duration_timer = DASH_DURATION;
        invincibility_timer = DASH_DURATION + 0.1f;
        SoundSystem::instance().play_dash();
        SoundSystem::instance().play_thruster();
    }

    void try_chakram(std::vector<Bullet>& out_bullets) {
        if (chakram_timer > 0) return;
        chakram_timer = chakram_cooldown;
        shots_fired += 1;

        Bullet b;
        b.active = true;
        b.pos = pos;
        float rad = angle * (3.14159f / 180.0f);
        b.vel = { std::cos(rad) * 420.0f, std::sin(rad) * 420.0f };
        b.radius = has_boon(BoonType::SUDARSHANA_KEEN_EDGE) ? 22.0f : 16.0f;
        b.damage = has_boon(BoonType::SUDARSHANA_KEEN_EDGE) ? CHAKRAM_DAMAGE * 2 : CHAKRAM_DAMAGE;
        b.type = BulletType::CHAKRAM;
        b.pierce_remaining = 999;
        b.max_lifetime = 5.0f;
        b.owner_player_id = player_id;
        b.is_player_owned = true;
        out_bullets.push_back(b);
        SoundSystem::instance().play_sfx("online_laser_small.ogg", 0.7f);
    }

    void use_soma_vial() {
        if (inventory.soma_vials > 0) {
            inventory.soma_vials--;
            hp = std::min(max_hp, hp + static_cast<int>(max_hp * 0.45f));
        }
    }

    void use_vajra_flare(std::vector<Bullet>& out_bullets) {
        if (inventory.vajra_flares > 0) {
            inventory.vajra_flares--;
            SoundSystem::instance().play_sfx("online_explosion_crunch.ogg", 0.9f);
            shots_fired += 24;
            // Spawn 24 outward pulse blades
            for (int i = 0; i < 24; ++i) {
                float rad = (i * 15.0f) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.pos = pos;
                b.vel = { std::cos(rad) * 550.0f, std::sin(rad) * 550.0f };
                b.damage = 40;
                b.radius = 7.0f;
                b.color = COLOR_CYAN_BRIGHT;
                b.pierce_remaining = 2;
                b.owner_player_id = player_id;
                b.is_player_owned = true;
                out_bullets.push_back(b);
            }
        }
    }

    void take_damage(int amount) {
        if (invincibility_timer > 0 || is_dashing) return;

        if (has_kavach_shield) {
            has_kavach_shield = false;
            invincibility_timer = 0.5f;
            SoundSystem::instance().play_sfx("online_impact_metal.ogg", 0.8f);
            SoundSystem::instance().play_force_field();
            return;
        }

        // Check consumable Kavach Shield charge for fatal damage negation
        if (hp - amount <= 0 && inventory.kavach_charges > 0) {
            inventory.kavach_charges--;
            hp = static_cast<int>(max_hp * 0.35f);
            has_kavach_shield = true;
            kavach_timer = 3.0f;
            invincibility_timer = 1.0f;
            SoundSystem::instance().play_sfx("synergy.wav", 1.0f);
            return;
        }

        hp -= amount;
        invincibility_timer = PLAYER_INVINCIBILITY_TIME;
        SoundSystem::instance().play_hit();
        if (hp < 0) hp = 0;
    }

    void add_combo() {
        combo = std::min(50, combo + 1);
        combo_timer = 2.8f;
        if (combo > max_combo) max_combo = combo;
    }

    void draw(Texture2D tex) const {
        // Spectator Reticle
        if (is_spectator) {
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), 18.0f, ColorAlpha(COLOR_CYAN_BRIGHT, 0.7f));
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), 4.0f, COLOR_CYAN_BRIGHT);
            DrawText("SPECTATOR CAM [WASD FLY // F PING]", static_cast<int>(pos.x - 90.0f), static_cast<int>(pos.y - 32.0f), 10, COLOR_CYAN_BRIGHT);
            return;
        }

        // Dash trail & i-frames flicker
        if (invincibility_timer > 0 && !is_dashing) {
            if (static_cast<int>(GetTime() * 20) % 2 == 0) return; // Flash
        }

        // Kavach Shield Dome
        if (has_kavach_shield) {
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.5f, COLOR_CYAN_BRIGHT);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.45f, ColorAlpha(COLOR_CYAN, 0.2f));
        }

        Color tint = WHITE;
        if (is_dashing) {
            tint = COLOR_CYAN_BRIGHT;
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.2f, ColorAlpha(COLOR_CYAN, 0.4f));
        }

        if (tex.id > 0) {
            Rectangle src = { 0.0f, 0.0f, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { pos.x, pos.y, radius * 2.2f, radius * 2.2f };
            Vector2 origin = { dest.width / 2.0f, dest.height / 2.0f };
            DrawTexturePro(tex, src, dest, origin, angle + 90.0f, tint);
        } else {
            // Procedural geometric ship
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, archetype ? archetype->accent_color : COLOR_GOLD);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius, COLOR_PARCHMENT);
        }

        // Co-op Downed Beacon
        if (is_downed) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 15.0f + 5.0f * pulse, COLOR_RED_BRIGHT);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 8.0f, ColorAlpha(COLOR_RED_BRIGHT, 0.25f));
            DrawText("⚠ DOWNED [HOLD E TO REVIVE]", static_cast<int>(pos.x - 75.0f), static_cast<int>(pos.y - radius - 20.0f), 10, COLOR_RED_BRIGHT);
            if (self_revive_timer > 0.0f) {
                float pct = std::clamp(self_revive_timer / 30.0f, 0.0f, 1.0f);
                DrawRectangle(static_cast<int>(pos.x - 50.0f), static_cast<int>(pos.y + radius + 10.0f), 100, 8, DARKGRAY);
                DrawRectangle(static_cast<int>(pos.x - 50.0f), static_cast<int>(pos.y + radius + 10.0f), static_cast<int>(100.0f * pct), 8, COLOR_GOLD_BRIGHT);
                DrawText(TextFormat("SELF-REVIVING: %.0f%% [R]", pct * 100.0f), static_cast<int>(pos.x - 55.0f), static_cast<int>(pos.y + radius + 22.0f), 10, COLOR_GOLD_BRIGHT);
            } else {
                DrawText("[HOLD R TO SELF-REVIVE (30s)]", static_cast<int>(pos.x - 70.0f), static_cast<int>(pos.y + radius + 10.0f), 9, COLOR_GOLD);
            }
        }
    }
};

} // namespace Vimana
