#pragma once
#include <string>
#include <unordered_map>
#include <iostream>
#include <filesystem>
#include <vector>
#include <unordered_set>
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

        bool found_assets = false;
        for (const auto& candidate : candidates) {
            std::error_code ec;
            if (std::filesystem::is_directory(candidate, ec)) {
                m_base_path = std::filesystem::weakly_canonical(candidate, ec).string();
                if (m_base_path.empty()) m_base_path = candidate.lexically_normal().string();
                found_assets = true;
                break;
            }
        }
        std::cout << "[AssetManager] Resolved assets base path: " << m_base_path << std::endl;
        if (!found_assets) report_asset_problem("asset directory", m_base_path);

        // Preload fonts — load at LARGE raster sizes so downscaling is crisp.
// (Loading at 36 and drawing at 9-12 makes everything blurry at 900x600.)
        std::string title_font_path = m_base_path + "/fonts/Cinzel-Bold.ttf";
        if (std::filesystem::exists(title_font_path)) {
            m_main_font = LoadFontEx(title_font_path.c_str(), 96, nullptr, 0);
            SetTextureFilter(m_main_font.texture, TEXTURE_FILTER_BILINEAR);
            std::cout << "[AssetManager] Loaded Title Font: " << title_font_path << std::endl;
        } else {
            report_asset_problem("missing font", title_font_path);
            m_main_font = GetFontDefault();
        }

        std::string body_font_path = m_base_path + "/fonts/SpaceGrotesk-Bold.ttf";
        if (std::filesystem::exists(body_font_path)) {
            m_body_font = LoadFontEx(body_font_path.c_str(), 64, nullptr, 0);
            SetTextureFilter(m_body_font.texture, TEXTURE_FILTER_BILINEAR);
            std::cout << "[AssetManager] Loaded Body Font: " << body_font_path << std::endl;
        } else {
            report_asset_problem("missing font", body_font_path);
            m_body_font = m_main_font;
        }

        std::string mono_font_path = m_base_path + "/fonts/JetBrainsMono-Bold.ttf";
        if (std::filesystem::exists(mono_font_path)) {
            m_mono_font = LoadFontEx(mono_font_path.c_str(), 48, nullptr, 0);
            SetTextureFilter(m_mono_font.texture, TEXTURE_FILTER_BILINEAR);
            std::cout << "[AssetManager] Loaded Mono Font: " << mono_font_path << std::endl;
        } else {
            report_asset_problem("missing font", mono_font_path);
            m_mono_font = m_body_font;
        }
    }

    void cleanup() {
        for (auto& [key, tex] : m_textures) {
            if (tex.id > 0) UnloadTexture(tex);
        }
        m_textures.clear();

        for (auto& [key, snd] : m_sounds) {
            if (snd.stream.buffer != nullptr) UnloadSound(snd);
        }
        m_sounds.clear();

        if (m_music.stream.buffer != nullptr) {
            UnloadMusicStream(m_music);
        }
        if (m_ambience.stream.buffer != nullptr) UnloadMusicStream(m_ambience);
        m_music_file.clear();
        m_ambience_file.clear();
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
                if (tex.id == 0) {
                    report_asset_problem("texture load", full_path);
                    m_textures[filename] = { 0 };
                    return { 0 };
                }
                SetTextureFilter(tex, TEXTURE_FILTER_BILINEAR);
                m_textures[filename] = tex;
                return tex;
            }
        }

        report_asset_problem("missing texture", filename);
        m_textures[filename] = { 0 };
        return { 0 };
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
                if (snd.stream.buffer == nullptr) {
                    report_asset_problem("sound load", full_path);
                    m_sounds[filename] = { 0 };
                    return { 0 };
                }
                m_sounds[filename] = snd;
                return snd;
            }
        }

        report_asset_problem("missing sound", filename);
        m_sounds[filename] = { 0 };
        return { 0 };
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
            } else {
                report_asset_problem("music load", full_path);
            }
        } else {
            report_asset_problem("missing music", filename);
        }
    }

    void load_ambience(const std::string& filename) {
        if (m_ambience.stream.buffer != nullptr && m_ambience_file == filename) return;
        std::string full_path = m_base_path + "/sounds/" + filename;
        if (!std::filesystem::exists(full_path)) {
            report_asset_problem("missing ambience", filename);
            return;
        }
        if (m_ambience.stream.buffer != nullptr) UnloadMusicStream(m_ambience);
        m_ambience = LoadMusicStream(full_path.c_str());
        m_ambience.looping = true;
        if (m_ambience.stream.buffer != nullptr) {
            m_ambience_file = filename;
            PlayMusicStream(m_ambience);
        } else {
            report_asset_problem("ambience load", full_path);
        }
    }

    void update_music() {
        if (m_music.stream.buffer != nullptr) {
            UpdateMusicStream(m_music);
        }
        if (m_ambience.stream.buffer != nullptr) UpdateMusicStream(m_ambience);
    }

    void set_music_volume(float vol) {
        if (m_music.stream.buffer != nullptr) {
            SetMusicVolume(m_music, vol);
        }
    }

    void set_ambience_volume(float vol) {
        if (m_ambience.stream.buffer != nullptr) SetMusicVolume(m_ambience, vol);
    }

    Font font() const { return m_main_font; }
    Font title_font() const { return m_main_font; }
    Font body_font() const { return m_body_font; }
    Font mono_font() const { return m_mono_font; }
    const std::string& base_path() const { return m_base_path; }

private:
    void report_asset_problem(const std::string& kind, const std::string& path) {
        const std::string key = kind + ": " + path;
        if (m_reported_asset_problems.insert(key).second) {
            std::cerr << "[AssetManager] " << key << std::endl;
        }
    }

    AssetManager() = default;
    ~AssetManager() = default;

    std::string m_base_path = "assets";
    Font m_main_font = { 0 };
    Font m_body_font = { 0 };
    Font m_mono_font = { 0 };
    Music m_music = { 0 };
    Music m_ambience = { 0 };
    std::string m_music_file;
    std::string m_ambience_file;
    std::unordered_set<std::string> m_reported_asset_problems;
    std::unordered_map<std::string, Texture2D> m_textures;
    std::unordered_map<std::string, Sound> m_sounds;
};

} // namespace Vimana
