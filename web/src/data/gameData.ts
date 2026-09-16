const ASSET = 'https://raw.githubusercontent.com/chetan270418-exe/Vimana-Wars/main/assets/images/';

export type Ship = {
  id: string;
  name: string;
  shipClass: string;
  lore: string;
  stats: { speed: number; firepower: number; armor: number; shield: number; agility: number };
  weapon: string;
  ability: string;
  img: string;
  color: string;
};

export const SHIPS: Ship[] = [
  {
    id: 'pushpaka',
    name: 'Pushpaka',
    shipClass: 'Celestial Carrier',
    lore: 'The original divine vimana gifted to Kubera by Vishwakarma. Retrofitted with tri-axial plasma cannons and a regenerating divine barrier system.',
    stats: { speed: 55, firepower: 70, armor: 82, shield: 88, agility: 48 },
    weapon: 'Brahmastra Cannon',
    ability: 'Divine Barrier',
    img: `${ASSET}pushpaka.png`,
    color: '#E9C400',
  },
  {
    id: 'garuda',
    name: 'Garuda',
    shipClass: 'Aerial Assault',
    lore: 'Modeled after the divine eagle of Vishnu. Supreme velocity and piercing solar bolts that dissolve Asura formations before they can return fire.',
    stats: { speed: 92, firepower: 78, armor: 55, shield: 60, agility: 95 },
    weapon: 'Solar Lance Array',
    ability: 'Gale Dive',
    img: `${ASSET}garuda.png`,
    color: '#FFD060',
  },
  {
    id: 'tripura',
    name: 'Tripura',
    shipClass: 'Siege Platform',
    lore: 'Replicates the three flying cities annihilated by Shiva. Overwhelming sustained barrage from triple barrels — slow, devastating, unstoppable.',
    stats: { speed: 40, firepower: 96, armor: 75, shield: 70, agility: 35 },
    weapon: 'Triple Agni Mortars',
    ability: 'Triple Convergence',
    img: `${ASSET}tripura.png`,
    color: '#FF6B30',
  },
  {
    id: 'naga',
    name: 'Naga',
    shipClass: 'Venom Stalker',
    lore: 'Engineered from the scales of the cosmic serpent Vasuki. Toxic payload systems erode enemy shields before the killing blow.',
    stats: { speed: 72, firepower: 68, armor: 60, shield: 55, agility: 80 },
    weapon: 'Venom Torpedoes',
    ability: 'Serpent Coil',
    img: `${ASSET}naga.png`,
    color: '#40E090',
  },
  {
    id: 'vajra',
    name: 'Vajra',
    shipClass: 'Storm Striker',
    lore: "Forged from the bones of the sage Dadhichi. Indra's own weapon of lightning, scaled for orbital warfare and chain-discharge combat.",
    stats: { speed: 80, firepower: 90, armor: 62, shield: 72, agility: 75 },
    weapon: 'Thunderbolt Cannon',
    ability: 'Storm Cascade',
    img: `${ASSET}vajra.png`,
    color: '#7EA8FF',
  },
  {
    id: 'soma',
    name: 'Soma',
    shipClass: 'Support Carrier',
    lore: 'Named after the moon deity and nectar of immortality. Deploys amrita healing pods and amplifies allied systems in co-op engagements.',
    stats: { speed: 58, firepower: 45, armor: 70, shield: 95, agility: 62 },
    weapon: 'Amrita Projector',
    ability: 'Lunar Renewal',
    img: `${ASSET}soma.png`,
    color: '#C0C8FF',
  },
  {
    id: 'kubera',
    name: 'Kubera',
    shipClass: 'Heavy Fortress',
    lore: "The treasury of the gods rendered as armor. Virtually impenetrable plating makes it the ultimate last line of defense against Ravana's elites.",
    stats: { speed: 35, firepower: 75, armor: 98, shield: 90, agility: 30 },
    weapon: 'Ratna Siege Gun',
    ability: 'Fortress Mode',
    img: `${ASSET}kubera.png`,
    color: '#E8A020',
  },
  {
    id: 'surya',
    name: 'Surya',
    shipClass: 'Solar Radiant',
    lore: 'The chariot of the sun god remade as a weapon of purification. Solar flares cascade across Asura hordes, stripping shields and scorching hulls.',
    stats: { speed: 68, firepower: 88, armor: 65, shield: 75, agility: 70 },
    weapon: 'Solar Flare Burst',
    ability: 'Radiance Surge',
    img: `${ASSET}surya.png`,
    color: '#FFAA00',
  },
];

