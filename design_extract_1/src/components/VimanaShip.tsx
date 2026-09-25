export type ShipId = 'pushpaka' | 'garuda' | 'nandi' | 'hamsa' | 'airavata';

export const SHIPS = [
  {
    id: 'pushpaka' as ShipId, name: 'Pushpaka', role: 'Celestial Cruiser', roleTag: 'BALANCED',
    stats: { hull: 80, velocity: 65, cannon: 60, dash: 55 },
    weapons: ['Kavach (120)', 'Soma (100)', 'Vajra (80)'],
    color: '#C0C8D8', accent: '#CC2020',
    lore: 'The sacred flying chariot of Kubera, repurposed as a multi-role combat platform.',
  },
  {
    id: 'garuda' as ShipId, name: 'Garuda', role: 'Attack Fighter', roleTag: 'ASSAULT',
    stats: { hull: 55, velocity: 95, cannon: 88, dash: 80 },
    weapons: ['Pasha (140)', 'Agni (110)', 'Sudarshana (90)'],
    color: '#D4A030', accent: '#FF8800',
    lore: "Modeled after Vishnu's divine eagle mount. Apex predator of the cosmic battlefield.",
  },
  {
    id: 'nandi' as ShipId, name: 'Nandi', role: 'Heavy Gunship', roleTag: 'TANK',
    stats: { hull: 120, velocity: 40, cannon: 75, dash: 30 },
    weapons: ['Trishula (180)', 'Pinaka (160)', 'Brahmastra (200)'],
    color: '#708090', accent: '#4488AA',
    lore: "Shiva's sacred bull incarnated as a siege platform. Unmovable, indestructible.",
  },
  {
    id: 'hamsa' as ShipId, name: 'Hamsa', role: 'Scout Skiff', roleTag: 'AGILITY',
    stats: { hull: 40, velocity: 100, cannon: 45, dash: 95 },
    weapons: ['Vayu (90)', 'Cakra (70)', 'Indrastra (85)'],
    color: '#90D0D8', accent: '#00E5FF',
    lore: "Brahma's divine swan, optimized for reconnaissance and lightning strike missions.",
  },
  {
    id: 'airavata' as ShipId, name: 'Airavata', role: 'Astral Bomber', roleTag: 'DEVASTATION',
    stats: { hull: 90, velocity: 50, cannon: 110, dash: 40 },
    weapons: ['Mahameru (220)', 'Pralaya (190)', 'Kalki (150)'],
    color: '#8060A8', accent: '#A020F0',
    lore: "Indra's celestial elephant reshaped into a payload carrier of apocalyptic yield.",
  },
];

const Pushpaka = () => (
  <svg viewBox="0 0 180 220" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="eng1" cx="50%" cy="50%"><stop offset="0%" stopColor="#00E5FF" stopOpacity="0.9"/>
        <stop offset="100%" stopColor="#00E5FF" stopOpacity="0"/></radialGradient>
      <linearGradient id="body1" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stopColor="#D8DCE8"/><stop offset="100%" stopColor="#A8B0C0"/></linearGradient>
    </defs>
    {/* left wing */}
    <path d="M90 55 L12 168 L46 168 L90 80 Z" fill="#B31C1C"/>
    <path d="M12 168 L46 168 L38 192 L4 192 Z" fill="#881414"/>
    <path d="M90 80 L46 168 L50 168 L90 90 Z" fill="#CC2020" opacity="0.4"/>
    {/* right wing */}
    <path d="M90 55 L168 168 L134 168 L90 80 Z" fill="#B31C1C"/>
    <path d="M168 168 L134 168 L142 192 L176 192 Z" fill="#881414"/>
    <path d="M90 80 L134 168 L130 168 L90 90 Z" fill="#CC2020" opacity="0.4"/>
    {/* body */}
    <path d="M76 22 L104 22 L114 190 L66 190 Z" fill="url(#body1)"/>
    <path d="M80 60 L100 60 L108 190 L72 190 Z" fill="#B8BCC8" opacity="0.3"/>
    {/* detail stripes */}
    <line x1="78" y1="85" x2="102" y2="85" stroke="#8090A0" strokeWidth="0.8" opacity="0.6"/>
    <line x1="76" y1="110" x2="104" y2="110" stroke="#8090A0" strokeWidth="0.8" opacity="0.6"/>
    <line x1="74" y1="140" x2="106" y2="140" stroke="#8090A0" strokeWidth="0.8" opacity="0.6"/>
    {/* cockpit */}
    <ellipse cx="90" cy="48" rx="16" ry="24" fill="#2860A8"/>
    <ellipse cx="90" cy="45" rx="11" ry="18" fill="#3878C8" opacity="0.7"/>
    <ellipse cx="90" cy="42" rx="7" ry="12" fill="#60A0E0" opacity="0.45"/>
    <ellipse cx="86" cy="38" rx="3" ry="5" fill="#80C0F8" opacity="0.35"/>
    {/* nose cap */}
    <path d="M78 20 L102 20 L100 32 L80 32 Z" fill="#586070"/>
    <path d="M84 14 L96 14 L96 20 L84 20 Z" fill="#404850"/>
    {/* engine nozzles */}
    <ellipse cx="80" cy="195" rx="9" ry="5" fill="#181C22"/>
    <ellipse cx="100" cy="195" rx="9" ry="5" fill="#181C22"/>
    <ellipse cx="80" cy="195" rx="6" ry="3" fill="url(#eng1)"/>
    <ellipse cx="100" cy="195" rx="6" ry="3" fill="url(#eng1)"/>
    <ellipse cx="80" cy="198" rx="7" ry="5" fill="#00E5FF" opacity="0.12"/>
    <ellipse cx="100" cy="198" rx="7" ry="5" fill="#00E5FF" opacity="0.12"/>
    {/* weapon hardpoints */}
    <rect x="60" y="130" width="5" height="22" fill="#404850" rx="1"/>
    <rect x="115" y="130" width="5" height="22" fill="#404850" rx="1"/>
    <rect x="57" y="150" width="11" height="3" fill="#2A3040"/>
    <rect x="112" y="150" width="11" height="3" fill="#2A3040"/>
  </svg>
);

