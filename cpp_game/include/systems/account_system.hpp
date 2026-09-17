#pragma once
#include <string>
#include <vector>
#include <functional>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <ctime>
#include <windows.h>
#include "json.hpp"
#include "core/types.hpp"
#include "systems/http_client.hpp"
#include "systems/currency_system.hpp"
#include "systems/db_system.hpp"

namespace Vimana {

enum class AuthState {
    LOGGED_OUT,
    LOGGING_IN,
    LOGGED_IN,
    GUEST
};

enum class CloudSyncStatus {
    IDLE,
    SYNCING,
    SYNCED,
    OFFLINE_LOCAL,
    ERROR_OCCURRED
};

struct UserInfo {
    std::string game_id      = "VMN-LOCAL";  // Overwritten by server on login/register
    std::string email        = "";
    std::string player_name  = "Warrior";
    bool        email_verified = false;
    std::vector<std::string> owned_ships;    // Cloud-synced ship roster
};

class AccountSystem {
public:
    static AccountSystem& instance() {
        static AccountSystem sys;
        return sys;
    }

    void init() {
        m_api_base = "http://127.0.0.1:5000";
        m_auth_state = AuthState::GUEST;
        m_sync_status = CloudSyncStatus::OFFLINE_LOCAL;
        m_sync_message = "Local mode (Guest)";

        // Read saved session token from save.json
        load_session_from_save();

        // If no stored game_id yet, generate a local VMN-XXXX-XXXX identifier
        if (m_user.game_id == "VMN-LOCAL" || m_user.game_id.empty()) {
            m_user.game_id = generate_guest_game_id();
            save_session_to_save();
        }

        // Wire ship unlock notification from CurrencySystem
        CurrencySystem::instance().set_on_ship_unlocked([this](const std::string& ship_id) {
            grant_ship(ship_id);
        });

        if (!m_auth_token.empty()) {
            std::cout << "[AccountSystem] Found saved session token. Attempting auto-login..." << std::endl;
            auto_login();
        } else {
            std::cout << "[AccountSystem] No saved session token. Starting in Guest mode." << std::endl;
        }
    }

    // Configuration
    void set_api_base(const std::string& url) { m_api_base = url; }
    const std::string& api_base() const { return m_api_base; }

    // State getters
    AuthState auth_state() const { return m_auth_state; }
    CloudSyncStatus sync_status() const { return m_sync_status; }
    const std::string& sync_message() const { return m_sync_message; }
    const UserInfo& user() const { return m_user; }
    const std::string& token() const { return m_auth_token; }
    bool is_logged_in() const { return m_auth_state == AuthState::LOGGED_IN; }
    bool is_guest() const { return m_auth_state == AuthState::GUEST; }

    // User data accessors
    const std::string& game_id() const { return m_user.game_id; }
    const std::string& email() const { return m_user.email; }
    const std::string& player_name() const { return m_user.player_name; }
    bool email_verified() const { return m_user.email_verified; }
    const std::vector<std::string>& owned_ships() const { return m_user.owned_ships; }

    bool owns_ship(const std::string& ship_id) const {
        return std::find(m_user.owned_ships.begin(), m_user.owned_ships.end(), ship_id) != m_user.owned_ships.end();
    }

    void grant_ship(const std::string& ship_id) {
        if (!owns_ship(ship_id)) {
            m_user.owned_ships.push_back(ship_id);
            if (is_logged_in()) {
                sync_profile(nullptr);
            }
        }
    }

    // ── Authentication API ───────────────────────────────────────────────────

