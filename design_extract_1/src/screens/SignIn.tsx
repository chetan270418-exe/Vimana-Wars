import { useState } from 'react';
import StarField from '../components/StarField';
import NeonPanel from '../components/NeonPanel';

type AuthTab = '1. SIGN IN' | '2. REGISTER' | '3. VERIFY' | '4. RESET PW';
const AUTH_TABS: AuthTab[] = ['1. SIGN IN', '2. REGISTER', '3. VERIFY', '4. RESET PW'];
const TAB_COLORS = ['gold', 'cyan', 'green', 'orange'] as const;

interface SignInProps {
  onBack: () => void;
}

export default function SignIn({ onBack }: SignInProps) {
  const [tab, setTab] = useState<AuthTab>('1. SIGN IN');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [callsign, setCallsign] = useState('');
  const [verifyCode, setVerifyCode] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  const tabIdx = AUTH_TABS.indexOf(tab);

  const handleSubmit = () => {
    setStatus('CONNECTING TO SANGHA ASTRAL NETWORK...');
    setTimeout(() => setStatus('OFFLINE MODE ACTIVE — SERVER UNREACHABLE'), 1500);
  };

  const inputClass = `w-full px-3 py-2.5 font-mono text-sm bg-card outline-none transition-all
    focus:border-[#00E5FF] focus:shadow-[0_0_8px_rgba(0,229,255,0.3)]`;

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ background: 'radial-gradient(ellipse 80% 70% at 50% 40%, #060E18 0%, #05080E 100%)' }}>
      <StarField count={100} />

      {/* Header */}
      <NeonPanel color="gold" corners={false} className="absolute top-0 left-0 right-0 px-6 py-3 z-10">
        <div className="font-display text-sm tracking-widest glow-gold" style={{ color: '#FFB800' }}>
          SANGHA ASTRAL PILOT NETWORK // CLOUD COMMAND
        </div>
      </NeonPanel>

      {/* Tabs */}
      <div className="absolute top-14 left-6 right-6 flex gap-2 z-10">
        {AUTH_TABS.map((t, i) => (
          <NeonPanel key={t} color={TAB_COLORS[i]} hover corners={false}
            onClick={() => { setTab(t); setStatus(null); }}
            className={`flex-1 py-2.5 text-center transition-all ${tab === t ? 'bg-[rgba(255,255,255,0.04)]' : ''}`}>
            <span className="font-body text-xs font-semibold tracking-widest"
              style={{ color: tab === t ? '#fff' : 'var(--muted-foreground)' }}>
              {t}
            </span>
          </NeonPanel>
        ))}
      </div>

      {/* Form area */}
      <div className="absolute inset-0 flex items-center justify-center pt-16">
        <div className="w-full max-w-md px-6">
          <NeonPanel color={TAB_COLORS[tabIdx]} className="p-6 space-y-4 animate-fade-up">

            {(tab === '1. SIGN IN' || tab === '2. REGISTER') && (
              <>
                <div>
                  <label className="font-mono text-[9px] tracking-widest text-muted-foreground block mb-1.5">
                    EMAIL ADDRESS
                  </label>
                  <input type="email" value={email} onChange={e => setEmail(e.target.value)}
                    className={inputClass}
                    style={{ border: '1px solid #FFB800', color: '#C0D0E0' }}
                    placeholder="pilot@celestial.net"/>
                </div>

                {tab === '2. REGISTER' && (
                  <div>
                    <label className="font-mono text-[9px] tracking-widest text-muted-foreground block mb-1.5">
                      CALLSIGN
                    </label>
                    <input type="text" value={callsign} onChange={e => setCallsign(e.target.value)}
                      className={inputClass}
                      style={{ border: '1px solid #00E5FF', color: '#C0D0E0' }}
                      placeholder="Enter your callsign"/>
                  </div>
                )}

                <div>
                  <label className="font-mono text-[9px] tracking-widest text-muted-foreground block mb-1.5">
                    PILOT PASSWORD
                  </label>
                  <div className="relative">
                    <input type={showPw ? 'text' : 'password'} value={password}
                      onChange={e => setPassword(e.target.value)}
                      className={inputClass + ' pr-20'}
                      style={{ border: '1px solid #162030', color: '#C0D0E0' }}
                      placeholder="Enter password"/>
                    <button onClick={() => setShowPw(p => !p)}
                      className="absolute right-2 top-1/2 -translate-y-1/2 font-mono text-[9px] tracking-widest
                        px-2 py-1 transition-colors hover:text-white"
                      style={{ color: '#4A6070', border: '1px solid #2A3A50' }}>
                      {showPw ? 'HIDE' : 'SHOW'}
                    </button>
                  </div>
                </div>

                {tab === '1. SIGN IN' && (
                  <div className="font-mono text-[9px] text-center" style={{ color: '#00FF88', opacity: 0.7 }}>
                    Sign in with your pilot credentials or play offline as guest
                  </div>
                )}

                <div className="space-y-2 pt-1">
                  <NeonPanel color="gold" hover corners={false} className="py-3.5 text-center"
                    onClick={handleSubmit}>
                    <span className="font-mono text-[10px] tracking-widest" style={{ color: '#FFB800' }}>
                      {tab === '1. SIGN IN' ? 'SIGN IN // CONNECT' : 'CREATE PILOT ACCOUNT'}
                    </span>
                  </NeonPanel>
                  {tab === '1. SIGN IN' && (
                    <NeonPanel color="cyan" hover corners={false} className="py-3.5 text-center">
                      <span className="font-mono text-[10px] tracking-widest" style={{ color: '#00E5FF' }}>
                        PLAY AS GUEST (OFFLINE)
                      </span>
                    </NeonPanel>
                  )}
                </div>
              </>
            )}

            {tab === '3. VERIFY' && (
              <>
                <div className="font-body text-sm text-center leading-relaxed" style={{ color: '#8090A8' }}>
                  Enter the 6-digit verification code sent to your registered email address.
                </div>
                <div>
                  <label className="font-mono text-[9px] tracking-widest text-muted-foreground block mb-1.5">
                    VERIFICATION CODE
                  </label>
                  <input type="text" value={verifyCode} onChange={e => setVerifyCode(e.target.value)}
                    className={inputClass + ' text-center text-xl tracking-[0.5em]'}
                    style={{ border: '1px solid #00FF88', color: '#00FF88' }}
                    placeholder="000000" maxLength={6}/>
                </div>
                <NeonPanel color="green" hover corners={false} className="py-3.5 text-center"
                  onClick={handleSubmit}>
                  <span className="font-mono text-[10px] tracking-widest" style={{ color: '#00FF88' }}>
                    VERIFY PILOT IDENTITY
                  </span>
                </NeonPanel>
              </>
            )}

            {tab === '4. RESET PW' && (
              <>
                <div className="font-body text-sm text-center leading-relaxed" style={{ color: '#8090A8' }}>
                  Enter your registered email to receive a password reset link.
                </div>
                <div>
                  <label className="font-mono text-[9px] tracking-widest text-muted-foreground block mb-1.5">
                    REGISTERED EMAIL
                  </label>
                  <input type="email" value={email} onChange={e => setEmail(e.target.value)}
                    className={inputClass}
                    style={{ border: '1px solid #FF6B00', color: '#C0D0E0' }}
                    placeholder="pilot@celestial.net"/>
                </div>
                <NeonPanel color="orange" hover corners={false} className="py-3.5 text-center"
                  onClick={handleSubmit}>
                  <span className="font-mono text-[10px] tracking-widest" style={{ color: '#FF6B00' }}>
                    SEND RESET LINK
                  </span>
                </NeonPanel>
              </>
            )}

            {/* Status message */}
            {status && (
              <div className="font-mono text-[9px] text-center animate-data-flicker"
                style={{ color: status.includes('UNREACHABLE') ? '#FF2244' : '#00E5FF' }}>
                {status}
              </div>
            )}
          </NeonPanel>
        </div>
      </div>

      {/* Back button + server info */}
      <div className="absolute bottom-5 left-6 right-6 flex items-center justify-between">
        <NeonPanel color="white" hover onClick={onBack} corners={false} className="px-8 py-3">
          <span className="font-mono text-[10px] tracking-widest text-muted-foreground">TITLE</span>
        </NeonPanel>
        <div className="font-mono text-[8px] tracking-widest" style={{ color: '#2A3A50' }}>
          SERVER: https://your-api-service.onrender.com
        </div>
      </div>
    </div>
  );
}
