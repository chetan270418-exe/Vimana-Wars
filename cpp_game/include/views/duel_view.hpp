#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "entities/player.hpp"
#include "entities/ai_bot.hpp"
#include "entities/bullet.hpp"
#include "systems/particle_system.hpp"
#include "systems/sound_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class DuelView : public IView {
public:
    DuelView() : m_next_view(ViewType::DUEL), m_is_training_mode(true), m_bot(BotDifficulty::SKILLED) {
        init();
    }

    void init() override {
        m_next_view = ViewType::DUEL;
        m_bullets.clear();
        m_p1_wins = 0;
        m_p2_wins = 0;
        m_round_over = false;
        m_round_timer = 0.0f;

        // Player 1 (Pushpaka)
        m_p1.init(&SHIP_FLEET[0]);
        m_p1.pos = { 200.0f, SCREEN_HEIGHT / 2.0f };

        // Player 2 / Bot (Garuda)
        m_p2.init(&SHIP_FLEET[2]);
        m_p2.pos = { SCREEN_WIDTH - 200.0f, SCREEN_HEIGHT / 2.0f };

        // Buttons
        m_btn_toggle_mode = UI::Button({ 40, 20, 240, 36 }, "MODE: AI TRAINING", COLOR_CYAN_BRIGHT);
        m_btn_toggle_bot = UI::Button({ 300, 20, 220, 36 }, "BOT: SKILLED", COLOR_GOLD);
        m_btn_rematch = UI::Button({ SCREEN_WIDTH / 2.0f - 90, SCREEN_HEIGHT / 2.0f + 40, 180, 40 }, "REMATCH", COLOR_GOLD_BRIGHT);
        m_btn_back = UI::Button({ SCREEN_WIDTH - 150, 20, 110, 36 }, "EXIT", COLOR_MUTED);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
            return;
        }

        if (m_btn_toggle_mode.update(mouse_pos)) {
            m_is_training_mode = !m_is_training_mode;
            m_btn_toggle_mode.set_label(m_is_training_mode ? "MODE: AI TRAINING" : "MODE: LOCAL 1V1 PVP");
            reset_round();
        }

        if (m_is_training_mode && m_btn_toggle_bot.update(mouse_pos)) {
            BotDifficulty curr = m_bot.get_difficulty();
            if (curr == BotDifficulty::NOVICE) {
                m_bot.set_difficulty(BotDifficulty::SKILLED);
                m_btn_toggle_bot.set_label("BOT: SKILLED");
            } else if (curr == BotDifficulty::SKILLED) {
                m_bot.set_difficulty(BotDifficulty::ASURA_MASTER);
                m_btn_toggle_bot.set_label("BOT: ASURA MASTER");
            } else {
                m_bot.set_difficulty(BotDifficulty::NOVICE);
                m_btn_toggle_bot.set_label("BOT: NOVICE");
            }
            reset_round();
        }

        if (m_round_over) {
            if (m_btn_rematch.update(mouse_pos) || IsKeyPressed(KEY_ENTER)) {
                reset_round();
            }
            return;
        }

        // Update P1 (WASD + Mouse)
        m_p1.handle_input(dt, mouse_pos, m_bullets, false);
        m_p1.update(dt);

        // Update P2 or AI Bot
        if (m_is_training_mode) {
            m_bot.update(dt, m_p2, m_p1, m_bullets, m_bullets);
            m_p2.update(dt);
        } else {
            m_p2.handle_input(dt, mouse_pos, m_bullets, true);
            m_p2.update(dt);
        }

        // Update Bullets
        for (auto& b : m_bullets) {
            if (!b.active) continue;
            b.update(dt);

            // Check Bullet vs P1
            if (b.is_enemy && Vector2Distance(b.pos, m_p1.pos) < (b.radius + m_p1.radius)) {
                m_p1.take_damage(b.damage);
                m_particles.emit_explosion(b.pos, COLOR_RED_BRIGHT, 8, 120.0f);
                b.active = false;
            }

            // Check Bullet vs P2
            if (!b.is_enemy && Vector2Distance(b.pos, m_p2.pos) < (b.radius + m_p2.radius)) {
                m_p2.take_damage(b.damage);
                m_particles.emit_explosion(b.pos, COLOR_GOLD_BRIGHT, 8, 120.0f);
                b.active = false;
            }
        }

        m_particles.update(dt);

        // Check Round End
        if (m_p1.hp <= 0) {
            m_round_over = true;
            m_p2_wins++;
            m_winner_text = m_is_training_mode ? "AI BOT VICTORIOUS!" : "PLAYER 2 VICTORIOUS!";
            SoundSystem::instance().play_sfx("game_over.wav");
        } else if (m_p2.hp <= 0) {
            m_round_over = true;
            m_p1_wins++;
            m_winner_text = "PLAYER 1 VICTORIOUS!";
            SoundSystem::instance().play_sfx("victory.wav");
        }
    }

    void reset_round() {
        m_round_over = false;
        m_bullets.clear();
        m_p1.hp = m_p1.max_hp;
        m_p1.pos = { 200.0f, SCREEN_HEIGHT / 2.0f };
        m_p2.hp = m_p2.max_hp;
        m_p2.pos = { SCREEN_WIDTH - 200.0f, SCREEN_HEIGHT / 2.0f };
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Arena Boundaries
        UI::DrawChamferedPanel({ 30, 75, SCREEN_WIDTH - 60, SCREEN_HEIGHT - 100 }, COLOR_GOLD, { 8, 12, 22, 255 }, 8.0f);

        // Header Buttons
        m_btn_toggle_mode.draw(font);
        if (m_is_training_mode) m_btn_toggle_bot.draw(font);
        m_btn_back.draw(font);

        // Score Counters
        std::string score_txt = "P1: " + std::to_string(m_p1_wins) + "  |  " +
                                (m_is_training_mode ? "BOT: " : "P2: ") + std::to_string(m_p2_wins);
        Vector2 sc_sz = MeasureTextEx(font, score_txt.c_str(), 18, 1.0f);
        DrawTextEx(font, score_txt.c_str(), { (SCREEN_WIDTH - sc_sz.x) / 2.0f, 26 }, 18, 1.0f, COLOR_GOLD_BRIGHT);

        // Health Bars: Top Left P1, Top Right P2
        float p1_ratio = std::clamp(static_cast<float>(m_p1.hp) / m_p1.max_hp, 0.0f, 1.0f);
        DrawRectangle(45, 90, 200, 14, { 30, 30, 30, 255 });
        DrawRectangle(45, 90, static_cast<int>(200 * p1_ratio), 14, COLOR_CYAN_BRIGHT);
        DrawRectangleLines(45, 90, 200, 14, COLOR_GOLD);
        DrawText("P1 HULL", 45, 108, 11, COLOR_CYAN_BRIGHT);

        float p2_ratio = std::clamp(static_cast<float>(m_p2.hp) / m_p2.max_hp, 0.0f, 1.0f);
        DrawRectangle(SCREEN_WIDTH - 245, 90, 200, 14, { 30, 30, 30, 255 });
        DrawRectangle(SCREEN_WIDTH - 245, 90, static_cast<int>(200 * p2_ratio), 14, COLOR_RED_BRIGHT);
        DrawRectangleLines(SCREEN_WIDTH - 245, 90, 200, 14, COLOR_GOLD);
        DrawText(m_is_training_mode ? "AI BOT HULL" : "P2 HULL", SCREEN_WIDTH - 245, 108, 11, COLOR_RED_BRIGHT);

        // Draw Entities
        m_p1.draw(AssetManager::instance().get_texture("pushpaka.png"));
        m_p2.draw(AssetManager::instance().get_texture("garuda.png"));

        for (const auto& b : m_bullets) {
            if (b.active) b.draw();
        }

        m_particles.draw();

        // Round Over Overlay
        if (m_round_over) {
            UI::DrawChamferedPanel({ SCREEN_WIDTH / 2.0f - 180, SCREEN_HEIGHT / 2.0f - 60, 360, 160 }, COLOR_GOLD_BRIGHT, COLOR_SURFACE_HIGH, 6.0f);
            Vector2 win_sz = MeasureTextEx(font, m_winner_text.c_str(), 22, 1.0f);
            DrawTextEx(font, m_winner_text.c_str(), { (SCREEN_WIDTH - win_sz.x) / 2.0f, SCREEN_HEIGHT / 2.0f - 30 }, 22, 1.0f, COLOR_GOLD_BRIGHT);
            m_btn_rematch.draw(font);
        }

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::DUEL; }

private:
    ViewType m_next_view;
    bool m_is_training_mode;
    AIBotController m_bot;
    Player m_p1;
    Player m_p2;
    std::vector<Bullet> m_bullets;
    ParticleSystem m_particles;

    int m_p1_wins;
    int m_p2_wins;
    bool m_round_over;
    float m_round_timer;
    std::string m_winner_text;

    UI::Button m_btn_toggle_mode;
    UI::Button m_btn_toggle_bot;
    UI::Button m_btn_rematch;
    UI::Button m_btn_back;
};

} // namespace Vimana