    // Silent background auto-login with stored bearer token
    void auto_login(std::function<void(bool, const std::string&)> on_done = nullptr) {
        if (m_auth_token.empty()) {
            m_auth_state = AuthState::GUEST;
            if (on_done) on_done(false, "No saved token");
            return;
        }

        m_auth_state = AuthState::LOGGING_IN;
        m_sync_status = CloudSyncStatus::SYNCING;
        m_sync_message = "Connecting to Sangha Cloud...";

        std::string url = m_api_base + "/auth/me";
        HTTPClient::instance().get_async(url, m_auth_token, [this, on_done](HTTPClient::Response resp) {
            if (resp.success) {
                try {
                    auto j = nlohmann::json::parse(resp.body);
                    if (j.contains("user")) {
                        auto u = j["user"];
                        m_user.game_id = u.value("game_id", "VMN-7704");
                        m_user.email = u.value("email", "");
                        m_user.player_name = u.value("player_name", "Warrior");
                        m_user.email_verified = u.value("email_verified", false);

                        DBSystem::instance().set_player_name(m_user.player_name);
                        m_auth_state = AuthState::LOGGED_IN;
                        m_sync_status = CloudSyncStatus::SYNCED;
                        m_sync_message = "Connected as " + m_user.player_name;
                        std::cout << "[AccountSystem] Auto-login success: " << m_user.game_id << " (" << m_user.player_name << ")" << std::endl;

                        // Pull remote profile to sync high score, waves, and ships
                        pull_profile();

                        if (on_done) on_done(true, "Signed in as " + m_user.player_name);
                        return;
                    }
                } catch (...) {}
            }

            // If token invalid or server unavailable, fall back to guest
            std::cout << "[AccountSystem] Auto-login failed (code " << resp.status_code << "). Defaulting to Guest." << std::endl;
            m_auth_state = AuthState::GUEST;
            m_sync_status = CloudSyncStatus::OFFLINE_LOCAL;
            m_sync_message = "Local mode (Offline / Guest)";
            if (on_done) on_done(false, "Offline or session expired");
        });
    }

    // Login with Email & Password
    void login(const std::string& email, const std::string& password,
               std::function<void(bool success, const std::string& message)> callback) {
        m_auth_state = AuthState::LOGGING_IN;
        m_sync_status = CloudSyncStatus::SYNCING;
        m_sync_message = "Authenticating pilot credentials...";

        nlohmann::json payload;
        payload["email"] = email;
        payload["password"] = password;

        std::string url = m_api_base + "/auth/login";
        HTTPClient::instance().post_async(url, payload.dump(), "", [this, callback](HTTPClient::Response resp) {
            try {
                auto j = nlohmann::json::parse(resp.body);
                if (resp.success && j.value("success", false)) {
                    m_auth_token = j.value("token", "");
                    if (j.contains("user")) {
                        auto u = j["user"];
                        m_user.game_id = u.value("game_id", "VMN-7704");
                        m_user.email = u.value("email", "");
                        m_user.player_name = u.value("player_name", "Warrior");
                        m_user.email_verified = u.value("email_verified", false);
                        DBSystem::instance().set_player_name(m_user.player_name);
                    }

                    m_auth_state = AuthState::LOGGED_IN;
                    m_sync_status = CloudSyncStatus::SYNCED;
                    m_sync_message = "Online: " + m_user.player_name;

                    save_session_to_save();
                    pull_profile();

                    if (callback) callback(true, "Authentication successful. Welcome, " + m_user.player_name + "!");
                    return;
                } else {
                    std::string err = j.value("error", "Sign in failed. Check credentials.");
                    m_auth_state = AuthState::LOGGED_OUT;
                    m_sync_status = CloudSyncStatus::OFFLINE_LOCAL;
                    m_sync_message = err;
                    if (callback) callback(false, err);
                    return;
                }
            } catch (const std::exception& ex) {
                m_auth_state = AuthState::LOGGED_OUT;
                m_sync_status = CloudSyncStatus::ERROR_OCCURRED;
                std::string err = "Failed to reach server. Please try again.";
                if (callback) callback(false, err);
            }
        });
    }

