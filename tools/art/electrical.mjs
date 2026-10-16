// Illustrations for the electrical pack, keyed by SKU. Drawn from scratch:
// no brand marks, no certification marks.
import { C, ACCENT, tile, label } from './style.mjs';
import { illustrations as partA } from './electrical-a.mjs';
import { illustrations as partB } from './electrical-b.mjs';

const A = ACCENT.electrical;
const FONT = 'font-family="Helvetica, Arial, sans-serif"';

// A flat cable drum seen from above at an angle, with a sticker and a cable end.
const drum = (rx, ry, layers, text) => {
  const stack = Array.from({ length: layers }, (_, i) =>
    `<ellipse cx="200" cy="${206 + i * 7}" rx="${rx}" ry="${ry}" fill="${C.body}"/>`).join('');
  return tile(
    `<ellipse cx="200" cy="${206 + layers * 7}" rx="${rx - 4}" ry="${ry - 4}" fill="${C.dark}"/>` +
    stack +
    `<ellipse cx="200" cy="200" rx="${rx}" ry="${ry}" fill="${C.mid}"/>` +
    `<ellipse cx="200" cy="200" rx="${rx * 0.42}" ry="${ry * 0.42}" fill="${C.dark}"/>` +
    `<path d="M${200 + rx - 6} 196 q 26 -4 30 24 t 8 34 h 6" fill="none" stroke="${C.dark}" stroke-width="10" stroke-linecap="round"/>` +
    `<rect x="${200 - 46}" y="${200 - ry * 0.72}" width="92" height="28" rx="6" fill="${A}"/>` +
    `<text x="200" y="${200 - ry * 0.72 + 20}" text-anchor="middle" ${FONT} font-size="17" font-weight="700" fill="#fff">${text}</text>`,
  );
};

// A single-core wire on a small spool, seen from the front.
const spool = () => tile(
  `<rect x="150" y="150" width="100" height="180" fill="${C.light}"/>` +
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => `<line x1="150" y1="${162 + i * 16}" x2="250" y2="${162 + i * 16}" stroke="${C.mid}" stroke-width="5"/>`).join('') +
  `<rect x="112" y="118" width="22" height="236" rx="8" fill="${C.body}"/>` +
  `<rect x="266" y="118" width="22" height="236" rx="8" fill="${C.body}"/>` +
  `<path d="M250 318 q 30 10 30 -30" fill="none" stroke="${C.dark}" stroke-width="6" stroke-linecap="round"/>` +
  label(150, 120, 100, 34, '1 × 1.5', A, 18),
);

// A flush-mounted switch plate with a rocker.
const switchPlate = () => tile(
  `<rect x="128" y="112" width="144" height="168" rx="16" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<circle cx="200" cy="132" r="4" fill="${C.light}"/><circle cx="200" cy="260" r="4" fill="${C.light}"/>` +
  `<rect x="176" y="164" width="48" height="84" rx="12" fill="${C.body}"/>` +
  `<rect x="186" y="172" width="28" height="8" rx="4" fill="${A}"/>`,
);

// A cover frame for two inserts.
const coverFrame = () => tile(
  `<rect x="96" y="128" width="208" height="144" rx="18" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="126" y="156" width="66" height="88" rx="10" fill="${C.dark}"/>` +
  `<rect x="208" y="156" width="66" height="88" rx="10" fill="${C.dark}"/>` +
  `<rect x="262" y="248" width="30" height="6" rx="3" fill="${A}"/>`,
);

// A socket outlet in a given face colour. Earthing contacts stay visible.
const socket = (face, holes = C.mid, badge) => tile(
  `<rect x="126" y="110" width="148" height="148" rx="18" fill="${face}" stroke="${C.light}" stroke-width="2"/>` +
  `<circle cx="176" cy="184" r="10" fill="${holes}"/><circle cx="224" cy="184" r="10" fill="${holes}"/>` +
  `<circle cx="200" cy="222" r="12" fill="${holes}"/>` +
  `<rect x="182" y="244" width="36" height="6" rx="3" fill="${A}"/>`,
  { badge, accent: A },
);

