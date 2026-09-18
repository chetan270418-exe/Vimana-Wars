import { useEffect, useState } from 'react';
import Panel from './ui/Panel';
import StarField from './ui/StarField';
import { loadSettings, resetSettings, saveSettings } from '../lib/settings';
import type { UserSettings } from '../types/game';

type Tab = 'audio' | 'display' | 'controls';

const BINDINGS = [
  { action: 'MOVE UP',       key: 'W / ↑',       category: 'Movement' },
  { action: 'MOVE DOWN',     key: 'S / ↓',       category: 'Movement' },
  { action: 'MOVE LEFT',     key: 'A / ←',       category: 'Movement' },
  { action: 'MOVE RIGHT',    key: 'D / →',       category: 'Movement' },
  { action: 'PRIMARY FIRE',  key: 'SPACE / LMB', category: 'Combat' },
  { action: 'DIVINE ABILITY',key: 'SHIFT',       category: 'Combat' },
  { action: 'PAUSE',         key: 'ESC',         category: 'System' },
  { action: 'TOGGLE HUD',    key: 'H',           category: 'System' },
  { action: 'SCREENSHOT',    key: 'F12',         category: 'System' },
];

function Slider({ label, value, onChange, color = '#E9C400' }: {
  label: string; value: number; onChange: (v: number) => void; color?: string;
}) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between items-center">
        <span className="text-xs tracking-[0.2em]" style={{ fontFamily: '"Cinzel", serif', color: '#D0C6AB' }}>
          {label}
        </span>
        <span
          className="text-xs w-8 text-right"
          style={{ fontFamily: '"JetBrains Mono", monospace', color }}
        >
          {value}
        </span>
      </div>
      <div className="relative">
        <div
          className="absolute top-1/2 left-0 -translate-y-1/2 h-[3px] pointer-events-none"
          style={{ width: `${value}%`, background: color, boxShadow: `0 0 6px ${color}66` }}
        />
        <input
          type="range"
          min={0}
          max={100}
          value={value}
          onChange={e => onChange(Number(e.target.value))}
          className="relative z-10"
          style={{ width: '100%' }}
        />
      </div>
    </div>
  );
}

function Toggle({ label, desc, value, onChange }: {
  label: string; desc?: string; value: boolean; onChange: (v: boolean) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-4">
      <div>
        <div className="text-xs tracking-[0.18em]" style={{ fontFamily: '"Cinzel", serif', color: '#D0C6AB' }}>{label}</div>
        {desc && <div className="text-[10px] mt-0.5 tracking-wider" style={{ color: '#8F98A8' }}>{desc}</div>}
      </div>
      <button
        onClick={() => onChange(!value)}
        className="flex-shrink-0 transition-all duration-200"
        style={{
          width: 42, height: 22,
          background: value ? 'rgba(0,219,231,0.2)' : 'rgba(143,152,168,0.1)',
          border: `1px solid ${value ? 'rgba(0,219,231,0.6)' : 'rgba(143,152,168,0.3)'}`,
          clipPath: 'polygon(4px 0%,calc(100% - 4px) 0%,100% 4px,100% calc(100% - 4px),calc(100% - 4px) 100%,4px 100%,0% calc(100% - 4px),0% 4px)',
          position: 'relative',
        }}
      >
        <div
          style={{
            position: 'absolute',
            top: 3, bottom: 3,
            width: 16,
            left: value ? 'calc(100% - 19px)' : 3,
            background: value ? '#00DBE7' : '#8F98A8',
            transition: 'all 0.2s ease',
            boxShadow: value ? '0 0 6px rgba(0,219,231,0.7)' : 'none',
          }}
        />
      </button>
    </div>
  );
}

type Props = { onNavigate: (s: string) => void };

