"""
game/views/stats_view.py
Lifetime stats screen — surfaces save.json progress across all runs.
Bento-grid layout with sections for Core / Per-Difficulty / Per-Ship /
Mastery / Collection.
"""
import arcade
from constants import WIDTH, HEIGHT, COLOR_BG, COLOR_SCORE
from game.systems import save_system
from game.ui.easing import clamp
from game.ui.tween import TweenManager
from game.ui.transitions import TransitionOverlay
from game.systems.achievement_system import ACHIEVEMENTS_LIST


# ── Helpers ──────────────────────────────────────────────────────────

def _fmt_hms(seconds: float) -> str:
    """Format seconds as 'Xh Ym' or 'Ym Zs' — never shows seconds when hours are present."""
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h > 0:
        return f"{h}h {m:02d}m"
    return f"{m}m {s:02d}s"

def _fmt_int(n: int) -> str:
    return f"{n:,}"


# ── Bento panel primitive ────────────────────────────────────────────

class StatPanel:
    """A single bento card — title + 2-3 stat lines, with hover lift."""
    def __init__(self, cx, cy, w, h, title, accent=(120, 180, 255)):
        self.cx = cx
        self.cy = cy
        self.w = w
        self.h = h
        self.title = title
        self.accent = accent
        self.lines: list[tuple] = []  # (label, value, value_color)
        self.hover_anim = 0.0
        self.appear_delay = 0.0
        self.appear_anim = 0.0  # 0..1, driven by TweenManager

        # Cached Text objects (per panel) — content/alpha/position update in-place.
        # Max 6 line pairs per panel is more than enough for our 2-3 line panels.
        self._title_text = arcade.Text(
            title.upper(), cx - w / 2 + 14, cy + h / 2 - 14,
            (*accent, 230), font_size=9, bold=True,
        )
        self._label_texts: list[arcade.Text] = []
        self._value_texts: list[arcade.Text] = []
        for _ in range(6):
            self._label_texts.append(arcade.Text(
                "", cx - w / 2 + 14, 0,
                (140, 150, 180, 200), font_size=9, bold=True,
            ))
            self._value_texts.append(arcade.Text(
                "", cx + w / 2 - 14, 0,
                (220, 230, 250, 240), font_size=11, bold=True,
                anchor_x="right",
            ))

    def _sync_line_text(self, idx, label, value, vcol, alpha):
        """Update one cached Text pair with current label/value/alpha."""
        lt = self._label_texts[idx]
        vt = self._value_texts[idx]
        lt.text = label
        vt.text = value
        lt.color = (140, 150, 180, int(200 * alpha))
        vt.color = (*vcol, int(240 * alpha))

    @property
    def left(self):   return self.cx - self.w / 2
    @property
    def right(self):  return self.cx + self.w / 2
    @property
    def bottom(self): return self.cy - self.h / 2
    @property
    def top(self):    return self.cy + self.h / 2

    def hit_test(self, x, y):
        return self.left <= x <= self.right and self.bottom <= y <= self.top

    def update(self, dt, mouse_x, mouse_y):
        target = 1.0 if self.hit_test(mouse_x, mouse_y) else 0.0
        self.hover_anim += (target - self.hover_anim) * min(1.0, 12.0 * dt)
        # Drive appear anim
        if self.appear_delay > 0:
            self.appear_delay -= dt
        else:
            self.appear_anim = min(1.0, self.appear_anim + dt * 2.5)

    def draw(self):
        if self.appear_anim <= 0.0:
            return
        a = clamp(self.appear_anim)
        scale = 0.92 + 0.08 * a + 0.02 * self.hover_anim
        cx = self.cx
        cy = self.cy - (1.0 - a) * 12  # rise-in
        w = self.w * scale
        h = self.h * scale

        # Background — blend with hover
        idle = (18, 24, 46)
        hov  = (28, 38, 72)
        bg = _lerp(idle, hov, self.hover_anim)
        arcade.draw_lrbt_rectangle_filled(
            cx - w / 2, cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*bg, int(220 * a)),
        )
        # Accent stripe on the left
        arcade.draw_lrbt_rectangle_filled(
            cx - w / 2, cx - w / 2 + 4,
            cy - h / 2, cy + h / 2,
            (*self.accent, int(220 * a)),
        )
        # Border
        border = (90, 110, 150) if self.hover_anim < 0.5 else self.accent
        arcade.draw_lrbt_rectangle_outline(
            cx - w / 2, cx + w / 2,
            cy - h / 2, cy + h / 2,
            (*border, int(220 * a)), 2 if self.hover_anim > 0.5 else 1,
        )

        # Title — cached Text, position + color update per frame.
        self._title_text.position = (cx - w / 2 + 14, cy + h / 2 - 14)
        self._title_text.color = (*self.accent, int(230 * a))
        self._title_text.draw()

        # Stat lines — cached Text pairs, no per-frame arcade.draw_text.
        line_y = cy + h / 2 - 30
        for idx, (label, value, vcol) in enumerate(self.lines):
            self._sync_line_text(idx, label, value, vcol, a)
            self._label_texts[idx].position = (cx - w / 2 + 14, line_y)
            self._value_texts[idx].position = (cx + w / 2 - 14, line_y)
            self._label_texts[idx].draw()
            self._value_texts[idx].draw()
            line_y -= 16


