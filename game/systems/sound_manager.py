"""
game/systems/sound_manager.py
Wraps arcade.Sound — silently skips missing files so the game never crashes
if a sound file hasn't been dropped in yet.

HOW TO ADD SOUNDS
─────────────────
1. Download free CC0 files from a reputable asset source and verify the license
2. Save them as WAV (preferred) or OGG into  assets/sounds/
3. Name them to match the keys in _SOUND_FILES below
4. Restart the game — they load automatically

Suggested search terms on Freesound:
  shoot.wav    → "laser shoot 8bit"
  hit.wav      → "damage hit player"
  explosion.wav→ "explosion arcade"
  powerup.wav  → "item pickup"
  boss_roar.wav→ "monster roar"
  victory.wav  → "fanfare win"
  game_over.wav→ "game over sting"
  wave_clear.wav → "stage clear jingle"
"""
import arcade
from pathlib import Path

_ASSETS = Path(__file__).resolve().parent.parent.parent / "assets" / "sounds"

_SOUND_FILES: dict[str, str] = {
    "shoot":         "shoot.wav",
    "dash":          "dash.wav",
    "hit":           "hit.wav",
    "explosion":     "explosion.wav",
    "powerup":       "powerup.wav",
    "boss_roar":     "boss_roar.wav",
    "victory":       "victory.wav",
    "game_over":     "game_over.wav",
    "wave_clear":    "wave_clear.wav",
    "ui_click":      "ui_click.wav",
    "warning_siren": "warning_siren.wav",
    "dodge_chime":   "dodge_chime.wav",
    "synergy":       "synergy.wav",
    # Optional CC0 Kenney variations.  The generated WAVs remain fallbacks.
    "shoot_online":  "online_laser_small.ogg",
    "hit_online":    "online_impact_metal.ogg",
    "explosion_online": "online_explosion_crunch.ogg",
    "dash_online":   "online_thruster_fire.ogg",
}
_MUSIC_FILE = _ASSETS / "combat_loop.mp3"


class SoundManager:
    """
    Create one instance (e.g. in GameView.__init__).
    Call play_*(volume) methods anywhere in the game.
    Auto-synthesizes clean procedural sounds if sound files are missing.
    """

    _music_player = None

    def __init__(self):
        try:
            from game.systems.audio_synthesizer import generate_all_sounds
            generate_all_sounds()
        except Exception:
            pass

        self._sounds: dict[str, arcade.Sound | None] = {}
        for key, filename in _SOUND_FILES.items():
            path = _ASSETS / filename
            try:
                self._sounds[key] = arcade.load_sound(str(path))
            except Exception:
                self._sounds[key] = None

        try:
            self._music = arcade.load_sound(str(_MUSIC_FILE), streaming=True)
        except Exception:
            self._music = None

        self.master_vol = 0.8
        self.sfx_vol = 0.8
        self.music_vol = 0.8
        self.reload_volume()

    def reload_volume(self) -> None:
        try:
            from game.systems import save_system
            data = save_system.load()
            self.master_vol = data.get("volume", 80) / 100.0
            self.sfx_vol = data.get("sfx_volume", data.get("volume", 80)) / 100.0
            self.music_vol = data.get("music_volume", data.get("volume", 80)) / 100.0
        except Exception:
            self.master_vol = 0.8
            self.sfx_vol = 0.8
            self.music_vol = 0.8

        if SoundManager._music_player is not None:
            try:
                SoundManager._music_player.volume = max(0.0, min(1.0, 0.24 * self.music_vol))
            except Exception:
                pass

    def start_music(self, volume: float = 0.24) -> None:
        """Start the looping combat bed once for the current application."""
        if self._music is None or SoundManager._music_player is not None:
            return
        final_vol = max(0.0, min(1.0, volume * self.music_vol))
        if final_vol <= 0.01:
            return
        try:
            SoundManager._music_player = arcade.play_sound(
                self._music, volume=final_vol, loop=True
            )
        except Exception:
            SoundManager._music_player = None

    @classmethod
    def stop_music(cls) -> None:
        """Stop the shared music player when leaving gameplay."""
        if cls._music_player is None:
            return
        try:
            arcade.stop_sound(cls._music_player)
        except Exception:
            pass
        finally:
            cls._music_player = None

    def _play(self, key: str, volume: float = 1.0) -> None:
        final_vol = max(0.0, min(1.0, volume * self.sfx_vol))
        sound = self._sounds.get(key)
        if sound is not None and final_vol > 0.01:
            try:
                arcade.play_sound(sound, volume=final_vol)
            except Exception:
                pass

    def _play_any(self, keys: tuple[str, ...], volume: float = 1.0) -> None:
        """Play the first loaded variant, keeping generated audio as fallback."""
        final_vol = max(0.0, min(1.0, volume * self.sfx_vol))
        if final_vol <= 0.01:
            return
        for key in keys:
            sound = self._sounds.get(key)
            if sound is None:
                continue
            try:
                arcade.play_sound(sound, volume=final_vol)
            except Exception:
                pass
            return

    def play_dash(self, volume: float = 0.55) -> None: self._play_any(("dash_online", "dash"), volume)

    # ── Convenience methods ──────────────────────────────────────────
    def play_shoot(self,         volume: float = 0.35) -> None: self._play_any(("shoot_online", "shoot"), volume)
    def play_hit(self,           volume: float = 0.70) -> None: self._play_any(("hit_online", "hit"), volume)
    def play_explosion(self,     volume: float = 0.80) -> None: self._play_any(("explosion_online", "explosion"), volume)
    def play_powerup(self,       volume: float = 1.00) -> None: self._play("powerup",       volume)
    def play_boss_roar(self,     volume: float = 1.00) -> None: self._play("boss_roar",     volume)
    def play_victory(self,       volume: float = 1.00) -> None: self._play("victory",       volume)
    def play_game_over(self,     volume: float = 0.90) -> None: self._play("game_over",     volume)
    def play_wave_clear(self,    volume: float = 0.70) -> None: self._play("wave_clear",    volume)
    def play_ui_click(self,      volume: float = 0.60) -> None: self._play("ui_click",      volume)
    def play_warning_siren(self, volume: float = 0.85) -> None: self._play("warning_siren", volume)
    def play_dodge_chime(self,   volume: float = 0.75) -> None: self._play("dodge_chime",   volume)
    def play_synergy(self,       volume: float = 1.00) -> None: self._play("synergy",       volume)
