const SCREENS = [
  { id: 'main-menu',   label: 'HOME' },
  { id: 'ship-select', label: 'ARMORY' },
  { id: 'boon-select', label: 'BOON' },
  { id: 'game-hud',    label: 'HUD' },
  { id: 'game-over',   label: 'DEFEAT' },
  { id: 'victory',     label: 'VICTORY' },
  { id: 'realm-map',   label: 'MAP' },
  { id: 'leaderboard', label: 'SCORES' },
  { id: 'achievements', label: 'TROPHIES' },
  { id: 'sangha',      label: 'SANGHA' },
  { id: 'account',     label: 'ACCOUNT' },
  { id: 'settings',    label: 'CONFIG' },
  { id: 'codex',       label: 'CODEX' },
];

type Props = {
  current: string;
  onNavigate: (s: string) => void;
};

export default function ScreenNav({ current, onNavigate }: Props) {
  return (
    <div
      className="fixed bottom-0 left-0 right-0 z-50 flex items-center justify-center gap-1 px-4 py-2"
      style={{
        background: 'rgba(8,9,15,0.95)',
        borderTop: '1px solid rgba(233,196,0,0.15)',
        backdropFilter: 'blur(10px)',
      }}
    >
      <span
        className="text-[9px] tracking-[0.25em] mr-3 shrink-0"
        style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}
      >
        PREVIEW
      </span>
      {SCREENS.map(s => {
        const active = current === s.id;
        return (
          <button
            key={s.id}
            onClick={() => onNavigate(s.id)}
            className="px-2.5 py-1 text-[10px] tracking-[0.2em] transition-all duration-150"
            style={{
              fontFamily: '"Cinzel", serif',
              color: active ? '#E9C400' : '#8F98A8',
              background: active ? 'rgba(233,196,0,0.1)' : 'transparent',
              border: `1px solid ${active ? 'rgba(233,196,0,0.35)' : 'transparent'}`,
              clipPath: active
                ? 'polygon(4px 0%,calc(100% - 4px) 0%,100% 4px,100% calc(100% - 4px),calc(100% - 4px) 100%,4px 100%,0% calc(100% - 4px),0% 4px)'
                : 'none',
            }}
          >
            {s.label}
          </button>
        );
      })}
    </div>
  );
}
