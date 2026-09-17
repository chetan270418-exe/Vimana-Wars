import { SHIPS } from '../data/gameData';
import { sound } from './audio';
import { getActiveDuelSocket } from '../lib/socket';
import type { RunConfig, RunResult, DuelConfig, DuelResult } from '../types/game';

export interface CombatEngineOptions {
  canvas: HTMLCanvasElement;
  mode: 'single' | 'duel';
  runConfig?: RunConfig;
  duelConfig?: DuelConfig;
  activeBoons?: string[];
  onWaveComplete?: (wave: number) => void;
  onGameOver?: (result: RunResult) => void;
  onVictory?: (result: RunResult) => void;
  onDuelOver?: (result: DuelResult) => void;
  onPauseToggle?: (paused: boolean) => void;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  color: string;
  size: number;
  life: number;
  maxLife: number;
}

interface FloatingText {
  x: number;
  y: number;
  text: string;
  color: string;
  life: number;
  maxLife: number;
}

interface Projectile {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  damage: number;
  isPlayer: boolean;
  ownerId: string; // 'p1', 'p2', or 'enemy'
  color: string;
}

interface AsuraEnemy {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  hp: number;
  maxHp: number;
  type: 'fast' | 'ranged' | 'tank' | 'boss';
  color: string;
  shootCooldown: number;
  maxCooldown: number;
  scoreValue: number;
}

export class CombatEngine {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private animId: number | null = null;
  private lastTime: number = 0;
  private isPaused: boolean = false;
  private isDestroyed: boolean = false;

  public mode: 'single' | 'duel';
  private runConfig?: RunConfig;
  private duelConfig?: DuelConfig;
  private activeBoons: string[] = [];

  // Callbacks
  private onWaveComplete?: (wave: number) => void;
  private onGameOver?: (result: RunResult) => void;
  private onVictory?: (result: RunResult) => void;
  private onDuelOver?: (result: DuelResult) => void;
  private onPauseToggle?: (paused: boolean) => void;

  // Key tracking
  private keys: Record<string, boolean> = {};

  // Entities
  private projectiles: Projectile[] = [];
  private enemies: AsuraEnemy[] = [];
  private particles: Particle[] = [];
  private floatingTexts: FloatingText[] = [];

  // Stars background
  private stars: Array<{ x: number; y: number; speed: number; size: number; color: string }> = [];

  // Player 1 state
  public p1 = {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    radius: 20,
    hp: 100,
    maxHp: 100,
    shield: 50,
    maxShield: 50,
    shieldRegenTimer: 0,
    speed: 380,
    dashCooldown: 0,
    fireCooldown: 0,
    fireRate: 0.18,
    color: '#E9C400',
    name: 'Pushpaka',
    shipId: 'pushpaka',
  };

  // Player 2 state (for 1v1 PvP Duel)
  public p2 = {
    x: 0,
    y: 0,
    vx: 0,
    vy: 0,
    radius: 20,
    hp: 100,
    maxHp: 100,
    shield: 50,
    maxShield: 50,
    shieldRegenTimer: 0,
    speed: 380,
    dashCooldown: 0,
    fireCooldown: 0,
    fireRate: 0.18,
    color: '#FF6B72',
    name: 'Garuda',
    shipId: 'garuda',
  };

  // Single player progression metrics
  public wave: number = 1;
  public maxWaves: number = 20;
  public score: number = 0;
  public kills: number = 0;
  public totalDamage: number = 0;
  public highestCombo: number = 0;
  public currentCombo: number = 0;
  public comboTimer: number = 0;
  private waveSpawnTimer: number = 0;
  private waveEnemiesSpawned: number = 0;
  private waveEnemiesTarget: number = 8;
  private startTime: number = Date.now();

  constructor(opts: CombatEngineOptions) {
    this.canvas = opts.canvas;
    const ctx = opts.canvas.getContext('2d');
    if (!ctx) throw new Error('Could not get 2D canvas context');
    this.ctx = ctx;

    this.mode = opts.mode;
    this.runConfig = opts.runConfig;
    this.duelConfig = opts.duelConfig;
    this.activeBoons = opts.activeBoons || [];
    this.onWaveComplete = opts.onWaveComplete;
    this.onGameOver = opts.onGameOver;
    this.onVictory = opts.onVictory;
    this.onDuelOver = opts.onDuelOver;
    this.onPauseToggle = opts.onPauseToggle;

    this.initCanvasSize();
    this.initStars();
    this.initShips();
    if (this.mode === 'duel' && this.duelConfig?.roomCode) {
      this.bindOnlineDuelSocket();
    }
    this.bindEvents();
    this.start();
  }

