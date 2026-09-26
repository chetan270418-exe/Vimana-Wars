#pragma once
#include <string>
#include <unordered_map>
#include <iostream>
#include <filesystem>
#include <vector>
#include "raylib.h"

namespace Vimana {

class AssetManager {
public:
    static AssetManager& instance() {
        static AssetManager mgr;
        return mgr;
    }

    void init() {
        // Resolve from the executable as well as the working directory. The
        // latter changes between IDE, bin/, packaged, and double-click runs.
        std::vector<std::filesystem::path> candidates = {
            std::filesystem::path("assets"),
            std::filesystem::path("../assets"),
            std::filesystem::path("../../assets")
        };
        std::filesystem::path app_dir = std::filesystem::path(GetApplicationDirectory());
        candidates.push_back(app_dir / "assets");
        candidates.push_back(app_dir / ".." / "assets");
        candidates.push_back(app_dir / ".." / ".." / "assets");

        for (const auto& candidate : candidates) {
            std::error_code ec;
            if (std::filesystem::is_directory(candidate, ec)) {
                m_base_path = std::filesystem::weakly_canonical(candidate, ec).string();
                if (m_base_path.empty()) m_base_path = candidate.lexically_normal().string();
                break;
            }
        }
        std::cout << "[AssetManager] Resolved assets base path: " << m_base_path << std::endl;

        // Preload fonts — load at LARGE raster sizes so downscaling is crisp.
// (Loading at 36 and drawing at 9-12 makes everything blurry at 900x600.)
        std::string title_font_path = m_base_path + "/fonts/Cinzel-Bold.ttf";
        if (std::filesystem::exists(title_font_path)) {
            m_main_font = LoadFontEx(title_font_path.c_str(), 96, nullptr, 0);
            SetTextureFilter(m_main_font.texture, TEXTURE_FILTER_BILINEAR);
            std::cout << "[AssetManager] Loaded Title Font: " << title_font_path << std::endl;
        } else {
            m_main_font = GetFontDefault();
        }

        std::string body_font_path = m_base_path + "/fonts/SpaceGrotesk-Bold.ttf";
        if (std::filesystem::exists(body_font_path)) {
            m_body_font = LoadFontEx(body_font_path.c_str(), 64, nullptr, 0);
            SetTextureFilter(m_body_font.texture, TEXTURE_FILTER_BILINEAR);
            std::cout << "[AssetManager] Loaded Body Font: " << body_font_path << std::endl;
        } else {
            m_body_font = m_main_font;
        }

        std::string mono_font_path = m_base_path + "/fonts/JetBrainsMono-Bold.ttf";
        if (std::filesystem::exists(mono_font_path)) {
            m_mono_font = LoadFontEx(mono_font_path.c_str(), 48, nullptr, 0);
            SetTextureFilter(m_mono_font.texture, TEXTURE_FILTER_BILINEAR);
            std::cout << "[AssetManager] Loaded Mono Font: " << mono_font_path << std::endl;
        } else {
            m_mono_font = m_body_font;
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
        m_music_file.clear();
        if (m_main_font.texture.id != GetFontDefault().texture.id) {
            UnloadFont(m_main_font);
        }
        if (m_body_font.texture.id != GetFontDefault().texture.id && m_body_font.texture.id != m_main_font.texture.id) {
            UnloadFont(m_body_font);
        }
        if (m_mono_font.texture.id != GetFontDefault().texture.id && m_mono_font.texture.id != m_body_font.texture.id && m_mono_font.texture.id != m_main_font.texture.id) {
            UnloadFont(m_mono_font);
        }
    }

    Texture2D get_texture(const std::string& filename) {
        if (m_textures.find(filename) != m_textures.end()) {
            return m_textures[filename];
        }

        // Search in priority directories
        std::vector<std::string> search_dirs = {
            m_base_path + "/images/",
            m_base_path + "/images/ships/",
            m_base_path + "/images/bosses/",
            m_base_path + "/images/realms/",
            m_base_path + "/ui/",
            m_base_path + "/ui/icons/",
            m_base_path + "/vfx/",
            m_base_path + "/online/phase8_sources/kenney_simple_space_2d/PNG/Default/",
            m_base_path + "/online/phase8_sources/kenney_simple_space_2d/PNG/Retina/",
            m_base_path + "/online/phase9_sources/space_ships_pack3_2d/",
            m_base_path + "/online/kenney_space_shooter_extension/PNG/",
            m_base_path + "/"
        };

        for (const auto& dir : search_dirs) {
            std::string full_path = dir + filename;
            if (std::filesystem::exists(full_path)) {
                Texture2D tex = LoadTexture(full_path.c_str());
                SetTextureFilter(tex, TEXTURE_FILTER_BILINEAR);
                m_textures[filename] = tex;
                return tex;
            }
        }

        // Return empty dummy texture if not found
        Texture2D empty = { 0 };
        return empty;
    }

    Sound get_sound(const std::string& filename) {
        if (m_sounds.find(filename) != m_sounds.end()) {
            return m_sounds[filename];
        }

        std::vector<std::string> search_dirs = {
            m_base_path + "/sounds/",
            m_base_path + "/online/kenney_sci-fi_sounds/Audio/",
            m_base_path + "/online/phase8_sources/kenney_sci_fi_sounds_2/Audio/",
            m_base_path + "/"
        };

        for (const auto& dir : search_dirs) {
            std::string full_path = dir + filename;
            if (std::filesystem::exists(full_path)) {
                Sound snd = LoadSound(full_path.c_str());
                m_sounds[filename] = snd;
                return snd;
            }
        }

        Sound empty = { 0 };
        return empty;
    }

    void load_music(const std::string& filename) {
        if (m_music.stream.buffer != nullptr && m_music_file == filename) return;
        std::string full_path = m_base_path + "/sounds/" + filename;
        if (!std::filesystem::exists(full_path)) {
            full_path = m_base_path + "/" + filename;
        }
        if (std::filesystem::exists(full_path)) {
            if (m_music.stream.buffer != nullptr) {
                UnloadMusicStream(m_music);
            }
            m_music = LoadMusicStream(full_path.c_str());
            m_music.looping = true;
            if (m_music.stream.buffer != nullptr) {
                m_music_file = filename;
                PlayMusicStream(m_music);
            }
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
    Font title_font() const { return m_main_font; }
    Font body_font() const { return m_body_font; }
    Font mono_font() const { return m_mono_font; }
    const std::string& base_path() const { return m_base_path; }

private:
    AssetManager() = default;
    ~AssetManager() = default;

    std::string m_base_path = "assets";
    Font m_main_font = { 0 };
    Font m_body_font = { 0 };
    Font m_mono_font = { 0 };
    Music m_music = { 0 };
    std::string m_music_file;
    std::unordered_map<std::string, Texture2D> m_textures;
    std::unordered_map<std::string, Sound> m_sounds;
};

} // namespace Vimana
