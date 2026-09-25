#pragma once
#include <vector>
#include <cmath>
#include <string>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "entities/bullet.hpp"
#include "entities/player.hpp"
#include "entities/enemy.hpp"
#include "entities/boss.hpp"

namespace Vimana {

class IPlayerController {
public:
    virtual ~IPlayerController() = default;
    virtual void update(
        float dt,
        Player& self,
        std::vector<Bullet>& out_bullets,
        Vector2 mouse_pos,
        std::vector<Player>& squad,
        const std::vector<Enemy>& enemies,
        const Boss* boss
    ) = 0;
};

// -- Human Controller (Local Player) ------------------------------------------
class HumanController : public IPlayerController {
public:
    HumanController(int player_index = 0) : m_player_idx(player_index), m_revive_hold_timer(0.0f) {}

    void update(
        float dt,
        Player& self,
        std::vector<Bullet>& out_bullets,
        Vector2 mouse_pos,
        std::vector<Player>& squad,
        const std::vector<Enemy>& enemies,
        const Boss* boss
    ) override {
        if (self.is_downed) {
            // Downed movement is sluggish crawl
            Vector2 crawl = { 0, 0 };
            if (IsKeyDown(KEY_W) || IsKeyDown(KEY_UP)) crawl.y -= 1.0f;
            if (IsKeyDown(KEY_S) || IsKeyDown(KEY_DOWN)) crawl.y += 1.0f;
            if (IsKeyDown(KEY_A) || IsKeyDown(KEY_LEFT)) crawl.x -= 1.0f;
            if (IsKeyDown(KEY_D) || IsKeyDown(KEY_RIGHT)) crawl.x += 1.0f;
            if (Vector2Length(crawl) > 0.1f) crawl = Vector2Normalize(crawl);
            self.vel.x = crawl.x * 40.0f;
            self.vel.y = crawl.y * 40.0f;
            return;
        }

        // Standard movement & aiming
        Vector2 input_dir = { 0, 0 };
        if (m_player_idx == 0) {
            // WASD
            if (IsKeyDown(KEY_W)) input_dir.y -= 1.0f;
            if (IsKeyDown(KEY_S)) input_dir.y += 1.0f;
            if (IsKeyDown(KEY_A)) input_dir.x -= 1.0f;
            if (IsKeyDown(KEY_D)) input_dir.x += 1.0f;

            // Aim towards mouse
            self.angle = Vector2AngleDeg(self.pos, mouse_pos);

            // Primary fire
            if (IsMouseButtonDown(MOUSE_BUTTON_LEFT) || IsKeyDown(KEY_SPACE)) {
                self.try_shoot(out_bullets);
            }

            // Dash
            if (IsKeyPressed(KEY_LEFT_SHIFT) || IsMouseButtonPressed(MOUSE_BUTTON_RIGHT)) {
                self.try_dash(input_dir);
            }

            // Sudarshana Chakram
            if (IsKeyPressed(KEY_Q)) {
                self.try_chakram(out_bullets);
            }

            // Consumables: Soma Vial (C) and Vajra Flare (V)
            if (IsKeyPressed(KEY_C)) {
                self.use_soma_vial();
            }
            if (IsKeyPressed(KEY_V)) {
                self.use_vajra_flare(out_bullets);
            }
        } else {
            // Arrow keys for P2
            if (IsKeyDown(KEY_UP)) input_dir.y -= 1.0f;
            if (IsKeyDown(KEY_DOWN)) input_dir.y += 1.0f;
            if (IsKeyDown(KEY_LEFT)) input_dir.x -= 1.0f;
            if (IsKeyDown(KEY_RIGHT)) input_dir.x += 1.0f;

            if (Vector2Length(input_dir) > 0.1f) {
                self.angle = std::atan2(input_dir.y, input_dir.x) * (180.0f / 3.14159f);
            }

            if (IsKeyDown(KEY_RIGHT_CONTROL)) {
                self.try_shoot(out_bullets);
            }
            if (IsKeyPressed(KEY_SLASH) || IsKeyPressed(KEY_RIGHT_SHIFT)) {
                self.try_dash(input_dir);
            }
        }

        input_dir = Vector2Normalize(input_dir);
        float spd = self.is_dashing ? DASH_SPEED_BURST : self.current_speed;
        self.vel.x = input_dir.x * spd;
        self.vel.y = input_dir.y * spd;

        // Revive Interaction: Hold E within 80px of any downed squadmate
        bool holding_e = IsKeyDown(KEY_E);
        Player* target_downed = nullptr;
        for (auto& mate : squad) {
            if (&mate != &self && mate.is_downed) {
                float dist = Vector2Distance(self.pos, mate.pos);
                if (dist <= REVIVE_RANGE) {
                    target_downed = &mate;
                    break;
                }
            }
        }

        if (holding_e && target_downed) {
            m_revive_hold_timer += dt;
            if (m_revive_hold_timer >= REVIVE_TIME) {
                target_downed->is_downed = false;
                target_downed->hp = static_cast<int>(target_downed->max_hp * 0.40f);
                target_downed->invincibility_timer = 2.0f;
                target_downed->downed_timer = 0.0f;
                target_downed->self_revive_timer = 0.0f;
                target_downed->last_stand_timer = 0.0f;
                self.revives_given++;
                m_revive_hold_timer = 0.0f;
            }
        } else {
            m_revive_hold_timer = 0.0f;
        }
    }

