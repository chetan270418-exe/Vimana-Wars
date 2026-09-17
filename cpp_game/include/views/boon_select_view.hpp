#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/boon_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class BoonSelectView : public IView {
public:
    BoonSelectView() : m_next_view(ViewType::BOON_SELECT), m_selected_card(-1) {
        init();
    }

    void init() override {
        m_next_view = ViewType::BOON_SELECT;
        m_selected_card = 0;
        m_draft_boons = BoonSystem::generate_draft({});

        m_btn_confirm = UI::Button({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 80, 280, 44 }, "ACCEPT BLESSING", COLOR_GOLD_BRIGHT);
    }

    void set_draft(const std::vector<BoonInfo>& draft) {
        m_draft_boons = draft;
        m_selected_card = 0;
    }

    void update(float dt, Vector2 mouse_pos) override {
        // Card hover/click detection
        float card_w = 230.0f;
        float card_h = 320.0f;
        float spacing = 35.0f;
        float total_w = 3 * card_w + 2 * spacing;
        float start_x = (SCREEN_WIDTH - total_w) / 2.0f;
        float start_y = 140.0f;

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
        Vector2 t_sz = MeasureTextEx(font, title, 24, 1.0f);
        DrawTextEx(font, title, { (SCREEN_WIDTH - t_sz.x) / 2.0f, 45 }, 24, 1.0f, COLOR_GOLD_BRIGHT);

        const char* sub = "CHOOSE A CELESTIAL POWER TO AUGMENT YOUR VIMANA FOR THE NEXT REALM";
        Vector2 s_sz = MeasureTextEx(font, sub, 12, 1.0f);
        DrawTextEx(font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 80 }, 12, 1.0f, COLOR_CYAN_BRIGHT);

        float card_w = 230.0f;
        float card_h = 320.0f;
        float spacing = 35.0f;
        float total_w = 3 * card_w + 2 * spacing;
        float start_x = (SCREEN_WIDTH - total_w) / 2.0f;
        float start_y = 130.0f;

        for (size_t i = 0; i < m_draft_boons.size(); ++i) {
            const auto& boon = m_draft_boons[i];
            bool is_sel = (m_selected_card == static_cast<int>(i));
            Rectangle card_rec = { start_x + i * (card_w + spacing), start_y, card_w, card_h };

            Color border = is_sel ? COLOR_GOLD_BRIGHT : boon.color;
            Color fill = is_sel ? COLOR_SURFACE_HIGH : COLOR_SURFACE_LOW;
            UI::DrawChamferedPanel(card_rec, border, fill, 8.0f, is_sel);

            // Deity Icon / Header
            DrawText(boon.deity.c_str(), static_cast<int>(card_rec.x + 20), static_cast<int>(card_rec.y + 25), 11, COLOR_MUTED);

            // Boon Name
            DrawTextEx(font, boon.name.c_str(), { card_rec.x + 20, card_rec.y + 48 }, 18, 1.0f, boon.color);

            DrawLine(static_cast<int>(card_rec.x + 20), static_cast<int>(card_rec.y + 85), static_cast<int>(card_rec.x + card_w - 20), static_cast<int>(card_rec.y + 85), COLOR_MUTED);

            // Description wrapped
            DrawText(boon.description.c_str(), static_cast<int>(card_rec.x + 20), static_cast<int>(card_rec.y + 110), 13, COLOR_PARCHMENT);

            // Selection indicator
            if (is_sel) {
                DrawText("[ SELECTED ]", static_cast<int>(card_rec.x + 65), static_cast<int>(card_rec.y + card_h - 35), 14, COLOR_GOLD_BRIGHT);
            }
        }

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
    UI::Button m_btn_confirm;
};

} // namespace Vimana
