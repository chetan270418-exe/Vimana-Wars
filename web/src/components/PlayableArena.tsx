import { useEffect, useRef, useState } from 'react';
import { CombatEngine } from '../game/combatEngine';
import type { RunConfig, RunResult, DuelConfig, DuelResult, ScreenId } from '../types/game';
import VedicButton from './ui/VedicButton';
import Panel from './ui/Panel';

interface PlayableArenaProps {
  mode: 'single' | 'duel';
  runConfig?: RunConfig;
  duelConfig?: DuelConfig;
  activeBoons?: string[];
  onNavigate: (s: ScreenId) => void;
  onWaveComplete?: (wave: number) => void;
  onGameOver?: (result: RunResult) => void;
  onVictory?: (result: RunResult) => void;
  onDuelOver?: (result: DuelResult) => void;
}

export default function PlayableArena({
  mode,
  runConfig,
  duelConfig,
  activeBoons,
  onNavigate,
  onWaveComplete,
  onGameOver,
  onVictory,
  onDuelOver,
}: PlayableArenaProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const engineRef = useRef<CombatEngine | null>(null);
  const [paused, setPaused] = useState(false);

  useEffect(() => {
    if (!canvasRef.current) return;

    const engine = new CombatEngine({
      canvas: canvasRef.current,
      mode,
      runConfig,
      duelConfig,
      activeBoons,
      onWaveComplete,
      onGameOver,
      onVictory,
      onDuelOver,
      onPauseToggle: (isPaused) => setPaused(isPaused),
    });

    engineRef.current = engine;

    return () => {
      engine.destroy();
      engineRef.current = null;
    };
  }, [mode, runConfig, duelConfig, activeBoons, onWaveComplete, onGameOver, onVictory, onDuelOver]);

  const handleResume = () => {
    engineRef.current?.resume();
    setPaused(false);
  };

  const handleAbandon = () => {
    engineRef.current?.destroy();
    onNavigate('main-menu');
  };

  return (
    <div className="relative w-full h-full overflow-hidden select-none" style={{ background: '#060810' }}>
      {/* Top command bar */}
      <div
        className="absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-6 pointer-events-auto"
        style={{
          height: 48,
          background: 'rgba(8, 9, 15, 0.75)',
          borderBottom: '1px solid rgba(233, 196, 0, 0.15)',
          backdropFilter: 'blur(8px)',
        }}
      >
        <div className="flex items-center gap-3">
          <button
            onClick={() => engineRef.current?.togglePause()}
            className="text-[10px] tracking-[0.25em] px-2 py-1 transition-colors hover:text-gold"
            style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8', border: '1px solid rgba(143,152,168,0.3)' }}
          >
            {paused ? 'RESUME [ESC]' : 'PAUSE [ESC]'}
          </button>
          <span className="text-xs tracking-[0.2em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
            {mode === 'duel' ? '⚔ 1V1 DUEL ARENA' : `CELESTIAL COMBAT · WAVE ${runConfig?.startWave || 1}`}
          </span>
        </div>

        <div className="text-[10px] tracking-wider hidden sm:block" style={{ fontFamily: '"JetBrains Mono", monospace', color: '#74F5FF' }}>
          {mode === 'duel'
            ? 'P1: [W A S D] + [SPACE] | P2: [ARROWS] + [ENTER]'
            : 'STEER: [W A S D / ARROWS] · FIRE: [SPACE] · DASH: [SHIFT]'}
        </div>
      </div>

      {/* Main Canvas */}
      <canvas
        ref={canvasRef}
        className="w-full h-full block"
        style={{ touchAction: 'none' }}
      />

      {/* Pause Overlay Modal */}
      {paused && (
        <div className="absolute inset-0 z-30 flex items-center justify-center bg-black/75 backdrop-blur-sm">
          <Panel variant="selected" cut={14} style={{ maxWidth: 420, width: '90%' }}>
            <div className="p-7 flex flex-col items-center text-center gap-4">
              <div className="text-[9px] tracking-[0.4em]" style={{ fontFamily: '"Cinzel", serif', color: '#E9C400' }}>
                TACTICAL COMMUNION
              </div>
              <h2 className="text-2xl font-black tracking-[0.2em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
                BATTLE SUSPENDED
              </h2>
              <p className="text-xs leading-relaxed" style={{ color: '#D0C6AB' }}>
                Vimana thrusters idle in orbit. Choose your directive:
              </p>

              <div className="flex flex-col gap-3 w-full mt-2">
                <VedicButton variant="primary" fullWidth onClick={handleResume}>
                  RESUME COMBAT ▶
                </VedicButton>
                <VedicButton variant="ghost" fullWidth onClick={handleAbandon}>
                  ABANDON TO MAIN MENU
                </VedicButton>
              </div>
            </div>
          </Panel>
        </div>
      )}
    </div>
  );
}
