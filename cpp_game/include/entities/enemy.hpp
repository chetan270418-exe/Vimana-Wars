#pragma once
#include <string>
#include <vector>
#include <cmath>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/bullet.hpp"

namespace Vimana {

// ── Elite Affixes (§2 spec) ───────────────────────────────────────────────
enum class EliteAffix : uint8_t {
    NONE       = 0,
    REFLECTIVE = 1 << 0,  // 30% damage returned to attacker
    SWIFT      = 1 << 1,  // speed ×1.5
    REGEN      = 1 << 2,  // 2% HP/s regeneration
    VOLATILE   = 1 << 3   // explodes on death (handled in game_view)
};
inline EliteAffix operator|(EliteAffix a, EliteAffix b) {
    return static_cast<EliteAffix>(static_cast<uint8_t>(a) | static_cast<uint8_t>(b));
}
inline bool has_affix(EliteAffix flags, EliteAffix bit) {
    return (static_cast<uint8_t>(flags) & static_cast<uint8_t>(bit)) != 0;
}

enum class EnemyType {
    ASURA_CHASER,
    ASURA_TANK,
    ASURA_SHOOTER,
    ASURA_KAMIKAZE,
    ASURA_HEALER,
    ASURA_SNIPER,
    ASURA_MINELAYER,   // drops proximity mines
    ASURA_CARRIER      // launches Chaser squads every 8s
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
    bool is_elite = false;
    bool is_miniboss = false;
    std::string miniboss_name;
    Color elite_tint = COLOR_GOLD_BRIGHT;

    // Elite affixes (per §2 spec — randomly assigned 1-2 per elite)
    EliteAffix affixes = EliteAffix::NONE;
    float regen_timer = 0.0f;          // REGEN: accumulates HP/s
    bool volatile_exploded = false;    // VOLATILE: death explosion guard
    std::string affix_label;           // display string e.g. "[SWIFT+REGEN]"

    // Minelayer / Carrier state
    float mine_timer = 0.0f;
    float launch_timer = 0.0f;
    int mines_placed = 0;

    const char* damage_source_name() const {
        if (is_miniboss) {
            if (miniboss_name == "RIFT MAULER") return "Rift Mauler";
            if (miniboss_name == "SILENCE WARDEN") return "Silence Warden";
            if (miniboss_name == "EMBER TYRANT") return "Ember Tyrant";
        }
        switch (type) {
            case EnemyType::ASURA_CHASER:     return "Asura Chaser";
            case EnemyType::ASURA_TANK:       return "Asura Tank";
            case EnemyType::ASURA_SHOOTER:    return "Asura Shooter";
            case EnemyType::ASURA_KAMIKAZE:   return "Asura Kamikaze";
            case EnemyType::ASURA_HEALER:     return "Asura Healer";
            case EnemyType::ASURA_SNIPER:     return "Asura Sniper";
            case EnemyType::ASURA_MINELAYER:  return "Asura Minelayer";
            case EnemyType::ASURA_CARRIER:    return "Asura Carrier";
            default: return "Asura hostile";
        }
    }

    // Assign random 1-2 affixes to an elite enemy
    void assign_affixes() {
        if (!is_elite || is_miniboss) return;
        // Use position as simple seed for variety
        int seed = static_cast<int>(pos.x * 7 + pos.y * 13);
        static const EliteAffix pool[4] = {
            EliteAffix::REFLECTIVE, EliteAffix::SWIFT,
            EliteAffix::REGEN,      EliteAffix::VOLATILE
        };
        int a1 = ((seed >> 2) & 3);
        int a2 = ((seed ^ (seed >> 5)) & 3);
        affixes = pool[a1];
        if (a2 != a1) affixes = affixes | pool[a2]; // 50% chance of 2nd affix
        // Apply SWIFT immediately
        if (has_affix(affixes, EliteAffix::SWIFT)) speed *= 1.5f;
        // Build label string
        affix_label = "[";
        if (has_affix(affixes, EliteAffix::REFLECTIVE)) affix_label += "REF+";
        if (has_affix(affixes, EliteAffix::SWIFT))      affix_label += "SWF+";
        if (has_affix(affixes, EliteAffix::REGEN))      affix_label += "REG+";
        if (has_affix(affixes, EliteAffix::VOLATILE))   affix_label += "VOL+";
        if (affix_label.back() == '+') affix_label.pop_back();
        affix_label += "]";
        // Tint elite by affix combo
        if (has_affix(affixes, EliteAffix::REFLECTIVE)) elite_tint = { 200, 200, 255, 255 };
        else if (has_affix(affixes, EliteAffix::REGEN)) elite_tint = { 80, 255, 130, 255 };
        else if (has_affix(affixes, EliteAffix::VOLATILE)) elite_tint = { 255, 120, 50, 255 };
        else elite_tint = COLOR_GOLD_BRIGHT;
    }

