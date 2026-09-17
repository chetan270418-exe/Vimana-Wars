#pragma once
#include <string>
#include <vector>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "ui/vedic_theme.hpp"
#include "ui/button.hpp"
#include "systems/asset_manager.hpp"
#include "systems/db_system.hpp"
#include "systems/currency_system.hpp"
#include "systems/account_system.hpp"
#include "entities/ship_archetypes.hpp"

namespace Vimana {

class PlayerCardOverlay {
public:
    PlayerCardOverlay() 
        : m_visible(false),
          m_copied_toast_timer(0.0f),
          m_btn_copy({ SCREEN_WIDTH / 2.0f - 160, 205, 140, 28 }, "COPY ID [C]", COLOR_CYAN_BRIGHT),
          m_btn_close({ SCREEN_WIDTH / 2.0f + 20, 205, 140, 28 }, "CLOSE [P/ESC]", COLOR_MUTED)
    {}

    bool is_visible() const { return m_visible; }
    void set_visible(bool v) { m_visible = v; }
    void toggle() { m_visible = !m_visible; }

    void update(float dt, Vector2 mouse_pos) {
        if (!m_visible) return;

        if (m_copied_toast_timer > 0.0f) {
            m_copied_toast_timer -= dt;
        }

        if (IsKeyPressed(KEY_P) || IsKeyPressed(KEY_ESCAPE)) {
            m_visible = false;
            return;
        }

        // Copy ID to clipboard
        if (IsKeyPressed(KEY_C) || m_btn_copy.update(mouse_pos)) {
            std::string gid = AccountSystem::instance().game_id();
            SetClipboardText(gid.c_str());
            m_copied_toast_timer = 2.0f;
        }

        if (m_btn_close.update(mouse_pos)) {
            m_visible = false;
        }
    }

    void draw(Font title_f, Font body_f) {
        if (!m_visible) return;

        // Dark ambient backdrop
        DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 0, 0, 0, 190 });

        Rectangle card = { SCREEN_WIDTH / 2.0f - 260, 85, 520, 430 };
        UI::DrawYantraPanel(card, COLOR_GOLD_BRIGHT, COLOR_SURFACE_HIGH, 8.0f, true);

        // Header Title
        UI::DrawVedicHeading(title_f, "PILOT IDENTIFICATION DOSSIER", { card.x + 40, card.y + 18 }, 18, COLOR_GOLD_BRIGHT);
        DrawLine(static_cast<int>(card.x + 25), static_cast<int>(card.y + 45), static_cast<int>(card.x + card.width - 25), static_cast<int>(card.y + 45), COLOR_MUTED);

        // Pilot Callsign & Rank
        std::string callsign = DBSystem::instance().player_name();
        int max_wave = DBSystem::instance().max_wave();
        std::string rank_str = "INITIATE";
        if (max_wave >= 30) rank_str = "MAHAMAHESHWARA (VIMANA MASTER)";
        else if (max_wave >= 20) rank_str = "ASURA SLAYER (COMMANDER)";
        else if (max_wave >= 10) rank_str = "KSHATRIYA (WARRIOR)";
        else if (max_wave >= 5)  rank_str = "ASTRAL PILOT (VANGUARD)";

