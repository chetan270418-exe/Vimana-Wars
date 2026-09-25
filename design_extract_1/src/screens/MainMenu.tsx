import { useState } from 'react';
import StarField from '../components/StarField';
import MandalaEmblem from '../components/MandalaEmblem';
import NeonPanel from '../components/NeonPanel';
import PilotDossierModal from '../components/PilotDossierModal';

type NavColor = 'cyan' | 'gold' | 'orange' | 'magenta' | 'green' | 'white';

const MENU_ITEMS: { label: string; key: string; color: NavColor; shortcut: string }[] = [
  { label: 'ENTER CAMPAIGN (MAHAYUDDHA)', key: 'campaign-map',      color: 'cyan',    shortcut: '1' },
  { label: 'VIMANA HANGAR & SHIPS',       key: 'vimana-hangar',     color: 'gold',    shortcut: '2' },
  { label: 'PILOT DOSSIER & PROFILE',     key: 'dossier',           color: 'gold',    shortcut: '3' },
  { label: 'ASTRAL CODEX & BESTIARY',     key: 'astral-codex',      color: 'orange',  shortcut: '4' },
  { label: 'DUEL & SIMULATOR',            key: 'duel',              color: 'magenta', shortcut: '5' },
  { label: 'SQUADRON MULTIPLAYER',        key: 'squadron',          color: 'magenta', shortcut: '6' },
  { label: 'HALL OF VALOR (RANKS)',       key: 'hall',              color: 'green',   shortcut: '7' },
  { label: 'SYSTEM SETTINGS',             key: 'settings',           color: 'white',   shortcut: '8' },
  { label: 'SIGN IN / CREATE GAME ID',    key: 'sign-in',           color: 'green',   shortcut: '9' },
];

interface MainMenuProps {
  onNavigate: (screen: string) => void;
}