export default function Settings({ onNavigate }: Props) {
  const [tab, setTab] = useState<Tab>('audio');
  const [settings, setSettings] = useState<UserSettings>(() => loadSettings());

  useEffect(() => {
    saveSettings(settings);
  }, [settings]);

  const update = <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => {
    setSettings(previous => ({ ...previous, [key]: value }));
  };

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />

      {/* Header */}
      <div
        className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6"
        style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.85)', backdropFilter: 'blur(12px)' }}
      >
        <button
          onClick={() => onNavigate('main-menu')}
          className="text-[10px] tracking-[0.25em] transition-colors hover:text-gold"
          style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}
        >
          ← MAIN MENU
        </button>
        <div className="h-4 w-px" style={{ background: 'rgba(233,196,0,0.2)' }} />
        <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
          SETTINGS
        </span>
      </div>

      {/* Content */}
      <div className="absolute inset-0 flex gap-5 z-10" style={{ top: 52, bottom: 40, padding: '20px 24px' }}>

        {/* Sidebar tabs */}
        <div className="flex flex-col gap-1.5 shrink-0" style={{ width: 160 }}>
          {(['audio', 'display', 'controls'] as Tab[]).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className="text-left px-4 py-3 transition-all duration-150"
              style={{
                fontFamily: '"Cinzel", serif',
                fontSize: 11,
                letterSpacing: '0.22em',
                color: tab === t ? '#FFF6DF' : '#8F98A8',
                background: tab === t ? 'rgba(233,196,0,0.08)' : 'transparent',
                borderLeft: `2px solid ${tab === t ? '#E9C400' : 'rgba(233,196,0,0.15)'}`,
              }}
            >
              {t.toUpperCase()}
            </button>
          ))}

          {/* Decorative */}
          <div className="mt-4 flex flex-col gap-2">
            <div className="h-px" style={{ background: 'rgba(233,196,0,0.1)' }} />
            <div className="text-[9px] tracking-[0.2em] px-1" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
              v2.0 VEDIC-PUNK
            </div>
            <div className="text-[9px] tracking-wider px-1" style={{ fontFamily: '"JetBrains Mono", monospace', color: 'rgba(143,152,168,0.5)' }}>
              BUILD 20260916
            </div>
          </div>
        </div>

        {/* Panel */}
        <Panel variant="default" cut={14} className="flex-1">
          <div className="p-6 flex flex-col gap-6 overflow-y-auto" style={{ maxHeight: '100%' }}>

            {tab === 'audio' && (
              <>
                <div>
                  <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    AUDIO LEVELS
                  </div>
                  <div className="flex flex-col gap-5">
                    <Slider label="MASTER VOLUME" value={settings.masterVolume} onChange={v => update('masterVolume', v)} color="#E9C400" />
                    <Slider label="MUSIC" value={settings.musicVolume} onChange={v => update('musicVolume', v)} color="#74F5FF" />
                    <Slider label="SOUND EFFECTS" value={settings.sfxVolume} onChange={v => update('sfxVolume', v)} color="#74F5FF" />
                    <Slider label="AMBIENCE" value={settings.ambienceVolume} onChange={v => update('ambienceVolume', v)} color="#8F98A8" />
                  </div>
                </div>

                <div className="h-px" style={{ background: 'rgba(233,196,0,0.1)' }} />

                <div>
                  <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    AUDIO OPTIONS
                  </div>
                  <div className="flex flex-col gap-4">
                    <Toggle label="MUTE WHEN UNFOCUSED" desc="Silence audio when window loses focus" value={settings.muteWhenUnfocused} onChange={v => update('muteWhenUnfocused', v)} />
                    <Toggle label="DYNAMIC MUSIC" desc="Music intensity adapts to combat state" value={settings.dynamicMusic} onChange={v => update('dynamicMusic', v)} />
                  </div>
                </div>
              </>
            )}

            {tab === 'display' && (
              <>
                <div>
                  <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    DISPLAY
                  </div>
                  <div className="flex flex-col gap-4">
                    <Toggle label="FULLSCREEN" desc="Run in fullscreen mode" value={settings.fullscreen} onChange={v => update('fullscreen', v)} />
                    <Toggle label="VSYNC" desc="Cap frame rate to display refresh rate" value={settings.vsync} onChange={v => update('vsync', v)} />
                    <div className="flex flex-col gap-2">
                      <span className="text-xs tracking-[0.18em]" style={{ fontFamily: '"Cinzel", serif', color: '#D0C6AB' }}>RESOLUTION</span>
                      <div className="flex gap-2">
                        {['1920 × 1080', '2560 × 1440', '3840 × 2160'].map(r => (
                          <button
                            key={r}
                            className="px-3 py-1.5 text-[10px] tracking-wider transition-all duration-150"
                            style={{
                              fontFamily: '"JetBrains Mono", monospace',
                              color: r === settings.resolution ? '#FFF6DF' : '#8F98A8',
                              background: r === settings.resolution ? 'rgba(233,196,0,0.1)' : 'transparent',
                              border: `1px solid ${r === settings.resolution ? 'rgba(233,196,0,0.4)' : 'rgba(143,152,168,0.2)'}`,
                            }}
                            onClick={() => update('resolution', r)}
                          >
                            {r}
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="h-px" style={{ background: 'rgba(233,196,0,0.1)' }} />

                <div>
                  <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    VISUAL EFFECTS
                  </div>
                  <div className="flex flex-col gap-4">
                    <Toggle label="PARTICLE EFFECTS" desc="Explosions, engine trails, debris" value={settings.particles} onChange={v => update('particles', v)} />
                    <Toggle label="SCANLINE OVERLAY" desc="CRT scanline aesthetic on UI panels" value={settings.scanlines} onChange={v => update('scanlines', v)} />
                    <Toggle label="BLOOM EFFECT" desc="Glow on weapons and ship engines" value={settings.bloom} onChange={v => update('bloom', v)} />
                    <Toggle label="REDUCED FLASHING" desc="Minimizes rapid flash effects" value={settings.reducedFlashes} onChange={v => update('reducedFlashes', v)} />
                  </div>
                </div>
              </>
            )}

            {tab === 'controls' && (
              <>
                <div>
                  <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    KEY BINDINGS
                  </div>
                  <div className="flex flex-col gap-0">
                    {(() => {
                      const categories = [...new Set(BINDINGS.map(b => b.category))];
                      return categories.map(cat => (
                        <div key={cat} className="mb-4">
                          <div className="text-[9px] tracking-[0.3em] mb-2 px-1" style={{ fontFamily: '"Cinzel", serif', color: 'rgba(233,196,0,0.5)' }}>
                            {cat.toUpperCase()}
                          </div>
                          {BINDINGS.filter(b => b.category === cat).map(b => (
                            <div
                              key={b.action}
                              className="flex justify-between items-center py-2 px-3 transition-colors hover:bg-white/[0.02]"
                              style={{ borderBottom: '1px solid rgba(255,255,255,0.04)' }}
                            >
                              <span className="text-xs tracking-wider" style={{ color: '#D0C6AB' }}>{b.action}</span>
                              <span
                                className="text-xs px-2 py-0.5"
                                style={{
                                  fontFamily: '"JetBrains Mono", monospace',
                                  color: '#74F5FF',
                                  background: 'rgba(0,219,231,0.08)',
                                  border: '1px solid rgba(0,219,231,0.2)',
                                }}
                              >
                                {b.key}
                              </span>
                            </div>
                          ))}
                        </div>
                      ));
                    })()}
                  </div>
                  <button
                    className="text-[10px] tracking-[0.18em] mt-3 px-3 py-2"
                    style={{ color: '#E9C400', border: '1px solid rgba(233,196,0,0.3)' }}
                    onClick={() => setSettings(resetSettings())}
                  >
                    RESET ALL SETTINGS
                  </button>
                  <div className="text-[10px] tracking-wider mt-3" style={{ color: '#8F98A8' }}>
                    Settings are saved automatically on this device.
                  </div>
                </div>
              </>
            )}
          </div>
        </Panel>
      </div>
    </div>
  );
}
