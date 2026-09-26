#pragma once
#include <string>
#include <vector>
#include <regex>
#include <cmath>
#include "raylib.h"
#include "core/constants.hpp"
#include "core/types.hpp"
#include "views/view_interface.hpp"
#include "systems/asset_manager.hpp"
#include "systems/db_system.hpp"
#include "systems/account_system.hpp"
#include "systems/achievement_system.hpp"
#include "ui/button.hpp"
#include "ui/vedic_theme.hpp"

namespace Vimana {

class AuthView : public IView {
public:
    struct InputField {
        Rectangle bounds;
        std::string label;
        std::string text;
        std::string placeholder;
        bool is_password = false;
        bool focused = false;
        size_t max_len = 48;

        void handle_input() {
            if (!focused) return;
            int key = GetCharPressed();
            while (key > 0) {
                if (key >= 32 && key <= 126 && text.length() < max_len) {
                    text.push_back(static_cast<char>(key));
                }
                key = GetCharPressed();
            }
            if (IsKeyPressed(KEY_BACKSPACE) && !text.empty()) {
                text.pop_back();
            }
        }

        void draw(Font font, bool show_password, float blink_time) const {
            // Label
            DrawTextEx(font, label.c_str(), { bounds.x, bounds.y - 18 }, 12, 1.0f, focused ? COLOR_GOLD_BRIGHT : COLOR_MUTED);

            // Field box
            Color border = focused ? COLOR_GOLD_BRIGHT : (text.empty() ? COLOR_SURFACE_HIGH : COLOR_CYAN_BRIGHT);
            UI::DrawChamferedPanel(bounds, border, COLOR_SURFACE_MID, 3.0f);

            // Text / Masked display
            std::string display_str = text;
            if (is_password && !show_password) {
                display_str = std::string(text.length(), '*');
            }

            if (display_str.empty() && !focused) {
                DrawTextEx(font, placeholder.c_str(), { bounds.x + 10, bounds.y + 8 }, 14, 1.0f, COLOR_MUTED);
            } else {
                DrawTextEx(font, display_str.c_str(), { bounds.x + 10, bounds.y + 8 }, 14, 1.0f, COLOR_PARCHMENT);
            }

            // Blinking cursor
            if (focused && std::fmod(blink_time, 1.0f) < 0.5f) {
                Vector2 sz = MeasureTextEx(font, display_str.c_str(), 14, 1.0f);
                DrawRectangle(static_cast<int>(bounds.x + 12 + sz.x), static_cast<int>(bounds.y + 7), 2, 18, COLOR_GOLD_BRIGHT);
            }
        }
    };

    AuthView()
        : m_next_view(ViewType::AUTH),
          m_active_tab(0),
          m_show_password(false),
          m_blink_timer(0.0f),
          m_status_msg("Sign in with your pilot account or play as guest"),
          m_status_is_error(false),
          m_is_loading(false),
          m_btn_tab_login({ 140, 80, 150, 34 }, "1. SIGN IN", COLOR_GOLD_BRIGHT, "", Vimana::UI::ButtonKind::PRIMARY),
          m_btn_tab_register({ 300, 80, 150, 34 }, "2. REGISTER", COLOR_CYAN_BRIGHT, "", Vimana::UI::ButtonKind::SECONDARY),
          m_btn_tab_verify({ 460, 80, 140, 34 }, "3. VERIFY", COLOR_GREEN_BRIGHT, "", Vimana::UI::ButtonKind::TERTIARY),
          m_btn_tab_reset({ 610, 80, 150, 34 }, "4. RESET PW", COLOR_ORANGE_BRIGHT, "", Vimana::UI::ButtonKind::TERTIARY),
          m_btn_submit({ 320, 410, 260, 42 }, "SIGN IN TO CLOUD", COLOR_GOLD_BRIGHT, "", Vimana::UI::ButtonKind::PRIMARY),
          m_btn_guest({ 320, 462, 260, 36 }, "PLAY AS GUEST (OFFLINE)", COLOR_CYAN_BRIGHT, "", Vimana::UI::ButtonKind::SECONDARY),
          m_btn_toggle_pw({ 665, 255, 75, 32 }, "SHOW", COLOR_MUTED, "", Vimana::UI::ButtonKind::GHOST),
          m_btn_back({ 40, 525, 120, 36 }, "TITLE", COLOR_MUTED, "", Vimana::UI::ButtonKind::GHOST)
    {
        init();
    }

