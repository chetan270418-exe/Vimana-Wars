#pragma once
#include <algorithm>
#include <string>
#include <unordered_set>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/account_system.hpp"
#include "systems/achievement_system.hpp"
#include "systems/asset_manager.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"
#include "systems/http_client.hpp"
#include "ui/button.hpp"
#include "ui/design_tokens.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class AchievementsView : public IView {
public:
    AchievementsView()
        : m_next_view(ViewType::ACHIEVEMENTS),
          m_btn_back({ 35, 535, 150, 38 }, "BACK TO MENU", COLOR_MUTED),
          m_btn_prev({ 650, 535, 88, 38 }, "< PREV", COLOR_CYAN_BRIGHT),
          m_btn_next({ 760, 535, 105, 38 }, "NEXT >", COLOR_GOLD_BRIGHT) {
        init();
    }

    void init() override {
        m_next_view = ViewType::ACHIEVEMENTS;
        m_page = 0;
        m_cloud_unlocked.clear();
        m_status = AccountSystem::instance().is_logged_in()
            ? "SYNCING CLOUD TROPHIES..." : "LOCAL TROPHIES // SIGN IN TO CHECK CLOUD UNLOCKS";
        m_match_count = static_cast<int>(DBSystem::instance().fetch_match_history(10).size());

        if (AccountSystem::instance().is_logged_in()) {
            const std::string url = AccountSystem::instance().api_base() + "/achievements";
            HTTPClient::instance().get_async(url, AccountSystem::instance().token(), [this](HTTPClient::Response response) {
                if (!response.success) {
                    m_status = "CLOUD UNAVAILABLE // LOCAL RECORDS SHOWN";
                    return;
                }
                try {
                    const auto root = nlohmann::json::parse(response.body);
                    if (root.contains("unlocked") && root["unlocked"].is_array()) {
                        for (const auto& id : root["unlocked"]) {
                            if (id.is_string()) m_cloud_unlocked.insert(id.get<std::string>());
                        }
                    }
                    m_status = "CLOUD TROPHIES SYNCED // " + std::to_string(m_cloud_unlocked.size()) + " ONLINE UNLOCKS";
                } catch (...) {
                    m_status = "CLOUD RESPONSE INVALID // LOCAL RECORDS SHOWN";
                }
            });
        }
    }

    void update(float, Vector2 mouse_pos) override {
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
            return;
        }
        if (m_btn_prev.update(mouse_pos) || IsKeyPressed(KEY_LEFT)) {
            m_page = (m_page + page_count() - 1) % page_count();
        }
        if (m_btn_next.update(mouse_pos) || IsKeyPressed(KEY_RIGHT)) {
            m_page = (m_page + 1) % page_count();
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        const Font title_font = AssetManager::instance().title_font();
        const Font body_font = AssetManager::instance().body_font();

        UI::DrawYantraPanel({ 30, 20, 840, 58 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f, true);
        const int unlocked_count = static_cast<int>(AchievementSystem::instance().unlocked().size());
        const std::string title = "ACHIEVEMENT HALL // " + std::to_string(unlocked_count) + "/" +
                                  std::to_string(ALL_ACHIEVEMENTS.size()) + " LOCAL UNLOCKS";
        DrawTextEx(title_font, title.c_str(), { 48, 30 }, 21, 1.0f, COLOR_GOLD_BRIGHT);

        const int first = m_page * ITEMS_PER_PAGE;
        const int last = std::min(first + ITEMS_PER_PAGE, static_cast<int>(ALL_ACHIEVEMENTS.size()));
        for (int index = first; index < last; ++index) {
            const int within_page = index - first;
            const int col = within_page / 4;
            const int row = within_page % 4;
            const Rectangle card = { 35.0f + col * 430.0f, 95.0f + row * 104.0f, 400.0f, 88.0f };
            const auto& achievement = ALL_ACHIEVEMENTS[index];
            const std::string cloud_id = AchievementSystem::cloud_id_for(achievement.id);
            const bool local = AchievementSystem::instance().is_unlocked(achievement.id);
            const bool cloud = m_cloud_unlocked.find(cloud_id) != m_cloud_unlocked.end();
            const bool unlocked = local || cloud;
            const Color accent = unlocked ? COLOR_GOLD_BRIGHT : COLOR_MUTED;

            UI::DrawChamferedPanel(card, accent, COLOR_SURFACE_LOW, 5.0f);
            UI::DrawStarIcon({ card.x + 22.0f, card.y + 23.0f }, 8.0f, accent);
            DrawTextEx(title_font, achievement.title.c_str(), { card.x + 42.0f, card.y + 10.0f },
                       13.0f, 1.0f, unlocked ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT);
            const std::string category = achievement.category + (cloud ? " // CLOUD" : (local ? " // LOCAL" : " // LOCKED"));
            DrawTextEx(body_font, category.c_str(), { card.x + 42.0f, card.y + 29.0f }, 9.0f, 1.0f,
                       unlocked ? COLOR_CYAN_BRIGHT : COLOR_MUTED);
            DrawTextEx(body_font, achievement.description.c_str(), { card.x + 12.0f, card.y + 47.0f },
                       9.0f, 1.0f, COLOR_PARCHMENT);

            const auto progress = progress_for(achievement.id, unlocked);
            const Rectangle bar = { card.x + 12.0f, card.y + 72.0f, card.width - 24.0f, 7.0f };
            DrawRectangleRec(bar, COLOR_SURFACE_HIGH);
            DrawRectangleRec({ bar.x, bar.y, bar.width * progress.first, bar.height }, unlocked ? COLOR_GOLD_BRIGHT : COLOR_CYAN_BRIGHT);
            DrawTextEx(body_font, progress.second.c_str(), { card.x + card.width - 115.0f, card.y + 59.0f },
                       8.0f, 1.0f, unlocked ? COLOR_GOLD_BRIGHT : COLOR_MUTED);
        }

        DrawTextEx(body_font, m_status.c_str(), { 205, 546 }, 9, 1.0f, COLOR_CYAN_BRIGHT);
        const std::string page_label = "PAGE " + std::to_string(m_page + 1) + "/" + std::to_string(page_count());
        DrawText(page_label.c_str(), 705, 520, 10, COLOR_PARCHMENT);
        m_btn_back.draw(title_font);
        m_btn_prev.draw(title_font);
        m_btn_next.draw(title_font);
        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::ACHIEVEMENTS; }

private:
    static constexpr int ITEMS_PER_PAGE = 8;

    int page_count() const {
        return std::max(1, (static_cast<int>(ALL_ACHIEVEMENTS.size()) + ITEMS_PER_PAGE - 1) / ITEMS_PER_PAGE);
    }

    std::pair<float, std::string> progress_for(const std::string& id, bool unlocked) const {
        if (unlocked) return { 1.0f, "COMPLETE" };
        const int max_wave = DBSystem::instance().max_wave();
        if (id == "WAVE_5") return { std::clamp(max_wave / 5.0f, 0.0f, 1.0f), std::to_string(std::min(max_wave, 5)) + "/5 WAVES" };
        if (id == "WAVE_15") return { std::clamp(max_wave / 15.0f, 0.0f, 1.0f), std::to_string(std::min(max_wave, 15)) + "/15 WAVES" };
        if (id == "WAVE_30") return { std::clamp(max_wave / 30.0f, 0.0f, 1.0f), std::to_string(std::min(max_wave, 30)) + "/30 WAVES" };
        if (id == "REGISTER") return { AccountSystem::instance().is_logged_in() ? 1.0f : 0.0f,
                                         AccountSystem::instance().is_logged_in() ? "ACCOUNT READY" : "SIGN IN" };
        if (id == "PLAY_10") {
            return { std::clamp(m_match_count / 10.0f, 0.0f, 1.0f), std::to_string(m_match_count) + "/10 SORTIES" };
        }
        if (id == "ALL_SHIPS" || id == "UNLOCK_SHIP") {
            int ready = 0;
            for (const auto& ship : SHIP_FLEET) {
                if (CurrencySystem::instance().is_ship_unlocked(ship.id, max_wave)) ++ready;
            }
            const int target = (id == "ALL_SHIPS") ? static_cast<int>(SHIP_FLEET.size()) : 4;
            return { std::clamp(static_cast<float>(ready) / target, 0.0f, 1.0f),
                     std::to_string(std::min(ready, target)) + "/" + std::to_string(target) + " SHIPS" };
        }
        return { 0.0f, "COMBAT TRACKED" };
    }

    ViewType m_next_view;
    int m_page = 0;
    int m_match_count = 0;
    std::string m_status;
    std::unordered_set<std::string> m_cloud_unlocked;
    UI::Button m_btn_back;
    UI::Button m_btn_prev;
    UI::Button m_btn_next;
};

} // namespace Vimana
