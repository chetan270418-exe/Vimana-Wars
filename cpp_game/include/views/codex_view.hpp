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
        Font font = AssetManager::instance().font();

        // Header
        const char* title = "ASTRAL CODEX // CELESTIAL REPOSITORY & BESTIARY";
        DrawTextEx(font, title, { 40, 25 }, 24, 1.0f, COLOR_GOLD_BRIGHT);
        DrawText("STRATEGIC INTEL • ASURA THREAT ASSESSMENTS • DIVINE WEAPON BLUEPRINTS", 42, 54, 11, COLOR_CYAN_BRIGHT);

        // Draw Tab Buttons
        for (size_t i = 0; i < m_tab_buttons.size(); ++i) {
            bool is_active = (m_active_tab == static_cast<CodexTab>(i));
            m_tab_buttons[i].draw(font);
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

        draw_tab_content(font, list_box, detail_box);

        m_btn_back.draw(font);
        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::CODEX; }

private:
    int get_item_count() const {
        switch (m_active_tab) {
            case CodexTab::REALMS: return 7;
            case CodexTab::VIMANAS: return static_cast<int>(SHIP_FLEET.size());
            case CodexTab::ASURAS: return 5;
            case CodexTab::BOSSES: return 4;
            case CodexTab::SYNERGIES: return static_cast<int>(ALL_SYNERGIES.size());
        }
        return 0;
    }

    void draw_tab_content(Font font, Rectangle list_box, Rectangle detail_box) {
        if (m_active_tab == CodexTab::REALMS) {
            struct RInfo { const char* name; const char* waves; const char* boss; const char* lore; const char* tactic; };
            static const RInfo realms[] = {
                { "Swarga Outpost", "Waves 1-3", "None", "Indra's orbital gate protecting the higher planes. Scouting waves test perimeter defenses.", "High agility skiffs. Focus on keeping combos active." },
                { "Kshira Sagara", "Waves 4-6", "Makara Leviathan", "The celestial Ocean of Milk. Glowing tides of stellar dust and ancient relics.", "Flank Makara when he coils to discharge vortex orbs." },
                { "Dandaka Void", "Waves 7-10", "None", "Dark nebulas filled with asteroid mines and camouflaged demon raiders.", "Avoid colliding with dark matter clusters; conserve dash charges." },
                { "Lanka Approach", "Waves 11-15", "Kumbhakarna", "The outer perimeter of Ravana's golden citadel, guarded by heavy siege engines.", "Kumbhakarna deploys wide flak barriers; target his core vents." },
                { "Setu Expanse", "Waves 16-20", "Meghnada", "A colossal bridge of floating planetary cores woven with electromagnetic webs.", "Meghnada conjures illusions; look for the true radar ping." },
                { "Naraka Forge", "Waves 21-25", "None", "Subterranean magma pits generating legions of biomechanical Asuras.", "Thermal aura gradually heats hull; pick up Amrita promptly." },
                { "Mahayuddha Citadel", "Waves 26-30", "Hiranyakashipu", "The throne of darkness. The ultimate clash for universal cosmic dharma.", "Immortal aura requires shattering solar beacons to inflict harm." }
            };

            for (int i = 0; i < 7; ++i) {
                Rectangle item_rec = { list_box.x + 10, list_box.y + 10 + i * 36.0f, list_box.width - 20, 30 };
                bool sel = (m_selected_index == i);
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawText(realms[i].name, static_cast<int>(item_rec.x + 10), static_cast<int>(item_rec.y + 7), 12, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& r = realms[m_selected_index];
            DrawTextEx(font, r.name, { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
            DrawText(("OPERATIONAL SPAN: " + std::string(r.waves)).c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 48), 12, COLOR_CYAN_BRIGHT);
            DrawText(("TITAN GUARDIAN: " + std::string(r.boss)).c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 68), 12, COLOR_RED_BRIGHT);

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 95), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 95), COLOR_MUTED);

            DrawText("SECTOR LORE ARCHIVE:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 115), 11, COLOR_MUTED);
            DrawText(r.lore, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 135), 12, COLOR_PARCHMENT);

            DrawText("TACTICAL RECOMMENDATION:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 200), 11, COLOR_MUTED);
            DrawText(r.tactic, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 220), 12, COLOR_GREEN_BRIGHT);
        }
        else if (m_active_tab == CodexTab::VIMANAS) {
            for (size_t i = 0; i < SHIP_FLEET.size(); ++i) {
                Rectangle item_rec = { list_box.x + 10, list_box.y + 10 + i * 36.0f, list_box.width - 20, 30 };
                bool sel = (m_selected_index == static_cast<int>(i));
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawText(SHIP_FLEET[i].name.c_str(), static_cast<int>(item_rec.x + 10), static_cast<int>(item_rec.y + 7), 12, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& s = SHIP_FLEET[m_selected_index];
            DrawTextEx(font, s.name.c_str(), { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
            DrawText(s.role.c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 48), 12, COLOR_CYAN_BRIGHT);

            // Sprite preview
            Texture2D tex = AssetManager::instance().get_texture(s.sprite_file);
            if (tex.id > 0) {
                DrawTextureEx(tex, { detail_box.x + detail_box.width - 120, detail_box.y + 20 }, 0.0f, 1.2f, WHITE);
            }

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 80), static_cast<int>(detail_box.x + detail_box.width - 140), static_cast<int>(detail_box.y + 80), COLOR_MUTED);

            // Stats
            DrawText(("HULL INTEGRITY: " + std::to_string(s.max_hp) + " HP").c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 95), 12, COLOR_GREEN_BRIGHT);
            DrawText(("PROPULSION VELOCITY: " + std::to_string(static_cast<int>(s.speed)) + " M/S").c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 115), 12, COLOR_CYAN_BRIGHT);
            DrawText(("WARP DASH COOLDOWN: " + std::to_string(s.dash_cooldown).substr(0, 4) + " SEC").c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 135), 12, COLOR_PURPLE_BRIGHT);

            DrawText("DESIGNATION & CLASS:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 175), 11, COLOR_MUTED);
            DrawText(s.subtitle.c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 195), 12, COLOR_GOLD);

            DrawText("COMMISSION REQUIREMENTS:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 240), 11, COLOR_MUTED);
            std::string cost_str = "PRANA COST: " + std::to_string(s.prana_cost) + " | WAVE UNLOCK: " + std::to_string(s.unlock_wave);
            DrawText(cost_str.c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 260), 11, COLOR_PARCHMENT);
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
                Rectangle item_rec = { list_box.x + 10, list_box.y + 10 + i * 36.0f, list_box.width - 20, 30 };
                bool sel = (m_selected_index == i);
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawText(asuras[i].name, static_cast<int>(item_rec.x + 10), static_cast<int>(item_rec.y + 7), 12, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& a = asuras[m_selected_index];
            DrawTextEx(font, a.name, { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_RED_BRIGHT);
            DrawText(a.threat, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 48), 12, COLOR_ORANGE_BRIGHT);
            DrawText(a.role, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 68), 12, COLOR_CYAN_BRIGHT);

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 95), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 95), COLOR_MUTED);

            DrawText("ASURA TACTICAL BLUEPRINT:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 115), 11, COLOR_MUTED);
            DrawText(a.desc, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 135), 12, COLOR_PARCHMENT);

            DrawText("IDENTIFIED VULNERABILITY:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 200), 11, COLOR_MUTED);
            DrawText(a.weakness, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 220), 12, COLOR_GREEN_BRIGHT);
        }
        else if (m_active_tab == CodexTab::BOSSES) {
            struct BossIntel { const char* name; const char* wave; const char* title; const char* telegraph; const char* strat; };
            static const BossIntel bosses[] = {
                { "Makara Leviathan", "Wave 6 Boss", "Terror of Kshira Sagara", "1.2s warning banner before discharging concentric Void Orbs.", "Maintain distance during vortex charge; attack during recovery cool-down." },
                { "Kumbhakarna", "Wave 15 Boss", "The Sleeping Colossus", "Audible siren and red targeting laser preceding mega-beam discharge.", "Heavy armor deflects frontal shots. Maneuver behind the titan to hit exhaust vents." },
                { "Meghnada", "Wave 20 Boss", "Sorcerer of Storms (Indrajit)", "Lightning arc telegraph creates glowing danger zones before striking.", "Use Vajra Flares to dissolve lightning traps and reveal his genuine position." },
                { "Hiranyakashipu", "Wave 30 Final Boss", "Immortal Demon Emperor", "Charges apocalyptic Brahmashira cannon with full-screen crimson reticle.", "Deploy Brahmastra bombs to break invulnerability shield; prioritize dodging over DPS." }
            };

            for (int i = 0; i < 4; ++i) {
                Rectangle item_rec = { list_box.x + 10, list_box.y + 10 + i * 36.0f, list_box.width - 20, 30 };
                bool sel = (m_selected_index == i);
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawText(bosses[i].name, static_cast<int>(item_rec.x + 10), static_cast<int>(item_rec.y + 7), 12, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& b = bosses[m_selected_index];
            DrawTextEx(font, b.name, { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, COLOR_GOLD_BRIGHT);
            DrawText(b.wave, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 48), 12, COLOR_RED_BRIGHT);
            DrawText(b.title, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 68), 12, COLOR_PURPLE_BRIGHT);

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 95), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 95), COLOR_MUTED);

            DrawText("ATTACK TELEGRAPH WARNING:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 115), 11, COLOR_MUTED);
            DrawText(b.telegraph, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 135), 12, COLOR_ORANGE_BRIGHT);

            DrawText("COUNTER-STRATEGY:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 200), 11, COLOR_MUTED);
            DrawText(b.strat, static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 220), 12, COLOR_GREEN_BRIGHT);
        }
        else if (m_active_tab == CodexTab::SYNERGIES) {
            for (size_t i = 0; i < ALL_SYNERGIES.size(); ++i) {
                Rectangle item_rec = { list_box.x + 10, list_box.y + 10 + i * 36.0f, list_box.width - 20, 30 };
                bool sel = (m_selected_index == static_cast<int>(i));
                if (sel) DrawRectangleRec(item_rec, COLOR_SURFACE_HIGH);
                DrawText(ALL_SYNERGIES[i].name.c_str(), static_cast<int>(item_rec.x + 10), static_cast<int>(item_rec.y + 7), 12, sel ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            }

            const auto& syn = ALL_SYNERGIES[m_selected_index];
            DrawTextEx(font, syn.name.c_str(), { detail_box.x + 25, detail_box.y + 20 }, 20, 1.0f, syn.color);
            DrawText(("RECIPE FORMULA: " + syn.formula).c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 48), 13, COLOR_GOLD_BRIGHT);

            DrawLine(static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 80), static_cast<int>(detail_box.x + detail_box.width - 25), static_cast<int>(detail_box.y + 80), COLOR_MUTED);

            DrawText("DIVINE SYNERGISTIC EFFECT:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 105), 11, COLOR_MUTED);
            DrawText(syn.description.c_str(), static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 130), 13, COLOR_PARCHMENT);

            DrawText("STRATEGIC UTILITY:", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 200), 11, COLOR_MUTED);
            DrawText("Combining these two boons during rogue draft unlocks this passive power permanently for your expedition!", static_cast<int>(detail_box.x + 25), static_cast<int>(detail_box.y + 220), 11, COLOR_CYAN_BRIGHT);
        }
    }

    ViewType m_next_view;
    CodexTab m_active_tab;
    int m_selected_index;
    std::vector<UI::Button> m_tab_buttons;
    UI::Button m_btn_back;
};

} // namespace Vimana
