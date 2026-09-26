# Vimana Wars C++ Design Pack

This folder is the shared design context for the native C++ game. It is scoped to `cpp_game/`; Python, web, backend, and deployment code are intentionally out of scope.

## Read in this order

1. [Game design](GAME_DESIGN.md) — player loop, systems, progression, and boundaries.
2. [UI/UX specification](UI_UX_SPEC.md) — screen-by-screen purpose, layout, and interactions, using the supplied images as visual references.
3. [Implementation roadmap](IMPLEMENTATION_ROADMAP.md) — phased, traceable work with status labels.
4. [C++ audit tasks](../IMPLEMENTATION_TASKS.md) — the existing 35-item source/build audit; it remains separate from the larger feature roadmap.

## Context guardrails

- Treat the checked-in C++ source as the implementation authority; attached prose and screenshots are design input, not proof that a feature exists.
- Reuse current `ViewType` pages and systems where possible. Add a new page only where the flow needs a distinct user decision or loading state.
- The reference images establish mood and hierarchy, not a requirement to copy another game's art, logo, or proprietary assets.
- Keep multiplayer claims precise: the current lobby/network work is local/LAN-oriented and is not yet authoritative internet combat replication.
- Mark a feature complete only after its code path is implemented and its relevant automated or hands-on check passes.

