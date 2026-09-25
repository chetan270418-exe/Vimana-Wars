---
name: Vimana Wars
colors:
  surface: '#11131d'
  surface-dim: '#11131d'
  surface-bright: '#373944'
  surface-container-lowest: '#0b0e18'
  surface-container-low: '#191b26'
  surface-container: '#1d1f2a'
  surface-container-high: '#272935'
  surface-container-highest: '#323440'
  on-surface: '#e1e1f1'
  on-surface-variant: '#d0c6ac'
  inverse-surface: '#e1e1f1'
  inverse-on-surface: '#2e303b'
  outline: '#999078'
  outline-variant: '#4d4632'
  surface-tint: '#e9c400'
  primary: '#ffe16f'
  on-primary: '#3a3000'
  primary-container: '#e9c400'
  on-primary-container: '#625100'
  inverse-primary: '#705d00'
  secondary: '#75f5ff'
  on-secondary: '#00363a'
  secondary-container: '#03dbe7'
  on-secondary-container: '#005c61'
  tertiary: '#ffdea5'
  on-tertiary: '#412d00'
  tertiary-container: '#e9c177'
  on-tertiary-container: '#6a4e0d'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffe16e'
  primary-fixed-dim: '#e9c400'
  on-primary-fixed: '#221b00'
  on-primary-fixed-variant: '#544600'
  secondary-fixed: '#75f5ff'
  secondary-fixed-dim: '#03dbe7'
  on-secondary-fixed: '#002022'
  on-secondary-fixed-variant: '#004f54'
  tertiary-fixed: '#ffdea5'
  tertiary-fixed-dim: '#e9c176'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5d4201'
  background: '#11131d'
  on-background: '#e1e1f1'
  surface-variant: '#323440'
typography:
  display-lg:
    fontFamily: Cinzel
    fontSize: 48px
    fontWeight: '900'
    lineHeight: 56px
    letterSpacing: 0.05em
  display-lg-mobile:
    fontFamily: Cinzel
    fontSize: 32px
    fontWeight: '900'
    lineHeight: 40px
    letterSpacing: 0.05em
  headline-lg:
    fontFamily: Cinzel
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: 0.08em
  headline-md:
    fontFamily: Cinzel
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: 0.1em
  title-md:
    fontFamily: Space Grotesk
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: 0.05em
  title-sm:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: 0.04em
  body-lg:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: 0.02em
  body-md:
    fontFamily: Space Grotesk
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
    letterSpacing: 0.01em
  body-sm:
    fontFamily: Space Grotesk
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-caps:
    fontFamily: Cinzel
    fontSize: 12px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.18em
  telemetry-mono:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.15em
  telemetry-sm:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.12em
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes a Vedic-Punk aesthetic that fuses ancient Indian sacred cosmology with deep-space military avionics. The interface simulates a celestial command cockpit hovering within an infinite cosmic void, balancing sacred epigraphy with precise space combat telemetry.

### Personality & Emotional Response
The UI evokes ceremonial awe, surgical precision, and cosmic tension. The user feels not merely like a pilot, but like an astral warrior consecrated to navigate divine war engines (*Vimanas*). Surfaces recall chiselled temple stone, oxidized temple bronze, and obsidian glass, punctuated by luminous energy conduits.

### Design Movement
The visual language synthesizes **High-Contrast Dark Mode**, **Tactile Sci-Fi HUD**, and **Sacred Geometric Ornamentation**:
- **Geometry**: Strict polygonal chamfers (45° beveled corners via clip-paths), interlocking yantra reticles, and L-bracket brass corner clasps. Rounded pill shapes and bubbly curves are strictly forbidden.
- **Atmosphere**: Cosmic obsidian panels over infinite void fields, punctuated by delicate CRT phosphor scanlines and celestial star charts.
- **Lighting Model**: Luminous plasma conduits casting focused edge glows rather than broad diffuse ambient shadows.

## Colors

The palette enforces strict functional authority, grounding operational noise in light-absorbing obsidian voids while reserving high-intensity plasma emitters for tactical awareness.

### Palette Architecture
- **Primary — Divine Celestial Gold (`#E9C400`)**: Consecrated temple gold reserved for active focus targets, primary firing authorizations, selected navigation items, and victory milestones. Pair with bright core text `#FFF6DF`.
- **Secondary — Prana Cyan / Celestial Plasma (`#00DBE7`)**: Telemetry grids, shield capacitators, hyperlane routes, and operational confirmation rings. Pairs with highlight cyan `#74F5FF`.
- **Tertiary — Ancient Temple Brass (`#C5A059`)**: Structural L-brackets, sacred runic dividers, locked tier emblems, and secondary iconography.
- **Neutral — Cosmic Void Black (`#070913`)**: The absolute zero canvas. Base obsidian window frames reside at `#08090F`, recessed gauge wells sit at `#0E1320`, and translucent panel glass sits at `#141A28` with 85% to 92% opacity.

