#pragma once
#include <string>
#include <vector>
#include <unordered_set>
#include <fstream>
#include <filesystem>
#include <iostream>
#include "raylib.h"
#include "json.hpp"
#include "core/constants.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/sound_system.hpp"
#include "systems/http_client.hpp"
#include "systems/account_system.hpp"

namespace Vimana {

struct AchievementDef {
    std::string id;
    std::string title;
    std::string description;
    std::string category;
};

inline const std::vector<AchievementDef> ALL_ACHIEVEMENTS = {
    { "FIRST_BLOOD",       "First Blood",            "Destroy your first enemy asura in combat.",       "COMBAT" },
    { "WAVE_5",            "Survivor of Swarga",     "Clear wave 5 and penetrate the astral defenses.",  "CAMPAIGN" },
    { "WAVE_15",           "Kshatriya Vanguard",     "Reach wave 15 deep in the cosmic void.",           "CAMPAIGN" },
    { "WAVE_30",           "Act I Vanguard",         "Clear the first 30-wave act of Mahayuddha.",       "ULTIMATE" },
    { "BOSS_1",            "Kumbhakarna Defeated",   "Defeat the first act's guardian titan.",            "BOSS" },
    { "BOSS_5",            "Ravana Overthrown",      "Defeat Emperor Ravana in a boss encounter.",        "BOSS" },
    { "PERFECT_WAVE",      "Untouched Warrior",      "Clear an entire wave taking zero damage.",         "SKILL" },
    { "COMBO_25",          "Combo Disciple",         "Build a sustained x25 combat strike streak.",      "COMBAT" },
    { "COMBO_50",          "Divya Astra Resonance",  "Achieve the legendary x50 maximum combo.",         "COMBAT" },
    { "BRAHMASTRA",        "Celestial Cataclysm",    "Detonate the ultimate Brahmastra celestial nuke.",  "WEAPON" },
    { "COOP_REVIVE",       "Brother's Keeper",       "Revive a downed squadmate in the heat of battle.", "CO-OP" },
    { "COOP_DUAL_ASTRA",   "Thunder Tempest",        "Execute a synchronized dual-Astra cooperative fury.","CO-OP" },
    { "ALL_BOONS",         "Deva Blessed",           "Equip all available divine boons during a run.",   "BUILD" },
    { "UNLOCK_SHIP",       "Astral Shipwright",      "Commission a new Vimana with astral prana.",       "PROGRESSION" },
    { "ALL_SHIPS",         "Supreme Armada",         "Command all 60 Vimanas in the celestial fleet.",   "PROGRESSION" },
    { "DAILY_WIN",         "Daily Devotion",         "Complete a daily cosmic challenge sortie.",        "EVENT" },
    { "IRON_MODE",         "Iron Ascetic",           "Survive a campaign sortie on Chakravyuha tier.",   "MASTERY" },
    { "LEADERBOARD_TOP10", "Sangha Vanguard",        "Enter the top 10 rankings on the cloud leaderboard.","ONLINE" },
    { "REGISTER",          "Sangha Commissioned",    "Create an authenticated Sangha pilot account.",    "ACCOUNT" },
    { "PLAY_10",           "Veteran of the Void",    "Deploy on 10 combat sorties across the 10 acts.",  "CAREER" }
};

class AchievementSystem {
public:
    static AchievementSystem& instance() {
        static AchievementSystem sys;
        return sys;
    }

    void init() {
        m_unlocked.clear();
        m_toast_timer = 0.0f;
        load_from_save();
    }

    bool is_unlocked(const std::string& id) const {
        return m_unlocked.find(id) != m_unlocked.end();
    }

    const std::unordered_set<std::string>& unlocked() const {
        return m_unlocked;
    }

    static std::string cloud_id_for(const std::string& local_id) {
        std::string cloud_id = local_id;
        for (char& ch : cloud_id) {
            if (ch >= 'A' && ch <= 'Z') ch = static_cast<char>(ch - 'A' + 'a');
        }
        return cloud_id;
    }

