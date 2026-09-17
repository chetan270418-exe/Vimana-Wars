#pragma once
#include "raylib.h"
#include "core/constants.hpp"
#include "views/view_interface.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/asset_manager.hpp"

namespace Vimana {

class DifficultyView : public IView {
public:
    DifficultyView() : m_next_view(ViewType::DIFFICULTY_SELECT), m_difficulty(Difficulty::NORMAL) {
        init();
    }

    void init() override {
        m_next_view = ViewType::DIFFICULTY_SELECT;
        float cx = SCREEN_WIDTH / 2.0f - 130.0f;
        m_btn_easy = UI::Button({ cx, 180, 260, 42 }, "EASY // SADHAKA", COLOR_GREEN_BRIGHT);
        m_btn_normal = UI::Button({ cx, 240, 260, 42 }, "NORMAL // KSHATRIYA", COLOR_GOLD_BRIGHT);
        m_btn_hard = UI::Button({ cx, 300, 260, 42 }, "HARD // ASURA SLAYER", COLOR_RED_BRIGHT);
        m_btn_back = UI::Button({ cx, 380, 260, 40 }, "BACK", COLOR_MUTED);
    }

    void update(float dt, Vector2 mouse_pos) override {
        if (m_btn_easy.update(mouse_pos)) {
            m_difficulty = Difficulty::EASY;
            m_next_view = ViewType::SHIP_SELECT;
        } else if (m_btn_normal.update(mouse_pos)) {
            m_difficulty = Difficulty::NORMAL;
            m_next_view = ViewType::SHIP_SELECT;
        } else if (m_btn_hard.update(mouse_pos)) {
            m_difficulty = Difficulty::HARD;
            m_next_view = ViewType::SHIP_SELECT;
        } else if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::MENU;
        }
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font font = AssetManager::instance().font();

        const char* title = "SELECT CAMPAIGN DIFFICULTY";
        Vector2 sz = MeasureTextEx(font, title, 26, 1.0f);
        DrawTextEx(font, title, { (SCREEN_WIDTH - sz.x) / 2.0f, 100 }, 26, 1.0f, COLOR_GOLD_BRIGHT);

        m_btn_easy.draw(font);
        m_btn_normal.draw(font);
        m_btn_hard.draw(font);
        m_btn_back.draw(font);

        UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::DIFFICULTY_SELECT; }
    Difficulty selected_difficulty() const { return m_difficulty; }

private:
    ViewType m_next_view;
    Difficulty m_difficulty;
    UI::Button m_btn_easy;
    UI::Button m_btn_normal;
    UI::Button m_btn_hard;
    UI::Button m_btn_back;
};

} // namespace Vimana
