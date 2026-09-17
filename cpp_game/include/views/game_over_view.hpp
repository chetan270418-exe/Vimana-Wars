#pragma once
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/db_system.hpp"
#include "systems/currency_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class GameOverView : public IView {
public:
    GameOverView(bool is_victory = false)
        : m_next_view(is_victory ? ViewType::VICTORY : ViewType::GAME_OVER), m_is_victory(is_victory) {
        init();
    }

    void init() override {
        m_next_view = m_is_victory ? ViewType::VICTORY : ViewType::GAME_OVER;

        float cx = SCREEN_WIDTH / 2.0f;
        m_btn_replay = UI::Button({ cx - 130, 420, 260, 42 }, "FLY AGAIN", COLOR_GOLD_BRIGHT);
        m_btn_hangar = UI::Button({ cx - 130, 475, 260, 38 }, "VIMANA HANGAR", COLOR_CYAN_BRIGHT);
        m_btn_menu = UI::Button({ cx - 130, 525, 260, 38 }, "RETURN TO MAIN MENU", COLOR_MUTED);
    }

    void set_results(bool victory, int score, int wave, int kills, int damage, const std::string& ship_name) {
        m_is_victory = victory;
        m_score = score;
        m_wave = wave;
        m_kills = kills;
        m_damage = damage;
        m_ship = ship_name;

        // Save score to database
        ScoreEntry entry;
        entry.player_name = DBSystem::instance().player_name();
        entry.score = score;
        entry.level_reached = wave;
        entry.ship_class = ship_name;
        entry.kills = kills;
        entry.total_damage = damage;
        DBSystem::instance().insert_score(entry);
        DBSystem::instance().update_high_score(score);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_replay.update(mouse_pos)) {
            m_next_view = ViewType::SHIP_SELECT;
        } else if (m_btn_hangar.update(mouse_pos)) {
            m_next_view = ViewType::SHIP_SELECT;
        } else if (m_btn_menu.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Main Result Card
        UI::DrawChamferedPanel({ SCREEN_WIDTH / 2.0f - 240, 50, 480, 340 }, m_is_victory ? COLOR_GOLD_BRIGHT : COLOR_RED_BRIGHT, COLOR_SURFACE_LOW, 8.0f);

        if (m_is_victory) {
            const char* vic = "MAHAYUDDHA VICTORIOUS!";
            Vector2 v_sz = MeasureTextEx(font, vic, 28, 1.0f);
            DrawTextEx(font, vic, { (SCREEN_WIDTH - v_sz.x) / 2.0f, 75 }, 28, 1.0f, COLOR_GOLD_BRIGHT);

            const char* sub = "EMPEROR HIRANYAKASHIPU VANQUISHED • NARASIMHA AWAKENS!";
            Vector2 s_sz = MeasureTextEx(font, sub, 11, 1.0f);
            DrawTextEx(font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 112 }, 11, 1.0f, COLOR_CYAN_BRIGHT);
        } else {
            const char* def = "VIMANA LOST IN ASTRAL VOID";
            Vector2 d_sz = MeasureTextEx(font, def, 26, 1.0f);
            DrawTextEx(font, def, { (SCREEN_WIDTH - d_sz.x) / 2.0f, 75 }, 26, 1.0f, COLOR_RED_BRIGHT);

            const char* sub = "THE ASURA ARMADA RECLAIMS THE HEAVENS • FORGE A NEW VIMANA";
            Vector2 s_sz = MeasureTextEx(font, sub, 11, 1.0f);
            DrawTextEx(font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 112 }, 11, 1.0f, COLOR_MUTED);
        }

        DrawLine(SCREEN_WIDTH / 2 - 200, 135, SCREEN_WIDTH / 2 + 200, 135, COLOR_MUTED);

        // Stats Display
        float cx = SCREEN_WIDTH / 2.0f - 160;
        DrawText("FINAL COMBAT SCORE:", cx, 160, 14, COLOR_PARCHMENT);
        DrawText(std::to_string(m_score).c_str(), cx + 220, 160, 18, COLOR_GOLD_BRIGHT);

        DrawText("HIGHEST WAVE REACHED:", cx, 195, 14, COLOR_PARCHMENT);
        DrawText(("WAVE " + std::to_string(m_wave)).c_str(), cx + 220, 195, 16, COLOR_CYAN_BRIGHT);

        DrawText("ASURAS DESTROYED:", cx, 230, 14, COLOR_PARCHMENT);
        DrawText(std::to_string(m_kills).c_str(), cx + 220, 230, 16, COLOR_RED_BRIGHT);

        DrawText("TOTAL DAMAGE DEALT:", cx, 265, 14, COLOR_PARCHMENT);
        DrawText(std::to_string(m_damage).c_str(), cx + 220, 265, 16, COLOR_ORANGE_BRIGHT);

        DrawText("VESSEL CLASS:", cx, 300, 14, COLOR_PARCHMENT);
        DrawText(m_ship.c_str(), cx + 220, 300, 16, COLOR_GOLD);

        // Buttons
        m_btn_replay.draw(font);
        m_btn_hangar.draw(font);
        m_btn_menu.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = m_is_victory ? ViewType::VICTORY : ViewType::GAME_OVER; }

private:
    ViewType m_next_view;
    bool m_is_victory;
    int m_score = 0;
    int m_wave = 1;
    int m_kills = 0;
    int m_damage = 0;
    std::string m_ship = "Pushpaka";

    UI::Button m_btn_replay;
    UI::Button m_btn_hangar;
    UI::Button m_btn_menu;
};

} // namespace Vimana
