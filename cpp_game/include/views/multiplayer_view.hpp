#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/network_manager.hpp"
#include "systems/account_system.hpp"
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
          m_cloud_status("Querying active online lobbies..."),
          m_btn_quick({ 580, 100, 260, 34 }, "QUICK LOCAL SQUAD", COLOR_GOLD_BRIGHT),
          m_btn_create_cloud({ 580, 142, 260, 34 }, "HOST ONLINE CLOUD LOBBY", COLOR_GOLD_BRIGHT),
          m_btn_create({ 580, 184, 260, 32 }, "HOST LOCAL LAN [7704]", COLOR_CYAN_BRIGHT),
          m_btn_join_lan({ 580, 280, 260, 34 }, "JOIN LAN HOST >>", COLOR_GREEN_BRIGHT),
          m_btn_duel({ 580, 322, 260, 32 }, "1V1 ARENA DUEL", COLOR_ORANGE_BRIGHT),
          m_btn_refresh_lobbies({ 420, 95, 115, 26 }, "REFRESH", COLOR_CYAN_BRIGHT),
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
        m_cloud_status = "Querying live Sangha lobbies...";

        m_lobbies = {
            { "LAN01", "Swarga Assault (2/4)", "CO-OP PVE", "READY" },
            { "LAN02", "Lanka Rift Incursion (1/4)", "CO-OP PVE", "WAITING" },
            { "DUEL1", "Celestial Colosseum (1/2)", "1V1 PVP", "CHALLENGE" }
        };

        fetch_online_lobbies();
    }

    void fetch_online_lobbies() {
        AccountSystem::instance().fetch_lobbies([this](bool success, const std::vector<nlohmann::json>& lobbies) {
            if (success && !lobbies.empty()) {
                m_lobbies.clear();
                for (const auto& l : lobbies) {
                    std::string code = l.value("code", "VMN");
                    std::string mode = l.value("mode", "campaign");
                    int max_p = l.value("max_players", 4);
                    int current_p = l.contains("players") ? static_cast<int>(l["players"].size()) : 1;
                    std::string status = l.value("status", "waiting");
                    std::string name = (mode == "duel" ? "Celestial Duel (" : "Swarga Assault (") + std::to_string(current_p) + "/" + std::to_string(max_p) + ")";
                    std::string mode_str = (mode == "duel" ? "1V1 PVP" : "CO-OP PVE");
                    std::string status_str = (status == "waiting" ? "OPEN" : "IN COMBAT");
                    m_lobbies.push_back({ code, name, mode_str, status_str });
                }
                m_cloud_status = "Cloud lobbies synced: " + std::to_string(m_lobbies.size()) + " rooms available";
            } else {
                m_cloud_status = "Showing standard LAN broadcast lobbies";
            }
        });
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
            if (m_btn_refresh_lobbies.update(mouse_pos)) {
                fetch_online_lobbies();
            }

            // Click lobby row to select
            int ly = 158;
            for (const auto& lob : m_lobbies) {
                Rectangle row_rec = { 45, static_cast<float>(ly - 4), 490, 34 };
                if (CheckCollisionPointRec(mouse_pos, row_rec) && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                    m_in_room = true;
                    NetworkManager::instance().join_session(m_target_ip, 7704, DBSystem::instance().player_name(), "pushpaka");
                    break;
                }
                ly += 42;
            }

            // IP Input interaction
            Rectangle ip_rec = { 580, 240, 260, 32 };
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
            if (m_btn_create_cloud.update(mouse_pos)) {
                AccountSystem::instance().create_lobby("campaign", 4, "garuda", [this](bool success, const std::string& code, const std::string& msg) {
                    m_in_room = true;
                    NetworkManager::instance().host_session(DBSystem::instance().player_name(), "garuda", 7704);
                });
            } else if (m_btn_create.update(mouse_pos)) {
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
                m_btn_ready.set_label(m_is_ready ? "STATUS: [READY]" : "READY PILOT [SPACE]");
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
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(title_font, "SANGHA NETWORK // REAL WINSOCK2 UDP SQUAD COMMAND", { 45, 30 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        // Ping Indicator
        std::string ping_str = "RTT: " + std::to_string(NetworkManager::instance().ping_ms()) + " ms | PORT 7704";
        DrawCircle(SCREEN_WIDTH - 245, 45, 4.0f, COLOR_GREEN_BRIGHT);
        DrawTextEx(body_font, ping_str.c_str(), { static_cast<float>(SCREEN_WIDTH - 235), 37.0f }, 13, 1.0f, COLOR_GREEN_BRIGHT);

        if (!m_in_room) {
            // -- BROWSER MODE --
            UI::DrawChamferedPanel({ 30, 85, 520, 420 }, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            DrawTextEx(title_font, "OPEN SQUAD LOBBIES", { 50, 100 }, 14, 1.0f, COLOR_GOLD_BRIGHT);
            m_btn_refresh_lobbies.draw(title_font);

            DrawTextEx(body_font, "ROOM", { 50, 125 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, "MISSION / REALM", { 130, 125 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, "MODE", { 330, 125 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, "STATUS", { 440, 125 }, 11, 1.0f, COLOR_MUTED);
            DrawLine(45, 142, 535, 142, COLOR_SURFACE_HIGH);

            int y = 158;
            for (const auto& lob : m_lobbies) {
                Rectangle row_rec = { 45, static_cast<float>(y - 4), 490, 34 };
                UI::DrawChamferedPanel(row_rec, COLOR_SURFACE_MID, COLOR_SURFACE_MID, 3.0f);

                DrawTextEx(title_font, lob.code.c_str(), { 50, static_cast<float>(y + 4) }, 13, 1.0f, COLOR_GOLD_BRIGHT);
                DrawTextEx(body_font, lob.name.c_str(), { 130, static_cast<float>(y + 4) }, 12, 1.0f, COLOR_PARCHMENT);
                DrawTextEx(body_font, lob.slots.c_str(), { 330, static_cast<float>(y + 4) }, 12, 1.0f, COLOR_CYAN_BRIGHT);
                DrawTextEx(body_font, lob.status.c_str(), { 440, static_cast<float>(y + 4) }, 12, 1.0f, COLOR_GREEN_BRIGHT);
                y += 42;
            }

            // Cloud Status at bottom of browser panel
            DrawTextEx(body_font, m_cloud_status.c_str(), { 50, 480 }, 11, 1.0f, COLOR_MUTED);

            // Right Actions
            UI::DrawChamferedPanel({ 560, 85, 310, 420 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
            DrawTextEx(title_font, "SQUAD DEPLOYMENT", { 580, 92 }, 12, 1.0f, COLOR_MUTED);

            m_btn_quick.draw(title_font);
            m_btn_create_cloud.draw(title_font);
            m_btn_create.draw(title_font);

            // IP Entry box
            DrawTextEx(body_font, "TARGET LAN HOST IP & PORT:", { 580, 222 }, 11, 1.0f, COLOR_PARCHMENT);
            Rectangle ip_rec = { 580, 240, 260, 32 };
            DrawRectangleRec(ip_rec, m_ip_focused ? COLOR_SURFACE_HIGH : COLOR_SURFACE_MID);
            DrawRectangleLinesEx(ip_rec, 1.5f, m_ip_focused ? COLOR_CYAN_BRIGHT : COLOR_SURFACE_HIGH);
            DrawTextEx(body_font, m_target_ip.c_str(), { 590, 233 }, 14, 1.0f, WHITE);
            if (m_ip_focused && (static_cast<int>(GetTime() * 2) % 2 == 0)) {
                Vector2 txt_sz = MeasureTextEx(body_font, m_target_ip.c_str(), 14, 1.0f);
                DrawLine(590 + static_cast<int>(txt_sz.x) + 2, 229, 590 + static_cast<int>(txt_sz.x) + 2, 251, COLOR_CYAN_BRIGHT);
            }

            m_btn_join_lan.draw(title_font);
            m_btn_duel.draw(title_font);

            DrawTextEx(body_font, "ACTIVE SQUAD NETCODE:", { 580, 355 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, "- Winsock2 Non-blocking UDP (Port 7704)", { 580, 375 }, 11, 1.0f, COLOR_CYAN_BRIGHT);
            DrawTextEx(body_font, "- 30Hz Server Snapshots + 60Hz Inputs", { 580, 395 }, 11, 1.0f, COLOR_PARCHMENT);
            DrawTextEx(body_font, "- 15s Reconnect Window + AI Takeover", { 580, 415 }, 11, 1.0f, COLOR_GOLD_BRIGHT);
            DrawTextEx(body_font, "- Downed Beacon [Hold E to Revive]", { 580, 435 }, 11, 1.0f, COLOR_GREEN_BRIGHT);

        } else {
            // -- SQUAD ROOM VIEW --
            UI::DrawChamferedPanel({ 30, 85, 520, 420 }, COLOR_GOLD_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            std::string code_header = "VIMANA SQUAD // ROOM: " + NetworkManager::instance().room_code();
            if (NetworkManager::instance().role() == NetworkRole::HOST) code_header += " [HOST - PORT 7704]";
            else code_header += " [CLIENT - " + NetworkManager::instance().target_host_ip() + "]";

            DrawTextEx(title_font, code_header.c_str(), { 50, 98 }, 15, 1.0f, COLOR_GOLD_BRIGHT);

            const auto& players = NetworkManager::instance().players();

            for (int i = 0; i < 4; ++i) {
                float slot_y = 130.0f + i * 86.0f;
                Rectangle slot_box = { 45, slot_y, 490, 78 };
                bool filled = (i < static_cast<int>(players.size()));

                Color slot_border = filled ? COLOR_GOLD : COLOR_SURFACE_HIGH;
                Color slot_bg = filled ? COLOR_SURFACE_MID : COLOR_SURFACE_LOW;
                UI::DrawChamferedPanel(slot_box, slot_border, slot_bg, 4.0f);

                if (filled) {
                    // Ship Sprite Preview
                    std::string sid = players[i].ship_id;
                    if (sid.empty()) sid = "garuda";
                    std::string tex_key = sid + ".png";
                    Texture2D tex = AssetManager::instance().get_texture(tex_key);
                    if (tex.id == 0) tex = AssetManager::instance().get_texture(sid);
                    if (tex.id == 0) tex = AssetManager::instance().get_texture("pushpaka.png");

                    if (tex.id > 0) {
                        Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
                        Rectangle dst = { 55, slot_y + 12, 54, 54 };
                        DrawRectangleRec({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, COLOR_SURFACE_LOW);
                        DrawRectangleLinesEx({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, 1.0f, COLOR_GOLD);
                        DrawTexturePro(tex, src, dst, { 0, 0 }, 0.0f, WHITE);
                    }

                    // Pilot info
                    DrawTextEx(body_font, ("PILOT SLOT 0" + std::to_string(i + 1)).c_str(), { 120, slot_y + 8 }, 10, 1.0f, COLOR_MUTED);

                    std::string p_name = (i == 0) ? DBSystem::instance().player_name() + " [HOST]" : "SQUAD PILOT 0" + std::to_string(i + 1);
                    DrawTextEx(title_font, p_name.c_str(), { 120, slot_y + 22 }, 15, 1.0f, COLOR_GOLD_BRIGHT);

                    std::string vessel_str = "VESSEL: " + std::string(players[i].ship_id);
                    DrawTextEx(body_font, vessel_str.c_str(), { 120, slot_y + 44 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

                    const char* role_badge = (i == 0) ? "ROLE: MOBILITY (DPS)" :
                                             (i == 1) ? "ROLE: TANK (FRONT)" :
                                             (i == 2) ? "ROLE: HEAVY DPS" : "ROLE: SUPPORT (HEAL)";
                    DrawTextEx(body_font, role_badge, { 120, slot_y + 58 }, 10, 1.0f, COLOR_PARCHMENT);

                    // Ready Badge
                    Rectangle ready_bg = { 375, slot_y + 24, 95, 28 };
                    DrawRectangleRec(ready_bg, ColorAlpha(COLOR_GREEN_BRIGHT, 0.2f));
                    DrawRectangleLinesEx(ready_bg, 1.0f, COLOR_GREEN_BRIGHT);
                    DrawTextEx(body_font, "[ READY ]", { 390, slot_y + 30 }, 12, 1.0f, COLOR_GREEN_BRIGHT);
                } else {
                    DrawTextEx(body_font, ("PILOT SLOT 0" + std::to_string(i + 1) + " // VACANT").c_str(), { 60, slot_y + 16 }, 11, 1.0f, COLOR_MUTED);
                    DrawTextEx(body_font, "AWAITING SQUAD PILOT OR AI BOT", { 60, slot_y + 36 }, 12, 1.0f, COLOR_SURFACE_HIGH);
                }
            }

            // Right Panel Room Controls
            UI::DrawChamferedPanel({ 560, 85, 310, 420 }, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 6.0f);
            DrawTextEx(title_font, "SQUAD BRIEFING & LAUNCH", { 580, 100 }, 13, 1.0f, COLOR_MUTED);

            DrawTextEx(body_font, "MISSION: MAHAYUDDHA CO-OP", { 580, 130 }, 13, 1.0f, COLOR_GOLD_BRIGHT);
            DrawTextEx(body_font, "DIFFICULTY: KSHATRIYA", { 580, 155 }, 12, 1.0f, COLOR_RED_BRIGHT);
            DrawTextEx(body_font, "OBJECTIVE: SURVIVE & SLAY BOSS", { 580, 180 }, 11, 1.0f, COLOR_PARCHMENT);
            DrawTextEx(body_font, "CO-OP ASTRA: DUAL SYNERGY", { 580, 205 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

            DrawLine(580, 235, 850, 235, COLOR_SURFACE_HIGH);

            m_btn_add_ai.draw(title_font);
            m_btn_ready.draw(title_font);
            m_btn_start.draw(title_font);
        }

        m_btn_back.draw(title_font);
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
    std::string m_cloud_status;
    std::vector<LobbyEntry> m_lobbies;

    UI::Button m_btn_quick;
    UI::Button m_btn_create_cloud;
    UI::Button m_btn_create;
    UI::Button m_btn_join_lan;
    UI::Button m_btn_duel;
    UI::Button m_btn_refresh_lobbies;
    UI::Button m_btn_ready;
    UI::Button m_btn_start;
    UI::Button m_btn_add_ai;
    UI::Button m_btn_back;
};

} // namespace Vimana