const Garuda = () => (
  <svg viewBox="0 0 180 220" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="eng2" cx="50%" cy="50%"><stop offset="0%" stopColor="#FF8800" stopOpacity="0.9"/>
        <stop offset="100%" stopColor="#FF8800" stopOpacity="0"/></radialGradient>
    </defs>
    {/* swept back wings - more aggressive */}
    <path d="M90 40 L8 145 L35 145 L90 65 Z" fill="#D47820"/>
    <path d="M8 145 L35 145 L20 180 L0 180 Z" fill="#A06010"/>
    <path d="M90 40 L172 145 L145 145 L90 65 Z" fill="#D47820"/>
    <path d="M172 145 L145 145 L160 180 L180 180 Z" fill="#A06010"/>
    {/* fuselage - sleeker */}
    <path d="M80 15 L100 15 L108 185 L72 185 Z" fill="#C09030"/>
    <path d="M84 40 L96 40 L102 185 L78 185 Z" fill="#D4A840" opacity="0.3"/>
    {/* cockpit */}
    <ellipse cx="90" cy="38" rx="14" ry="22" fill="#804010"/>
    <ellipse cx="90" cy="35" rx="9" ry="15" fill="#A05020" opacity="0.7"/>
    <ellipse cx="90" cy="32" rx="5" ry="9" fill="#C07030" opacity="0.5"/>
    <path d="M80 12 L100 12 L98 22 L82 22 Z" fill="#504030"/>
    <path d="M86 6 L94 6 L94 14 L86 14 Z" fill="#384030"/>
    {/* cannons - forward mounted */}
    <rect x="64" y="60" width="4" height="40" fill="#604020" rx="1"/>
    <rect x="112" y="60" width="4" height="40" fill="#604020" rx="1"/>
    <rect x="62" y="98" width="8" height="3" fill="#402A10"/>
    <rect x="110" y="98" width="8" height="3" fill="#402A10"/>
    {/* engine */}
    <ellipse cx="82" cy="190" rx="8" ry="5" fill="#181008"/>
    <ellipse cx="98" cy="190" rx="8" ry="5" fill="#181008"/>
    <ellipse cx="82" cy="190" rx="5" ry="3" fill="url(#eng2)"/>
    <ellipse cx="98" cy="190" rx="5" ry="3" fill="url(#eng2)"/>
    <ellipse cx="82" cy="194" rx="6" ry="4" fill="#FF8800" opacity="0.1"/>
    <ellipse cx="98" cy="194" rx="6" ry="4" fill="#FF8800" opacity="0.1"/>
    {/* detail lines */}
    <line x1="82" y1="80" x2="98" y2="80" stroke="#806020" strokeWidth="0.8" opacity="0.6"/>
    <line x1="80" y1="110" x2="100" y2="110" stroke="#806020" strokeWidth="0.8" opacity="0.6"/>
  </svg>
);

