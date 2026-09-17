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
#include "systems/account_system.hpp"
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
        float btn_h = 34.0f;
        float spacing = 38.0f;
        float center_x = 50.0f; // Left column

        m_buttons.emplace_back(Rectangle{ center_x, start_y, btn_w, btn_h }, "1. ENTER CAMPAIGN (MAHAYUDDHA)", COLOR_GOLD_BRIGHT, "[1]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing, btn_w, btn_h }, "2. VIMANA HANGAR & SHIPS", COLOR_CYAN_BRIGHT, "[2]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 2, btn_w, btn_h }, "3. PILOT DOSSIER & PROFILE", COLOR_GREEN_BRIGHT, "[3]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 3, btn_w, btn_h }, "4. ASTRAL CODEX & BESTIARY", COLOR_PARCHMENT, "[4]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 4, btn_w, btn_h }, "5. DUEL & SIMULATOR", COLOR_ORANGE_BRIGHT, "[5]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 5, btn_w, btn_h }, "6. SQUADRON MULTIPLAYER", COLOR_PURPLE_BRIGHT, "[6]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 6, btn_w, btn_h }, "7. HALL OF VALOR (RANKS)", COLOR_GOLD, "[7]");
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 7, btn_w, btn_h }, "8. SYSTEM SETTINGS", COLOR_MUTED, "[8]");

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

        // Animated Flagship Thruster
        m_ship_bob += dt * 2.5f;

        // Button clicks or Keyboard shortcuts [1-8]
        if (m_buttons[0].update(mouse_pos) || IsKeyPressed(KEY_ONE)) m_next_view = ViewType::CAMPAIGN_MAP;
        else if (m_buttons[1].update(mouse_pos) || IsKeyPressed(KEY_TWO)) m_next_view = ViewType::SHIP_SELECT;
        else if (m_buttons[2].update(mouse_pos) || IsKeyPressed(KEY_THREE)) m_next_view = ViewType::PROFILE;
        else if (m_buttons[3].update(mouse_pos) || IsKeyPressed(KEY_FOUR)) m_next_view = ViewType::CODEX;
        else if (m_buttons[4].update(mouse_pos) || IsKeyPressed(KEY_FIVE)) m_next_view = ViewType::DUEL;
        else if (m_buttons[5].update(mouse_pos) || IsKeyPressed(KEY_SIX)) m_next_view = ViewType::MULTIPLAYER_LOBBY;
        else if (m_buttons[6].update(mouse_pos) || IsKeyPressed(KEY_SEVEN)) m_next_view = ViewType::LEADERBOARD;
        else if (m_buttons[7].update(mouse_pos) || IsKeyPressed(KEY_EIGHT)) m_next_view = ViewType::SETTINGS;

        // Click on top-right Pilot Badge opens Profile
        Rectangle pilot_badge = { SCREEN_WIDTH - 360, 25, 310, 48 };
        if (CheckCollisionPointRec(mouse_pos, pilot_badge) && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            m_next_view = ViewType::PROFILE;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);

        // Draw parallax stars
        for (const auto& star : m_stars) {
            DrawCircle(static_cast<int>(star.x), static_cast<int>(star.y), star.z, { 200, 220, 255, 160 });
        }

        Font title_f = AssetManager::instance().title_font();
        Font body_f = AssetManager::instance().body_font();

        // Vedic Corner Etchings on Screen Frame
        UI::DrawCornerEtching(12, 12, 28, COLOR_GOLD);
        UI::DrawCornerEtching(SCREEN_WIDTH - 40, 12, 28, COLOR_GOLD);
        UI::DrawCornerEtching(12, SCREEN_HEIGHT - 40, 28, COLOR_GOLD);
        UI::DrawCornerEtching(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, 28, COLOR_GOLD);

        // ── TOP BAR: LOGO & PILOT CALLOUT ────────────────────────────────────────
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            float scale = 0.22f;
            DrawTextureEx(logo, { 50, 25 }, 0.0f, scale, WHITE);
        } else {
            UI::DrawVedicHeading(title_f, "VIMANA WARS", { 50, 30 }, 36, COLOR_GOLD_BRIGHT);
        }

        // Pilot Callout Strip (Top Right)
        Rectangle pilot_badge = { SCREEN_WIDTH - 360, 25, 310, 48 };
        bool badge_hover = CheckCollisionPointRec(GetMousePosition(), pilot_badge);
        UI::DrawYantraPanel(pilot_badge, badge_hover ? COLOR_GOLD_BRIGHT : COLOR_GOLD, COLOR_SURFACE_MID, 4.0f, badge_hover);
        DrawText("PILOT IDENTIFICATION RECORD (CLICK FOR DOSSIER):", static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 7), 9, COLOR_MUTED);
        std::string callsign_line = AccountSystem::instance().game_id() + std::string(" // ") + DBSystem::instance().player_name();
        DrawTextEx(title_f, callsign_line.c_str(), { pilot_badge.x + 12, pilot_badge.y + 19 }, 13, 1.0f, COLOR_GOLD_BRIGHT);
        std::string cloud_info = AccountSystem::instance().is_logged_in() ? "[☁ CLOUD SYNCED // ONLINE]" : "[☁ LOCAL GUEST // OFFLINE]";
        Color cloud_col = AccountSystem::instance().is_logged_in() ? COLOR_GREEN_BRIGHT : COLOR_CYAN_BRIGHT;
        DrawText(cloud_info.c_str(), static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 34), 10, cloud_col);

        // Subtitle line
        DrawText("CELESTIAL ASTRAL COMBAT // THE 7 REALMS OF MAHAYUDDHA", 52, 160, 12, COLOR_CYAN_BRIGHT);
        DrawLine(50, 180, SCREEN_WIDTH - 50, 180, COLOR_SURFACE_HIGH);

        // ── LEFT COLUMN: NAVIGATION BUTTONS ─────────────────────────────────────
        for (const auto& btn : m_buttons) {
            btn.draw(title_f);
        }

        // ── RIGHT COLUMN: TELEMETRY DASHBOARD STATUS TILES ──────────────────────
        Rectangle dash_box = { 395, 195, 460, 325 };
        UI::DrawYantraPanel(dash_box, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f, true);

        DrawTextEx(title_f, "COMMAND TELEMETRY // SECTOR STATUS", { dash_box.x + 20, dash_box.y + 14 }, 15, 1.0f, COLOR_GOLD_BRIGHT);
        DrawLine(static_cast<int>(dash_box.x + 20), static_cast<int>(dash_box.y + 38), static_cast<int>(dash_box.x + dash_box.width - 20), static_cast<int>(dash_box.y + 38), COLOR_MUTED);

        // Floating Flagship Preview in Telemetry Header (Right side of box)
        Texture2D ship_tex = AssetManager::instance().get_texture("pushpaka.png");
        if (ship_tex.id > 0) {
            float float_y = dash_box.y + 75.0f + std::sin(m_ship_bob) * 5.0f;
            float ship_cx = dash_box.x + dash_box.width - 75.0f;

            // Rotating Yantra Halo Ring behind flagship
            DrawCircleLines(static_cast<int>(ship_cx), static_cast<int>(float_y), 42, ColorAlpha(COLOR_GOLD, 0.4f));
            DrawCircleLines(static_cast<int>(ship_cx), static_cast<int>(float_y), 36, ColorAlpha(COLOR_CYAN_BRIGHT, 0.3f));

            // Ship sprite
            Rectangle src = { 0, 0, static_cast<float>(ship_tex.width), static_cast<float>(ship_tex.height) };
            Rectangle dest = { ship_cx, float_y, 64, 64 };
            DrawTexturePro(ship_tex, src, dest, { 32, 32 }, 0.0f, WHITE);

            // Thruster glow
            DrawCircle(static_cast<int>(ship_cx), static_cast<int>(float_y + 28), 5.0f, COLOR_CYAN_BRIGHT);
        }

        // Tile 1: Campaign Progression & High Score
        int max_wave = DBSystem::instance().max_wave();
        if (max_wave < 1) max_wave = 1;
        Rectangle tile1 = { dash_box.x + 20, dash_box.y + 48, dash_box.width - 165, 52 };
        UI::DrawChamferedPanel(tile1, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);
        DrawText("CAMPAIGN EXPEDITION MILESTONE", static_cast<int>(tile1.x + 12), static_cast<int>(tile1.y + 8), 9, COLOR_MUTED);
        std::string wave_prog = "WAVE " + std::to_string(max_wave) + " / 30";
        DrawTextEx(title_f, wave_prog.c_str(), { tile1.x + 12, tile1.y + 22 }, 15, 1.0f, COLOR_GOLD_BRIGHT);

        // Tile 2: Fleet Readiness
        int unlocked_count = 0;
        for (const auto& ship : SHIP_FLEET) {
            if (CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave)) unlocked_count++;
        }
        Rectangle tile2 = { dash_box.x + 20, dash_box.y + 110, dash_box.width - 40, 52 };
        UI::DrawChamferedPanel(tile2, COLOR_CYAN_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        DrawText("VIMANA FLEET COMMISSIONED", static_cast<int>(tile2.x + 15), static_cast<int>(tile2.y + 8), 9, COLOR_MUTED);
        std::string fleet_str = std::to_string(unlocked_count) + " / " + std::to_string(SHIP_FLEET.size()) + " VIMANAS COMBAT READY";
        DrawTextEx(body_f, fleet_str.c_str(), { tile2.x + 15, tile2.y + 24 }, 13, 1.0f, COLOR_CYAN_BRIGHT);

        // Tile 3: Prana Shards Treasury & High Score
        int prana = CurrencySystem::instance().prana_shards();
        Rectangle tile3 = { dash_box.x + 20, dash_box.y + 172, dash_box.width - 40, 52 };
        UI::DrawChamferedPanel(tile3, COLOR_GREEN_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        DrawText("ASTRAL PRANA CURRENCY & RECORD", static_cast<int>(tile3.x + 15), static_cast<int>(tile3.y + 8), 9, COLOR_MUTED);
        std::string prana_str = std::to_string(prana) + " PRANA SHARDS";
        DrawTextEx(body_f, prana_str.c_str(), { tile3.x + 15, tile3.y + 24 }, 13, 1.0f, COLOR_GREEN_BRIGHT);
        std::string hs_str = "HIGH: " + std::to_string(DBSystem::instance().high_score());
        DrawText(hs_str.c_str(), static_cast<int>(tile3.x + 250), static_cast<int>(tile3.y + 26), 12, COLOR_GOLD_BRIGHT);

        // Quick tip & keybind hint
        DrawText("PRESS [1-8] ON KEYBOARD OR CLICK TO NAVIGATE • 60 FPS NATIVE", static_cast<int>(dash_box.x + 20), static_cast<int>(dash_box.y + 285), 10, COLOR_MUTED);

        // Footer hint
        const char* footer = "VIMANA WARS // NATIVE C++20 ENGINE • ADVANCED DSA • WINSOCK2 UDP LAN NETWORKING";
        Vector2 f_sz = MeasureTextEx(title_f, footer, 11, 1.0f);
        DrawTextEx(title_f, footer, { (SCREEN_WIDTH - f_sz.x) / 2.0f, SCREEN_HEIGHT - 24 }, 11, 1.0f, COLOR_MUTED);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MENU; }

private:
    struct Star { float x, y, z; };
    std::vector<Star> m_stars;
    std::vector<UI::Button> m_buttons;
    ViewType m_next_view;
    float m_ship_bob = 0.0f;
};

} // namespace Vimana