    float revive_progress() const { return std::min(1.0f, m_revive_hold_timer / REVIVE_TIME); }

private:
    int m_player_idx;
    float m_revive_hold_timer;
};

// -- AI Wingman Controller ---------------------------------------------------
class AIController : public IPlayerController {
public:
    AIController(int slot_index = 1) 
        : m_slot(slot_index), m_revive_channel_timer(0.0f), m_dodge_timer(0.0f) {}

    void update(
        float dt,
        Player& self,
        std::vector<Bullet>& out_bullets,
        Vector2 mouse_pos,
        std::vector<Player>& squad,
        const std::vector<Enemy>& enemies,
        const Boss* boss
    ) override {
        if (self.is_downed) {
            self.vel = { 0, 0 };
            return;
        }

        // Emergency heal
        if (self.hp < static_cast<int>(self.max_hp * 0.35f) && self.inventory.soma_vials > 0) {
            self.use_soma_vial();
        }

        // 1. High-Priority Check: Revive downed teammate
        Player* downed_target = nullptr;
        for (auto& mate : squad) {
            if (&mate != &self && mate.is_downed) {
                downed_target = &mate;
                break;
            }
        }

        if (downed_target) {
            float dist = Vector2Distance(self.pos, downed_target->pos);
            if (dist > 50.0f) {
                Vector2 dir = Vector2Normalize({ downed_target->pos.x - self.pos.x, downed_target->pos.y - self.pos.y });
                self.vel.x = dir.x * self.current_speed;
                self.vel.y = dir.y * self.current_speed;
                self.angle = Vector2AngleDeg(self.pos, downed_target->pos);
                m_revive_channel_timer = 0.0f;
            } else {
                self.vel = { 0, 0 };
                m_revive_channel_timer += dt;
                if (m_revive_channel_timer >= REVIVE_TIME) {
                    downed_target->is_downed = false;
                    downed_target->hp = static_cast<int>(downed_target->max_hp * 0.40f);
                    downed_target->invincibility_timer = 2.0f;
                    downed_target->downed_timer = 0.0f;
                    downed_target->self_revive_timer = 0.0f;
                    downed_target->last_stand_timer = 0.0f;
                    self.revives_given++;
                    m_revive_channel_timer = 0.0f;
                }
            }
            return;
        }

        m_revive_channel_timer = 0.0f;

        // 2. Flight Position: Formation relative to Player 0
        Vector2 lead_pos = { SCREEN_WIDTH / 2.0f, SCREEN_HEIGHT * 0.75f };
        if (!squad.empty()) lead_pos = squad[0].pos;

        Vector2 target_pos = lead_pos;
        if (m_slot == 1)      target_pos = { lead_pos.x - 75.0f, lead_pos.y + 35.0f };
        else if (m_slot == 2) target_pos = { lead_pos.x + 75.0f, lead_pos.y + 35.0f };
        else                  target_pos = { lead_pos.x, lead_pos.y + 70.0f };

        target_pos.x = std::clamp(target_pos.x, 60.0f, SCREEN_WIDTH - 60.0f);
        target_pos.y = std::clamp(target_pos.y, 80.0f, SCREEN_HEIGHT - 60.0f);

        Vector2 to_target = { target_pos.x - self.pos.x, target_pos.y - self.pos.y };
        float dist_to_form = Vector2Length(to_target);
        if (dist_to_form > 15.0f) {
            Vector2 form_dir = Vector2Normalize(to_target);
            float move_spd = std::min(self.current_speed, dist_to_form * 4.0f);
            self.vel.x = form_dir.x * move_spd;
            self.vel.y = form_dir.y * move_spd;
        } else {
            self.vel.x *= 0.8f;
            self.vel.y *= 0.8f;
        }

        // 3. Combat Aiming & Firing
        Vector2 aim_target = { self.pos.x, -100.0f };
        bool has_target = false;

        if (boss && boss->active) {
            aim_target = boss->pos;
            has_target = true;
        } else {
            float closest_dist = 9999.0f;
            for (const auto& e : enemies) {
                if (!e.active) continue;
                float d = Vector2Distance(self.pos, e.pos);
                if (d < closest_dist) {
                    closest_dist = d;
                    aim_target = e.pos;
                    has_target = true;
                }
            }
        }

        if (has_target) {
            float desired_angle = Vector2AngleDeg(self.pos, aim_target);
            float diff = desired_angle - self.angle;
            while (diff < -180.0f) diff += 360.0f;
            while (diff > 180.0f) diff -= 360.0f;
            self.angle += diff * std::min(1.0f, dt * 8.0f);

            if (std::abs(diff) < 35.0f) {
                self.try_shoot(out_bullets);
                if (std::abs(diff) < 15.0f && self.chakram_timer <= 0) {
                    self.try_chakram(out_bullets);
                }
            }
        } else {
            self.angle = -90.0f;
        }
    }

private:
    int m_slot;
    float m_revive_channel_timer;
    float m_dodge_timer;
};

// -- Network Remote Controller ------------------------------------------------
class NetworkController : public IPlayerController {
public:
    NetworkController(uint8_t remote_player_id) 
        : m_remote_id(remote_player_id), m_target_pos({ 0, 0 }), m_has_data(false) {}

