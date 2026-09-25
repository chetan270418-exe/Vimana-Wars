// ── VIMANA WARS // DESIGN TOKENS ──────────────────────────────────────────────
// Centralized tokens matching the Stitch / Figma "Vimana Wars" design system.
// Use these everywhere instead of raw colors — keeps the palette coherent.
//
// Hierarchy:
//   DT_         → design system color (raw hex)
//   PAL_*       → semantic palette alias for UI roles
//   PAL_*_GLASS → translucent variant for layered panels
//
// Reference:  design_extract_2/stitch.../vimana_wars/DESIGN.md
#pragma once
#include "raylib.h"

namespace Vimana::UI {

// ── RAW PALETTE HEX (design system source of truth) ───────────────────────────
namespace DT_ {
    // Surfaces
    constexpr int SURFACE_VOID         = 0x070913; // base cosmic obsidian
    constexpr int SURFACE_FRAME        = 0x08090F; // window frame
    constexpr int SURFACE_WELL         = 0x0E1320; // recessed gauge wells
    constexpr int SURFACE_GLASS        = 0x141A28; // translucent cockpit glass
    constexpr int SURFACE_FOCUS        = 0x1F293C; // elevated focus / modals
    constexpr int SURFACE_HIGH         = 0x272935; // surface container high
    constexpr int SURFACE_HIGHEST      = 0x323440; // surface container highest

    // Brand
    constexpr int DIVINE_GOLD          = 0xE9C400; // primary
    constexpr int DIVINE_GOLD_BRIGHT   = 0xFFE16F; // bright variant
    constexpr int DIVINE_GOLD_CORE     = 0xFFF6DF; // bright core text on gold
    constexpr int PRANA_CYAN           = 0x00DBE7; // secondary
    constexpr int PRANA_CYAN_BRIGHT    = 0x74F5FF; // bright cyan
    constexpr int TEMPLE_BRASS         = 0xC5A059; // tertiary
    constexpr int TEMPLE_BRASS_BRIGHT  = 0xFFDEA5; // brass bright

    // Functional alerts
    constexpr int VEDIC_JADE           = 0x1EC846; // healthy / stable
    constexpr int SOLAR_AMBER          = 0xDCC828; // warning
    constexpr int SOLAR_AMBER_DEEP     = 0xE9C177; // amber deep
    constexpr int ASTRA_RED            = 0xBF0036; // destructive
    constexpr int ASTRA_RED_BRIGHT       = 0xFF6B72; // bright red text
    constexpr int CRIMSON_FLARE        = 0xDC3C00; // critical pulse
    constexpr int VERMILION            = 0xDC2828; // damage trail

