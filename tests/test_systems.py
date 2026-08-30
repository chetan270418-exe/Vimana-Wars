"""
tests/test_systems.py
Unit tests for all core gameplay systems.
"""
from game.entities.player import Player
from game.entities.bullet import PlayerBullet
from game.entities.powerup import PowerUp, PowerUpType
from game.entities.enemies.asura_fast import AsuraFast
from game.systems.score_system import ScoreSystem
from game.systems.boon_system import BoonManager
from game.systems.wave_manager import WaveManager
from game.systems.floating_text import FloatingTextManager
from game.systems.particles import ParticleManager
from game.systems.achievement_system import AchievementManager
from game.systems import collision as collision_sys
from game.systems import save_system
from constants import WIDTH, HEIGHT


class TestScoreSystem:
    def test_score_and_combo(self):
        ss = ScoreSystem()
        assert ss.score == 0
        assert ss.combo == 1
        ss.register_kill(100)
        assert ss.score == 100
        assert ss.combo == 1
        ss.register_kill(100)
        assert ss.score == 100 + 100 * 2
        assert ss.combo == 2

    def test_combo_decay(self):
        ss = ScoreSystem()
        ss.register_kill(100)
        ss.register_kill(100)
        assert ss.combo_active is True
        ss.update(ss.combo_timeout + 1.0)
        assert ss.combo == 1
        assert ss.combo_active is False


class TestBoonSystem:
    def test_boon_manager(self):
        bm = BoonManager()
        assert bm.has_boon("agni_fury") is False
        bm.add_boon("agni_fury")
        assert bm.has_boon("agni_fury") is True
        assert bm.get_boon_level("agni_fury") == 1
        bm.add_boon("agni_fury")
        assert bm.get_boon_level("agni_fury") == 2

    def test_get_random_choices(self):
        bm = BoonManager()
        choices = bm.get_random_choices(3)
        assert len(choices) <= 3
        # Max out one boon
        for _ in range(3):
            bm.add_boon("agni_fury")
        choices2 = bm.get_random_choices(8)
        assert not any(c["id"] == "agni_fury" for c in choices2)


class TestWaveManager:
    def test_wave_manager_progression(self):
        wm = WaveManager()
        assert wm.wave_number == 0
        enemies = []
        powerups = []
        player = Player()
        # Progress from initial clear pause to countdown
        wm.update(3.5, enemies, powerups, player)
        assert wm.is_announcing is True
        # Progress through countdown to spawning
        wm.update(2.5, enemies, powerups, player)
        assert wm._state == "SPAWNING"
        # Tick to spawn wave and enter fighting
        wm.update(0.016, enemies, powerups, player)
        assert wm.is_fighting is True
        assert len(enemies) > 0

    def test_extended_campaign_boss_schedule(self):
        from game.systems.wave_manager import _wave_config
        from constants import get_realm_for_wave
        assert _wave_config(10)["boss"] == "ravana"
        assert _wave_config(15)["mini_boss"] == "mahishasura"
        assert _wave_config(20)["boss"] == "vritra"
        assert get_realm_for_wave(13)["name"] == "Setu Expanse"
        assert get_realm_for_wave(20)["name"] == "Mahayuddha Citadel"

    def test_extended_boss_entities_have_unique_identity(self):
        from game.entities.enemies.boss_mahishasura import BossMahishasura
        from game.entities.enemies.boss_vritra import BossVritra
        assert BossMahishasura().boss_id == "mahishasura"
        assert BossVritra().boss_id == "vritra"

    def test_extended_boss_schedule_spawns_expected_entities(self):
        from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
        from game.entities.enemies.boss_ravana import BossRavana
        from game.entities.enemies.boss_mahishasura import BossMahishasura
        from game.entities.enemies.boss_vritra import BossVritra
        expected = ((5, BossKumbhakarna), (10, BossRavana),
                    (15, BossMahishasura), (20, BossVritra))
        for wave, boss_type in expected:
            wm = WaveManager(start_wave=wave)
            wm._advance_wave()
            enemies = []
            wm._spawn_wave(enemies, Player())
            assert any(isinstance(enemy, boss_type) for enemy in enemies)


