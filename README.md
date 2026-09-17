# 🛸 Vimana Wars // Dual-Engine Celestial Combat

> **Vimana Wars** is an arcade mythological space shooter set in the Vedic cosmos. Available in two full implementations:
> 1. ⚡ **C++ Engine (`cpp_game/`)**: High-performance native C++20 / Raylib 6.0 desktop build running at 60 FPS with custom DSA, 12 ships, 30 waves, 4-player co-op squad room, and SQLite3 persistence.
> 2. 🐍 **Python Edition (`python_game/`)**: Original Python Arcade edition, featuring the full modular game, backend REST/Socket.IO services, and **`vimana_wars_python_all_in_one.py`** (all 77 source modules in one single file).

---

## 📂 Repository Structure
```
Vimana-Wars/
├── cpp_game/                       # ⚡ Native C++20 Desktop Game (Raylib 6.0 + SQLite3)
│   ├── bin/VimanaWars.exe          # Compiled 64-bit Windows Binary
│   ├── include/                    # Core headers, entities, views, and DSA
│   ├── src/main.cpp                # Master game loop & FSM
│   └── build.bat                   # 1-click C++ compilation script
├── python_game/                    # 🐍 Python Arcade Edition
│   ├── game/                       # Modular Python packages (entities, systems, UI, views)
│   ├── backend/                    # Flask REST API & Socket.IO server
│   ├── tests/                      # Automated unit tests
│   ├── main.py                     # Entry point (python main.py)
│   ├── vimana_wars_python_all_in_one.py # Complete 77-file consolidated Python archive
│   └── start_python_game.bat       # 1-click Python batch launcher
├── assets/                         # Shared images, audio, and font assets
├── vimana_wars_python_all_in_one.py # Root copy of consolidated Python archive
├── start.bat                       # Interactive launcher (C++ or Python)
├── start_cpp_game.bat              # Direct C++ launcher
└── start_python_game.bat           # Direct Python launcher
```

---

## 🎮 Key Features

- **9 Distinct Ship Archetypes** (three starters plus six campaign unlocks):
  - 🪽 **Pushpaka**: Balanced celestial cruiser with all-round combat stats.
  - 🛡️ **Tripura**: Heavily armored dreadnought with increased hull HP and high-impact plasma cannons.
  - 🦅 **Garuda**: Hyper-agile vanguard vessel with twin dash charges, high fire rate, and nimble handling.
  - ⚡ **Vajra Spear**, 🐍 **Naga Coil**, 🔥 **Agneyastra**, 🌙 **Soma Ark**, 💰 **Kubera Galleon**, and ☀️ **Surya Flare** unlock as you reach later campaign waves. Each uses its own Kenney CC0 ship sprite and combat profile.

- **8 Roguelite Deva Boons & Blessing Upgrades**:
  - 🔥 **Agni's Solar Fury**: Burning damage-over-time that causes defeated foes to detonate in fiery explosions.
  - ⚡ **Indra's Vajra Thunderbolt**: Chance on hit to unleash chain lightning zapping nearby enemies.
  - 🌪️ **Vayu's Gale Tempest**: 35% dash cooldown reduction and damaging wind cyclones left in your wake.
  - 🦅 **Garuda's Celestial Magnet**: Magnetically pulls power-ups and healing drops towards your ship.
  - 🌊 **Varuna's Oceanic Ward**: Maximum HP bonus and passive celestial health regeneration.
  - 🪓 **Sudarshana Keen Edge**: Massive Chakram weapon size and damage increase with reduced cooldown.
  - 💀 **Yama's Fatal Decree**: +60% critical execution damage against weakened enemies.
  - ☀️ **Surya's Radiant Pierce**: Every 7th shot fires a golden piercing solar slug.

