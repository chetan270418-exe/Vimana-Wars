#pragma once

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#define NOMINMAX
#endif
#ifndef NOGDI
#define NOGDI
#endif
#ifndef NOUSER
#define NOUSER
#endif
#include <winsock2.h>
#include <ws2tcpip.h>

// Undefine Windows macros that conflict with Raylib functions & types
#ifdef DrawText
#undef DrawText
#endif
#ifdef DrawTextEx
#undef DrawTextEx
#endif
#ifdef CloseWindow
#undef CloseWindow
#endif
#ifdef ShowCursor
#undef ShowCursor
#endif
#ifdef LoadImage
#undef LoadImage
#endif
#ifdef PlaySound
#undef PlaySound
#endif
#ifdef Rectangle
#undef Rectangle
#endif

#include <cstdint>
#include <cstring>
#include <string>
#include <iostream>
#include <chrono>

namespace Vimana {

constexpr uint16_t VW_PACKET_MAGIC = 0x5657; // "VW"
constexpr uint8_t  VW_PACKET_VERSION = 1;
constexpr uint16_t DEFAULT_NET_PORT = 7704;

enum class PacketType : uint8_t {
    PING            = 0,
    JOIN_REQUEST    = 1,
    JOIN_ACCEPT     = 2,
    JOIN_REJECT     = 3,
    INPUT_SYNC      = 4,
    SNAPSHOT_SYNC   = 5,
    LOBBY_STATE     = 6,
    DISCONNECT      = 7
};

#pragma pack(push, 1)
struct PacketHeader {
    uint16_t magic       = VW_PACKET_MAGIC;
    uint8_t  version     = VW_PACKET_VERSION;
    uint8_t  packet_type = 0;
    uint32_t sequence    = 0;
    uint32_t ack         = 0;
    uint16_t payload_size= 0;
};
#pragma pack(pop)

class NetworkSocket {
public:
    NetworkSocket() : m_socket(INVALID_SOCKET), m_is_initialized(false), m_local_port(0) {}

    ~NetworkSocket() {
        close();
    }

    bool initialize() {
        if (m_is_initialized) return true;
        WSADATA wsa_data;
        int res = WSAStartup(MAKEWORD(2, 2), &wsa_data);
        if (res != 0) {
            std::cerr << "[NetworkSocket] WSAStartup failed: " << res << std::endl;
            return false;
        }
        m_is_initialized = true;
        return true;
    }

    bool open(uint16_t port = 0) {
        if (!initialize()) return false;
        close();

        m_socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (m_socket == INVALID_SOCKET) {
            std::cerr << "[NetworkSocket] socket() failed: " << WSAGetLastError() << std::endl;
            return false;
        }

        // Set non-blocking mode
        u_long mode = 1;
        if (ioctlsocket(m_socket, FIONBIO, &mode) != 0) {
            std::cerr << "[NetworkSocket] ioctlsocket FIONBIO failed: " << WSAGetLastError() << std::endl;
            close();
            return false;
        }

        // Enable reuse address
        int reuse = 1;
        setsockopt(m_socket, SOL_SOCKET, SO_REUSEADDR, (const char*)&reuse, sizeof(reuse));

        // Bind socket
        sockaddr_in addr;
        std::memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = INADDR_ANY;
        addr.sin_port = htons(port);

        if (bind(m_socket, (sockaddr*)&addr, sizeof(addr)) != 0) {
            std::cerr << "[NetworkSocket] bind() failed on port " << port << ": " << WSAGetLastError() << std::endl;
            close();
            return false;
        }

        m_local_port = port;
        std::cout << "[NetworkSocket] Bound non-blocking UDP socket on port " << port << std::endl;
        return true;
    }

    void close() {
        if (m_socket != INVALID_SOCKET) {
            closesocket(m_socket);
            m_socket = INVALID_SOCKET;
        }
        m_local_port = 0;
    }

    bool is_open() const {
        return m_socket != INVALID_SOCKET;
    }

    uint16_t local_port() const {
        return m_local_port;
    }

    int send_to(const std::string& ip, uint16_t port, const void* data, int size) {
        if (!is_open() || !data || size <= 0) return -1;

        sockaddr_in dest;
        std::memset(&dest, 0, sizeof(dest));
        dest.sin_family = AF_INET;
        dest.sin_port = htons(port);
        inet_pton(AF_INET, ip.c_str(), &dest.sin_addr);

        int sent = sendto(m_socket, (const char*)data, size, 0, (sockaddr*)&dest, sizeof(dest));
        return sent;
    }

    int recv_from(std::string& out_ip, uint16_t& out_port, void* buffer, int max_size) {
        if (!is_open() || !buffer || max_size <= 0) return -1;

        sockaddr_in sender;
        int sender_len = sizeof(sender);
        std::memset(&sender, 0, sizeof(sender));

        int received = recvfrom(m_socket, (char*)buffer, max_size, 0, (sockaddr*)&sender, &sender_len);
        if (received > 0) {
            char ip_str[INET_ADDRSTRLEN] = {};
            inet_ntop(AF_INET, &sender.sin_addr, ip_str, INET_ADDRSTRLEN);
            out_ip = ip_str;
            out_port = ntohs(sender.sin_port);
            return received;
        }

        return -1; // Would block or error
    }

private:
    SOCKET   m_socket;
    bool     m_is_initialized;
    uint16_t m_local_port;
};

} // namespace Vimana
