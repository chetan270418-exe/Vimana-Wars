import { useEffect, useState } from 'react';
import StarField from './ui/StarField';
import { getApiHealth } from '../lib/api';

const ASSET = 'https://raw.githubusercontent.com/chetan270418-exe/Vimana-Wars/main/assets/images/';

const NAV = [
  { label: 'PLAY CAMPAIGN',    screen: 'ship-select', primary: true,  desc: 'Launch a new run' },
  { label: 'ARMORY',           screen: 'ship-select', primary: false, desc: 'Browse all Vimanas' },
  { label: 'REALM MAP',        screen: 'realm-map',   primary: false, desc: '7 realms · 20 waves' },
  { label: 'SANGHA NETWORK',   screen: 'sangha',      primary: false, desc: '1v1 rooms · matchmaking' },
  { label: 'PILOT ACCOUNT',    screen: 'account',     primary: false, desc: 'Game ID · cloud progress' },
  { label: 'SETTINGS',         screen: 'settings',    primary: false, desc: 'Audio · Display · Controls' },
  { label: 'CODEX',            screen: 'codex',       primary: false, desc: 'Enemy & lore archive' },
];

const ORBIT_DOTS = Array.from({ length: 8 }, (_, i) => {
  const angle = (i * 45) * Math.PI / 180;
  return { i, cx: Math.cos(angle), cy: Math.sin(angle), gold: i % 2 === 0 };
});

type Props = { onNavigate: (s: string) => void };

