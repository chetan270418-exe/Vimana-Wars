#pragma once
#include <string>
#include <vector>
#include <array>
#include <iostream>
#include <chrono>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include "core/types.hpp"
#include "core/constants.hpp"
#include "systems/network_socket.hpp"

namespace Vimana {

struct RemotePeer {
    std::string ip = "127.0.0.1";
    uint16_t    port = DEFAULT_NET_PORT;
    uint8_t     player_id = 1;
    std::string name = "Pilot";
    std::string ship_id = "garuda";
    float       last_seen = 0.0f;
    bool        is_connected = false;
    bool        is_ai_takeover = false;
    int         ping_ms = 20;
    InputPacket last_input;
};

class NetworkManager {
public:
    static NetworkManager& instance() {
        static NetworkManager mgr;
        return mgr;
    }

    void init() {
        m_socket.close();
        m_role = NetworkRole::OFFLINE;
        m_room_code = "VX82Q";
        m_ping_ms = 18;
        m_packet_loss_pct = 0.0f;
        m_tick = 0;
        m_seq = 0;
        m_peers.clear();
        m_players.clear();
        m_target_host_ip = "127.0.0.1";
        m_target_host_port = DEFAULT_NET_PORT;
        m_local_player_id = 0;
        m_is_connected = false;
        m_connection_timer = 0.0f;
    }

    NetworkRole role() const { return m_role; }
    void set_role(NetworkRole r) { m_role = r; }

    const std::string& room_code() const { return m_room_code; }
    int ping_ms() const { return m_ping_ms; }
    float packet_loss_pct() const { return m_packet_loss_pct; }
    uint32_t tick() const { return m_tick; }
    uint32_t sequence() const { return m_seq; }
    bool is_connected() const { return m_is_connected; }
    uint8_t local_player_id() const { return m_local_player_id; }
    const std::string& target_host_ip() const { return m_target_host_ip; }
    uint16_t target_host_port() const { return m_target_host_port; }
    void set_target_host(const std::string& ip, uint16_t port) {
        m_target_host_ip = ip;
        m_target_host_port = port;
    }

    const std::vector<PlayerNetState>& players() const { return m_players; }
    std::vector<PlayerNetState>& players_mut() { return m_players; }
    const std::vector<RemotePeer>& peers() const { return m_peers; }

    std::string generate_room_code() {
        static const char charset[] = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
        std::string code = "";
        for (int i = 0; i < 5; ++i) {
            code += charset[std::rand() % (sizeof(charset) - 1)];
        }
        m_room_code = code;
        return m_room_code;
    }

    bool host_session(const std::string& host_name, const std::string& ship_id, uint16_t port = DEFAULT_NET_PORT) {
        m_role = NetworkRole::HOST;
        m_local_player_id = 0;
        m_is_connected = true;
        generate_room_code();
        m_players.clear();
        m_peers.clear();

        if (!m_socket.open(port)) {
            std::cerr << "[NetworkManager] Failed to host on port " << port << std::endl;
            return false;
        }

        // Slot 0: Host Player
        PlayerNetState p0;
        p0.player_id = 0;
        p0.pos_x = 350.0f;
        p0.pos_y = 480.0f;
        p0.hp = 100;
        p0.score = 0;
        p0.combo = 0;
        p0.is_downed = false;
        std::strncpy(p0.ship_id, ship_id.c_str(), sizeof(p0.ship_id) - 1);
        m_players.push_back(p0);

        std::cout << "[NetworkManager] Hosting LAN room: " << m_room_code << " on port " << port << std::endl;
        return true;
    }

    bool join_session(const std::string& host_ip, uint16_t host_port, const std::string& player_name, const std::string& ship_id) {
        m_role = NetworkRole::CLIENT;
        m_target_host_ip = host_ip;
        m_target_host_port = host_port;
        m_is_connected = false;
        m_connection_timer = 0.0f;

        if (!m_socket.open(0)) { // Bind ephemeral client port
            std::cerr << "[NetworkManager] Failed to open client socket" << std::endl;
            return false;
        }

        // Send JOIN_REQUEST packet to host
        PacketHeader hdr;
        hdr.magic = VW_PACKET_MAGIC;
        hdr.version = VW_PACKET_VERSION;
        hdr.packet_type = static_cast<uint8_t>(PacketType::JOIN_REQUEST);
        hdr.sequence = ++m_seq;
        hdr.ack = 0;
        hdr.payload_size = sizeof(LobbyMessage);

        LobbyMessage msg;
        msg.type = LobbyMessage::Type::JOIN;
        msg.player_id = 0;
        std::strncpy(msg.player_name, player_name.c_str(), sizeof(msg.player_name) - 1);
        std::strncpy(msg.ship_id, ship_id.c_str(), sizeof(msg.ship_id) - 1);

        char packet_buf[sizeof(PacketHeader) + sizeof(LobbyMessage)];
        std::memcpy(packet_buf, &hdr, sizeof(PacketHeader));
        std::memcpy(packet_buf + sizeof(PacketHeader), &msg, sizeof(LobbyMessage));

        m_socket.send_to(host_ip, host_port, packet_buf, sizeof(packet_buf));
        std::cout << "[NetworkManager] Sent JOIN_REQUEST to " << host_ip << ":" << host_port << std::endl;
        return true;
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

        RemotePeer peer;
        peer.player_id = p.player_id;
        peer.name = name;
        peer.ship_id = ship_id;
        peer.is_connected = true;
        peer.is_ai_takeover = is_ai;
        peer.last_seen = 0.0f;
        m_peers.push_back(peer);

        std::cout << "[NetworkManager] Added squadmate " << name << " (Slot " << (int)p.player_id << ")" << (is_ai ? " [AI]" : "") << std::endl;
    }