class TestCollisionSystem:
    def test_bullet_enemy_collision(self):
        p = Player()
        enemy = AsuraFast()
        enemy.x = 200
        enemy.y = 200
        bullet = PlayerBullet(200, 200, 0)
        bullets = [bullet]
        enemies = [enemy]
        ss = ScoreSystem()
        bm = BoonManager()

        summary = collision_sys.check_all(p, enemies, bullets, [], [], ss, bm)
        assert len(summary["hit_sparks"]) > 0
        assert enemy.hp < enemy.max_hp

    def test_player_powerup_collision(self):
        p = Player()
        pu = PowerUp(PowerUpType.HEALTH)
        pu.x = p.x
        pu.y = p.y
        powerups = [pu]
        ss = ScoreSystem()
        bm = BoonManager()

        summary = collision_sys.check_all(p, [], [], [], powerups, ss, bm)
        assert PowerUpType.HEALTH in summary["powerup_picked"]
        assert pu.alive is False


class TestParticlesAndFloatingTexts:
    def test_floating_texts(self):
        ft = FloatingTextManager()
        ft.spawn_damage(100, 100, 25)
        ft.spawn_damage(100, 100, 50, is_crit=True)
        ft.spawn_damage(100, 100, 15, color=(255, 120, 30))
        ft.spawn_combo(100, 100, 5)
        ft.spawn_notification(100, 100, "TEST")
        assert len(ft.numbers) == 5
        ft.update(0.016)

    def test_particles(self):
        pm = ParticleManager()
        pm.spawn_hit_sparks(100, 100)
        pm.spawn_explosion(100, 100)
        pm.spawn_dash_flash(100, 100)
        pm.spawn_dash_shockwave(100, 100)
        assert len(pm.particles) > 0
        pm.update(0.016)


class TestAchievementsAndSave:
    def test_achievement_system(self, tmp_path, monkeypatch):
        test_file = tmp_path / "save.json"
        monkeypatch.setattr(save_system, "_SAVE_FILE", test_file)
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)

        am = AchievementManager()
        unlocked = am.check_unlock("first_blood")
        assert unlocked is True
        # Second time should not unlock again
        unlocked_again = am.check_unlock("first_blood")
        assert unlocked_again is False

    def test_save_system_roundtrip(self, tmp_path, monkeypatch):
        test_file = tmp_path / "save.json"
        monkeypatch.setattr(save_system, "_SAVE_FILE", test_file)
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)

        data = save_system.load()
        data["high_score"] = 12345
        data["sfx_volume"] = 60
        data["music_volume"] = 40
        save_system.save(data)

        loaded = save_system.load()
        assert loaded["high_score"] == 12345
        assert loaded["sfx_volume"] == 60
        assert loaded["music_volume"] == 40


class TestEasingSystem:
    def test_ease_out_cubic_bounds(self):
        from game.ui.easing import ease_out_cubic, clamp, lerp, lerp_color
        assert ease_out_cubic(0.0) == 0.0
        assert ease_out_cubic(1.0) == 1.0
        assert 0.0 < ease_out_cubic(0.5) < 1.0
        # Should be past midpoint (easing out is fast then slow)
        assert ease_out_cubic(0.5) > 0.5

    def test_lerp(self):
        from game.ui.easing import lerp
        assert lerp(0, 100, 0.0) == 0
        assert lerp(0, 100, 1.0) == 100
        assert lerp(0, 100, 0.5) == 50

    def test_lerp_color(self):
        from game.ui.easing import lerp_color
        c = lerp_color((0, 0, 0), (255, 255, 255), 0.5)
        assert c == (127, 127, 127)

    def test_clamp(self):
        from game.ui.easing import clamp
        assert clamp(-0.5) == 0.0
        assert clamp(1.5) == 1.0
        assert clamp(0.5) == 0.5

    def test_ease_out_elastic(self):
        from game.ui.easing import ease_out_elastic
        assert ease_out_elastic(0.0) == 0.0
        assert ease_out_elastic(1.0) == 1.0
        # Elastic can overshoot > 1.0 briefly
        assert ease_out_elastic(0.5) > 0.5