    void set_remote_state(Vector2 pos, Vector2 vel, float angle, int hp, bool downed, bool firing) {
        m_target_pos = pos;
        m_target_vel = vel;
        m_target_angle = angle;
        m_target_hp = hp;
        m_is_downed = downed;
        m_is_firing = firing;
        m_has_data = true;
    }

    void update(
        float dt,
        Player& self,
        std::vector<Bullet>& out_bullets,
        Vector2 mouse_pos,
        std::vector<Player>& squad,
        const std::vector<Enemy>& enemies,
        const Boss* boss
    ) override {
        if (!m_has_data) return;

        self.pos.x += (m_target_pos.x - self.pos.x) * std::min(1.0f, dt * 15.0f);
        self.pos.y += (m_target_pos.y - self.pos.y) * std::min(1.0f, dt * 15.0f);
        self.vel = m_target_vel;
        self.angle = m_target_angle;
        self.hp = m_target_hp;
        self.is_downed = m_is_downed;

        if (m_is_firing && !self.is_downed) {
            self.try_shoot(out_bullets);
        }
    }

private:
    uint8_t m_remote_id;
    Vector2 m_target_pos;
    Vector2 m_target_vel = { 0, 0 };
    float m_target_angle = -90.0f;
    int m_target_hp = 100;
    bool m_is_downed = false;
    bool m_is_firing = false;
    bool m_has_data = false;
};

} // namespace Vimana
