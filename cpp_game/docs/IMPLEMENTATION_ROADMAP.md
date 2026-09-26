# Vimana Wars C++ — Implementation Roadmap

This is the feature roadmap from the supplied guide, adapted to the checked-in native C++ project. Status is based on source inspection and the existing C++ audit, not a claim that every path has been manually playtested.

Status: `[x]` source implementation present (see validation); `[~]` partial or needs live QA; `[ ]` not implemented / not verified. The numbered list preserves the source guide's 70-item order.

## Phase 1 — Core polish

- [~] **01 Fix gameplay bugs:** use the 35-action [C++ audit task file](../IMPLEMENTATION_TASKS.md); several runtime/device cases still need live QA.
- [x] **02 Mouse aiming:** combat has mouse-based aim and fire input.
- [~] **03 Shooting feel:** firing has muzzle flash/SFX, directional recoil, an aim tracer, and a short hit-confirm marker (gold on critical hits); weapon balance still needs hands-on playtesting.
- [x] **04 Enemy targeting:** AI threat/targeting systems are present.
- [x] **05 Wave progression:** act/wave campaign data and multi-enemy formations exist.
- [~] **06 Damage feedback:** player damage and landed shots have distinct popups/ripples, enemy hit flashes, critical color, and optional shake; live readability/accessibility pass remains.
- [x] **07 Player death/revive:** downed state, revives, and individual lives exist; new rule variants added in this slice.
- [~] **08 Boss mechanics:** all eight bosses retain unique attack/phase patterns; both entity and HUD telegraphs respect reduced-flash mode, and audit tests phase thresholds/attack tells. Full encounter playtesting remains.
- [x] **09 Pause system:** pause and abort-confirmation overlay exist.
- [~] **10 Performance profiling:** F7 graphs 120 frame times and reports current/average/P95/peak plus rolling update and draw/present timings; target-hardware baseline and release-build profiling remain.

## Phase 2 — Progression

- [x] **11 Coins/Prana:** currency exists; run-completion payout is now added.
- [x] **12 Pilot XP:** run XP payout, local persistence, derived levels, menu progress bar, and post-run reward line are implemented; level perks/cloud sync are not included.
- [x] **13 Ship unlocks:** wave/boss gates and Prana purchases exist; invalid catalog IDs are now rejected.
- [x] **14 Ship upgrades:** persistent ship upgrade levels exist.
- [x] **15 Save/load:** versioned local JSON save exists; schema 6 adds equipped vessel, co-op rule, and supply stock.
- [x] **16 Score:** combat scoring and local leaderboard persistence exist.
- [x] **17 Combo:** player/team combo systems exist.
- [x] **18 Rank:** wave/run result rank is present.
- [x] **19 Rewards:** wave rewards remain; one-time score/wave/victory run payout is now shown and saved.
- [~] **20 Achievements:** trophy archive includes reachable individual awards for all eight bosses plus an all-guardians award; removed the unearnable daily-event trophy. Remaining trigger coverage and cloud sync need live verification.

## Phase 3 — UI

- [x] **21 Main menu:** cinematic flagship-art backdrop, animated text navigation, keyboard/mouse focus, pilot XP, equipped-ship preview, and all existing destinations are reachable.
- [x] **22 Hangar:** `ShipSelectView` already serves as Hangar/Armory; reuse it.
- [x] **23 Ship selection:** browsing and locked-launch guard exist; last equipped ship is restored.
- [x] **24 Loadout:** tactical supply preparation exists and now shares purchase caps/persistence.
- [x] **25 Campaign map:** act selection and continue-wave behavior exist.
- [~] **26 Mission briefing:** loadout now leads to a briefing with act/wave, story transmission, realm hazard, guardian, difficulty, and ship signature before launch; visual/readability QA remains.
- [~] **27 Loading screen:** full-screen splash incrementally preloads fleet, boss, realm, and backdrop textures with real asset progress and fallback art; engine/font initialization still precedes the splash, and continuation waits for preload completion.
- [x] **28 HUD:** mission act/wave, score, animated combo, live contact count, realm, ship, mode, and difficulty are visible in the gameplay header.
- [x] **29 Pause screen:** present.
- [x] **30 Victory:** result view exists.
- [x] **31 Defeat:** result view includes death cause and now the Prana payout.
- [x] **32 Micro animations/transitions:** view changes use eased fade timing and a rotating mandala transition cue; existing combo pulse remains.

## Phase 4 — Content

- [x] **33 More ships:** added two late-act, progression-locked ships using the existing Phase 9 sprites; the fleet catalog and achievement target now include 62 ships.
- [~] **34 Unique ship abilities:** Amogha, Nandi, Soma, Dhanvantari, Surya, Varaha, and Kubera hulls now have distinct, test-covered combat passives; the rest of the 62-ship fleet still needs bespoke ability design and balance.
- [x] **35 Enemy types:** multiple enemy archetypes are present.
- [x] **36 Elite enemies:** elite spawning and behavior exist.
- [x] **37 Mini-bosses:** three named mini-bosses recur at act waves 8/18/28, join mixed enemy formations, have boss sprites/nameplates, heavier health, distinct volleys, guaranteed supply drops, and Codex counters.
- [x] **38 Multi-phase bosses:** boss phase machinery exists; continue per-boss content QA.
- [x] **39 More waves:** act-based progression and authored formations exist.
- [x] **40 Realm mechanics:** all seven modifier families now affect combat/HUD (movement, projectile drift, sensor loss/shorter sniper warning, fire damage, dash distance, extra flak, and hostile-bullet distortion); smoke checks cover each.
- [x] **41 Story events:** twenty original authored transmissions span all ten acts and display at their campaign waves; the Codex archives each event with its speaker and act.
- [x] **42 Codex:** all ten realms, 62 ships, six enemy profiles, eight bosses, three mini-bosses, twenty story events, and boon synergies are browsable with mouse-wheel/keyboard scrolling and tab navigation.

