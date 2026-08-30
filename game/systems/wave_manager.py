"""
game/systems/wave_manager.py
Controls wave progression, 3-2-1 countdowns, wave objectives, and diverse enemy fleet spawns.
"""
import random
from constants import (
    WAVE_CLEAR_DELAY,
    BOSS_WAVE_NUMBER, POWERUP_SPAWN_EVERY_N_WAVES,
    MAX_POWERUPS_ACTIVE, get_realm_for_wave,
)


def _wave_config(wave_num: int) -> dict:
    effective = ((wave_num - 1) % BOSS_WAVE_NUMBER) + 1

    if effective == 10:
        return {"boss": True}
    elif effective == 5:
        return {"mini_boss": True, "fast": 3, "kamikaze": 2}

    configs = [
        {"fast": 5},                                          # 1
        {"fast": 6, "healer": 1},                             # 2
        {"fast": 6, "kamikaze": 3},                           # 3
        {"fast": 4, "tank": 2, "sniper": 1},                  # 4
        {"mini_boss": True, "fast": 3},                       # 5
        {"fast": 5, "tank": 2, "healer": 1, "kamikaze": 3},   # 6
        {"fast": 4, "ranged": 3, "sniper": 2},                # 7
        {"fast": 5, "tank": 3, "ranged": 2, "healer": 1},     # 8
        {"fast": 6, "tank": 3, "sniper": 2, "kamikaze": 4},   # 9
    ]
    return configs[effective - 1]