    // Register a new Pilot Account
    void register_account(const std::string& email, const std::string& password, const std::string& player_name,
                          std::function<void(bool success, const std::string& message, bool needs_verify)> callback) {
        nlohmann::json payload;
        payload["email"] = email;
        payload["password"] = password;
        payload["player_name"] = player_name.empty() ? "Warrior" : player_name;

        std::string url = m_api_base + "/auth/register";
        HTTPClient::instance().post_async(url, payload.dump(), "", [this, player_name, callback](HTTPClient::Response resp) {
            try {
                auto j = nlohmann::json::parse(resp.body);
                if (resp.success && j.value("success", false)) {
                    bool needs_verify = j.value("verification_required", false);
                    m_auth_token = j.value("token", "");
                    if (j.contains("user")) {
                        auto u = j["user"];
                        m_user.game_id = u.value("game_id", "VMN-7704");
                        m_user.email = u.value("email", "");
                        m_user.player_name = u.value("player_name", player_name);
                        m_user.email_verified = u.value("email_verified", !needs_verify);
                        DBSystem::instance().set_player_name(m_user.player_name);
                    }

                    if (!m_auth_token.empty()) {
                        m_auth_state = AuthState::LOGGED_IN;
                        m_sync_status = CloudSyncStatus::SYNCED;
                        m_sync_message = "Registered as " + m_user.player_name;
                        save_session_to_save();
                        // Push initial local progress so user keeps offline high scores
                        sync_profile();
                    } else {
                        m_auth_state = AuthState::LOGGED_OUT;
                    }

                    std::string msg = needs_verify 
                        ? "Account created! Please verify your email with the token sent."
                        : "Account registered successfully! Welcome to the Sangha, Pilot.";
                    if (callback) callback(true, msg, needs_verify);
                    return;
                } else {
                    std::string err = j.value("error", "Registration rejected by server.");
                    if (err.find("already exists") != std::string::npos) {
                        err = "Email already registered! Tap '1. SIGN IN' tab to sign in.";
                    }
                    if (callback) callback(false, err, false);
                    return;
                }
            } catch (...) {
                std::string fallback_err = resp.body.empty() 
                    ? "Cannot reach server. Ensure backend is running."
                    : "Registration failed: " + resp.body;
                if (callback) callback(false, fallback_err, false);
            }
        });
    }

    // Verify Email with 1-Time Token
    void verify_email(const std::string& token, std::function<void(bool success, const std::string& message)> callback) {
        nlohmann::json payload;
        payload["token"] = token;

        std::string url = m_api_base + "/auth/verify-email";
        HTTPClient::instance().post_async(url, payload.dump(), "", [this, callback](HTTPClient::Response resp) {
            try {
                auto j = nlohmann::json::parse(resp.body);
                if (resp.success && j.value("success", false)) {
                    m_auth_token = j.value("token", m_auth_token);
                    m_user.email_verified = true;
                    m_auth_state = AuthState::LOGGED_IN;
                    save_session_to_save();
                    if (callback) callback(true, "Email successfully verified! Pilot license active.");
                } else {
                    std::string err = j.value("error", "Invalid or expired verification token.");
                    if (callback) callback(false, err);
                }
            } catch (...) {
                if (callback) callback(false, "Network error while verifying token.");
            }
        });
    }

    // Password Reset Request
    void request_password_reset(const std::string& email, std::function<void(bool success, const std::string& message)> callback) {
        nlohmann::json payload;
        payload["email"] = email;

        std::string url = m_api_base + "/auth/request-password-reset";
        HTTPClient::instance().post_async(url, payload.dump(), "", [callback](HTTPClient::Response resp) {
            try {
                auto j = nlohmann::json::parse(resp.body);
                std::string msg = j.value("message", "If that email exists, reset instructions have been generated.");
                if (j.contains("reset_token")) {
                    msg += " [DEV TOKEN: " + j["reset_token"].get<std::string>() + "]";
                }
                if (callback) callback(true, msg);
            } catch (...) {
                if (callback) callback(false, "Failed to connect to reset service.");
            }
        });
    }

    // Reset Password with Token
    void reset_password(const std::string& token, const std::string& new_password,
                        std::function<void(bool success, const std::string& message)> callback) {
        nlohmann::json payload;
        payload["token"] = token;
        payload["password"] = new_password;

        std::string url = m_api_base + "/auth/reset-password";
        HTTPClient::instance().post_async(url, payload.dump(), "", [callback](HTTPClient::Response resp) {
            try {
                auto j = nlohmann::json::parse(resp.body);
                if (resp.success && j.value("success", false)) {
                    if (callback) callback(true, "Password updated successfully! Please sign in.");
                } else {
                    std::string err = j.value("error", "Password reset failed. Check token.");
                    if (callback) callback(false, err);
                }
            } catch (...) {
                if (callback) callback(false, "Network error updating password.");
            }
        });
    }

