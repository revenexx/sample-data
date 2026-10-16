// More industrial illustrations, keyed by SKU (part b). Same style as industrial.mjs.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.industrial;
const WOOD = '#C8A27A';
const WOOD_D = '#A9825A';
const ABR = '#B98D5E';
const ABR_L = '#D8B98E';

const hex = (cx, cy, r, fill) => {
  const pts = Array.from({ length: 6 }, (_, i) => {
    const a = (Math.PI / 3) * i;
    return `${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`;
  }).join(' ');
  return `<polygon points="${pts}" fill="${fill}"/>`;
};

const stroke = (d, w, col) =>
  `<path d="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;

// ---- tools -------------------------------------------------------------

// Socket case: a grid of sockets in a moulded tray. Drive size sets the socket size.
const socketSet = (cols, rows, r, count, text, bar = false) => {
  const step = 2 * r + 10;
  const W = cols * step + 30;
  const H = rows * step + 30;
  const x0 = 200 - W / 2 - (bar ? 20 : 0);
  const y0 = 318 - H;
  let s =
    `<rect x="${x0}" y="${y0}" width="${W}" height="${H}" rx="14" fill="${C.dark}"/>` +
    `<rect x="${x0 + 10}" y="${y0 + 10}" width="${W - 20}" height="${H - 20}" rx="8" fill="${C.light}"/>`;
  for (let i = 0; i < count; i++) {
    const cx = x0 + 15 + step / 2 + (i % cols) * step;
    const cy = y0 + 15 + step / 2 + Math.floor(i / cols) * step;
    s += hex(cx, cy, r, C.dark) + `<circle cx="${cx}" cy="${cy}" r="${(r * 0.35).toFixed(1)}" fill="${C.light}"/>`;
  }
  if (bar) {
    s +=
      `<rect x="${x0 + W - 8}" y="${y0 + H / 2 - 8}" width="60" height="16" rx="8" fill="${C.body}"/>` +
      `<circle cx="${x0 + W - 8}" cy="${y0 + H / 2}" r="16" fill="${C.body}"/>`;
  }
  s += label(x0, y0 - 34, 170, 26, text, A, 14);
  return tile(s);
};

// Open-end spanners lying in a stack, each a little shorter than the last.
const spannerSet = (count, text) => {
  let s = '';
  for (let i = 0; i < count; i++) {
    const y = 130 + i * 20;
    const len = 230 - i * 6;
    const x1 = 300 - len;
    const col = i % 3 === 2 ? C.mid : C.metal;
    s +=
      `<rect x="${x1}" y="${y - 5}" width="${len}" height="10" rx="5" fill="${col}"/>` +
      `<circle cx="${x1 + 12}" cy="${y}" r="11" fill="${col}"/>` +
      `<rect x="${x1 - 2}" y="${y - 5}" width="14" height="10" fill="${C.tile}"/>`;
  }
  s += label(150, 292, 100, 26, text, A, 15);
  return tile(s);
};

const screwdriverSet = () => {
  let s = `<rect x="84" y="296" width="232" height="26" rx="8" fill="${C.dark}"/>`;
  const handles = [C.body, C.mid, A, C.body, C.mid, C.dark];
  for (let i = 0; i < 6; i++) {
    const x = 110 + i * 34;
    const top = 110 + (i % 2) * 14 + i * 2;
    s +=
      `<rect x="${x - 3}" y="${top + 50}" width="6" height="${246 - top - 50}" fill="${C.metal}"/>` +
      `<rect x="${x - 13}" y="${top}" width="26" height="54" rx="12" fill="${handles[i]}"/>`;
  }
  return tile(s + label(146, 298, 108, 22, '6 pcs', A, 14));
};

const hexKeySet = () => {
  let s = `<rect x="96" y="296" width="208" height="22" rx="8" fill="${C.dark}"/>`;
  for (let i = 0; i < 9; i++) {
    const x = 118 + i * 20;
    const top = 170 + ((i * 37) % 5) * 12;
    s += stroke(`M${x} 296 V${top} H${x + 18}`, 9, i === 4 ? A : C.metal);
  }
  return tile(s + label(150, 298, 100, 22, '9 pcs', A, 14));
};

const pipeWrench = () => tile(
  `<rect x="150" y="298" width="170" height="22" rx="10" fill="${C.body}"/>` +
  `<rect x="290" y="298" width="12" height="22" rx="4" fill="${A}"/>` +
  `<rect x="96" y="236" width="80" height="86" rx="12" fill="${C.dark}"/>` +
  `<path d="M74 246 h26 v62 h-26 z" fill="${C.metal}"/>` +
  `<path d="M74 254 l22 8 M74 270 l22 8 M74 286 l22 8" stroke="${C.mid}" stroke-width="3"/>` +
  `<circle cx="126" cy="280" r="16" fill="${C.mid}"/>`,
);

// Plier family, drawn upright: jaws at the top, two long handles crossing at a round pivot (y=150).
const plierHandles = (cL, cR) =>
  stroke('M166 312 L200 150', 26, cL) + stroke('M234 312 L200 150', 26, cR) +
  stroke('M166 312 L176 262', 30, A) + stroke('M234 312 L223 262', 30, A);
const plierPivot = `<circle cx="200" cy="150" r="11" fill="${C.mid}"/><circle cx="200" cy="150" r="4" fill="${A}"/>`;

// Combination pliers: two flat parallel jaws with a few serrations.
const pliers = () => tile(
  plierHandles(C.body, C.dark) +
  `<rect x="184" y="94" width="14" height="58" rx="3" fill="${C.metal}" stroke="${C.mid}" stroke-width="2"/>` +
  `<rect x="202" y="94" width="14" height="58" rx="3" fill="${C.metal}" stroke="${C.mid}" stroke-width="2"/>` +
  [104, 114, 124, 134, 144].map((y) => `<path d="M186 ${y} H196 M204 ${y} H214" stroke="${C.mid}" stroke-width="2"/>`).join('') +
  plierPivot,
);

// Side cutters: two short pointed blades meeting in a V cutting edge.
const sideCutters = () => tile(
  plierHandles(C.body, C.dark) +
  `<path d="M186 150 L200 92 L203 122 L196 150 Z" fill="${C.metal}" stroke="${C.mid}" stroke-width="2" stroke-linejoin="round"/>` +
  `<path d="M214 150 L200 92 L197 122 L204 150 Z" fill="${C.metal}" stroke="${C.mid}" stroke-width="2" stroke-linejoin="round"/>` +
  plierPivot,
);

// Water pump pliers: wider open handles, one long straight jaw, one offset jaw set at an angle.
const pumpPliers = () => tile(
  stroke('M150 312 L200 150', 26, C.body) + stroke('M250 312 L200 150', 26, C.dark) +
  stroke('M150 312 L165 262', 30, A) + stroke('M250 312 L235 262', 30, A) +
  stroke('M200 150 L176 88', 16, C.metal) + stroke('M200 150 L238 98 L252 98', 16, C.metal) +
  plierPivot,
);

const hammer = () => tile(
  `<polygon points="186,160 214,160 218,322 182,322" fill="${WOOD}"/>` +
  `<rect x="118" y="118" width="164" height="42" rx="8" fill="${C.dark}"/>` +
  `<rect x="118" y="118" width="22" height="42" rx="6" fill="${C.mid}"/>` +
  `<rect x="250" y="118" width="8" height="42" fill="${A}"/>` +
  `<rect x="190" y="150" width="20" height="10" fill="${A}"/>`,
);

const mallet = () => tile(
  `<rect x="190" y="170" width="22" height="152" rx="10" fill="${C.mid}"/>` +
  `<rect x="112" y="100" width="176" height="74" rx="36" fill="${C.body}"/>` +
  `<rect x="150" y="100" width="10" height="74" fill="${A}"/>` +
  label(162, 122, 80, 30, '500 g', A, 15),
);

const flatFile = () => tile(
  `<g transform="translate(0 8)">` +
  `<polygon points="120,292 84,300 120,308" fill="${C.metal}"/>` +
  `<rect x="120" y="292" width="180" height="16" fill="${C.metal}"/>` +
  [0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<path d="M${136 + i * 20} 294 v12" stroke="${C.mid}" stroke-width="2"/>`).join('') +
  `<rect x="296" y="280" width="62" height="40" rx="18" fill="${C.dark}"/>` +
  `<rect x="292" y="284" width="6" height="32" fill="${A}"/>` +
  `</g>`,
);

