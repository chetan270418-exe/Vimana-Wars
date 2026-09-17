#pragma once
#include <cmath>
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
        // Subtle outer glow
        Color glow = border;
        glow.a = 40;
        DrawRectangleLines(static_cast<int>(x - 2), static_cast<int>(y - 2), static_cast<int>(w + 4), static_cast<int>(h + 4), glow);
    }
}

inline void DrawCornerEtching(float x, float y, float size, Color color) {
    DrawLineEx({ x, y }, { x + size, y }, 2.0f, color);
    DrawLineEx({ x, y }, { x, y + size }, 2.0f, color);
}

inline void DrawScanlines() {
    // Subtle CRT scanline effect
    for (int y = 0; y < SCREEN_HEIGHT; y += 4) {
        DrawLine(0, y, SCREEN_WIDTH, y, { 0, 0, 0, 20 });
    }
}

} // namespace Vimana::UI