    void init() override {
        m_next_view = ViewType::AUTH;
        m_blink_timer = 0.0f;
        m_show_password = false;
        m_is_loading = false;
        m_status_msg = AccountSystem::instance().is_logged_in() 
            ? "Signed in as: " + AccountSystem::instance().player_name() + " (" + AccountSystem::instance().game_id() + ")"
            : "Sign in with your pilot credentials or play offline as guest";
        m_status_is_error = false;

        setup_inputs();
    }

    void setup_inputs() {
        float cx = SCREEN_WIDTH / 2.0f;
        float w = 380.0f;
        float x = cx - w / 2.0f;

        m_inputs.clear();

        if (m_active_tab == 0) {
            // LOGIN TAB
            m_inputs.push_back({ { x, 195, w, 34 }, "EMAIL ADDRESS", AccountSystem::instance().email(), "pilot@vimana.astral", false, true, 64 });
            m_inputs.push_back({ { x, 265, w - 70, 34 }, "PILOT PASSWORD", "", "Enter password", true, false, 64 });
            m_btn_toggle_pw.set_rect({ x + w - 60, 265, 60, 34 });
            m_btn_submit.set_label("SIGN IN // CONNECT");
            m_btn_submit.set_color(COLOR_GOLD_BRIGHT);
            m_btn_submit.set_rect({ cx - 140, 345, 280, 40 });
            m_btn_guest.set_rect({ cx - 140, 395, 280, 34 });
        } else if (m_active_tab == 1) {
            // REGISTER TAB
            m_inputs.push_back({ { x, 150, w, 32 }, "EMAIL ADDRESS", "", "pilot@vimana.astral", false, true, 64 });
            m_inputs.push_back({ { x, 205, w, 32 }, "PILOT CALLSIGN", DBSystem::instance().player_name() == "Warrior" ? "" : DBSystem::instance().player_name(), "e.g. ARJUNA_77", false, false, 20 });
            m_inputs.push_back({ { x, 260, w - 70, 32 }, "PASSWORD (MIN 8 CHARACTERS)", "", "Create secure password", true, false, 64 });
            m_inputs.push_back({ { x, 315, w, 32 }, "CONFIRM PASSWORD", "", "Re-enter password", true, false, 64 });
            m_btn_toggle_pw.set_rect({ x + w - 60, 260, 60, 32 });
            m_btn_submit.set_label("COMMISSION PILOT (REGISTER)");
            m_btn_submit.set_color(COLOR_CYAN_BRIGHT);
            m_btn_submit.set_rect({ cx - 150, 375, 300, 38 });
            m_btn_guest.set_rect({ cx - 150, 420, 300, 32 });
        } else if (m_active_tab == 2) {
            // VERIFY EMAIL TAB
            m_inputs.push_back({ { x, 220, w, 36 }, "ONE-TIME VERIFICATION TOKEN", "", "Paste token here", false, true, 64 });
            m_btn_submit.set_label("ACTIVATE PILOT LICENSE");
            m_btn_submit.set_color(COLOR_GREEN_BRIGHT);
            m_btn_submit.set_rect({ cx - 140, 310, 280, 42 });
        } else if (m_active_tab == 3) {
            // PASSWORD RESET TAB
            m_inputs.push_back({ { x, 160, w, 32 }, "ACCOUNT EMAIL", "", "pilot@vimana.astral", false, true, 64 });
            m_inputs.push_back({ { x, 225, w, 32 }, "RESET TOKEN", "", "Paste reset token", false, false, 64 });
            m_inputs.push_back({ { x, 290, w, 32 }, "NEW PASSWORD", "", "Min 8 characters", true, false, 64 });
            m_btn_submit.set_label("APPLY NEW PASSWORD");
            m_btn_submit.set_color(COLOR_ORANGE_BRIGHT);
            m_btn_submit.set_rect({ cx - 140, 355, 280, 40 });
        }
    }

    void update(float dt, Vector2 mouse_pos) override {
        m_blink_timer += dt;

        // Navigation back
        if (m_btn_back.update(mouse_pos) || IsKeyPressed(KEY_ESCAPE)) {
            m_next_view = ViewType::TITLE;
            return;
        }

        // Tab selection
        int prev_tab = m_active_tab;
        if (m_btn_tab_login.update(mouse_pos)) m_active_tab = 0;
        if (m_btn_tab_register.update(mouse_pos)) m_active_tab = 1;
        if (m_btn_tab_verify.update(mouse_pos)) m_active_tab = 2;
        if (m_btn_tab_reset.update(mouse_pos)) m_active_tab = 3;

        if (m_active_tab != prev_tab) {
            m_status_msg = "";
            m_status_is_error = false;
            setup_inputs();
        }

        // Password visibility toggle
        if ((m_active_tab == 0 || m_active_tab == 1) && m_btn_toggle_pw.update(mouse_pos)) {
            m_show_password = !m_show_password;
            m_btn_toggle_pw.set_label(m_show_password ? "HIDE" : "SHOW");
        }

        // Focus handling via click
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) {
            for (auto& input : m_inputs) {
                input.focused = CheckCollisionPointRec(mouse_pos, input.bounds);
            }
        }

