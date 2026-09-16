const STARS = Array.from({ length: 260 }, (_, i) => ({
  id: i,
  x: ((i * 47.317 + 13.7) % 97) + 1.5,
  y: ((i * 53.139 + 7.31) % 97) + 1.5,
  size: ((i * 1.73) % 2.2) + 0.4,
  opacity: ((i * 0.233) % 0.62) + 0.12,
  delay: (i * 1.317) % 7,
  duration: ((i * 1.17) % 3.5) + 2,
  type: i % 5, // 0-4 for variety
}));

export default function StarField({ className = '' }: { className?: string }) {
  return (
    <div className={`absolute inset-0 overflow-hidden pointer-events-none ${className}`}>
      {STARS.map(s => (
        <div
          key={s.id}
          className="absolute rounded-full"
          style={{
            left: `${s.x}%`,
            top: `${s.y}%`,
            width: `${s.size}px`,
            height: `${s.size}px`,
            background:
              s.type === 0 ? `rgba(116,245,255,${s.opacity * 0.7})` :
              s.type === 1 ? `rgba(233,196,0,${s.opacity * 0.5})` :
              `rgba(255,246,223,${s.opacity})`,
            animation: `twinkle ${s.duration}s ease-in-out ${s.delay}s infinite`,
          }}
        />
      ))}
      {/* Nebula depth layers */}
      <div
        className="absolute inset-0"
        style={{
          background: [
            'radial-gradient(ellipse 55% 45% at 75% 50%, rgba(40,15,70,0.45) 0%, transparent 70%)',
            'radial-gradient(ellipse 40% 55% at 20% 35%, rgba(0,25,55,0.5) 0%, transparent 65%)',
            'radial-gradient(ellipse 30% 30% at 50% 80%, rgba(10,30,20,0.2) 0%, transparent 60%)',
          ].join(','),
        }}
      />
    </div>
  );
}
