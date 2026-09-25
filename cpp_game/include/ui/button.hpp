#pragma once
#include <string>
#include <functional>
#include <algorithm>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "ui/design_tokens.hpp"
#include "ui/vedic_theme.hpp"
#include "systems/sound_system.hpp"

namespace Vimana::UI {

// ── DESIGN-SYSTEM BUTTON ─────────────────────────────────────────────────────
// Per the Vimana Wars design spec:
//   - Chamfered 8-point polygon with 1px border
//   - Height 44px (compact 36px)
//   - Primary (Divine Gold):  bg rgba(gold,.12), border rgba(gold,.85), text #FFF6DF
//     - Hover: bg rgba(gold,.28), scale 1.02x, glow expands to 20px
//     - Pressed: scale 0.98x, solid gold flash
//   - Trailing shortcut badge in JetBrains Mono style
//   - Focus ring for keyboard navigation
class Button {
public:
    Button()
        : m_rect{ 0, 0, 100, 30 }, m_label(""), m_color(COLOR_GOLD),
          m_kind(ButtonKind::PRIMARY), m_hovered(false), m_pressed(false),
          m_disabled(false), m_focused(false), m_shortcut(""),
          m_hover_anim(0.0f), m_press_anim(0.0f) {}

    Button(Rectangle rect, const std::string& label, Color color = COLOR_GOLD,
           const std::string& shortcut = "", ButtonKind kind = ButtonKind::PRIMARY)
        : m_rect(rect), m_label(label), m_color(color), m_kind(kind),
          m_hovered(false), m_pressed(false), m_disabled(false),
          m_focused(false), m_shortcut(shortcut),
          m_hover_anim(0.0f), m_press_anim(0.0f) {}

    bool update(Vector2 mouse_pos) {
        if (m_disabled) {
            m_hovered = false;
            m_pressed = false;
            m_hover_anim *= 0.85f;
            m_press_anim *= 0.85f;
            return false;
        }

        bool prev_hover = m_hovered;
        m_hovered = CheckCollisionPointRec(mouse_pos, m_rect);

        // Smooth hover anim (0 -> 1 on enter, 1 -> 0 on leave)
        float target = m_hovered ? 1.0f : 0.0f;
        m_hover_anim += (target - m_hover_anim) * 0.25f;

        if (m_hovered && !prev_hover) {
            SoundSystem::instance().play_sfx("ui_click.wav", 0.35f);
        }

        m_pressed = m_hovered && IsMouseButtonPressed(MOUSE_BUTTON_LEFT);
        if (m_pressed) {
            m_press_anim = 1.0f;
            SoundSystem::instance().play_sfx("ui_click.wav", 0.75f);
        }
        // Decay press anim back to 0
        m_press_anim *= 0.80f;

        // Tab-key focus tracking (rough: any tab press focuses first interactive
        // element in view; views can call set_focused() explicitly).
        return m_pressed;
    }