- **6 Asura Enemy Vessels & 4 Boss Battles across 20 campaign waves**:
  - **Asura Chaser (Fast)**: Swarming vanguard scouts.
  - **Asura Brute (Tank)**: Armored heavy cruisers with visual hull cracking under damage.
  - **Asura Shooter (Ranged)**: Tactical spread gunships.
  - **Asura Kamikaze**: High-speed suicide interceptors with AOE blast radius.
  - **Asura Healer**: Priest vessels that emit regenerative waves to nearby allies.
  - **Asura Sniper**: Long-range railgun snipers with telegraphed laser sights.
  - 🛡️ **Titan Kumbhakarna (Wave 5 Mini-Boss)**: Shockwave slams and ground pounds.
  - 👑 **Emperor Ravana (Wave 10 Boss)**: Multi-phase emperor fight with rotating spiral voids and fleet summons.
  - 🐂 **Warlord Mahishasura (Wave 15 Mini-Boss)**: A charging late-campaign warlord with escalating pressure.
  - ⚡ **Storm Serpent Vritra (Wave 20 Final Boss)**: The campaign's final multi-phase citadel guardian.

- **Astral Ability Cubes**:
  - Collect rotating 3D-style cubes during combat for Kavach shields, Agneyastra spread fire, Vayavyastra speed, Amrita healing, Brahmastra bombs, and Astra Overdrive rapid fire.
  - Active effects are shown in the HUD, with pickup notifications and achievements for dedicated collectors.

- **Campaign Progression & Achievements**:
  - Seven connected realm nodes unlock through campaign progress, with nine warships gated by wave milestones.
  - Trophy cabinet tracks combat, bosses, boon mastery, ability-cube collection, ship mastery, and full-campaign clears.

- **Visual Overhaul & PV Deliverables**:
  - Vedic-Punk UI redesign applied to the Arcade game: animated telemetry, scanlines, chamfered panels, selection pulses, cockpit HUD framing, and accessibility-aware motion.
  - Design references and the generated PV are tracked in the workspace root: `main-menu-ui.png`, `mission-control-hud.png`, `astra-arsenal.png`, `boss-overlay-system.png`, and `vimana_wars_pv_final.mp4`.
  - Planning documents: `vimana-wars-pv-storyboard.md` and `vimana-wars-final-video-prompt.md`.
  - Automatic launch sequence: the bundled PV plays inside the game window,
    then transitions into the loading screen and finally the story/menu flow.

- **Polished Combat Juice & Visuals**:
  - 🌌 Parallax cosmic background with drifting mythological realms.
  - ✨ Procedural particle sparks, engine flares, and explosion bursts.
  - 🎯 Off-screen threat radar with directional arrows for enemies and collectables.
  - 💥 Dynamic screen shake, hit stop, combo multiplier meter, and rising combat damage numbers.

- **Audio & Soundtrack**:
  - 🎵 CC0 combat soundtrack (*HydroGene via OpenGameArt.org*).
  - 🔊 Built-in procedural audio synthesizer for fallback sound generation.
  - 🎚️ Independent SFX and Music volume sliders in settings.
  - 🚨 Boss warning, roar, wave-clear, dodge, synergy, pickup, and UI feedback cues.

- **Global Online Leaderboard**:
  - REST API built with Flask + SQLite (`backend/app.py`).
  - Asynchronous score submission and top leaderboard viewer.
  - Optional email login/registration from the in-game **ACCOUNT** screen.
  - Stable `VMN-XXXXXXXX` Game IDs attach authenticated scores to one player;
    offline guest play remains available.

- **Multiplayer Lobby Network**:
  - Main Menu → Multiplayer opens the authenticated Sangha lobby browser.
  - Players can create or join campaign/endless wings, select a ship, ready
    up, start as host, and leave safely with host transfer.
  - The current implementation is the pre-match lobby layer; real-time
    synchronized combat requires a dedicated authoritative game server.

---

## 🕹️ Controls

