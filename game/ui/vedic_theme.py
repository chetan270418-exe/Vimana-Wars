"""
Canonical design tokens and drawing primitives for Vimana Wars.
Follows the authoritative Vimana Wars UI Redesign & Platform Design Document.
Single source of truth for all colours, typography fallbacks, chamfers, and gauges.
"""
import math
import arcade
from constants import WIDTH, HEIGHT


# ── Canonical Colours (Section 4.1) ──────────────────────────────────────────
VOID              = (7, 10, 19)          # Deepest background, starfield ground (#070A13)
OBSIDIAN          = (11, 13, 18)         # Window base, view background (#0B0D12)
WELL              = (14, 19, 32)         # Recessed insets behind bars & inputs (#0E1320)
SURFACE_LOW       = (20, 26, 40)         # Base RGB for low-tier glass (#141A28)
SURFACE_HIGH      = (32, 42, 61)         # Base RGB for high-tier glass (#202A3D)
GLASS_LOW         = (20, 26, 40, 217)    # Default panels and cards (85% opacity)
GLASS_HIGH        = (32, 42, 61, 235)    # Hovered / selected / focal panels (92% opacity)
GOLD              = (233, 196, 0)        # Primary action & current selection only (#E9C400)
GOLD_BRIGHT       = (255, 246, 223)      # Text on gold, victory headline (#FFF6DF)
CYAN              = (0, 219, 231)        # Operational: shields, ready states, links, sync (#00DBE7)
CYAN_BRIGHT       = (116, 245, 255)      # Cyan emphasis, warp lines (#74F5FF)
BRASS             = (197, 160, 89)       # Hardware plates, dividers, locked tiers (#C5A059)
ASTRA_RED         = (191, 0, 54)         # Danger, bosses, destructive confirm (#BF0036)
ASTRA_RED_BRIGHT  = (255, 107, 114)      # Red text, breach alarm (#FF6B72)
PARCHMENT         = (208, 198, 171)      # Lore and secondary body copy (#D0C6AB)
STARLIGHT         = (240, 237, 230)      # Primary body copy (#F0EDE6)
GREY              = (143, 152, 168)      # Hints, inactive data, disabled (#8F98A8)

# Aliases for backward-compatibility with existing views
MUTED        = GREY
RED          = ASTRA_RED
RED_BRIGHT   = ASTRA_RED_BRIGHT
HAIRLINE_GOLD = (*GOLD, 72)
HAIRLINE_CYAN = (*CYAN, 58)

# ── Gauge Color Ramp (Section 4.1) ───────────────────────────────────────────
JADE        = (30, 200, 70)     # > 0.60 (#1EC846)
AMBER       = (220, 200, 40)    # 0.30 - 0.60 (#DCC828)
CRIMSON     = (220, 60, 0)      # < 0.30 (#DC3C00)
GHOST_TRAIL = (220, 40, 40)     # Decays over 600ms (#DC2828)


def get_gauge_color(fraction: float) -> tuple[int, int, int]:
    """Return the canonical gauge color for a normalized 0.0-1.0 fraction."""
    if fraction > 0.60:
        return JADE
    if fraction >= 0.30:
        return AMBER
    return CRIMSON


# ── Boon Elemental Accents (Section 4.1) ─────────────────────────────────────
BOON_ACCENTS = {
    "Agni":       (255, 120, 30),   # #FF781E
    "Indra":      (120, 220, 255),  # #78DCFF
    "Vayu":       (100, 255, 180),  # #64FFB4
    "Yama":       (170, 80, 255),   # #AA50FF
    "Varuna":     (0, 160, 200),    # #00A0C8
    "Garuda":     (233, 196, 0),    # #E9C400
    "Sudarshana": (116, 245, 255),  # #74F5FF
    "Surya":      (255, 215, 0),    # #FFD700
}


# ── Canonical Typography Roles (Section 4.2) ─────────────────────────────────
FONT_CEREMONIAL = ("Cinzel", "Times New Roman", "serif")
FONT_INTERFACE   = ("Space Grotesk", "Arial", "sans-serif")
FONT_TELEMETRY   = ("JetBrains Mono", "Consolas", "monospace")


# ── Motion & Animation Helpers (Section 4.4) ─────────────────────────────────
def pulse_alpha(elapsed: float, low: int = 90, high: int = 190,
                speed: float = 3.0, reduced: bool = False) -> int:
    """Return a pulsing alpha value, honoring the player's reduced motion setting."""
    if reduced:
        return low
    phase = (math.sin(elapsed * speed) + 1.0) * 0.5
    return int(low + (high - low) * phase)


