#pragma once
#include <string>
#include <unordered_map>
#include <iostream>
#include <filesystem>
#include "raylib.h"

namespace Vimana {

class AssetManager {
public:
    static AssetManager& instance() {
        static AssetManager mgr;
        return mgr;
    }

    void init() {
        // Look for assets in common relative locations
        m_base_path = "assets";
        if (!std::filesystem::exists(m_base_path)) {
            if (std::filesystem::exists("../assets")) {
                m_base_path = "../assets";
            } else if (std::filesystem::exists("../../assets")) {
                m_base_path = "../../assets";
            }
        }
        std::cout << "[AssetManager] Resolved assets base path: " << m_base_path << std::endl;

        // Preload default font if available
        std::string font_path = m_base_path + "/fonts/Cinzel-SemiBold.ttf";
        if (std::filesystem::exists(font_path)) {
            m_main_font = LoadFontEx(font_path.c_str(), 32, nullptr, 0);
            SetTextureFilter(m_main_font.texture, TEXTURE_FILTER_BILINEAR);
        } else {
            m_main_font = GetFontDefault();
        }
    }

    void cleanup() {
        for (auto& [key, tex] : m_textures) {
            UnloadTexture(tex);
        }
        m_textures.clear();

        for (auto& [key, snd] : m_sounds) {
            UnloadSound(snd);
        }
        m_sounds.clear();

        if (m_music.stream.buffer != nullptr) {
            UnloadMusicStream(m_music);
        }
        if (m_main_font.texture.id != GetFontDefault().texture.id) {
            UnloadFont(m_main_font);
        }
    }

    Texture2D get_texture(const std::string& filename) {
        if (m_textures.find(filename) != m_textures.end()) {
            return m_textures[filename];
        }

        std::string full_path = m_base_path + "/images/" + filename;
        if (std::filesystem::exists(full_path)) {
            Texture2D tex = LoadTexture(full_path.c_str());
            SetTextureFilter(tex, TEXTURE_FILTER_BILINEAR);
            m_textures[filename] = tex;
            return tex;
        }

        // Return empty dummy texture if not found
        Texture2D empty = { 0 };
        return empty;
    }

    Sound get_sound(const std::string& filename) {
        if (m_sounds.find(filename) != m_sounds.end()) {
            return m_sounds[filename];
        }

        std::string full_path = m_base_path + "/sounds/" + filename;
        if (std::filesystem::exists(full_path)) {
            Sound snd = LoadSound(full_path.c_str());
            m_sounds[filename] = snd;
            return snd;
        }

        Sound empty = { 0 };
        return empty;
    }

    void load_music(const std::string& filename) {
        std::string full_path = m_base_path + "/sounds/" + filename;
        if (std::filesystem::exists(full_path)) {
            if (m_music.stream.buffer != nullptr) {
                UnloadMusicStream(m_music);
            }
            m_music = LoadMusicStream(full_path.c_str());
            m_music.looping = true;
            PlayMusicStream(m_music);
        }
    }

    void update_music() {
        if (m_music.stream.buffer != nullptr) {
            UpdateMusicStream(m_music);
        }
    }

    void set_music_volume(float vol) {
        if (m_music.stream.buffer != nullptr) {
            SetMusicVolume(m_music, vol);
        }
    }

    Font font() const { return m_main_font; }
    const std::string& base_path() const { return m_base_path; }

private:
    AssetManager() = default;
    ~AssetManager() = default;

    std::string m_base_path = "assets";
    Font m_main_font = { 0 };
    Music m_music = { 0 };
    std::unordered_map<std::string, Texture2D> m_textures;
    std::unordered_map<std::string, Sound> m_sounds;
};

} // namespace Vimana
