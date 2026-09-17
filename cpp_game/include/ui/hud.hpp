#pragma once
#include <string>
#include <vector>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "entities/player.hpp"
#include "entities/boss.hpp"
#include "entities/enemy.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana::UI {

class HUD {
public:
    static void draw(
        const std::vector<Player>& squad,
        int wave,
        const RealmData& realm,
        const Boss* boss,
        const std::vector<Enemy>& enemies,
        int team_combo,
        float transcendence_timer,
        Font title_font,
        Font body_font
    ) {
        if (squad.empty()) return;
        const Player& player = squad[0];

        // ── Top Header Panel ────────────────────────────────────────────────
        DrawYantraPanel({ 15, 12, 870, 48 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f, true);

        // Score & Realm info
        std::string score_str = "SCORE: " + std::to_string(player.score);
        DrawTextEx(title_font, score_str.c_str(), { 30, 24 }, 18, 1.0f, COLOR_GOLD_BRIGHT);

        std::string realm_str = std::string(realm.name) + " // WAVE " + std::to_string(wave);
        Vector2 realm_sz = MeasureTextEx(title_font, realm_str.c_str(), 18, 1.0f);
        DrawTextEx(title_font, realm_str.c_str(), { (SCREEN_WIDTH - realm_sz.x) / 2.0f, 24 }, 18, 1.0f, realm.accent_color);

        // Team Combo Multiplier (with animated pulse at milestones)
        int display_combo = team_combo > player.combo ? team_combo : player.combo;
        if (display_combo > 1) {
            float pulse = (display_combo >= 10) ? (0.8f + 0.2f * std::sin(GetTime() * 12.0f)) : 1.0f;
            Color combo_col = (display_combo >= 25) ? COLOR_GOLD_BRIGHT : ((display_combo >= 10) ? COLOR_ORANGE_BRIGHT : COLOR_CYAN_BRIGHT);
            std::string combo_str = "x" + std::to_string(display_combo) + " SQUAD COMBO";
            Vector2 c_sz = MeasureTextEx(title_font, combo_str.c_str(), 16 * pulse, 1.0f);
            DrawTextEx(title_font, combo_str.c_str(), { SCREEN_WIDTH - c_sz.x - 30, 25 }, 16 * pulse, 1.0f, combo_col);
        }

        // ── Co-op Squadron Widget (Top Right below header) ──────────────────
        if (squad.size() > 1) {
            float sx = SCREEN_WIDTH - 225.0f;
            float sy = 68.0f;
            for (size_t i = 1; i < squad.size(); ++i) {
                const auto& mate = squad[i];
                Rectangle mate_bar = { sx, sy, 210, 26 };
                Color border_col = mate.is_downed ? COLOR_RED_BRIGHT : COLOR_CYAN_BRIGHT;
                DrawChamferedPanel(mate_bar, border_col, COLOR_SURFACE_MID, 3.0f);

                DrawText(mate.callsign.c_str(), static_cast<int>(sx + 8), static_cast<int>(sy + 6), 9, COLOR_PARCHMENT);
                if (mate.is_downed) {
                    float flash = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
                    Color d_col = ColorAlpha(COLOR_RED_BRIGHT, 0.7f + 0.3f * flash);
                    std::string down_str = "[DOWNED " + std::to_string(static_cast<int>(mate.downed_timer)) + "s]";
                    DrawText(down_str.c_str(), static_cast<int>(sx + 115), static_cast<int>(sy + 6), 9, d_col);
                } else {
                    float hp_pct = std::clamp(static_cast<float>(mate.hp) / mate.max_hp, 0.0f, 1.0f);
                    Rectangle hp_f = { sx + 105, sy + 7, 95 * hp_pct, 12 };
                    Color bar_col = hp_pct > 0.3f ? COLOR_GREEN_BRIGHT : COLOR_RED_BRIGHT;
                    DrawRectangleRec(hp_f, bar_col);
                    DrawRectangleLinesEx({ sx + 105, sy + 7, 95, 12 }, 1.0f, COLOR_SURFACE_HIGH);
                }
                sy += 30.0f;
            }
        }

        // ── Boss Health Bar with Phase Tick Marks ───────────────────────────
        if (boss && boss->active) {
            float boss_hp_ratio = std::clamp(static_cast<float>(boss->hp) / boss->max_hp, 0.0f, 1.0f);
            Rectangle boss_panel = { 180, 68, 540, 38 };
            DrawYantraPanel(boss_panel, boss->theme_color, COLOR_SURFACE_LOW, 4.0f, true);

            DrawTextEx(title_font, boss->name.c_str(), { 200, 72 }, 13, 1.0f, boss->theme_color);
            DrawText(boss->attack_name.c_str(), 450, 73, 10, COLOR_GOLD);

            // Health bar container
            Rectangle bar_rec = { 200, 89, 500, 11 };
            DrawRectangleRec(bar_rec, { 40, 15, 20, 255 });
            DrawRectangle(static_cast<int>(bar_rec.x), static_cast<int>(bar_rec.y), static_cast<int>(bar_rec.width * boss_hp_ratio), static_cast<int>(bar_rec.height), boss->theme_color);
            DrawRectangleLinesEx(bar_rec, 1.0f, COLOR_GOLD_BRIGHT);

            // Phase division notches at 50% and 20%
            DrawLineEx({ bar_rec.x + bar_rec.width * 0.50f, bar_rec.y - 2 }, { bar_rec.x + bar_rec.width * 0.50f, bar_rec.y + bar_rec.height + 2 }, 2.0f, COLOR_GOLD);
            DrawLineEx({ bar_rec.x + bar_rec.width * 0.20f, bar_rec.y - 2 }, { bar_rec.x + bar_rec.width * 0.20f, bar_rec.y + bar_rec.height + 2 }, 2.0f, COLOR_RED_BRIGHT);
        }

        // ── Bottom Cockpit Instruments ──────────────────────────────────────
        DrawYantraPanel({ 15, SCREEN_HEIGHT - 65, 870, 52 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f, true);

        // 1. Health Bar
        float hp_ratio = std::clamp(static_cast<float>(player.hp) / player.max_hp, 0.0f, 1.0f);
        Color hp_col = (hp_ratio > 0.5f) ? COLOR_GREEN_BRIGHT : (hp_ratio > 0.25f ? COLOR_GOLD : COLOR_RED_BRIGHT);

        DrawText("HULL INTEGRITY", 30, SCREEN_HEIGHT - 58, 9, COLOR_MUTED);
        DrawRectangle(30, SCREEN_HEIGHT - 44, 180, 18, { 25, 30, 45, 255 });
        DrawRectangle(30, SCREEN_HEIGHT - 44, static_cast<int>(180 * hp_ratio), 18, hp_col);
        DrawRectangleLines(30, SCREEN_HEIGHT - 44, 180, 18, COLOR_GOLD);

        std::string hp_text = std::to_string(player.hp) + "/" + std::to_string(player.max_hp);
        DrawText(hp_text.c_str(), 95, SCREEN_HEIGHT - 41, 11, COLOR_OBSIDIAN);

        // 2. Dash Charges (Pip Meter)
        DrawText("VAYU DASH", 230, SCREEN_HEIGHT - 58, 9, COLOR_MUTED);
        UI::DrawPipMeter({ 230, SCREEN_HEIGHT - 44 }, player.dash_charges, player.max_dash_charges, COLOR_CYAN_BRIGHT, COLOR_SURFACE_HIGH, 22.0f, 18.0f, 6.0f);

        // 3. Sudarshana Chakram Cooldown Dial
        DrawText("CHAKRAM [Q/E]", 335, SCREEN_HEIGHT - 58, 9, COLOR_MUTED);
        float chakram_ratio = 1.0f - std::clamp(player.chakram_timer / player.chakram_cooldown, 0.0f, 1.0f);
        DrawRectangle(335, SCREEN_HEIGHT - 44, 105, 18, { 25, 30, 45, 255 });
        DrawRectangle(335, SCREEN_HEIGHT - 44, static_cast<int>(105 * chakram_ratio), 18, (chakram_ratio >= 1.0f) ? COLOR_GOLD_BRIGHT : COLOR_SURFACE_HIGH);
        DrawRectangleLines(335, SCREEN_HEIGHT - 44, 105, 18, COLOR_GOLD);
        DrawText((chakram_ratio >= 1.0f) ? "READY" : "CHARGING", 360, SCREEN_HEIGHT - 41, 10, COLOR_OBSIDIAN);

        // 4. Brahmastra Bomb
        DrawText("BRAHMASTRA [F]", 460, SCREEN_HEIGHT - 58, 9, COLOR_MUTED);
        std::string bomb_str = "x" + std::to_string(player.brahmastra_bombs);
        DrawTextEx(title_font, bomb_str.c_str(), { 490, SCREEN_HEIGHT - 44 }, 16, 1.0f, COLOR_GOLD_BRIGHT);

        // 5. Consumables (Soma Vial 'C', Vajra Flare 'V', Kavach Shield 'S')
        DrawText("TACTICAL CONSUMABLES", 575, SCREEN_HEIGHT - 58, 9, COLOR_MUTED);

        // Soma [C]
        std::string soma_str = "[C] SOMA: " + std::to_string(player.inventory.soma_vials);
        DrawText(soma_str.c_str(), 575, SCREEN_HEIGHT - 43, 11, (player.inventory.soma_vials > 0) ? COLOR_GREEN_BRIGHT : COLOR_MUTED);

        // Vajra [V]
        std::string vajra_str = "[V] FLARE: " + std::to_string(player.inventory.vajra_flares);
        DrawText(vajra_str.c_str(), 680, SCREEN_HEIGHT - 43, 11, (player.inventory.vajra_flares > 0) ? COLOR_CYAN_BRIGHT : COLOR_MUTED);

        // Kavach [S]
        std::string kavach_str = "KAVACH: " + std::to_string(player.inventory.kavach_charges);
        DrawText(kavach_str.c_str(), 785, SCREEN_HEIGHT - 43, 11, (player.inventory.kavach_charges > 0) ? COLOR_GOLD_BRIGHT : COLOR_MUTED);

        // ── Off-screen Threat Radar Arrows ──────────────────────────────────
        for (const auto& enemy : enemies) {
            if (!enemy.active) continue;
            if (enemy.pos.x < 30 || enemy.pos.x > SCREEN_WIDTH - 30 || enemy.pos.y < 70 || enemy.pos.y > SCREEN_HEIGHT - 70) {
                float cx = std::clamp(enemy.pos.x, 35.0f, SCREEN_WIDTH - 35.0f);
                float cy = std::clamp(enemy.pos.y, 75.0f, SCREEN_HEIGHT - 75.0f);
                DrawCircle(static_cast<int>(cx), static_cast<int>(cy), 5, COLOR_RED_BRIGHT);
                DrawCircleLines(static_cast<int>(cx), static_cast<int>(cy), 8, COLOR_GOLD);
            }
        }
    }
};

} // namespace Vimana::UI
