#pragma once
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/sound_system.hpp"
#include "systems/db_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class SettingsView : public IView {
public:
    SettingsView() 
        : m_next_view(ViewType::SETTINGS), 
          m_active_tab(0),
          m_tab_audio({ 60, 95, 120, 32 }, "AUDIO", COLOR_GOLD_BRIGHT),
          m_tab_controls({ 190, 95, 120, 32 }, "CONTROLS", COLOR_CYAN_BRIGHT),
          m_tab_access({ 320, 95, 140, 32 }, "ACCESSIBILITY", COLOR_GREEN_BRIGHT)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::SETTINGS;

        float cx = SCREEN_WIDTH / 2.0f;
        m_btn_vol_down = UI::Button({ cx - 110, 160, 40, 30 }, "-", COLOR_GOLD);
        m_btn_vol_up = UI::Button({ cx + 70, 160, 40, 30 }, "+", COLOR_GOLD);

        m_btn_sfx_down = UI::Button({ cx - 110, 205, 40, 30 }, "-", COLOR_GOLD);
        m_btn_sfx_up = UI::Button({ cx + 70, 205, 40, 30 }, "+", COLOR_GOLD);

        m_btn_music_down = UI::Button({ cx - 110, 250, 40, 30 }, "-", COLOR_GOLD);
        m_btn_music_up = UI::Button({ cx + 70, 250, 40, 30 }, "+", COLOR_GOLD);

        m_btn_ui_down = UI::Button({ cx - 110, 295, 40, 30 }, "-", COLOR_GOLD);
        m_btn_ui_up = UI::Button({ cx + 70, 295, 40, 30 }, "+", COLOR_GOLD);

        m_btn_boss_down = UI::Button({ cx - 110, 340, 40, 30 }, "-", COLOR_GOLD);
        m_btn_boss_up = UI::Button({ cx + 70, 340, 40, 30 }, "+", COLOR_GOLD);

        m_btn_fullscreen = UI::Button({ cx - 110, 395, 220, 36 }, "TOGGLE FULLSCREEN", COLOR_CYAN_BRIGHT);
        m_btn_colorblind = UI::Button({ cx + 20, 160, 190, 34 }, "TOGGLE PALETTE", COLOR_GREEN_BRIGHT);
        m_btn_shake = UI::Button({ cx + 20, 245, 190, 34 }, "TOGGLE SHAKE", COLOR_CYAN_BRIGHT);
        m_btn_scanlines = UI::Button({ cx + 20, 330, 190, 34 }, "TOGGLE SCANLINES", COLOR_GOLD_BRIGHT);

        m_btn_back = UI::Button({ 40, 520, 110, 36 }, "SAVE & BACK", COLOR_MUTED);
        m_btn_reset_defaults = UI::Button({ SCREEN_WIDTH - 230, 520, 190, 36 }, "RESET DEFAULTS", COLOR_RED_BRIGHT);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            DBSystem::instance().save_game();
            m_next_view = ViewType::MENU;
        }

        if (m_btn_reset_defaults.update(mouse_pos)) {
            SoundSystem::instance().set_master_volume(1.0f);
            SoundSystem::instance().set_sfx_volume(0.8f);
            SoundSystem::instance().set_music_volume(0.7f);
            SoundSystem::instance().set_ui_volume(0.8f);
            SoundSystem::instance().set_boss_volume(0.9f);
            g_colorblind_mode = false;
            g_screen_shake_enabled = true;
            g_scanlines_enabled = true;
            DBSystem::instance().save_game();
        }

        // Tab Switching
        if (m_tab_audio.update(mouse_pos)) m_active_tab = 0;
        if (m_tab_controls.update(mouse_pos)) m_active_tab = 1;
        if (m_tab_access.update(mouse_pos)) m_active_tab = 2;

        if (m_active_tab == 0) {
            // Master Volume
            if (m_btn_vol_down.update(mouse_pos)) {
                SoundSystem::instance().set_master_volume(SoundSystem::instance().master_volume() - 0.1f);
            }
            if (m_btn_vol_up.update(mouse_pos)) {
                SoundSystem::instance().set_master_volume(SoundSystem::instance().master_volume() + 0.1f);
            }

            // SFX Volume
            if (m_btn_sfx_down.update(mouse_pos)) {
                SoundSystem::instance().set_sfx_volume(SoundSystem::instance().sfx_volume() - 0.1f);
            }
            if (m_btn_sfx_up.update(mouse_pos)) {
                SoundSystem::instance().set_sfx_volume(SoundSystem::instance().sfx_volume() + 0.1f);
            }

            // Music Volume
            if (m_btn_music_down.update(mouse_pos)) {
                SoundSystem::instance().set_music_volume(SoundSystem::instance().music_volume() - 0.1f);
            }
            if (m_btn_music_up.update(mouse_pos)) {
                SoundSystem::instance().set_music_volume(SoundSystem::instance().music_volume() + 0.1f);
            }

            // UI Audio Volume
            if (m_btn_ui_down.update(mouse_pos)) {
                SoundSystem::instance().set_ui_volume(SoundSystem::instance().ui_volume() - 0.1f);
            }
            if (m_btn_ui_up.update(mouse_pos)) {
                SoundSystem::instance().set_ui_volume(SoundSystem::instance().ui_volume() + 0.1f);
            }

            // Boss Audio Volume
            if (m_btn_boss_down.update(mouse_pos)) {
                SoundSystem::instance().set_boss_volume(SoundSystem::instance().boss_volume() - 0.1f);
            }
            if (m_btn_boss_up.update(mouse_pos)) {
                SoundSystem::instance().set_boss_volume(SoundSystem::instance().boss_volume() + 0.1f);
            }

            // Fullscreen Toggle
            if (m_btn_fullscreen.update(mouse_pos)) {
                ToggleFullscreen();
            }
        } else if (m_active_tab == 2) {
            if (m_btn_colorblind.update(mouse_pos)) {
                g_colorblind_mode = !g_colorblind_mode;
            }
            if (m_btn_shake.update(mouse_pos)) {
                g_screen_shake_enabled = !g_screen_shake_enabled;
            }
            if (m_btn_scanlines.update(mouse_pos)) {
                g_scanlines_enabled = !g_scanlines_enabled;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(title_font, "ASTRAL SYSTEM SETTINGS & TELEMETRY", { 45, 30 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        // Tab Navigation
        m_tab_audio.draw(title_font);
        m_tab_controls.draw(title_font);
        m_tab_access.draw(title_font);

        // Content Area
        Rectangle content_box = { 30, 135, 840, 365 };
        UI::DrawChamferedPanel(content_box, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        float cx = SCREEN_WIDTH / 2.0f;

        if (m_active_tab == 0) {
            // ── AUDIO TAB ──
            DrawTextEx(body_font, "MASTER AUDIO VOLUME", { cx - 220, 166 }, 13, 1.0f, COLOR_PARCHMENT);
            m_btn_vol_down.draw(title_font);
            int vol_pct = static_cast<int>(SoundSystem::instance().master_volume() * 100);
            DrawTextEx(title_font, (std::to_string(vol_pct) + "%").c_str(), { cx - 35, 166 }, 14, 1.0f, COLOR_GOLD_BRIGHT);
            m_btn_vol_up.draw(title_font);

            DrawTextEx(body_font, "SOUND EFFECTS (SFX)", { cx - 220, 211 }, 13, 1.0f, COLOR_PARCHMENT);
            m_btn_sfx_down.draw(title_font);
            int sfx_pct = static_cast<int>(SoundSystem::instance().sfx_volume() * 100);
            DrawTextEx(title_font, (std::to_string(sfx_pct) + "%").c_str(), { cx - 35, 211 }, 14, 1.0f, COLOR_CYAN_BRIGHT);
            m_btn_sfx_up.draw(title_font);

            DrawTextEx(body_font, "CELESTIAL SOUNDTRACK", { cx - 220, 256 }, 13, 1.0f, COLOR_PARCHMENT);
            m_btn_music_down.draw(title_font);
            int mus_pct = static_cast<int>(SoundSystem::instance().music_volume() * 100);
            DrawTextEx(title_font, (std::to_string(mus_pct) + "%").c_str(), { cx - 35, 256 }, 14, 1.0f, COLOR_GREEN_BRIGHT);
            m_btn_music_up.draw(title_font);

            DrawTextEx(body_font, "TACTICAL UI AUDIO", { cx - 220, 301 }, 13, 1.0f, COLOR_PARCHMENT);
            m_btn_ui_down.draw(title_font);
            int ui_pct = static_cast<int>(SoundSystem::instance().ui_volume() * 100);
            DrawTextEx(title_font, (std::to_string(ui_pct) + "%").c_str(), { cx - 35, 301 }, 14, 1.0f, COLOR_PURPLE_BRIGHT);
            m_btn_ui_up.draw(title_font);

            DrawTextEx(body_font, "BOSS COMBAT DYNAMICS", { cx - 220, 346 }, 13, 1.0f, COLOR_PARCHMENT);
            m_btn_boss_down.draw(title_font);
            int boss_pct = static_cast<int>(SoundSystem::instance().boss_volume() * 100);
            DrawTextEx(title_font, (std::to_string(boss_pct) + "%").c_str(), { cx - 35, 346 }, 14, 1.0f, COLOR_RED_BRIGHT);
            m_btn_boss_up.draw(title_font);

            m_btn_fullscreen.draw(title_font);

        } else if (m_active_tab == 1) {
            // ── CONTROLS TAB ──
            float lx = 80.0f;
            float ly = 160.0f;

            DrawTextEx(title_font, "FLIGHT CONTROLS & WEAPON SYSTEMS", { lx, ly }, 16, 1.0f, COLOR_GOLD_BRIGHT);
            DrawLine(static_cast<int>(lx), static_cast<int>(ly + 22), static_cast<int>(lx + 700), static_cast<int>(ly + 22), COLOR_SURFACE_MID);

            ly += 35.0f;
            auto draw_binding = [&](const char* action, const char* key, Color col) {
                DrawTextEx(body_font, action, { lx + 20, ly }, 13, 1.0f, COLOR_PARCHMENT);
                DrawTextEx(title_font, key, { lx + 360, ly - 1 }, 12, 1.0f, col);
                ly += 26.0f;
            };

            draw_binding("VIMANA THRUSTER MOVEMENT", "[ W / A / S / D ] or [ ARROW KEYS ]", COLOR_GOLD_BRIGHT);
            draw_binding("PRIMARY WEAPONS (ASTRA CANNON)", "[ LEFT MOUSE BUTTON ] or [ J ]", COLOR_CYAN_BRIGHT);
            draw_binding("WARP DASH / PERFECT DODGE", "[ SPACEBAR ]", COLOR_GREEN_BRIGHT);
            draw_binding("CHAKRAM CLEAVER DEPLOY", "[ Q ] or [ E ]", COLOR_ORANGE_BRIGHT);
            draw_binding("BRAHMASTRA SCREEN DETONATION", "[ F ]", COLOR_RED_BRIGHT);
            draw_binding("SOMA AMPOULE (EMERGENCY HEAL)", "[ C ]", COLOR_GREEN_BRIGHT);
            draw_binding("VAJRA FLARE (DEFENSE BARRIER)", "[ V ]", COLOR_PURPLE_BRIGHT);
            draw_binding("TACTICAL PAUSE & FLIGHT TELEMETRY", "[ ESC ]", COLOR_MUTED);

        } else if (m_active_tab == 2) {
            // ── ACCESSIBILITY TAB ──
            DrawTextEx(body_font, "HIGH-CONTRAST / COLORBLIND MODE", { cx - 220, 160 }, 13, 1.0f, COLOR_PARCHMENT);
            std::string cb_status = g_colorblind_mode ? "ACTIVE // HIGH-CONTRAST PALETTE" : "OFF // STANDARD VEDIC PALETTE";
            DrawTextEx(body_font, cb_status.c_str(), { cx - 220, 180 }, 11, 1.0f, g_colorblind_mode ? COLOR_GREEN_BRIGHT : COLOR_MUTED);
            m_btn_colorblind.draw(title_font);

            DrawTextEx(body_font, "SCREEN SHAKE INTENSITY", { cx - 220, 245 }, 13, 1.0f, COLOR_PARCHMENT);
            std::string shake_status = g_screen_shake_enabled ? "ENABLED // FULL IMPACT FEEDBACK" : "DISABLED // STATIC CAMERA";
            DrawTextEx(body_font, shake_status.c_str(), { cx - 220, 265 }, 11, 1.0f, g_screen_shake_enabled ? COLOR_CYAN_BRIGHT : COLOR_MUTED);
            m_btn_shake.draw(title_font);

            DrawTextEx(body_font, "CRT SCANLINE OVERLAY", { cx - 220, 330 }, 13, 1.0f, COLOR_PARCHMENT);
            std::string scan_status = g_scanlines_enabled ? "ENABLED // RETRO WAR CONSOLE" : "DISABLED // CRISP HI-DEF";
            DrawTextEx(body_font, scan_status.c_str(), { cx - 220, 350 }, 11, 1.0f, g_scanlines_enabled ? COLOR_GOLD_BRIGHT : COLOR_MUTED);
            m_btn_scanlines.draw(title_font);
        }

        m_btn_back.draw(title_font);
        m_btn_reset_defaults.draw(title_font);
        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::SETTINGS; }

private:
    ViewType m_next_view;
    int m_active_tab;

    UI::Button m_tab_audio;
    UI::Button m_tab_controls;
    UI::Button m_tab_access;

    UI::Button m_btn_vol_down;
    UI::Button m_btn_vol_up;
    UI::Button m_btn_sfx_down;
    UI::Button m_btn_sfx_up;
    UI::Button m_btn_music_down;
    UI::Button m_btn_music_up;
    UI::Button m_btn_ui_down;
    UI::Button m_btn_ui_up;
    UI::Button m_btn_boss_down;
    UI::Button m_btn_boss_up;
    UI::Button m_btn_fullscreen;
    UI::Button m_btn_colorblind;
    UI::Button m_btn_shake;
    UI::Button m_btn_scanlines;
    UI::Button m_btn_back;
    UI::Button m_btn_reset_defaults;
};

} // namespace Vimana
