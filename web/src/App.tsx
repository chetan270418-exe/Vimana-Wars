import { useState } from 'react';
import MainMenu from './components/MainMenu';
import ShipSelect from './components/ShipSelect';
import BoonSelect from './components/BoonSelect';
import GameHUD from './components/GameHUD';
import GameOver from './components/GameOver';
import Victory from './components/Victory';
import RealmMap from './components/RealmMap';
import Leaderboard from './components/Leaderboard';
import Settings from './components/Settings';
import Codex from './components/Codex';
import Account from './components/Account';
import SanghaNetwork from './components/SanghaNetwork';
import ScreenNav from './components/ui/ScreenNav';

export default function App() {
  const [screen, setScreen] = useState('main-menu');
  const [fading, setFading] = useState(false);

  const navigate = (to: string) => {
    if (to === screen) return;
    setFading(true);
    setTimeout(() => {
      setScreen(to);
      setFading(false);
    }, 160);
  };

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
          transition: 'opacity 0.16s ease',
        }}
      >
        {screen === 'main-menu'  && <MainMenu  {...props} />}
        {screen === 'ship-select'&& <ShipSelect {...props} />}
        {screen === 'boon-select'&& <BoonSelect {...props} />}
        {screen === 'game-hud'   && <GameHUD   {...props} />}
        {screen === 'game-over'  && <GameOver  {...props} />}
        {screen === 'victory'    && <Victory   {...props} />}
        {screen === 'realm-map'  && <RealmMap  {...props} />}
        {screen === 'leaderboard'&& <Leaderboard {...props} />}
        {screen === 'account'   && <Account   {...props} />}
        {screen === 'sangha'    && <SanghaNetwork {...props} />}
        {screen === 'settings'   && <Settings  {...props} />}
        {screen === 'codex'      && <Codex     {...props} />}
      </div>

      <ScreenNav current={screen} onNavigate={navigate} />
    </div>
  );
}
