import StarField from './ui/StarField';

type Props = { onNavigate: (s: string) => void };

const ASSET = 'https://raw.githubusercontent.com/chetan270418-exe/Vimana-Wars/main/assets/images/';

function HBar({ value, max, color, label }: { value: number; max: number; color: string; label: string }) {
  const pct = (value / max) * 100;
  return (
    <div className="flex flex-col gap-1" style={{ width: 200 }}>
      <div className="flex justify-between text-[9px] tracking-[0.2em]" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
        <span>{label}</span>
        <span style={{ color }}>{value}/{max}</span>
      </div>
      <div className="h-2 relative" style={{ background: 'rgba(255,255,255,0.06)', clipPath: 'polygon(2px 0%,calc(100% - 2px) 0%,100% 2px,100% 100%,0% 100%,0% 2px)' }}>
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            background: `linear-gradient(to right, ${color}88, ${color})`,
            boxShadow: `0 0 8px ${color}66`,
            transition: 'width 0.3s ease',
          }}
        />
      </div>
    </div>
  );
}

export default function GameHUD({ onNavigate }: Props) {
  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#030408', paddingBottom: 40 }}>
      <StarField />

      {/* Simulated enemy ships scattered */}
      {[
        { x: 55, y: 20, size: 28, color: '#FF4646' },
        { x: 70, y: 35, size: 22, color: '#FF6B72' },
        { x: 45, y: 15, size: 18, color: '#FF4646' },
        { x: 75, y: 18, size: 32, color: '#FF6B72' },
        { x: 62, y: 28, size: 20, color: '#FF4646' },
      ].map((e, i) => (
        <div key={i} className="absolute" style={{ left: `${e.x}%`, top: `${e.y}%` }}>
          <img
            src={`${ASSET}asura_fast.png`}
            alt="enemy"
            style={{ width: e.size, height: e.size, filter: `hue-rotate(320deg) brightness(0.9) drop-shadow(0 0 4px ${e.color})`, opacity: 0.8 }}
            onError={e2 => { (e2.target as HTMLImageElement).style.display = 'none'; }}
          />
        </div>
      ))}

      {/* Player vimana center-bottom */}
      <div className="absolute z-10" style={{ left: '50%', bottom: 140, transform: 'translateX(-50%)' }}>
        <img
          src={`${ASSET}garuda.png`}
          alt="player ship"
          style={{
            width: 64, height: 64,
            filter: 'drop-shadow(0 0 12px rgba(0,219,231,0.6)) drop-shadow(0 0 6px rgba(116,245,255,0.8))',
          }}
          onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
        />
        {/* engine trail */}
        <div className="absolute left-1/2 -translate-x-1/2" style={{ top: 56, width: 6, height: 20, background: 'linear-gradient(to bottom, rgba(116,245,255,0.8), transparent)', filter: 'blur(2px)' }} />
      </div>

      {/* Wave announcement */}
      <div className="absolute inset-0 flex items-start justify-center z-20 pointer-events-none" style={{ top: '22%' }}>
        <div className="text-center" style={{ animation: 'wave-announce 3.5s ease forwards' }}>
          <div className="text-[10px] tracking-[0.5em] mb-1" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
            DANDAKA VOID
          </div>
          <div className="text-3xl tracking-[0.25em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF', textShadow: '0 0 30px rgba(233,196,0,0.6)' }}>
            WAVE 8 / 20
          </div>
          <div className="text-sm tracking-[0.3em] mt-1" style={{ color: '#E9C400' }}>
            ELITE ASURAS INCOMING
          </div>
        </div>
      </div>

      {/* === HUD OVERLAY === */}

      {/* Top-left: HP + Shield */}
      <div className="absolute top-4 left-4 z-20 flex flex-col gap-2">
        <div
          className="px-3 py-2 flex flex-col gap-2"
          style={{
            background: 'rgba(8,9,15,0.82)',
            border: '1px solid rgba(233,196,0,0.18)',
            clipPath: 'polygon(8px 0%,calc(100% - 8px) 0%,100% 8px,100% 100%,0% 100%,0% 8px)',
            backdropFilter: 'blur(8px)',
          }}
        >
          <div className="text-[9px] tracking-[0.3em] mb-0.5" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>
            GARUDA — PILOT: DHRUVA
          </div>
          <HBar value={72} max={100} color="#30C846" label="HULL" />
          <HBar value={45} max={100} color="#7EA8FF" label="SHIELD" />
        </div>
      </div>

      {/* Top-right: Score + Wave */}
      <div className="absolute top-4 right-4 z-20 text-right">
        <div
          className="px-4 py-2 inline-flex flex-col gap-1"
          style={{
            background: 'rgba(8,9,15,0.82)',
            border: '1px solid rgba(233,196,0,0.18)',
            clipPath: 'polygon(8px 0%,calc(100% - 8px) 0%,100% 8px,100% 100%,0% 100%,0% 8px)',
            backdropFilter: 'blur(8px)',
          }}
        >
          <div className="text-[9px] tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>SCORE</div>
          <div className="text-2xl font-black tracking-widest" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#E9C400', textShadow: '0 0 14px rgba(233,196,0,0.5)' }}>
            4,328,900
          </div>
          <div className="text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#74F5FF' }}>
            ×3.5 COMBO
          </div>
        </div>
      </div>

      {/* Bottom HUD bar */}
      <div
        className="absolute bottom-10 left-0 right-0 z-20 flex items-end gap-4 px-4 pb-3 pt-2"
        style={{
          background: 'linear-gradient(to top, rgba(8,9,15,0.95), rgba(8,9,15,0.6), transparent)',
        }}
      >
        {/* Weapon selector */}
        <div
          className="flex items-center gap-3 px-3 py-2"
          style={{
            background: 'rgba(8,9,15,0.85)',
            border: '1px solid rgba(233,196,0,0.2)',
            clipPath: 'polygon(6px 0%,calc(100% - 6px) 0%,100% 6px,100% 100%,0% 100%,0% 6px)',
          }}
        >
          <div className="w-6 h-6 flex items-center justify-center text-sm" style={{ color: '#E9C400' }}>⚡</div>
          <div>
            <div className="text-[9px] tracking-[0.2em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>PRIMARY</div>
            <div className="text-xs font-semibold" style={{ fontFamily: '"Rajdhani", sans-serif', color: '#FFF6DF' }}>Solar Lance Array</div>
          </div>
          <div className="ml-3 text-xs" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#74F5FF' }}>∞</div>
        </div>

        {/* Ability cooldown */}
        <div
          className="flex items-center gap-3 px-3 py-2"
          style={{
            background: 'rgba(8,9,15,0.85)',
            border: '1px solid rgba(0,219,231,0.2)',
            clipPath: 'polygon(6px 0%,calc(100% - 6px) 0%,100% 6px,100% 100%,0% 100%,0% 6px)',
          }}
        >
          <div className="w-6 h-6 flex items-center justify-center text-sm" style={{ color: '#74F5FF' }}>◎</div>
          <div>
            <div className="text-[9px] tracking-[0.2em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>ABILITY</div>
            <div className="text-xs font-semibold" style={{ fontFamily: '"Rajdhani", sans-serif', color: '#74F5FF' }}>Gale Dive — READY</div>
          </div>
        </div>

        {/* Minimap */}
        <div
          className="ml-auto flex-shrink-0"
          style={{
            width: 90, height: 70,
            background: 'rgba(8,9,15,0.9)',
            border: '1px solid rgba(0,219,231,0.2)',
            clipPath: 'polygon(6px 0%,calc(100% - 6px) 0%,100% 6px,100% 100%,0% 100%,0% 6px)',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          <div className="absolute inset-0 opacity-30" style={{ background: 'radial-gradient(circle at 50% 70%, rgba(0,219,231,0.3) 0%, transparent 60%)' }} />
          {/* Enemy dots */}
          {[[55,25],[70,18],[45,20],[62,15],[75,22]].map(([x,y],i) => (
            <div key={i} className="absolute w-1.5 h-1.5 rounded-full" style={{ left: `${x}%`, top: `${y}%`, background: '#FF4646', boxShadow: '0 0 4px #FF4646' }} />
          ))}
          {/* Player dot */}
          <div className="absolute w-2 h-2 rounded-full" style={{ left: 'calc(50% - 4px)', bottom: 16, background: '#74F5FF', boxShadow: '0 0 6px #74F5FF' }} />
          <div className="absolute bottom-0 left-0 right-0 text-center text-[8px] py-0.5" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8', background: 'rgba(8,9,15,0.7)' }}>
            RADAR
          </div>
        </div>
      </div>

      {/* Boss bar */}
      <div
        className="absolute left-4 right-4 z-20"
        style={{ bottom: 118, animation: 'boss-bar-in 0.5s ease 0.4s both' }}
      >
        <div
          className="px-4 py-2"
          style={{
            background: 'rgba(8,9,15,0.9)',
            border: '1px solid rgba(191,0,54,0.4)',
            clipPath: 'polygon(8px 0%,calc(100% - 8px) 0%,100% 8px,100% 100%,0% 100%,0% 8px)',
          }}
        >
          <div className="flex justify-between text-[9px] tracking-[0.25em] mb-1.5" style={{ fontFamily: '"Cinzel", serif' }}>
            <span style={{ color: '#FF6B72' }}>KUMBHAKARNA — PHASE I</span>
            <span style={{ color: '#8F98A8' }}>HP: 68,400 / 100,000</span>
          </div>
          <div className="h-3 relative" style={{ background: 'rgba(191,0,54,0.15)' }}>
            <div
              style={{
                width: '68.4%', height: '100%',
                background: 'linear-gradient(to right, #6B0020, #BF0036)',
                boxShadow: '0 0 12px rgba(191,0,54,0.5)',
              }}
            />
            {/* Phase marker */}
            <div className="absolute top-0 bottom-0 w-px" style={{ left: '50%', background: 'rgba(255,107,114,0.7)' }}>
              <div className="absolute -top-2 -left-1 text-[8px]" style={{ color: '#FF6B72' }}>II</div>
            </div>
          </div>
        </div>
      </div>

      {/* Back */}
      <button
        onClick={() => onNavigate('boon-select')}
        className="absolute top-4 left-1/2 -translate-x-1/2 z-30 text-[10px] tracking-[0.25em] px-4 py-1.5 transition-colors hover:text-gold"
        style={{
          fontFamily: '"Cinzel", serif',
          color: '#8F98A8',
          background: 'rgba(8,9,15,0.85)',
          border: '1px solid rgba(233,196,0,0.15)',
        }}
      >
        ← BACK TO BOON SELECT
      </button>
    </div>
  );
}
