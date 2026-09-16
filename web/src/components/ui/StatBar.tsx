type Props = {
  label: string;
  value: number;
  color?: string;
  animated?: boolean;
};

export default function StatBar({ label, value, color = '#E9C400', animated = true }: Props) {
  return (
    <div className="flex items-center gap-3">
      <span
        className="w-20 text-xs tracking-[0.15em] uppercase shrink-0"
        style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}
      >
        {label}
      </span>
      <div className="flex-1 h-[3px] relative" style={{ background: 'rgba(255,255,255,0.07)' }}>
        <div
          className={animated ? 'transition-all duration-700 ease-out' : ''}
          style={{
            width: `${value}%`,
            height: '100%',
            background: `linear-gradient(to right, ${color}99, ${color})`,
            boxShadow: `0 0 6px ${color}55`,
          }}
        />
        {/* tick marks */}
        {[25, 50, 75].map(t => (
          <div
            key={t}
            className="absolute top-0 w-px h-full"
            style={{ left: `${t}%`, background: 'rgba(255,255,255,0.12)' }}
          />
        ))}
      </div>
      <span
        className="w-7 text-right text-xs shrink-0"
        style={{ fontFamily: '"JetBrains Mono", monospace', color }}
      >
        {value}
      </span>
    </div>
  );
}
