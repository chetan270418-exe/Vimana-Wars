#pragma once
#include <cmath>
#include <string>
#include <vector>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"

namespace Vimana::UI {

inline void DrawChamferedPanel(Rectangle rect, Color border, Color fill, float cut = 6.0f, bool selected = false) {
    float x = rect.x;
    float y = rect.y;
    float w = rect.width;
    float h = rect.height;

    // Background fill
    Vector2 points[8] = {
        { x + cut, y },
        { x + w - cut, y },
        { x + w, y + cut },
        { x + w, y + h - cut },
        { x + w - cut, y + h },
        { x + cut, y + h },
        { x, y + h - cut },
        { x, y + cut }
    };

    // Draw solid center
    DrawRectangle(static_cast<int>(x + cut), static_cast<int>(y), static_cast<int>(w - cut * 2), static_cast<int>(h), fill);
    DrawRectangle(static_cast<int>(x), static_cast<int>(y + cut), static_cast<int>(cut), static_cast<int>(h - cut * 2), fill);
    DrawRectangle(static_cast<int>(x + w - cut), static_cast<int>(y + cut), static_cast<int>(cut), static_cast<int>(h - cut * 2), fill);

    // Corner triangles
    DrawTriangle({ x, y + cut }, { x + cut, y }, { x + cut, y + cut }, fill);
    DrawTriangle({ x + w - cut, y }, { x + w, y + cut }, { x + w - cut, y + cut }, fill);
    DrawTriangle({ x + cut, y + h - cut }, { x + cut, y + h }, { x, y + h - cut }, fill);
    DrawTriangle({ x + w - cut, y + h - cut }, { x + w, y + h - cut }, { x + w - cut, y + h }, fill);

    // Border lines
    float thick = selected ? 2.5f : 1.5f;
    for (int i = 0; i < 8; ++i) {
        DrawLineEx(points[i], points[(i + 1) % 8], thick, border);
    }

    if (selected) {
        // Outer glow
        Color glow = border;
        glow.a = 50;
        DrawRectangleLines(static_cast<int>(x - 2), static_cast<int>(y - 2), static_cast<int>(w + 4), static_cast<int>(h + 4), glow);
        glow.a = 25;
        DrawRectangleLines(static_cast<int>(x - 4), static_cast<int>(y - 4), static_cast<int>(w + 8), static_cast<int>(h + 8), glow);
    }
}

inline void DrawGlowBorder(Rectangle rect, Color color, float thickness = 2.0f, float alpha = 0.35f) {
    Color glow = color;
    glow.a = static_cast<unsigned char>(alpha * 255.0f);
    DrawRectangleLinesEx({ rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4 }, thickness, glow);
    glow.a = static_cast<unsigned char>(alpha * 128.0f);
    DrawRectangleLinesEx({ rect.x - 4, rect.y - 4, rect.width + 8, rect.height + 8 }, thickness, glow);
}

inline void DrawCornerEtching(float x, float y, float size, Color color) {
    DrawLineEx({ x, y }, { x + size, y }, 2.0f, color);
    DrawLineEx({ x, y }, { x, y + size }, 2.0f, color);
}

inline void DrawYantraCornerDeco(Rectangle rect, float size, Color color) {
    // 4 decorative Vedic corner brackets with inner notch
    float x = rect.x;
    float y = rect.y;
    float w = rect.width;
    float h = rect.height;

    // Top-Left
    DrawLineEx({ x, y }, { x + size, y }, 2.0f, color);
    DrawLineEx({ x, y }, { x, y + size }, 2.0f, color);
    DrawCircle(static_cast<int>(x + 3), static_cast<int>(y + 3), 1.5f, color);

    // Top-Right
    DrawLineEx({ x + w, y }, { x + w - size, y }, 2.0f, color);
    DrawLineEx({ x + w, y }, { x + w, y + size }, 2.0f, color);
    DrawCircle(static_cast<int>(x + w - 3), static_cast<int>(y + 3), 1.5f, color);

    // Bottom-Left
    DrawLineEx({ x, y + h }, { x + size, y + h }, 2.0f, color);
    DrawLineEx({ x, y + h }, { x, y + h - size }, 2.0f, color);
    DrawCircle(static_cast<int>(x + 3), static_cast<int>(y + h - 3), 1.5f, color);

    // Bottom-Right
    DrawLineEx({ x + w, y + h }, { x + w - size, y + h }, 2.0f, color);
    DrawLineEx({ x + w, y + h }, { x + w, y + h - size }, 2.0f, color);
    DrawCircle(static_cast<int>(x + w - 3), static_cast<int>(y + h - 3), 1.5f, color);
}

inline void DrawYantraPanel(Rectangle rect, Color border, Color fill, float cut = 8.0f, bool glow = false, float glow_alpha = 0.35f) {
    DrawChamferedPanel(rect, border, fill, cut, glow);
    DrawYantraCornerDeco(rect, cut + 6.0f, border);
    if (glow) {
        DrawGlowBorder(rect, border, 1.5f, glow_alpha);
    }
}

// ── PROCEDURAL VECTOR GLYPHS (Resolution-independent & Unicode-safe) ─────────

inline void DrawStarIcon(Vector2 center, float radius, Color color, bool fill = true) {
    // 5-pointed celestial star
    Vector2 pts[10];
    float inner_r = radius * 0.45f;
    float angle_step = 3.14159265f / 5.0f;
    float start_angle = -3.14159265f / 2.0f;

    for (int i = 0; i < 10; ++i) {
        float r = (i % 2 == 0) ? radius : inner_r;
        float a = start_angle + i * angle_step;
        pts[i] = { center.x + std::cos(a) * r, center.y + std::sin(a) * r };
    }

    if (fill) {
        for (int i = 0; i < 10; ++i) {
            DrawTriangle(center, pts[i], pts[(i + 1) % 10], color);
        }
    } else {
        for (int i = 0; i < 10; ++i) {
            DrawLineEx(pts[i], pts[(i + 1) % 10], 1.5f, color);
        }
    }
}

inline void DrawVedicDiamond(Vector2 center, float size, Color color, bool fill = true) {
    Vector2 p1 = { center.x, center.y - size };
    Vector2 p2 = { center.x + size, center.y };
    Vector2 p3 = { center.x, center.y + size };
    Vector2 p4 = { center.x - size, center.y };

    if (fill) {
        DrawTriangle(p1, p4, p2, color);
        DrawTriangle(p3, p2, p4, color);
    } else {
        DrawLineEx(p1, p2, 1.5f, color);
        DrawLineEx(p2, p3, 1.5f, color);
        DrawLineEx(p3, p4, 1.5f, color);
        DrawLineEx(p4, p1, 1.5f, color);
    }
}

inline void DrawPipMeter(Vector2 pos, int current, int max_pips, Color active_col, Color inactive_col, float pip_w = 16.0f, float pip_h = 10.0f, float gap = 4.0f) {
    for (int i = 0; i < max_pips; ++i) {
        Rectangle r = { pos.x + i * (pip_w + gap), pos.y, pip_w, pip_h };
        if (i < current) {
            DrawRectangleRec(r, active_col);
            DrawRectangleLinesEx(r, 1.0f, COLOR_PARCHMENT);
        } else {
            DrawRectangleRec(r, { 25, 30, 45, 200 });
            DrawRectangleLinesEx(r, 1.0f, inactive_col);
        }
    }
}

inline void DrawCircularGauge(Vector2 center, float radius, float progress, Color fill_col, Color track_col, float thickness = 4.0f) {
    // Background circle track
    DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), radius, track_col);

    // Progress arc
    int segments = 36;
    float clamped_prog = std::clamp(progress, 0.0f, 1.0f);
    int active_segs = static_cast<int>(segments * clamped_prog);
    float step = (2.0f * 3.14159265f) / segments;
    float start = -3.14159265f / 2.0f;

    for (int i = 0; i < active_segs; ++i) {
        float a1 = start + i * step;
        float a2 = start + (i + 1) * step;
        Vector2 p1 = { center.x + std::cos(a1) * radius, center.y + std::sin(a1) * radius };
        Vector2 p2 = { center.x + std::cos(a2) * radius, center.y + std::sin(a2) * radius };
        DrawLineEx(p1, p2, thickness, fill_col);
    }
}

