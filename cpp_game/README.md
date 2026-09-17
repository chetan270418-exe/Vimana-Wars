# 🛸 Vimana Wars // C++ Native Desktop Edition

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
- **Expanded 12-Ship Fleet**:
  - Starter: Pushpaka, Tripura, Garuda
  - Wave Unlocks: Vajra Spear, Naga Coil, Agneyastra, Soma Ark, Kubera Galleon, Surya Flare
  - **NEW** Tank Archetype: 🐘 **Airavata** (300 HP, kinetic barrier absorption)
  - **NEW** Support Archetype: 🐄 **Kamadhenu** (Passive hull regeneration & amrita aura)
  - **NEW** Wave 30 Ultimate: 🦁 **Narasimha** (High-risk ferocious claw slashes, solar roar & berserk damage scaling)
- **Campaign & Boss Encounters (30 Waves)**:
  - Wave 5: Titan Kumbhakarna
  - Wave 10: Emperor Ravana
  - Wave 11–12: Vibhishana defection story beat
  - Wave 15: Warlord Mahishasura
  - Wave 25: Conqueror Indrajit (Cloaking mirages & serpent arrows)
  - Wave 30: Tyrant Hiranyakashipu (3-phase immortal barrier — vanquishing him unlocks Narasimha!)
- **Prana Shards & Consumables Armory**:
  - Earn Prana Shards from waves, bosses, and duels.
  - Spend in the Armory to unlock ships early or purchase pre-run consumables:
    - 🛡️ **Kavach Shield Charge**: One-time automatic fatal hit negation.
    - 🧪 **Soma Vial** (`C` key): Mid-run emergency restorative heal.
    - ⚡ **Vajra Flare** (`V` key): Tactical 24-blade sub-screen clear.
- **Multiplayer & Training Modes**:
  - **Local 1v1 PvP**: Same-keyboard combat (P1: WASD + Space/Q vs P2: Arrows + Enter/Slash).
  - **AI Bot Training**: Practice vs customizable AI bot with 3 difficulty levels (**Novice**, **Skilled**, **Asura Master**).
  - **Sangha Lobby Browser**: Network lobby browser connecting to the Flask backend.
- **Database Integration**:
  - Embedded SQLite3 engine reading/writing directly to `leaderboard.db`.
  - JSON save system storing pilot progression in `~/.vimana_wars/save.json`.

---

## 🕹️ Controls

| Action | Player 1 (WASD) | Player 2 (Local Duel) |
|---|---|---|
| **Move** | `W`, `A`, `S`, `D` | Arrow Keys (`Up`, `Down`, `Left`, `Right`) |
| **Aim & Shoot** | Mouse Cursor + `LMB` / `Space` | Facing direction + `Enter` / `Right Ctrl` |
| **Vayu Dash** | `Left Shift` / `RMB` | `Slash` (`/`) / `Right Shift` |
| **Sudarshana Chakram** | `Q` / `E` | — |
| **Brahmastra Bomb** | `F` | — |
| **Soma Vial Heal** | `C` | — |
| **Vajra Flare** | `V` | — |
| **Pause / Menu** | `ESC` | `ESC` |

---

## 🚀 Quick Start

- **Launch Game**: Run `start.bat` in this folder or `start_cpp_game.bat` in the repository root.
- **Build / Recompile**: Run `build.bat` in this folder.
