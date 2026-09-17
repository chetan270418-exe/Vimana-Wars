#pragma once
#include <string>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
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
        : m_next_view(is_victory ? ViewType::VICTORY : ViewType::GAME_OVER), 
          m_is_victory(is_victory),
          m_is_new_high_score(false),
          m_btn_replay({ SCREEN_WIDTH / 2.0f - 220, 470, 135, 40 }, "FLY AGAIN", COLOR_GOLD_BRIGHT),
          m_btn_profile({ SCREEN_WIDTH / 2.0f - 75, 470, 150, 40 }, "PILOT PROFILE", COLOR_CYAN_BRIGHT),
          m_btn_menu({ SCREEN_WIDTH / 2.0f + 85, 470, 135, 40 }, "MAIN MENU", COLOR_MUTED)
    {
        init();
    }

    void init() override {
        m_next_view = m_is_victory ? ViewType::VICTORY : ViewType::GAME_OVER;
    }

    void set_results(bool victory, int score, int wave, int kills, int damage, const std::string& ship_name) {
        m_is_victory = victory;
        m_score = score;
        m_wave = wave;
        m_kills = kills;
        m_damage = damage;
        m_ship = ship_name;

        int previous_high = DBSystem::instance().high_score();
        m_is_new_high_score = (score > previous_high && score > 0);

        // Determine Rank
        if (victory || (wave >= 20 && score > 150000)) {
            m_rank = PerformanceRank::S_RANK;
            m_rank_reason = "Transcendent celestial supremacy in battle";
        } else if (wave >= 12 || score > 80000) {
            m_rank = PerformanceRank::A_RANK;
            m_rank_reason = "Valiant performance against the Asura horde";
        } else if (wave >= 6) {
            m_rank = PerformanceRank::B_RANK;
            m_rank_reason = "Honorable sortie with tactical prowess";
        } else {
            m_rank = PerformanceRank::C_RANK;
            m_rank_reason = "Vessel sustained catastrophic structural failure";
        }

        // Save score to SQLite database
        ScoreEntry entry;
        entry.player_name = DBSystem::instance().player_name();
        entry.score = score;
        entry.level_reached = wave;
        entry.ship_class = ship_name;
        entry.kills = kills;
        entry.total_damage = damage;
        entry.duration_seconds = 0.0f;
        DBSystem::instance().insert_score(entry);
        DBSystem::instance().update_high_score(score);
        DBSystem::instance().update_max_wave(wave);
        DBSystem::instance().save_game();
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_replay.update(mouse_pos)) {
            m_next_view = ViewType::CAMPAIGN_MAP;
        } else if (m_btn_profile.update(mouse_pos)) {
            m_next_view = ViewType::PROFILE;
        } else if (m_btn_menu.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Main Result Card
        Color header_col = m_is_victory ? COLOR_GOLD_BRIGHT : COLOR_RED_BRIGHT;
        Rectangle card = { SCREEN_WIDTH / 2.0f - 270, 45, 540, 410 };
        UI::DrawChamferedPanel(card, header_col, COLOR_SURFACE_LOW, 8.0f);

        if (m_is_victory) {
            const char* vic = "MAHAYUDDHA VICTORIOUS!";
            Vector2 v_sz = MeasureTextEx(title_font, vic, 24, 1.0f);
            DrawTextEx(title_font, vic, { (SCREEN_WIDTH - v_sz.x) / 2.0f, card.y + 20 }, 24, 1.0f, COLOR_GOLD_BRIGHT);

            const char* sub = "EMPEROR HIRANYAKASHIPU VANQUISHED - NARASIMHA AWAKENS!";
            Vector2 s_sz = MeasureTextEx(body_font, sub, 11, 1.0f);
            DrawTextEx(body_font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, card.y + 50 }, 11, 1.0f, COLOR_CYAN_BRIGHT);
        } else {
            const char* def = "VIMANA LOST IN ASTRAL VOID";
            Vector2 d_sz = MeasureTextEx(title_font, def, 22, 1.0f);
            DrawTextEx(title_font, def, { (SCREEN_WIDTH - d_sz.x) / 2.0f, card.y + 20 }, 22, 1.0f, COLOR_RED_BRIGHT);

            const char* sub = "THE ASURA ARMADA RECLAIMS THE HEAVENS - REFORGE AT HANGAR";
            Vector2 s_sz = MeasureTextEx(body_font, sub, 11, 1.0f);
            DrawTextEx(body_font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, card.y + 50 }, 11, 1.0f, COLOR_MUTED);
        }

        DrawLine(static_cast<int>(card.x + 25), static_cast<int>(card.y + 72), static_cast<int>(card.x + card.width - 25), static_cast<int>(card.y + 72), COLOR_SURFACE_HIGH);

        // New Personal Best banner
        if (m_is_new_high_score) {
            float pulse = 0.5f + 0.5f * std::sin(GetTime() * 12.0f);
            Rectangle pb_bar = { card.x + 30, card.y + 80, card.width - 60, 26 };
            DrawRectangleRec(pb_bar, ColorAlpha(COLOR_GOLD, 0.25f + 0.15f * pulse));
            UI::DrawStarIcon({ pb_bar.x + 20, pb_bar.y + 13 }, 6.0f, COLOR_GOLD_BRIGHT);
            UI::DrawStarIcon({ pb_bar.x + pb_bar.width - 20, pb_bar.y + 13 }, 6.0f, COLOR_GOLD_BRIGHT);
            const char* pb_text = "NEW ALL-TIME PERSONAL BEST HIGH SCORE!";
            Vector2 pb_sz = MeasureTextEx(title_font, pb_text, 12, 1.0f);
            DrawTextEx(title_font, pb_text, { (SCREEN_WIDTH - pb_sz.x) / 2.0f, pb_bar.y + 7 }, 12, 1.0f, COLOR_GOLD_BRIGHT);
        }

        // Stats Block
        float cy = card.y + (m_is_new_high_score ? 120.0f : 95.0f);
        float lx = card.x + 40.0f;
        float rx = card.x + card.width - 150.0f;

        DrawTextEx(body_font, "FINAL COMBAT SCORE :", { lx, cy }, 13, 1.0f, COLOR_PARCHMENT);
        DrawTextEx(title_font, std::to_string(m_score).c_str(), { rx, cy - 2 }, 16, 1.0f, COLOR_GOLD_BRIGHT);

        cy += 28.0f;
        DrawTextEx(body_font, "HIGHEST WAVE REACHED :", { lx, cy }, 13, 1.0f, COLOR_PARCHMENT);
        DrawTextEx(title_font, ("WAVE " + std::to_string(m_wave)).c_str(), { rx, cy - 2 }, 15, 1.0f, COLOR_CYAN_BRIGHT);

        cy += 28.0f;
        DrawTextEx(body_font, "ASURAS DESTROYED :", { lx, cy }, 13, 1.0f, COLOR_PARCHMENT);
        DrawTextEx(title_font, std::to_string(m_kills).c_str(), { rx, cy - 2 }, 15, 1.0f, COLOR_RED_BRIGHT);

        cy += 28.0f;
        DrawTextEx(body_font, "TOTAL DAMAGE DEALT :", { lx, cy }, 13, 1.0f, COLOR_PARCHMENT);
        DrawTextEx(title_font, std::to_string(m_damage).c_str(), { rx, cy - 2 }, 15, 1.0f, COLOR_ORANGE_BRIGHT);

        cy += 28.0f;
        DrawTextEx(body_font, "VESSEL CLASS :", { lx, cy }, 13, 1.0f, COLOR_PARCHMENT);
        DrawTextEx(title_font, m_ship.c_str(), { rx, cy - 2 }, 15, 1.0f, COLOR_GOLD);

        // Performance Rank Medal Display
        cy += 38.0f;
        Rectangle rank_box = { card.x + 30, cy, card.width - 60, 52 };
        UI::DrawChamferedPanel(rank_box, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);

        const char* rank_letter = (m_rank == PerformanceRank::S_RANK) ? "S" :
                                  (m_rank == PerformanceRank::A_RANK) ? "A" :
                                  (m_rank == PerformanceRank::B_RANK) ? "B" : "C";
        Color rank_color = (m_rank == PerformanceRank::S_RANK) ? COLOR_GOLD_BRIGHT :
                           (m_rank == PerformanceRank::A_RANK) ? COLOR_CYAN_BRIGHT :
                           (m_rank == PerformanceRank::B_RANK) ? COLOR_GREEN_BRIGHT : COLOR_RED_BRIGHT;

        DrawTextEx(title_font, rank_letter, { rank_box.x + 18, rank_box.y + 8 }, 34, 1.0f, rank_color);
        DrawTextEx(body_font, "PERFORMANCE RANK EVALUATION", { rank_box.x + 60, rank_box.y + 10 }, 10, 1.0f, COLOR_MUTED);
        DrawTextEx(body_font, m_rank_reason.c_str(), { rank_box.x + 60, rank_box.y + 26 }, 11, 1.0f, COLOR_PARCHMENT);

        // Action Buttons
        m_btn_replay.draw(title_font);
        m_btn_profile.draw(title_font);
        m_btn_menu.draw(title_font);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = m_is_victory ? ViewType::VICTORY : ViewType::GAME_OVER; }

private:
    ViewType m_next_view;
    bool m_is_victory;
    bool m_is_new_high_score;
    int m_score = 0;
    int m_wave = 1;
    int m_kills = 0;
    int m_damage = 0;
    std::string m_ship = "Pushpaka";
    PerformanceRank m_rank = PerformanceRank::B_RANK;
    std::string m_rank_reason = "";

    UI::Button m_btn_replay;
    UI::Button m_btn_profile;
    UI::Button m_btn_menu;
};

} // namespace Vimana
