#pragma once
#include <algorithm>
#include <array>
#include <cmath>
#include <string>
#include <vector>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "ui/design_tokens.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"
#include "systems/db_system.hpp"
#include "systems/account_system.hpp"
#include "systems/sound_system.hpp"
#include "entities/ship_archetypes.hpp"

namespace Vimana {

class MenuView : public IView {
public:
    MenuView() : m_next_view(ViewType::MENU) { init(); }

    void init() override {
        m_next_view = ViewType::MENU;
        m_nav = {
            { { 56, 181, 340, 31 }, "SINGLE PLAYER",      ViewType::CAMPAIGN_MAP,      UI::PAL_PRIMARY_BRIGHT,   "1" },
            { { 56, 216, 340, 31 }, "MULTIPLAYER",        ViewType::MULTIPLAYER_LOBBY, UI::PAL_SECONDARY_BRIGHT, "2" },
            { { 56, 251, 340, 31 }, "SELECT YOUR SHIP",   ViewType::SHIP_SELECT,       UI::PAL_SECONDARY_BRIGHT, "3" },
            { { 56, 286, 340, 31 }, "ACHIEVEMENTS",       ViewType::ACHIEVEMENTS,      UI::PAL_PRIMARY_BRIGHT,   "4" },
            { { 56, 321, 340, 31 }, "LEADERBOARDS",       ViewType::LEADERBOARD,       UI::PAL_SECONDARY_BRIGHT, "5" },
            { { 56, 356, 340, 31 }, "CODEX / LORE",       ViewType::CODEX,              UI::PAL_SECONDARY_BRIGHT, "6" },
            { { 56, 391, 340, 31 }, "DUEL / TRAINING",    ViewType::DUEL,               UI::PAL_SECONDARY_BRIGHT, "7" },
            { { 56, 426, 340, 31 }, "SETTINGS",           ViewType::SETTINGS,           UI::PAL_TEXT_VARIANT,     "8" },
            { { 56, 461, 340, 31 }, "QUIT",               ViewType::QUIT,               UI::PAL_DESTRUCTIVE_BRIGHT,"9" }
        };
        m_hover_anim.assign(m_nav.size(), 0.0f);
        m_selected = 0;
        m_hovered = -1;
        m_badge_hovered = false;
        m_continue_hovered = false;
        m_has_mouse_position = false;

        m_stars.clear();
        for (int i = 0; i < 48; ++i) {
            m_stars.push_back({ static_cast<float>(GetRandomValue(0, SCREEN_WIDTH)),
                                static_cast<float>(GetRandomValue(0, SCREEN_HEIGHT)),
                                0.35f + static_cast<float>(GetRandomValue(0, 12)) / 10.0f });
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        const bool mouse_moved = !m_has_mouse_position ||
            std::fabs(mouse_pos.x - m_last_mouse_pos.x) > 1.0f ||
            std::fabs(mouse_pos.y - m_last_mouse_pos.y) > 1.0f;
        m_last_mouse_pos = mouse_pos;
        m_has_mouse_position = true;

        for (auto& star : m_stars) {
            star.y += star.speed * 9.0f * dt;
            if (star.y > SCREEN_HEIGHT) {
                star.y = 0.0f;
                star.x = static_cast<float>(GetRandomValue(0, SCREEN_WIDTH));
            }
        }
        m_ship_bob += dt * 1.8f;

        const int saved_wave = DBSystem::instance().continue_wave();
        const bool has_continue = saved_wave > 1 || DBSystem::instance().max_wave() > 1;
        const Rectangle continue_rect = { 56, 132, 340, 36 };
        m_continue_hovered = has_continue && CheckCollisionPointRec(mouse_pos, continue_rect);
        if (m_continue_hovered && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            SoundSystem::instance().play_ui_click();
            m_next_view = ViewType::CAMPAIGN_MAP;
            return;
        }
        if (has_continue && IsKeyPressed(KEY_C)) {
            m_next_view = ViewType::CAMPAIGN_MAP;
            return;
        }

        // Numeric shortcuts preserve fast access; arrows/Enter provide a gamepad-like keyboard flow.
        static constexpr std::array<int, 9> nav_keys = {
            KEY_ONE, KEY_TWO, KEY_THREE, KEY_FOUR, KEY_FIVE,
            KEY_SIX, KEY_SEVEN, KEY_EIGHT, KEY_NINE
        };
        for (size_t i = 0; i < nav_keys.size(); ++i) {
            if (IsKeyPressed(nav_keys[i])) {
                m_selected = static_cast<int>(i);
                SoundSystem::instance().play_ui_click();
                m_next_view = m_nav[i].target;
                return;
            }
        }

        const bool keyboard_navigation = IsKeyPressed(KEY_DOWN) || IsKeyPressed(KEY_S) ||
                                        IsKeyPressed(KEY_UP) || IsKeyPressed(KEY_W);
        if (IsKeyPressed(KEY_DOWN) || IsKeyPressed(KEY_S)) {
            m_selected = (m_selected + 1) % static_cast<int>(m_nav.size());
            SoundSystem::instance().play_ui_hover();
        } else if (IsKeyPressed(KEY_UP) || IsKeyPressed(KEY_W)) {
            m_selected = (m_selected + static_cast<int>(m_nav.size()) - 1) % static_cast<int>(m_nav.size());
            SoundSystem::instance().play_ui_hover();
        }
        if (IsKeyPressed(KEY_ENTER) || IsKeyPressed(KEY_SPACE)) {
            SoundSystem::instance().play_ui_confirm();
            m_next_view = m_nav[static_cast<size_t>(m_selected)].target;
            return;
        }

        const int previous_hovered = m_hovered;
        if (keyboard_navigation) m_hovered = -1;
        else if (mouse_moved || IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            m_hovered = -1;
            for (size_t i = 0; i < m_nav.size(); ++i) {
                if (CheckCollisionPointRec(mouse_pos, m_nav[i].bounds)) {
                    m_hovered = static_cast<int>(i);
                    if (mouse_moved && previous_hovered != m_hovered) SoundSystem::instance().play_ui_hover();
                    m_selected = m_hovered;
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                        SoundSystem::instance().play_ui_click();
                        m_next_view = m_nav[i].target;
                        return;
                    }
                    break;
                }
            }
        }

        for (size_t i = 0; i < m_hover_anim.size(); ++i) {
            const float target = (static_cast<int>(i) == m_hovered || static_cast<int>(i) == m_selected) ? 1.0f : 0.0f;
            m_hover_anim[i] += (target - m_hover_anim[i]) * std::min(1.0f, dt * 11.0f);
        }

        const Rectangle badge = pilot_badge_bounds();
        m_badge_hovered = CheckCollisionPointRec(mouse_pos, badge);
        if (m_badge_hovered && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            SoundSystem::instance().play_ui_click();
            m_next_view = ViewType::PROFILE;
        } else if (IsKeyPressed(KEY_P)) {
            m_next_view = ViewType::PROFILE;
        }

        if (IsKeyPressed(KEY_ESCAPE)) m_next_view = ViewType::QUIT;
    }

