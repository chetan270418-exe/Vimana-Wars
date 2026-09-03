"""
game/views/leaderboard_view.py
In-game Online Leaderboard screen.
Fetches top scores from the backend API asynchronously.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.systems.leaderboard_client import leaderboard_client
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import MUTED, CYAN_BRIGHT, draw_menu_backdrop, draw_focus_panel


_FILTERS = ["all", "easy", "normal", "hard", "endless"]
_FILTER_LABELS = {
    "all":    "ALL DIFFICULTIES",
    "easy":   "EASY",
    "normal": "NORMAL",
    "hard":   "HARD",
    "endless": "ENDLESS MAHAYUDDHA",
}


class LeaderboardView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._filter_index = 0
        self._pulse = 0.0

        # UI Text elements
        self._title = arcade.Text(
            "GLOBAL LEADERBOARD",
            WIDTH // 2, HEIGHT - 50,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._tab_hint = arcade.Text(
            "TAB / ← → : Filter   •   R : Refresh   •   ESC : Back",
            WIDTH // 2, 28,
            (160, 160, 190), font_size=11, bold=True,
            anchor_x="center",
        )
        self._status_text = arcade.Text(
            "Loading scores...", WIDTH // 2, HEIGHT // 2,
            COLOR_WHITE, font_size=14,
            anchor_x="center", anchor_y="center",
        )

        # Pre-built rows text cache
        self._row_texts: list[list[arcade.Text]] = []
        self._current_filter_text = arcade.Text(
            "", WIDTH // 2, HEIGHT - 95,
            COLOR_WAVE, font_size=13, bold=True,
            anchor_x="center",
        )

        # Trigger initial fetch
        self._refresh()

    def _refresh(self) -> None:
        selected_diff = _FILTERS[self._filter_index]
        diff_arg = None if selected_diff == "all" else selected_diff
        self._status_text.text = "Contacting realm archive..."
        self._current_filter_text.text = f"«  {_FILTER_LABELS[selected_diff]}  »"
        
        leaderboard_client.fetch_top(
            limit=10,
            difficulty=diff_arg,
            on_complete=self._on_fetch_complete
        )

    def _on_fetch_complete(self, scores: list[dict], error: str | None) -> None:
        # Save raw data thread-safely; build Arcade OpenGL Text on the main thread in on_update
        self._pending_data = (scores, error)

    def _apply_fetch_results(self, scores: list[dict], error: str | None) -> None:
        self._row_texts.clear()

        if error:
            self._status_text.text = f"{error}\n(Run 'python backend/app.py' to host online server)"
            return

        if not scores:
            self._status_text.text = "No heroic deeds recorded yet in this category."
            return

        self._status_text.text = ""

        # Build table rows
        rank_colors = [
            (255, 215, 0),   # 1st Gold
            (210, 215, 230), # 2nd Silver
            (205, 127, 50),  # 3rd Bronze
        ]

        start_y = HEIGHT - 150
        row_height = 36

        for i, row in enumerate(scores):
            y = start_y - i * row_height
            rank_color = rank_colors[i] if i < 3 else (180, 180, 200)
            
            rank_str = f"#{row['rank']}"
            name_str = row['player_name']
            game_id_str = row.get('game_id') or "GUEST"
            score_str = f"{row['score']:,}"
            wave_str = f"W{row['level_reached']}"
            diff_str = row.get('difficulty', 'normal').upper()

            t_rank = arcade.Text(rank_str, 90, y, rank_color, font_size=13, bold=True)
            t_name = arcade.Text(name_str, 160, y + 6, COLOR_WHITE, font_size=12, bold=(i < 3))
            t_game_id = arcade.Text(game_id_str, 160, y - 8,
                                    CYAN_BRIGHT if game_id_str != "GUEST" else MUTED,
                                    font_size=8, bold=game_id_str != "GUEST")
            t_score = arcade.Text(score_str, WIDTH - 260, y, COLOR_SCORE, font_size=13, bold=True, anchor_x="right")
            t_wave = arcade.Text(wave_str, WIDTH - 160, y, (120, 200, 255), font_size=12, anchor_x="center")
            t_diff = arcade.Text(diff_str, WIDTH - 80, y, (160, 160, 170), font_size=11, anchor_x="right")

            self._row_texts.append([t_rank, t_name, t_game_id, t_score, t_wave, t_diff])

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._pulse += delta_time
        pending = getattr(self, "_pending_data", None)
        if pending is not None:
            self._pending_data = None
            scores, error = pending
            self._apply_fetch_results(scores, error)

    def on_draw(self) -> None:
        draw_menu_backdrop("GLOBAL LEADERBOARD", "ONLINE ARCHIVE // LOCAL PLAY REMAINS AVAILABLE OFFLINE", COLOR_SCORE, pulse=self._pulse)
        self._title.draw()
        self._current_filter_text.draw()

        # Header bar
        header_y = HEIGHT - 122
        draw_focus_panel(70, WIDTH - 70, header_y - 6, header_y + 18, COLOR_WAVE)
        arcade.draw_text("RANK", 90, header_y, (120, 140, 180), font_size=10, bold=True)
        arcade.draw_text("WARRIOR / GAME ID", 160, header_y, (120, 140, 180), font_size=10, bold=True)
        arcade.draw_text("SCORE", WIDTH - 260, header_y, (120, 140, 180), font_size=10, bold=True, anchor_x="right")
        arcade.draw_text("WAVE", WIDTH - 160, header_y, (120, 140, 180), font_size=10, bold=True, anchor_x="center")
        arcade.draw_text("DIFFICULTY", WIDTH - 80, header_y, (120, 140, 180), font_size=10, bold=True, anchor_x="right")

        # Table rows or status
        if self._status_text.text:
            self._status_text.draw()
        else:
            for i, row in enumerate(self._row_texts):
                row_y = HEIGHT - 150 - i * 36
                # Alternating row background highlight
                if i % 2 == 1:
                    arcade.draw_lrbt_rectangle_filled(70, WIDTH - 70, row_y - 8, row_y + 20, (12, 12, 30, 80))
                for cell in row:
                    cell.draw()

        self._tab_hint.draw()
        TransitionOverlay.draw()

    def on_key_press(self, key, modifiers) -> None:
        if key in (arcade.key.TAB, arcade.key.RIGHT, arcade.key.D):
            self._filter_index = (self._filter_index + 1) % len(_FILTERS)
            self._refresh()
        elif key in (arcade.key.LEFT, arcade.key.A):
            self._filter_index = (self._filter_index - 1) % len(_FILTERS)
            self._refresh()
        elif key == arcade.key.R:
            self._refresh()
        elif key == arcade.key.ESCAPE:
            if self.return_view:
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                transition_to(self.window, MenuView())
