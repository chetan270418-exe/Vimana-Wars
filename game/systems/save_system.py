"""
game/systems/save_system.py
Local save/load using a JSON file in the user's app data directory.
Saves: high score, settings (volume, screen shake, particles, fullscreen, difficulty).
"""
import json
import os
from pathlib import Path

# Save file lives in user home directory under ~/.vimana_wars/
_SAVE_DIR  = Path(os.path.expanduser("~")) / ".vimana_wars"
_SAVE_FILE = _SAVE_DIR / "save.json"

_DEFAULTS = {
    "player_name":   "Warrior",
    "high_score":    0,
    "last_wave":     0,
    "difficulty":    "normal",   # "easy" | "normal" | "hard" | "endless"
    "last_ship":     "pushpaka",
    # Online identity is optional; guest play remains available offline.
    "auth_token":    "",
    "game_id":       "",
    "account_email": "",
    "last_realm":    1,
    "realm_unlock_seen": [],
    "total_kills":   0,
    "games_played":  0,
    "total_damage":      0,            # lifetime damage dealt
    "best_combo":        1,            # highest single-run combo ever
    "total_boons":       0,            # total boons claimed across all runs
    "bosses_defeated":   [],           # list of boss ids the player has beaten
    "playtime_seconds":  0,            # total in-game time across sessions
    "ships_mastered":    [],           # ship ids used to clear campaign
    "volume":             80,         # 0 - 100 (master/legacy)
    "sfx_volume":         80,         # 0 - 100
    "music_volume":       80,         # 0 - 100
    "screen_shake":       "full",     # "full" | "low" | "off"
    "particles":          "high",     # "high" | "low"
    "reduced_flashes":    False,      # True | False (accessibility)
    "colorblind_mode":    "off",      # "off" | "protan" | "deutan" | "tritan"
    "fullscreen":         False,
    "endless_high_wave":  0,
    "endless_high_score": 0,
}

_SYNC_KEYS = (
    "player_name", "high_score", "last_wave", "difficulty", "last_ship",
    "last_realm", "realm_unlock_seen", "total_kills", "games_played",
    "total_damage", "best_combo", "total_boons", "bosses_defeated",
    "playtime_seconds", "ships_mastered", "achievements", "endless_high_wave",
    "endless_high_score",
)


def _ensure_dir() -> None:
    _SAVE_DIR.mkdir(parents=True, exist_ok=True)


def load() -> dict:
    """Return save data, falling back to defaults if the file doesn't exist."""
    _ensure_dir()
    if not _SAVE_FILE.exists():
        return dict(_DEFAULTS)
    try:
        with open(_SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key, default in _DEFAULTS.items():
            data.setdefault(key, default)
        return data
    except (json.JSONDecodeError, OSError):
        return dict(_DEFAULTS)


def save(data: dict) -> None:
    """Write data dict to disk."""
    _ensure_dir()
    try:
        with open(_SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass   # graceful degradation — never crash over a save failure


def profile_for_sync(data: dict = None) -> dict:
    """Return only safe gameplay state for authenticated cloud synchronization."""
    source = data if data is not None else load()
    return {key: source.get(key, _DEFAULTS.get(key)) for key in _SYNC_KEYS}


def update_after_game(score: int, wave: int, kills: int,
                      *, highest_combo: int = 1,
                      total_damage: int = 0,
                      boons_claimed: int = 0,
                      bosses_defeated: list = None,
                      ship_class: str = None,
                      campaign_cleared: bool = False) -> dict:
    """
    Convenience: load, update lifetime stats, save, return updated data.
    All new args are optional for backward compatibility.
    """
    data = load()
    data["high_score"]   = max(data["high_score"], score)
    data["last_wave"]    = max(data["last_wave"], wave)
    data["total_kills"] += kills
    data["games_played"] += 1
    data["total_damage"] += max(0, total_damage)
    data["best_combo"]   = max(data["best_combo"], max(1, highest_combo))
    data["total_boons"]  += max(0, boons_claimed)
    if bosses_defeated:
        existing = set(data.get("bosses_defeated") or [])
        for bid in bosses_defeated:
            existing.add(bid)
        data["bosses_defeated"] = sorted(existing)
    if ship_class and campaign_cleared:
        mastered = set(data.get("ships_mastered") or [])
        mastered.add(ship_class)
        data["ships_mastered"] = sorted(mastered)
    save(data)
    return data


def add_playtime(seconds: float) -> dict:
    """Accumulate playtime (called each frame from the active game view)."""
    if seconds <= 0:
        return load()
    data = load()
    data["playtime_seconds"] = float(data.get("playtime_seconds", 0)) + seconds
    save(data)
    return data


def get_difficulty() -> str:
    return load().get("difficulty", "normal")


def set_difficulty(level: str) -> None:
    assert level in ("easy", "normal", "hard", "endless"), f"Unknown difficulty: {level}"
    data = load()
    data["difficulty"] = level
    save(data)