    void leave_session() {
        if (m_role == NetworkRole::CLIENT && m_is_connected) {
            PacketHeader hdr;
            hdr.packet_type = static_cast<uint8_t>(PacketType::DISCONNECT);
            m_socket.send_to(m_target_host_ip, m_target_host_port, &hdr, sizeof(hdr));
        }
        m_socket.close();
        m_role = NetworkRole::OFFLINE;
        m_is_connected = false;
        m_players.clear();
        m_peers.clear();
    }

    void update(float dt) {
        if (m_role == NetworkRole::OFFLINE || !m_socket.is_open()) return;

        // 1. Process incoming non-blocking UDP packets
        uint8_t buffer[2048];
        std::string sender_ip;
        uint16_t sender_port;

        int bytes_read = 0;
        while ((bytes_read = m_socket.recv_from(sender_ip, sender_port, buffer, sizeof(buffer))) > 0) {
            if (bytes_read < static_cast<int>(sizeof(PacketHeader))) continue;

            PacketHeader hdr;
            std::memcpy(&hdr, buffer, sizeof(PacketHeader));
            if (hdr.magic != VW_PACKET_MAGIC) continue;

            const uint8_t* payload = buffer + sizeof(PacketHeader);
            int payload_len = bytes_read - sizeof(PacketHeader);

            PacketType p_type = static_cast<PacketType>(hdr.packet_type);

            if (m_role == NetworkRole::HOST) {
                handle_host_packet(p_type, hdr, payload, payload_len, sender_ip, sender_port);
            } else if (m_role == NetworkRole::CLIENT) {
                handle_client_packet(p_type, hdr, payload, payload_len, sender_ip, sender_port);
            }
        }

        // 2. Peer liveness & AI Takeover tracking (Host side)
        if (m_role == NetworkRole::HOST) {
            for (auto& peer : m_peers) {
                if (peer.is_connected && !peer.is_ai_takeover) {
                    peer.last_seen += dt;
                    if (peer.last_seen > 15.0f) {
                        // 15-second timeout: Seamless AI Takeover
                        peer.is_ai_takeover = true;
                        std::cout << "[NetworkManager] Pilot " << peer.name << " timed out (15s). Wingman AI took over flight controls!" << std::endl;
                    }
                }
            }
        }
    }

    void send_input(const InputPacket& input) {
        if (m_role != NetworkRole::CLIENT || !m_socket.is_open()) return;

        PacketHeader hdr;
        hdr.magic = VW_PACKET_MAGIC;
        hdr.version = VW_PACKET_VERSION;
        hdr.packet_type = static_cast<uint8_t>(PacketType::INPUT_SYNC);
        hdr.sequence = ++m_seq;
        hdr.ack = m_tick;
        hdr.payload_size = sizeof(InputPacket);

        uint8_t packet[sizeof(PacketHeader) + sizeof(InputPacket)];
        std::memcpy(packet, &hdr, sizeof(PacketHeader));
        std::memcpy(packet + sizeof(PacketHeader), &input, sizeof(InputPacket));

        m_socket.send_to(m_target_host_ip, m_target_host_port, packet, sizeof(packet));
    }

    void broadcast_snapshot(const SnapshotPacket& snap) {
        m_last_snapshot = snap;
        m_tick = snap.tick;

        if (m_role != NetworkRole::HOST || !m_socket.is_open()) return;

        PacketHeader hdr;
        hdr.magic = VW_PACKET_MAGIC;
        hdr.version = VW_PACKET_VERSION;
        hdr.packet_type = static_cast<uint8_t>(PacketType::SNAPSHOT_SYNC);
        hdr.sequence = ++m_seq;
        hdr.ack = m_tick;
        hdr.payload_size = sizeof(SnapshotPacket);

        uint8_t packet[sizeof(PacketHeader) + sizeof(SnapshotPacket)];
        std::memcpy(packet, &hdr, sizeof(PacketHeader));
        std::memcpy(packet + sizeof(PacketHeader), &snap, sizeof(SnapshotPacket));

        for (const auto& peer : m_peers) {
            if (peer.is_connected && !peer.is_ai_takeover) {
                m_socket.send_to(peer.ip, peer.port, packet, sizeof(packet));
            }
        }
    }

