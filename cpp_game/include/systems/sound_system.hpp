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

    void play_sfx(const std::string& sound_file, float volume_mult = 1.0f) {
        Sound snd = AssetManager::instance().get_sound(sound_file);
        if (snd.stream.buffer != nullptr) {
            SetSoundVolume(snd, m_sfx_volume * volume_mult);
            PlaySound(snd);
        }
    }

    void play_music(const std::string& music_file) {
        AssetManager::instance().load_music(music_file);
        AssetManager::instance().set_music_volume(m_music_volume);
    }

    void update_music() {
        AssetManager::instance().update_music();
    }

    void set_master_volume(float vol) {
        m_master_volume = std::clamp(vol, 0.0f, 1.0f);
        SetMasterVolume(m_master_volume);
    }

    void set_sfx_volume(float vol) {
        m_sfx_volume = std::clamp(vol, 0.0f, 1.0f);
    }

    void set_music_volume(float vol) {
        m_music_volume = std::clamp(vol, 0.0f, 1.0f);
        AssetManager::instance().set_music_volume(m_music_volume);
    }

    float master_volume() const { return m_master_volume; }
    float sfx_volume() const { return m_sfx_volume; }
    float music_volume() const { return m_music_volume; }

private:
    SoundSystem() = default;
    ~SoundSystem() = default;

    float m_master_volume = 0.8f;
    float m_sfx_volume = 0.8f;
    float m_music_volume = 0.7f;
};

} // namespace Vimana