    void init(EnemyType t, Vector2 spawn_pos, float speed_mult = 1.0f, float hp_mult = 1.0f,
              bool elite = false, bool miniboss = false) {
        active = true;
        type = t;
        pos = spawn_pos;
        hit_flash = 0.0f;
        is_charging = false;
        special_timer = 0.0f;
        mine_timer = 0.0f;
        launch_timer = 0.0f;
        mines_placed = 0;
        regen_timer = 0.0f;
        volatile_exploded = false;
        affixes = EliteAffix::NONE;
        affix_label.clear();
        is_elite = elite;
        is_miniboss = miniboss;
        miniboss_name.clear();
        elite_tint = COLOR_GOLD_BRIGHT;
        if (is_elite) {
            hp_mult *= ELITE_HP_MULT;
            speed_mult *= ELITE_SPEED_MULT;
        }


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
            case EnemyType::ASURA_MINELAYER:
                radius = 18.0f;
                max_hp = static_cast<int>(55 * hp_mult);
                speed = 110.0f * speed_mult;
                score_value = 220;
                shoot_interval = 4.5f;  // mine-drop timer
                mine_timer = 2.0f;      // first mine after 2s
                sprite_key = "asura_ranged.png";  // reuse art
                break;
            case EnemyType::ASURA_CARRIER:
                radius = 30.0f;
                max_hp = static_cast<int>(200 * hp_mult);
                speed = 55.0f * speed_mult;
                score_value = 450;
                shoot_interval = 999.0f;
                launch_timer = 8.0f;    // first launch at 8s
                sprite_key = "asura_tank.png";    // reuse art
                break;
        }
        hp = max_hp;
        if (is_miniboss) {
            radius = std::min(38.0f, radius * 1.35f);
            max_hp = static_cast<int>(std::round(max_hp * 2.3f));

            hp = max_hp;
            score_value *= 4;
        }
        shoot_timer = ((std::rand() % 100) / 100.0f) * shoot_interval;
        assign_affixes();  // set elite affix flags + label + tint
    }


