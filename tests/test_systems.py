"""
tests/test_systems.py
Unit tests for all core gameplay systems.
"""
import pytest
from game.entities.player import Player
from game.entities.bullet import PlayerBullet, EnemyBullet
from game.entities.powerup import PowerUp, PowerUpType
from game.entities.enemies.asura_fast import AsuraFast
from game.entities.enemies.asura_tank import AsuraTank
from game.entities.enemies.asura_kamikaze import AsuraKamikaze
from game.systems.score_system import ScoreSystem
from game.systems.boon_system import BoonManager, BOONS_DATABASE
from game.systems.wave_manager import WaveManager
from game.systems.floating_text import FloatingTextManager
from game.systems.particles import ParticleManager
from game.systems.achievement_system import AchievementManager
from game.systems import collision as collision_sys
from game.systems import save_system


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
