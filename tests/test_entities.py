"""
tests/test_entities.py
Unit tests for all game entities.
"""
import pytest
from constants import (
    WIDTH, HEIGHT,
    PLAYER_MAX_HP,
    PLAYER_BULLET_DAMAGE,
    ASURA_FAST_HP,
    ASURA_TANK_HP,
    ASURA_RANGED_HP,
    ASURA_KAMIKAZE_HP,
    KUMBHAKARNA_HP,
    RAVANA_HP,
)
from game.entities.player import Player
from game.entities.bullet import PlayerBullet, EnemyBullet
from game.entities.chakram import Chakram
from game.entities.powerup import PowerUp, PowerUpType, PowerUpEffect
from game.entities.ship_classes import SHIP_CLASSES
from game.entities.enemies.asura_fast import AsuraFast
from game.entities.enemies.asura_tank import AsuraTank
from game.entities.enemies.asura_ranged import AsuraRanged
from game.entities.enemies.asura_kamikaze import AsuraKamikaze
from game.entities.enemies.asura_healer import AsuraHealer
from game.entities.enemies.asura_sniper import AsuraSniper
from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
from game.entities.enemies.boss_ravana import BossRavana


class TestPlayer:
    def test_player_init(self):
        p = Player()
        assert p.hp == PLAYER_MAX_HP
        assert p.alive is True
        assert p.x == WIDTH / 2
        assert p.y == HEIGHT / 2
        assert p.dash_charges >= 1

    def test_player_take_damage(self):
        p = Player()
        initial_hp = p.hp
        hit = p.take_damage(20)
        assert hit is True
        assert p.hp == initial_hp - 20

    def test_player_heal(self):
        p = Player()
        p.take_damage(40)
        p.heal(25)
        assert p.hp == PLAYER_MAX_HP - 15
        p.heal(100)
        assert p.hp == p.max_hp

    def test_player_shield_powerup(self):
        p = Player()
        p.apply_powerup(PowerUpType.SHIELD)
        assert p.shield_hits > 0
        initial_hp = p.hp
        hit = p.take_damage(30)
        assert hit is False  # absorbed by shield
        assert p.hp == initial_hp

    def test_player_dash(self):
        p = Player()
        assert p.dash_ready is True
        dashed = p.trigger_dash()
        assert dashed is True
        assert p.is_dashing is True

    def test_ship_classes(self):
        for sid, sdata in SHIP_CLASSES.items():
            p = Player()
            p.apply_ship_class(sdata)
            assert p.max_hp == sdata["hp"]
            assert p.hp == sdata["hp"]
            assert p.fire_rate_stat == sdata["fire_rate"]
            if sid == "garuda":
                assert p.dash_charges_max == 2


class TestBulletsAndAbilities:
    def test_player_bullet(self):
        b = PlayerBullet(100, 100, 90)
        assert b.damage == PLAYER_BULLET_DAMAGE
        assert b.alive is True
        b.update(0.016)
        assert b.y > 100

    def test_enemy_bullet(self):
        eb = EnemyBullet(200, 200, 0)
        assert eb.alive is True
        eb.update(0.016)
        assert eb.x > 200

    def test_chakram(self):
        chk = Chakram(300, 300, 45)
        assert chk.alive is True
        chk.update(0.016, 300, 300)
        assert chk.alive is True


class TestPowerups:
    def test_powerup_creation(self):
        for ptype in PowerUpType:
            pu = PowerUp(ptype)
            assert pu.type == ptype
            assert pu.alive is True

    def test_powerup_effect_expiration(self):
        eff = PowerUpEffect(PowerUpType.SPEED)
        assert eff.expired is False
        eff.update(eff.duration + 1.0)
        assert eff.expired is True


class TestEnemies:
    def test_asura_fast(self):
        e = AsuraFast()
        assert e.hp == ASURA_FAST_HP
        assert e.alive is True
        e.update(0.016, 100, 100)

    def test_asura_tank(self):
        e = AsuraTank()
        assert e.hp == ASURA_TANK_HP
        assert e.alive is True

    def test_asura_ranged(self):
        e = AsuraRanged()
        assert e.hp == ASURA_RANGED_HP
        bullets = e.update(0.016, 100, 100)
        assert isinstance(bullets, list)

    def test_asura_kamikaze(self):
        e = AsuraKamikaze()
        assert e.hp == ASURA_KAMIKAZE_HP
        e.explode()
        assert e.exploded is True
        assert e.is_dead() is True

    def test_asura_healer(self):
        e = AsuraHealer()
        assert e.alive is True
        ally = AsuraFast()
        ally.x = e.x + 50
        ally.y = e.y + 50
        ally.hp = 10
        e._heal_timer = 0.0
        healed = e.perform_heal_pulse([ally])
        assert healed is True
        assert ally.hp > 10

    def test_asura_sniper(self):
        e = AsuraSniper()
        assert e.alive is True

    def test_boss_kumbhakarna(self):
        boss = BossKumbhakarna()
        assert boss.hp == KUMBHAKARNA_HP
        assert boss.alive is True

    def test_boss_ravana(self):
        boss = BossRavana()
        assert boss.hp == RAVANA_HP
        assert boss.phase == 1
        boss.take_damage(int(RAVANA_HP * 0.4))
        boss._update_phase()
        assert boss.phase == 2