export default function MainMenu({ onNavigate }: MainMenuProps) {
  const [dossierOpen, setDossierOpen] = useState(false);
  const [hovered, setHovered] = useState<string | null>(null);

  const handleNav = (key: string) => {
    if (key === 'dossier') { setDossierOpen(true); return; }
    if (key === 'duel' || key === 'hall') return;
    onNavigate(key);
  };

  return (
    <div className="relative w-full h-full overflow-hidden scanline-overlay"
      style={{ background: 'radial-gradient(ellipse 90% 80% at 30% 40%, #08122A 0%, #05080E 100%)' }}>
      <StarField count={180} />

      {/* Corner decorations */}
      {[['top-3 left-3', 'top', 'left'], ['top-3 right-3', 'top', 'right'],
        ['bottom-3 left-3', 'bottom', 'left'], ['bottom-3 right-3', 'bottom', 'right']].map(([pos], i) => (
        <div key={i} className={`absolute ${pos} w-6 h-6 pointer-events-none`}
          style={{
            borderTop: i < 2 ? '1px solid rgba(255,184,0,0.3)' : 'none',
            borderBottom: i >= 2 ? '1px solid rgba(255,184,0,0.3)' : 'none',
            borderLeft: (i === 0 || i === 2) ? '1px solid rgba(255,184,0,0.3)' : 'none',
            borderRight: (i === 1 || i === 3) ? '1px solid rgba(255,184,0,0.3)' : 'none',
          }}/>
      ))}

      {/* Pilot ID card - top right */}
      <div className="absolute top-4 right-6 z-10 w-64 animate-slide-right">
        <NeonPanel color="gold" hover onClick={() => setDossierOpen(true)} className="p-3">
          <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1">
            PILOT IDENTIFICATION RECORD (CLICK FOR DOSSIER)
          </div>
          <div className="font-display text-[10px]" style={{ color: '#FFB800' }}>VMN-7517-A969 // WARRIOR</div>
          <div className="font-mono text-[9px] mt-1 animate-blink" style={{ color: '#00FF88' }}>
            [P LOCAL GUEST // OFFLINE]
          </div>
        </NeonPanel>
      </div>

      {/* Left column - logo + nav */}
      <div className="absolute left-6 top-0 bottom-0 flex flex-col justify-center" style={{ width: 380 }}>
        {/* Logo area */}
        <div className="flex items-center gap-4 mb-6 animate-slide-left">
          <div className="relative shrink-0">
            <div className="animate-rotate-slow absolute inset-0" style={{ width: 90, height: 90 }}>
              <MandalaEmblem size={90} />
            </div>
            <div style={{ width: 90, height: 90 }}/>
          </div>
          <div>
            <div className="font-display glow-gold" style={{ fontSize: 22, color: '#FFB800', letterSpacing: '0.15em' }}>
              vimana WARS
            </div>
            <div className="font-mono text-[7px] tracking-[0.3em] mt-1" style={{ color: '#00E5FF', opacity: 0.6 }}>
              CELESTIAL ASTRAL COMBAT // THE 7 REALMS OF MAHAYUDDHA
            </div>
          </div>
        </div>

        {/* Navigation */}
        <div className="space-y-1.5 animate-fade-up">
          {MENU_ITEMS.map((item, i) => {
            const isDisabled = item.key === 'duel' || item.key === 'hall';
            return (
              <NeonPanel
                key={item.key}
                color={isDisabled ? 'white' : item.color}
                hover={!isDisabled}
                dim={isDisabled}
                onClick={() => !isDisabled && handleNav(item.key)}
                className="px-4 py-2.5"
                corners={false}
              >
                <div className="flex items-center justify-between">
                  <span className="font-body font-semibold text-sm tracking-widest uppercase"
                    style={{ color: hovered === item.key ? '#fff' : 'var(--foreground)' }}
                    onMouseEnter={() => setHovered(item.key)}
                    onMouseLeave={() => setHovered(null)}>
                    {i + 1}. {item.label}
                  </span>
                  {isDisabled
                    ? <span className="font-mono text-[8px] tracking-wider" style={{ color: '#405060' }}>LOCKED</span>
                    : <span className="font-mono text-[9px] opacity-40">[{item.shortcut}]</span>
                  }
                </div>
              </NeonPanel>
            );
          })}
        </div>
      </div>

      {/* Right column - Command Telemetry */}
      <div className="absolute right-6 top-0 bottom-0 flex flex-col justify-center" style={{ width: 380, paddingTop: 60 }}>
        <NeonPanel color="gold" title="COMMAND TELEMETRY // SECTOR STATUS" className="p-4 space-y-3 animate-slide-right">
          {/* Current mission */}
          <NeonPanel color="white" className="p-3" corners={false}>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1">
              CAMPAIGN EXPEDITION MILESTONE
            </div>
            <div className="flex items-center gap-3">
              <div className="flex-1">
                <div className="font-body text-base font-semibold" style={{ color: '#C0D0E0' }}>
                  WAVE 26 / 30
                </div>
                <div className="h-1 mt-1 bg-muted overflow-hidden">
                  <div className="h-full" style={{ width: '86%', background: '#FFB800', boxShadow: '0 0 6px #FFB800' }}/>
                </div>
              </div>
              {/* Ship icon */}
              <svg viewBox="0 0 60 80" width="40" height="54" fill="none">
                <path d="M30 5 L8 55 L22 55 L30 18 Z" fill="#B31C1C" opacity="0.8"/>
                <path d="M30 5 L52 55 L38 55 L30 18 Z" fill="#B31C1C" opacity="0.8"/>
                <path d="M24 3 L36 3 L40 72 L20 72 Z" fill="#C0C8D8"/>
                <ellipse cx="30" cy="18" rx="7" ry="12" fill="#2860A8" opacity="0.8"/>
              </svg>
            </div>
          </NeonPanel>

          {/* Fleet status */}
          <NeonPanel color="white" className="p-3" corners={false}>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1">
              VIMANA FLEET COMMISSIONED
            </div>
            <div className="flex items-center justify-between">
              <div className="font-body text-base font-semibold" style={{ color: '#00E5FF' }}>
                42 / 52 VIMANAS COMBAT READY
              </div>
            </div>
            <div className="h-1 mt-2 bg-muted overflow-hidden">
              <div className="h-full" style={{ width: '80%', background: '#00E5FF', boxShadow: '0 0 6px #00E5FF' }}/>
            </div>
          </NeonPanel>

          {/* Currency */}
          <NeonPanel color="white" className="p-3" corners={false}>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1">
              ASTRAL PRANA CURRENCY & RECORD
            </div>
            <div className="flex items-center justify-between">
              <div className="font-body text-base font-semibold" style={{ color: '#FF6B00' }}>
                33,644 PRANA SHARDS
              </div>
              <div className="font-mono text-[9px]" style={{ color: '#FFB800' }}>
                HIGH: 6,110,580
              </div>
            </div>
          </NeonPanel>

          {/* Sector detail */}
          <NeonPanel color="cyan" className="p-3" corners={false}>
            <div className="font-mono text-[8px] tracking-widest mb-2" style={{ color: '#00E5FF', opacity: 0.7 }}>
              ACTIVE SECTOR // MAHAYUDDHA CITADEL
            </div>
            <div className="font-body text-xs leading-relaxed" style={{ color: '#8090A8' }}>
              Throne of the Demon Sovereign. Confront the immortal tyrant Hiranyakashipu.
              Reality Distortion Field active. Titan Guardian: HIRANYAKASHIPU.
            </div>
          </NeonPanel>

          {/* Status bar */}
          <div className="font-mono text-[8px] tracking-widest text-muted-foreground text-center pt-1">
            PRESS [1-9] NAVIGATE &nbsp;·&nbsp; [P] PILOT CARD DOSSIER &nbsp;·&nbsp; 60 FPS NATIVE
          </div>
        </NeonPanel>

        {/* Bottom tech footer */}
        <div className="mt-4 text-center font-mono text-[8px] tracking-[0.2em] text-muted-foreground">
          VIMANA WARS // NATIVE C++20 ENGINE / ADVANCED BSA / WINSOCK2 UDP LAN NETWORKING
        </div>
      </div>

      {dossierOpen && <PilotDossierModal onClose={() => setDossierOpen(false)} />}
    </div>
  );
}