// C-shaped tubular frame open on the right, pistol grip at the back, blade across the open side.
const hacksaw = () => {
  const teeth = Array.from({ length: 21 }, (_, i) => `${i % 2 ? 289 : 284},${160 + i * 5}`).join(' ');
  return tile(`<g transform="translate(10 0)">` +
    `<path d="M276 170 H140 Q122 170 122 188 V232 Q122 250 140 250 H276" fill="none" stroke="${C.body}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>` +
    `<rect x="84" y="200" width="46" height="84" rx="22" fill="${C.dark}"/>` +
    `<rect x="84" y="262" width="46" height="8" rx="3" fill="${A}"/>` +
    `<polyline points="${teeth}" fill="none" stroke="${C.light}" stroke-width="3" stroke-linejoin="round"/>` +
    `<circle cx="250" cy="156" r="6" fill="${C.dark}"/>` +
    `<ellipse cx="238" cy="156" rx="9" ry="4" fill="${A}"/><ellipse cx="262" cy="156" rx="9" ry="4" fill="${A}"/>` +
    `</g>`);
};

const spiritLevel = () => tile(
  `<rect x="70" y="262" width="260" height="58" rx="6" fill="${C.metal}"/>` +
  `<rect x="70" y="262" width="16" height="58" rx="4" fill="${C.dark}"/>` +
  `<rect x="314" y="262" width="16" height="58" rx="4" fill="${C.dark}"/>` +
  `<rect x="130" y="270" width="56" height="22" rx="11" fill="#BFD9EA" opacity="0.85"/>` +
  `<circle cx="158" cy="281" r="5" fill="${C.dark}"/>` +
  `<rect x="214" y="270" width="56" height="22" rx="11" fill="#BFD9EA" opacity="0.85"/>` +
  `<circle cx="242" cy="281" r="5" fill="${C.dark}"/>` +
  `<rect x="70" y="312" width="260" height="8" fill="${A}"/>`,
);

