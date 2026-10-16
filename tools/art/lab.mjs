// Illustrations for the lab pack, keyed by SKU (variants included).
// Drawn from scratch in the shared style; neutral product colours, the pack
// accent only as a small detail, no logos and no real product designs.
import { C, ACCENT, tile } from './style.mjs';
import { illustrations as partA } from './lab-a.mjs';
import { illustrations as partB } from './lab-b.mjs';

const A = ACCENT.lab;
const FONT = 'font-family="Helvetica, Arial, sans-serif"';

// Corner badge for a variant: wider than the shared badge so "1000 µl" fits.
const badgeTag = (text) =>
  `<g><rect x="262" y="24" width="118" height="40" rx="20" fill="${A}"/>` +
  `<text x="321" y="51" text-anchor="middle" ${FONT} font-size="21" font-weight="700" fill="#fff">${text}</text></g>`;

const microcentrifuge = () => tile(
  `<rect x="110" y="196" width="180" height="124" rx="16" fill="${C.body}"/>` +
  `<path d="M126 200 Q200 118 274 200 Z" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="184" rx="44" ry="20" fill="${C.dark}"/>` +
  `<ellipse cx="200" cy="184" rx="16" ry="7" fill="${C.mid}"/>` +
  `<rect x="126" y="282" width="148" height="28" rx="8" fill="${C.dark}"/>` +
  `<rect x="140" y="292" width="50" height="8" rx="3" fill="${C.mid}"/>` +
  `<circle cx="262" cy="296" r="6" fill="${A}"/>`,
);

const benchtop = () => tile(
  `<rect x="84" y="168" width="232" height="152" rx="18" fill="${C.body}"/>` +
  `<path d="M100 172 Q200 60 300 172 Z" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="146" rx="62" ry="26" fill="${C.dark}"/>` +
  `<ellipse cx="200" cy="146" rx="22" ry="9" fill="${C.mid}"/>` +
  `<rect x="100" y="280" width="200" height="30" rx="8" fill="${C.dark}"/>` +
  `<rect x="116" y="291" width="54" height="8" rx="3" fill="${C.mid}"/>` +
  `<circle cx="282" cy="295" r="6" fill="${A}"/>`,
);

const vortex = () => tile(
  `<rect x="112" y="300" width="176" height="26" rx="13" fill="${C.dark}"/>` +
  `<rect x="180" y="250" width="40" height="52" rx="8" fill="${C.body}"/>` +
  `<rect x="150" y="186" width="100" height="72" rx="16" fill="${C.body}"/>` +
  `<ellipse cx="200" cy="186" rx="58" ry="20" fill="${C.dark}"/>` +
  `<ellipse cx="200" cy="186" rx="34" ry="10" fill="${C.mid}"/>` +
  `<rect x="186" y="312" width="28" height="6" rx="3" fill="${A}"/>`,
);

const timer = () => tile(
  `<rect x="120" y="150" width="160" height="150" rx="26" fill="${C.body}"/>` +
  `<rect x="150" y="174" width="100" height="40" rx="8" fill="${C.dark}"/>` +
  `<rect x="164" y="186" width="72" height="8" rx="3" fill="${C.mid}"/>` +
  `<circle cx="200" cy="268" r="34" fill="${C.light}"/>` +
  `<path d="M200 268 V242" stroke="${C.dark}" stroke-width="5" stroke-linecap="round"/>` +
  `<path d="M200 268 L222 280" stroke="${A}" stroke-width="5" stroke-linecap="round"/>` +
  `<rect x="186" y="128" width="28" height="22" rx="6" fill="${C.dark}"/>`,
);

// Single-channel pipette, upright: plunger, volume window, barrel, tip.
const pipette = (badge) => tile(
  `<rect x="188" y="62" width="24" height="26" rx="8" fill="${C.dark}"/>` +
  `<rect x="180" y="84" width="40" height="24" rx="8" fill="${C.body}"/>` +
  `<rect x="176" y="108" width="48" height="110" rx="14" fill="${C.body}"/>` +
  `<rect x="186" y="128" width="28" height="22" rx="4" fill="${C.dark}"/>` +
  `<rect x="190" y="134" width="20" height="3" fill="${C.mid}"/>` +
  `<rect x="176" y="150" width="48" height="5" fill="${A}"/>` +
  `<rect x="184" y="218" width="32" height="44" rx="10" fill="${C.mid}"/>` +
  `<rect x="190" y="262" width="20" height="46" fill="${C.metal}"/>` +
  `<path d="M190 308 L210 308 L205 330 L195 330 Z" fill="${C.light}"/>`,
).replace('</svg>', `${badge ? badgeTag(badge) : ''}</svg>`);

// Tip rack: tips stand in a row, the rack in front.
const tipRack = () => {
  const tip = (x, y) =>
    `<path d="M${x - 16} ${y} h32 l-10 70 h-12 z" fill="${C.light}"/>` +
    `<path d="M${x - 2} ${y + 62} h4 v10 h-4 z" fill="${C.light}"/>`;
  const back = [60, 100, 140, 180, 220, 260, 300].map((x) => tip(x, 140).replace(new RegExp(C.light, 'g'), C.metal)).join('');
  const front = [80, 120, 160, 200, 240, 280, 320].map((x) => tip(x, 170)).join('');
  return tile(
    back +
    front +
    `<rect x="52" y="236" width="296" height="62" rx="8" fill="${C.body}"/>` +
    [0, 1, 2, 3, 4, 5, 6].map((i) => `<rect x="${72 + i * 40}" y="262" width="14" height="8" rx="3" fill="${C.dark}"/>`).join('') +
    `<rect x="132" y="246" width="136" height="12" rx="4" fill="${A}"/>`,
  );
};

