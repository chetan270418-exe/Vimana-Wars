import NeonPanel from './NeonPanel';

interface PilotDossierModalProps {
  onClose: () => void;
}

export default function PilotDossierModal({ onClose }: PilotDossierModalProps) {
  return (
    <div className="absolute inset-0 z-50 flex items-center justify-center"
      style={{ background: 'rgba(3,6,12,0.8)', backdropFilter: 'blur(4px)' }}
      onClick={onClose}>
      <div onClick={e => e.stopPropagation()} className="animate-fade-up w-[520px]">
        <NeonPanel color="gold" title="PILOT IDENTIFICATION DOSSIER" className="p-0">
          <div className="p-6 space-y-5">
            {/* Callsign + rank */}
            <div>
              <div className="font-mono text-[9px] tracking-widest text-muted-foreground uppercase mb-1">
                CALLSIGN // RANK
              </div>
              <div className="font-display text-2xl glow-gold" style={{ color: '#FFB800' }}>WARRIOR</div>
              <div className="font-body text-sm mt-0.5" style={{ color: '#00FF88' }}>
                ASURA SLAYER (COMMANDER)
              </div>
            </div>

            {/* Action buttons */}
            <div className="grid grid-cols-2 gap-3">
              <button className="font-mono text-[10px] tracking-widest uppercase py-2.5 transition-all
                hover:bg-[rgba(0,229,255,0.08)] active:scale-[0.98]"
                style={{ border: '1px solid #00E5FF', color: '#00E5FF' }}>
                COPY ID [C]
              </button>
              <button onClick={onClose}
                className="font-mono text-[10px] tracking-widest uppercase py-2.5 transition-all
                hover:bg-[rgba(0,229,255,0.08)] active:scale-[0.98]"
                style={{ border: '1px solid #00E5FF', color: '#00E5FF' }}>
                CLOSE [ESC]
              </button>
            </div>

            {/* Network ID */}
            <NeonPanel color="cyan" className="p-3">
              <div className="font-mono text-[9px] tracking-widest text-muted-foreground mb-1">
                SANGHA NETWORK ID
              </div>
              <div className="flex items-center justify-between">
                <span className="font-display text-xl glow-cyan" style={{ color: '#00E5FF' }}>
                  VMN-7517-A969
                </span>
                <span className="font-mono text-[9px] animate-blink" style={{ color: '#FF6B00' }}>
                  [OFFLINE GUEST PILOT]
                </span>
              </div>
            </NeonPanel>

            {/* Stats grid */}
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: 'MAX CAMPAIGN WAVE', value: 'WAVE 26 / 30', color: '#FFB800' },
                { label: 'CAREER HIGH SCORE', value: '6,110,580 PTS', color: '#FFB800' },
                { label: 'COMMISSIONED VIMANAS', value: '42 / 52 SHIPS', color: '#00FF88' },
                { label: 'ASTRAL PRANA TREASURY', value: '33,644 SHARDS', color: '#FF6B00' },
              ].map(item => (
                <NeonPanel key={item.label} color="white" className="p-3">
                  <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1">
                    {item.label}
                  </div>
                  <div className="font-body text-base font-semibold" style={{ color: item.color }}>
                    {item.value}
                  </div>
                </NeonPanel>
              ))}
            </div>

            {/* Close hint */}
            <div className="text-center font-mono text-[9px] tracking-widest text-muted-foreground">
              PRESS [ESC] OR CLICK OUTSIDE TO CLOSE DOSSIER
            </div>
          </div>
        </NeonPanel>
      </div>
    </div>
  );
}