const tapeMeasure = () => tile(
  `<circle cx="168" cy="250" r="66" fill="${C.dark}"/>` +
  `<circle cx="168" cy="250" r="30" fill="${C.mid}"/>` +
  `<circle cx="168" cy="250" r="12" fill="${C.light}"/>` +
  `<rect x="228" y="262" width="110" height="14" rx="3" fill="${C.metal}"/>` +
  [0, 1, 2, 3, 4, 5, 6].map((i) => `<rect x="${242 + i * 14}" y="262" width="2" height="7" fill="${C.dark}"/>`).join('') +
  `<rect x="330" y="256" width="14" height="28" rx="4" fill="${A}"/>` +
  label(118, 176, 100, 26, '5 m', A, 15),
);

const centrePunch = () => tile(
  `<rect x="186" y="140" width="28" height="130" rx="8" fill="${C.metal}"/>` +
  [0, 1, 2, 3].map((i) => `<rect x="${190 + i * 6}" y="150" width="2" height="110" fill="${C.mid}"/>`).join('') +
  `<polygon points="188,268 212,268 200,322" fill="${C.dark}"/>` +
  `<rect x="186" y="140" width="28" height="8" rx="4" fill="${A}"/>` +
  label(228, 190, 96, 26, '150 mm', A, 14),
);

// ---- abrasives ---------------------------------------------------------

const flapDisc = (grit) => {
  const cx = 200;
  const cy = 212;
  let s = `<circle cx="${cx}" cy="${cy + 12}" r="98" fill="${C.mid}"/>` + `<circle cx="${cx}" cy="${cy}" r="98" fill="${ABR}"/>`;
  for (let i = 0; i < 18; i++) {
    const a = (Math.PI / 9) * i;
    s += `<line x1="${(cx + 40 * Math.cos(a)).toFixed(1)}" y1="${(cy + 40 * Math.sin(a)).toFixed(1)}" ` +
      `x2="${(cx + 92 * Math.cos(a)).toFixed(1)}" y2="${(cy + 92 * Math.sin(a)).toFixed(1)}" ` +
      `stroke="${ABR_L}" stroke-width="7" stroke-linecap="round"/>`;
  }
  s += `<circle cx="${cx}" cy="${cy}" r="34" fill="${C.metal}"/><circle cx="${cx}" cy="${cy}" r="12" fill="${C.tile}"/>`;
  return tile(s + label(cx - 46, cy + 56, 92, 26, grit, A, 16));
};

const sandingBelt = () => tile(
  `<rect x="78" y="252" width="244" height="70" rx="35" fill="${ABR}"/>` +
  `<rect x="78" y="252" width="244" height="8" rx="4" fill="${ABR_L}"/>` +
  `<circle cx="116" cy="287" r="20" fill="${C.tile}"/><circle cx="284" cy="287" r="20" fill="${C.tile}"/>` +
  label(120, 222, 160, 24, '100 × 610 mm', A, 14) +
  label(150, 272, 100, 30, 'P120', A, 16),
);

