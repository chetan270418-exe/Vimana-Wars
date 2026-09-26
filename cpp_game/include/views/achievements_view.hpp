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
        ClearBackground(UI::PAL_BG_VOID);
        const Font title_font = AssetManager::instance().title_font();
        const Font body_font = AssetManager::instance().body_font();

        const Texture2D backdrop = AssetManager::instance().get_texture("hero_vimana_wars.png");
        if (backdrop.id > 0) {
            const Rectangle src = { 0, 0, static_cast<float>(backdrop.width), static_cast<float>(backdrop.height) };
            const Rectangle dst = { 0, 0, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT) };
            DrawTexturePro(backdrop, src, dst, { 0, 0 }, 0.0f, { 130, 148, 182, 255 });
        }
        DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, { 5, 8, 17, 188 });
        DrawRectangleGradientV(0, 0, SCREEN_WIDTH, 105, { 5, 8, 17, 225 }, { 5, 8, 17, 70 });
        DrawRectangleGradientV(0, 470, SCREEN_WIDTH, 130, { 5, 8, 17, 80 }, { 5, 8, 17, 245 });

        int unlocked_count = 0;
        for (const auto& achievement : ALL_ACHIEVEMENTS) {
            const std::string cloud_id = AchievementSystem::cloud_id_for(achievement.id);
            if (AchievementSystem::instance().is_unlocked(achievement.id) || m_cloud_unlocked.contains(cloud_id)) {
                ++unlocked_count;
            }
        }
        const int total = static_cast<int>(ALL_ACHIEVEMENTS.size());

        const Rectangle header = { 28, 18, 844, 62 };
        UI::DrawElevationPanel(header, UI::ElevationGlass(), false);
        UI::DrawCornerBrackets(header, 10.0f, UI::PAL_PRIMARY);
        UI::DrawStarIcon({ 57, 49 }, 13.0f, UI::PAL_PRIMARY_BRIGHT);
        DrawTextEx(title_font, "TROPHY ARCHIVE", { 82, 27 }, 22, 1.0f, UI::PAL_PRIMARY_BRIGHT);
        DrawTextEx(body_font, "PILOT COMMENDATIONS  //  LOCAL + CLOUD RECORDS", { 83, 54 }, 10, 1.0f, UI::PAL_TEXT_MUTED);

        DrawTextEx(title_font, (std::to_string(unlocked_count) + " / " + std::to_string(total)).c_str(),
                   { 701, 27 }, 20, 1.0f, UI::PAL_PRIMARY_CORE);
        DrawTextEx(body_font, "COMMENDATIONS EARNED", { 701, 52 }, 9, 1.0f, UI::PAL_SECONDARY_BRIGHT);
        const Rectangle overall_bar = { 701, 69, 154, 4 };
        DrawRectangleRec(overall_bar, UI::PAL_OUTLINE_VARIANT);
        DrawRectangleRec({ overall_bar.x, overall_bar.y,
                           overall_bar.width * static_cast<float>(unlocked_count) / std::max(1, total),
                           overall_bar.height }, UI::PAL_PRIMARY_BRIGHT);

        const Rectangle status_panel = { 32, 88, 836, 25 };
        DrawRectangleRec(status_panel, ColorAlpha(UI::PAL_SURFACE_WELL, 0.84f));
        DrawRectangleLinesEx(status_panel, 1.0f, ColorAlpha(UI::PAL_SECONDARY, 0.43f));
        const std::string summary = "SORTIES RECORDED  " + std::to_string(m_match_count) +
                                    "    //    " + std::to_string(total - unlocked_count) + " COMMENDATIONS REMAIN";
        DrawTextEx(body_font, summary.c_str(), { 44, 94 }, 10, 1.0f, UI::PAL_TEXT_VARIANT);
        DrawTextEx(body_font, ("PAGE " + std::to_string(m_page + 1) + " / " + std::to_string(page_count())).c_str(),
                   { 752, 94 }, 10, 1.0f, UI::PAL_PRIMARY_BRIGHT);

        const int first = m_page * ITEMS_PER_PAGE;
        const int last = std::min(first + ITEMS_PER_PAGE, static_cast<int>(ALL_ACHIEVEMENTS.size()));
        for (int index = first; index < last; ++index) {
            const int within_page = index - first;
            const int col = within_page / 4;
            const int row = within_page % 4;
            const Rectangle card = { 32.0f + col * 430.0f, 121.0f + row * 91.0f, 406.0f, 82.0f };
            const auto& achievement = ALL_ACHIEVEMENTS[index];
            const std::string cloud_id = AchievementSystem::cloud_id_for(achievement.id);
            const bool local = AchievementSystem::instance().is_unlocked(achievement.id);
            const bool cloud = m_cloud_unlocked.find(cloud_id) != m_cloud_unlocked.end();
            const bool unlocked = local || cloud;
            const Color accent = unlocked ? UI::PAL_PRIMARY_BRIGHT : UI::PAL_TEXT_MUTED;

            UI::DrawElevationPanel(card, unlocked ? UI::ElevationGlass() : UI::ElevationWell(), false);
            UI::DrawCornerBrackets(card, 7.0f, ColorAlpha(accent, unlocked ? 0.80f : 0.41f));
            DrawCircleV({ card.x + 24.0f, card.y + 24.0f }, 14.0f,
                        ColorAlpha(unlocked ? UI::PAL_PRIMARY : UI::PAL_TEXT_MUTED, unlocked ? 0.16f : 0.10f));
            UI::DrawStarIcon({ card.x + 24.0f, card.y + 24.0f }, 8.5f, accent);
            DrawTextEx(title_font, achievement.title.c_str(), { card.x + 47.0f, card.y + 7.0f },
                       14.0f, 1.0f, unlocked ? UI::PAL_PRIMARY_CORE : UI::PAL_TEXT_VARIANT);
            const std::string source = cloud ? (local ? "LOCAL + CLOUD" : "CLOUD RECORD") : (local ? "LOCAL RECORD" : "LOCKED");
            const std::string category = achievement.category + "  //  " + source;
            DrawTextEx(body_font, category.c_str(), { card.x + 48.0f, card.y + 27.0f }, 9.0f, 1.0f,
                       unlocked ? UI::PAL_SECONDARY_BRIGHT : UI::PAL_TEXT_MUTED);
            DrawTextEx(body_font, achievement.description.c_str(), { card.x + 12.0f, card.y + 45.0f },
                       9.5f, 1.0f, UI::PAL_TEXT_VARIANT);

            const auto progress = progress_for(achievement.id, unlocked);
            const Rectangle bar = { card.x + 12.0f, card.y + 69.0f, card.width - 24.0f, 4.0f };
            DrawRectangleRec(bar, UI::PAL_OUTLINE_VARIANT);
            DrawRectangleRec({ bar.x, bar.y, bar.width * progress.first, bar.height },
                             unlocked ? UI::PAL_PRIMARY_BRIGHT : UI::PAL_SECONDARY_BRIGHT);
            DrawTextEx(body_font, progress.second.c_str(), { card.x + card.width - 116.0f, card.y + 57.0f },
                       8.0f, 1.0f, unlocked ? UI::PAL_PRIMARY_BRIGHT : UI::PAL_TEXT_MUTED);
        }

        DrawTextEx(body_font, m_status.c_str(), { 202, 548 }, 9, 1.0f, UI::PAL_SECONDARY_BRIGHT);
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
        if (id == "BOSS_ARCHIVE") {
            int defeated = 0;
            for (const auto& entry : AchievementSystem::boss_achievement_ids()) {
                const std::string cloud_id = AchievementSystem::cloud_id_for(entry.second);
                if (AchievementSystem::instance().is_unlocked(entry.second) || m_cloud_unlocked.contains(cloud_id)) ++defeated;
            }
            return { static_cast<float>(defeated) / 8.0f, std::to_string(defeated) + "/8 GUARDIANS" };
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
        if (id == "IRON_MODE") return { 0.0f, "CLEAR AN ACT ON CHAKRAVYUHA" };
        if (id == "LEADERBOARD_TOP10") return { 0.0f, "TOP 10 CLOUD RANK" };
        if (id == "ALL_BOONS") return { 0.0f, "COLLECT ALL 9 UNIQUE BOONS" };
        if (id == "COOP_REVIVE") return { 0.0f, "REVIVE A DOWNED SQUADMATE" };
        if (id == "COOP_DUAL_ASTRA") return { 0.0f, "SYNC TWO SQUAD ASTRAS" };
        if (id.rfind("BOSS_", 0) == 0) return { 0.0f, "DEFEAT THE NAMED GUARDIAN" };
        if (id == "FIRST_BLOOD") return { 0.0f, "DESTROY YOUR FIRST ASURA" };
        if (id == "PERFECT_WAVE") return { 0.0f, "CLEAR A WAVE WITHOUT DAMAGE" };
        if (id == "COMBO_25") return { 0.0f, "REACH A X25 COMBO" };
        if (id == "COMBO_50") return { 0.0f, "REACH A X50 COMBO" };
        if (id == "BRAHMASTRA") return { 0.0f, "DETONATE THE BRAHMASTRA" };
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
