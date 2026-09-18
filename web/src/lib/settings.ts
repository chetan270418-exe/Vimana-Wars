import { DEFAULT_SETTINGS, type UserSettings } from '../types/game';

const SETTINGS_KEY = 'vimana-web-settings-v1';

function clampVolume(value: unknown, fallback: number): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? Math.min(100, Math.max(0, Math.round(parsed))) : fallback;
}

export function loadSettings(): UserSettings {
  try {
    const raw = window.localStorage.getItem(SETTINGS_KEY);
    if (!raw) return DEFAULT_SETTINGS;
    const parsed = JSON.parse(raw) as Partial<UserSettings>;
    return {
      ...DEFAULT_SETTINGS,
      ...parsed,
      masterVolume: clampVolume(parsed.masterVolume, DEFAULT_SETTINGS.masterVolume),
      musicVolume: clampVolume(parsed.musicVolume, DEFAULT_SETTINGS.musicVolume),
      sfxVolume: clampVolume(parsed.sfxVolume, DEFAULT_SETTINGS.sfxVolume),
      ambienceVolume: clampVolume(parsed.ambienceVolume, DEFAULT_SETTINGS.ambienceVolume),
      keybindings: { ...DEFAULT_SETTINGS.keybindings, ...(parsed.keybindings ?? {}) },
    };
  } catch {
    return DEFAULT_SETTINGS;
  }
}

export function saveSettings(settings: UserSettings): void {
  try {
    window.localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  } catch {
    // Private browsing or a disabled storage provider should not break play.
  }
}

export function resetSettings(): UserSettings {
  saveSettings(DEFAULT_SETTINGS);
  return DEFAULT_SETTINGS;
}
