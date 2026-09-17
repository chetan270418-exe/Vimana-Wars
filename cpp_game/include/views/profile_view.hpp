#pragma once
#include <string>
#include <vector>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/db_system.hpp"
#include "systems/currency_system.hpp"
#include "systems/asset_manager.hpp"
#include "entities/ship_archetypes.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class ProfileView : public IView {
public:
    ProfileView() 
        : m_next_view(ViewType::PROFILE),
          m_btn_back({ 50, 520, 110, 36 }, "BACK", COLOR_MUTED)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::PROFILE;
        m_history = DBSystem::instance().fetch_match_history(8);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "ASTRAL PILOT DOSSIER // SERVICE RECORDS", { 45, 30 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        // ── LEFT PANEL: PILOT PROFILE ──────────────────────────────────────────
        Rectangle left_panel = { 30, 85, 350, 420 };
        UI::DrawChamferedPanel(left_panel, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);

        float lx = left_panel.x + 20.0f;
        float ly = left_panel.y + 20.0f;

        DrawText("PILOT IDENTITY RECORD", lx, ly, 10, COLOR_MUTED);
        ly += 16.0f;
        std::string name_line = DBSystem::instance().player_name() + " // " + PILOT_ID;
        DrawTextEx(font, name_line.c_str(), { lx, ly }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        ly += 30.0f;
        DrawText("SQUADRON FLEET", lx, ly, 10, COLOR_MUTED);
        ly += 14.0f;
        DrawText(PILOT_SQUADRON, lx, ly, 13, COLOR_CYAN_BRIGHT);

        ly += 26.0f;
        DrawLine(lx, ly, left_panel.x + left_panel.width - 20, ly, COLOR_SURFACE_HIGH);

        ly += 15.0f;
        DrawText("CAREER STATISTICS", lx, ly, 11, COLOR_GOLD);

        ly += 22.0f;
        DrawText("LIFETIME HIGH SCORE :", lx, ly, 12, COLOR_PARCHMENT);
        DrawText(std::to_string(DBSystem::instance().high_score()).c_str(), lx + 180, ly, 13, COLOR_GOLD_BRIGHT);

        ly += 24.0f;
        DrawText("HIGHEST REALM WAVE  :", lx, ly, 12, COLOR_PARCHMENT);
        DrawText(("WAVE " + std::to_string(DBSystem::instance().max_wave())).c_str(), lx + 180, ly, 13, COLOR_CYAN_BRIGHT);

        ly += 24.0f;
        DrawText("ASTRAL PRANA SHARDS :", lx, ly, 12, COLOR_PARCHMENT);
        DrawText((std::to_string(CurrencySystem::instance().prana_shards()) + " SHARDS").c_str(), lx + 180, ly, 13, COLOR_GREEN_BRIGHT);

        // Count unlocked ships
        int unlocked_count = 0;
        for (const auto& ship : SHIP_FLEET) {
            if (CurrencySystem::instance().is_ship_unlocked(ship.id, DBSystem::instance().max_wave())) {
                unlocked_count++;
            }
        }
        ly += 24.0f;
        DrawText("FLEET COMMISSIONED  :", lx, ly, 12, COLOR_PARCHMENT);
        DrawText((std::to_string(unlocked_count) + " / " + std::to_string(SHIP_FLEET.size()) + " SHIPS").c_str(), lx + 180, ly, 13, COLOR_GOLD);

        ly += 36.0f;
        // Pilot Rank Badge
        Rectangle rank_box = { lx, ly, left_panel.width - 40, 56 };
        UI::DrawChamferedPanel(rank_box, COLOR_GOLD_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        DrawText("HONORARY CELESTIAL RANK", rank_box.x + 12, rank_box.y + 8, 10, COLOR_MUTED);
        const char* rank_title = (DBSystem::instance().max_wave() >= 25) ? "MAHAYUDDHA SUPREME DEVA" :
                                 (DBSystem::instance().max_wave() >= 15) ? "ASTRAL ASURA SLAYER" :
                                 (DBSystem::instance().max_wave() >= 8)  ? "KSHATRIYA COMMANDER" : "SADHAKA INITIATE";
        DrawTextEx(font, rank_title, { rank_box.x + 12, rank_box.y + 24 }, 15, 1.0f, COLOR_GOLD_BRIGHT);

        // ── RIGHT PANEL: MATCH HISTORY ─────────────────────────────────────────
        Rectangle right_panel = { 400, 85, 470, 420 };
        UI::DrawChamferedPanel(right_panel, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        DrawTextEx(font, "COMBAT MISSION LOGS // RECENT SORTIES", { right_panel.x + 20, right_panel.y + 15 }, 16, 1.0f, COLOR_GOLD_BRIGHT);
        DrawLine(right_panel.x + 20, right_panel.y + 40, right_panel.x + right_panel.width - 20, right_panel.y + 40, COLOR_SURFACE_HIGH);

        // Table Column Headers
        float ry = right_panel.y + 50.0f;
        DrawText("WAVE", right_panel.x + 20, ry, 10, COLOR_MUTED);
        DrawText("VESSEL", right_panel.x + 85, ry, 10, COLOR_MUTED);
        DrawText("SCORE", right_panel.x + 195, ry, 10, COLOR_MUTED);
        DrawText("KILLS", right_panel.x + 300, ry, 10, COLOR_MUTED);
        DrawText("RANK", right_panel.x + 380, ry, 10, COLOR_MUTED);

        DrawLine(right_panel.x + 20, ry + 16, right_panel.x + right_panel.width - 20, ry + 16, COLOR_SURFACE_MID);

        ry += 24.0f;

        if (m_history.empty()) {
            DrawText("NO PRIOR MISSION DATA RECORDED IN ASTRAL ARCHIVES", right_panel.x + 30, ry + 40, 11, COLOR_MUTED);
        } else {
            for (const auto& rec : m_history) {
                // Row background
                Rectangle row_rec = { right_panel.x + 15, ry - 3, right_panel.width - 30, 32 };
                UI::DrawChamferedPanel(row_rec, COLOR_SURFACE_MID, COLOR_SURFACE_MID, 2.0f);

                DrawText(("W" + std::to_string(rec.wave)).c_str(), right_panel.x + 20, ry + 6, 12, COLOR_CYAN_BRIGHT);
                DrawText(rec.ship_id.substr(0, 10).c_str(), right_panel.x + 85, ry + 6, 12, COLOR_PARCHMENT);
                DrawText(std::to_string(rec.score).c_str(), right_panel.x + 195, ry + 6, 12, COLOR_GOLD_BRIGHT);
                DrawText(std::to_string(rec.kills).c_str(), right_panel.x + 300, ry + 6, 12, COLOR_RED_BRIGHT);

                // Rank Medal
                const char* r_str = (rec.rank == PerformanceRank::S_RANK) ? "S" :
                                    (rec.rank == PerformanceRank::A_RANK) ? "A" :
                                    (rec.rank == PerformanceRank::B_RANK) ? "B" : "C";
                Color r_col = (rec.rank == PerformanceRank::S_RANK) ? COLOR_GOLD_BRIGHT :
                              (rec.rank == PerformanceRank::A_RANK) ? COLOR_CYAN_BRIGHT :
                              (rec.rank == PerformanceRank::B_RANK) ? COLOR_GREEN_BRIGHT : COLOR_MUTED;
                DrawText(r_str, right_panel.x + 395, ry + 4, 15, r_col);

                ry += 38.0f;
            }
        }

        m_btn_back.draw(font);
        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::PROFILE; }

private:
    ViewType m_next_view;
    std::vector<MatchRecord> m_history;
    UI::Button m_btn_back;
};

} // namespace Vimana
