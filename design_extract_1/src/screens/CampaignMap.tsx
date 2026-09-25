import { useState } from 'react';
import StarField from '../components/StarField';
import NeonPanel from '../components/NeonPanel';

const SECTORS = [
  {
    id: 1, name: 'Swarga Outpost', x: 82, y: 420, completed: true,
    waves: '1 – 3', titan: 'None',
    lore: "Indra's orbital gate protecting the higher planes. Scouting waves test perimeter defenses.",
    tactic: 'High agility skiffs. Focus on keeping combos active.',
    hazard: 'None',
  },
  {
    id: 2, name: 'Kshira Sagara', x: 210, y: 340, completed: true,
    waves: '4 – 7', titan: 'Sheshanaga Mk-II',
    lore: 'The celestial milk ocean between realms. Asura patrol units enforce blockade protocols.',
    tactic: 'Torpedo craft recommended. Enemy shields regenerate rapidly.',
    hazard: 'Astral Current — periodic velocity surges.',
  },
  {
    id: 3, name: 'Dandaka Void', x: 310, y: 390, completed: true,
    waves: '8 – 12', titan: 'Tataka Prime',
    lore: 'The forbidden forest expanse of deep space. Demon skirmishers spawn in formation waves.',
    tactic: 'Area denial weapons excel. Watch flanks.',
    hazard: 'Void Mist — sensor reduction 40%.',
  },
  {
    id: 4, name: 'Lanka Approach', x: 455, y: 295, completed: true,
    waves: '13 – 18', titan: 'Ravana Aspect-I',
    lore: 'Ravana\'s fortified staging ground. Multi-tier enemy formations backed by siege units.',
    tactic: 'Heavy gunship loadout advised. Prioritize anti-armor rounds.',
    hazard: 'Lanka Vortex — pull field near map center.',
  },
  {
    id: 5, name: 'Setu Expanse', x: 580, y: 345, completed: true,
    waves: '19 – 22', titan: 'Kumbhakarna Unit',
    lore: 'The bridge between the mortal and demon realms. Bridgehead assault scenario.',
    tactic: 'Balanced loadout. Maintain momentum through the kill-zones.',
    hazard: 'Plasma Bridge — periodic corridor hazards.',
  },
  {
    id: 6, name: 'Naraka Forge', x: 680, y: 270, completed: true,
    waves: '23 – 25', titan: 'Mahishasura',
    lore: "The demon weapon foundry at the abyss. Armored producer units spawn combat constructs.",
    tactic: 'Target producers first. Anti-construct ordnance mandatory.',
    hazard: 'Forge Eruptions — periodic area blasts.',
  },
  {
    id: 7, name: 'Mahayuddha Citadel', x: 795, y: 175, completed: false,
    waves: '26 – 30', titan: 'Hiranyakashipu',
    lore: 'Throne of the Demon Sovereign. The immortal tyrant Hiranyakashipu commands the final bastion.',
    tactic: 'Peak loadout required. All weapon slots should be filled.',
    hazard: 'Reality Distortion Field — unpredictable physics.',
    active: true,
  },
];

interface CampaignMapProps {
  onBack: () => void;
  onLaunch: () => void;
}

