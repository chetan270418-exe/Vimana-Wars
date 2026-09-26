# Vimana Wars C++ — Implementation Roadmap

This is the feature roadmap from the supplied guide, adapted to the checked-in native C++ project. Status is based on source inspection and the existing C++ audit, not a claim that every path has been manually playtested.

Status: `[x]` source implementation present (see validation); `[~]` partial or needs live QA; `[ ]` not implemented / not verified. The numbered list preserves the source guide's 70-item order.

## Phase 1 — Core polish

- [~] **01 Fix gameplay bugs:** use the 35-action [C++ audit task file](../IMPLEMENTATION_TASKS.md); several runtime/device cases still need live QA.
- [x] **02 Mouse aiming:** combat has mouse-based aim and fire input.
- [~] **03 Shooting feel:** primary weapons now play the existing `shoot.wav` alongside the muzzle-flash VFX; verify mix/volume during live play.
- [x] **04 Enemy targeting:** AI threat/targeting systems are present.
- [x] **05 Wave progression:** act/wave campaign data and multi-enemy formations exist.
- [~] **06 Damage feedback:** HP-loss/shield popups, impact bursts, and single hit SFX are wired for projectile/contact damage; live readability pass remains.
- [x] **07 Player death/revive:** downed state, revives, and individual lives exist; new rule variants added in this slice.
- [~] **08 Boss mechanics:** overlapping special telegraphs keep priority; boss damage/shield hit-confirm now reflects actual HP applied; boss pattern QA remains.
- [x] **09 Pause system:** pause and abort-confirmation overlay exist.
- [ ] **10 Performance profiling:** no documented profiling baseline or target hardware pass yet.

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
- [~] **20 Achievements:** trophy archive is reachable from the menu; implemented boon, ship, co-op, hard-act, leaderboard, and sortie triggers are wired. Daily-win remains unavailable until a daily challenge mode exists.

## Phase 3 — UI

- [x] **21 Main menu:** cinematic flagship-art backdrop, animated text navigation, keyboard/mouse focus, pilot XP, equipped-ship preview, and all existing destinations are reachable.
- [x] **22 Hangar:** `ShipSelectView` already serves as Hangar/Armory; reuse it.
- [x] **23 Ship selection:** browsing and locked-launch guard exist; last equipped ship is restored.
- [x] **24 Loadout:** tactical supply preparation exists and now shares purchase caps/persistence.
- [x] **25 Campaign map:** act selection and continue-wave behavior exist.
- [ ] **26 Mission briefing:** no separate mission-brief page yet.
- [~] **27 Loading screen:** full-screen hero-art boot splash now has staged progress, percentage, skip controls, and a fallback; core assets still initialize before the view, so this is not asynchronous loading.
- [x] **28 HUD:** mission act/wave, score, animated combo, live contact count, realm, ship, mode, and difficulty are visible in the gameplay header.
- [x] **29 Pause screen:** present.
- [x] **30 Victory:** result view exists.
- [x] **31 Defeat:** result view includes death cause and now the Prana payout.
- [x] **32 Micro animations/transitions:** view changes use eased fade timing and a rotating mandala transition cue; existing combo pulse remains.

## Phase 4 — Content

- [x] **33 More ships:** added two late-act, progression-locked ships using the existing Phase 9 sprites; the fleet catalog and achievement target now include 62 ships.
- [~] **34 Unique ship abilities:** the 62-ship catalog exposes hull stats, roles, and weapon profiles; Amogha Lancer and Nandi Aegis have new, test-covered combat passives. Most ships still share their archetype's weapon/passive behavior rather than each having a bespoke active Astra.
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

- [~] **56 Sound effects:** assets exist; UI now uses its own volume channel, transition cues are wired, and live device/mix QA remains.
- [~] **57 Music:** category volume no longer double-applies master gain; same-track wave starts preserve playback; live mix QA remains.
- [~] **58 VFX:** combat particles, dash ghosts, boss phase rings, Astra effects, and damage feedback are wired; visual balance QA remains.
- [x] **59 Screen shake:** implemented with an accessibility toggle.
- [x] **60 Particles:** particle system is used for combat feedback.
- [~] **61 UI transitions:** all view changes use the central fade/mandala transition except in-combat boon selection; subtle close/open audio cues added.
- [ ] **62 Controller support:** gamepad UX is not complete.
- [~] **63 Settings:** master/SFX/music/UI/boss levels and accessibility toggles persist; automated save audit exists, live control/resolution QA remains.
- [~] **64 Accessibility:** colorblind mode now changes projectile shape/palette and threat-radar contrast; shake and scanline toggles persist; broader presets/readability remain.
- [ ] **65 FPS/performance optimization:** profile before setting optimization claims.
- [x] **66 Save corruption protection:** malformed save is backed up; audit verifies this behavior.
- [~] **67 Crash/error handling:** local guards exist; expand failure-injection tests.
- [~] **68 Final QA:** automated audit exists, hands-on matrix remains.
- [~] **69 Build/package:** native build scripts exist; signed/release packaging not certified.
- [ ] **70 Release version:** no completed release checklist/versioning workflow.

## Current implementation slice

- [x] Run payout formula, once-per-run guard, save-on-award, result-page reward line.
- [x] Pilot XP payout and level tracking, version-7 save migration default, menu progress meter, and post-run XP display.
- [x] Primary-fire audio, player damage/shield hit feedback, actual boss damage accounting, and overlapping boss telegraph priority.
- [x] Currency safety for negative spending, integer overflow, invalid ship IDs, and supply caps.
- [x] Ten-act Codex/story coverage, recurring three-pattern mini-boss encounters, and gameplay hooks for every configured realm modifier.
- [~] Bespoke ship identity: two new ships have unique tested passives; the remaining fleet still needs individual active-ability design and balance.
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
