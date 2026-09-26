#pragma once
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "systems/db_system.hpp"
#include "systems/account_system.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

// ── BOOT VIEW ─────────────────────────────────────────────────────────────────
// Full-screen launch splash with a skippable progress presentation, then TITLE.
class BootView : public IView {
public:
    BootView() : m_next_view(ViewType::BOOT) { init(); }

    void init() override {
        m_next_view = ViewType::BOOT;
        m_timer = 0.0f;
        m_duration = 2.5f;
        m_bar_pct = 0.0f;

        // Staged boot presentation: the core systems are initialized before
        // the first view is shown, so these are launch-sequence cues rather
        // than claims about asynchronous asset loading.
        m_load_steps = {
            "FLIGHT SYSTEMS // INITIALIZING",
            "PILOT PROFILE // SYNCHRONIZING",
            "CAMPAIGN ROUTE // PREPARING",
            "WEAPON SYSTEMS // CALIBRATING",
            "FINAL LAUNCH CHECK",
            "READY FOR LAUNCH"
        };
        m_load_step = 0;
        m_load_timer = 0.0f;
        m_step_interval = m_duration / static_cast<float>(m_load_steps.size());
    }

    void update(float dt, Vector2 /*mouse_pos*/) override {
        m_timer += dt;
        m_bar_pct = std::min(1.0f, m_timer / m_duration);

        m_load_timer += dt;
        if (m_load_timer >= m_step_interval) {
            m_load_timer -= m_step_interval;
            if (m_load_step < (int)m_load_steps.size() - 1) m_load_step++;
        }

        // The boot presentation can be skipped with keyboard or mouse.
        if (m_timer >= m_duration || IsKeyPressed(KEY_SPACE) || IsKeyPressed(KEY_ENTER) ||
            IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            m_next_view = ViewType::TITLE;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();
        const float pulse = 0.5f + 0.5f * std::sin(GetTime() * 2.0f);

        // Use the existing cinematic artwork as a true full-screen boot plate.
        const Texture2D backdrop = AssetManager::instance().get_texture("hero_vimana_wars.png");
        if (backdrop.id > 0) {
            DrawTexturePro(backdrop,
                { 0, 0, static_cast<float>(backdrop.width), static_cast<float>(backdrop.height) },
                { 0, 0, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT) },
                { 0, 0 }, 0.0f, WHITE);
            DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 3, 8, 18, 95 });
            DrawRectangleGradientH(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT,
                                   { 3, 8, 18, 235 }, { 3, 8, 18, 24 });
        } else {
            // Keep a usable boot screen if the optional artwork is absent.
            for (int i = 0; i < 70; ++i) {
                const float x = static_cast<float>((i * 137) % SCREEN_WIDTH);
                const float y = static_cast<float>((i * 83) % SCREEN_HEIGHT);
                DrawCircle(static_cast<int>(x), static_cast<int>(y), (i % 3) + 1.0f,
                           ColorAlpha(COLOR_CYAN_BRIGHT, 0.25f));
            }
        }

        // Quiet rotating instrument mark keeps the right half of the artwork alive.
        UI::DrawMandalaReticle({ SCREEN_WIDTH * 0.76f, SCREEN_HEIGHT * 0.43f },
                               118.0f + 5.0f * pulse, GetTime() * 0.25,
                               COLOR_CYAN_BRIGHT, COLOR_GOLD_BRIGHT, 0.18f);

        // Compact logo and mission-ready hierarchy on the readable left side.
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            const float scale = 0.16f;
            DrawTextureEx(logo, { 66.0f, 54.0f }, 0.0f, scale, WHITE);
        } else {
            const char* title = "VIMANA WARS";
            DrawTextEx(font, title, { 72.0f, 76.0f }, 36, 1.5f, COLOR_GOLD_BRIGHT);
        }

        DrawTextEx(font, "ASTRAL COMBAT SYSTEMS", { 74.0f, 276.0f }, 22, 1.2f, COLOR_PARCHMENT);
        DrawTextEx(font, "PREPARING YOUR FLIGHT DECK", { 76.0f, 307.0f }, 12, 1.0f, COLOR_CYAN_BRIGHT);
        DrawRectangle(76, 338, 250, 2, ColorAlpha(COLOR_GOLD_BRIGHT, 0.7f));

        // Loading stage and percentage share one aligned, high-contrast panel.
        const Rectangle panel = { 58.0f, 440.0f, 784.0f, 112.0f };
        UI::DrawChamferedPanel(panel, COLOR_CYAN, { 7, 13, 25, 225 }, 5.0f);
        const std::string stage = m_load_step < static_cast<int>(m_load_steps.size())
            ? m_load_steps[m_load_step] : "READY FOR LAUNCH";
        DrawTextEx(font, stage.c_str(), { 78.0f, 458.0f }, 12, 1.0f, COLOR_PARCHMENT);
        const std::string percent = std::to_string(static_cast<int>(m_bar_pct * 100.0f)) + "%";
        const Vector2 percent_size = MeasureTextEx(font, percent.c_str(), 12, 1.0f);
        DrawTextEx(font, percent.c_str(), { 820.0f - percent_size.x, 458.0f }, 12, 1.0f, COLOR_GOLD_BRIGHT);

        const Rectangle bar_bg = { 78.0f, 484.0f, 744.0f, 8.0f };
        DrawRectangleRec(bar_bg, COLOR_SURFACE_HIGH);
        const int fill_width = static_cast<int>(bar_bg.width * m_bar_pct);
        if (fill_width > 0) {
            DrawRectangleGradientH(static_cast<int>(bar_bg.x), static_cast<int>(bar_bg.y),
                                   fill_width, static_cast<int>(bar_bg.height),
                                   COLOR_CYAN_BRIGHT, COLOR_GOLD_BRIGHT);
            const float marker_x = bar_bg.x + fill_width;
            DrawCircle(static_cast<int>(marker_x), static_cast<int>(bar_bg.y + bar_bg.height * 0.5f),
                       4.0f + pulse * 1.5f, COLOR_PARCHMENT);
        }
        DrawRectangleLinesEx(bar_bg, 1.0f, ColorAlpha(COLOR_MUTED, 0.75f));

        DrawText("VIMANA WARS  //  DESKTOP EDITION", 76, 521, 9, COLOR_MUTED);
        const char* skip = "SPACE / ENTER / CLICK  //  SKIP";
        const int skip_width = MeasureText(skip, 9);
        DrawText(skip, SCREEN_WIDTH - skip_width - 78, 521, 9,
                 ColorAlpha(COLOR_PARCHMENT, 0.65f + 0.3f * pulse));

        UI::DrawScanlines();
    }

    ViewType next_view()  const override { return m_next_view; }
    void reset_next_view() override      { m_next_view = ViewType::BOOT; }

