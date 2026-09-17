#pragma once
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "systems/db_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class PilotSetupView : public IView {
public:
    PilotSetupView() 
        : m_next_view(ViewType::PILOT_SETUP),
          m_btn_confirm({ SCREEN_WIDTH / 2.0f - 130.0f, 365, 260, 36 }, "CONFIRM CALLSIGN", COLOR_GOLD_BRIGHT),
          m_btn_skip({ SCREEN_WIDTH / 2.0f - 130.0f, 408, 260, 32 }, "USE GUEST CALLSIGN (WARRIOR)", COLOR_MUTED),
          m_btn_auth({ SCREEN_WIDTH / 2.0f - 130.0f, 448, 260, 32 }, "SIGN IN TO CLOUD ACCOUNT >>", COLOR_CYAN_BRIGHT)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::PILOT_SETUP;
        m_callsign = DBSystem::instance().player_name();
        if (m_callsign.empty() || m_callsign == "Warrior") {
            m_callsign = "WARRIOR";
        }
        m_cursor_timer = 0.0f;
    }

    void update(float dt, Vector2 mouse_pos) override {
        m_cursor_timer += dt;

        // Handle text input
        int key = GetCharPressed();
        while (key > 0) {
            // Only allow standard ASCII alphanumeric / space / dash
            if ((key >= 32) && (key <= 125) && (m_callsign.length() < 16)) {
                // Auto uppercase
                if (key >= 'a' && key <= 'z') key -= 32;
                m_callsign.push_back(static_cast<char>(key));
            }
            key = GetCharPressed();
        }

        if (IsKeyPressed(KEY_BACKSPACE)) {
            if (!m_callsign.empty()) {
                m_callsign.pop_back();
            }
        }

        if (IsKeyPressed(KEY_ENTER) || m_btn_confirm.update(mouse_pos)) {
            if (m_callsign.empty()) m_callsign = "WARRIOR";
            DBSystem::instance().set_player_name(m_callsign);
            DBSystem::instance().save_game();
            m_next_view = ViewType::MENU;
        }

        if (m_btn_skip.update(mouse_pos)) {
            m_callsign = "WARRIOR";
            DBSystem::instance().set_player_name(m_callsign);
            DBSystem::instance().save_game();
            m_next_view = ViewType::MENU;
        }

        if (m_btn_auth.update(mouse_pos)) {
            m_next_view = ViewType::AUTH;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Card Container
        Rectangle card = { SCREEN_WIDTH / 2.0f - 240, 90, 480, 410 };
        UI::DrawChamferedPanel(card, COLOR_GOLD, COLOR_SURFACE_LOW, 8.0f);

        const char* title = "CELESTIAL PILOT REGISTRATION";
        Vector2 t_sz = MeasureTextEx(font, title, 20, 1.0f);
        DrawTextEx(font, title, { (SCREEN_WIDTH - t_sz.x) / 2.0f, card.y + 25 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        const char* sub = "ENTER YOUR SQUADRON CALLSIGN TO COMMISSION YOUR VIMANA";
        Vector2 s_sz = MeasureTextEx(font, sub, 10, 1.0f);
        DrawTextEx(font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, card.y + 55 }, 10, 1.0f, COLOR_CYAN_BRIGHT);

        DrawLine(card.x + 30, card.y + 75, card.x + card.width - 30, card.y + 75, COLOR_SURFACE_HIGH);

        // Registry Specs
        float cy = card.y + 95;
        DrawText("ASSIGNED PILOT ID :", card.x + 40, cy, 12, COLOR_MUTED);
        DrawText(PILOT_ID, card.x + 220, cy, 13, COLOR_GOLD_BRIGHT);

        DrawText("SQUADRON FLEET   :", card.x + 40, cy + 28, 12, COLOR_MUTED);
        DrawText(PILOT_SQUADRON, card.x + 220, cy + 28, 13, COLOR_CYAN_BRIGHT);

        DrawText("SERVICE CLASS     :", card.x + 40, cy + 56, 12, COLOR_MUTED);
        DrawText("MAHAYUDDHA ASTRAL RECON", card.x + 220, cy + 56, 13, COLOR_PARCHMENT);

        // Text Input Field Box
        Rectangle input_box = { card.x + 40, cy + 100, card.width - 80, 46 };
        UI::DrawChamferedPanel(input_box, COLOR_CYAN_BRIGHT, COLOR_SURFACE_MID, 4.0f);

        std::string display_name = m_callsign;
        bool cursor_visible = (static_cast<int>(m_cursor_timer * 2.0f) % 2) == 0;
        if (cursor_visible) {
            display_name += "_";
        }

        DrawTextEx(font, display_name.c_str(), { input_box.x + 16, input_box.y + 12 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
        DrawText("TYPE USING KEYBOARD • PRESS ENTER TO CONFIRM", card.x + 40, input_box.y + 52, 10, COLOR_MUTED);

        // Action Buttons
        m_btn_confirm.draw(font);
        m_btn_skip.draw(font);
        m_btn_auth.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::PILOT_SETUP; }

private:
    ViewType m_next_view;
    std::string m_callsign;
    float m_cursor_timer;
    UI::Button m_btn_confirm;
    UI::Button m_btn_skip;
    UI::Button m_btn_auth;
};

} // namespace Vimana