## Phase 5 — Multiplayer

- [~] **43 Four-player lobby:** lobby/AI slots exist; networking remains local/LAN-oriented.
- [~] **44 Multiplayer ship selection:** local launch uses Hangar selection; per-peer ship selection is incomplete.
- [ ] **45 Player synchronization:** end-to-end authoritative combat sync is not complete.
- [ ] **46 Real-time online combat:** no production internet combat relay/server.
- [x] **47 Squad lives:** optional six-life shared pool is now selectable in the lobby.
- [x] **48 Revive:** standard down/revive flow exists; Hardcore bypasses it by design.
- [~] **49 Team combos:** team combo/Astra systems exist; broader coordinated skill design is future work.
- [~] **50 Multiplayer enemy scaling:** some scaling exists; validate density/patterns as well as boss HP.
- [~] **51 Multiplayer boss mechanics:** current boss scaling exists; player-targeted co-op patterns need work.
- [~] **52 Reconnect:** transport has reconnect-related code; reliable match recovery needs integration tests.
- [~] **53 Disconnect handling:** AI takeover/protocol pieces exist; end-to-end behavior needs live tests.
- [~] **54 Match result:** local result page exists; remote result integrity/cloud sync is separate.
- [~] **55 Multiplayer rewards:** local run payout is implemented; authoritative anti-cheat/cloud grant must wait for server validation.

## Phase 6 — Final polish

- [~] **56 Sound effects:** gameplay/UI SFX are wired, missing/decode-failed resources now emit one actionable diagnostic, and live device/mix QA remains.
- [~] **57 Music:** combat loop is paired with looping act-specific ambience; music/ambience have separate stream volumes and share the music setting; live mix QA remains.
- [~] **58 VFX:** combat particles, dash ghosts, boss phase rings, Astra effects, and damage feedback are wired; visual balance QA remains.
- [x] **59 Screen shake:** implemented with an accessibility toggle.
- [x] **60 Particles:** particle system is used for combat feedback.
- [~] **61 UI transitions:** all view changes use the central fade/mandala transition except in-combat boon selection; subtle close/open audio cues added.
- [ ] **62 Controller support:** gamepad UX is not complete.
- [~] **63 Settings:** master/SFX/music/UI/boss levels and accessibility toggles persist, including reduced flashes; automated save audit exists, live control/resolution QA remains.
- [~] **64 Accessibility:** colorblind mode changes projectile shape/palette and threat-radar contrast; shake, scanline, and reduced-flash settings persist. Scanlines now respect the toggle across views; reduced flashes suppresses invincibility blinking and hit flashes; broader presets/readability remain.
- [ ] **65 FPS/performance optimization:** profile before setting optimization claims.
- [x] **66 Save corruption protection:** malformed save is backed up; audit verifies this behavior.
- [~] **67 Crash/error handling:** missing assets report once, failed asset lookups are cached, save-path filesystem exceptions are caught, and uncaught runtime exceptions are logged at the app boundary; expand failure-injection tests.
- [~] **68 Final QA:** automated audit exists, hands-on matrix remains.
- [~] **69 Build/package:** native build scripts exist; signed/release packaging not certified.
- [ ] **70 Release version:** no completed release checklist/versioning workflow.

## Current implementation slice

- [x] Run payout formula, once-per-run guard, save-on-award, result-page reward line.
- [x] Pilot XP payout and level tracking, version-8 save migration default, menu progress meter, and post-run XP display.
- [x] Primary-fire audio, player damage/shield hit feedback, actual boss damage accounting, and overlapping boss telegraph priority.
- [x] Currency safety for negative spending, integer overflow, invalid ship IDs, and supply caps.
- [x] Ten-act Codex/story coverage, recurring three-pattern mini-boss encounters, and gameplay hooks for every configured realm modifier.
- [~] Bespoke ship identity: seven passive designs are covered by tests across eight hulls; the remaining fleet still needs individual ability design and balance.
- [x] Incremental boot preload, realm ambience streams, reduced-flash accessibility, and actionable missing-resource/fatal-error logging.
- [x] Persistent equipped ship and tactical stock; Hangar purchases survive restart and stock is consumed on deploy.
- [x] Multiplayer entry in the main menu and persistent Standard / Shared Squad Lives / Hardcore selector.
- [x] Co-op rule behavior and HUD label; schema bumped to version 6 with backward-compatible defaults.
- [x] Build and audit smoke tests pass, including payout/currency boundaries and save round-trip for the new fields.
- [ ] Live visual pass for menu, Hangar, loadout, shared-lives respawn, and Hardcore elimination.

## Next execution order

1. Build and run the C++ audit; fix regressions in this slice.
2. Perform one solo run and one local co-op run for reward, inventory, rule, and restart behavior.
3. Finish the mission brief/deployment page and expand the post-run breakdown using metrics already recorded.
4. Complete per-ship ability definitions and boss/miniboss encounter tables.
5. Design authoritative multiplayer protocol/server separately; do not advertise lobby-directory support as full online combat.
