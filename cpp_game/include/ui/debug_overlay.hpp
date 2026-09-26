#pragma once
#include <algorithm>
#include <array>
#include <iostream>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "systems/currency_system.hpp"

namespace Vimana {

class DebugOverlay {
public:
    struct FrameSample { float frame_ms = 0.0f; float update_ms = 0.0f; float render_ms = 0.0f; };
    static constexpr int PROFILE_SAMPLE_COUNT = 120;

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
        // F1: Toggle Hitboxes (always safe)
        if (IsKeyPressed(KEY_F1)) {
            show_hitboxes = !show_hitboxes;
            std::cout << "[DEBUG] Hitboxes: " << (show_hitboxes ? "ON" : "OFF") << std::endl;
        }

#if defined(_DEBUG) || defined(VIMANA_DEBUG)
        // F2: Skip to Next Wave - DEBUG BUILD ONLY
        if (IsKeyPressed(KEY_F2)) {
            skip_wave_requested = true;
            std::cout << "[DEBUG] Skip Wave Triggered" << std::endl;
        }

        // F3: Add 1000 Prana Shards - DEBUG BUILD ONLY
        if (IsKeyPressed(KEY_F3)) {
            CurrencySystem::instance().add_prana_shards(1000);
            std::cout << "[DEBUG] Added 1000 Prana Shards" << std::endl;
        }

        // F4: God Mode - DEBUG BUILD ONLY
        if (IsKeyPressed(KEY_F4)) {
            god_mode = !god_mode;
            std::cout << "[DEBUG] God Mode: " << (god_mode ? "ENABLED" : "DISABLED") << std::endl;
        }

        // F5: Jump to Boss Wave - DEBUG BUILD ONLY
        if (IsKeyPressed(KEY_F5)) {
            boss_jump_requested = true;
            std::cout << "[DEBUG] Jump to Boss Wave Triggered" << std::endl;
        }
#endif

        // F7: Toggle FPS Overlay
        if (IsKeyPressed(KEY_F7)) {
            show_fps_graph = !show_fps_graph;
        }

        // F8: Toggle Network Debug Telemetry Overlay
        if (IsKeyPressed(KEY_F8)) {
            show_net_overlay = !show_net_overlay;
        }
    }

    void record_frame(float frame_ms, float update_ms, float render_ms) {
        m_frame_samples[m_frame_write] = {
            std::max(0.0f, frame_ms), std::max(0.0f, update_ms), std::max(0.0f, render_ms)
        };
        m_frame_write = (m_frame_write + 1) % PROFILE_SAMPLE_COUNT;
        m_frame_count = std::min(m_frame_count + 1, PROFILE_SAMPLE_COUNT);
    }

    int frame_sample_count() const { return m_frame_count; }
    const FrameSample& latest_frame_sample() const {
        static const FrameSample empty{};
        return m_frame_count > 0
            ? m_frame_samples[(m_frame_write + PROFILE_SAMPLE_COUNT - 1) % PROFILE_SAMPLE_COUNT]
            : empty;
    }

    bool show_net_overlay = false;

    void draw() const {
        if (show_fps_graph) {
            constexpr int panel_x = SCREEN_WIDTH - 270;
            constexpr int panel_y = SCREEN_HEIGHT - 183;
            DrawRectangle(panel_x, panel_y, 255, 173, { 0, 0, 0, 215 });
            DrawRectangleLines(panel_x, panel_y, 255, 173, COLOR_CYAN_BRIGHT);
            DrawText("FRAME PROFILE // F7 TO HIDE", panel_x + 10, panel_y + 8, 10, COLOR_GOLD_BRIGHT);

            float average_ms = 0.0f;
            float peak_ms = 0.0f;
            float average_update_ms = 0.0f;
            float average_render_ms = 0.0f;
            std::array<float, PROFILE_SAMPLE_COUNT> ordered_frames{};
            for (int i = 0; i < m_frame_count; ++i) {
                const FrameSample& sample = m_frame_samples[(m_frame_write + PROFILE_SAMPLE_COUNT - m_frame_count + i) % PROFILE_SAMPLE_COUNT];
                ordered_frames[i] = sample.frame_ms;
                average_ms += sample.frame_ms;
                peak_ms = std::max(peak_ms, sample.frame_ms);
                average_update_ms += sample.update_ms;
                average_render_ms += sample.render_ms;
            }
            if (m_frame_count > 0) {
                const float sample_count = static_cast<float>(m_frame_count);
                average_ms /= sample_count;
                average_update_ms /= sample_count;
                average_render_ms /= sample_count;
                std::sort(ordered_frames.begin(), ordered_frames.begin() + m_frame_count);
            }
            const FrameSample& latest = latest_frame_sample();
            const int p95_index = std::max(0, (m_frame_count * 95 + 99) / 100 - 1);

            DrawText(TextFormat("FPS %d // FRAME %.1f ms", GetFPS(), latest.frame_ms),
                     panel_x + 10, panel_y + 25, 10, COLOR_PARCHMENT);
            DrawText(TextFormat("AVG %.1f // P95 %.1f // PEAK %.1f ms", average_ms,
                                m_frame_count ? ordered_frames[p95_index] : 0.0f, peak_ms),
                     panel_x + 10, panel_y + 41, 9, COLOR_MUTED);
            DrawText(TextFormat("UPDATE %.2f ms // DRAW+PRESENT %.2f ms", latest.update_ms, latest.render_ms),
                     panel_x + 10, panel_y + 56, 9, COLOR_CYAN_BRIGHT);
            DrawText(TextFormat("ROLLING AVG // UPDATE %.2f  DRAW+PRESENT %.2f", average_update_ms, average_render_ms),
                     panel_x + 10, panel_y + 70, 8, COLOR_MUTED);

            const int graph_x = panel_x + 10;
            const int graph_y = panel_y + 88;
            constexpr int graph_width = 235;
            constexpr int graph_height = 72;
            DrawRectangle(graph_x, graph_y, graph_width, graph_height, { 10, 16, 26, 255 });
            DrawLine(graph_x, graph_y + graph_height - 1, graph_x + graph_width, graph_y + graph_height - 1, COLOR_MUTED);
            const float slot_width = static_cast<float>(graph_width) / PROFILE_SAMPLE_COUNT;
            for (int i = 0; i < m_frame_count; ++i) {
                const int sample_index = (m_frame_write + PROFILE_SAMPLE_COUNT - m_frame_count + i) % PROFILE_SAMPLE_COUNT;
                const float ms = m_frame_samples[sample_index].frame_ms;
                const float normalized = std::clamp(ms / 50.0f, 0.0f, 1.0f);
                const int height = std::max(1, static_cast<int>(normalized * (graph_height - 4)));
                const int x = graph_x + static_cast<int>((PROFILE_SAMPLE_COUNT - m_frame_count + i) * slot_width);
                const Color color = ms > 33.3f ? COLOR_RED_BRIGHT : ms > 20.0f ? COLOR_GOLD_BRIGHT : COLOR_CYAN_BRIGHT;
                DrawRectangle(x, graph_y + graph_height - height - 1,
                              std::max(1, static_cast<int>(slot_width)), height, color);
            }
            DrawText("50 ms", graph_x + graph_width - 33, graph_y + 2, 8, COLOR_MUTED);
        } else if (god_mode) {
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
    std::array<FrameSample, PROFILE_SAMPLE_COUNT> m_frame_samples{};
    int m_frame_write = 0;
    int m_frame_count = 0;

    DebugOverlay() = default;
};

} // namespace Vimana
