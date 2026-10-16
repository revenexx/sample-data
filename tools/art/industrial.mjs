// Illustrations for the industrial pack, keyed by SKU.
import { C, ACCENT, tile, label } from './style.mjs';
import { illustrations as partA } from './industrial-a.mjs';
import { illustrations as partB } from './industrial-b.mjs';

const A = ACCENT.industrial;

const drill = (compact = false) => {
  const len = compact ? 150 : 190;
  const x0 = 200 - len / 2 - 20;
  return tile(
    // housing
    `<rect x="${x0}" y="118" width="${len}" height="62" rx="28" fill="${C.body}"/>` +
    `<rect x="${x0 + 14}" y="128" width="${len - 60}" height="10" rx="5" fill="${C.mid}"/>` +
    // chuck and bit
    (compact
      ? `<rect x="${x0 + len - 4}" y="132" width="26" height="34" rx="6" fill="${C.dark}"/>` +
        `<rect x="${x0 + len + 20}" y="142" width="34" height="14" rx="3" fill="${C.metal}"/>`
      : `<path d="M${x0 + len - 6} 128 h34 l14 10 v22 l-14 10 h-34 z" fill="${C.dark}"/>` +
        `<rect x="${x0 + len + 40}" y="144" width="54" height="10" rx="2" fill="${C.metal}"/>` +
        `<rect x="${x0 + len + 4}" y="128" width="6" height="42" fill="${A}"/>`) +
    // grip, trigger, battery
    `<path d="M${x0 + 52} 176 h52 l-10 112 h-40 z" fill="${C.body}"/>` +
    `<path d="M${x0 + 60} 190 h36 l-8 84 h-26 z" fill="${C.dark}"/>` +
    `<rect x="${x0 + 100}" y="182" width="12" height="30" rx="5" fill="${C.dark}"/>` +
    `<rect x="${x0 + 26}" y="284" width="112" height="44" rx="8" fill="${C.dark}"/>` +
    `<rect x="${x0 + 36}" y="296" width="44" height="8" rx="4" fill="${A}"/>`,
  );
};

const grinder = () => tile(
  `<rect x="96" y="168" width="196" height="56" rx="26" fill="${C.body}"/>` +
  `<rect x="112" y="178" width="120" height="10" rx="5" fill="${C.mid}"/>` +
  `<rect x="60" y="180" width="40" height="32" rx="12" fill="${C.dark}"/>` +
  `<path d="M286 150 h44 v92 h-44 z" fill="${C.dark}"/>` +
  `<ellipse cx="318" cy="246" rx="16" ry="74" fill="${C.metal}"/>` +
  `<ellipse cx="318" cy="246" rx="6" ry="20" fill="${C.mid}"/>` +
  `<path d="M300 176 a40 74 0 0 1 36 0 v34 h-36 z" fill="${C.light}"/>` +
  `<rect x="284" y="110" width="16" height="44" rx="7" fill="${C.dark}"/>` +
  `<rect x="140" y="214" width="60" height="8" rx="4" fill="${A}"/>`,
);

const battery = () => tile(
  `<rect x="112" y="150" width="176" height="150" rx="18" fill="${C.dark}"/>` +
  `<rect x="128" y="120" width="144" height="44" rx="10" fill="${C.body}"/>` +
  `<rect x="148" y="112" width="104" height="14" rx="4" fill="${C.mid}"/>` +
  `<rect x="132" y="190" width="136" height="44" rx="8" fill="${A}"/>` +
  `<text x="200" y="221" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="700" fill="#fff">18 V · 5.0 Ah</text>` +
  [0, 1, 2, 3].map((i) => `<circle cx="${172 + i * 18}" cy="262" r="5" fill="${i < 3 ? '#7CD08A' : C.mid}"/>`).join(''),
);

const box = (text, contents) => tile(
  `<path d="M96 170 L200 130 L304 170 L200 210 Z" fill="${C.paper}"/>` +
  `<path d="M96 170 L200 210 V320 L96 280 Z" fill="${C.paperDark}"/>` +
  `<path d="M304 170 L200 210 V320 L304 280 Z" fill="${C.paper}"/>` +
  `<g transform="translate(214 222) skewY(-21)">${label(0, 0, 80, 34, text, A, 17)}</g>` +
  contents,
);

const screw = (x, y, s = 1) =>
  `<g transform="translate(${x} ${y}) scale(${s})">` +
  `<path d="M-14 0 h28 l-10 10 h-8 z" fill="${C.metal}"/>` +
  `<rect x="-4" y="10" width="8" height="64" fill="${C.metal}"/>` +
  [0, 1, 2, 3, 4, 5].map((i) => `<path d="M-6 ${22 + i * 9} l12 -4" stroke="${C.mid}" stroke-width="2"/>`).join('') +
  `<path d="M-4 74 l4 12 l4 -12 z" fill="${C.metal}"/></g>`;