        // Tab key cycles through fields
        if (IsKeyPressed(KEY_TAB)) {
            size_t focused_idx = 0;
            bool found = false;
            for (size_t i = 0; i < m_inputs.size(); ++i) {
                if (m_inputs[i].focused) {
                    m_inputs[i].focused = false;
                    focused_idx = (i + 1) % m_inputs.size();
                    found = true;
                    break;
                }
            }
            if (found && focused_idx < m_inputs.size()) {
                m_inputs[focused_idx].focused = true;
            } else if (!m_inputs.empty()) {
                m_inputs[0].focused = true;
            }
        }

        // Typing in focused field
        for (auto& input : m_inputs) {
            input.handle_input();
        }

        // Guest mode button
        if ((m_active_tab == 0 || m_active_tab == 1) && m_btn_guest.update(mouse_pos)) {
            AccountSystem::instance().play_as_guest();
            m_next_view = ViewType::MENU;
            return;
        }

        // Submit action
        bool do_submit = m_btn_submit.update(mouse_pos) || IsKeyPressed(KEY_ENTER);
        if (do_submit && !m_is_loading) {
            execute_submit();
        }
    }

    void execute_submit() {
        if (m_active_tab == 0) {
            // SIGN IN
            std::string email = m_inputs[0].text;
            std::string password = m_inputs[1].text;

            if (email.empty() || password.empty()) {
                set_status("Please enter both email and password.", true);
                return;
            }

            m_is_loading = true;
            set_status("Authenticating pilot with Sangha Cloud...", false);

            AccountSystem::instance().login(email, password, [this](bool success, const std::string& msg) {
                m_is_loading = false;
                if (success) {
                    set_status(msg, false);
                    m_next_view = ViewType::MENU;
                } else {
                    set_status(msg, true);
                }
            });

        } else if (m_active_tab == 1) {
            // REGISTER
            std::string email = m_inputs[0].text;
            std::string callsign = m_inputs[1].text;
            std::string password = m_inputs[2].text;
            std::string confirm_pw = m_inputs[3].text;

            static const std::regex email_regex(R"(^[^@\s]+@[^@\s]+\.[^@\s]+$)");
            if (!std::regex_match(email, email_regex)) {
                set_status("Please enter a valid email address.", true);
                return;
            }
            if (callsign.length() < 3) {
                set_status("Callsign must be at least 3 characters long.", true);
                return;
            }
            if (password.length() < 8) {
                set_status("Password must be at least 8 characters long.", true);
                return;
            }
            if (password != confirm_pw) {
                set_status("Passwords do not match.", true);
                return;
            }

            m_is_loading = true;
            set_status("Commissioning new Astral Pilot...", false);

            AccountSystem::instance().register_account(email, password, callsign,
                [this](bool success, const std::string& msg, bool needs_verify) {
                    m_is_loading = false;
                    if (success) {
                        set_status(msg, false);
                        AchievementSystem::instance().check_and_award("REGISTER");
                        if (needs_verify) {
                            m_active_tab = 2; // Switch to verify tab
                            setup_inputs();
                        } else {
                            m_next_view = ViewType::MENU;
                        }
                    } else {
                        set_status(msg, true);
                    }
                });

        } else if (m_active_tab == 2) {
            // VERIFY EMAIL
            std::string token = m_inputs[0].text;
            if (token.empty()) {
                set_status("Please enter the verification token.", true);
                return;
            }

            m_is_loading = true;
            set_status("Validating verification token...", false);

            AccountSystem::instance().verify_email(token, [this](bool success, const std::string& msg) {
                m_is_loading = false;
                set_status(msg, !success);
                if (success) {
                    m_next_view = ViewType::MENU;
                }
            });

        } else if (m_active_tab == 3) {
            // RESET PASSWORD
            std::string email = m_inputs[0].text;
            std::string token = m_inputs[1].text;
            std::string new_pw = m_inputs[2].text;

            if (token.empty()) {
                // Step 1: Request token
                if (email.empty()) {
                    set_status("Enter your account email to request a reset token.", true);
                    return;
                }
                m_is_loading = true;
                set_status("Requesting password reset instructions...", false);

                AccountSystem::instance().request_password_reset(email, [this](bool success, const std::string& msg) {
                    m_is_loading = false;
                    set_status(msg, !success);
                });
            } else {
                // Step 2: Submit new password
                if (new_pw.length() < 8) {
                    set_status("New password must be at least 8 characters.", true);
                    return;
                }
                m_is_loading = true;
                set_status("Updating password on Sangha Cloud...", false);

                AccountSystem::instance().reset_password(token, new_pw, [this](bool success, const std::string& msg) {
                    m_is_loading = false;
                    set_status(msg, !success);
                    if (success) {
                        m_active_tab = 0; // Switch to login
                        setup_inputs();
                    }
                });
            }
        }
    }