const Nandi = () => (
  <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="eng3" cx="50%" cy="50%"><stop offset="0%" stopColor="#4488AA" stopOpacity="0.9"/>
        <stop offset="100%" stopColor="#4488AA" stopOpacity="0"/></radialGradient>
    </defs>
    {/* wide boxy wings */}
    <path d="M100 50 L10 130 L40 130 L100 70 Z" fill="#506070"/>
    <path d="M10 130 L40 130 L30 170 L5 170 Z" fill="#3A4A58"/>
    <path d="M100 50 L190 130 L160 130 L100 70 Z" fill="#506070"/>
    <path d="M190 130 L160 130 L170 170 L195 170 Z" fill="#3A4A58"/>
    {/* heavy boxy body */}
    <rect x="70" y="20" width="60" height="170" fill="#5A6878" rx="1"/>
    <rect x="76" y="26" width="48" height="158" fill="#4A5868" rx="1"/>
    {/* layered armor plates */}
    <rect x="72" y="60" width="56" height="8" fill="#6A7888" opacity="0.5"/>
    <rect x="72" y="90" width="56" height="8" fill="#6A7888" opacity="0.5"/>
    <rect x="72" y="120" width="56" height="8" fill="#6A7888" opacity="0.5"/>
    <rect x="72" y="150" width="56" height="8" fill="#6A7888" opacity="0.5"/>
    {/* cockpit - smaller, more armored */}
    <rect x="82" y="22" width="36" height="30" fill="#304860" rx="2"/>
    <rect x="86" y="26" width="28" height="22" fill="#3860A0" opacity="0.5" rx="1"/>
    {/* multi-weapon mounts */}
    <rect x="50" y="85" width="8" height="30" fill="#404850"/>
    <rect x="142" y="85" width="8" height="30" fill="#404850"/>
    <rect x="46" y="112" width="16" height="4" fill="#303840"/>
    <rect x="138" y="112" width="16" height="4" fill="#303840"/>
    <rect x="58" y="105" width="8" height="25" fill="#404850"/>
    <rect x="134" y="105" width="8" height="25" fill="#404850"/>
    {/* triple engines */}
    <ellipse cx="84" cy="192" rx="8" ry="5" fill="#181C22"/>
    <ellipse cx="100" cy="192" rx="8" ry="5" fill="#181C22"/>
    <ellipse cx="116" cy="192" rx="8" ry="5" fill="#181C22"/>
    <ellipse cx="84" cy="192" rx="5" ry="3" fill="url(#eng3)"/>
    <ellipse cx="100" cy="192" rx="5" ry="3" fill="url(#eng3)"/>
    <ellipse cx="116" cy="192" rx="5" ry="3" fill="url(#eng3)"/>
  </svg>
);

const Hamsa = () => (
  <svg viewBox="0 0 160 220" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="eng4" cx="50%" cy="50%"><stop offset="0%" stopColor="#00E5FF" stopOpacity="0.9"/>
        <stop offset="100%" stopColor="#00E5FF" stopOpacity="0"/></radialGradient>
    </defs>
    {/* ultra-thin swept wings */}
    <path d="M80 60 L10 140 L25 140 L80 75 Z" fill="#708898"/>
    <path d="M80 60 L150 140 L135 140 L80 75 Z" fill="#708898"/>
    <path d="M10 140 L25 140 L18 165 L5 165 Z" fill="#506070"/>
    <path d="M150 140 L135 140 L142 165 L155 165 Z" fill="#506070"/>
    {/* slim fuselage */}
    <path d="M72 18 L88 18 L94 200 L66 200 Z" fill="#90C0C8"/>
    <path d="M75 40 L85 40 L90 200 L70 200 Z" fill="#B0D8E0" opacity="0.25"/>
    {/* elongated cockpit */}
    <ellipse cx="80" cy="40" rx="11" ry="26" fill="#1860A8"/>
    <ellipse cx="80" cy="37" rx="7" ry="19" fill="#2880C8" opacity="0.7"/>
    <ellipse cx="80" cy="33" rx="4" ry="12" fill="#60B0E8" opacity="0.5"/>
    <ellipse cx="78" cy="29" rx="2" ry="6" fill="#90D0F8" opacity="0.35"/>
    {/* needle nose */}
    <path d="M75 16 L85 16 L82 6 L78 6 Z" fill="#506878"/>
    <path d="M78 6 L82 6 L81 0 L79 0 Z" fill="#405060"/>
    {/* single engine - narrow */}
    <ellipse cx="80" cy="202" rx="7" ry="4" fill="#181C22"/>
    <ellipse cx="80" cy="202" rx="5" ry="3" fill="url(#eng4)"/>
    <ellipse cx="80" cy="206" rx="6" ry="5" fill="#00E5FF" opacity="0.12"/>
    {/* detail lines */}
    <line x1="74" y1="90" x2="86" y2="90" stroke="#6090A8" strokeWidth="0.6" opacity="0.7"/>
    <line x1="73" y1="120" x2="87" y2="120" stroke="#6090A8" strokeWidth="0.6" opacity="0.7"/>
    <line x1="72" y1="155" x2="88" y2="155" stroke="#6090A8" strokeWidth="0.6" opacity="0.7"/>
  </svg>
);