### Alert & Threat Signatures
- **Sacred Vermilion / Astra Red (`#BF0036` / `#DC2626`)**: Critical hull breaches, Asura demon bosses, lock-on warnings, and catastrophic failure states.
- **Vedic Jade (`#1EC846`)**: Full vital integrity and stable prana balance.
- **Solar Amber (`#DCC828`)**: Compromised energy systems and heat build-up.

## Typography

The type system creates an intentional tension between majestic monument stone carvings and clinical military telemetry.

### Font Hierarchy & Roles
- **Headlines & Display (`Cinzel`)**: Inscribed stone capital aesthetic invoking ancient Sanskrit edicts, temple copperplates, and royal dynastic titles. All instances must use uppercase tracking (`+0.05em` to `+0.18em`) to mimic stone chisel kerning.
- **Interface & Lore Body (`Space Grotesk`)**: An angular, geometric sans-serif that echoes mechanical joints, high x-height clarity, and tactical pilot dossiers. Keeps lore readable without losing the sci-fi tone.
- **Data & Telemetry (`JetBrains Mono`)**: Strict tabular monospace numbers for coordinates, shield ratios, weapon heat cycles, and real-time millisecond combat tickers to prevent layout shifting.

### Typographic Polish
- Maintain narrative lore blocks at a maximum line length of 65 characters (`680px` max container width) for optimal pilot readability during briefings.
- All numbers indicating weapon charges, shield counts, and ammo tallies must use tabular figure alignments.

## Layout & Spacing

The layout model is governed by a 4px baseline grid operating inside a rigid structural framework.

### Grid & Viewport Partitioning
- **Command Deck / Hangar Mode**:
  - **Left Rail**: 240px to 280px fixed width docked navigation column displaying vessel seals, core routes, and pilot vital meters.
  - **Main Viewport Stage**: Fluid stage (remaining width) hosting 3D wireframe models, weapon sockets, or celestial realm navigation maps.
  - **Status Header**: 48px fixed bar housing system sync beacon, Dharmic Karma ledgers, and audio channels.
- **Combat HUD Mode**:
  - Full-screen fluid canvas with a **safe perimeter zone of 32px (`space-xl`)** to prevent HUD elements from running against screen bezels.
  - Telemetry is anchored to cardinal anchors (Top-Left: Shield/Hull; Top-Right: Astra Ordnance; Bottom-Center: Supercharge Core).
  - The central 50% circular sector of the screen remains unencumbered by background glass cards to maintain unobstructed sightlines for incoming enemy fire.

### Responsive Breakpoints
- **Desktop Ultrawide / 4K (`> 1920px`)**: Constrain UI stage to max 1920px center-anchored with outer atmospheric starfield void padding.
- **Standard Desktop (`1024px – 1920px`)**: Full default two-column command layout with 24px margins.
- **Tablet / Mini Display (`768px – 1023px`)**: Command rail collapses into a vertical icon rail (72px width), shifting text labels to flyout panels.

## Elevation & Depth

Visual hierarchy is constructed via planar optical glass layering, precision hairline neon borders, and edge luminescence rather than traditional dropped shadows.

### Elevation Architecture
1. **Level 0 (The Deep Cosmic Void)**: Pure black base `#070913` layered with procedurally scrolling micro-stars and faint yantra coordinate grid vectors at 10% opacity.
2. **Level 1 (Recessed Wells & Trays)**: Background `#0E1320` sunken with `inset 0 2px 4px rgba(0, 0, 0, 0.8)`. Used for gauge backgrounds, uncharged ammunition chambers, and text input fields.
3. **Level 2 (Cockpit Glass Panels & Cards)**: Translucent obsidian `#141A28` (88% opacity) backed by a 12px backdrop blur. Bordered with a 1px crisp outline (`rgba(22, 32, 48, 0.9)` or hairline `rgba(0, 219, 231, 0.35)`). Features repeating 3px horizontal CRT scanlines at 3% opacity.
4. **Level 3 (Elevated Focus / Modals / Active Reticles)**: Obsidian `#1F293C` (95% opacity), accompanied by a concentrated 1px Divine Gold border (`rgba(233, 196, 0, 0.9)`) and a focused optical glow: `drop-shadow(0 0 16px rgba(233, 196, 0, 0.35))`.

### Edge & Corner Accents
Panels utilize geometric L-bracket corner reinforcements in Temple Brass (`#C5A059`) at each chamfer vertex to reinforce a bolted instrument chassis appearance.

## Shapes

The shape system is strictly non-Euclidean and angular, rooted in **chamfered geometry (beveled 45-degree angles)** and circular sacred yantra mandalas.

### Chamfer Specification
All UI boxes, interactive triggers, and cards discard rounded borders (`border-radius: 0px`). Instead, corners are clipped using precise CSS clip-path polygons:
- **Small Elements (Chips, Buttons, Inputs)**: 6px chamfer cut:
  `clip-path: polygon(6px 0, calc(100% - 6px) 0, 100% 6px, 100% calc(100% - 6px), calc(100% - 6px) 100%, 6px 100%, 0 calc(100% - 6px), 0 6px)`
