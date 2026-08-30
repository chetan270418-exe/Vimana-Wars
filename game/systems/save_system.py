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
    "difficulty":    "normal",   # "easy" | "normal" | "hard"
    "total_kills":   0,
    "games_played":  0,
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


def update_after_game(score: int, wave: int, kills: int) -> dict:
    """
    Convenience: load, update high score / wave / kills, save, return updated data.
    """
    data = load()
    data["high_score"]   = max(data["high_score"], score)
    data["last_wave"]    = max(data["last_wave"], wave)
    data["total_kills"] += kills
    data["games_played"] += 1
    save(data)
    return data


def get_difficulty() -> str:
    return load().get("difficulty", "normal")


def set_difficulty(level: str) -> None:
    assert level in ("easy", "normal", "hard"), f"Unknown difficulty: {level}"
    data = load()
    data["difficulty"] = level
    save(data)
