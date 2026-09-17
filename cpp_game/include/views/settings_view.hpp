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
    SettingsView() : m_next_view(ViewType::SETTINGS) {
        init();
    }

    void init() override {
        m_next_view = ViewType::SETTINGS;

        float cx = SCREEN_WIDTH / 2.0f;
        m_btn_vol_down = UI::Button({ cx - 110, 160, 40, 36 }, "-", COLOR_GOLD);
        m_btn_vol_up = UI::Button({ cx + 70, 160, 40, 36 }, "+", COLOR_GOLD);

        m_btn_sfx_down = UI::Button({ cx - 110, 220, 40, 36 }, "-", COLOR_GOLD);
        m_btn_sfx_up = UI::Button({ cx + 70, 220, 40, 36 }, "+", COLOR_GOLD);

        m_btn_music_down = UI::Button({ cx - 110, 280, 40, 36 }, "-", COLOR_GOLD);
        m_btn_music_up = UI::Button({ cx + 70, 280, 40, 36 }, "+", COLOR_GOLD);

        m_btn_fullscreen = UI::Button({ cx - 110, 350, 220, 38 }, "TOGGLE FULLSCREEN", COLOR_CYAN_BRIGHT);
        m_btn_back = UI::Button({ 40, 520, 110, 36 }, "SAVE & BACK", COLOR_MUTED);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            DBSystem::instance().save_game();
            m_next_view = ViewType::MENU;
        }

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
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "ASTRAL SYSTEM SETTINGS", { 45, 30 }, 24, 1.0f, COLOR_GOLD_BRIGHT);

        UI::DrawChamferedPanel({ SCREEN_WIDTH / 2.0f - 240, 100, 480, 390 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        float cx = SCREEN_WIDTH / 2.0f;

        // Master Volume
        DrawText("MASTER AUDIO VOLUME", cx - 200, 170, 13, COLOR_PARCHMENT);
        m_btn_vol_down.draw(font);
        int vol_pct = static_cast<int>(SoundSystem::instance().master_volume() * 100);
        DrawText((std::to_string(vol_pct) + "%").c_str(), cx - 35, 170, 15, COLOR_GOLD_BRIGHT);
        m_btn_vol_up.draw(font);

        // SFX Volume
        DrawText("SOUND EFFECTS (SFX)", cx - 200, 230, 13, COLOR_PARCHMENT);
        m_btn_sfx_down.draw(font);
        int sfx_pct = static_cast<int>(SoundSystem::instance().sfx_volume() * 100);
        DrawText((std::to_string(sfx_pct) + "%").c_str(), cx - 35, 230, 15, COLOR_CYAN_BRIGHT);
        m_btn_sfx_up.draw(font);

        // Music Volume
        DrawText("CELESTIAL SOUNDTRACK", cx - 200, 290, 13, COLOR_PARCHMENT);
        m_btn_music_down.draw(font);
        int mus_pct = static_cast<int>(SoundSystem::instance().music_volume() * 100);
        DrawText((std::to_string(mus_pct) + "%").c_str(), cx - 35, 290, 15, COLOR_GREEN_BRIGHT);
        m_btn_music_up.draw(font);

        // Display
        m_btn_fullscreen.draw(font);
        m_btn_back.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::SETTINGS; }

private:
    ViewType m_next_view;
    UI::Button m_btn_vol_down;
    UI::Button m_btn_vol_up;
    UI::Button m_btn_sfx_down;
    UI::Button m_btn_sfx_up;
    UI::Button m_btn_music_down;
    UI::Button m_btn_music_up;
    UI::Button m_btn_fullscreen;
    UI::Button m_btn_back;
};

} // namespace Vimana