- **Large Panels (Cockpit Enclosures, Hangar Cards)**: 12px chamfer cut:
  `clip-path: polygon(12px 0, calc(100% - 12px) 0, 100% 12px, 100% calc(100% - 12px), calc(100% - 12px) 100%, 12px 100%, 0 calc(100% - 12px), 0 12px)`

### Symbolic Geometry
Indicators and focal markers make deliberate use of 45-degree rotated diamonds, hexagrams, and 8-pointed solar star nodes. Circular forms are reserved exclusively for rotating targeting reticles, mandalas, and planetary orbital maps.

## Components

### 1. Buttons (`VedicButton`)
- **Structure**: Chamfered 8-point polygon with 1px border. Height 44px (compact: 36px).
- **Primary (Divine Gold)**: Background `rgba(233, 196, 0, 0.12)`, border `rgba(233, 196, 0, 0.85)`, text `#FFF6DF`. Font `Cinzel` 13px bold, letter-spacing `0.18em`. Outer glow: `drop-shadow(0 0 12px rgba(233, 196, 0, 0.35))`.
  - *Hover State*: Background transitions to `rgba(233, 196, 0, 0.28)`, scale expands to `1.02x`, outer glow expands to `20px`.
  - *Active / Pressed*: Scale snaps to `0.98x`, solid gold flash.
- **Secondary (Prana Cyan)**: Background `rgba(0, 219, 231, 0.08)`, border `rgba(0, 219, 231, 0.6)`, text `#74F5FF`.
- **Destructive (Astra Red)**: Background `rgba(191, 0, 54, 0.12)`, border `rgba(191, 0, 54, 0.8)`, text `#FF6B72`.
- **Keyboard Accelerators**: Embedded trailing badge in `JetBrains Mono` 10px (e.g., `[SPACE]`, `[ESC]`) rendered with a faint slate border.

### 2. Cards & Cockpit Panels
- **Structure**: Obsidian panel with 12px beveled corners, backed by a 1px cyan or brass outline.
- **Surface Texture**: Subtle 3px repeating horizontal CRT scanline pattern at 4% opacity overlaid above the obsidian base.
- **Corner Brackets**: Brass or cyan vector L-brackets framing the four corners with an inset diamond rivet.
- **Locked Ship Variant**: Desaturated grayscale wireframe, overlaid with an ancient brass lock emblem and vermilion prerequisite requirement label.

### 3. Segmented Energy & Health Gauges
- **Architecture**: A linear recessed well (`#0E1320`) broken into 12 to 20 discrete rectangular cells with 2px air gaps.
- **Shields**: Filled cells cast a cyan-to-white gradient (`#00DBE7` → `#74F5FF`) with a soft glow.
- **Hull / Prana**: Dynamic chromatic state:
  - `> 60%`: Vedic Jade (`#1EC846`)
  - `30% - 60%`: Solar Amber (`#DCC828`)
  - `< 30%`: Pulsing Crimson Flare (`#DC3C00`)
- **Ghost Damage Trail**: Depleted segments hold a decaying vermilion trail (`#DC2828`) that dissipates over 600ms to visualize impact severity.

### 4. Input Fields
- **Container**: Recessed `#0E1320`, 6px chamfered corners, 1px border `rgba(0, 219, 231, 0.25)`. Height 40px, text color `#F0EDE6` in `Space Grotesk` 14px.
- **Focus State**: Border transitions to Divine Gold `#E9C400` with an amber glow; blinking rectangular terminal block cursor in gold.
- **Data Coordinates**: Pinned labels using `JetBrains Mono` 10px uppercase aligned to the top-left corner bracket.

### 5. Selection Chips & Filter Tabs
- **Geometry**: Compact 6px beveled tags, height 28px.
- **Inactive**: Transparent background, border `rgba(143, 152, 168, 0.3)`, text `#8F98A8` in `Space Grotesk` 12px.
- **Active**: Background `rgba(0, 219, 231, 0.18)`, border `#00DBE7`, text `#FFFFFF` accompanied by an active left diamond indicator pip.

### 6. Boss Threat Banner (`BossBar`)
- Mounted top-center, spanning 600px width.
- Flanked by ancient Sanskrit winged glyph brackets in Temple Brass.
- Dual-line segmented health pool with dynamic phase milestone pips (Phase I, II, III).
- Red alert strobe along the border whenever a special telegraph attack is triggered.

### 7. Sacred Geometry Reticle (`MandalaReticle`)
- Multi-tiered vector mandala used for gunner targeting, radar sweeps, and warp gates.
- Composed of an outer 16-point petal compass, a middle counter-rotating wheel with Vedic numerics, and an inner intersecting Sri Yantra triangle cluster that locks and pulses cyan on hostile entities.