// A surface-mounted junction box with a gasket line and cable entries.
const junctionBox = () => tile(
  `<rect x="112" y="150" width="176" height="138" rx="14" fill="${C.body}"/>` +
  `<rect x="112" y="150" width="176" height="36" rx="14" fill="${C.mid}"/>` +
  `<rect x="124" y="186" width="152" height="5" fill="${C.dark}"/>` +
  `<circle cx="132" cy="164" r="5" fill="${C.light}"/><circle cx="268" cy="164" r="5" fill="${C.light}"/>` +
  `<circle cx="152" cy="288" r="11" fill="${C.dark}"/><circle cx="200" cy="288" r="11" fill="${C.dark}"/><circle cx="248" cy="288" r="11" fill="${C.dark}"/>` +
  `<rect x="180" y="160" width="40" height="6" rx="3" fill="${A}"/>` +
  label(150, 206, 100, 30, 'IP55', A, 17),
);

// A flat LED ceiling panel, seen at an angle, with a thin edge.
const ledPanel = () => tile(
  `<polygon points="88,176 200,122 312,176 200,230" fill="${C.light}"/>` +
  `<polygon points="88,176 200,230 200,244 88,190" fill="${C.mid}"/>` +
  `<polygon points="200,230 312,176 312,190 200,244" fill="${C.body}"/>` +
  `<polygon points="120,176 200,138 280,176 200,214" fill="#FFFDF6"/>` +
  `<polygon points="200,214 280,176 280,180 200,218" fill="#EDEBE6"/>` +
  label(160, 252, 80, 30, '62 × 62', A, 17),
);

// A linear T8 tube with end caps.
const tube = () => tile(
  `<rect x="68" y="172" width="264" height="44" rx="22" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="90" y="186" width="220" height="16" rx="8" fill="#FFFDF6"/>` +
  `<rect x="52" y="168" width="18" height="52" rx="5" fill="${C.body}"/>` +
  `<rect x="330" y="168" width="18" height="52" rx="5" fill="${C.body}"/>` +
  `<rect x="180" y="228" width="40" height="6" rx="3" fill="${A}"/>`,
);

// A motion sensor: a dome lens with fan-shaped zones on a base plate.
const motion = () => tile(
  `<path d="M110 252 A90 90 0 0 1 290 252 Z" fill="${C.body}"/>` +
  `<path d="M150 252 A50 50 0 0 1 250 252 Z" fill="${C.mid}"/>` +
  [-60, -30, 0, 30, 60].map((a) => {
    const r = (a - 90) * Math.PI / 180;
    return `<line x1="200" y1="252" x2="${200 + 90 * Math.cos(r)}" y2="${252 + 90 * Math.sin(r)}" stroke="${C.light}" stroke-width="2" opacity="0.6"/>`;
  }).join('') +
  `<circle cx="200" cy="196" r="7" fill="${A}"/>` +
  `<rect x="100" y="252" width="200" height="20" rx="6" fill="${C.dark}"/>`,
);

const SOCKET_BLACK = '#1C1F24';
const SOCKET_ANTHRACITE = '#3A4046';

export const illustrations = {
  'DEMO-ELE-1001': drum(132, 58, 4, '3 × 1.5'),
  'DEMO-ELE-1002': drum(108, 46, 6, '5 × 2.5'),
  'DEMO-ELE-1003': spool(),
  'DEMO-ELE-2001': switchPlate(),
  'DEMO-ELE-2002': coverFrame(),
  'DEMO-ELE-2003': socket('#FFFFFF', C.mid),
  'DEMO-ELE-2003-WHITE': socket('#FFFFFF', C.mid),
  'DEMO-ELE-2003-BLACK': socket(SOCKET_BLACK, '#5B626D'),
  'DEMO-ELE-2003-ANTHRACITE': socket(SOCKET_ANTHRACITE, '#2A2F35'),
  'DEMO-ELE-2004': junctionBox(),
  'DEMO-ELE-3001': ledPanel(),
  'DEMO-ELE-3002': tube(),
  'DEMO-ELE-3003': motion(),
  ...partA,
  ...partB,
};
