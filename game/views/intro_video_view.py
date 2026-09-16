"""Automatic launch cinematic shown before the loading screen.

The game deliberately keeps the cinematic inside the Arcade window instead of
opening a second media-player window.  OpenCV is used only for decoding video
frames; it is imported lazily so a missing optional decoder can never prevent
the game from starting.  In that case the view shows a short branded fallback
and continues to the normal loading screen.
"""
from __future__ import annotations

import threading
import time
from pathlib import Path

import arcade

from constants import HEIGHT, WIDTH
from game.systems.sound_manager import SoundManager
from game.ui.transitions import TransitionOverlay, transition_to
from game.ui.vedic_theme import (
    CYAN,
    CYAN_BRIGHT,
    GOLD,
    GOLD_BRIGHT,
    MUTED,
    OBSIDIAN,
    FONT_CEREMONIAL,
    FONT_TELEMETRY,
    draw_scanlines,
)
from game.ui.easing import clamp


class IntroVideoView(arcade.View):
    """Play the launch PV automatically, then hand off to ``LoadingView``."""

    def __init__(self) -> None:
        super().__init__()
        self._elapsed = 0.0
        self._duration = 1.0
        self._fallback = False
        self._fallback_message = "PREPARING CELESTIAL ORDER SYSTEMS..."
        self._finished = False
        self._eof = False
        self._reader_thread: threading.Thread | None = None
        self._stop_reader = threading.Event()
        self._frame_lock = threading.Lock()
        self._pending_frame = None
        self._texture: arcade.Texture | None = None
        self._frame_number = 0
        self._frame_size = (16, 9)

        self._title = arcade.Text(
            "VIMANA WARS",
            WIDTH // 2,
            48,
            GOLD_BRIGHT,
            font_size=16,
            bold=True,
            anchor_x="center",
            anchor_y="center",
            font_name=FONT_CEREMONIAL[0],
        )
        self._status = arcade.Text(
            "CELESTIAL ORDER // THE RECLAMATION OF DHARMA",
            WIDTH // 2,
            25,
            CYAN_BRIGHT,
            font_size=8,
            bold=True,
            anchor_x="center",
            anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )

    @property
    def _video_path(self) -> Path:
        return Path(__file__).resolve().parents[2] / "vimana_wars_pv_final.mp4"

    def on_show_view(self) -> None:
        arcade.set_background_color((0, 0, 0))
        # Arcade's built-in media backend does not decode MP4 audio, so use
        # the bundled CC0 combat bed as a reliable cinematic audio bed.  The
        # loading screen stops it before the main UI appears.
        self.sound_manager = SoundManager()
        self.sound_manager.start_music(volume=0.18)
        self._start_video_reader()

    def on_hide_view(self) -> None:
        self._stop_video_reader()

    def _start_video_reader(self) -> None:
        path = self._video_path
        if not path.exists():
            self._use_fallback("LAUNCH CINEMATIC NOT FOUND — CONTINUING...", 0.9)
            return

        try:
            import cv2
            from PIL import Image
        except ImportError:
            self._use_fallback("VIDEO DECODER NOT INSTALLED — CONTINUING...", 0.9)
            return

        capture = cv2.VideoCapture(str(path))
        if not capture.isOpened():
            capture.release()
            self._use_fallback("CINEMATIC COULD NOT BE OPENED — CONTINUING...", 0.9)
            return

        fps = float(capture.get(cv2.CAP_PROP_FPS) or 24.0)
        fps = max(1.0, min(60.0, fps))
        frame_count = float(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0)
        self._duration = max(1.0, frame_count / fps) if frame_count else 12.0
        frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 16)
        frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 9)
        self._frame_size = (max(1, frame_width), max(1, frame_height))
        self._reader_thread = threading.Thread(
            target=self._read_frames,
            args=(capture, cv2, Image, fps),
            name="vimana-intro-video",
            daemon=True,
        )
        self._reader_thread.start()

    def _use_fallback(self, message: str, duration: float) -> None:
        self._fallback = True
        self._fallback_message = message
        self._duration = duration

    def _read_frames(self, capture, cv2, image_cls, fps: float) -> None:
        """Decode at real-time speed and keep only the newest frame."""
        frame_interval = 1.0 / fps
        next_frame_at = time.monotonic()
        try:
            while not self._stop_reader.is_set():
                ok, frame = capture.read()
                if not ok:
                    break

                # The source is 2560x1440.  1280x720 is more than enough for
                # the game's logical 900x600 viewport and greatly reduces
                # texture upload cost during the intro.
                height, width = frame.shape[:2]
                if width > 1280:
                    scale = 1280.0 / width
                    frame = cv2.resize(
                        frame,
                        (1280, max(1, int(height * scale))),
                        interpolation=cv2.INTER_AREA,
                    )
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Arcade's texture hitbox path requires an RGBA image.
                image = image_cls.fromarray(frame).convert("RGBA")
                with self._frame_lock:
                    self._pending_frame = image

                next_frame_at += frame_interval
                wait = next_frame_at - time.monotonic()
                if wait > 0:
                    self._stop_reader.wait(wait)
                elif wait < -frame_interval * 2:
                    next_frame_at = time.monotonic()
        finally:
            capture.release()
            self._eof = True

    def _stop_video_reader(self) -> None:
        self._stop_reader.set()
        thread = self._reader_thread
        if thread and thread.is_alive():
            thread.join(timeout=0.25)
        self._reader_thread = None

    def _consume_pending_frame(self) -> None:
        with self._frame_lock:
            image = self._pending_frame
            self._pending_frame = None
        if image is None:
            return

        self._frame_number += 1
        # A unique hash prevents Arcade's texture cache from confusing two
        # different video frames that share the same dimensions.
        self._texture = arcade.Texture(
            image,
            hash=f"vimana-intro-frame-{self._frame_number}",
        )
        self._frame_size = (image.width, image.height)

    def _go_to_loading(self) -> None:
        if self._finished or not self.window or TransitionOverlay.is_active:
            return
        self._finished = True
        self._stop_video_reader()
        from game.views.loading_screen import LoadingView
        transition_to(self.window, LoadingView(), duration=0.45, style="fade")

    def on_update(self, delta_time: float) -> None:
        TransitionOverlay.update(delta_time)
        if self._finished:
            return
        self._elapsed += max(0.0, delta_time)
        self._consume_pending_frame()

        if self._fallback:
            if self._elapsed >= self._duration:
                self._go_to_loading()
            return

        if self._eof and self._elapsed >= self._duration:
            self._go_to_loading()

    def on_draw(self) -> None:
        self.clear()
        if self._texture:
            frame_w, frame_h = self._frame_size
            scale = min(WIDTH / frame_w, HEIGHT / frame_h)
            draw_w = frame_w * scale
            draw_h = frame_h * scale
            rect = arcade.rect.LBWH(
                (WIDTH - draw_w) / 2,
                (HEIGHT - draw_h) / 2,
                draw_w,
                draw_h,
            )
            arcade.draw_texture_rect(self._texture, rect)
        else:
            arcade.draw_lrbt_rectangle_filled(0, WIDTH, 0, HEIGHT, OBSIDIAN)

        # Minimal branded chrome keeps the transition intentional while the
        # first decoded frame arrives, without covering the cinematic.
        draw_scanlines(0, WIDTH, 0, HEIGHT, CYAN, spacing=36, alpha=3)
        progress = clamp(self._elapsed / max(0.1, self._duration))
        arcade.draw_lrbt_rectangle_filled(0, WIDTH * progress, 0, 3, GOLD)
        self._title.draw()
        self._status.text = self._fallback_message if self._fallback else self._status.text
        self._status.color = MUTED if self._fallback else CYAN_BRIGHT
        self._status.draw()
        arcade.draw_text(
            "PRESS ESC TO SKIP TO LOADING",
            WIDTH - 18,
            HEIGHT - 20,
            (*MUTED[:3], 190),
            font_size=8,
            anchor_x="right",
            anchor_y="center",
            font_name=FONT_TELEMETRY[0],
        )
        TransitionOverlay.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.ESCAPE, arcade.key.SPACE, arcade.key.ENTER):
            self._go_to_loading()