  private bindOnlineDuelSocket() {
    const sock = getActiveDuelSocket();
    if (!sock) return;
    sock.updateHandlers({
      onOpponentState: (state) => {
        if (this.isDestroyed) return;
        this.p2.x = state.x;
        this.p2.y = state.y;
        if (state.firing && this.p2.fireCooldown <= 0) {
          this.p2.fireCooldown = this.p2.fireRate;
          this.firePlayerLaser(this.p2.x, this.p2.y - this.p2.radius, 'p2', this.p2.color);
        }
        if (state.dash) {
          sound.playDash();
          this.spawnThrustBurst(this.p2.x, this.p2.y, this.p2.color, 16);
        }
      },
      onHpUpdate: (update) => {
        if (this.isDestroyed) return;
        for (const player of update.players) {
          if (player.game_id === this.duelConfig?.player1.gameId) {
            this.p1.hp = player.hp;
          } else {
            this.p2.hp = player.hp;
          }
        }
      },
      onDuelEnd: (payload) => {
        if (this.isDestroyed) return;
        const winner = payload.winner_game_id === this.duelConfig?.player1.gameId ? 'p1' : 'p2';
        this.handleDuelOver(winner);
      },
    });
  }

  private initCanvasSize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = Math.max(rect.width, 320) * dpr;
    this.canvas.height = Math.max(rect.height, 240) * dpr;
    this.ctx.scale(dpr, dpr);
  }

  private get width(): number {
    return this.canvas.getBoundingClientRect().width || 800;
  }

  private get height(): number {
    return this.canvas.getBoundingClientRect().height || 600;
  }

  private initStars() {
    this.stars = [];
    const count = 90;
    for (let i = 0; i < count; i++) {
      this.stars.push({
        x: Math.random() * this.width,
        y: Math.random() * this.height,
        speed: 20 + Math.random() * 80,
        size: Math.random() * 2 + 0.5,
        color: Math.random() > 0.8 ? '#74F5FF' : Math.random() > 0.6 ? '#E9C400' : '#FFFFFF',
      });
    }
  }

  private initShips() {
    const w = this.width;
    const h = this.height;

    // Load ship stats from catalog
    const ship1Id = this.runConfig?.shipId || this.duelConfig?.player1.shipId || 'pushpaka';
    const ship1Data = SHIPS.find(s => s.id === ship1Id) || SHIPS[0];

    this.p1.shipId = ship1Data.id;
    this.p1.name = ship1Data.name;
    this.p1.color = ship1Data.color;
    this.p1.speed = 320 + (ship1Data.stats.speed / 100) * 160;
    this.p1.maxHp = 80 + (ship1Data.stats.armor / 100) * 80;
    this.p1.hp = this.p1.maxHp;
    this.p1.maxShield = 40 + (ship1Data.stats.shield / 100) * 60;
    this.p1.shield = this.p1.maxShield;
    this.p1.fireRate = Math.max(0.1, 0.28 - (ship1Data.stats.firepower / 100) * 0.16);

    // Apply Boon bonuses if present
    if (this.activeBoons.includes('vishnu-blessing')) {
      this.p1.maxShield *= 1.3;
      this.p1.shield = this.p1.maxShield;
    }
    if (this.activeBoons.includes('shiva-power')) {
      this.p1.fireRate *= 0.8;
    }

    if (this.mode === 'duel') {
      // Duel positions: P1 on left, P2 on right
      this.p1.x = w * 0.25;
      this.p1.y = h * 0.5;

      const ship2Id = this.duelConfig?.player2.shipId || 'garuda';
      const ship2Data = SHIPS.find(s => s.id === ship2Id) || SHIPS[1];

      this.p2.shipId = ship2Data.id;
      this.p2.name = ship2Data.name;
      this.p2.color = ship2Data.color;
      this.p2.speed = 320 + (ship2Data.stats.speed / 100) * 160;
      this.p2.maxHp = 80 + (ship2Data.stats.armor / 100) * 80;
      this.p2.hp = this.p2.maxHp;
      this.p2.maxShield = 40 + (ship2Data.stats.shield / 100) * 60;
      this.p2.shield = this.p2.maxShield;
      this.p2.fireRate = Math.max(0.1, 0.28 - (ship2Data.stats.firepower / 100) * 0.16);
      this.p2.x = w * 0.75;
      this.p2.y = h * 0.5;
    } else {
      // Single player: P1 center bottom
      this.p1.x = w * 0.5;
      this.p1.y = h * 0.8;
      this.wave = this.runConfig?.startWave || 1;
      this.waveEnemiesTarget = 6 + this.wave * 3;
    }
  }

  private onKeyDown = (e: KeyboardEvent) => {
    this.keys[e.code] = true;
    if (e.code === 'Escape') {
      e.preventDefault();
      this.togglePause();
    }
  };

  private onKeyUp = (e: KeyboardEvent) => {
    this.keys[e.code] = false;
  };

  private onResize = () => {
    this.initCanvasSize();
  };

  private bindEvents() {
    window.addEventListener('keydown', this.onKeyDown);
    window.addEventListener('keyup', this.onKeyUp);
    window.addEventListener('resize', this.onResize);
  }

  public togglePause() {
    this.isPaused = !this.isPaused;
    if (this.onPauseToggle) this.onPauseToggle(this.isPaused);
    if (!this.isPaused) {
      this.lastTime = performance.now();
    }
  }

  public resume() {
    if (this.isPaused) {
      this.isPaused = false;
      this.lastTime = performance.now();
      if (this.onPauseToggle) this.onPauseToggle(false);
    }
  }

  public start() {
    this.lastTime = performance.now();
    const loop = (time: number) => {
      if (this.isDestroyed) return;
      const dt = Math.min((time - this.lastTime) / 1000, 0.1);
      this.lastTime = time;

      if (!this.isPaused) {
        this.update(dt);
      }
      this.render();

      this.animId = requestAnimationFrame(loop);
    };
    this.animId = requestAnimationFrame(loop);
  }

  private update(dt: number) {
    this.updateStars(dt);
    this.updatePlayer1(dt);

    if (this.mode === 'duel') {
      this.updatePlayer2(dt);
      this.checkDuelCollisions();
    } else {
      this.updateSinglePlayerWaves(dt);
      this.updateEnemies(dt);
      this.checkSinglePlayerCollisions();
    }

    this.updateProjectiles(dt);
    this.updateParticles(dt);
    this.updateFloatingTexts(dt);

    // Combo decay
    if (this.comboTimer > 0) {
      this.comboTimer -= dt;
      if (this.comboTimer <= 0) {
        this.currentCombo = 0;
      }
    }
  }

  private updateStars(dt: number) {
    const h = this.height;
    for (const star of this.stars) {
      star.y += star.speed * dt;
      if (star.y > h) {
        star.y = 0;
        star.x = Math.random() * this.width;
      }
    }
  }

  private updatePlayer1(dt: number) {
    const p = this.p1;
    let dx = 0;
    let dy = 0;

    if (this.keys['KeyW'] || (this.mode === 'single' && this.keys['ArrowUp'])) dy -= 1;
    if (this.keys['KeyS'] || (this.mode === 'single' && this.keys['ArrowDown'])) dy += 1;
    if (this.keys['KeyA'] || (this.mode === 'single' && this.keys['ArrowLeft'])) dx -= 1;
    if (this.keys['KeyD'] || (this.mode === 'single' && this.keys['ArrowRight'])) dx += 1;

    // Normalize diagonal
    if (dx !== 0 && dy !== 0) {
      dx *= 0.7071;
      dy *= 0.7071;
    }

    // Dash
    if (p.dashCooldown > 0) p.dashCooldown -= dt;
    if ((this.keys['ShiftLeft'] || this.keys['KeyQ']) && p.dashCooldown <= 0 && (dx !== 0 || dy !== 0)) {
      p.dashCooldown = 1.6;
      p.x += dx * 90;
      p.y += dy * 90;
      sound.playDash();
      this.spawnThrustBurst(p.x, p.y, p.color, 16);
    }

    p.x += dx * p.speed * dt;
    p.y += dy * p.speed * dt;

    // Bounds
    const w = this.width;
    const h = this.height;
    p.x = Math.max(p.radius, Math.min(w - p.radius, p.x));
    p.y = Math.max(p.radius, Math.min(h - p.radius, p.y));

    // Engine thrust particles
    if (Math.random() < 0.6) {
      this.particles.push({
        x: p.x + (Math.random() * 8 - 4),
        y: p.y + p.radius + 2,
        vx: (Math.random() - 0.5) * 20,
        vy: 40 + Math.random() * 60,
        color: p.color,
        size: 2.5,
        life: 0.25,
        maxLife: 0.25,
      });
    }

    // Shield passive recharge
    p.shieldRegenTimer += dt;
    if (p.shieldRegenTimer > 3.0 && p.shield < p.maxShield) {
      p.shield = Math.min(p.maxShield, p.shield + 12 * dt);
    }

    // Firing
    if (p.fireCooldown > 0) p.fireCooldown -= dt;
    if (this.keys['Space'] && p.fireCooldown <= 0) {
      p.fireCooldown = p.fireRate;
      this.firePlayerLaser(p.x, p.y - p.radius, 'p1', p.color);
    }

    // Transmit state in online duel mode
    if (this.mode === 'duel' && this.duelConfig?.roomCode) {
      const sock = getActiveDuelSocket();
      if (sock?.isConnected) {
        sock.sendInput({
          x: p.x,
          y: p.y,
          dx,
          dy,
          firing: Boolean(this.keys['Space']),
          dash: Boolean((this.keys['ShiftLeft'] || this.keys['KeyQ']) && p.dashCooldown > 1.4),
        });
      }
    }
  }

  private updatePlayer2(dt: number) {
    const p = this.p2;

    if (this.duelConfig?.roomCode) {
      // In online duel mode, P2 is driven by opponent WebSocket events
      p.shieldRegenTimer += dt;
      if (p.shieldRegenTimer > 3.0 && p.shield < p.maxShield) {
        p.shield = Math.min(p.maxShield, p.shield + 12 * dt);
      }
      if (p.fireCooldown > 0) p.fireCooldown -= dt;
      return;
    }

    let dx = 0;
    let dy = 0;

    if (this.keys['ArrowUp']) dy -= 1;
    if (this.keys['ArrowDown']) dy += 1;
    if (this.keys['ArrowLeft']) dx -= 1;
    if (this.keys['ArrowRight']) dx += 1;

    if (dx !== 0 && dy !== 0) {
      dx *= 0.7071;
      dy *= 0.7071;
    }

    // P2 Dash: RightShift or Numpad0
    if (p.dashCooldown > 0) p.dashCooldown -= dt;
    if ((this.keys['ShiftRight'] || this.keys['Numpad0'] || this.keys['KeyM']) && p.dashCooldown <= 0 && (dx !== 0 || dy !== 0)) {
      p.dashCooldown = 1.6;
      p.x += dx * 90;
      p.y += dy * 90;
      sound.playDash();
      this.spawnThrustBurst(p.x, p.y, p.color, 16);
    }

    p.x += dx * p.speed * dt;
    p.y += dy * p.speed * dt;

    const w = this.width;
    const h = this.height;
    p.x = Math.max(p.radius, Math.min(w - p.radius, p.x));
    p.y = Math.max(p.radius, Math.min(h - p.radius, p.y));

    // Engine thrust
    if (Math.random() < 0.6) {
      this.particles.push({
        x: p.x + (Math.random() * 8 - 4),
        y: p.y + p.radius + 2,
        vx: (Math.random() - 0.5) * 20,
        vy: 40 + Math.random() * 60,
        color: p.color,
        size: 2.5,
        life: 0.25,
        maxLife: 0.25,
      });
    }

    // Shield passive regen
    p.shieldRegenTimer += dt;
    if (p.shieldRegenTimer > 3.0 && p.shield < p.maxShield) {
      p.shield = Math.min(p.maxShield, p.shield + 12 * dt);
    }

    // P2 Fire: Enter or NumpadEnter or Slash
    if (p.fireCooldown > 0) p.fireCooldown -= dt;
    if ((this.keys['Enter'] || this.keys['NumpadEnter'] || this.keys['Slash']) && p.fireCooldown <= 0) {
      p.fireCooldown = p.fireRate;
      this.firePlayerLaser(p.x, p.y - p.radius, 'p2', p.color);
    }
  }

  private firePlayerLaser(x: number, y: number, ownerId: string, color: string) {
    sound.playLaser(ownerId === 'p1' ? 750 : 620);
    const vy = this.mode === 'duel' && ownerId === 'p2' ? -460 : -520;
    const damage = 25;

    // Single shot or multishot if indra-storm or soma
    this.projectiles.push({
      x,
      y,
      vx: 0,
      vy,
      radius: 4,
      damage,
      isPlayer: true,
      ownerId,
      color,
    });

    if (this.activeBoons.includes('indra-storm') && ownerId === 'p1') {
      this.projectiles.push(
        { x: x - 8, y, vx: -60, vy, radius: 3, damage: 15, isPlayer: true, ownerId, color: '#74F5FF' },
        { x: x + 8, y, vx: 60, vy, radius: 3, damage: 15, isPlayer: true, ownerId, color: '#74F5FF' }
      );
    }
  }

  private updateSinglePlayerWaves(dt: number) {
    this.waveSpawnTimer += dt;
    if (this.waveEnemiesSpawned < this.waveEnemiesTarget && this.waveSpawnTimer >= 1.2) {
      this.waveSpawnTimer = 0;
      this.spawnAsuraEnemy();
      this.waveEnemiesSpawned++;
    }

    // Wave cleared when all enemies spawned and slain
    if (this.waveEnemiesSpawned >= this.waveEnemiesTarget && this.enemies.length === 0) {
      this.handleWaveClear();
    }
  }

  private spawnAsuraEnemy() {
    const w = this.width;
    const randType = Math.random();
    let type: AsuraEnemy['type'] = 'fast';
    let hp = 30 + this.wave * 8;
    let color = '#FF6B72';
    let radius = 16;
    let maxCooldown = 2.0;
    let scoreVal = 100;

    if (this.wave % 5 === 0 && this.waveEnemiesSpawned === this.waveEnemiesTarget - 1) {
      type = 'boss';
      hp = 300 + this.wave * 40;
      color = '#FF2040';
      radius = 32;
      maxCooldown = 1.0;
      scoreVal = 1500;
    } else if (randType > 0.65) {
      type = 'tank';
      hp = 80 + this.wave * 12;
      color = '#FF9650';
      radius = 22;
      maxCooldown = 2.5;
      scoreVal = 250;
    } else if (randType > 0.35) {
      type = 'ranged';
      hp = 40 + this.wave * 6;
      color = '#FF4646';
      radius = 18;
      maxCooldown = 1.6;
      scoreVal = 150;
    }

    this.enemies.push({
      x: 40 + Math.random() * (w - 80),
      y: -radius,
      vx: (Math.random() - 0.5) * 60,
      vy: type === 'fast' ? 140 : type === 'tank' ? 60 : 90,
      radius,
      hp,
      maxHp: hp,
      type,
      color,
      shootCooldown: Math.random() * maxCooldown,
      maxCooldown,
      scoreValue: scoreVal,
    });
  }

  private updateEnemies(dt: number) {
    const h = this.height;
    const w = this.width;

    for (let i = this.enemies.length - 1; i >= 0; i--) {
      const e = this.enemies[i];
      e.x += e.vx * dt;
      e.y += e.vy * dt;

      // Bounce off walls
      if (e.x < e.radius || e.x > w - e.radius) {
        e.vx = -e.vx;
      }

      // Ranged enemies shoot crimson plasma
      if (e.type === 'ranged' || e.type === 'boss') {
        e.shootCooldown -= dt;
        if (e.shootCooldown <= 0) {
          e.shootCooldown = e.maxCooldown;
          this.projectiles.push({
            x: e.x,
            y: e.y + e.radius,
            vx: (this.p1.x - e.x) * 0.5,
            vy: 220,
            radius: 4,
            damage: 15,
            isPlayer: false,
            ownerId: 'enemy',
            color: '#FF3344',
          });
        }
      }

      // Despawn if passed bottom screen
      if (e.y > h + e.radius + 20) {
        this.enemies.splice(i, 1);
      }
    }
  }

  private updateProjectiles(dt: number) {
    const h = this.height;
    const w = this.width;

    for (let i = this.projectiles.length - 1; i >= 0; i--) {
      const p = this.projectiles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;

      if (p.y < -20 || p.y > h + 20 || p.x < -20 || p.x > w + 20) {
        this.projectiles.splice(i, 1);
      }
    }
  }

  private checkSinglePlayerCollisions() {
    // 1. Player projectiles hit enemies
    for (let pi = this.projectiles.length - 1; pi >= 0; pi--) {
      const proj = this.projectiles[pi];
      if (!proj.isPlayer) continue;

      for (let ei = this.enemies.length - 1; ei >= 0; ei--) {
        const enemy = this.enemies[ei];
        const dist = Math.hypot(proj.x - enemy.x, proj.y - enemy.y);
        if (dist < proj.radius + enemy.radius) {
          // Hit!
          enemy.hp -= proj.damage;
          this.totalDamage += proj.damage;
          this.projectiles.splice(pi, 1);
          sound.playHit();
          this.spawnHitSparks(proj.x, proj.y, proj.color, 6);
          this.addFloatingText(proj.x, proj.y - 10, `-${proj.damage}`, '#FFF6DF');

          if (enemy.hp <= 0) {
            // Defeated enemy
            this.handleEnemyDefeated(enemy);
            this.enemies.splice(ei, 1);
          }
          break;
        }
      }
    }

    // 2. Enemy projectiles / collision hit Player 1
    const p = this.p1;
    for (let pi = this.projectiles.length - 1; pi >= 0; pi--) {
      const proj = this.projectiles[pi];
      if (proj.isPlayer) continue;

      const dist = Math.hypot(proj.x - p.x, proj.y - p.y);
      if (dist < proj.radius + p.radius) {
        this.projectiles.splice(pi, 1);
        this.applyDamageToShip(p, proj.damage);
        sound.playHit();
        this.spawnHitSparks(proj.x, proj.y, '#FF4444', 8);
      }
    }

    // Direct collision between Player and Enemies
    for (let ei = this.enemies.length - 1; ei >= 0; ei--) {
      const enemy = this.enemies[ei];
      const dist = Math.hypot(p.x - enemy.x, p.y - enemy.y);
      if (dist < p.radius + enemy.radius) {
        this.applyDamageToShip(p, 30);
        enemy.hp -= 40;
        sound.playExplosion(false);
        this.spawnHitSparks(p.x, p.y, '#FF6B72', 12);
        if (enemy.hp <= 0) {
          this.handleEnemyDefeated(enemy);
          this.enemies.splice(ei, 1);
        }
      }
    }
  }

  private checkDuelCollisions() {
    // Check projectiles against both players
    for (let pi = this.projectiles.length - 1; pi >= 0; pi--) {
      const proj = this.projectiles[pi];

      // P1 hit by P2 laser
      if (proj.ownerId === 'p2') {
        const dist = Math.hypot(proj.x - this.p1.x, proj.y - this.p1.y);
        if (dist < proj.radius + this.p1.radius) {
          this.projectiles.splice(pi, 1);
          this.applyDamageToShip(this.p1, proj.damage);
          sound.playHit();
          this.spawnHitSparks(proj.x, proj.y, '#74F5FF', 8);
          this.addFloatingText(this.p1.x, this.p1.y - 12, `-${proj.damage}`, '#FF6B72');
          if (this.p1.hp <= 0) {
            this.handleDuelOver('p2');
          }
          continue;
        }
      }

      // P2 hit by P1 laser
      if (proj.ownerId === 'p1') {
        const dist = Math.hypot(proj.x - this.p2.x, proj.y - this.p2.y);
        if (dist < proj.radius + this.p2.radius) {
          this.projectiles.splice(pi, 1);
          this.applyDamageToShip(this.p2, proj.damage);
          sound.playHit();
          this.spawnHitSparks(proj.x, proj.y, '#E9C400', 8);
          this.addFloatingText(this.p2.x, this.p2.y - 12, `-${proj.damage}`, '#E9C400');
          if (this.duelConfig?.roomCode) {
            getActiveDuelSocket()?.reportHit(proj.damage);
          }
          if (this.p2.hp <= 0) {
            this.handleDuelOver('p1');
          }
        }
      }
    }
  }

  private applyDamageToShip(ship: typeof this.p1, rawDamage: number) {
    ship.shieldRegenTimer = 0;
    if (ship.shield > 0) {
      if (ship.shield >= rawDamage) {
        ship.shield -= rawDamage;
      } else {
        const leftover = rawDamage - ship.shield;
        ship.shield = 0;
        ship.hp = Math.max(0, ship.hp - leftover);
      }
    } else {
      ship.hp = Math.max(0, ship.hp - rawDamage);
    }

    if (ship.hp <= 0 && this.mode === 'single') {
      sound.playExplosion(true);
      this.handleGameOver();
    }
  }

  private handleEnemyDefeated(enemy: AsuraEnemy) {
    sound.playExplosion(enemy.type === 'boss');
    this.spawnThrustBurst(enemy.x, enemy.y, enemy.color, enemy.type === 'boss' ? 36 : 14);

    this.kills++;
    this.currentCombo++;
    this.comboTimer = 2.5;
    if (this.currentCombo > this.highestCombo) {
      this.highestCombo = this.currentCombo;
    }

    const mult = 1 + (this.currentCombo - 1) * 0.1;
    const earnedScore = Math.floor(enemy.scoreValue * mult);
    this.score += earnedScore;

    this.addFloatingText(enemy.x, enemy.y - 10, `+${earnedScore}`, '#E9C400');
  }

  private handleWaveClear() {
    sound.playBoon();
    this.wave++;
    this.waveEnemiesSpawned = 0;
    this.waveEnemiesTarget = 6 + this.wave * 3;

    if (this.wave > this.maxWaves) {
      this.handleVictory();
    } else if (this.onWaveComplete) {
      this.isPaused = true;
      this.onWaveComplete(this.wave);
    }
  }

  private handleGameOver() {
    this.isPaused = true;
    const duration = Math.floor((Date.now() - this.startTime) / 1000);
    const result: RunResult = {
      runId: this.runConfig?.runId || `run_${Date.now()}`,
      shipId: this.p1.shipId,
      mode: this.runConfig?.mode || 'campaign',
      difficulty: this.runConfig?.difficulty || 'normal',
      score: this.score,
      waveReached: this.wave,
      kills: this.kills,
      totalDamage: this.totalDamage,
      highestCombo: this.highestCombo,
      boons: this.activeBoons,
      durationSeconds: duration,
      outcome: 'defeat',
      timestamp: Date.now(),
    };
    if (this.onGameOver) this.onGameOver(result);
  }

  private handleVictory() {
    this.isPaused = true;
    const duration = Math.floor((Date.now() - this.startTime) / 1000);
    const result: RunResult = {
      runId: this.runConfig?.runId || `run_${Date.now()}`,
      shipId: this.p1.shipId,
      mode: this.runConfig?.mode || 'campaign',
      difficulty: this.runConfig?.difficulty || 'normal',
      score: this.score + 50000,
      waveReached: this.wave,
      kills: this.kills,
      totalDamage: this.totalDamage,
      highestCombo: this.highestCombo,
      boons: this.activeBoons,
      durationSeconds: duration,
      outcome: 'victory',
      timestamp: Date.now(),
    };
    if (this.onVictory) this.onVictory(result);
  }

  private handleDuelOver(winner: 'p1' | 'p2') {
    this.isPaused = true;
    sound.playExplosion(true);
    const duration = Math.floor((Date.now() - this.startTime) / 1000);
    const winnerId = winner === 'p1' ? this.duelConfig?.player1.gameId || 'Player 1' : this.duelConfig?.player2.gameId || 'Player 2';
    const duelRes: DuelResult = {
      roomCode: this.duelConfig?.roomCode,
      winnerGameId: winnerId,
      player1: {
        gameId: this.duelConfig?.player1.gameId || 'P1',
        name: this.duelConfig?.player1.name || 'PILOT 1',
        shipId: this.p1.shipId,
        health: Math.max(0, Math.floor(this.p1.hp)),
        maxHealth: 100,
        score: Math.floor(this.p1.hp),
      },
      player2: {
        gameId: this.duelConfig?.player2.gameId || 'P2',
        name: this.duelConfig?.player2.name || 'PILOT 2',
        shipId: this.p2.shipId,
        health: Math.max(0, Math.floor(this.p2.hp)),
        maxHealth: 100,
        score: Math.floor(this.p2.hp),
      },
      durationSeconds: duration,
      timestamp: Date.now(),
    };
    if (this.onDuelOver) this.onDuelOver(duelRes);
  }

  private spawnHitSparks(x: number, y: number, color: string, count = 8) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 40 + Math.random() * 120;
      this.particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        color,
        size: 1.5 + Math.random() * 2,
        life: 0.2 + Math.random() * 0.15,
        maxLife: 0.35,
      });
    }
  }

  private spawnThrustBurst(x: number, y: number, color: string, count = 12) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 60 + Math.random() * 180;
      this.particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        color,
        size: 2 + Math.random() * 3,
        life: 0.35 + Math.random() * 0.25,
        maxLife: 0.6,
      });
    }
  }

  private addFloatingText(x: number, y: number, text: string, color: string) {
    this.floatingTexts.push({
      x,
      y,
      text,
      color,
      life: 0.8,
      maxLife: 0.8,
    });
  }

  private updateParticles(dt: number) {
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;
      if (p.life <= 0) {
        this.particles.splice(i, 1);
      }
    }
  }

  private updateFloatingTexts(dt: number) {
    for (let i = this.floatingTexts.length - 1; i >= 0; i--) {
      const t = this.floatingTexts[i];
      t.y -= 25 * dt;
      t.life -= dt;
      if (t.life <= 0) {
        this.floatingTexts.splice(i, 1);
      }
    }
  }

  // --- Rendering ---
  private render() {
    const ctx = this.ctx;
    const w = this.width;
    const h = this.height;

    // Clear background
    ctx.fillStyle = '#060810';
    ctx.fillRect(0, 0, w, h);

    // Stars
    for (const star of this.stars) {
      ctx.fillStyle = star.color;
      ctx.fillRect(star.x, star.y, star.size, star.size);
    }

    // Particles
    for (const p of this.particles) {
      const alpha = p.life / p.maxLife;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Projectiles
    for (const proj of this.projectiles) {
      ctx.save();
      ctx.fillStyle = proj.color;
      ctx.shadowColor = proj.color;
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.arc(proj.x, proj.y, proj.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Enemies (Single player)
    if (this.mode === 'single') {
      for (const e of this.enemies) {
        this.drawEnemy(e);
      }
    }

    // Ships
    this.drawShip(this.p1, 'P1');
    if (this.mode === 'duel') {
      this.drawShip(this.p2, 'P2');
    }

    // Floating text
    for (const t of this.floatingTexts) {
      const alpha = t.life / t.maxLife;
      ctx.save();
      ctx.globalAlpha = alpha;
      ctx.font = 'bold 12px "JetBrains Mono", monospace';
      ctx.fillStyle = t.color;
      ctx.textAlign = 'center';
      ctx.fillText(t.text, t.x, t.y);
      ctx.restore();
    }

    // On-screen HUD elements
    this.drawHUD();
  }

  private drawShip(ship: typeof this.p1, label: string) {
    const ctx = this.ctx;
    const { x, y, radius, color } = ship;

    ctx.save();
    ctx.translate(x, y);

    // Shield bubble
    if (ship.shield > 0) {
      const shieldPct = ship.shield / ship.maxShield;
      ctx.strokeStyle = `rgba(116, 245, 255, ${0.3 + shieldPct * 0.45})`;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(0, 0, radius + 8, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Ship hull shape (sleek arrowhead)
    ctx.fillStyle = color;
    ctx.shadowColor = color;
    ctx.shadowBlur = 12;
    ctx.beginPath();
    ctx.moveTo(0, -radius);
    ctx.lineTo(radius * 0.85, radius);
    ctx.lineTo(0, radius * 0.55);
    ctx.lineTo(-radius * 0.85, radius);
    ctx.closePath();
    ctx.fill();

    // Pilot cockpit glass
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.arc(0, -radius * 0.2, radius * 0.25, 0, Math.PI * 2);
    ctx.fill();

    // Label tag
    ctx.font = '9px "Cinzel", serif';
    ctx.fillStyle = '#FFF6DF';
    ctx.textAlign = 'center';
    ctx.fillText(label, 0, radius + 14);

    ctx.restore();
  }

  private drawEnemy(e: AsuraEnemy) {
    const ctx = this.ctx;
    ctx.save();
    ctx.translate(e.x, e.y);

    ctx.fillStyle = e.color;
    ctx.shadowColor = e.color;
    ctx.shadowBlur = 10;

    if (e.type === 'boss') {
      // Boss octagon
      ctx.beginPath();
      for (let i = 0; i < 8; i++) {
        const angle = (i * Math.PI) / 4;
        const px = Math.cos(angle) * e.radius;
        const py = Math.sin(angle) * e.radius;
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.fill();
    } else {
      // Inverted downward arrowhead
      ctx.beginPath();
      ctx.moveTo(0, e.radius);
      ctx.lineTo(e.radius, -e.radius);
      ctx.lineTo(0, -e.radius * 0.4);
      ctx.lineTo(-e.radius, -e.radius);
      ctx.closePath();
      ctx.fill();
    }

    // Mini HP bar
    if (e.hp < e.maxHp) {
      const barW = e.radius * 2;
      const barH = 3;
      ctx.fillStyle = 'rgba(0,0,0,0.6)';
      ctx.fillRect(-barW / 2, -e.radius - 8, barW, barH);
      ctx.fillStyle = '#FF4444';
      ctx.fillRect(-barW / 2, -e.radius - 8, barW * (e.hp / e.maxHp), barH);
    }

    ctx.restore();
  }

  private drawHUD() {
    const ctx = this.ctx;
    const w = this.width;

    ctx.save();
    ctx.font = '10px "JetBrains Mono", monospace';

    if (this.mode === 'duel') {
      // P1 Health (top-left)
      this.drawBar(20, 20, 160, 10, this.p1.hp, this.p1.maxHp, '#30C846', `P1 ${this.p1.name.toUpperCase()}`);
      this.drawBar(20, 36, 160, 6, this.p1.shield, this.p1.maxShield, '#7EA8FF', 'SHIELD');

      // P2 Health (top-right)
      this.drawBar(w - 180, 20, 160, 10, this.p2.hp, this.p2.maxHp, '#FF6B72', `P2 ${this.p2.name.toUpperCase()}`);
      this.drawBar(w - 180, 36, 160, 6, this.p2.shield, this.p2.maxShield, '#7EA8FF', 'SHIELD');

      // Center Duel Banner
      ctx.textAlign = 'center';
      ctx.font = 'bold 12px "Cinzel", serif';
      ctx.fillStyle = '#E9C400';
      ctx.fillText('1V1 DUEL ARENA', w / 2, 28);
      ctx.font = '9px "JetBrains Mono", monospace';
      ctx.fillStyle = '#8F98A8';
      ctx.fillText('P1: WASD+SPACE | P2: ARROWS+ENTER', w / 2, 42);
    } else {
      // Single Player HUD
      // Player HP & Shield (top-left)
      this.drawBar(20, 20, 180, 10, this.p1.hp, this.p1.maxHp, '#30C846', `HULL ${Math.ceil(this.p1.hp)}/${this.p1.maxHp}`);
      this.drawBar(20, 36, 180, 6, this.p1.shield, this.p1.maxShield, '#7EA8FF', `SHIELD ${Math.ceil(this.p1.shield)}/${this.p1.maxShield}`);

      // Wave and Score (top-right)
      ctx.textAlign = 'right';
      ctx.fillStyle = '#FFF6DF';
      ctx.font = 'bold 14px "Cinzel", serif';
      ctx.fillText(`SCORE: ${this.score.toLocaleString()}`, w - 24, 26);

      ctx.fillStyle = '#E9C400';
      ctx.font = '11px "JetBrains Mono", monospace';
      ctx.fillText(`WAVE ${this.wave} / ${this.maxWaves}`, w - 24, 42);

      if (this.currentCombo > 1) {
        ctx.fillStyle = '#74F5FF';
        ctx.fillText(`COMBO x${this.currentCombo}!`, w - 24, 58);
      }
    }

    ctx.restore();
  }

  private drawBar(x: number, y: number, width: number, height: number, val: number, max: number, color: string, label: string) {
    const ctx = this.ctx;
    const pct = Math.max(0, Math.min(1, val / max));

    ctx.fillStyle = 'rgba(10, 15, 25, 0.75)';
    ctx.fillRect(x, y, width, height);

    ctx.fillStyle = color;
    ctx.fillRect(x, y, width * pct, height);

    ctx.strokeStyle = 'rgba(233, 196, 0, 0.25)';
    ctx.lineWidth = 1;
    ctx.strokeRect(x, y, width, height);

    ctx.fillStyle = '#FFF6DF';
    ctx.textAlign = 'left';
    ctx.fillText(label, x, y - 3);
  }

  public destroy() {
    this.isDestroyed = true;
    if (this.animId) cancelAnimationFrame(this.animId);
    window.removeEventListener('keydown', this.onKeyDown);
    window.removeEventListener('keyup', this.onKeyUp);
    window.removeEventListener('resize', this.onResize);
  }
}
