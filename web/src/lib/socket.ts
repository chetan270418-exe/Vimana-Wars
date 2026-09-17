/**
 * web/src/lib/socket.ts
 * Socket.IO client wrapper for Vimana Wars online 1v1 duel mode.
 *
 * Usage:
 *   const duelSocket = createDuelSocket({ token, roomCode, gameId, shipClass });
 *   await duelSocket.connect({ onOpponentState, onHpUpdate, onDuelEnd, onOpponentJoined });
 *   // each game frame:
 *   duelSocket.sendInput({ x, y, dx, dy, firing, dash });
 *   // when local bullet hits opponent:
 *   duelSocket.reportHit(damage);
 *   // on cleanup:
 *   destroyDuelSocket();
 */

const API_URL = (import.meta.env.VITE_API_URL as string | undefined) ?? 'http://localhost:5000';

export interface OpponentState {
  x: number;
  y: number;
  dx: number;
  dy: number;
  firing: boolean;
  dash: boolean;
}

export interface HpUpdate {
  players: Array<{ game_id: string; hp: number }>;
}

export interface DuelEndPayload {
  winner_game_id: string;
  reason?: string;
}

export interface DuelSocketHandlers {
  onOpponentJoined?: (gameId: string, shipClass: string) => void;
  onOpponentState?: (state: OpponentState) => void;
  onHpUpdate?: (update: HpUpdate) => void;
  onDuelEnd?: (payload: DuelEndPayload) => void;
  onError?: (message: string) => void;
  onDisconnect?: () => void;
}

export interface DuelSocketConfig {
  /** Override API base URL — defaults to VITE_API_URL env var */
  apiUrl?: string;
  /** Bearer token from getSession() */
  token: string;
  /** 6-char lobby code */
  roomCode: string;
  /** Local player's game_id */
  gameId: string;
  /** Local player's selected ship */
  shipClass: string;
}

export class DuelSocket {
  private cfg: Required<DuelSocketConfig>;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private socket: any = null;
  private lastSendTime = 0;
  private handlers: DuelSocketHandlers = {};
  public isConnected = false;
  public opponentConnected = false;

  constructor(config: DuelSocketConfig) {
    this.cfg = { apiUrl: API_URL, ...config };
  }

  async connect(handlers: DuelSocketHandlers): Promise<void> {
    this.handlers = handlers;

    // Lazy-load socket.io-client — only bundled when online duel is used
    const { io } = await import('socket.io-client');

    this.socket = io(this.cfg.apiUrl, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      timeout: 10_000,
    });

    this.socket.on('connect', () => {
      this.isConnected = true;
      this.socket.emit('join_duel', {
        token: this.cfg.token,
        room_code: this.cfg.roomCode,
        game_id: this.cfg.gameId,
        ship_class: this.cfg.shipClass,
      });
    });

    this.socket.on('disconnect', () => {
      this.isConnected = false;
      this.handlers.onDisconnect?.();
    });

    this.socket.on('connect_error', (err: Error) => {
      this.handlers.onError?.(`Connection failed: ${err.message}`);
    });

    this.socket.on('player_joined', (data: { game_id: string; ship_class: string }) => {
      if (data.game_id !== this.cfg.gameId) {
        this.opponentConnected = true;
        this.handlers.onOpponentJoined?.(data.game_id, data.ship_class);
      }
    });

    this.socket.on('opponent_state', (state: OpponentState) => {
      this.handlers.onOpponentState?.(state);
    });

    this.socket.on('hp_update', (update: HpUpdate) => {
      this.handlers.onHpUpdate?.(update);
    });

    this.socket.on('duel_end', (payload: DuelEndPayload) => {
      this.handlers.onDuelEnd?.(payload);
    });

    this.socket.on('error', (data: { message?: string }) => {
      this.handlers.onError?.(data.message ?? 'Unknown socket error');
    });
  }

  /** Merge additional or updated event handlers without reconnecting */
  updateHandlers(handlers: Partial<DuelSocketHandlers>): void {
    this.handlers = { ...this.handlers, ...handlers };
  }

  /**
   * Send local player input — throttled to 20 sends/second max.
   * Call this every game frame; the throttle handles rate limiting.
   */
  sendInput(input: {
    x: number; y: number;
    dx: number; dy: number;
    firing: boolean; dash: boolean;
  }): void {
    if (!this.socket?.connected) return;
    const now = performance.now();
    if (now - this.lastSendTime < 50) return; // 20 Hz cap
    this.lastSendTime = now;
    this.socket.emit('player_input', {
      x: Math.round(input.x * 10) / 10,
      y: Math.round(input.y * 10) / 10,
      dx: Math.round(input.dx * 100) / 100,
      dy: Math.round(input.dy * 100) / 100,
      firing: input.firing,
      dash: input.dash,
    });
  }

  /**
   * Report a hit on the opponent — server validates and broadcasts authoritative hp_update.
   */
  reportHit(damage: number): void {
    if (!this.socket?.connected) return;
    this.socket.emit('hit_registered', {
      damage: Math.min(50, Math.max(1, Math.round(damage))),
    });
  }

  disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
    this.isConnected = false;
    this.opponentConnected = false;
  }
}

// ── Singleton helpers ─────────────────────────────────────────────────────────

let _activeSocket: DuelSocket | null = null;

export function createDuelSocket(config: DuelSocketConfig): DuelSocket {
  _activeSocket?.disconnect();
  _activeSocket = new DuelSocket(config);
  return _activeSocket;
}

export function getActiveDuelSocket(): DuelSocket | null {
  return _activeSocket;
}

export function destroyDuelSocket(): void {
  _activeSocket?.disconnect();
  _activeSocket = null;
}

