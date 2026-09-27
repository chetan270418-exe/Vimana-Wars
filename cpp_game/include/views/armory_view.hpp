#pragma once
// ── VIMANA WARS // ARMORY ──────────────────────────────────────────────────────
// Closes the core economy loop: every Prana Shard earned on a run is spendable
// here on new ships (FLEET tab) or consumable stock (CONSUMABLES tab).
// Purchases are atomic: validate → charge → unlock → save → feedback. Never
// leaves the wallet debited if the unlock fails (see CurrencySystem::try_*).
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "systems/sound_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "ui/design_tokens.hpp"
#include "entities/ship_archetypes.hpp"

namespace Vimana {

class ArmoryView : public IView {
public:
    enum class Tab { FLEET = 0, CONSUMABLES = 1 };
    enum class FlashKind { NONE, SUCCESS, INSUFFICIENT, ALREADY_OWNED };

    ArmoryView() : m_next_view(ViewType::ARMORY), m_active_tab(0), m_selected_idx(0) {
        init();
    }

    void init() override {
        m_next_view = ViewType::ARMORY;
        m_flash_timer = 0.0f;
        m_flash_kind = FlashKind::NONE;

        // Tabs
        m_tab_fleet     = UI::Button({ 60, 95, 130, 32 }, "FLEET", COLOR_GOLD_BRIGHT,  "", UI::ButtonKind::PRIMARY);
        m_tab_consum    = UI::Button({ 200, 95, 150, 32 }, "CONSUMABLES", COLOR_CYAN_BRIGHT, "", UI::ButtonKind::SECONDARY);

        // Fleet actions
        m_btn_buy        = UI::Button({ SCREEN_WIDTH - 290, 250, 250, 42 }, "UNLOCK SHIP", COLOR_GOLD_BRIGHT, "", UI::ButtonKind::PRIMARY);
        m_btn_prev       = UI::Button({ 50, 270, 40, 40 }, "<", COLOR_GOLD, "[A]", UI::ButtonKind::SECONDARY);
        m_btn_next       = UI::Button({ 360, 270, 40, 40 }, ">", COLOR_GOLD, "[D]", UI::ButtonKind::SECONDARY);
        m_btn_back       = UI::Button({ 40, SCREEN_HEIGHT - 56, 130, 36 }, "BACK TO MENU", COLOR_MUTED, "[ESC]", UI::ButtonKind::GHOST);

        // Consumables (3 buy buttons)
        m_btn_buy_kavach = UI::Button({ 500, 250, 200, 38 }, "KAVACH (120)",  COLOR_CYAN,         "", UI::ButtonKind::SECONDARY);
        m_btn_buy_soma   = UI::Button({ 500, 300, 200, 38 }, "SOMA (100)",    COLOR_GREEN_BRIGHT, "", UI::ButtonKind::SECONDARY);
        m_btn_buy_vajra  = UI::Button({ 500, 350, 200, 38 }, "VAJRA (80)",    COLOR_ORANGE_BRIGHT,"", UI::ButtonKind::SECONDARY);
    }

