#pragma once
#include <algorithm>
#include <iterator>
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "ui/design_tokens.hpp"
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
        m_show_all = false;
        m_temp_inv = DBSystem::instance().armory_inventory();
        const auto equipped = std::find_if(SHIP_FLEET.begin(), SHIP_FLEET.end(), [](const ShipArchetype& ship) {
            return ship.id == DBSystem::instance().equipped_ship();
        });
        if (equipped != SHIP_FLEET.end() &&
            CurrencySystem::instance().is_ship_unlocked(equipped->id, DBSystem::instance().max_wave())) {
            m_selected_idx = static_cast<size_t>(std::distance(SHIP_FLEET.begin(), equipped));
            m_show_all = m_selected_idx >= 3;
        }

        m_btn_prev = UI::Button({ 80, 240, 48, 48 }, "<", COLOR_GOLD, "[A]", UI::ButtonKind::SECONDARY);
        m_btn_next = UI::Button({ 370, 240, 48, 48 }, ">", COLOR_GOLD, "[D]", UI::ButtonKind::SECONDARY);
        const std::string launch_label = m_return_view == ViewType::MENU ? "EQUIP VESSEL" : "SELECT VESSEL";
        m_btn_launch = UI::Button({ 520, 500, 320, 44 }, launch_label, COLOR_GOLD_BRIGHT, "[ENTER]", UI::ButtonKind::PRIMARY);
        m_btn_back = UI::Button({ 35, 520, 110, 36 }, "BACK", COLOR_MUTED, "[ESC]", UI::ButtonKind::GHOST);
        m_btn_unlock = UI::Button({ 520, 440, 320, 40 }, "UNLOCK WITH PRANA", COLOR_CYAN_BRIGHT, "", UI::ButtonKind::SECONDARY);
        m_btn_upgrade = UI::Button({ 520, 276, 320, 34 }, "UPGRADE SHIP FRAME", COLOR_GOLD_BRIGHT, "", UI::ButtonKind::PRIMARY);
        m_btn_toggle_fleet = UI::Button({ 35, 478, 200, 32 }, "VIEW FULL FLEET [TAB]", COLOR_MUTED, "", UI::ButtonKind::GHOST);

        // Consumable store buttons
        m_btn_buy_kavach = UI::Button({ 520, 362, 95, 32 }, "KAVACH", COLOR_CYAN, "", UI::ButtonKind::SECONDARY);
        m_btn_buy_soma = UI::Button({ 630, 362, 95, 32 }, "SOMA", COLOR_GREEN_BRIGHT, "", UI::ButtonKind::SECONDARY);
        m_btn_buy_vajra = UI::Button({ 740, 362, 95, 32 }, "VAJRA", COLOR_ORANGE_BRIGHT, "", UI::ButtonKind::SECONDARY);
        m_btn_buy_kavach.set_label("KAVACH (" + std::to_string(COST_KAVACH_SHIELD) + ")");
        m_btn_buy_soma.set_label("SOMA (" + std::to_string(COST_SOMA_VIAL) + ")");
        m_btn_buy_vajra.set_label("VAJRA (" + std::to_string(COST_VAJRA_FLARE) + ")");
    }

    void update(float dt, Vector2 mouse_pos) override {
        int max_wave = DBSystem::instance().max_wave();
        // Starter-only by default (Pushpaka/Tripura/Garuda). Full fleet behind TAB toggle.
        size_t fleet_size = m_show_all ? SHIP_FLEET.size() : 3;
        if (m_selected_idx >= fleet_size) m_selected_idx = 0;
        const auto& current_ship = m_show_all ? SHIP_FLEET[m_selected_idx] : SHIP_FLEET[m_selected_idx % 3];
        bool is_unlocked = CurrencySystem::instance().is_ship_unlocked(current_ship.id, max_wave);

        if (m_btn_toggle_fleet.update(mouse_pos) || IsKeyPressed(KEY_TAB)) {
            m_show_all = !m_show_all;
            m_selected_idx = 0;
            SoundSystem::instance().play_sfx("ui_click.wav");
        }
        if (m_btn_prev.update(mouse_pos) || IsKeyPressed(KEY_LEFT) || IsKeyPressed(KEY_A)) {
            m_selected_idx = (m_selected_idx - 1 + fleet_size) % fleet_size;
            SoundSystem::instance().play_sfx("ui_click.wav");
        }
        if (m_btn_next.update(mouse_pos) || IsKeyPressed(KEY_RIGHT) || IsKeyPressed(KEY_D)) {
            m_selected_idx = (m_selected_idx + 1) % fleet_size;
            SoundSystem::instance().play_sfx("ui_click.wav");
        }

        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = m_return_view;
        }

        if (is_unlocked && m_btn_upgrade.update(mouse_pos)) {
            const bool upgraded = CurrencySystem::instance().upgrade_ship(current_ship.id, max_wave);
            if (upgraded) {
                DBSystem::instance().save_game();
                SoundSystem::instance().play_sfx("powerup.wav");
            } else {
                SoundSystem::instance().play_ui_click();
            }
        }

        if (!is_unlocked) {
            if (current_ship.boss_unlock_id.empty()) {
                std::string unlock_txt = "UNLOCK FOR " + std::to_string(current_ship.prana_cost) + " PRANA";
                m_btn_unlock.set_label(unlock_txt);
                if (m_btn_unlock.update(mouse_pos)) {
                    if (CurrencySystem::instance().try_unlock_ship_with_prana(current_ship.id, max_wave)) {
                        DBSystem::instance().save_game();
                        SoundSystem::instance().play_sfx("powerup.wav");
                    } else {
                        SoundSystem::instance().play_ui_click();
                    }
                }
            }
        } else {
            if (is_unlocked && (m_btn_launch.update(mouse_pos) || IsKeyPressed(KEY_ENTER))) {
                DBSystem::instance().set_equipped_ship(current_ship.id);
                DBSystem::instance().save_game();
                m_next_view = m_return_view;
            }
        }

        // Armory purchases
        if (m_btn_buy_kavach.update(mouse_pos)) {
            if (CurrencySystem::instance().buy_consumable(m_temp_inv, "kavach")) {
                DBSystem::instance().set_armory_inventory(m_temp_inv);
                DBSystem::instance().save_game();
            }
        }
        if (m_btn_buy_soma.update(mouse_pos)) {
            if (CurrencySystem::instance().buy_consumable(m_temp_inv, "soma")) {
                DBSystem::instance().set_armory_inventory(m_temp_inv);
                DBSystem::instance().save_game();
            }
        }
        if (m_btn_buy_vajra.update(mouse_pos)) {
            if (CurrencySystem::instance().buy_consumable(m_temp_inv, "vajra")) {
                DBSystem::instance().set_armory_inventory(m_temp_inv);
                DBSystem::instance().save_game();
            }
        }
    }

    void draw() override {
        using namespace Vimana::UI;
        ClearBackground(PAL_BG_VOID);
        Font title_f = AssetManager::instance().title_font();
        Font body_f = AssetManager::instance().body_font();

        // Header
        Rectangle header = { 30, 20, 840, 50 };
        DrawElevationPanel(header, ElevationGlass(), true);
        DrawCornerBrackets(header, 10.0f, PAL_PRIMARY);
        DrawTextEx(title_f, "VIMANA HANGAR & ARMORY // COMMISSION SHIPS", { 45, 30 }, 20, 1.0f, PAL_PRIMARY_BRIGHT);

        std::string prana_str = "PRANA SHARDS: " + std::to_string(CurrencySystem::instance().prana_shards());
        DrawTextEx(title_f, prana_str.c_str(), { 640, 32 }, 15, 1.0f, PAL_PRIMARY_BRIGHT);

        size_t draw_fleet = m_show_all ? SHIP_FLEET.size() : 3;
        size_t draw_idx = m_selected_idx % draw_fleet;
        const auto& ship = m_show_all ? SHIP_FLEET[draw_idx] : SHIP_FLEET[draw_idx % 3];
        int max_wave = DBSystem::instance().max_wave();
        bool is_unlocked = CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave);

        // ── Left: Ship Inspection Display ───────────────────────────────────
        Rectangle inspect = { 40, 90, 420, 410 };
        Color ship_accent = is_unlocked ? ship.accent_color : PAL_TEXT_MUTED;
        ElevationStyle inspect_elev = { PAL_SURFACE_GLASS, ship_accent, Chamfer::LARGE };
        DrawElevationPanel(inspect, inspect_elev, true);
        DrawCornerBrackets(inspect, 12.0f, ship_accent);

        // Mandala reticle behind ship (replaces simple concentric rings)
        Color reticle_p = ship_accent;
        Color reticle_s = PAL_PRIMARY;
        if (!is_unlocked) { reticle_p.a = 100; reticle_s.a = 80; }
        DrawMandalaReticle({ 250, 255 }, 78.0f, GetTime(), reticle_p, reticle_s, is_unlocked ? 0.85f : 0.45f);

        // Ship Sprite Center
        Texture2D tex = AssetManager::instance().get_texture(ship.sprite_file);
        if (tex.id > 0) {
            float s = 1.35f;
            Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { 250, 255, tex.width * s, tex.height * s };
            Vector2 origin = { dest.width / 2.0f, dest.height / 2.0f };
            DrawTexturePro(tex, src, dest, origin, 0.0f, is_unlocked ? WHITE : Color{ 70, 70, 80, 200 });
        } else {
            DrawCircle(250, 255, 50, is_unlocked ? ship.accent_color : Color{ 60, 60, 60, 255 });
        }

        m_btn_prev.draw(title_f);
        m_btn_next.draw(title_f);

        // Ship Title & Subtitle
        std::string ship_num = m_show_all
            ? "[" + std::to_string(draw_idx + 1) + " / " + std::to_string(SHIP_FLEET.size()) + "] " + (is_unlocked ? "READY" : "LOCKED")
            : "[STARTER " + std::to_string(draw_idx + 1) + " / 3] " + (is_unlocked ? "READY" : "LOCKED") + "  ·  TAB FOR FULL FLEET";
        DrawTextEx(body_f, ship_num.c_str(), { 65, 108 }, 12, 1.0f, is_unlocked ? PAL_HEALTH_HIGH : PAL_DESTRUCTIVE_BRIGHT);
        DrawTextEx(title_f, ship.name.c_str(), { 65, 125 }, 22, 1.0f, is_unlocked ? ship.accent_color : PAL_TEXT_MUTED);
        DrawTextEx(body_f, ship.subtitle.c_str(), { 65, 155 }, 12, 1.0f, PAL_SECONDARY_BRIGHT);
        DrawTextEx(body_f, ("ROLE: " + ship.role).c_str(), { 65, 172 }, 11, 1.0f, PAL_TEXT_BODY);
        const int mastery_sorties = CurrencySystem::instance().ship_sorties(ship.id);
        const bool ship_mastered = CurrencySystem::instance().is_ship_mastered(ship.id);
        const std::string mastery_label = ship_mastered
            ? "MASTERY COMPLETE // GOLDEN SKIN ACTIVE"
            : "SHIP MASTERY // " + std::to_string(mastery_sorties) + "/" +
              std::to_string(CurrencySystem::SHIP_MASTERY_SORTIES) + " SORTIES";
        DrawTextEx(body_f, mastery_label.c_str(), { 65, 190 }, 10, 1.0f,
                   ship_mastered ? COLOR_GOLD_BRIGHT : COLOR_CYAN_BRIGHT);

        // Lock Banner Overlay if locked
        if (!is_unlocked) {
            Rectangle lock_box = { 80, 365, 340, 52 };
            DrawElevationPanel(lock_box, ElevationFocus());
            DrawCornerBrackets(lock_box, 8.0f, PAL_DESTRUCTIVE);
            UI::DrawLockIcon({ 110, 391 }, 10.0f, PAL_DESTRUCTIVE_BRIGHT);
            DrawTextEx(title_f, "RESTRICTED VESSEL // CLEARANCE REQUIRED", { 135, 375 }, 11, 1.0f, PAL_DESTRUCTIVE_BRIGHT);
            std::string req = ship.boss_unlock_id.empty()
                ? "UNLOCKED AT CAMPAIGN WAVE " + std::to_string(ship.unlock_wave) + " OR PRANA SHARDS"
                : "DEFEAT " + ship.boss_unlock_name;
            DrawTextEx(body_f, req.c_str(), { 135, 395 }, 9, 1.0f, PAL_TEXT_BODY);
        }

        // ── Right: Detailed Stats & Armory ──────────────────────────────────
        Rectangle stats = { 490, 90, 380, 480 };
        DrawElevationPanel(stats, ElevationGlass(), true);
        DrawCornerBrackets(stats, 12.0f, PAL_PRIMARY);
        DrawTextEx(title_f, "VESSEL SPECIFICATIONS & ARMORY", { 515, 105 }, 16, 1.0f, PAL_PRIMARY_BRIGHT);

        // Stat bars — now use segmented gauges for chromatic state
        auto draw_stat = [&](int y, const char* label, float value, float max_val, Color col) {
            DrawTextEx(body_f, label, { 515, static_cast<float>(y) }, 11, 1.0f, PAL_TEXT_BODY);
            Rectangle gauge_rect = { 640, static_cast<float>(y + 2), 200, 12 };
            // Color-code based on ratio: green > 60%, amber 30-60%, crimson < 30%
            float pct = std::clamp(value / max_val, 0.0f, 1.0f);
            Color cell_col;
            if (pct > 0.6f)      cell_col = PAL_HEALTH_HIGH;
            else if (pct > 0.3f) cell_col = PAL_HEALTH_MID;
            else                 cell_col = PAL_HEALTH_LOW;
            // 10-segment gauge tinted with ship accent
            DrawSegmentedHealthGauge(gauge_rect, value, max_val, 10, 0.0f);
            (void)col;
            (void)cell_col;
        };

        const float upgrade_level = static_cast<float>(CurrencySystem::instance().ship_upgrade_level(ship.id));
        draw_stat(135, "HULL INTEGRITY", ship.max_hp * (1.0f + 0.05f * upgrade_level), 600.0f, COLOR_GREEN_BRIGHT);
        draw_stat(155, "VELOCITY", ship.speed * (1.0f + 0.015f * upgrade_level), 500.0f, COLOR_CYAN_BRIGHT);
        draw_stat(175, "CANNON DAMAGE", ship.bullet_damage * (1.0f + 0.03f * upgrade_level), 100.0f, COLOR_RED_BRIGHT);
        draw_stat(195, "DASH CHARGES", static_cast<float>(ship.dash_charges), 4.0f, COLOR_GOLD_BRIGHT);

        const int frame_level = CurrencySystem::instance().ship_upgrade_level(ship.id);
        DrawLine(510, 218, 850, 218, COLOR_MUTED);
        DrawTextEx(title_f, "PERMANENT FRAME REFORGE", { 515, 226 }, 11, 1.0f, COLOR_GOLD_BRIGHT);
        std::string level_label = "FRAME LEVEL " + std::to_string(frame_level) + " / " + std::to_string(CurrencySystem::MAX_SHIP_UPGRADE_LEVEL);
        DrawTextEx(body_f, level_label.c_str(), { 515, 244 }, 12, 1.0f, COLOR_CYAN_BRIGHT);
        DrawTextEx(body_f, "+5% hull · +3% weapon · +1.5% speed per level", { 515, 262 }, 9, 1.0f, COLOR_PARCHMENT);
        if (is_unlocked && frame_level < CurrencySystem::MAX_SHIP_UPGRADE_LEVEL) {
            const int cost = CurrencySystem::instance().next_ship_upgrade_cost(ship.id);
            m_btn_upgrade.set_label("REFORGE FRAME // " + std::to_string(cost) + " PRANA");
            m_btn_upgrade.draw(title_f);
        } else if (is_unlocked) {
            DrawTextEx(body_f, "MAXIMUM FRAME RANK REACHED", { 575, 341 }, 11, 1.0f, PAL_HEALTH_HIGH);
        } else {
            DrawTextEx(body_f, "UNLOCK THIS VIMANA TO REFORGE ITS FRAME", { 535, 341 }, 10, 1.0f, PAL_TEXT_MUTED);
        }

        // Consumable Armory section
        DrawLine(510, 318, 850, 318, PAL_OUTLINE_VARIANT);
        DrawTextEx(title_f, "TACTICAL CONSUMABLES (PRANA ARMORY)", { 515, 326 }, 10, 1.0f, PAL_PRIMARY);

        // Consumables inventory counts
        std::string inv_str = "OWNED: [KAVACH: " + std::to_string(m_temp_inv.kavach_charges) +
                              "]  [SOMA: " + std::to_string(m_temp_inv.soma_vials) +
                              "]  [VAJRA: " + std::to_string(m_temp_inv.vajra_flares) + "]";
        DrawTextEx(body_f, inv_str.c_str(), { 515, 344 }, 11, 1.0f, PAL_SECONDARY_BRIGHT);

        m_btn_buy_kavach.draw(title_f);
        m_btn_buy_soma.draw(title_f);
        m_btn_buy_vajra.draw(title_f);

        // Action Buttons
        if (!is_unlocked) {
            if (ship.boss_unlock_id.empty()) {
                m_btn_unlock.draw(title_f);
            } else {
                DrawTextEx(body_f, "BOSS SALVAGE // CLEAR THIS ACT'S BOSS", { 530, 452 }, 11, 1.0f, PAL_HEALTH_MID);
            }
        } else {
            m_btn_launch.draw(title_f);
        }
        m_btn_back.draw(title_f);
        m_btn_toggle_fleet.draw(title_f);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::SHIP_SELECT; }
    void set_return_view(ViewType v) { m_return_view = v; }
    const ShipArchetype& selected_ship() const {
        if (m_show_all) return SHIP_FLEET[m_selected_idx % SHIP_FLEET.size()];
        return SHIP_FLEET[m_selected_idx % 3];
    }
    const ConsumableInventory& consumables() const { return m_temp_inv; }

private:
    size_t m_selected_idx;
    bool m_show_all = false;
    ViewType m_next_view;
    ViewType m_return_view = ViewType::MENU;
    UI::Button m_btn_prev;
    UI::Button m_btn_next;
    UI::Button m_btn_launch;
    UI::Button m_btn_back;
    UI::Button m_btn_unlock;
    UI::Button m_btn_upgrade;
    UI::Button m_btn_toggle_fleet;
    UI::Button m_btn_buy_kavach;
    UI::Button m_btn_buy_soma;
    UI::Button m_btn_buy_vajra;
    ConsumableInventory m_temp_inv;
};

} // namespace Vimana