    void set_status(const std::string& msg, bool is_error) {
        m_status_msg = msg;
        m_status_is_error = is_error;
    }

    void draw() override {
        ClearBackground(COLOR_OBSIDIAN);
        Font title_font = AssetManager::instance().title_font();
        Font body_font = AssetManager::instance().body_font();

        // Header Panel
        UI::DrawChamferedPanel({ 30, 15, 840, 50 }, COLOR_GOLD, COLOR_SURFACE_LOW, 6.0f);
        DrawTextEx(title_font, "SANGHA ASTRAL PILOT NETWORK // CLOUD COMMAND", { 45, 25 }, 20, 1.0f, COLOR_GOLD_BRIGHT);

        // Tab Navigation Bar
        m_btn_tab_login.draw(title_font);
        m_btn_tab_register.draw(title_font);
        m_btn_tab_verify.draw(title_font);
        m_btn_tab_reset.draw(title_font);

        // Main Form Card
        Rectangle card = { SCREEN_WIDTH / 2.0f - 240, 125, 480, 380 };
        Color card_border = (m_active_tab == 0) ? COLOR_GOLD_BRIGHT :
                            (m_active_tab == 1) ? COLOR_CYAN_BRIGHT :
                            (m_active_tab == 2) ? COLOR_GREEN_BRIGHT : COLOR_ORANGE_BRIGHT;
        UI::DrawChamferedPanel(card, card_border, COLOR_SURFACE_LOW, 8.0f);

        // Render Input Fields
        for (const auto& input : m_inputs) {
            input.draw(body_font, m_show_password, m_blink_timer);
        }

        // Show password toggle button on Login & Register tabs
        if (m_active_tab == 0 || m_active_tab == 1) {
            m_btn_toggle_pw.draw(body_font);
        }

        // Action Buttons
        m_btn_submit.draw(title_font);
        if (m_active_tab == 0 || m_active_tab == 1) {
            m_btn_guest.draw(title_font);
        }

        // Status / Feedback Banner
        if (!m_status_msg.empty()) {
            Color stat_col = m_status_is_error ? COLOR_RED_BRIGHT : (m_is_loading ? COLOR_CYAN_BRIGHT : COLOR_GREEN_BRIGHT);
            Vector2 sz = MeasureTextEx(body_font, m_status_msg.c_str(), 12, 1.0f);
            float msg_x = std::max(card.x + 10.0f, (SCREEN_WIDTH - sz.x) / 2.0f);
            float msg_y = (m_active_tab == 1) ? 352.0f : (m_active_tab == 0 ? 320.0f : 280.0f);
            DrawTextEx(body_font, m_status_msg.c_str(), { msg_x, msg_y }, 12, 1.0f, stat_col);
        }

        // Bottom Navigation
        m_btn_back.draw(title_font);

        // Cloud Server Indicator in bottom right
        std::string srv_info = "SERVER: " + AccountSystem::instance().api_base();
        DrawText(srv_info.c_str(), SCREEN_WIDTH - 300, 535, 10, COLOR_MUTED);

        if (g_scanlines_enabled) UI::DrawScanlines();
    }

    ViewType next_view() const override { return m_next_view; }
    void reset_next_view() override { m_next_view = ViewType::AUTH; }

private:
    ViewType m_next_view;
    int m_active_tab;
    bool m_show_password;
    float m_blink_timer;
    std::string m_status_msg;
    bool m_status_is_error;
    bool m_is_loading;

    std::vector<InputField> m_inputs;

    UI::Button m_btn_tab_login;
    UI::Button m_btn_tab_register;
    UI::Button m_btn_tab_verify;
    UI::Button m_btn_tab_reset;
    UI::Button m_btn_submit;
    UI::Button m_btn_guest;
    UI::Button m_btn_toggle_pw;
    UI::Button m_btn_back;
};

} // namespace Vimana
