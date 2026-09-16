import { useEffect, useState } from 'react';
import { LEADERBOARD } from '../data/gameData';
import type { LeaderboardEntry } from '../data/gameData';
import { getTopScores } from '../lib/api';
import Panel from './ui/Panel';
import StarField from './ui/StarField';
import VedicButton from './ui/VedicButton';

type Tab = 'global' | 'weekly' | 'monthly';

const MEDALS = ['🥇', '🥈', '🥉'];

function formatScore(n: number) {
  return n.toLocaleString('en-US');
}

type Props = { onNavigate: (s: string) => void };

export default function Leaderboard({ onNavigate }: Props) {
  const [tab, setTab] = useState<Tab>('global');
  const [remoteEntries, setRemoteEntries] = useState<LeaderboardEntry[] | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    getTopScores(10, controller.signal).then(payload => {
      const mapped = (payload.leaderboard ?? []).map((row, index) => ({
        rank: index + 1,
        player: String(row.player_name ?? row.game_id ?? 'UNKNOWN PILOT'),
        score: Number(row.score ?? 0),
        realmReached: `Wave ${Number(row.level_reached ?? 0)}`,
        ship: String(row.ship_class ?? 'pushpaka'),
        date: String(row.created_at ?? '').slice(0, 10) || '—',
        isCurrentPlayer: false,
      }));
      if (mapped.length > 0) setRemoteEntries(mapped);
    }).catch(() => {
      // Keep the local preview records visible when the hosted API is asleep
      // or the player is offline.
    });
    return () => controller.abort();
  }, []);

  const entries = (remoteEntries ?? LEADERBOARD).map((e, i) => ({
    ...e,
    score: tab === 'weekly' ? Math.floor(e.score * 0.62) : tab === 'monthly' ? Math.floor(e.score * 0.88) : e.score,
    rank: i + 1,
  }));

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />

      {/* Header */}
      <div
        className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6"
        style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.85)', backdropFilter: 'blur(12px)' }}
      >
        <button
          onClick={() => onNavigate('main-menu')}
          className="text-[10px] tracking-[0.25em] transition-colors hover:text-gold"
          style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}
        >
          ← MAIN MENU
        </button>
        <div className="h-4 w-px" style={{ background: 'rgba(233,196,0,0.2)' }} />
        <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
          SANGHA NETWORK
        </span>
        <div
          className="ml-2 px-2 py-0.5 text-[9px] tracking-wider"
          style={{ fontFamily: '"JetBrains Mono", monospace', color: '#40E090', background: 'rgba(64,224,144,0.1)', border: '1px solid rgba(64,224,144,0.3)' }}
        >
          ● ONLINE
        </div>
        <div className="ml-auto text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
          1,847 PILOTS RANKED
        </div>
      </div>

      {/* Main content */}
      <div className="absolute inset-0 z-10 flex flex-col" style={{ top: 52, bottom: 40, padding: '20px 24px', gap: 16 }}>

        {/* Tabs */}
        <div className="flex gap-2 items-center">
          {(['global', 'weekly', 'monthly'] as Tab[]).map(t => (
            <button
              key={t}
              onClick={() => setTab(t)}
              className="px-4 py-1.5 text-xs tracking-[0.25em] transition-all duration-150"
              style={{
                fontFamily: '"Cinzel", serif',
                color: tab === t ? '#FFF6DF' : '#8F98A8',
                background: tab === t ? 'rgba(233,196,0,0.1)' : 'transparent',
                border: `1px solid ${tab === t ? 'rgba(233,196,0,0.45)' : 'rgba(143,152,168,0.2)'}`,
                clipPath: 'polygon(5px 0%,calc(100% - 5px) 0%,100% 5px,100% 100%,0% 100%,0% 5px)',
              }}
            >
              {t.toUpperCase()}
            </button>
          ))}
          <div className="ml-auto text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
            COSMIC RECORDS
          </div>
        </div>

        {/* Top 3 spotlight */}
        <div className="grid grid-cols-3 gap-3" style={{ maxWidth: 640 }}>
          {entries.slice(0, 3).map((entry, i) => (
            <Panel key={entry.player} variant={i === 0 ? 'selected' : 'default'} cut={10}>
              <div className="p-3 text-center flex flex-col gap-1">
                <div className="text-2xl">{MEDALS[i]}</div>
                <div
                  className="text-xs tracking-[0.18em] font-semibold"
                  style={{ fontFamily: '"Cinzel", serif', color: i === 0 ? '#FFF6DF' : '#D0C6AB' }}
                >
                  {entry.player}
                </div>
                <div
                  className="text-sm font-black tracking-wider"
                  style={{ fontFamily: '"JetBrains Mono", monospace', color: i === 0 ? '#E9C400' : '#8F98A8' }}
                >
                  {formatScore(entry.score)}
                </div>
                <div className="text-[9px] tracking-wider" style={{ color: '#8F98A8' }}>{entry.ship}</div>
              </div>
            </Panel>
          ))}
        </div>

        {/* Full table */}
        <Panel variant="default" cut={12} className="flex-1 overflow-hidden">
          <div className="flex flex-col h-full overflow-hidden">
            {/* Table header */}
            <div
              className="grid px-4 py-2 text-[9px] tracking-[0.25em] shrink-0"
              style={{
                fontFamily: '"Cinzel", serif',
                color: '#8F98A8',
                borderBottom: '1px solid rgba(233,196,0,0.12)',
                gridTemplateColumns: '40px 1fr 140px 140px 80px 80px',
              }}
            >
              <span>#</span>
              <span>PILOT</span>
              <span>SCORE</span>
              <span>REALM</span>
              <span>SHIP</span>
              <span className="text-right">DATE</span>
            </div>

            {/* Rows */}
            <div className="overflow-y-auto flex-1">
              {entries.slice(3).map(entry => (
                <div
                  key={entry.player}
                  className="grid px-4 py-2.5 text-xs transition-colors hover:bg-white/[0.02]"
                  style={{
                    borderBottom: '1px solid rgba(255,255,255,0.04)',
                    gridTemplateColumns: '40px 1fr 140px 140px 80px 80px',
                    background: entry.isCurrentPlayer ? 'rgba(233,196,0,0.05)' : 'transparent',
                    border: entry.isCurrentPlayer ? '1px solid rgba(233,196,0,0.2)' : undefined,
                  }}
                >
                  <span style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
                    {entry.rank}
                  </span>
                  <span
                    style={{
                      fontFamily: '"Cinzel", serif',
                      color: entry.isCurrentPlayer ? '#E9C400' : '#D0C6AB',
                      display: 'flex',
                      alignItems: 'center',
                      gap: 6,
                    }}
                  >
                    {entry.player}
                    {entry.isCurrentPlayer && (
                      <span className="text-[8px] tracking-wider px-1.5 py-0.5" style={{ background: 'rgba(233,196,0,0.15)', color: '#E9C400' }}>
                        YOU
                      </span>
                    )}
                  </span>
                  <span style={{ fontFamily: '"JetBrains Mono", monospace', color: '#FFF6DF' }}>
                    {formatScore(entry.score)}
                  </span>
                  <span style={{ color: '#74F5FF' }}>{entry.realmReached}</span>
                  <span style={{ color: '#D0C6AB' }}>{entry.ship}</span>
                  <span className="text-right" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8', fontSize: 10 }}>
                    {entry.date.slice(5)}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </Panel>

        {/* Footer row */}
        <div className="flex items-center justify-between shrink-0">
          <div className="text-[10px] tracking-wider" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#8F98A8' }}>
            YOUR RANK: #10 · SCORE: 2,344,100 · REALM: KSHIRA SAGARA
          </div>
          <VedicButton variant="primary" onClick={() => onNavigate('ship-select')}>
            CLIMB THE RANKS ▶
          </VedicButton>
        </div>
      </div>
    </div>
  );
}
