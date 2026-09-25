#pragma once
#include <cmath>
#include <string>
#include <vector>
#include <algorithm>
#include "raylib.h"
#include "core/constants.hpp"
#include "ui/design_tokens.hpp"   // ElevationStyle, PAL_*, Type, Space, Chamfer

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

// ════════════════════════════════════════════════════════════════════════════
// DESIGN-SYSTEM COMPONENTS  (see design_tokens.hpp)
// ════════════════════════════════════════════════════════════════════════════

// ── 12px CHAMFER FOR LARGE PANELS (cockpit enclosures, hangar cards) ──────────
// Per design spec: large panels use 12px beveled corners. Identical fill
// algorithm to DrawChamferedPanel, just a larger cut and glow halo.
inline void DrawChamferedPanel12(Rectangle rect, Color border, Color fill, bool focused = false) {
    const float cut = Chamfer::LARGE;
    float x = rect.x, y = rect.y, w = rect.width, h = rect.height;
    if (w < cut * 2 + 2 || h < cut * 2 + 2) {
        DrawChamferedPanel(rect, border, fill, 6.0f, focused);
        return;
    }

    Vector2 points[8] = {
        { x + cut, y }, { x + w - cut, y }, { x + w, y + cut }, { x + w, y + h - cut },
        { x + w - cut, y + h }, { x + cut, y + h }, { x, y + h - cut }, { x, y + cut }
    };
    DrawRectangle(static_cast<int>(x + cut), static_cast<int>(y), static_cast<int>(w - cut * 2), static_cast<int>(h), fill);
    DrawRectangle(static_cast<int>(x), static_cast<int>(y + cut), static_cast<int>(cut), static_cast<int>(h - cut * 2), fill);
    DrawRectangle(static_cast<int>(x + w - cut), static_cast<int>(y + cut), static_cast<int>(cut), static_cast<int>(h - cut * 2), fill);
    DrawTriangle({ x, y + cut }, { x + cut, y }, { x + cut, y + cut }, fill);
    DrawTriangle({ x + w - cut, y }, { x + w, y + cut }, { x + w - cut, y + cut }, fill);
    DrawTriangle({ x + cut, y + h - cut }, { x + cut, y + h }, { x, y + h - cut }, fill);
    DrawTriangle({ x + w - cut, y + h - cut }, { x + w, y + h - cut }, { x + w - cut, y + h }, fill);

    float thick = focused ? 2.5f : 1.5f;
    for (int i = 0; i < 8; ++i) {
        DrawLineEx(points[i], points[(i + 1) % 8], thick, border);
    }
    if (focused) {
        Color g = border; g.a = 50;
        DrawRectangleLinesEx({ x - 4, y - 4, w + 8, h + 8 }, 1.0f, g);
        g.a = 25;
        DrawRectangleLinesEx({ x - 8, y - 8, w + 16, h + 16 }, 1.0f, g);
    }
}

// ── ELEVATION PANEL ──────────────────────────────────────────────────────────
// Draw a panel using an ElevationStyle from design_tokens.hpp. Automatically
// applies the right chamfer cut and CRT scanline texture.
inline void DrawElevationPanel(Rectangle rect, ElevationStyle style, bool focused = false) {
    DrawChamferedPanel12(rect, style.border, style.fill, focused);

    // Subtle 3% opacity horizontal scanlines over the panel
    Color scan = { 0, 0, 0, 10 };
    for (int y = static_cast<int>(rect.y); y < static_cast<int>(rect.y + rect.height); y += 4) {
        DrawLine(static_cast<int>(rect.x), y, static_cast<int>(rect.x + rect.width), y, scan);
    }
}