    // Logout
    void logout(std::function<void()> callback = nullptr) {
        if (!m_auth_token.empty()) {
            std::string url = m_api_base + "/auth/logout";
            HTTPClient::instance().post_async(url, "{}", m_auth_token, nullptr);
        }

        m_auth_token = "";
        m_user = UserInfo();
        m_user.game_id = "VMN-LOCAL";
        m_user.player_name = DBSystem::instance().player_name();
        m_auth_state = AuthState::GUEST;
        m_sync_status = CloudSyncStatus::OFFLINE_LOCAL;
        m_sync_message = "Offline (Guest)";

        save_session_to_save();
        if (callback) callback();
    }

    // Play in Guest / Offline mode
    void play_as_guest() {
        m_auth_state = AuthState::GUEST;
        m_sync_status = CloudSyncStatus::OFFLINE_LOCAL;
        m_sync_message = "Local mode (Guest)";
    }

    // ── Profile & Cloud Progression Sync ─────────────────────────────────────

    // Pull progression from server and merge with local
    void pull_profile(std::function<void(bool success, const std::string& msg)> callback = nullptr) {
        if (m_auth_token.empty() || m_auth_state != AuthState::LOGGED_IN) {
            if (callback) callback(false, "Not authenticated");
            return;
        }

        std::string url = m_api_base + "/account/profile";
        HTTPClient::instance().get_async(url, m_auth_token, [this, callback](HTTPClient::Response resp) {
            if (resp.success) {
                try {
                    auto j = nlohmann::json::parse(resp.body);
                    if (j.contains("profile")) {
                        auto prof = j["profile"];
                        int cloud_high = prof.value("high_score", 0);
                        int cloud_wave = prof.value("last_wave", 1);
                        int local_high = DBSystem::instance().high_score();
                        int local_wave = DBSystem::instance().max_wave();

                        // Take the maximum of local and cloud
                        if (cloud_high > local_high) DBSystem::instance().update_high_score(cloud_high);
                        if (cloud_wave > local_wave) DBSystem::instance().update_max_wave(cloud_wave);

                        if (prof.contains("ships_mastered") && prof["ships_mastered"].is_array()) {
                            m_user.owned_ships.clear();
                            for (auto& s : prof["ships_mastered"]) {
                                std::string ship_id = s.get<std::string>();
                                m_user.owned_ships.push_back(ship_id);
                                CurrencySystem::instance().unlock_ship(ship_id);
                            }
                        }

                        DBSystem::instance().save_game();
                        m_sync_status = CloudSyncStatus::SYNCED;
                        m_sync_message = "Progression synchronized with cloud";
                        std::cout << "[AccountSystem] Cloud profile merged successfully." << std::endl;
                        if (callback) callback(true, "Cloud profile updated");
                        return;
                    }
                } catch (...) {}
            }

            m_sync_status = CloudSyncStatus::OFFLINE_LOCAL;
            if (callback) callback(false, "Could not fetch cloud profile");
        });
    }

    // Push local progression to server with maximum merge
    void sync_profile(std::function<void(bool success, const std::string& msg)> callback = nullptr) {
        if (m_auth_token.empty() || m_auth_state != AuthState::LOGGED_IN) {
            if (callback) callback(false, "Not authenticated");
            return;
        }

        m_sync_status = CloudSyncStatus::SYNCING;
        m_sync_message = "Backing up progress to cloud...";

        // Union local unlocked ships with user owned ships
        auto all_unlocked = CurrencySystem::instance().unlocked_ships();
        for (const auto& s : m_user.owned_ships) {
            if (std::find(all_unlocked.begin(), all_unlocked.end(), s) == all_unlocked.end()) {
                all_unlocked.push_back(s);
            }
        }

        nlohmann::json prof;
        prof["player_name"] = DBSystem::instance().player_name();
        prof["high_score"] = DBSystem::instance().high_score();
        prof["last_wave"] = DBSystem::instance().max_wave();
        prof["ships_mastered"] = all_unlocked;

        nlohmann::json root;
        root["profile"] = prof;

        std::string url = m_api_base + "/account/profile";
        HTTPClient::instance().put_async(url, root.dump(), m_auth_token, [this, callback](HTTPClient::Response resp) {
            if (resp.success) {
                m_sync_status = CloudSyncStatus::SYNCED;
                m_sync_message = "Progress safely backed up to cloud";
                std::cout << "[AccountSystem] Cloud backup succeeded." << std::endl;
                if (callback) callback(true, "Cloud sync complete");
            } else {
                m_sync_status = CloudSyncStatus::ERROR_OCCURRED;
                m_sync_message = "Cloud sync failed";
                if (callback) callback(false, "Failed to sync to cloud");
            }
        });
    }

