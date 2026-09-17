#pragma once
#include <iostream>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "systems/currency_system.hpp"

namespace Vimana {

class DebugOverlay {
public:
    static DebugOverlay& instance() {
        static DebugOverlay dbg;
        return dbg;
    }

    bool show_hitboxes = false;
    bool god_mode = false;
    bool show_fps_graph = false;
    bool skip_wave_requested = false;
    bool boss_jump_requested = false;

    void update() {
        // F1: Toggle Hitboxes
        if (IsKeyPressed(KEY_F1)) {
            show_hitboxes = !show_hitboxes;
            std::cout << "[DEBUG] Hitboxes: " << (show_hitboxes ? "ON" : "OFF") << std::endl;
        }

        // F2: Skip to Next Wave
        if (IsKeyPressed(KEY_F2)) {
            skip_wave_requested = true;
            std::cout << "[DEBUG] Skip Wave Triggered" << std::endl;
        }

        // F3: Add 1000 Prana Shards
        if (IsKeyPressed(KEY_F3)) {
            CurrencySystem::instance().add_prana_shards(1000);
            std::cout << "[DEBUG] Added 1000 Prana Shards" << std::endl;
        }

        // F4: God Mode
        if (IsKeyPressed(KEY_F4)) {
            god_mode = !god_mode;
            std::cout << "[DEBUG] God Mode: " << (god_mode ? "ENABLED" : "DISABLED") << std::endl;
        }

        // F5: Jump to Boss Wave
        if (IsKeyPressed(KEY_F5)) {
            boss_jump_requested = true;
            std::cout << "[DEBUG] Jump to Boss Wave Triggered" << std::endl;
        }

        // F7: Toggle FPS Overlay
        if (IsKeyPressed(KEY_F7)) {
            show_fps_graph = !show_fps_graph;
        }

        // F8: Toggle Network Debug Telemetry Overlay
        if (IsKeyPressed(KEY_F8)) {
            show_net_overlay = !show_net_overlay;
        }
    }

    bool show_net_overlay = false;

    void draw() const {
        if (show_fps_graph || god_mode) {
            DrawRectangle(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 65, 170, 55, { 0, 0, 0, 180 });
            DrawRectangleLines(SCREEN_WIDTH - 180, SCREEN_HEIGHT - 65, 170, 55, COLOR_MUTED);

            std::string fps_text = "FPS: " + std::to_string(GetFPS());
            DrawText(fps_text.c_str(), SCREEN_WIDTH - 170, SCREEN_HEIGHT - 55, 12, COLOR_GREEN_BRIGHT);

            if (god_mode) {
                DrawText("★ GOD MODE ACTIVE", SCREEN_WIDTH - 170, SCREEN_HEIGHT - 35, 11, COLOR_GOLD_BRIGHT);
            }
        }

        if (show_net_overlay) {
            // Draw real-time network debug box
            Rectangle net_rec = { 15, 15, 270, 120 };
            DrawRectangleRec(net_rec, { 10, 15, 25, 230 });
            DrawRectangleLinesEx(net_rec, 1.5f, COLOR_CYAN_BRIGHT);

            DrawText("NET TELEMETRY // F8 TO HIDE", 25, 22, 10, COLOR_GOLD_BRIGHT);
            DrawText(("ROLE: " + std::string(NetworkManager::instance().role() == NetworkRole::HOST ? "HOST (PORT 7704)" : NetworkManager::instance().role() == NetworkRole::CLIENT ? "CLIENT" : "OFFLINE")).c_str(), 25, 40, 11, COLOR_CYAN_BRIGHT);
            DrawText(("RTT PING: " + std::to_string(NetworkManager::instance().ping_ms()) + " ms").c_str(), 25, 58, 11, COLOR_GREEN_BRIGHT);
            DrawText(("TICK: " + std::to_string(NetworkManager::instance().tick()) + " | SEQ: " + std::to_string(NetworkManager::instance().sequence())).c_str(), 25, 76, 11, COLOR_PARCHMENT);
            DrawText(("PEERS: " + std::to_string(NetworkManager::instance().peers().size()) + " | LOSS: 0.0%").c_str(), 25, 94, 11, COLOR_GOLD);
            DrawText(("ROOM: " + NetworkManager::instance().room_code()).c_str(), 25, 112, 10, COLOR_MUTED);
        }
    }

private:
    DebugOverlay() = default;
};

} // namespace Vimana