    const SnapshotPacket& latest_snapshot() const {
        return m_last_snapshot;
    }

private:
    NetworkManager() 
        : m_role(NetworkRole::OFFLINE), m_room_code("VX82Q"), m_ping_ms(18),
          m_packet_loss_pct(0.0f), m_tick(0), m_seq(0), m_is_connected(false),
          m_local_player_id(0), m_target_host_ip("127.0.0.1"), m_target_host_port(DEFAULT_NET_PORT),
          m_connection_timer(0.0f) {}

    void handle_host_packet(PacketType type, const PacketHeader& hdr, const uint8_t* payload, int len, const std::string& ip, uint16_t port) {
        if (type == PacketType::JOIN_REQUEST) {
            if (m_players.size() >= MAX_CO_OP_PLAYERS) {
                // Reject
                PacketHeader reject_hdr;
                reject_hdr.packet_type = static_cast<uint8_t>(PacketType::JOIN_REJECT);
                m_socket.send_to(ip, port, &reject_hdr, sizeof(reject_hdr));
                return;
            }

            // Accept new player
            uint8_t assigned_id = static_cast<uint8_t>(m_players.size());
            std::string p_name = "Pilot-" + std::to_string(assigned_id);
            std::string p_ship = "garuda";

            if (len >= static_cast<int>(sizeof(LobbyMessage))) {
                const LobbyMessage* msg = reinterpret_cast<const LobbyMessage*>(payload);
                if (msg->player_name[0] != '\0') p_name = msg->player_name;
                if (msg->ship_id[0] != '\0') p_ship = msg->ship_id;
            }

            RemotePeer peer;
            peer.ip = ip;
            peer.port = port;
            peer.player_id = assigned_id;
            peer.name = p_name;
            peer.ship_id = p_ship;
            peer.is_connected = true;
            peer.last_seen = 0.0f;
            peer.ping_ms = 18;
            m_peers.push_back(peer);

            PlayerNetState pnet;
            pnet.player_id = assigned_id;
            pnet.pos_x = 350.0f + assigned_id * 80.0f;
            pnet.pos_y = 480.0f;
            pnet.hp = 100;
            pnet.is_downed = false;
            std::strncpy(pnet.ship_id, p_ship.c_str(), sizeof(pnet.ship_id) - 1);
            m_players.push_back(pnet);

            // Send JOIN_ACCEPT
            PacketHeader accept_hdr;
            accept_hdr.packet_type = static_cast<uint8_t>(PacketType::JOIN_ACCEPT);
            accept_hdr.sequence = ++m_seq;
            accept_hdr.ack = assigned_id; // Assigned player ID
            m_socket.send_to(ip, port, &accept_hdr, sizeof(accept_hdr));

            std::cout << "[NetworkManager] Accepted client " << p_name << " from " << ip << ":" << port << " as Player " << (int)assigned_id << std::endl;
        } else if (type == PacketType::INPUT_SYNC) {
            if (len >= static_cast<int>(sizeof(InputPacket))) {
                const InputPacket* in = reinterpret_cast<const InputPacket*>(payload);
                for (auto& peer : m_peers) {
                    if (peer.ip == ip && peer.port == port) {
                        peer.last_input = *in;
                        peer.last_seen = 0.0f;
                        peer.ping_ms = std::max(5, (int)(hdr.ack % 60));
                        break;
                    }
                }
            }
        } else if (type == PacketType::DISCONNECT) {
            for (auto& peer : m_peers) {
                if (peer.ip == ip && peer.port == port) {
                    peer.is_ai_takeover = true;
                    std::cout << "[NetworkManager] Client " << peer.name << " gracefully disconnected; wingman AI takeover" << std::endl;
                    break;
                }
            }
        }
    }

    void handle_client_packet(PacketType type, const PacketHeader& hdr, const uint8_t* payload, int len, const std::string& ip, uint16_t port) {
        if (type == PacketType::JOIN_ACCEPT) {
            m_is_connected = true;
            m_local_player_id = static_cast<uint8_t>(hdr.ack);
            m_ping_ms = 16;
            std::cout << "[NetworkManager] Successfully joined session! Assigned Player ID: " << (int)m_local_player_id << std::endl;
        } else if (type == PacketType::SNAPSHOT_SYNC) {
            if (len >= static_cast<int>(sizeof(SnapshotPacket))) {
                const SnapshotPacket* snap = reinterpret_cast<const SnapshotPacket*>(payload);
                m_last_snapshot = *snap;
                m_tick = snap->tick;
                m_is_connected = true;
                m_ping_ms = std::max(8, (int)(m_seq - hdr.sequence));
            }
        }
    }

    NetworkSocket m_socket;
    NetworkRole   m_role;
    std::string   m_room_code;
    int           m_ping_ms;
    float         m_packet_loss_pct;
    uint32_t      m_tick;
    uint32_t      m_seq;
    bool          m_is_connected;
    uint8_t       m_local_player_id;
    std::string   m_target_host_ip;
    uint16_t      m_target_host_port;
    float         m_connection_timer;

    std::vector<PlayerNetState> m_players;
    std::vector<RemotePeer>     m_peers;
    SnapshotPacket              m_last_snapshot;
};

} // namespace Vimana