    void update(float dt, Vector2 mouse_pos) override {
        // Tab switching
        if (m_tab_fleet.update(mouse_pos))   m_active_tab = 0;
        if (m_tab_consum.update(mouse_pos))  m_active_tab = 1;
        if (IsKeyPressed(KEY_ONE))  m_active_tab = 0;
        if (IsKeyPressed(KEY_TWO))  m_active_tab = 1;
        if (IsKeyPressed(KEY_LEFT) || IsKeyPressed(KEY_A)) m_active_tab = 0;
        if (IsKeyPressed(KEY_RIGHT) || IsKeyPressed(KEY_D)) m_active_tab = 1;

        if (m_flash_timer > 0.0f) {
            m_flash_timer -= dt;
            if (m_flash_timer <= 0.0f) m_flash_kind = FlashKind::NONE;
        }

        if (m_active_tab == 0) {
            // ── FLEET: browse ships + purchase ────────────────────────────
            if (SHIP_FLEET.empty()) return;
            const size_t fleet_n = SHIP_FLEET.size();
            if (m_btn_prev.update(mouse_pos) || IsKeyPressed(KEY_LEFT_BRACKET)) {
                m_selected_idx = static_cast<int>((m_selected_idx - 1 + fleet_n) % fleet_n);
            }
            if (m_btn_next.update(mouse_pos) || IsKeyPressed(KEY_RIGHT_BRACKET)) {
                m_selected_idx = static_cast<int>((m_selected_idx + 1) % fleet_n);
            }

            const auto& ship = SHIP_FLEET[m_selected_idx];
            int max_wave = DBSystem::instance().max_wave();
            bool already_owned = CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave);

            // Refresh the buy button label to reflect the current selection.
            std::string buy_label;
            UI::ButtonKind buy_kind = UI::ButtonKind::PRIMARY;
            if (already_owned) {
                buy_label = "OWNED";
                buy_kind = UI::ButtonKind::GHOST;
                m_btn_buy.set_label(buy_label);
            } else if (!ship.boss_unlock_id.empty()) {
                buy_label = std::string("DEFEAT ") + ship.boss_unlock_name;
                buy_kind = UI::ButtonKind::GHOST;
                m_btn_buy.set_label(buy_label);
            } else if (max_wave < ship.unlock_wave) {
                buy_label = "LOCKED // WAVE " + std::to_string(ship.unlock_wave);
                buy_kind = UI::ButtonKind::GHOST;
                m_btn_buy.set_label(buy_label);
            } else if (CurrencySystem::instance().prana_shards() < ship.prana_cost) {
                buy_label = std::to_string(ship.prana_cost) + " PRANA REQUIRED";
                buy_kind = UI::ButtonKind::GHOST;
                m_btn_buy.set_label(buy_label);
            } else {
                buy_label = "UNLOCK FOR " + std::to_string(ship.prana_cost) + " PRANA";
                buy_kind = UI::ButtonKind::PRIMARY;
                m_btn_buy.set_label(buy_label);
            }
            m_btn_buy.set_kind(buy_kind);

            const bool buy_clicked = m_btn_buy.update(mouse_pos);
            if (buy_clicked && !already_owned && ship.boss_unlock_id.empty()
                && max_wave >= ship.unlock_wave
                && CurrencySystem::instance().prana_shards() >= ship.prana_cost) {
                bool success = CurrencySystem::instance().try_unlock_ship_with_prana(ship.id, max_wave);
                if (success) {
                    DBSystem::instance().save_game();   // crash-safe persistence
                    SoundSystem::instance().play_sfx("powerup.wav");
                    m_flash_kind = FlashKind::SUCCESS;
                    m_flash_timer = 1.2f;
                    m_flash_text = "ACQUIRED // " + ship.name;
                } else {
                    m_flash_kind = FlashKind::INSUFFICIENT;
                    m_flash_timer = 1.2f;
                    m_flash_text = "TRANSACTION FAILED";
                }
            } else if (buy_clicked && already_owned) {
                m_flash_kind = FlashKind::ALREADY_OWNED;
                m_flash_timer = 1.0f;
                m_flash_text = "ALREADY IN FLEET";
            } else if (buy_clicked) {
                m_flash_kind = FlashKind::INSUFFICIENT;
                m_flash_timer = 1.0f;
                m_flash_text = "REQUIREMENTS NOT MET";
            }
        } else {
            // ── CONSUMABLES ────────────────────────────────────────────────
            auto try_consum = [&](const char* name, const char* item) {
                ConsumableInventory inventory = DBSystem::instance().armory_inventory();
                if (!CurrencySystem::instance().buy_consumable(inventory, item)) {
                    m_flash_kind = FlashKind::INSUFFICIENT;
                    m_flash_timer = 1.0f;
                    m_flash_text = std::string("SUPPLY LIMIT OR INSUFFICIENT PRANA // ") + name;
                } else {
                    DBSystem::instance().set_armory_inventory(inventory);
                    DBSystem::instance().save_game();
                    SoundSystem::instance().play_sfx("ui_click.wav");
                    m_flash_kind = FlashKind::SUCCESS;
                    m_flash_timer = 1.0f;
                    m_flash_text = std::string("ACQUIRED // ") + name;
                }
            };
            if (m_btn_buy_kavach.update(mouse_pos)) {
                try_consum("KAVACH", "kavach");
            }
            if (m_btn_buy_soma.update(mouse_pos)) {
                try_consum("SOMA", "soma");
            }
            if (m_btn_buy_vajra.update(mouse_pos)) {
                try_consum("VAJRA", "vajra");
            }
        }

        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        using namespace Vimana::UI;
        ClearBackground(PAL_BG_VOID);

