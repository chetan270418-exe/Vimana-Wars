import { REALMS, SHIPS } from '../data/gameData';

export type WebProgression = {
  lastWave: number;
  lastShip: string;
  completedRealms: string[];
};

const KEY = 'vimana-web-progression';
const SHIP_UNLOCK_WAVES: Record<string, number> = {
  pushpaka: 0,
  garuda: 0,
  tripura: 4,
  naga: 7,
  vajra: 10,
  soma: 13,
  kubera: 16,
  surya: 19,
};

function parseWave(waves: string): number {
  return Number(waves.split(/[–-]/)[0]) || 1;
}

export function getProgression(): WebProgression {
  try {
    const saved = JSON.parse(window.localStorage.getItem(KEY) || '{}') as Partial<WebProgression>;
    return {
      lastWave: Math.max(0, Number(saved.lastWave) || 0),
      lastShip: typeof saved.lastShip === 'string' ? saved.lastShip : 'pushpaka',
      completedRealms: Array.isArray(saved.completedRealms) ? saved.completedRealms.filter((id): id is string => typeof id === 'string') : [],
    };
  } catch {
    return { lastWave: 0, lastShip: 'pushpaka', completedRealms: [] };
  }
}

export function saveProgression(patch: Partial<WebProgression>): WebProgression {
  const next = { ...getProgression(), ...patch };
  window.localStorage.setItem(KEY, JSON.stringify(next));
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
