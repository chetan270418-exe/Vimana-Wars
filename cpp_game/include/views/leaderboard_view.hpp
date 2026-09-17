#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/db_system.hpp"
#include "systems/http_client.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class LeaderboardView : public IView {
public:
    LeaderboardView() : m_next_view(ViewType::LEADERBOARD), m_cloud_mode(false) {
        init();
    }

    void init() override {
        m_next_view = ViewType::LEADERBOARD;
        m_cloud_mode = false;
        m_scores = DBSystem::instance().fetch_top_scores(10);

        m_btn_back = UI::Button({ 40, 520, 110, 36 }, "BACK", COLOR_MUTED);
        m_btn_refresh = UI::Button({ SCREEN_WIDTH - 200, 520, 160, 36 }, "REFRESH", COLOR_CYAN_BRIGHT);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }

        if (m_btn_refresh.update(mouse_pos)) {
            m_scores = DBSystem::instance().fetch_top_scores(10);
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "ASTRAL LEADERBOARD // TOP CELESTIAL PILOTS", { 45, 30 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        // Leaderboard Table Panel
        UI::DrawChamferedPanel({ 30, 85, 840, 415 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        // Column Titles
        DrawText("RANK", 55, 105, 12, COLOR_MUTED);
        DrawText("PILOT NAME", 135, 105, 12, COLOR_MUTED);
        DrawText("SCORE", 345, 105, 12, COLOR_MUTED);
        DrawText("WAVE", 475, 105, 12, COLOR_MUTED);
        DrawText("SHIP ARSENAL", 575, 105, 12, COLOR_MUTED);
        DrawText("DIFFICULTY", 725, 105, 12, COLOR_MUTED);

        DrawLine(45, 125, 855, 125, COLOR_MUTED);

        // Rows
        int y = 140;
        for (size_t i = 0; i < m_scores.size(); ++i) {
            const auto& s = m_scores[i];
            Color row_col = (i == 0) ? COLOR_GOLD_BRIGHT : ((i < 3) ? COLOR_CYAN_BRIGHT : COLOR_PARCHMENT);

            std::string rank_str = "#" + std::to_string(i + 1);
            DrawText(rank_str.c_str(), 55, y, 14, row_col);
            DrawText(s.player_name.c_str(), 135, y, 14, row_col);
            DrawText(std::to_string(s.score).c_str(), 345, y, 14, COLOR_GOLD_BRIGHT);
            DrawText(std::to_string(s.level_reached).c_str(), 475, y, 14, COLOR_PARCHMENT);
            DrawText(s.ship_class.c_str(), 575, y, 14, COLOR_CYAN);
            DrawText(s.difficulty.c_str(), 725, y, 14, COLOR_MUTED);

            y += 32;
        }

        if (m_scores.empty()) {
            DrawText("No pilot records found in database yet. Fly into battle to forge your legend!", 180, 240, 14, COLOR_MUTED);
        }

        m_btn_back.draw(font);
        m_btn_refresh.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::LEADERBOARD; }

private:
    ViewType m_next_view;
    bool m_cloud_mode;
    std::vector<ScoreEntry> m_scores;
    UI::Button m_btn_back;
    UI::Button m_btn_refresh;
};

} // namespace Vimana
