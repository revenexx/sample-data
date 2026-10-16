// Illustrations for the office pack, keyed by SKU (variants included).
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.office;

// Cover colours for the ring binder variants: plain product colours, not a brand's.
const COVER = {
  model: [C.mid, C.body],
  blue: ['#2F5FA8', '#244D8A'],
  red: ['#B73A3A', '#942E2E'],
  black: ['#2A2D33', '#1C1F24'],
};

// Ring binder seen from the front, spine on the left. Lever arch uses the same
// body with a wider spine and a metal lever on top.
const binder = ([cover, spine], { lever = false, spineW = 30, badge } = {}) => tile(
  `<rect x="${140 - spineW}" y="104" width="${spineW}" height="222" rx="6" fill="${spine}"/>` +
  `<rect x="140" y="104" width="160" height="222" rx="8" fill="${cover}"/>` +
  `<rect x="${140 - spineW + 6}" y="132" width="${spineW - 12}" height="8" rx="3" fill="${C.light}"/>` +
  `<rect x="${140 - spineW + 6}" y="290" width="${spineW - 12}" height="8" rx="3" fill="${C.light}"/>` +
  `<rect x="164" y="170" width="112" height="60" rx="5" fill="#fff"/>` +
  `<rect x="164" y="170" width="8" height="60" rx="3" fill="${A}"/>` +
  `<rect x="186" y="186" width="70" height="8" rx="3" fill="${C.light}"/>` +
  `<rect x="186" y="202" width="48" height="8" rx="3" fill="${C.light}"/>` +
  `<rect x="174" y="250" width="92" height="10" rx="5" fill="${spine}" opacity="0.6"/>` +
  (lever
    ? `<rect x="${140 - spineW - 6}" y="86" width="${spineW + 40}" height="16" rx="6" fill="${C.metal}"/>` +
      `<rect x="${140 - spineW + 8}" y="96" width="${spineW - 16}" height="12" fill="${C.dark}"/>`
    : `<rect x="${140 - spineW - 8}" y="92" width="${spineW + 16}" height="14" rx="6" fill="${C.metal}"/>` +
      `<circle cx="${140 - spineW / 2}" cy="99" r="4" fill="${C.dark}"/>`),
  { badge, accent: A },
);

// A ballpoint pen or highlighter lying at an angle, ink-coloured body, pointed or chisel tip.
const pen = (x, y, angle, body, { chisel = false } = {}) =>
  `<g transform="translate(${x} ${y}) rotate(${angle})">` +
  `<rect x="0" y="-7" width="110" height="14" rx="7" fill="${body}"/>` +
  `<rect x="-14" y="-5" width="16" height="10" rx="3" fill="${C.dark}"/>` +
  (chisel
    ? `<path d="M-14 -5 l-6 6 h6 z" fill="${C.dark}"/>`
    : `<path d="M-14 -4 l-8 4 l8 4 z" fill="${C.dark}"/>`) +
  `<rect x="50" y="-7" width="46" height="5" rx="2" fill="#fff" opacity="0.45"/>` +
  `</g>`;

const paperRam = () => tile(
  `<path d="M110 150 L150 122 L330 122 L290 150 Z" fill="#FBFBFA" stroke="${C.light}" stroke-width="2"/>` +
  `<path d="M290 150 L330 122 L330 292 L290 320 Z" fill="#E4E7EB" stroke="${C.light}" stroke-width="2"/>` +
  [0, 1, 2, 3, 4].map((i) => `<path d="M294 ${162 + i * 30} L326 ${138 + i * 30}" stroke="${C.light}" stroke-width="2"/>`).join('') +
  `<rect x="110" y="150" width="180" height="170" rx="4" fill="#fff" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="110" y="262" width="180" height="18" fill="${A}"/>` +
  label(128, 184, 144, 46, 'A4 · 80 g', A, 22),
);

const pensBox = () => tile(
  `<path d="M120 216 L200 190 L280 216 L200 242 Z" fill="${C.paper}"/>` +
  `<path d="M120 216 L200 242 V318 L120 292 Z" fill="${C.paperDark}"/>` +
  `<path d="M280 216 L200 242 V318 L280 292 Z" fill="${C.paper}"/>` +
  `<g transform="translate(212 254) skewY(-21)">${label(0, 0, 60, 30, '50 ×', A, 17)}</g>` +
  pen(150, 206, -18, '#3558A8') + pen(186, 200, -8, '#3558A8') + pen(230, 204, 6, '#3558A8'),
);

const highlighters = () => tile(
  pen(92, 220, -28, '#F2D23C', { chisel: true }) +
  pen(120, 250, -18, '#7CD08A', { chisel: true }) +
  pen(150, 282, -10, '#F28BB0', { chisel: true }) +
  pen(190, 300, -4, '#6FA8DC', { chisel: true }),
);

