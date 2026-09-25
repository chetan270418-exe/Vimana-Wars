interface MandalaEmblemProps {
  size?: number;
  animate?: boolean;
}

export default function MandalaEmblem({ size = 200, animate = false }: MandalaEmblemProps) {
  const cx = size / 2, cy = size / 2;
  const pts = (n: number, r: number, offset = 0) =>
    Array.from({ length: n }, (_, i) => {
      const a = ((i * 360) / n + offset) * (Math.PI / 180);
      return { x: cx + r * Math.cos(a - Math.PI / 2), y: cy + r * Math.sin(a - Math.PI / 2) };
    });

  return (
    <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} fill="none">
      {/* Outer rings */}
      <circle cx={cx} cy={cy} r={cx * 0.95} stroke="#FFB800" strokeWidth="0.6" opacity="0.25"/>
      <circle cx={cx} cy={cy} r={cx * 0.88} stroke="#FFB800" strokeWidth="0.4" opacity="0.15"/>

      {/* 16 outer petals */}
      {pts(16, cx * 0.82).map((p, i) => (
        <circle key={`op${i}`} cx={p.x} cy={p.y} r={3} fill="#FFB800" opacity="0.3"/>
      ))}

      {/* Radial spokes */}
      {pts(12, cx * 0.75).map((p, i) => (
        <line key={`sp${i}`} x1={cx} y1={cy} x2={p.x} y2={p.y}
          stroke="#FFB800" strokeWidth="0.4" opacity="0.12"/>
      ))}

      {/* Middle ring */}
      <circle cx={cx} cy={cy} r={cx * 0.65} stroke="#00E5FF" strokeWidth="0.8" opacity="0.2"
        className={animate ? 'animate-rotate-slow-rev' : ''} style={{ transformOrigin: `${cx}px ${cy}px` }}/>

      {/* 8 inner petal diamond shapes */}
      {pts(8, cx * 0.56, 22.5).map((p, i) => {
        const a = ((i * 45 + 22.5) * Math.PI) / 180;
        const dx = cx * 0.07 * Math.cos(a); const dy = cx * 0.07 * Math.sin(a);
        return (
          <polygon key={`ip${i}`}
            points={`${p.x},${p.y - 5} ${p.x + dx},${p.y} ${p.x},${p.y + 5} ${p.x - dx},${p.y}`}
            fill="#FFB800" opacity="0.25"/>
        );
      })}

      {/* Inner spoke ring */}
      <circle cx={cx} cy={cy} r={cx * 0.48} stroke="#FFB800" strokeWidth="1" opacity="0.3"
        strokeDasharray="4 3"/>

      {/* 6-point star inner */}
      {pts(6, cx * 0.38).map((p, i) => {
        const opp = pts(6, cx * 0.38, 60)[i];
        return <line key={`st${i}`} x1={p.x} y1={p.y} x2={opp.x} y2={opp.y}
          stroke="#FFB800" strokeWidth="0.6" opacity="0.2"/>;
      })}

      {/* Core rings */}
      <circle cx={cx} cy={cy} r={cx * 0.30} stroke="#FFB800" strokeWidth="1.2" opacity="0.4"
        fill={`rgba(255,184,0,0.03)`}/>
      <circle cx={cx} cy={cy} r={cx * 0.22} stroke="#00E5FF" strokeWidth="0.6" opacity="0.35"/>
      <circle cx={cx} cy={cy} r={cx * 0.14} stroke="#FFB800" strokeWidth="1" opacity="0.5"
        fill="rgba(255,184,0,0.06)"/>

      {/* Center dot */}
      <circle cx={cx} cy={cy} r={3} fill="#FFB800" opacity="0.7"/>
    </svg>
  );
}
