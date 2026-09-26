#pragma once
#include <algorithm>
#include <sstream>
#include <string>
#include "raylib.h"
#include "core/campaign_content.hpp"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "entities/ship_archetypes.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "views/view_interface.hpp"

namespace Vimana {

class MissionBriefingView : public IView {
public:
    MissionBriefingView()
        : m_next_view(ViewType::MISSION_BRIEFING),
          m_ship(&SHIP_FLEET.front()),
          m_btn_launch({ SCREEN_WIDTH - 290, SCREEN_HEIGHT - 66, 255, 42 }, "LAUNCH SORTIE >>", COLOR_GOLD_BRIGHT),
          m_btn_back({ 35, SCREEN_HEIGHT - 66, 190, 42 }, "<< RETURN TO LOADOUT", COLOR_MUTED) {}

    void set_mission(int wave, const ShipArchetype* ship, Difficulty difficulty) {
        m_wave = std::clamp(wave, 1, WAVES_PER_ACT * static_cast<int>(CAMPAIGN_REALMS.size()));
        if (ship) m_ship = ship;
        m_difficulty = difficulty;
    }

    void init() override { m_next_view = ViewType::MISSION_BRIEFING; }

    void update(float, Vector2 mouse_pos) override {
        const bool launch_clicked = m_btn_launch.update(mouse_pos);
        const bool back_clicked = m_btn_back.update(mouse_pos);
        if (launch_clicked || IsKeyPressed(KEY_ENTER) || IsKeyPressed(KEY_SPACE)) {
            m_next_view = ViewType::GAMEPLAY;
        } else if (back_clicked || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::LOADOUT;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        const Texture2D backdrop = AssetManager::instance().get_texture("hero_vimana_wars.png");
        if (backdrop.id > 0) {
            DrawTexturePro(backdrop,
                { 0, 0, static_cast<float>(backdrop.width), static_cast<float>(backdrop.height) },
                { 0, 0, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT) },
                { 0, 0 }, 0.0f, { 120, 138, 168, 255 });
        }
        DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 5, 8, 16, 218 });

        const Font title_font = AssetManager::instance().title_font();
        const Font body_font = AssetManager::instance().body_font();
        const CampaignRealm& realm = GetCampaignRealmForWave(m_wave);
        const CampaignStoryEvent* story = GetCampaignStoryEvent(m_wave);
        const int act = CampaignActForWave(m_wave);
        const int act_wave = CampaignWaveWithinAct(m_wave);

