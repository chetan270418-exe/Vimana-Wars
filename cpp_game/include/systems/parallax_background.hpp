#pragma once
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "systems/asset_manager.hpp"

namespace Vimana {

class ParallaxBackground {
public:
    static ParallaxBackground& instance() {
        static ParallaxBackground bg;
        return bg;
    }

    void init() {
        m_stars_far.clear();
        m_stars_mid.clear();
        m_debris.clear();

        // 1. Far Stars (Layer 2)
        for (int i = 0; i < 70; ++i) {
            m_stars_far.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                0.8f + (std::rand() % 10) / 10.0f
            });
        }

        // 2. Mid Stars (Layer 3)
        for (int i = 0; i < 50; ++i) {
            m_stars_mid.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                1.5f + (std::rand() % 12) / 10.0f
            });
        }

        // 3. Near Floating Cosmic Debris / Yantra Shards (Layer 4)
        for (int i = 0; i < 25; ++i) {
            m_debris.push_back({
                static_cast<float>(std::rand() % SCREEN_WIDTH),
                static_cast<float>(std::rand() % SCREEN_HEIGHT),
                2.5f + (std::rand() % 20) / 10.0f,
                static_cast<float>((std::rand() % 360))
            });
        }

        m_bg_offset_y = 0.0f;
        m_active_realm_id = -1;
    }

    void set_realm(const RealmData& realm) {
        if (m_active_realm_id == realm.id) return;
        m_active_realm_id = realm.id;

        // Map realm to image
        switch (realm.id) {
            case 1: m_texture_key = "realm_swarga.png"; break;
            case 2: m_texture_key = "realm_kshira_sagara.png"; break;
            case 3: m_texture_key = "realm_dandaka_void.png"; break;
            case 4: m_texture_key = "realm_lanka_approach.png"; break;
            case 5: m_texture_key = "realm_setu_expanse.png"; break;
            case 6: m_texture_key = "realm_naraka_forge.png"; break;
            case 7: m_texture_key = "realm_mahayuddha_citadel.png"; break;
            default: m_texture_key = "realm_swarga.png"; break;
        }
        m_realm_color = realm.accent_color;
    }

    void update(float dt, Vector2 player_vel = { 0, 0 }) {
        float base_speed = 30.0f;
        float p_dy = player_vel.y * 0.05f;

        // Layer 1 Background Texture scroll
        m_bg_offset_y += (base_speed * 0.35f + p_dy * 0.2f) * dt;
        if (m_bg_offset_y >= SCREEN_HEIGHT) m_bg_offset_y -= SCREEN_HEIGHT;

        // Layer 2 Far Stars
        for (auto& s : m_stars_far) {
            s.y += (base_speed * 0.6f + p_dy * 0.3f) * dt;
            if (s.y > SCREEN_HEIGHT) { s.y = 0; s.x = static_cast<float>(std::rand() % SCREEN_WIDTH); }
            else if (s.y < 0) { s.y = SCREEN_HEIGHT; s.x = static_cast<float>(std::rand() % SCREEN_WIDTH); }
        }

        // Layer 3 Mid Stars
        for (auto& s : m_stars_mid) {
            s.y += (base_speed * 1.2f + p_dy * 0.6f) * dt;
            if (s.y > SCREEN_HEIGHT) { s.y = 0; s.x = static_cast<float>(std::rand() % SCREEN_WIDTH); }
            else if (s.y < 0) { s.y = SCREEN_HEIGHT; s.x = static_cast<float>(std::rand() % SCREEN_WIDTH); }
        }

        // Layer 4 Cosmic Debris
        for (auto& d : m_debris) {
            d.y += (base_speed * 1.8f + p_dy * 0.9f) * dt;
            d.rot += 15.0f * dt;
            if (d.y > SCREEN_HEIGHT) { d.y = 0; d.x = static_cast<float>(std::rand() % SCREEN_WIDTH); }
            else if (d.y < 0) { d.y = SCREEN_HEIGHT; d.x = static_cast<float>(std::rand() % SCREEN_WIDTH); }
        }
    }

    void draw() const {
        // Layer 1: Realm Background Texture (Rendered with vertical wrap)
        Texture2D tex = AssetManager::instance().get_texture(m_texture_key);
        if (tex.id > 0) {
            float y1 = m_bg_offset_y;
            float y2 = m_bg_offset_y - SCREEN_HEIGHT;

            Rectangle src = { 0, 0, static_cast<float>(tex.width), static_cast<float>(tex.height) };
            Rectangle dest1 = { 0, y1, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT) };
            Rectangle dest2 = { 0, y2, static_cast<float>(SCREEN_WIDTH), static_cast<float>(SCREEN_HEIGHT) };

            DrawTexturePro(tex, src, dest1, { 0, 0 }, 0.0f, WHITE);
            DrawTexturePro(tex, src, dest2, { 0, 0 }, 0.0f, WHITE);
        } else {
            ClearBackground(COLOR_OBSIDIAN);
        }

        // Layer 2: Far Stars
        for (const auto& s : m_stars_far) {
            DrawCircle(static_cast<int>(s.x), static_cast<int>(s.y), s.z, { 180, 210, 255, 140 });
        }

        // Layer 3: Mid Stars with subtle realm tint
        Color mid_col = m_realm_color;
        mid_col.a = 180;
        for (const auto& s : m_stars_mid) {
            DrawCircle(static_cast<int>(s.x), static_cast<int>(s.y), s.z, mid_col);
        }

        // Layer 4: Floating Yantra Shards
        for (const auto& d : m_debris) {
            Color d_col = COLOR_GOLD;
            d_col.a = 110;
            // Draw small rotating diamond
            float sz = d.z * 2.0f;
            DrawRectanglePro({ d.x, d.y, sz, sz }, { sz / 2.0f, sz / 2.0f }, d.rot, d_col);
        }

        // Layer 5: Atmospheric Realm Ambient Light Gradient
        DrawRectangleGradientV(0, 0, SCREEN_WIDTH, 80, ColorAlpha(COLOR_OBSIDIAN, 0.4f), ColorAlpha(COLOR_OBSIDIAN, 0.0f));
        DrawRectangleGradientV(0, SCREEN_HEIGHT - 90, SCREEN_WIDTH, 90, ColorAlpha(COLOR_OBSIDIAN, 0.0f), ColorAlpha(COLOR_OBSIDIAN, 0.5f));
    }

private:
    ParallaxBackground() = default;
    ~ParallaxBackground() = default;

    struct Star { float x, y, z; };
    struct Debris { float x, y, z, rot; };

    std::vector<Star> m_stars_far;
    std::vector<Star> m_stars_mid;
    std::vector<Debris> m_debris;

    std::string m_texture_key = "realm_swarga.png";
    Color m_realm_color = COLOR_GOLD_BRIGHT;
    int m_active_realm_id = -1;
    float m_bg_offset_y = 0.0f;
};

} // namespace Vimana
