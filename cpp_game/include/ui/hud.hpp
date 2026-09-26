#pragma once
#include <algorithm>
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
        Font body_font,
        CoopRule coop_rule = CoopRule::REVIVE_MODE,
        Difficulty difficulty = Difficulty::KSHATRIYA,
        bool sensors_jammed = false
    ) {
        if (squad.empty()) return;
        const Player& player = squad[0];

        // ── Top header: ship, mission, score, combo, contacts, and mode ──
        DrawYantraPanel({ 15, 12, 870, 36 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f, true);

        int display_combo = team_combo > player.combo ? team_combo : player.combo;
        const std::string mission_line = "ACT " + std::to_string(CampaignActForWave(wave)) +
            "  //  WAVE " + std::to_string(CampaignWaveWithinAct(wave)) + "/" +
            std::to_string(WAVES_PER_ACT);
        DrawTextEx(title_font, mission_line.c_str(), { 30, 22 }, 12, 1.0f, COLOR_GOLD_BRIGHT);

        const std::string score_line = "SCORE " + std::to_string(player.score);
        DrawTextEx(body_font, score_line.c_str(), { 194, 24 }, 9, 1.0f, COLOR_PARCHMENT);
        if (display_combo > 1) {
            const Vector2 score_size = MeasureTextEx(body_font, score_line.c_str(), 9, 1.0f);
            const float pulse = 1.0f + 0.08f * std::sin(GetTime() * 8.0);
            const float combo_size = 11.0f * pulse;
            const Color combo_color = display_combo >= 25 ? COLOR_RED_BRIGHT :
                                     display_combo >= 10 ? COLOR_GOLD_BRIGHT : COLOR_CYAN_BRIGHT;
            const std::string combo_text = "x" + std::to_string(display_combo);
            DrawTextEx(title_font, combo_text.c_str(),
                       { 194.0f + score_size.x + 10.0f, 23.0f - (combo_size - 11.0f) * 0.5f },
                       combo_size, 1.0f, combo_color);
        }

        int active_contacts = 0;
        for (const auto& enemy : enemies) active_contacts += enemy.active ? 1 : 0;
        if (boss && boss->active) ++active_contacts;
        const std::string contacts = sensors_jammed
            ? "SENSOR JAM // CONTACTS LOST"
            : "CONTACTS " + std::to_string(active_contacts);
        DrawTextEx(body_font, contacts.c_str(), { 425, 24 }, 9, 1.0f,
                   sensors_jammed || active_contacts >= 10 ? COLOR_RED_BRIGHT : COLOR_CYAN_BRIGHT);

        // Ship name + gun type
        if (player.archetype) {
            std::string ship_label = player.archetype->name;
            if (!player.archetype->gun_type.empty() && player.archetype->gun_type != "STANDARD") {
                ship_label += " [" + player.archetype->gun_type + "]";
            }
            DrawTextEx(body_font, ship_label.c_str(), { 30, 9 }, 9, 1.0f, player.archetype->accent_color);
        }

        const char* difficulty_name = "NORMAL";
        switch (difficulty) {
            case Difficulty::NOVICE: difficulty_name = "EASY"; break;
            case Difficulty::ASURA_SLAYER: difficulty_name = "HARD"; break;
            case Difficulty::CHAKRAVYUHA: difficulty_name = "CHAKRAVYUHA"; break;
            case Difficulty::KSHATRIYA: default: break;
        }
        const std::string mode_label = (squad.size() > 1
            ? "CO-OP " + std::to_string(squad.size()) + "P"
            : "SOLO") + "  //  " + difficulty_name;
        const Vector2 mode_size = MeasureTextEx(body_font, mode_label.c_str(), 9, 1.0f);
        DrawTextEx(body_font, mode_label.c_str(),
                   { SCREEN_WIDTH - mode_size.x - 30.0f, 9 }, 9, 1.0f,
                   squad.size() > 1 ? COLOR_CYAN_BRIGHT : COLOR_MUTED);

        std::string realm_str = std::string(realm.name);
        Vector2 realm_sz = MeasureTextEx(body_font, realm_str.c_str(), 12, 1.0f);
        DrawTextEx(body_font, realm_str.c_str(), { SCREEN_WIDTH - realm_sz.x - 30, 23 }, 12, 1.0f, realm.accent_color);

        // ── Co-op Squadron Widget (Top Right below header) ──────────────────
        if (squad.size() > 1) {
            float sx = SCREEN_WIDTH - 225.0f;
            float sy = 68.0f;
            for (size_t i = 1; i < squad.size(); ++i) {
                const auto& mate = squad[i];
                Rectangle mate_bar = { sx, sy, 210, 26 };
                Color border_col = mate.is_downed ? COLOR_RED_BRIGHT : COLOR_CYAN_BRIGHT;
                DrawChamferedPanel(mate_bar, border_col, COLOR_SURFACE_MID, 3.0f);

                const std::string life_status = coop_rule == CoopRule::SQUAD_LIVES ? " [SQUAD]" :
                                                coop_rule == CoopRule::HARDCORE ? " [HC]" :
                                                " [L:" + std::to_string(mate.lives) + "]";
                std::string mate_name = mate.callsign + life_status;
                DrawText(mate_name.c_str(), static_cast<int>(sx + 8), static_cast<int>(sy + 6), 9, COLOR_PARCHMENT);
                if (mate.is_spectator) {
                    DrawText("[SPECTATING]", static_cast<int>(sx + 120), static_cast<int>(sy + 6), 9, COLOR_MUTED);
                } else if (mate.is_downed) {
                    float flash = 0.5f + 0.5f * std::sin(GetTime() * 10.0f);
                    Color d_col = ColorAlpha(COLOR_RED_BRIGHT, 0.7f + 0.3f * flash);
                    std::string down_str = "[DOWNED " + std::to_string(static_cast<int>(mate.downed_timer)) + "s]";
                    DrawText(down_str.c_str(), static_cast<int>(sx + 115), static_cast<int>(sy + 6), 9, d_col);
                } else {
                    // Use segmented gauge for squadmate hull integrity
                    Rectangle hp_f = { sx + 105, sy + 7, 95, 12 };
                    DrawSegmentedHealthGauge(hp_f, static_cast<float>(mate.hp), static_cast<float>(mate.max_hp), 8, GetTime());
                }
                sy += 30.0f;
            }
        }

        // ── Boss Health Bar (boss waves only), attack name UNDER bar ─────
        if (boss && boss->active) {
            float boss_hp_ratio = std::clamp(static_cast<float>(boss->hp) / boss->max_hp, 0.0f, 1.0f);
            const float boss_panel_width = squad.size() > 1 ? 450.0f : 540.0f;
            Rectangle boss_panel = { 180, 56, boss_panel_width, 46 };
            DrawBossThreatBanner(boss_panel, boss->name, static_cast<float>(boss->hp), static_cast<float>(boss->max_hp), 3, 3, false, GetTime());

            // Boss name on top of banner
            DrawTextEx(title_font, boss->name.c_str(), { 200, 60 }, 13, 1.0f, boss->theme_color);

            // Phase division notches at 50% and 20% (kept from original for clarity)
            Rectangle bar_rec = { 200, 77, boss_panel_width - 40.0f, 11 };
            DrawLineEx({ bar_rec.x + bar_rec.width * 0.50f, bar_rec.y - 2 }, { bar_rec.x + bar_rec.width * 0.50f, bar_rec.y + bar_rec.height + 2 }, 2.0f, COLOR_GOLD);
            DrawLineEx({ bar_rec.x + bar_rec.width * 0.20f, bar_rec.y - 2 }, { bar_rec.x + bar_rec.width * 0.20f, bar_rec.y + bar_rec.height + 2 }, 2.0f, COLOR_RED_BRIGHT);
            // Attack name UNDER bar, not beside name
            DrawText(boss->attack_name.c_str(), 200, 90, 10, COLOR_GOLD);
        }

        // ── Bottom Cockpit Instruments ──────────────────────────────────
        DrawYantraPanel({ 15, SCREEN_HEIGHT - 42, 870, 28 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f, true);

        // 1. Health Bar
        DrawText("HULL", 30, SCREEN_HEIGHT - 34, 8, COLOR_MUTED);
        Rectangle player_hp_rect = { 30, SCREEN_HEIGHT - 26, 140, 12 };
        DrawSegmentedHealthGauge(player_hp_rect, static_cast<float>(player.hp), static_cast<float>(player.max_hp), 12, GetTime());
        std::string hp_text = std::to_string(player.hp) + "/" + std::to_string(player.max_hp);
        DrawText(hp_text.c_str(), 90, SCREEN_HEIGHT - 22, 10, COLOR_OBSIDIAN);

        // 2. Dash Charges
        DrawText("VAYU", 180, SCREEN_HEIGHT - 34, 8, COLOR_MUTED);
        UI::DrawPipMeter({ 180, SCREEN_HEIGHT - 26 }, player.dash_charges, player.max_dash_charges, COLOR_CYAN_BRIGHT, COLOR_SURFACE_HIGH, 14.0f, 12.0f, 4.0f);

        // 3. Chakram Ready
        DrawText("CHAKRAM [Q]", 240, SCREEN_HEIGHT - 34, 8, COLOR_MUTED);
        float chakram_ratio = 1.0f - std::clamp(player.chakram_timer / player.chakram_cooldown, 0.0f, 1.0f);
        DrawRectangle(240, SCREEN_HEIGHT - 26, 80, 12, { 25, 30, 45, 255 });
        DrawRectangle(240, SCREEN_HEIGHT - 26, static_cast<int>(80 * chakram_ratio), 12, (chakram_ratio >= 1.0f) ? COLOR_GOLD_BRIGHT : COLOR_SURFACE_HIGH);
        DrawRectangleLines(240, SCREEN_HEIGHT - 26, 80, 12, COLOR_GOLD);

        // 4. Brahmastra
        DrawText("BOMB [F]", 340, SCREEN_HEIGHT - 34, 8, COLOR_MUTED);
        std::string bomb_str = "x" + std::to_string(player.brahmastra_bombs);
        DrawTextEx(title_font, bomb_str.c_str(), { 410, SCREEN_HEIGHT - 27 }, 12, 1.0f, COLOR_GOLD_BRIGHT);

        // 5. Consumables - hidden unless owned
        if (player.inventory.soma_vials > 0 || player.inventory.vajra_flares > 0 || player.inventory.kavach_charges > 0) {
            DrawText("ITEMS", 470, SCREEN_HEIGHT - 34, 8, COLOR_MUTED);
            float ix = 470;
            if (player.inventory.soma_vials > 0) {
                std::string soma_str = "SOMA x" + std::to_string(player.inventory.soma_vials);
                DrawText(soma_str.c_str(), (int)ix, SCREEN_HEIGHT - 27, 10, COLOR_GREEN_BRIGHT);
                ix += 75;
            }
            if (player.inventory.vajra_flares > 0) {
                std::string vajra_str = "VAJRA x" + std::to_string(player.inventory.vajra_flares);
                DrawText(vajra_str.c_str(), (int)ix, SCREEN_HEIGHT - 27, 10, COLOR_CYAN_BRIGHT);
                ix += 75;
            }
            if (player.inventory.kavach_charges > 0) {
                std::string kavach_str = "KAVACH x" + std::to_string(player.inventory.kavach_charges);
                DrawText(kavach_str.c_str(), (int)ix, SCREEN_HEIGHT - 27, 10, COLOR_GOLD_BRIGHT);
            }
        }

        // ── Co-op squad minimap ─────────────────────────────────────────────
        if (squad.size() > 1) {
            const Rectangle radar = { 755.0f, SCREEN_HEIGHT - 166.0f, 120.0f, 92.0f };
            const Rectangle field = { radar.x + 7.0f, radar.y + 19.0f, radar.width - 14.0f, radar.height - 26.0f };
            DrawChamferedPanel(radar, COLOR_CYAN_BRIGHT, COLOR_SURFACE_LOW, 4.0f);
            DrawTextEx(body_font, "SQUAD RADAR", { radar.x + 8.0f, radar.y + 5.0f }, 9.0f, 1.0f, COLOR_CYAN_BRIGHT);
            DrawRectangleRec(field, ColorAlpha(COLOR_SURFACE_MID, 0.9f));
            DrawRectangleLinesEx(field, 1.0f, COLOR_SURFACE_HIGH);
            DrawLine(static_cast<int>(field.x + field.width * 0.5f), static_cast<int>(field.y),
                     static_cast<int>(field.x + field.width * 0.5f), static_cast<int>(field.y + field.height), COLOR_SURFACE_HIGH);
            DrawLine(static_cast<int>(field.x), static_cast<int>(field.y + field.height * 0.5f),
                     static_cast<int>(field.x + field.width), static_cast<int>(field.y + field.height * 0.5f), COLOR_SURFACE_HIGH);

            const auto radar_pos = [&field](Vector2 world_pos) {
                return Vector2{
                    field.x + std::clamp(world_pos.x / SCREEN_WIDTH, 0.0f, 1.0f) * field.width,
                    field.y + std::clamp(world_pos.y / SCREEN_HEIGHT, 0.0f, 1.0f) * field.height
                };
            };

            for (const auto& enemy : enemies) {
                if (sensors_jammed) break;
                if (!enemy.active) continue;
                const Vector2 dot = radar_pos(enemy.pos);
                const Color enemy_color = g_colorblind_mode ? COLOR_CB_HOSTILE_SHOT :
                    (enemy.is_elite ? COLOR_GOLD_BRIGHT : COLOR_RED_BRIGHT);
                DrawCircleV(dot, enemy.is_elite ? 2.8f : 1.8f, enemy_color);
                if (g_colorblind_mode) {
                    DrawCircleLines(static_cast<int>(dot.x), static_cast<int>(dot.y), enemy.is_elite ? 4.0f : 3.0f, WHITE);
                }
            }
            if (!sensors_jammed && boss && boss->active) {
                const Vector2 dot = radar_pos(boss->pos);
                DrawCircleV(dot, 4.0f, g_colorblind_mode ? COLOR_CB_HOSTILE_SHOT : COLOR_GOLD_BRIGHT);
                DrawCircleLines(static_cast<int>(dot.x), static_cast<int>(dot.y), 6.0f,
                                g_colorblind_mode ? WHITE : COLOR_ORANGE_BRIGHT);
            }
            for (size_t i = 0; i < squad.size(); ++i) {
                const auto& mate = squad[i];
                const Vector2 dot = radar_pos(mate.pos);
                const Color marker = g_colorblind_mode
                    ? (mate.is_downed ? COLOR_GOLD_BRIGHT : COLOR_CB_PLAYER_SHOT)
                    : (mate.is_downed ? COLOR_RED_BRIGHT : (i == 0 ? COLOR_GREEN_BRIGHT : COLOR_CYAN_BRIGHT));
                if (mate.is_spectator) {
                    DrawCircleLines(static_cast<int>(dot.x), static_cast<int>(dot.y), 3.5f, COLOR_MUTED);
                } else {
                    DrawCircleV(dot, i == 0 ? 3.0f : 2.5f, marker);
                }
            }
        }

        // ── Off-screen Threat Radar: edge triangles pointing at threat ───
        for (const auto& enemy : enemies) {
            if (sensors_jammed) break;
            if (!enemy.active) continue;
            if (enemy.pos.x < 30 || enemy.pos.x > SCREEN_WIDTH - 30 || enemy.pos.y < 70 || enemy.pos.y > SCREEN_HEIGHT - 70) {
                float cx = std::clamp(enemy.pos.x, 35.0f, SCREEN_WIDTH - 35.0f);
                float cy = std::clamp(enemy.pos.y, 75.0f, SCREEN_HEIGHT - 75.0f);
                float ang = std::atan2(enemy.pos.y - cy, enemy.pos.x - cx);
                Vector2 tip = { cx + std::cos(ang) * 10.0f, cy + std::sin(ang) * 10.0f };
                Vector2 l = { cx + std::cos(ang + 2.5f) * 7.0f, cy + std::sin(ang + 2.5f) * 7.0f };
                Vector2 r = { cx + std::cos(ang - 2.5f) * 7.0f, cy + std::sin(ang - 2.5f) * 7.0f };
                const Color threat_color = g_colorblind_mode ? COLOR_CB_HOSTILE_SHOT :
                    (enemy.is_elite ? COLOR_GOLD_BRIGHT : COLOR_RED_BRIGHT);
                DrawTriangle(tip, l, r, threat_color);
                if (g_colorblind_mode) DrawTriangleLines(tip, l, r, WHITE);
            }
        }
    }
};

} // namespace Vimana::UI