class WaveManager:
    def __init__(self, spawn_mult: float = 1.0, enemy_spd_mult: float = 1.0, is_endless: bool = False):
        self.wave_number = 0
        self.boss_alive = False
        self.boss_wave_cleared = False
        self._difficulty_mult = spawn_mult
        self.enemy_speed_mult = enemy_spd_mult
        self.is_endless = is_endless

        # State machine: CLEAR_PAUSE -> COUNTDOWN -> SPAWNING -> FIGHTING
        self._state = "CLEAR_PAUSE"
        self._timer = WAVE_CLEAR_DELAY
        self.announce_text = ""
        self.announce_subtitle = ""
        self.announce_alpha = 0
        self.countdown_val = 3

        # Objective & Enemy tracking
        self.current_objective = "Defeat all Asuras"
        self.total_wave_enemies = 0
        self.wave_time = 0.0
        self.took_damage_this_wave = False

        # Power-up spawning
        self._waves_since_powerup = 0

    def update(self, delta_time: float, enemies: list, powerups: list, player=None) -> None:
        if self._state == "COUNTDOWN":
            self._timer -= delta_time
            self.countdown_val = max(1, int(self._timer + 1))
            self.announce_alpha = max(0, min(255, int(255 * (self._timer / 2.0))))

            if self._timer <= 0:
                self._state = "SPAWNING"

        elif self._state == "SPAWNING":
            self._spawn_wave(enemies, player)
            self.total_wave_enemies = len(enemies)
            self._state = "FIGHTING"
            self.wave_time = 0.0
            self.took_damage_this_wave = False

        elif self._state == "FIGHTING":
            self.wave_time += delta_time
            all_dead = (len(enemies) == 0) or all(not e.alive for e in enemies)
            if all_dead:
                if self.boss_alive:
                    self.boss_alive = False
                    self._waves_since_powerup += 1
                    self._maybe_spawn_powerup(powerups)
                    if self.wave_number == BOSS_WAVE_NUMBER and not self.is_endless:
                        self.boss_wave_cleared = True
                        return
                self._state = "CLEAR_PAUSE"
                self._timer = WAVE_CLEAR_DELAY

        elif self._state == "CLEAR_PAUSE":
            self._timer -= delta_time
            if self._timer <= 0:
                self._advance_wave()

    def _advance_wave(self) -> None:
        self.wave_number += 1
        realm = get_realm_for_wave(self.wave_number)

        if self.wave_number > BOSS_WAVE_NUMBER:
            loops = (self.wave_number - 1) // BOSS_WAVE_NUMBER
            self._difficulty_mult = 1.0 + loops * 0.3

        self._waves_since_powerup += 1

        wave_objectives = {
            1: "Eliminate Asura Chaser scouts [5 vessels]",
            2: "Priority Target: Eliminate the Support Healer!",
            3: "Evasive Action: Evade and destroy Kamikaze swarm",
            4: "Armor Piercing: Crack 2 Heavy Brutes & Snipers",
            5: "Defeat the Armored Titan Kumbhakarna",
            6: "Survive Crossfire: Clear mixed Asura armada",
            7: "Long-Range Threat: Neutralize backline Snipers",
            8: "Break the Phalanx: Dismantle Heavy Battlefleet",
            9: "Armageddon Swarm: Annihilate vanguard assault fleet",
            10: "Vanquish the Ten-Headed Demon King Ravana",
        }

        effective = ((self.wave_number - 1) % BOSS_WAVE_NUMBER) + 1
        self.current_objective = wave_objectives.get(effective, "Eliminate all incoming Asura vessels")

        if self.wave_number == BOSS_WAVE_NUMBER:
            self.announce_text = "BOSS WAVE — RAVANA APPROACHES!"
            self.announce_subtitle = f"Realm of {realm['name']} • {realm['subtitle']}"
        elif (self.wave_number % BOSS_WAVE_NUMBER) == 5:
            self.announce_text = "MINI-BOSS — KUMBHAKARNA AWAKENS!"
            self.announce_subtitle = f"Realm of {realm['name']} • {realm['subtitle']}"
        else:
            self.announce_text = f"Wave {self.wave_number}"
            self.announce_subtitle = f"Realm: {realm['name']} — {realm['subtitle']}"

        self._timer = 2.4
        self._state = "COUNTDOWN"

    def _spawn_wave(self, enemies: list, player=None) -> None:
        config = _wave_config(self.wave_number)

        if config.get("boss"):
            from game.entities.enemies.boss_ravana import BossRavana
            boss = BossRavana()
            boss.speed *= self.enemy_speed_mult
            enemies.append(boss)
            self.boss_alive = True
            return

        if config.get("mini_boss"):
            from game.entities.enemies.boss_kumbhakarna import BossKumbhakarna
            mini = BossKumbhakarna()
            mini.speed *= self.enemy_speed_mult
            enemies.append(mini)
            self.boss_alive = True

        mult = self._difficulty_mult
        from constants import WIDTH, HEIGHT
        px = player.x if player else WIDTH / 2
        py = player.y if player else HEIGHT / 2

        def add(cls, n):
            for _ in range(max(1, int(n * mult))):
                try:
                    e = cls(safe_player_x=px, safe_player_y=py)
                except TypeError:
                    e = cls()
                e.speed *= self.enemy_speed_mult
                if self.wave_number >= 3 and random.random() < 0.15:
                    e.hp *= 2
                    e.max_hp = e.hp
                    e.score_value *= 2
                    setattr(e, "is_elite", True)
                enemies.append(e)

        from game.entities.enemies.asura_fast     import AsuraFast
        from game.entities.enemies.asura_tank     import AsuraTank
        from game.entities.enemies.asura_ranged   import AsuraRanged
        from game.entities.enemies.asura_kamikaze import AsuraKamikaze
        from game.entities.enemies.asura_healer   import AsuraHealer
        from game.entities.enemies.asura_sniper   import AsuraSniper

        if config.get("fast"):     add(AsuraFast,     config["fast"])
        if config.get("tank"):     add(AsuraTank,     config["tank"])
        if config.get("ranged"):   add(AsuraRanged,   config["ranged"])
        if config.get("kamikaze"): add(AsuraKamikaze, config["kamikaze"])
        if config.get("healer"):   add(AsuraHealer,   config["healer"])
        if config.get("sniper"):   add(AsuraSniper,   config["sniper"])

    def _maybe_spawn_powerup(self, powerups: list) -> None:
        if len(powerups) >= MAX_POWERUPS_ACTIVE:
            return
        if self._waves_since_powerup >= POWERUP_SPAWN_EVERY_N_WAVES:
            from game.entities.powerup import PowerUp
            powerups.append(PowerUp())
            self._waves_since_powerup = 0

    @property
    def is_boss_wave(self) -> bool:
        return (self.wave_number % BOSS_WAVE_NUMBER) == 0

    @property
    def is_mini_boss_wave(self) -> bool:
        return (self.wave_number % BOSS_WAVE_NUMBER) == 5

    @property
    def is_announcing(self) -> bool:
        return self._state == "COUNTDOWN"

    @property
    def is_clearing(self) -> bool:
        return self._state == "CLEAR_PAUSE" and self.wave_number > 0

    @property
    def is_fighting(self) -> bool:
        return self._state == "FIGHTING"
