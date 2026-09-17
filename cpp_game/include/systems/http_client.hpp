#pragma once
#include <string>
#include <vector>
#include <iostream>
#include <functional>
#include <thread>
#include <mutex>
#include <queue>
#include <sstream>

#define WIN32_LEAN_AND_MEAN
#define NOGDI
#define NOUSER
#include <windows.h>
#include <winhttp.h>
#undef DrawText
#undef DrawTextEx
#undef CloseWindow
#undef ShowCursor
#undef PlaySound
#undef LoadImage
#undef Rectangle

#include "json.hpp"

namespace Vimana {

class HTTPClient {
public:
    static HTTPClient& instance() {
        static HTTPClient client;
        return client;
    }

    struct Response {
        int status_code = 0;
        std::string body = "";
        bool success = false;
    };

    struct ParsedURL {
        bool use_https = false;
        std::string host = "127.0.0.1";
        int port = 5000;
        std::string path = "/";
    };

    static ParsedURL parse_url(const std::string& url) {
        ParsedURL res;
        std::string s = url;
        if (s.rfind("https://", 0) == 0) {
            res.use_https = true;
            res.port = 443;
            s = s.substr(8);
        } else if (s.rfind("http://", 0) == 0) {
            res.use_https = false;
            res.port = 80;
            s = s.substr(7);
        }

        size_t slash_pos = s.find('/');
        std::string host_port = (slash_pos == std::string::npos) ? s : s.substr(0, slash_pos);
        res.path = (slash_pos == std::string::npos) ? "/" : s.substr(slash_pos);

        size_t colon_pos = host_port.find(':');
        if (colon_pos != std::string::npos) {
            res.host = host_port.substr(0, colon_pos);
            try {
                res.port = std::stoi(host_port.substr(colon_pos + 1));
            } catch (...) {
                res.port = res.use_https ? 443 : 80;
            }
        } else {
            res.host = host_port;
        }

        return res;
    }

