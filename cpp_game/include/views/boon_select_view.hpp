#pragma once
#include <vector>
#include <string>
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "systems/boon_system.hpp"
#include "systems/asset_manager.hpp"
#include "systems/sound_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class BoonSelectView : public IView {
public:
    BoonSelectView() : m_next_view(ViewType::BOON_SELECT), m_selected_card(-1), m_btn_confirm({ SCREEN_WIDTH / 2.0f - 140, SCREEN_HEIGHT - 65, 280, 40 }, "ACCEPT BLESSING >>", COLOR_GOLD_BRIGHT) {
        init();
    }

    void init() override {
        m_next_view = ViewType::BOON_SELECT;
        m_selected_card = 0;
        m_draft_boons = BoonSystem::generate_draft(m_current_boons);
    }

    void set_player_boons(const std::vector<BoonType>& current_boons) {
        m_current_boons = current_boons;
        m_draft_boons = BoonSystem::generate_draft(m_current_boons);
        m_selected_card = 0;
    }

    static const char* get_boon_icon_file(BoonType type) {
        switch (type) {
            case BoonType::AGNI_SOLAR_FURY: return "boon_agni_inferno.png";
            case BoonType::INDRA_VAJRA_THUNDER: return "boon_vajra_strike.png";
            case BoonType::VAYU_GALE_TEMPEST: return "boon_vayu_celerity.png";
            case BoonType::GARUDA_CELESTIAL_MAGNET: return "boon_garuda_wings.png";
            case BoonType::VARUNA_OCEANIC_WARD: return "boon_varuna_shield.png";
            case BoonType::SUDARSHANA_KEEN_EDGE: return "icon_chakram.png";
            case BoonType::YAMA_FATAL_DECREE: return "boon_yama_reap.png";
            case BoonType::SURYA_RADIANT_PIERCE: return "boon_surya_blessing.png";
            case BoonType::NARASIMHA_BERSERK_MIGHT: return "boon_narasimha_berserk.png";
            default: return "icon_chakram.png";
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        float card_w = 246.0f;
        float card_h = 350.0f;
        float spacing = 24.0f;
        float total_w = 3 * card_w + 2 * spacing;
        float start_x = (SCREEN_WIDTH - total_w) / 2.0f;
        float start_y = 100.0f;

        // Mouse Selection
        for (size_t i = 0; i < m_draft_boons.size(); ++i) {
            Rectangle card_rec = { start_x + i * (card_w + spacing), start_y, card_w, card_h };
            if (CheckCollisionPointRec(mouse_pos, card_rec)) {
                if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                    m_selected_card = static_cast<int>(i);
                    SoundSystem::instance().play_ui_click();
                }
            }
        }

        // Hotkey selection [1], [2], [3]
        if ((IsKeyPressed(KEY_ONE) || IsKeyPressed(KEY_KP_1)) && m_draft_boons.size() > 0) {
            m_selected_card = 0;
            SoundSystem::instance().play_ui_click();
        }
        if ((IsKeyPressed(KEY_TWO) || IsKeyPressed(KEY_KP_2)) && m_draft_boons.size() > 1) {
            m_selected_card = 1;
            SoundSystem::instance().play_ui_click();
        }
        if ((IsKeyPressed(KEY_THREE) || IsKeyPressed(KEY_KP_3)) && m_draft_boons.size() > 2) {
            m_selected_card = 2;
            SoundSystem::instance().play_ui_click();
        }

        if (m_btn_confirm.update(mouse_pos) || IsKeyPressed(KEY_ENTER) || IsKeyPressed(KEY_SPACE)) {
            if (m_selected_card >= 0 && m_selected_card < static_cast<int>(m_draft_boons.size())) {
                m_chosen_boon = m_draft_boons[m_selected_card].type;
                m_next_view = ViewType::GAMEPLAY;
            }
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Title Header
        const char* title = "DEVA BLESSINGS // SELECT A ROGUELITE BOON";
        Vector2 t_sz = MeasureTextEx(title_font, title, 20, 1.0f);
        DrawTextEx(title_font, title, { (SCREEN_WIDTH - t_sz.x) / 2.0f, 30 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        const char* sub = "CHOOSE A CELESTIAL POWER - DRAFT SYNERGIES FOR COMPOUNDING COMBAT POWER";
        Vector2 s_sz = MeasureTextEx(body_font, sub, 11, 1.0f);
        DrawTextEx(body_font, sub, { (SCREEN_WIDTH - s_sz.x) / 2.0f, 58 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

        float card_w = 246.0f;
        float card_h = 350.0f;
        float spacing = 24.0f;
        float total_w = 3 * card_w + 2 * spacing;
        float start_x = (SCREEN_WIDTH - total_w) / 2.0f;
        float start_y = 100.0f;

        for (size_t i = 0; i < m_draft_boons.size(); ++i) {
            const auto& boon = m_draft_boons[i];
            bool is_sel = (m_selected_card == static_cast<int>(i));
            Rectangle card_rec = { start_x + i * (card_w + spacing), start_y, card_w, card_h };

            BoonSynergy syn;
            bool completes_synergy = BoonSystem::check_synergy_unlocked(m_current_boons, boon.type, syn);

            Color border = is_sel ? COLOR_GOLD_BRIGHT : (completes_synergy ? syn.color : boon.color);
            Color fill = is_sel ? COLOR_SURFACE_HIGH : COLOR_SURFACE_LOW;
            UI::DrawChamferedPanel(card_rec, border, fill, 8.0f, is_sel);

            // Hotkey indicator in top-right
            std::string key_tag = "[" + std::to_string(i + 1) + "]";
            DrawTextEx(body_font, key_tag.c_str(), { card_rec.x + card_rec.width - 32, card_rec.y + 10 }, 11, 1.0f, is_sel ? COLOR_GOLD_BRIGHT : COLOR_MUTED);

            // Synergy Banner on card top
            float content_y = card_rec.y + 14.0f;
            if (completes_synergy) {
                Rectangle syn_rec = { card_rec.x + 10, content_y, card_rec.width - 50, 20 };
                UI::DrawChamferedPanel(syn_rec, syn.color, COLOR_SURFACE_HIGH, 3.0f);
                std::string syn_text = "[SYNERGY] " + syn.name;
                DrawTextEx(body_font, syn_text.c_str(), { syn_rec.x + 6, syn_rec.y + 4 }, 10, 1.0f, syn.color);
                content_y += 26.0f;
            }

            // Boon Icon (48x48)
            const char* icon_file = get_boon_icon_file(boon.type);
            Texture2D icon_tex = AssetManager::instance().get_texture(icon_file);
            float icon_x = card_rec.x + 16.0f;
            float icon_y = content_y + 4.0f;

            if (icon_tex.id > 0) {
                Rectangle icon_bg = { icon_x - 2, icon_y - 2, 48, 48 };
                DrawRectangleRec(icon_bg, COLOR_SURFACE_MID);
                DrawRectangleLinesEx(icon_bg, 1.0f, is_sel ? COLOR_GOLD_BRIGHT : boon.color);
                DrawTexturePro(icon_tex, 
                    { 0, 0, static_cast<float>(icon_tex.width), static_cast<float>(icon_tex.height) },
                    { icon_x, icon_y, 44, 44 },
                    { 0, 0 }, 0.0f, WHITE);
            }

            // Deity Header next to icon
            DrawTextEx(body_font, boon.deity.c_str(), { icon_x + 54.0f, icon_y + 4.0f }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(title_font, boon.name.c_str(), { icon_x + 54.0f, icon_y + 20.0f }, 13, 1.0f, boon.color);

            content_y = icon_y + 54.0f;
            DrawLine(static_cast<int>(card_rec.x + 16), static_cast<int>(content_y), static_cast<int>(card_rec.x + card_w - 16), static_cast<int>(content_y), COLOR_MUTED);
            content_y += 10.0f;

            // Description
            DrawTextEx(body_font, boon.description.c_str(), { card_rec.x + 16, content_y }, 11, 1.0f, COLOR_PARCHMENT);

            // If synergy, also describe the bonus combo
            if (completes_synergy) {
                float syn_y = content_y + 70.0f;
                DrawTextEx(body_font, "SYNERGISTIC FUSION:", { card_rec.x + 16, syn_y }, 10, 1.0f, COLOR_GOLD_BRIGHT);
                DrawTextEx(body_font, syn.description.c_str(), { card_rec.x + 16, syn_y + 16 }, 11, 1.0f, syn.color);
            }

            // Selection indicator at bottom
            if (is_sel) {
                Rectangle sel_badge = { card_rec.x + 50, card_rec.y + card_h - 36, card_rec.width - 100, 24 };
                DrawRectangleRec(sel_badge, ColorAlpha(COLOR_GOLD, 0.25f));
                DrawRectangleLinesEx(sel_badge, 1.0f, COLOR_GOLD_BRIGHT);
                Vector2 sel_sz = MeasureTextEx(body_font, "[ SELECTED ]", 12, 1.0f);
                DrawTextEx(body_font, "[ SELECTED ]", { sel_badge.x + (sel_badge.width - sel_sz.x) / 2.0f, sel_badge.y + 5 }, 12, 1.0f, COLOR_GOLD_BRIGHT);
            }
        }

        // Active Passives indicator bar at bottom
        std::string active_str = "CURRENT VIMANA BOONS: " + std::to_string(m_current_boons.size()) + " EQUIPPED";
        DrawTextEx(body_font, active_str.c_str(), { 45, static_cast<float>(SCREEN_HEIGHT - 55) }, 12, 1.0f, COLOR_MUTED);

        m_btn_confirm.draw(title_font);
        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::BOON_SELECT; }
    BoonType chosen_boon() const { return m_chosen_boon; }

private:
    ViewType m_next_view;
    int m_selected_card;
    BoonType m_chosen_boon = BoonType::AGNI_SOLAR_FURY;
    std::vector<BoonInfo> m_draft_boons;
    std::vector<BoonType> m_current_boons;
    UI::Button m_btn_confirm;
};

} // namespace Vimana
