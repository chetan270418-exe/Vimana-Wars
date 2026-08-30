"""
game/systems/audio_synthesizer.py
Pure-Python Procedural Sound Generator using standard library `wave`, `math`, and `struct`.
Generates crisp, retro-sci-fi 16-bit sound effects directly into assets/sounds/
so audio works out of the box with zero external downloads!
"""
import math
import random
import struct
import wave
from pathlib import Path


SOUND_DIR = Path("assets/sounds")


def _write_wav(filename: str, samples: list[float], sample_rate: int = 22050) -> None:
    SOUND_DIR.mkdir(parents=True, exist_ok=True)
    filepath = SOUND_DIR / filename
    if filepath.exists():
        return  # Don't overwrite existing files

    with wave.open(str(filepath), "wb") as wav_file:
        wav_file.setnchannels(1)       # Mono
        wav_file.setsampwidth(2)       # 16-bit
        wav_file.setframerate(sample_rate)

        # Convert float (-1.0 to 1.0) to 16-bit signed integer (-32767 to 32767)
        raw_frames = bytearray()
        for sample in samples:
            clamped = max(-1.0, min(1.0, sample))
            val = int(clamped * 32760)
            raw_frames.extend(struct.pack("<h", val))

        wav_file.writeframes(raw_frames)


def generate_all_sounds() -> None:
    """Generates all 8 core sound effects if missing."""
    sample_rate = 22050

    # 1. shoot.wav — Punchy high-frequency laser sweep
    samples = []
    dur = 0.12
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 880 - (t / dur) * 600
        vol = (1.0 - (t / dur)) ** 1.5
        sample = math.sin(2 * math.pi * freq * t) * vol
        samples.append(sample)
    _write_wav("shoot.wav", samples, sample_rate)

    # 2. dash.wav — Swift wind warp whoosh
    samples = []
    dur = 0.18
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 300 + math.sin(t * 30) * 150 + (t / dur) * 400
        noise = (random.random() * 2 - 1) * 0.35
        vol = math.sin(math.pi * (t / dur)) * 0.9
        sample = (math.sin(2 * math.pi * freq * t) * 0.65 + noise) * vol
        samples.append(sample)
    _write_wav("dash.wav", samples, sample_rate)

    # 3. hit.wav — Crisp metallic kinetic thud
    samples = []
    dur = 0.10
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 240 - (t / dur) * 160
        noise = (random.random() * 2 - 1) * 0.4
        vol = (1.0 - (t / dur)) ** 2
        sample = (math.sin(2 * math.pi * freq * t) * 0.6 + noise) * vol
        samples.append(sample)
    _write_wav("hit.wav", samples, sample_rate)

    # 4. explosion.wav — Heavy crunching blast with low-end rumble
    samples = []
    dur = 0.35
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 120 * (1.0 - (t / dur) * 0.7)
        noise = (random.random() * 2 - 1) * 0.75
        vol = (1.0 - (t / dur)) ** 1.2
        sample = (math.sin(2 * math.pi * freq * t) * 0.35 + noise * 0.65) * vol
        samples.append(sample)
    _write_wav("explosion.wav", samples, sample_rate)

    # 5. powerup.wav — Ascending celestial golden chime
    samples = []
    dur = 0.30
    total_samples = int(sample_rate * dur)
    notes = [440, 554.37, 659.25, 880]  # A Major chord arpeggio
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur)) * 0.85
        sample = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)) * vol
        samples.append(sample)
    _write_wav("powerup.wav", samples, sample_rate)

    # 6. boss_roar.wav — Deep terrifying sub-bass growl
    samples = []
    dur = 0.80
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 70 + math.sin(t * 24) * 35 - (t / dur) * 30
        noise = (random.random() * 2 - 1) * 0.4
        vol = math.sin(math.pi * (t / dur)) * 0.95
        sample = (math.sin(2 * math.pi * freq * t) * 0.7 + noise) * vol
        samples.append(sample)
    _write_wav("boss_roar.wav", samples, sample_rate)

    # 7. wave_clear.wav — Bright positive victory stinger
    samples = []
    dur = 0.40
    total_samples = int(sample_rate * dur)
    notes = [523.25, 659.25, 783.99, 1046.50]  # C Major fanfare
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur)) * 0.8
        sample = math.sin(2 * math.pi * freq * t) * vol
        samples.append(sample)
    _write_wav("wave_clear.wav", samples, sample_rate)

    # 8. victory.wav — Grand celebratory fanfare
    samples = []
    dur = 1.0
    total_samples = int(sample_rate * dur)
    melody = [(523.25, 0.2), (659.25, 0.2), (783.99, 0.2), (1046.50, 0.4)]
    for freq, note_dur in melody:
        note_samples = int(sample_rate * note_dur)
        for i in range(note_samples):
            t = i / sample_rate
            vol = (1.0 - (t / note_dur)) * 0.85
            sample = (math.sin(2 * math.pi * freq * t) + 0.2 * math.sin(4 * math.pi * freq * t)) * vol
            samples.append(sample)
    _write_wav("victory.wav", samples, sample_rate)

    # 9. game_over.wav — Descending minor collapse tone
    samples = []
    dur = 0.6
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 300 - (t / dur) * 220
        vol = (1.0 - (t / dur)) * 0.8
        sample = (math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(2 * math.pi * (freq * 0.5) * t)) * vol
        samples.append(sample)
    _write_wav("game_over.wav", samples, sample_rate)

    # 10. ui_click.wav — Crisp gentle UI selection click
    samples = []
    dur = 0.05
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 1200 - (t / dur) * 700
        vol = (1.0 - (t / dur)) ** 3
        sample = math.sin(2 * math.pi * freq * t) * vol * 0.7
        samples.append(sample)
    _write_wav("ui_click.wav", samples, sample_rate)

    # 11. warning_siren.wav — Pulsing danger klaxon for boss warning
    samples = []
    dur = 0.55
    total_samples = int(sample_rate * dur)
    for i in range(total_samples):
        t = i / sample_rate
        freq = 600 + math.sin(t * 28) * 250
        vol = math.sin(math.pi * (t / dur)) * 0.85
        sample = math.sin(2 * math.pi * freq * t) * vol
        samples.append(sample)
    _write_wav("warning_siren.wav", samples, sample_rate)

    # 12. dodge_chime.wav — Sparkling high chime for perfect dodge / near miss
    samples = []
    dur = 0.22
    total_samples = int(sample_rate * dur)
    notes = [1046.50, 1318.51, 1567.98]  # High C Major
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur)) * 0.75
        sample = (math.sin(2 * math.pi * freq * t) + 0.4 * math.sin(4 * math.pi * freq * t)) * vol
        samples.append(sample)
    _write_wav("dodge_chime.wav", samples, sample_rate)

    # 13. synergy.wav — Grand harmonic resonance for Deva Boon Fusion
    samples = []
    dur = 0.85
    total_samples = int(sample_rate * dur)
    notes = [523.25, 659.25, 783.99, 1046.50, 1318.51]  # Full ascending arpeggio with shimmering harmonics
    for i in range(total_samples):
        t = i / sample_rate
        note_idx = min(int((t / dur) * len(notes)), len(notes) - 1)
        freq = notes[note_idx]
        vol = (1.0 - (t / dur) * 0.8) * 0.9
        sample = (math.sin(2 * math.pi * freq * t) * 0.6 +
                  math.sin(2 * math.pi * (freq * 1.5) * t) * 0.25 +
                  math.sin(4 * math.pi * freq * t) * 0.15) * vol
        samples.append(sample)
    _write_wav("synergy.wav", samples, sample_rate)