| Action | Keyboard | Mouse / Gamepad |
|---|---|---|
| **Move / Fly** | `W`, `A`, `S`, `D` / Arrow Keys | Left Analog Stick |
| **Aim & Shoot** | Mouse Cursor + Hold `LMB` | Right Analog Stick (360°) + `RT` |
| **Vayu Dash** | `Space` / `Left Shift` | `RMB` / `LB` / Gamepad Button 4 |
| **Sudarshana Chakram** | `Q` / `E` | `MMB` / Gamepad Button 3 |
| **Brahmastra Bomb** | `F` | Gamepad `X` / `LT` |
| **Pause / Resume** | `ESC` | Gamepad Start / Button 7 |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10 or higher (Tested on Python 3.11)
- The desktop launch cinematic uses `opencv-python-headless` for MP4 frame
  decoding. It is installed by the requirements file; if unavailable, the
  game safely skips the cinematic and continues booting.

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/chetan270418-exe/Vimana-Wars.git
cd Vimana-Wars
pip install -r requirements.txt
```

### 3. Launch the Game
```bash
python main.py
```

### 4. Optional: Run Local Leaderboard Backend
In a separate terminal window:
```bash
python backend/app.py
```

The game shows **GUEST MODE** until the backend is running and an account is
linked from **Main Menu → ACCOUNT**. After registration, the local session is
remembered between launches and authenticated leaderboard scores use the
displayed Game ID.

### 5. Run the React Web Frontend

The URL that returns the endpoint JSON is the API health page, not the web UI.
Run the React/Vite frontend separately:

```bash
cd web
pnpm install --frozen-lockfile
pnpm run dev
```

To point the web UI at a different API during development:

```bash
VITE_API_URL=http://127.0.0.1:5000 pnpm run dev
```

The Render blueprint now defines two services: `vimana-wars-api` for Flask and
`vimana-wars-web` for the static React build. Configure `CORS_ORIGINS` on the
API with the final web URL if you rename either service.

If PowerShell says `pnpm` is not recognized, Node.js/npm is enough:

```powershell
cd web
.\start_web.ps1
```

The helper uses pnpm when available and automatically falls back to npm. If you
are already inside `web`, do not run `cd web` a second time.

If the project already has `web/node_modules`, the helper reuses it and starts
Vite directly. This avoids an npm 11 false `Unsupported URL Type
"workspace:*"` error caused by pnpm's internal links. You can also run
`npm run dev` directly from `web` after dependencies are installed.

For the desktop game, keep the virtual environment active and run:

```powershell
cd "D:\Vimana Wars"
python main.py
```

To connect the desktop build to a hosted API, set the URL before launching:

```powershell
$env:VIMANA_API_URL = "https://vimana-wars.onrender.com"
python main.py
```

For production hosting, deploy `backend.app:app` with Gunicorn and provide a
managed PostgreSQL `DATABASE_URL`. The included `render.yaml` is a starting
point for HTTPS-hosted deployment; set `VIMANA_API_URL` to the resulting HTTPS
API URL before releasing a build.

### Vercel web deployment

The API URL and the visual web UI are different services. In Vercel, either set
the project Root Directory to `web` (Build Command `npm run build`, Output
Directory `dist`) or deploy from the repository root using the included
`vercel.json`. Add the environment variable
`VITE_API_URL=https://vimana-wars.onrender.com`, redeploy, and open the Vercel
URL—not the Render API URL. A successful API root response is JSON by design;
it is not the game website.

The included Render defaults keep email verification off because the project
does not yet have an SMTP provider configured; otherwise new accounts would be
created but users would never receive their verification token. Enable
`REQUIRE_EMAIL_VERIFICATION=true` only after wiring a transactional email
provider and a secure verification-email delivery path.

---

## 🧪 Running Automated Tests

Run the full automated test suite with `pytest`:
```bash
python -m pytest
```

---

## 📦 Building a Standalone Executable

To bundle Vimana Wars into a standalone `.exe` for distribution:
```bash
python build_exe.py
```
The output executable will be generated in `dist/VimanaWars/`.

---

## 📜 License & Credits

- Game Code: MIT License
- Framework: [Python Arcade](https://arcade.academy/)
- Audio: Attributions listed in [`CREDITS.md`](CREDITS.md) (CC0 Public Domain).
