# Vimana Wars — Vedic-Punk UI Design

This is the implementation guide for the visual overhaul supplied in
`stitch_vimana_wars_visual_overhaul.zip`. It translates the Stitch web mockup
into the existing Python Arcade game rather than copying HTML/Tailwind.

The implemented UI pass lives in `game/ui/vedic_theme.py`, `game/ui/hud.py`,
`game/ui/boss_bar.py`, `game/ui/menu_button.py`, `game/views/menu_view.py`,
`game/views/ship_select_view.py`, and `game/views/stats_view.py`. The generated
PV and design references are tracked in the workspace root and catalogued in
`assets/design/README.md`.

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
- **Multiplayer / Sangha Network:** split the screen into an "Open Wings"
  lobby list and a right-side command panel. Use cyan for connected/ready
  players, gold for the selected lobby code, red for unavailable actions, and
  keep the player Game ID visible so invitations are unambiguous.

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
- Treat the HTTP multiplayer layer as lobby/matchmaking only. Live movement,
  combat, and authoritative state must use a real-time transport in a later
  game-server layer.

## Narrative Spine — "The Reclamation of Dharma"

Dharma — cosmic balance — is unraveling. Ravana, Lord of the Asuras, has broken his ancient exile and corrupts the celestial realms one by one, drawing their Prana to fuel his full resurrection. The player is the last pilot of the Celestial Order, sent into falling heavens to burn a corridor to Lanka and restore cosmic order.

### Act Breakdown
- **Act I — Swarga: The Heavenly Celestial Realm (Waves 1–3):** Outer wards breached. The war begins in heaven itself. Tutorial in disguise; players witness a sacred realm begin to crack.
- **Act II — Kshira Sagara: The Cosmic Ocean of Milk (Waves 4–6):** Primordial ocean corrupted. At Wave 5, Kumbhakarna (slumbering titan) is awakened from the depths to guard the expanse.
- **Act III — Dandaka Void: The Mystical Astral Forest (Waves 7–9):** Piercing into hostile territory where reality thins. Feral Asura swarms and disorienting fauna test player reflexes before the point of no return.
- **Act IV — Lanka: The Molten Rift of Ravana (Wave 10):** The final siege against Ravana. All systems, Astras, and evasion mechanics are tested at once.

### Vimana Lineage & Pilot Lore
- **Pushpaka Mk-I:** The balanced flagship chariot of kings and gods. Steady, enduring, built to survive the full campaign.
- **Tripura Destroyer:** Heavy fortress hull with impenetrable plating and piercing railguns. Outlasts and shatters enemy fire.
- **Garuda Interceptor:** High-speed void striker named for Vishnu's mount. Trades durability for supreme evasion, rapid needle blasters, and dual dashes.

### Endings
- **Victory — "Karmic Transcendence":** Ravana falls, Dharma is restored across all realms. The Dharmic Ledger logs total reclaimed karma.
- **Defeat — "Dharmic Rebirth":** Physical hull lost, but Karma returns to the Akashic Records to reincarnate (`[R] REINCARNATE`, `[ESC] RETURN TO SOURCE`).

---

## Deployment Guide: Multiplayer & Cloud Backend

### Free Deployment via Render.com (Recommended)

Render provides free hosting for Python web services with direct GitHub integration and zero server administration:

1. **Sign Up / Log In:** Go to [render.com](https://render.com) and sign in using your GitHub account.
2. **Create New Web Service:**
   - Click **New +** → **Web Service**
   - Select your repository: `chetan270418-exe/Vimana-Wars`
3. **Configure Service Settings:**
   - **Name:** `vimana-wars-api`
   - **Root Directory:** `backend` (or leave root if using the included `render.yaml`)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r ../requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free (750 free hours/month)
4. **Environment Variables:**
   - `SECRET_KEY`: `<generate-a-random-secret-key>`
   - `REQUIRE_EMAIL_VERIFICATION`: `0` (or `1` if configuring SMTP)
   - `DATABASE_URL`: Leave empty for zero-config SQLite (`leaderboard.db`), or provide a PostgreSQL connection URI (e.g. from Supabase or Neon).
5. **Connect Client to Live Server:**
   - Copy your Render URL (e.g., `https://vimana-wars-api.onrender.com`).
   - In `constants.py`, update:
     ```python
     API_BASE_URL = "https://vimana-wars-api.onrender.com"
     ```

### Free Cloud Database Options

| Provider | Free Tier Specification | Best Use Case | Setup Simplicity |
|---|---|---|---|
| **SQLite (Built-in)** | Zero setup, local file | Testing & small lobbies (<10,000 runs) | Instant (0 min) |
| **Supabase** | 500 MB PostgreSQL, free forever | Production cloud database with full SQL | 2 min (`DATABASE_URL=...`) |
| **Neon.tech** | 3 GB Serverless PostgreSQL | High performance with auto-sleep | 2 min (`DATABASE_URL=...`) |
| **Render PostgreSQL** | 1 GB Free PostgreSQL (90 days) | All-in-one with Render service | 1 min in Render dashboard |

### AWS Deployment Alternatives (Using Your AWS Account)

- **AWS EC2 (t2.micro Free Tier):**
  - 12 months free on AWS Free Tier.
  - Full Ubuntu Linux server control with nginx reverse proxy and systemd service running gunicorn.
  - Best for learning Linux systems administration and devops.
- **AWS App Runner:**
  - Fully managed container service. Directly connect your GitHub repo and let AWS build and scale the Flask app.
- **AWS RDS (db.t2.micro Free Tier):**
  - 12 months free managed PostgreSQL (20 GB storage). Pair with EC2 or Render via standard `DATABASE_URL`.
