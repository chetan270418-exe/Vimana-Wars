import React from 'react';

type NeonColor = 'gold' | 'cyan' | 'green' | 'magenta' | 'orange' | 'red' | 'purple' | 'white';

const COLOR_MAP: Record<NeonColor, { border: string; glow: string; header: string }> = {
  gold:    { border: '#FFB800', glow: 'box-glow-gold',    header: '#FFB800' },
  cyan:    { border: '#00E5FF', glow: 'box-glow-cyan',    header: '#00E5FF' },
  green:   { border: '#00FF88', glow: 'box-glow-green',   header: '#00FF88' },
  magenta: { border: '#FF00FF', glow: 'box-glow-magenta', header: '#FF00FF' },
  orange:  { border: '#FF6B00', glow: 'box-glow-orange',  header: '#FF6B00' },
  red:     { border: '#FF2244', glow: 'box-glow-red',     header: '#FF2244' },
  purple:  { border: '#A020F0', glow: 'box-glow-purple',  header: '#A020F0' },
  white:   { border: '#8090A8', glow: '',                  header: '#8090A8' },
};

interface NeonPanelProps {
  color?: NeonColor;
  title?: string;
  className?: string;
  children: React.ReactNode;
  onClick?: () => void;
  hover?: boolean;
  corners?: boolean;
  dim?: boolean;
}

export default function NeonPanel({
  color = 'gold', title, className = '', children,
  onClick, hover = false, corners = true, dim = false,
}: NeonPanelProps) {
  const c = COLOR_MAP[color];
  return (
    <div
      role={onClick ? 'button' : undefined}
      tabIndex={onClick ? 0 : undefined}
      onClick={onClick}
      onKeyDown={onClick ? (e) => e.key === 'Enter' && onClick() : undefined}
      className={`relative bg-card ${c.glow} transition-all duration-150 ${
        hover ? `hover:bg-[rgba(255,255,255,0.03)] cursor-pointer active:scale-[0.99]` : ''
      } ${dim ? 'opacity-50' : ''} ${className}`}
      style={{ border: `1px solid ${c.border}` }}
    >
      {corners && (
        <>
          <div className="absolute top-0 left-0 w-3 h-3 pointer-events-none"
            style={{ borderTop: `2px solid ${c.border}`, borderLeft: `2px solid ${c.border}` }}/>
          <div className="absolute top-0 right-0 w-3 h-3 pointer-events-none"
            style={{ borderTop: `2px solid ${c.border}`, borderRight: `2px solid ${c.border}` }}/>
          <div className="absolute bottom-0 left-0 w-3 h-3 pointer-events-none"
            style={{ borderBottom: `2px solid ${c.border}`, borderLeft: `2px solid ${c.border}` }}/>
          <div className="absolute bottom-0 right-0 w-3 h-3 pointer-events-none"
            style={{ borderBottom: `2px solid ${c.border}`, borderRight: `2px solid ${c.border}` }}/>
        </>
      )}
      {title && (
        <div className="px-3 py-1.5 font-display text-[10px] tracking-widest uppercase"
          style={{ color: c.header, borderBottom: `1px solid ${c.border}22` }}>
          {title}
        </div>
      )}
      {children}
    </div>
  );
}