const Airavata = () => (
  <svg viewBox="0 0 200 220" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <radialGradient id="eng5" cx="50%" cy="50%"><stop offset="0%" stopColor="#A020F0" stopOpacity="0.9"/>
        <stop offset="100%" stopColor="#A020F0" stopOpacity="0"/></radialGradient>
    </defs>
    {/* large angled wings with payload bays */}
    <path d="M100 45 L15 150 L50 150 L100 68 Z" fill="#604888"/>
    <path d="M15 150 L50 150 L40 185 L8 185 Z" fill="#482860"/>
    <path d="M100 45 L185 150 L150 150 L100 68 Z" fill="#604888"/>
    <path d="M185 150 L150 150 L160 185 L192 185 Z" fill="#482860"/>
    {/* wide boxy body - bomber style */}
    <path d="M76 15 L124 15 L130 200 L70 200 Z" fill="#785090"/>
    <path d="M82 22 L118 22 L124 200 L76 200 Z" fill="#6A4880" opacity="0.4"/>
    {/* payload bay doors */}
    <rect x="80" y="110" width="40" height="60" fill="#402860" rx="1"/>
    <line x1="100" y1="110" x2="100" y2="170" stroke="#A020F0" strokeWidth="0.8" opacity="0.5"/>
    <line x1="80" y1="140" x2="120" y2="140" stroke="#A020F0" strokeWidth="0.5" opacity="0.3"/>
    {/* cockpit */}
    <ellipse cx="100" cy="40" rx="18" ry="24" fill="#302060"/>
    <ellipse cx="100" cy="37" rx="12" ry="17" fill="#4030A0" opacity="0.6"/>
    <ellipse cx="100" cy="34" rx="7" ry="11" fill="#8060D0" opacity="0.4"/>
    <path d="M84 14 L116 14 L113 26 L87 26 Z" fill="#403050"/>
    {/* quad engines */}
    <ellipse cx="82" cy="202" rx="9" ry="5" fill="#1A1220"/>
    <ellipse cx="97" cy="202" rx="9" ry="5" fill="#1A1220"/>
    <ellipse cx="103" cy="202" rx="9" ry="5" fill="#1A1220"/>
    <ellipse cx="118" cy="202" rx="9" ry="5" fill="#1A1220"/>
    <ellipse cx="82" cy="202" rx="6" ry="3" fill="url(#eng5)"/>
    <ellipse cx="97" cy="202" rx="6" ry="3" fill="url(#eng5)"/>
    <ellipse cx="103" cy="202" rx="6" ry="3" fill="url(#eng5)"/>
    <ellipse cx="118" cy="202" rx="6" ry="3" fill="url(#eng5)"/>
    {/* armor plates */}
    <line x1="78" y1="70" x2="122" y2="70" stroke="#805098" strokeWidth="0.8" opacity="0.5"/>
    <line x1="76" y1="95" x2="124" y2="95" stroke="#805098" strokeWidth="0.8" opacity="0.5"/>
  </svg>
);

const SHIP_SVGS: Record<ShipId, React.FC> = {
  pushpaka: Pushpaka,
  garuda: Garuda,
  nandi: Nandi,
  hamsa: Hamsa,
  airavata: Airavata,
};

export default function VimanaShip({ id }: { id: ShipId }) {
  const Ship = SHIP_SVGS[id];
  return <Ship />;
}
