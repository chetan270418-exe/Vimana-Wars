#pragma once
#include <string>
#include <functional>
#include "raylib.h"
#include "core/constants.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/sound_system.hpp"

namespace Vimana::UI {

class Button {
public:
    Button() : m_rect{ 0, 0, 100, 30 }, m_label(""), m_color(COLOR_GOLD), m_hovered(false), m_pressed(false) {}

    Button(Rectangle rect, const std::string& label, Color color = COLOR_GOLD)
        : m_rect(rect), m_label(label), m_color(color), m_hovered(false), m_pressed(false) {}

    bool update(Vector2 mouse_pos) {
        bool prev_hover = m_hovered;
        m_hovered = CheckCollisionPointRec(mouse_pos, m_rect);

        if (m_hovered && !prev_hover) {
            SoundSystem::instance().play_sfx("ui_click.wav", 0.35f);
        }

        m_pressed = m_hovered && IsMouseButtonPressed(MOUSE_BUTTON_LEFT);
        if (m_pressed) {
            SoundSystem::instance().play_sfx("ui_click.wav", 0.7f);
        }
        return m_pressed;
    }

    void draw(Font font) const {
        Color border = m_hovered ? COLOR_GOLD_BRIGHT : m_color;
        Color fill = m_hovered ? COLOR_SURFACE_HIGH : COLOR_SURFACE_LOW;

        DrawChamferedPanel(m_rect, border, fill, 5.0f, m_hovered);

        // Center text
        int font_size = 18;
        Vector2 text_size = MeasureTextEx(font, m_label.c_str(), static_cast<float>(font_size), 1.0f);
        Vector2 text_pos = {
            m_rect.x + (m_rect.width - text_size.x) / 2.0f,
            m_rect.y + (m_rect.height - text_size.y) / 2.0f
        };

        Color text_color = m_hovered ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT;
        DrawTextEx(font, m_label.c_str(), text_pos, static_cast<float>(font_size), 1.0f, text_color);
    }

    void set_rect(Rectangle r) { m_rect = r; }
    void set_label(const std::string& l) { m_label = l; }
    void set_color(Color c) { m_color = c; }
    const Rectangle& rect() const { return m_rect; }
    bool is_hovered() const { return m_hovered; }

private:
    Rectangle m_rect;
    std::string m_label;
    Color m_color;
    bool m_hovered;
    bool m_pressed;
};

} // namespace Vimana::UI
