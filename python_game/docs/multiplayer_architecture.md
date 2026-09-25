# Vimana Wars — Multiplayer Architecture

**Status:** Design proposal, not implemented. Aimed at the Python/Arcade client + Flask backend you already have.

---

## TL;DR — what kind of multiplayer you actually want

Before writing a single line of netcode, pick a target. These are very different engineering efforts:

| Mode | Players | Latency tolerance | Bandwidth | Difficulty | What it gives you |
|---|---|---|---|---|---|
| **Co-op campaign** | 2 | medium (~150 ms) | high | hard | Play through waves together; revive each other; shared score |
| **Versus arena** | 2–4 | low (~50 ms) | medium | very hard | Real-time duel; whoever kills the other wins |
| **Async leaderboard race** | many | any | low | easy | Same seed, "ghost" of another player's run; leaderboard ranking |
| **Async duel** | 2 | any | low | medium | Two players run separately, "replay" each other's wave, judged by score |
| **Co-op endless horde** | 2–4 | medium | high | very hard | Endless waves, both players vs shared enemy spawn |

For a solo project already running on arcade, my honest recommendation: **ship async leaderboard race first**, then **co-op campaign**. Skip real-time versus until you have a budget — it's a 6-month project on its own.

The rest of this doc covers how to build **async leaderboard race** (1–2 weeks) and **co-op campaign** (3–6 weeks). Real-time versus is mentioned briefly at the end.

---

## 1. Async leaderboard race (do this first)

### What it actually is
- Player A finishes a run. Their final state (wave reached, score, boss kills, combo peak, ship, difficulty) gets uploaded.
- Player B starts a new run on a difficulty/ship/wave combo that matches an existing ghost.
- During Player B's run, every ~10–15 seconds they get a brief "phantom" challenge: "beat this score at wave 5 in 60 seconds." Phantom challenges are seeded from Player A's actual gameplay data.
- After Player B finishes, both runs are compared side-by-side on the leaderboard view.

The **player never sees another player's ship live**. It's all score-comparison and "beat this checkpoint" challenges. This is how Vampire Survivors handles the async social layer.

### What you need
- ✅ Already have: Flask backend with `scores` table
- ❌ Need to add: `run_snapshots` table with checkpoints

```sql
-- New table
CREATE TABLE IF NOT EXISTS run_snapshots (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT NOT NULL,                 -- one run = one row group
    player_name     TEXT NOT NULL,
    ship_class      TEXT NOT NULL,
    difficulty      TEXT NOT NULL,
    wave_number     INTEGER NOT NULL,
    score           INTEGER NOT NULL,
    elapsed_seconds REAL NOT NULL,
    boss_kills      INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_snapshots_lookup
    ON run_snapshots (ship_class, difficulty, wave_number, score);
```

- ❌ Need to add: `ghosts` view that picks matching ghost for a fresh run
- ❌ Need to add: client-side `GhostManager` that pulls one checkpoint per ~12 seconds and shows a small toast: "Ghost target: 4,200 pts at wave 5. Beat it?"

### Implementation cost
- **Backend:** 1 day. ~150 lines of Flask, 1 SQL migration, 1 new test file.
- **Client:** 2–3 days. A `GhostManager` class, periodic fetch with `threading.Timer`, a `GhostToastView` that shows the challenge. Tied into the existing `achievement_manager` for "Beat 10 ghosts" achievements.
- **Polish:** 2 days. Comparing runs side-by-side at game-over, score-difference arrows, "you beat ghost by 1,200 pts" toast.

---

## 2. Co-op campaign (real network play, but not real-time combat)

This is what I'd build next. The key insight: **you don't need real-time combat for co-op**. The "trick" is to keep combat single-player but synchronize *between waves*.

### Game design: turn-based-ish co-op

- Player A and Player B both start the same run (same ship, same difficulty, same starting wave).
- Each player fights their OWN enemies on their OWN screen.
- Between waves (during the 3-second clear pause), the game syncs results:
  - "Your teammate cleared wave 3 with 850 pts. Combo was ×4."
  - "Boss arrives next wave — get ready."
