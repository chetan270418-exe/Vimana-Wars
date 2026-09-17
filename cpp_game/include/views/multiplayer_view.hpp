#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/http_client.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class MultiplayerView : public IView {
public:
    MultiplayerView() : m_next_view(ViewType::MULTIPLAYER_LOBBY) {
        init();
    }

    void init() override {
        m_next_view = ViewType::MULTIPLAYER_LOBBY;

        m_btn_create = UI::Button({ 600, 140, 240, 38 }, "CREATE SANGHA WING", COLOR_GOLD_BRIGHT);
        m_btn_duel = UI::Button({ 600, 200, 240, 38 }, "LAUNCH 1V1 DUEL", COLOR_CYAN_BRIGHT);
        m_btn_refresh = UI::Button({ 600, 260, 240, 38 }, "SCAN NETWORK", COLOR_GOLD);
        m_btn_back = UI::Button({ 40, 520, 110, 36 }, "BACK", COLOR_MUTED);

        m_lobbies = {
            { "VMN-8821", "Swarga Wing (Co-op)", "2/2", "IN BATTLE" },
            { "VMN-4192", "Dandaka Squad", "1/2", "STANDBY" },
            { "VMN-1055", "Lanka Assault", "1/2", "READY" }
        };
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }

        if (m_btn_duel.update(mouse_pos)) {
            m_next_view = ViewType::DUEL;
        }

        if (m_btn_create.update(mouse_pos)) {
            m_lobbies.push_back({ "VMN-" + std::to_string(1000 + std::rand() % 8999), "New Wing (You)", "1/2", "HOSTING" });
        }

        if (m_btn_refresh.update(mouse_pos)) {
            // Can query backend /api/multiplayer/lobbies via HTTPClient
            HTTPClient::instance().get("127.0.0.1", 5000, "/api/multiplayer/lobbies");
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        // Header
        UI::DrawChamferedPanel({ 30, 20, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(font, "SANGHA NETWORK // MULTIPLAYER LOBBY BROWSER", { 45, 30 }, 22, 1.0f, COLOR_GOLD_BRIGHT);

        // Left: Active Lobbies
        UI::DrawChamferedPanel({ 30, 90, 530, 400 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawText("ACTIVE SANGHA WINGS", 50, 105, 12, COLOR_MUTED);

        DrawText("WING CODE", 50, 130, 11, COLOR_MUTED);
        DrawText("NAME / MISSION", 150, 130, 11, COLOR_MUTED);
        DrawText("SLOTS", 340, 130, 11, COLOR_MUTED);
        DrawText("STATUS", 420, 130, 11, COLOR_MUTED);
        DrawLine(45, 148, 545, 148, COLOR_MUTED);

        int y = 165;
        for (const auto& lob : m_lobbies) {
            DrawText(lob.code.c_str(), 50, y, 13, COLOR_GOLD_BRIGHT);
            DrawText(lob.name.c_str(), 150, y, 13, COLOR_PARCHMENT);
            DrawText(lob.slots.c_str(), 340, y, 13, COLOR_CYAN_BRIGHT);
            DrawText(lob.status.c_str(), 420, y, 13, (lob.status == "READY") ? COLOR_GREEN_BRIGHT : COLOR_ORANGE_BRIGHT);
            y += 35;
        }

        // Right: Actions
        UI::DrawChamferedPanel({ 580, 90, 290, 400 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawText("NETWORK OPERATIONS", 600, 105, 12, COLOR_MUTED);

        m_btn_create.draw(font);
        m_btn_duel.draw(font);
        m_btn_refresh.draw(font);
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
    std::vector<LobbyEntry> m_lobbies;
    UI::Button m_btn_create;
    UI::Button m_btn_duel;
    UI::Button m_btn_refresh;
    UI::Button m_btn_back;
};

} // namespace Vimana