# ── Drawing Primitives (Section 4.3 & 5) ──────────────────────────────────────
def _chamfer_points(left: float, right: float, bottom: float, top: float, cut: float = 8.0):
    """Calculate the 8 vertices of an octagonally chamfered box."""
    cut = min(cut, max(1.0, (right - left) / 3.0), max(1.0, (top - bottom) / 3.0))
    return [
        (left + cut, bottom), (right - cut, bottom),
        (right, bottom + cut), (right, top - cut),
        (right - cut, top), (left + cut, top),
        (left, top - cut), (left, bottom + cut),
    ]


def draw_chamfered_panel(left: float, right: float, bottom: float, top: float,
                         accent=GOLD, *, fill=SURFACE_LOW, alpha: int = 225,
                         border_width: int = 1, selected: bool = False,
                         cut: float = 8.0, scanlines: bool = False) -> None:
    """Draw an authentic Tier 1-3 chamfered glass panel with luminous border."""
    points = _chamfer_points(left, right, bottom, top, cut)
    arcade.draw_polygon_filled(points, (*fill[:3], alpha))

    border_alpha = min(255, alpha + 25 if selected else alpha)
    width = max(border_width, 2 if selected else border_width)
    for i, point in enumerate(points):
        nxt = points[(i + 1) % len(points)]
        arcade.draw_line(point[0], point[1], nxt[0], nxt[1],
                         (*accent[:3], border_alpha), width)

    # Accent hairline near top edge
    if top - bottom > 18:
        arcade.draw_line(left + cut + 6, top - 3, right - cut - 6, top - 3,
                         (*accent[:3], min(110, border_alpha)), 1)

    if scanlines and top - bottom > 20:
        draw_scanlines(left + 2, right - 2, bottom + 2, top - 2, CYAN, spacing=16, alpha=6)


def draw_corner_etching(left: float, right: float, bottom: float, top: float,
                        color=GOLD, length: float = 12.0, alpha: int = 90) -> None:
    """Draw four cockpit-style L-bracket etchings around a focal panel."""
    c = (*color[:3], alpha)
    arcade.draw_line(left, top, left + length, top, c, 1)
    arcade.draw_line(left, top, left, top - length, c, 1)
    arcade.draw_line(right, top, right - length, top, c, 1)
    arcade.draw_line(right, top, right, top - length, c, 1)
    arcade.draw_line(left, bottom, left + length, bottom, c, 1)
    arcade.draw_line(left, bottom, left, bottom + length, c, 1)
    arcade.draw_line(right, bottom, right - length, bottom, c, 1)
    arcade.draw_line(right, bottom, right, bottom + length, c, 1)


def draw_segmented_bar(left: float, right: float, bottom: float, top: float,
                       fraction: float, color=CYAN, segments: int = 10,
                       background=WELL, gap: float = 3.0,
                       ghost_fraction: float = 0.0) -> None:
    """Render a canonical 10-segment telemetry bar with optional ghost trail."""
    fraction = max(0.0, min(1.0, fraction))
    ghost_fraction = max(fraction, min(1.0, ghost_fraction))
    width = right - left
    segment_width = (width - gap * (segments - 1)) / segments

    for i in range(segments):
        x1 = left + i * (segment_width + gap)
        x2 = x1 + segment_width
        filled = fraction >= (i + 1) / segments
        partial = max(0.0, min(1.0, fraction * segments - i))

        # Base background well
        arcade.draw_lrbt_rectangle_filled(x1, x2, bottom, top, (*background[:3], 220))

        # Ghost decay trail
        if ghost_fraction > fraction:
            g_partial = max(0.0, min(1.0, ghost_fraction * segments - i))
            if g_partial > 0:
                arcade.draw_lrbt_rectangle_filled(
                    x1, x1 + segment_width * g_partial, bottom, top,
                    (*GHOST_TRAIL, 180)
                )

        # Active fill
        if filled or partial > 0:
            arcade.draw_lrbt_rectangle_filled(
                x1, x1 + segment_width * partial, bottom, top,
                (*color[:3], 240),
            )


def draw_scanlines(left: float, right: float, bottom: float, top: float,
                   color=CYAN, spacing: int = 18, alpha: int = 8) -> None:
    """Draw subtle vertical or horizontal holographic scanline mesh."""
    y = bottom + spacing
    while y < top:
        arcade.draw_line(left, y, right, y, (*color[:3], alpha), 1)
        y += spacing


