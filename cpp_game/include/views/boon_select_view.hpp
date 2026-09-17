#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/boon_system.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class BoonSelectView : public IView {
public:
    BoonSelectView() : m_next_view(ViewType::BOON_SELECT), m_selected_card(-1), m_btn_confirm({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 65, 280, 40 }, "ACCEPT BLESSING >>", COLOR_GOLD_BRIGHT) {
        init();
    }

    void init() override {
        m_next_view = ViewType::BOON_SELECT;
        m_selected_card = 0;
        m_draft_boons = BoonSystem::generate_draft(m_current_boons);
    }

    void set_player_boons(const std::vector<BoonType>& current_boons) {
        m_current_boons = current_boons;
        m_draft_boons = BoonSystem::generate_draft(m_current_boons);
        m_selected_card = 0;
    }

    void update(float dt, Vector2 mouse_pos) override {
        float card_w = 240.0f;
        float card_h = 320.0f;
        float spacing = 30.0f;
        float total_w = 3 * card_w + 2 * spacing;
        float start_x = (SCREEN_WIDTH - total_w) / 2.0f;
        float start_y = 120.0f;

        for (size_t i = 0; i < m_draft_boons.size(); ++i) {
            Rectangle card_rec = { start_x + i * (card_w + spacing), start_y, card_w, card_h };
            if (CheckCollisionPointRec(mouse_pos, card_rec)) {
                if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                    m_selected_card = static_cast<int>(i);
                    SoundSystem::instance().play_sfx("ui_click.wav");
                }
            }
        }

        if (m_btn_confirm.update(mouse_pos) || IsKeyPressed(KEY_ENTER)) {
            if (m_selected_card >= 0 && m_selected_card < static_cast<int>(m_draft_boons.size())) {
                m_chosen_boon = m_draft_boons[m_selected_card].type;
                m_next_view = ViewType::GAMEPLAY;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Title Header
        const char* title = "DEVA BLESSINGS // SELECT A ROGUELITE BOON";
        Vector2 t_sz = MeasureTextEx(font, title, 22, 1.0f);
        DrawTextEx(font, title, { (SCREEN_WIDTH - t_sz.x) / 2.0f, 35 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        const char* sub = "CHOOSE A CELESTIAL POWER • DRAFT SYNERGIES FOR COMPOUNDING COMBAT POWER";
        Vector2 s_sz = MeasureTextEx(font, sub, 12, 1.0f);
        DrawTextEx(font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 65 }, 12, 1.0f, COLOR_CYAN_BRIGHT);

        float card_w = 240.0f;
        float card_h = 320.0f;
        float spacing = 30.0f;
        float total_w = 3 * card_w + 2 * spacing;
        float start_x = (SCREEN_WIDTH - total_w) / 2.0f;
        float start_y = 110.0f;

        for (size_t i = 0; i < m_draft_boons.size(); ++i) {
            const auto& boon = m_draft_boons[i];
            bool is_sel = (m_selected_card == static_cast<int>(i));
            Rectangle card_rec = { start_x + i * (card_w + spacing), start_y, card_w, card_h };

            BoonSynergy syn;
            bool completes_synergy = BoonSystem::check_synergy_unlocked(m_current_boons, boon.type, syn);

            Color border = is_sel ? COLOR_GOLD_BRIGHT : (completes_synergy ? syn.color : boon.color);
            Color fill = is_sel ? COLOR_SURFACE_HIGH : COLOR_SURFACE_LOW;
            UI::DrawChamferedPanel(card_rec, border, fill, 8.0f, is_sel);

            // Synergy Banner on card top
            if (completes_synergy) {
                Rectangle syn_rec = { card_rec.x + 10, card_rec.y + 12, card_rec.width - 20, 22 };
                UI::DrawChamferedPanel(syn_rec, syn.color, COLOR_SURFACE_HIGH, 3.0f);
                std::string syn_text = "★ SYNERGY: " + syn.name + " ★";
                DrawText(syn_text.c_str(), static_cast<int>(syn_rec.x + 8), static_cast<int>(syn_rec.y + 5), 10, syn.color);
            }

            // Deity Icon / Header
            float top_offset = completes_synergy ? 42.0f : 20.0f;
            DrawText(boon.deity.c_str(), static_cast<int>(card_rec.x + 18), static_cast<int>(card_rec.y + top_offset), 11, COLOR_MUTED);

            // Boon Name
            DrawTextEx(font, boon.name.c_str(), { card_rec.x + 18, card_rec.y + top_offset + 22 }, 16, 1.0f, boon.color);

            DrawLine(static_cast<int>(card_rec.x + 18), static_cast<int>(card_rec.y + top_offset + 52), static_cast<int>(card_rec.x + card_w - 18), static_cast<int>(card_rec.y + top_offset + 52), COLOR_MUTED);

            // Description wrapped
            DrawText(boon.description.c_str(), static_cast<int>(card_rec.x + 18), static_cast<int>(card_rec.y + top_offset + 68), 12, COLOR_PARCHMENT);

            // If synergy, also describe the bonus combo
            if (completes_synergy) {
                DrawText("SYNERGISTIC FUSION:", static_cast<int>(card_rec.x + 18), static_cast<int>(card_rec.y + top_offset + 150), 10, COLOR_GOLD_BRIGHT);
                DrawText(syn.description.c_str(), static_cast<int>(card_rec.x + 18), static_cast<int>(card_rec.y + top_offset + 168), 11, syn.color);
            }

            // Selection indicator
            if (is_sel) {
                DrawText("[ SELECTED ]", static_cast<int>(card_rec.x + 72), static_cast<int>(card_rec.y + card_h - 32), 14, COLOR_GOLD_BRIGHT);
            }
        }

        // Active Passives indicator bar at bottom
        std::string active_str = "CURRENT VIMANA BOONS: " + std::to_string(m_current_boons.size()) + " EQUIPPED";
        DrawText(active_str.c_str(), 45, SCREEN_HEIGHT - 55, 12, COLOR_MUTED);

        m_btn_confirm.draw(font);
        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::BOON_SELECT; }
    BoonType chosen_boon() const { return m_chosen_boon; }

private:
    ViewType m_next_view;
    int m_selected_card;
    BoonType m_chosen_boon = BoonType::AGNI_SOLAR_FURY;
    std::vector<BoonInfo> m_draft_boons;
    std::vector<BoonType> m_current_boons;
    UI::Button m_btn_confirm;
};

} // namespace Vimana