inline void DrawLockIcon(Vector2 center, float size, Color color) {
    // Padlock body
    Rectangle body = { center.x - size * 0.7f, center.y, size * 1.4f, size * 1.1f };
    DrawRectangleRec(body, color);
    // Shackle
    Rectangle shackle = { center.x - size * 0.5f, center.y - size * 0.8f, size, size * 0.8f };
    DrawRectangleLinesEx(shackle, 1.5f, color);
    // Keyhole
    DrawCircle(static_cast<int>(center.x), static_cast<int>(center.y + size * 0.45f), size * 0.22f, COLOR_OBSIDIAN);
}

inline void DrawCheckmarkIcon(Vector2 center, float size, Color color) {
    Vector2 p1 = { center.x - size * 0.7f, center.y };
    Vector2 p2 = { center.x - size * 0.15f, center.y + size * 0.6f };
    Vector2 p3 = { center.x + size * 0.8f, center.y - size * 0.6f };
    DrawLineEx(p1, p2, 2.5f, color);
    DrawLineEx(p2, p3, 2.5f, color);
}

inline void DrawWarningIcon(Vector2 center, float size, Color color) {
    Vector2 p1 = { center.x, center.y - size };
    Vector2 p2 = { center.x + size, center.y + size };
    Vector2 p3 = { center.x - size, center.y + size };
    DrawTriangleLines(p1, p3, p2, color);
    DrawLineEx({ center.x, center.y - size * 0.3f }, { center.x, center.y + size * 0.3f }, 2.0f, color);
    DrawCircle(static_cast<int>(center.x), static_cast<int>(center.y + size * 0.65f), 1.5f, color);
}

