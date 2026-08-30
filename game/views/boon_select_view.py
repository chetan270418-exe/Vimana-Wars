"""
game/views/boon_select_view.py
3-Card Roguelite Deva Blessing selection screen between waves.
Presented during wave transitions so the player can choose an astral upgrade.
"""
import math
import random
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE, COLOR_WAVE, COLOR_WHITE
from game.ui.easing import ease_out_back, ease_out_cubic, lerp, clamp
from game.ui.tween import TweenManager, Tween
from game.ui.transitions import transition_to, TransitionOverlay
from game.systems.sound_manager import SoundManager
# Low-level draw primitives that don't have any of the convenience-layer
# surprises (alpha parsing, rect-validation, etc.) that can silently make
# cards invisible on some arcade versions / GPU drivers.
from arcade import draw_rect_filled, draw_rect_outline, LRBT


class CardState:
    def __init__(self):
        self.flip_progress = 0.0
        self.lift = 0.0
        self.scale = 1.0
        self.alpha = 255.0
        self.fly_text_y = 0.0
        self.fly_text_alpha = 0.0
        # Cached Text objects — content/position/alpha updated per frame.
        # Using Text (not draw_text) avoids the slow-draw silent-failure path
        # that was making the cards invisible in the user's screenshot.
        self._text_deva = arcade.Text("", 0, 0, (255, 255, 255, 255),
                                      font_size=9, bold=True,
                                      anchor_x="center", anchor_y="center")
        self._text_name = arcade.Text("", 0, 0, (255, 255, 255, 255),
                                      font_size=13, bold=True,
                                      anchor_x="center", anchor_y="center")
        self._text_num  = arcade.Text("", 0, 0, (255, 255, 255, 255),
                                      font_size=18, bold=True,
                                      anchor_x="center", anchor_y="center")
        # 4 description lines is enough for our 24-char wrapped boons
        self._text_desc = [arcade.Text("", 0, 0, (210, 215, 230, 255),
                                        font_size=10, bold=True,
                                        anchor_x="center", anchor_y="center")
                           for _ in range(4)]
        self._text_claim = arcade.Text("", 0, 0, (255, 220, 50, 255),
                                       font_size=9, bold=True,
                                       anchor_x="center", anchor_y="center")
        self._text_fly = arcade.Text("", 0, 0, (255, 215, 0, 255),
                                     font_size=16, bold=True,
                                     anchor_x="center", anchor_y="center")