    // Neutrals
    constexpr int ON_SURFACE           = 0xE1E1F1; // primary text
    constexpr int ON_SURFACE_VARIANT   = 0xD0C6AC; // secondary text
    constexpr int PARCHMENT            = 0xF0EDE6; // body text
    constexpr int MUTED                = 0x8F98A8; // muted text
    constexpr int OUTLINE              = 0x999078; // outline
    constexpr int OUTLINE_VARIANT      = 0x4D4632; // outline variant
}

// ── RAYLIB COLOR INSTANCES (use these directly) ───────────────────────────────
inline const Color PAL_BG_VOID            = { 0x07, 0x09, 0x13, 255 };
inline const Color PAL_SURFACE_FRAME      = { 0x08, 0x09, 0x0F, 255 };
inline const Color PAL_SURFACE_WELL       = { 0x0E, 0x13, 0x20, 255 };
inline const Color PAL_SURFACE_GLASS      = { 0x14, 0x1A, 0x28, 230 }; // 88% opacity
inline const Color PAL_SURFACE_GLASS_92   = { 0x14, 0x1A, 0x28, 235 }; // 92% opacity
inline const Color PAL_SURFACE_FOCUS      = { 0x1F, 0x29, 0x3C, 242 }; // 95% opacity

inline const Color PAL_PRIMARY            = { 0xE9, 0xC4, 0x00, 255 }; // divine gold
inline const Color PAL_PRIMARY_BRIGHT     = { 0xFF, 0xE1, 0x6F, 255 };
inline const Color PAL_PRIMARY_CORE       = { 0xFF, 0xF6, 0xDF, 255 };
inline const Color PAL_PRIMARY_FILL       = { 0xE9, 0xC4, 0x00,  31 }; // 12% bg fill
inline const Color PAL_PRIMARY_FILL_HOVER = { 0xE9, 0xC4, 0x00,  71 }; // 28% bg fill

inline const Color PAL_SECONDARY          = { 0x00, 0xDB, 0xE7, 255 }; // prana cyan
inline const Color PAL_SECONDARY_BRIGHT   = { 0x74, 0xF5, 0xFF, 255 };
inline const Color PAL_SECONDARY_FILL     = { 0x00, 0xDB, 0xE7,  20 }; // 8% bg fill

inline const Color PAL_TERTIARY           = { 0xC5, 0xA0, 0x59, 255 }; // temple brass
inline const Color PAL_TERTIARY_BRIGHT    = { 0xFF, 0xDE, 0xA5, 255 };

inline const Color PAL_TEXT               = { 0xE1, 0xE1, 0xF1, 255 };
inline const Color PAL_TEXT_VARIANT       = { 0xD0, 0xC6, 0xAC, 255 };
inline const Color PAL_TEXT_BODY          = { 0xF0, 0xED, 0xE6, 255 };
inline const Color PAL_TEXT_MUTED         = { 0x8F, 0x98, 0xA8, 255 };

inline const Color PAL_OUTLINE            = { 0x99, 0x90, 0x78, 255 };
inline const Color PAL_OUTLINE_VARIANT    = { 0x4D, 0x46, 0x32, 255 };
inline const Color PAL_OUTLINE_CYAN       = { 0x00, 0xDB, 0xE7, 102 }; // cyan @ 40%

inline const Color PAL_HEALTH_HIGH        = { 0x1E, 0xC8, 0x46, 255 }; // vedic jade
inline const Color PAL_HEALTH_MID         = { 0xDC, 0xC8, 0x28, 255 }; // solar amber
inline const Color PAL_HEALTH_LOW         = { 0xDC, 0x3C, 0x00, 255 }; // crimson flare
inline const Color PAL_DAMAGE_TRAIL       = { 0xDC, 0x28, 0x28, 180 };

inline const Color PAL_DESTRUCTIVE        = { 0xBF, 0x00, 0x36, 255 };
inline const Color PAL_DESTRUCTIVE_FILL   = { 0xBF, 0x00, 0x36,  31 };
inline const Color PAL_DESTRUCTIVE_BRIGHT = { 0xFF, 0x6B, 0x72, 255 };

// ── TYPOGRAPHY ROLES ─────────────────────────────────────────────────────────
// Font files (from assets/fonts/):
//   Cinzel-Bold.ttf        → Cinzel (headlines / display / label-caps)
//   SpaceGrotesk-Bold.ttf  → Space Grotesk (body / titles / lore)
//   JetBrainsMono-Bold.ttf → JetBrains Mono (telemetry / data)
//
// Recommended usage:
//   Display/Headline/Title  → title font (Cinzel)
//   Body/Title-small       → body font (Space Grotesk)
//   Telemetry/Mono         → mono font (JetBrains Mono)
namespace Type {
    // Display
    constexpr int DISPLAY_LG = 48;     // Cinzel 900, letter-spacing +0.05em
    constexpr int HEADLINE_LG = 32;    // Cinzel 700, +0.08em
    constexpr int HEADLINE_MD = 24;    // Cinzel 700, +0.10em

    // Title
    constexpr int TITLE_MD = 18;       // Space Grotesk 600, +0.05em
    constexpr int TITLE_SM = 16;       // Space Grotesk 600, +0.04em

    // Body
    constexpr int BODY_LG = 16;        // Space Grotesk 400, +0.02em
    constexpr int BODY_MD = 14;        // Space Grotesk 400, +0.01em
    constexpr int BODY_SM = 12;        // Space Grotesk 400, +0.01em

    // Labels & Telemetry
    constexpr int LABEL_CAPS = 12;     // Cinzel 700, +0.18em (uppercase)
    constexpr int TELEMETRY = 11;      // JetBrains Mono 600, +0.15em
    constexpr int TELEMETRY_SM = 10;   // JetBrains Mono 500, +0.12em
}

// ── SPACING TOKENS (4px baseline grid) ────────────────────────────────────────
namespace Space {
    constexpr float XS  = 4.0f;
    constexpr float SM  = 8.0f;
    constexpr float MD  = 16.0f;
    constexpr float LG  = 24.0f;
    constexpr float XL  = 32.0f;
    constexpr float XXL = 48.0f;
}

// ── CHAMFER CUTS (per design spec) ────────────────────────────────────────────
namespace Chamfer {
    constexpr float SMALL  = 6.0f;   // chips, buttons, inputs
    constexpr float LARGE  = 12.0f;  // large panels, cockpit enclosures
}

// ── ELEVATION HELPERS ─────────────────────────────────────────────────────────
// Returns the (fill, border) color pair appropriate for the requested tier.
struct ElevationStyle {
    Color fill;
    Color border;
    float  chamfer;
};

inline ElevationStyle ElevationVoid()         { return { PAL_BG_VOID,        PAL_OUTLINE_VARIANT, 0.0f  }; }
inline ElevationStyle ElevationWell()         { return { PAL_SURFACE_WELL,    PAL_OUTLINE_CYAN,    Chamfer::SMALL }; }
inline ElevationStyle ElevationGlass()        { return { PAL_SURFACE_GLASS,   PAL_OUTLINE_VARIANT, Chamfer::LARGE }; }
inline ElevationStyle ElevationFocus()        { return { PAL_SURFACE_FOCUS,   PAL_PRIMARY,         Chamfer::LARGE }; }
inline ElevationStyle ElevationFocusCyan()    { return { PAL_SURFACE_FOCUS,   PAL_SECONDARY,       Chamfer::LARGE }; }

} // namespace Vimana::UI