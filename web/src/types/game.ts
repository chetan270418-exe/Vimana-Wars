export type GameMode = 'campaign' | 'endless' | 'duel';
export type GameDifficulty = 'easy' | 'normal' | 'hard' | 'endless';

export type ScreenId =
  | 'main-menu'
  | 'ship-select'
  | 'boon-select'
  | 'game-hud'
  | 'game-over'
  | 'victory'
  | 'realm-map'
  | 'leaderboard'
  | 'achievements'
  | 'account'
  | 'sangha'
  | 'settings'
  | 'codex'
  | 'duel';

export type RunConfig = {
  runId: string;
  shipId: string;
  mode: GameMode;
  difficulty: GameDifficulty;
  startRealm: string;
  startWave: number;
  seed?: number;
};

export type RunOutcome = 'victory' | 'defeat' | 'abandoned';

export type RunResult = {
  runId: string;
  shipId: string;
  mode: GameMode;
  difficulty: GameDifficulty;
  score: number;
  waveReached: number;
  kills: number;
  totalDamage: number;
  highestCombo: number;
  boons: string[];
  durationSeconds: number;
  outcome: RunOutcome;
  timestamp: number;
};

export type DuelPlayerState = {
  gameId: string;
  name: string;
  shipId: string;
  health: number;
  maxHealth: number;
  score: number;
};

export type DuelConfig = {
  mode: 'duel';
  roomCode?: string;
  player1: DuelPlayerState;
  player2: DuelPlayerState;
};

export type DuelResult = {
  roomCode?: string;
  winnerGameId: string;
  player1: DuelPlayerState;
  player2: DuelPlayerState;
  durationSeconds: number;
  timestamp: number;
};

export type UserSettings = {
  masterVolume: number;
  musicVolume: number;
  sfxVolume: number;
  ambienceVolume: number;
  fullscreen: boolean;
  vsync: boolean;
  particles: boolean;
  scanlines: boolean;
  bloom: boolean;
  muteWhenUnfocused: boolean;
  dynamicMusic: boolean;
  resolution: string;
  screenShake: boolean;
  reducedMotion: boolean;
  reducedFlashes: boolean;
  showFps: boolean;
  keybindings: {
    moveUp: string;
    moveDown: string;
    moveLeft: string;
    moveRight: string;
    primaryFire: string;
    dash: string;
    astraAbility: string;
    pause: string;
  };
};

export const DEFAULT_SETTINGS: UserSettings = {
  masterVolume: 80,
  musicVolume: 70,
  sfxVolume: 80,
  ambienceVolume: 50,
  fullscreen: true,
  vsync: true,
  particles: true,
  scanlines: true,
  bloom: true,
  muteWhenUnfocused: true,
  dynamicMusic: true,
  resolution: '1920 × 1080',
  screenShake: true,
  reducedMotion: false,
  reducedFlashes: false,
  showFps: false,
  keybindings: {
    moveUp: 'KeyW',
    moveDown: 'KeyS',
    moveLeft: 'KeyA',
    moveRight: 'KeyD',
    primaryFire: 'Space',
    dash: 'ShiftLeft',
    astraAbility: 'KeyE',
    pause: 'Escape',
  },
};