    void draw(Font font) const {
        // ── Compute scaled rect (transform-only, never shifts layout because
        //    we draw from the same origin each frame).
        //    Disabled = 1.0x, Idle = 1.0x, Hover = 1.0..1.02, Pressed = 1.0..0.98
        float scale = 1.0f
            + 0.02f * m_hover_anim     // hover expands
            - 0.04f * m_press_anim;    // press contracts
        Rectangle r = scale_rect_about_center(m_rect, scale);

        // ── Resolve visual tokens for current kind
        ButtonVisual v = GetButtonVisual(m_kind);

        if (m_disabled) {
            DrawChamferedPanel(r, { 60, 65, 80, 255 }, { 15, 18, 25, 220 }, 5.0f, false);
            draw_label(font, r, COLOR_MUTED);
            return;
        }

        // Background fill: lerp from idle to hover
        Color fill;
        fill.r = (unsigned char)(v.fill_idle.r + (v.fill_hover.r - v.fill_idle.r) * m_hover_anim);
        fill.g = (unsigned char)(v.fill_idle.g + (v.fill_hover.g - v.fill_idle.g) * m_hover_anim);
        fill.b = (unsigned char)(v.fill_idle.b + (v.fill_hover.b - v.fill_idle.b) * m_hover_anim);
        fill.a = (unsigned char)(v.fill_idle.a + (v.fill_hover.a - v.fill_idle.a) * m_hover_anim);

        // Solid gold flash on press
        if (m_press_anim > 0.05f) {
            fill = v.border;
            fill.a = (unsigned char)(255.0f * m_press_anim);
        }

        // Glow halo (idle: 12px, hover: 20px). Additive alpha.
        if (m_hover_anim > 0.01f) {
            float glow_alpha = v.glow_strength * m_hover_anim * 0.55f;
            Color g = v.border;
            g.a = (unsigned char)(255.0f * glow_alpha);
            DrawRectangleLinesEx({ r.x - 6, r.y - 6, r.width + 12, r.height + 12 }, 1.0f, g);
            g.a = (unsigned char)(128.0f * glow_alpha);
            DrawRectangleLinesEx({ r.x - 12, r.y - 12, r.width + 24, r.height + 24 }, 1.0f, g);
        }

        // Panel body with proper chamfer per kind
        DrawChamferedPanel(r, v.border, fill, 5.0f, m_hover_anim > 0.5f);

        // L-bracket corner reinforcement (only on hover, for visual interest)
        if (m_hover_anim > 0.4f) {
            DrawCornerBrackets(r, 6.0f, v.border);
        }

        // Keyboard focus ring
        if (m_focused || (m_hover_anim > 0.7f && m_hovered)) {
            Color focus = v.border;
            focus.a = 200;
            DrawRectangleLinesEx({ r.x - 2, r.y - 2, r.width + 4, r.height + 4 }, 1.5f, focus);
        }

        // Text — color lerps on hover
        Color text_col;
        text_col.r = (unsigned char)(v.text.r + (v.text_hover.r - v.text.r) * m_hover_anim);
        text_col.g = (unsigned char)(v.text.g + (v.text_hover.g - v.text.g) * m_hover_anim);
        text_col.b = (unsigned char)(v.text.b + (v.text_hover.b - v.text.b) * m_hover_anim);
        text_col.a = 255;
        draw_label(font, r, text_col);

        // Trailing shortcut badge (JetBrains Mono style, slate border)
        if (!m_shortcut.empty()) {
            Vector2 sc_sz = MeasureTextEx(font, m_shortcut.c_str(), 10, 1.0f);
            float pad_x = 6.0f, pad_y = 3.0f;
            Rectangle badge = {
                r.x + r.width - sc_sz.x - pad_x * 2 - 6,
                r.y + (r.height - sc_sz.y) / 2.0f - pad_y + 1,
                sc_sz.x + pad_x * 2,
                sc_sz.y + pad_y * 2
            };
            DrawRectangleRec(badge, { 0x0E, 0x13, 0x20, 220 });
            DrawRectangleLinesEx(badge, 1.0f, PAL_OUTLINE_VARIANT);
            Color sc_col = m_hover_anim > 0.5f ? PAL_SECONDARY_BRIGHT : PAL_TEXT_MUTED;
            DrawTextEx(font, m_shortcut.c_str(), { badge.x + pad_x, badge.y + pad_y }, 10, 1.0f, sc_col);
        }
    }

    // Setters
    void set_rect(Rectangle r) { m_rect = r; }
    void set_label(const std::string& l) { m_label = l; }
    void set_color(Color c) { m_color = c; }
    void set_kind(ButtonKind k) { m_kind = k; }
    void set_disabled(bool d) { m_disabled = d; }
    void set_shortcut(const std::string& sc) { m_shortcut = sc; }
    void set_focused(bool f) { m_focused = f; }

    // Getters
    const Rectangle& rect() const { return m_rect; }
    bool is_hovered() const { return m_hovered; }
    bool is_disabled() const { return m_disabled; }
    bool is_focused() const { return m_focused; }
    ButtonKind kind() const { return m_kind; }

private:
    // Helper: scale a rectangle around its center; pure transform, no layout shift.
    static Rectangle scale_rect_about_center(Rectangle r, float s) {
        float cx = r.x + r.width * 0.5f;
        float cy = r.y + r.height * 0.5f;
        float nw = r.width * s;
        float nh = r.height * s;
        return { cx - nw * 0.5f, cy - nh * 0.5f, nw, nh };
    }

    // Helper: center-draw the label, accounting for shortcut badge width.
    void draw_label(Font font, Rectangle r, Color col) const {
        int font_size = 17;
        float label_w = MeasureTextEx(font, m_label.c_str(), static_cast<float>(font_size), 1.0f).x;
        float shortcut_w = 0.0f;
        if (!m_shortcut.empty()) {
            shortcut_w = MeasureTextEx(font, m_shortcut.c_str(), 10, 1.0f).x + 18.0f;
        }
        float total_w = label_w + shortcut_w;
        float start_x = r.x + (r.width - total_w) / 2.0f;
        Vector2 text_pos = { start_x, r.y + (r.height - font_size) / 2.0f };
        DrawTextEx(font, m_label.c_str(), text_pos, static_cast<float>(font_size), 1.0f, col);
    }

    Rectangle m_rect;
    std::string m_label;
    Color m_color;            // legacy fallback (kept for any old callers)
    ButtonKind m_kind;
    bool m_hovered;
    bool m_pressed;
    bool m_disabled;
    bool m_focused;
    std::string m_shortcut;
    mutable float m_hover_anim;   // smoothed hover state 0..1
    mutable float m_press_anim;   // press flash 0..1
};

} // namespace Vimana::UI