        DrawText("CALLSIGN // RANK:", static_cast<int>(card.x + 30), static_cast<int>(card.y + 55), 9, COLOR_MUTED);
        DrawTextEx(title_f, callsign.c_str(), { card.x + 30, card.y + 70 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
        DrawTextEx(body_f, rank_str.c_str(), { card.x + 30, card.y + 96 }, 12, 1.0f, COLOR_CYAN_BRIGHT);

        // Dynamic Game ID Display Box
        Rectangle id_box = { card.x + 30, card.y + 125, card.width - 60, 70 };
        UI::DrawChamferedPanel(id_box, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 4.0f);
        DrawText("SANGHA NETWORK GAME ID (SHARE WITH SQUADMATES):", static_cast<int>(id_box.x + 14), static_cast<int>(id_box.y + 10), 10, COLOR_MUTED);
        
        std::string gid = AccountSystem::instance().game_id();
        DrawTextEx(title_f, gid.c_str(), { id_box.x + 14, id_box.y + 28 }, 24, 2.0f, COLOR_GOLD_BRIGHT);

        // Account status pill
        std::string acc_type = AccountSystem::instance().is_logged_in() ? "[ONLINE SANGHA ACCOUNT]" : "[OFFLINE GUEST PILOT]";
        Color acc_col = AccountSystem::instance().is_logged_in() ? COLOR_GREEN_BRIGHT : COLOR_ORANGE_BRIGHT;
        DrawText(acc_type.c_str(), static_cast<int>(id_box.x + id_box.width - 190), static_cast<int>(id_box.y + 35), 10, acc_col);

        // Buttons: Copy ID & Close
        m_btn_copy.draw(title_f);
        m_btn_close.draw(title_f);

        if (m_copied_toast_timer > 0.0f) {
            DrawText("COPIED TO CLIPBOARD!", static_cast<int>(card.x + card.width / 2.0f - 75), static_cast<int>(card.y + 240), 11, COLOR_GREEN_BRIGHT);
        }

        // Stats Matrix (2x2 Grid)
        float grid_y = card.y + 265;
        float col_w = (card.width - 70) / 2.0f;

        // Stat 1: Max Wave Reached
        Rectangle s1 = { card.x + 30, grid_y, col_w, 58 };
        UI::DrawChamferedPanel(s1, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
        DrawText("MAX CAMPAIGN WAVE", static_cast<int>(s1.x + 12), static_cast<int>(s1.y + 8), 9, COLOR_MUTED);
        std::string w_txt = "WAVE " + std::to_string(max_wave) + " / 30";
        DrawTextEx(title_f, w_txt.c_str(), { s1.x + 12, s1.y + 24 }, 16, 1.0f, COLOR_GOLD);

        // Stat 2: High Score
        Rectangle s2 = { card.x + 40 + col_w, grid_y, col_w, 58 };
        UI::DrawChamferedPanel(s2, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
        DrawText("CAREER HIGH SCORE", static_cast<int>(s2.x + 12), static_cast<int>(s2.y + 8), 9, COLOR_MUTED);
        std::string hs_txt = std::to_string(DBSystem::instance().high_score()) + " PTS";
        DrawTextEx(title_f, hs_txt.c_str(), { s2.x + 12, s2.y + 24 }, 16, 1.0f, COLOR_GOLD_BRIGHT);

        // Stat 3: Fleet Unlocks
        int unlocked_ships = 0;
        for (const auto& s : SHIP_FLEET) {
            if (CurrencySystem::instance().is_ship_unlocked(s.id, max_wave)) unlocked_ships++;
        }
        Rectangle s3 = { card.x + 30, grid_y + 68, col_w, 58 };
        UI::DrawChamferedPanel(s3, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
        DrawText("COMMISSIONED VIMANAS", static_cast<int>(s3.x + 12), static_cast<int>(s3.y + 8), 9, COLOR_MUTED);
        std::string sh_txt = std::to_string(unlocked_ships) + " / " + std::to_string(SHIP_FLEET.size()) + " SHIPS";
        DrawTextEx(title_f, sh_txt.c_str(), { s3.x + 12, s3.y + 24 }, 16, 1.0f, COLOR_CYAN_BRIGHT);

        // Stat 4: Prana Shards Balance
        Rectangle s4 = { card.x + 40 + col_w, grid_y + 68, col_w, 58 };
        UI::DrawChamferedPanel(s4, COLOR_MUTED, COLOR_SURFACE_MID, 4.0f);
        DrawText("ASTRAL PRANA TREASURY", static_cast<int>(s4.x + 12), static_cast<int>(s4.y + 8), 9, COLOR_MUTED);
        std::string pr_txt = std::to_string(CurrencySystem::instance().prana_shards()) + " SHARDS";
        DrawTextEx(title_f, pr_txt.c_str(), { s4.x + 12, s4.y + 24 }, 16, 1.0f, COLOR_GREEN_BRIGHT);

        // Footer hint
        DrawText("PRESS [P] OR [ESC] TO CLOSE DOSSIER", static_cast<int>(card.x + card.width / 2.0f - 110), static_cast<int>(card.y + card.height - 20), 10, COLOR_MUTED);
    }

private:
    bool m_visible;
    float m_copied_toast_timer;
    UI::Button m_btn_copy;
    UI::Button m_btn_close;
};

} // namespace Vimana