// ── CORNER BRACKETS WITH DIAMOND RIVETS ──────────────────────────────────────
// L-bracket frame on each corner + small diamond rivet inset. Brass by default.
inline void DrawCornerBrackets(Rectangle rect, float size, Color color) {
    float x = rect.x, y = rect.y, w = rect.width, h = rect.height;
    float thick = 1.5f;

    // Top-Left L-bracket
    DrawLineEx({ x, y }, { x + size, y }, thick, color);
    DrawLineEx({ x, y }, { x, y + size }, thick, color);
    DrawVedicDiamond({ x + 4, y + 4 }, 2.0f, color);

    // Top-Right
    DrawLineEx({ x + w, y }, { x + w - size, y }, thick, color);
    DrawLineEx({ x + w, y }, { x + w, y + size }, thick, color);
    DrawVedicDiamond({ x + w - 4, y + 4 }, 2.0f, color);

    // Bottom-Left
    DrawLineEx({ x, y + h }, { x + size, y + h }, thick, color);
    DrawLineEx({ x, y + h }, { x, y + h - size }, thick, color);
    DrawVedicDiamond({ x + 4, y + h - 4 }, 2.0f, color);

    // Bottom-Right
    DrawLineEx({ x + w, y + h }, { x + w - size, y + h }, thick, color);
    DrawLineEx({ x + w, y + h }, { x + w, y + h - size }, thick, color);
    DrawVedicDiamond({ x + w - 4, y + h - 4 }, 2.0f, color);
}

// ── SEGMENTED HEALTH / PRANA GAUGE ───────────────────────────────────────────
// Per design spec: linear recessed well (#0E1320) broken into discrete cells.
// Dynamic chromatic state:
//   > 60%  → Vedic Jade (#1EC846)
//   30-60% → Solar Amber (#DCC828)
//   < 30%  → Pulsing Crimson Flare (#DC3C00)
//
// Optional damage_trail shows recent losses in vermilion fading to void.
inline void DrawSegmentedHealthGauge(Rectangle rect, float current, float maximum,
                                     int segments = 16, float pulse_t = 0.0f,
                                     bool show_trail = false, float trail_pct = 0.0f) {
    if (maximum <= 0.0f) maximum = 1.0f;
    float pct = std::clamp(current / maximum, 0.0f, 1.0f);
    int active_segs = static_cast<int>(pct * segments + 0.5f);
    int trail_segs  = show_trail ? static_cast<int>(trail_pct * segments + 0.5f) : 0;

    // Pick chromatic state
    Color fill_col;
    if (pct > 0.60f)       fill_col = PAL_HEALTH_HIGH;
    else if (pct > 0.30f)  fill_col = PAL_HEALTH_MID;
    else {
        // Pulsing for critical
        float pulse = 0.55f + 0.45f * std::sin(pulse_t * 5.0f);
        fill_col = PAL_HEALTH_LOW;
        fill_col.a = static_cast<unsigned char>(pulse * 255.0f);
    }

    // Recessed well background
    DrawRectangleRec(rect, PAL_SURFACE_WELL);
    DrawRectangleLinesEx(rect, 1.0f, PAL_OUTLINE_VARIANT);

    // Inner padding
    float pad = 2.0f;
    Rectangle inner = { rect.x + pad, rect.y + pad, rect.width - pad * 2, rect.height - pad * 2 };
    if (inner.width <= 4.0f || inner.height <= 4.0f) return;

    float seg_w = (inner.width - (segments - 1) * 2.0f) / segments;
    for (int i = 0; i < segments; ++i) {
        float x = inner.x + i * (seg_w + 2.0f);
        Rectangle cell = { x, inner.y, seg_w, inner.height };

        if (i < active_segs) {
            DrawRectangleRec(cell, fill_col);
            // Soft inner glow on active cells
            Color glow = fill_col;
            glow.a = 80;
            DrawRectangleLinesEx({ cell.x - 1, cell.y - 1, cell.width + 2, cell.height + 2 }, 1.0f, glow);
        } else if (i < active_segs + trail_segs && show_trail) {
            // Damage trail (decaying vermilion)
            Color t = PAL_DAMAGE_TRAIL;
            t.a = static_cast<unsigned char>(60 - (i - active_segs) * 8);
            DrawRectangleRec(cell, t);
        } else {
            // Empty cell - very dark
            DrawRectangleRec(cell, { 0x05, 0x07, 0x10, 255 });
        }
    }
}

