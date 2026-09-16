import { useState } from 'react';
import { REALMS, type Realm } from '../data/gameData';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';

const COMPLETED = new Set(['swarga', 'kshira-sagara']);
const CURRENT = 'dandaka';

const PATH_POINTS = REALMS.map(r => `${r.x}% ${r.y}%`).join(', ');

type Props = { onNavigate: (s: string) => void };

function RealmNode({ realm, status, selected, onClick }: {
  realm: Realm;
  status: 'completed' | 'current' | 'locked';
  selected: boolean;
  onClick: () => void;
}) {
  const colors = {
    completed: { ring: realm.accentColor, bg: `${realm.accentColor}22`, icon: realm.accentColor },
    current:   { ring: '#00DBE7', bg: 'rgba(0,219,231,0.12)', icon: '#74F5FF' },
    locked:    { ring: 'rgba(143,152,168,0.3)', bg: 'rgba(20,26,40,0.5)', icon: '#8F98A8' },
  }[status];

  return (
    <button
      onClick={onClick}
      className="absolute flex flex-col items-center gap-1.5 -translate-x-1/2 -translate-y-1/2 group"
      style={{ left: `${realm.x}%`, top: `${realm.y}%` }}
    >
      {/* Node circle */}
      <div
        className="relative flex items-center justify-center transition-transform duration-200 group-hover:scale-110"
        style={{
          width: 44, height: 44,
          borderRadius: '50%',
          background: colors.bg,
          border: `2px solid ${selected ? '#FFF6DF' : colors.ring}`,
          boxShadow: status !== 'locked'
            ? `0 0 ${selected ? 20 : 12}px ${colors.ring}66, inset 0 0 10px ${colors.bg}`
            : 'none',
          animation: status === 'current' ? 'pulse-cyan 2s ease-in-out infinite' : undefined,
        }}
      >
        {status === 'completed' && <span style={{ color: colors.icon, fontSize: 16 }}>✓</span>}
        {status === 'current' && <span style={{ color: colors.icon, fontSize: 16 }}>◈</span>}
        {status === 'locked' && <span style={{ color: colors.icon, fontSize: 14 }}>⊘</span>}
      </div>
      {/* Label */}
      <div className="text-center" style={{ minWidth: 72 }}>
        <div
          className="text-[9px] tracking-[0.18em] font-semibold"
          style={{
            fontFamily: '"Cinzel", serif',
            color: status === 'locked' ? '#8F98A8' : '#FFF6DF',
          }}
        >
          {realm.name.toUpperCase()}
        </div>
        <div
          className="text-[8px] tracking-wider"
          style={{ fontFamily: '"JetBrains Mono", monospace', color: colors.ring }}
        >
          {realm.waves}
        </div>
      </div>
    </button>
  );
}