// ── TYPOGRAPHY & OVERLAYS ───────────────────────────────────────────────────

inline void DrawVedicHeading(Font font, const std::string& text, Vector2 pos, float size, Color main_col, Color shadow_col = { 0, 0, 0, 180 }) {
    DrawTextEx(font, text.c_str(), { pos.x + 2, pos.y + 2 }, size, 1.0f, shadow_col);
    DrawTextEx(font, text.c_str(), pos, size, 1.0f, main_col);
}

inline void DrawVedicHeadingCentered(Font font, const std::string& text, float y, float size, Color main_col, Color shadow_col = { 0, 0, 0, 180 }) {
    Vector2 sz = MeasureTextEx(font, text.c_str(), size, 1.0f);
    Vector2 pos = { (SCREEN_WIDTH - sz.x) / 2.0f, y };
    DrawVedicHeading(font, text, pos, size, main_col, shadow_col);
}

inline void DrawTooltip(Vector2 pos, const std::string& title, const std::string& desc, Font title_font, Font body_font) {
    Vector2 t_sz = MeasureTextEx(title_font, title.c_str(), 14, 1.0f);
    Vector2 d_sz = MeasureTextEx(body_font, desc.c_str(), 12, 1.0f);
    float box_w = std::max(t_sz.x, d_sz.x) + 24.0f;
    float box_h = t_sz.y + d_sz.y + 18.0f;

    // Keep tooltip on screen
    if (pos.x + box_w > SCREEN_WIDTH - 10) pos.x = SCREEN_WIDTH - box_w - 10;
    if (pos.y + box_h > SCREEN_HEIGHT - 10) pos.y = SCREEN_HEIGHT - box_h - 10;

    Rectangle tip_box = { pos.x, pos.y, box_w, box_h };
    DrawChamferedPanel(tip_box, COLOR_GOLD_BRIGHT, COLOR_SURFACE_HIGH, 4.0f, true);
    DrawTextEx(title_font, title.c_str(), { pos.x + 12, pos.y + 6 }, 14, 1.0f, COLOR_GOLD_BRIGHT);
    DrawTextEx(body_font, desc.c_str(), { pos.x + 12, pos.y + 8 + t_sz.y }, 12, 1.0f, COLOR_PARCHMENT);
}

inline void DrawScanlines() {
    // Subtle CRT scanline effect
    for (int y = 0; y < SCREEN_HEIGHT; y += 4) {
        DrawLine(0, y, SCREEN_WIDTH, y, { 0, 0, 0, 18 });
    }
}

} // namespace Vimana::UI
