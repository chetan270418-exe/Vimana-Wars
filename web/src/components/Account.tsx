import { FormEvent, useEffect, useState } from 'react';
import Panel from './ui/Panel';
import VedicButton from './ui/VedicButton';
import StarField from './ui/StarField';
import {
  clearSession,
  getAccountStats,
  getCurrentUser,
  getSession,
  loginAccount,
  logoutAccount,
  registerAccount,
  requestPasswordReset,
  resetPassword,
  type User,
} from '../lib/api';

type Props = { onNavigate: (s: string) => void };
type AuthMode = 'login' | 'register' | 'reset';

function Field({ label, value, onChange, type = 'text', placeholder }: {
  label: string; value: string; onChange: (value: string) => void; type?: string; placeholder: string;
}) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-[9px] tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>{label}</span>
      <input
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={event => onChange(event.target.value)}
        className="w-full px-3 py-2.5 outline-none"
        style={{
          background: 'rgba(8,9,15,0.72)',
          border: '1px solid rgba(0,219,231,0.24)',
          color: '#FFF6DF',
          fontFamily: '"JetBrains Mono", monospace',
          fontSize: 12,
        }}
      />
    </label>
  );
}

export default function Account({ onNavigate }: Props) {
  const [mode, setMode] = useState<AuthMode>('login');
  const [user, setUser] = useState<User | null>(getSession()?.user ?? null);
  const [stats, setStats] = useState<Record<string, number | string> | null>(null);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [playerName, setPlayerName] = useState('');
  const [token, setToken] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!getSession()) return;
    getCurrentUser()
      .then(result => setUser(result.user))
      .catch(() => { clearSession(); setUser(null); });
  }, []);

  useEffect(() => {
    if (!user) { setStats(null); return; }
    getAccountStats().then(setStats).catch(() => setStats(null));
  }, [user]);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setBusy(true); setError(''); setMessage('');
    try {
      if (mode === 'login') {
        const result = await loginAccount(email.trim(), password);
        setUser(result.user);
        setMessage(`Welcome back, ${result.user.player_name}.`);
      } else if (mode === 'register') {
        const result = await registerAccount(email.trim(), password, playerName.trim() || 'Warrior');
        setUser(result.user);
        setMessage(result.verification_required
          ? 'Account created. Verify your email before production sign-in.'
          : `Game ID created: ${result.user.game_id}`);
        if (result.verification_token) setToken(result.verification_token);
      } else {
        if (!token.trim()) {
          const result = await requestPasswordReset(email.trim());
          setMessage(`${result.message}${result.reset_token ? ` Dev reset token: ${result.reset_token}` : ''}`);
        } else {
          const result = await resetPassword(token.trim(), password);
          setMessage(result.message);
          setMode('login'); setToken('');
        }
      }
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Account request failed');
    } finally { setBusy(false); }
  };

  const signOut = async () => {
    await logoutAccount();
    setUser(null); setStats(null); setMessage('Signed out. Progress remains on this device.');
  };

  return (
    <div className="relative w-full h-full overflow-hidden" style={{ background: '#08090F', paddingBottom: 40 }}>
      <StarField />
      <div className="absolute top-0 left-0 right-0 z-20 flex items-center gap-4 px-6" style={{ height: 52, borderBottom: '1px solid rgba(233,196,0,0.12)', background: 'rgba(8,9,15,0.86)', backdropFilter: 'blur(12px)' }}>
        <button onClick={() => onNavigate('main-menu')} className="text-[10px] tracking-[0.25em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>← MAIN MENU</button>
        <div className="h-4 w-px" style={{ background: 'rgba(233,196,0,0.2)' }} />
        <span className="text-sm tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>PILOT ACCOUNT</span>
      </div>

      <div className="relative z-10 h-full flex items-center justify-center overflow-y-auto" style={{ padding: '72px 24px 64px' }}>
        {!user ? (
          <Panel variant="selected" cut={14} className="w-full" style={{ maxWidth: 590 }}>
            <form onSubmit={submit} className="p-7 flex flex-col gap-5">
              <div>
                <div className="text-[9px] tracking-[0.4em] mb-2" style={{ fontFamily: '"Cinzel", serif', color: '#E9C400' }}>CLOUD COMMAND ID</div>
                <h1 className="text-2xl tracking-[0.16em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>
                  {mode === 'login' ? 'SIGN IN' : mode === 'register' ? 'CREATE GAME ID' : 'RECOVER ACCOUNT'}
                </h1>
                <p className="text-xs mt-2 leading-relaxed" style={{ color: '#D0C6AB' }}>
                  {mode === 'reset' ? 'Request a reset token, then submit it with a new password.' : 'Sync achievements, personal statistics, and Sangha matchmaking across devices.'}
                </p>
              </div>

              {mode === 'register' && <Field label="PILOT NAME" value={playerName} onChange={setPlayerName} placeholder="Your display name" />}
              <Field label="EMAIL" value={email} onChange={setEmail} type="email" placeholder="pilot@example.com" />
              {mode !== 'reset' && <Field label="PASSWORD" value={password} onChange={setPassword} type="password" placeholder="At least 8 characters" />}
              {mode === 'reset' && token.trim() && <Field label="NEW PASSWORD" value={password} onChange={setPassword} type="password" placeholder="At least 8 characters" />}

              {mode === 'reset' && !token.trim() && (
                <div className="text-[10px] leading-relaxed" style={{ color: '#8F98A8' }}>After the request, paste the token into the field below to set a new password.</div>
              )}
              {mode === 'reset' && <Field label="RESET TOKEN (OPTIONAL FOR REQUEST)" value={token} onChange={setToken} placeholder="Paste token when received" />}

              {error && <div className="text-xs leading-relaxed" style={{ color: '#FF6B72' }}>{error}</div>}
              {message && <div className="text-xs leading-relaxed" style={{ color: '#74F5FF' }}>{message}</div>}
              <VedicButton variant="primary" fullWidth disabled={busy}>
                {busy ? 'CONNECTING…' : mode === 'login' ? 'ENTER COMMAND' : mode === 'register' ? 'CREATE GAME ID' : token.trim() ? 'SET NEW PASSWORD' : 'SEND RESET TOKEN'}
              </VedicButton>

              <div className="flex flex-wrap gap-3 justify-center pt-1">
                <button type="button" onClick={() => { setMode('login'); setError(''); setMessage(''); }} className="text-[10px] tracking-wider" style={{ color: mode === 'login' ? '#E9C400' : '#8F98A8' }}>SIGN IN</button>
                <button type="button" onClick={() => { setMode('register'); setError(''); setMessage(''); }} className="text-[10px] tracking-wider" style={{ color: mode === 'register' ? '#E9C400' : '#8F98A8' }}>REGISTER</button>
                <button type="button" onClick={() => { setMode('reset'); setError(''); setMessage(''); }} className="text-[10px] tracking-wider" style={{ color: mode === 'reset' ? '#E9C400' : '#8F98A8' }}>FORGOT PASSWORD</button>
              </div>
            </form>
          </Panel>
        ) : (
          <div className="w-full flex flex-col gap-4" style={{ maxWidth: 760 }}>
            <Panel variant="selected" cut={14}>
              <div className="p-7 flex flex-wrap gap-6 items-center">
                <div className="w-14 h-14 flex items-center justify-center" style={{ border: '1px solid rgba(233,196,0,0.6)', color: '#E9C400', background: 'rgba(233,196,0,0.08)', fontFamily: '"JetBrains Mono", monospace' }}>ID</div>
                <div className="flex-1 min-w-[220px]">
                  <div className="text-[9px] tracking-[0.3em]" style={{ fontFamily: '"Cinzel", serif', color: '#8F98A8' }}>PILOT PROFILE</div>
                  <h1 className="text-2xl tracking-[0.15em] font-black" style={{ fontFamily: '"Cinzel", serif', color: '#FFF6DF' }}>{user.player_name.toUpperCase()}</h1>
                  <div className="text-xs mt-1" style={{ color: '#74F5FF', fontFamily: '"JetBrains Mono", monospace' }}>{user.game_id} · {user.email}</div>
                </div>
                <VedicButton variant="ghost" onClick={signOut}>SIGN OUT</VedicButton>
              </div>
            </Panel>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                ['GAMES', stats?.games ?? '—'], ['BEST SCORE', stats?.best_score ?? '—'], ['BEST WAVE', stats?.best_wave ?? '—'], ['ACHIEVEMENTS', stats?.achievements_unlocked ?? '—'],
              ].map(([label, value]) => (
                <Panel key={label} variant="dim" cut={8}><div className="p-4"><div className="text-[9px] tracking-[0.2em]" style={{ color: '#8F98A8' }}>{label}</div><div className="text-xl mt-2" style={{ color: '#FFF6DF', fontFamily: '"JetBrains Mono", monospace' }}>{String(value)}</div></div></Panel>
              ))}
            </div>
            <div className="flex flex-wrap gap-3 justify-end">
              <VedicButton variant="secondary" onClick={() => onNavigate('sangha')}>OPEN SANGHA NETWORK</VedicButton>
              <VedicButton variant="ghost" onClick={() => onNavigate('realm-map')}>VIEW CAMPAIGN</VedicButton>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
