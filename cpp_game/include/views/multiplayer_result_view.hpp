#pragma once
#include <string>
#include <vector>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/db_system.hpp"
#include "systems/network_manager.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class MultiplayerResultView : public IView {
public:
    MultiplayerResultView()
        : m_next_view(ViewType::MULTIPLAYER_RESULT),
          m_btn_rematch({ SCREEN_WIDTH / 2.0f - 220, 480, 135, 40 }, "REMATCH", COLOR_GOLD_BRIGHT),
          m_btn_lobby({ SCREEN_WIDTH / 2.0f - 75, 480, 150, 40 }, "SQUAD LOBBY", COLOR_CYAN_BRIGHT),
          m_btn_menu({ SCREEN_WIDTH / 2.0f + 85, 480, 135, 40 }, "MAIN MENU", COLOR_MUTED)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::MULTIPLAYER_RESULT;

        // Squad members stats breakdown
        m_squad_stats = {
            { DBSystem::instance().player_name(), "GARUDA (MOBILITY)", 148500, 192, 28, 2, "DAMAGE MASTER ★" },
            { "ROHAN", "TRIPURA (TANK)", 92400, 114, 45, 4, "REVIVAL MASTER ★" },
            { "ARYA", "VAJRA (DPS)", 116200, 142, 31, 1, "COMBO MASTER ★" },
            { "DEV", "KAMADHENU (SUPPORT)", 48000, 68, 62, 3, "SUPPORT ACE ★" }
        };
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_rematch.update(mouse_pos)) {
            m_next_view = ViewType::GAMEPLAY;
        } else if (m_btn_lobby.update(mouse_pos)) {
            m_next_view = ViewType::MULTIPLAYER_LOBBY;
        } else if (m_btn_menu.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header Panel
        UI::DrawChamferedPanel({ 30, 20, 840, 55 }, COLOR_GOLD_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "SANGHA SQUADRON DEBRIEFING // VICTORY AT LANKA", { 45, 28 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        DrawText("ALL OBJECTIVES SECURED • TITAN HIRANYAKASHIPU VANQUISHED", 45, 52, 10, COLOR_CYAN_BRIGHT);
        DrawText("TEAM SCORE: 405,100", SCREEN_WIDTH - 240, 36, 16, COLOR_GOLD_BRIGHT);

        // Squad Performance Cards (4 columns)
        float start_x = 35.0f;
        float card_w = 200.0f;
        float card_h = 370.0f;
        float gap = 10.0f;
        float y = 90.0f;

        for (size_t i = 0; i < m_squad_stats.size(); ++i) {
            const auto& stat = m_squad_stats[i];
            Rectangle card = { start_x + i * (card_w + gap), y, card_w, card_h };
            Color border = (i == 0) ? COLOR_GOLD_BRIGHT : COLOR_CYAN_BRIGHT;

            UI::DrawChamferedPanel(card, border, COLOR_SURFACE_LOW, 6.0f);

            float cx = card.x + 12.0f;
            float cy = card.y + 16.0f;

            // Callsign & Role
            DrawTextEx(font, stat.name.c_str(), { cx, cy }, 16, 1.0f, (i == 0) ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            cy += 22.0f;
            DrawText(stat.role.c_str(), cx, cy, 9, COLOR_CYAN_BRIGHT);

            DrawLine(cx, cy + 18, card.x + card.width - 12, cy + 18, COLOR_SURFACE_HIGH);

            // Metrics
            cy += 30.0f;
            DrawText("COMBAT METRICS:", cx, cy, 10, COLOR_MUTED);

            cy += 20.0f;
            DrawText("TOTAL DAMAGE :", cx, cy, 11, COLOR_PARCHMENT);
            DrawText(std::to_string(stat.damage).c_str(), cx + 105, cy, 12, COLOR_GOLD_BRIGHT);

            cy += 22.0f;
            DrawText("ASURA KILLS  :", cx, cy, 11, COLOR_PARCHMENT);
            DrawText(std::to_string(stat.kills).c_str(), cx + 105, cy, 12, COLOR_RED_BRIGHT);

            cy += 22.0f;
            DrawText("TEAM ASSISTS :", cx, cy, 11, COLOR_PARCHMENT);
            DrawText(std::to_string(stat.assists).c_str(), cx + 105, cy, 12, COLOR_CYAN_BRIGHT);

            cy += 22.0f;
            DrawText("REVIVES DONE :", cx, cy, 11, COLOR_PARCHMENT);
            DrawText(std::to_string(stat.revives).c_str(), cx + 105, cy, 12, COLOR_GREEN_BRIGHT);

            // Honors Badge
            cy += 40.0f;
            Rectangle badge_box = { card.x + 10, cy, card.width - 20, 48 };
            UI::DrawChamferedPanel(badge_box, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);
            DrawText("SQUAD CITATION AWARD", badge_box.x + 8, badge_box.y + 6, 8, COLOR_MUTED);
            DrawTextEx(font, stat.citation.c_str(), { badge_box.x + 8, badge_box.y + 20 }, 12, 1.0f, COLOR_GOLD_BRIGHT);
        }

        m_btn_rematch.draw(font);
        m_btn_lobby.draw(font);
        m_btn_menu.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MULTIPLAYER_RESULT; }

private:
    struct SquadMemberStat {
        std::string name;
        std::string role;
        int damage;
        int kills;
        int assists;
        int revives;
        std::string citation;
    };

    ViewType m_next_view;
    std::vector<SquadMemberStat> m_squad_stats;

    UI::Button m_btn_rematch;
    UI::Button m_btn_lobby;
    UI::Button m_btn_menu;
};

} // namespace Vimana
