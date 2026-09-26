# Vimana Wars C++ — Implementation Roadmap

This is the feature roadmap from the supplied guide, adapted to the checked-in native C++ project. Status is based on source inspection and the existing C++ audit, not a claim that every path has been manually playtested.

Status: `[x]` source implementation present (see validation); `[~]` partial or needs live QA; `[ ]` not implemented / not verified. The numbered list preserves the source guide's 70-item order.

## Phase 1 — Core polish

- [~] **01 Fix gameplay bugs:** use the 35-action [C++ audit task file](../IMPLEMENTATION_TASKS.md); several runtime/device cases still need live QA.
- [x] **02 Mouse aiming:** combat has mouse-based aim and fire input.
- [~] **03 Shooting feel:** firing/impact feedback exists; continue tuning hit-confirmation and audiovisual layering.
- [x] **04 Enemy targeting:** AI threat/targeting systems are present.
- [x] **05 Wave progression:** act/wave campaign data and multi-enemy formations exist.
- [~] **06 Damage feedback:** particles, hit flashes, and shake exist; broader attack feedback needs playtest.
- [x] **07 Player death/revive:** downed state, revives, and individual lives exist; new rule variants added in this slice.
- [~] **08 Boss mechanics:** distinct bosses/phases/telegraphs exist; content and rendered behavior need further QA.
- [x] **09 Pause system:** pause and abort-confirmation overlay exist.
- [ ] **10 Performance profiling:** no documented profiling baseline or target hardware pass yet.

## Phase 2 — Progression

- [x] **11 Coins/Prana:** currency exists; run-completion payout is now added.
- [ ] **12 Pilot XP:** no complete XP earning/level/reward loop yet.
- [x] **13 Ship unlocks:** wave/boss gates and Prana purchases exist; invalid catalog IDs are now rejected.
- [x] **14 Ship upgrades:** persistent ship upgrade levels exist.
- [x] **15 Save/load:** versioned local JSON save exists; schema 6 adds equipped vessel, co-op rule, and supply stock.
- [x] **16 Score:** combat scoring and local leaderboard persistence exist.
- [x] **17 Combo:** player/team combo systems exist.
- [x] **18 Rank:** wave/run result rank is present.
- [x] **19 Rewards:** wave rewards remain; one-time score/wave/victory run payout is now shown and saved.
- [~] **20 Achievements:** system/gallery exist; full unlock coverage and reward QA remain.

## Phase 3 — UI

- [~] **21 Main menu:** command-center layout exists; multiplayer is now reachable and the hero vessel follows the equipped ship.
- [x] **22 Hangar:** `ShipSelectView` already serves as Hangar/Armory; reuse it.
- [x] **23 Ship selection:** browsing and locked-launch guard exist; last equipped ship is restored.
- [x] **24 Loadout:** tactical supply preparation exists and now shares purchase caps/persistence.
- [x] **25 Campaign map:** act selection and continue-wave behavior exist.
- [ ] **26 Mission briefing:** no separate mission-brief page yet.
- [~] **27 Loading screen:** boot/title presentation exists, but there is no asset-aware deployment/loading page.
- [~] **28 HUD:** gameplay HUD exists; keep refining information hierarchy and mode clarity.
- [x] **29 Pause screen:** present.
- [x] **30 Victory:** result view exists.
- [x] **31 Defeat:** result view includes death cause and now the Prana payout.
- [~] **32 Micro animations/transitions:** buttons, particles, and transition system exist; consistency audit remains.

## Phase 4 — Content

- [~] **33 More ships:** large catalog exists; validate every sprite, silhouette, and gameplay role.
- [~] **34 Unique ship abilities:** ship stats/guns differ; signature Astra identity for every ship is not complete.
- [x] **35 Enemy types:** multiple enemy archetypes are present.
- [x] **36 Elite enemies:** elite spawning and behavior exist.
- [~] **37 Mini-bosses:** boss content exists; a clearly separate mini-boss encounter layer needs confirmation.
- [x] **38 Multi-phase bosses:** boss phase machinery exists; continue per-boss content QA.
- [x] **39 More waves:** act-based progression and authored formations exist.
- [~] **40 Realm mechanics:** realm modifiers/background systems exist; verify all realms in live play.
- [~] **41 Story events:** transmissions/lore are present but not a full mission narrative sequence.
- [~] **42 Codex:** Codex view exists; catalog completeness and unlock links need validation.

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

- [~] **56 Sound effects:** assets/calls exist; every event/device needs playback QA.
- [~] **57 Music:** tracks and switching exist; transitions/mix need hands-on QA.
- [~] **58 VFX:** particles and boss/combat effects exist; coverage and clarity pass remains.
- [x] **59 Screen shake:** implemented with an accessibility toggle.
- [x] **60 Particles:** particle system is used for combat feedback.
- [~] **61 UI transitions:** transition infrastructure exists; audit all routes for consistency.
- [ ] **62 Controller support:** gamepad UX is not complete.
- [~] **63 Settings:** audio/accessibility settings persist; test every control and resolution.
- [~] **64 Accessibility:** shake/scanline/color settings exist; broader presets/readability remain.
- [ ] **65 FPS/performance optimization:** profile before setting optimization claims.
- [x] **66 Save corruption protection:** malformed save is backed up; audit verifies this behavior.
- [~] **67 Crash/error handling:** local guards exist; expand failure-injection tests.
- [~] **68 Final QA:** automated audit exists, hands-on matrix remains.
- [~] **69 Build/package:** native build scripts exist; signed/release packaging not certified.
- [ ] **70 Release version:** no completed release checklist/versioning workflow.

## Current implementation slice

- [x] Run payout formula, once-per-run guard, save-on-award, result-page reward line.
- [x] Currency safety for negative spending, integer overflow, invalid ship IDs, and supply caps.
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