    // ── Online Leaderboard & Score Submission ────────────────────────────────

    void submit_score(int score, int wave, int kills, int damage, float duration_seconds,
                      const std::string& difficulty, const std::string& ship_class,
                      std::function<void(bool success, const std::string& msg)> callback = nullptr) {
        nlohmann::json payload;
        payload["player_name"] = DBSystem::instance().player_name();
        payload["score"] = score;
        payload["level_reached"] = std::max(1, wave);
        payload["kills"] = kills;
        payload["total_damage"] = damage;
        payload["duration_seconds"] = duration_seconds;
        payload["difficulty"] = difficulty.empty() ? "normal" : difficulty;
        payload["ship_class"] = ship_class.empty() ? "pushpaka" : ship_class;

        std::string url = m_api_base + "/scores";
        HTTPClient::instance().post_async(url, payload.dump(), m_auth_token, [callback](HTTPClient::Response resp) {
            if (resp.success) {
                std::cout << "[AccountSystem] Score submitted successfully to online leaderboard." << std::endl;
                if (callback) callback(true, "Score posted to Hall of Valor!");
            } else {
                std::cout << "[AccountSystem] Score submission failed: " << resp.body << std::endl;
                if (callback) callback(false, "Could not submit score to online server");
            }
        });
    }

    void fetch_top_scores(int limit, const std::string& difficulty,
                          std::function<void(bool success, const std::vector<ScoreEntry>& entries)> callback) {
        std::string url = m_api_base + "/scores/top?limit=" + std::to_string(limit);
        if (!difficulty.empty() && difficulty != "all") {
            url += "&difficulty=" + difficulty;
        }

        HTTPClient::instance().get_async(url, "", [callback](HTTPClient::Response resp) {
            std::vector<ScoreEntry> entries;
            if (resp.success) {
                try {
                    auto j = nlohmann::json::parse(resp.body);
                    if (j.contains("leaderboard") && j["leaderboard"].is_array()) {
                        for (const auto& item : j["leaderboard"]) {
                            ScoreEntry e;
                            e.id = item.value("rank", 0);
                            e.player_name = item.value("player_name", "Anonymous");
                            e.score = item.value("score", 0);
                            e.level_reached = item.value("level_reached", 1);
                            e.difficulty = item.value("difficulty", "normal");
                            e.ship_class = item.value("ship_class", "pushpaka");
                            e.kills = 0;
                            e.total_damage = 0;
                            e.created_at = item.value("created_at", "");
                            entries.push_back(e);
                        }
                    }
                    if (callback) callback(true, entries);
                    return;
                } catch (...) {}
            }
            if (callback) callback(false, entries);
        });
    }

    // ── Online Multiplayer Lobby Management ──────────────────────────────────

    void fetch_lobbies(std::function<void(bool success, const std::vector<nlohmann::json>& lobbies)> callback) {
        std::string url = m_api_base + "/multiplayer/lobbies";
        HTTPClient::instance().get_async(url, "", [callback](HTTPClient::Response resp) {
            std::vector<nlohmann::json> lobbies;
            if (resp.success) {
                try {
                    auto j = nlohmann::json::parse(resp.body);
                    if (j.contains("lobbies") && j["lobbies"].is_array()) {
                        for (const auto& item : j["lobbies"]) {
                            lobbies.push_back(item);
                        }
                    }
                    if (callback) callback(true, lobbies);
                    return;
                } catch (...) {}
            }
            if (callback) callback(false, lobbies);
        });
    }

