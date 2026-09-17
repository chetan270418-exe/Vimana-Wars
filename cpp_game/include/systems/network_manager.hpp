#pragma once
#include <string>
#include <vector>
#include <array>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <cstring>
#include "core/types.hpp"
#include "core/constants.hpp"

namespace Vimana {

class NetworkManager {
public:
    static NetworkManager& instance() {
        static NetworkManager mgr;
        return mgr;
    }

    void init() {
        m_role = NetworkRole::OFFLINE;
        m_room_code = "VX82Q";
        m_ping_ms = 18;
        m_players.clear();
    }

    NetworkRole role() const { return m_role; }
    void set_role(NetworkRole r) { m_role = r; }

    const std::string& room_code() const { return m_room_code; }
    int ping_ms() const { return m_ping_ms; }

    const std::vector<PlayerNetState>& players() const { return m_players; }
    std::vector<PlayerNetState>& players_mut() { return m_players; }

    std::string generate_room_code() {
        static const char charset[] = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
        std::string code = "";
        for (int i = 0; i < 5; ++i) {
            code += charset[std::rand() % (sizeof(charset) - 1)];
        }
        m_room_code = code;
        return m_room_code;
    }

    void host_session(const std::string& host_name, const std::string& ship_id) {
        m_role = NetworkRole::HOST;
        generate_room_code();
        m_players.clear();

        // Slot 0: Host Player
        PlayerNetState p1;
        p1.player_id = 0;
        p1.pos_x = 350.0f;
        p1.pos_y = 480.0f;
        p1.hp = 100;
        p1.score = 0;
        p1.combo = 0;
        p1.is_downed = false;
        std::strncpy(p1.ship_id, ship_id.c_str(), sizeof(p1.ship_id) - 1);
        m_players.push_back(p1);

        std::cout << "[NetworkManager] Hosting room: " << m_room_code << " with host: " << host_name << std::endl;
    }

    void add_teammate(const std::string& name, const std::string& ship_id, bool is_ai = false) {
        if (m_players.size() >= MAX_CO_OP_PLAYERS) return;

        PlayerNetState p;
        p.player_id = static_cast<uint8_t>(m_players.size());
        p.pos_x = 350.0f + p.player_id * 80.0f;
        p.pos_y = 480.0f;
        p.hp = 100;
        p.score = 0;
        p.combo = 0;
        p.is_downed = false;
        std::strncpy(p.ship_id, ship_id.c_str(), sizeof(p.ship_id) - 1);
        m_players.push_back(p);

        std::cout << "[NetworkManager] Joined squad: " << name << " (" << ship_id << ")" << (is_ai ? " [AI PILOT]" : "") << std::endl;
    }

    bool join_session(const std::string& room_code, const std::string& player_name, const std::string& ship_id) {
        m_role = NetworkRole::CLIENT;
        m_room_code = room_code;
        m_players.clear();

        // Slot 0: Remote Host (Arjuna Ace)
        PlayerNetState host_p;
        host_p.player_id = 0;
        host_p.pos_x = 350.0f;
        host_p.pos_y = 480.0f;
        host_p.hp = 100;
        std::strncpy(host_p.ship_id, "garuda", sizeof(host_p.ship_id) - 1);
        m_players.push_back(host_p);

        // Slot 1: Local Player
        PlayerNetState local_p;
        local_p.player_id = 1;
        local_p.pos_x = 450.0f;
        local_p.pos_y = 480.0f;
        local_p.hp = 100;
        std::strncpy(local_p.ship_id, ship_id.c_str(), sizeof(local_p.ship_id) - 1);
        m_players.push_back(local_p);

        m_ping_ms = 22 + (std::rand() % 15);
        std::cout << "[NetworkManager] Joined room " << room_code << " with ping " << m_ping_ms << "ms" << std::endl;
        return true;
    }

    void leave_session() {
        m_role = NetworkRole::OFFLINE;
        m_players.clear();
    }

    void broadcast_snapshot(const SnapshotPacket& snap) {
        m_last_snapshot = snap;
    }

    const SnapshotPacket& latest_snapshot() const {
        return m_last_snapshot;
    }

private:
    NetworkManager() : m_role(NetworkRole::OFFLINE), m_room_code("VX82Q"), m_ping_ms(24) {}
    ~NetworkManager() = default;

    NetworkRole m_role;
    std::string m_room_code;
    int m_ping_ms;
    std::vector<PlayerNetState> m_players;
    SnapshotPacket m_last_snapshot;
};

} // namespace Vimana
