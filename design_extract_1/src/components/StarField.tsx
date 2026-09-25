import { useMemo } from 'react';

interface Star {
  id: number; x: number; y: number;
  size: number; opacity: number; delay: number; dur: number;
}

export default function StarField({ count = 140 }: { count?: number }) {
  const stars = useMemo<Star[]>(() => {
    const rng = (seed: number) => {
      let s = seed;
      return () => { s = (s * 1664525 + 1013904223) & 0xffffffff; return (s >>> 0) / 0xffffffff; };
    };
    const rand = rng(42);
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      x: rand() * 100,
      y: rand() * 100,
      size: rand() * 1.8 + 0.4,
      opacity: rand() * 0.65 + 0.15,
      delay: rand() * 4,
      dur: rand() * 3 + 2,
    }));
  }, [count]);

  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {stars.map(s => (
        <div
          key={s.id}
          className="absolute rounded-full bg-white animate-pulse-glow"
          style={{
            left: `${s.x}%`, top: `${s.y}%`,
            width: s.size, height: s.size,
            opacity: s.opacity,
            animationDelay: `${s.delay}s`,
            animationDuration: `${s.dur}s`,
          }}
        />
      ))}
      {/* Nebula hint */}
      <div className="absolute inset-0"
        style={{
          background: `
            radial-gradient(ellipse 60% 40% at 20% 70%, rgba(0,80,140,0.08) 0%, transparent 70%),
            radial-gradient(ellipse 40% 30% at 80% 30%, rgba(80,0,140,0.06) 0%, transparent 70%)
          `,
        }}
      />
    </div>
  );
}