const sheetStack = (grit, tint) => {
  let s = '';
  for (let k = 0; k < 6; k++) {
    s += `<rect x="${112 + k * 3}" y="${300 - k * 12}" width="176" height="12" rx="2" ` +
      `fill="${k % 2 ? tint : C.paperDark}" stroke="${C.paperDark}" stroke-width="1"/>`;
  }
  return tile(s + label(104, 230, 192, 28, `230 × 280 · ${grit}`, A, 14));
};

const sandingRoll = () => tile(
  `<rect x="92" y="240" width="216" height="74" fill="${ABR}"/>` +
  `<ellipse cx="92" cy="277" rx="16" ry="37" fill="${ABR_L}"/>` +
  `<ellipse cx="308" cy="277" rx="16" ry="37" fill="${ABR_L}"/>` +
  `<ellipse cx="308" cy="277" rx="7" ry="14" fill="${C.mid}"/>` +
  label(120, 256, 140, 30, '115 × 5 m', A, 16),
);

const fleeceRoll = () => tile(
  `<rect x="80" y="226" width="240" height="90" fill="${C.light}"/>` +
  [120, 160, 200, 240, 280].map((x) => `<path d="M${x} 228 v86" stroke="${C.metal}" stroke-width="2"/>`).join('') +
  `<ellipse cx="80" cy="271" rx="18" ry="45" fill="${C.metal}"/>` +
  `<ellipse cx="320" cy="271" rx="18" ry="45" fill="${C.light}" stroke="${C.metal}" stroke-width="3"/>` +
  label(130, 180, 140, 30, '150 × 10 m', A, 16),
);

const cuttingDisc = () => tile(
  `<circle cx="200" cy="232" r="74" fill="${C.mid}"/>` +
  `<circle cx="200" cy="222" r="74" fill="${C.metal}"/>` +
  `<circle cx="200" cy="222" r="22" fill="${C.tile}"/>` +
  label(146, 268, 108, 26, '115 mm', A, 15),
);

const diamondDisc = () => tile(
  `<circle cx="200" cy="210" r="104" fill="${C.metal}"/>` +
  `<circle cx="200" cy="210" r="104" fill="none" stroke="${C.dark}" stroke-width="12" stroke-dasharray="26 12"/>` +
  `<circle cx="200" cy="210" r="22" fill="${C.tile}"/>` +
  label(138, 262, 124, 26, '230 mm', A, 15),
);

const polishingPad = () => tile(
  `<circle cx="200" cy="240" r="78" fill="${C.mid}"/>` +
  `<circle cx="200" cy="222" r="78" fill="${C.light}"/>` +
  `<circle cx="200" cy="222" r="78" fill="none" stroke="${A}" stroke-width="8"/>` +
  `<circle cx="200" cy="222" r="30" fill="${C.dark}"/>` +
  label(150, 262, 100, 26, '150 mm', A, 15),
);

// ---- workshop ----------------------------------------------------------

const workbench = () => tile(
  `<rect x="84" y="176" width="14" height="144" fill="${C.body}"/>` +
  `<rect x="302" y="176" width="14" height="144" fill="${C.body}"/>` +
  `<rect x="84" y="284" width="232" height="10" rx="3" fill="${C.body}"/>` +
  `<rect x="70" y="150" width="260" height="24" rx="4" fill="${WOOD}"/>` +
  `<rect x="110" y="186" width="180" height="40" rx="4" fill="${WOOD_D}"/>` +
  `<rect x="186" y="198" width="28" height="8" rx="4" fill="${A}"/>` +
  label(140, 236, 120, 28, '1500 mm', A, 15),
);

const benchVise = () => tile(
  `<rect x="130" y="300" width="140" height="22" rx="6" fill="${C.dark}"/>` +
  `<rect x="122" y="232" width="150" height="70" rx="8" fill="${C.body}"/>` +
  `<rect x="108" y="196" width="22" height="106" rx="4" fill="${C.dark}"/>` +
  `<rect x="270" y="208" width="22" height="94" rx="4" fill="${C.mid}"/>` +
  `<rect x="290" y="250" width="66" height="10" rx="4" fill="${C.metal}"/>` +
  `<rect x="352" y="232" width="10" height="40" rx="4" fill="${A}"/>` +
  label(150, 246, 100, 26, '125 mm', A, 14),
);

