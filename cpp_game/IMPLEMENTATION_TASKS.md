# Vimana Wars C++ Audit Task File

Scope: C++ game and its C++-specific README only (`cpp_game/`). The attached audit's roadmap actually numbers **35 actions**, not 34. Duplicate findings are linked to their main action rather than implemented twice.

Status key: `[x]` implemented/present and verified by source/build; `[~]` partly checked; `[ ]` still needs work or hands-on validation.

## Roadmap actions

### Critical/gameplay

- [x] **01 — Locked ship launch guard.** Enter cannot bypass the unlock check.
- [x] **02 — Basic boss telegraph reset.** Warning clears when the attack fires.
- [x] **03 — Basic boss telegraph target.** Telegraph beam/marker targets the current player.
- [x] **04 — Star field.** Populate and render game-view stars.
- [x] **05 — Downed movement.** Controller velocity is the sole movement path.
- [x] **06 — Boon pause state.** Selecting a boon resumes gameplay.
- [x] **07 — Agneyastra/gun ordering.** Buff spread does not replace a ship's native gun pattern.
- [x] **08 — Mahishasura/Indrajit attacks.** Both have distinct basic attack patterns.
- [x] **09 — Boss speed/arena cap.** Phase/act speed is bounded and boss X is clamped to the arena.
- [x] **10 — Team combo baseline.** Combo begins at zero.
- [x] **11 — P2 abilities.** Separate keypad 1/2/3 bindings prevent triggering P1's Q/C/V abilities.
- [x] **12 — Screen transitions.** Transition manager is used; combat boon selection deliberately switches immediately.
- [x] **13 — Fullscreen placement.** Toggle is on Accessibility and shows current state.
- [x] **14 — Pilot profile shortcut.** P opens the profile from the main menu.
- [x] **15 — Shared shop prices.** UI labels use `COST_*` constants.
- [x] **16 — Death cause.** Damage source reaches Game Over and is stored in local score records and per-ship save data.
- [x] **17 — Continue wave.** The saved next/current wave is restored on the campaign map.
- [x] **18 — Victory result.** Victory suppresses defeat text and stores an empty death cause.
- [x] **19 — Act I waves 6–10.** Waves 6–9 use authored formations; wave 10 remains its boss-plus-escort encounter.
- [x] **20 — Boss attacks/telegraphs.** Eight bosses have distinct basic patterns; basic telegraphs point at the player.
- [x] **21 — Act/phase speed ceiling.** Boss speed caps are applied after scaling and phase changes.
- [~] **22 — Enemy scaling balance.** Enemy counts are capped at 180 and scaling formulas were reviewed; real difficulty balance still needs playtesting.

### VFX and networking

- [x] **23 — Muzzle flashes.** Emitted when a player fires.
- [x] **24 — Dash trails.** Dash ghosts are emitted during/after a dash.
- [x] **25 — Screen shake.** Impact shake is applied to the camera offset and respects the accessibility toggle.
- [x] **26 — Enemy explosion effects.** Kill/Astra paths emit explosion particles.
- [ ] **27 — Network damage authority.** The snapshot/controller types can carry HP, but there is no connected combat replication path to establish and enforce host-owned damage end-to-end.
- [ ] **28 — Lag compensation.** Add prediction/reconciliation and sequence/timestamp rules; current smoothing is not full reconciliation.
- [ ] **29 — Dedicated server.** Requires a separate authoritative server target and protocol design; current networking is host/LAN oriented.

### QA actions

- [~] **30 — Ship gameplay QA.** Automated smoke initializes and fires all 60 ship archetypes and validates their projectiles; real gameplay runs remain.
- [~] **31 — Boss QA.** Automated simulation checks all eight basic attack telegraphs, firing patterns, damage attribution, and phase speed caps; rendered/gameplay QA remains.
- [~] **32 — Difficulty QA.** Automated smoke spawns a full representative wave and verifies increasing wave/boss scaling across all four difficulties; play-balance judgment still needs hands-on runs.
- [x] **33 — Persistence QA.** Isolated-profile test round-trips JSON progression, all five audio volumes, accessibility flags, and tutorial state; malformed JSON is preserved in a verified corrupt-save backup. SQLite migration and score/death-cause round trip are also tested.
- [~] **34 — Local co-op QA.** Headless controller-path test drives P1/P2 movement, fire, dash, chakram, Soma, and Vajra together, and checks downed input restrictions; keyboard feel/input conflicts still need a live two-player session.
- [~] **35 — Crash/edge QA.** Automated edge checks cover NaN/infinite and clamped network values, downed controls, corrupted saves, full difficulty scaling, ship firing, and boss/wave simulations; prolonged live play and window/device failure cases remain.

## Additional findings from the audit

- `TitleView` is in `boot_view.hpp`; a separate `title_view.hpp` is not required.
- The previously “dead” GameView network timer/zero-size quit buttons were removed rather than left as misleading unused UI.
- Settings now supports 1–3 and Left/Right tab switching; fullscreen is resettable and saved across launches.
- AI teammate revives consume one Soma from the AI rescuer. P2 uses numpad abilities to avoid sharing P1's keys.
- Local SQLite score rows already included difficulty and run metrics. Death cause was added with an additive schema migration; old rows retain an empty cause.
- Audio scan: every literal filename used by C++ `play_sfx()`/`play_music()` calls was found under the shared `assets/sounds/` directory. This verifies file presence, not playback quality/device behavior.
- The repeated boss rotation, no gamepad support, and menu Quit prominence are content/design or feature gaps, not compiler errors; they remain candidates for later scoped work.
- Enemy role glyphs used to draw from `Enemy::init()` during wave updates; they now render only inside `Enemy::draw()`, keeping the update path free of rendering calls.
- Online multiplayer is not claimed complete. Host snapshots, damage authority, prediction, and server deployment need an end-to-end protocol and runtime tests.
- `send_input()` and `broadcast_snapshot()` have no gameplay call sites, and no caller feeds host input into `NetworkController`; the UDP lobby/snapshot code is therefore not playable online combat replication yet.
- Host-side input packets now require exact payload sizes, valid finite/clamped axes and aims, matching monotonic sequence numbers, and valid ping enums; clients accept snapshots only from the configured host and reject malformed, stale, or invalid state. This hardens transport inputs but does not itself synchronize combat.
- README wording explicitly says the UDP lobby prototype is not playable online combat replication.

## Verification run

- `cmd /c build.bat` — passed after the implementation changes, including enemy draw/update separation.
- `cmd /c test_audit.bat` — passed: SQLite migration and death-cause round trip, JSON save/settings/progression load and corrupt backup, Continue wave restore, network validation helpers, all 60 ship firing patterns, two-pilot controller/action flow, four-difficulty wave/boss scaling, eight bosses' basic telegraphs/attacks and phase caps, and actual spawns for waves 6–10.
- `git diff --check -- cpp_game` — no whitespace errors; Git only reports the repository's existing LF/CRLF normalization notices.