private:
    ViewType m_next_view;
    float    m_timer;
    float    m_duration;
    float    m_bar_pct;
    float    m_load_timer;
    float    m_step_interval;
    int      m_load_step;
    std::vector<std::string> m_load_steps;
};

// ── TITLE VIEW ────────────────────────────────────────────────────────────────
// Title card with parallax starfield and pulsing PRESS SPACE prompt.
class TitleView : public IView {
public:
    TitleView() : m_next_view(ViewType::TITLE) { init(); }

    void init() override {
        m_next_view = ViewType::TITLE;
        m_timer = 0.0f;
        m_blink = 0.0f;
        m_stars.clear();
        for (int i = 0; i < 150; ++i) {
            m_stars.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                0.3f + (std::rand() % 25) / 10.0f
            });
        }
    }

    void update(float dt, Vector2 /*mouse_pos*/) override {
        m_timer += dt;
        m_blink += dt;

        for (auto& s : m_stars) {
            s.y += s.z * 18.0f * dt;
            if (s.y > SCREEN_HEIGHT) {
                s.y = 0;
                s.x = static_cast<float>(std::rand() % SCREEN_WIDTH);
            }
        }

        if (IsKeyPressed(KEY_SPACE) || IsKeyPressed(KEY_ENTER) ||
            IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Parallax stars (3 layers)
        for (const auto& s : m_stars) {
            unsigned char alpha = static_cast<unsigned char>(80 + s.z * 50);
            DrawCircle(static_cast<int>(s.x), static_cast<int>(s.y),
                       s.z * 0.6f, Color{200, 220, 255, alpha});
        }

        // Top sacred geometry arc
        float t = GetTime();
        for (int i = 0; i < 12; ++i) {
            float angle = (i / 12.0f) * 6.2831853f + t * 0.3f;
            float r = 260.0f;
            DrawCircle(
                static_cast<int>(SCREEN_WIDTH / 2 + std::cos(angle) * r),
                static_cast<int>(SCREEN_HEIGHT / 2 + std::sin(angle) * r),
                2.0f, ColorAlpha(COLOR_GOLD, 0.25f)
            );
        }
        DrawCircleLines(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 260.0f, ColorAlpha(COLOR_GOLD, 0.07f));

        // Main logo
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            float scale = 0.55f;
            float lw = logo.width * scale;
            float lh = logo.height * scale;
            DrawTextureEx(logo, { (SCREEN_WIDTH - lw) / 2.0f, 120 }, 0.0f, scale, WHITE);
        } else {
            const char* title = "VIMANA WARS";
            Vector2 tsz = MeasureTextEx(font, title, 60, 2.0f);
            DrawTextEx(font, title, { (SCREEN_WIDTH - tsz.x) / 2.0f, 140 }, 60, 2.0f, COLOR_GOLD_BRIGHT);
        }

        const char* tagline = "CELESTIAL ASTRAL COMBAT // ACT I · 30 WAVES";
        Vector2 tl_sz = MeasureTextEx(font, tagline, 13, 1.0f);
        DrawTextEx(font, tagline, { (SCREEN_WIDTH - tl_sz.x) / 2.0f, 310 }, 13, 1.0f, COLOR_CYAN_BRIGHT);

        // Dynamic Pilot badge
        UI::DrawChamferedPanel({ SCREEN_WIDTH / 2.0f - 195, 345, 390, 42 }, COLOR_GOLD, COLOR_SURFACE_LOW, 5.0f);
        std::string p_name = DBSystem::instance().player_name();
        std::string g_id = AccountSystem::instance().game_id();
        int max_w = DBSystem::instance().max_wave();
        std::string rank_title = (max_w >= 300) ? "MAHAYUDDHA LEGEND" :
                                 (max_w >= 210) ? "ARJUNA ACE" :
                                 (max_w >= 90)  ? "KSHATRIYA VANGUARD" : "ASTRAL PILOT";
        std::string pilot_line = "PILOT: " + p_name + "  //  " + g_id + "  //  " + rank_title;
        Vector2 pl_sz = MeasureTextEx(font, pilot_line.c_str(), 11, 1.0f);
        DrawTextEx(font, pilot_line.c_str(), { (SCREEN_WIDTH - pl_sz.x) / 2.0f, 359 }, 11, 1.0f, COLOR_GOLD_BRIGHT);

        // Pulsing PRESS SPACE
        float pulse = 0.5f + 0.5f * std::sin(m_blink * 3.5f);
        const char* prompt = "PRESS  SPACE  OR  CLICK  TO  BEGIN";
        Vector2 pr_sz = MeasureTextEx(font, prompt, 18, 1.5f);
        DrawTextEx(font, prompt,
            { (SCREEN_WIDTH - pr_sz.x) / 2.0f, 445 }, 18, 1.5f,
            ColorAlpha(COLOR_GOLD_BRIGHT, 0.55f + 0.45f * pulse));

        // Version
        DrawText("v2.0 // DESKTOP EDITION // FINAL YEAR PROJECT",
            SCREEN_WIDTH / 2 - 140, SCREEN_HEIGHT - 28, 10, COLOR_MUTED);

        UI::DrawScanlines();
    }

    ViewType next_view()  const override { return m_next_view; }
    void reset_next_view() override      { m_next_view = ViewType::TITLE; }

private:
    struct Star { float x, y, z; };
    ViewType         m_next_view;
    float            m_timer;
    float            m_blink;
    std::vector<Star>m_stars;
};

} // namespace Vimana
