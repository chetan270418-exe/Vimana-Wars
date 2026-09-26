#pragma once
#include <algorithm>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "systems/sound_system.hpp"
#include "ui/vedic_theme.hpp"

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
        SoundSystem::instance().play_door_close();
    }

    // Returns true on the exact frame the view should switch
    bool update(float dt, ViewType& out_next_view) {
        if (!m_in_transition || dt <= 0.0f) return false;

        m_timer += dt;
        float half_dur = m_duration * 0.5f;

        if (!m_midpoint_reached && m_timer >= half_dur) {
            m_midpoint_reached = true;
            out_next_view = m_target;
            SoundSystem::instance().play_door_open();
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
            const float t = std::clamp(m_timer / half_dur, 0.0f, 1.0f);
            alpha = t * t * (3.0f - 2.0f * t);
        } else {
            // Fading in from black
            const float t = std::clamp((m_timer - half_dur) / half_dur, 0.0f, 1.0f);
            const float eased = t * t * (3.0f - 2.0f * t);
            alpha = 1.0f - eased;
        }

        Color fade_col = { 8, 10, 15, static_cast<unsigned char>(alpha * 240) };
        DrawRectangle(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, fade_col);

        // Mandala reticle marks the switch point; eased opacity avoids a hard pop.
        if (alpha > 0.15f) {
            const float visibility = std::clamp((alpha - 0.15f) / 0.85f, 0.0f, 1.0f);
            const float ring_radius = 48.0f + (1.0f - alpha) * 76.0f;
            UI::DrawMandalaReticle({ SCREEN_WIDTH * 0.5f, SCREEN_HEIGHT * 0.5f },
                                   ring_radius, GetTime() * 0.8,
                                   COLOR_CYAN_BRIGHT, COLOR_GOLD_BRIGHT,
                                   visibility * 0.55f);
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
