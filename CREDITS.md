# Vimana Wars — Master Credits & Asset Licenses

This document registers all audio, visual, typography, and engine assets utilized in **Vimana Wars** (C++20 Native Raylib Engine & Python Legacy edition).

---

## 1. Engine & Native Libraries

- **Raylib 6.0**: High-performance multiplatform graphics and windowing library.
  - License: [zlib/libpng License](https://github.com/raysan5/raylib/blob/master/LICENSE)
  - Copyright (c) 2013-2026 Ramon Santamaria (@raysan5)
- **SQLite 3**: Embedded transactional relational database engine.
  - License: [Public Domain](https://www.sqlite.org/copyright.html)
- **Winsock2 (WS2_32)**: Microsoft Windows low-latency asynchronous socket API.
  - Non-blocking UDP LAN packet delivery system.
- **Python Arcade**: Legacy 2D game engine (MIT License).

---

## 2. Typography & Fonts

All font families are licensed under the **SIL Open Font License (OFL) Version 1.1**:

- **Cinzel Bold** (`Cinzel-Bold.ttf`)
  - Author: Natanael Gama
  - License: [SIL Open Font License 1.1](https://scripts.sil.org/OFL)
  - Usage: Primary Title font, Yantra headers, victory declarations, boss telegraph banners.
- **Space Grotesk Bold** (`SpaceGrotesk-Bold.ttf`)
  - Author: Florian Karsten
  - License: [SIL Open Font License 1.1](https://scripts.sil.org/OFL)
  - Usage: Cockpit HUD telemetry, tactical descriptions, pilot profiles, stats breakdown.
- **JetBrains Mono Bold** (`JetBrainsMono-Bold.ttf`)
  - Author: JetBrains
  - License: [SIL Open Font License 1.1](https://scripts.sil.org/OFL)
  - Usage: Network diagnostic overlay (F8 HUD), LAN IP addresses, packet tick numbers.

---

## 3. Audio & Music Architecture

- **Kenney Sci-Fi Sounds Pack** (`assets/online/kenney_sci-fi_sounds/Audio/`)
  - Creator: Kenney (Asset Jesus)
  - License: [Creative Commons Zero (CC0) Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)
  - Assets: Laser blasts (`laserSmall_*.ogg`), impact crunches (`explosionCrunch_*.ogg`), shield deflections, thruster bursts, warning klaxons (`warning_siren.wav`).
- **Celestial Combat Soundtrack** (`assets/sounds/combat_loop.mp3`)
  - Track: "8-bit Epic Space Shooter Music" by HydroGene
  - Source: [OpenGameArt.org](https://opengameart.org/content/8-bit-epic-space-shooter-music)
  - License: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)
- **Dynamic 5-Channel Audio Engine** (`SoundSystem`):
  - Master, Music, SFX, UI, Boss channels with dynamic boss phase pitch/volume escalation.

---

## 4. Visual Art, Sprites & VFX

- **Kenney Space Shooter Extension** (`assets/online/kenney_space-shooter-extension/`)
  - Creator: Kenney
  - License: [Creative Commons Zero (CC0) Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)
  - Assets: Base ship silhouettes and mechanical weapon sprites.
- **Phase 7 Custom Vedic-Cyberpunk Assets** (`tools/generate_phase7_assets.py`):
  - **12 Vimana Vessels**:
    - `airavata.png`: Indra's Multi-tusked Bastion (256×256 RGBA)
    - `kamadhenu.png`: Divine Sustenance Support Chariot (256×256 RGBA)
    - `narasimha.png`: Golden Lion Avatar of Righteous Wrath (256×256 RGBA)
    - `pushpaka.png`, `tripura.png`, `garuda.png`, `vajra.png`, `naga.png`, `agneyastra.png`, `soma.png`, `kubera.png`, `surya.png`
  - **5 Campaign Boss Titans**:
    - `boss_makara.png`: Terror of Kshira Sagara
    - `boss_indrajit.png`: Sorcerer of Lanka (320×320 RGBA)
    - `boss_kumbhakarna.png`: Sleeping Colossus Dreadnought
    - `boss_meghnada.png`: Master of Thunder and Illusion
    - `boss_hiranyakashipu.png`: Immortal Demon Emperor (360×360 RGBA)
  - **7 Layered Parallax Realms**:
    - `realm_swarga.png` (Swarga Outpost)
    - `realm_kshira_sagara.png` (Ocean of Milk)
    - `realm_dandaka_void.png` (Dandaka Asteroid Void)
    - `realm_lanka_approach.png` (Molten Citadel Approach)
    - `realm_setu_expanse.png` (Bridge of Floating Spheres)
    - `realm_naraka_forge.png` (Naraka Foundries)
    - `realm_mahayuddha_citadel.png` (Citadel of the Final Apocalypse)
  - **9 Deva Boon Tarot Icons**:
    - `boon_garuda_wings.png`, `boon_vajra_strike.png`, `boon_surya_blessing.png`, `boon_varuna_shield.png`, `boon_vayu_celerity.png`, `boon_yama_reap.png`, `boon_agni_inferno.png`, `boon_soma_nectar.png`, `boon_narasimha_berserk.png`
  - **6 Tactical Ability Icons**:
    - `icon_chakram.png`, `icon_brahmastra.png`, `icon_dash.png`, `icon_soma.png`, `icon_vajra_flare.png`, `icon_kavach.png`
  - **4 Combat Particle VFX**:
    - `vfx_laser_glow.png`, `vfx_shield_hex.png`, `vfx_yantra_mandala.png`, `vfx_spark.png`

---

## 5. Procedural UI Design System

- Built with native Raylib vector geometry in `cpp_game/include/ui/vedic_theme.hpp`:
  - `DrawYantraPanel`, `DrawChamferedPanel`, `DrawGlowBorder`, `DrawYantraCornerDeco`
  - Resolution-independent procedural vector glyphs: `DrawStarIcon`, `DrawVedicDiamond`, `DrawCircularGauge`, `DrawPipMeter`, `DrawLockIcon`, `DrawCheckmarkIcon`, `DrawWarningIcon`, `DrawScanlines`.
