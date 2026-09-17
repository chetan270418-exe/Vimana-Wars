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
        m_btn_vol_down = UI::Button({ cx - 110, 180, 40, 34 }, "-", COLOR_GOLD);
        m_btn_vol_up = UI::Button({ cx + 70, 180, 40, 34 }, "+", COLOR_GOLD);

        m_btn_sfx_down = UI::Button({ cx - 110, 235, 40, 34 }, "-", COLOR_GOLD);
        m_btn_sfx_up = UI::Button({ cx + 70, 235, 40, 34 }, "+", COLOR_GOLD);

        m_btn_music_down = UI::Button({ cx - 110, 290, 40, 34 }, "-", COLOR_GOLD);
        m_btn_music_up = UI::Button({ cx + 70, 290, 40, 34 }, "+", COLOR_GOLD);

        m_btn_fullscreen = UI::Button({ cx - 110, 350, 220, 36 }, "TOGGLE FULLSCREEN", COLOR_CYAN_BRIGHT);
        m_btn_colorblind = UI::Button({ cx - 110, 260, 220, 36 }, "TOGGLE COLORBLIND", COLOR_GREEN_BRIGHT);

        m_btn_back = UI::Button({ 40, 520, 110, 36 }, "SAVE & BACK", COLOR_MUTED);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            DBSystem::instance().save_game();
            m_next_view = ViewType::MENU;
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

            // Fullscreen Toggle
            if (m_btn_fullscreen.update(mouse_pos)) {
                ToggleFullscreen();
            }
        } else if (m_active_tab == 2) {
            if (m_btn_colorblind.update(mouse_pos)) {
                g_colorblind_mode = !g_colorblind_mode;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "ASTRAL SYSTEM SETTINGS & TELEMETRY", { 45, 30 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        // Tab Navigation
        m_tab_audio.draw(font);
        m_tab_controls.draw(font);
        m_tab_access.draw(font);

        // Content Area
        Rectangle content_box = { 30, 135, 840, 365 };
        UI::DrawChamferedPanel(content_box, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        float cx = SCREEN_WIDTH / 2.0f;

        if (m_active_tab == 0) {
            // ── AUDIO TAB ──
            DrawText("MASTER AUDIO VOLUME", cx - 200, 190, 13, COLOR_PARCHMENT);
            m_btn_vol_down.draw(font);
            int vol_pct = static_cast<int>(SoundSystem::instance().master_volume() * 100);
            DrawText((std::to_string(vol_pct) + "%").c_str(), cx - 35, 190, 15, COLOR_GOLD_BRIGHT);
            m_btn_vol_up.draw(font);

            DrawText("SOUND EFFECTS (SFX)", cx - 200, 245, 13, COLOR_PARCHMENT);
            m_btn_sfx_down.draw(font);
            int sfx_pct = static_cast<int>(SoundSystem::instance().sfx_volume() * 100);
            DrawText((std::to_string(sfx_pct) + "%").c_str(), cx - 35, 245, 15, COLOR_CYAN_BRIGHT);
            m_btn_sfx_up.draw(font);

            DrawText("CELESTIAL SOUNDTRACK", cx - 200, 300, 13, COLOR_PARCHMENT);
            m_btn_music_down.draw(font);
            int mus_pct = static_cast<int>(SoundSystem::instance().music_volume() * 100);
            DrawText((std::to_string(mus_pct) + "%").c_str(), cx - 35, 300, 15, COLOR_GREEN_BRIGHT);
            m_btn_music_up.draw(font);

            m_btn_fullscreen.draw(font);

        } else if (m_active_tab == 1) {
            // ── CONTROLS TAB ──
            float lx = 80.0f;
            float ly = 160.0f;

            DrawTextEx(font, "FLIGHT CONTROLS & WEAPON SYSTEMS", { lx, ly }, 16, 1.0f, COLOR_GOLD_BRIGHT);
            DrawLine(lx, ly + 22, lx + 700, ly + 22, COLOR_SURFACE_MID);

            ly += 35.0f;
            auto draw_binding = [&](const char* action, const char* key, Color col) {
                DrawText(action, lx + 20, ly, 13, COLOR_PARCHMENT);
                DrawText(key, lx + 360, ly, 13, col);
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
            DrawText("HIGH-CONTRAST / COLORBLIND MODE", cx - 220, 200, 14, COLOR_PARCHMENT);
            std::string cb_status = g_colorblind_mode ? "ACTIVE // HIGH-CONTRAST PALETTE" : "STANDARD // VEDIC PALETTE";
            Color cb_col = g_colorblind_mode ? COLOR_GREEN_BRIGHT : COLOR_MUTED;
            DrawText(cb_status.c_str(), cx - 220, 225, 12, cb_col);
            m_btn_colorblind.draw(font);

            DrawText("SCREEN SHAKE REDUCTION", cx - 220, 325, 14, COLOR_PARCHMENT);
            DrawText("STANDARD // ACTIVE WITH IMPACT INTENSITY", cx - 220, 348, 12, COLOR_CYAN_BRIGHT);

            DrawText("CRT SCANLINE OVERLAY", cx - 220, 385, 14, COLOR_PARCHMENT);
            DrawText("ACTIVE // CELESTIAL WAR CONSOLE SIMULATION", cx - 220, 408, 12, COLOR_GOLD_BRIGHT);
        }

        m_btn_back.draw(font);
        UI::DrawScanlines();
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
    UI::Button m_btn_fullscreen;
    UI::Button m_btn_colorblind;
    UI::Button m_btn_back;
};

} // namespace Vimana
