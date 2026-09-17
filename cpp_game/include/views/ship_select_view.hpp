#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "entities/ship_archetypes.hpp"

namespace Vimana {

class ShipSelectView : public IView {
public:
    ShipSelectView() : m_selected_idx(0), m_next_view(ViewType::SHIP_SELECT) {
        init();
    }

    void init() override {
        m_next_view = ViewType::SHIP_SELECT;
        m_selected_idx = 0;

        m_btn_prev = UI::Button({ 80, 240, 48, 48 }, "<", COLOR_GOLD);
        m_btn_next = UI::Button({ 370, 240, 48, 48 }, ">", COLOR_GOLD);
        m_btn_launch = UI::Button({ 520, 500, 320, 44 }, "LAUNCH MISSION", COLOR_GOLD_BRIGHT);
        m_btn_back = UI::Button({ 35, 520, 110, 36 }, "BACK", COLOR_MUTED);
        m_btn_unlock = UI::Button({ 520, 440, 320, 40 }, "UNLOCK WITH PRANA", COLOR_CYAN_BRIGHT);

        // Consumable store buttons
        m_btn_buy_kavach = UI::Button({ 520, 230, 95, 32 }, "KAVACH (120)", COLOR_CYAN);
        m_btn_buy_soma = UI::Button({ 630, 230, 95, 32 }, "SOMA (100)", COLOR_GREEN_BRIGHT);
        m_btn_buy_vajra = UI::Button({ 740, 230, 95, 32 }, "VAJRA (80)", COLOR_ORANGE_BRIGHT);
    }

    void update(float dt, Vector2 mouse_pos) override {
        int max_wave = DBSystem::instance().max_wave();
        const auto& current_ship = SHIP_FLEET[m_selected_idx];
        bool is_unlocked = CurrencySystem::instance().is_ship_unlocked(current_ship.id, max_wave);

        if (m_btn_prev.update(mouse_pos)) {
            m_selected_idx = (m_selected_idx - 1 + SHIP_FLEET.size()) % SHIP_FLEET.size();
        }
        if (m_btn_next.update(mouse_pos)) {
            m_selected_idx = (m_selected_idx + 1) % SHIP_FLEET.size();
        }

        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = m_return_view;
        }

        if (!is_unlocked) {
            std::string unlock_txt = "UNLOCK FOR " + std::to_string(current_ship.prana_cost) + " PRANA";
            m_btn_unlock.set_label(unlock_txt);
            if (m_btn_unlock.update(mouse_pos)) {
                CurrencySystem::instance().try_unlock_ship_with_prana(current_ship.id, max_wave);
            }
        } else {
            if (m_btn_launch.update(mouse_pos) || IsKeyPressed(KEY_ENTER)) {
                m_next_view = (m_return_view == ViewType::LOADOUT) ? ViewType::LOADOUT : ViewType::GAMEPLAY;
            }
        }

        // Armory purchases
        if (m_btn_buy_kavach.update(mouse_pos)) {
            CurrencySystem::instance().buy_consumable(m_temp_inv, "kavach");
        }
        if (m_btn_buy_soma.update(mouse_pos)) {
            CurrencySystem::instance().buy_consumable(m_temp_inv, "soma");
        }
        if (m_btn_buy_vajra.update(mouse_pos)) {
            CurrencySystem::instance().buy_consumable(m_temp_inv, "vajra");
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "VIMANA HANGAR & ARMORY", { 45, 30 }, 24, 1.0f, COLOR_GOLD_BRIGHT);

        std::string prana_str = "PRANA SHARDS: " + std::to_string(CurrencySystem::instance().prana_shards());
        DrawTextEx(font, prana_str.c_str(), { 640, 32 }, 16, 1.0f, COLOR_GOLD_BRIGHT);

        const auto& ship = SHIP_FLEET[m_selected_idx];
        int max_wave = DBSystem::instance().max_wave();
        bool is_unlocked = CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave);