        // Parallax stars (reuse pattern from other views)
        for (int i = 0; i < 60; ++i) {
            DrawCircle(20 + i * 17 % SCREEN_WIDTH, (10 + i * 31) % SCREEN_HEIGHT,
                       0.6f + (i % 3) * 0.3f, { 180, 200, 240, 110 });
        }

        Font title_f = AssetManager::instance().title_font();
        Font body_f  = AssetManager::instance().body_font();

        // Header
        Rectangle header = { 30, 20, 840, 50 };
        DrawElevationPanel(header, ElevationGlass(), true);
        DrawCornerBrackets(header, 10.0f, PAL_PRIMARY);
        DrawTextEx(title_f, "CELESTIAL ARMORY // SHOP & SUPPLY", { 45, 30 }, 19, 1.0f, PAL_PRIMARY_BRIGHT);

        std::string balance = "PRANA: " + std::to_string(CurrencySystem::instance().prana_shards());
        Vector2 bs = MeasureTextEx(body_f, balance.c_str(), 15, 1.0f);
        DrawTextEx(body_f, balance.c_str(), { SCREEN_WIDTH - bs.x - 50, 35 }, 15, 1.0f, PAL_PRIMARY_BRIGHT);

        // Tabs
        m_tab_fleet.draw(title_f);
        m_tab_consum.draw(title_f);

        if (m_active_tab == 0) draw_fleet_tab(title_f, body_f);
        else                   draw_consumables_tab(title_f, body_f);

        m_btn_back.draw(title_f);

        // Feedback flash banner
        if (m_flash_kind != FlashKind::NONE && m_flash_timer > 0.0f) {
            Color flash_col = (m_flash_kind == FlashKind::SUCCESS)    ? PAL_HEALTH_HIGH
                            : (m_flash_kind == FlashKind::ALREADY_OWNED) ? PAL_SECONDARY_BRIGHT
                            : PAL_DESTRUCTIVE_BRIGHT;
            Rectangle fb = { 200, SCREEN_HEIGHT - 110, 500, 32 };
            DrawRectangleRec(fb, { 0x0E, 0x13, 0x20, 230 });
            DrawRectangleLinesEx(fb, 1.5f, flash_col);
            Vector2 sz = MeasureTextEx(title_f, m_flash_text.c_str(), 16, 1.0f);
            DrawTextEx(title_f, m_flash_text.c_str(),
                       { fb.x + (fb.width - sz.x) * 0.5f, fb.y + (fb.height - 16) * 0.5f },
                       16, 1.0f, flash_col);
        }

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::ARMORY; }

private:
    void draw_fleet_tab(Font title_f, Font body_f) {
        using namespace Vimana::UI;
        if (SHIP_FLEET.empty()) return;
        const auto& ship = SHIP_FLEET[m_selected_idx];
        int max_wave = DBSystem::instance().max_wave();
        bool owned = CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave);

        // Selected ship display
        Rectangle card = { 60, 150, 380, 350 };
        auto elev = owned ? ElevationFocus() : ElevationWell();
        DrawElevationPanel(card, elev);
        DrawCornerBrackets(card, 12.0f, owned ? PAL_PRIMARY : PAL_TEXT_MUTED);

        // Big ship preview
        Texture2D tex = AssetManager::instance().get_texture(ship.sprite_file);
        if (tex.id > 0) {
            Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest = { card.x + card.width * 0.5f, card.y + 130, tex.width * 1.2f, tex.height * 1.2f };
            Vector2 origin = { dest.width * 0.5f, dest.height * 0.5f };
            DrawTexturePro(tex, src, dest, origin, std::sin(GetTime() * 1.5f) * 2.0f,
                           owned ? WHITE : Color{ 90, 90, 110, 220 });
        }

