import { useEffect, useMemo, useState } from 'react';
import Panel from './ui/Panel';
import StarField from './ui/StarField';
import { getAchievements, getProfile, type Achievement } from '../lib/api';

type Props = { onNavigate: (screen: string) => void };

const LOCAL_ACHIEVEMENTS_KEY = 'vimana-local-achievements';

function readLocalUnlocks(): string[] {
  try {
    const value = JSON.parse(window.localStorage.getItem(LOCAL_ACHIEVEMENTS_KEY) || '[]');
    return Array.isArray(value) ? value.filter(item => typeof item === 'string') : [];
  } catch {
    return [];
  }
}

export default function Achievements({ onNavigate }: Props) {
  const [catalog, setCatalog] = useState<Achievement[]>([]);
  const [unlocked, setUnlocked] = useState<string[]>(readLocalUnlocks);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const controller = new AbortController();
    void Promise.all([getAchievements(), getProfile().catch(() => null)])
      .then(([remote, profile]) => {
        const profileAchievements = profile?.profile?.achievements;
        const merged = new Set(unlocked);
        remote.unlocked.forEach(id => merged.add(id));
        if (Array.isArray(profileAchievements)) {
          profileAchievements.filter(id => typeof id === 'string').forEach(id => merged.add(id));
        }
        const mergedIds = [...merged];
        setCatalog(remote.achievements);
        setUnlocked(mergedIds);
        window.localStorage.setItem(LOCAL_ACHIEVEMENTS_KEY, JSON.stringify(mergedIds));
      })
      .catch((cause: unknown) => {
        if (!controller.signal.aborted) setError(cause instanceof Error ? cause.message : 'Achievement link unavailable');
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, []);

  const groups = useMemo(() => {
    const grouped = new Map<string, Achievement[]>();
    catalog.forEach(item => {
      const list = grouped.get(item.category) || [];
      list.push(item);
      grouped.set(item.category, list);
    });
    return [...grouped.entries()];
  }, [catalog]);

  const unlockedCount = catalog.filter(item => unlocked.includes(item.id)).length;

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />
      <div className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6" style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.88)' }}>
        <button onClick={() => onNavigate('main-menu')} className="text-[10px] tracking-[0.25em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>← MAIN MENU</button>
        <div className="h-4 w-px" style={{ background: 'rgba(233,196,0,0.2)' }} />
        <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>ACHIEVEMENTS GALLERY</span>
        <span className="ml-auto text-[10px] tracking-[0.18em]" style={{ color: '#E9C400', fontFamily: '"JetBrains Mono", monospace' }}>{unlockedCount}/{catalog.length || '—'} UNLOCKED</span>
      </div>

      <div className="absolute inset-0 z-10 overflow-y-auto" style={{ top: 52, bottom: 40, padding: '24px 28px 40px' }}>
        <Panel variant="default" cut={14}>
          <div className="p-6">
            <div className="flex items-end justify-between mb-6">
              <div>
                <div className="text-[9px] tracking-[0.4em]" style={{ color: '#8F98A8', fontFamily: '"Cinzel", serif' }}>THE HALL OF VALOR</div>
                <h1 className="text-2xl tracking-[0.14em] mt-2" style={{ color: '#FFF6DF', fontFamily: '"Cinzel Decorative", serif' }}>PILOT RECORD</h1>
              </div>
              {error && <div className="text-[10px] tracking-wider text-right" style={{ color: '#FF6B72' }}>OFFLINE CACHE · {error}</div>}
            </div>

            {loading && <div className="py-16 text-center text-xs tracking-[0.25em]" style={{ color: '#8F98A8' }}>SYNCING TROPHY ARCHIVE…</div>}
            {!loading && !catalog.length && <div className="py-16 text-center text-xs tracking-[0.25em]" style={{ color: '#8F98A8' }}>NO TROPHIES RECEIVED — CHECK THE API LINK</div>}
            {!loading && groups.map(([category, items]) => (
              <section key={category} className="mb-7">
                <div className="text-[9px] tracking-[0.35em] mb-3" style={{ color: '#00DBE7', fontFamily: '"Cinzel", serif' }}>{category.toUpperCase()}</div>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3">
                  {items.map(item => {
                    const isUnlocked = unlocked.includes(item.id);
                    return (
                      <div key={item.id} className="flex gap-3 p-4 transition-all" style={{ border: `1px solid ${isUnlocked ? 'rgba(233,196,0,0.45)' : 'rgba(143,152,168,0.16)'}`, background: isUnlocked ? 'rgba(233,196,0,0.07)' : 'rgba(255,255,255,0.015)', opacity: isUnlocked ? 1 : 0.62 }}>
                        <div className="w-11 h-11 flex items-center justify-center text-xl shrink-0" style={{ background: isUnlocked ? 'rgba(233,196,0,0.14)' : 'rgba(143,152,168,0.08)', filter: isUnlocked ? 'none' : 'grayscale(1)' }}>{isUnlocked ? item.icon : '◈'}</div>
                        <div className="min-w-0">
                          <div className="text-xs tracking-[0.14em]" style={{ color: isUnlocked ? '#FFF6DF' : '#8F98A8', fontFamily: '"Cinzel", serif' }}>{item.name}</div>
                          <div className="text-[10px] mt-1 leading-relaxed" style={{ color: '#8F98A8' }}>{item.description}</div>
                          <div className="text-[9px] tracking-[0.2em] mt-2" style={{ color: isUnlocked ? '#E9C400' : '#687080' }}>{isUnlocked ? 'UNLOCKED' : 'LOCKED'}</div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            ))}
          </div>
        </Panel>
      </div>
    </div>
  );
}
