import { useState } from 'react';
import StarField from '../components/StarField';
import NeonPanel from '../components/NeonPanel';

type SettingsTab = 'AUDIO' | 'CONTROLS' | 'ACCESSIBILITY';

const AUDIO_SETTINGS = [
  { label: 'MASTER AUDIO VOLUME', key: 'master', value: 80, color: '#FFB800' },
  { label: 'SOUND EFFECTS (SFX)', key: 'sfx', value: 80, color: '#FFB800' },
  { label: 'CELESTIAL SOUNDTRACKS', key: 'music', value: 70, color: '#00FF88' },
  { label: 'TACTICAL UI AUDIO', key: 'ui', value: 75, color: '#FFB800' },
  { label: 'BOSS COMBAT DYNAMICS', key: 'boss', value: 85, color: '#FF6B00' },
];

const CONTROL_BINDINGS = [
  { action: 'MOVE',           binding: 'WASD / ARROW KEYS' },
  { action: 'PRIMARY FIRE',   binding: 'SPACE / LEFT MOUSE' },
  { action: 'SPECIAL WEAPON', binding: 'Q / RIGHT MOUSE' },
  { action: 'DASH',           binding: 'SHIFT / MIDDLE MOUSE' },
  { action: 'CHARGED SHOT',   binding: 'HOLD SPACE' },
  { action: 'PAUSE',          binding: 'ESCAPE / P' },
  { action: 'PILOT DOSSIER',  binding: 'P (MENU)' },
  { action: 'REVIVE BEACON',  binding: 'HOLD F (MULTIPLAYER)' },
  { action: 'SQUADRON CHAT',  binding: 'ENTER' },
];

const ACCESS_SETTINGS = [
  { label: 'COLOR BLIND MODE', key: 'colorblind', options: ['OFF', 'DEUTERANOPIA', 'PROTANOPIA', 'TRITANOPIA'], current: 'OFF' },
  { label: 'UI SCALE', key: 'uiscale', options: ['75%', '100%', '125%', '150%'], current: '100%' },
  { label: 'SCREENSHAKE', key: 'screenshake', options: ['OFF', 'LOW', 'MEDIUM', 'HIGH'], current: 'MEDIUM' },
  { label: 'SUBTITLES', key: 'subtitles', options: ['OFF', 'ON'], current: 'OFF' },
];

interface SystemSettingsProps {
  onBack: () => void;
}

