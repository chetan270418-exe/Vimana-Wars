"""Account and stable Game ID screen.

The game remains playable as a guest, but this view lets a player link a
stable Vimana Wars identity to online leaderboard submissions. Network work
is delegated to ``LeaderboardClient`` so the Arcade render thread never
blocks while a server is unavailable.
"""
import arcade

from constants import WIDTH, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.systems.sound_manager import SoundManager
from game.ui.menu_button import MenuButton
from game.ui.nav_rail import NavRail
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
        self._nav_rail = NavRail(current_screen="account")

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

        self._buttons = self._build_buttons()

    def _build_buttons(self):
        cx = (240 + WIDTH - 90) // 2  # 525
        if leaderboard_client.current_account():
            data = [
                ("SIGN OUT OF ASTRAL NETWORK", "logout", RED_BRIGHT, 300, 38, 145),
                ("BACK TO COMMAND DECK", "back", CYAN, 240, 32, 100),
            ]
        elif self._mode == "reset_request":
            data = [
                ("SEND RECOVERY TOKEN  ▶", "submit", GOLD, 290, 38, 140),
                ("RETURN TO SIGN IN", "login", CYAN, 250, 32, 95),
            ]
        elif self._mode == "reset_password":
            data = [
                ("UPDATE PASSWORD  ▶", "submit", GOLD, 290, 38, 140),
                ("RETURN TO SIGN IN", "login", CYAN, 250, 32, 95),
            ]
        elif self._mode == "verify":
            data = [
                ("CONFIRM VERIFICATION  ▶", "submit", CYAN, 290, 38, 140),
                ("RETURN TO SIGN IN", "login", MUTED, 250, 32, 95),
            ]
        elif self._mode == "register":
            data = [
                ("CREATE ASTRAL IDENTITY  ▶", "submit", GOLD, 310, 38, 145),
                ("ALREADY REGISTERED? SIGN IN", "login", CYAN, 280, 32, 100),
            ]
        else:  # login
            data = [
                ("SIGN IN TO WARSHIP  ▶", "submit", GOLD, 290, 38, 145),
                ("NEED AN ACCOUNT? CREATE ONE", "register", CYAN, 290, 32, 100),
                ("FORGOT PASSWORD / RECOVERY", "reset_request", MUTED, 240, 26, 62),
            ]

        buttons = []
        for label, action, color, w, h, y in data:
            buttons.append((MenuButton(label, cx, y, w, h, color), action))
        return buttons

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
        self._nav_rail.update(delta_time)
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
        arcade.draw_lrbt_rectangle_filled(240, WIDTH - 90, 50, 490, (9, 14, 25, 240))
        draw_chamfered_panel(240, WIDTH - 90, 50, 490, CYAN,
                             fill=OBSIDIAN, alpha=240, border_width=1, cut=16)
        draw_corner_etching(240, WIDTH - 90, 50, 490, GOLD, length=20, alpha=130)
        # Slow scan line gives the account console a little life.
        scan_y = 65 + ((self._pulse * 24) % 410)
        arcade.draw_lrbt_rectangle_filled(265, WIDTH - 115, scan_y, scan_y + 1, (80, 210, 255, 30))

    def _draw_tabs(self) -> None:
        tabs = [("SIGN IN", "login"), ("CREATE ACCOUNT", "register"), ("RECOVERY", "reset_request"), ("PILOT CARD", "profile")]
        cx = (240 + WIDTH - 90) // 2
        tab_start_x = cx - 180
        for i, (t_label, t_mode) in enumerate(tabs):
            tx = tab_start_x + i * 120
            if leaderboard_client.current_account():
                active = (t_mode == "profile")
            else:
                active = (self._mode == t_mode or (t_mode == "login" and self._mode not in ("register", "reset_request", "reset_password", "verify", "profile")))
            col = GOLD_BRIGHT if active else MUTED
            arcade.draw_text(t_label, tx, 452, col, font_size=10, bold=True, anchor_x="center", font_name=FONT_INTERFACE)
            if active:
                arcade.draw_line(tx - 35, 442, tx + 35, 442, GOLD, 2)

    def _get_fields(self):
        cx = (240 + WIDTH - 90) // 2  # 525
        w = 420
        left = cx - w // 2
        right = cx + w // 2

        if self._mode == "register":
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 370, 404), False, "Used to link your permanent Game ID"),
                (1, "PASSWORD (MIN 8 CHARS)", "•" * len(self._password) if self._password else "", (left, right, 305, 339), True, "Secured on celestial server"),
                (2, "WARRIOR CALLSIGN", self._player_name, (left, right, 240, 274), False, "Displayed on the global leaderboard"),
            ]
        elif self._mode == "reset_request":
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 340, 376), False, "A reset token will be delivered to your inbox"),
            ]
        elif self._mode == "reset_password":
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 370, 404), False, "Registered email address"),
                (1, "RESET TOKEN", self._reset_token, (left, right, 305, 339), False, "Paste token received in email"),
                (2, "NEW PASSWORD", "•" * len(self._password) if self._password else "", (left, right, 240, 274), True, "Minimum 8 characters"),
            ]
        elif self._mode == "verify":
            return [
                (0, "VERIFICATION TOKEN", self._verify_token, (left, right, 340, 376), False, "Enter token delivered by email"),
            ]
        else:  # login
            return [
                (0, "EMAIL ADDRESS", self._email, (left, right, 350, 386), False, "Registered pilot email"),
                (1, "PASSWORD", "•" * len(self._password) if self._password else "", (left, right, 270, 306), True, "Account password"),
            ]

    def _draw_profile(self, account: dict) -> None:
        draw_chamfered_panel(540, 840, 160, 410, GOLD, fill=SURFACE_LOW, alpha=245, cut=9)
        draw_corner_etching(540, 840, 160, 410, GOLD, length=12, alpha=100)
        
        arcade.draw_text("PILOT CARD", 690, 380, GOLD_BRIGHT, font_size=14, bold=True, anchor_x="center")
        arcade.draw_text("WARRIOR DESIGNATION", 690, 340, MUTED, font_size=8, bold=True, anchor_x="center")
        arcade.draw_text(account.get("player_name", "Warrior").upper(), 690, 315, PARCHMENT, font_size=16, bold=True, anchor_x="center")
        
        arcade.draw_text("GAME ID", 690, 270, MUTED, font_size=8, bold=True, anchor_x="center")
        arcade.draw_text(account.get("game_id", "—"), 690, 245, CYAN_BRIGHT, font_size=20, bold=True, anchor_x="center")
        
        stats = self._account_stats or {}
        score = int(stats.get('best_score', 0))
        arcade.draw_text(f"TOTAL SCORE: {score:,}", 690, 190, GOLD, font_size=10, bold=True, anchor_x="center")

        arcade.draw_text("ASTRAL IDENTITY ACTIVE", 390, 300, CYAN_BRIGHT, font_size=14, bold=True, anchor_x="center")

    def _draw_form(self) -> None:
        fields = self._get_fields()
        for i, label, value, (left, right, bottom, top), is_pwd, hint in fields:
            selected = self._selected_field == i
            accent = CYAN_BRIGHT if selected else (65, 90, 125)
            fill = SURFACE_HIGH if selected else SURFACE_LOW
            arcade.draw_text(label, left, top + 5, accent, font_size=8, bold=True)
            draw_chamfered_panel(left, right, bottom, top, accent,
                                 fill=fill, alpha=245, border_width=2 if selected else 1, cut=6)
            shown = value or "TYPE HERE"
            shown_color = PARCHMENT if value else MUTED
            arcade.draw_text(shown, left + 14, bottom + 10, shown_color, font_size=11)
            if selected and hint:
                arcade.draw_text(hint, left, bottom - 14, (110, 135, 165), font_size=7)

    def on_draw(self) -> None:
        self._draw_background()
        self._title.draw()
        self._subtitle.draw()
        self._draw_tabs()
        account = leaderboard_client.current_account()
        if account:
            self._draw_profile(account)
        else:
            self._draw_form()
        if self._status_msg:
            msg_lower = self._status_msg.lower()
            if "error" in msg_lower or "fail" in msg_lower or "required" in msg_lower:
                pill_color = (220, 50, 50)
            elif "success" in msg_lower or "registered" in msg_lower or "signed in" in msg_lower or "secured" in msg_lower or "linked" in msg_lower or "verified" in msg_lower or "ready" in msg_lower:
                pill_color = (50, 200, 100)
            else:
                pill_color = (200, 180, 50)
            
            w = len(self._status_msg) * 6.5 + 40
            cx, cy = (240 + WIDTH - 90) // 2, 195
            draw_chamfered_panel(cx - w//2, cx + w//2, cy - 12, cy + 12, pill_color, fill=(*pill_color[:3], 40), alpha=255, cut=6)
            
            self._status_text.text = self._status_msg
            self._status_text.color = pill_color
            self._status_text.x = cx
            self._status_text.y = cy
            self._status_text.draw()
        for button, _ in self._buttons:
            button.draw()
        self._hint.draw()
        self._nav_rail.draw()
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
        elif action == "submit":
            self._submit()
        elif action in ("login", "switch_login"):
            self._mode = "login"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action in ("register", "switch_register"):
            self._mode = "register"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action in ("reset_request", "switch_reset"):
            self._mode = "reset_request"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action == "reset_password":
            self._mode = "reset_password"
            self._selected_field = 1
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action == "verify":
            self._mode = "verify"
            self._selected_field = 0
            self._status_msg = ""
            self._buttons = self._build_buttons()
        elif action == "logout":
            self._submitting = True
            self._status_msg = "SIGNING OUT..."
            self._status_color = MUTED

            def on_done(error):
                self._pending_logout = (error,)

            leaderboard_client.logout(on_done)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._nav_rail.on_mouse_motion(x, y)
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
        nav = self._nav_rail.on_mouse_press(x, y, self.window)
        if nav:
            return
        
        # Tab selection
        if 430 <= y <= 475:
            cx = (240 + WIDTH - 90) // 2
            tab_start_x = cx - 180
            for i, t_mode in enumerate(["login", "register", "reset_request", "profile"]):
                tx = tab_start_x + i * 120
                if tx - 55 <= x <= tx + 55:
                    if t_mode in ("login", "register", "reset_request"):
                        self.sound_manager.play_ui_click()
                        self._activate(t_mode)
                    return
                    
        account = leaderboard_client.current_account()
        if not account:
            for i, label, value, (left, right, bottom, top), is_pwd, hint in self._get_fields():
                if left <= x <= right and bottom <= y <= top:
                    self._selected_field = i
                    self.sound_manager.play_ui_click(volume=0.2)
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
        fields = self._get_fields()
        num_fields = len(fields) if fields else 1
        if key in (arcade.key.TAB, arcade.key.DOWN):
            self._selected_field = (self._selected_field + 1) % num_fields
        elif key in (arcade.key.UP,):
            self._selected_field = (self._selected_field - 1) % num_fields
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
        elif self._selected_field == 2:
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
