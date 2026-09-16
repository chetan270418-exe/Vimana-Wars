import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';

const PARTICLES = Array.from({ length: 24 }, (_, i) => ({
  id: i,
  x: ((i * 43.1 + 8) % 85) + 7.5,
  dx: ((i * 17.3) % 24) - 12,
  delay: (i * 0.18) % 2.5,
  duration: ((i * 0.27) % 1.2) + 1,
  size: ((i * 1.2) % 5) + 3,
  color: i % 3 === 0 ? '#E9C400' : i % 3 === 1 ? '#74F5FF' : '#FFF6DF',
}));

import { useMemo } from 'react';
import type { RunResult } from '../types/game';

const DEFAULT_STATS = [
  { label: 'REALM LIBERATED', value: 'Kshira Sagara', color: '#50F0DC' },
  { label: 'FINAL SCORE',     value: '7,441,200',     color: '#E9C400' },
  { label: 'WAVES PERFECT',   value: '3 / 3',         color: '#40E090' },
  { label: 'ENEMIES SLAIN',   value: '318',           color: '#74F5FF' },
  { label: 'BOSS DEFEATED',   value: 'Vritra',        color: '#FF9650' },
  { label: 'BOON USED',       value: 'Vajra Overcharge', color: '#7EA8FF' },
  { label: 'VIMANA',          value: 'Vajra',         color: '#FFD060' },
  { label: 'TIME',            value: '14:22',         color: '#8F98A8' },
];

const REWARDS = [
  { label: 'DIVINE CURRENCY', value: '+480 SC',  color: '#E9C400' },
  { label: 'ACHIEVEMENT',     value: 'REALM PURIFIER', color: '#74F5FF' },
  { label: 'NEXT REALM',      value: 'Dandaka Void UNLOCKED', color: '#D264FF' },
];

type Props = {
  onNavigate: (s: string) => void;
  result?: RunResult | null;
};

export default function Victory({ onNavigate, result }: Props) {
  const stats = useMemo(() => {
    if (!result) return DEFAULT_STATS;
    const mins = Math.floor(result.durationSeconds / 60);
    const secs = result.durationSeconds % 60;
    const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    return [
      { label: 'REALM LIBERATED', value: 'Dandaka Void', color: '#50F0DC' },
      { label: 'FINAL SCORE', value: result.score.toLocaleString(), color: '#E9C400' },
      { label: 'WAVES CLEARED', value: `${result.waveReached} / 20`, color: '#40E090' },
      { label: 'ENEMIES SLAIN', value: result.kills.toString(), color: '#74F5FF' },
      { label: 'MAX COMBO', value: `x${result.highestCombo}`, color: '#FF9650' },
      { label: 'BOONS CLAIMED', value: `${result.boons.length} Deva Gifts`, color: '#7EA8FF' },
      { label: 'VIMANA', value: result.shipId.toUpperCase(), color: '#FFD060' },
      { label: 'TIME', value: timeStr, color: '#8F98A8' },
    ];
  }, [result]);
  return (
    <div
      className="relative w-full h-full overflow-hidden flex flex-col items-center justify-center"
      style={{ background: '#030A08', paddingBottom: 40 }}
    >
      <StarField />

      {/* Gold-cyan gradient vignette */}
      <div className="absolute inset-0 pointer-events-none" style={{
        background: [
          'radial-gradient(ellipse 70% 70% at 50% 30%, rgba(20,60,40,0.45) 0%, transparent 70%)',
          'radial-gradient(ellipse 50% 50% at 30% 70%, rgba(0,30,60,0.35) 0%, transparent 60%)',
        ].join(','),
      }} />

      {/* Celebration particles */}
      {PARTICLES.map(p => (
        <div
          key={p.id}
          className="absolute pointer-events-none"
          style={{
            left: `${p.x}%`,
            bottom: 0,
            width: p.size,
            height: p.size * 2.5,
            background: p.color,
            boxShadow: `0 0 ${p.size * 1.5}px ${p.color}`,
            animation: `ember ${p.duration}s ease-out ${p.delay}s infinite`,
            ['--dx' as string]: `${p.dx}px`,
            opacity: 0.8,
          }}
        />
      ))}

      {/* Content */}
      <div className="relative z-10 w-full flex flex-col items-center" style={{ maxWidth: 640, padding: '0 24px' }}>

        {/* Header */}
        <div className="text-center mb-6" style={{ animation: 'fade-in 0.7s ease' }}>
          <div className="text-[10px] tracking-[0.5em] mb-2" style={{ fontFamily: '"Cinzel", serif', color: '#40E090', opacity: 0.8 }}>
            — REALM CLEANSED —
          </div>
          <h1
            className="text-5xl font-black tracking-[0.15em] mb-1"
            style={{
              fontFamily: '"Cinzel Decorative", serif',
              color: '#FFF6DF',
              textShadow: '0 0 40px rgba(233,196,0,0.6), 0 0 80px rgba(0,219,231,0.25)',
            }}
          >
            VICTORY
          </h1>
          <div className="flex items-center gap-3 justify-center mt-2">
            <div className="h-px w-20" style={{ background: 'linear-gradient(to right, transparent, rgba(233,196,0,0.7))' }} />
            <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#E9C400' }}>◈</span>
            <div className="h-px w-20" style={{ background: 'linear-gradient(to left, transparent, rgba(233,196,0,0.7))' }} />
          </div>
        </div>

        {/* Stats */}
        <Panel variant="active" cut={14} className="w-full" style={{ animation: 'slide-in-up 0.5s ease 0.2s both' }}>
          <div className="p-5">
            <div className="text-[9px] tracking-[0.4em] mb-4" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
              MISSION DEBRIEF
            </div>
            <div className="grid grid-cols-2 gap-x-8 gap-y-2.5">
              {stats.map(row => (
                <div key={row.label} className="flex justify-between items-center">
                  <span className="text-xs tracking-wider" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    {row.label}
                  </span>
                  <span
                    className="text-sm font-semibold"
                    style={{ fontFamily: '"JetBrains Mono", monospace', color: row.color }}
                  >
                    {row.value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </Panel>

        {/* Rewards */}
        <div className="flex gap-3 w-full mt-3" style={{ animation: 'slide-in-up 0.5s ease 0.35s both' }}>
          {REWARDS.map(r => (
            <Panel key={r.label} variant="dim" cut={8} className="flex-1">
              <div className="p-3 text-center">
                <div className="text-[9px] tracking-[0.2em] mb-1" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                  {r.label}
                </div>
                <div className="text-xs font-bold tracking-wider" style={{ color: r.color }}>{r.value}</div>
              </div>
            </Panel>
          ))}
        </div>

        {/* Buttons */}
        <div className="flex gap-4 mt-5" style={{ animation: 'fade-in 0.5s ease 0.5s both' }}>
          <VedicButton variant="ghost" onClick={() => onNavigate('main-menu')}>
            MAIN MENU
          </VedicButton>
          <VedicButton variant="secondary" onClick={() => onNavigate('realm-map')}>
            VIEW REALM MAP
          </VedicButton>
          <VedicButton variant="primary" onClick={() => onNavigate('ship-select')}>
            CONTINUE CAMPAIGN ▶
          </VedicButton>
        </div>
      </div>
    </div>
  );
}
