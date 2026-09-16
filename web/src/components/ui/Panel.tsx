type Variant = 'default' | 'selected' | 'active' | 'danger' | 'dim';

const VSTYLES: Record<Variant, { border: string; bg: string; glow: string }> = {
  default:  { border: 'rgba(233,196,0,0.22)',  bg: 'rgba(14,20,35,0.93)',  glow: 'drop-shadow(0 0 4px rgba(233,196,0,0.08))' },
  selected: { border: 'rgba(233,196,0,0.88)',  bg: 'rgba(22,32,52,0.97)',  glow: 'drop-shadow(0 0 14px rgba(233,196,0,0.42)) drop-shadow(0 2px 30px rgba(233,196,0,0.18))' },
  active:   { border: 'rgba(0,219,231,0.65)',  bg: 'rgba(10,24,40,0.95)',  glow: 'drop-shadow(0 0 10px rgba(0,219,231,0.32))' },
  danger:   { border: 'rgba(191,0,54,0.72)',   bg: 'rgba(28,8,18,0.95)',   glow: 'drop-shadow(0 0 10px rgba(191,0,54,0.38))' },
  dim:      { border: 'rgba(143,152,168,0.18)', bg: 'rgba(11,15,24,0.88)', glow: 'none' },
};

type PanelProps = {
  children: React.ReactNode;
  variant?: Variant;
  cut?: number;
  className?: string;
  style?: React.CSSProperties;
  onClick?: () => void;
  scanlines?: boolean;
  corners?: boolean;
};

function cp(c: number) {
  return `polygon(${c}px 0%,calc(100% - ${c}px) 0%,100% ${c}px,100% calc(100% - ${c}px),calc(100% - ${c}px) 100%,${c}px 100%,0% calc(100% - ${c}px),0% ${c}px)`;
}

export default function Panel({
  children,
  variant = 'default',
  cut = 12,
  className = '',
  style,
  onClick,
  scanlines = true,
  corners = true,
}: PanelProps) {
  const s = VSTYLES[variant];
  const cut2 = Math.max(cut - 1, 0);

  return (
    <div
      className={`relative ${onClick ? 'cursor-pointer' : ''} ${className}`}
      style={{ filter: s.glow, ...style }}
      onClick={onClick}
    >
      {/* border */}
      <div className="absolute inset-0 pointer-events-none" style={{ clipPath: cp(cut), background: s.border }} />
      {/* bg */}
      <div className="absolute inset-[1px] pointer-events-none" style={{ clipPath: cp(cut2), background: s.bg }} />
      {/* scanlines */}
      {scanlines && (
        <div
          className="absolute inset-[1px] pointer-events-none z-10 opacity-[0.03]"
          style={{
            clipPath: cp(cut2),
            backgroundImage: 'repeating-linear-gradient(0deg,transparent 0px,transparent 3px,rgba(255,255,255,1) 3px,rgba(255,255,255,1) 4px)',
          }}
        />
      )}
      {/* corner etchings */}
      {corners && (
        <div className="absolute inset-[4px] pointer-events-none z-10">
          <div className="absolute top-0 left-0 w-3 h-3 border-t border-l" style={{ borderColor: s.border }} />
          <div className="absolute top-0 right-0 w-3 h-3 border-t border-r" style={{ borderColor: s.border }} />
          <div className="absolute bottom-0 left-0 w-3 h-3 border-b border-l" style={{ borderColor: s.border }} />
          <div className="absolute bottom-0 right-0 w-3 h-3 border-b border-r" style={{ borderColor: s.border }} />
        </div>
      )}
      {/* content */}
      <div className="relative z-20">{children}</div>
    </div>
  );
}
