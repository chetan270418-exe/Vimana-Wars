#pragma once
#include <string>
#include <functional>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/sound_system.hpp"

namespace Vimana::UI {

class Button {
public:
    Button() : m_rect{ 0, 0, 100, 30 }, m_label(""), m_color(COLOR_GOLD), m_hovered(false), m_pressed(false), m_disabled(false), m_shortcut("") {}

    Button(Rectangle rect, const std::string& label, Color color = COLOR_GOLD, const std::string& shortcut = "")
        : m_rect(rect), m_label(label), m_color(color), m_hovered(false), m_pressed(false), m_disabled(false), m_shortcut(shortcut) {}

    bool update(Vector2 mouse_pos) {
        if (m_disabled) {
            m_hovered = false;
            m_pressed = false;
            return false;
        }

        bool prev_hover = m_hovered;
        m_hovered = CheckCollisionPointRec(mouse_pos, m_rect);

        if (m_hovered && !prev_hover) {
            SoundSystem::instance().play_sfx("ui_click.wav", 0.35f);
        }

        m_pressed = m_hovered && IsMouseButtonPressed(MOUSE_BUTTON_LEFT);
        if (m_pressed) {
            SoundSystem::instance().play_sfx("ui_click.wav", 0.75f);
        }
        return m_pressed;
    }

    void draw(Font font) const {
        if (m_disabled) {
            DrawChamferedPanel(m_rect, { 60, 65, 80, 255 }, { 15, 18, 25, 220 }, 5.0f, false);
            int font_size = 17;
            Vector2 text_size = MeasureTextEx(font, m_label.c_str(), static_cast<float>(font_size), 1.0f);
            Vector2 text_pos = {
                m_rect.x + (m_rect.width - text_size.x) / 2.0f,
                m_rect.y + (m_rect.height - text_size.y) / 2.0f
            };
            DrawTextEx(font, m_label.c_str(), text_pos, static_cast<float>(font_size), 1.0f, COLOR_MUTED);
            return;
        }

        Color border = m_hovered ? COLOR_GOLD_BRIGHT : m_color;
        Color fill = m_hovered ? COLOR_SURFACE_HIGH : COLOR_SURFACE_LOW;

        DrawYantraPanel(m_rect, border, fill, 5.0f, m_hovered, 0.45f);

        // Center text
        int font_size = 17;
        Vector2 text_size = MeasureTextEx(font, m_label.c_str(), static_cast<float>(font_size), 1.0f);
        Vector2 text_pos = {
            m_rect.x + (m_rect.width - text_size.x) / 2.0f,
            m_rect.y + (m_rect.height - text_size.y) / 2.0f
        };

        Color text_color = m_hovered ? COLOR_GOLD_BRIGHT : COLOR_PARCHMENT;
        DrawTextEx(font, m_label.c_str(), text_pos, static_cast<float>(font_size), 1.0f, text_color);

        // Draw shortcut badge if present
        if (!m_shortcut.empty()) {
            Vector2 sc_sz = MeasureTextEx(font, m_shortcut.c_str(), 11, 1.0f);
            DrawTextEx(font, m_shortcut.c_str(), { m_rect.x + m_rect.width - sc_sz.x - 10, m_rect.y + (m_rect.height - sc_sz.y) / 2.0f }, 11, 1.0f, m_hovered ? COLOR_CYAN_BRIGHT : COLOR_MUTED);
        }
    }

    void set_rect(Rectangle r) { m_rect = r; }
    void set_label(const std::string& l) { m_label = l; }
    void set_color(Color c) { m_color = c; }
    void set_disabled(bool d) { m_disabled = d; }
    void set_shortcut(const std::string& sc) { m_shortcut = sc; }
    const Rectangle& rect() const { return m_rect; }
    bool is_hovered() const { return m_hovered; }
    bool is_disabled() const { return m_disabled; }

private:
    Rectangle m_rect;
    std::string m_label;
    Color m_color;
    bool m_hovered;
    bool m_pressed;
    bool m_disabled;
    std::string m_shortcut;
};

} // namespace Vimana::UI
