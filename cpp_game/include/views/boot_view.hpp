#pragma once
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

// ── BOOT VIEW ─────────────────────────────────────────────────────────────────
// 2-second animated logo splash with loading bar, then auto-advances to TITLE.
class BootView : public IView {
public:
    BootView() : m_next_view(ViewType::BOOT) { init(); }

    void init() override {
        m_next_view = ViewType::BOOT;
        m_timer = 0.0f;
        m_duration = 2.5f;
        m_bar_pct = 0.0f;

        // Simulate load steps
        m_load_steps = {
            "Initializing Astral Combat Engine...",
            "Loading Vimana Fleet Schematics...",
            "Synchronizing Vedic Boon Database...",
            "Calibrating Weapon Systems...",
            "Establishing Celestial Network Link...",
            "Ready."
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

        // SPACE or any key skips boot
        if (m_timer >= m_duration || IsKeyPressed(KEY_SPACE) || IsKeyPressed(KEY_ENTER)) {
            m_next_view = ViewType::TITLE;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Sacred geometry background circle
        float pulse = 0.5f + 0.5f * std::sin(GetTime() * 2.0f);
        DrawCircleLines(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 180.0f + 20.0f * pulse,
                        ColorAlpha(COLOR_GOLD, 0.12f + 0.08f * pulse));
        DrawCircleLines(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 220.0f + 20.0f * pulse,
                        ColorAlpha(COLOR_CYAN, 0.06f));

        // Logo or text title
        Texture2D logo = AssetManager::instance().get_texture("vimana_wars_logo.png");
        if (logo.id > 0) {
            float scale = 0.45f;
            float lw = logo.width * scale;
            float lh = logo.height * scale;
            DrawTextureEx(logo, { (SCREEN_WIDTH - lw) / 2.0f, (SCREEN_HEIGHT / 2.0f) - lh - 30.0f }, 0.0f, scale, WHITE);
        } else {
            const char* title = "VIMANA WARS";
            Vector2 tsz = MeasureTextEx(font, title, 52, 2.0f);
            DrawTextEx(font, title, { (SCREEN_WIDTH - tsz.x) / 2.0f, 185 }, 52, 2.0f, COLOR_GOLD_BRIGHT);
            const char* sub = "CELESTIAL ASTRAL COMBAT";
            Vector2 ssz = MeasureTextEx(font, sub, 16, 1.0f);
            DrawTextEx(font, sub, { (SCREEN_WIDTH - ssz.x) / 2.0f, 248 }, 16, 1.0f, COLOR_CYAN_BRIGHT);
        }

        // Loading bar
        Rectangle bar_bg = { SCREEN_WIDTH / 2.0f - 200, SCREEN_HEIGHT / 2.0f + 90, 400, 10 };
        Rectangle bar_fg = { bar_bg.x, bar_bg.y, bar_bg.width * m_bar_pct, bar_bg.height };
        DrawRectangleRec(bar_bg, COLOR_SURFACE_HIGH);
        DrawRectangleGradientH(
            static_cast<int>(bar_fg.x), static_cast<int>(bar_fg.y),
            static_cast<int>(bar_fg.width), static_cast<int>(bar_fg.height),
            COLOR_CYAN, COLOR_GOLD_BRIGHT
        );
        DrawRectangleLinesEx(bar_bg, 1.0f, COLOR_MUTED);

        // Current load step text
        if (m_load_step < (int)m_load_steps.size()) {
            const char* step_text = m_load_steps[m_load_step].c_str();
            Vector2 st_sz = MeasureTextEx(font, step_text, 11, 1.0f);
            DrawTextEx(font, step_text,
                { (SCREEN_WIDTH - st_sz.x) / 2.0f, bar_bg.y + 18 }, 11, 1.0f, COLOR_MUTED);
        }

        // Version & engine tag
        DrawText("v2.0 // RAYLIB 6.0 + C++20 + SQLITE3",
            SCREEN_WIDTH / 2 - 105, SCREEN_HEIGHT - 30, 10, COLOR_SURFACE_HIGH);

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

        const char* tagline = "CELESTIAL ASTRAL COMBAT // THE 7 REALMS OF MAHAYUDDHA";
        Vector2 tl_sz = MeasureTextEx(font, tagline, 13, 1.0f);
        DrawTextEx(font, tagline, { (SCREEN_WIDTH - tl_sz.x) / 2.0f, 310 }, 13, 1.0f, COLOR_CYAN_BRIGHT);

        // Pilot badge
        UI::DrawChamferedPanel({ SCREEN_WIDTH / 2.0f - 175, 345, 350, 42 }, COLOR_GOLD, COLOR_SURFACE_LOW, 5.0f);
        const char* pilot_line = "PILOT: CHETAN  //  VMN-7704  //  ARJUNA ACE";
        Vector2 pl_sz = MeasureTextEx(font, pilot_line, 12, 1.0f);
        DrawTextEx(font, pilot_line, { (SCREEN_WIDTH - pl_sz.x) / 2.0f, 358 }, 12, 1.0f, COLOR_GOLD_BRIGHT);

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
