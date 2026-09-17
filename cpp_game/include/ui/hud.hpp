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
        const Player& player,
        int wave,
        const RealmData& realm,
        const Boss* boss,
        const std::vector<Enemy>& enemies,
        Font font
    ) {
        // ── Top Header Panel ────────────────────────────────────────────────
        DrawChamferedPanel({ 15, 12, 870, 48 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        // Score & Realm info
        std::string score_str = "SCORE: " + std::to_string(player.score);
        DrawTextEx(font, score_str.c_str(), { 30, 24 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        std::string realm_str = std::string(realm.name) + " // WAVE " + std::to_string(wave);
        Vector2 realm_sz = MeasureTextEx(font, realm_str.c_str(), 18, 1.0f);
        DrawTextEx(font, realm_str.c_str(), { (SCREEN_WIDTH - realm_sz.x) / 2.0f, 26 }, 18, 1.0f, realm.accent_color);

        // Combo Multiplier
        if (player.combo > 1) {
            std::string combo_str = "x" + std::to_string(player.combo) + " COMBO";
            DrawTextEx(font, combo_str.c_str(), { SCREEN_WIDTH - 160, 24 }, 20, 1.0f, COLOR_ORANGE_BRIGHT);
        }

        // ── Bottom Cockpit Instruments ──────────────────────────────────────
        DrawChamferedPanel({ 15, SCREEN_HEIGHT - 65, 870, 52 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);

        // 1. Health Bar
        float hp_ratio = std::clamp(static_cast<float>(player.hp) / player.max_hp, 0.0f, 1.0f);
        Color hp_col = (hp_ratio > 0.5f) ? COLOR_GREEN_BRIGHT : (hp_ratio > 0.25f ? COLOR_GOLD : COLOR_RED_BRIGHT);

        DrawText("HULL INTEGRITY", 30, SCREEN_HEIGHT - 58, 10, COLOR_MUTED);
        DrawRectangle(30, SCREEN_HEIGHT - 44, 180, 18, { 25, 30, 45, 255 });
        DrawRectangle(30, SCREEN_HEIGHT - 44, static_cast<int>(180 * hp_ratio), 18, hp_col);
        DrawRectangleLines(30, SCREEN_HEIGHT - 44, 180, 18, COLOR_GOLD);

        std::string hp_text = std::to_string(player.hp) + "/" + std::to_string(player.max_hp);
        DrawText(hp_text.c_str(), 95, SCREEN_HEIGHT - 41, 12, COLOR_OBSIDIAN);

        // 2. Dash Charges
        DrawText("VAYU DASH", 235, SCREEN_HEIGHT - 58, 10, COLOR_MUTED);
        for (int i = 0; i < player.max_dash_charges; ++i) {
            Color dash_col = (i < player.dash_charges) ? COLOR_CYAN_BRIGHT : COLOR_MUTED;
            DrawRectangle(235 + i * 28, SCREEN_HEIGHT - 44, 22, 18, dash_col);
            DrawRectangleLines(235 + i * 28, SCREEN_HEIGHT - 44, 22, 18, COLOR_PARCHMENT);
        }

        // 3. Sudarshana Chakram Cooldown
        DrawText("CHAKRAM [Q/E]", 335, SCREEN_HEIGHT - 58, 10, COLOR_MUTED);
        float chakram_ratio = 1.0f - std::clamp(player.chakram_timer / player.chakram_cooldown, 0.0f, 1.0f);
        DrawRectangle(335, SCREEN_HEIGHT - 44, 110, 18, { 25, 30, 45, 255 });
        DrawRectangle(335, SCREEN_HEIGHT - 44, static_cast<int>(110 * chakram_ratio), 18, (chakram_ratio >= 1.0f) ? COLOR_GOLD_BRIGHT : COLOR_MUTED);
        DrawRectangleLines(335, SCREEN_HEIGHT - 44, 110, 18, COLOR_GOLD);
        DrawText((chakram_ratio >= 1.0f) ? "READY" : "CHARGING", 365, SCREEN_HEIGHT - 41, 11, COLOR_OBSIDIAN);

        // 4. Brahmastra Bomb
        DrawText("BRAHMASTRA [F]", 470, SCREEN_HEIGHT - 58, 10, COLOR_MUTED);
        std::string bomb_str = "x" + std::to_string(player.brahmastra_bombs);
        DrawText(bomb_str.c_str(), 500, SCREEN_HEIGHT - 44, 18, COLOR_GOLD_BRIGHT);

        // 5. Consumables (Soma Vial 'C', Vajra Flare 'V', Kavach Shield 'S')
        DrawText("CONSUMABLES", 580, SCREEN_HEIGHT - 58, 10, COLOR_MUTED);

        // Soma [C]
        std::string soma_str = "[C] SOMA: " + std::to_string(player.inventory.soma_vials);
        DrawText(soma_str.c_str(), 580, SCREEN_HEIGHT - 43, 12, (player.inventory.soma_vials > 0) ? COLOR_GREEN_BRIGHT : COLOR_MUTED);

        // Vajra [V]
        std::string vajra_str = "[V] FLARE: " + std::to_string(player.inventory.vajra_flares);
        DrawText(vajra_str.c_str(), 685, SCREEN_HEIGHT - 43, 12, (player.inventory.vajra_flares > 0) ? COLOR_CYAN_BRIGHT : COLOR_MUTED);

        // Kavach [S]
        std::string kavach_str = "KAVACH: " + std::to_string(player.inventory.kavach_charges);
        DrawText(kavach_str.c_str(), 790, SCREEN_HEIGHT - 43, 12, (player.inventory.kavach_charges > 0) ? COLOR_GOLD_BRIGHT : COLOR_MUTED);

        // ── Boss Health Bar ─────────────────────────────────────────────────
        if (boss && boss->active) {
            float boss_hp_ratio = std::clamp(static_cast<float>(boss->hp) / boss->max_hp, 0.0f, 1.0f);
            DrawChamferedPanel({ 180, 68, 540, 36 }, COLOR_RED_BRIGHT, COLOR_SURFACE_LOW, 4.0f);

            DrawText(boss->name.c_str(), 200, 74, 12, COLOR_RED_BRIGHT);
            DrawText(boss->attack_name.c_str(), 450, 74, 11, COLOR_GOLD);

            DrawRectangle(200, 88, 500, 10, { 40, 20, 20, 255 });
            DrawRectangle(200, 88, static_cast<int>(500 * boss_hp_ratio), 10, COLOR_RED_BRIGHT);
            DrawRectangleLines(200, 88, 500, 10, COLOR_GOLD_BRIGHT);
        }

        // ── Off-screen Threat Radar Arrows ──────────────────────────────────
        for (const auto& enemy : enemies) {
            if (!enemy.active) continue;
            // Draw directional pointer if enemy is off-screen or near screen edge
            if (enemy.pos.x < 30 || enemy.pos.x > SCREEN_WIDTH - 30 || enemy.pos.y < 70 || enemy.pos.y > SCREEN_HEIGHT - 70) {
                float cx = std::clamp(enemy.pos.x, 35.0f, SCREEN_WIDTH - 35.0f);
                float cy = std::clamp(enemy.pos.y, 75.0f, SCREEN_HEIGHT - 75.0f);
                DrawCircle(static_cast<int>(cx), static_cast<int>(cy), 5, COLOR_RED_BRIGHT);
            }
        }
    }
};

} // namespace Vimana::UI
