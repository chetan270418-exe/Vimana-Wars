#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/design_tokens.hpp"   // must come before vedic_theme (defines ElevationStyle)
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "systems/account_system.hpp"
#include "entities/player.hpp"
#include "views/player_card_view.hpp"

namespace Vimana {

class MenuView : public IView {
public:
    MenuView() : m_next_view(ViewType::MENU) {
        init();
    }

    void init() override {
        m_next_view = ViewType::MENU;
        m_buttons.clear();
        m_card_overlay.set_visible(false);
        m_btn_continue = UI::Button({ 50, 148, 320, 36 }, "CONTINUE", COLOR_GOLD_BRIGHT, "", Vimana::UI::ButtonKind::PRIMARY);

        float start_y = 190.0f;
        float btn_w = 320.0f;
        float btn_h = 30.0f;
        float spacing = 32.0f;
        float center_x = 50.0f; // Left column

        m_buttons.emplace_back(Rectangle{ center_x, start_y,                     btn_w, btn_h }, "1.  ENTER CAMPAIGN",            COLOR_GOLD_BRIGHT,   "[1]", Vimana::UI::ButtonKind::PRIMARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 1,       btn_w, btn_h }, "2.  VIMANA HANGAR",             COLOR_CYAN_BRIGHT,   "[2]", Vimana::UI::ButtonKind::SECONDARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 2,       btn_w, btn_h }, "3.  PILOT PROFILE",             COLOR_GREEN_BRIGHT,  "[3]", Vimana::UI::ButtonKind::SECONDARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 3,       btn_w, btn_h }, "4.  ASTRAL CODEX",              COLOR_PARCHMENT,     "[4]", Vimana::UI::ButtonKind::TERTIARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 4,       btn_w, btn_h }, "5.  DUEL MODE",                 COLOR_ORANGE_BRIGHT, "[5]", Vimana::UI::ButtonKind::SECONDARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 5,       btn_w, btn_h }, "6.  MULTIPLAYER",               COLOR_PURPLE_BRIGHT, "[6]", Vimana::UI::ButtonKind::SECONDARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 6,       btn_w, btn_h }, "7.  LEADERBOARD",               COLOR_GOLD,          "[7]", Vimana::UI::ButtonKind::PRIMARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 7,       btn_w, btn_h }, "8.  SETTINGS",                  COLOR_MUTED,         "[8]", Vimana::UI::ButtonKind::GHOST);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 8,       btn_w, btn_h }, "9.  SIGN IN / REGISTER",         COLOR_GREEN_BRIGHT,  "[9]", Vimana::UI::ButtonKind::SECONDARY);
        m_buttons.emplace_back(Rectangle{ center_x, start_y + spacing * 9,       btn_w, btn_h }, "0.  ACHIEVEMENT HALL",           COLOR_GOLD_BRIGHT,   "[0]", Vimana::UI::ButtonKind::SECONDARY);

        // Bottom-right secondary actions (separate row, smaller)
        m_buttons.emplace_back(Rectangle{ SCREEN_WIDTH - 260, SCREEN_HEIGHT - 56, 110, 28 }, "FULLSCREEN",  COLOR_MUTED,    "[F11]", Vimana::UI::ButtonKind::GHOST);
        m_buttons.emplace_back(Rectangle{ SCREEN_WIDTH - 145, SCREEN_HEIGHT - 56, 110, 28 }, "QUIT GAME",   COLOR_RED_BRIGHT,"[ESC]", Vimana::UI::ButtonKind::DESTRUCTIVE);

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
        // Overlay takes priority if open
        if (m_card_overlay.is_visible()) {
            m_card_overlay.update(dt, mouse_pos);
            return;
        }

        // Toggle Player Card Overlay via [P]
        if (IsKeyPressed(KEY_P)) {
            m_card_overlay.toggle();
        }

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

        // CONTINUE hero action if save exists
        int saved_wave = DBSystem::instance().max_wave();
        if (saved_wave > 1) {
            std::string cont_label = "CONTINUE WAVE " + std::to_string(saved_wave);
            m_btn_continue.set_label(cont_label);
            if (m_btn_continue.update(mouse_pos)) m_next_view = ViewType::CAMPAIGN_MAP;
        }

        // Button clicks or keyboard shortcuts [1-9]
        if (m_buttons[0].update(mouse_pos) || IsKeyPressed(KEY_ONE)) m_next_view = ViewType::CAMPAIGN_MAP;
        else if (m_buttons[1].update(mouse_pos) || IsKeyPressed(KEY_TWO)) m_next_view = ViewType::SHIP_SELECT;
        else if (m_buttons[2].update(mouse_pos) || IsKeyPressed(KEY_THREE)) m_card_overlay.set_visible(true);
        else if (m_buttons[3].update(mouse_pos) || IsKeyPressed(KEY_FOUR)) m_next_view = ViewType::CODEX;
        else if (m_buttons[4].update(mouse_pos) || IsKeyPressed(KEY_FIVE)) m_next_view = ViewType::DUEL;
        else if (m_buttons[5].update(mouse_pos) || IsKeyPressed(KEY_SIX)) m_next_view = ViewType::MULTIPLAYER_LOBBY;
        else if (m_buttons[6].update(mouse_pos) || IsKeyPressed(KEY_SEVEN)) m_next_view = ViewType::LEADERBOARD;
        else if (m_buttons[7].update(mouse_pos) || IsKeyPressed(KEY_EIGHT)) m_next_view = ViewType::SETTINGS;
        else if (m_buttons[8].update(mouse_pos) || IsKeyPressed(KEY_NINE)) m_next_view = ViewType::AUTH;

        // Bottom-right secondary actions: Fullscreen + Quit
        // Indices 10 (FULLSCREEN) and 11 (QUIT GAME)
        if (m_buttons.size() >= 12) {
            if (m_buttons[10].update(mouse_pos) || IsKeyPressed(KEY_F11)) {
                int mode = 0; // toggle: 0 = windowed, 1 = borderless fullscreen
                if (IsWindowFullscreen()) mode = 0;
                else mode = 1;
                ToggleFullscreen();
                (void)mode;
            }
            if (m_buttons[11].update(mouse_pos)) {
                m_next_view = ViewType::QUIT;
            }
        }

        if (m_buttons[9].update(mouse_pos) || IsKeyPressed(KEY_ZERO)) m_next_view = ViewType::ACHIEVEMENTS;

        // Click on top-right Pilot Badge opens Player Card
        Rectangle pilot_badge = { SCREEN_WIDTH - 360, 25, 310, 48 };
        if (CheckCollisionPointRec(mouse_pos, pilot_badge) && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            m_card_overlay.set_visible(true);
        }
    }

    void draw() override {
        using namespace Vimana::UI;
        ClearBackground(PAL_BG_VOID);

        // Draw parallax stars
        for (const auto& star : m_stars) {
            DrawCircle(static_cast<int>(star.x), static_cast<int>(star.y), star.z, { 200, 220, 255, 160 });
        }

        Font title_f = AssetManager::instance().title_font();
        Font body_f = AssetManager::instance().body_font();

        // Vedic Corner Etchings on Screen Frame — now with diamond rivets
        Rectangle frame = { 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT };
        UI::DrawCornerBrackets(frame, 28.0f, PAL_TERTIARY);

        // ── TOP BAR: LOGO & PILOT CALLOUT ────────────────────────────────────────
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            float scale = 0.22f;
            DrawTextureEx(logo, { 50, 25 }, 0.0f, scale, WHITE);
        } else {
            UI::DrawVedicHeading(title_f, "VIMANA WARS", { 50, 30 }, 36, PAL_PRIMARY_BRIGHT);
        }

        // Pilot Callout Strip (Top Right) — design system ElevationPanel + brackets
        Rectangle pilot_badge = { SCREEN_WIDTH - 360, 25, 310, 48 };
        bool badge_hover = CheckCollisionPointRec(GetMousePosition(), pilot_badge);
        auto pilot_elev = UI::ElevationGlass();
        UI::DrawElevationPanel(pilot_badge, pilot_elev, badge_hover);
        Color border_col = badge_hover ? PAL_PRIMARY : PAL_TERTIARY;
        UI::DrawCornerBrackets(pilot_badge, 8.0f, border_col);
        DrawText("PILOT ID RECORD // CLICK FOR DOSSIER", static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 7), 12, PAL_TEXT_MUTED);
        std::string callsign_line = AccountSystem::instance().game_id() + std::string(" // ") + DBSystem::instance().player_name();
        DrawTextEx(title_f, callsign_line.c_str(), { pilot_badge.x + 12, pilot_badge.y + 21 }, 16, 1.0f, PAL_PRIMARY_BRIGHT);
        std::string cloud_info = AccountSystem::instance().is_logged_in() ? "[CLOUD SYNCED // ONLINE]" : "[LOCAL GUEST // OFFLINE]";
        Color cloud_col = AccountSystem::instance().is_logged_in() ? PAL_HEALTH_HIGH : PAL_SECONDARY_BRIGHT;
        DrawText(cloud_info.c_str(), static_cast<int>(pilot_badge.x + 12), static_cast<int>(pilot_badge.y + 39), 12, cloud_col);

        // Subtitle line — telemetry-mono style
        DrawText("CELESTIAL ASTRAL COMBAT // 10 ACTS · 300 WAVES", 52, 160, 12, PAL_SECONDARY_BRIGHT);
        DrawLine(50, 180, SCREEN_WIDTH - 50, 180, PAL_OUTLINE_VARIANT);

        // ── LEFT COLUMN: NAVIGATION BUTTONS ─────────────────────────────────────
        if (DBSystem::instance().max_wave() > 1) m_btn_continue.draw(title_f);
        for (const auto& btn : m_buttons) {
            btn.draw(title_f);
        }

        // ── RIGHT COLUMN: TELEMETRY DASHBOARD STATUS TILES ──────────────────────
        Rectangle dash_box = { 395, 195, 460, 325 };
        auto dash_elev = UI::ElevationGlass();
        UI::DrawElevationPanel(dash_box, dash_elev, true);
        UI::DrawCornerBrackets(dash_box, 14.0f, PAL_SECONDARY);

        DrawTextEx(title_f, "COMMAND TELEMETRY // SECTOR STATUS", { dash_box.x + 20, dash_box.y + 14 }, 15, 1.0f, PAL_PRIMARY_BRIGHT);
        DrawLine(static_cast<int>(dash_box.x + 20), static_cast<int>(dash_box.y + 38), static_cast<int>(dash_box.x + dash_box.width - 20), static_cast<int>(dash_box.y + 38), PAL_OUTLINE_VARIANT);

        // Floating Flagship Preview in Telemetry Header (Right side of box)
        Texture2D ship_tex = AssetManager::instance().get_texture("pushpaka.png");
        if (ship_tex.id > 0) {
            float float_y = dash_box.y + 75.0f + std::sin(m_ship_bob) * 5.0f;
            float ship_cx = dash_box.x + dash_box.width - 75.0f;

            // Mandala reticle behind flagship (replaces simple concentric rings)
            UI::DrawMandalaReticle({ ship_cx, float_y }, 42.0f, GetTime(), PAL_PRIMARY, PAL_SECONDARY, 0.65f);

            // Ship sprite
            Rectangle src = { 0, 0, static_cast<float>(ship_tex.width), static_cast<float>(ship_tex.height) };
            Rectangle dest = { ship_cx, float_y, 64, 64 };
            DrawTexturePro(ship_tex, src, dest, { 32, 32 }, 0.0f, WHITE);

            // Thruster glow
            DrawCircle(static_cast<int>(ship_cx), static_cast<int>(float_y + 28), 5.0f, PAL_SECONDARY_BRIGHT);
        }

        // Tile 1: Campaign Progression & High Score
        int max_wave = DBSystem::instance().max_wave();
        if (max_wave < 1) max_wave = 1;
        Rectangle tile1 = { dash_box.x + 20, dash_box.y + 48, dash_box.width - 165, 52 };
        UI::DrawElevationPanel(tile1, UI::ElevationWell());
        UI::DrawCornerBrackets(tile1, 6.0f, PAL_PRIMARY);
        DrawText("CAMPAIGN MILESTONE", static_cast<int>(tile1.x + 12), static_cast<int>(tile1.y + 8), 11, PAL_TEXT_MUTED);
        std::string wave_prog = "ACT " + std::to_string(CampaignActForWave(max_wave)) + " / 10  ·  WAVE " +
                                std::to_string(CampaignWaveWithinAct(max_wave)) + " / " + std::to_string(WAVES_PER_ACT);
        DrawTextEx(title_f, wave_prog.c_str(), { tile1.x + 12, tile1.y + 22 }, 16, 1.0f, PAL_PRIMARY_BRIGHT);

        // Tile 2: Fleet Readiness
        int unlocked_count = 0;
        for (const auto& ship : SHIP_FLEET) {
            if (CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave)) unlocked_count++;
        }
        Rectangle tile2 = { dash_box.x + 20, dash_box.y + 110, dash_box.width - 40, 52 };
        UI::DrawElevationPanel(tile2, UI::ElevationWell());
        UI::DrawCornerBrackets(tile2, 6.0f, PAL_SECONDARY);
        DrawText("VIMANA FLEET COMMISSIONED", static_cast<int>(tile2.x + 15), static_cast<int>(tile2.y + 8), 11, PAL_TEXT_MUTED);
        std::string fleet_str = std::to_string(unlocked_count) + " / " + std::to_string(SHIP_FLEET.size()) + " VIMANAS COMBAT READY";
        DrawTextEx(body_f, fleet_str.c_str(), { tile2.x + 15, tile2.y + 24 }, 13, 1.0f, PAL_SECONDARY_BRIGHT);

        // Tile 3: Prana Shards Treasury & High Score — use segmented gauge instead of plain number
        int prana = CurrencySystem::instance().prana_shards();
        Rectangle tile3 = { dash_box.x + 20, dash_box.y + 172, dash_box.width - 40, 52 };
        UI::DrawElevationPanel(tile3, UI::ElevationWell());
        UI::DrawCornerBrackets(tile3, 6.0f, PAL_HEALTH_HIGH);
        DrawText("PRANA SHARDS & RECORD", static_cast<int>(tile3.x + 15), static_cast<int>(tile3.y + 8), 11, PAL_TEXT_MUTED);
        std::string prana_str = std::to_string(prana) + " PRANA SHARDS";
        DrawTextEx(body_f, prana_str.c_str(), { tile3.x + 15, tile3.y + 24 }, 13, 1.0f, PAL_HEALTH_HIGH);
        std::string hs_str = "HIGH: " + std::to_string(DBSystem::instance().high_score());
        DrawText(hs_str.c_str(), static_cast<int>(tile3.x + 250), static_cast<int>(tile3.y + 26), 12, PAL_PRIMARY_BRIGHT);

        // Quick tip & keybind hint — telemetry style
        DrawText("[1-9, 0] NAVIGATE  ·  [P] PILOT CARD  ·  [F11] FULLSCREEN  ·  60 FPS NATIVE", static_cast<int>(dash_box.x + 20), static_cast<int>(dash_box.y + 285), 12, PAL_TEXT_MUTED);

        // Footer hint
        const char* footer = "VIMANA WARS  //  WINDOWS BUILD  ·  C++20 + RAYLIB  ·  60 FPS";
        Vector2 f_sz = MeasureTextEx(title_f, footer, 13, 1.0f);
        DrawTextEx(title_f, footer, { (SCREEN_WIDTH - f_sz.x) / 2.0f, SCREEN_HEIGHT - 86 }, 13, 1.0f, PAL_TEXT_MUTED);

        // Pilot Card Overlay (draws on top of everything when active)
        m_card_overlay.draw(title_f, body_f);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MENU; }

private:
    struct Star { float x, y, z; };
    std::vector<Star> m_stars;
    std::vector<UI::Button> m_buttons;
    UI::Button m_btn_continue = UI::Button({50,148,320,36}, "CONTINUE", COLOR_GOLD_BRIGHT);
    ViewType m_next_view;
    float m_ship_bob = 0.0f;
    PlayerCardOverlay m_card_overlay;
};

} // namespace Vimana