        // Ship name
        DrawTextEx(title_f, ship.name.c_str(), { card.x + 18, card.y + 14 }, 19, 1.0f,
                   owned ? PAL_PRIMARY_BRIGHT : PAL_TEXT_VARIANT);
        DrawTextEx(body_f, ship.subtitle.c_str(), { card.x + 18, card.y + 40 }, 12, 1.0f, PAL_SECONDARY_BRIGHT);

        // Counter / role
        std::string role_line = std::string("ROLE: ") + ship.role + "  //  " +
                                std::to_string(m_selected_idx + 1) + "/" + std::to_string(SHIP_FLEET.size());
        DrawTextEx(body_f, role_line.c_str(), { card.x + 18, card.y + 60 }, 11, 1.0f, PAL_TEXT_BODY);

        // Stats lines
        auto stat_line = [&](int y, const char* label, float v, float maxv, Color c) {
            DrawTextEx(body_f, label, { card.x + 18, static_cast<float>(y) }, 11, 1.0f, PAL_TEXT_BODY);
            Rectangle g = { card.x + 130, static_cast<float>(y + 2), 220, 11 };
            DrawSegmentedHealthGauge(g, v, maxv, 10, 0.0f);
            (void)c;
        };
        stat_line(280, "HULL",  ship.max_hp * 1.0f, 600.0f, PAL_HEALTH_HIGH);
        stat_line(305, "SPEED", ship.speed, 500.0f, PAL_SECONDARY_BRIGHT);
        stat_line(330, "DAMAGE", ship.bullet_damage, 100.0f, PAL_DESTRUCTIVE_BRIGHT);
        stat_line(355, "DASH",   static_cast<float>(ship.dash_charges), 3.0f, PAL_PRIMARY_BRIGHT);

        // Status strip
        std::string status_text;
        Color status_col;
        if (owned) {
            status_text = "OWNED // READY FOR DEPLOYMENT";
            status_col = PAL_HEALTH_HIGH;
        } else if (!ship.boss_unlock_id.empty()) {
            status_text = "DEFEAT " + std::string(ship.boss_unlock_name) + " // BOSS SALVAGE";
            status_col = PAL_DESTRUCTIVE_BRIGHT;
        } else if (max_wave < ship.unlock_wave) {
            status_text = "REACH WAVE " + std::to_string(ship.unlock_wave) + " // " +
                          std::to_string(max_wave) + " / 30 OF ACT " +
                          std::to_string(CampaignActForWave(max_wave));
            status_col = PAL_HEALTH_MID;
        } else {
            status_text = "AVAILABLE FOR PURCHASE";
            status_col = PAL_SECONDARY_BRIGHT;
        }
        DrawTextEx(body_f, status_text.c_str(), { card.x + 18, card.y + 388 }, 11, 1.0f, status_col);

        // Browse + Buy buttons (right column)
        m_btn_prev.draw(title_f);
        m_btn_next.draw(title_f);
        m_btn_buy.draw(title_f);

