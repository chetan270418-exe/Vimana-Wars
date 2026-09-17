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
    }

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
    }

private:
    DebugOverlay() = default;
};

} // namespace Vimana
