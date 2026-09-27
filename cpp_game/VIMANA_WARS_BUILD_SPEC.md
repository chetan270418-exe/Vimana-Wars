# Vimana Wars — Complete Build Specification (C++ / Raylib 6.0)
**Purpose:** Hand this document to your coding agent (Codex/Claude/ChatGPT) as the single source of truth for what to build, fix, and improve. Every section has: current state → what's wrong/missing → exact implementation → acceptance test.
**My decision up front:** Stay on C++20 + Raylib. Do NOT port to Unity (C#) — you'd rewrite 60 ships, 300 waves, and the netcode for zero player-visible gain. All work below is incremental on `cpp_game/`.

---

## 0. Master Gaps (executive summary)

### ❌ Still missing entirely
1. **Armory / Ship Shop view** — coins are earned (`grant_run_completion_reward`) but there is no shop destination in the FSM. The economy loop is open-ended.
2. **Boss ability framework** — bosses have phases and names but no scripted ability kits, telegraphs, or add-summons.
3. **Ship-unique ACTIVE abilities** — ships differ only by stats + gun_type. No per-ship ability on a key.
4. **Enemy squad/formation AI** — enemies fight as individuals; no coordinated tactics.
5. **Story/dialogue system** — no `DialogueView`, no script files, no branching, no allegiance choice.
6. **Public multiplayer (internet)** — only LAN UDP by IP. No room registry, no NAT traversal, no reconnect.
7. **Team/shared lives UI** — `coop_rule()` exists in DB but no shared-hearts HUD, no squad-life config screen.
8. **Rebindable controls, tutorial/onboarding, daily quests, cloud save, stats screen.**

### 🐛 Actually broken
1. **Co-op rule desync** — every client calls `start_with_ship(..., DBSystem::coop_rule())` from *local* DB. Host set HARDCORE, client set REVIVE → different simulation rules → desync. Rule must travel in the snapshot.
2. **`num_squad` default = 2** when `players()` is empty — solo starter gets 2-player scaling.
3. **Fake ping** — `peer.ping_ms = max(5, (int)(hdr.ack % 60))` uses the tick counter as RTT. Not real ping.
4. **Reward double-grant risk** — act-clear rewards (in `WAVE_CLEAR` path) and `grant_run_completion_reward` (in `GAME_OVER` path) can both fire for one run. Needs a `reward_granted` flag.
5. **AI takeover freezes input** — a timed-out peer keeps applying its last `InputPacket` forever; ship flies into a wall. Needs a real autopilot.
6. **`NET_INTERP_DELAY` unused** — remote players snap; no interpolation buffer.
7. **Multiplayer game over grants no Prana** — `MULTIPLAYER_RESULT` never calls `grant_run_completion_reward`.
8. **Wallet not saved at purchase moment** — if the game crashes after buying a ship, coins/ships are lost.

### ⚠️ Implemented but weak
- UI: 18 hand-rolled views with no shared widget library → inconsistent look/feel.
- Waves: linear difficulty; no performance-reading "director".
- Score: flat values; no style bonuses (graze, no-hit, multi-kill).
- Save: schema not versioned; no migration path; no cloud conflict rule.
- Performance: no texture atlas, no particle pooling, O(n×m) collision, per-frame string-key lookups.
- Audio: static soundtrack; no intensity layers, no low-HP feedback, no kill-confirm differentiation.

---

## 1. 🪙 Coins / Score / XP / Unlocks / Upgrades

### Current state
- Prana exists; ships have `prana_cost`; `grant_run_completion_reward(is_vic, xp)` exists; `DBSystem` persists.

### Build it
**Constants** (`core/constants.hpp`):
```cpp
constexpr int PRANA_GAME_OVER_BASE     = 40;
constexpr int PRANA_PER_1000_SCORE     = 10;
constexpr int PRANA_PER_WAVE           = 8;
constexpr int PRANA_VICTORY_BONUS      = 500;
constexpr float PRANA_COOP_TEAM_BONUS  = 1.25f;  // all squad members alive at end
constexpr float PRANA_HARDCORE_MULT    = 2.5f;
constexpr int XP_PER_WAVE              = 15;
constexpr int XP_PER_BOSS              = 120;
// Pilot levels: level n requires 100*n*(n+1)/2 cumulative XP
inline int xp_for_level(int lvl) { return 100 * lvl * (lvl + 1) / 2; }
```

**DB schema (version 2)** — add tables/columns: `prana INT`, `pilot_xp INT`, `owned_ships TEXT` (comma ids), `settings_json TEXT`. Bump `DB_VERSION`, write a migration: if version < 2 → `ALTER TABLE` / defaults.

**DBSystem API** (must be atomic, must save immediately):
```cpp
int  prana() const;
bool add_prana(int amount, const char* reason);   // adds + save_game()
bool spend_prana(int amount);                     // false if insufficient
bool owns_ship(const std::string& id) const;
bool unlock_ship(const std::string& id);          // spends prana, verifies cost, saves
int  pilot_level() const;                         // derived from xp_for_level
```

**Reward formula** (single function, idempotent):
```cpp
// game_view.hpp
struct RunReward { int prana; int xp; bool granted; };
RunReward compute_run_reward(bool victory, int wave, int score,
                             int squad_size, int squad_alive, CoopRule rule);
```
- `granted` flag prevents double-pay across WAVE_CLEAR → GAME_OVER transitions.
- HARDCORE rule multiplies Prana ×2.5.
- Co-op: if `squad_alive == squad_size`, ×1.25 team bonus.

**ArmoryView** (new view, `ViewType::ARMORY`) — see §5 for UI spec. Two tabs: FLEET (grid of all 60 `SHIP_FLEET` entries, locked ones show `prana_cost` or boss-unlock requirement, owned show OWNED), CONSUMABLES (Kavach/Soma/Vajra). Purchase → `spend_prana` → unlock → play coin sfx + ship fly-in animation. Wire into main.cpp FSM: `GameOverView` button "VISIT ARMORY" → ARMORY → MENU.

**Score system improvements**:
```cpp
constexpr int SCORE_GRAZE          = 25;   // exists
constexpr int SCORE_MULTIKILL_STEP = 50;   // each kill within 1.5s of last adds +50 chain
constexpr int SCORE_NO_HIT_WAVE    = 200;  // exceeds BONUS_PERFECT_WAVE(75) — raise it
constexpr int SCORE_STYLE_DASH_KILL= 75;   // kill while dashing through enemy
```
Add a combo multiplier meter (exists) → make it affect score AND Prana (score/1000 prana uses combo-multiplied score). Death resets multiplier — already the genre standard.

**Upgrade track** (meta-progression, keeps runs meaningful): in Armory, per-ship upgrade slots ×3: HULL +15% HP each, CANNON +10% dmg each, THRUSTER +8% speed each. Cost: 200/400/800 Prana. Store per-ship upgrade levels in DB. Applied at `start_with_ship`.

**Acceptance:** Play a run to wave 10, die → game over shows animated Prana payout → Armory opens → buy Vajra Spear (350) → ship appears in loadout → restart game → new ship usable. Force-kill process after purchase → relaunch → ship still owned, Prana deducted.

---

## 2. 👾 Enemy + Boss Variety and Abilities

### Enemy work
**Add 2 new archetypes** (data in wave tables):
- **Asura Minelayer**: drops proximity mines (telegraphed 0.5s beep + glow), forces movement.
- **Asura Carrier**: slow, high HP, launches Chaser squads every 8s until destroyed. Killing it early = skill expression.

**Elite affixes** (random 1–2 per elite, shown by aura color):
- REFLECTIVE (30% damage returned), SWIFT (speed ×1.5), REGEN (2% HP/s), VOLATILE (explodes on death, larger radius).

**Squad AI** — new lightweight system:
```cpp
enum class SquadTactic { SWARM, PINCER, SCREEN, FOCUS_FIRE, ESCORT };
struct Squad {
    std::vector<size_t> members;  // indices into enemy array
    SquadTactic tactic;
    float retask_timer = 4.0f;    // re-evaluate every 4s
};
```
- SCREEN: Brutes form a horizontal wall; Shooters/Snipers fire from behind it.
- PINCER: Chasers split into two groups that converge on the player.
- FOCUS_FIRE: all ranged enemies target the lowest-HP player (co-op only) — forces peeling.
- ESCORT: Healers stay behind Brutes; killing the wall opens them up.
Squads are assigned in the wave-spawn table; one brain tick per second per squad; members just follow orders. This is the single biggest "fun" upgrade for combat feel.

### Boss framework
```cpp
struct BossAbility {
    const char* name;            // "Dasha Barrage"
    float cooldown, telegraph;   // telegraph = wind-up with warning visual
    int min_phase;               // phase gating
    void (*execute)(Boss&, GameWorld&);   // or std::function
};
struct Boss {
    int phase;  // 1/2/3 from HP thresholds 100/66/33%
    std::vector<BossAbility> kit;
    float ability_timer;
};
```
**Non-negotiable rule:** every ability has a visible telegraph (≥0.6s glow/warning line/roar sfx). Players must never die to invisible information.

**Per-boss kits** (6+ abilities for act bosses, 2 for mini-bosses):
- **Tyrant Hiranyakashipu** (Act 1/9): Aegis Bubble (invuln 3s, must kill adds), Solar Flare line-beam, Summon Honor Guard, Enrage.
- **Meghnada, Storm Illusionist** (Act 2/10): **Mirror Clone** (3 copies, only one takes damage — the tell is subtle color), Lightning Grid (telegraphed cross-hatch zones), Blink Strike.
- **Vritra, Sky-Sealing Serpent**: **Seal Dash** (disables player dash 5s — UI shows padlock), Flood Wave (slow-moving wall, dash through gap), Coil (wraps arena edge, spawns bullet spiral inward).
- **Emperor Ravana** (signature, 10 abilities — one per head): Spiral Void (P1), Fleet Summon (P1), Dasha Barrage 10-lane (P2), Illusion Step + decoy explosion (P2), Throne Crush shockwave with gap (P3), Enrage (P3).
- **Makara, Abyssal Leviathan**: Tidal Pull (gravity well drags player), Undertow (arena floods from bottom 3s, bottom half is damage zone), Devour (telegraphed bite — dodge window).
- **Indrajit, Conqueror**: Serpent Arrows (homing, destructible), Shakti spear (aimed railgun, 1.2s telegraph), Vanish (untargetable 2s, reappears behind lowest-HP player).

Phase transitions: 0.8s slow-mo + roar + arena flash + music sting + HP bar segment break.

**Acceptance:** Each act boss uses ≥4 abilities with telegraphs; killing adds is required during at least one boss's invuln phase; no unavoidable damage patterns exist (verify: every bullet pattern has a gap ≥ player radius + dash distance).

---

## 3. 🚀 Ships + Unique Abilities

### Problem
60 ships × stat-only differences = no identity. Players will fly 3 ships and ignore 57.

### Solution — one ACTIVE ability per ship (key `RMB`/`Q`… pick one, bindable)
Add to `ShipArchetype`:
```cpp
enum class ShipAbilityType {
    NONE,
    OVERDRIVE,   // +80% fire rate 4s          (Garuda, Marut)
    AEGIS,       // 2s invuln bubble           (Soma Ark, Lakshmi Grace)
    BLINK,       // teleport 140px to cursor   (Ketu Shadow, Garuda Prime)
    NOVA,        // radial knockback + damage  (Shiva's Eye, Tripura)
    DRONE,       // orbital drone 6s           (Vishnu Prime, Indra's Chariot)
    BERSERK,     // +damage as HP drops, 5s    (Narasimha, Kali Storm)
    SALVAGE,     // vacuum all pickups         (Kubera Galleon)
    REPAIR_AURA, // heal 25 HP over 3s         (Dhanvantari, Kamadhenu)
    NULL_FIELD,  // enemy bullets slowed 50%   (Rahu Devourer)
};
ShipAbilityType ability = ShipAbilityType::NONE;
float ability_cooldown = 12.0f;
```
Starter ships get simple abilities (Pushpaka = small NOVA, Tripura = AEGIS, Garuda = OVERDRIVE) so new players learn the mechanic. Cooldown shown as a radial icon near the dash pips. **Balance rule:** ability power ∝ ship tier — Tier 1 abilities ~60% the strength of Tier 6, but Tier 1 ships have no unlock cost. This keeps starters viable (roguelite principle).

Also add **per-ship passive** derived from `gun_type`: BURST fires 3-round bursts, PIERCE shots pass through 2 enemies, BURN applies 3s DoT. Verify these are actually implemented in the bullet system — the field exists in data; if fire logic ignores it, that's a 🐛.

**Acceptance:** Every one of the 60 ships has a non-NONE ability; ability icon + cooldown visible in HUD; using ability has sfx + VFX; AI squadmates in co-op use their abilities on cooldown.

---

## 4. 👥 4-Player Co-op Architecture

### Current state
LAN UDP, host-authoritative snapshots, input sync, 15s-timeout AI takeover. Decent bones.

### Build it (in order)
1. **Rules from host, never local DB.** Add `uint8_t coop_rule` to `SnapshotPacket` + `LobbyMessage`. Clients must override their local rule on first snapshot. (Fixes desync bug #1.)
2. **True player count** — host includes `player_count` in the start broadcast; clients never infer from `players().size()`. (Fixes bug #2.)
3. **Real ping** — timestamp echo: client sends `InputPacket` with `send_time_ms = GetTime()*1000`; host replies with `PING_ECHO` containing it; client computes RTT. Update HUD lobby ping with real values.
4. **Interpolation** — client keeps the last 2 snapshots (they arrive at tick rate); render remote entities 33ms (`NET_INTERP_DELAY`) in the past, lerping position/angle. Local player: predict own movement, reconcile when snapshot divergence > 8px (`NET_RECONCILE_THRESHOLD` exists).
5. **Snapshot bandwidth** — full-state snapshots every tick is wasteful. Send at 20Hz (movement lerps anyway); include full enemy list only every 5th packet, deltas otherwise. Cap `SnapshotPacket` arrays to real counts + explicit count fields.
6. **Reconnect** — on disconnect, keep slot reserved for `NET_RECONNECT_WINDOW` (15s exists). Rejoining client sends `REJOIN_REQUEST` with old `player_id`; host restores state. After window → AI takeover (already exists) **but with real autopilot**: implement a simple wingman AI (seek nearest enemy, strafe, fire when in range) instead of frozen last-input (bug #5).
7. **Public rooms (internet play)** — you already run a Flask backend (`backend/app.py`). Add endpoints:
   ```
   POST /rooms        → host registers {code, ip, port, mode, players, max_players}
   GET  /rooms        → list of open rooms
   POST /rooms/<code>/heartbeat  → every 25s
   DELETE /rooms/<code>          → on session end
   ```
   Clients browse rooms in `MultiplayerView` (list instead of raw IP entry). **NAT:** UDP hole-punching needs a rendezvous; simplest robust path is integrating Valve's GameNetworkingSockets (Steam relay) — note it as a stretch goal; LAN + room registry covers most friend-groups.
8. **Squad Nova** — the `CO_OP_ASTRA_SYNC_WIN` (1.5s window) becomes a real mechanic: all players hit Brahmastra within 1.5s → screen-clearing Squad Nova + team combo buff (exists: `TEAM_COMBO_BUFF_*`). This creates shouted "PRESS F NOW" moments — the best co-op emotion.

**Acceptance:** 4 instances on one machine (loopback) run a full wave in sync; client sees smooth remote movement at 200ms artificial latency (use a lag switch / clumsy to test); host quits mid-wave → host-transfer works or run ends cleanly with message; rules change on host applies to all clients.

---

## 5. ❤️ Death / Revive / Team-Life System

### Current state
`REVIVE_TIME 3.5s`, `DOWNED_TIMER 15s`, AI takeover. `CoopRule` exists in DB but only one mode is truly playable.

### Build it
```cpp
enum class CoopRule : uint8_t { REVIVE_MODE = 0, SQUAD_LIVES = 1, HARDCORE = 2 };
```
- **REVIVE_MODE** (current): downed → teammate revives in 3.5s within 80px; bleed-out 15s → eliminated → AI takeover.
- **SQUAD_LIVES**: lobby sets `shared_lives` (default 3, shown as hearts in HUD). Death consumes 1 life → instant respawn at wave-start position with 1.5s invuln. At 0 lives: next death ends the run for everyone: "THE SQUAD HAS FALLEN".
- **HARDCORE** (the user's ask): any death = run over for all. Payout ×2.5. Show a skull icon next to the mode in lobby; require unanimous ready-up in lobby to start (all 4 must confirm HARDCORE).

**HUD:** top-center row of heart icons (shared), each player's frame greys out + "DOWN" tag when downed, revive progress ring over downed ally, bleed-out bar. In HARDCORE, when anyone dies: 1s slow-mo of the death, then fade — make it *felt*.

**Acceptance:** All three rules selectable in lobby (host picks, broadcast per §4.1); SQUAD_LIVES hearts decrement visibly; HARDCORE ends run on first death with correct ×2.5 payout.

---

## 6. 🌊 Wave & Difficulty Scaling

### Current state
Linear wave tables; 4 difficulty profiles; co-op enemy scale `+35%/player`; act modifiers (`RealmModifierType`) exist — good bones.

### Build it
1. **Co-op wave variants** — in co-op, waves use alternate compositions: paired Healers behind Brute walls, simultaneous PINCER + SCREEN squads, elite duos (two elites with complementary affixes). Difficulty multiplier: co-op acts count as +1 act for spawn budgets.
2. **Director AI** (lightweight): every 10s, read `(avg squad HP, recent damage taken, combo)`. If squad is dominating → +15% spawn budget next wave + elite chance up. If struggling → +drop rate of healing cubes. Bounded: never more than ±20% from baseline. Makes waves feel "alive" without rubber-banding.
3. **Escalation curve per act** — within each act of 30 waves: waves 1–10 standard, 11–20 mixed squads + elites, 21–29 heavy variants + events every 3 waves, 30 boss. You have `MiniEventType` defined — schedule it: wave 13 ELITE_INVASION, wave 17 TREASURE_SHIP, wave 24 VOID_RIFT, etc.
4. **Endless scaling** — past wave 300: enemy HP ×1.08^n, new "corrupted" variant palette every 50 waves. Leaderboard seasons reset.

**Acceptance:** A 4-player CHAKRAVYUHA co-op run at act 5 is survivable only with squad coordination (heal share, focus fire); a solo NOVICE run at wave 5 is comfortably winnable by a new player.

---

## 7. 📖 Campaign / Story Progression

### Build it
**DialogueView** (`ViewType::DIALOGUE`): portrait, typewriter text (30 chars/s, click to skip), 1–2 choice buttons, letterbox bars. Data format (plain text, parse at load — no JSON dependency):

```
# node id | speaker | portrait | text
N1|WING COMMANDER TARA|portrait_tara.png|The Asura blockade surrounds Indra's gate, pilot. Your vimana is the only one fast enough to break it.
> Take the vanguard. I'll clear a path.|N2
> Request the Garuda wing as escort.|N3
N2|...|...|Then fly true. [BOON:+5% damage this act]
N3|...|...|Escort granted. [PRANA:+150]
```

**Triggers:** auto-play on entering a boss wave −1 (pre-fight banter), after boss kill (reaction), first unlock of each boss-salvaged ship (flavor). Skippable, re-readable in Codex.

**Two allegiance storylines** — at campaign start choose **DEVA PATH** (defend the realms) or **ASURA PACT** (fight for Ravana's vengeance). Same 300 waves, different dialogue trees, different act cutscenes, different endings, and 2–3 story-choice boons per act (choice grants different boons). Content cost: ~1 dialogue file per act per path (20 files). Replay value doubles.

**Acceptance:** New campaign → allegiance choice screen → act 1 opens with dialogue; choices grant the advertised boon; Codex contains a "Chronicle" tab with all viewed scenes.

---

## 8. 🎨 UI — Main Menu, HUD, Hangar, Loadout

### Build it: a widget library first (`ui/`)
```cpp
namespace ui {
struct Theme {  // single source of truth, from constants.hpp palette
    Color bg, surface, accent, accent2, text, muted, danger;
    Font title, body, mono;
    float corner_radius = 6.0f;
    float anim_fast = 0.12f, anim_med = 0.22f;  // match TransitionManager
};
struct Button { Rect bounds; std::string label; bool hover, pressed; float t; };
// draw/update handle: hover glow lerp → accent, pressed scale 0.97, tick sfx
struct Panel  { /* chamfered corners, 1px accent border, subtle scanline */ };
struct TabBar { /* animated indicator slide */ };
struct RadialCooldown { /* ability/dash icons */ };
struct Toast, Tooltip, ProgressBar, Slider...
}
```
Every view refactored onto these widgets. This is what makes the UI feel "one game" instead of 18 screens.

**Main Menu:** animated starfield + drifting flagship silhouette; menu items with staggered slide-in (0.05s delay each); footer shows pilot level + Prana balance at all times (reminds players of the economy). Settings/Armory/Leaderboard reachable in ≤2 clicks.

**HUD:** ship silhouette with segmented HP pips (not a bar — more readable), dash charges as chevrons, ability radial, combo meter with tier colors, boss banner (name + phased HP bar) top-center, threat radar corners, team frames (co-op) left edge.

**Hangar/Armory:** 3D-ish rotating ship render (just sprite + slow rotation + engine glow), stats as bar comparison vs. currently equipped ship, ability description, price, BUY button with insufficient-funds shake animation.

**Loadout:** ship grid → selected ship big preview → consumable slots → difficulty → LAUNCH. Max 4 clicks from menu to gameplay.

**Loading screen:** parallax starfield, progress bar, rotating tips ("Hold SHIFT to dash — i-frames included", "Kill the Healer first"), lore snippets. Show on: boot, entering gameplay, act transitions.

**Pause:** resume / settings / abandon run (with confirm). Time-scale 0 with blur-ish dark overlay.

**Acceptance:** All buttons share hover/click behavior; no raw `DrawText`+`CheckCollisionPointRec` pairs left outside `ui/`; UI at 1280×720 and 4K scales cleanly (virtual canvas already handles this — verify widgets use logical coords).

---

## 9. 🔊 Audio / VFX / Feedback

1. **Dynamic music:** 2 layers (ambient/combat) + boss stinger. Crossfade by enemy count & boss presence. `SoundSystem` already updates music per frame — add layer mixing.
2. **Kill feedback:** kill-confirm sfx pitch rises with combo (classic arcade dopamine). Hit-marker tick on every hit.
3. **Low-HP state:** heartbeat + desaturated vignette under 25% HP.
4. **Boss:** warning siren on entry, roar per phase change, ability-specific telegraph sounds (distinct per ability type — players learn audio tells).
5. **UI:** hover tick, purchase cha-ching with coin visual, unlock fanfare (short — ≤1.5s).
6. **VFX:** dash afterimage (3 fading sprites), muzzle flashes, enemy hull-cracking (exists for Brute — extend to all), death explosions scaled by ship size, screen-space damage flash toggle in settings (photosensitivity).

**Acceptance:** Mute any single category in settings and it actually mutes; audio tells exist for every boss telegraph; no sfx plays more than 3× per second (voice cap in SoundSystem).

---

## 10. ⚡ Performance

Ordered by expected frame-cost win:
1. **Spatial hash for collisions** — grid cell 64px; bullets×enemies and enemies×chakram. Target: 200 bullets × 50 enemies < 0.5ms.
2. **Particle pool** — fixed 2048 slots, recycling; kill per-frame allocations in the hot loop (explosions, damage numbers).
3. **Texture atlas** — pack ship sprites into 1–2 atlases at `AssetManager::init`; draw calls for ships drop from ~60 to ~2.
4. **Fixed timestep simulation** — sim at 60Hz fixed, render interpolation. Removes dt-clamp slow-mo after hitches (current `dt > 0.1f` clamp = physics slowdown on lag spikes).
5. **Cache archetype pointers** — `GetShipArchetype()` string scan at spawn only; store `const ShipArchetype*` in Player/Enemy.
6. **Sound voice cap** — max 16 simultaneous SFX.
7. Profile with `DebugOverlay` (exists) — add frame-time graph; budget: update < 4ms, draw < 8ms at 60FPS.

**Acceptance:** 4-player co-op, wave 250, CHAKRAVYUHA difficulty: stable 60 FPS on a mid-range laptop; frame-time graph flat; no allocations per frame (verify with a debug counter).

---

## 11. 💾 Save / Progression

1. **Schema versioning** — `PRAGMA user_version`; migration functions per version; never crash on old saves.
2. **Save triggers:** purchase, run end, settings change, act clear, achievement. Never rely on quit-time only.
3. **Save shape:** wallet, XP/level, owned ships + upgrade levels, campaign progress (highest wave per act), achievements, stats (lifetime kills, favorite ship), settings.
4. **Cloud sync (logged-in users):** on login, compare `server_updated_at` vs local. Rule: **server wins for leaderboard/achievements; wallet merges by taking max(local, server)** (never delete a player's earned coins). Queue offline earnings and submit on next login.
5. **Backup:** on migration, copy `vimana_save.db` → `vimana_save_backup_v<N>.db`.

**Acceptance:** Kill process at random moments during gameplay — relaunch loses nothing earned. Downgrade the binary with an older schema → migration or clean fallback, no crash.

---

## 12. 🔄 Loading / Victory / Defeat / Pause Screens

- **Game Over:** slow-mo death replay (1s), "KILLED BY {cause}" (exists), animated Prana counter counting up with coin ticks, XP bar filling, buttons: RETRY / ARMORY / MENU. New: run stats grid (accuracy, damage dealt, cubes collected, best combo).
- **Victory:** act-clear already routes to WAVE_CLEAR; add campaign-complete cinematic: fleet flyby + credits + total stats + "New Game+ unlocked (ASURA PACT path)".
- **Multiplayer result:** squad scoreboard (per-player kills/damage/revives), team bonus breakdown, shared Prana payout, REMATCH button (reuses lobby).
- **Pause:** see §8. Add "controls reference" card inside pause.
- **Boot:** keep PV → loading → title; add tip rotation and version string.

---

## 13. 🧹 Code / Architecture Issues

1. **`main.cpp` FSM** — the `switch_to_view` lambda is ~150 lines and growing. Move to a `ViewRouter` class with a registry: `router.register(ViewType::MENU, &menu_view)` and a data table for the special-case wiring (loadout targets, game-view start paths). main.cpp should be <100 lines.
2. **Header-only everything** — `constants.hpp` includes raylib and defines 60 ships; every TU compiles it. Split: declarations in headers, `SHIP_FLEET`/`CAMPAIGN_REALMS` into one `.cpp`. Compile times will drop dramatically.
3. **Data vs code** — wave tables, boss kits, dialogue should be loadable data files (see §7 format), not C++ recompiles for tuning.
4. **Tests** — you have pytest only for Python. Add minimal C++ tests for: `compute_run_reward` (all rule combos), `sanitize_input_packet`, `validate_snapshot`, DB migration, squad assignment. Even a tiny assert-based runner is fine (`tests/test_economy.cpp` run in build.bat).
5. **Naming/ownership** — `players_mut()` public mutable access invites desync bugs; make mutation host-only with a debug assert.

---

## 13.5 Reconciliation — live-code audit vs. this spec (READ FIRST)

A second-pass audit of the *actual current code* supersedes parts of §0–13. Corrections:

**DONE already (remove from scope):**
- ~~Squad lives / Hardcore co-op rules~~ — implemented (3 individual lives, downed/revive, 6-pool Squad Lives, Hardcore). Only needs *live* 2–4 player verification, not construction.
- ~~Spatial-hash collision~~ — already solved. ~~Particle pooling~~ — already solved. Do not redo.
- ~~Boss telegraphs/phases~~ — 8 bosses DO have real multi-phase patterns with telegraphs. The gap is *depth* (phase-3 ultimates, encounter balance), not existence.
- ~~Corrupted-save handling~~ — solid and tested.
- Pause as an overlay inside `game_view.hpp` — this is the CORRECT pattern. A standalone pause view is unnecessary; skip that ticket.

**MORE BROKEN than this spec knew:**
- **Multiplayer combat is not actually networked.** `send_input()`/`broadcast_snapshot()` have *no gameplay caller* — nothing enforces host-owned damage. Your "4 friends play online" ask currently cannot work end-to-end. This jumps to P0.
- **42 of 62 ships have no real passive** (8 added this session; ~20 total have them, unbalanced as a set).
- **Zero gamepad support** — keyboard/mouse only.
- **No CMake / cross-platform build** — Windows batch + WinSock2 only.

**Adjusted build order (supersedes §14):**
| Phase | Tickets |
|---|---|
| **P0** | Wire netcode into gameplay (host-owned damage, snapshot→renderer path); per-peer ship selection online; end-to-end 2-client test; gamepad support (Raylib `IsGamepadAvailable`) |
| **P1** | Data-driven ship ability/passive system (kills the `if (id=="x")` sprawl); fill remaining ~42 passives; squad/formation AI; boss phase-3 ultimates + variants (fix 8-boss rotation repetition); ArmoryView economy close; pilot-level perks (make XP spendable) |
| **P2** | Upgrade 20 transmissions → choice-dialogue scenes; allegiance path (Deva/Asura); co-op-exclusive enemy compositions; UI widget library pass; game-over/victory visual pass |
| **P3** | Texture atlas; true fixed-timestep accumulator; CMake build; dynamic music layers; live playtest pass on target hardware (your docs rightly say: don't optimize blind); live audio mix pass |

**Meta-issue the audit exposes:** nearly everything is "verified by automated state tests, never live." Before P3, schedule one real playtest session (even solo + 2 loopback clients) and log a feel-notes doc. Code inspection cannot validate "fun."

---

## 14. Original Build Order (superseded by §13.5 — kept for reference)

| Phase | Tickets | Why first |
|---|---|---|
| **0 — Infra** | Fix `c_cpp_properties.json` (done ✔); split data into .cpp; ViewRouter refactor; DB schema v2 + migrations | Everything below touches these |
| **1 — Economy loop** | Reward formula + idempotency; DBSystem wallet APIs; ArmoryView + FSM wiring; per-ship upgrades | Closes the core loop; highest retention value |
| **2 — Co-op rules** | CoopRule in snapshot; shared lives HUD; HARDCORE; autopilot takeover; real ping; player_count fix | Your #1 multiplayer ask |
| **3 — Combat depth** | Squad AI; 2 new enemies; elite affixes; boss ability framework + Ravana kit first; ship ACTIVE abilities | The "fun" |
| **4 — Netcode hardening** | Interpolation; 20Hz snapshots + delta; reconnect; Flask room registry | Online play |
| **5 — Story** | DialogueView; parser; allegiance choice; Act 1 both paths | Campaign identity |
| **6 — UI system** | ui/ widget library; refactor all 18 views; loading screen; game-over animation | Perceived quality |
| **7 — Performance** | Spatial hash; particle pool; atlas; fixed timestep | Scale to wave 300 + 4P |
| **8 — Polish/live-ops** | Dynamic music; director AI; daily quests; stats screen; rebindable keys; localization (EN + HI flavor text) | Long-tail retention |

**Definition of Done (whole project):** A new player can: finish tutorial run → earn coins → buy a ship with a unique ability → feel combat escalation via squads → fight a multi-ability boss with fair telegraphs → reach an act boss with story dialogue → and 4 friends can squad up online, pick 4 different ships, and feel the run end together when the squad falls. All at 60 FPS.
