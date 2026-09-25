# 🛸 Vimana Wars // C++ Native Desktop Edition (Windows-only)

> **Platform:** Windows 10/11 64-bit only (MinGW + WinSock2 + Raylib). No Linux/macOS build.
> Build with `build.bat` (MinGW g++ required). Do not commit `bin/VimanaWars.exe`.

A high-performance, native C++20 port of **Vimana Wars** built with **Raylib 6.0**, featuring custom Data Structures & Algorithms (DSA), SQLite3 database integration, local multiplayer, and AI training.

---

## ⚡ Key Highlights

- **Native C++ Performance**: Statically compiled 64-bit Windows executable running at a steady 60 FPS with zero external DLL dependencies.
- **Aspect-Preserving Logical Scaling**: 900×600 virtual canvas rendered via bilinear hardware FBO, scaling dynamically to any screen resolution or fullscreen.
- **Data Structures & Algorithms (DSA)**:
  - **Spatial Partitioning Grid (`SpatialGrid`)**: Amortized $O(1)$ broadphase collision detection for all projectiles, ships, and astral drops.
  - **Object Pools (`ObjectPool<T>`)**: Preallocated memory pools for bullets and particles ensuring zero heap allocations during intense bullet hell combat.
  - **Circular Ring Buffers (`RingBuffer<T>`)**: Zero-overhead FIFO queue for floating combat damage numbers.
  - **Hierarchical State Machine (`StateMachine`)**: Robust management of screens and multi-phase boss attack states.
- **Hangar (Starter Ships + Unlockable Fleet)**:
   - Three starter ships (Pushpaka/Tripura/Garuda) with unique guns; Vajra [BURST], Naga [PIERCE], Agneyastra [BURN] beyond Act I.
   - Airavata is a heavy tank, Kamadhenu regenerates hull, and Narasimha gains damage as its hull falls.
   - Ship frame upgrades persist and improve hull, weapon damage, speed, and dash recovery.
- **Campaign & Boss Encounters (Act I: 30 Waves)**:
   - Waves escalate through five distinct act beats culminating in Kumbhakarna and Ravana boss encounters with 3 unique telegraph patterns each.
   - Act II and beyond are planned as Endless Mode after Act I is polished.
- **Prana Shards & Consumables Armory**:
  - Earn Prana Shards from waves, bosses, and duels.
  - Spend in the Armory to unlock ships early or purchase pre-run consumables:
    - 🛡️ **Kavach Shield Charge**: One-time automatic fatal hit negation.
    - 🧪 **Soma Vial** (`C` key): Mid-run emergency restorative heal.
    - ⚡ **Vajra Flare** (`V` key): Tactical 24-blade sub-screen clear.
- **Multiplayer & Training Modes**:
  - **Local 1v1 PvP**: Same-keyboard combat (P1: WASD + Space/Q; P2: Arrows + Right Ctrl/Slash, abilities on Numpad 1–3).
  - **AI Bot Training**: Practice vs customizable AI bot with 3 difficulty levels (**Novice**, **Skilled**, **Asura Master**).
  - **Sangha Lobby Browser**: Lobby discovery/UDP room prototypes exist, but cross-client combat replication is not wired end-to-end. Local same-keyboard PvP is playable; do not treat the lobby as online co-op yet.
- **Database Integration**:
  - Embedded SQLite3 engine reading/writing directly to `leaderboard.db`.
  - JSON save system storing pilot progression in `~/.vimana_wars/save.json`.

---

## 🕹️ Controls

| Action | Player 1 (WASD) | Player 2 (Local Duel) |
|---|---|---|
| **Move** | `W`, `A`, `S`, `D` | Arrow Keys (`Up`, `Down`, `Left`, `Right`) |
| **Aim & Shoot** | Mouse Cursor + `LMB` / `Space` | Facing direction + `Right Ctrl` |
| **Vayu Dash** | `Left Shift` / `RMB` | `Slash` (`/`) / `Right Shift` |
| **Sudarshana Chakram** | `Q` (revive = `E`) | Numpad `1` |
| **Brahmastra Bomb** | `F` | — |
| **Soma Vial Heal** | `C` | Numpad `2` |
| **Vajra Flare** | `V` | Numpad `3` |
| **Pause / Menu** | `ESC` or `P` | `ESC` |

`ENTER` confirms selections in menus; Player 2 fires with `Right Ctrl` during local combat.
`P` opens the pilot profile from the main menu and pauses during gameplay. Gamepad input is not implemented yet; the current build is keyboard/mouse only. `F11` toggles fullscreen.

---

## 🚀 Quick Start

- **Launch Game**: Run `start.bat` in this folder or `start_cpp_game.bat` in the repository root.
- **Build / Recompile**: Run `build.bat` in this folder.
- **Run C++ audit smoke checks**: Run `test_audit.bat` for ship registry, boss/wave simulation, networking validation helpers, Continue-wave selection, and SQLite migration/score round-trip checks.