export type Boon = {
  id: string;
  deity: string;
  symbol: string;
  name: string;
  description: string;
  effect: string;
  color: string;
};

export const BOONS: Boon[] = [
  {
    id: 'vishnu-blessing',
    deity: 'VISHNU',
    symbol: '⊕',
    name: 'Preservation Shield',
    description: 'The Preserver extends divine protection. Hull regenerates 2% per second between enemy waves and critical hits trigger an emergency micro-barrier.',
    effect: '+2% HP regen · Critical shield on low HP',
    color: '#7EA8FF',
  },
  {
    id: 'shiva-power',
    deity: 'SHIVA',
    symbol: '☽',
    name: "Destroyer's Fury",
    description: 'Channel the third eye of the Destroyer. All weapons deal 25% increased damage and enemy projectiles slow by 15% for three waves.',
    effect: '+25% weapon damage (3 waves)',
    color: '#FF6B72',
  },
  {
    id: 'brahma-wisdom',
    deity: 'BRAHMA',
    symbol: '◎',
    name: "Creator's Foresight",
    description: 'The Creator reveals hidden enemy patterns. All elite Asuras are marked with tactical outlines for 5 waves — no ambush is possible.',
    effect: 'Elite enemies marked for 5 waves',
    color: '#E9C400',
  },
  {
    id: 'indra-storm',
    deity: 'INDRA',
    symbol: '⚡',
    name: 'Vajra Overcharge',
    description: "Indra channels storm energy into your weapon systems. Each hit chains lightning to 2 nearby enemies, clearing dense formations.",
    effect: 'Shots chain to 2 nearby enemies',
    color: '#74F5FF',
  },
  {
    id: 'kali-wrath',
    deity: 'KALI',
    symbol: '✦',
    name: 'Dark Time Rift',
    description: 'The goddess of time tears the battlefield apart. Critical hits deal 3x damage and your movement speed surges for 1 second after each kill.',
    effect: 'Critical multiplier 2x → 3x',
    color: '#C040FF',
  },
  {
    id: 'saraswati-flow',
    deity: 'SARASWATI',
    symbol: '≋',
    name: 'River of Light',
    description: 'The goddess of knowledge optimizes your targeting systems. Accuracy increases by 40% and weapon spread reduces by 20%.',
    effect: '+40% accuracy, -20% spread',
    color: '#40E090',
  },
];

export type Realm = {
  id: string;
  name: string;
  waves: string;
  description: string;
  bossName: string;
  bossImg?: string;
  accentColor: string;
  x: number;
  y: number;
  transmission: { speaker: string; title: string; body: string };
};

