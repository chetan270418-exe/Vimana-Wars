#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "systems/currency_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class WaveClearView : public IView {
public:
    WaveClearView() 
        : m_next_view(ViewType::WAVE_CLEAR),
          m_timer(0.0f),
          m_btn_continue({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 80, 280, 44 }, "DRAFT DIVINE BOON >>", COLOR_GOLD_BRIGHT)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::WAVE_CLEAR;
        m_timer = 0.0f;
        m_sfx_played = false;
    }

    void set_results(const WaveResult& result, bool is_final_wave = false) {
        m_result = result;
        m_is_final = is_final_wave;
        m_timer = 0.0f;
        m_sfx_played = false;

        if (m_is_final) {
            m_btn_continue = UI::Button({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 80, 280, 44 }, "CELESTIAL VICTORY >>", COLOR_GOLD_BRIGHT);
        } else {
            m_btn_continue = UI::Button({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 80, 280, 44 }, "DRAFT DIVINE BOON >>", COLOR_GOLD_BRIGHT);
        }
    }

    const WaveResult& results() const { return m_result; }

    void update(float dt, Vector2 mouse_pos) override {
        m_timer += dt;

        if (!m_sfx_played && m_timer > 0.6f) {
            SoundSystem::instance().play_sfx("wave_clear.wav");
            m_sfx_played = true;
        }

        if (m_btn_continue.update(mouse_pos) || IsKeyPressed(KEY_ENTER) || IsKeyPressed(KEY_SPACE)) {
            if (m_is_final) {
                m_next_view = ViewType::VICTORY;
            } else {
                m_next_view = ViewType::BOON_SELECT;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Banner Title
        std::string title = "WAVE " + std::to_string(m_result.wave_num) + " CLEARED // SECTOR CONQUERED";
        Vector2 t_sz = MeasureTextEx(font, title.c_str(), 24, 1.0f);
        DrawTextEx(font, title.c_str(), { (SCREEN_WIDTH - t_sz.x) / 2.0f, 40 }, 24, 1.0f, COLOR_GOLD_BRIGHT);

        const char* sub = "ASTRAL TELEMETRY BREAKDOWN • COMBAT COMMENDATIONS";
        Vector2 s_sz = MeasureTextEx(font, sub, 12, 1.0f);
        DrawTextEx(font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 72 }, 12, 1.0f, COLOR_CYAN_BRIGHT);

        // Main Performance Card
        Rectangle panel = { SCREEN_WIDTH / 2.0f - 300, 110, 600, 360 };
        UI::DrawChamferedPanel(panel, COLOR_GOLD, COLOR_SURFACE_LOW, 8.0f);

        // Rank Badge on Right
        Rectangle rank_box = { panel.x + 390, panel.y + 35, 170, 170 };
        Color rank_color = COLOR_GOLD_BRIGHT;
        const char* rank_letter = "S";
        const char* rank_title = "SUPREME ASTRA";

        if (m_result.rank == PerformanceRank::S_RANK) {
            rank_color = COLOR_GOLD_BRIGHT;
            rank_letter = "S";
            rank_title = "TRANSCENDENT";
        } else if (m_result.rank == PerformanceRank::A_RANK) {
            rank_color = COLOR_CYAN_BRIGHT;
            rank_letter = "A";
            rank_title = "CELESTIAL ACE";
        } else if (m_result.rank == PerformanceRank::B_RANK) {
            rank_color = COLOR_GREEN_BRIGHT;
            rank_letter = "B";
            rank_title = "WARRIOR OF SWARGA";
        } else {
            rank_color = COLOR_ORANGE_BRIGHT;
            rank_letter = "C";
            rank_title = "SURVIVOR";
        }

        UI::DrawChamferedPanel(rank_box, rank_color, COLOR_SURFACE_MID, 6.0f);
        DrawTextEx(font, "PERFORMANCE", { rank_box.x + 32, rank_box.y + 14 }, 12, 1.0f, COLOR_MUTED);

        // Big Rank Letter
        Vector2 letter_sz = MeasureTextEx(font, rank_letter, 72, 2.0f);
        DrawTextEx(font, rank_letter, { rank_box.x + (rank_box.width - letter_sz.x) / 2.0f, rank_box.y + 35 }, 72, 2.0f, rank_color);

        Vector2 rt_sz = MeasureTextEx(font, rank_title, 11, 1.0f);
        DrawTextEx(font, rank_title, { rank_box.x + (rank_box.width - rt_sz.x) / 2.0f, rank_box.y + 130 }, 11, 1.0f, rank_color);

        // Metrics breakdown roll-up animation
        float roll = std::min(1.0f, m_timer / 0.5f);
        float py = panel.y + 35;
        float px = panel.x + 30;

        auto draw_row = [&](const char* label, const std::string& val, Color val_col) {
            DrawText(label, static_cast<int>(px), static_cast<int>(py), 13, COLOR_PARCHMENT);
            DrawText(val.c_str(), static_cast<int>(px + 230), static_cast<int>(py), 13, val_col);
            py += 32;
        };

        int display_enemies = static_cast<int>(m_result.enemies_destroyed * roll);
        draw_row("HOSTILES PURGED:", std::to_string(display_enemies) + " ASURAS", COLOR_GOLD_BRIGHT);

        int display_combo = static_cast<int>(m_result.max_combo * roll);
        draw_row("MAXIMUM COMBO:", "x" + std::to_string(display_combo), COLOR_CYAN_BRIGHT);

        int display_dmg = static_cast<int>(m_result.damage_taken * roll);
        draw_row("HULL DAMAGE TAKEN:", std::to_string(display_dmg) + " HP", display_dmg == 0 ? COLOR_GREEN_BRIGHT : COLOR_RED_BRIGHT);

        if (m_result.no_damage) {
            draw_row("UNTOUCHED VALOR BONUS:", "+100 SCORE", COLOR_GOLD_BRIGHT);
        } else {
            draw_row("SECTOR DEFENSE ACCURACY:", std::to_string(m_result.accuracy_pct) + "%", COLOR_PARCHMENT);
        }

        DrawLine(static_cast<int>(px), static_cast<int>(py), static_cast<int>(panel.x + panel.width - 30), static_cast<int>(py), COLOR_MUTED);
        py += 15;

        // Bottom Totals
        int display_score = static_cast<int>(m_result.score_earned * roll);
        DrawText("SECTOR SCORE BOUNTY:", static_cast<int>(px), static_cast<int>(py), 15, COLOR_GOLD);
        DrawText(("+" + std::to_string(display_score)).c_str(), static_cast<int>(px + 230), static_cast<int>(py), 16, COLOR_GOLD_BRIGHT);
        py += 32;

        int display_prana = static_cast<int>(m_result.prana_earned * roll);
        DrawText("PRANA SHARDS HARVESTED:", static_cast<int>(px), static_cast<int>(py), 15, COLOR_CYAN_BRIGHT);
        DrawText(("+" + std::to_string(display_prana) + " SHARDS").c_str(), static_cast<int>(px + 230), static_cast<int>(py), 16, COLOR_CYAN_BRIGHT);

        // Action button
        m_btn_continue.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::WAVE_CLEAR; }

private:
    ViewType m_next_view;
    WaveResult m_result;
    bool m_is_final = false;
    float m_timer = 0.0f;
    bool m_sfx_played = false;

    UI::Button m_btn_continue;
};

} // namespace Vimana
