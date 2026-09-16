import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import type { DuelResult, ScreenId } from '../types/game';

interface DuelResultModalProps {
  result: DuelResult;
  onRematch: () => void;
  onNavigate: (s: ScreenId) => void;
}

export default function DuelResultModal({ result, onRematch, onNavigate }: DuelResultModalProps) {
  const isP1Winner = result.winnerGameId === result.player1.gameId;
  const winner = isP1Winner ? result.player1 : result.player2;
  const loser = isP1Winner ? result.player2 : result.player1;

  return (
    <div className="absolute inset-0 z-40 flex items-center justify-center bg-black/85 backdrop-blur-md p-4">
      <Panel variant="selected" cut={14} style={{ maxWidth: 540, width: '100%' }}>
        <div className="p-8 flex flex-col items-center text-center gap-5">
          <div className="text-[10px] tracking-[0.4em]" style={{ fontFamily: '"Cinzel", serif', color: '#E9C400' }}>
            DUEL COMPLETED · 1V1 DOGFIGHT
          </div>

          <h1 className="text-3xl tracking-[0.18em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
            {winner.name.toUpperCase()} TRIUMPHS!
          </h1>

          <p className="text-sm leading-relaxed" style={{ color: '#D0C6AB' }}>
            Opponent vessel neutralized in celestial dogfight after {result.durationSeconds} seconds of combat.
          </p>

          {/* Duelists Stats Compare */}
          <div className="grid grid-cols-2 gap-4 w-full my-2">
            <div
              className="p-4 flex flex-col items-center gap-1 rounded"
              style={{
                background: isP1Winner ? 'rgba(233,196,0,0.12)' : 'rgba(255,255,255,0.04)',
                border: isP1Winner ? '1px solid #E9C400' : '1px solid rgba(143,152,168,0.2)',
              }}
            >
              <div className="text-[9px] tracking-widest text-[#8F98A8]">PILOT 1</div>
              <div className="text-base font-bold text-[#FFF6DF]">{result.player1.name}</div>
              <div className="text-xs text-[#E9C400] mt-1">{result.player1.shipId.toUpperCase()}</div>
              <div className="text-sm font-mono mt-2" style={{ color: result.player1.health > 0 ? '#30C846' : '#FF6B72' }}>
                {result.player1.health > 0 ? `${result.player1.health} HP REMAINING` : 'VESSEL DESTROYED'}
              </div>
            </div>

            <div
              className="p-4 flex flex-col items-center gap-1 rounded"
              style={{
                background: !isP1Winner ? 'rgba(233,196,0,0.12)' : 'rgba(255,255,255,0.04)',
                border: !isP1Winner ? '1px solid #E9C400' : '1px solid rgba(143,152,168,0.2)',
              }}
            >
              <div className="text-[9px] tracking-widest text-[#8F98A8]">PILOT 2</div>
              <div className="text-base font-bold text-[#FFF6DF]">{result.player2.name}</div>
              <div className="text-xs text-[#E9C400] mt-1">{result.player2.shipId.toUpperCase()}</div>
              <div className="text-sm font-mono mt-2" style={{ color: result.player2.health > 0 ? '#30C846' : '#FF6B72' }}>
                {result.player2.health > 0 ? `${result.player2.health} HP REMAINING` : 'VESSEL DESTROYED'}
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-3 justify-center w-full mt-2">
            <VedicButton variant="primary" onClick={onRematch}>
              REMATCH DUEL ⚔
            </VedicButton>
            <VedicButton variant="ghost" onClick={() => onNavigate('sangha')}>
              RETURN TO SANGHA LOBBY
            </VedicButton>
            <VedicButton variant="ghost" onClick={() => onNavigate('main-menu')}>
              MAIN MENU
            </VedicButton>
          </div>
        </div>
      </Panel>
    </div>
  );
}
