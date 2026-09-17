#pragma once
#include <vector>
#include <string>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
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

        float tab_w = 140;
        float tab_h = 36;
        float tab_x = 40;
        float tab_y = 75;

        m_tab_buttons.clear();
        m_tab_buttons.emplace_back(Rectangle{ tab_x, tab_y, tab_w, tab_h }, "1. REALMS", COLOR_CYAN_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 150, tab_y, tab_w, tab_h }, "2. VIMANAS", COLOR_GOLD_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 300, tab_y, tab_w, tab_h }, "3. ASURAS", COLOR_RED_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 450, tab_y, tab_w, tab_h }, "4. TITANS", COLOR_PURPLE_BRIGHT);
        m_tab_buttons.emplace_back(Rectangle{ tab_x + 600, tab_y, tab_w, tab_h }, "5. SYNERGIES", COLOR_GREEN_BRIGHT);
    }

    void update(float dt, Vector2 mouse_pos) override {
        for (size_t i = 0; i < m_tab_buttons.size(); ++i) {
            if (m_tab_buttons[i].update(mouse_pos)) {
                m_active_tab = static_cast<CodexTab>(i);
                m_selected_index = 0;
            }
        }

        // List item clicking
        int max_items = get_item_count();
        float list_y = 135;
        for (int i = 0; i < max_items; ++i) {
            Rectangle item_rec = { 40, list_y + i * 36.0f, 260, 32 };
            if (CheckCollisionPointRec(mouse_pos, item_rec) && IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
                m_selected_index = i;
            }
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
        DrawTextEx(body_font, "STRATEGIC INTEL - ASURA THREAT ASSESSMENTS - DIVINE WEAPON BLUEPRINTS", { 42, 52 }, 11, 1.0f, COLOR_CYAN_BRIGHT);

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

        m_btn_back.draw(title_font);
        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::CODEX; }

private:
    int get_item_count() const {
        switch (m_active_tab) {
            case CodexTab::REALMS: return 7;
            case CodexTab::VIMANAS: return static_cast<int>(SHIP_FLEET.size());
            case CodexTab::ASURAS: return 5;
            case CodexTab::BOSSES: return 5;
            case CodexTab::SYNERGIES: return static_cast<int>(ALL_SYNERGIES.size());
        }
        return 0;
    }

    void draw_tab_content(Font font, Rectangle list_box, Rectangle detail_box) {
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        if (m_active_tab == CodexTab::REALMS) {
            struct RInfo { const char* name; const char* waves; const char* boss; const char* lore; const char* tactic; };
            static const RInfo realms[] = {
                { "Swarga Outpost", "Waves 1-3", "None", "Indra's orbital gate protecting the higher planes. Scouting waves test perimeter defenses.", "High agility skiffs. Focus on keeping combos active." },
                { "Kshira Sagara", "Waves 4-6", "Makara Leviathan", "The celestial Ocean of Milk. Glowing tides of stellar dust and ancient relics.", "Flank Makara when he coils to discharge vortex orbs." },
                { "Dandaka Void", "Waves 7-10", "Indrajit Ravana", "Dark nebulas filled with asteroid mines and camouflaged demon raiders.", "Avoid colliding with dark matter clusters; conserve dash charges." },
                { "Lanka Approach", "Waves 11-15", "Kumbhakarna", "The outer perimeter of Ravana's golden citadel, guarded by heavy siege engines.", "Kumbhakarna deploys wide flak barriers; target his core vents." },
                { "Setu Expanse", "Waves 16-20", "Meghnada Stormlord", "A colossal bridge of floating planetary cores woven with electromagnetic webs.", "Meghnada conjures illusions; look for the true radar ping." },
                { "Naraka Forge", "Waves 21-25", "None", "Subterranean magma pits generating legions of biomechanical Asuras.", "Thermal aura gradually heats hull; pick up Amrita promptly." },
                { "Mahayuddha Citadel", "Waves 26-30", "Emperor Hiranyakashipu", "The throne of darkness. The ultimate clash for universal cosmic dharma.", "Immortal aura requires shattering solar beacons to inflict harm." }
            };

            static const char* realm_bg_files[] = {
                "realm_swarga.png",
                "realm_kshira_sagara.png",
                "realm_dandaka_void.png",
                "realm_lanka_approach.png",
                "realm_setu_expanse.png",
                "realm_naraka_forge.png",
                "realm_mahayuddha_citadel.png"
            };

            for (int i = 0; i < 7; ++i) {
                Rectangle item_rec = { list_box.x + 8, list_box.y + 10 + i * 36.0f, list_box.width - 16, 32 };
                bool sel = (m_selected_index == i);
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawTextEx(body_font, realms[i].name, { item_rec.x + 10, item_rec.y + 8 }, 12, 1.0f, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& r = realms[m_selected_index];
            DrawTextEx(title_font, r.name, { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
            DrawTextEx(body_font, ("OPERATIONAL SPAN: " + std::string(r.waves)).c_str(), { detail_box.x + 25, detail_box.y + 48 }, 12, 1.0f, COLOR_CYAN_BRIGHT);
            DrawTextEx(body_font, ("TITAN GUARDIAN: " + std::string(r.boss)).c_str(), { detail_box.x + 25, detail_box.y + 68 }, 12, 1.0f, COLOR_RED_BRIGHT);

            // Realm Thumbnail Preview
            Texture2D rtex = AssetManager::instance().get_texture(realm_bg_files[m_selected_index]);
            if (rtex.id > 0) {
                Rectangle src = { 0, 0, static_cast<float>(rtex.width), static_cast<float>(rtex.height) };
                Rectangle dst = { detail_box.x + detail_box.width - 160, detail_box.y + 18, 140, 80 };
                DrawRectangleRec({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, COLOR_SURFACE_LOW);
                DrawRectangleLinesEx({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, 1.0f, COLOR_GOLD);
                DrawTexturePro(rtex, src, dst, { 0, 0 }, 0.0f, WHITE);
            }

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 105), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 105), COLOR_MUTED);

            DrawTextEx(body_font, "SECTOR LORE ARCHIVE:", { detail_box.x + 25, detail_box.y + 120 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, r.lore, { detail_box.x + 25, detail_box.y + 140 }, 12, 1.0f, COLOR_PARCHMENT);

            DrawTextEx(body_font, "TACTICAL RECOMMENDATION:", { detail_box.x + 25, detail_box.y + 205 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, r.tactic, { detail_box.x + 25, detail_box.y + 225 }, 12, 1.0f, COLOR_GREEN_BRIGHT);
        }
        else if (m_active_tab == CodexTab::VIMANAS) {
            for (size_t i = 0; i < SHIP_FLEET.size(); ++i) {
                Rectangle item_rec = { list_box.x + 8, list_box.y + 8 + i * 31.0f, list_box.width - 16, 28 };
                bool sel = (m_selected_index == static_cast<int>(i));
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawTextEx(body_font, SHIP_FLEET[i].name.c_str(), { item_rec.x + 10, item_rec.y + 6 }, 11, 1.0f, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& s = SHIP_FLEET[m_selected_index];
            DrawTextEx(title_font, s.name.c_str(), { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
            DrawTextEx(body_font, s.role.c_str(), { detail_box.x + 25, detail_box.y + 48 }, 12, 1.0f, COLOR_CYAN_BRIGHT);

            // Sprite preview
            Texture2D tex = AssetManager::instance().get_texture(s.sprite_file);
            if (tex.id > 0) {
                Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
                Rectangle dst = { detail_box.x + detail_box.width - 105, detail_box.y + 18, 80, 80 };
                DrawRectangleRec({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, COLOR_SURFACE_LOW);
                DrawRectangleLinesEx({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, 1.0f, s.accent_color);
                DrawTexturePro(tex, src, dst, { 0, 0 }, 0.0f, WHITE);
            }

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 80), static_cast<int>(detail_box.x + detail_box.width - 120), static_cast<int>(detail_box.y + 80), COLOR_MUTED);

            // Stats
            DrawTextEx(body_font, ("HULL INTEGRITY: " + std::to_string(s.max_hp) + " HP").c_str(), { detail_box.x + 25, detail_box.y + 95 }, 12, 1.0f, COLOR_GREEN_BRIGHT);
            DrawTextEx(body_font, ("PROPULSION VELOCITY: " + std::to_string(static_cast<int>(s.speed)) + " M/S").c_str(), { detail_box.x + 25, detail_box.y + 115 }, 12, 1.0f, COLOR_CYAN_BRIGHT);
            DrawTextEx(body_font, ("WARP DASH COOLDOWN: " + std::to_string(s.dash_cooldown).substr(0, 4) + " SEC").c_str(), { detail_box.x + 25, detail_box.y + 135 }, 12, 1.0f, COLOR_PURPLE_BRIGHT);

            DrawTextEx(body_font, "DESIGNATION & CLASS:", { detail_box.x + 25, detail_box.y + 175 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, s.subtitle.c_str(), { detail_box.x + 25, detail_box.y + 195 }, 12, 1.0f, COLOR_GOLD);

            DrawTextEx(body_font, "COMMISSION REQUIREMENTS:", { detail_box.x + 25, detail_box.y + 240 }, 11, 1.0f, COLOR_MUTED);
            std::string cost_str = "PRANA COST: " + std::to_string(s.prana_cost) + " | WAVE UNLOCK: " + std::to_string(s.unlock_wave);
            DrawTextEx(body_font, cost_str.c_str(), { detail_box.x + 25, detail_box.y + 260 }, 11, 1.0f, COLOR_PARCHMENT);
        }
        else if (m_active_tab == CodexTab::ASURAS) {
            struct AsuraIntel { const char* name; const char* threat; const char* role; const char* weakness; const char* desc; };
            static const AsuraIntel asuras[] = {
                { "Asura Scout", "THREAT: LOW (1/5)", "Recon & Flanking", "Fragile chassis; easily eliminated with standard plasma shots.", "Light, agile interceptors deployed to harass and split Deva formations." },
                { "Ravana Fighter", "THREAT: MODERATE (2/5)", "Assault Skiff", "Vulnerable right after releasing twin plasma bursts.", "Workhorse fighter equipped with twin red plasma cannons." },
                { "Void Destroyer", "THREAT: HEAVY (3/5)", "Heavy Gunship", "Sluggish maneuverability; flank and attack from the rear.", "Armored gunship unleashing 3-way spread salvos. High hull resistance." },
                { "Rakshasa Marauder", "THREAT: SEVERE (4/5)", "High-Speed Ramming", "Predictable charge path; dash perpendicular to dodge.", "Rocket-propelled kamikaze vessel loaded with volatile dark matter explosives." },
                { "Naga Cruiser", "THREAT: LETHAL (4/5)", "Missile Platform", "Missiles can be intercepted with fire or wiped with Vajra Flares.", "Advanced heavy vessel launching homing venom torpedoes that track the Vimana." }
            };

            for (int i = 0; i < 5; ++i) {
                Rectangle item_rec = { list_box.x + 8, list_box.y + 10 + i * 36.0f, list_box.width - 16, 32 };
                bool sel = (m_selected_index == i);
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawTextEx(body_font, asuras[i].name, { item_rec.x + 10, item_rec.y + 8 }, 12, 1.0f, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& a = asuras[m_selected_index];
            DrawTextEx(title_font, a.name, { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_RED_BRIGHT);
            DrawTextEx(body_font, a.threat, { detail_box.x + 25, detail_box.y + 48 }, 12, 1.0f, COLOR_ORANGE_BRIGHT);
            DrawTextEx(body_font, a.role, { detail_box.x + 25, detail_box.y + 68 }, 12, 1.0f, COLOR_CYAN_BRIGHT);

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 95), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 95), COLOR_MUTED);

            DrawTextEx(body_font, "ASURA TACTICAL BLUEPRINT:", { detail_box.x + 25, detail_box.y + 115 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, a.desc, { detail_box.x + 25, detail_box.y + 135 }, 12, 1.0f, COLOR_PARCHMENT);

            DrawTextEx(body_font, "IDENTIFIED VULNERABILITY:", { detail_box.x + 25, detail_box.y + 200 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, a.weakness, { detail_box.x + 25, detail_box.y + 220 }, 12, 1.0f, COLOR_GREEN_BRIGHT);
        }
        else if (m_active_tab == CodexTab::BOSSES) {
            struct BossIntel { const char* name; const char* wave; const char* title; const char* telegraph; const char* strat; const char* sprite; };
            static const BossIntel bosses[] = {
                { "Makara Leviathan", "Wave 6 Boss", "Terror of Kshira Sagara", "1.2s warning banner before discharging concentric Void Orbs.", "Maintain distance during vortex charge; attack during recovery cool-down.", "boss_makara" },
                { "Indrajit Ravana", "Wave 10 Boss", "Lord of Lanka & Sorcery", "Invisibility cloaking followed by illusion clones and poison darts.", "Track true radar ping; detonate Chakram to dispel illusion doubles.", "boss_indrajit.png" },
                { "Kumbhakarna", "Wave 15 Boss", "The Sleeping Colossus", "Audible siren and red targeting laser preceding mega-beam discharge.", "Heavy armor deflects frontal shots. Maneuver behind the titan to hit exhaust vents.", "boss_kumbhakarna" },
                { "Meghnada Stormlord", "Wave 20 Boss", "Master of Illusion & Thunder", "Lightning arc telegraph creates glowing danger zones before striking.", "Use Vajra Flares to dissolve lightning traps and reveal his genuine position.", "boss_indrajit.png" },
                { "Hiranyakashipu", "Wave 30 Final Boss", "Immortal Demon Emperor", "Charges apocalyptic Brahmashira cannon with full-screen crimson reticle.", "Deploy Brahmastra bombs to break invulnerability shield; prioritize dodging over DPS.", "boss_hiranyakashipu.png" }
            };

            for (int i = 0; i < 5; ++i) {
                Rectangle item_rec = { list_box.x + 8, list_box.y + 10 + i * 36.0f, list_box.width - 16, 32 };
                bool sel = (m_selected_index == i);
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawTextEx(body_font, bosses[i].name, { item_rec.x + 10, item_rec.y + 8 }, 12, 1.0f, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& b = bosses[m_selected_index];
            DrawTextEx(title_font, b.name, { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
            DrawTextEx(body_font, b.wave, { detail_box.x + 25, detail_box.y + 48 }, 12, 1.0f, COLOR_RED_BRIGHT);
            DrawTextEx(body_font, b.title, { detail_box.x + 25, detail_box.y + 68 }, 12, 1.0f, COLOR_PURPLE_BRIGHT);

            // Boss Portrait preview
            Texture2D btex = AssetManager::instance().get_texture(b.sprite);
            if (btex.id > 0) {
                Rectangle src = { 0, 0, static_cast<float>(btex.width), static_cast<float>(btex.height) };
                Rectangle dst = { detail_box.x + detail_box.width - 105, detail_box.y + 18, 80, 80 };
                DrawRectangleRec({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, COLOR_SURFACE_LOW);
                DrawRectangleLinesEx({ dst.x - 2, dst.y - 2, dst.width + 4, dst.height + 4 }, 1.0f, COLOR_RED_BRIGHT);
                DrawTexturePro(btex, src, dst, { 0, 0 }, 0.0f, WHITE);
            }

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 95), static_cast<int>(detail_box.x + detail_box.width - 120), static_cast<int>(detail_box.y + 95), COLOR_MUTED);

            DrawTextEx(body_font, "ATTACK TELEGRAPH WARNING:", { detail_box.x + 25, detail_box.y + 115 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, b.telegraph, { detail_box.x + 25, detail_box.y + 135 }, 12, 1.0f, COLOR_ORANGE_BRIGHT);

            DrawTextEx(body_font, "COUNTER-STRATEGY:", { detail_box.x + 25, detail_box.y + 200 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, b.strat, { detail_box.x + 25, detail_box.y + 220 }, 12, 1.0f, COLOR_GREEN_BRIGHT);
        }
        else if (m_active_tab == CodexTab::SYNERGIES) {
            for (size_t i = 0; i < ALL_SYNERGIES.size(); ++i) {
                Rectangle item_rec = { list_box.x + 8, list_box.y + 10 + i * 36.0f, list_box.width - 16, 32 };
                bool sel = (m_selected_index == static_cast<int>(i));
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawTextEx(body_font, ALL_SYNERGIES[i].name.c_str(), { item_rec.x + 10, item_rec.y + 8 }, 12, 1.0f, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& syn = ALL_SYNERGIES[m_selected_index];
            DrawTextEx(title_font, syn.name.c_str(), { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, syn.color);
            DrawTextEx(body_font, ("RECIPE FORMULA: " + syn.formula).c_str(), { detail_box.x + 25, detail_box.y + 48 }, 13, 1.0f, COLOR_GOLD_BRIGHT);

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 80), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 80), COLOR_MUTED);

            DrawTextEx(body_font, "DIVINE SYNERGISTIC EFFECT:", { detail_box.x + 25, detail_box.y + 105 }, 11, 1.0f, COLOR_MUTED);
            DrawTextEx(body_font, syn.description.c_str(), { detail_box.x + 25, detail_box.y + 130 }, 13, 1.0f, COLOR_PARCHMENT);

            DrawTextEx(body_font, "STRATEGIC UTILITY:", { detail_box.x + 25, detail_box.y + 200 }, 11, 1.0f, COLOR_MUTED);
        }
    }

    ViewType m_next_view;
    CodexTab m_active_tab;
    int m_selected_index;
    std::vector<UI::Button> m_tab_buttons;
    UI::Button m_btn_back;
};

} // namespace Vimana