export default function RealmMap({ onNavigate }: Props) {
  const [selected, setSelected] = useState<Realm>(REALMS.find(r => r.id === CURRENT) ?? REALMS[0]);

  const status = (id: string) => COMPLETED.has(id) ? 'completed' : id === CURRENT ? 'current' : 'locked';

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />

      {/* Deep space background tint */}
      <div className="absolute inset-0 pointer-events-none" style={{
        background: 'radial-gradient(ellipse 80% 60% at 55% 50%, rgba(15,5,40,0.5) 0%, transparent 70%)',
      }} />

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
          REALM MAP — CAMPAIGN
        </span>
        <div className="ml-auto flex items-center gap-4 text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
          <span style={{ color: '#E9C400' }}>2 REALMS CLEANSED</span>
          <span>·</span>
          <span>CURRENT: DANDAKA VOID</span>
        </div>
      </div>

      {/* Map canvas */}
      <div className="absolute z-10" style={{ top: 52, bottom: 40, left: 0, right: 320 }}>
        {/* SVG connection path */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none" preserveAspectRatio="none">
          {/* Base path */}
          <polyline
            points={REALMS.map(r => `${r.x * window.innerWidth / 100 - 320 / 100},${r.y * (window.innerHeight - 92) / 100}`).join(' ')}
            fill="none"
            stroke="rgba(143,152,168,0.12)"
            strokeWidth="2"
            strokeDasharray="6 4"
          />
          {/* Completed path */}
          <polyline
            points={[...REALMS.slice(0, 3)].map(r => `${r.x * window.innerWidth / 100 - 320 / 100},${r.y * (window.innerHeight - 92) / 100}`).join(' ')}
            fill="none"
            stroke="rgba(233,196,0,0.35)"
            strokeWidth="2"
          />
        </svg>
        {/* Simple CSS path overlay using divs */}
        {REALMS.map((realm, i) => {
          if (i === 0) return null;
          const prev = REALMS[i - 1];
          const isPast = COMPLETED.has(realm.id) || COMPLETED.has(prev.id);
          return (
            <div
              key={`path-${i}`}
              className="absolute pointer-events-none"
              style={{
                left: `${Math.min(prev.x, realm.x)}%`,
                top: `${Math.min(prev.y, realm.y)}%`,
                width: `${Math.abs(realm.x - prev.x)}%`,
                height: `${Math.abs(realm.y - prev.y)}%`,
                borderLeft: `1px dashed ${isPast ? 'rgba(233,196,0,0.3)' : 'rgba(143,152,168,0.12)'}`,
              }}
            />
          );
        })}
        {/* Realm nodes */}
        {REALMS.map(realm => (
          <RealmNode
            key={realm.id}
            realm={realm}
            status={status(realm.id) as 'completed' | 'current' | 'locked'}
            selected={selected.id === realm.id}
            onClick={() => setSelected(realm)}
          />
        ))}
      </div>

      {/* Side detail panel */}
      <div
        className="absolute right-0 z-20 flex flex-col gap-3 p-4"
        style={{ top: 52, bottom: 40, width: 300, borderLeft: '1px solid rgba(233,196,0,0.1)' }}
      >
        <Panel variant={status(selected.id) === 'completed' ? 'selected' : status(selected.id) === 'current' ? 'active' : 'dim'} cut={12} className="flex-1">
          <div className="p-4 flex flex-col gap-4 h-full">
            <div>
              <div
                className="text-[9px] tracking-[0.4em] mb-1"
                style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}
              >
                {status(selected.id) === 'completed' ? '✓ LIBERATED' : status(selected.id) === 'current' ? '◈ CURRENT REALM' : '⊘ LOCKED'}
              </div>
              <h2
                className="text-xl tracking-[0.15em] font-black mb-0.5"
                style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}
              >
                {selected.name.toUpperCase()}
              </h2>
              <div className="text-xs tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: selected.accentColor }}>
                WAVES {selected.waves}
              </div>
            </div>

            <div className="h-px" style={{ background: `linear-gradient(to right, ${selected.accentColor}50, transparent)` }} />

            <p className="text-xs leading-relaxed flex-1" style={{ color: '#D0C6AB' }}>
              {selected.description}
            </p>

            <Panel variant="dim" cut={8} scanlines={false} corners={false}>
              <div className="p-3">
                <div className="text-[9px] tracking-[0.2em] mb-1" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                  REALM BOSS
                </div>
                {selected.bossImg ? (
                  <div className="flex items-center gap-3">
                    <img
                      src={selected.bossImg}
                      alt={selected.bossName}
                      className="w-10 h-10 object-contain"
                      style={{ filter: `drop-shadow(0 0 8px ${selected.accentColor}66)` }}
                      onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
                    />
                    <span className="text-sm font-semibold" style={{ color: '#FF6B72', fontFamily: '"Cinzel", serif' }}>
                      {selected.bossName}
                    </span>
                  </div>
                ) : (
                  <span className="text-sm font-semibold" style={{ color: '#FF6B72', fontFamily: '"Cinzel", serif' }}>
                    {selected.bossName}
                  </span>
                )}
              </div>
            </Panel>

            {status(selected.id) !== 'locked' && (
              <VedicButton
                variant={status(selected.id) === 'current' ? 'primary' : 'secondary'}
                onClick={() => onNavigate('ship-select')}
                fullWidth
              >
                {status(selected.id) === 'completed' ? 'REPLAY REALM' : 'ENTER REALM ▶'}
              </VedicButton>
            )}
          </div>
        </Panel>

        {/* Legend */}
        <Panel variant="dim" cut={8} scanlines={false} corners={false}>
          <div className="p-3 flex flex-col gap-1.5">
            {[
              { symbol: '✓', color: '#E9C400', label: 'Liberated' },
              { symbol: '◈', color: '#74F5FF', label: 'Current Realm' },
              { symbol: '⊘', color: '#8F98A8', label: 'Locked' },
            ].map(l => (
              <div key={l.label} className="flex items-center gap-2 text-[10px]" style={{ color: '#8F98A8' }}>
                <span style={{ color: l.color, width: 14 }}>{l.symbol}</span>
                {l.label}
              </div>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}
