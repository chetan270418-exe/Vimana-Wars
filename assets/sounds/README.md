# Vimana Wars — Sound Assets

Place sound files in this directory. The game loads them automatically.
**Missing files are silently skipped** — the game will never crash over audio.

## Required Files

| Filename | What it's for | Freesound search |
|---|---|---|
| `shoot.wav` | Player fires a bullet | "laser shoot 8bit" |
| `hit.wav` | Player takes damage | "damage hit player" |
| `explosion.wav` | Enemy explodes | "explosion arcade" |
| `powerup.wav` | Power-up collected | "item pickup jingle" |
| `boss_roar.wav` | Ravana appears | "monster roar deep" |
| `victory.wav` | Ravana defeated | "fanfare win short" |
| `game_over.wav` | Player dies | "game over sting" |
| `wave_clear.wav` | Wave completed | "stage clear short" |
| `combat_loop.mp3` | Looping combat background music | OpenGameArt CC0 track |

The `online_*.ogg` files are selected CC0 variations from Kenney's Sci-fi
Sounds pack. The game prefers them for shooting, impacts, explosions, and
dashes, and falls back to the generated WAVs if the OGG files are unavailable.

## License Reminder
The generated WAV effects require no external attribution.
The combat loop is a CC0 track; its source and author are recorded in
the project-level CREDITS.md.

## Format
WAV (preferred) or OGG. MP3 can work but may have latency issues on some systems.
