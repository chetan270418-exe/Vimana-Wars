#pragma once
#include <algorithm>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"

namespace Vimana {

class TransitionManager {
public:
    static TransitionManager& instance() {
        static TransitionManager tm;
        return tm;
    }

    void start_transition(ViewType target_view, float duration = 0.25f) {
        if (m_in_transition && m_target == target_view) return;
        m_in_transition = true;
        m_duration = duration > 0.05f ? duration : 0.25f;
        m_timer = 0.0f;
        m_target = target_view;
        m_midpoint_reached = false;
    }

    // Returns true on the exact frame the view should switch
    bool update(float dt, ViewType& out_next_view) {
        if (!m_in_transition) return false;

        m_timer += dt;
        float half_dur = m_duration * 0.5f;

        if (!m_midpoint_reached && m_timer >= half_dur) {
            m_midpoint_reached = true;
            out_next_view = m_target;
            return true;
        }

        if (m_timer >= m_duration) {
            m_in_transition = false;
            m_timer = 0.0f;
            m_midpoint_reached = false;
        }

        return false;
    }

    void draw() const {
        if (!m_in_transition) return;

        float half_dur = m_duration * 0.5f;
        float alpha = 0.0f;

        if (m_timer < half_dur) {
            // Fading out to black
            alpha = std::clamp(m_timer / half_dur, 0.0f, 1.0f);
        } else {
            // Fading in from black
            alpha = std::clamp(1.0f - ((m_timer - half_dur) / half_dur), 0.0f, 1.0f);
        }

        Color fade_col = { 8, 10, 15, static_cast<unsigned char>(alpha * 240) };
        DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fade_col);

        // Subtle expanding/contracting golden yantra ring at midpoint
        if (alpha > 0.3f) {
            float ring_r = 40.0f + (1.0f - alpha) * 100.0f;
            Color ring_col = COLOR_GOLD_BRIGHT;
            ring_col.a = static_cast<unsigned char>((alpha - 0.3f) * 120.0f);
            DrawCircleLines(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, ring_r, ring_col);
        }
    }

    bool is_transitioning() const { return m_in_transition; }

private:
    TransitionManager() = default;
    ~TransitionManager() = default;

    bool m_in_transition = false;
    bool m_midpoint_reached = false;
    float m_timer = 0.0f;
    float m_duration = 0.25f;
    ViewType m_target = ViewType::BOOT;
};

} // namespace Vimana
