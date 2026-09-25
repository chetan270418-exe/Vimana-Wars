import { useState } from 'react';
import StarField from '../components/StarField';
import NeonPanel from '../components/NeonPanel';

const TABS = ['1. REALMS', '2. VIMANAS', '3. ASURAS', '4. TITANS', '5. SYNERGIES'] as const;
type Tab = typeof TABS[number];

const TAB_COLORS = ['cyan', 'gold', 'red', 'orange', 'green'] as const;

const REALMS = [
  { name: 'Swarga Outpost', waves: '1–3', titan: 'None',
    lore: "Indra's orbital gate protecting the higher planes. Scouting waves test perimeter defenses.",
    tactic: 'High agility skiffs. Focus on keeping combos active.', color: '#4488AA' },
  { name: 'Kshira Sagara', waves: '4–7', titan: 'Sheshanaga Mk-II',
    lore: 'The celestial milk ocean. Enemy shields regenerate rapidly between assault waves.',
    tactic: 'Torpedo craft recommended. Sustain fire on shield cores.', color: '#44AACC' },
  { name: 'Dandaka Void', waves: '8–12', titan: 'Tataka Prime',
    lore: 'Deep space forbidden forest. Demon skirmishers spawn in coordinated formation swarms.',
    tactic: 'Area denial weapons excel here. Watch your flanks.', color: '#8844AA' },
  { name: 'Lanka Approach', waves: '13–18', titan: 'Ravana Aspect-I',
    lore: "Ravana's fortified staging ground. Multi-tier formations backed by siege artillery.",
    tactic: 'Heavy gunship loadout. Prioritize anti-armor ordnance.', color: '#AA4444' },
  { name: 'Setu Expanse', waves: '19–22', titan: 'Kumbhakarna Unit',
    lore: 'Bridge between mortal and demon realms. Bridgehead assault scenario. High pressure.',
    tactic: 'Balanced loadout. Maintain momentum through kill-zones.', color: '#AA8844' },
  { name: 'Naraka Forge', waves: '23–25', titan: 'Mahishasura',
    lore: "The demon weapon foundry at the abyss. Armored producer units spawn combat constructs.",
    tactic: 'Target producers first. Anti-construct ordnance mandatory.', color: '#884422' },
  { name: 'Mahayuddha Citadel', waves: '26–30', titan: 'Hiranyakashipu',
    lore: 'Throne of the Demon Sovereign. The immortal tyrant Hiranyakashipu commands the final bastion.',
    tactic: 'Peak loadout required. Fill all weapon slots. Bring all charged abilities.', color: '#FFB800' },
];

const VIMANAS_INFO = [
  { name: 'Pushpaka', type: 'Celestial Cruiser', tag: 'BALANCED', unlock: 'DEFAULT',
    desc: 'Multi-role combat platform. Sacred flying chariot of Kubera, repurposed for celestial warfare.' },
  { name: 'Garuda', type: 'Attack Fighter', tag: 'ASSAULT', unlock: 'WAVE 5',
    desc: "Apex predator of the cosmic battlefield. Modeled after Vishnu's divine eagle mount." },
  { name: 'Nandi', type: 'Heavy Gunship', tag: 'TANK', unlock: 'WAVE 10',
    desc: "Siege platform incarnate. Shiva's sacred bull reborn as an unmovable combat fortress." },
  { name: 'Hamsa', type: 'Scout Skiff', tag: 'AGILITY', unlock: 'WAVE 8',
    desc: "Brahma's divine swan — reconnaissance and lightning strike specialist. Fastest in the fleet." },
  { name: 'Airavata', type: 'Astral Bomber', tag: 'DEVASTATION', unlock: 'WAVE 15',
    desc: "Indra's celestial elephant reshaped into a payload carrier of apocalyptic destructive yield." },
];

const ASURAS_INFO = [
  { name: 'Daitya Grunt', tier: 'T1', threat: 'LOW', desc: 'Basic infantry. Fast, numerous, low armor. Coordinate swarm patterns.' },
  { name: 'Rakshasa Skirmisher', tier: 'T2', threat: 'MEDIUM', desc: 'Hit-and-run specialist. Cloaking module active at 50% health.' },
  { name: 'Asura Berserker', tier: 'T2', threat: 'HIGH', desc: 'Enrages below 30% health. All weapon systems overdrive.' },
  { name: 'Narakapala Sentinel', tier: 'T3', threat: 'ELITE', desc: 'Shield projector. Keeps nearby units protected. Priority target.' },
  { name: 'Danavendra Commander', tier: 'T4', threat: 'CRITICAL', desc: 'Field commander. Buffs surrounding units. Escape vector enabled.' },
];