        DrawTextEx(title_font, "MISSION BRIEFING // PILOT REVIEW", { 38, 22 }, 23, 1.0f, COLOR_GOLD_BRIGHT);
        const std::string subtitle = "ACT " + std::to_string(act) + " OF " + std::to_string(CAMPAIGN_REALMS.size()) +
            "  //  " + realm.name + "  //  WAVE " + std::to_string(act_wave) + "/" + std::to_string(WAVES_PER_ACT) +
            "  //  " + difficulty_name();
        DrawTextEx(body_font, subtitle.c_str(), { 40, 55 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

        const Rectangle intel = { 36, 91, 518, 395 };
        UI::DrawYantraPanel(intel, realm.accent_color, COLOR_SURFACE_LOW, 7.0f, true);
        DrawTextEx(title_font, realm.sanskrit_title, { 57, 109 }, 17, 1.0f, COLOR_GOLD_BRIGHT);
        DrawTextEx(body_font, ("THEATER // " + std::string(realm.name)).c_str(), { 59, 135 }, 10, 1.0f, COLOR_CYAN_BRIGHT);

        DrawTextEx(body_font, story ? "TRANSMISSION // PRIORITY INTEL" : "THEATER INTEL", { 59, 169 }, 10, 1.0f, COLOR_GOLD_BRIGHT);
        if (story) {
            DrawTextEx(body_font, story->speaker, { 59, 188 }, 9, 1.0f, COLOR_CYAN_BRIGHT);
            DrawTextEx(title_font, story->title, { 59, 207 }, 14, 1.0f, COLOR_PARCHMENT);
            draw_wrapped(body_font, story->message, { 59, 233 }, 466, 12, COLOR_PARCHMENT);
        } else {
            draw_wrapped(body_font, realm.description, { 59, 193 }, 466, 12, COLOR_PARCHMENT);
        }

        DrawLine(59, 310, 530, 310, ColorAlpha(realm.accent_color, 0.55f));
        DrawTextEx(body_font, "SORTIE OBJECTIVE", { 59, 326 }, 10, 1.0f, COLOR_GOLD_BRIGHT);
        draw_wrapped(body_font,
            "Clear wave " + std::to_string(m_wave) + " and push through the act's mixed enemy formations.",
            { 59, 347 }, 466, 12, COLOR_PARCHMENT);
        DrawTextEx(body_font, ("ACT GUARDIAN // " + std::string(realm.boss_name) + " // WAVE " + std::to_string(realm.boss_wave)).c_str(),
                   { 59, 405 }, 10, 1.0f, COLOR_RED_BRIGHT);
        DrawTextEx(body_font, ("REALM MODIFIER // " + std::string(realm.modifier_desc)).c_str(),
                   { 59, 430 }, 10, 1.0f, COLOR_CYAN_BRIGHT);

        const Rectangle craft = { 574, 91, 290, 395 };
        UI::DrawChamferedPanel(craft, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 7.0f);
        DrawTextEx(title_font, "ASSIGNED VIMANA", { 595, 110 }, 15, 1.0f, COLOR_GOLD_BRIGHT);
        DrawTextEx(body_font, m_ship->name.c_str(), { 596, 139 }, 14, 1.0f, COLOR_CYAN_BRIGHT);
        DrawTextEx(body_font, m_ship->role.c_str(), { 596, 160 }, 10, 1.0f, COLOR_MUTED);

        const Texture2D ship_texture = AssetManager::instance().get_texture(m_ship->sprite_file);
        if (ship_texture.id > 0) {
            const Rectangle source = { 0, 0, static_cast<float>(ship_texture.width), static_cast<float>(ship_texture.height) };
            const Rectangle destination = { 719, 236, 116, 96 };
            DrawCircleLines(719, 236, 58, ColorAlpha(COLOR_CYAN_BRIGHT, 0.45f));
            DrawTexturePro(ship_texture, source, destination, { destination.width / 2.0f, destination.height / 2.0f }, 0.0f, WHITE);
        } else {
            DrawCircle(719, 236, 30, m_ship->accent_color);
            DrawCircleLines(719, 236, 39, COLOR_CYAN_BRIGHT);
        }

        DrawTextEx(body_font, ("SIGNATURE // " + ShipSignatureName(*m_ship)).c_str(), { 596, 304 }, 10, 1.0f, COLOR_GOLD_BRIGHT);
        draw_wrapped(body_font, ShipSignatureDescription(*m_ship), { 596, 323 }, 244, 10, COLOR_PARCHMENT);
        DrawLine(595, 370, 842, 370, ColorAlpha(COLOR_CYAN_BRIGHT, 0.45f));
        DrawTextEx(body_font, "REALM HAZARD", { 596, 384 }, 10, 1.0f, COLOR_RED_BRIGHT);
        draw_wrapped(body_font, realm.modifier_desc, { 596, 402 }, 244, 10, COLOR_PARCHMENT);

        DrawTextEx(body_font, "WASD MOVE  //  SPACE OR LMB FIRE  //  SHIFT DASH  //  ESC BACK", { 223, 510 }, 9, 1.0f, COLOR_MUTED);
        m_btn_back.draw(title_font);
        m_btn_launch.draw(title_font);
        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MISSION_BRIEFING; }

private:
    const char* difficulty_name() const {
        switch (m_difficulty) {
            case Difficulty::NOVICE: return "NOVICE";
            case Difficulty::ASURA_SLAYER: return "ASURA SLAYER";
            case Difficulty::CHAKRAVYUHA: return "CHAKRAVYUHA";
            default: return "KSHATRIYA";
        }
    }

    static void draw_wrapped(Font font, const std::string& text, Vector2 position,
                             float max_width, float font_size, Color color) {
        std::istringstream words(text);
        std::string word;
        std::string line;
        float y = position.y;
        while (words >> word) {
            const std::string candidate = line.empty() ? word : line + " " + word;
            if (!line.empty() && MeasureTextEx(font, candidate.c_str(), font_size, 1.0f).x > max_width) {
                DrawTextEx(font, line.c_str(), { position.x, y }, font_size, 1.0f, color);
                y += font_size + 5.0f;
                line = word;
            } else {
                line = candidate;
            }
        }
        if (!line.empty()) DrawTextEx(font, line.c_str(), { position.x, y }, font_size, 1.0f, color);
    }

    ViewType m_next_view;
    const ShipArchetype* m_ship;
    int m_wave = 1;
    Difficulty m_difficulty = Difficulty::KSHATRIYA;
    UI::Button m_btn_launch;
    UI::Button m_btn_back;
};

} // namespace Vimana
