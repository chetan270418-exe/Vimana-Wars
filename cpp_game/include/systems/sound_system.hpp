#pragma once
#include <string>
#include <algorithm>
#include "raylib.h"
#include "systems/asset_manager.hpp"

namespace Vimana {

class SoundSystem {
public:
    static SoundSystem& instance() {
        static SoundSystem sys;
        return sys;
    }

    void init() {
        InitAudioDevice();
        SetMasterVolume(m_master_volume);
    }

    void cleanup() {
        CloseAudioDevice();
    }

    // ── AUDIO CHANNELS ──────────────────────────────────────────────────────
    void play_sfx(const std::string& sound_file, float volume_mult = 1.0f) {
        if (!IsAudioDeviceReady()) return;
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_sfx_volume * volume_mult * m_master_volume);
            PlaySound(snd);
        }
    }

    void play_ui(const std::string& sound_file, float volume_mult = 1.0f) {
        if (!IsAudioDeviceReady()) return;
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_ui_volume * volume_mult * m_master_volume);
            PlaySound(snd);
        }
    }

    void play_boss(const std::string& sound_file, float volume_mult = 1.0f) {
        if (!IsAudioDeviceReady()) return;
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_boss_volume * volume_mult * m_master_volume);
            PlaySound(snd);
        }
    }

    void play_music(const std::string& music_file) {
        if (!IsAudioDeviceReady()) return;
        AssetManager::instance().load_music(music_file);
        AssetManager::instance().set_music_volume(m_music_volume * m_master_volume);
    }

    void update_music() {
        AssetManager::instance().update_music();
    }

    // ── DYNAMIC BOSS PHASE ESCALATION ───────────────────────────────────────
    void set_boss_phase(int phase) {
        if (phase == m_boss_phase) return;
        // Subtle pitch and intensity shift per boss phase
        m_boss_phase = phase;
        // Adjust music volume / tension dynamically
        if (phase == 2) {
            AssetManager::instance().set_music_volume(std::min(1.0f, m_music_volume * 1.15f) * m_master_volume);
            play_boss("boss_roar.wav", 0.75f);
        } else if (phase == 3) {
            AssetManager::instance().set_music_volume(std::min(1.0f, m_music_volume * 1.25f) * m_master_volume);
            play_boss("warning_siren.wav", 0.8f);
            play_boss("boss_roar.wav", 0.9f);
        } else {
            AssetManager::instance().set_music_volume(m_music_volume * m_master_volume);
        }
    }

    // ── DEDICATED SFX TRIGGERS ──────────────────────────────────────────────
    void play_ui_click() { play_ui("ui_click.wav", 0.7f); }
    void play_ui_hover() { play_ui("ui_click.wav", 0.3f); }
    void play_ui_confirm() { play_ui("powerup.wav", 0.8f); }
    void play_dash() { play_sfx("dash.wav", 0.85f); }
    void play_hit() { play_sfx("hit.wav", 0.75f); }
    void play_explosion() { play_sfx("explosion.wav", 0.9f); }
    void play_downed_alert() { play_sfx("warning_siren.wav", 0.9f); }
    void play_revive_complete() { play_sfx("synergy.wav", 1.0f); }
    void play_transcendence() { play_sfx("victory.wav", 0.9f); }
    void play_boss_roar() { play_boss("boss_roar.wav", 1.0f); }

    // ── MODERN PHASE 8/9 SCI-FI SFX (Kenney Sci-Fi Sounds Pack — CC0) ─────────
    // Lasers
    void play_heavy_laser()     { play_sfx("laserLarge_000.ogg",        0.90f); }
    void play_retro_laser()     { play_sfx("laserRetro_000.ogg",        0.80f); }
    void play_small_laser()     { play_sfx("laserSmall_000.ogg",        0.75f); }
    // Explosions
    void play_crunch_explosion(){ play_sfx("explosionCrunch_000.ogg",   0.95f); }
    void play_low_explosion()   { play_sfx("lowFrequency_explosion_000.ogg", 1.0f); }
    // Impacts
    void play_metal_impact()    { play_sfx("impactMetal_000.ogg",       0.85f); }
    void play_force_field()     { play_sfx("forceField_000.ogg",        0.80f); }
    // Engines
    void play_engine_boost()    { play_sfx("engineCircular_000.ogg",    0.70f); }
    void play_engine_large()    { play_sfx("spaceEngineLarge_000.ogg",  0.70f); }
    void play_engine_low()      { play_sfx("spaceEngineLow_000.ogg",    0.65f); }
    void play_engine_small()    { play_sfx("spaceEngineSmall_000.ogg",  0.60f); }
    void play_thruster()        { play_sfx("thrusterFire_000.ogg",      0.65f); }
    // UI / Computer
    void play_telemetry_chime() { play_ui("computerNoise_000.ogg",      0.70f); }
    void play_door_open()       { play_ui("doorOpen_000.ogg",           0.60f); }
    void play_door_close()      { play_ui("doorClose_000.ogg",          0.55f); }
    // Legacy named aliases (keep compatibility with existing code)
    void play_heavy_laser_legacy()     { play_sfx("phase8_laserLarge_000.ogg",        0.90f); }
    void play_crunch_explosion_legacy(){ play_sfx("phase8_explosionCrunch_001.ogg",   0.95f); }
    void play_metal_impact_legacy()    { play_sfx("phase8_impactMetal_001.ogg",       0.85f); }
    void play_engine_boost_legacy()    { play_sfx("phase8_engineCircular_001.ogg",    0.75f); }
    void play_telemetry_chime_legacy() { play_ui("phase8_computerNoise_001.ogg",      0.70f); }

    // ── VOLUME SETTERS & GETTERS ────────────────────────────────────────────
    void set_master_volume(float vol) {
        m_master_volume = std::clamp(vol, 0.0f, 1.0f);
        if (IsAudioDeviceReady()) SetMasterVolume(m_master_volume);
    }

    void set_sfx_volume(float vol) {
        m_sfx_volume = std::clamp(vol, 0.0f, 1.0f);
    }

    void set_ui_volume(float vol) {
        m_ui_volume = std::clamp(vol, 0.0f, 1.0f);
    }

    void set_boss_volume(float vol) {
        m_boss_volume = std::clamp(vol, 0.0f, 1.0f);
    }

    void set_music_volume(float vol) {
        m_music_volume = std::clamp(vol, 0.0f, 1.0f);
        AssetManager::instance().set_music_volume(m_music_volume * m_master_volume);
    }

    float master_volume() const { return m_master_volume; }
    float sfx_volume() const { return m_sfx_volume; }
    float ui_volume() const { return m_ui_volume; }
    float boss_volume() const { return m_boss_volume; }
    float music_volume() const { return m_music_volume; }

private:
    SoundSystem() = default;
    ~SoundSystem() = default;

    float m_master_volume = 0.8f;
    float m_sfx_volume = 0.8f;
    float m_ui_volume = 0.75f;
    float m_boss_volume = 0.85f;
    float m_music_volume = 0.7f;
    int m_boss_phase = 1;
};

} // namespace Vimana
