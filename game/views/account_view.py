"""Account and stable Game ID screen.

The game remains playable as a guest, but this view lets a player link a
stable Vimana Wars identity to online leaderboard submissions. Network work
is delegated to ``LeaderboardClient`` so the Arcade render thread never
blocks while a server is unavailable.
"""
import arcade

from constants import WIDTH, HEIGHT, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.systems.sound_manager import SoundManager
from game.ui.menu_button import MenuButton
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT, CYAN,
    CYAN_BRIGHT, PARCHMENT, MUTED, RED_BRIGHT,
    draw_chamfered_panel, draw_corner_etching,
)


class AccountView(arcade.View):
    """Email account registration/login and local profile display."""

    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self.sound_manager = SoundManager()
        saved = save_system.load()
        self._email = saved.get("account_email", "")
        self._password = ""
        self._player_name = saved.get("player_name", "Warrior")
        self._mode = "login"
        self._reset_token = ""
        self._verify_token = ""
        self._selected_field = 0
        self._submitting = False
        self._pending_result = None
        self._pending_logout = None
        self._pending_stats = None
        self._pending_action = None
        self._account_stats = None
        self._status_msg = ""
        self._status_color = MUTED
        self._hovered = -1
        self._pulse = 0.0

        self._title = arcade.Text(
            "ACCOUNT // ASTRAL IDENTITY", WIDTH // 2, 548,
            GOLD_BRIGHT, font_size=25, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._subtitle = arcade.Text(
            "LINK YOUR WARSHIP TO A PERMANENT VIMANA WARS GAME ID",
            WIDTH // 2, 516, CYAN_BRIGHT, font_size=10, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, 105, MUTED, font_size=11, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "TAB / ↑↓ : FIELD   •   ENTER : CONFIRM   •   ESC : BACK",
            WIDTH // 2, 32, MUTED, font_size=10,
            anchor_x="center", anchor_y="center",
        )

        self._field_rects = [
            (300, 420, 470, 455),
            (300, 420, 390, 425),
            (300, 420, 310, 345),
        ]
        self._buttons = self._build_buttons()

    def _build_buttons(self):
        if leaderboard_client.current_account():
            data = [("SIGN OUT", "logout", RED_BRIGHT), ("BACK", "back", CYAN)]
        elif self._mode == "reset_request":
            data = [
                ("SEND RESET CODE", "reset_request", GOLD),
                ("SIGN IN", "login", CYAN),
                ("CREATE ACCOUNT", "register", MUTED),
                ("BACK", "back", MUTED),
            ]
        elif self._mode == "reset_password":
            data = [
                ("SET NEW PASSWORD", "reset_password", GOLD),
                ("RESET REQUEST", "reset_request", CYAN),
                ("SIGN IN", "login", MUTED),
                ("BACK", "back", MUTED),
            ]
        elif self._mode == "verify":
            data = [
                ("VERIFY EMAIL", "verify", CYAN),
                ("SIGN IN", "login", MUTED),
                ("BACK", "back", MUTED),
            ]
        else:
            data = [
                ("SIGN IN", "login", CYAN),
                ("CREATE ACCOUNT", "register", GOLD),
                ("RESET PASSWORD", "reset_request", (180, 150, 255)),
                ("BACK", "back", MUTED),
            ]
        y_values = ((180, 135, 90, 45) if len(data) == 4 else
                    (180, 135, 78) if len(data) == 3 and self._mode == "verify" else
                    (155, 95))
        return [
            (MenuButton(label, WIDTH // 2, y_values[i], 225 if i == 1 and len(data) == 3 else 190, 34, color), action)
            for i, (label, action, color) in enumerate(data)
        ]

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        self._buttons = self._build_buttons()
        self._hovered = -1
        self._account_stats = None
        if leaderboard_client.current_account():
            def on_stats(stats, error):
                self._pending_stats = (stats, error)
            leaderboard_client.fetch_account_stats(on_stats)
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        for i, (button, _) in enumerate(self._buttons):
            button.update(delta_time, i == self._hovered)
        if self._pending_result is not None:
            result = self._pending_result
            self._pending_result = None
            self._submitting = False
            success, error, user = result
            if success and user:
                self._password = ""
                if user.get("verification_required") and not leaderboard_client.current_account():
                    self._mode = "verify"
                    self._selected_field = 0
                    self._verify_token = user.get("verification_token", "")
                    self._status_msg = "ACCOUNT CREATED — ENTER THE VERIFICATION TOKEN FROM YOUR EMAIL"
                    if user.get("verification_token"):
                        self._status_msg += f"  •  DEV TOKEN {user['verification_token']}"
                else:
                    self._status_msg = f"ACCOUNT LINKED  •  GAME ID {user.get('game_id', '')}"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            else:
                self._status_msg = error or "Account request failed"
                self._status_color = RED_BRIGHT
        if self._pending_logout is not None:
            (error,) = self._pending_logout
            self._pending_logout = None
            self._submitting = False
            self._status_msg = error or "SIGNED OUT — guest mode active"
            self._status_color = MUTED if error else CYAN_BRIGHT
            self._buttons = self._build_buttons()
        if self._pending_stats is not None:
            stats, error = self._pending_stats
            self._pending_stats = None
            self._account_stats = stats or {}
            if error and not self._status_msg:
                self._status_msg = error
                self._status_color = MUTED
        if self._pending_action is not None:
            success, error, body = self._pending_action
            self._pending_action = None
            self._submitting = False
            if success and self._mode == "reset_request":
                self._mode = "reset_password"
                self._selected_field = 2
                if body.get("reset_token"):
                    self._reset_token = body["reset_token"]
                    self._status_msg = "RESET CODE READY — set a new password below"
                else:
                    self._status_msg = "RESET INSTRUCTIONS CREATED — check your email"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            elif success and self._mode == "reset_password":
                self._mode = "login"
                self._password = ""
                self._reset_token = ""
                self._selected_field = 1
                self._status_msg = "PASSWORD UPDATED — sign in with your new password"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            elif success and self._mode == "verify":
                self._mode = "login"
                self._selected_field = 1
                self._status_msg = "EMAIL VERIFIED — ACCOUNT LINKED"
                self._status_color = CYAN_BRIGHT
                self._buttons = self._build_buttons()
            elif not success:
                self._status_msg = error or "Account action failed"
                self._status_color = RED_BRIGHT

    def _draw_background(self) -> None:
        self.clear()
        arcade.draw_lrbt_rectangle_filled(90, WIDTH - 90, 75, 490, (9, 14, 25, 235))
        draw_chamfered_panel(90, WIDTH - 90, 75, 490, CYAN,
                             fill=OBSIDIAN, alpha=235, border_width=1, cut=16)
        draw_corner_etching(90, WIDTH - 90, 75, 490, GOLD, length=20, alpha=130)
        # Slow scan line gives the account console a little life.
        scan_y = 95 + ((self._pulse * 24) % 370)
        arcade.draw_lrbt_rectangle_filled(115, WIDTH - 115, scan_y, scan_y + 1, (80, 210, 255, 35))

    def _draw_profile(self, account: dict) -> None:
        arcade.draw_text("ACCOUNT LINKED", WIDTH // 2, 430, CYAN_BRIGHT,
                         font_size=14, bold=True, anchor_x="center")
        arcade.draw_text("Your online records are attached to this identity.",
                         WIDTH // 2, 400, PARCHMENT, font_size=11,
                         anchor_x="center")
        draw_chamfered_panel(255, 645, 235, 365, CYAN,
                             fill=SURFACE_LOW, alpha=245, cut=9)
        arcade.draw_text("GAME ID", 285, 340, MUTED, font_size=9, bold=True)
        arcade.draw_text(account.get("game_id", "—"), 285, 315,
                         GOLD_BRIGHT, font_size=22, bold=True)
        arcade.draw_text("WARRIOR", 285, 280, MUTED, font_size=9, bold=True)
        arcade.draw_text(account.get("player_name", "Warrior"), 285, 257,
                         PARCHMENT, font_size=14, bold=True)
        arcade.draw_text("EMAIL", 285, 220, MUTED, font_size=9, bold=True)
        arcade.draw_text(account.get("email", "—"), 285, 198,
                         PARCHMENT, font_size=11)
        stats = self._account_stats or {}
        arcade.draw_text(
            f"ONLINE RUNS  {stats.get('games', 0)}    BEST SCORE  {int(stats.get('best_score', 0)):,}    BEST WAVE  {stats.get('best_wave', 0)}",
            WIDTH // 2, 175, CYAN, font_size=9, bold=True, anchor_x="center",
        )

    def _draw_form(self) -> None:
        is_register = self._mode == "register"
        title = ("CREATE A NEW ACCOUNT" if is_register else
                 "RESET PASSWORD" if self._mode in ("reset_request", "reset_password") else
                 "VERIFY EMAIL" if self._mode == "verify" else
                 "SIGN IN TO YOUR ACCOUNT")
        arcade.draw_text(title,
                         WIDTH // 2, 455, GOLD, font_size=14, bold=True,
                         anchor_x="center")
        if self._mode == "verify":
            labels = ["VERIFICATION TOKEN", "", ""]
            values = [self._verify_token, "", ""]
        elif self._mode == "reset_request":
            labels = ["EMAIL ADDRESS", "PASSWORD", "WARRIOR NAME"]
            values = [self._email, "", ""]
        elif self._mode == "reset_password":
            labels = ["EMAIL ADDRESS", "RESET TOKEN", "NEW PASSWORD"]
            values = [self._email, self._reset_token, "•" * len(self._password)]
        else:
            labels = ["EMAIL ADDRESS", "PASSWORD", "WARRIOR NAME"]
            values = [self._email, "•" * len(self._password), self._player_name]
        for i, ((left, right, bottom, top), label, value) in enumerate(
                zip(self._field_rects, labels, values)):
            visible = ((is_register or self._mode == "register") or
                       (self._mode == "reset_password") or
                       (self._mode == "verify" and i == 0) or
                       (self._mode == "login" and i < 2) or
                       (self._mode == "reset_request" and i == 0))
            if not visible:
                continue
            selected = self._selected_field == i
            accent = GOLD_BRIGHT if selected else (65, 90, 125)
            fill = SURFACE_HIGH if selected else SURFACE_LOW
            draw_chamfered_panel(left, right, bottom, top, accent,
                                 fill=fill, alpha=245, border_width=2 if selected else 1, cut=6)
            arcade.draw_text(label, left + 14, top + 8, accent,
                             font_size=8, bold=True)
            shown = value or "TYPE HERE"
            shown_color = PARCHMENT if value else MUTED
            arcade.draw_text(shown, left + 14, bottom + 10, shown_color,
                             font_size=12)

        if self._mode == "verify":
            arcade.draw_text("Use the one-time token from your verification email.",
                             WIDTH // 2, 285, MUTED, font_size=9, anchor_x="center")
        elif self._mode == "reset_request":
            arcade.draw_text("A reset token will be delivered by the configured email provider.",
                             WIDTH // 2, 285, MUTED, font_size=9, anchor_x="center")
        elif self._mode == "reset_password":
            arcade.draw_text("Paste the one-time token from your email, then choose a new password.",
                             WIDTH // 2, 285, MUTED, font_size=9, anchor_x="center")
        elif not is_register:
            arcade.draw_text("Need an account? Choose CREATE ACCOUNT below.",
                             WIDTH // 2, 285, MUTED, font_size=9,
                             anchor_x="center")
        else:
            arcade.draw_text("Minimum 8 characters • Your password is never stored locally.",
                             WIDTH // 2, 285, MUTED, font_size=9,
                             anchor_x="center")

    def on_draw(self) -> None:
        self._draw_background()
        self._title.draw()
        self._subtitle.draw()
        account = leaderboard_client.current_account()
        if account:
            self._draw_profile(account)
        else:
            self._draw_form()
        if self._status_msg:
            self._status_text.text = self._status_msg
            self._status_text.color = self._status_color
            self._status_text.draw()
        for button, _ in self._buttons:
            button.draw()
        self._hint.draw()
        TransitionOverlay.draw()

    def _back(self) -> None:
        if TransitionOverlay.is_active:
            return
        self.sound_manager.play_ui_click()
        target = self.return_view
        if target is None:
            from game.views.menu_view import MenuView
            target = MenuView()
        transition_to(self.window, target)

    def _submit(self) -> None:
        if self._submitting:
            return
        email = self._email.strip()
        password = self._password
        if self._mode == "verify":
            if not self._verify_token:
                self._status_msg = "Verification token is required"
                self._status_color = RED_BRIGHT
                return
        elif self._mode == "reset_request":
            if not email:
                self._status_msg = "Email is required"
                self._status_color = RED_BRIGHT
                return
        elif self._mode == "reset_password":
            if not self._reset_token or not password:
                self._status_msg = "Reset token and new password are required"
                self._status_color = RED_BRIGHT
                return
            if len(password) < 8:
                self._status_msg = "Password must be at least 8 characters"
                self._status_color = RED_BRIGHT
                return
        elif not email or not password:
            self._status_msg = "Email and password are required"
            self._status_color = RED_BRIGHT
            return
        if self._mode == "register" and len(password) < 8:
            self._status_msg = "Password must be at least 8 characters"
            self._status_color = RED_BRIGHT
            return
        self._submitting = True
        self._status_msg = "CONTACTING ASTRAL IDENTITY SERVER..."
        self._status_color = CYAN_BRIGHT

        def on_done(success, error, user):
            self._pending_result = (success, error, user)

        def on_action_done(success, error, body):
            # Only queue data here; on_update owns all visible UI changes.
            self._pending_action = (success, error, body)

        if self._mode == "register":
            leaderboard_client.register(email, password, self._player_name.strip() or "Warrior", on_done)
        elif self._mode == "login":
            leaderboard_client.login(email, password, on_done)
        elif self._mode == "reset_request":
            leaderboard_client.request_password_reset(email, on_action_done)
        elif self._mode == "reset_password":
            leaderboard_client.reset_password(self._reset_token, password, on_action_done)
        elif self._mode == "verify":
            leaderboard_client.verify_email(self._verify_token, on_action_done)

    def _activate(self, action: str) -> None:
        if action == "back":
            self._back()
        elif action == "login":
            self._mode = "login"
            self._selected_field = min(self._selected_field, 1)
            self._status_msg = ""
        elif action == "register":
            self._mode = "register"
            self._selected_field = min(self._selected_field, 2)
            self._status_msg = ""
        elif action == "reset_request":
            self._mode = "reset_request"
            self._selected_field = 0
            self._status_msg = ""
        elif action == "reset_password":
            self._mode = "reset_password"
            self._selected_field = 2
            self._status_msg = ""
        elif action == "verify":
            self._mode = "verify"
            self._selected_field = 0
            self._status_msg = ""
        elif action == "logout":
            self._submitting = True
            self._status_msg = "SIGNING OUT..."
            self._status_color = MUTED

            def on_done(error):
                # Defer all view/UI mutation to on_update on the Arcade thread.
                self._pending_logout = (error,)

            leaderboard_client.logout(on_done)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        new_hovered = -1
        for i, (button, _) in enumerate(self._buttons):
            if button.contains(x, y):
                new_hovered = i
                break
        if new_hovered != self._hovered and new_hovered >= 0:
            self.sound_manager.play_ui_click(volume=0.18)
        self._hovered = new_hovered

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if button != arcade.MOUSE_BUTTON_LEFT or self._submitting:
            return
        account = leaderboard_client.current_account()
        if not account:
            for i, rect in enumerate(self._field_rects):
                visible = (self._mode == "register" or self._mode == "reset_password" or
                           self._mode == "verify" or
                           (self._mode == "login" and i < 2) or
                           (self._mode == "reset_request" and i == 0))
                if not visible:
                    continue
                left, right, bottom, top = rect
                if left <= x <= right and bottom <= y <= top:
                    self._selected_field = i
                    return
        for i, (menu_button, action) in enumerate(self._buttons):
            if menu_button.contains(x, y):
                self._hovered = i
                self.sound_manager.play_ui_click()
                self._activate(action)
                return

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            self._back()
            return
        if self._submitting or leaderboard_client.current_account():
            return
        if key in (arcade.key.TAB, arcade.key.DOWN, arcade.key.RIGHT):
            max_field = (2 if self._mode in ("register", "reset_password") else
                         0 if self._mode in ("reset_request", "verify") else 1)
            self._selected_field = (self._selected_field + 1) % (max_field + 1)
        elif key in (arcade.key.UP, arcade.key.LEFT):
            max_field = (2 if self._mode in ("register", "reset_password") else
                         0 if self._mode in ("reset_request", "verify") else 1)
            self._selected_field = (self._selected_field - 1) % (max_field + 1)
        elif key in (arcade.key.ENTER, arcade.key.RETURN):
            self._submit()
        elif key == arcade.key.F1:
            self._activate("login")
        elif key == arcade.key.F2:
            self._activate("register")
        elif key == arcade.key.BACKSPACE:
            self._delete_character()

    def _delete_character(self) -> None:
        if self._selected_field == 0:
            if self._mode == "verify":
                self._verify_token = self._verify_token[:-1]
            else:
                self._email = self._email[:-1]
        elif self._selected_field == 1:
            if self._mode == "reset_password":
                self._reset_token = self._reset_token[:-1]
            else:
                self._password = self._password[:-1]
        else:
            if self._mode == "reset_password":
                self._password = self._password[:-1]
            else:
                self._player_name = self._player_name[:-1]

    def on_text(self, text: str) -> None:
        if self._submitting or leaderboard_client.current_account() or not text.isprintable():
            return
        if self._selected_field == 0:
            if self._mode == "verify" and len(self._verify_token) < 128:
                self._verify_token += text
            elif self._mode != "verify" and len(self._email) < 254:
                self._email += text
        elif self._selected_field == 1 and len(self._password) < 128:
            if self._mode == "reset_password":
                self._reset_token += text
            else:
                self._password += text
        elif self._selected_field == 2:
            if self._mode == "reset_password" and len(self._password) < 128:
                self._password += text
            elif self._mode != "reset_password" and len(self._player_name) < 20:
                self._player_name += text

    def on_joyhat_motion(self, joystick, hat_x, hat_y) -> None:
        if hat_y or hat_x:
            self.on_key_press(arcade.key.DOWN if (hat_y < 0 or hat_x > 0) else arcade.key.UP, 0)

    def on_joybutton_press(self, joystick, button) -> None:
        if button == 0:
            self._submit()
        elif button in (1, 4):
            self._back()