const bolt = (x, y, s = 1) =>
  `<g transform="translate(${x} ${y}) scale(${s})">` +
  `<path d="M-15 0 h30 v14 h-30 z" fill="${C.mid}"/><path d="M-15 0 h10 v14 h-10 z" fill="${C.metal}"/>` +
  `<rect x="-6" y="14" width="12" height="62" fill="${C.metal}"/>` +
  [0, 1, 2, 3, 4, 5, 6].map((i) => `<path d="M-6 ${24 + i * 8} l12 -4" stroke="${C.mid}" stroke-width="2"/>`).join('') +
  `</g>`;

const discs = () => tile(
  [0, 1, 2].map((i) =>
    `<ellipse cx="200" cy="${262 - i * 18}" rx="120" ry="44" fill="${i === 2 ? C.dark : C.body}"/>` +
    `<ellipse cx="200" cy="${256 - i * 18}" rx="120" ry="44" fill="${i === 2 ? C.mid : C.body}"/>`).join('') +
  `<ellipse cx="200" cy="220" rx="44" ry="16" fill="${A}"/>` +
  `<ellipse cx="200" cy="220" rx="16" ry="6" fill="${C.tile}"/>` +
  `<text x="200" y="196" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="#fff">125 × 1.0</text>`,
);

const glove = (badge) => tile(
  `<path d="M150 318 v-120 c0 -10 -6 -24 -14 -44 c-6 -14 8 -22 16 -10 l20 32 v-92 c0 -16 22 -16 22 0 v74 v-92 c0 -16 22 -16 22 0 v92 v-80 c0 -16 22 -16 22 0 v84 v-60 c0 -16 22 -16 22 0 v120 c0 20 -10 34 -10 36 v4 z" fill="${C.light}"/>` +
  `<path d="M150 270 h104 v48 h-104 z" fill="${C.light}"/>` +
  `<path d="M172 104 c0 -16 22 -16 22 0 v40 h-22 z M194 86 c0 -16 22 -16 22 0 v40 h-22 z M216 98 c0 -16 22 -16 22 0 v40 h-22 z M238 122 c0 -16 22 -16 22 0 v34 h-22 z" fill="${C.body}"/>` +
  `<path d="M150 296 h104 v22 h-104 z" fill="${A}"/>`,
  { badge, accent: A },
);

const glasses = () => tile(
  `<path d="M70 168 h260 v10 h-260 z" fill="${C.body}"/>` +
  `<path d="M84 176 h112 c4 0 8 6 6 16 l-12 52 c-4 16 -16 22 -32 22 h-34 c-16 0 -28 -10 -32 -26 l-10 -48 c-2 -10 2 -16 2 -16 z" fill="#BFD9EA" opacity="0.85"/>` +
  `<path d="M204 176 h112 c0 0 4 6 2 16 l-10 48 c-4 16 -16 26 -32 26 h-34 c-16 0 -28 -6 -32 -22 l-12 -52 c-2 -10 2 -16 6 -16 z" fill="#BFD9EA" opacity="0.85"/>` +
  `<path d="M112 196 l40 -12" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.7"/>` +
  `<path d="M232 196 l40 -12" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity="0.7"/>` +
  `<path d="M70 168 l-24 96" stroke="${C.dark}" stroke-width="10" stroke-linecap="round"/>` +
  `<path d="M330 168 l24 96" stroke="${C.dark}" stroke-width="10" stroke-linecap="round"/>` +
  `<rect x="186" y="164" width="28" height="14" rx="4" fill="${A}"/>`,
);

const earDefenders = () => tile(
  `<path d="M106 226 C106 96 294 96 294 226" fill="none" stroke="${C.dark}" stroke-width="22" stroke-linecap="round"/>` +
  `<path d="M106 226 C106 110 294 110 294 226" fill="none" stroke="${A}" stroke-width="6"/>` +
  `<rect x="72" y="200" width="70" height="112" rx="32" fill="${C.body}"/>` +
  `<rect x="258" y="200" width="70" height="112" rx="32" fill="${C.body}"/>` +
  `<rect x="128" y="212" width="20" height="88" rx="10" fill="${C.dark}"/>` +
  `<rect x="252" y="212" width="20" height="88" rx="10" fill="${C.dark}"/>`,
);

export const illustrations = {
  'DEMO-IND-1001': drill(false),
  'DEMO-IND-1002': drill(true),
  'DEMO-IND-1003': grinder(),
  'DEMO-IND-1004': battery(),
  'DEMO-IND-2001': box('4 × 40', screw(150, 196, 0.9) + screw(124, 210, 0.9)),
  'DEMO-IND-2002': box('M8 × 40', bolt(150, 190, 0.9) + bolt(122, 206, 0.9)),
  'DEMO-IND-2003': discs(),
  'DEMO-IND-3001': glove(),
  'DEMO-IND-3001-S': glove('S'),
  'DEMO-IND-3001-M': glove('M'),
  'DEMO-IND-3001-L': glove('L'),
  'DEMO-IND-3001-XL': glove('XL'),
  'DEMO-IND-3002': glasses(),
  'DEMO-IND-3003': earDefenders(),
  ...partA,
  ...partB,
};