    void update(float dt, Vector2 player_pos, std::vector<Bullet>& out_bullets,
                std::vector<Enemy>& all_enemies, int extra_flak_projectiles = 0,
                float telegraph_warning_mult = 1.0f) {
        if (!active) return;
        if (hit_flash > 0) hit_flash -= dt;

        // REGEN affix: 2% HP/s regeneration
        if (has_affix(affixes, EliteAffix::REGEN) && hp < max_hp) {
            regen_timer += dt;
            if (regen_timer >= 0.5f) {
                hp = std::min(max_hp, hp + std::max(1, static_cast<int>(max_hp * 0.01f)));
                regen_timer = 0.0f;
            }
        }

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
                    // Rift Maulers widen the tank's normal fan into a five-lane breach volley.
                    const int projectile_count = is_miniboss ? 5 : 3;
                    for (int i = 0; i < projectile_count; ++i) {
                        const int offset = is_miniboss ? (i - 2) * 14 : (i - 1) * 20;
                        float rad = (angle + offset) * (3.14159f / 180.0f);
                        Bullet b;
                        b.active = true;
                        b.is_enemy = true;
                        b.damage_source = damage_source_name();
                        b.pos = pos;
                        const float speed_mult = is_miniboss ? 1.08f : 1.0f;
                        b.vel = { std::cos(rad) * ENEMY_BULLET_SPEED * speed_mult, std::sin(rad) * ENEMY_BULLET_SPEED * speed_mult };
                        b.damage = is_miniboss ? 20 : 14;
                        b.radius = is_miniboss ? 7.0f : 6.0f;
                        b.color = is_miniboss ? COLOR_RED_BRIGHT : COLOR_ORANGE_BRIGHT;
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
                    b.damage_source = damage_source_name();
                    b.pos = pos;
                    b.vel = Vector2Scale(dir, ENEMY_BULLET_SPEED * 1.1f);
                    b.damage = 12;
                    b.color = COLOR_RED_BRIGHT;
                    out_bullets.push_back(b);
                    if (is_miniboss) {
                        for (const int offset : { -18, 18 }) {
                            const float spread_rad = (angle + offset) * (3.14159f / 180.0f);
                            Bullet spread;
                            spread.active = true;
                            spread.is_enemy = true;
                            spread.damage_source = damage_source_name();
                            spread.pos = pos;
                            spread.vel = { std::cos(spread_rad) * ENEMY_BULLET_SPEED,
                                           std::sin(spread_rad) * ENEMY_BULLET_SPEED };
                            spread.damage = 10;
                            spread.radius = 5.0f;
                            spread.color = COLOR_ORANGE_BRIGHT;
                            out_bullets.push_back(spread);
                        }
                    }
                    for (int i = 0; i < extra_flak_projectiles; ++i) {
                        const float flak_rad = (angle + 18.0f + i * 12.0f) * (3.14159f / 180.0f);
                        Bullet flak;
                        flak.active = true;
                        flak.is_enemy = true;
                        flak.damage_source = damage_source_name();
                        flak.pos = pos;
                        flak.vel = { std::cos(flak_rad) * ENEMY_BULLET_SPEED * 0.9f,
                                     std::sin(flak_rad) * ENEMY_BULLET_SPEED * 0.9f };
                        flak.damage = 8;
                        flak.radius = 4.0f;
                        flak.color = COLOR_ORANGE_BRIGHT;
                        out_bullets.push_back(flak);
                    }
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
                if (shoot_timer <= 0.8f * std::clamp(telegraph_warning_mult, 0.3f, 1.0f)) {
                    is_charging = true;
                }
                if (shoot_timer <= 0) {
                    shoot_timer = shoot_interval;
                    is_charging = false;
                    Bullet b;
                    b.active = true;
                    b.is_enemy = true;
                    b.damage_source = damage_source_name();
                    b.pos = pos;
                    b.vel = Vector2Scale(dir, ENEMY_BULLET_SPEED * 2.2f);
                    b.damage = 30;
                    b.radius = 7.0f;
                    b.type = BulletType::ENEMY_SNIPER_BEAM;
                    b.color = COLOR_CYAN_BRIGHT;
                    out_bullets.push_back(b);
                    if (is_miniboss) {
                        for (const int offset : { -7, 7 }) {
                            const float beam_rad = (angle + offset) * (3.14159f / 180.0f);
                            Bullet side_beam;
                            side_beam.active = true;
                            side_beam.is_enemy = true;
                            side_beam.damage_source = damage_source_name();
                            side_beam.pos = pos;
                            side_beam.vel = { std::cos(beam_rad) * ENEMY_BULLET_SPEED * 1.8f,
                                              std::sin(beam_rad) * ENEMY_BULLET_SPEED * 1.8f };
                            side_beam.damage = 18;
                            side_beam.radius = 5.0f;
                            side_beam.type = BulletType::ENEMY_SNIPER_BEAM;
                            side_beam.color = COLOR_PURPLE_BRIGHT;
                            out_bullets.push_back(side_beam);
                        }
                    }
                }
                break;

            case EnemyType::ASURA_MINELAYER:
                // Drift sideways slowly, drop mines periodically
                pos.x += -dir.y * speed * 0.6f * dt;
                pos.y = std::max(60.0f, pos.y - speed * 0.15f * dt);  // stay upper area
                mine_timer -= dt;
                if (mine_timer <= 0 && mines_placed < 6) {
                    mine_timer = shoot_interval;
                    ++mines_placed;
                    // Mine = slow enemy bullet that hovers near drop point
                    Bullet mine;
                    mine.active = true;
                    mine.is_enemy = true;
                    mine.damage_source = "Asura Mine";
                    mine.pos = pos;
                    mine.vel = { 0.0f, 20.0f };   // slow drift downward
                    mine.damage = 22;
                    mine.radius = 10.0f;
                    mine.color = COLOR_ORANGE_BRIGHT;
                    mine.type = BulletType::ENEMY_PROXIMITY_MINE;
                    out_bullets.push_back(mine);
                }
                break;

            case EnemyType::ASURA_CARRIER:
                // Slow drift down + clockwise orbit
                pos.y += speed * 0.3f * dt;
                special_timer += dt;
                pos.x += std::sin(special_timer * 0.4f) * speed * 0.5f * dt;
                launch_timer -= dt;
                if (launch_timer <= 0) {
                    launch_timer = 8.0f;
                    // Spawn 3 Chasers around the carrier via bullets the game_view can handle
                    for (int i = 0; i < 3; ++i) {
                        float spawn_rad = (i * 120.0f) * (3.14159f / 180.0f);
                        Bullet spawn_beacon;
                        spawn_beacon.active = true;
                        spawn_beacon.is_enemy = true;
                        spawn_beacon.damage_source = "Carrier Squad";
                        spawn_beacon.pos = { pos.x + std::cos(spawn_rad) * 30.0f,
                                             pos.y + std::sin(spawn_rad) * 30.0f };
                        spawn_beacon.vel = { 0.0f, 0.0f };
                        spawn_beacon.damage = 0;
                        spawn_beacon.radius = 5.0f;
                        spawn_beacon.color = COLOR_RED_BRIGHT;
                        spawn_beacon.type = BulletType::CARRIER_SPAWN_SIGNAL;
                        out_bullets.push_back(spawn_beacon);
                    }
                }
                break;
        }

        // Clamp inside screen bounds
        pos.x = std::max(radius, std::min(SCREEN_WIDTH - radius, pos.x));
        pos.y = std::max(radius, std::min(SCREEN_HEIGHT - radius, pos.y));
    }