// Microcentrifuge tube standing upright, centred on x.
const tube = (x, top, scale = 1, opts = {}) => {
  const w = 13 * scale, cap = 9 * scale;
  const capTop = top, bodyTop = top + 14 * scale, coneTop = top + 84 * scale, bottom = top + 102 * scale;
  return `<rect x="${x - w - 3}" y="${capTop}" width="${(w + 3) * 2}" height="${cap}" rx="3" fill="${opts.cap || C.dark}"/>` +
    `<rect x="${x - w - 3}" y="${capTop + cap - 3}" width="${(w + 3) * 2}" height="3" fill="${A}"/>` +
    `<rect x="${x - w}" y="${bodyTop}" width="${w * 2}" height="${coneTop - bodyTop}" fill="${opts.body || C.light}"/>` +
    `<path d="M${x - w} ${coneTop} h${w * 2} l${-w * 0.8} ${bottom - coneTop} h${-w * 0.4} z" fill="${opts.body || C.light}"/>` +
    `<rect x="${x - w + 3}" y="${bodyTop + 6}" width="4" height="${coneTop - bodyTop - 14}" rx="2" fill="${C.white}" opacity="0.8"/>`;
};

const bag = () => tile(
  `<path d="M92 168 h216 v146 q0 10 -10 10 h-196 q-10 0 -10 -10 z" fill="${C.paper}"/>` +
  `<path d="M92 168 h216 v20 h-216 z" fill="${C.paperDark}"/>` +
  `<rect x="150" y="216" width="100" height="56" rx="6" fill="#fff"/>` +
  `<rect x="150" y="216" width="8" height="56" rx="3" fill="${A}"/>` +
  `<text x="204" y="251" text-anchor="middle" ${FONT} font-size="20" font-weight="700" fill="${C.dark}">1.5 ml</text>` +
  tube(118, 170, 0.9) + tube(282, 176, 0.9),
);

const rack50 = () => tile(
  `<rect x="96" y="290" width="208" height="34" rx="8" fill="${C.body}"/>` +
  [0, 1, 2, 3, 4].map((i) => `<circle cx="${124 + i * 38}" cy="307" r="7" fill="${C.dark}"/>`).join('') +
  tube(160, 128, 1.6) + tube(240, 128, 1.6),
);

const dishes = () => tile(
  [0, 1, 2, 3].map((i) =>
    `<ellipse cx="200" cy="${306 - i * 24}" rx="118" ry="28" fill="${i % 2 ? C.light : C.metal}"/>` +
    `<ellipse cx="200" cy="${300 - i * 24}" rx="118" ry="28" fill="${C.light}"/>`).join('') +
  `<ellipse cx="200" cy="${300 - 3 * 24}" rx="44" ry="11" fill="${A}" opacity="0.85"/>` +
  `<ellipse cx="200" cy="${300 - 3 * 24}" rx="22" ry="5" fill="${C.white}"/>`,
  {},
);

const gloveBox = () => tile(
  `<path d="M120 190 L200 160 L280 190 L200 220 Z" fill="${C.paper}"/>` +
  `<path d="M120 190 L200 220 V320 L120 290 Z" fill="${C.paperDark}"/>` +
  `<path d="M280 190 L200 220 V320 L280 290 Z" fill="${C.paper}"/>` +
  `<g transform="translate(214 232) skewY(-21)"><rect width="56" height="30" rx="5" fill="#fff"/><rect width="6" height="30" rx="2" fill="${A}"/>` +
  `<text x="32" y="21" text-anchor="middle" ${FONT} font-size="15" font-weight="700" fill="${C.dark}">100 ×</text></g>` +
  `<path d="M160 190 v-64 c0 -12 20 -12 20 0 v58 M182 190 v-82 c0 -12 20 -12 20 0 v76 M204 190 v-76 c0 -12 20 -12 20 0 v70 M226 190 v-60 c0 -12 20 -12 20 0 v66" stroke="${C.light}" stroke-width="18" stroke-linecap="round" fill="none"/>` +
  `<path d="M150 176 h96 v22 h-96 z" fill="${C.light}"/>`,
);

export const illustrations = {
  'DEMO-LAB-1001': microcentrifuge(),
  'DEMO-LAB-1002': benchtop(),
  'DEMO-LAB-1003': vortex(),
  'DEMO-LAB-1004': timer(),
  'DEMO-LAB-2001': pipette(null),
  'DEMO-LAB-2001-10UL': pipette('10 µl'),
  'DEMO-LAB-2001-200UL': pipette('200 µl'),
  'DEMO-LAB-2001-1000UL': pipette('1000 µl'),
  'DEMO-LAB-2002': tipRack(),
  'DEMO-LAB-3001': bag(),
  'DEMO-LAB-3002': rack50(),
  'DEMO-LAB-3003': dishes(),
  'DEMO-LAB-3004': gloveBox(),
  ...partA,
  ...partB,
};
