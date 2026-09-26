# Vimana Wars — C++ Game Design

## Product goal

Vimana Wars is a readable, replayable sci-fi arcade shooter with mythic naming and a distinct celestial-cockpit identity. Each run should create a clear feedback loop: choose a vessel, prepare, survive escalating formations, defeat bosses, earn Prana, and return to the Hangar with meaningful progress.

## Design pillars

1. **Readable combat:** threats, telegraphs, health, wave goals, and player state must be understandable at a glance.
2. **Distinct vessels:** ship roles should change movement, survivability, or weapon patterns—not only ship art and stat totals.
3. **Earned progression:** runs grant transparent rewards; purchases and unlocks persist; locked content explains its requirement.
4. **Layered feedback:** meaningful actions respond through animation/VFX, audio, and concise UI feedback where available.
5. **Co-op with consequences:** revive choices and team survival rules should support teamwork. LAN lobby features must not be presented as internet matchmaking until combat replication exists.
6. **One coherent visual language:** obsidian/glass surfaces, luminous gold/cyan, restrained danger red, chamfered panels, and animated celestial geometry.

## Core sortie loop

```text
Main Menu → Campaign / Multiplayer → Hangar → Loadout → Difficulty / Mission
          → Combat waves → Wave tally / boon → Boss and act clear
          → Victory or defeat → Prana payout → Hangar / next run
```

The existing C++ views already cover most of this loop. The `ShipSelectView` is the Hangar/Armory; `LoadoutView` is the tactical preparation page. Avoid creating duplicate Hangar or loadout implementations.

## Progression and economy

- **Prana** remains the primary currency. Wave-clear earnings remain intact.
- Run completion adds one separately reported payout, granted once per run and saved immediately:

  ```text
  40 base + 10 per full 1,000 score + 8 per wave reached + 500 for victory
  ```

- Ship unlocks continue to honor the existing wave/boss gates; Prana purchase is allowed only for catalogued, non-boss-salvage ships with a configured price.
- Ship upgrades and purchased tactical supplies use the existing currency system and save file. Tactical stock is consumed on deployment, not when the player merely opens the Hangar.
- XP and Astra Shards are not added in this slice. They need clear earning/spending rules, UI, and save semantics before becoming another currency.
- Save schema version 6 adds the equipped ship, co-op rule, and Hangar consumable stock while keeping missing fields backward-compatible with older saves.

## Vessels and combat roles

The fleet should express Fighter, Assault, Control, Damage, Speed, Energy, Shield, and Execution playstyles. Existing ship archetype stats and projectile patterns are the source of truth. A future signature-ability pass should specify each ship's ability, cooldown, VFX, audio cue, upgrade interaction, and co-op interactions before adding ability code.

Each new ship must have a verified archetype, unlock path, balance role, texture or intentional procedural fallback, and Hangar display. Do not create a ship by duplicating another ship's name/art and changing only its HP.

## Encounter and boss design

- A wave is a formation/encounter, not a single enemy spawned in isolation.
- Escalation should come from composition, elite frequency, attack patterns, hazards, and objective pressure—not only larger HP numbers.
- Bosses should telegraph attacks, expose phase changes, and create safe reaction windows. Later-phase adds and arena patterns should remain readable for solo play and co-op.
- The existing act/wave and realm systems are content foundations. Expand them through authored wave tables and boss behaviors rather than a second progression manager.

## Co-op rule modes

- **Standard Revives:** existing downed/revive loop and three lives per pilot.
- **Shared Squad Lives:** six shared respawns; a pilot spends one only after bleed-out. A pilot is eliminated when the team pool is empty at their bleed-out.
- **Hardcore:** hull reaching zero eliminates the pilot immediately; no downed state, self-revive, or teammate revive.

These are local game rules in this implementation. They do not make the current LAN prototype an online authoritative multiplayer service. Rule negotiation/synchronization across network peers remains a multiplayer roadmap item.

## Technical ownership map

| Concern | Existing C++ owner |
| --- | --- |
| Screen state and transitions | `core/types.hpp`, `views/*_view.hpp`, `src/main.cpp` |
| Ship catalog and player combat | `entities/ship_archetypes.hpp`, `entities/player.hpp`, `views/game_view.hpp` |
| Waves, bosses, realm progression | `systems/wave_manager.hpp`, `entities/boss.hpp`, `core/constants.hpp` |
| Currency and unlock rules | `systems/currency_system.hpp` |
| Save and SQLite scores | `systems/db_system.hpp` |
| Multiplayer transport/lobby prototype | `systems/network_manager.hpp`, `views/multiplayer_view.hpp` |
| Shared UI styling | `ui/vedic_theme.hpp`, `ui/design_tokens.hpp`, `ui/button.hpp`, `ui/hud.hpp` |

