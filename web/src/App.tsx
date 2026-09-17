import { useState, useCallback } from 'react';
import MainMenu from './components/MainMenu';
import ShipSelect from './components/ShipSelect';
import BoonSelect from './components/BoonSelect';
import GameOver from './components/GameOver';
import Victory from './components/Victory';
import RealmMap from './components/RealmMap';
import Leaderboard from './components/Leaderboard';
import Settings from './components/Settings';
import Codex from './components/Codex';
import Account from './components/Account';
import SanghaNetwork from './components/SanghaNetwork';
import PlayableArena from './components/PlayableArena';
import DuelResultModal from './components/DuelResultModal';
import ScreenNav from './components/ui/ScreenNav';
import { getSession, submitScore } from './lib/api';
import { getProgression, saveProgression } from './lib/progression';
import type { ScreenId, RunConfig, RunResult, DuelConfig, DuelResult } from './types/game';

export default function App() {
  const [screen, setScreen] = useState<ScreenId>('main-menu');
  const [fading, setFading] = useState(false);
  const [showNavRail, setShowNavRail] = useState(false);

  // Single player state
  const [runConfig, setRunConfig] = useState<RunConfig | null>(null);
  const [activeBoons, setActiveBoons] = useState<string[]>([]);
  const [currentWave, setCurrentWave] = useState(1);
  const [lastResult, setLastResult] = useState<RunResult | null>(null);

  // 1v1 PvP Duel state
  const [duelConfig, setDuelConfig] = useState<DuelConfig | null>(null);
  const [duelResult, setDuelResult] = useState<DuelResult | null>(null);

  const navigate = useCallback((to: ScreenId | string) => {
    setScreen(prev => {
      if (prev === (to as ScreenId)) return prev;
      return prev; // handled via fading below
    });
    setFading(true);
    setTimeout(() => {
      setScreen(to as ScreenId);
      setFading(false);
    }, 140);
  }, []);

  const handleStartRun = useCallback((config: RunConfig) => {
    setRunConfig(config);
    setActiveBoons([]);
    setCurrentWave(config.startWave || 1);
  }, []);

  const handleWaveComplete = useCallback((wave: number) => {
    setCurrentWave(wave);
    setScreen('boon-select');
  }, []);

  const handleClaimBoon = useCallback((boonId: string) => {
    setActiveBoons(prev => [...prev, boonId]);
  }, []);

  const handleSingleGameOver = useCallback((result: RunResult) => {
    setLastResult(result);
    // Update progression
    const current = getProgression();
    if (result.waveReached > current.lastWave) {
      saveProgression({ lastWave: result.waveReached });
    }

    // Submit score to backend
    const session = getSession();
    void submitScore({
      player_name: session?.user.player_name || 'Pilot',
      score: result.score,
      level_reached: result.waveReached,
      difficulty: result.difficulty,
      ship_class: result.shipId,
      kills: result.kills,
      total_damage: result.totalDamage,
      duration_seconds: result.durationSeconds,
    }).catch(() => {
      /* offline or network error allowed */
    });

    setScreen('game-over');
  }, []);

  const handleSingleVictory = useCallback((result: RunResult) => {
    setLastResult(result);
    const current = getProgression();
    saveProgression({
      lastWave: Math.max(current.lastWave, 20),
      completedRealms: Array.from(new Set([...current.completedRealms, 'dandaka'])),
    });

    const session = getSession();
    void submitScore({
      player_name: session?.user.player_name || 'Pilot',
      score: result.score,
      level_reached: 20,
      difficulty: result.difficulty,
      ship_class: result.shipId,
      kills: result.kills,
      total_damage: result.totalDamage,
      duration_seconds: result.durationSeconds,
    }).catch(() => {});

    setScreen('victory');
  }, []);

  const handleStartDuel = useCallback((config: DuelConfig) => {
    setDuelConfig(config);
    setDuelResult(null);
    setScreen('duel');
  }, []);

  const handleDuelOver = useCallback((res: DuelResult) => {
    setDuelResult(res);
  }, []);

  const handleDuelRematch = useCallback(() => {
    setDuelResult(null);
    setDuelConfig(prev => {
      if (!prev) return prev;
      return {
        ...prev,
        player1: { ...prev.player1, health: 100 },
        player2: { ...prev.player2, health: 100 },
      };
    });
  }, []);

  const props = { onNavigate: navigate };

  return (
    <div
      className="w-full h-full relative overflow-hidden"
      style={{ background: '#08090F', fontFamily: "'Rajdhani', sans-serif" }}
    >
      <div
        style={{
          width: '100%',
          height: '100%',
          opacity: fading ? 0 : 1,
          transition: 'opacity 0.14s ease',
        }}
      >
        {screen === 'main-menu' && <MainMenu {...props} />}
        {screen === 'ship-select' && <ShipSelect {...props} onStartRun={handleStartRun} />}
        {screen === 'boon-select' && (
          <BoonSelect {...props} currentWave={currentWave} onClaimBoon={handleClaimBoon} />
        )}
        {screen === 'game-hud' && (
          <PlayableArena
            mode="single"
            runConfig={runConfig || undefined}
            activeBoons={activeBoons}
            onNavigate={navigate}
            onWaveComplete={handleWaveComplete}
            onGameOver={handleSingleGameOver}
            onVictory={handleSingleVictory}
          />
        )}
        {screen === 'game-over' && <GameOver {...props} result={lastResult} />}
        {screen === 'victory' && <Victory {...props} result={lastResult} />}
        {screen === 'realm-map' && <RealmMap {...props} />}
        {screen === 'leaderboard' && <Leaderboard {...props} />}
        {screen === 'account' && <Account {...props} />}
        {screen === 'sangha' && <SanghaNetwork {...props} onStartDuel={handleStartDuel} />}
        {screen === 'duel' && (
          <div className="relative w-full h-full">
            <PlayableArena
              mode="duel"
              duelConfig={duelConfig || undefined}
              onNavigate={navigate}
              onDuelOver={handleDuelOver}
            />
            {duelResult && (
              <DuelResultModal
                result={duelResult}
                onRematch={handleDuelRematch}
                onNavigate={navigate}
              />
            )}
          </div>
        )}
        {screen === 'settings' && <Settings {...props} />}
        {screen === 'codex' && <Codex {...props} />}
      </div>

      {/* Dev / Showcase screen switcher toggle */}
      <div className="absolute bottom-1 right-2 z-50">
        <button
          onClick={() => setShowNavRail(!showNavRail)}
          className="text-[9px] px-2 py-0.5 rounded opacity-40 hover:opacity-100 transition-opacity"
          style={{ background: 'rgba(0,0,0,0.6)', color: '#8F98A8', border: '1px solid rgba(255,255,255,0.1)' }}
        >
          {showNavRail ? 'HIDE DEV NAV' : 'DEV NAV'}
        </button>
      </div>

      {showNavRail && <ScreenNav current={screen} onNavigate={navigate} />}
    </div>
  );
}