    void draw(Texture2D tex) const {
        if (!active) return;

        // Mini-bosses use a double-ring and nameplate; regular elites retain the gold aura.
        if (is_miniboss) {
            const float pulse = 0.5f + 0.5f * std::sin(GetTime() * 6.0f);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 9.0f + 4.0f * pulse, COLOR_RED_BRIGHT);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 15.0f, ColorAlpha(COLOR_GOLD_BRIGHT, 0.55f));
            DrawText("MINI-BOSS", static_cast<int>(pos.x - 29.0f), static_cast<int>(pos.y - radius - 43.0f), 9, COLOR_GOLD_BRIGHT);
            const int name_width = MeasureText(miniboss_name.c_str(), 9);
            DrawText(miniboss_name.c_str(), static_cast<int>(pos.x - name_width * 0.5f), static_cast<int>(pos.y - radius - 31.0f), 9, COLOR_PARCHMENT);
        } else if (is_elite) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 8.0f);
            DrawCircleLines(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 6.0f + 3.0f * pulse, elite_tint);
            DrawCircle(static_cast<int>(pos.x), static_cast<int>(pos.y), radius + 4.0f, ColorAlpha(elite_tint, 0.12f));
            DrawText("ELITE", static_cast<int>(pos.x - 14.0f), static_cast<int>(pos.y - radius - 26.0f), 9, elite_tint);
            if (!affix_label.empty()) {
                int aw = MeasureText(affix_label.c_str(), 8);
                DrawText(affix_label.c_str(), static_cast<int>(pos.x - aw * 0.5f),
                         static_cast<int>(pos.y - radius - 15.0f), 8, ColorAlpha(elite_tint, 0.9f));
            }
        }
        // Carrier nameplate
        if (type == EnemyType::ASURA_CARRIER) {
            DrawText("CARRIER", static_cast<int>(pos.x - 22.0f), static_cast<int>(pos.y - radius - 16.0f), 9, COLOR_RED_BRIGHT);
        }
        if (type == EnemyType::ASURA_MINELAYER) {
            DrawText("MINELAYER", static_cast<int>(pos.x - 28.0f), static_cast<int>(pos.y - radius - 16.0f), 9, COLOR_ORANGE_BRIGHT);
        }


        // Sniper telegraph laser
        if (type == EnemyType::ASURA_SNIPER && is_charging) {
            float rad = angle * (3.14159f / 180.0f);
            Vector2 aim_end = { pos.x + std::cos(rad) * 600.0f, pos.y + std::sin(rad) * 600.0f };
            DrawLineEx(pos, aim_end, 1.5f, ColorAlpha(COLOR_RED_BRIGHT, 0.45f));
        }

        Color tint = (!g_reduce_flashes && hit_flash > 0) ? WHITE : COLOR_PARCHMENT;
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

        // Role glyphs are presentation only: draw them during rendering, never
        // from init()/update(), where Raylib draw calls have no active frame.
        const Vector2 glyph = { pos.x, pos.y - radius - (is_miniboss ? 50.0f : is_elite ? 28.0f : 10.0f) };
        switch (type) {
            case EnemyType::ASURA_CHASER:
                DrawTriangle({ glyph.x, glyph.y - 5 }, { glyph.x - 5, glyph.y + 4 }, { glyph.x + 5, glyph.y + 4 }, COLOR_ORANGE_BRIGHT);
                break;
            case EnemyType::ASURA_TANK:
                DrawRectangle(static_cast<int>(glyph.x - 4), static_cast<int>(glyph.y - 4), 8, 8, COLOR_GOLD_BRIGHT);
                break;
            case EnemyType::ASURA_HEALER:
                DrawCircleLines(static_cast<int>(glyph.x), static_cast<int>(glyph.y), 5, COLOR_GREEN_BRIGHT);
                DrawLine(static_cast<int>(glyph.x - 3), static_cast<int>(glyph.y), static_cast<int>(glyph.x + 3), static_cast<int>(glyph.y), COLOR_GREEN_BRIGHT);
                DrawLine(static_cast<int>(glyph.x), static_cast<int>(glyph.y - 3), static_cast<int>(glyph.x), static_cast<int>(glyph.y + 3), COLOR_GREEN_BRIGHT);
                break;
            case EnemyType::ASURA_SNIPER:
                DrawCircleLines(static_cast<int>(glyph.x), static_cast<int>(glyph.y), 5, COLOR_CYAN_BRIGHT);
                DrawLine(static_cast<int>(glyph.x - 7), static_cast<int>(glyph.y), static_cast<int>(glyph.x + 7), static_cast<int>(glyph.y), COLOR_CYAN_BRIGHT);
                DrawLine(static_cast<int>(glyph.x), static_cast<int>(glyph.y - 7), static_cast<int>(glyph.x), static_cast<int>(glyph.y + 7), COLOR_CYAN_BRIGHT);
                break;
            case EnemyType::ASURA_KAMIKAZE:
                DrawCircle(static_cast<int>(glyph.x), static_cast<int>(glyph.y), 5, COLOR_RED_BRIGHT);
                DrawCircleLines(static_cast<int>(glyph.x), static_cast<int>(glyph.y), 8, COLOR_GOLD_BRIGHT);
                break;
            case EnemyType::ASURA_SHOOTER:
                DrawPoly(glyph, 4, 6.0f, 45.0f, COLOR_PURPLE_BRIGHT);
                break;
            case EnemyType::ASURA_MINELAYER:
                DrawCircle(static_cast<int>(glyph.x), static_cast<int>(glyph.y), 4, COLOR_ORANGE_BRIGHT);
                DrawCircleLines(static_cast<int>(glyph.x), static_cast<int>(glyph.y), 7, COLOR_RED_BRIGHT);
                break;
            case EnemyType::ASURA_CARRIER:
                DrawRectangle(static_cast<int>(glyph.x - 6), static_cast<int>(glyph.y - 3), 12, 6, COLOR_RED_BRIGHT);
                DrawRectangleLines(static_cast<int>(glyph.x - 7), static_cast<int>(glyph.y - 4), 14, 8, COLOR_GOLD_BRIGHT);
                break;
        }

        // Mini HP Bar for Tanks & Healers
        if (hp < max_hp || is_miniboss) {
            const float bar_w = radius * (is_miniboss ? 2.6f : 2.0f);
            const float bar_h = is_miniboss ? 5.0f : 3.0f;
            float hp_ratio = static_cast<float>(hp) / max_hp;
            const int bar_y = static_cast<int>(pos.y - radius - (is_miniboss ? 10.0f : 8.0f));
            DrawRectangle(static_cast<int>(pos.x - bar_w / 2), bar_y, static_cast<int>(bar_w), static_cast<int>(bar_h), { 30, 30, 30, 200 });
            DrawRectangle(static_cast<int>(pos.x - bar_w / 2), bar_y, static_cast<int>(bar_w * hp_ratio), static_cast<int>(bar_h), is_miniboss ? COLOR_GOLD_BRIGHT : COLOR_RED_BRIGHT);
        }
    }
};

} // namespace Vimana