    void draw() override {
        using namespace UI;
        ClearBackground(PAL_BG_VOID);

        const Texture2D backdrop = AssetManager::instance().get_texture("hero_vimana_wars.png");
        if (backdrop.id > 0) {
            const Rectangle src = { 0, 0, static_cast<float>(backdrop.width), static_cast<float>(backdrop.height) };
            const Rectangle dst = { 0, 0, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT) };
            DrawTexturePro(backdrop, src, dst, { 0, 0 }, 0.0f, { 178, 190, 218, 255 });
        }
        DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 5, 8, 19, 86 });
        DrawRectangleGradientH(0, 0, 555, SCREEN_HEIGHT, { 5, 8, 18, 242 }, { 5, 8, 18, 0 });
        DrawRectangleGradientV(0, SCREEN_HEIGHT - 120, SCREEN_WIDTH, 120, { 5, 8, 18, 0 }, { 5, 8, 18, 180 });

        for (const auto& star : m_stars) {
            DrawCircleV({ star.x, star.y }, star.radius, { 210, 235, 255, 95 });
        }

        const Font title_font = AssetManager::instance().title_font();
        const Font body_font = AssetManager::instance().body_font();
        const Font mono_font = AssetManager::instance().mono_font();

        DrawTextEx(title_font, "VIMANA WARS", { 54, 30 }, 31, 1.5f, PAL_PRIMARY_BRIGHT);
        DrawTextEx(mono_font, "THE RECLAMATION OF DHARMA  //  PILOT COMMAND", { 58, 72 }, 10, 1.0f, PAL_SECONDARY_BRIGHT);
        DrawLine(56, 103, 384, 103, ColorAlpha(PAL_PRIMARY, 0.59f));

        DrawPilotBadge(title_font, body_font);

        const int max_wave = std::max(1, DBSystem::instance().max_wave());
        const std::string act_line = "CAMPAIGN  //  ACT " + std::to_string(CampaignActForWave(max_wave)) +
                                     "   WAVE " + std::to_string(CampaignWaveWithinAct(max_wave)) +
                                     " / " + std::to_string(WAVES_PER_ACT);
        DrawTextEx(mono_font, act_line.c_str(), { 58, 112 }, 10, 1.0f, PAL_TEXT_MUTED);

        const int saved_wave = DBSystem::instance().continue_wave();
        if (saved_wave > 1 || DBSystem::instance().max_wave() > 1) {
            const Rectangle continue_rect = { 56, 132, 340, 36 };
            const Color accent = m_continue_hovered ? PAL_PRIMARY_BRIGHT : PAL_PRIMARY;
            DrawRectangleRec(continue_rect, ColorAlpha(PAL_PRIMARY, m_continue_hovered ? 0.20f : 0.09f));
            DrawRectangleLinesEx(continue_rect, 1.0f, ColorAlpha(accent, 0.73f));
            const std::string continue_label = saved_wave > 1
                ? "CONTINUE SORTIE  //  WAVE " + std::to_string(saved_wave)
                : "CONTINUE CAMPAIGN";
            DrawTextEx(body_font, continue_label.c_str(),
                       { continue_rect.x + 12, continue_rect.y + 10 }, 13, 1.0f, accent);
            DrawTextEx(mono_font, "C", { continue_rect.x + continue_rect.width - 23, continue_rect.y + 11 }, 10, 1.0f, PAL_TEXT_MUTED);
        }

        for (size_t i = 0; i < m_nav.size(); ++i) {
            const auto& item = m_nav[i];
            const float anim = m_hover_anim[i];
            const bool selected = static_cast<int>(i) == m_selected;
            const Color accent = item.accent;
            if (anim > 0.01f) {
                DrawRectangleRec({ item.bounds.x, item.bounds.y + 2, item.bounds.width, item.bounds.height - 4 },
                                 ColorAlpha(accent, 0.07f + 0.10f * anim));
            }
            DrawRectangleRec({ item.bounds.x, item.bounds.y + 5, selected ? 3.0f : 1.0f, item.bounds.height - 10 },
                             ColorAlpha(accent, selected ? 0.96f : 0.31f));
            const Color text_color = selected ? PAL_PRIMARY_CORE : Color{ 207, 219, 235, 235 };
            DrawTextEx(title_font, item.label.c_str(), { item.bounds.x + 18 + anim * 4.0f, item.bounds.y + 5 },
                       17 + anim * 1.0f, 1.0f, text_color);
            DrawTextEx(mono_font, item.shortcut.c_str(), { item.bounds.x + item.bounds.width - 22, item.bounds.y + 9 },
                       10, 1.0f, selected ? accent : Color{ 154, 168, 191, 210 });
            if (selected) {
                DrawLine(static_cast<int>(item.bounds.x + 18), static_cast<int>(item.bounds.y + item.bounds.height - 1),
                         static_cast<int>(item.bounds.x + 110), static_cast<int>(item.bounds.y + item.bounds.height - 1),
                         ColorAlpha(accent, 0.59f));
            }
        }

        DrawFlagship(title_font);
        DrawPilotProgress(body_font, mono_font);

        const char* footer = "W / S OR ↑ / ↓ NAVIGATE     ENTER SELECT     ESC EXIT";
        const Vector2 footer_size = MeasureTextEx(mono_font, footer, 9, 1.0f);
        DrawTextEx(mono_font, footer, { (SCREEN_WIDTH - footer_size.x) / 2.0f, SCREEN_HEIGHT - 22.0f }, 9, 1.0f,
                   ColorAlpha(PAL_TEXT_MUTED, 0.86f));
        if (g_scanlines_enabled) DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MENU; }