// ── MANDALA RETICLE ──────────────────────────────────────────────────────────
// Outer 16-point petal compass + middle counter-rotating wheel + inner
// intersecting Sri Yantra triangles. Rotates over time.
inline void DrawMandalaReticle(Vector2 center, float radius, float time, Color primary, Color secondary, float alpha_scale = 1.0f) {
    float rot1 = time * 0.6f;
    float rot2 = -time * 1.2f;
    unsigned char a = static_cast<unsigned char>(alpha_scale * 255.0f);
    Color p = primary; p.a = a;
    Color s = secondary; s.a = a;

    // Outer 16-point petal compass
    int petals = 16;
    for (int i = 0; i < petals; ++i) {
        float a1 = rot1 + (i * 2.0f * 3.14159265f) / petals;
        float a2 = a1 + (3.14159265f / petals) * 0.35f;
        Vector2 p1 = { center.x + std::cos(a1) * radius, center.y + std::sin(a1) * radius };
        Vector2 p2 = { center.x + std::cos(a2) * radius * 0.85f, center.y + std::sin(a2) * radius * 0.85f };
        DrawLineEx(p1, p2, 1.0f, p);
    }

    // Middle rotating ring (counter-rotation)
    DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), radius * 0.65f, p);
    DrawCircleLines(static_cast<int>(center.x), static_cast<int>(center.y), radius * 0.62f, s);
    int ticks = 18;
    for (int i = 0; i < ticks; ++i) {
        float ang = rot2 + (i * 2.0f * 3.14159265f) / ticks;
        Vector2 ti = { center.x + std::cos(ang) * radius * 0.62f, center.y + std::sin(ang) * radius * 0.62f };
        Vector2 to = { center.x + std::cos(ang) * radius * 0.68f, center.y + std::sin(ang) * radius * 0.68f };
        DrawLineEx(ti, to, 1.0f, s);
    }

    // Inner Sri Yantra triangle cluster (4 + 4 interlocking triangles)
    float inner_r = radius * 0.35f;
    for (int i = 0; i < 4; ++i) {
        float base_ang = rot1 + i * (3.14159265f / 2.0f);
        Vector2 v1 = { center.x, center.y - inner_r };
        Vector2 v2 = { center.x + std::cos(base_ang - 0.4f) * inner_r, center.y + std::sin(base_ang - 0.4f) * inner_r };
        Vector2 v3 = { center.x + std::cos(base_ang + 0.4f) * inner_r, center.y + std::sin(base_ang + 0.4f) * inner_r };
        DrawLineEx(v1, v2, 1.0f, p);
        DrawLineEx(v2, v3, 1.0f, p);
        DrawLineEx(v3, v1, 1.0f, p);
    }

    // Center pulse point
    float pulse_r = 2.0f + 1.0f * std::sin(time * 4.0f);
    DrawCircle(static_cast<int>(center.x), static_cast<int>(center.y), pulse_r, p);
}

