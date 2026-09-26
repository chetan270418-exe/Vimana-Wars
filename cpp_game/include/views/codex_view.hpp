#pragma once
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <sstream>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/campaign_content.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "entities/player.hpp"
#include "systems/boon_system.hpp"
#include "systems/asset_manager.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

enum class CodexTab {
    REALMS,
    VIMANAS,
    ASURAS,
    BOSSES,
    LORE,
    SYNERGIES
};

class CodexView : public IView {
public:
    CodexView() 
        : m_next_view(ViewType::CODEX),
          m_active_tab(CodexTab::REALMS),
          m_selected_index(0),
          m_btn_back({ 40, SCREEN_HEIGHT - 65, 170, 40 }, "<< MAIN MENU", COLOR_MUTED)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::CODEX;
        m_selected_index = 0;
        m_list_start = 0;

        const float tab_w = 128.0f;
        float tab_h = 36;
        float tab_x = 40;
        float tab_y = 75;

        m_tab_buttons.clear();
        m_tab_buttons.emplace_back(Rectangle{ tab_x, tab_y, tab_w, tab_h }, "1. REALMS", COLOR_CYAN_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 138, tab_y, tab_w, tab_h }, "2. SHIPS", COLOR_GOLD_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 276, tab_y, tab_w, tab_h }, "3. ASURAS", COLOR_RED_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 414, tab_y, tab_w, tab_h }, "4. BOSSES", COLOR_PURPLE_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 552, tab_y, tab_w, tab_h }, "5. LORE", COLOR_CYAN_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 690, tab_y, tab_w, tab_h }, "6. SYNERGIES", COLOR_GREEN_BRIGHT);
    }

    void update(float dt, Vector2 mouse_pos) override {
        for (size_t i = 0; i < m_tab_buttons.size(); ++i) {
            if (m_tab_buttons[i].update(mouse_pos)) {
                m_active_tab = static_cast<CodexTab>(i);
                m_selected_index = 0;
                m_list_start = 0;
            }
        }

        if (IsKeyPressed(KEY_RIGHT) || IsKeyPressed(KEY_TAB)) {
            m_active_tab = static_cast<CodexTab>((static_cast<int>(m_active_tab) + 1) % static_cast<int>(m_tab_buttons.size()));
            m_selected_index = m_list_start = 0;
        } else if (IsKeyPressed(KEY_LEFT)) {
            const int tab_count = static_cast<int>(m_tab_buttons.size());
            m_active_tab = static_cast<CodexTab>((static_cast<int>(m_active_tab) + tab_count - 1) % tab_count);
            m_selected_index = m_list_start = 0;
        }
        const int max_items = get_item_count();
        if (max_items > 0) {
            if (IsKeyPressed(KEY_DOWN)) ++m_selected_index;
            if (IsKeyPressed(KEY_UP)) --m_selected_index;
            if (CheckCollisionPointRec(mouse_pos, { 40, 125, 270, 395 })) {
                const float wheel = GetMouseWheelMove();
                if (wheel != 0.0f) m_selected_index -= static_cast<int>(wheel) * 3;
                if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                    const int row = static_cast<int>((mouse_pos.y - 135.0f) / 36.0f);
                    if (row >= 0 && row < CODEX_LIST_ROWS) m_selected_index = m_list_start + row;
                }
            }
            m_selected_index = std::clamp(m_selected_index, 0, max_items - 1);
            if (m_selected_index < m_list_start) m_list_start = m_selected_index;
            if (m_selected_index >= m_list_start + CODEX_LIST_ROWS) m_list_start = m_selected_index - CODEX_LIST_ROWS + 1;
            m_list_start = std::clamp(m_list_start, 0, std::max(0, max_items - CODEX_LIST_ROWS));
        }

        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Header
        const char* title = "ASTRAL CODEX // CELESTIAL REPOSITORY & BESTIARY";
        DrawTextEx(title_font, title, { 40, 24 }, 22, 1.0f, COLOR_GOLD_BRIGHT);
        DrawTextEx(body_font, "10 REALMS  //  62 VIMANAS  //  8 BOSSES  //  MINI-BOSSES  //  CAMPAIGN LORE", { 42, 52 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

        // Draw Tab Buttons
        for (size_t i = 0; i < m_tab_buttons.size(); ++i) {
            bool is_active = (m_active_tab == static_cast<CodexTab>(i));
            m_tab_buttons[i].draw(title_font);
            if (is_active) {
                const auto& r = m_tab_buttons[i].rect();
                DrawRectangle(static_cast<int>(r.x), static_cast<int>(r.y + r.height), static_cast<int>(r.width), 3, COLOR_GOLD_BRIGHT);
            }
        }

        // Left List Container
        Rectangle list_box = { 40, 125, 270, 395 };
        UI::DrawChamferedPanel(list_box, COLOR_SURFACE_HIGH, COLOR_SURFACE_LOW, 6.0f);

        // Right Detail Container
        Rectangle detail_box = { 330, 125, 530, 395 };
        UI::DrawChamferedPanel(detail_box, COLOR_GOLD, COLOR_SURFACE_MID, 6.0f);

        draw_tab_content(title_font, list_box, detail_box);

        const int item_count = get_item_count();
        if (item_count > CODEX_LIST_ROWS) {
            const Rectangle track = { 300.0f, 139.0f, 3.0f, 360.0f };
            DrawRectangleRec(track, COLOR_SURFACE_HIGH);
            const float thumb_h = track.height * CODEX_LIST_ROWS / item_count;
            const float thumb_y = track.y + (track.height - thumb_h) * m_list_start / (item_count - CODEX_LIST_ROWS);
            DrawRectangleRec({ track.x, thumb_y, track.width, thumb_h }, COLOR_CYAN_BRIGHT);
        }

        DrawTextEx(body_font, "UP/DOWN OR WHEEL: BROWSE   //   LEFT/RIGHT: SECTION", { 330, 530 }, 10, 1.0f, COLOR_MUTED);
        m_btn_back.draw(title_font);
        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::CODEX; }

private:
    int get_item_count() const {
        switch (m_active_tab) {
            case CodexTab::REALMS: return static_cast<int>(CAMPAIGN_REALMS.size());
            case CodexTab::VIMANAS: return static_cast<int>(SHIP_FLEET.size());
            case CodexTab::ASURAS: return 6;
            case CodexTab::BOSSES: return 8 + static_cast<int>(MINI_BOSS_INTEL.size());
            case CodexTab::LORE: return static_cast<int>(CAMPAIGN_STORY_EVENTS.size());
            case CodexTab::SYNERGIES: return static_cast<int>(ALL_SYNERGIES.size());
        }
        return 0;
    }

    void draw_tab_content(Font, Rectangle list_box, Rectangle detail_box) {
        const Font title_font = AssetManager::instance().title_font();
        const Font body_font = AssetManager::instance().body_font();
        const auto draw_row = [&](int index, const std::string& label, Color accent = COLOR_GOLD_BRIGHT) {
            const int row = index - m_list_start;
            if (row < 0 || row >= CODEX_LIST_ROWS) return;
            const Rectangle item = { list_box.x + 8, list_box.y + 10 + row * 36.0f, list_box.width - 20, 32 };
            const bool selected = index == m_selected_index;
            if (selected) {
                DrawRectangleRec(item, COLOR_SURFACE_HIGH);
                DrawRectangle(static_cast<int>(item.x), static_cast<int>(item.y), 3, static_cast<int>(item.height), accent);
            }
            DrawTextEx(body_font, label.c_str(), { item.x + 10, item.y + 8 }, 12, 1.0f,
                       selected ? accent : COLOR_PARCHMENT);
        };
        const auto draw_preview = [&](const std::string& path, Color accent, float width = 92.0f) {
            const Texture2D texture = AssetManager::instance().get_texture(path);
            if (texture.id <= 0) return;
            const Rectangle dst = { detail_box.x + detail_box.width - width - 25, detail_box.y + 18, width, 76 };
            DrawRectangleRec({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, COLOR_SURFACE_LOW);
            DrawRectangleLinesEx({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, 1.0f, accent);
            DrawTexturePro(texture, { 0, 0, static_cast<float>(texture.width), static_cast<float>(texture.height) },
                           dst, { 0, 0 }, 0.0f, WHITE);
        };
        const auto heading = [&](const std::string& text, float y) {
            DrawTextEx(title_font, text.c_str(), { detail_box.x + 25, detail_box.y + y }, 20, 1.0f, COLOR_GOLD_BRIGHT);
        };
        const auto label = [&](const std::string& text, float y, Color color = COLOR_CYAN_BRIGHT) {
            DrawTextEx(body_font, text.c_str(), { detail_box.x + 25, detail_box.y + y }, 12, 1.0f, color);
        };
        const float text_width = detail_box.width - 50.0f;

        if (m_active_tab == CodexTab::REALMS) {
            static const std::array<const char*, 10> backgrounds = {{
                "realm_swarga.png", "realm_kshira_sagara.png", "realm_dandaka_void.png",
                "realm_lanka_approach.png", "realm_setu_expanse.png", "realm_naraka_forge.png",
                "realm_mahayuddha_citadel.png", "realm_kshira_sagara.png", "realm_dandaka_void.png",
                "realm_mahayuddha_citadel.png"
            }};
            for (int i = m_list_start; i < std::min(get_item_count(), m_list_start + CODEX_LIST_ROWS); ++i)
                draw_row(i, "ACT " + std::to_string(CAMPAIGN_REALMS[i].id) + " // " + CAMPAIGN_REALMS[i].name, CAMPAIGN_REALMS[i].accent_color);

            const CampaignRealm& realm = CAMPAIGN_REALMS[m_selected_index];
            heading(realm.name, 20);
            label("ACT " + std::to_string(realm.id) + "  //  WAVES " + std::to_string(realm.start_wave) + "-" + std::to_string(realm.end_wave), 49);
            label(std::string("GUARDIAN: ") + realm.boss_name, 69, COLOR_RED_BRIGHT);
            draw_preview(backgrounds[m_selected_index], realm.accent_color, 125.0f);
            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 105),
                     static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 105), COLOR_MUTED);
            DrawTextEx(body_font, "REALM BRIEFING", { detail_box.x + 25, detail_box.y + 120 }, 11, 1.0f, COLOR_MUTED);
            draw_wrapped_text(body_font, realm.description, { detail_box.x + 25, detail_box.y + 140 }, text_width, 12, 1.0f, COLOR_PARCHMENT, 3);
            DrawTextEx(body_font, "REALM MECHANIC", { detail_box.x + 25, detail_box.y + 225 }, 11, 1.0f, COLOR_MUTED);
            label(realm.modifier_desc, 245, realm.accent_color);
            DrawTextEx(body_font, "TACTIC: adapt movement and firing to the active sector effect.",
                       { detail_box.x + 25, detail_box.y + 282 }, 11, 1.0f, COLOR_GREEN_BRIGHT);
        } else if (m_active_tab == CodexTab::VIMANAS) {
            for (int i = m_list_start; i < std::min(get_item_count(), m_list_start + CODEX_LIST_ROWS); ++i)
                draw_row(i, SHIP_FLEET[i].name, SHIP_FLEET[i].accent_color);
            const ShipArchetype& ship = SHIP_FLEET[m_selected_index];
            heading(ship.name, 20);
            label(ship.role, 49);
            draw_preview(ship.sprite_file, ship.accent_color);
            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 82),
                     static_cast<int>(detail_box.x + detail_box.width - 130), static_cast<int>(detail_box.y + 82), COLOR_MUTED);
            label("HULL " + std::to_string(ship.max_hp) + "  //  SPEED " + std::to_string(static_cast<int>(ship.speed)), 98, COLOR_GREEN_BRIGHT);
            label("DASH COOLDOWN " + std::to_string(ship.dash_cooldown).substr(0, 4) + " SEC", 119, COLOR_PURPLE_BRIGHT);
            DrawTextEx(body_font, "COMBAT IDENTITY // PASSIVE OR WEAPON PROFILE", { detail_box.x + 25, detail_box.y + 157 }, 11, 1.0f, COLOR_MUTED);
            label(ShipSignatureName(ship), 177, ship.accent_color);
            draw_wrapped_text(body_font, ShipSignatureDescription(ship), { detail_box.x + 25, detail_box.y + 198 }, text_width, 12, 1.0f, COLOR_PARCHMENT, 3);
            DrawTextEx(body_font, ("COMMISSION: WAVE " + std::to_string(ship.unlock_wave) + "  //  " + std::to_string(ship.prana_cost) + " PRANA").c_str(),
                       { detail_box.x + 25, detail_box.y + 280 }, 11, 1.0f, COLOR_GOLD_BRIGHT);
            if (!ship.boss_unlock_id.empty())
                DrawTextEx(body_font, (std::string("SALVAGE CONDITION: DEFEAT ") + ship.boss_unlock_name).c_str(),
                           { detail_box.x + 25, detail_box.y + 303 }, 11, 1.0f, COLOR_RED_BRIGHT);
        } else if (m_active_tab == CodexTab::ASURAS) {
            struct AsuraIntel { const char* name; const char* threat; const char* role; const char* weakness; const char* desc; };
            static const std::array<AsuraIntel, 6> asuras = {{
                { "Asura Scout", "THREAT: LOW (1/5)", "Recon & Flanking", "Fragile chassis; standard shots are effective.", "Light interceptors deployed to harass and split Deva formations." },
                { "Ravana Fighter", "THREAT: MODERATE (2/5)", "Assault Skiff", "Attack after it releases its twin plasma bursts.", "Workhorse fighter equipped with twin red plasma cannons." },
                { "Void Destroyer", "THREAT: HEAVY (3/5)", "Heavy Gunship", "Flank its slow turn and attack from behind.", "Armored gunship unleashing three-way spread salvos." },
                { "Rakshasa Marauder", "THREAT: SEVERE (4/5)", "High-Speed Ramming", "Dash perpendicular to its predictable charge.", "Rocket-propelled kamikaze vessel loaded with volatile dark matter." },
                { "Naga Cruiser", "THREAT: LETHAL (4/5)", "Missile Platform", "Intercept missiles or clear them with Vajra Flares.", "Heavy vessel launching homing venom torpedoes." },
                { "Asura Healer", "THREAT: HIGH (3/5)", "Fleet Support", "Focus it before nearby enemies recover their hull.", "Support craft restore the health of nearby hostile ships; their value rises sharply inside large formations." }
            }};
            for (int i = m_list_start; i < std::min(get_item_count(), m_list_start + CODEX_LIST_ROWS); ++i)
                draw_row(i, asuras[i].name, COLOR_RED_BRIGHT);
            const AsuraIntel& asura = asuras[m_selected_index];
            heading(asura.name, 20);
            label(asura.threat, 49, COLOR_ORANGE_BRIGHT);
            label(asura.role, 70);
            DrawTextEx(body_font, "HOSTILE PROFILE", { detail_box.x + 25, detail_box.y + 112 }, 11, 1.0f, COLOR_MUTED);
            draw_wrapped_text(body_font, asura.desc, { detail_box.x + 25, detail_box.y + 134 }, text_width, 12, 1.0f, COLOR_PARCHMENT, 4);
            DrawTextEx(body_font, "COUNTERMEASURE", { detail_box.x + 25, detail_box.y + 235 }, 11, 1.0f, COLOR_MUTED);
            draw_wrapped_text(body_font, asura.weakness, { detail_box.x + 25, detail_box.y + 257 }, text_width, 12, 1.0f, COLOR_GREEN_BRIGHT, 3);
        } else if (m_active_tab == CodexTab::BOSSES) {
            struct BossIntel { const char* name; const char* title; const char* telegraph; const char* strategy; const char* sprite; };
            static const std::array<BossIntel, 8> bosses = {{
                { "Kumbhakarna", "The Sleeping Colossus", "Seismic stomp and broad, heavy projectile arcs pressure the squadron.", "Keep moving and attack between volleys.", "boss_kumbhakarna.png" },
                { "Ravana", "Tenfold Emperor of Lanka", "Void spiral rings sweep the arena and accelerate at low health.", "Read the rotation and dash through a safe lane.", "boss_ravana.png" },
                { "Mahishasura", "The Unyielding Buffalo King", "A targeted lance fan follows the telegraphed charge.", "Break formation and sidestep before the burst lands.", "boss_mahishasura.png" },
                { "Makara Leviathan", "Terror of the Celestial Deep", "Tidal lance spreads leave a moving safe lane.", "Track the opening and attack during recovery.", "boss_makara.png" },
                { "Conqueror Indrajit", "Master of Illusions & Astras", "A phase-shift cloak precedes teleport and serpent arrows.", "Reposition when the attack marker returns.", "boss_indrajit.png" },
                { "Hiranyakashipu", "Immortal Demon Sovereign", "An invulnerability pact guards his final-phase wrath burst.", "Survive the burst, then punish recovery.", "boss_hiranyakashipu.png" },
                { "Meghnada", "Storm Illusionist of Lanka", "Lightning fan and teleporting crossfire target your last position.", "Move during the warning; leave the marked lane.", "boss_meghnada.png" },
                { "Vritra", "Sky-Sealing Serpent", "A descending wall leaves a telegraphed safe corridor.", "Move into the corridor before the wall arrives.", "boss_vritra.png" }
            }};
            for (int i = m_list_start; i < std::min(get_item_count(), m_list_start + CODEX_LIST_ROWS); ++i) {
                const std::string name = i < static_cast<int>(bosses.size()) ? bosses[i].name : MINI_BOSS_INTEL[i - bosses.size()].name;
                draw_row(i, name, i < static_cast<int>(bosses.size()) ? COLOR_RED_BRIGHT : COLOR_ORANGE_BRIGHT);
            }
            if (m_selected_index < static_cast<int>(bosses.size())) {
                const BossIntel& boss = bosses[m_selected_index];
                heading(boss.name, 20);
                label("BOSS FLEET // EVERY FIFTH WAVE", 49, COLOR_RED_BRIGHT);
                label(boss.title, 70, COLOR_PURPLE_BRIGHT);
                draw_preview(boss.sprite, COLOR_RED_BRIGHT);
                DrawTextEx(body_font, "SIGNATURE TELEGRAPH", { detail_box.x + 25, detail_box.y + 117 }, 11, 1.0f, COLOR_MUTED);
                draw_wrapped_text(body_font, boss.telegraph, { detail_box.x + 25, detail_box.y + 139 }, text_width, 12, 1.0f, COLOR_ORANGE_BRIGHT, 3);
                DrawTextEx(body_font, "COUNTER-PLAY", { detail_box.x + 25, detail_box.y + 226 }, 11, 1.0f, COLOR_MUTED);
                draw_wrapped_text(body_font, boss.strategy, { detail_box.x + 25, detail_box.y + 248 }, text_width, 12, 1.0f, COLOR_GREEN_BRIGHT, 3);
            } else {
                const MiniBossIntel& miniboss = MINI_BOSS_INTEL[m_selected_index - bosses.size()];
                heading(miniboss.name, 20);
                label("RECURRING MINI-BOSS // ACT WAVE " + std::to_string(miniboss.act_wave), 49, COLOR_RED_BRIGHT);
                label(miniboss.title, 70, COLOR_PURPLE_BRIGHT);
                draw_preview(miniboss.sprite_file, COLOR_ORANGE_BRIGHT);
                DrawTextEx(body_font, "FORMATION WARNING", { detail_box.x + 25, detail_box.y + 117 }, 11, 1.0f, COLOR_MUTED);
                draw_wrapped_text(body_font, miniboss.warning, { detail_box.x + 25, detail_box.y + 139 }, text_width, 12, 1.0f, COLOR_ORANGE_BRIGHT, 3);
                DrawTextEx(body_font, "COUNTER-PLAY", { detail_box.x + 25, detail_box.y + 226 }, 11, 1.0f, COLOR_MUTED);
                draw_wrapped_text(body_font, miniboss.counter, { detail_box.x + 25, detail_box.y + 248 }, text_width, 12, 1.0f, COLOR_GREEN_BRIGHT, 3);
            }
        } else if (m_active_tab == CodexTab::LORE) {
            for (int i = m_list_start; i < std::min(get_item_count(), m_list_start + CODEX_LIST_ROWS); ++i) {
                const CampaignStoryEvent& event = CAMPAIGN_STORY_EVENTS[i];
                draw_row(i, "WAVE " + std::to_string(event.wave) + " // " + event.title, COLOR_CYAN_BRIGHT);
            }
            const CampaignStoryEvent& event = CAMPAIGN_STORY_EVENTS[m_selected_index];
            heading(event.title, 20);
            label("CAMPAIGN EVENT // WAVE " + std::to_string(event.wave), 51, COLOR_GOLD_BRIGHT);
            DrawTextEx(body_font, event.speaker, { detail_box.x + 25, detail_box.y + 99 }, 12, 1.0f, COLOR_CYAN_BRIGHT);
            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 127),
                     static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 127), COLOR_MUTED);
            draw_wrapped_text(body_font, event.message, { detail_box.x + 25, detail_box.y + 151 }, text_width, 15, 1.0f, COLOR_PARCHMENT, 6);
            DrawTextEx(body_font, ("TRANSMISSION ARCHIVED // ACT " + std::to_string(CampaignActForWave(event.wave))).c_str(),
                       { detail_box.x + 25, detail_box.y + 285 }, 11, 1.0f, COLOR_MUTED);
        } else if (m_active_tab == CodexTab::SYNERGIES) {
            for (int i = m_list_start; i < std::min(get_item_count(), m_list_start + CODEX_LIST_ROWS); ++i)
                draw_row(i, ALL_SYNERGIES[i].name, ALL_SYNERGIES[i].color);
            const BoonSynergy& synergy = ALL_SYNERGIES[m_selected_index];
            heading(synergy.name, 20);
            label("RECIPE // " + synergy.formula, 51, synergy.color);
            DrawTextEx(body_font, "FUSION EFFECT", { detail_box.x + 25, detail_box.y + 108 }, 11, 1.0f, COLOR_MUTED);
            draw_wrapped_text(body_font, synergy.description, { detail_box.x + 25, detail_box.y + 131 }, text_width, 14, 1.0f, COLOR_PARCHMENT, 6);
        }
    }

    void draw_wrapped_text(Font font, const std::string& text, Vector2 pos, float max_width,
                           float font_size, float spacing, Color color, int max_lines) {
        std::istringstream words(text);
        std::string word;
        std::string line;
        int lines = 0;
        const float line_height = font_size + 6.0f;
        while (words >> word) {
            const std::string candidate = line.empty() ? word : line + " " + word;
            if (!line.empty() && MeasureTextEx(font, candidate.c_str(), font_size, spacing).x > max_width) {
                DrawTextEx(font, line.c_str(), { pos.x, pos.y + lines * line_height }, font_size, spacing, color);
                if (++lines >= max_lines) return;
                line = word;
            } else {
                line = candidate;
            }
        }
        if (!line.empty() && lines < max_lines)
            DrawTextEx(font, line.c_str(), { pos.x, pos.y + lines * line_height }, font_size, spacing, color);
    }

    ViewType m_next_view;
    CodexTab m_active_tab;
    int m_selected_index;
    int m_list_start = 0;
    static constexpr int CODEX_LIST_ROWS = 10;
    std::vector<UI::Button> m_tab_buttons;
    UI::Button m_btn_back;
};

} // namespace Vimana