const trolley = () => tile(
  `<rect x="110" y="104" width="8" height="206" fill="${C.dark}"/>` +
  `<rect x="282" y="104" width="8" height="206" fill="${C.dark}"/>` +
  `<rect x="100" y="98" width="200" height="10" rx="5" fill="${C.dark}"/>` +
  [150, 214, 278].map((y) => `<rect x="104" y="${y}" width="192" height="8" fill="${C.metal}"/>`).join('') +
  `<rect x="130" y="124" width="46" height="26" rx="3" fill="${C.paper}"/>` +
  `<rect x="190" y="128" width="60" height="22" rx="3" fill="${C.paperDark}"/>` +
  `<rect x="130" y="252" width="60" height="26" rx="3" fill="${C.paper}"/>` +
  `<rect x="200" y="256" width="44" height="22" rx="3" fill="${C.paperDark}"/>` +
  label(148, 178, 104, 26, '120 kg', A, 14) +
  `<circle cx="124" cy="316" r="12" fill="${C.dark}"/><circle cx="276" cy="316" r="12" fill="${C.dark}"/>`,
);

const extractionUnit = () => tile(
  `<path d="M250 210 C300 210 304 250 300 290 L300 306" fill="none" stroke="${C.dark}" stroke-width="10" stroke-linecap="round"/>` +
  `<rect x="112" y="148" width="132" height="150" rx="20" fill="${C.body}"/>` +
  `<rect x="106" y="134" width="144" height="20" rx="8" fill="${C.dark}"/>` +
  `<rect x="112" y="222" width="132" height="10" fill="${A}"/>` +
  label(138, 240, 80, 26, '50 L', A, 15) +
  `<circle cx="140" cy="314" r="12" fill="${C.dark}"/><circle cx="216" cy="314" r="12" fill="${C.dark}"/>`,
);

const compressor = () => tile(
  `<rect x="150" y="176" width="92" height="56" rx="12" fill="${C.dark}"/>` +
  `<path d="M124 176 Q196 124 268 176" fill="none" stroke="${C.dark}" stroke-width="9" stroke-linecap="round"/>` +
  `<circle cx="174" cy="204" r="13" fill="${C.white}" stroke="${C.mid}" stroke-width="4"/>` +
  `<rect x="100" y="230" width="200" height="82" rx="41" fill="${C.body}"/>` +
  `<rect x="100" y="260" width="200" height="10" fill="${A}"/>` +
  `<rect x="122" y="306" width="36" height="16" rx="4" fill="${C.dark}"/>` +
  `<rect x="242" y="306" width="36" height="16" rx="4" fill="${C.dark}"/>` +
  label(248, 184, 72, 26, '24 L', A, 15),
);

const sackTruck = () => tile(
  `<rect x="168" y="96" width="12" height="206" rx="5" fill="${C.dark}"/>` +
  `<rect x="222" y="96" width="12" height="206" rx="5" fill="${C.dark}"/>` +
  `<rect x="160" y="84" width="80" height="16" rx="8" fill="${C.body}"/>` +
  `<rect x="168" y="196" width="66" height="10" fill="${C.mid}"/>` +
  `<rect x="138" y="300" width="112" height="12" rx="4" fill="${C.body}"/>` +
  `<circle cx="214" cy="298" r="22" fill="${C.dark}"/>` +
  `<circle cx="214" cy="298" r="8" fill="${A}"/>` +
  label(240, 120, 76, 26, '200 kg', A, 14),
);

const shelfUnit = () => tile(
  `<rect x="92" y="120" width="10" height="200" fill="${C.body}"/>` +
  `<rect x="298" y="120" width="10" height="200" fill="${C.body}"/>` +
  `<rect x="92" y="120" width="216" height="8" fill="${C.body}"/>` +
  `<rect x="92" y="222" width="216" height="8" fill="${C.body}"/>` +
  `<rect x="92" y="312" width="216" height="10" fill="${C.body}"/>` +
  `<rect x="196" y="128" width="8" height="184" fill="${C.body}"/>` +
  `<rect x="110" y="140" width="70" height="66" rx="3" fill="${C.paper}"/>` +
  `<rect x="214" y="140" width="70" height="66" rx="3" fill="${C.paper}"/>` +
  `<rect x="110" y="240" width="70" height="56" rx="3" fill="${C.paperDark}"/>` +
  `<rect x="214" y="240" width="70" height="56" rx="3" fill="${C.paperDark}"/>`,
);