        // Owned fleet summary at the bottom
        int owned_count = 0;
        for (const auto& s : SHIP_FLEET) {
            if (CurrencySystem::instance().is_ship_unlocked(s.id, max_wave)) ++owned_count;
        }
        std::string fleet_line = "FLEET: " + std::to_string(owned_count) + " / " +
                                 std::to_string(SHIP_FLEET.size()) + " VIMANAS COMBAT READY";
        DrawTextEx(body_f, fleet_line.c_str(), { 60, SCREEN_HEIGHT - 60 }, 12, 1.0f, PAL_HEALTH_HIGH);
    }

    void draw_consumables_tab(Font title_f, Font body_f) {
        using namespace Vimana::UI;
        Rectangle info = { 60, 150, 380, 280 };
        DrawElevationPanel(info, ElevationWell());
        DrawCornerBrackets(info, 12.0f, PAL_SECONDARY);

        DrawTextEx(title_f, "TACTICAL CONSUMABLES", { info.x + 18, info.y + 14 }, 18, 1.0f, PAL_PRIMARY_BRIGHT);
        DrawTextEx(body_f, "Per-run stock is consumed on deploy.", { info.x + 18, info.y + 42 }, 11, 1.0f, PAL_TEXT_MUTED);

        // What each does (short)
        DrawTextEx(body_f, "KAVACH",  { info.x + 18, info.y + 90 },  13, 1.0f, PAL_SECONDARY_BRIGHT);
        DrawTextEx(body_f, "Absorbs one hit on next contact.",  { info.x + 18, info.y + 108 }, 10, 1.0f, PAL_TEXT_BODY);
        DrawTextEx(body_f, "SOMA",    { info.x + 18, info.y + 138 }, 13, 1.0f, PAL_HEALTH_HIGH);
        DrawTextEx(body_f, "Self-revive or revive a downed ally.", { info.x + 18, info.y + 156 }, 10, 1.0f, PAL_TEXT_BODY);
        DrawTextEx(body_f, "VAJRA",   { info.x + 18, info.y + 186 }, 13, 1.0f, PAL_DESTRUCTIVE_BRIGHT);
        DrawTextEx(body_f, "AOE explosion clears the screen.",   { info.x + 18, info.y + 204 }, 10, 1.0f, PAL_TEXT_BODY);

        // Buy panel
        Rectangle buy = { 480, 150, 360, 280 };
        DrawElevationPanel(buy, ElevationWell());
        DrawCornerBrackets(buy, 12.0f, PAL_PRIMARY);
        DrawTextEx(title_f, "PURCHASE SUPPLY", { buy.x + 18, buy.y + 14 }, 18, 1.0f, PAL_PRIMARY_BRIGHT);

        std::string bal = "PRANA: " + std::to_string(CurrencySystem::instance().prana_shards());
        DrawTextEx(body_f, bal.c_str(), { buy.x + 18, buy.y + 42 }, 13, 1.0f, PAL_PRIMARY_BRIGHT);

        DrawTextEx(body_f, "Cap: 3 KAVACH / 5 SOMA / 5 VAJRA per run",
                   { buy.x + 18, buy.y + 70 }, 10, 1.0f, PAL_TEXT_MUTED);

        m_btn_buy_kavach.draw(title_f);
        m_btn_buy_soma.draw(title_f);
        m_btn_buy_vajra.draw(title_f);

        // Affordability hints
        int ps = CurrencySystem::instance().prana_shards();
        std::string k_aff = ps >= COST_KAVACH_SHIELD ? "[OK]" : "[NEED " + std::to_string(COST_KAVACH_SHIELD - ps) + " MORE]";
        std::string s_aff = ps >= COST_SOMA_VIAL     ? "[OK]" : "[NEED " + std::to_string(COST_SOMA_VIAL - ps) + " MORE]";
        std::string v_aff = ps >= COST_VAJRA_FLARE   ? "[OK]" : "[NEED " + std::to_string(COST_VAJRA_FLARE - ps) + " MORE]";
        DrawTextEx(body_f, k_aff.c_str(), { buy.x + 240, buy.y + 123 }, 11, 1.0f,
                   ps >= COST_KAVACH_SHIELD ? PAL_HEALTH_HIGH : PAL_DESTRUCTIVE_BRIGHT);
        DrawTextEx(body_f, s_aff.c_str(), { buy.x + 240, buy.y + 173 }, 11, 1.0f,
                   ps >= COST_SOMA_VIAL ? PAL_HEALTH_HIGH : PAL_DESTRUCTIVE_BRIGHT);
        DrawTextEx(body_f, v_aff.c_str(), { buy.x + 240, buy.y + 223 }, 11, 1.0f,
                   ps >= COST_VAJRA_FLARE ? PAL_HEALTH_HIGH : PAL_DESTRUCTIVE_BRIGHT);
    }

    ViewType m_next_view;
    int m_active_tab;
    int m_selected_idx;
    float m_flash_timer = 0.0f;
    FlashKind m_flash_kind = FlashKind::NONE;
    std::string m_flash_text;

    UI::Button m_tab_fleet;
    UI::Button m_tab_consum;
    UI::Button m_btn_buy;
    UI::Button m_btn_prev;
    UI::Button m_btn_next;
    UI::Button m_btn_back;
    UI::Button m_btn_buy_kavach;
    UI::Button m_btn_buy_soma;
    UI::Button m_btn_buy_vajra;
};

} // namespace Vimana
