#pragma once
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <filesystem>
#include "sqlite3.h"
#include "json.hpp"
#include "core/types.hpp"
#include "systems/currency_system.hpp"

namespace Vimana {

class DBSystem {
public:
    static DBSystem& instance() {
        static DBSystem sys;
        return sys;
    }

    void init() {
        // Resolve database path
        std::string db_file = "leaderboard.db";
        if (!std::filesystem::exists(db_file)) {
            if (std::filesystem::exists("../leaderboard.db")) {
                db_file = "../leaderboard.db";
            }
        }

        int rc = sqlite3_open(db_file.c_str(), &m_db);
        if (rc != SQLITE_OK) {
            std::cerr << "[DBSystem] Cannot open database: " << sqlite3_errmsg(m_db) << std::endl;
            m_db = nullptr;
        } else {
            std::cout << "[DBSystem] Opened database successfully: " << db_file << std::endl;
            ensure_tables();
        }

        load_save_game();
    }

    void cleanup() {
        save_game();
        if (m_db) {
            sqlite3_close(m_db);
            m_db = nullptr;
        }
    }

    std::vector<ScoreEntry> fetch_top_scores(int limit = 10) {
        std::vector<ScoreEntry> entries;
        if (!m_db) return entries;

        const char* sql = "SELECT id, player_name, score, level_reached, difficulty, ship_class, kills, total_damage, created_at "
                          "FROM scores ORDER BY score DESC LIMIT ?;";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(m_db, sql, -1, &stmt, nullptr) == SQLITE_OK) {
            sqlite3_bind_int(stmt, 1, limit);
            while (sqlite3_step(stmt) == SQLITE_ROW) {
                ScoreEntry e;
                e.id = sqlite3_column_int(stmt, 0);
                e.player_name = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));
                e.score = sqlite3_column_int(stmt, 2);
                e.level_reached = sqlite3_column_int(stmt, 3);
                e.difficulty = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 4));
                e.ship_class = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
                e.kills = sqlite3_column_int(stmt, 6);
                e.total_damage = sqlite3_column_int(stmt, 7);
                e.created_at = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 8));
                entries.push_back(e);
            }
            sqlite3_finalize(stmt);
        }
        return entries;
    }

    bool insert_score(const ScoreEntry& e) {
        if (!m_db) return false;
        const char* sql = "INSERT INTO scores (player_name, score, level_reached, difficulty, ship_class, kills, total_damage, duration_seconds) "
                          "VALUES (?, ?, ?, ?, ?, ?, ?, ?);";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(m_db, sql, -1, &stmt, nullptr) == SQLITE_OK) {
            sqlite3_bind_text(stmt, 1, e.player_name.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(stmt, 2, e.score);
            sqlite3_bind_int(stmt, 3, e.level_reached);
            sqlite3_bind_text(stmt, 4, e.difficulty.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_text(stmt, 5, e.ship_class.c_str(), -1, SQLITE_TRANSIENT);
            sqlite3_bind_int(stmt, 6, e.kills);
            sqlite3_bind_int(stmt, 7, e.total_damage);
            sqlite3_bind_double(stmt, 8, e.duration_seconds);

            int rc = sqlite3_step(stmt);
            sqlite3_finalize(stmt);
            return (rc == SQLITE_DONE);
        }
        return false;
    }

    void load_save_game() {
        std::string home_dir = "";
        const char* userprofile = std::getenv("USERPROFILE");
        if (userprofile) home_dir = userprofile;
        if (home_dir.empty()) return;

        std::string save_dir = home_dir + "/.vimana_wars";
        std::string save_path = save_dir + "/save.json";
        if (!std::filesystem::exists(save_path)) return;

        try {
            std::ifstream f(save_path);
            nlohmann::json j;
            f >> j;

            m_player_name = j.value("player_name", "Warrior");
            m_high_score = j.value("high_score", 0);
            m_max_wave = j.value("last_wave", 1);
            int shards = j.value("prana_shards", 200);
            CurrencySystem::instance().set_prana_shards(shards);

            if (j.contains("unlocked_ships") && j["unlocked_ships"].is_array()) {
                std::vector<std::string> ships;
                for (auto& s : j["unlocked_ships"]) ships.push_back(s.get<std::string>());
                CurrencySystem::instance().set_unlocked_ships(ships);
            }
            std::cout << "[DBSystem] Loaded savegame: " << m_player_name << " HighScore: " << m_high_score << std::endl;
        } catch (const std::exception& ex) {
            std::cerr << "[DBSystem] Error loading save.json: " << ex.what() << std::endl;
        }
    }

    void save_game() {
        std::string home_dir = "";
        const char* userprofile = std::getenv("USERPROFILE");
        if (userprofile) home_dir = userprofile;
        if (home_dir.empty()) return;

        std::string save_dir = home_dir + "/.vimana_wars";
        std::filesystem::create_directories(save_dir);
        std::string save_path = save_dir + "/save.json";

        try {
            nlohmann::json j;
            j["player_name"] = m_player_name;
            j["high_score"] = m_high_score;
            j["last_wave"] = m_max_wave;
            j["prana_shards"] = CurrencySystem::instance().prana_shards();
            j["unlocked_ships"] = CurrencySystem::instance().unlocked_ships();

            std::ofstream f(save_path);
            f << j.dump(2);
        } catch (const std::exception& ex) {
            std::cerr << "[DBSystem] Error saving save.json: " << ex.what() << std::endl;
        }
    }

    const std::string& player_name() const { return m_player_name; }
    void set_player_name(const std::string& name) { m_player_name = name; }
    int high_score() const { return m_high_score; }
    void update_high_score(int score) { if (score > m_high_score) m_high_score = score; }
    int max_wave() const { return m_max_wave; }
    void update_max_wave(int wave) { if (wave > m_max_wave) m_max_wave = wave; }

    std::vector<MatchRecord> fetch_match_history(int limit = 10) {
        std::vector<MatchRecord> records;
        if (!m_db) return records;

        const char* sql = "SELECT level_reached, score, kills, total_damage, duration_seconds, ship_class, created_at "
                          "FROM scores ORDER BY id DESC LIMIT ?;";
        sqlite3_stmt* stmt = nullptr;
        if (sqlite3_prepare_v2(m_db, sql, -1, &stmt, nullptr) == SQLITE_OK) {
            sqlite3_bind_int(stmt, 1, limit);
            while (sqlite3_step(stmt) == SQLITE_ROW) {
                MatchRecord r;
                r.wave = sqlite3_column_int(stmt, 0);
                r.score = sqlite3_column_int(stmt, 1);
                r.kills = sqlite3_column_int(stmt, 2);
                r.total_damage = sqlite3_column_int(stmt, 3);
                r.duration_sec = static_cast<float>(sqlite3_column_double(stmt, 4));
                const char* sc = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 5));
                r.ship_id = sc ? sc : "pushpaka";
                const char* ca = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 6));
                r.created_at = ca ? ca : "";

                if (r.wave >= 20 || r.score > 200000) r.rank = PerformanceRank::S_RANK;
                else if (r.wave >= 10 || r.score > 100000) r.rank = PerformanceRank::A_RANK;
                else if (r.wave >= 5) r.rank = PerformanceRank::B_RANK;
                else r.rank = PerformanceRank::C_RANK;

                records.push_back(r);
            }
            sqlite3_finalize(stmt);
        }
        return records;
    }

private:
    DBSystem() : m_db(nullptr), m_player_name("Warrior"), m_high_score(0), m_max_wave(1) {}
    ~DBSystem() = default;

    void ensure_tables() {
        const char* sql = "CREATE TABLE IF NOT EXISTS scores ("
                          "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                          "player_name TEXT NOT NULL,"
                          "score INTEGER NOT NULL,"
                          "level_reached INTEGER NOT NULL,"
                          "difficulty TEXT DEFAULT 'normal',"
                          "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                          "ship_class TEXT DEFAULT 'pushpaka',"
                          "kills INTEGER DEFAULT 0,"
                          "total_damage INTEGER DEFAULT 0,"
                          "duration_seconds REAL DEFAULT 0);";
        sqlite3_exec(m_db, sql, nullptr, nullptr, nullptr);
    }

    sqlite3* m_db;
    std::string m_player_name;
    int m_high_score;
    int m_max_wave;
};

} // namespace Vimana
