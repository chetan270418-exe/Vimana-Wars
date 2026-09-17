#pragma once
#include <cmath>
#include <vector>
#include "raylib.h"
#include "core/types.hpp"
#include "core/constants.hpp"
#include "entities/player.hpp"
#include "entities/bullet.hpp"

namespace Vimana {

class AIBotController {
public:
    AIBotController(BotDifficulty diff = BotDifficulty::SKILLED) : m_difficulty(diff) {}

    void set_difficulty(BotDifficulty diff) { m_difficulty = diff; }
    BotDifficulty get_difficulty() const { return m_difficulty; }

    void update(float dt, Player& bot, const Player& opponent, const std::vector<Bullet>& bullets, std::vector<Bullet>& out_bullets) {
        Vector2 to_opp = Vector2Subtract(opponent.pos, bot.pos);
        float dist = Vector2Length(to_opp);
        Vector2 dir_opp = Vector2Normalize(to_opp);

        // 1. Aiming Logic (with lead calculation based on difficulty)
        Vector2 target_pos = opponent.pos;
        if (m_difficulty != BotDifficulty::NOVICE) {
            float bullet_speed = PLAYER_BULLET_SPEED;
            float time_to_hit = dist / bullet_speed;
            // Lead target by opponent velocity
            target_pos.x += opponent.vel.x * time_to_hit * (m_difficulty == BotDifficulty::ASURA_MASTER ? 1.0f : 0.6f);
            target_pos.y += opponent.vel.y * time_to_hit * (m_difficulty == BotDifficulty::ASURA_MASTER ? 1.0f : 0.6f);
        }
        bot.angle = Vector2AngleDeg(bot.pos, target_pos);

        // 2. Movement & Evasion
        Vector2 move_dir = { 0, 0 };
        float optimal_range = (m_difficulty == BotDifficulty::ASURA_MASTER) ? 200.0f : 250.0f;

        if (dist > optimal_range + 50.0f) {
            move_dir.x += dir_opp.x;
            move_dir.y += dir_opp.y;
        } else if (dist < optimal_range - 50.0f) {
            move_dir.x -= dir_opp.x;
            move_dir.y -= dir_opp.y;
        } else {
            // Strafe perpendicular
            move_dir.x += -dir_opp.y;
            move_dir.y += dir_opp.x;
        }

        // 3. Bullet Avoidance
        bool should_dash = false;
        Vector2 dodge_vector = { 0, 0 };

        for (const auto& b : bullets) {
            if (!b.active) continue;
            // Only avoid bullets moving toward us
            float d = Vector2Distance(bot.pos, b.pos);
            if (d < 150.0f) {
                Vector2 to_bot = Vector2Subtract(bot.pos, b.pos);
                float dot = b.vel.x * to_bot.x + b.vel.y * to_bot.y;
                if (dot > 0) { // Moving toward bot
                    dodge_vector.x += (to_bot.x / d);
                    dodge_vector.y += (to_bot.y / d);
                    if (d < 70.0f && m_difficulty != BotDifficulty::NOVICE) {
                        should_dash = true;
                    }
                }
            }
        }

        if (Vector2Length(dodge_vector) > 0.1f) {
            move_dir = Vector2Normalize(Vector2Add(move_dir, dodge_vector));
        }

        move_dir = Vector2Normalize(move_dir);
        float spd = bot.is_dashing ? DASH_SPEED_BURST : bot.current_speed;
        bot.vel.x = move_dir.x * spd;
        bot.vel.y = move_dir.y * spd;

        if (should_dash && (m_difficulty == BotDifficulty::ASURA_MASTER || (std::rand() % 10 < 7))) {
            bot.try_dash(move_dir);
        }

        // 4. Combat Decisions
        float shoot_chance = (m_difficulty == BotDifficulty::ASURA_MASTER) ? 0.95f : (m_difficulty == BotDifficulty::SKILLED ? 0.75f : 0.45f);
        if (((std::rand() % 100) / 100.0f) < shoot_chance) {
            bot.try_shoot(out_bullets);
        }

        // Use Chakram when aligned and ready
        if (m_difficulty != BotDifficulty::NOVICE && dist < 260.0f) {
            bot.try_chakram(out_bullets);
        }

        // Emergency heal with Soma Vial
        if (bot.hp < bot.max_hp * 0.4f && bot.inventory.soma_vials > 0) {
            bot.use_soma_vial();
        }
    }

private:
    BotDifficulty m_difficulty;
};

} // namespace Vimana
