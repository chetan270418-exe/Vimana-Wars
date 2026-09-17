"""
game/systems/collision.py
Centralised circle-circle collision detection.
Runs all checks in one place so game_view stays clean.
"""
import math
from constants import PLAYER_CONTACT_DAMAGE


def _circles_overlap(ax, ay, ar, bx, by, br) -> bool:
    return math.hypot(ax - bx, ay - by) < ar + br


def check_all(
    player,
    enemies: list,
    player_bullets: list,
    enemy_bullets: list,
    powerups: list,
    score_system,
    boon_manager,
) -> dict:
    """
    Run every collision pair. Mutates entity lists and player state in place.
    Returns a summary dict with event coordinates for particles and SFX.
    """
    summary = {
        "kills": 0,
        "player_hit": False,
        "powerup_picked": [],
        "kamikaze_exploded": False,
        "hit_sparks": [],      # [(x, y, color)]
        "explosions": [],      # [(x, y, radius, color)]
        "powerup_auras": [],   # [(x, y, color)]
        "bullet_hits": [],     # [(x, y, enemy)]
    }

    px, py, pr = player.x, player.y, player.radius

    # ── 1. Player bullets ↔ enemies ──────────────────────────────────────
    for bullet in player_bullets[:]:
        if not bullet.alive:
            continue
        for enemy in enemies:
            if not enemy.alive:
                continue
            
            is_piercing = getattr(bullet, "is_piercing", False)
            if is_piercing:
                if not hasattr(bullet, "hit_enemies"):
                    bullet.hit_enemies = set()
                if enemy in bullet.hit_enemies:
                    continue

            if _circles_overlap(bullet.x, bullet.y, bullet.radius,
                                 enemy.x, enemy.y, enemy.radius):
                dmg = bullet.damage
                is_crit = False
                if boon_manager.has_boon("yama_execution") and enemy.max_hp > 0 and (enemy.hp / enemy.max_hp) < 0.45:
                    dmg = int(dmg * 1.6)
                    is_crit = True
                enemy.take_damage(dmg)
                summary["hit_sparks"].append((bullet.x, bullet.y, (255, 240, 100) if not is_crit else (255, 80, 80)))
                summary["bullet_hits"].append((bullet.x, bullet.y, enemy))

                if boon_manager.has_boon("agni_fury"):
                    enemy._burning = 3.0

                if enemy.is_dead():
                    summary["kills"] += 1
                    score_system.register_kill(enemy.score_value)
                    player.enemies_killed += 1
                    base_col = getattr(enemy, "_color", (255, 120, 30))
                    
                    if boon_manager.has_boon("agni_fury") and getattr(enemy, "_burning", 0) > 0:
                        summary["explosions"].append((enemy.x, enemy.y, enemy.radius * 1.5, (255, 120, 30)))
                        for other in enemies:
                            if other is not enemy and other.alive:
                                if _circles_overlap(enemy.x, enemy.y, enemy.radius * 2, other.x, other.y, other.radius):
                                    other.take_damage(25)
                                    if other.is_dead():
                                        summary["kills"] += 1
                                        score_system.register_kill(other.score_value)
                                        player.enemies_killed += 1
                                        summary["explosions"].append((other.x, other.y, other.radius, (255, 120, 30)))
                    else:
                        summary["explosions"].append((enemy.x, enemy.y, enemy.radius, base_col))
                
                if is_piercing:
                    bullet.hit_enemies.add(enemy)
                else:
                    bullet.alive = False
                    break   # one bullet hits one enemy

    # ── 2. Enemy bullets ↔ player ────────────────────────────────────────
    for bullet in enemy_bullets[:]:
        if not bullet.alive:
            continue
        if _circles_overlap(bullet.x, bullet.y, bullet.radius, px, py, pr):
            hit = player.take_damage(bullet.damage)
            bullet.alive = False
            summary["hit_sparks"].append((bullet.x, bullet.y, (255, 80, 80)))
            if hit:
                summary["player_hit"] = True

    # ── 3. Enemy contact ↔ player ────────────────────────────────────────
    for enemy in enemies:
        if not enemy.alive:
            continue
        if _circles_overlap(enemy.x, enemy.y, enemy.radius, px, py, pr):
            # Kamikaze: AOE explosion
            from game.entities.enemies.asura_kamikaze import AsuraKamikaze
            if isinstance(enemy, AsuraKamikaze) and not enemy.exploded:
                enemy.explode()
                hit = player.take_damage(enemy.explosion_damage)
                summary["kamikaze_exploded"] = True
                summary["explosions"].append((enemy.x, enemy.y, enemy.explosion_radius, (255, 60, 60)))
                if hit:
                    summary["player_hit"] = True
                # AOE: also hurt nearby enemies with the shockwave
                for other in enemies:
                    if other is not enemy and other.alive:
                        if _circles_overlap(enemy.x, enemy.y,
                                            enemy.explosion_radius,
                                            other.x, other.y, other.radius):
                            other.take_damage(20)
                            if other.is_dead():
                                summary["kills"] += 1
                                score_system.register_kill(other.score_value)
                                player.enemies_killed += 1
                                summary["explosions"].append((other.x, other.y, other.radius, (255, 120, 30)))
            else:
                # Normal contact damage
                contact_dmg = getattr(enemy, "contact_damage", PLAYER_CONTACT_DAMAGE)
                hit = player.take_damage(contact_dmg)
                if hit:
                    summary["player_hit"] = True
                    summary["hit_sparks"].append((player.x, player.y, (255, 100, 100)))

    # ── 4. Player ↔ power-ups ─────────────────────────────────────────────
    for pu in powerups[:]:
        if not pu.alive:
            continue
        if _circles_overlap(pu.x, pu.y, pu.radius, px, py, pr):
            player.apply_powerup(pu.type)
            summary["powerup_picked"].append(pu.type)
            summary["powerup_auras"].append((pu.x, pu.y, getattr(pu, "_color", (255, 220, 60))))
            pu.alive = False

    return summary
