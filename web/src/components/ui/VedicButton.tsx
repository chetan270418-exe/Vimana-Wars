type Variant = 'primary' | 'secondary' | 'ghost' | 'danger';

type Props = {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: Variant;
  className?: string;
  disabled?: boolean;
  fullWidth?: boolean;
};

const CUT = 8;
function cp(c: number) {
  return `polygon(${c}px 0%,calc(100% - ${c}px) 0%,100% ${c}px,100% calc(100% - ${c}px),calc(100% - ${c}px) 100%,${c}px 100%,0% calc(100% - ${c}px),0% ${c}px)`;
}

const VSTYLE: Record<Variant, { border: string; bg: string; text: string; hoverBorder: string; hoverBg: string; glow: string }> = {
  primary:   { border: 'rgba(233,196,0,0.8)',  bg: 'rgba(233,196,0,0.1)',  text: '#FFF6DF', hoverBorder: '#E9C400', hoverBg: 'rgba(233,196,0,0.18)', glow: '0 0 16px rgba(233,196,0,0.3)' },
  secondary: { border: 'rgba(0,219,231,0.6)',  bg: 'rgba(0,219,231,0.06)', text: '#74F5FF', hoverBorder: '#00DBE7', hoverBg: 'rgba(0,219,231,0.12)', glow: '0 0 12px rgba(0,219,231,0.25)' },
  ghost:     { border: 'rgba(208,198,171,0.3)', bg: 'transparent',          text: '#D0C6AB', hoverBorder: 'rgba(208,198,171,0.6)', hoverBg: 'rgba(208,198,171,0.06)', glow: 'none' },
  danger:    { border: 'rgba(191,0,54,0.7)',   bg: 'rgba(191,0,54,0.08)',  text: '#FF6B72', hoverBorder: '#BF0036', hoverBg: 'rgba(191,0,54,0.15)', glow: '0 0 14px rgba(191,0,54,0.3)' },
};

export default function VedicButton({ children, onClick, variant = 'primary', className = '', disabled = false, fullWidth = false }: Props) {
  const v = VSTYLE[variant];

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`group relative select-none transition-all duration-150 ${fullWidth ? 'w-full' : ''} ${disabled ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'} ${className}`}
      style={{ filter: disabled ? 'none' : undefined }}
    >
      {/* border */}
      <div
        className="absolute inset-0 transition-all duration-150"
        style={{ clipPath: cp(CUT), background: v.border }}
      />
      {/* bg */}
      <div
        className="absolute inset-[1px] transition-all duration-150 group-hover:opacity-100"
        style={{ clipPath: cp(CUT - 1), background: v.bg }}
      />
      {/* hover bg overlay */}
      <div
        className="absolute inset-[1px] opacity-0 group-hover:opacity-100 transition-opacity duration-150"
        style={{ clipPath: cp(CUT - 1), background: v.hoverBg }}
      />
      {/* text */}
      <span
        className="relative z-10 flex items-center justify-center gap-2 px-6 py-2.5 text-sm tracking-[0.18em] font-semibold"
        style={{ fontFamily: '"Cinzel", serif', color: v.text }}
      >
        {children}
      </span>
    </button>
  );
}
