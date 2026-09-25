import { useState } from 'react';
import SplashScreen from './screens/SplashScreen';
import MainMenu from './screens/MainMenu';
import CampaignMap from './screens/CampaignMap';
import VimanaHangar from './screens/VimanaHangar';
import AstralCodex from './screens/AstralCodex';
import SquadronMultiplayer from './screens/SquadronMultiplayer';
import SystemSettings from './screens/SystemSettings';
import SignIn from './screens/SignIn';

type Screen =
  | 'splash'
  | 'main-menu'
  | 'campaign-map'
  | 'vimana-hangar'
  | 'astral-codex'
  | 'squadron'
  | 'settings'
  | 'sign-in';

export default function App() {
  const [screen, setScreen] = useState<Screen>('splash');

  const nav = (s: string) => setScreen(s as Screen);
  const back = () => setScreen('main-menu');

  return (
    <div className="w-full h-full relative overflow-hidden"
      style={{ background: '#05080E', fontFamily: 'var(--font-mono)' }}>
      {screen === 'splash' && (
        <SplashScreen onComplete={() => setScreen('main-menu')} />
      )}
      {screen === 'main-menu' && (
        <MainMenu onNavigate={nav} />
      )}
      {screen === 'campaign-map' && (
        <CampaignMap onBack={back} onLaunch={() => setScreen('vimana-hangar')} />
      )}
      {screen === 'vimana-hangar' && (
        <VimanaHangar onBack={back} />
      )}
      {screen === 'astral-codex' && (
        <AstralCodex onBack={back} />
      )}
      {screen === 'squadron' && (
        <SquadronMultiplayer onBack={back} />
      )}
      {screen === 'settings' && (
        <SystemSettings onBack={back} />
      )}
      {screen === 'sign-in' && (
        <SignIn onBack={back} />
      )}
    </div>
  );
}