const assortmentBox = () => tile(
  `<rect x="84" y="200" width="232" height="24" rx="5" fill="${C.body}"/>` +
  `<rect x="90" y="236" width="220" height="86" rx="6" fill="${C.mid}"/>` +
  `<rect x="100" y="246" width="60" height="66" rx="4" fill="${C.light}"/>` +
  `<rect x="170" y="246" width="60" height="66" rx="4" fill="${C.light}"/>` +
  `<rect x="240" y="246" width="60" height="66" rx="4" fill="${C.light}"/>` +
  `<rect x="90" y="236" width="220" height="8" rx="4" fill="${A}"/>` +
  label(138, 201, 124, 22, '3 compartments', A, 13),
);

const workLight = () => tile(
  `<path d="M200 250 L150 322 M200 250 L250 322" stroke="${C.dark}" stroke-width="8" stroke-linecap="round"/>` +
  `<rect x="194" y="180" width="12" height="74" fill="${C.dark}"/>` +
  `<rect x="116" y="112" width="168" height="72" rx="10" fill="${C.dark}"/>` +
  `<rect x="128" y="124" width="144" height="48" rx="6" fill="${C.white}"/>` +
  [0, 1, 2, 3, 4, 5].map((c) => [0, 1].map((r) =>
    `<circle cx="${146 + c * 22}" cy="${136 + r * 16}" r="4" fill="${C.light}"/>`).join('')).join('') +
  `<rect x="116" y="176" width="168" height="8" rx="4" fill="${A}"/>` +
  label(256, 200, 70, 24, '20 W', A, 14),
);

const airHose = () => tile(
  `<ellipse cx="188" cy="252" rx="130" ry="68" fill="${C.dark}"/>` +
  `<ellipse cx="188" cy="250" rx="130" ry="68" fill="${C.body}"/>` +
  `<ellipse cx="188" cy="250" rx="100" ry="50" fill="${C.mid}"/>` +
  `<ellipse cx="188" cy="250" rx="72" ry="34" fill="${C.body}"/>` +
  `<ellipse cx="188" cy="250" rx="40" ry="18" fill="${C.tile}"/>` +
  `<rect x="318" y="236" width="40" height="16" rx="4" fill="${C.dark}"/>` +
  `<rect x="352" y="232" width="12" height="24" rx="3" fill="${A}"/>` +
  label(120, 176, 90, 26, '10 m', A, 15),
);

export const illustrations = {
  'DEMO-IND-4001': screwdriverSet(),
  'DEMO-IND-4002': socketSet(7, 4, 9, 26, '1/4 in · 26 pcs'),
  'DEMO-IND-4003': socketSet(5, 4, 14, 20, '1/2 in · 20 pcs', true),
  'DEMO-IND-4004': spannerSet(8, '8 pcs'),
  'DEMO-IND-4005': pipeWrench(),
  'DEMO-IND-4006': pliers(),
  'DEMO-IND-4007': sideCutters(),
  'DEMO-IND-4008': pumpPliers(),
  'DEMO-IND-4009': hammer(),
  'DEMO-IND-4010': mallet(),
  'DEMO-IND-4011': flatFile(),
  'DEMO-IND-4012': hacksaw(),
  'DEMO-IND-4013': spiritLevel(),
  'DEMO-IND-4014': tapeMeasure(),
  'DEMO-IND-4015': centrePunch(),
  'DEMO-IND-4016': hexKeySet(),
  'DEMO-IND-5001': flapDisc('P80'),
  'DEMO-IND-5002': flapDisc('P120'),
  'DEMO-IND-5003': sandingBelt(),
  'DEMO-IND-5004': sheetStack('P180', '#EFE6D6'),
  'DEMO-IND-5005': sheetStack('P80', '#D9C7A6'),
  'DEMO-IND-5006': sandingRoll(),
  'DEMO-IND-5007': cuttingDisc(),
  'DEMO-IND-5008': diamondDisc(),
  'DEMO-IND-5009': fleeceRoll(),
  'DEMO-IND-5010': polishingPad(),
  'DEMO-IND-6001': workbench(),
  'DEMO-IND-6002': benchVise(),
  'DEMO-IND-6003': trolley(),
  'DEMO-IND-6004': extractionUnit(),
  'DEMO-IND-6005': compressor(),
  'DEMO-IND-6006': sackTruck(),
  'DEMO-IND-6007': shelfUnit(),
  'DEMO-IND-6008': assortmentBox(),
  'DEMO-IND-6009': workLight(),
  'DEMO-IND-6010': airHose(),
};