    void create_lobby(const std::string& mode, int max_players, const std::string& ship_class,
                      std::function<void(bool success, const std::string& code, const std::string& msg)> callback) {
        if (m_auth_token.empty() || m_auth_state != AuthState::LOGGED_IN) {
            if (callback) callback(false, "", "Sign in to an online pilot account to host cloud lobbies");
            return;
        }

        nlohmann::json payload;
        payload["mode"] = mode.empty() ? "campaign" : mode;
        payload["max_players"] = std::clamp(max_players, 2, 4);
        payload["ship_class"] = ship_class.empty() ? "pushpaka" : ship_class;

        std::string url = m_api_base + "/multiplayer/lobbies";
        HTTPClient::instance().post_async(url, payload.dump(), m_auth_token, [callback](HTTPClient::Response resp) {
            if (resp.success) {
                try {
                    auto j = nlohmann::json::parse(resp.body);
                    if (j.contains("lobby")) {
                        std::string code = j["lobby"].value("code", "");
                        if (callback) callback(true, code, "Lobby created!");
                        return;
                    }
                } catch (...) {}
            }
            if (callback) callback(false, "", "Server rejected lobby creation");
        });
    }

    // ── GDPR Account Deletion ────────────────────────────────────────────────
    void delete_account(std::function<void(bool success, const std::string& msg)> callback) {
        // Logout & wipe local session
        logout();
        if (callback) callback(true, "Pilot credentials wiped from this station.");
    }

    // ── Update loop (call in main.cpp once per frame) ────────────────────────
    void update() {
        HTTPClient::instance().update();
    }

private:
    AccountSystem()
        : m_api_base("http://127.0.0.1:5000"),
          m_auth_state(AuthState::GUEST),
          m_sync_status(CloudSyncStatus::OFFLINE_LOCAL),
          m_sync_message("Local mode (Guest)") {}
    ~AccountSystem() = default;

    // Generate a local VMN-XXXX-XXXX Game ID for offline/guest pilots
    std::string generate_guest_game_id() {
        // Seed with time + hash of USERPROFILE env to get a stable-ish unique ID
        const char* up = std::getenv("USERPROFILE");
        size_t seed = std::hash<std::string>{}(up ? up : "guest");
        seed ^= static_cast<size_t>(std::time(nullptr));
        seed ^= static_cast<size_t>(GetCurrentProcessId());
        const char* hex = "0123456789ABCDEF";
        std::string a, b;
        for (int i = 0; i < 4; ++i) { a += hex[(seed >> (i * 4)) & 0xF]; }
        seed = seed * 6364136223846793005ULL + 1442695040888963407ULL;
        for (int i = 0; i < 4; ++i) { b += hex[(seed >> (i * 4)) & 0xF]; }
        return "VMN-" + a + "-" + b;
    }

    std::string get_save_path() const {
        const char* userprofile = std::getenv("USERPROFILE");
        if (!userprofile) return "";
        return std::string(userprofile) + "/.vimana_wars/save.json";
    }

    void load_session_from_save() {
        std::string path = get_save_path();
        if (path.empty() || !std::filesystem::exists(path)) return;

        try {
            std::ifstream f(path);
            nlohmann::json j;
            f >> j;

            m_auth_token = j.value("auth_token", "");
            m_user.game_id = j.value("auth_game_id", "VMN-LOCAL");
            m_user.email = j.value("auth_email", "");
            m_user.player_name = j.value("player_name", "Warrior");
            m_user.email_verified = j.value("auth_verified", false);
        } catch (...) {}
    }

    void save_session_to_save() {
        std::string path = get_save_path();
        if (path.empty()) return;

        try {
            nlohmann::json j;
            if (std::filesystem::exists(path)) {
                std::ifstream fi(path);
                fi >> j;
            }

            j["version"] = 3;
            j["auth_token"] = m_auth_token;
            j["auth_game_id"] = m_user.game_id;
            j["auth_email"] = m_user.email;
            j["auth_verified"] = m_user.email_verified;

            std::ofstream fo(path);
            fo << j.dump(2);
        } catch (...) {}
    }

    std::string m_api_base;
    std::string m_auth_token;
    UserInfo m_user;
    AuthState m_auth_state;
    CloudSyncStatus m_sync_status;
    std::string m_sync_message;
};

} // namespace Vimana