const TITANS_INFO = [
  { name: 'Sheshanaga Mk-II', realm: 'Kshira Sagara', rank: 'GUARDIAN',
    desc: "The eternal serpent rearmed. Regenerating hull. Tail sweep clears entire lane." },
  { name: 'Tataka Prime', realm: 'Dandaka Void', rank: 'GUARDIAN',
    desc: "The forest demoness ascended. Summons Yaksha sub-units every 90 seconds." },
  { name: 'Ravana Aspect-I', realm: 'Lanka Approach', rank: 'WARLORD',
    desc: "First form of Ravana. Ten weapon systems, each requiring separate neutralization." },
  { name: 'Kumbhakarna Unit', realm: 'Setu Expanse', rank: 'COLOSSUS',
    desc: "Massive siege engine. Periodic sleep phase — exploit with sustained heavy fire." },
  { name: 'Mahishasura', realm: 'Naraka Forge', rank: 'DEMONLORD',
    desc: "The shape-shifter. Cycle through three combat forms per engagement phase." },
  { name: 'Hiranyakashipu', realm: 'Mahayuddha Citadel', rank: 'SOVEREIGN',
    desc: "Immortal Demon Sovereign. Reality Distortion makes projectile paths unpredictable." },
];

const SYNERGIES_INFO = [
  { combo: 'Garuda + Vajra + Pasha', type: 'ASSAULT CHAIN',
    desc: 'Maximum DPS burst window. Pasha stuns, Vajra exploits. Optimal for boss phases.' },
  { combo: 'Nandi + Brahmastra + Trishula', type: 'SIEGE PROTOCOL',
    desc: 'Sustained area denial. Brahmastra clears waves while Trishula pressures the titan.' },
  { combo: 'Hamsa + Vayu + Cakra', type: 'PHANTOM STRIKE',
    desc: 'Hit-and-run loop. Vayu grants invincibility frames. Loop indefinitely vs slow enemies.' },
  { combo: 'Pushpaka + Soma + Kavach', type: 'ENDURANCE FIELD',
    desc: 'Maximum survivability. Kavach absorbs, Soma regenerates. Viable for all sectors.' },
  { combo: 'Airavata + Mahameru + Pralaya', type: 'TOTAL ANNIHILATION',
    desc: 'Highest possible burst damage. Limited dash survivability — requires master timing.' },
];

interface AstralCodexProps {
  onBack: () => void;
}