private:
    struct NavItem {
        Rectangle bounds;
        std::string label;
        ViewType target;
        Color accent;
        std::string shortcut;
    };
    struct Star { float x, y, radius, speed; };

    static Rectangle pilot_badge_bounds() { return { SCREEN_WIDTH - 286.0f, 24.0f, 246.0f, 57.0f }; }

    void DrawPilotBadge(Font title_font, Font body_font) const {
        const Rectangle badge = pilot_badge_bounds();
        DrawRectangleRec(badge, ColorAlpha(UI::PAL_BG_VOID, 0.80f));
        DrawRectangleLinesEx(badge, 1.0f, ColorAlpha(m_badge_hovered ? UI::PAL_PRIMARY_BRIGHT : UI::PAL_SECONDARY, 0.67f));
        UI::DrawCornerBrackets(badge, 7.0f, m_badge_hovered ? UI::PAL_PRIMARY : UI::PAL_SECONDARY);
        DrawTextEx(body_font, "PILOT DOSSIER  //  P", { badge.x + 11, badge.y + 7 }, 9, 1.0f, UI::PAL_TEXT_MUTED);
        std::string callsign = DBSystem::instance().player_name();
        if (callsign.size() > 18) callsign.resize(18);
        DrawTextEx(title_font, callsign.c_str(), { badge.x + 11, badge.y + 22 }, 15, 1.0f, UI::PAL_PRIMARY_CORE);
        const std::string id = AccountSystem::instance().game_id();
        DrawTextEx(body_font, (id + (AccountSystem::instance().is_logged_in() ? "  // CLOUD" : "  // LOCAL")).c_str(),
                   { badge.x + 11, badge.y + 41 }, 9, 1.0f,
                   AccountSystem::instance().is_logged_in() ? UI::PAL_HEALTH_HIGH : UI::PAL_SECONDARY_BRIGHT);
    }

    void DrawFlagship(Font title_font) const {
        const ShipArchetype* ship = GetShipArchetype(DBSystem::instance().equipped_ship());
        if (!ship) ship = GetShipArchetype("pushpaka");
        if (!ship) return;

        const float x = 690.0f;
        const float y = 408.0f + std::sin(m_ship_bob) * 6.0f;
        UI::DrawMandalaReticle({ x, y }, 105.0f, GetTime() * 0.28, ship->accent_color,
                               UI::PAL_PRIMARY, 0.32f);
        const Texture2D texture = AssetManager::instance().get_texture(ship->sprite_file);
        if (texture.id > 0) {
            const Rectangle src = { 0, 0, static_cast<float>(texture.width), static_cast<float>(texture.height) };
            const Rectangle dst = { x, y, 168, 168 };
            DrawTexturePro(texture, src, dst, { 84, 84 }, std::sin(m_ship_bob * 0.7f) * 2.0f, WHITE);
        }
        DrawCircleV({ x, y + 65 }, 4.0f + std::sin(m_ship_bob * 2.0f) * 1.2f, UI::PAL_SECONDARY_BRIGHT);
        const std::string ship_label = ship->name + "  //  EQUIPPED";
        const Vector2 label_size = MeasureTextEx(title_font, ship_label.c_str(), 13, 1.0f);
        DrawTextEx(title_font, ship_label.c_str(), { x - label_size.x / 2.0f, y + 89 }, 13, 1.0f, UI::PAL_PRIMARY_BRIGHT);
        DrawText("READY FOR DEPLOYMENT", static_cast<int>(x - 64), static_cast<int>(y + 108), 9, UI::PAL_TEXT_MUTED);
    }

    void DrawPilotProgress(Font body_font, Font mono_font) const {
        const float x = 56.0f;
        const float y = 510.0f;
        const int level = DBSystem::instance().pilot_level();
        const int xp = DBSystem::instance().pilot_xp_progress();
        DrawTextEx(body_font, ("WELCOME, " + DBSystem::instance().player_name()).c_str(), { x, y }, 16, 1.0f, UI::PAL_PRIMARY_BRIGHT);
        DrawTextEx(mono_font, ("PILOT LEVEL " + std::to_string(level)).c_str(), { x, y + 24 }, 10, 1.0f, UI::PAL_SECONDARY_BRIGHT);
        const std::string xp_line = std::to_string(xp) + " / " + std::to_string(DBSystem::PILOT_XP_PER_LEVEL) + " XP";
        DrawTextEx(mono_font, xp_line.c_str(), { x + 191, y + 24 }, 9, 1.0f, UI::PAL_TEXT_MUTED);
        const Rectangle bar = { x, y + 42, 252, 5 };
        DrawRectangleRec(bar, ColorAlpha(UI::PAL_TEXT_MUTED, 0.25f));
        const float ratio = std::clamp(static_cast<float>(xp) / DBSystem::PILOT_XP_PER_LEVEL, 0.0f, 1.0f);
        DrawRectangleRec({ bar.x, bar.y, bar.width * ratio, bar.height }, UI::PAL_SECONDARY_BRIGHT);
    }

    std::vector<NavItem> m_nav;
    std::vector<float> m_hover_anim;
    std::vector<Star> m_stars;
    ViewType m_next_view;
    int m_selected = 0;
    int m_hovered = -1;
    bool m_badge_hovered = false;
    bool m_continue_hovered = false;
    bool m_has_mouse_position = false;
    Vector2 m_last_mouse_pos = { 0.0f, 0.0f };
    float m_ship_bob = 0.0f;
};

} // namespace Vimana
