"""
game/views/name_entry_view.py
Name Entry Screen displayed after game over or victory.
Allows player to type their warrior name and submit to the online leaderboard.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG
from game.systems import save_system
from game.systems.leaderboard_client import leaderboard_client
from game.ui.transitions import transition_to, TransitionOverlay
from game.ui.vedic_theme import (
    OBSIDIAN, SURFACE_LOW, SURFACE_HIGH, GOLD, GOLD_BRIGHT, CYAN,
    CYAN_BRIGHT, PARCHMENT, STARLIGHT, MUTED, ASTRA_RED,
    FONT_CEREMONIAL, FONT_INTERFACE, FONT_TELEMETRY,
    draw_chamfered_panel, draw_corner_etching, draw_scanlines,
)


class NameEntryView(arcade.View):
    def __init__(self, score: int, wave: int, kills: int, highest_combo: int,
                 difficulty: str = "normal", ship_class: str = "pushpaka",
                 is_victory: bool = False, stats: dict = None,
                 start_wave: int = 1, is_endless: bool = False):
        super().__init__()
        self.score = score
        self.wave = wave
        self.kills = kills
        self.highest_combo = highest_combo
        self.difficulty = difficulty
        self.ship_class = ship_class
        self.is_victory = is_victory
        self.stats = stats or {}
        self.start_wave = start_wave
        self.is_endless = is_endless

        saved = save_system.load()
        self.player_name = saved.get("player_name", "Warrior")
        self._cursor_timer = 0.0
        self._submitting = False
        self._status_msg = ""

        # UI Text Objects
        header_str = "CELESTIAL VICTORY" if is_victory else "DHARMIC REBIRTH"
        self._title = arcade.Text(
            header_str, WIDTH // 2, int(HEIGHT * 0.78),
            GOLD_BRIGHT if is_victory else ASTRA_RED,
            font_size=32, bold=True, font_name=FONT_CEREMONIAL[0],
            anchor_x="center", anchor_y="center"
        )
        self._sub = arcade.Text(
            f"SCORE: {score:,}   •   WAVE: {wave:02d}   •   DIFFICULTY: {difficulty.upper()}",
            WIDTH // 2, int(HEIGHT * 0.70),
            CYAN_BRIGHT, font_size=11, bold=True, font_name=FONT_TELEMETRY[0],
            anchor_x="center", anchor_y="center"
        )
        self._prompt = arcade.Text(
            "COMMISSION PILOT RECORD INTO AKASHIC ARCHIVES",
            WIDTH // 2, int(HEIGHT * 0.58),
            PARCHMENT, font_size=10, bold=True, font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center"
        )
        self._name_display = arcade.Text(
            "", WIDTH // 2, int(HEIGHT * 0.46),
            GOLD_BRIGHT, font_size=24, bold=True, font_name=FONT_INTERFACE[0],
            anchor_x="center", anchor_y="center"
        )
        self._status_text = arcade.Text(
            "", WIDTH // 2, int(HEIGHT * 0.34),
            CYAN, font_size=11, bold=True, font_name=FONT_TELEMETRY[0],
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "ENTER : TRANSMIT RECORD   •   ESC : SKIP TO DEBRIEF",
            WIDTH // 2, int(HEIGHT * 0.16),
            MUTED, font_size=10, bold=True, font_name=FONT_TELEMETRY[0],
            anchor_x="center"
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
        
        # Backdrop console panel
        draw_chamfered_panel(WIDTH // 2 - 260, WIDTH // 2 + 260, 60, HEIGHT - 60, CYAN,
                             fill=OBSIDIAN, alpha=240, border_width=1, cut=16)
        draw_corner_etching(WIDTH // 2 - 260, WIDTH // 2 + 260, 60, HEIGHT - 60, GOLD, length=18, alpha=140)
        draw_scanlines(WIDTH // 2 - 250, WIDTH // 2 + 250, 70, HEIGHT - 70, CYAN, spacing=24, alpha=4)

        self._title.draw()
        self._sub.draw()
        self._prompt.draw()

        # Input box with chamfered panel
        box_y = int(HEIGHT * 0.46)
        draw_chamfered_panel(WIDTH // 2 - 180, WIDTH // 2 + 180, box_y - 24, box_y + 24, CYAN_BRIGHT,
                             fill=SURFACE_HIGH, alpha=245, border_width=2, cut=8)

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
            ship_class=self.ship_class,
            stats={**self.stats, "kills": self.kills},
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
                highest_combo=self.highest_combo,
                total_damage=self.stats.get("total_damage", 0),
                boons_claimed=self.stats.get("boons_claimed", 0),
                bosses_defeated=self.stats.get("bosses_defeated", []),
                ship_class=self.ship_class,
                campaign_cleared=self.is_victory,
            )
            from game.systems.leaderboard_client import leaderboard_client
            leaderboard_client.push_profile()
            transition_to(self.window, GameOverView(
                score=self.score,
                wave=self.wave,
                kills=self.kills,
                highest_combo=self.highest_combo,
                high_score=updated["high_score"],
                difficulty=self.difficulty,
                ship_class=self.ship_class,
                stats=self.stats,
                start_wave=self.start_wave,
                is_endless=self.is_endless,
            ))
