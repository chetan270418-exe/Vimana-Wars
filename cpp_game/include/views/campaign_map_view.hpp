#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "systems/db_system.hpp"
#include "systems/currency_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class CampaignMapView : public IView {
public:
    CampaignMapView() : m_next_view(ViewType::CAMPAIGN_MAP), m_selected_node(0), m_starting_wave(1) {
        init();
    }

    void init() override {
        m_next_view = ViewType::CAMPAIGN_MAP;
        m_max_unlocked_wave = DBSystem::instance().max_wave();
        if (m_max_unlocked_wave < 1) m_max_unlocked_wave = 1;

        // Auto-select latest available realm
        m_selected_node = 0;
        for (size_t i = 0; i < CAMPAIGN_REALMS.size(); ++i) {
            if (m_max_unlocked_wave >= CAMPAIGN_REALMS[i].start_wave) {
                m_selected_node = static_cast<int>(i);
            }
        }
        m_starting_wave = CAMPAIGN_REALMS[m_selected_node].start_wave;

        m_btn_loadout = UI::Button({ SCREEN_WIDTH - 280, SCREEN_HEIGHT - 75, 250, 42 }, "CONFIGURE LOADOUT >>", COLOR_GOLD_BRIGHT);
        m_btn_back = UI::Button({ 30, SCREEN_HEIGHT - 75, 180, 42 }, "<< MAIN MENU", COLOR_MUTED);

        // Ambient astral particles
        m_particles.clear();
        for (int i = 0; i < 70; ++i) {
            m_particles.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                0.5f + (std::rand() % 15) / 10.0f
            });
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        m_pulse_time += dt * 3.0f;

        // Ambient particles drift
        for (auto& p : m_particles) {
            p.y += p.z * 15.0f * dt;
            if (p.y > SCREEN_HEIGHT) {
                p.y = 0;
                p.x = static_cast<float>(std::rand() % SCREEN_WIDTH);
            }
        }

        // Check node selection
        for (size_t i = 0; i < CAMPAIGN_REALMS.size(); ++i) {
            const auto& node = CAMPAIGN_REALMS[i];
            bool unlocked = (m_max_unlocked_wave >= node.start_wave);

            if (CheckCollisionPointCircle(mouse_pos, node.map_pos, 26.0f)) {
                if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && unlocked) {
                    m_selected_node = static_cast<int>(i);
                    m_starting_wave = node.start_wave;
                    SoundSystem::instance().play_sfx("ui_click.wav");
                }
            }
        }

        if (m_btn_loadout.update(mouse_pos) || IsKeyPressed(KEY_ENTER)) {
            m_next_view = ViewType::LOADOUT;
        } else if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Astral particles
        for (const auto& p : m_particles) {
            DrawCircle(static_cast<int>(p.x), static_cast<int>(p.y), p.z, { 180, 200, 240, 130 });
        }

        // Header
        const char* title = "MAHAYUDDHA CAMPAIGN MAP // REALM PROGRESSION";
        DrawTextEx(font, title, { 35, 25 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        std::string sub = "SELECT SECTOR DESTINATION • HIGHEST CONQUERED WAVE: " + std::to_string(m_max_unlocked_wave);
        DrawText(sub.c_str(), 36, 52, 12, COLOR_CYAN_BRIGHT);

        // Draw connecting hyperlane conduits between nodes
        for (size_t i = 0; i < CAMPAIGN_REALMS.size() - 1; ++i) {
            Vector2 p1 = CAMPAIGN_REALMS[i].map_pos;
            Vector2 p2 = CAMPAIGN_REALMS[i+1].map_pos;
            bool unlocked = (m_max_unlocked_wave >= CAMPAIGN_REALMS[i+1].start_wave);

            Color line_col = unlocked ? Color{ 80, 200, 255, 180 } : Color{ 60, 60, 80, 100 };
            DrawLineEx(p1, p2, unlocked ? 3.0f : 1.5f, line_col);

            // Energy pulse along unlocked hyperlanes
            if (unlocked) {
                float t = std::fmod(m_pulse_time + i * 0.4f, 1.0f);
                Vector2 pulse_pos = { p1.x + (p2.x - p1.x) * t, p1.y + (p2.y - p1.y) * t };
                DrawCircleV(pulse_pos, 4.0f, COLOR_CYAN_BRIGHT);
            }
        }

        // Draw Nodes
        for (size_t i = 0; i < CAMPAIGN_REALMS.size(); ++i) {
            const auto& node = CAMPAIGN_REALMS[i];
            bool unlocked = (m_max_unlocked_wave >= node.start_wave);
            bool cleared = (m_max_unlocked_wave > node.end_wave);
            bool is_selected = (m_selected_node == static_cast<int>(i));

            float radius = is_selected ? 22.0f : 17.0f;
            Color ring_color = unlocked ? node.accent_color : COLOR_MUTED;
            Color fill_color = unlocked ? (is_selected ? COLOR_SURFACE_HIGH : COLOR_SURFACE_MID) : COLOR_SURFACE_LOW;

            // Outer selection halo
            if (is_selected) {
                float pulse_r = radius + 6.0f + std::sin(m_pulse_time) * 3.0f;
                DrawCircleLinesV(node.map_pos, pulse_r, COLOR_GOLD_BRIGHT);
            }

            DrawCircleV(node.map_pos, radius, fill_color);
            DrawCircleLinesV(node.map_pos, radius, ring_color);

            // Node Index or Cleared Icon
            if (cleared) {
                DrawText("✓", static_cast<int>(node.map_pos.x - 6), static_cast<int>(node.map_pos.y - 8), 16, COLOR_GOLD_BRIGHT);
            } else if (unlocked) {
                std::string num_str = std::to_string(node.id);
                DrawText(num_str.c_str(), static_cast<int>(node.map_pos.x - 4), static_cast<int>(node.map_pos.y - 7), 14, WHITE);
            } else {
                DrawText("🔒", static_cast<int>(node.map_pos.x - 6), static_cast<int>(node.map_pos.y - 7), 12, COLOR_MUTED);
            }

            // Realm short title below node
            Vector2 label_sz = MeasureTextEx(font, node.name, 11, 1.0f);
            Color text_col = unlocked ? (is_selected ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT) : COLOR_MUTED;
            DrawTextEx(font, node.name, { node.map_pos.x - label_sz.x / 2.0f, node.map_pos.y + 24 }, 11, 1.0f, text_col);
        }

        // Selected Realm Intel Dossier (Bottom Drawer / Right Panel)
        if (m_selected_node >= 0 && m_selected_node < static_cast<int>(CAMPAIGN_REALMS.size())) {
            const auto& node = CAMPAIGN_REALMS[m_selected_node];
            Rectangle dossier_rec = { 230, SCREEN_HEIGHT - 130, SCREEN_WIDTH - 530, 105 };
            UI::DrawChamferedPanel(dossier_rec, node.accent_color, COLOR_SURFACE_MID, 6.0f);

            std::string realm_hdr = "SECTOR " + std::to_string(node.id) + ": " + node.name + " (" + node.sanskrit_title + ")";
            DrawTextEx(font, realm_hdr.c_str(), { dossier_rec.x + 16, dossier_rec.y + 12 }, 15, 1.0f, node.accent_color);

            std::string wave_rng = "WAVES: " + std::to_string(node.start_wave) + " - " + std::to_string(node.end_wave);
            DrawText(wave_rng.c_str(), static_cast<int>(dossier_rec.x + 16), static_cast<int>(dossier_rec.y + 35), 12, COLOR_CYAN_BRIGHT);

            if (std::string(node.boss_name) != "None") {
                std::string boss_warn = "⚠ TITAN ALERT: " + std::string(node.boss_name);
                DrawText(boss_warn.c_str(), static_cast<int>(dossier_rec.x + 140), static_cast<int>(dossier_rec.y + 35), 12, COLOR_RED_BRIGHT);
            }

            std::string mod_str = std::string("SECTOR HAZARD: ") + node.modifier_desc;
            DrawText(mod_str.c_str(), static_cast<int>(dossier_rec.x + 16), static_cast<int>(dossier_rec.y + 55), 11, COLOR_GOLD);

            DrawText(node.description, static_cast<int>(dossier_rec.x + 16), static_cast<int>(dossier_rec.y + 74), 10, COLOR_PARCHMENT);
        }

        // Draw Action Buttons
        m_btn_loadout.draw(font);
        m_btn_back.draw(font);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::CAMPAIGN_MAP; }
    int starting_wave() const { return m_starting_wave; }
    int selected_realm_id() const { return m_selected_node + 1; }

private:
    struct Star { float x, y, z; };
    ViewType m_next_view;
    int m_selected_node;
    int m_starting_wave;
    int m_max_unlocked_wave = 1;
    float m_pulse_time = 0.0f;
    std::vector<Star> m_particles;

    UI::Button m_btn_loadout;
    UI::Button m_btn_back;
};

} // namespace Vimana
