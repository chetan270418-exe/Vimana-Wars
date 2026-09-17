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
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_sfx_volume * volume_mult * m_master_volume);
            PlaySound(snd);
        }
    }

    void play_ui(const std::string& sound_file, float volume_mult = 1.0f) {
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_ui_volume * volume_mult * m_master_volume);
            PlaySound(snd);
        }
    }

    void play_boss(const std::string& sound_file, float volume_mult = 1.0f) {
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_boss_volume * volume_mult * m_master_volume);
            PlaySound(snd);
        }
    }

    void play_music(const std::string& music_file) {
        AssetManager::instance().load_music(music_file);
        AssetManager::instance().set_music_volume(m_music_volume * m_master_volume);
    }

    void update_music() {
        AssetManager::instance().update_music();
    }

    // ── DYNAMIC BOSS PHASE ESCALATION ───────────────────────────────────────
    void set_boss_phase(int phase) {
        // Subtle pitch and intensity shift per boss phase
        m_boss_phase = phase;
        // Adjust music volume / tension dynamically
        if (phase == 2) {
            AssetManager::instance().set_music_volume(std::min(1.0f, m_music_volume * 1.15f) * m_master_volume);
        } else if (phase == 3) {
            AssetManager::instance().set_music_volume(std::min(1.0f, m_music_volume * 1.25f) * m_master_volume);
            play_boss("warning_siren.wav", 0.8f);
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

    // ── VOLUME SETTERS & GETTERS ────────────────────────────────────────────
    void set_master_volume(float vol) {
        m_master_volume = std::clamp(vol, 0.0f, 1.0f);
        SetMasterVolume(m_master_volume);
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
