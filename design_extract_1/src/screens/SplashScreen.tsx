import { useEffect, useState } from 'react';
import StarField from '../components/StarField';
import MandalaEmblem from '../components/MandalaEmblem';

interface SplashScreenProps {
  onComplete: () => void;
}

const STATUS_LINES = [
  'INITIALIZING VEDIC COMPUTATION ENGINE...',
  'SYNCHRONIZING CELESTIAL DATABASE...',
  'LOADING ASTRAL COMBAT MATRICES...',
  'CALIBRATING PRANA FIELD RESONATORS...',
  'ESTABLISHING SANGHA NETWORK UPLINK...',
  'COMPILING REALM TOPOGRAPHY DATA...',
  'SYSTEMS NOMINAL — ENTERING CELESTIAL ORBIT',
];

export default function SplashScreen({ onComplete }: SplashScreenProps) {
  const [progress, setProgress] = useState(0);
  const [statusIdx, setStatusIdx] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) { clearInterval(interval); return 100; }
        return p + 1.4;
      });
    }, 42);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (progress < 100) {
      const idx = Math.min(STATUS_LINES.length - 1, Math.floor((progress / 100) * STATUS_LINES.length));
      setStatusIdx(idx);
    }
  }, [progress]);

  useEffect(() => {
    if (progress >= 100) {
      const t = setTimeout(onComplete, 900);
      return () => clearTimeout(t);
    }
  }, [progress, onComplete]);

  return (
    <div className="relative w-full h-full flex flex-col items-center justify-center overflow-hidden scanline-overlay"
      style={{ background: 'radial-gradient(ellipse 80% 70% at 50% 40%, #081420 0%, #05080E 100%)' }}>
      <StarField count={160} />

      {/* Outer decorative ring - slow rotate */}
      <div className="absolute animate-rotate-slow" style={{ width: 440, height: 440 }}>
        <MandalaEmblem size={440} />
      </div>
      {/* Inner ring - reverse rotate */}
      <div className="absolute animate-rotate-slow-rev" style={{ width: 300, height: 300 }}>
        <MandalaEmblem size={300} />
      </div>

      {/* Ship - floating */}
      <div className="relative z-10 animate-float" style={{ marginBottom: 12 }}>
        <svg viewBox="0 0 140 170" width="180" height="210" fill="none" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <radialGradient id="splashEng" cx="50%" cy="50%">
              <stop offset="0%" stopColor="#00E5FF" stopOpacity="0.95"/>
              <stop offset="100%" stopColor="#00E5FF" stopOpacity="0"/>
            </radialGradient>
            <filter id="shipGlow">
              <feGaussianBlur stdDeviation="3" result="blur"/>
              <feComposite in="SourceGraphic" in2="blur" operator="over"/>
            </filter>
          </defs>
          <path d="M70 40 L10 130 L36 130 L70 60 Z" fill="#B31C1C" filter="url(#shipGlow)"/>
          <path d="M10 130 L36 130 L28 152 L4 152 Z" fill="#881414"/>
          <path d="M70 40 L130 130 L104 130 L70 60 Z" fill="#B31C1C" filter="url(#shipGlow)"/>
          <path d="M130 130 L104 130 L112 152 L136 152 Z" fill="#881414"/>
          <path d="M59 14 L81 14 L89 152 L51 152 Z" fill="#C8CCD8"/>
          <path d="M63 45 L77 45 L83 152 L57 152 Z" fill="#B0B4C0" opacity="0.3"/>
          <ellipse cx="70" cy="38" rx="13" ry="20" fill="#2860A8"/>
          <ellipse cx="70" cy="35" rx="8" ry="14" fill="#4090D0" opacity="0.65"/>
          <ellipse cx="70" cy="32" rx="5" ry="9" fill="#80C8F0" opacity="0.4"/>
          <path d="M60 12 L80 12 L78 24 L62 24 Z" fill="#505868"/>
          <path d="M65 6 L75 6 L75 14 L65 14 Z" fill="#383E4A"/>
          <ellipse cx="63" cy="157" rx="7" ry="4" fill="#181C22"/>
          <ellipse cx="77" cy="157" rx="7" ry="4" fill="#181C22"/>
          <ellipse cx="63" cy="157" rx="4.5" ry="2.5" fill="url(#splashEng)"/>
          <ellipse cx="77" cy="157" rx="4.5" ry="2.5" fill="url(#splashEng)"/>
          <ellipse cx="63" cy="161" rx="5" ry="4" fill="#00E5FF" opacity="0.15"/>
          <ellipse cx="77" cy="161" rx="5" ry="4" fill="#00E5FF" opacity="0.15"/>
        </svg>
      </div>

      {/* Logo */}
      <div className="relative z-10 text-center mb-10" style={{ marginTop: -8 }}>
        <div className="font-display tracking-[0.25em] select-none" style={{ fontSize: 44 }}>
          <span style={{ color: '#FFB800' }} className="glow-gold">vimana</span>
          {' '}
          <span className="text-white" style={{ textShadow: '0 0 30px rgba(255,255,255,0.4)' }}>WARS</span>
        </div>
        <div className="font-body tracking-[0.5em] text-xs mt-1"
          style={{ color: '#00E5FF', opacity: 0.7 }}>
          CELESTIAL COMBAT // THE 7 REALMS OF MAHAYUDDHA
        </div>
      </div>

      {/* Progress bar */}
      <div className="relative z-10 w-80">
        <div className="h-px mb-2 overflow-hidden" style={{ background: '#162030' }}>
          <div className="h-full transition-all duration-100"
            style={{
              width: `${progress}%`,
              background: 'linear-gradient(90deg, #004488 0%, #00E5FF 60%, #FFB800 100%)',
              boxShadow: '0 0 8px #00E5FF',
            }}
          />
        </div>
        <div className="flex justify-between items-center">
          <span className="font-mono text-[9px] tracking-widest animate-data-flicker"
            style={{ color: '#00E5FF', opacity: 0.7 }}>
            {STATUS_LINES[statusIdx]}
          </span>
          <span className="font-mono text-[10px]" style={{ color: '#FFB800' }}>
            {Math.min(100, Math.round(progress))}%
          </span>
        </div>
      </div>

      {/* Bottom tech line */}
      <div className="absolute bottom-5 font-mono text-[8px] tracking-[0.3em] text-center"
        style={{ color: '#2A3A50' }}>
        V2.0 // RAYLIB 5.0 + C++20 + SQLITE3 // NATIVE ENGINE
      </div>

      {/* Scanline */}
      <div className="absolute left-0 right-0 h-16 pointer-events-none"
        style={{
          background: 'linear-gradient(180deg, transparent, rgba(0,229,255,0.04), transparent)',
          animation: 'scanline 4s linear infinite',
        }}
      />
    </div>
  );
}
