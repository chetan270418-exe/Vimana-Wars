# Vimana Wars — C++ UI/UX Screen Specification

The attached images are visual references: (1) cinematic command-menu framing, (2) an information-rich ship hangar, (3) a colorful space-combat equipment HUD, and (4) a readable wave/lives/bonus-sector HUD. Use their hierarchy and atmosphere; retain Vimana Wars' own assets, branding, and Vedic-punk palette.

## Shared visual rules

- Base: deep obsidian/space; panels: glass/slate; primary action: gold; active/info: cyan; safe: green; danger: red.
- Use the existing chamfered/yantra panels and design tokens. Keep decorative geometry behind content and low contrast.
- Every actionable control needs a visible hover/focus state, selected/locked state, and concise feedback. Keyboard paths remain available.
- At 900×600 logical resolution, preserve readable text and never cover the player, boss health, or telegraph with decoration.
- Present progression in familiar units: `ACT n/10 · WAVE n/30`, wallet balance, ship readiness, and explicit unlock conditions.

## Screen inventory and page contracts

| Page (`ViewType`) | Purpose and required hierarchy | Primary action / state |
| --- | --- | --- |
| Boot (`BOOT`) | Vimana Wars identity, short cinematic/splash, skip affordance. | Enter title/menu; never strand the player on a video. |
| Title (`TITLE`) | Establish the game world and move into pilot setup or menu. | Continue; fresh-profile route is explicit. |
| Pilot Setup (`PILOT_SETUP`) | Callsign/Game ID setup with validation and save confirmation. | Confirm pilot; explain local guest vs signed-in state. |
| Main Menu (`MENU`) | Left navigation, large atmospheric field, right command telemetry, pilot badge, last-used ship, campaign progress, wallet. Reference image 1. | Campaign, Multiplayer, Hangar, Profile, Duel, Settings, Quit. Continue appears only when valid. |
| Campaign Map (`CAMPAIGN_MAP`) | Ten connected acts/realms, completed/current/locked states, act and wave progress. | Select an unlocked start/continue point; locked nodes explain their prerequisite. |
| Hangar / Armory (`SHIP_SELECT`) | Hero ship, name/role, stat bars, mastery, wallet, unlock gate or price, upgrade, compact owned-supply counts. Reference image 2. | Browse, buy eligible ship, upgrade, buy supplies, equip/deploy. Locked ships cannot launch. |
| Mission Loadout (`LOADOUT`) | Selected ship and destination on left; capped tactical supplies and current stock on right. | Prepare and deploy; purchases use the same economy/caps as the Hangar. |
| Difficulty (`DIFFICULTY_SELECT`) | Four difficulty tiers with concise scaling description and selected starting wave. | Confirm difficulty; do not reset the chosen campaign wave. |
| Mission Brief (planned; no separate `ViewType` yet) | Realm story, objective, enemy/boss forecast, reward hint, controls reminder. | Deploy or return. Add only when the brief has unique content. |
| Loading / Drop-in (planned; no separate `ViewType` yet) | Realm name, progress, one rotating lore/tip line, selected ship, short deployment animation. | Auto-continue when assets/state are ready; skip only the presentation, never required initialization. |
| Combat HUD (`GAMEPLAY`) | Top wave/score/combo/realm; boss bar and telegraph; hull/dash/weapon/consumables; squad and threat radar. References images 3–4. | Combat input stays unobstructed; objective and remaining threats should be clear. |
| Pause / Abort (`GAMEPLAY` overlay) | Resume first, controls reminder, restart/abort confirmation. | Resume or confirm; abort warns about forfeiting current wave progress. |
| Boon Draft (`BOON_SELECT`) | Distinct choice cards with effect, rarity/role, synergy hint when known. | Choose one; gameplay resumes exactly once. |
| Wave Tally (`WAVE_CLEAR`) | Rank, kills, damage, combo, accuracy, wave Prana, boss salvage/unlock. | Continue to next wave/act or return to campaign. |
| Victory (`VICTORY`) | Boss/act completion, combat breakdown, run payout, unlock reveal, next-act status. | Continue campaign, Hangar, or menu. |
| Defeat (`GAME_OVER`) | Cause of death, score, wave, kills, damage, duration, rank, Prana payout. | Retry/continue, Profile, or menu. Reward must not duplicate on redraw/re-entry. |
| Multiplayer Browser (`MULTIPLAYER_LOBBY`, browser state) | Real lobby data only; clearly distinguish online room directory from playable LAN transport. | Refresh, host/join LAN, quick local squad, or Duel. |
| Squad Room (`MULTIPLAYER_LOBBY`, room state) | Pilot slots, vessel/role, ready state, selected co-op rule and its consequences. | Add AI, ready, deploy, leave. Rule choice persists. |
| Multiplayer Result (`MULTIPLAYER_RESULT`) | Team outcome and squad performance without claiming cloud persistence not provided. | Replay or return. |
| Duel (`DUEL`) | Local 1v1/training rules, visible player controls, round outcome. | Start/restart or return. |
| Leaderboard (`LEADERBOARD`) | Local/cloud source indicator, difficulty filter, rank, pilot, score, ship, wave. | Change filter/source; failures have a useful empty/error state. |
| Profile (`PROFILE`) | Game ID, progression, high score, match history, cloud/local state. | Sign in/out and return; never imply guest data was uploaded if it was not. |
| Achievements (`ACHIEVEMENTS`) | Browsable locked/unlocked awards, progress, reward, category. | Filter category and inspect details. |
| Codex (`CODEX`) | Ships, enemies, bosses, Astras, realms, lore; locked entries show reveal conditions. | Browse without interrupting a run. |
| Settings (`SETTINGS`) | Audio channels, controls, display, accessibility; saved changes visibly confirm. | Adjust; defaults/reset are reversible. |
| Auth (`AUTH`) | Sign-in/register form, validation, loading/error/success, account Game ID. | Submit; password visibility and back path; network failure preserves typed input. |
| Quit (`QUIT`) | Not a separate page: safe teardown owned by `src/main.cpp`. | Persist required state, stop audio/network, close cleanly. |

## Interaction details for the first slice

- Main-menu `2` opens the multiplayer lobby; the click target and keyboard shortcut must agree.
- Hangar remembers the last equipped unlocked ship and shows that ship in the menu telemetry panel.
- Purchases are atomic: validate ship/item, validate funds/caps, charge once, update stock/unlock, save, then play success feedback.
- Run-end Prana is calculated once at the game-result transition, saved immediately, and displayed on the result page. Wave-clear Prana remains a separate reward.
- Co-op rule control cycles Standard Revives → Shared Squad Lives → Hardcore; its explanation is visible before deployment and in the combat HUD.

