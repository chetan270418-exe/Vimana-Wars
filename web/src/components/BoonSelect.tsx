import { useState } from 'react';
import { BOONS } from '../data/gameData';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';

const WAVE_BOONS = [BOONS[0], BOONS[2], BOONS[4]];

type Props = {
  onNavigate: (s: string) => void;
  currentWave?: number;
  onClaimBoon?: (boonId: string) => void;
};

export default function BoonSelect({ onNavigate, currentWave = 1, onClaimBoon }: Props) {
  const [selected, setSelected] = useState<string | null>(null);

  return (
    <div className="relative w-full h-full overflow-hidden flex flex-col items-center justify-center" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />

      {/* Vignette */}
      <div className="absolute inset-0 pointer-events-none" style={{
        background: 'radial-gradient(ellipse 70% 80% at 50% 50%, transparent 40%, rgba(8,9,15,0.7) 100%)',
      }} />

      {/* Header */}
      <div className="relative z-10 text-center mb-8" style={{ animation: 'fade-in 0.6s ease' }}>
        <div className="text-[10px] tracking-[0.4em] mb-2" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
          WAVE {currentWave} COMPLETE · DANDAKA VOID
        </div>
        <h1 className="text-3xl tracking-[0.22em] font-black mb-2" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
          CHOOSE YOUR DIVINE BOON
        </h1>
        <div className="flex items-center gap-3 justify-center">
          <div className="h-px w-24" style={{ background: 'linear-gradient(to right, transparent, rgba(233,196,0,0.6))' }} />
          <span className="text-xs tracking-widest" style={{ color: '#E9C400', fontFamily: '"Cinzel", serif' }}>
            THE DEVAS OFFER THREE GIFTS
          </span>
          <div className="h-px w-24" style={{ background: 'linear-gradient(to left, transparent, rgba(233,196,0,0.6))' }} />
        </div>
      </div>

      {/* Boon cards */}
      <div className="relative z-10 flex gap-5 px-8" style={{ animation: 'slide-in-up 0.5s ease 0.2s both', maxWidth: 900, width: '100%' }}>
        {WAVE_BOONS.map((boon, idx) => {
          const isSelected = selected === boon.id;
          return (
            <Panel
              key={boon.id}
              variant={isSelected ? 'selected' : 'default'}
              cut={14}
              className="flex-1 transition-transform duration-200 hover:-translate-y-1"
              onClick={() => setSelected(boon.id)}
              style={{ animationDelay: `${idx * 0.1}s` }}
            >
              <div className="p-6 flex flex-col items-center text-center gap-4 h-full" style={{ minHeight: 360 }}>
                {/* Deity */}
                <div
                  className="text-[9px] tracking-[0.4em]"
                  style={{ fontFamily: '"Cinzel", serif', color: boon.color }}
                >
                  {boon.deity}
                </div>

                {/* Symbol */}
                <div
                  className="text-5xl"
                  style={{
                    color: boon.color,
                    filter: `drop-shadow(0 0 12px ${boon.color}88)`,
                    animation: isSelected ? 'float-slow 3s ease-in-out infinite' : undefined,
                  }}
                >
                  {boon.symbol}
                </div>

                {/* Divider */}
                <div className="w-full flex items-center gap-2">
                  <div className="flex-1 h-px" style={{ background: `${boon.color}40` }} />
                  <div className="w-1 h-1 rotate-45" style={{ background: boon.color }} />
                  <div className="flex-1 h-px" style={{ background: `${boon.color}40` }} />
                </div>

                {/* Name */}
                <div>
                  <h2
                    className="text-base tracking-[0.15em] font-bold mb-2"
                    style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}
                  >
                    {boon.name}
                  </h2>
                  <p className="text-sm leading-relaxed" style={{ color: '#D0C6AB', fontFamily: '"Rajdhani", sans-serif' }}>
                    {boon.description}
                  </p>
                </div>

                {/* Effect badge */}
                <div
                  className="mt-auto px-4 py-2 text-xs tracking-wider text-center"
                  style={{
                    fontFamily: '"JetBrains Mono", monospace',
                    color: boon.color,
                    background: `${boon.color}12`,
                    border: `1px solid ${boon.color}40`,
                    clipPath: 'polygon(6px 0%,calc(100% - 6px) 0%,100% 6px,100% calc(100% - 6px),calc(100% - 6px) 100%,6px 100%,0% calc(100% - 6px),0% 6px)',
                    width: '100%',
                  }}
                >
                  {boon.effect}
                </div>

                {isSelected && (
                  <div className="text-[10px] tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#E9C400' }}>
                    ◈ SELECTED
                  </div>
                )}
              </div>
            </Panel>
          );
        })}
      </div>

      {/* Accept */}
      <div className="relative z-10 mt-8 flex gap-4" style={{ animation: 'fade-in 0.5s ease 0.5s both' }}>
        <VedicButton variant="ghost" onClick={() => onNavigate('ship-select')}>
          ← RETURN
        </VedicButton>
        <VedicButton
          variant="primary"
          disabled={!selected}
          onClick={() => {
            if (selected && onClaimBoon) onClaimBoon(selected);
            onNavigate('game-hud');
          }}
        >
          ACCEPT BOON · CONTINUE ▶
        </VedicButton>
      </div>

      {selected === null && (
        <p className="relative z-10 mt-3 text-xs tracking-wider" style={{ color: '#8F98A8' }}>
          Choose one boon to continue
        </p>
      )}
    </div>
  );
}