export default function CampaignMap({ onBack, onLaunch }: CampaignMapProps) {
  const [selected, setSelected] = useState(SECTORS[6]);

  const pathD = SECTORS.reduce((d, s, i) => {
    if (i === 0) return `M ${s.x} ${s.y}`;
    const prev = SECTORS[i - 1];
    const mx = (prev.x + s.x) / 2;
    return d + ` C ${mx} ${prev.y}, ${mx} ${s.y}, ${s.x} ${s.y}`;
  }, '');

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 100% 80% at 50% 50%, #060E22 0%, #05080E 100%)' }}>
      <StarField count={200} />

      {/* Header */}
      <div className="absolute top-0 left-0 right-0 px-6 pt-5 pb-4 z-10">
        <div className="font-display text-base tracking-widest glow-gold" style={{ color: '#FFB800' }}>
          MAHAYUDDHA CAMPAIGN MAP // REALM PROGRESSION
        </div>
        <div className="font-mono text-[9px] tracking-widest mt-1" style={{ color: '#00E5FF', opacity: 0.7 }}>
          SELECT SECTOR DESTINATION &nbsp;·&nbsp; HIGHEST CONQUERED WAVE: 25
        </div>
      </div>

      {/* SVG Map */}
      <svg className="absolute inset-0" width="100%" height="100%" style={{ top: 60 }}>
        <defs>
          <filter id="nodeGlow">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
          </filter>
        </defs>

        {/* Path line */}
        <path d={pathD} stroke="#FFB800" strokeWidth="1.5" fill="none" opacity="0.25"
          strokeDasharray="6 4"/>
        <path d={pathD} stroke="#00E5FF" strokeWidth="0.6" fill="none" opacity="0.15"/>

        {/* Waypoints on path */}
        {SECTORS.slice(0, -1).map((s, i) => {
          const next = SECTORS[i + 1];
          const mx = (s.x + next.x) / 2;
          const my = (s.y + next.y) / 2;
          return <circle key={`wp${i}`} cx={mx} cy={my} r="2" fill="#00E5FF" opacity="0.3"/>;
        })}

        {/* Nodes */}
        {SECTORS.map(sector => (
          <g key={sector.id} onClick={() => setSelected(sector)} style={{ cursor: 'pointer' }}>
            {/* Selection ring */}
            {selected.id === sector.id && (
              <>
                <circle cx={sector.x} cy={sector.y} r="28" stroke="#FFB800" strokeWidth="1"
                  fill="none" opacity="0.4"/>
                <circle cx={sector.x} cy={sector.y} r="28" stroke="#FFB800" strokeWidth="1"
                  fill="none" opacity="0.2" className="animate-pulse-glow"/>
              </>
            )}
            {/* Pulse ring for active */}
            {sector.active && (
              <circle cx={sector.x} cy={sector.y} r="22" stroke="#FFB800" strokeWidth="1.5"
                fill="none" opacity="0.3" className="animate-pulse-glow"/>
            )}
            {/* Node circle */}
            <circle cx={sector.x} cy={sector.y} r="18"
              fill={sector.active ? '#141A0A' : sector.completed ? '#0A1A1A' : '#0A0808'}
              stroke={sector.active ? '#FFB800' : sector.completed ? '#00E5FF' : '#3A4050'}
              strokeWidth={sector.active ? 2 : 1.5}
              filter="url(#nodeGlow)"/>
            {/* Check / number */}
            {sector.completed && !sector.active
              ? <text x={sector.x} y={sector.y + 5} textAnchor="middle" fill="#00FF88"
                  fontSize="14" fontFamily="Orbitron">✓</text>
              : <text x={sector.x} y={sector.y + 5} textAnchor="middle"
                  fill={sector.active ? '#FFB800' : '#405060'}
                  fontSize="12" fontFamily="Orbitron">{sector.id}</text>
            }
            {/* Label */}
            <text x={sector.x} y={sector.y + 32} textAnchor="middle"
              fill={sector.active ? '#FFB800' : '#405870'}
              fontSize="8" fontFamily="JetBrains Mono, monospace"
              letterSpacing="0.1em">
              {sector.name.toUpperCase()}
            </text>
          </g>
        ))}
      </svg>

      {/* Info panel - bottom */}
      <div className="absolute bottom-5 left-6 right-6 z-10">
        <div className="flex items-end gap-4">
          {/* Selected sector info */}
          <NeonPanel color={selected.active ? 'gold' : 'cyan'} className="flex-1 p-4" corners>
            <div className="font-display text-xs tracking-widest mb-3"
              style={{ color: selected.active ? '#FFB800' : '#00E5FF' }}>
              SECTOR {selected.id}: {selected.name.toUpperCase()}
            </div>
            <div className="grid grid-cols-3 gap-3 mb-3 text-[9px] font-mono tracking-widest">
              <div>
                <span className="text-muted-foreground">WAVES: </span>
                <span style={{ color: '#FFB800' }}>{selected.waves}</span>
              </div>
              <div>
                <span className="text-muted-foreground">TITAN: </span>
                <span style={{ color: '#FF6B00' }}>{selected.titan}</span>
              </div>
              {selected.hazard && selected.hazard !== 'None' && (
                <div>
                  <span className="text-muted-foreground">HAZARD: </span>
                  <span style={{ color: '#FF2244' }}>{selected.hazard}</span>
                </div>
              )}
            </div>
            <div className="font-body text-xs leading-relaxed mb-2" style={{ color: '#6A8090' }}>
              {selected.lore}
            </div>
            <div className="font-mono text-[9px]" style={{ color: '#00FF88' }}>
              TACTIC: {selected.tactic}
            </div>
          </NeonPanel>

          {/* Action buttons */}
          <div className="flex flex-col gap-2">
            <NeonPanel color="white" hover onClick={onBack} className="px-8 py-3" corners={false}>
              <span className="font-mono text-[10px] tracking-widest text-muted-foreground">
                &lt;&lt; MAIN MENU
              </span>
            </NeonPanel>
            <NeonPanel color="gold" hover onClick={selected.active ? onLaunch : undefined}
              className={`px-8 py-3 ${!selected.active ? 'opacity-40' : ''}`} corners={false}>
              <span className="font-mono text-[10px] tracking-widest"
                style={{ color: '#FFB800' }}>
                CONFIGURE LOADOUT &gt;&gt;
              </span>
            </NeonPanel>
          </div>
        </div>
      </div>
    </div>
  );
}
