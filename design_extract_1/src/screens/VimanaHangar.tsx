import { useState } from 'react';
import StarField from '../components/StarField';
import NeonPanel from '../components/NeonPanel';
import VimanaShip, { SHIPS, ShipId } from '../components/VimanaShip';
import StatBar from '../components/StatBar';

interface VimanaHangarProps {
  onBack: () => void;
}

export default function VimanaHangar({ onBack }: VimanaHangarProps) {
  const [idx, setIdx] = useState(0);
  const [selectedWeapon, setSelectedWeapon] = useState(0);
  const [rotating, setRotating] = useState(false);

  const ship = SHIPS[idx];
  const total = SHIPS.length;

  const prev = () => { setRotating(true); setTimeout(() => { setIdx(i => (i - 1 + total) % total); setRotating(false); }, 160); };
  const next = () => { setRotating(true); setTimeout(() => { setIdx(i => (i + 1) % total); setRotating(false); }, 160); };

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 70% 60% at 50% 40%, #080E1E 0%, #05080E 100%)' }}>
      <StarField count={120} />

      {/* Header bar */}
      <NeonPanel color="gold" corners={false} className="absolute top-0 left-0 right-0 px-6 py-3 z-10">
        <div className="flex items-center justify-between">
          <div className="font-display text-sm tracking-widest glow-gold" style={{ color: '#FFB800' }}>
            VIMANA HANGAR & ARMORY // COMMISSION SHIPS
          </div>
          <div className="font-mono text-[10px] tracking-widest" style={{ color: '#FF6B00' }}>
            PRANA SHARDS: 33,644
          </div>
        </div>
      </NeonPanel>

      {/* Main content */}
      <div className="absolute inset-0 flex gap-5 px-6 pt-20 pb-6">
        {/* Left: ship viewer */}
        <NeonPanel color="gold" className="flex-1 flex flex-col relative" title={`[${idx + 1} / ${total}] READY`}>
          <div className="absolute top-10 left-4 z-10">
            <div className="font-display text-lg glow-gold mb-0.5" style={{ color: '#FFB800' }}>{ship.name.toUpperCase()}</div>
            <div className="font-body text-sm" style={{ color: '#00E5FF' }}>{ship.role}</div>
            <div className="font-mono text-[9px] tracking-widest mt-1" style={{ color: '#7090A8' }}>
              ROLE: {ship.roleTag}
            </div>
          </div>

          {/* Ship display */}
          <div className={`flex-1 flex items-center justify-center transition-opacity duration-150 ${rotating ? 'opacity-0' : 'opacity-100'}`}>
            <div className="animate-float" style={{ height: 260, display: 'flex', alignItems: 'center' }}>
              <div style={{ width: 200, height: 260 }}>
                <VimanaShip id={ship.id as ShipId} />
              </div>
            </div>
          </div>

          {/* Lore text */}
          <div className="p-4 font-body text-xs leading-relaxed" style={{ color: '#4A6070', borderTop: '1px solid #162030' }}>
            {ship.lore}
          </div>

          {/* Nav arrows */}
          <div className="absolute inset-y-0 left-3 flex items-center">
            <NeonPanel color="gold" hover onClick={prev} className="w-9 h-9 flex items-center justify-center" corners={false}>
              <span className="font-display text-sm" style={{ color: '#FFB800' }}>&lt;</span>
            </NeonPanel>
          </div>
          <div className="absolute inset-y-0 right-3 flex items-center">
            <NeonPanel color="gold" hover onClick={next} className="w-9 h-9 flex items-center justify-center" corners={false}>
              <span className="font-display text-sm" style={{ color: '#FFB800' }}>&gt;</span>
            </NeonPanel>
          </div>

          {/* Ship dots nav */}
          <div className="flex justify-center gap-2 py-2">
            {SHIPS.map((_, i) => (
              <button key={i} onClick={() => setIdx(i)}
                className="w-2 h-2 rounded-full transition-all duration-200"
                style={{ background: i === idx ? '#FFB800' : '#1A2840', boxShadow: i === idx ? '0 0 6px #FFB800' : 'none' }}/>
            ))}
          </div>
        </NeonPanel>

        {/* Right: specs + weapons */}
        <div className="w-80 flex flex-col gap-4">
          <NeonPanel color="cyan" title="VESSEL SPECIFICATIONS & ARMORY" className="p-4 flex-1 flex flex-col gap-4">
            {/* Stats */}
            <div className="space-y-1">
              <StatBar label="Hull Integrity" value={ship.stats.hull}  color="#00FF88"/>
              <StatBar label="Velocity"       value={ship.stats.velocity} color="#00E5FF"/>
              <StatBar label="Cannon Damage"  value={ship.stats.cannon} color="#FF6B00"/>
              <StatBar label="Dash Charges"   value={ship.stats.dash} color="#FFB800"/>
            </div>

            {/* Divider */}
            <div className="h-px bg-border"/>

            {/* Weapons */}
            <div>
              <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-2">
                ARMORY LOADOUT — SELECT WEAPON SLOT
              </div>
              <div className="space-y-2">
                {ship.weapons.map((w, i) => {
                  const wColor = i === 0 ? 'cyan' : i === 1 ? 'green' : 'orange';
                  return (
                    <NeonPanel key={w} color={wColor} hover corners={false}
                      onClick={() => setSelectedWeapon(i)}
                      className={`p-2.5 transition-all ${selectedWeapon === i ? 'bg-[rgba(255,255,255,0.04)]' : ''}`}>
                      <div className="flex items-center justify-between">
                        <span className="font-body text-sm font-semibold tracking-widest"
                          style={{ color: selectedWeapon === i ? '#fff' : 'var(--foreground)' }}>
                          {w}
                        </span>
                        {selectedWeapon === i && (
                          <span className="font-mono text-[8px]" style={{ color: '#00FF88' }}>EQUIPPED</span>
                        )}
                      </div>
                    </NeonPanel>
                  );
                })}
              </div>
            </div>

            {/* Spacer */}
            <div className="flex-1"/>

            {/* Launch */}
            <NeonPanel color="gold" hover className="p-4 text-center" corners>
              <span className="font-display text-xs tracking-widest glow-gold" style={{ color: '#FFB800' }}>
                LAUNCH MISSION
              </span>
            </NeonPanel>
          </NeonPanel>

          {/* Back */}
          <NeonPanel color="white" hover onClick={onBack} className="p-3 text-center" corners={false}>
            <span className="font-mono text-[10px] tracking-widest text-muted-foreground">BACK</span>
          </NeonPanel>
        </div>
      </div>
    </div>
  );
}