def _lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1[:3], c2[:3]))


# ── Main view ────────────────────────────────────────────────────────

class StatsView(arcade.View):
    def __init__(self, return_view=None):
        super().__init__()
        self.return_view = return_view
        self._mouse_x = 0.0
        self._mouse_y = 0.0
        self._pulse = 0.0
        self._tweens = TweenManager()

        # Title text
        self._title = arcade.Text(
            "WARRIOR ARCHIVES — LIFETIME STATS",
            WIDTH // 2, HEIGHT - 50,
            COLOR_SCORE, font_size=24, bold=True,
            anchor_x="center", anchor_y="center",
        )
        self._hint = arcade.Text(
            "ESC : Back",
            WIDTH // 2, 30,
            (160, 160, 190), font_size=11, bold=True,
            anchor_x="center",
        )
        # Empty-state notice (shown when nothing has been recorded yet)
        self._empty = arcade.Text(
            "No runs yet — defeat some Asuras to fill this archive!",
            WIDTH // 2, HEIGHT // 2,
            (180, 180, 210), font_size=13,
            anchor_x="center", anchor_y="center",
        )
        self._show_empty = False

        # Build the panels
        self._panels: list[StatPanel] = []
        self._build_panels()

    # ── Panel layout ───────────────────────────────────────────────────

    def _build_panels(self) -> None:
        data = save_system.load()
        played = data["games_played"] > 0

        # Panel size + spacing
        pw, ph = 240, 110
        gap_x, gap_y = 20, 20
        # 3 columns × 2 rows
        cols = 3
        col_w = pw
        total_w = cols * col_w + (cols - 1) * gap_x
        start_x = WIDTH // 2 - total_w / 2 + col_w / 2
        # Vertically centered with title above
        row_h = ph
        start_y = HEIGHT // 2 + 30

        def pos(c, r):
            return (start_x + c * (col_w + gap_x),
                    start_y - r * (row_h + gap_y))

        def make_panel(c, r, title, accent):
            p = StatPanel(*pos(c, r), pw, ph, title, accent=accent)
            return p

        # ── Row 0 ──────────────────────────────────────────────────────
        # Core
        p = make_panel(0, 0, "Core Records", (255, 215, 60))
        p.lines = [
            ("High Score",  _fmt_int(data["high_score"]),  (255, 220, 50)),
            ("Best Wave",   f"{data['last_wave']}",        (200, 230, 255)),
            ("Total Kills", _fmt_int(data["total_kills"]), (255, 100, 100)),
        ]
        self._panels.append(p)

        # Playtime
        p = make_panel(1, 0, "Time in Combat", (100, 220, 200))
        p.lines = [
            ("Lifetime",    _fmt_hms(data["playtime_seconds"]), (100, 230, 200)),
            ("Runs Played", f"{data['games_played']}",          (220, 230, 255)),
            ("Best Combo",  f"×{max(1, data['best_combo'])}",   (255, 150, 30)),
        ]
        self._panels.append(p)

        # Damage & Boons
        p = make_panel(2, 0, "Damage & Boons", (220, 100, 220))
        p.lines = [
            ("Total Damage",  _fmt_int(data["total_damage"]), (255, 160, 60)),
            ("Boons Claimed", f"{data['total_boons']}",       (255, 100, 220)),
            ("Endless Best",  f"W{data['endless_high_wave']}  {_fmt_int(data['endless_high_score'])} pts",
                                                              (160, 220, 255)),
        ]
        self._panels.append(p)

        # ── Row 1 ──────────────────────────────────────────────────────
        # Achievements (collection)
        unlocked = set(data.get("achievements") or [])
        total = len(ACHIEVEMENTS_LIST)
        pct = (len(unlocked) / total * 100) if total else 0
        p = make_panel(0, 1, "Trophy Collection", (255, 200, 100))
        p.lines = [
            ("Unlocked",     f"{len(unlocked)} / {total}",  (255, 230, 60)),
            ("Completion",   f"{pct:.0f}%",                 (200, 220, 255)),
            ("Last Trophy",  self._last_unlocked_name(unlocked) or "—",
                                                              (160, 200, 240)),
        ]
        self._panels.append(p)

        # Bosses
        bosses = data.get("bosses_defeated") or []
        p = make_panel(1, 1, "Bosses Vanquished", (220, 60, 100))
        p.lines = [
            ("Total",       f"{len(bosses)} / 4",          (255, 100, 130)),
            ("Kumbhakarna", "✓" if "kumbhakarna" in bosses else "—",
                                                            (210, 140, 20)),
            ("Ravana",      "✓" if "ravana"      in bosses else "—",
                                                            (220, 0, 80)),
            ("Mahishasura", "✓" if "mahishasura" in bosses else "—",
                                                            (255, 120, 40)),
            ("Vritra",      "✓" if "vritra"      in bosses else "—",
                                                            (190, 80, 255)),
        ]
        self._panels.append(p)

        # Ships mastered
        from game.entities.ship_classes import SHIP_CLASSES
        mastered = set(data.get("ships_mastered") or [])
        p = make_panel(2, 1, "Vimana Mastery", (120, 240, 255))
        ship_lines = []
        for sid, sdata in SHIP_CLASSES.items():
            mark = "✓" if sid in mastered else "—"
            ship_lines.append((sdata["name"], mark,
                               sdata["color"] if sid in mastered else (120, 130, 150)))
        p.lines = ship_lines
        self._panels.append(p)

        # Stagger the panel appearances for a nice cascade
        for i, panel in enumerate(self._panels):
            panel.appear_anim = 0.0
            panel.appear_delay = i * 0.06

        # Show empty state if the player has never finished a run
        self._show_empty = not played

    def _last_unlocked_name(self, unlocked: set) -> str | None:
        if not unlocked:
            return None
        # ACHIEVEMENTS_LIST is in declared order; last is most-recent visually
        for ach in reversed(ACHIEVEMENTS_LIST):
            if ach["id"] in unlocked:
                return ach["name"]
        return None

    # ── Lifecycle ──────────────────────────────────────────────────────

    def on_show_view(self) -> None:
        arcade.set_background_color(COLOR_BG)

    def on_update(self, delta_time: float) -> None:
        self._pulse += delta_time
        for panel in self._panels:
            panel.update(delta_time, self._mouse_x, self._mouse_y)

    def on_draw(self) -> None:
        self.clear()
        self._title.draw()
        if self._show_empty:
            self._empty.draw()
        else:
            for panel in self._panels:
                panel.draw()
        self._hint.draw()
        TransitionOverlay.draw()

    # ── Input ──────────────────────────────────────────────────────────

    def on_mouse_motion(self, x, y, dx, dy) -> None:
        self._mouse_x = x
        self._mouse_y = y

    def on_key_press(self, key, modifiers) -> None:
        if key == arcade.key.ESCAPE:
            if self.return_view:
                from game.ui.transitions import transition_to
                transition_to(self.window, self.return_view)
            else:
                from game.views.menu_view import MenuView
                from game.ui.transitions import transition_to
                transition_to(self.window, MenuView())
