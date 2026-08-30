# Vimana Wars — Vedic-Punk UI Design

This is the implementation guide for the visual overhaul supplied in
`stitch_vimana_wars_visual_overhaul.zip`. It translates the Stitch web mockup
into the existing Python Arcade game rather than copying HTML/Tailwind.

## Visual direction

Vimana Wars is a celestial war console: deep obsidian surfaces, sacred
geometry, luminous cyan telemetry, and restrained celestial-gold actions.
The UI should feel like a holographic cockpit projected over a cosmic void.

## Tokens

| Token | Value | Use |
|---|---|---|
| Obsidian | `#0B0D12` | Window/background base |
| Glass low | `#141A28` at 85% | Panels and cards |
| Glass high | `#202A3D` at 92% | Selected/hovered controls |
| Celestial gold | `#E9C400` / `#FFD700` | Primary actions, selected states |
| Prana cyan | `#00DBE7` / `#74F5FF` | Active telemetry, HP, ready states |
| Astra red | `#BF0036` / `#FF6B72` | Bosses, damage, destructive actions |
| Muted parchment | `#D0C6AB` | Secondary readable copy |
| Technical grey | `#8F98A8` | Hints and inactive data |

## Layout structure

- Main menu and front-end screens use a 220px logical left rail.
- A compact top header identifies the current console and sync state.
- The content area uses glass panels with thin 1px luminous borders.
- Controls use sharp/chamfered corners, not soft rounded cards.
- Gold is reserved for the selected/primary action; cyan means active or
  operational; red means danger.
- Keep the existing 900x600 logical coordinate system so windowed and
  fullscreen modes share the same layout.

## Screen mapping

- **Main menu:** left navigation rail, Vimana Vitals (campaign progress and
  achievements), animated cosmic hero panel, last-used ship and mission state.
- **Astra Arsenal:** the existing ship selector becomes the armory. Three cards
  per page remain for readability; locked ships show their unlock wave and a
  dimmed silhouette. Asset images are optional and always have vector fallbacks.
- **Mission Control HUD:** retain gameplay readability first. Add a thin cockpit
  frame, telemetry lines, segmented status bars, and a bottom Astra strip.
- **Settings and pause:** reuse the same glass/chamfered controls and preserve
  keyboard, mouse, and controller navigation.

## Motion and feedback

- Hover: 3–4% scale, brighter border, short UI click sound.
- Selection: gold/cyan border pulse, never a full-screen flash.
- Transitions: use `TransitionOverlay` for view changes.
- New unlocks: use the existing realm/achievement popup treatment.
- Accessibility: `Reduced Flashes`, `Colorblind Mode`, and `Screen Shake` must
  continue to reduce intensity globally.

## Implementation rules

- Prefer cached `arcade.Text` objects for persistent labels.
- Draw with Arcade 3.x APIs only (`draw_lrbt_rectangle_*`, `draw_rect_*`,
  `draw_polygon_filled`).
- Do not make online UI assets a runtime dependency. Local assets and vector
  fallbacks must both work offline.
- Keep gameplay input isolated from overlay views; every gameplay return path
  calls `Player.reset_input_state()`.
