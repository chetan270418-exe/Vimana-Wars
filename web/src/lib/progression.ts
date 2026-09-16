import { REALMS, SHIPS } from '../data/gameData';
import { getSession } from './api';

export type WebProgression = {
  lastWave: number;
  lastShip: string;
  completedRealms: string[];
};

const LEGACY_KEY = 'vimana-web-progression';

export function getProgressionKey(customGameId?: string): string {
  const gameId = customGameId ?? getSession()?.user.game_id;
  return gameId ? `vimana-progression:${gameId}` : 'vimana-progression:guest';
}

const SHIP_UNLOCK_WAVES: Record<string, number> = {
  pushpaka: 0,
  tripura: 0,
  garuda: 0,
  vajra: 5,
  naga: 8,
  agneyastra: 10,
  soma: 13,
  kubera: 15,
  surya: 20,
};

function parseWave(waves: string): number {
  return Number(waves.split(/[–-]/)[0]) || 1;
}

export function getProgression(customGameId?: string): WebProgression {
  const key = getProgressionKey(customGameId);
  try {
    let raw = window.localStorage.getItem(key);
    if (!raw && key === 'vimana-progression:guest') {
      raw = window.localStorage.getItem(LEGACY_KEY);
    }
    const saved = JSON.parse(raw || '{}') as Partial<WebProgression>;
    return {
      lastWave: Math.max(0, Number(saved.lastWave) || 0),
      lastShip: typeof saved.lastShip === 'string' ? saved.lastShip : 'pushpaka',
      completedRealms: Array.isArray(saved.completedRealms) ? saved.completedRealms.filter((id): id is string => typeof id === 'string') : [],
    };
  } catch {
    return { lastWave: 0, lastShip: 'pushpaka', completedRealms: [] };
  }
}

export function saveProgression(patch: Partial<WebProgression>, customGameId?: string): WebProgression {
  const key = getProgressionKey(customGameId);
  const next = { ...getProgression(customGameId), ...patch };
  window.localStorage.setItem(key, JSON.stringify(next));
  return next;
}

export function shipUnlockWave(shipId: string): number {
  return SHIP_UNLOCK_WAVES[shipId] ?? 999;
}

export function isShipUnlocked(shipId: string, lastWave = getProgression().lastWave): boolean {
  return lastWave >= shipUnlockWave(shipId);
}

export function unlockedShipCount(lastWave = getProgression().lastWave): number {
  return SHIPS.filter(ship => isShipUnlocked(ship.id, lastWave)).length;
}

export function realmUnlockWave(realmId: string): number {
  const index = REALMS.findIndex(item => item.id === realmId);
  if (index === 0) return 0;
  const realm = index >= 0 ? REALMS[index] : undefined;
  return realm ? parseWave(realm.waves) : 999;
}

export function isRealmUnlocked(realmId: string, lastWave = getProgression().lastWave): boolean {
  return lastWave >= realmUnlockWave(realmId);
}

export function realmStartWave(realmId: string): number {
  return realmUnlockWave(realmId);
}

export function realmEndWave(realmId: string): number {
  const realm = REALMS.find(item => item.id === realmId);
  return realm ? Number(realm.waves.split(/[–-]/)[1]) || realmUnlockWave(realmId) : 0;
}