class BoonSelectView(arcade.View):
    def __init__(self, game_view, choices: list[dict]):
        super().__init__()
        self.game_view = game_view
        self.choices = choices
        self._selected_card = 0
        self._pulse = 0.0

        self.sound_manager = SoundManager()
        self._tweens = TweenManager()
        
        self._pick_phase = False
        self._pick_timer = 0.0
        self._transition_started = False
        
        self._cards = [CardState() for _ in range(len(self.choices))]
        
        # Background Particles
        self._particles = []
        for _ in range(20):
            self._particles.append({
                "x": random.uniform(0, WIDTH),
                "y": random.uniform(0, HEIGHT),
                "speed": random.uniform(10, 30),
                "wobble_offset": random.uniform(0, math.pi * 2),
                "wobble_speed": random.uniform(1, 3),
                "wobble_amp": random.uniform(5, 15)
            })

        # UI Text Objects
        self._title = arcade.Text(
            "BLESSING OF THE DEVAS",
            WIDTH // 2, HEIGHT - 70,
            COLOR_SCORE, font_size=32, bold=True,
            anchor_x="center", anchor_y="center"
        )
        self._sub = arcade.Text(
            "Choose a Divine Astral Boon to empower your Vimana",
            WIDTH // 2, HEIGHT - 110,
            COLOR_WAVE, font_size=14,
            anchor_x="center", anchor_y="center"
        )
        self._hint = arcade.Text(
            "1, 2, 3 or ← → : Select   •   ENTER / Click : Claim Boon",
            WIDTH // 2, 35,
            (160, 170, 200), font_size=12, bold=True,
            anchor_x="center"
        )

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)
        
        if hasattr(self.game_view, "player"):
            self.game_view.player.reset_input_state()
        
        for i, card in enumerate(self._cards):
            card.flip_progress = 0.0
            card.lift = 0.0
            card.scale = 1.0
            card.alpha = 255.0
            card.fly_text_y = 0.0
            card.fly_text_alpha = 0.0
            
            self._tweens.tween(
                target=card,
                attr="flip_progress",
                end=1.0,
                duration=0.4,
                ease=ease_out_back,
                delay=i * 0.15
            )

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time
        self._tweens.update(delta_time)
        TransitionOverlay.update(delta_time)
        
        # Update particles
        for p in self._particles:
            p["y"] += p["speed"] * delta_time
            if p["y"] > HEIGHT + 20:
                p["y"] = -20
                p["x"] = random.uniform(0, WIDTH)

        # Handle smooth hover states if not picked
        if not self._pick_phase:
            for i, card in enumerate(self._cards):
                is_sel = (i == self._selected_card)
                target_lift = 12.0 if is_sel else 0.0
                target_scale = 1.05 if is_sel else 1.0
                target_alpha = 255.0 if is_sel else 153.0
                
                card.lift = lerp(card.lift, target_lift, delta_time * 10)
                card.scale = lerp(card.scale, target_scale, delta_time * 10)
                card.alpha = lerp(card.alpha, target_alpha, delta_time * 10)
        else:
            self._pick_timer -= delta_time
            if self._pick_timer <= 0 and not self._transition_started:
                self._transition_started = True
                if hasattr(self.game_view, "player"):
                    self.game_view.player.reset_input_state()
                self.window.show_view(self.game_view)

    def on_draw(self) -> None:
        self.clear()

        # Draw background particles
        chosen = self.choices[self._selected_card]
        p_color = chosen["color"]
        for p in self._particles:
            px = p["x"] + math.sin(p["wobble_offset"] + self._pulse * p["wobble_speed"]) * p["wobble_amp"]
            py = p["y"]
            arcade.draw_circle_filled(px, py, 2, (p_color[0], p_color[1], p_color[2], 100))

        self._title.draw()
        self._sub.draw()

        card_w = 230
        card_h = 320
        start_x = WIDTH // 2 - 270
        spacing = 270
        cy = HEIGHT // 2 - 20

        for i, boon in enumerate(self.choices):
            card = self._cards[i]
            is_sel = (i == self._selected_card)

            # Draw Face Down Back
            if card.flip_progress <= 0.0:
                cx = start_x + i * spacing
                # Direct low-level call: avoids the convenience-layer alpha
                # parsing that has caused "invisible cards" regressions before.
                draw_rect_filled(LRBT(
                    cx - card_w // 2, cx + card_w // 2,
                    cy - card_h // 2, cy + card_h // 2,
                ), (20, 25, 45, 255))
                # Rotating glow rings
                arcade.draw_arc_outline(
                    cx, cy, 80, 80, (100, 120, 200, 150),
                    0, 270, border_width=4, tilt_angle=math.degrees(self._pulse * 3)
                )
                arcade.draw_arc_outline(
                    cx, cy, 50, 50, (80, 100, 180, 100),
                    0, 180, border_width=2, tilt_angle=math.degrees(-self._pulse * 4)
                )
                continue

            width_scale = card.flip_progress
            cx = start_x + i * spacing
            cy_lifted = cy + card.lift

            w = card_w * width_scale * card.scale
            h = card_h * card.scale

            alpha = int(clamp(card.alpha, 0.0, 255.0))

            # Card Background — always use 4-tuple color for consistent alpha
            if is_sel:
                bg_color = (35, 45, 80, alpha)
            else:
                bg_color = (25, 30, 55, alpha)
            draw_rect_filled(LRBT(
                cx - w // 2, cx + w // 2,
                cy_lifted - int(h / 2), cy_lifted + int(h / 2),
            ), bg_color)

            # Glowing Border
            if is_sel:
                t = (math.sin(self._pulse * 4) + 1.0) / 2.0
                pulse_val = int(200 + 55 * ease_out_cubic(t))
                border_col = (boon["color"][0], boon["color"][1], boon["color"][2], min(alpha, pulse_val))
                border_width = max(1, int(3 * card.scale))
            else:
                border_col = (70, 80, 110, alpha)
                border_width = max(1, int(1 * card.scale))

            draw_rect_outline(LRBT(
                cx - w // 2, cx + w // 2,
                cy_lifted - int(h / 2), cy_lifted + int(h / 2),
            ), border_col, border_width)

            text_alpha = int(alpha * clamp(width_scale, 0.0, 1.0))
            if text_alpha <= 0:
                continue

            # God Name Header
            arcade.draw_text(
                boon["deva"],
                cx, cy_lifted + 125 * card.scale,
                (200, 210, 240, text_alpha), font_size=int(9 * card.scale), bold=True, anchor_x="center"
            )

            # Boon Name
            b_col = boon["color"]
            arcade.draw_text(
                boon["name"],
                cx, cy_lifted + 90 * card.scale,
                (b_col[0], b_col[1], b_col[2], text_alpha), font_size=int(13 * card.scale), bold=True, anchor_x="center"
            )

            # Decorative Emblem
            arcade.draw_circle_filled(cx, cy_lifted + 20 * card.scale, 36 * card.scale, (15, 20, 35, alpha))
            arcade.draw_circle_outline(cx, cy_lifted + 20 * card.scale, 36 * card.scale, (b_col[0], b_col[1], b_col[2], alpha), int(2 * card.scale))
            arcade.draw_text(
                f"[{i + 1}]",
                cx, cy_lifted + 12 * card.scale,
                (255, 255, 255, text_alpha), font_size=int(18 * card.scale), bold=True, anchor_x="center"
            )

            # Description (Wrapped)
            desc_lines = self._wrap_text(boon["desc"], 24)
            for l_idx, line in enumerate(desc_lines):
                arcade.draw_text(
                    line,
                    cx, cy_lifted - 45 * card.scale - l_idx * 18 * card.scale,
                    (210, 215, 230, text_alpha), font_size=int(10 * card.scale), bold=True, anchor_x="center"
                )

            # Selection Tag
            if is_sel and not self._pick_phase:
                t2 = (math.sin(self._pulse * 4) + 1.0) / 2.0
                pulse_val2 = int(200 + 55 * ease_out_cubic(t2))
                arcade.draw_text(
                    "★ PRESS ENTER TO CLAIM ★",
                    cx, cy_lifted - 135 * card.scale,
                    (255, 220, 50, pulse_val2), font_size=int(9 * card.scale), bold=True, anchor_x="center"
                )
                
            # Picked Fly Text
            if card.fly_text_alpha > 0:
                arcade.draw_text(
                    "+1 BOON OBTAINED",
                    cx, cy_lifted + card.fly_text_y,
                    (255, 215, 0, int(card.fly_text_alpha)), font_size=16, bold=True, anchor_x="center"
                )

        self._hint.draw()
        TransitionOverlay.draw()

    def _wrap_text(self, text: str, max_chars: int) -> list[str]:
        words = text.split()
        lines = []
        cur = []
        cur_len = 0
        for w in words:
            if cur_len + len(w) + 1 > max_chars:
                lines.append(" ".join(cur))
                cur = [w]
                cur_len = len(w)
            else:
                cur.append(w)
                cur_len += len(w) + 1
        if cur:
            lines.append(" ".join(cur))
        return lines

    def on_key_press(self, key, modifiers) -> None:
        if self._pick_phase:
            return
            
        old_sel = self._selected_card
        
        if key in (arcade.key.LEFT, arcade.key.A):
            self._selected_card = (self._selected_card - 1) % len(self.choices)
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._selected_card = (self._selected_card + 1) % len(self.choices)
        elif key == arcade.key.KEY_1 and len(self.choices) >= 1:
            self._selected_card = 0
            self._claim_selected()
        elif key == arcade.key.KEY_2 and len(self.choices) >= 2:
            self._selected_card = 1
            self._claim_selected()
        elif key == arcade.key.KEY_3 and len(self.choices) >= 3:
            self._selected_card = 2
            self._claim_selected()
        elif key in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._claim_selected()
            
        if self._selected_card != old_sel:
            self.sound_manager.play_ui_click()

    def on_key_release(self, key, modifiers) -> None:
        if hasattr(self.game_view, "player"):
            self.game_view.player.keys_pressed.discard(key)

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        if hasattr(self.game_view, "player"):
            self.game_view.player.mouse_x = x
            self.game_view.player.mouse_y = y
            self.game_view.player.mouse_held = False
        if not self._pick_phase:
            card_w = 230
            card_h = 320
            start_x = WIDTH // 2 - 270
            spacing = 270
            cy = HEIGHT // 2 - 20
            for i in range(len(self.choices)):
                cx = start_x + i * spacing
                if cx - card_w // 2 <= x <= cx + card_w // 2 and cy - card_h // 2 <= y <= cy + card_h // 2:
                    if self._selected_card != i:
                        self._selected_card = i
                        self.sound_manager.play_ui_click(volume=0.20)
                    break

    def on_mouse_press(self, x, y, button, modifiers) -> None:
        if self._pick_phase:
            return
            
        if hasattr(self.game_view, "player"):
            self.game_view.player.mouse_x = x
            self.game_view.player.mouse_y = y
            self.game_view.player.mouse_held = False

        card_w = 230
        card_h = 320
        start_x = WIDTH // 2 - 270
        spacing = 270
        cy = HEIGHT // 2 - 20

        for i in range(len(self.choices)):
            cx = start_x + i * spacing
            if cx - card_w // 2 <= x <= cx + card_w // 2 and cy - card_h // 2 <= y <= cy + card_h // 2:
                old_sel = self._selected_card
                self._selected_card = i
                if old_sel != i:
                    self.sound_manager.play_ui_click()
                self._claim_selected()
                break

    def on_mouse_release(self, x, y, button, modifiers) -> None:
        if hasattr(self.game_view, "player"):
            self.game_view.player.mouse_held = False

    def _claim_selected(self) -> None:
        if self._pick_phase:
            return
            
        self._pick_phase = True
        self._pick_timer = 0.6
        self._transition_started = False
        
        chosen = self.choices[self._selected_card]
        self.game_view.apply_boon(chosen)
        
        for i, card in enumerate(self._cards):
            if i == self._selected_card:
                self._tweens.tween(card, "scale", 1.3, 0.3, ease=ease_out_back)
                self._tweens.tween(card, "fly_text_y", 40.0, 0.5, ease=ease_out_cubic)
                card.fly_text_alpha = 255.0
                self._tweens.tween(card, "fly_text_alpha", 0.0, 0.5, ease=ease_out_cubic, delay=0.2)
            else:
                self._tweens.tween(card, "alpha", 76.5, 0.2, ease=ease_out_cubic)