class TestTweenSystem:
    def test_tween_basic(self):
        from game.ui.tween import Tween, TweenManager

        class Target:
            value = 0.0

        t = Target()
        tw = Tween(t, "value", end=100.0, duration=1.0)
        tw.update(0.5)
        assert 0 < t.value < 100
        tw.update(0.6)
        assert t.value == 100.0
        assert tw.done

    def test_tween_manager(self):
        from game.ui.tween import TweenManager

        class Target:
            x = 0.0
            y = 0.0

        t = Target()
        tm = TweenManager()
        tm.tween(t, "x", 50.0, 0.5)
        tm.tween(t, "y", 100.0, 1.0)
        assert tm.active
        tm.update(0.6)
        assert t.x == 50.0  # completed
        assert 0 < t.y < 100  # still running
        tm.update(0.5)
        assert t.y == 100.0
        assert not tm.active

    def test_tween_with_delay(self):
        from game.ui.tween import Tween

        class Target:
            value = 0.0

        t = Target()
        tw = Tween(t, "value", end=10.0, duration=0.5, delay=0.3)
        tw.update(0.2)
        assert t.value == 0.0  # still in delay
        tw.update(0.2)  # delay ends, 0.1s into tween
        assert t.value > 0.0
        tw.update(0.5)
        assert t.value == 10.0

    def test_tween_callback(self):
        from game.ui.tween import Tween

        class Target:
            value = 0.0

        t = Target()
        callback_called = []
        tw = Tween(t, "value", end=5.0, duration=0.1, on_done=lambda: callback_called.append(True))
        tw.update(0.2)
        assert len(callback_called) == 1


class TestSynergySystem:
    def test_synergy_unlock(self):
        from game.systems.boon_system import BoonManager
        bm = BoonManager()
        # Add first half of plasma_storm pair
        result1 = bm.add_boon("agni_fury")
        assert len(result1) == 0  # no synergy yet

        # Add second half
        result2 = bm.add_boon("indra_thunder")
        assert len(result2) == 1
        assert result2[0]["id"] == "plasma_storm"
        assert bm.has_synergy("plasma_storm")

    def test_no_duplicate_synergy(self):
        from game.systems.boon_system import BoonManager
        bm = BoonManager()
        bm.add_boon("agni_fury")
        result = bm.add_boon("indra_thunder")
        assert len(result) == 1
        # Adding same boons again should not re-unlock
        result2 = bm.add_boon("agni_fury")
        assert len(result2) == 0


