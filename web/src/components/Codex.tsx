import { useMemo, useState } from 'react';
import { BOONS, REALMS, SHIPS } from '../data/gameData';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';

type Props = { onNavigate: (s: string) => void };
type Section = 'realms' | 'vimanas' | 'astras';

const TABS: Array<{ id: Section; label: string }> = [
  { id: 'realms', label: 'REALMS' },
  { id: 'vimanas', label: 'VIMANAS' },
  { id: 'astras', label: 'ASTRAS' },
];

export default function Codex({ onNavigate }: Props) {
  const [section, setSection] = useState<Section>('realms');
  const [selected, setSelected] = useState(0);

  const records = useMemo(() => {
    if (section === 'vimanas') return SHIPS.map(ship => ({ id: ship.id, title: ship.name, subtitle: ship.shipClass, body: ship.lore, accent: ship.color, detail: ship.ability }));
    if (section === 'astras') return BOONS.map(boon => ({ id: boon.id, title: boon.name, subtitle: boon.deity, body: boon.description, accent: boon.color, detail: boon.effect }));
    return REALMS.map(realm => ({ id: realm.id, title: realm.name, subtitle: `WAVES ${realm.waves} · ${realm.bossName}`, body: realm.description, accent: realm.accentColor, detail: 'ARCHIVE RECORD // CAMPAIGN ROUTE' }));
  }, [section]);

  const current = records[Math.min(selected, records.length - 1)];
  const changeSection = (next: Section) => { setSection(next); setSelected(0); };

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />
      <div className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6" style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.85)', backdropFilter: 'blur(12px)' }}>
        <button onClick={() => onNavigate('main-menu')} className="text-[10px] tracking-[0.25em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>← MAIN MENU</button>
        <div className="h-4 w-px" style={{ background: 'rgba(233,196,0,0.2)' }} />
        <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>AKASHIC CODEX</span>
      </div>
      <div className="absolute inset-0 z-10 flex gap-4" style={{ top: 52, bottom: 40, padding: '20px 24px' }}>
        <Panel variant="default" cut={12} className="shrink-0" style={{ width: 270 }}>
          <div className="p-4 h-full flex flex-col">
            <div className="text-[9px] tracking-[0.3em] mb-3" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>ARCHIVE INDEX</div>
            <div className="flex gap-1 mb-4">
              {TABS.map(tab => <button key={tab.id} onClick={() => changeSection(tab.id)} className="px-2 py-1 text-[9px] tracking-wider" style={{ color: section === tab.id ? '#FFF6DF' : '#8F98A8', background: section === tab.id ? 'rgba(233,196,0,0.14)' : 'transparent', border: `1px solid ${section === tab.id ? 'rgba(233,196,0,0.42)' : 'rgba(143,152,168,0.18)'}` }}>{tab.label}</button>)}
            </div>
            <div className="flex flex-col gap-1 overflow-y-auto">
              {records.map((record, index) => <button key={record.id} onClick={() => setSelected(index)} className="text-left px-3 py-2 transition-colors" style={{ borderLeft: `2px solid ${index === selected ? record.accent : 'rgba(143,152,168,0.18)'}`, background: index === selected ? 'rgba(233,196,0,0.08)' : 'transparent' }}><div className="text-xs tracking-wider" style={{ fontFamily: '"Cinzel", serif', color: index === selected ? '#FFF6DF' : '#D0C6AB' }}>{record.title}</div><div className="text-[9px] tracking-wider mt-1" style={{ color: record.accent, opacity: index === selected ? 1 : 0.6 }}>{record.subtitle}</div></button>)}
            </div>
          </div>
        </Panel>
        <Panel variant="active" cut={14} className="flex-1" style={{ minWidth: 0 }}>
          <div className="p-8 h-full flex flex-col justify-center max-w-3xl">
            <div className="text-[10px] tracking-[0.35em] mb-3" style={{ fontFamily: '"JetBrains Mono", monospace', color: current.accent }}>{current.subtitle}</div>
            <h1 className="text-4xl tracking-[0.12em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF', textShadow: `0 0 22px ${current.accent}55` }}>{current.title.toUpperCase()}</h1>
            <div className="h-px w-full mt-4 mb-6" style={{ background: `linear-gradient(to right, ${current.accent}99, transparent)` }} />
            <p className="text-lg leading-relaxed max-w-2xl" style={{ color: '#D0C6AB' }}>{current.body}</p>
            <Panel variant="dim" cut={8} className="mt-8 max-w-xl" scanlines={false}><div className="p-4"><div className="text-[9px] tracking-[0.3em] mb-2" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>TACTICAL NOTE</div><div className="text-sm tracking-wider" style={{ color: current.accent }}>{current.detail}</div></div></Panel>
            <div className="mt-8"><VedicButton variant="ghost" onClick={() => onNavigate('realm-map')}>OPEN CAMPAIGN MAP</VedicButton></div>
          </div>
        </Panel>
      </div>
    </div>
  );
}
