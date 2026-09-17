#pragma once
#include <string>
#include <vector>
#include <iostream>
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

    Response get(const std::string& host, int port, const std::string& path, bool use_https = false) {
        return request(L"GET", host, port, path, "", use_https);
    }

    Response post(const std::string& host, int port, const std::string& path, const std::string& json_body, bool use_https = false) {
        return request(L"POST", host, port, path, json_body, use_https);
    }

private:
    HTTPClient() = default;
    ~HTTPClient() = default;

    Response request(const std::wstring& method, const std::string& host_str, int port, const std::string& path_str, const std::string& body, bool use_https) {
        Response resp;
        HINTERNET hSession = WinHttpOpen(L"VimanaWars/1.0", WINHTTP_ACCESS_TYPE_DEFAULT_PROXY, WINHTTP_NO_PROXY_NAME, WINHTTP_NO_PROXY_BYPASS, 0);
        if (!hSession) return resp;

        std::wstring host(host_str.begin(), host_str.end());
        std::wstring path(path_str.begin(), path_str.end());

        HINTERNET hConnect = WinHttpConnect(hSession, host.c_str(), static_cast<INTERNET_PORT>(port), 0);
        if (!hConnect) {
            WinHttpCloseHandle(hSession);
            return resp;
        }

        DWORD flags = use_https ? WINHTTP_FLAG_SECURE : 0;
        HINTERNET hRequest = WinHttpOpenRequest(hConnect, method.c_str(), path.c_str(), nullptr, WINHTTP_NO_REFERER, WINHTTP_DEFAULT_ACCEPT_TYPES, flags);
        if (!hRequest) {
            WinHttpCloseHandle(hConnect);
            WinHttpCloseHandle(hSession);
            return resp;
        }

        // Set timeout to 2.5 seconds
        WinHttpSetTimeouts(hRequest, 2500, 2500, 2500, 2500);

        std::wstring headers = L"Content-Type: application/json\r\n";
        BOOL bResults = FALSE;

        if (body.empty()) {
            bResults = WinHttpSendRequest(hRequest, headers.c_str(), static_cast<DWORD>(headers.length()), nullptr, 0, 0, 0);
        } else {
            bResults = WinHttpSendRequest(hRequest, headers.c_str(), static_cast<DWORD>(headers.length()), (LPVOID)body.c_str(), static_cast<DWORD>(body.length()), static_cast<DWORD>(body.length()), 0);
        }

        if (bResults) {
            bResults = WinHttpReceiveResponse(hRequest, nullptr);
        }

        if (bResults) {
            DWORD dwStatusCode = 0;
            DWORD dwSize = sizeof(dwStatusCode);
            WinHttpQueryHeaders(hRequest, WINHTTP_QUERY_STATUS_CODE | WINHTTP_QUERY_FLAG_NUMBER, WINHTTP_HEADER_NAME_BY_INDEX, &dwStatusCode, &dwSize, WINHTTP_NO_HEADER_INDEX);
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
        }

        WinHttpCloseHandle(hRequest);
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return resp;
    }
};

} // namespace Vimana
