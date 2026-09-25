import { useState } from 'react';
import StarField from '../components/StarField';
import NeonPanel from '../components/NeonPanel';

interface SquadronMultiplayerProps {
  onBack: () => void;
}

export default function SquadronMultiplayer({ onBack }: SquadronMultiplayerProps) {
  const [lanIp, setLanIp] = useState('127.0.0.1');
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = () => {
    setRefreshing(true);
    setTimeout(() => setRefreshing(false), 1200);
  };

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 80% 70% at 50% 40%, #060E18 0%, #05080E 100%)' }}>
      <StarField count={110} />

      {/* Header */}
      <NeonPanel color="gold" corners={false} className="absolute top-0 left-0 right-0 px-6 py-3 z-10">
        <div className="flex items-center justify-between">
          <div className="font-display text-sm tracking-widest glow-gold" style={{ color: '#FFB800' }}>
            SANGHA NETWORK // REAL WINSOCK2 UDP SQUAD COMMAND
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full animate-pulse-glow" style={{ background: '#00FF88', boxShadow: '0 0 6px #00FF88' }}/>
            <span className="font-mono text-[9px]" style={{ color: '#00FF88' }}>RTT: 18 ms | PORT 7704</span>
          </div>
        </div>
      </NeonPanel>

      {/* Main content */}
      <div className="absolute inset-0 flex gap-5 px-6 pt-16 pb-6">
        {/* Left: lobby list */}
        <NeonPanel color="gold" title="OPEN SQUAD LOBBIES" className="flex-1 flex flex-col">
          {/* Column headers */}
          <div className="flex items-center px-4 py-2" style={{ borderBottom: '1px solid #162030' }}>
            <span className="font-mono text-[8px] tracking-widest text-muted-foreground w-24">ROOM</span>
            <span className="font-mono text-[8px] tracking-widest text-muted-foreground flex-1">MISSION / REALM</span>
            <span className="font-mono text-[8px] tracking-widest text-muted-foreground w-24">MODE</span>
            <span className="font-mono text-[8px] tracking-widest text-muted-foreground w-20 text-right">STATUS</span>
          </div>

          {/* Empty lobby state */}
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="font-mono text-[9px] tracking-widest text-muted-foreground">
                Online lobby list unavailable
              </div>
              <div className="font-mono text-[9px] tracking-widest mt-1" style={{ color: '#4A6070' }}>
                Host a LAN room or use Quick Local Squad
              </div>
            </div>
          </div>

          {/* Refresh button */}
          <div className="p-3" style={{ borderTop: '1px solid #162030' }}>
            <NeonPanel color="cyan" hover onClick={handleRefresh} corners={false}
              className="py-2.5 text-center">
              <span className="font-mono text-[10px] tracking-widest" style={{ color: '#00E5FF' }}>
                {refreshing ? 'SCANNING...' : 'REFRESH'}
              </span>
            </NeonPanel>
          </div>
        </NeonPanel>

        {/* Right: deployment options */}
        <div className="w-80 flex flex-col gap-3">
          <div className="font-mono text-[8px] tracking-widest text-muted-foreground">
            SQUAD DEPLOYMENT:
          </div>

          {/* Quick local squad */}
          <NeonPanel color="gold" hover corners={false}
            className="py-3.5 text-center">
            <span className="font-body text-sm font-semibold tracking-widest" style={{ color: '#FFB800' }}>
              QUICK LOCAL SQUAD
            </span>
          </NeonPanel>

          {/* Host online */}
          <NeonPanel color="gold" hover corners={false}
            className="py-3.5 text-center opacity-60">
            <span className="font-body text-sm font-semibold tracking-widest" style={{ color: '#FFB800' }}>
              HOST ONLINE CLOUD LOBBY
            </span>
          </NeonPanel>

          {/* Host LAN */}
          <NeonPanel color="cyan" hover corners={false}
            className="py-3.5 text-center">
            <span className="font-body text-sm font-semibold tracking-widest" style={{ color: '#00E5FF' }}>
              HOST LOCAL LAN [7704]
            </span>
          </NeonPanel>

          {/* Join LAN */}
          <div>
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground mb-1.5">
              TARGET LAN HOST IP & PORT:
            </div>
            <input
              type="text"
              value={lanIp}
              onChange={e => setLanIp(e.target.value)}
              className="w-full px-3 py-2 font-mono text-xs bg-card text-foreground outline-none"
              style={{ border: '1px solid #162030', color: '#C0D0E0' }}
            />
          </div>
          <NeonPanel color="green" hover corners={false}
            className="py-3.5 text-center">
            <span className="font-body text-sm font-semibold tracking-widest" style={{ color: '#00FF88' }}>
              JOIN LAN HOST &gt;&gt;
            </span>
          </NeonPanel>

          {/* 1v1 Arena */}
          <NeonPanel color="orange" hover corners={false}
            className="py-3.5 text-center">
            <span className="font-body text-sm font-semibold tracking-widest" style={{ color: '#FF6B00' }}>
              1V1 ARENA DUEL
            </span>
          </NeonPanel>

          {/* Netcode info */}
          <div className="space-y-1 pt-1">
            <div className="font-mono text-[8px] tracking-widest text-muted-foreground">ACTIVE SQUAD NETCODE:</div>
            {[
              'Winsock2 Non-blocking UDP (Port 7704)',
              '30Hz Server Snapshots + 60Hz Inputs',
              '15s Reconnect Window + AI Takeover',
              'Downed Beacon [Hold F to Revive]',
            ].map(line => (
              <div key={line} className="font-mono text-[8px]" style={{ color: '#00FF88', opacity: 0.7 }}>{line}</div>
            ))}
          </div>

          {/* Back */}
          <div className="mt-auto">
            <NeonPanel color="white" hover onClick={onBack} corners={false}
              className="py-3 text-center">
              <span className="font-mono text-[10px] tracking-widest text-muted-foreground">BACK</span>
            </NeonPanel>
          </div>
        </div>
      </div>
    </div>
  );
}
