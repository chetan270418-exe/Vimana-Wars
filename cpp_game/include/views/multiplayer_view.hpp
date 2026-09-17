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
          m_target_ip("127.0.0.1"),
          m_target_port("7704"),
          m_ip_focused(false),
          m_btn_quick({ 580, 105, 260, 36 }, "QUICK MATCH (LOCAL)", COLOR_GOLD_BRIGHT),
          m_btn_create({ 580, 150, 260, 36 }, "HOST LAN SERVER [7704]", COLOR_CYAN_BRIGHT),
          m_btn_join_lan({ 580, 265, 260, 36 }, "JOIN LAN HOST >>", COLOR_GREEN_BRIGHT),
          m_btn_duel({ 580, 310, 260, 36 }, "1V1 PVP ARENA DUEL", COLOR_ORANGE_BRIGHT),
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
        m_ip_focused = false;

        m_lobbies = {
            { "VX82Q", "Swarga Assault (2/4)", "CO-OP PVE", "READY" },
            { "LK99A", "Lanka Rift Incursion (1/4)", "CO-OP PVE", "WAITING" },
            { "DUEL1", "Celestial Colosseum (1/2)", "1V1 PVP", "CHALLENGE" }
        };
    }

    void update(float dt, Vector2 mouse_pos) override {
        NetworkManager::instance().update(dt);

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
            // IP Input interaction
            Rectangle ip_rec = { 580, 225, 260, 32 };
            if (CheckCollisionPointRec(mouse_pos, ip_rec) && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                m_ip_focused = true;
            } else if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                m_ip_focused = false;
            }

            if (m_ip_focused) {
                int key = GetCharPressed();
                while (key > 0) {
                    if (((key >= '0' && key <= '9') || key == '.' || key == ':') && m_target_ip.length() < 21) {
                        m_target_ip.push_back(static_cast<char>(key));
                    }
                    key = GetCharPressed();
                }
                if (IsKeyPressed(KEY_BACKSPACE) && !m_target_ip.empty()) {
                    m_target_ip.pop_back();
                }
            }

            // Browser View Actions
            if (m_btn_create.update(mouse_pos)) {
                m_in_room = true;
                NetworkManager::instance().host_session(DBSystem::instance().player_name(), "garuda", 7704);
            } else if (m_btn_join_lan.update(mouse_pos)) {
                m_in_room = true;
                NetworkManager::instance().join_session(m_target_ip, 7704, DBSystem::instance().player_name(), "pushpaka");
            } else if (m_btn_quick.update(mouse_pos)) {
                m_in_room = true;
                NetworkManager::instance().host_session(DBSystem::instance().player_name(), "garuda", 7704);
                NetworkManager::instance().add_teammate("ROHAN // AI", "tripura", true);
            } else if (m_btn_duel.update(mouse_pos)) {
                m_next_view = ViewType::DUEL;
            }
        } else {
            // Squad Room View Actions
            if (m_btn_ready.update(mouse_pos) || IsKeyPressed(KEY_SPACE)) {
                m_is_ready = !m_is_ready;
                m_btn_ready.set_label(m_is_ready ? "STATUS: READY ?" : "READY PILOT [SPACE]");
                m_btn_ready.set_color(m_is_ready ? COLOR_GOLD_BRIGHT : COLOR_GREEN_BRIGHT);
            }

            if (m_btn_add_ai.update(mouse_pos)) {
                size_t p_count = NetworkManager::instance().players().size();
                if (p_count == 1) {
                    NetworkManager::instance().add_teammate("ROHAN // AI", "tripura", true);
                } else if (p_count == 2) {
                    NetworkManager::instance().add_teammate("ARYA // AI", "vajra", true);
                } else if (p_count == 3) {
                    NetworkManager::instance().add_teammate("DEV // AI", "kamadhenu", true);
                }
            }

            if (m_btn_start.update(mouse_pos)) {
                // Launch into co-op combat!
                m_next_view = ViewType::GAMEPLAY;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "SANGHA NETWORK // REAL WINSOCK2 UDP SQUAD COMMAND", { 45, 30 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        // Ping Indicator
        std::string ping_str = "?? RTT " + std::to_string(NetworkManager::instance().ping_ms()) + " ms [PORT 7704]";
        DrawText(ping_str.c_str(), SCREEN_WIDTH - 240, 36, 12, COLOR_GREEN_BRIGHT);

        if (!m_in_room) {
            // -- BROWSER MODE --
            UI::DrawChamferedPanel({ 30, 85, 520, 420 }, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            DrawText("OPEN SQUAD LAN PROTOCOLS", 50, 100, 12, COLOR_GOLD_BRIGHT);

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
            DrawText("LAN SQUAD SETUP", 580, 95, 11, COLOR_MUTED);

            m_btn_quick.draw(font);
            m_btn_create.draw(font);

            // IP Entry box
            DrawText("TARGET LAN HOST IP & PORT:", 580, 205, 10, COLOR_PARCHMENT);
            Rectangle ip_rec = { 580, 225, 260, 32 };
            DrawRectangleRec(ip_rec, m_ip_focused ? COLOR_SURFACE_HIGH : COLOR_SURFACE_MID);
            DrawRectangleLinesEx(ip_rec, 1.5f, m_ip_focused ? COLOR_CYAN_BRIGHT : COLOR_SURFACE_HIGH);
            DrawText(m_target_ip.c_str(), 590, 233, 14, WHITE);
            if (m_ip_focused && (static_cast<int>(GetTime() * 2) % 2 == 0)) {
                int txt_w = MeasureText(m_target_ip.c_str(), 14);
                DrawLine(590 + txt_w + 2, 229, 590 + txt_w + 2, 251, COLOR_CYAN_BRIGHT);
            }

            m_btn_join_lan.draw(font);
            m_btn_duel.draw(font);

            DrawText("ACTIVE SQUAD NETCODE:", 580, 360, 10, COLOR_MUTED);
            DrawText("• Winsock2 Non-blocking UDP (Port 7704)", 580, 380, 11, COLOR_CYAN_BRIGHT);
            DrawText("• 30Hz Server Snapshots + 60Hz Inputs", 580, 400, 11, COLOR_PARCHMENT);
            DrawText("• 15s Reconnect Window + AI Takeover", 580, 420, 11, COLOR_GOLD_BRIGHT);
            DrawText("• Downed Beacon [Hold E to Revive]", 580, 440, 11, COLOR_GREEN_BRIGHT);

        } else {
            // -- SQUAD ROOM VIEW --
            UI::DrawChamferedPanel({ 30, 85, 520, 420 }, COLOR_GOLD_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            std::string code_header = "VIMANA SQUAD // ROOM: " + NetworkManager::instance().room_code();
            if (NetworkManager::instance().role() == NetworkRole::HOST) code_header += " [HOST - PORT 7704]";
            else code_header += " [CLIENT - " + NetworkManager::instance().target_host_ip() + "]";

            DrawTextEx(font, code_header.c_str(), { 50, 100 }, 15, 1.0f, COLOR_GOLD_BRIGHT);

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

                    DrawText("STATUS: READY ?", 380, slot_y + 28, 12, COLOR_GREEN_BRIGHT);
                } else {
                    DrawText("EMPTY SQUAD POSITION", 55, slot_y + 28, 13, COLOR_MUTED);
                    DrawText("AWAITING SQUAD PILOT OR AI BOT", 55, slot_y + 46, 10, COLOR_SURFACE_HIGH);
                }
            }

            // Right Panel Room Controls
            UI::DrawChamferedPanel({ 560, 85, 310, 420 }, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            DrawText("SQUAD BRIEFING & LAUNCH", 580, 100, 11, COLOR_MUTED);

            DrawText("MISSION: MAHAYUDDHA CO-OP", 580, 130, 13, COLOR_GOLD_BRIGHT);
            DrawText("DIFFICULTY: KSHATRIYA", 580, 155, 12, COLOR_RED_BRIGHT);
            DrawText("OBJECTIVE: SURVIVE & SLAY BOSS", 580, 180, 11, COLOR_PARCHMENT);
            DrawText("CO-OP ASTRA: DUAL SYNERGY", 580, 205, 11, COLOR_CYAN_BRIGHT);

            DrawLine(580, 235, 850, 235, COLOR_SURFACE_HIGH);

            m_btn_add_ai.draw(font);
            m_btn_ready.draw(font);
            m_btn_start.draw(font);
        }

        m_btn_back.draw(font);
        if (g_scanlines_enabled) UI::DrawScanlines();
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
    std::string m_target_ip;
    std::string m_target_port;
    bool m_ip_focused;
    std::vector<LobbyEntry> m_lobbies;

    UI::Button m_btn_quick;
    UI::Button m_btn_create;
    UI::Button m_btn_join_lan;
    UI::Button m_btn_duel;
    UI::Button m_btn_ready;
    UI::Button m_btn_start;
    UI::Button m_btn_add_ai;
    UI::Button m_btn_back;
};

} // namespace Vimana