export const REALMS: Realm[] = [
  {
    id: 'swarga',
    name: 'Swarga',
    waves: '1–3',
    description: 'The celestial realm of Indra. Golden spires pierce the clouds as Asura raiders breach the divine borders for the first time in an age.',
    bossName: "Indra's Vanguard",
    accentColor: '#78C8FF',
    x: 10,
    y: 72,
    transmission: { speaker: 'COMMANDER TARA', title: 'THE FIRST SIGNAL', body: 'The border beacons are burning. Hold Swarga long enough for the celestial fleet to wake.' },
  },
  {
    id: 'kshira-sagara',
    name: 'Kshira Sagara',
    waves: '4–6',
    description: 'The cosmic ocean of milk. Vritra the storm serpent has poisoned the sacred waters and commands the deep-space aquatic legions.',
    bossName: 'Vritra',
    bossImg: `${ASSET}boss_vritra.png`,
    accentColor: '#50F0DC',
    x: 25,
    y: 55,
    transmission: { speaker: 'VARUNA', title: 'A POISONED OCEAN', body: 'Vritra has turned the milk sea against us. Follow the current and cut the serpent off from the deep.' },
  },
  {
    id: 'dandaka',
    name: 'Dandaka Void',
    waves: '7–9',
    description: 'A haunted nebula dense with ancient darkness. Kumbhakarna and his sleeping army have awakened, filling the void with dread.',
    bossName: 'Kumbhakarna',
    bossImg: `${ASSET}boss_kumbhakarna.png`,
    accentColor: '#D264FF',
    x: 42,
    y: 62,
    transmission: { speaker: 'SAGE AGASTYA', title: 'THE SLEEPER AWAKENS', body: 'The Dandaka Void remembers every fear. Kumbhakarna is awake; your light is the only map home.' },
  },
  {
    id: 'lanka',
    name: 'Lanka',
    waves: '10–12',
    description: "The island fortress of Ravana remade in orbit. The ten-headed demon king commands his finest elite battalions in a final stand.",
    bossName: 'Ravana',
    bossImg: `${ASSET}boss_ravana.png`,
    accentColor: '#FF4646',
    x: 56,
    y: 44,
    transmission: { speaker: 'VIBHISHANA', title: 'THE TENFOLD CROWN', body: 'Lanka is no longer a fortress below the clouds. Ravana has raised it into orbit, and every gun is aimed at Dharma.' },
  },
  {
    id: 'setu',
    name: 'Setu Expanse',
    waves: '13–15',
    description: "The cosmic causeway between worlds. Mahishasura's buffalo war-legions charge across the bridge in unstoppable numbers.",
    bossName: 'Mahishasura',
    bossImg: `${ASSET}boss_mahishasura.png`,
    accentColor: '#FF9650',
    x: 70,
    y: 55,
    transmission: { speaker: 'HANUMAN', title: 'THE BRIDGE OF FIRE', body: 'The Setu is breaking piece by piece. Keep the causeway alive and the scattered worlds can still be joined.' },
  },
  {
    id: 'naraka',
    name: 'Naraka Forge',
    waves: '16–18',
    description: 'The hellfire foundry where Asura war machines are forged. Namuci commands the forge demons in the furnace at the edge of creation.',
    bossName: 'Namuci',
    accentColor: '#FF6428',
    x: 81,
    y: 40,
    transmission: { speaker: 'VISHWAKARMA', title: 'FORGE OF ASURA', body: 'Every war machine here was made from stolen celestial metal. Survive the furnace and reclaim the blueprint of the next age.' },
  },
  {
    id: 'mahayuddha',
    name: 'Mahayuddha Citadel',
    waves: '19–20',
    description: 'The final battlefield at the edge of creation. Hiranyakashipu himself descends from the void to annihilate all mortal resistance.',
    bossName: 'Hiranyakashipu',
    accentColor: '#FF50BE',
    x: 90,
    y: 25,
    transmission: { speaker: 'THE LAST ARCHIVIST', title: 'MAHAYUDDHA', body: 'There is no retreat beyond this citadel. Bring every boon, every lesson, and every liberated voice to the final sky.' },
  },
];

export type LeaderboardEntry = {
  rank: number;
  player: string;
  score: number;
  realmReached: string;
  ship: string;
  date: string;
  isCurrentPlayer?: boolean;
};

export const LEADERBOARD: LeaderboardEntry[] = [
  { rank: 1, player: 'ARJUNA_PRIME', score: 9847320, realmReached: 'Mahayuddha', ship: 'Garuda', date: '2026-09-14' },
  { rank: 2, player: 'KRISHNA_314', score: 8912440, realmReached: 'Mahayuddha', ship: 'Vajra', date: '2026-09-13' },
  { rank: 3, player: 'DRONA_ACE', score: 7654900, realmReached: 'Naraka Forge', ship: 'Tripura', date: '2026-09-15' },
  { rank: 4, player: 'KARNA_XV', score: 6341200, realmReached: 'Naraka Forge', ship: 'Surya', date: '2026-09-12' },
  { rank: 5, player: 'ABHIMANYU_S', score: 5877350, realmReached: 'Setu Expanse', ship: 'Naga', date: '2026-09-10' },
  { rank: 6, player: 'SATYAKI_7', score: 4932100, realmReached: 'Lanka', ship: 'Pushpaka', date: '2026-09-11' },
  { rank: 7, player: 'BHEEMA_88', score: 4100900, realmReached: 'Lanka', ship: 'Kubera', date: '2026-09-09' },
  { rank: 8, player: 'NAKULA_X', score: 3677200, realmReached: 'Dandaka Void', ship: 'Garuda', date: '2026-09-15' },
  { rank: 9, player: 'SAHADEVA_2', score: 2988400, realmReached: 'Dandaka Void', ship: 'Soma', date: '2026-09-08' },
  { rank: 10, player: 'YUDHISHTHIR', score: 2344100, realmReached: 'Kshira Sagara', ship: 'Vajra', date: '2026-09-14', isCurrentPlayer: true },
];