export default function MainMenu({ onNavigate }: Props) {
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    getApiHealth(controller.signal)
      .then(payload => setApiOnline(payload.status === 'online'))
      .catch(() => setApiOnline(false));
    return () => controller.abort();
  }, []);

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />

      {/* Vertical gold accent line */}
      <div
        className="absolute top-0 bottom-0 pointer-events-none"
        style={{ left: '40%', width: 1, background: 'linear-gradient(to bottom, transparent, rgba(233,196,0,0.2) 30%, rgba(233,196,0,0.2) 70%, transparent)' }}
      />

      {/* LEFT COLUMN */}
      <div className="absolute top-0 left-0 bottom-0 w-2/5 flex flex-col z-10" style={{ padding: '40px 32px 56px' }}>
        {/* Logo */}
        <div className="mb-8">
          <img
            src={`${ASSET}vimana_wars_logo.png`}
            alt="Vimana Wars"
            className="w-60 object-contain"
            style={{ filter: 'drop-shadow(0 0 22px rgba(233,196,0,0.5)) drop-shadow(0 0 6px rgba(233,196,0,0.8))' }}
            onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
          />
          <div
            className="text-4xl font-black mt-1"
            style={{ fontFamily: '"Cinzel Decorative", serif', color: '#FFF6DF', letterSpacing: '0.1em', textShadow: '0 0 30px rgba(233,196,0,0.4)', display: 'none' }}
          >
            VIMANA WARS
          </div>
          <div className="flex items-center gap-2 mt-3">
            <div className="h-px flex-1" style={{ background: 'linear-gradient(to right, rgba(233,196,0,0.7), transparent)' }} />
            <span className="text-[10px] tracking-[0.35em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>VEDIC-PUNK · v2.0</span>
            <div className="h-px flex-1" style={{ background: 'linear-gradient(to left, rgba(233,196,0,0.7), transparent)' }} />
          </div>
        </div>

        {/* Nav */}
        <nav className="flex flex-col gap-1 flex-1">
          {NAV.map(item => (
            <button
              key={item.label}
              onClick={() => onNavigate(item.screen)}
              className="group flex items-center gap-4 py-3 pl-4 pr-3 text-left transition-all duration-200 hover:bg-white/[0.03]"
              style={{
                borderLeft: `2px solid ${item.primary ? '#E9C400' : 'rgba(233,196,0,0.18)'}`,
                transition: 'all 0.18s ease',
              }}
            >
              <div className="flex flex-col gap-0.5">
                <span
                  className="text-sm tracking-[0.22em] transition-colors duration-150 group-hover:text-gold-bright"
                  style={{ fontFamily: '"Cinzel", serif', color: item.primary ? '#FFF6DF' : '#D0C6AB' }}
                >
                  {item.label}
                </span>
                <span className="text-[10px] tracking-wider opacity-0 group-hover:opacity-100 transition-opacity duration-200" style={{ color: '#8F98A8' }}>
                  {item.desc}
                </span>
              </div>
              {item.primary && (
                <span className="ml-auto text-xs" style={{ color: '#E9C400' }}>▶</span>
              )}
            </button>
          ))}
        </nav>

        {/* Footer */}
        <div className="flex flex-col gap-1 mt-4">
          <div className="text-[10px] tracking-[0.25em]" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
            BUILD 20260916 · PYTHON ARCADE 3.x
          </div>
          <div className="text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: 'rgba(143,152,168,0.5)' }}>
            © 2026 CHETAN DEV · CC BY-SA 4.0
          </div>
        </div>
      </div>

      {/* RIGHT AREA — Hero Vimana */}
      <div className="absolute right-0 top-0 bottom-0 flex items-center justify-center z-10"
        style={{ left: '40%', paddingBottom: 40 }}>

        {/* Concentric orbital rings */}
        {[520, 390, 270].map((d, ri) => (
          <div
            key={d}
            className="absolute rounded-full pointer-events-none"
            style={{
              width: d, height: d,
              border: `1px ${ri === 1 ? 'dashed' : 'solid'} ${ri === 0 ? 'rgba(233,196,0,0.09)' : ri === 1 ? 'rgba(0,219,231,0.12)' : 'rgba(233,196,0,0.07)'}`,
              animation: `${ri % 2 === 0 ? 'rotate-ring' : 'counter-rotate'} ${30 + ri * 12}s linear infinite`,
            }}
          />
        ))}

        {/* Orbital dots at 220px radius */}
        {ORBIT_DOTS.map(({ i, cx, cy, gold }) => (
          <div
            key={i}
            className="absolute rounded-full pointer-events-none"
            style={{
              width: 6, height: 6,
              left: `calc(50% + ${cx * 195}px - 3px)`,
              top: `calc(50% + ${cy * 195}px - 3px)`,
              background: gold ? '#E9C400' : '#00DBE7',
              boxShadow: `0 0 8px ${gold ? '#E9C400' : '#00DBE7'}`,
              animation: `rotate-ring 30s linear ${i * -3.75}s infinite`,
            }}
          />
        ))}

        {/* Hero ship */}
        <img
          src={`${ASSET}hero_vimana_wars.png`}
          alt="Vimana Wars — hero ship"
          className="relative z-10 object-contain"
          style={{
            width: 'clamp(240px, 35vw, 420px)',
            filter: 'drop-shadow(0 0 32px rgba(0,219,231,0.38)) drop-shadow(0 0 60px rgba(233,196,0,0.18))',
            animation: 'float 4.5s ease-in-out infinite',
          }}
          onError={e => { (e.target as HTMLImageElement).style.display = 'none'; }}
        />

        {/* Radar crosshair */}
        <div className="absolute pointer-events-none" style={{ width: 100, height: 100 }}>
          <div className="absolute inset-0 rounded-full" style={{ border: '1px solid rgba(0,219,231,0.2)' }} />
          <div className="absolute top-1/2 left-0 right-0 h-px" style={{ background: 'rgba(0,219,231,0.2)' }} />
          <div className="absolute left-1/2 top-0 bottom-0 w-px" style={{ background: 'rgba(0,219,231,0.2)' }} />
        </div>
      </div>

      {/* Player chip top-right */}
      <div className="absolute top-5 right-6 z-20 flex items-center gap-3">
        <div className="text-right">
          <div className="text-[10px] tracking-[0.3em]" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>PILOT</div>
          <div className="text-sm tracking-widest" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>DHRUVA KRISHNA</div>
        </div>
        <div
          className="w-9 h-9 flex items-center justify-center text-xs font-bold"
          style={{
            background: 'rgba(20,26,40,0.9)',
            border: '1px solid rgba(233,196,0,0.35)',
            clipPath: 'polygon(6px 0%,calc(100% - 6px) 0%,100% 6px,100% calc(100% - 6px),calc(100% - 6px) 100%,6px 100%,0% calc(100% - 6px),0% 6px)',
            fontFamily: '"JetBrains Mono", monospace',
            color: '#E9C400',
          }}
        >
          12
        </div>
        <div className="text-[9px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: apiOnline === true ? '#40E090' : apiOnline === false ? '#FF6B72' : '#8F98A8' }}>
          {apiOnline === true ? '● API ONLINE' : apiOnline === false ? '● OFFLINE MODE' : '○ LINKING'}
        </div>
      </div>

      {/* Scrolling news ticker */}
      <div
        className="absolute bottom-10 left-0 right-0 overflow-hidden z-10"
        style={{ borderTop: '1px solid rgba(233,196,0,0.12)', borderBottom: '1px solid rgba(233,196,0,0.12)' }}
      >
        <div
          className="whitespace-nowrap py-1.5 text-[10px] tracking-[0.25em]"
          style={{
            fontFamily: '"JetBrains Mono", monospace',
            color: '#8F98A8',
            animation: 'none',
          }}
        >
          &nbsp;&nbsp;&nbsp;◈ WAVE RECORD: 20/20 — ARJUNA_PRIME &nbsp;&nbsp; ◈ PATCH 2.0: SOMA VIMANA ADDED &nbsp;&nbsp; ◈ REALM KSHIRA SAGARA REBALANCED &nbsp;&nbsp; ◈ MAHAYUDDHA CITADEL NOW ACCESSIBLE &nbsp;&nbsp; ◈ SANGHA NETWORK ONLINE &nbsp;&nbsp; ◈ NEW BOON: DARK TIME RIFT
        </div>
      </div>
    </div>
  );
}
