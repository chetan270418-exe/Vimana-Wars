#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"
#include "systems/currency_system.hpp"

namespace Vimana {

class MenuView : public IView {
public:
    MenuView() : m_next_view(ViewType::MENU) {
        init();
    }

    void init() override {
        m_next_view = ViewType::MENU;
        m_buttons.clear();

        float start_y = 230.0f;
        float btn_w = 260.0f;
        float btn_h = 38.0f;
        float spacing = 48.0f;
        float center_x = (SCREEN_WIDTH - btn_w) / 2.0f;

        m_buttons.emplace_back(Rectangle{ center_x, start_y, btn_w, btn_h }, "ENTER MAHAYUDDHA", COLOR_GOLD_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing, btn_w, btn_h }, "VIMANA HANGAR", COLOR_CYAN_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 2, btn_w, btn_h }, "TRAINING & 1V1 DUEL", COLOR_ORANGE_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 3, btn_w, btn_h }, "SANGHA NETWORK", COLOR_PURPLE_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 4, btn_w, btn_h }, "ASTRAL LEADERBOARD", COLOR_GOLD);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 5, btn_w, btn_h }, "SETTINGS", COLOR_MUTED);

        // Generate ambient stars
        m_stars.clear();
        for (int i = 0; i < 90; ++i) {
            m_stars.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                0.5f + (std::rand() % 15) / 10.0f
            });
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        // Starfield drift
        for (auto& star : m_stars) {
            star.y += star.z * 20.0f * dt;
            if (star.y > SCREEN_HEIGHT) {
                star.y = 0;
                star.x = static_cast<float>(std::rand() % SCREEN_WIDTH);
            }
        }

        if (m_buttons[0].update(mouse_pos)) m_next_view = ViewType::SHIP_SELECT;
        else if (m_buttons[1].update(mouse_pos)) m_next_view = ViewType::SHIP_SELECT;
        else if (m_buttons[2].update(mouse_pos)) m_next_view = ViewType::DUEL;
        else if (m_buttons[3].update(mouse_pos)) m_next_view = ViewType::MULTIPLAYER_LOBBY;
        else if (m_buttons[4].update(mouse_pos)) m_next_view = ViewType::LEADERBOARD;
        else if (m_buttons[5].update(mouse_pos)) m_next_view = ViewType::SETTINGS;
    }

    void draw() override {
        // Deep cosmic background
        ClearBackground(COLOR_OBSIDIAN);

        // Stars
        for (const auto& star : m_stars) {
            DrawCircle(static_cast<int>(star.x), static_cast<int>(star.y), star.z, { 200, 220, 255, 160 });
        }

        Font font = AssetManager::instance().font();

        // Logo / Title banner
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            float scale = 0.28f;
            DrawTextureEx(logo, { (SCREEN_WIDTH - logo.width * scale) / 2.0f, 35 }, 0.0f, scale, WHITE);
        } else {
            const char* title = "VIMANA WARS";
            Vector2 sz = MeasureTextEx(font, title, 44, 2.0f);
            DrawTextEx(font, title, { (SCREEN_WIDTH - sz.x) / 2.0f, 60 }, 44, 2.0f, COLOR_GOLD_BRIGHT);
        }

        const char* sub = "CELESTIAL ASTRAL COMBAT // THE TEN HEADS OF RAVANA";
        Vector2 sub_sz = MeasureTextEx(font, sub, 13, 1.0f);
        DrawTextEx(font, sub, { (SCREEN_WIDTH - sub_sz.x) / 2.0f, 175 }, 13, 1.0f, COLOR_CYAN_BRIGHT);

        // Currency banner (Prana Shards)
        std::string prana_str = "PRANA SHARDS: " + std::to_string(CurrencySystem::instance().prana_shards());
        UI::DrawChamferedPanel({ 25, 25, 190, 32 }, COLOR_GOLD, COLOR_SURFACE_LOW, 4.0f);
        DrawTextEx(font, prana_str.c_str(), { 35, 32 }, 13, 1.0f, COLOR_GOLD_BRIGHT);

        // Draw Menu Buttons
        for (const auto& btn : m_buttons) {
            btn.draw(font);
        }

        // Footer hint
        const char* footer = "SELECT A MISSION • 60 FPS NATIVE C++ ENGINE • ESC TO RETURN";
        Vector2 f_sz = MeasureTextEx(font, footer, 11, 1.0f);
        DrawTextEx(font, footer, { (SCREEN_WIDTH - f_sz.x) / 2.0f, SCREEN_HEIGHT - 30 }, 11, 1.0f, COLOR_MUTED);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MENU; }

private:
    struct Star { float x, y, z; };
    std::vector<Star> m_stars;
    std::vector<UI::Button> m_buttons;
    ViewType m_next_view;
};

} // namespace Vimana