export default function AstralCodex({ onBack }: AstralCodexProps) {
  const [tab, setTab] = useState<Tab>('1. REALMS');
  const [selectedIdx, setSelectedIdx] = useState(0);

  const tabIdx = TABS.indexOf(tab);

  const getItems = () => {
    if (tab === '1. REALMS')    return REALMS.map(r => r.name);
    if (tab === '2. VIMANAS')   return VIMANAS_INFO.map(v => v.name);
    if (tab === '3. ASURAS')    return ASURAS_INFO.map(a => a.name);
    if (tab === '4. TITANS')    return TITANS_INFO.map(t => t.name);
    if (tab === '5. SYNERGIES') return SYNERGIES_INFO.map(s => s.combo);
    return [];
  };

  const renderDetail = () => {
    if (tab === '1. REALMS') {
      const r = REALMS[selectedIdx];
      return (
        <div className="space-y-4">
          <div>
            <div className="font-display text-base tracking-widest mb-1" style={{ color: r.color }}>{r.name.toUpperCase()}</div>
            <div className="grid grid-cols-2 gap-2 mb-3">
              <div className="font-mono text-[9px] text-muted-foreground">OPERATIONAL SPAN: <span style={{ color: '#FFB800' }}>Waves {r.waves}</span></div>
              <div className="font-mono text-[9px] text-muted-foreground">TITAN GUARDIAN: <span style={{ color: '#FF6B00' }}>{r.titan}</span></div>
            </div>
          </div>
          <div>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1.5">SECTOR LORE ARCHIVE:</div>
            <div className="font-body text-sm leading-relaxed" style={{ color: '#8090A8' }}>{r.lore}</div>
          </div>
          <div>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1.5">TACTICAL RECOMMENDATION:</div>
            <div className="font-body text-sm" style={{ color: '#00FF88' }}>{r.tactic}</div>
          </div>
        </div>
      );
    }
    if (tab === '2. VIMANAS') {
      const v = VIMANAS_INFO[selectedIdx];
      return (
        <div className="space-y-4">
          <div>
            <div className="font-display text-base tracking-widest mb-0.5 glow-gold" style={{ color: '#FFB800' }}>{v.name.toUpperCase()}</div>
            <div className="flex gap-3 items-center">
              <span className="font-mono text-[9px]" style={{ color: '#00E5FF' }}>{v.type}</span>
              <span className="font-mono text-[8px] px-2 py-0.5" style={{ border: '1px solid #FF6B00', color: '#FF6B00' }}>{v.tag}</span>
            </div>
          </div>
          <div>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1.5">UNLOCK CONDITION: <span style={{ color: '#00FF88' }}>{v.unlock}</span></div>
            <div className="font-body text-sm leading-relaxed" style={{ color: '#8090A8' }}>{v.desc}</div>
          </div>
        </div>
      );
    }
    if (tab === '3. ASURAS') {
      const a = ASURAS_INFO[selectedIdx];
      const threatColor = { LOW: '#00FF88', MEDIUM: '#FFB800', HIGH: '#FF6B00', ELITE: '#FF2244', CRITICAL: '#FF0080' }[a.threat] || '#fff';
      return (
        <div className="space-y-4">
          <div>
            <div className="font-display text-base tracking-widest mb-0.5" style={{ color: '#FF4444' }}>{a.name.toUpperCase()}</div>
            <div className="flex gap-3">
              <span className="font-mono text-[9px] text-muted-foreground">TIER: <span style={{ color: '#FFB800' }}>{a.tier}</span></span>
              <span className="font-mono text-[9px] text-muted-foreground">THREAT: <span style={{ color: threatColor }}>{a.threat}</span></span>
            </div>
          </div>
          <div className="font-body text-sm leading-relaxed" style={{ color: '#8090A8' }}>{a.desc}</div>
        </div>
      );
    }
    if (tab === '4. TITANS') {
      const t = TITANS_INFO[selectedIdx];
      return (
        <div className="space-y-4">
          <div>
            <div className="font-display text-base tracking-widest mb-0.5 glow-orange" style={{ color: '#FF6B00' }}>{t.name.toUpperCase()}</div>
            <div className="flex gap-3">
              <span className="font-mono text-[9px] text-muted-foreground">REALM: <span style={{ color: '#00E5FF' }}>{t.realm}</span></span>
              <span className="font-mono text-[9px] text-muted-foreground">RANK: <span style={{ color: '#FF2244' }}>{t.rank}</span></span>
            </div>
          </div>
          <div className="font-body text-sm leading-relaxed" style={{ color: '#8090A8' }}>{t.desc}</div>
        </div>
      );
    }
    if (tab === '5. SYNERGIES') {
      const s = SYNERGIES_INFO[selectedIdx];
      return (
        <div className="space-y-4">
          <div>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1">SYNERGY TYPE: <span style={{ color: '#00FF88' }}>{s.type}</span></div>
            <div className="font-display text-sm tracking-wide glow-green" style={{ color: '#00FF88' }}>{s.combo}</div>
          </div>
          <div className="font-body text-sm leading-relaxed" style={{ color: '#8090A8' }}>{s.desc}</div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 80% 70% at 50% 40%, #070D1C 0%, #05080E 100%)' }}>
      <StarField count={100} />

      {/* Header */}
      <div className="absolute top-0 left-0 right-0 px-6 pt-5 pb-3 z-10">
        <div className="font-display text-sm tracking-widest glow-gold mb-1" style={{ color: '#FFB800' }}>
          ASTRAL CODEX // CELESTIAL REPOSITORY & BESTIARY
        </div>
        <div className="font-mono text-[8px] tracking-widest" style={{ color: '#4A6070' }}>
          STRATEGIC INTEL &nbsp;·&nbsp; ASURA THREAT ASSESSMENTS &nbsp;·&nbsp; DIVINE WEAPON BLUEPRINTS
        </div>
      </div>

      {/* Tabs */}
      <div className="absolute top-16 left-6 right-6 flex gap-2 z-10">
        {TABS.map((t, i) => (
          <NeonPanel key={t} color={TAB_COLORS[i]} hover corners={false}
            onClick={() => { setTab(t); setSelectedIdx(0); }}
            className={`flex-1 py-2 text-center transition-all ${tab === t ? 'bg-[rgba(255,255,255,0.05)]' : ''}`}>
            <span className="font-body text-xs font-semibold tracking-widest"
              style={{ color: tab === t ? '#fff' : 'var(--muted-foreground)' }}>
              {t}
            </span>
          </NeonPanel>
        ))}
      </div>

      {/* Content */}
      <div className="absolute inset-0 flex gap-4 px-6 pt-28 pb-16">
        {/* Left: list */}
        <NeonPanel color="white" className="w-52 overflow-y-auto">
          {getItems().map((item, i) => (
            <div key={i} onClick={() => setSelectedIdx(i)}
              className={`px-4 py-2.5 cursor-pointer transition-all font-body text-xs tracking-wide border-b
                hover:bg-[rgba(255,255,255,0.04)] ${selectedIdx === i ? 'bg-[rgba(255,184,0,0.06)]' : ''}`}
              style={{
                color: selectedIdx === i ? '#FFB800' : '#8090A8',
                borderColor: '#162030',
              }}>
              {item}
            </div>
          ))}
        </NeonPanel>

        {/* Right: detail */}
        <NeonPanel color={TAB_COLORS[tabIdx]} className="flex-1 p-6">
          {renderDetail()}
        </NeonPanel>
      </div>

      {/* Back button */}
      <div className="absolute bottom-5 left-6">
        <NeonPanel color="white" hover onClick={onBack} className="px-8 py-3" corners={false}>
          <span className="font-mono text-[10px] tracking-widest text-muted-foreground">&lt;&lt; MAIN MENU</span>
        </NeonPanel>
      </div>
    </div>
  );
}