    // Synchronous Request
    Response request(const std::wstring& method, const std::string& host_str, int port,
                     const std::string& path_str, const std::string& body, bool use_https,
                     const std::string& auth_bearer = "") {
        Response resp;
        HINTERNET hSession = WinHttpOpen(L"VimanaWars/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
                                         WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
        if (!hSession) {
            resp.body = "{\"error\":\"Failed to initialize HTTP session\"}";
            return resp;
        }

        std::wstring host(host_str.begin(), host_str.end());
        std::wstring path(path_str.begin(), path_str.end());

        HINTERNET hConnect = WinHttpConnect(hSession, host.c_str(), static_cast<INTERNET_PORT>(port), 0);
        if (!hConnect) {
            WinHttpCloseHandle(hSession);
            resp.body = "{\"error\":\"Failed to connect to host\"}";
            return resp;
        }

        DWORD flags = use_https ? WINHTTP_FLAG_SECURE : 0;
        HINTERNET hRequest = WinHttpOpenRequest(hConnect, method.c_str(), path.c_str(),
                                               nullptr, WINHTTP_NO_REFERER,
                                               WINHTTP_DEFAULT_ACCEPT_TYPES, flags);
        if (!hRequest) {
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            resp.body = "{\"error\":\"Failed to open HTTP request\"}";
            return resp;
        }

        // Resilient timeouts (10s resolve/connect, 15s receive) for cloud database operations
        WinHttpSetTimeouts(hRequest, 10000, 10000, 10000, 15000);

        std::wstring headers = L"Content-Type: application/json\r\nAccept: application/json\r\n";
        if (!auth_bearer.empty()) {
            std::wstring token_w(auth_bearer.begin(), auth_bearer.end());
            headers += L"Authorization: Bearer " + token_w + L"\r\n";
        }

        BOOL bResults = FALSE;
        if (body.empty()) {
            bResults = WinHttpSendRequest(hRequest, headers.c_str(), static_cast<DWORD>(headers.length()),
                                          nullptr, 0, 0, 0);
        } else {
            bResults = WinHttpSendRequest(hRequest, headers.c_str(), static_cast<DWORD>(headers.length()),
                                          (LPVOID)body.c_str(), static_cast<DWORD>(body.length()),
                                          static_cast<DWORD>(body.length()), 0);
        }

        if (bResults) {
            bResults = WinHttpReceiveResponse(hRequest, nullptr);
        }

        if (bResults) {
            DWORD dwStatusCode = 0;
            DWORD dwSize = sizeof(dwStatusCode);
            WinHttpQueryHeaders(hRequest, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER,
                                WINHTTP_HEADER_NAME_BY_INDEX, &dwStatusCode, &dwSize, WINHTTP_NO_HEADER_INDEX);
            resp.status_code = static_cast<int>(dwStatusCode);

            DWORD dwDownloaded = 0;
            do {
                dwSize = 0;
                if (!WinHttpQueryDataAvailable(hRequest, &dwSize)) break;
                if (dwSize == 0) break;

                std::vector<char> buffer(dwSize + 1, 0);
                if (WinHttpReadData(hRequest, buffer.data(), dwSize, &dwDownloaded)) {
                    resp.body.append(buffer.data(), dwDownloaded);
                }
            } while (dwSize > 0);

            resp.success = (resp.status_code >= 200 && resp.status_code < 300);
        } else {
            resp.status_code = 0;
            resp.body = "{\"error\":\"Network request timed out or host unreachable\"}";
        }

        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return resp;
    }

    // Direct synchronous helpers
    Response get(const std::string& host, int port, const std::string& path, bool use_https = false, const std::string& auth = "") {
        return request(L"GET", host, port, path, "", use_https, auth);
    }
    Response post(const std::string& host, int port, const std::string& path, const std::string& json_body, bool use_https = false, const std::string& auth = "") {
        return request(L"POST", host, port, path, json_body, use_https, auth);
    }
    Response put(const std::string& host, int port, const std::string& path, const std::string& json_body, bool use_https = false, const std::string& auth = "") {
        return request(L"PUT", host, port, path, json_body, use_https, auth);
    }
    Response del(const std::string& host, int port, const std::string& path, bool use_https = false, const std::string& auth = "") {
        return request(L"DELETE", host, port, path, "", use_https, auth);
    }

    // URL-based synchronous helpers
    Response get_url(const std::string& url, const std::string& auth = "") {
        auto parsed = parse_url(url);
        return get(parsed.host, parsed.port, parsed.path, parsed.use_https, auth);
    }
    Response post_url(const std::string& url, const std::string& json_body, const std::string& auth = "") {
        auto parsed = parse_url(url);
        return post(parsed.host, parsed.port, parsed.path, json_body, parsed.use_https, auth);
    }
    Response put_url(const std::string& url, const std::string& json_body, const std::string& auth = "") {
        auto parsed = parse_url(url);
        return put(parsed.host, parsed.port, parsed.path, json_body, parsed.use_https, auth);
    }
    Response delete_url(const std::string& url, const std::string& auth = "") {
        auto parsed = parse_url(url);
        return del(parsed.host, parsed.port, parsed.path, parsed.use_https, auth);
    }

    // ── Non-blocking Asynchronous Request Architecture ──────────────────────
    // Spawns worker thread, then queues callback to be dispatched safely on the main thread via update().
    void request_async(const std::wstring& method, const std::string& host, int port,
                       const std::string& path, const std::string& body, bool use_https,
                       const std::string& auth, std::function<void(Response)> callback) {
        std::thread([this, method, host, port, path, body, use_https, auth, callback]() {
            Response resp = this->request(method, host, port, path, body, use_https, auth);
            std::lock_guard<std::mutex> lock(this->m_queue_mutex);
            this->m_callback_queue.push([callback, resp]() {
                if (callback) callback(resp);
            });
        }).detach();
    }

    void request_url_async(const std::wstring& method, const std::string& url,
                           const std::string& body, const std::string& auth,
                           std::function<void(Response)> callback) {
        auto parsed = parse_url(url);
        request_async(method, parsed.host, parsed.port, parsed.path, body, parsed.use_https, auth, callback);
    }

    void get_async(const std::string& url, const std::string& auth, std::function<void(Response)> callback) {
        request_url_async(L"GET", url, "", auth, callback);
    }
    void post_async(const std::string& url, const std::string& json_body, const std::string& auth, std::function<void(Response)> callback) {
        request_url_async(L"POST", url, json_body, auth, callback);
    }
    void put_async(const std::string& url, const std::string& json_body, const std::string& auth, std::function<void(Response)> callback) {
        request_url_async(L"PUT", url, json_body, auth, callback);
    }
    void delete_async(const std::string& url, const std::string& auth, std::function<void(Response)> callback) {
        request_url_async(L"DELETE", url, "", auth, callback);
    }

    // Called once per frame in main loop on the Raylib main thread
    void update() {
        std::queue<std::function<void()>> local_queue;
        {
            std::lock_guard<std::mutex> lock(m_queue_mutex);
            std::swap(local_queue, m_callback_queue);
        }
        while (!local_queue.empty()) {
            auto cb = local_queue.front();
            local_queue.pop();
            if (cb) cb();
        }
    }

private:
    HTTPClient() = default;
    ~HTTPClient() = default;

    std::mutex m_queue_mutex;
    std::queue<std::function<void()>> m_callback_queue;
};

} // namespace Vimana