// ── BOSS THREAT BANNER ───────────────────────────────────────────────────────
// Per design spec: top-center, 600px wide, flanked by Sanskrit winged brackets,
// dual-line HP pool with phase milestone pips. Red strobe when telegraphing.
inline void DrawBossThreatBanner(Rectangle rect, const std::string& boss_name,
                                 float current_hp, float max_hp, int current_phase, int total_phases,
                                 bool telegraphing, float time) {
    // Strobing red background when telegraphing
    if (telegraphing) {
        float strobe = 0.5f + 0.5f * std::sin(time * 12.0f);
        Color alert = PAL_DESTRUCTIVE;
        alert.a = static_cast<unsigned char>(40 + strobe * 80.0f);
        DrawRectangleRec(rect, alert);
    }

    // Recessed well background
    DrawRectangleRec(rect, PAL_SURFACE_WELL);
    DrawRectangleLinesEx(rect, 1.0f, PAL_OUTLINE_VARIANT);

    // Sanskrit winged brackets (L-brackets at edges)
    float bracket_w = 18.0f;
    DrawLineEx({ rect.x, rect.y }, { rect.x + bracket_w, rect.y + rect.height / 2 }, 2.0f, PAL_TERTIARY);
    DrawLineEx({ rect.x + bracket_w, rect.y + rect.height / 2 }, { rect.x, rect.y + rect.height }, 2.0f, PAL_TERTIARY);
    DrawLineEx({ rect.x + rect.width, rect.y }, { rect.x + rect.width - bracket_w, rect.y + rect.height / 2 }, 2.0f, PAL_TERTIARY);
    DrawLineEx({ rect.x + rect.width - bracket_w, rect.y + rect.height / 2 }, { rect.x + rect.width, rect.y + rect.height }, 2.0f, PAL_TERTIARY);

    // Boss name (uppercase, label-caps style)
    // Caller is responsible for drawing text; here we just emit segmented gauge.
    float gauge_x = rect.x + 24;
    float gauge_y = rect.y + rect.height * 0.55f;
    float gauge_w = rect.width - 48;
    float gauge_h = rect.height * 0.32f;
    Rectangle gauge = { gauge_x, gauge_y, gauge_w, gauge_h };

    // Use 20 segments per design spec
    DrawSegmentedHealthGauge(gauge, current_hp, max_hp, 20, time, false, 0.0f);

    // Phase milestone pips across the top edge
    if (total_phases > 1) {
        float pip_spacing = (rect.width - 60) / (total_phases - 1);
        for (int i = 0; i < total_phases; ++i) {
            float px = rect.x + 30 + i * pip_spacing;
            float py = rect.y + 6;
            Color pc = (i < current_phase) ? PAL_PRIMARY : PAL_TEXT_MUTED;
            DrawVedicDiamond({ px, py }, 3.0f, pc);
        }
    }
}

// ── BUTTON STATE STYLE (used by Button class to render correctly) ────────────
enum class ButtonKind { PRIMARY, SECONDARY, TERTIARY, DESTRUCTIVE, GHOST };
struct ButtonVisual {
    Color fill_idle;
    Color fill_hover;
    Color border;
    Color text;
    Color text_hover;
    float  glow_strength;  // 0..1 for hover glow alpha
};

inline ButtonVisual ButtonVisualPrimary() {
    return { PAL_PRIMARY_FILL, PAL_PRIMARY_FILL_HOVER,
             PAL_PRIMARY, PAL_PRIMARY_CORE, PAL_PRIMARY_CORE, 0.85f };
}
inline ButtonVisual ButtonVisualSecondary() {
    return { PAL_SECONDARY_FILL, { 0x00, 0xDB, 0xE7, 50 },
             PAL_SECONDARY, PAL_SECONDARY_BRIGHT, PAL_SECONDARY_BRIGHT, 0.60f };
}
inline ButtonVisual ButtonVisualDestructive() {
    return { PAL_DESTRUCTIVE_FILL, { 0xBF, 0x00, 0x36, 60 },
             PAL_DESTRUCTIVE, PAL_DESTRUCTIVE_BRIGHT, PAL_DESTRUCTIVE_BRIGHT, 0.80f };
}
inline ButtonVisual ButtonVisualTertiary() {
    return { { 0, 0, 0, 0 }, { 0xC5, 0xA0, 0x59, 40 },
             PAL_TERTIARY, PAL_TERTIARY, PAL_TERTIARY_BRIGHT, 0.50f };
}
inline ButtonVisual ButtonVisualGhost() {
    return { { 0, 0, 0, 0 }, { 0xE1, 0xE1, 0xF1, 30 },
             { 0x8F, 0x98, 0xA8, 200 }, PAL_TEXT, PAL_TEXT, 0.30f };
}

inline ButtonVisual GetButtonVisual(ButtonKind k) {
    switch (k) {
        case ButtonKind::PRIMARY:     return ButtonVisualPrimary();
        case ButtonKind::SECONDARY:   return ButtonVisualSecondary();
        case ButtonKind::DESTRUCTIVE: return ButtonVisualDestructive();
        case ButtonKind::TERTIARY:    return ButtonVisualTertiary();
        case ButtonKind::GHOST:       return ButtonVisualGhost();
    }
    return ButtonVisualPrimary();
}

} // namespace Vimana::UI
