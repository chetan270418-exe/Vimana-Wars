#pragma once
#include <string>
#include <vector>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"

namespace Vimana {

class DifficultyView : public IView {
public:
    DifficultyView() 
        : m_next_view(ViewType::DIFFICULTY_SELECT), 
          m_selected_difficulty(Difficulty::KSHATRIYA),
          m_btn_back({ 50, 520, 110, 36 }, "BACK", COLOR_MUTED)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::DIFFICULTY_SELECT;
        m_tier_cards.clear();        float start_x = 50.0f;
        float card_w = 185.0f;
        float card_h = 360.0f;
        float gap = 20.0f;
        float y = 130.0f;

        for (int i = 0; i < 4; ++i) {
            Rectangle rec = { start_x + i * (card_w + gap), y, card_w, card_h };
            Color accent = COLOR_GOLD_BRIGHT;
            if (i == 0) accent = COLOR_GREEN_BRIGHT;
            else if (i == 1) accent = COLOR_CYAN_BRIGHT;
            else if (i == 2) accent = COLOR_ORANGE_BRIGHT;
            else if (i == 3) accent = COLOR_RED_BRIGHT;

            m_tier_cards.push_back({ rec, DIFFICULTY_PROFILES[i], accent });
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::CAMPAIGN_MAP;
            return;
        }

        for (size_t i = 0; i < m_tier_cards.size(); ++i) {
            if (CheckCollisionPointRec(mouse_pos, m_tier_cards[i].bounds)) {
                if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                    m_selected_difficulty = m_tier_cards[i].profile.tier;
                    m_next_view = ViewType::LOADOUT;
                }
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 60 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "SELECT CAMPAIGN DIFFICULTY // DHARMA OF COMBAT", { 50, 32 }, 22, 1.0f, COLOR_GOLD_BRIGHT);
        DrawText("ENEMIES SCALE IN STRENGTH, SPEED AND ELITE AGGRESSION", 52, 60, 10, COLOR_CYAN_BRIGHT);

        Vector2 mouse = GetMousePosition();

        // 4 Difficulty Tier Cards
        for (const auto& card : m_tier_cards) {
            bool is_hover = CheckCollisionPointRec(mouse, card.bounds);
            Color border = is_hover ? card.accent : COLOR_SURFACE_HIGH;
            Color bg = is_hover ? COLOR_SURFACE_HIGH : COLOR_SURFACE_LOW;

            UI::DrawChamferedPanel(card.bounds, border, bg, 6.0f);

            float cx = card.bounds.x + 12.0f;
            float cy = card.bounds.y + 15.0f;

            // Tier Title
            DrawTextEx(font, card.profile.name, { cx, cy }, 18, 1.0f, card.accent);
            DrawLine(cx, cy + 24, card.bounds.x + card.bounds.width - 12, cy + 24, COLOR_SURFACE_MID);

            // Flavor text
            cy += 35.0f;
            DrawText(card.profile.flavor, cx, cy, 9, COLOR_PARCHMENT);

            // Multipliers Specs
            cy += 65.0f;
            DrawText("COMBAT METRICS:", cx, cy, 10, COLOR_MUTED);

            cy += 18.0f;
            std::string hp_str = "ENEMY HP: " + std::to_string(static_cast<int>(card.profile.enemy_hp_mult * 100)) + "%";
            DrawText(hp_str.c_str(), cx, cy, 11, COLOR_GOLD_BRIGHT);

            cy += 18.0f;
            std::string spd_str = "SPEED: " + std::to_string(static_cast<int>(card.profile.bullet_speed_mult * 100)) + "%";
            DrawText(spd_str.c_str(), cx, cy, 11, COLOR_CYAN_BRIGHT);

            cy += 18.0f;
            std::string elite_str = "ELITE CHANCE: +" + std::to_string(static_cast<int>(card.profile.elite_chance_bonus * 100)) + "%";
            DrawText(elite_str.c_str(), cx, cy, 11, card.accent);

            // Click to deploy badge
            Rectangle deploy_badge = { card.bounds.x + 15, card.bounds.y + card.bounds.height - 45, card.bounds.width - 30, 30 };
            UI::DrawChamferedPanel(deploy_badge, card.accent, is_hover ? card.accent : COLOR_SURFACE_MID, 4.0f);
            Color text_col = is_hover ? COLOR_OBSIDIAN : card.accent;
            DrawText("SELECT TIER", deploy_badge.x + 25, deploy_badge.y + 9, 11, text_col);
        }

        m_btn_back.draw(font);
        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::DIFFICULTY_SELECT; }
    Difficulty selected_difficulty() const { return m_selected_difficulty; }
    void set_starting_wave(int wave) { m_starting_wave = wave; }
    int starting_wave() const { return m_starting_wave; }

private:
    struct TierCard {
        Rectangle bounds;
        DifficultyProfile profile;
        Color accent;
    };

    ViewType m_next_view;
    Difficulty m_selected_difficulty;
    int m_starting_wave = 1;
    std::vector<TierCard> m_tier_cards;
    UI::Button m_btn_back;
};

} // namespace Vimana