def draw_telemetry_ticks(left: float, right: float, y: float, color=CYAN,
                         count: int = 12, height: float = 5, alpha: int = 80) -> None:
    """Draw horizontal tick marks for cockpit dials and frame boundaries."""
    if count < 2:
        return
    step = (right - left) / (count - 1)
    arcade.draw_line(left, y, right, y, (*color[:3], alpha // 2), 1)
    for index in range(count):
        tick_height = height * (1.5 if index in (0, count - 1) else 1.0)
        x = left + index * step
        arcade.draw_line(x, y - tick_height, x, y + tick_height, (*color[:3], alpha), 1)


def draw_menu_backdrop(title: str, subtitle: str = "", accent=GOLD,
                       *, pulse: float = 0.0, reduced: bool = False) -> None:
    """Draw standard command-console backdrop used by front-end screens."""
    arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, OBSIDIAN)
    arcade.draw_lrbt_rectangle_filled(24, WIDTH - 24, 74, HEIGHT - 74, (*SURFACE_LOW, 175))
    arcade.draw_lrbt_rectangle_filled(24, WIDTH - 24, 74, 170, (*VOID, 125))

    for index in range(42):
        sx = 38 + ((index * 137) % (WIDTH - 76))
        sy = 92 + ((index * 71) % (HEIGHT - 184))
        drift = 0.0 if reduced else (pulse * (0.8 + (index % 3) * 0.22))
        x = 28 + ((sx + drift) % (WIDTH - 56))
        twinkle = 70 + ((index * 17) % 70)
        arcade.draw_circle_filled(x, sy, 0.7 + (index % 2) * 0.45,
                                  (110, 180, 220, twinkle))

    draw_scanlines(24, WIDTH - 24, 58, HEIGHT - 58, CYAN, spacing=24, alpha=6)
    draw_corner_etching(24, WIDTH - 24, 24, HEIGHT - 24, accent, length=22, alpha=105)
    arcade.draw_line(24, HEIGHT - 74, WIDTH - 24, HEIGHT - 74, (*accent, 105), 1)
    arcade.draw_line(24, 74, WIDTH - 24, 74, (*CYAN, 48), 1)

    arcade.draw_text(title, 42, HEIGHT - 52, accent, font_size=22, bold=True,
                     font_name=FONT_INTERFACE)
    if subtitle:
        arcade.draw_text(subtitle, 42, HEIGHT - 68, MUTED, font_size=8, bold=True,
                         font_name=FONT_TELEMETRY)
    draw_back_navigation()
    if not reduced:
        alpha = pulse_alpha(pulse, 12, 30, 1.7)
        arcade.draw_circle_outline(WIDTH - 100, HEIGHT - 50, 28, (*accent, alpha), 1)
        arcade.draw_line(WIDTH - 132, HEIGHT - 50, WIDTH - 68, HEIGHT - 50, (*accent, alpha), 1)
        arcade.draw_line(WIDTH - 100, HEIGHT - 82, WIDTH - 100, HEIGHT - 18, (*accent, alpha), 1)
    arcade.draw_text("AKASHIC LINK  //  LOCAL CONSOLE", WIDTH - 30, 38,
                     (*MUTED, 190), font_size=7, bold=True, anchor_x="right",
                     font_name=FONT_TELEMETRY)


def draw_focus_panel(left: float, right: float, bottom: float, top: float,
                     accent=CYAN, *, selected: bool = False) -> None:
    """Draw a highlighted Tier 2 focus panel."""
    draw_chamfered_panel(left, right, bottom, top, accent,
                         fill=SURFACE_HIGH if selected else SURFACE_LOW,
                         alpha=238, border_width=2 if selected else 1,
                         selected=selected, cut=10)


def draw_back_navigation(label: str = "ESC  BACK") -> None:
    """Standardized top-right back button hint."""
    arcade.draw_text(label, WIDTH - 30, HEIGHT - 52, MUTED, font_size=8,
                     bold=True, anchor_x="right", anchor_y="center",
                     font_name=FONT_TELEMETRY)


def draw_state_badge(x: float, y: float, label: str, color=CYAN, *, width: float = 92) -> None:
    """Draw a small chamfered status badge (e.g. READY, LOCKED, CLEARED)."""
    draw_chamfered_panel(x - width / 2, x + width / 2, y - 10, y + 10,
                         color, fill=WELL, alpha=225, border_width=1, cut=4)
    arcade.draw_text(label, x, y - 3, color, font_size=8, bold=True,
                     anchor_x="center", font_name=FONT_TELEMETRY)
