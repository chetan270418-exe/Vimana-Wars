"""
game/views/name_entry_view.py
Name Entry Screen displayed after game over or victory.
Allows player to type their warrior name and submit to the online leaderboard.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.ui.transitions import transition_to, TransitionOverlay


class NameEntryView(arcade.View):
    def __init__(self, score: int, wave: int, kills: int, highest_combo: int,
                 difficulty: str = "normal", ship_class: str = "pushpaka",
                 is_victory: bool = False, stats: dict = None):
        super().__init__()
        self.score = score
        self.wave = wave
        self.kills = kills
        self.highest_combo = highest_combo
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.is_victory = is_victory
        self.stats = stats or {}

        saved = save_system.load()
        self.player_name = saved.get("player_name", "Warrior")
        self._cursor_timer = 0.0
        self._submitting = False
        self._status_msg = ""

        # UI Text Objects
        header_str = "VICTORY ACHIEVED!" if is_victory else "VALIANT EFFORT!"
        self._title = arcade.Text(
            header_str, WIDTH // 2, int(HEIGHT * 0.80),
            (255, 215, 0) if is_victory else (240, 70, 70),
            font_size=34, bold=True, anchor_x="center", anchor_y="center"
        )
        self._sub = arcade.Text(
            f"Score: {score:,}  •  Wave: {wave}  •  Difficulty: {difficulty.upper()}",
            WIDTH // 2, int(HEIGHT * 0.70),
            COLOR_WAVE, font_size=14, anchor_x="center", anchor_y="center"
        )
        self._prompt = arcade.Text(
            "ENTER WARRIOR NAME FOR REALM ARCHIVES",
            WIDTH // 2, int(HEIGHT * 0.56),
            (200, 200, 220), font_size=12, bold=True, anchor_x="center", anchor_y="center"
        )
        self._name_display = arcade.Text(
            "", WIDTH // 2, int(HEIGHT * 0.44),
            (255, 255, 255), font_size=26, bold=True, anchor_x="center", anchor_y="center"
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, int(HEIGHT * 0.32),
            COLOR_SCORE, font_size=12, anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "ENTER : Submit & Continue   •   ESC : Skip to Results",
            WIDTH // 2, int(HEIGHT * 0.14),
            (160, 160, 180), font_size=12, anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        from game.systems.sound_manager import SoundManager
        SoundManager.stop_music()

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        self._cursor_timer += delta_time
        pending = getattr(self, "_pending_result", None)
        if pending is not None:
            self._pending_result = None
            self._proceed_to_results()

    def on_draw(self) -> None:
        self.clear()

        self._title.draw()
        self._sub.draw()
        self._prompt.draw()

        # Input box
        box_y = int(HEIGHT * 0.44)
        arcade.draw_lrbt_rectangle_filled(WIDTH // 2 - 180, WIDTH // 2 + 180, box_y - 24, box_y + 24, (20, 25, 50))
        arcade.draw_lrbt_rectangle_outline(WIDTH // 2 - 180, WIDTH // 2 + 180, box_y - 24, box_y + 24, COLOR_SCORE, 2)

        # Blinking cursor
        show_cursor = (int(self._cursor_timer * 2.5) % 2 == 0) and not self._submitting
        cursor_char = "_" if show_cursor else " "
        self._name_display.text = f"{self.player_name}{cursor_char}"
        self._name_display.draw()

        if self._status_msg:
            self._status_text.text = self._status_msg
            self._status_text.draw()

        self._hint.draw()
        TransitionOverlay.draw()

    def on_key_press(self, key, modifiers) -> None:
        if self._submitting:
            return

        if key in (arcade.key.ENTER, arcade.key.RETURN):
            self._submit_and_proceed()
        elif key == arcade.key.ESCAPE:
            self._proceed_to_results()
        elif key == arcade.key.BACKSPACE:
            if len(self.player_name) > 0:
                self.player_name = self.player_name[:-1]

    def on_text(self, text: str) -> None:
        if self._submitting:
            return
        if text.isprintable() and len(self.player_name) < 16:
            self.player_name += text

    def _submit_and_proceed(self) -> None:
        final_name = self.player_name.strip() or "Anonymous"
        
        # Persist name for next time
        saved = save_system.load()
        saved["player_name"] = final_name
        save_system.save(saved)

        self._submitting = True
        self._status_msg = "Transmitting record to online leaderboard..."

        def _on_done(success: bool, error: str | None):
            # Network callbacks run on a worker thread. Defer the view change
            # to on_update so Arcade/OpenGL state is touched only on the UI thread.
            self._pending_result = (success, error)

        leaderboard_client.submit_score(
            player_name=final_name,
            score=self.score,
            level_reached=self.wave,
            difficulty=self.difficulty,
            on_complete=_on_done
        )

    def _proceed_to_results(self) -> None:
        if self.is_victory:
            from game.views.victory_view import VictoryView
            transition_to(self.window, VictoryView(
                score=self.score,
                kills=self.kills,
                highest_combo=self.highest_combo,
                difficulty=self.difficulty,
                ship_class=self.ship_class,
                wave=self.wave,
                stats=self.stats,
            ))
        else:
            from game.views.game_over_view import GameOverView
            updated = save_system.update_after_game(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
            )
            transition_to(self.window, GameOverView(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
                highest_combo=self.highest_combo,
                high_score=updated["high_score"],
                difficulty=self.difficulty,
                ship_class=self.ship_class,
                stats=self.stats,
            ))