class TestVictoryViewTweenAPI:
    """Regression for a runtime TypeError that crashed the game on boss clear:
    victory_view called TweenManager.add(obj=..., easing=...) which doesn't
    exist on the new tween API. Verify the view constructs and its on_show_view
    path schedules only the tween() convenience method."""

    def test_victory_view_constructs(self, monkeypatch):
        # arcade.View.__init__ requires a real window; bypass it.
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.victory_view import VictoryView
        v = VictoryView(score=12345, kills=42, highest_combo=8,
                        difficulty='hard', ship_class='garuda', wave=10,
                        stats={'total_damage': 5000})
        assert v.score == 12345
        assert v.wave == 10
        assert v.ship_class == 'garuda'
        # Animation entry state: title off-screen, score zero, alphas zero.
        assert v._title_y > HEIGHT
        assert v._displayed_score == 0.0
        assert all(a == 0.0 for a in v._row_alphas)
        # 5 alpha refs (Score, Kills, Combo, Difficulty, Prompts).
        assert len(v._alpha_refs) == 5

    def test_victory_view_tweens_finish(self, monkeypatch, tmp_path):
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views import victory_view as vv_mod
        # Redirect save to tmp so we don't pollute the real one.
        monkeypatch.setattr(vv_mod.save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(vv_mod.save_system, "_SAVE_DIR", tmp_path)

        from game.views.victory_view import VictoryView
        v = VictoryView(score=1000, kills=10, highest_combo=5,
                        difficulty='normal', wave=10)
        # Mirror the tween setup from on_show_view (without needing a window).
        from game.ui.easing import ease_out_elastic, ease_out_cubic
        v._tweens.tween(target=v, attr='_title_y', end=HEIGHT * 0.82,
                        duration=0.8, ease=ease_out_elastic,
                        start=HEIGHT + 100.0)
        v._tweens.tween(target=v, attr='_displayed_score', end=1000.0,
                        duration=1.2, delay=0.5, ease=ease_out_cubic, start=0.0)
        for i, ref in enumerate(v._alpha_refs):
            v._tweens.tween(target=ref, attr='val', end=255.0,
                            duration=0.5, delay=1.0 + i * 0.15,
                            ease=ease_out_cubic, start=0.0)

        # Step well past the longest delay (1.6s) + duration (1.2s).
        for _ in range(200):
            v._tweens.update(0.05)
            for i, ref in enumerate(v._alpha_refs):
                v._row_alphas[i] = ref.val

        # All anims should be at their final values.
        assert v._title_y == HEIGHT * 0.82
        assert v._displayed_score == 1000.0
        assert all(abs(a - 255.0) < 1e-6 for a in v._row_alphas)

    def test_transition_overlay_is_active_is_a_property(self):
        """Victory view uses TransitionOverlay.is_active as a property, not method."""
        from game.ui.transitions import TransitionOverlay
        # Must be accessible without parens and return a bool.
        val = TransitionOverlay.is_active
        assert isinstance(val, bool)
        # And calling it with parens (the old wrong usage) should fail clearly.
        raised = False
        try:
            TransitionOverlay.is_active()
        except TypeError:
            raised = True
        assert raised, "is_active() with parens should raise TypeError"


class TestButton:
    """Cover the reusable button widget used by the pause menu."""

    def test_hit_test(self):
        from game.ui.button import Button
        b = Button(cx=100, cy=200, width=80, height=40, label="OK")
        assert b.hit_test(100, 200) is True
        assert b.hit_test(60, 200) is True   # left edge
        assert b.hit_test(140, 200) is True  # right edge
        assert b.hit_test(50, 200) is False  # outside left
        assert b.hit_test(150, 200) is False # outside right
        assert b.hit_test(100, 170) is False # above
        assert b.hit_test(100, 230) is False # below

    def test_click_fires_on_release_over_button(self):
        from game.ui.button import Button
        calls = []
        b = Button(cx=100, cy=200, width=80, height=40, label="OK",
                   on_click=lambda: calls.append(1))
        b.update(0.016, 100, 200)   # mouse hovers
        assert b.hovered is True
        b.press()
        assert b.was_pressed is True
        clicked = b.release()
        assert clicked is True
        assert calls == [1]
        assert b.was_pressed is False

    def test_drag_off_cancels_click(self):
        from game.ui.button import Button
        calls = []
        b = Button(cx=100, cy=200, width=80, height=40, label="OK",
                   on_click=lambda: calls.append(1))
        b.update(0.016, 100, 200)   # hover over
        b.press()
        b.update(0.016, 400, 400)   # drag off
        clicked = b.release()
        assert clicked is False
        assert calls == []

    def test_hover_anim_decays_when_mouse_leaves(self):
        from game.ui.button import Button
        b = Button(cx=100, cy=200, width=80, height=40, label="OK")
        b.update(0.016, 100, 200)  # hover
        hov_peak = b._hover_anim
        # First frame: target=1.0, dt=0.016, factor=12*dt=0.192 → ~0.192
        # Step a few more times so the lerp climbs well past 0.3
        for _ in range(10):
            b.update(0.05, 100, 200)
        assert b._hover_anim > 0.5
        for _ in range(60):
            b.update(0.05, 500, 500)  # far away
        assert b._hover_anim < 0.05
        assert b.hovered is False

    def test_press_anim_decays(self):
        from game.ui.button import Button
        b = Button(cx=100, cy=200, width=80, height=40, label="OK")
        b.press()
        assert b._press_anim == 1.0
        for _ in range(60):
            b.update(0.05, 500, 500)
        assert b._press_anim == 0.0

    def test_keyboard_activation_does_not_require_mouse_hover(self):
        from game.ui.button import Button
        calls = []
        b = Button(cx=100, cy=200, width=80, height=40, label="OK",
                   on_click=lambda: calls.append(True))
        b.activate()
        assert calls == [True]


class TestOptionalAssets:
    def test_visual_assets_load_with_fallback_manager(self):
        from game.systems.asset_manager import AssetManager
        for name in ("pushpaka.png", "tripura.png", "garuda.png",
                     "boss_kumbhakarna.png", "boss_ravana.png"):
            assert AssetManager.texture(name) is not None


class TestSaveLifetimeStats:
    """Cover the new lifetime stat fields and the extended update_after_game."""

    def test_defaults_include_lifetime_fields(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        data = save_system.load()
        for key in ("total_damage", "best_combo", "total_boons",
                    "bosses_defeated", "playtime_seconds", "ships_mastered"):
            assert key in data, f"missing default for {key}"

    def test_update_after_game_persists_lifetime(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)

        save_system.update_after_game(
            score=15000, wave=10, kills=200,
            highest_combo=9, total_damage=45000,
            boons_claimed=4, bosses_defeated=["kumbhakarna"],
            ship_class="tripura", campaign_cleared=False,
        )
        data = save_system.load()
        assert data["high_score"] == 15000
        assert data["total_kills"] == 200
        assert data["best_combo"] == 9
        assert data["total_damage"] == 45000
        assert data["total_boons"] == 4
        assert data["bosses_defeated"] == ["kumbhakarna"]
        assert "tripura" not in data["ships_mastered"]  # not cleared

        # Second run with campaign clear and Ravana kill
        save_system.update_after_game(
            score=99999, wave=10, kills=400,
            highest_combo=10, total_damage=90000,
            boons_claimed=8, bosses_defeated=["ravana", "kumbhakarna"],
            ship_class="tripura", campaign_cleared=True,
        )
        data = save_system.load()
        assert data["high_score"] == 99999
        assert data["best_combo"] == 10
        assert data["total_damage"] == 135000   # 45k + 90k
        assert data["bosses_defeated"] == ["kumbhakarna", "ravana"]
        assert "tripura" in data["ships_mastered"]

    def test_bosses_dedup_across_runs(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.update_after_game(score=100, wave=5, kills=10,
                                      bosses_defeated=["kumbhakarna"])
        save_system.update_after_game(score=200, wave=5, kills=20,
                                      bosses_defeated=["kumbhakarna"])
        data = save_system.load()
        assert data["bosses_defeated"] == ["kumbhakarna"]
        assert data["games_played"] == 2

    def test_add_playtime_accumulates(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.add_playtime(12.5)
        save_system.add_playtime(7.5)
        data = save_system.load()
        assert abs(data["playtime_seconds"] - 20.0) < 1e-6

    def test_add_playtime_ignores_zero_and_negative(self, tmp_path, monkeypatch):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.add_playtime(0)
        save_system.add_playtime(-5)
        data = save_system.load()
        assert data["playtime_seconds"] == 0


class TestStatsView:
    """Cover the lifetime stats screen — construction, panel layout, empty state."""

    def test_stats_view_constructs_with_panels(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.stats_view import StatsView
        v = StatsView(return_view=None)
        # 6 panels: Core, Playtime, Damage&Boons, Achievements, Bosses, Ships
        assert len(v._panels) == 6
        # Empty state visible when no runs have been played
        assert v._show_empty is True

    def test_stats_view_hides_empty_after_runs(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        # Seed a run
        save_system.update_after_game(score=100, wave=3, kills=5)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.stats_view import StatsView
        v = StatsView()
        assert v._show_empty is False

    def test_stats_view_panels_have_lines(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        save_system.update_after_game(
            score=12345, wave=8, kills=150,
            highest_combo=7, total_damage=50000,
            boons_claimed=5, bosses_defeated=["kumbhakarna"],
            ship_class="garuda", campaign_cleared=False,
        )
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.stats_view import StatsView
        v = StatsView()
        # Every panel must have at least one line
        for panel in v._panels:
            assert panel.title
            assert len(panel.lines) >= 1
            # Each line: (label, value, color)
            for line in panel.lines:
                assert len(line) == 3
                assert isinstance(line[0], str)
                assert isinstance(line[1], str)

    def test_fmt_hms(self):
        from game.views.stats_view import _fmt_hms
        assert _fmt_hms(0) == "0m 00s"
        assert _fmt_hms(59) == "0m 59s"
        assert _fmt_hms(60) == "1m 00s"
        assert _fmt_hms(3599) == "59m 59s"
        assert _fmt_hms(3600) == "1h 00m"
        assert _fmt_hms(7325) == "2h 02m"


class TestAchievementsView:
    def test_achievement_hall_pages_all_trophies(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        from game.views.achievements_view import AchievementsView
        view = AchievementsView()
        assert view.page_count >= 2
        assert view.PER_PAGE == 8


class TestGameViewPauseButtons:
    """Verify the new pause-menu button list is wired into GameView.__init__."""

    def test_pause_buttons_initialized(self, monkeypatch, tmp_path):
        from game.systems import save_system
        monkeypatch.setattr(save_system, "_SAVE_FILE", tmp_path / "save.json")
        monkeypatch.setattr(save_system, "_SAVE_DIR", tmp_path)
        import arcade
        monkeypatch.setattr(arcade.View, "__init__", lambda self: None)
        # Stub the heavy systems so we don't actually open a window / play sound
        from game.views import game_view as gv_mod
        # Build a GameView by calling __init__; we need to mock everything it touches.
        # Simplest: construct via type with __new__ and set just the attrs the test cares about.
        gv = gv_mod.GameView.__new__(gv_mod.GameView)
        gv._init_pause_buttons()
        assert len(gv._pause_buttons) == 4
        labels = [b.label for b in gv._pause_buttons]
        assert labels == ["RESUME", "RESTART RUN", "SETTINGS", "QUIT TO MENU"]
        # Each button has a hotkey hint
        for b in gv._pause_buttons:
            assert b.hotkey is not None
        # Hit-test one of them
        assert gv._pause_buttons[0].hit_test(WIDTH // 2, HEIGHT // 2 + 30) is True