        // ── Left: Ship Inspection Display ───────────────────────────────────
        UI::DrawChamferedPanel({ 40, 90, 420, 400 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        // Ship Sprite Center
        Texture2D tex = AssetManager::instance().get_texture(ship.sprite_file);
        if (tex.id > 0) {
            float s = 1.3f;
            Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { 250, 240, tex.width * s, tex.height * s };
            Vector2 origin = { dest.width / 2.0f, dest.height / 2.0f };
            DrawTexturePro(tex, src, dest, origin, 0.0f, is_unlocked ? WHITE : Color{ 80, 80, 80, 200 });
        } else {
            DrawCircle(250, 240, 50, is_unlocked ? ship.accent_color : Color{ 60, 60, 60, 255 });
        }

        m_btn_prev.draw(font);
        m_btn_next.draw(font);

        // Ship Title
        std::string ship_num = std::to_string(m_selected_idx + 1) + " / " + std::to_string(SHIP_FLEET.size());
        DrawText(ship_num.c_str(), 235, 110, 14, COLOR_MUTED);
        DrawTextEx(font, ship.name.c_str(), { 70, 130 }, 24, 1.0f, ship.accent_color);
        DrawText(ship.subtitle.c_str(), 70, 160, 12, COLOR_CYAN_BRIGHT);
        DrawText(("ROLE: " + ship.role).c_str(), 70, 180, 12, COLOR_PARCHMENT);

        // Lock Banner
        if (!is_unlocked) {
            UI::DrawChamferedPanel({ 110, 330, 280, 50 }, COLOR_RED_BRIGHT, { 35, 10, 10, 230 }, 4.0f);
            DrawText("LOCKED SHIP", 200, 338, 14, COLOR_RED_BRIGHT);
            std::string req = "UNLOCKED AT WAVE " + std::to_string(ship.unlock_wave);
            DrawText(req.c_str(), 165, 358, 11, COLOR_PARCHMENT);
        }

        // ── Right: Detailed Stats & Armory ──────────────────────────────────
        UI::DrawChamferedPanel({ 490, 90, 380, 480 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "SHIP SPECIFICATIONS", { 520, 105 }, 18, 1.0f, COLOR_GOLD);

        // Stat bars
        auto draw_stat = [&](int y, const char* label, float value, float max_val, Color col) {
            DrawText(label, 520, y, 12, COLOR_PARCHMENT);
            DrawRectangle(640, y + 2, 200, 12, { 25, 30, 45, 255 });
            DrawRectangle(640, y + 2, static_cast<int>(200 * (value / max_val)), 12, col);
            DrawRectangleLines(640, y + 2, 200, 12, COLOR_MUTED);
        };

        draw_stat(135, "HULL INTEGRITY", static_cast<float>(ship.max_hp), 300.0f, COLOR_GREEN_BRIGHT);
        draw_stat(155, "VELOCITY", ship.speed, 420.0f, COLOR_CYAN_BRIGHT);
        draw_stat(175, "CANON DAMAGE", static_cast<float>(ship.bullet_damage), 60.0f, COLOR_RED_BRIGHT);
        draw_stat(195, "DASH CHARGES", static_cast<float>(ship.dash_charges), 3.0f, COLOR_GOLD_BRIGHT);

        // Consumable Armory section
        DrawLine(510, 220, 850, 220, COLOR_MUTED);
        DrawText("PRE-RUN CONSUMABLES (PRANA SHOP)", 520, 212, 10, COLOR_GOLD);
        m_btn_buy_kavach.draw(font);
        m_btn_buy_soma.draw(font);
        m_btn_buy_vajra.draw(font);

        // Action Buttons
        if (!is_unlocked) {
            m_btn_unlock.draw(font);
        } else {
            m_btn_launch.draw(font);
        }
        m_btn_back.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::SHIP_SELECT; }
    void set_return_view(ViewType v) { m_return_view = v; }
    const ShipArchetype& selected_ship() const { return SHIP_FLEET[m_selected_idx]; }
    const ConsumableInventory& consumables() const { return m_temp_inv; }

private:
    size_t m_selected_idx;
    ViewType m_next_view;
    ViewType m_return_view = ViewType::MENU;
    UI::Button m_btn_prev;
    UI::Button m_btn_next;
    UI::Button m_btn_launch;
    UI::Button m_btn_back;
    UI::Button m_btn_unlock;
    UI::Button m_btn_buy_kavach;
    UI::Button m_btn_buy_soma;
    UI::Button m_btn_buy_vajra;
    ConsumableInventory m_temp_inv;
};

} // namespace Vimana