export default function SystemSettings({ onBack }: SystemSettingsProps) {
  const [tab, setTab] = useState<SettingsTab>('AUDIO');
  const [audio, setAudio] = useState<Record<string, number>>(
    Object.fromEntries(AUDIO_SETTINGS.map(s => [s.key, s.value]))
  );
  const [access, setAccess] = useState<Record<string, string>>(
    Object.fromEntries(ACCESS_SETTINGS.map(s => [s.key, s.current]))
  );

  const tabColors: Record<SettingsTab, 'gold' | 'cyan' | 'green'> = {
    AUDIO: 'gold', CONTROLS: 'cyan', ACCESSIBILITY: 'green',
  };

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 80% 70% at 50% 40%, #070D14 0%, #05080E 100%)' }}>
      <StarField count={90} />

      {/* Header */}
      <NeonPanel color="gold" corners={false} className="absolute top-0 left-0 right-0 px-6 py-3 z-10">
        <div className="font-display text-sm tracking-widest glow-gold" style={{ color: '#FFB800' }}>
          ASTRAL SYSTEM SETTINGS & TELEMETRY
        </div>
      </NeonPanel>

      {/* Tabs */}
      <div className="absolute top-14 left-6 right-6 flex gap-3 z-10">
        {(['AUDIO', 'CONTROLS', 'ACCESSIBILITY'] as SettingsTab[]).map(t => (
          <NeonPanel key={t} color={tabColors[t]} hover corners={false}
            onClick={() => setTab(t)}
            className={`px-8 py-2.5 transition-all ${tab === t ? 'bg-[rgba(255,255,255,0.05)]' : ''}`}>
            <span className="font-body text-sm font-semibold tracking-widest"
              style={{ color: tab === t ? '#fff' : 'var(--muted-foreground)' }}>
              {t}
            </span>
          </NeonPanel>
        ))}
      </div>

      {/* Content area */}
      <div className="absolute inset-0 px-6 pt-28 pb-20 flex flex-col">
        <NeonPanel color="gold" className="flex-1 p-6">
          {tab === 'AUDIO' && (
            <div className="space-y-5 max-w-lg mx-auto">
              {AUDIO_SETTINGS.map(setting => (
                <div key={setting.key} className="flex items-center gap-4">
                  <span className="font-mono text-[9px] tracking-widest text-muted-foreground w-52 shrink-0">
                    {setting.label}
                  </span>
                  {/* Minus button */}
                  <NeonPanel color="gold" hover corners={false}
                    onClick={() => setAudio(a => ({ ...a, [setting.key]: Math.max(0, a[setting.key] - 5) }))}
                    className="w-8 h-8 flex items-center justify-center shrink-0">
                    <span className="font-display text-xs" style={{ color: '#FFB800' }}>-</span>
                  </NeonPanel>
                  {/* Track + value */}
                  <div className="flex-1 h-1.5 bg-muted rounded-sm overflow-hidden cursor-pointer relative"
                    onClick={e => {
                      const rect = (e.target as HTMLElement).closest('.flex-1')!.getBoundingClientRect();
                      const pct = Math.round(((e.clientX - rect.left) / rect.width) * 100);
                      setAudio(a => ({ ...a, [setting.key]: Math.max(0, Math.min(100, pct)) }));
                    }}>
                    <div className="h-full transition-all duration-100"
                      style={{
                        width: `${audio[setting.key]}%`,
                        background: setting.color,
                        boxShadow: `0 0 6px ${setting.color}`,
                      }}/>
                  </div>
                  <span className="font-mono text-[10px] w-8 text-right shrink-0"
                    style={{ color: setting.color }}>
                    {audio[setting.key]}%
                  </span>
                  {/* Plus button */}
                  <NeonPanel color="gold" hover corners={false}
                    onClick={() => setAudio(a => ({ ...a, [setting.key]: Math.min(100, a[setting.key] + 5) }))}
                    className="w-8 h-8 flex items-center justify-center shrink-0">
                    <span className="font-display text-xs" style={{ color: '#FFB800' }}>+</span>
                  </NeonPanel>
                </div>
              ))}

              {/* Toggle fullscreen */}
              <div className="pt-4 flex justify-center">
                <NeonPanel color="cyan" hover corners={false} className="px-16 py-3 text-center">
                  <span className="font-mono text-[10px] tracking-widest" style={{ color: '#00E5FF' }}>
                    TOGGLE FULLSCREEN
                  </span>
                </NeonPanel>
              </div>
            </div>
          )}

          {tab === 'CONTROLS' && (
            <div className="max-w-lg mx-auto space-y-1">
              <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-4">
                KEY BINDINGS — READ ONLY // REBIND IN FUTURE UPDATE
              </div>
              {CONTROL_BINDINGS.map(b => (
                <div key={b.action} className="flex items-center justify-between py-2.5"
                  style={{ borderBottom: '1px solid #162030' }}>
                  <span className="font-mono text-[9px] tracking-widest text-muted-foreground">{b.action}</span>
                  <NeonPanel color="white" corners={false} className="px-4 py-1.5">
                    <span className="font-mono text-[10px]" style={{ color: '#C0D0E0' }}>{b.binding}</span>
                  </NeonPanel>
                </div>
              ))}
            </div>
          )}

          {tab === 'ACCESSIBILITY' && (
            <div className="max-w-lg mx-auto space-y-6">
              {ACCESS_SETTINGS.map(s => (
                <div key={s.key}>
                  <div className="font-mono text-[9px] tracking-widest text-muted-foreground mb-2">{s.label}</div>
                  <div className="flex gap-2">
                    {s.options.map(opt => (
                      <NeonPanel key={opt} color="green" hover corners={false}
                        onClick={() => setAccess(a => ({ ...a, [s.key]: opt }))}
                        className={`px-4 py-2 transition-all ${access[s.key] === opt ? 'bg-[rgba(0,255,136,0.08)]' : ''}`}>
                        <span className="font-mono text-[9px] tracking-widest"
                          style={{ color: access[s.key] === opt ? '#00FF88' : '#4A6070' }}>
                          {opt}
                        </span>
                      </NeonPanel>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </NeonPanel>
      </div>

      {/* Bottom actions */}
      <div className="absolute bottom-5 left-6 right-6 flex justify-between">
        <NeonPanel color="white" hover onClick={onBack} corners={false} className="px-8 py-3">
          <span className="font-mono text-[10px] tracking-widest text-muted-foreground">SAVE & BACK</span>
        </NeonPanel>
        <NeonPanel color="red" hover corners={false} className="px-8 py-3">
          <span className="font-mono text-[10px] tracking-widest" style={{ color: '#FF2244' }}>RESET DEFAULTS</span>
        </NeonPanel>
      </div>
    </div>
  );
}
