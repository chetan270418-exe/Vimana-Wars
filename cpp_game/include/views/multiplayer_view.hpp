#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/network_manager.hpp"
#include "systems/db_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class MultiplayerView : public IView {
public:
    MultiplayerView() 
        : m_next_view(ViewType::MULTIPLAYER_LOBBY),
          m_in_room(false),
          m_is_ready(false),
          m_btn_quick({ 580, 105, 260, 36 }, "QUICK MATCH (CO-OP)", COLOR_GOLD_BRIGHT),
          m_btn_create({ 580, 150, 260, 36 }, "CREATE SQUAD ROOM", COLOR_CYAN_BRIGHT),
          m_btn_duel({ 580, 195, 260, 36 }, "1V1 PVP ARENA DUEL", COLOR_ORANGE_BRIGHT),
          m_btn_refresh({ 580, 240, 260, 36 }, "REFRESH LOBBIES", COLOR_GOLD),
          m_btn_ready({ 580, 390, 260, 42 }, "READY PILOT [SPACE]", COLOR_GREEN_BRIGHT),
          m_btn_start({ 580, 440, 260, 42 }, "DEPLOY SQUADRON", COLOR_GOLD_BRIGHT),
          m_btn_add_ai({ 580, 340, 260, 36 }, "+ ADD AI SQUADMATE", COLOR_PURPLE_BRIGHT),
          m_btn_back({ 40, 520, 110, 36 }, "BACK", COLOR_MUTED)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::MULTIPLAYER_LOBBY;
        m_in_room = false;
        m_is_ready = false;

        m_lobbies = {
            { "VX82Q", "Swarga Assault (2/4)", "CO-OP PVE", "READY" },
            { "LK99A", "Lanka Rift Incursion (1/4)", "CO-OP PVE", "WAITING" },
            { "DUEL1", "Celestial Colosseum (1/2)", "1V1 PVP", "CHALLENGE" }
        };
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            if (m_in_room) {
                m_in_room = false;
                NetworkManager::instance().leave_session();
            } else {
                m_next_view = ViewType::MENU;
            }
            return;
        }

        if (!m_in_room) {
            // Browser View Actions
            if (m_btn_create.update(mouse_pos)) {
                m_in_room = true;
                NetworkManager::instance().host_session(DBSystem::instance().player_name(), "garuda");
            } else if (m_btn_quick.update(mouse_pos)) {
                m_in_room = true;
                NetworkManager::instance().join_session("VX82Q", DBSystem::instance().player_name(), "pushpaka");
                NetworkManager::instance().add_teammate("ROHAN", "tripura", false);
            } else if (m_btn_duel.update(mouse_pos)) {
                m_next_view = ViewType::DUEL;
            } else if (m_btn_refresh.update(mouse_pos)) {
                // Refresh list
                m_lobbies[0].status = "STANDBY";
            }
        } else {
            // Squad Room View Actions
            if (m_btn_ready.update(mouse_pos) || IsKeyPressed(KEY_SPACE)) {
                m_is_ready = !m_is_ready;
                m_btn_ready.set_label(m_is_ready ? "STATUS: READY ★" : "READY PILOT [SPACE]");
                m_btn_ready.set_color(m_is_ready ? COLOR_GOLD_BRIGHT : COLOR_GREEN_BRIGHT);
            }

            if (m_btn_add_ai.update(mouse_pos)) {
                if (NetworkManager::instance().players().size() == 1) {
                    NetworkManager::instance().add_teammate("ROHAN // AI", "tripura", true);
                } else if (NetworkManager::instance().players().size() == 2) {
                    NetworkManager::instance().add_teammate("ARYA // AI", "vajra", true);
                } else if (NetworkManager::instance().players().size() == 3) {
                    NetworkManager::instance().add_teammate("DEV // AI", "kamadhenu", true);
                }
            }

            if (m_btn_start.update(mouse_pos)) {
                // Launch directly into co-op combat!
                m_next_view = ViewType::GAMEPLAY;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "SANGHA NETWORK // MULTIPLAYER SQUAD COMMAND", { 45, 30 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        // Ping Indicator
        std::string ping_str = "🟢 " + std::to_string(NetworkManager::instance().ping_ms()) + " ms (SERVER AUTHORITATIVE)";
        DrawText(ping_str.c_str(), SCREEN_WIDTH - 300, 36, 12, COLOR_GREEN_BRIGHT);

        if (!m_in_room) {
            // ── BROWSER MODE ──
            UI::DrawChamferedPanel({ 30, 85, 520, 420 }, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            DrawText("OPEN SQUAD SESSIONS", 50, 100, 12, COLOR_GOLD_BRIGHT);

            DrawText("ROOM", 50, 125, 10, COLOR_MUTED);
            DrawText("MISSION / REALM", 130, 125, 10, COLOR_MUTED);
            DrawText("MODE", 330, 125, 10, COLOR_MUTED);
            DrawText("STATUS", 440, 125, 10, COLOR_MUTED);
            DrawLine(45, 142, 535, 142, COLOR_SURFACE_HIGH);

            int y = 158;
            for (const auto& lob : m_lobbies) {
                Rectangle row_rec = { 45, static_cast<float>(y - 4), 490, 34 };
                UI::DrawChamferedPanel(row_rec, COLOR_SURFACE_MID, COLOR_SURFACE_MID, 3.0f);

                DrawText(lob.code.c_str(), 50, y + 4, 12, COLOR_GOLD_BRIGHT);
                DrawText(lob.name.c_str(), 130, y + 4, 12, COLOR_PARCHMENT);
                DrawText(lob.slots.c_str(), 330, y + 4, 11, COLOR_CYAN_BRIGHT);
                DrawText(lob.status.c_str(), 440, y + 4, 11, COLOR_GREEN_BRIGHT);
                y += 42;
            }

            // Right Actions
            UI::DrawChamferedPanel({ 560, 85, 310, 420 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
            DrawText("SQUAD PROTOCOLS", 580, 100, 11, COLOR_MUTED);

            m_btn_quick.draw(font);
            m_btn_create.draw(font);
            m_btn_duel.draw(font);
            m_btn_refresh.draw(font);

            DrawText("CO-OP FEATURES ACTIVE:", 580, 295, 10, COLOR_MUTED);
            DrawText("• 2-4 Pilot Synchronized Combat", 580, 315, 11, COLOR_CYAN_BRIGHT);
            DrawText("• Downed + Revive Mechanic [Hold E]", 580, 335, 11, COLOR_PARCHMENT);
            DrawText("• Team Combo Transcendence Buff", 580, 355, 11, COLOR_GOLD_BRIGHT);
            DrawText("• Cooperative Dual-Astra Storms", 580, 375, 11, COLOR_GREEN_BRIGHT);

        } else {
            // ── SQUAD ROOM VIEW ──
            UI::DrawChamferedPanel({ 30, 85, 520, 420 }, COLOR_GOLD_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            std::string code_header = "VIMANA SQUAD // ROOM CODE: " + NetworkManager::instance().room_code();
            DrawTextEx(font, code_header.c_str(), { 50, 100 }, 16, 1.0f, COLOR_GOLD_BRIGHT);

            const auto& players = NetworkManager::instance().players();

            for (int i = 0; i < 4; ++i) {
                float slot_y = 135.0f + i * 85.0f;
                Rectangle slot_box = { 45, slot_y, 490, 75 };
                bool filled = (i < static_cast<int>(players.size()));

                Color slot_border = filled ? COLOR_GOLD : COLOR_SURFACE_HIGH;
                Color slot_bg = filled ? COLOR_SURFACE_MID : COLOR_SURFACE_LOW;
                UI::DrawChamferedPanel(slot_box, slot_border, slot_bg, 4.0f);

                DrawText(("PILOT SLOT 0" + std::to_string(i + 1)).c_str(), 55, slot_y + 8, 9, COLOR_MUTED);

                if (filled) {
                    std::string p_name = (i == 0) ? DBSystem::instance().player_name() + " [HOST]" : "SQUAD PILOT 0" + std::to_string(i + 1);
                    DrawText(p_name.c_str(), 55, slot_y + 24, 14, COLOR_GOLD_BRIGHT);

                    std::string vessel_str = "VESSEL: " + std::string(players[i].ship_id);
                    DrawText(vessel_str.c_str(), 55, slot_y + 44, 11, COLOR_CYAN_BRIGHT);

                    const char* role_badge = (i == 0) ? "ROLE: MOBILITY (DPS)" :
                                             (i == 1) ? "ROLE: TANK (FRONT)" :
                                             (i == 2) ? "ROLE: HEAVY DPS" : "ROLE: SUPPORT (HEAL)";
                    DrawText(role_badge, 220, slot_y + 44, 11, COLOR_PARCHMENT);

                    DrawText("STATUS: READY ★", 380, slot_y + 28, 12, COLOR_GREEN_BRIGHT);
                } else {
                    DrawText("EMPTY SQUAD POSITION", 55, slot_y + 28, 13, COLOR_MUTED);
                    DrawText("AWAITING SQUAD PILOT OR AI BOT", 55, slot_y + 46, 10, COLOR_SURFACE_HIGH);
                }
            }

            // Right Panel Room Controls
            UI::DrawChamferedPanel({ 560, 85, 310, 420 }, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            DrawText("SQUAD BRIEFING & LAUNCH", 580, 100, 11, COLOR_MUTED);

            DrawText("MISSION: LANKA ASSAULT", 580, 130, 13, COLOR_GOLD_BRIGHT);
            DrawText("DIFFICULTY: ASURA SLAYER", 580, 155, 12, COLOR_RED_BRIGHT);
            DrawText("OBJECTIVE: SURVIVE & SLAY BOSS", 580, 180, 11, COLOR_PARCHMENT);
            DrawText("CO-OP ASTRA: THUNDER TEMPEST", 580, 205, 11, COLOR_CYAN_BRIGHT);

            DrawLine(580, 235, 850, 235, COLOR_SURFACE_HIGH);

            m_btn_add_ai.draw(font);
            m_btn_ready.draw(font);
            m_btn_start.draw(font);
        }

        m_btn_back.draw(font);
        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::MULTIPLAYER_LOBBY; }

private:
    struct LobbyEntry {
        std::string code;
        std::string name;
        std::string slots;
        std::string status;
    };

    ViewType m_next_view;
    bool m_in_room;
    bool m_is_ready;
    std::vector<LobbyEntry> m_lobbies;

    UI::Button m_btn_quick;
    UI::Button m_btn_create;
    UI::Button m_btn_duel;
    UI::Button m_btn_refresh;
    UI::Button m_btn_ready;
    UI::Button m_btn_start;
    UI::Button m_btn_add_ai;
    UI::Button m_btn_back;
};

} // namespace Vimana