const stickyNotes = () => tile(
  `<g transform="rotate(-8 200 240)"><rect x="128" y="158" width="140" height="140" rx="3" fill="#9ED9E8"/>` +
  `<rect x="128" y="158" width="140" height="14" fill="#7BC4D6"/></g>` +
  `<g transform="rotate(4 200 240)"><rect x="132" y="160" width="140" height="140" rx="3" fill="#F7B7C8"/>` +
  `<rect x="132" y="160" width="140" height="14" fill="#EC9BB3"/></g>` +
  `<g transform="rotate(-2 200 240)"><rect x="132" y="168" width="140" height="140" rx="3" fill="#F5E27A"/>` +
  `<rect x="132" y="168" width="140" height="14" fill="#E6CF57"/>` +
  `<rect x="146" y="200" width="88" height="7" rx="3" fill="#D9C15A"/><rect x="146" y="218" width="66" height="7" rx="3" fill="#D9C15A"/>` +
  `<rect x="146" y="236" width="78" height="7" rx="3" fill="#D9C15A"/></g>` +
  `<rect x="216" y="312" width="52" height="8" rx="4" fill="${A}"/>`,
);

const stapler = () => tile(
  `<rect x="88" y="266" width="224" height="36" rx="10" fill="${C.dark}"/>` +
  `<path d="M96 266 L262 196 Q300 184 308 222 L304 266 Z" fill="${C.body}"/>` +
  `<rect x="112" y="262" width="168" height="8" rx="3" fill="${C.mid}"/>` +
  `<rect x="236" y="232" width="34" height="9" rx="4" fill="${A}"/>` +
  `<rect x="130" y="300" width="140" height="6" rx="3" fill="${C.mid}"/>`,
);

const coffeeBag = () => tile(
  `<path d="M128 150 Q200 128 272 150 L284 322 Q200 336 116 322 Z" fill="${C.body}"/>` +
  `<path d="M128 150 Q200 128 272 150" fill="none" stroke="${C.mid}" stroke-width="6"/>` +
  `<rect x="150" y="162" width="100" height="6" rx="3" fill="${A}"/>` +
  label(150, 186, 100, 44, '1 kg', A, 22) +
  [[160, 262, 22], [200, 254, -14], [240, 266, 30], [188, 290, 8], [226, 300, -24]]
    .map(([x, y, r]) => `<g transform="translate(${x} ${y}) rotate(${r})"><ellipse rx="13" ry="9" fill="#6B4A32"/>` +
      `<path d="M-9 0 Q0 -4 9 0" stroke="#4A3324" stroke-width="2" fill="none"/></g>`).join(''),
);

const towels = () => tile(
  `<rect x="110" y="232" width="180" height="88" rx="6" fill="${C.paper}" stroke="${C.paperDark}" stroke-width="2"/>` +
  [0, 1, 2, 3, 4].map((i) => `<path d="M${122 + i * 34} 236 l 17 12 l 17 -12" stroke="${C.paperDark}" stroke-width="3" fill="none"/>`).join('') +
  `<rect x="126" y="272" width="148" height="30" rx="4" fill="#fff"/>` +
  `<rect x="126" y="272" width="8" height="30" rx="2" fill="${A}"/>` +
  `<rect x="124" y="156" width="152" height="70" rx="6" fill="${C.white}" stroke="${C.light}" stroke-width="2"/>` +
  [0, 1, 2, 3].map((i) => `<path d="M${136 + i * 36} 160 l 18 12 l 18 -12" stroke="${C.light}" stroke-width="3" fill="none"/>`).join(''),
);

const soapRefill = () => tile(
  `<rect x="162" y="96" width="76" height="34" rx="8" fill="${C.dark}"/>` +
  `<rect x="180" y="128" width="40" height="18" fill="${C.body}"/>` +
  `<rect x="128" y="142" width="144" height="186" rx="30" fill="#EEF1F4" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="128" y="142" width="144" height="16" rx="8" fill="${A}"/>` +
  label(150, 226, 100, 44, '5 l', A, 22) +
  `<path d="M252 190 q28 0 28 36 q0 36 -28 36" fill="none" stroke="${C.light}" stroke-width="10" stroke-linecap="round"/>`,
);

export const illustrations = {
  'DEMO-OFF-1001': paperRam(),
  'DEMO-OFF-1002': binder(COVER.model),
  'DEMO-OFF-1002-BLUE': binder(COVER.blue),
  'DEMO-OFF-1002-RED': binder(COVER.red),
  'DEMO-OFF-1002-BLACK': binder(COVER.black),
  'DEMO-OFF-1003': binder(['#D9DDE3', '#B9BFC8'], { lever: true, spineW: 44 }),
  'DEMO-OFF-2001': pensBox(),
  'DEMO-OFF-2002': highlighters(),
  'DEMO-OFF-2003': stickyNotes(),
  'DEMO-OFF-2004': stapler(),
  'DEMO-OFF-3001': coffeeBag(),
  'DEMO-OFF-3002': towels(),
  'DEMO-OFF-3003': soapRefill(),
};
