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
#include "entities/ship_archetypes.hpp"
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

    void set_results(const WaveResult& result, bool is_final_wave = false, bool campaign_complete = false) {
        m_result = result;
        m_is_final = is_final_wave;
        m_campaign_complete = campaign_complete;
        m_timer = 0.0f;
        m_sfx_played = false;

        if (m_campaign_complete) {
            m_btn_continue = UI::Button({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 80, 280, 44 }, "CELESTIAL VICTORY // DEBRIEF >>", COLOR_GOLD_BRIGHT);
        } else if (m_is_final) {
            m_btn_continue = UI::Button({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 80, 280, 44 }, "ENTER NEXT ACT // DRAFT >>", COLOR_GOLD_BRIGHT);
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
            m_next_view = m_campaign_complete ? ViewType::VICTORY : ViewType::BOON_SELECT;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Banner Title
        const int act = CampaignActForWave(m_result.wave_num);
        const int act_wave = CampaignWaveWithinAct(m_result.wave_num);
        std::string title = (m_is_final ? "ACT " + std::to_string(act) + " COMPLETE // " : "ACT " + std::to_string(act) + " · ") +
                            "WAVE " + std::to_string(act_wave) + " CLEARED";
        Vector2 t_sz = MeasureTextEx(title_font, title.c_str(), 22, 1.0f);
        DrawTextEx(title_font, title.c_str(), { (SCREEN_WIDTH - t_sz.x) / 2.0f, 38 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        const char* sub = m_campaign_complete ? "ALL 10 ACTS CONQUERED // CELESTIAL ARMADA VICTORY" :
                          m_is_final ? "ACT COMPLETE // HOSTILE ARMADA ESCALATION INCOMING" :
                                       "ASTRAL TELEMETRY BREAKDOWN - COMBAT COMMENDATIONS";
        Vector2 s_sz = MeasureTextEx(body_font, sub, 11, 1.0f);
        DrawTextEx(body_font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 68 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

        // Main Performance Card
        Rectangle panel = { SCREEN_WIDTH / 2.0f - 300, 105, 600, 365 };
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
        DrawTextEx(body_font, "PERFORMANCE", { rank_box.x + 38, rank_box.y + 14 }, 11, 1.0f, COLOR_MUTED);

        // Big Rank Letter
        Vector2 letter_sz = MeasureTextEx(title_font, rank_letter, 64, 2.0f);
        DrawTextEx(title_font, rank_letter, { rank_box.x + (rank_box.width - letter_sz.x) / 2.0f, rank_box.y + 38 }, 64, 2.0f, rank_color);

        Vector2 rt_sz = MeasureTextEx(title_font, rank_title, 11, 1.0f);
        DrawTextEx(title_font, rank_title, { rank_box.x + (rank_box.width - rt_sz.x) / 2.0f, rank_box.y + 130 }, 11, 1.0f, rank_color);

        // Metrics breakdown roll-up animation
        float roll = std::min(1.0f, m_timer / 0.5f);
        float py = panel.y + 35;
        float px = panel.x + 30;

        auto draw_row = [&](const char* label, const std::string& val, Color val_col) {
            DrawTextEx(body_font, label, { px, py }, 12, 1.0f, COLOR_PARCHMENT);
            DrawTextEx(title_font, val.c_str(), { px + 225, py - 1 }, 13, 1.0f, val_col);
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
        DrawTextEx(body_font, "SECTOR SCORE BOUNTY:", { px, py }, 13, 1.0f, COLOR_GOLD);
        DrawTextEx(title_font, ("+" + std::to_string(display_score)).c_str(), { px + 225, py - 1 }, 15, 1.0f, COLOR_GOLD_BRIGHT);
        py += 32;

        int display_prana = static_cast<int>(m_result.prana_earned * roll);
        DrawTextEx(body_font, "PRANA SHARDS HARVESTED:", { px, py }, 13, 1.0f, COLOR_CYAN_BRIGHT);
        DrawTextEx(title_font, ("+" + std::to_string(display_prana) + " SHARDS").c_str(), { px + 225, py - 1 }, 15, 1.0f, COLOR_CYAN_BRIGHT);

        if (!m_result.boss_ship_unlocked.empty()) {
            const ShipArchetype* reward = GetShipArchetype(m_result.boss_ship_unlocked);
            const std::string reward_text = "BOSS SALVAGE UNLOCKED // " + reward->name + "  ·  HANGAR READY";
            UI::DrawChamferedPanel({ panel.x + 25, panel.y + 286, panel.width - 50, 38 }, COLOR_GOLD_BRIGHT, COLOR_SURFACE_MID, 4.0f);
            const Vector2 reward_size = MeasureTextEx(title_font, reward_text.c_str(), 11, 1.0f);
            DrawTextEx(title_font, reward_text.c_str(), { panel.x + (panel.width - reward_size.x) / 2.0f, panel.y + 298 }, 11, 1.0f, COLOR_GOLD_BRIGHT);
        }

        // Action button
        m_btn_continue.draw(title_font);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::WAVE_CLEAR; }

private:
    ViewType m_next_view;
    WaveResult m_result;
    bool m_is_final = false;
    bool m_campaign_complete = false;
    float m_timer = 0.0f;
    bool m_sfx_played = false;

    UI::Button m_btn_continue;
};

} // namespace Vimana
