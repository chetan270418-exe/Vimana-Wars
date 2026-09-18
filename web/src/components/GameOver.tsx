import { useMemo } from 'react';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';

const EMBERS = Array.from({ length: 28 }, (_, i) => ({
  id: i,
  x: ((i * 37.1 + 10) % 80) + 10,
  dx: ((i * 13.7) % 30) - 15,
  delay: (i * 0.21) % 3,
  duration: ((i * 0.31) % 1.5) + 1.2,
  size: ((i * 1.3) % 5) + 3,
  color: i % 3 === 0 ? '#FF6B72' : i % 3 === 1 ? '#E9C400' : '#FF3020',
}));

import type { RunResult } from '../types/game';

const DEFAULT_STATS = [
  { label: 'WAVE REACHED',   value: '8 / 20',     color: '#D0C6AB' },
  { label: 'FINAL SCORE',    value: '4,328,900',   color: '#E9C400' },
  { label: 'ENEMIES SLAIN',  value: '247',         color: '#74F5FF' },
  { label: 'ELITE KILLS',    value: '12',          color: '#FF9650' },
  { label: 'PERFECT WAVES',  value: '3',           color: '#40E090' },
  { label: 'REALM REACHED',  value: 'Dandaka Void', color: '#D264FF' },
  { label: 'TIME ELAPSED',   value: '18:47',       color: '#8F98A8' },
  { label: 'VIMANA USED',    value: 'Garuda',      color: '#FFD060' },
];

type Props = {
  onNavigate: (s: string) => void;
  result?: RunResult | null;
  syncStatus?: 'idle' | 'syncing' | 'synced' | 'offline';
};

export default function GameOver({ onNavigate, result, syncStatus = 'idle' }: Props) {
  const embers = useMemo(() => EMBERS, []);
  const stats = useMemo(() => {
    if (!result) return DEFAULT_STATS;
    const mins = Math.floor(result.durationSeconds / 60);
    const secs = result.durationSeconds % 60;
    const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    return [
      { label: 'WAVE REACHED', value: `${result.waveReached} / 20`, color: '#D0C6AB' },
      { label: 'FINAL SCORE', value: result.score.toLocaleString(), color: '#E9C400' },
      { label: 'ENEMIES SLAIN', value: result.kills.toString(), color: '#74F5FF' },
      { label: 'HIGHEST COMBO', value: `x${result.highestCombo}`, color: '#FF9650' },
      { label: 'TOTAL DAMAGE', value: result.totalDamage.toLocaleString(), color: '#40E090' },
      { label: 'ACTIVE BOONS', value: `${result.boons.length} Deva Gifts`, color: '#D264FF' },
      { label: 'TIME ELAPSED', value: timeStr, color: '#8F98A8' },
      { label: 'VIMANA USED', value: result.shipId.toUpperCase(), color: '#FFD060' },
    ];
  }, [result]);

  return (
    <div className="relative w-full h-full overflow-hidden flex flex-col items-center justify-center" style={{ background: '#050308', paddingBottom: 40 }}>
      <StarField />

      {/* Red vignette */}
      <div className="absolute inset-0 pointer-events-none" style={{
        background: 'radial-gradient(ellipse 80% 80% at 50% 50%, rgba(90,0,20,0.35) 0%, rgba(25,0,8,0.7) 70%, rgba(5,3,8,0.9) 100%)',
      }} />

      {/* Ember particles */}
      {embers.map(e => (
        <div
          key={e.id}
          className="absolute rounded-full pointer-events-none"
          style={{
            left: `${e.x}%`,
            bottom: 0,
            width: e.size,
            height: e.size,
            background: e.color,
            boxShadow: `0 0 ${e.size * 2}px ${e.color}`,
            animation: `ember ${e.duration}s ease-out ${e.delay}s infinite`,
            ['--dx' as string]: `${e.dx}px`,
          }}
        />
      ))}

      {/* Horizontal crack lines */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {[30, 55, 72].map(y => (
          <div key={y} className="absolute left-0 right-0 h-px" style={{
            top: `${y}%`,
            background: `linear-gradient(to right, transparent, rgba(191,0,54,${0.05 + y * 0.001}), transparent)`,
          }} />
        ))}
      </div>

      {/* Content */}
      <div className="relative z-10 w-full flex flex-col items-center" style={{ maxWidth: 620, padding: '0 24px' }}>

        {/* Title */}
        <div className="text-center mb-8" style={{ animation: 'fade-in 0.7s ease' }}>
          <div className="text-[10px] tracking-[0.5em] mb-2" style={{ fontFamily: '"Cinzel", serif', color: '#FF6B72', opacity: 0.7 }}>
            — MISSION FAILED —
          </div>
          <h1
            className="text-5xl font-black tracking-[0.15em] mb-1"
            style={{
              fontFamily: '"Cinzel Decorative", serif',
              color: '#FF6B72',
              textShadow: '0 0 40px rgba(191,0,54,0.7), 0 0 80px rgba(191,0,54,0.3)',
            }}
          >
            VIMANA
          </h1>
          <h1
            className="text-5xl font-black tracking-[0.15em]"
            style={{
              fontFamily: '"Cinzel Decorative", serif',
              color: '#FF6B72',
              textShadow: '0 0 40px rgba(191,0,54,0.7), 0 0 80px rgba(191,0,54,0.3)',
            }}
          >
            DESTROYED
          </h1>
        </div>

        {/* Stats panel */}
        <Panel variant="danger" cut={14} className="w-full" style={{ animation: 'slide-in-up 0.5s ease 0.3s both' }}>
          <div className="p-6">
            <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
              COMBAT REPORT
            </div>
            <div className="grid grid-cols-2 gap-x-8 gap-y-3">
              {stats.map(row => (
                <div key={row.label} className="flex justify-between items-center">
                  <span className="text-xs tracking-wider" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    {row.label}
                  </span>
                  <span
                    className="text-sm font-semibold tracking-wider"
                    style={{ fontFamily: '"JetBrains Mono", monospace', color: row.color }}
                  >
                    {row.value}
                  </span>
                </div>
              ))}
            </div>

            {/* Personal best note */}
            <div
              className="mt-4 px-3 py-2 text-xs tracking-wider text-center"
              style={{
                fontFamily: '"Cinzel", serif',
                color: '#E9C400',
                background: 'rgba(233,196,0,0.08)',
                border: '1px solid rgba(233,196,0,0.25)',
              }}
            >
              ◈ PERSONAL BEST: WAVE 11 — LANKA · SCORE 6,812,400
            </div>
          </div>
        </Panel>

        {syncStatus !== 'idle' && (
          <div className="mt-3 text-[10px] tracking-[0.18em]" style={{ color: syncStatus === 'synced' ? '#40E090' : syncStatus === 'offline' ? '#FF9650' : '#74F5FF' }}>
            {syncStatus === 'synced' ? '● SCORE SYNCED TO CLOUD' : syncStatus === 'offline' ? '◌ SCORE KEPT LOCALLY · CLOUD LINK UNAVAILABLE' : '◌ SYNCING SCORE…'}
          </div>
        )}

        {/* Buttons */}
        <div className="flex gap-4 mt-6" style={{ animation: 'fade-in 0.5s ease 0.6s both' }}>
          <VedicButton variant="ghost" onClick={() => onNavigate('main-menu')}>
            RETURN TO BASE
          </VedicButton>
          <VedicButton variant="danger" onClick={() => onNavigate('ship-select')}>
            RISE AGAIN ▶
          </VedicButton>
        </div>
      </div>
    </div>
  );
}