    void check_and_award(const std::string& id) {
        if (is_unlocked(id)) return; // Already awarded

        // Locate achievement definition
        const AchievementDef* def = nullptr;
        for (const auto& a : ALL_ACHIEVEMENTS) {
            if (a.id == id) { def = &a; break; }
        }
        if (!def) return;

        m_unlocked.insert(id);
        save_to_save();

        // Queue in-game visual toast
        m_toast_title = def->title;
        m_toast_desc = def->description;
        m_toast_timer = 4.0f;

        // Play glorious audio cue
        SoundSystem::instance().play_transcendence();

        // Sync to cloud backend if authenticated
        if (AccountSystem::instance().is_logged_in()) {
            std::string url = AccountSystem::instance().api_base() + "/achievements";
            nlohmann::json payload;
            payload["achievement_id"] = cloud_id_for(id);
            HTTPClient::instance().post_async(url, payload.dump(), AccountSystem::instance().token(), [](HTTPClient::Response resp) {
                if (resp.success) {
                    std::cout << "[AchievementSystem] Achievement backed up to cloud." << std::endl;
                }
            });
        }
    }

    void notify_event(const std::string& title, const std::string& description) {
        m_toast_title = title;
        m_toast_desc = description;
        m_toast_timer = 4.0f;
        SoundSystem::instance().play_transcendence();
    }

    void update(float dt) {
        if (m_toast_timer > 0.0f) {
            m_toast_timer -= dt;
        }
    }

    void draw_toast(Font title_f, Font body_f) {
        if (m_toast_timer <= 0.0f) return;

        // Slide-in animation from bottom-right
        float slide = 1.0f;
        if (m_toast_timer > 3.5f) {
            slide = (4.0f - m_toast_timer) / 0.5f; // Slide in
        } else if (m_toast_timer < 0.5f) {
            slide = m_toast_timer / 0.5f; // Slide out
        }
        slide = std::clamp(slide, 0.0f, 1.0f);

        float box_w = 320.0f;
        float box_h = 60.0f;
        float end_x = SCREEN_WIDTH - box_w - 20.0f;
        float start_x = SCREEN_WIDTH + 10.0f;
        float cur_x = start_x + (end_x - start_x) * slide;
        float cur_y = SCREEN_HEIGHT - box_h - 75.0f;

        Rectangle toast_rec = { cur_x, cur_y, box_w, box_h };
        UI::DrawYantraPanel(toast_rec, COLOR_GOLD_BRIGHT, COLOR_SURFACE_HIGH, 4.0f, true);

        // Vector Star Icon
        UI::DrawStarIcon({ cur_x + 22.0f, cur_y + box_h / 2.0f }, 10.0f, COLOR_GOLD_BRIGHT);

        // Text
        DrawText("ACHIEVEMENT UNLOCKED //", static_cast<int>(cur_x + 42), static_cast<int>(cur_y + 8), 9, COLOR_CYAN_BRIGHT);
        DrawTextEx(title_f, m_toast_title.c_str(), { cur_x + 42, cur_y + 20 }, 13, 1.0f, COLOR_GOLD_BRIGHT);
        DrawTextEx(body_f, m_toast_desc.c_str(), { cur_x + 42, cur_y + 38 }, 10, 1.0f, COLOR_PARCHMENT);
    }

private:
    AchievementSystem() : m_toast_timer(0.0f) {}
    ~AchievementSystem() = default;

    std::string get_save_path() const {
        const char* up = std::getenv("USERPROFILE");
        if (!up) return "";
        return std::string(up) + "/.vimana_wars/save.json";
    }

    void load_from_save() {
        std::string path = get_save_path();
        if (path.empty() || !std::filesystem::exists(path)) return;
        try {
            std::ifstream f(path);
            nlohmann::json j;
            f >> j;
            if (j.contains("achievements") && j["achievements"].is_array()) {
                for (const auto& item : j["achievements"]) {
                    m_unlocked.insert(item.get<std::string>());
                }
            }
        } catch (...) {}
    }

    void save_to_save() {
        std::string path = get_save_path();
        if (path.empty()) return;
        try {
            nlohmann::json j;
            if (std::filesystem::exists(path)) {
                std::ifstream fi(path);
                fi >> j;
            }
            std::vector<std::string> arr(m_unlocked.begin(), m_unlocked.end());
            j["version"] = SAVE_SCHEMA_VERSION;
            j["achievements"] = arr;
            std::ofstream fo(path);
            fo << j.dump(2);
        } catch (...) {}
    }

    std::unordered_set<std::string> m_unlocked;
    float m_toast_timer;
    std::string m_toast_title;
    std::string m_toast_desc;
};

} // namespace Vimana
