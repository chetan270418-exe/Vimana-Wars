import { useState } from 'react';
import { SHIPS, type Ship } from '../data/gameData';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StatBar from './ui/StatBar';
import StarField from './ui/StarField';
import { getProgression, isShipUnlocked, shipUnlockWave, unlockedShipCount } from '../lib/progression';

type Props = { onNavigate: (s: string) => void };

const STAT_COLORS: Record<string, string> = {
  speed: '#74F5FF',
  firepower: '#FF6B72',
  armor: '#E9C400',
  shield: '#7EA8FF',
  agility: '#40E090',
};

function ShipCard({ ship, selected, locked, onClick }: { ship: Ship; selected: boolean; locked: boolean; onClick: () => void }) {
  return (
    <Panel
      variant={selected ? 'selected' : 'default'}
      cut={8}
      onClick={onClick}
      className={`transition-transform duration-150 ${locked ? 'opacity-60' : 'hover:-translate-y-0.5'}`}
    >
      <div className="p-3 flex flex-col items-center gap-2">
        <img
          src={ship.img}
          alt={ship.name}
          className="w-14 h-14 object-contain"
          style={{
            filter: selected
              ? `drop-shadow(0 0 10px ${ship.color}88)`
              : locked ? 'brightness(0.35) saturate(0)' : 'brightness(0.7) saturate(0.7)',
          }}
          onError={e => { (e.target as HTMLImageElement).style.opacity = '0.3'; }}
        />
        <div className="text-center">
          <div
            className="text-xs tracking-[0.15em] font-semibold"
            style={{ fontFamily: '"Cinzel", serif', color: selected ? '#FFF6DF' : '#8F98A8' }}
          >
            {ship.name.toUpperCase()}
          </div>
          <div className="text-[9px] tracking-wider mt-0.5" style={{ color: ship.color, opacity: selected ? 1 : 0.5 }}>
            {locked ? `LOCKED · WAVE ${shipUnlockWave(ship.id)}` : ship.shipClass}
          </div>
        </div>
      </div>
    </Panel>
  );
}

export default function ShipSelect({ onNavigate }: Props) {
  const progression = getProgression();
  const [selected, setSelected] = useState<Ship>(SHIPS.find(ship => isShipUnlocked(ship.id, progression.lastWave)) ?? SHIPS[0]);

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />

      {/* header bar */}
      <div
        className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6"
        style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.8)', backdropFilter: 'blur(12px)' }}
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
          VIMANA ARMORY
        </span>
        <div className="ml-auto text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
          SELECT YOUR CRAFT
        </div>
      </div>

      {/* main content */}
      <div className="absolute inset-0 flex gap-5 z-10" style={{ top: 52, bottom: 40, padding: '20px 24px' }}>

        {/* Ship grid */}
        <div className="flex flex-col gap-3" style={{ width: 320 }}>
          <div className="text-[10px] tracking-[0.3em] mb-1" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
            {unlockedShipCount(progression.lastWave)} / {SHIPS.length} VIMANAS AVAILABLE
          </div>
          <div className="grid grid-cols-4 gap-2">
            {SHIPS.map(ship => (
              <ShipCard key={ship.id} ship={ship} locked={!isShipUnlocked(ship.id, progression.lastWave)} selected={selected.id === ship.id} onClick={() => { if (isShipUnlocked(ship.id, progression.lastWave)) setSelected(ship); }} />
            ))}
          </div>

          {/* Quick compare row */}
          <Panel variant="dim" cut={8} className="mt-2">
            <div className="p-3">
              <div className="text-[9px] tracking-[0.25em] mb-2" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>QUICK COMPARE</div>
              <div className="flex flex-col gap-1.5">
                {(Object.keys(STAT_COLORS) as string[]).map(stat => (
                  <StatBar
                    key={stat}
                    label={stat}
                    value={selected.stats[stat as keyof typeof selected.stats]}
                    color={STAT_COLORS[stat]}
                    animated
                  />
                ))}
              </div>
            </div>
          </Panel>
        </div>

        {/* Detail panel */}
        <div className="flex-1 flex flex-col gap-4">
          <Panel variant="selected" cut={14} className="flex-1">
            <div className="p-6 flex gap-6 h-full">
              {/* Ship art */}
              <div className="flex flex-col items-center justify-center" style={{ width: 220 }}>
                <div className="relative flex items-center justify-center" style={{ width: 200, height: 200 }}>
                  {/* Ambient glow ring */}
                  <div className="absolute rounded-full" style={{
                    width: 160, height: 160,
                    background: `radial-gradient(circle, ${selected.color}18 0%, transparent 70%)`,
                  }} />
                  <img
                    src={selected.img}
                    alt={selected.name}
                    className="object-contain relative z-10"
                    style={{
                      width: 150, height: 150,
                      filter: `drop-shadow(0 0 20px ${selected.color}55) drop-shadow(0 0 8px ${selected.color}88)`,
                      animation: 'float 4s ease-in-out infinite',
                    }}
                    onError={e => {
                      const t = e.target as HTMLImageElement;
                      t.style.display = 'none';
                    }}
                  />
                </div>
              </div>

              {/* Info */}
              <div className="flex-1 flex flex-col gap-4">
                <div>
                  <h1 className="text-3xl tracking-[0.18em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
                    {selected.name.toUpperCase()}
                  </h1>
                  <div className="h-px mt-2" style={{ background: `linear-gradient(to right, ${selected.color}60, transparent)` }} />
                </div>

                <p className="text-sm leading-relaxed" style={{ color: '#D0C6AB', fontFamily: '"Rajdhani", sans-serif' }}>
                  {selected.lore}
                </p>

                {/* Stats */}
                <div className="flex flex-col gap-2">
                  <div className="text-[10px] tracking-[0.3em] mb-1" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                    COMBAT TELEMETRY
                  </div>
                  {(Object.entries(selected.stats) as [string, number][]).map(([key, val]) => (
                    <StatBar key={key} label={key} value={val} color={STAT_COLORS[key] ?? '#E9C400'} animated />
                  ))}
                </div>

                {/* Loadout */}
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { label: 'PRIMARY WEAPON', value: selected.weapon },
                    { label: 'DIVINE ABILITY', value: selected.ability },
                  ].map(row => (
                    <Panel key={row.label} variant="dim" cut={6} scanlines={false} corners={false}>
                      <div className="p-3">
                        <div className="text-[9px] tracking-[0.2em] mb-1" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
                          {row.label}
                        </div>
                        <div className="text-sm font-semibold" style={{ color: '#FFF6DF' }}>{row.value}</div>
                      </div>
                    </Panel>
                  ))}
                </div>
              </div>
            </div>
          </Panel>

          {/* Deploy */}
          <div className="flex gap-3 justify-end">
            <VedicButton variant="ghost" onClick={() => onNavigate('realm-map')}>
              VIEW REALM MAP
            </VedicButton>
            <VedicButton variant="primary" onClick={() => onNavigate('boon-select')}>
              DEPLOY VIMANA ▶
            </VedicButton>
          </div>
        </div>
      </div>
    </div>
  );
}
