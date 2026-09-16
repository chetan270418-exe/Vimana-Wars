const API_BASE_URL = (import.meta.env.VITE_API_URL || 'https://vimana-wars.onrender.com').replace(/\/+$/, '');
const SESSION_KEY = 'vimana-web-session';

export type ApiHealth = {
  game?: string;
  status?: string;
  endpoints?: Record<string, string>;
};

export type User = {
  game_id: string;
  email: string;
  player_name: string;
  email_verified?: boolean;
};

export type Session = { token: string; user: User };

export type LobbyPlayer = {
  game_id: string;
  player_name: string;
  ship_class: string;
  ready: boolean;
  host: boolean;
  health: number;
  max_health: number;
};

export type Lobby = {
  code: string;
  mode: 'campaign' | 'endless' | 'duel';
  max_players: number;
  status: 'waiting' | 'running';
  host_game_id: string;
  players: LobbyPlayer[];
  created_at: number;
  rules?: { health: number; win_condition: string };
};

function readSession(): Session | null {
  try {
    const raw = window.localStorage.getItem(SESSION_KEY);
    return raw ? JSON.parse(raw) as Session : null;
  } catch {
    return null;
  }
}

export function getSession(): Session | null {
  return readSession();
}

export function saveSession(session: Session): void {
  window.localStorage.setItem(SESSION_KEY, JSON.stringify(session));
}

export function clearSession(): void {
  window.localStorage.removeItem(SESSION_KEY);
}

async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  const session = readSession();
  const headers = new Headers(init.headers);
  headers.set('Accept', 'application/json');
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  if (session?.token) headers.set('Authorization', `Bearer ${session.token}`);
  const response = await fetch(`${API_BASE_URL}${path}`, { ...init, headers });
  const payload = await response.json().catch(() => ({})) as T & { error?: string };
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status})`);
  return payload;
}

export async function getApiHealth(signal?: AbortSignal): Promise<ApiHealth> {
  const response = await fetch(`${API_BASE_URL}/`, { signal, headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`API returned ${response.status}`);
  return response.json() as Promise<ApiHealth>;
}

export async function getTopScores(limit = 10, signal?: AbortSignal) {
  const response = await fetch(`${API_BASE_URL}/scores/top?limit=${limit}`, { signal, headers: { Accept: 'application/json' } });
  if (!response.ok) throw new Error(`Leaderboard returned ${response.status}`);
  return response.json() as Promise<{ leaderboard?: Array<Record<string, unknown>> }>;
}

export async function registerAccount(email: string, password: string, playerName: string) {
  const payload = await apiFetch<{ token?: string | null; user: User; verification_required?: boolean; verification_token?: string }>('/auth/register', {
    method: 'POST', body: JSON.stringify({ email, password, player_name: playerName }),
  });
  if (payload.token) {
    saveSession({ token: payload.token, user: payload.user });
  }
  return payload;
}

export async function loginAccount(email: string, password: string) {
  const payload = await apiFetch<{ token: string; user: User }>('/auth/login', {
    method: 'POST', body: JSON.stringify({ email, password }),
  });
  saveSession({ token: payload.token, user: payload.user });
  return payload;
}

export async function logoutAccount() {
  try {
    await apiFetch('/auth/logout', { method: 'POST' });
  } catch {
    // Offline or server unreachable: still clear local session cleanly
  } finally {
    clearSession();
  }
}

export async function getCurrentUser() {
  return apiFetch<{ user: User }>('/auth/me');
}

export async function requestPasswordReset(email: string) {
  return apiFetch<{ success: boolean; message: string; reset_token?: string }>('/auth/request-password-reset', {
    method: 'POST', body: JSON.stringify({ email }),
  });
}

export async function resetPassword(token: string, password: string) {
  return apiFetch<{ success: boolean; message: string }>('/auth/reset-password', {
    method: 'POST', body: JSON.stringify({ token, password }),
  });
}

export async function verifyEmail(token: string) {
  const payload = await apiFetch<{ token: string; user: User }>('/auth/verify-email', {
    method: 'POST', body: JSON.stringify({ token }),
  });
  saveSession({ token: payload.token, user: payload.user });
  return payload;
}

export type CloudProfile = Record<string, unknown>;

export async function getProfile() {
  return apiFetch<{ profile: CloudProfile; updated_at: string | null }>('/account/profile');
}

export async function updateProfile(profile: Partial<CloudProfile>) {
  return apiFetch<{ success: boolean; profile: CloudProfile }>('/account/profile', {
    method: 'PUT',
    body: JSON.stringify({ profile }),
  });
}

export type ScoreSubmission = {
  player_name: string;
  score: number;
  level_reached: number;
  difficulty: string;
  ship_class: string;
  kills?: number;
  total_damage?: number;
  duration_seconds?: number;
};

export async function submitScore(scoreData: ScoreSubmission) {
  return apiFetch<{ success: boolean; id: number; score: number }>('/scores', {
    method: 'POST',
    body: JSON.stringify(scoreData),
  });
}

export async function getAccountStats() {
  return apiFetch<Record<string, number | string>>('/account/stats');
}

export async function listLobbies(signal?: AbortSignal) {
  const session = readSession();
  const headers: HeadersInit = { Accept: 'application/json' };
  if (session?.token) headers.Authorization = `Bearer ${session.token}`;
  const response = await fetch(`${API_BASE_URL}/multiplayer/lobbies`, { signal, headers });
  const payload = await response.json().catch(() => ({})) as { lobbies?: Lobby[]; error?: string };
  if (!response.ok) throw new Error(payload.error || `Lobby list failed (${response.status})`);
  return payload.lobbies ?? [];
}

export async function createLobby(mode: Lobby['mode'], shipClass: string) {
  return apiFetch<{ lobby: Lobby }>('/multiplayer/lobbies', {
    method: 'POST', body: JSON.stringify({ mode, max_players: mode === 'duel' ? 2 : 4, ship_class: shipClass }),
  });
}

export async function joinLobby(code: string, shipClass: string) {
  return apiFetch<{ lobby: Lobby }>(`/multiplayer/lobbies/${encodeURIComponent(code)}/join`, {
    method: 'POST', body: JSON.stringify({ ship_class: shipClass }),
  });
}

export async function setLobbyReady(code: string, ready: boolean) {
  return apiFetch<{ lobby: Lobby }>(`/multiplayer/lobbies/${encodeURIComponent(code)}/ready`, {
    method: 'POST', body: JSON.stringify({ ready }),
  });
}

export async function startLobby(code: string) {
  return apiFetch<{ lobby: Lobby }>(`/multiplayer/lobbies/${encodeURIComponent(code)}/start`, { method: 'POST' });
}

export async function leaveLobby(code: string) {
  return apiFetch<{ success: boolean; lobby?: Lobby }>(`/multiplayer/lobbies/${encodeURIComponent(code)}/leave`, { method: 'POST' });
}
