import { useEffect, useMemo, useState } from 'react';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';
import { SHIPS } from '../data/gameData';
import {
  createLobby,
  getSession,
  joinLobby,
  leaveLobby,
  listLobbies,
  setLobbyReady,
  startLobby,
  type Lobby,
} from '../lib/api';
import type { DuelConfig } from '../types/game';

type Props = {
  onNavigate: (s: string) => void;
  onStartDuel?: (config: DuelConfig) => void;
};

export default function SanghaNetwork({ onNavigate, onStartDuel }: Props) {
  const session = getSession();
  const [lobbies, setLobbies] = useState<Lobby[]>([]);
  const [currentLobby, setCurrentLobby] = useState<Lobby | null>(null);
  const [mode, setMode] = useState<Lobby['mode']>('duel');
  const [shipClass, setShipClass] = useState('pushpaka');
  const [joinCode, setJoinCode] = useState('');
  const [notice, setNotice] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  const refresh = async () => {
    try {
      const open = await listLobbies();
      setLobbies(open);
      setCurrentLobby(previous => previous ? (open.find(item => item.code === previous.code) ?? previous) : previous);
    } catch (reason) { setError(reason instanceof Error ? reason.message : 'Could not load lobbies'); }
  };

  useEffect(() => {
    let active = true;
    const poll = async () => {
      try {
        const open = await listLobbies();
        if (active) {
          setLobbies(open);
          setCurrentLobby(previous => {
            if (!previous) return previous;
            const updated = open.find(item => item.code === previous.code) ?? previous;
            if (updated.status === 'running' && updated.mode === 'duel' && onStartDuel) {
              const p1 = updated.players[0] || { game_id: 'P1', player_name: 'Pilot 1', ship_class: 'pushpaka' };
              const p2 = updated.players[1] || { game_id: 'P2', player_name: 'Pilot 2', ship_class: 'garuda' };
              onStartDuel({
                mode: 'duel',
                roomCode: updated.code,
                player1: { gameId: p1.game_id, name: p1.player_name, shipId: p1.ship_class, health: 100, maxHealth: 100, score: 0 },
                player2: { gameId: p2.game_id, name: p2.player_name, shipId: p2.ship_class, health: 100, maxHealth: 100, score: 0 },
              });
              onNavigate('duel');
            }
            return updated;
          });
        }
      } catch { /* offline mode is allowed */ }
    };
    void poll();
    const timer = window.setInterval(() => void poll(), 3000);
    return () => { active = false; window.clearInterval(timer); };
  }, [onStartDuel, onNavigate]);

  const currentPlayer = useMemo(
    () => currentLobby?.players.find(player => player.game_id === session?.user.game_id),
    [currentLobby, session?.user.game_id],
  );
  const isHost = currentPlayer?.host === true;

  const withBusy = async (action: () => Promise<void>) => {
    setBusy(true); setError('');
    try { await action(); } catch (reason) { setError(reason instanceof Error ? reason.message : 'Network action failed'); }
    finally { setBusy(false); }
  };

  const create = () => withBusy(async () => {
    const result = await createLobby(mode, shipClass);
    setCurrentLobby(result.lobby);
    setNotice(mode === 'duel' ? '1v1 duel room created. Share the six-character code.' : 'Sangha room created.');
    await refresh();
  });

  const join = (code: string) => withBusy(async () => {
    const result = await joinLobby(code.trim().toUpperCase(), shipClass);
    setCurrentLobby(result.lobby); setJoinCode(''); setNotice(`Joined ${result.lobby.code}. Ready when you are.`);
    await refresh();
  });

  const update = (result: Lobby) => { setCurrentLobby(result); setLobbies(items => items.map(item => item.code === result.code ? result : item)); };

  if (!session) {
    return (
      <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
        <StarField />
        <div className="relative z-10 h-full flex items-center justify-center p-6">
          <Panel variant="dim" cut={14} style={{ maxWidth: 520 }}>
            <div className="p-8 text-center flex flex-col gap-4">
              <div className="text-[9px] tracking-[0.4em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>SANGHA NETWORK</div>
              <h1 className="text-2xl tracking-[0.14em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>SIGN IN TO FLY TOGETHER</h1>
              <p className="text-sm leading-relaxed" style={{ color: '#D0C6AB' }}>A stable Game ID is required to create or join a duel room. This keeps lobby ownership and match results tied to a real pilot.</p>
              <VedicButton variant="primary" onClick={() => onNavigate('account')}>OPEN PILOT ACCOUNT</VedicButton>
              <VedicButton variant="ghost" onClick={() => onNavigate('main-menu')}>BACK TO MAIN MENU</VedicButton>
            </div>
          </Panel>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />
      <div className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6" style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.86)', backdropFilter: 'blur(12px)' }}>
        <button onClick={() => onNavigate('main-menu')} className="text-[10px] tracking-[0.25em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>← MAIN MENU</button>
        <div className="h-4 w-px" style={{ background: 'rgba(233,196,0,0.2)' }} />
        <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>SANGHA NETWORK</span>
        <span className="ml-auto text-[10px] tracking-wider" style={{ color: '#74F5FF', fontFamily: '"JetBrains Mono", monospace' }}>● MATCHMAKING LINK</span>
      </div>

      <div className="relative z-10 h-full flex gap-5 overflow-y-auto" style={{ padding: '72px 24px 64px' }}>
        <div className="flex-1 min-w-0 flex flex-col gap-4">
          <Panel variant="selected" cut={14}>
            <div className="p-6 flex flex-col gap-5">
              <div>
                <div className="text-[9px] tracking-[0.4em] mb-2" style={{ fontFamily: '"Cinzel", serif', color: '#E9C400' }}>PRIVATE MATCHMAKING</div>
                <h1 className="text-2xl tracking-[0.14em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>OPEN A WING</h1>
                <p className="text-xs mt-2" style={{ color: '#D0C6AB' }}>Duel is a two-pilot room with 100 HP each. Both pilots ready up before the host starts.</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <label className="flex flex-col gap-1.5"><span className="text-[9px] tracking-[0.25em]" style={{ color: '#8F98A8' }}>MODE</span><select value={mode} onChange={event => setMode(event.target.value as Lobby['mode'])} className="px-3 py-2.5" style={{ background: '#0B0F18', color: '#FFF6DF', border: '1px solid rgba(0,219,231,0.3)' }}><option value="duel">1V1 DUEL</option><option value="campaign">CO-OP CAMPAIGN</option><option value="endless">CO-OP ENDLESS</option></select></label>
                <label className="flex flex-col gap-1.5"><span className="text-[9px] tracking-[0.25em]" style={{ color: '#8F98A8' }}>VIMANA</span><select value={shipClass} onChange={event => setShipClass(event.target.value)} className="px-3 py-2.5" style={{ background: '#0B0F18', color: '#FFF6DF', border: '1px solid rgba(0,219,231,0.3)' }}>{SHIPS.map(ship => <option key={ship.id} value={ship.id}>{ship.name.toUpperCase()}</option>)}</select></label>
                <div className="flex flex-col gap-2 justify-end">
                  <VedicButton variant="primary" fullWidth disabled={busy} onClick={create}>CREATE {mode === 'duel' ? '1V1 DUEL' : 'ROOM'}</VedicButton>
                  <VedicButton
                    variant="secondary"
                    fullWidth
                    onClick={() => {
                      if (onStartDuel) {
                        onStartDuel({
                          mode: 'duel',
                          player1: { gameId: session?.user.game_id || 'P1', name: session?.user.player_name || 'Pilot 1', shipId: shipClass, health: 100, maxHealth: 100, score: 0 },
                          player2: { gameId: 'P2', name: 'Pilot 2', shipId: 'garuda', health: 100, maxHealth: 100, score: 0 },
                        });
                      }
                      onNavigate('duel');
                    }}
                  >
                    LOCAL 1V1 DUEL ⚔
                  </VedicButton>
                </div>
              </div>
            </div>
          </Panel>

          <Panel variant="default" cut={12}>
            <div className="p-5 flex flex-col gap-4">
              <div className="flex items-center"><div className="text-[9px] tracking-[0.35em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>OPEN ROOMS · {lobbies.length}</div><button onClick={() => void refresh()} className="ml-auto text-[10px] tracking-wider" style={{ color: '#74F5FF' }}>REFRESH ↻</button></div>
              <div className="flex gap-2"><input value={joinCode} onChange={event => setJoinCode(event.target.value.toUpperCase())} maxLength={6} placeholder="ENTER ROOM CODE" className="flex-1 px-3 py-2.5 outline-none" style={{ background: '#0B0F18', color: '#FFF6DF', border: '1px solid rgba(0,219,231,0.24)', fontFamily: '"JetBrains Mono", monospace' }} /><VedicButton variant="secondary" disabled={busy || joinCode.trim().length < 6} onClick={() => void join(joinCode)}>JOIN CODE</VedicButton></div>
              {lobbies.length === 0 && <div className="py-8 text-center text-xs" style={{ color: '#8F98A8' }}>No open wings. Create the first room or share your code with a pilot.</div>}
              <div className="flex flex-col gap-2">{lobbies.map(lobby => <div key={lobby.code} className="flex flex-wrap items-center gap-3 p-3" style={{ background: 'rgba(20,26,40,0.55)', border: '1px solid rgba(0,219,231,0.15)' }}><div className="w-20"><div className="text-sm" style={{ color: '#E9C400', fontFamily: '"JetBrains Mono", monospace' }}>{lobby.code}</div><div className="text-[9px] tracking-wider" style={{ color: '#8F98A8' }}>{lobby.mode.toUpperCase()}</div></div><div className="flex-1 text-xs" style={{ color: '#D0C6AB' }}>{lobby.players.length}/{lobby.max_players} PILOTS · {lobby.status.toUpperCase()}</div><VedicButton variant="ghost" disabled={busy || lobby.status !== 'waiting'} onClick={() => void join(lobby.code)}>JOIN</VedicButton></div>)}</div>
            </div>
          </Panel>
        </div>

        <div className="w-full md:w-[330px] shrink-0 flex flex-col gap-4">
          {currentLobby ? <Panel variant="active" cut={14} className="flex-1"><div className="p-6 flex flex-col gap-5 h-full"><div><div className="text-[9px] tracking-[0.35em]" style={{ color: '#8F98A8' }}>ACTIVE ROOM</div><div className="text-3xl mt-1 tracking-[0.18em]" style={{ color: '#FFF6DF', fontFamily: '"JetBrains Mono", monospace' }}>{currentLobby.code}</div><div className="text-xs mt-2" style={{ color: '#74F5FF' }}>{currentLobby.mode === 'duel' ? '1V1 DUEL · 100 HP EACH' : `${currentLobby.mode.toUpperCase()} · ${currentLobby.max_players} PILOTS`}</div></div><div className="flex flex-col gap-2 flex-1">{currentLobby.players.map(player => <div key={player.game_id} className="p-3" style={{ border: `1px solid ${player.ready ? 'rgba(0,219,231,0.55)' : 'rgba(143,152,168,0.2)'}`, background: 'rgba(8,9,15,0.42)' }}><div className="flex items-center gap-2"><span className="text-sm" style={{ color: '#FFF6DF' }}>{player.player_name}</span>{player.host && <span className="text-[9px]" style={{ color: '#E9C400' }}>HOST</span>}<span className="ml-auto text-[9px]" style={{ color: player.ready ? '#74F5FF' : '#8F98A8' }}>{player.ready ? 'READY' : 'STANDBY'}</span></div><div className="text-[9px] mt-1" style={{ color: '#8F98A8', fontFamily: '"JetBrains Mono", monospace' }}>{player.game_id} · {player.ship_class.toUpperCase()} · {player.health}/{player.max_health} HP</div></div>)}{currentLobby.players.length < currentLobby.max_players && <div className="p-3 text-xs text-center" style={{ border: '1px dashed rgba(143,152,168,0.25)', color: '#8F98A8' }}>WAITING FOR ANOTHER PILOT…</div>}</div><div className="text-[10px] leading-relaxed" style={{ color: '#8F98A8' }}>ROOM HANDSHAKE READY. The current server owns matchmaking and readiness; synchronized combat requires the dedicated real-time game server described in the deployment plan.</div>{notice && <div className="text-xs" style={{ color: '#74F5FF' }}>{notice}</div>}{error && <div className="text-xs" style={{ color: '#FF6B72' }}>{error}</div>}<div className="flex flex-wrap gap-2"><VedicButton variant="secondary" disabled={busy || currentLobby.status !== 'waiting'} onClick={() => void withBusy(async () => update((await setLobbyReady(currentLobby.code, !currentPlayer?.ready)).lobby))}>{currentPlayer?.ready ? 'CANCEL READY' : 'READY UP'}</VedicButton><VedicButton variant="primary" disabled={busy || currentLobby.players.length < 2 || !currentLobby.players.every(player => player.ready)} onClick={() => void withBusy(async () => {
  const res = await startLobby(currentLobby.code);
  update(res.lobby);
  if (onStartDuel) {
    const p1 = currentLobby.players[0] || { game_id: 'P1', player_name: 'Pilot 1', ship_class: 'pushpaka' };
    const p2 = currentLobby.players[1] || { game_id: 'P2', player_name: 'Pilot 2', ship_class: 'garuda' };
    onStartDuel({
      mode: 'duel',
      roomCode: currentLobby.code,
      player1: { gameId: p1.game_id, name: p1.player_name, shipId: p1.ship_class, health: 100, maxHealth: 100, score: 0 },
      player2: { gameId: p2.game_id, name: p2.player_name, shipId: p2.ship_class, health: 100, maxHealth: 100, score: 0 },
    });
    onNavigate('duel');
  }
})}>START DUEL</VedicButton><VedicButton variant="ghost" disabled={busy} onClick={() => void withBusy(async () => { await leaveLobby(currentLobby.code); setCurrentLobby(null); setNotice('You left the room.'); await refresh(); })}>LEAVE</VedicButton></div></div></Panel> : <Panel variant="dim" cut={14} className="flex-1"><div className="p-6 h-full flex flex-col justify-center gap-4"><div className="text-[9px] tracking-[0.35em]" style={{ color: '#8F98A8' }}>DUEL PROTOCOL</div><h2 className="text-xl tracking-[0.12em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>HEALTH IS THE OBJECTIVE</h2><p className="text-sm leading-relaxed" style={{ color: '#D0C6AB' }}>Each pilot enters with 100 HP. The authoritative match server will apply projectile hits, ability damage, shields, and defeat state; the lobby is ready for that transport layer.</p><div className="flex flex-col gap-2 text-[10px]" style={{ color: '#8F98A8', fontFamily: '"JetBrains Mono", monospace' }}><span>01 · CREATE OR JOIN A ROOM</span><span>02 · SELECT A LOCKED/UNLOCKED VIMANA</span><span>03 · READY UP WITH YOUR OPPONENT</span><span>04 · FIGHT UNTIL ONE HULL REACHES 0 HP</span></div></div></Panel>}
        </div>
      </div>
    </div>
  );
}