- Boss waves are SHARED damage: combined damage to the boss is split between the two runs (each player's boss has combined HP).
- Score is summed for the leaderboard entry.

This is how *It Takes Two*, *Overcooked* and *Shovel Knight: Shovel of Hope DX*'s online feature work — separate screens, periodic sync.

### Why this is the right choice for your codebase

Your existing code is already single-player with local state. You don't need to:
- Refactor collision to handle multiple worlds
- Rework boons, power-ups, or chakram targeting
- Add lag compensation or rollback netcode

You just need to:
- Track each player's state at "decision points" (wave clears, boss defeats)
- Send that state through the existing Flask backend
- Display the partner's last-known state in a corner UI

### Architecture

```
┌──────────────────────┐                            ┌──────────────────────┐
│   Client A           │                            │   Client B            │
│                      │   HTTPS / WebSocket        │                       │
│  ┌────────────────┐  │   via your existing Flask │  ┌────────────────┐   │
│  │ CoOpGameView   │  │   backend                  │  │ CoOpGameView   │   │
│  │   (extends      │◄─┤                            ├─►│   (extends     │   │
│  │    GameView)    │  │   GET /co-op/lobby         │  │    GameView)   │   │
│  └────────────────┘  │   POST /co-op/sync         │  └────────────────┘   │
│         ▲            │   GET /co-op/partner       │          ▲            │
│         │            │                            │          │            │
│  ┌──────┴──────┐     │                            │  ┌───────┴─────┐      │
│  │ CoOpSession │     │                            │  │ CoOpSession │      │
│  │ (sync loop) │     │                            │  │ (sync loop) │      │
│  └─────────────┘     │                            │  └─────────────┘      │
│                      │                            │                       │
└──────────────────────┘                            └───────────────────────┘
                                        ▲
                                        │
                              ┌─────────┴────────┐
                              │   Flask backend   │
                              │   /co-op/ routes  │
                              │   session table   │
                              └──────────────────┘
```

### Backend endpoints to add

```python
# All behind your existing @app.route patterns

POST /co-op/lobby              # create or join a session
    # Body: {session_code, player_name, ship_class, difficulty, start_wave}
    # Returns: {session_id, partner_name, partner_ship, partner_wave,
    #          partner_score, partner_combo}

POST /co-op/sync               # push my wave-end state, pull partner's
    # Body: {session_id, player_name, wave, score, elapsed_sec,
    #        boss_killed, combo_peak, hp_pct}
    # Returns: {partner_wave, partner_score, partner_hp_pct,
    #          partner_boss_killed, message_text}   # e.g. "Rohit crushed wave 4!"

POST /co-op/complete           # session done, return combined score
    # Returns: {partner_name, combined_score, leaderboard_rank}

GET  /co-op/sessions/<id>       # debug: get full session history
```

Backend additions: **~300 lines, 1 day.**

### Client additions

```
python_game/game/coop/
    __init__.py
    session.py          # CoOpSession — WebSocket/HTTP loop, retry logic
    ghost_partner.py    # GhostPartnerUI — corner card with partner state
    co_op_game_view.py  # CoOpGameView — extends GameView, calls session.sync()
    co_op_lobby_view.py # matchmaking UI (enter code / random partner)
```

Client additions: **~600 lines, 3–4 days.**

### Network choice: WebSocket vs polling

I'd use **HTTP polling every 3 seconds during wave clears, every 0.5 seconds during boss waves**. WebSockets add a dependency (`flask-socketio`) and your existing backend doesn't have them. Polling matches your existing Flask architecture perfectly and 3s latency is fine for wave-end sync. For boss waves you'd just increase the poll rate.

If you really want push notifications later, swap in `flask-socketio` — the polling code already abstracts the transport.

### Existing-code changes you'll need

1. **`WaveManager.update`** — call a hook at every wave clear with the wave summary. The hook in solo mode is a no-op; in co-op mode it calls `session.sync()`.

2. **`BossRavana.take_damage`** / **`BossKumbhakarna.take_damage`** — call a hook with the damage dealt. In co-op mode the hook adds to a shared HP pool.

3. **`ScoreSystem.register_kill`** — same hook pattern for combined scoring.

Use **dependency injection** rather than singletons:

```python
# In co_op_game_view.py:
self.wave_manager.on_wave_clear = self.session.push_wave_result
self.score_system.on_kill = self.session.push_kill
```

When the view exits, set them back to no-ops. Clean, no global state.

---

## 3. Real-time versus — **don't build this yet**

If you really want it, here's the honest scope:

| Component | Tech | Effort |
|---|---|---|
| Deterministic game state | Fixed-point math, no `random` without seed | 2 weeks refactor |
| Rollback netcode | GGPO-style input delay + re-simulation | 3 weeks |
| Lockstep or peer-to-peer host | One host, others clients, or P2P | 2 weeks |
| Disconnect handling | Reconnect + 10s grace | 1 week |
| Cheat prevention | Server-authoritative hits, sanity-check score deltas | 1 week |
| Testing | Deterministic replay suite, packet loss simulator | 1 week |

Total: **3 months of dedicated work.** Your current `random.random()` calls in wave_manager, particles, and damage variance are non-deterministic — every system would need a seeded RNG. Save data is local-only — needs server-side persistence with conflict resolution.

That's a real project, not a feature. Build async first, ship, get players, *then* decide if real-time combat is worth it.

---

## 4. Recommended rollout (concrete milestones)

| Week | Milestone | What ships |
|---|---|---|
| **1** | Backend `run_snapshots` + 2 endpoints | Ghost challenges appear in solo runs |
| **2** | Client `GhostManager` + ghost toast UI | Players see "beat this score" prompts during runs |
| **3** | Co-op session table + lobby endpoints | Two players can matchmake and start a co-op run |
| **4–5** | `CoOpGameView` + sync integration | Full co-op campaign playable |
| **6** | Co-op polish + leaderboard | Combined-score leaderboard entry, "best duo" badge |
| **optional** | Async duel mode (replays) | After co-op, judge runs against each other |

End of week 2 you have a shippable async social layer. End of week 6 you have a full co-op campaign.

---

## 5. Cheat prevention (you'll need this eventually)

Even for async, cheaters can:
- Submit fake scores from a script
- Modify local save.json to unlock everything

Quick wins:
- **Server-side validation:** reject score deltas that exceed theoretical max from wave + kills + time
- **Hash chain:** each snapshot includes `prev_hash`; server detects tampering
- **Account binding:** require email confirmation before leaderboard submission (you already have `account_view.py` — perfect)

Don't build this until you have 100+ players. Cheaters don't matter for an indie game with <1k active users.

---

## 6. The one thing to do today

Open your `backend/app.py`, find the scores route, and add this **one endpoint**:

```python
@app.route("/scores/ghost", methods=["GET"])
def get_ghost_target():
    """Return a checkpoint target for the current run."""
    difficulty = request.args.get("difficulty", "normal")
    ship_class = request.args.get("ship_class", "pushpaka")
    current_wave = int(request.args.get("wave", 1))

    row = get_db().execute("""
        SELECT player_name, score, wave_number
        FROM scores
        WHERE difficulty = ? AND wave_number = ?
          AND score > ?
        ORDER BY score ASC
        LIMIT 1
    """, (difficulty, current_wave, current_wave * 100)).fetchone()

    if row is None:
        return jsonify({"ghost": None})
    return jsonify({
        "ghost": {
            "name": row["player_name"],
            "target_score": row["score"],
            "at_wave": row["wave_number"],
        }
    })
```

This is **20 lines of backend**. Then in `GameView._trigger_wave_clear`, fetch a ghost and show a toast: *"Beat Vikram's wave-5 score of 4,200."* The whole feature is ~150 lines client-side and gives you an actual social hook for zero new infrastructure.

Build this. Then ship. Then talk to me about real-time.

---

## Open questions for you

1. **Co-op scope:** 2 players or up to 4? (4 needs shared-camera work, 2 is much simpler)
2. **Async ghost:** ship in next release, or wait for co-op?
3. **Account system:** use what you have (email-bound leaderboard via `account_view`), or guest accounts?
4. **Web version priority:** is the `web/` directory the priority now, or Python?
5. **cpp_game:** is the C++ port the long-term plan? If so, multiplayer needs C++ too, which doubles the scope.

Pick one or two and I'll start coding.
