#pragma once
#include <vector>
#include <string>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/db_system.hpp"
#include "systems/account_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class LeaderboardView : public IView {
public:
    LeaderboardView()
        : m_next_view(ViewType::LEADERBOARD),
          m_cloud_mode(true),
          m_diff_filter_idx(0),
          m_is_loading(false),
          m_status_text(""),
          m_btn_mode({ 450, 28, 200, 34 }, "MODE: POSTGRESQL CLOUD", COLOR_GOLD_BRIGHT),
          m_btn_diff({ 660, 28, 200, 34 }, "DIFF: ALL TIERS", COLOR_GOLD_BRIGHT),
          m_btn_back({ 40, 520, 110, 36 }, "BACK", COLOR_MUTED),
          m_btn_refresh({ SCREEN_WIDTH - 200, 520, 160, 36 }, "REFRESH", COLOR_CYAN_BRIGHT)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::LEADERBOARD;
        m_status_text = "";
        m_is_loading = false;
        refresh_scores();
    }

    void refresh_scores() {
        std::string diff = filter_string();
        if (!m_cloud_mode) {
            m_scores = DBSystem::instance().fetch_top_scores(12);
            m_status_text = "Displaying local flight telemetry records";
        } else {
            m_is_loading = true;
            m_status_text = "Querying Sangha Akashic Cloud records...";
            AccountSystem::instance().fetch_top_scores(15, diff, [this](bool success, const std::vector<ScoreEntry>& entries) {
                m_is_loading = false;
                if (success) {
                    m_scores = entries;
                    m_status_text = "Cloud records updated // " + std::to_string(entries.size()) + " pilots listed";
                } else {
                    m_status_text = "Cloud connection failed. Falling back to local cache.";
                    m_scores = DBSystem::instance().fetch_top_scores(12);
                }
            });
        }
    }

    std::string filter_string() const {
        switch (m_diff_filter_idx) {
            case 1: return "easy";
            case 2: return "normal";
            case 3: return "hard";
            case 4: return "hard";
            default: return "all";
        }
    }

    std::string filter_label() const {
        switch (m_diff_filter_idx) {
            case 1: return "DIFF: NOVICE";
            case 2: return "DIFF: KSHATRIYA";
            case 3: return "DIFF: ASURA SLAYER";
            case 4: return "DIFF: CHAKRAVYUHA";
            default: return "DIFF: ALL TIERS";
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }

        // Toggle Cloud / Local mode
        if (m_btn_mode.update(mouse_pos)) {
            m_cloud_mode = !m_cloud_mode;
            m_btn_mode.set_label(m_cloud_mode ? "MODE: POSTGRESQL CLOUD" : "MODE: LOCAL BACKUP");
            m_btn_mode.set_color(m_cloud_mode ? COLOR_GOLD_BRIGHT : COLOR_CYAN_BRIGHT);
            refresh_scores();
        }

        // Cycle Difficulty Filter
        if (m_btn_diff.update(mouse_pos)) {
            m_diff_filter_idx = (m_diff_filter_idx + 1) % 5;
            m_btn_diff.set_label(filter_label());
            refresh_scores();
        }

        if (m_btn_refresh.update(mouse_pos)) {
            refresh_scores();
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header Panel
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "ASTRAL HALL OF VALOR // LEADERBOARD", { 45, 30 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        // Control Buttons in Header
        m_btn_mode.draw(font);
        m_btn_diff.draw(font);

        // Leaderboard Table Panel
        UI::DrawChamferedPanel({ 30, 85, 840, 415 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        // Column Titles
        DrawText("RANK", 55, 102, 11, COLOR_MUTED);
        DrawText("PILOT CALLSIGN", 130, 102, 11, COLOR_MUTED);
        DrawText("SCORE", 345, 102, 11, COLOR_MUTED);
        DrawText("WAVE", 475, 102, 11, COLOR_MUTED);
        DrawText("VESSEL CLASS", 575, 102, 11, COLOR_MUTED);
        DrawText("DIFFICULTY", 725, 102, 11, COLOR_MUTED);

        DrawLine(45, 120, 855, 120, COLOR_MUTED);

        // Status Line inside table
        if (m_is_loading) {
            DrawText("ACCESSING SANGHA AKASHIC CLOUD DATABASE...", 260, 240, 14, COLOR_CYAN_BRIGHT);
        } else if (m_scores.empty()) {
            DrawText("No pilot records found matching query. Fly into battle to forge your legend!", 160, 240, 13, COLOR_MUTED);
        } else {
            int y = 132;
            std::string my_name = DBSystem::instance().player_name();

            for (size_t i = 0; i < m_scores.size() && i < 11; ++i) {
                const auto& s = m_scores[i];
                bool is_me = (s.player_name == my_name);
                Color row_col = (i == 0) ? COLOR_GOLD_BRIGHT : ((i < 3) ? COLOR_CYAN_BRIGHT : (is_me ? COLOR_GREEN_BRIGHT : COLOR_PARCHMENT));

                // Row highlight for current player
                if (is_me) {
                    DrawRectangle(45, y - 2, 810, 26, ColorAlpha(COLOR_GREEN_BRIGHT, 0.12f));
                }

                std::string rank_str = "#" + std::to_string(i + 1);
                DrawText(rank_str.c_str(), 55, y + 4, 13, row_col);
                
                std::string display_name = s.player_name + (is_me ? " [YOU]" : "");
                DrawText(display_name.c_str(), 130, y + 4, 13, row_col);

                DrawText(std::to_string(s.score).c_str(), 345, y + 4, 13, COLOR_GOLD_BRIGHT);
                DrawText(("W" + std::to_string(s.level_reached)).c_str(), 475, y + 4, 13, COLOR_PARCHMENT);
                DrawText(s.ship_class.c_str(), 575, y + 4, 13, COLOR_CYAN);
                DrawText(s.difficulty.c_str(), 725, y + 4, 13, COLOR_MUTED);

                y += 28;
            }
        }

        // Bottom status & navigation
        DrawText(m_status_text.c_str(), 170, 532, 11, COLOR_MUTED);

        m_btn_back.draw(font);
        m_btn_refresh.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::LEADERBOARD; }

private:
    ViewType m_next_view;
    bool m_cloud_mode;
    int m_diff_filter_idx;
    bool m_is_loading;
    std::string m_status_text;

    std::vector<ScoreEntry> m_scores;
    UI::Button m_btn_mode;
    UI::Button m_btn_diff;
    UI::Button m_btn_back;
    UI::Button m_btn_refresh;
};

} // namespace Vimana
