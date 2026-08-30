# 🛸 Vimana Wars

> **Vimana Wars** is an arcade-style, mythological space shooter built with [Python Arcade](https://arcade.academy/). Pilot celestial Vimanas against demonic Asura armadas, summon Divine Astras, earn blessings from the Devas, and vanquish the Ten-Headed Demon King Ravana!

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

For production hosting, deploy `backend.app:app` with Gunicorn and provide a
managed PostgreSQL `DATABASE_URL`. The included `render.yaml` is a starting
point for HTTPS-hosted deployment; configure the game’s `LEADERBOARD_API_URL`
to the resulting HTTPS API URL before releasing a build.

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
