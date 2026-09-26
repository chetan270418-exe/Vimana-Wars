#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "entities/player.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class LoadoutView : public IView {
public:
    LoadoutView() 
        : m_next_view(ViewType::LOADOUT), 
          m_selected_ship(&SHIP_FLEET[0]), 
          m_starting_wave(1),
          m_btn_launch({ SCREEN_WIDTH - 290, SCREEN_HEIGHT - 75, 260, 44 }, "ENGAGE MISSION >>", COLOR_GOLD_BRIGHT),
          m_btn_change_ship({ 50, 420, 200, 36 }, "CHANGE VIMANA", COLOR_CYAN_BRIGHT),
          m_btn_back({ 50, SCREEN_HEIGHT - 75, 170, 44 }, "<< CAMPAIGN MAP", COLOR_MUTED),
          m_btn_buy_kavach({ 680, 195, 120, 30 }, "BUY", COLOR_GOLD),
          m_btn_buy_soma({ 680, 260, 120, 30 }, "BUY", COLOR_GREEN_BRIGHT),
          m_btn_buy_vajra({ 680, 325, 120, 30 }, "BUY", COLOR_CYAN_BRIGHT)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::LOADOUT;
        m_ship_spin_angle = 0.0f;
        m_btn_buy_kavach.set_label("BUY (" + std::to_string(COST_KAVACH_SHIELD) + " P)");
        m_btn_buy_soma.set_label("BUY (" + std::to_string(COST_SOMA_VIAL) + " P)");
        m_btn_buy_vajra.set_label("BUY (" + std::to_string(COST_VAJRA_FLARE) + " P)");
    }

    void set_mission_target(int starting_wave, const ShipArchetype* ship, const ConsumableInventory& inv) {
        m_starting_wave = starting_wave;
        if (ship) m_selected_ship = ship;
        m_inventory = inv;
    }

    const ShipArchetype& selected_ship() const { return *m_selected_ship; }
    const ConsumableInventory& inventory() const { return m_inventory; }
    int starting_wave() const { return m_starting_wave; }

    void update(float dt, Vector2 mouse_pos) override {
        m_ship_spin_angle += dt * 45.0f;

        // Buy Consumables - single source of truth: COST_* in core/constants.hpp
        if (m_btn_buy_kavach.update(mouse_pos)) {
            if (CurrencySystem::instance().buy_consumable(m_inventory, "kavach")) {
                DBSystem::instance().set_armory_inventory(m_inventory);
                DBSystem::instance().save_game();
                SoundSystem::instance().play_ui_confirm();
            }
        }
        if (m_btn_buy_soma.update(mouse_pos)) {
            if (CurrencySystem::instance().buy_consumable(m_inventory, "soma")) {
                DBSystem::instance().set_armory_inventory(m_inventory);
                DBSystem::instance().save_game();
                SoundSystem::instance().play_ui_confirm();
            }
        }
        if (m_btn_buy_vajra.update(mouse_pos)) {
            if (CurrencySystem::instance().buy_consumable(m_inventory, "vajra")) {
                DBSystem::instance().set_armory_inventory(m_inventory);
                DBSystem::instance().save_game();
                SoundSystem::instance().play_ui_confirm();
            }
        }

        if (m_btn_launch.update(mouse_pos) || IsKeyPressed(KEY_ENTER)) {
            m_next_view = ViewType::MISSION_BRIEFING;
        } else if (m_btn_change_ship.update(mouse_pos)) {
            m_next_view = ViewType::SHIP_SELECT;
        } else if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::CAMPAIGN_MAP;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header Title
        const char* title = "MISSION LOADOUT // TACTICAL PREPARATION";
        DrawTextEx(font, title, { 50, 30 }, 24, 1.0f, COLOR_GOLD_BRIGHT);

        std::string sub = "REALM DESTINATION: WAVE " + std::to_string(m_starting_wave) + " • VERIFY ORDNANCE & DEFENSES";
        DrawText(sub.c_str(), 52, 60, 12, COLOR_CYAN_BRIGHT);

        // Wallet Display
        std::string wallet = "PRANA SHARDS: " + std::to_string(CurrencySystem::instance().prana_shards());
        UI::DrawChamferedPanel({ SCREEN_WIDTH - 240, 25, 190, 36 }, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);
        DrawTextEx(font, wallet.c_str(), { SCREEN_WIDTH - 225, 36 }, 13, 1.0f, COLOR_GOLD_BRIGHT);

        // ── LEFT PANEL: SELECTED VIMANA & STATS ──────────────────────────────────
        Rectangle ship_box = { 50, 100, 270, 305 };
        UI::DrawChamferedPanel(ship_box, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);

        DrawTextEx(font, m_selected_ship->name.c_str(), { ship_box.x + 20, ship_box.y + 16 }, 18, 1.0f, COLOR_GOLD_BRIGHT);
        DrawText(m_selected_ship->role.c_str(), static_cast<int>(ship_box.x + 20), static_cast<int>(ship_box.y + 40), 11, COLOR_MUTED);

        // Ship Sprite with rotating celestial ring
        Texture2D s_tex = AssetManager::instance().get_texture(m_selected_ship->sprite_file);
        Vector2 s_center = { ship_box.x + 135, ship_box.y + 115 };
        DrawCircleLinesV(s_center, 44.0f, Color{ 80, 200, 255, 70 });
        DrawCircleLinesV(s_center, 52.0f, ColorAlpha(COLOR_GOLD, 0.35f));

        if (s_tex.id > 0) {
            float s_scale = 1.3f;
            Rectangle src = { 0, 0, static_cast<float>(s_tex.width), static_cast<float>(s_tex.height) };
            Rectangle dest = { s_center.x, s_center.y, s_tex.width * s_scale, s_tex.height * s_scale };
            DrawTexturePro(s_tex, src, dest, { dest.width / 2.0f, dest.height / 2.0f }, 0.0f, WHITE);
        } else {
            DrawCircleV(s_center, 28.0f, COLOR_CYAN_BRIGHT);
        }

        // Stat Bars
        float bar_x = ship_box.x + 20;
        float bar_y = ship_box.y + 185;
        float bar_w = 230;

        auto draw_stat = [&](const char* label, float val, float max_val, Color col) {
            DrawText(label, static_cast<int>(bar_x), static_cast<int>(bar_y), 10, COLOR_PARCHMENT);
            DrawRectangle(static_cast<int>(bar_x + 90), static_cast<int>(bar_y + 2), static_cast<int>(bar_w - 90), 8, COLOR_SURFACE_HIGH);
            float fill_w = (val / max_val) * (bar_w - 90);
            DrawRectangle(static_cast<int>(bar_x + 90), static_cast<int>(bar_y + 2), static_cast<int>(fill_w), 8, col);
            bar_y += 20;
        };

        draw_stat("HULL ARMOR", static_cast<float>(m_selected_ship->max_hp), 600.0f, COLOR_GREEN_BRIGHT);
        draw_stat("SUB-LIGHT SPD", m_selected_ship->speed, 500.0f, COLOR_CYAN_BRIGHT);
        draw_stat("FIRING RATE", 1.0f / m_selected_ship->shoot_cooldown, 15.0f, COLOR_GOLD_BRIGHT);
        draw_stat("DASH CHARGES", static_cast<float>(m_selected_ship->dash_charges), 4.0f, COLOR_PURPLE_BRIGHT);

        m_btn_change_ship.draw(font);

        // ── RIGHT PANEL: CONSUMABLES & PREPARATION DEPOT ─────────────────────────
        Rectangle depot_box = { 350, 100, 500, 350 };
        UI::DrawYantraPanel(depot_box, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f, true);

        DrawTextEx(font, "TACTICAL CONSUMABLES DEPOT", { depot_box.x + 20, depot_box.y + 18 }, 16, 1.0f, COLOR_GOLD_BRIGHT);
        DrawText("EQUIP EXPENDABLE DEFENSES FOR THIS EXPEDITION", static_cast<int>(depot_box.x + 20), static_cast<int>(depot_box.y + 42), 11, COLOR_MUTED);

        // 1. Kavach Shield
        Rectangle k_rec = { depot_box.x + 20, depot_box.y + 75, depot_box.width - 40, 58 };
        UI::DrawChamferedPanel(k_rec, COLOR_GOLD, COLOR_SURFACE_MID, 4.0f);
        Texture2D ic_k = AssetManager::instance().get_texture("icon_kavach.png");
        if (ic_k.id > 0) DrawTexturePro(ic_k, { 0, 0, 64, 64 }, { k_rec.x + 10, k_rec.y + 9, 40, 40 }, { 0, 0 }, 0.0f, WHITE);
        DrawText("KAVACH DEATH-DEFIANCE BARRIER", static_cast<int>(k_rec.x + 58), static_cast<int>(k_rec.y + 12), 12, COLOR_GOLD_BRIGHT);
        DrawText("Auto-triggers upon lethal damage. Absorbs fatal hit & grants 3s shield.", static_cast<int>(k_rec.x + 58), static_cast<int>(k_rec.y + 32), 10, COLOR_PARCHMENT);
        std::string k_cnt = "CARRIED: " + std::to_string(m_inventory.kavach_charges) + " / 3";
        DrawText(k_cnt.c_str(), static_cast<int>(k_rec.x + 280), static_cast<int>(k_rec.y + 12), 11, COLOR_CYAN_BRIGHT);
        m_btn_buy_kavach.draw(font);

        // 2. Soma Vial
        Rectangle s_rec = { depot_box.x + 20, depot_box.y + 140, depot_box.width - 40, 58 };
        UI::DrawChamferedPanel(s_rec, COLOR_GREEN_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        Texture2D ic_s = AssetManager::instance().get_texture("icon_soma.png");
        if (ic_s.id > 0) DrawTexturePro(ic_s, { 0, 0, 64, 64 }, { s_rec.x + 10, s_rec.y + 9, 40, 40 }, { 0, 0 }, 0.0f, WHITE);
        DrawText("SOMA RESTORATIVE AMPOULE", static_cast<int>(s_rec.x + 58), static_cast<int>(s_rec.y + 12), 12, COLOR_GREEN_BRIGHT);
        DrawText("Instantly recovers +40 Hull HP in combat. Activated via [C] key.", static_cast<int>(s_rec.x + 58), static_cast<int>(s_rec.y + 32), 10, COLOR_PARCHMENT);
        std::string s_cnt = "CARRIED: " + std::to_string(m_inventory.soma_vials) + " / 5";
        DrawText(s_cnt.c_str(), static_cast<int>(s_rec.x + 280), static_cast<int>(s_rec.y + 12), 11, COLOR_CYAN_BRIGHT);
        m_btn_buy_soma.draw(font);

        // 3. Vajra EMP Flare
        Rectangle v_rec = { depot_box.x + 20, depot_box.y + 205, depot_box.width - 40, 58 };
        UI::DrawChamferedPanel(v_rec, COLOR_CYAN_BRIGHT, COLOR_SURFACE_MID, 4.0f);
        Texture2D ic_v = AssetManager::instance().get_texture("icon_vajra_flare.png");
        if (ic_v.id > 0) DrawTexturePro(ic_v, { 0, 0, 64, 64 }, { v_rec.x + 10, v_rec.y + 9, 40, 40 }, { 0, 0 }, 0.0f, WHITE);
        DrawText("VAJRA CELESTIAL FLARE", static_cast<int>(v_rec.x + 58), static_cast<int>(v_rec.y + 12), 12, COLOR_CYAN_BRIGHT);
        DrawText("Discharges electrical pulse neutralizing all hostile bullets. Key [V].", static_cast<int>(v_rec.x + 58), static_cast<int>(v_rec.y + 32), 10, COLOR_PARCHMENT);
        std::string v_cnt = "CARRIED: " + std::to_string(m_inventory.vajra_flares) + " / 5";
        DrawText(v_cnt.c_str(), static_cast<int>(v_rec.x + 280), static_cast<int>(v_rec.y + 12), 11, COLOR_CYAN_BRIGHT);
        m_btn_buy_vajra.draw(font);

        // Mission Controls Quick Ref
        Rectangle ctrl_rec = { depot_box.x + 20, depot_box.y + 278, depot_box.width - 40, 55 };
        UI::DrawChamferedPanel(ctrl_rec, COLOR_MUTED, COLOR_SURFACE_LOW, 4.0f);
        DrawText("PILOT CONTROLS BRIEFING:", static_cast<int>(ctrl_rec.x + 12), static_cast<int>(ctrl_rec.y + 8), 10, COLOR_MUTED);
        DrawText("[WASD] Move  -  [LMB/Space] Fire  -  [Shift/RMB] Dash", static_cast<int>(ctrl_rec.x + 12), static_cast<int>(ctrl_rec.y + 24), 11, COLOR_GOLD_BRIGHT);
        DrawText("[F] Bomb  -  [Q] Chakram  -  [C] Soma  -  [V] Flare  -  [E] Revive", static_cast<int>(ctrl_rec.x + 12), static_cast<int>(ctrl_rec.y + 39), 11, COLOR_CYAN_BRIGHT);

        // Bottom Action Buttons
        m_btn_launch.draw(font);
        m_btn_back.draw(font);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::LOADOUT; }

private:
    ViewType m_next_view;
    const ShipArchetype* m_selected_ship;
    int m_starting_wave;
    ConsumableInventory m_inventory;
    float m_ship_spin_angle = 0.0f;

    UI::Button m_btn_launch;
    UI::Button m_btn_change_ship;
    UI::Button m_btn_back;
    UI::Button m_btn_buy_kavach;
    UI::Button m_btn_buy_soma;
    UI::Button m_btn_buy_vajra;
};

} // namespace Vimana
