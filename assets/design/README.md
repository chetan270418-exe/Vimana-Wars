# Vimana Wars Design Deliverables

This folder documents the visual overhaul and the generated PV deliverables for the Vimana Wars game.

## Implemented in-game UI

The redesign is implemented in:

- `game/ui/vedic_theme.py`
- `game/ui/hud.py`
- `game/ui/boss_bar.py`
- `game/ui/menu_button.py`
- `game/views/menu_view.py`
- `game/views/ship_select_view.py`
- `game/views/stats_view.py`
- `game/views/multiplayer_view.py`

The visual system uses obsidian glass panels, cyan telemetry, celestial-gold selection states, Astra-red danger states, sacred-geometry framing, scanlines, pulses, cockpit HUD elements, and reduced-flash-aware animation.

## Design references

Generated UI reference images are kept in the project workspace root so they remain easy to preview and share:

- `main-menu-ui.png`
- `mission-control-hud.png`
- `astra-arsenal.png`
- `boss-overlay-system.png`
- `pushpaka-reference.png`
- `boss-ravana-reference.png`

These references are design assets only. The game remains offline-safe and does not require them at runtime.

## PV deliverables

- `vimana_wars_pv_final.mp4` — completed 15-second 16:9 game PV with native game-PV sound.
- `vimana-wars-pv-storyboard.md` — approved narrative storyboard and master timeline.
- `vimana-wars-final-video-prompt.md` — final generation prompt and reference bindings.

## Direction guardrails

- Preserve Vimana Wars as a mythological celestial PvE shooter.
- Keep Pushpaka, Ravana, Asura enemies, and sacred-geometry space identity consistent.
- Do not introduce real-life characters, live-action people, or PvP framing.
- Keep UI text sparse, readable, and functional.

The current multiplayer screen is a functional authenticated lobby browser;
the PV and UI reference images remain presentation assets and are not required
for gameplay startup.
