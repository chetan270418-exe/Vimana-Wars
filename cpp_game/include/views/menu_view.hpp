#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "entities/player.hpp"

namespace Vimana {

class MenuView : public IView {
public:
    MenuView() : m_next_view(ViewType::MENU) {
        init();
    }

    void init() override {
        m_next_view = ViewType::MENU;
        m_buttons.clear();

        float start_y = 195.0f;
        float btn_w = 320.0f;
        float btn_h = 36.0f;
        float spacing = 43.0f;
        float center_x = 50.0f; // Left aligned menu column with right telemetry dashboard

        m_buttons.emplace_back(Rectangle{ center_x, start_y, btn_w, btn_h }, "1. ENTER CAMPAIGN (MAHAYUDDHA)", COLOR_GOLD_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing, btn_w, btn_h }, "2. VIMANA HANGAR & SHIPS", COLOR_CYAN_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 2, btn_w, btn_h }, "3. ASTRAL CODEX & BESTIARY", COLOR_GREEN_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 3, btn_w, btn_h }, "4. DUEL & FLIGHT TRAINING", COLOR_ORANGE_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 4, btn_w, btn_h }, "5. SANGHA MULTIPLAYER LOBBY", COLOR_PURPLE_BRIGHT);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 5, btn_w, btn_h }, "6. HALL OF VALOR (LEADERBOARDS)", COLOR_GOLD);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 6, btn_w, btn_h }, "7. SYSTEM SETTINGS", COLOR_MUTED);

        // Ambient starfield
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

        if (m_buttons[0].update(mouse_pos)) m_next_view = ViewType::CAMPAIGN_MAP;
        else if (m_buttons[1].update(mouse_pos)) m_next_view = ViewType::SHIP_SELECT;
        else if (m_buttons[2].update(mouse_pos)) m_next_view = ViewType::CODEX;
        else if (m_buttons[3].update(mouse_pos)) m_next_view = ViewType::DUEL;
        else if (m_buttons[4].update(mouse_pos)) m_next_view = ViewType::MULTIPLAYER_LOBBY;
        else if (m_buttons[5].update(mouse_pos)) m_next_view = ViewType::LEADERBOARD;
        else if (m_buttons[6].update(mouse_pos)) m_next_view = ViewType::SETTINGS;
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);

        // Draw parallax stars
        for (const auto& star : m_stars) {
            DrawCircle(static_cast<int>(star.x), static_cast<int>(star.y), star.z, { 200, 220, 255, 160 });
        }

        Font font = AssetManager::instance().font();

        // ── TOP BAR: LOGO & PILOT CALLOUT ────────────────────────────────────────
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            float scale = 0.22f;
            DrawTextureEx(logo, { 50, 25 }, 0.0f, scale, WHITE);
        } else {
            DrawTextEx(font, "VIMANA WARS", { 50, 30 }, 36, 2.0f, COLOR_GOLD_BRIGHT);
        }

        // Pilot Callout Strip (Top Right)
        Rectangle pilot_badge = { SCREEN_WIDTH - 360, 25, 310, 48 };
        UI::DrawChamferedPanel(pilot_badge, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);
        DrawText("PILOT IDENTIFICATION RECORD:", static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 7), 10, COLOR_MUTED);
        DrawText("VMN-7704 // PILOT: CHETAN", static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 20), 13, COLOR_GOLD_BRIGHT);
        DrawText("SQUADRON: ARJUNA CELESTIAL ACE", static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 34), 10, COLOR_CYAN_BRIGHT);

        // Subtitle line
        DrawText("CELESTIAL ASTRAL COMBAT // THE 7 REALMS OF MAHAYUDDHA", 52, 160, 12, COLOR_CYAN_BRIGHT);
        DrawLine(50, 180, SCREEN_WIDTH - 50, 180, COLOR_SURFACE_HIGH);

        // ── LEFT COLUMN: NAVIGATION BUTTONS ─────────────────────────────────────
        for (const auto& btn : m_buttons) {
            btn.draw(font);
        }

        // ── RIGHT COLUMN: TELEMETRY DASHBOARD STATUS TILES ──────────────────────
        Rectangle dash_box = { 400, 195, 450, 305 };
        UI::DrawChamferedPanel(dash_box, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);

        DrawTextEx(font, "COMMAND TELEMETRY // SECTOR STATUS", { dash_box.x + 20, dash_box.y + 15 }, 16, 1.0f, COLOR_GOLD_BRIGHT);
        DrawLine(static_cast<int>(dash_box.x + 20), static_cast<int>(dash_box.y + 40), static_cast<int>(dash_box.x + dash_box.width - 20), static_cast<int>(dash_box.y + 40), COLOR_MUTED);

        // Tile 1: Campaign Progression
        int max_wave = DBSystem::instance().max_wave();
        if (max_wave < 1) max_wave = 1;
        Rectangle tile1 = { dash_box.x + 20, dash_box.y + 55, dash_box.width - 40, 52 };
        UI::DrawChamferedPanel(tile1, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);
        DrawText("CAMPAIGN EXPEDITION MILESTONE", static_cast<int>(tile1.x + 15), static_cast<int>(tile1.y + 8), 10, COLOR_MUTED);
        std::string wave_prog = "HIGHEST REALM WAVE: " + std::to_string(max_wave) + " / 30";
        DrawText(wave_prog.c_str(), static_cast<int>(tile1.x + 15), static_cast<int>(tile1.y + 24), 14, COLOR_GOLD_BRIGHT);
        std::string wave_stat = max_wave >= 30 ? "ALL REALMS LIBERATED" : "INCURSION ACTIVE";
        DrawText(wave_stat.c_str(), static_cast<int>(tile1.x + 240), static_cast<int>(tile1.y + 24), 12, COLOR_CYAN_BRIGHT);

        // Tile 2: Fleet Readiness
        int unlocked_count = 0;
        for (const auto& ship : SHIP_FLEET) {
            if (CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave)) unlocked_count++;
        }
        Rectangle tile2 = { dash_box.x + 20, dash_box.y + 120, dash_box.width - 40, 52 };
        UI::DrawChamferedPanel(tile2, COLOR_CYAN_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        DrawText("VIMANA FLEET COMMISSIONED", static_cast<int>(tile2.x + 15), static_cast<int>(tile2.y + 8), 10, COLOR_MUTED);
        std::string fleet_str = std::to_string(unlocked_count) + " / 9 VIMANAS COMBAT READY";
        DrawText(fleet_str.c_str(), static_cast<int>(tile2.x + 15), static_cast<int>(tile2.y + 24), 14, COLOR_CYAN_BRIGHT);
        DrawText("HANGAR INSPECTED", static_cast<int>(tile2.x + 260), static_cast<int>(tile2.y + 24), 11, COLOR_PARCHMENT);

        // Tile 3: Prana Shards Treasury
        int prana = CurrencySystem::instance().prana_shards();
        Rectangle tile3 = { dash_box.x + 20, dash_box.y + 185, dash_box.width - 40, 52 };
        UI::DrawChamferedPanel(tile3, COLOR_GREEN_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        DrawText("ASTRAL PRANA CURRENCY BALANCE", static_cast<int>(tile3.x + 15), static_cast<int>(tile3.y + 8), 10, COLOR_MUTED);
        std::string prana_str = std::to_string(prana) + " PRANA SHARDS AVAILABLE";
        DrawText(prana_str.c_str(), static_cast<int>(tile3.x + 15), static_cast<int>(tile3.y + 24), 14, COLOR_GREEN_BRIGHT);
        DrawText("READY FOR LOADOUT", static_cast<int>(tile3.x + 250), static_cast<int>(tile3.y + 24), 11, COLOR_GOLD);

        // Quick tip
        DrawText("PRESS [1-7] OR CLICK BUTTONS TO NAVIGATE • 60 FPS NATIVE DESKTOP", static_cast<int>(dash_box.x + 20), static_cast<int>(dash_box.y + 255), 10, COLOR_MUTED);

        // Footer hint
        const char* footer = "VIMANA WARS C++ ENGINE // ARCHITECTURE: RAYLIB + SQLITE3 + ADVANCED DSA";
        Vector2 f_sz = MeasureTextEx(font, footer, 11, 1.0f);
        DrawTextEx(font, footer, { (SCREEN_WIDTH - f_sz.x) / 2.0f, SCREEN_HEIGHT - 28 }, 11, 1.0f, COLOR_MUTED);

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
