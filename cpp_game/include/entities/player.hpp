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
#include "systems/currency_system.hpp"
#include "systems/sound_system.hpp"

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
    float firing_recoil = 0.0f;
    int bullet_damage = 25;
    int shot_counter = 0; // For Surya 7th shot pierce
    int signature_shot_counter = 0; // Per-ship cadence, separate from boon cadence

    // Vayu Dash
    int dash_charges = 2;
    int max_dash_charges = 2;
    float dash_cooldown = 1.6f;
    float dash_distance_multiplier = 1.0f;
    float dash_timer = 0.0f;
    float dash_duration_timer = 0.0f;
    bool is_dashing = false;

    bool just_shot = false;
    bool just_dashed = false;

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
    int ship_upgrade_level = 0;
    ConsumableInventory inventory;
    std::vector<BoonType> boons;

    // Identification
    uint8_t player_id = 0;
    std::string callsign = "Warrior";
    std::string last_damage_source;

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
    float last_stand_timer = 0.0f;
    float regen_bank = 0.0f;
    float kavach_auto_timer = 0.0f;
    int lives = 3;
    bool is_spectator = false;

    void init(const ShipArchetype* ship_arch) {
        archetype = ship_arch ? ship_arch : &SHIP_FLEET[0];
        ship_upgrade_level = CurrencySystem::instance().ship_upgrade_level(archetype->id);
        const float upgrade = static_cast<float>(ship_upgrade_level);
        radius = 20.0f;
        max_hp = static_cast<int>(std::round(archetype->max_hp * (1.0f + 0.05f * upgrade)));
        hp = max_hp;
        base_speed = archetype->speed * (1.0f + 0.015f * upgrade);
        current_speed = base_speed;
        bullet_damage = static_cast<int>(std::round(archetype->bullet_damage * (1.0f + 0.03f * upgrade)));
        shoot_cooldown = std::max(0.055f, archetype->shoot_cooldown * (1.0f - 0.025f * upgrade));
        max_dash_charges = archetype->dash_charges;
        dash_charges = max_dash_charges;
        dash_cooldown = std::max(0.55f, archetype->dash_cooldown * (1.0f - 0.02f * upgrade));
        dash_distance_multiplier = 1.0f;

        pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT * 0.78f };
        vel = { 0, 0 };
        is_dashing = false;
        dash_duration_timer = 0.0f;
        dash_timer = 0.0f;
        firing_recoil = 0.0f;
        invincibility_timer = 0.0f;
        has_kavach_shield = false;
        kavach_timer = 0.0f;
        chakram_timer = 0.0f;
        brahmastra_bombs = 1;
        buff_agneyastra_timer = 0.0f;
        buff_speed_timer = 0.0f;
        buff_overdrive_timer = 0.0f;
        shot_counter = 0;
        signature_shot_counter = 0;
        score = 0;
        last_damage_source.clear();
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
        last_stand_timer = 0.0f;
        regen_bank = 0.0f;
        kavach_auto_timer = 0.0f;
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
        firing_recoil = std::max(0.0f, firing_recoil - dt * 28.0f);
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

        // Kamadhenu & Varuna passive HP regen (float accumulator - int cast per-frame is 0 at 60fps)
        float regen_rate = 0.0f;
        if (archetype && archetype->id == "kamadhenu") {
            regen_rate += 3.0f;
        }
        if (archetype && archetype->id == "dhanvantari") {
            regen_rate += 4.0f;
        }
        if (has_boon(BoonType::VARUNA_OCEANIC_WARD)) {
            regen_rate += 2.0f;
        }
        if (regen_rate > 0.0f && hp < max_hp) {
            regen_bank += regen_rate * dt;
            int whole = static_cast<int>(regen_bank);
            if (whole > 0) {
                hp = std::min(max_hp, hp + whole);
                regen_bank -= static_cast<float>(whole);
            }
        } else {
            regen_bank = 0.0f;
        }

        // Signature defensive passives: Pushpaka's longer ward and Nandi's compact aegis.
        if (archetype && (archetype->id == "pushpaka" || archetype->id == "nandi_aegis" || archetype->id == "soma") && !is_downed) {
            const bool nandi_aegis = archetype->id == "nandi_aegis";
            const bool soma_ark = archetype->id == "soma";
            const float shield_cycle = nandi_aegis ? 10.0f : (soma_ark ? 15.0f : 12.0f);
            if (!has_kavach_shield) {
                kavach_auto_timer += dt;
                if (kavach_auto_timer >= shield_cycle) {
                    kavach_auto_timer = 0.0f;
                    has_kavach_shield = true;
                    kavach_timer = nandi_aegis ? 2.0f : (soma_ark ? 1.5f : 3.0f);
                }
            } else {
                kavach_auto_timer = 0.0f;
            }
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

        // Clamp inside playable fight area (away from top/bottom HUD chrome)
        constexpr float HUD_TOP = 70.0f;
        constexpr float HUD_BOTTOM = 530.0f;
        pos.x = std::max(radius, std::min(SCREEN_WIDTH - radius, pos.x));
        pos.y = std::max(HUD_TOP + radius * 0.5f, std::min(HUD_BOTTOM - radius * 0.5f, pos.y));
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
            if (IsKeyPressed(KEY_Q)) {
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

            if (IsKeyDown(KEY_RIGHT_CONTROL)) {
                try_shoot(out_bullets);
            }
            if (IsKeyPressed(KEY_SLASH) || IsKeyPressed(KEY_RIGHT_SHIFT)) {
                try_dash(input_dir);
            }
            // P2 uses the keypad to avoid overlapping P1's Q/C/V bindings.
            if (IsKeyPressed(KEY_KP_1)) {
                try_chakram(out_bullets);
            }
            if (IsKeyPressed(KEY_KP_2)) {
                use_soma_vial();
            }
            if (IsKeyPressed(KEY_KP_3)) {
                use_vajra_flare(out_bullets);
            }
        }

        input_dir = Vector2Normalize(input_dir);
        float spd = is_dashing ? DASH_SPEED_BURST * dash_distance_multiplier : current_speed;
        vel.x = input_dir.x * spd;
        vel.y = input_dir.y * spd;
    }

    void try_shoot(std::vector<Bullet>& out_bullets) {
        float cd = (buff_overdrive_timer > 0) ? shoot_cooldown * 0.45f : shoot_cooldown;
        if (shoot_timer > 0) return;
        shoot_timer = cd;
        firing_recoil = 5.0f;
        just_shot = true;
        shot_counter = (shot_counter % 7) + 1;
        const bool is_amogha = archetype && archetype->id == "amogha_lancer";
        if (is_amogha) signature_shot_counter = (signature_shot_counter % 5) + 1;

        float rad = angle * (3.14159f / 180.0f);
        Vector2 nose = { pos.x + std::cos(rad) * radius, pos.y + std::sin(rad) * radius };

        // Damage calculation
        int dmg = bullet_damage;
        const bool amogha_needle = is_amogha && signature_shot_counter == 5;
        if (amogha_needle) dmg = static_cast<int>(std::round(dmg * 1.25f));
        // Narasimha Archetype trait: low HP scaling
        if (archetype && archetype->id == "narasimha") {
            float missing_hp = 1.0f - (static_cast<float>(hp) / max_hp);
            dmg += static_cast<int>(missing_hp * 25);
        }
        // Narasimha 9th Boon: +40% damage when HP < 35%
        if (has_boon(BoonType::NARASIMHA_BERSERK_MIGHT) && (static_cast<float>(hp) / max_hp) < 0.35f) {
            dmg = static_cast<int>(dmg * 1.4f);
        }

        const bool surya_flare = archetype && archetype->id == "surya";
        bool is_pierce = ((surya_flare || has_boon(BoonType::SURYA_RADIANT_PIERCE)) && (shot_counter % 7 == 0));
        bool is_tripura = (archetype && archetype->id == "tripura");
        bool is_garuda = (archetype && (archetype->id == "garuda" || archetype->id == "garuda_prime" || archetype->id == "garuda_apex"));
        const int garuda_pierce_bonus = is_garuda ? 2 : 0;

        if (is_tripura && buff_agneyastra_timer <= 0) {
            // Tripura Dreadnought: native 3-shot heavy spread
            shots_fired += 3;
            for (int off : { -12, 0, 12 }) {
                float a = (angle + off) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true;
                b.pos = nose;
                b.vel = { std::cos(a) * PLAYER_BULLET_SPEED * 0.95f, std::sin(a) * PLAYER_BULLET_SPEED * 0.95f };
                b.damage = dmg;
                b.radius = 6.5f;
                b.color = COLOR_ORANGE_BRIGHT;
                b.pierce_remaining = (is_pierce ? 2 : 0) + garuda_pierce_bonus;
                b.owner_player_id = player_id;
                b.is_player_owned = true;
                out_bullets.push_back(b);
            }
        } else if (archetype && archetype->gun_type == "BURST") {
            // Vajra: 4 quick shots in a tight spread
            shots_fired += 4;
            for (int off : { -8, -3, 3, 8 }) {
                float a = (angle + off) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true; b.pos = nose;
                b.vel = { std::cos(a) * PLAYER_BULLET_SPEED * 1.05f, std::sin(a) * PLAYER_BULLET_SPEED * 1.05f };
                b.damage = dmg; b.radius = 4.0f;
                b.color = COLOR_CYAN_BRIGHT;
                b.pierce_remaining = (is_pierce ? 2 : 0) + garuda_pierce_bonus;
                b.owner_player_id = player_id; b.is_player_owned = true;
                out_bullets.push_back(b);
            }
        } else if (archetype && archetype->gun_type == "PIERCE") {
            // Naga: penetrating single shot with extra range
            shots_fired += 1;
            Bullet b;
            b.active = true; b.pos = nose;
            b.vel = { std::cos(rad) * PLAYER_BULLET_SPEED * 1.15f, std::sin(rad) * PLAYER_BULLET_SPEED * 1.15f };
            b.damage = dmg; b.radius = 7.0f;
            b.color = COLOR_GREEN_BRIGHT;
            b.pierce_remaining = (amogha_needle ? 8 : (is_pierce ? 4 : 3)) + garuda_pierce_bonus;
            b.owner_player_id = player_id; b.is_player_owned = true;
            out_bullets.push_back(b);
        } else if (archetype && archetype->gun_type == "BURN") {
            // Agneyastra: 2 fire shots with wider spread
            shots_fired += 2;
            for (int off : { -10, 10 }) {
                float a = (angle + off) * (3.14159f / 180.0f);
                Bullet b;
                b.active = true; b.pos = nose;
                b.vel = { std::cos(a) * PLAYER_BULLET_SPEED * 0.9f, std::sin(a) * PLAYER_BULLET_SPEED * 0.9f };
                b.damage = dmg; b.radius = 5.5f;
                b.color = COLOR_RED_BRIGHT;
                b.pierce_remaining = (is_pierce ? 2 : 0) + garuda_pierce_bonus;
                b.owner_player_id = player_id; b.is_player_owned = true;
                out_bullets.push_back(b);
            }
        } else {
            if (buff_agneyastra_timer > 0) {
                shots_fired += 3;
                for (int off : { -16, 0, 16 }) {
                    const float a = (angle + off) * (3.14159f / 180.0f);
                    Bullet b;
                    b.active = true;
                    b.pos = nose;
                    b.vel = { std::cos(a) * PLAYER_BULLET_SPEED, std::sin(a) * PLAYER_BULLET_SPEED };
                    b.damage = dmg;
                    b.radius = 6.0f;
                    b.color = COLOR_RED_BRIGHT;
                    b.pierce_remaining = (is_pierce ? 3 : 0) + garuda_pierce_bonus;
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
                b.pierce_remaining = (is_pierce ? 4 : 0) + garuda_pierce_bonus;
                b.owner_player_id = player_id;
                b.is_player_owned = true;
                if (archetype && archetype->id == "narasimha") b.type = BulletType::NARASIMHA_CLAW;
                out_bullets.push_back(b);
            }
        }
        SoundSystem::instance().play_sfx("shoot.wav", 0.3f);
    }

    void try_dash(Vector2 dir) {
        if (dash_charges <= 0 || is_dashing) return;
        dash_charges--;
        is_dashing = true;
        just_dashed = true;
        dash_duration_timer = DASH_DURATION;
        invincibility_timer = DASH_DURATION + 0.1f;
        if (archetype && archetype->id == "varaha") {
            has_kavach_shield = true;
            kavach_timer = std::max(kavach_timer, 0.65f);
        }
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

    bool take_damage(int amount, const char* damage_source = "Unknown hostile") {
        if (amount <= 0 || invincibility_timer > 0 || is_dashing || is_downed) return false;

        if (has_kavach_shield) {
            has_kavach_shield = false;
            invincibility_timer = 0.5f;
            SoundSystem::instance().play_sfx("online_impact_metal.ogg", 0.8f);
            SoundSystem::instance().play_force_field();
            return true;
        }

        // Check consumable Kavach Shield charge for fatal damage negation
        if (hp - amount <= 0 && inventory.kavach_charges > 0) {
            inventory.kavach_charges--;
            hp = static_cast<int>(max_hp * 0.35f);
            has_kavach_shield = true;
            kavach_timer = 3.0f;
            invincibility_timer = 1.0f;
            SoundSystem::instance().play_sfx("synergy.wav", 1.0f);
            return true;
        }

        last_damage_source = (damage_source && damage_source[0]) ? damage_source : "Unknown hostile";
        hp -= amount;
        invincibility_timer = PLAYER_INVINCIBILITY_TIME;
        SoundSystem::instance().play_hit();
        if (hp < 0) hp = 0;
        return true;
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
        if (!g_reduce_flashes && invincibility_timer > 0 && !is_dashing) {
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
        const bool mastery_skin = archetype && CurrencySystem::instance().is_ship_mastered(archetype->id);
        if (mastery_skin) {
            if (!is_dashing) tint = COLOR_GOLD_BRIGHT;
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius * 1.35f,
                            ColorAlpha(COLOR_GOLD_BRIGHT, 0.75f));
        }

        const float aim_rad = angle * (3.14159f / 180.0f);
        const Vector2 sprite_pos = { pos.x - std::cos(aim_rad) * firing_recoil,
                                     pos.y - std::sin(aim_rad) * firing_recoil };
        if (tex.id > 0) {
            Rectangle src = { 0.0f, 0.0f, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { sprite_pos.x, sprite_pos.y, radius * 2.2f, radius * 2.2f };
            Vector2 origin = { dest.width / 2.0f, dest.height / 2.0f };
            DrawTexturePro(tex, src, dest, origin, angle + 90.0f, tint);
        } else {
            // Procedural geometric ship
            DrawCircle(static_cast<int>(sprite_pos.x), static_cast<int>(sprite_pos.y), radius, archetype ? archetype->accent_color : COLOR_GOLD);
            DrawCircleLines(static_cast<int>(sprite_pos.x), static_cast<int>(sprite_pos.y), radius, COLOR_PARCHMENT);
        }

        // Co-op Downed Beacon
        if (is_downed) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 15.0f + 5.0f * pulse, COLOR_RED_BRIGHT);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 8.0f, ColorAlpha(COLOR_RED_BRIGHT, 0.25f));
            DrawText("⚠ DOWNED [HOLD E TO REVIVE]", static_cast<int>(pos.x - 75.0f), static_cast<int>(pos.y - radius - 20.0f), 10, COLOR_RED_BRIGHT);
            if (self_revive_timer > 0.0f) {
                float pct = std::clamp(self_revive_timer / REVIVE_TIME, 0.0f, 1.0f);
                DrawRectangle(static_cast<int>(pos.x - 50.0f), static_cast<int>(pos.y + radius + 10.0f), 100, 8, DARKGRAY);
                DrawRectangle(static_cast<int>(pos.x - 50.0f), static_cast<int>(pos.y + radius + 10.0f), static_cast<int>(100.0f * pct), 8, COLOR_GOLD_BRIGHT);
                DrawText(TextFormat("SELF-REVIVING: %.0f%% [E]", pct * 100.0f), static_cast<int>(pos.x - 55.0f), static_cast<int>(pos.y + radius + 22.0f), 10, COLOR_GOLD_BRIGHT);
            } else {
                const char* self_revive_hint = inventory.soma_vials > 0
                    ? "[HOLD E + SOMA TO REVIVE (3.5s)]"
                    : "[NO SOMA // WAIT FOR A REVIVE]";
                DrawText(self_revive_hint, static_cast<int>(pos.x - 92.0f), static_cast<int>(pos.y + radius + 10.0f), 9,
                         inventory.soma_vials > 0 ? COLOR_GOLD : COLOR_MUTED);
            }
        }
    }
};

} // namespace Vimana
