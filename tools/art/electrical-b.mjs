// More electrical illustrations, keyed by SKU (part b). Same style as electrical.mjs.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.electrical;
const FONT = 'font-family="Helvetica, Arial, sans-serif"';
const BRASS = '#C9A54A';
const GREY = '#8A9099';

const R = (x, y, w, h, fill, rx = 0, extra = '') =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" ${extra}/>`;
const E = (cx, cy, rx, ry, fill) =>
  `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}"/>`;
const Cc = (cx, cy, r, fill, extra = '') => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}" ${extra}/>`;
const LN = (x1, y1, x2, y2, stroke, w) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round"/>`;
const PL = (d, stroke, w, extra = '') =>
  `<path d="${d}" fill="none" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const POLY = (pts, fill) => `<polygon points="${pts}" fill="${fill}"/>`;
const TXT = (x, y, size, text, fill = C.dark) =>
  `<text x="${x}" y="${y}" text-anchor="middle" ${FONT} font-size="${size}" font-weight="700" fill="${fill}">${text}</text>`;
const hex = (cx, cy, r) =>
  Array.from({ length: 6 }, (_, i) => {
    const a = (Math.PI / 3) * i;
    return `${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`;
  }).join(' ');

// DIN-rail circuit breaker: one 84 px module per pole; multi-pole breakers share one handle.
const mcb = (poles, text) => {
  const m = 84;
  const w = m * poles;
  const x0 = 200 - w / 2;
  let s = R(x0, 132, w, 186, C.body, 8);
  for (let i = 0; i < poles; i++) {
    const cx = x0 + m * i + m / 2;
    s += R(cx - 12, 118, 24, 16, C.metal, 3) + R(cx - 12, 318, 24, 14, C.metal, 3);
  }
  s += poles === 1
    ? R(x0 + m / 2 - 17, 150, 34, 40, C.light, 5)
    : R(x0 + 8, 150, w - 16, 36, C.light, 5);
  s += label(x0 + 8, 214, w - 16, 52, text, A, poles === 1 ? 15 : 20);
  return tile(s);
};

// RCD, RCBO or surge protector: 62 px per pole, a test button or a status window.
const dev = (poles, text, { test = false, handle = false, window = false, size = 15 } = {}) => {
  const m = 62;
  const w = m * poles;
  const x0 = 200 - w / 2;
  let s = R(x0, 132, w, 186, C.body, 8);
  for (let i = 0; i < poles; i++) {
    const cx = x0 + m * i + m / 2;
    s += R(cx - 12, 118, 24, 16, C.metal, 3) + R(cx - 12, 318, 24, 14, C.metal, 3);
  }
  if (handle) s += R(x0 + 8, 150, w - 16, 34, C.light, 5);
  if (window) s += R(x0 + 10, 150, w - 20, 46, C.light, 5) + Cc(x0 + w / 2, 172, 7, A);
  if (test) s += R(x0 + w / 2 - 14, 198, 28, 18, A, 4);
  s += label(x0 + 8, 226, w - 16, 40, text, A, size);
  return tile(s);
};

// Distribution board in a surface housing (raised) or flush with the wall (recessed frame).
const board = (w, h, modules, text, flush) => {
  const x = 200 - w / 2;
  const y = 326 - h;
  let s = flush
    ? R(x - 12, y - 12, w + 24, h + 24, C.light, 16)
    : R(x - 8, y + 10, w + 16, h - 6, C.mid, 12);
  s += flush
    ? R(x, y, w, h, C.white, 10, `stroke="${C.light}" stroke-width="3"`)
    : R(x, y, w, h, C.body, 10);
  s += R(x + 12, y + 12, w - 24, h - 24, C.white, 6);
  s += label(x + 20, y + 20, w - 40, 30, text, A, 16);
  const rows = modules / 12;
  const step = (w - 48) / 12;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < 12; c++) {
      s += R(x + 24 + c * step, y + 70 + r * 36, step - 4, 26, C.light, 2);
    }
  }
  s += flush
    ? R(x + w / 2 - 16, y + h - 24, 32, 6, A, 3)
    : R(x + w / 2 - 16, y + h - 22, 32, 6, C.mid, 3);
  return tile(s);
};

// Flush or cavity box: a round cup seen from slightly above. Cavity boxes get mounting wings.
const cyl = (rx, depth, text, wings = false) => {
  const cy = 232;
  const ry = rx * 0.28;
  let s = E(200, cy + depth, rx, ry, C.mid);
  if (wings) s += R(200 - rx - 50, cy - 4, 50, 12, C.light, 5) + R(200 + rx, cy - 4, 50, 12, C.light, 5);
  s += R(200 - rx, cy, 2 * rx, depth, C.body);
  s += E(200, cy, rx, ry, C.light);
  s += E(200, cy, rx - 9, ry - 5, C.dark);
  s += label(200 - 60, cy + depth / 2 - 15, 120, 30, text, A, 15);
  return tile(s);
};

// Surface-mounted single-gang housing with a rocker opening and two cable entries.
const housing = () => tile(
  R(128, 140, 144, 172, C.body, 14) +
  R(128, 140, 144, 36, C.mid, 14) +
  R(140, 176, 120, 4, C.dark, 2) +
  label(152, 148, 96, 24, 'IP44', A, 14) +
  R(176, 200, 48, 58, C.dark, 8) +
  R(189, 210, 22, 36, C.light, 6) +
  Cc(160, 300, 10, C.metal) + Cc(240, 300, 10, C.metal),
);

// A cable tie: head, strap, length and width scaled from the spec.
// Cable tie: one tie closed into a loop (its head sits on the ring) plus two loose straps.
const tie = (mm, t, text) => {
  const L = mm * 0.9;                 // strap length in px
  const w = t * 2.2;                  // strap width in px, so the three SKUs differ
  const rx = 26 + mm * 0.12;          // loop grows with the length
  const ry = rx * 0.6;
  const cx = 200, cy = 168;
  const x0 = cx - L / 2;
  const strap = (y, dx) =>
    R(x0 + dx, y - 9, 14, 18, C.dark, 2) +
    R(x0 + dx + 7, y - w / 2, L - 7, w, C.body, w / 2);
  return tile(
    `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${C.body}" stroke-width="${w}"/>` +
    R(cx - 8, cy - ry - 9, 16, 18, C.dark, 2) +
    strap(252, 0) +
    strap(302, -10) +
    label(20, 28, 120, 30, text, A, 15),
  );
};

// Cable trunking, white, shown as an end face with the top and side receding.
const trunk = (w, h, text, size) => {
  const dx = 34;
  const dy = 28;
  const x = 200 - w / 2 - 14;
  const y = 320 - h;
  return tile(
    POLY(`${x},${y} ${x + dx},${y - dy} ${x + w + dx},${y - dy} ${x + w},${y}`, C.white) +
    POLY(`${x + w},${y} ${x + w + dx},${y - dy} ${x + w + dx},${y - dy + h} ${x + w},${y + h}`, C.light) +
    R(x, y, w, h, C.white, 4, `stroke="${C.light}" stroke-width="3"`) +
    R(x + 14, y + 14, w - 28, h - 28, C.light, 3) +
    R(x + 10, y + 10, w - 20, 6, A, 3) +
    label(x + w / 2 - 50, y + h - 40, 100, 28, text, A, size),
  );
};

// Flexible conduit: a tube with dashed ribs; the width follows the diameter.
const conduit = (w, text) => tile(
  PL('M48 262 C 130 150, 270 300, 352 168', C.body, w) +
  PL('M48 262 C 130 150, 270 300, 352 168', C.light, w - 8, 'stroke-dasharray="5 7"') +
  label(120, 302, 160, 28, text, A, 15),
);

// Cable gland: brass nut, thread, black dome cap. r is the thread radius in px.
const gland = (r, text) => {
  const cx = 200;
  let s = R(cx - r * 0.7, 250, r * 1.4, 70, C.metal, 3);
  for (let y = 258; y < 316; y += 8) s += LN(cx - r * 0.7, y, cx + r * 0.7, y, C.mid, 3);
  s += R(cx - r - 10, 230, 2 * r + 20, 26, BRASS, 4);
  s += R(cx - r, 172, 2 * r, 62, C.dark, r * 0.5);
  s += label(cx - r - 2, 194, 2 * r + 4, 26, text, A, 14);
  return tile(s);
};

// Terminal block on a DIN rail: grey housing, wire entry on top, screw on the front.
const tblock = (w, hole, text) => {
  const x = 200 - w / 2;
  return tile(
    R(x, 150, w, 150, GREY, 6) +
    Cc(200, 176, hole, C.dark) +
    Cc(200, 176, hole * 0.45, C.mid) +
    label(x + 8, 220, w - 16, 30, text, A, 15) +
    Cc(200, 276, 9, C.light) + LN(194, 276, 206, 276, C.dark, 3) +
    R(120, 300, 160, 10, C.mid, 3),
  );
};

// Wire ferrules, pack of 100 shown as three tubes; the tube width follows the wire size.
const ferrule = (tw, text) => {
  let s = '';
  for (let i = 0; i < 3; i++) {
    const x = 200 + (i - 1) * (tw + 18);
    s += R(x - tw / 2, 170, tw, 140, C.metal, tw / 2);
    s += E(x, 170, tw / 2, 4, C.dark);
    s += R(x - tw / 2 - 3, 296, tw + 6, 10, A, 3);
  }
  return tile(s + label(150, 118, 100, 30, text, A, 15));
};

// Five-pole pluggable terminal with five wire entries and a screw slot each.
const connector = () => {
  let s = R(90, 170, 220, 120, C.body, 10);
  for (let i = 0; i < 5; i++) {
    s += R(112 + i * 40, 186, 24, 22, C.dark, 3) + R(112 + i * 40, 228, 24, 6, C.light, 2);
  }
  s += R(90, 268, 220, 8, A, 3);
  s += label(130, 130, 140, 30, '5 × 2.5 mm²', A, 15);
  return tile(s);
};

// Hand tools: two arms meet at the pivot; jaws to the left, grips to the right.
// Pliers and cutters, drawn upright: jaws at the top, two handles crossing at a round pivot.
// Jaw shapes are drawn in a local frame: origin at the pivot, jaw pointing up (-y).
const PIV_X = 200, PIV_Y = 150, DEG = 180 / Math.PI;
const jawShape = {
  // wire stripper: two notches near the tip, adjusting screw on the jaw
  strip: (L) =>
    R(-8, -L, 16, L - 6, C.metal, 2, `stroke="${C.mid}" stroke-width="2"`) +
    R(-5, -L + 5, 10, 6, C.dark, 1) + R(-5, -L + 16, 10, 5, C.dark, 1) +
    Cc(0, -12, 3.5, C.dark),
  // automatic stripper: wider jaw, three stepped notches, round dial at the base
  auto: (L) =>
    R(-10, -L, 20, L - 6, C.metal, 4, `stroke="${C.mid}" stroke-width="2"`) +
    R(-6, -L + 4, 12, 4, C.dark, 1) + R(-5, -L + 13, 10, 4, C.dark, 1) + R(-4, -L + 22, 8, 4, C.dark, 1) +
    Cc(0, -12, 5, A),
  // crimping tool: wide jaw with three square cavities of decreasing size
  crimp: (L) =>
    R(-12, -L, 24, L - 6, C.metal, 2, `stroke="${C.mid}" stroke-width="2"`) +
    R(-6, -L + 8, 12, 12, C.dark, 1) + R(-4.5, -L + 22.5, 9, 9, C.dark, 1) + R(-3, -L + 36, 6, 6, C.dark, 1),
  // side cutter: short tapered jaw, the cutting edge runs to a point at the top
  cut: (L) =>
    POLY(`-8,-6 8,-6 8,${-L * 0.45} 0,${-L}`, C.metal) +
    LN(8, -L * 0.45, 0, -L, C.dark, 2) +
    PL(`M-8 -6 L0 ${-L}`, C.mid, 2),
  // cable cutter: curved hooked blade, like a parrot beak
  beak: (L) =>
    `<path d="M-9,-6 C-14,-28 -13,${-L + 12} -4,${-L + 2} Q 4,${-L + 2} 5,${-L + 12} C 5,${-L + 30} 3,-34 9,-6 Z" fill="${C.metal}" stroke="${C.mid}" stroke-width="2"/>`,
};
const plier = ({ jl = 62, js = 20, hl = 160, hs = 32, jaw, grip, gripW = 30, tail = null, text, extra = '' }) => {
  const Lj = Math.hypot(js, jl);          // jaw length
  const Lh = Math.hypot(hs, hl);          // handle length
  const tj = Math.atan2(-js, jl) * DEG;   // jaw tilt, left arm
  const th = Math.atan2(-hs, hl) * DEG;   // handle tilt, left arm
  const arm = (s) =>
    `<g transform="translate(${PIV_X} ${PIV_Y}) rotate(${s * th})">` +
      PL(`M0 0 L0 ${Lh}`, grip, gripW) +
      (tail ? PL(`M0 ${Lh - tail.len} L0 ${Lh}`, tail.fill, gripW) : '') +
    `</g>` +
    `<g transform="translate(${PIV_X} ${PIV_Y}) rotate(${s * tj})">${jawShape[jaw](Lj)}</g>`;
  return tile(
    arm(1) + arm(-1) +
    Cc(PIV_X, PIV_Y, 9, C.dark) + Cc(PIV_X, PIV_Y, 3.5, C.metal) +
    extra +
    label(24, 28, 120, 30, text, A, 16),
  );
};
// Cable sheath stripper: a round clamp with a hook blade inside, lever handle. Not pliers.
const sheathStripper = (text) => tile(
  `<path d="M246.8 173 A54 54 0 1 1 218.5 149.3" fill="none" stroke="${C.body}" stroke-width="18" stroke-linecap="butt"/>` +
  Cc(146, 200, 9, C.dark) +
  PL('M198 150 Q216 170 198 190', C.metal, 7) +
  PL('M202 256 L262 318', A, 30) +
  PL('M240 292 L262 318', C.dark, 30) +
  label(24, 28, 120, 30, text, A, 16),
);

// Two-pole voltage tester: a body with two probes and a window.
const tester = () => tile(
  LN(190, 176, 190, 96, C.metal, 5) + LN(210, 176, 210, 96, C.metal, 5) +
  R(170, 176, 60, 118, C.body, 14) +
  R(186, 196, 28, 14, C.light, 4) +
  R(170, 252, 60, 8, A, 3) +
  label(150, 306, 100, 26, '1000 V', A, 14),
);

// Phase tester in screwdriver form: a handle with a window and a short shaft.
const phaseTester = () => tile(
  R(196, 108, 8, 80, C.metal, 2) +
  R(170, 186, 60, 126, A, 28) +
  R(186, 206, 28, 30, C.light, 8) +
  label(140, 70, 120, 28, '230 V', A, 15),
);

// Digital multimeter: a screen, a rotary dial and two leads.
const multimeter = () => tile(
  PL('M160 318 q -24 16 -44 4', C.dark, 6) +
  PL('M240 318 q 24 16 44 4', C.dark, 6) +
  R(120, 116, 160, 204, C.body, 18) +
  R(140, 136, 120, 58, '#DDE5D6', 6) +
  TXT(200, 176, 22, '600 V') +
  Cc(200, 250, 34, C.mid) +
  LN(200, 250, 226, 230, A, 5) +
  Cc(200, 250, 6, C.dark),
);

// Insulated screwdriver set: six blades, handles alternating between the body and the accent.
const screwdrivers = () => {
  let s = label(150, 60, 100, 28, '6 pcs', A, 15);
  for (let i = 0; i < 6; i++) {
    const x = 118 + i * 32;
    s += R(x - 2, 170, 4, 150, C.light, 2);
    s += R(x - 12, 112, 24, 64, i % 2 ? A : C.body, 12);
  }
  return tile(s);
};


// Five new SKUs (part b, batch 2): single-core coil, emergency luminaire, main switch,
// large copper ferrules, cable knife.
const coil = (text) => {
  let s = '';
  for (let k = 4; k >= 0; k--) {
    s += E(200, 236 + k * 14, 124, 44, k === 0 ? '#C47A4A' : C.body);
  }
  s += E(200, 236, 46, 16, C.tile);
  s += PL('M324 236 Q360 236 360 270', '#C47A4A', 12);
  return tile(s + label(128, 294, 144, 30, text, A, 16));
};

const emergency = () => tile(
  R(104, 158, 192, 120, C.white, 12, `stroke="${C.light}" stroke-width="3"`) +
  R(124, 172, 152, 44, C.paper, 6) +
  Cc(118, 166, 4, C.mid) + Cc(282, 166, 4, C.mid) + Cc(118, 268, 4, C.mid) + Cc(282, 268, 4, C.mid) +
  label(144, 226, 112, 30, '3 W · IP44', A, 16),
);

// Three-pole main switch: 84 px per pole, one large lever on the front.
const mainSwitch = () => {
  const m = 84;
  const w = m * 3;
  const x0 = 200 - w / 2;
  let s = R(x0, 150, w, 150, C.body, 8);
  for (let i = 0; i < 3; i++) {
    const cx = x0 + m * i + m / 2;
    s += R(cx - 12, 136, 24, 16, C.metal, 3) + R(cx - 12, 298, 24, 14, C.metal, 3);
  }
  s += R(158, 96, 84, 56, C.light, 8) + R(158, 96, 84, 12, A, 4);
  s += label(x0 + 24, 218, w - 48, 48, '63 A', A, 22);
  return tile(s);
};

const bigFerrule = (text) => {
  let s = '';
  for (let i = 0; i < 3; i++) {
    const x = 200 + (i - 1) * 52;
    s += R(x - 22, 150, 44, 170, '#C47A4A', 22);
    s += E(x, 150, 22, 5, C.dark);
    s += R(x - 25, 300, 50, 12, A, 4);
  }
  return tile(s + label(120, 112, 160, 30, text, A, 16));
};

const cableKnife = (text) => tile(
  POLY('64,300 236,262 236,318', C.light) +
  LN(72, 300, 226, 272, C.white, 3) +
  R(234, 260, 98, 62, C.body, 26) +
  R(302, 260, 12, 62, A, 3) +
  Cc(262, 291, 7, C.light) +
  label(24, 28, 120, 30, text, A, 16),
);

export const illustrations = {
  // Circuit breakers
  'DEMO-ELE-4001': mcb(1, 'B 10 A'),
  'DEMO-ELE-4002': mcb(1, 'B 16 A'),
  'DEMO-ELE-4003': mcb(1, 'C 16 A'),
  'DEMO-ELE-4004': mcb(3, 'B 16 A'),
  'DEMO-ELE-4005': mcb(3, 'B 32 A'),
  // Residual current devices, combined device and surge protector
  'DEMO-ELE-4006': dev(2, '40 A · 30 mA', { test: true, size: 13 }),
  'DEMO-ELE-4007': dev(4, '40 A · 30 mA', { test: true, size: 18 }),
  'DEMO-ELE-4008': dev(4, '63 A · 300 mA', { test: true, size: 18 }),
  'DEMO-ELE-4009': dev(2, '16 A · 30 mA', { test: true, handle: true, size: 13 }),
  'DEMO-ELE-4010': dev(2, 'T2 · 1P+N', { window: true, size: 13 }),
  // Distribution boards
  'DEMO-ELE-4011': board(170, 200, 12, '12 M', false),
  'DEMO-ELE-4012': board(230, 250, 24, '24 M', false),
  'DEMO-ELE-4013': board(180, 220, 24, '24 M', true),
  // Boxes and housings
  'DEMO-ELE-5001': cyl(70, 80, 'Ø 60 × 60'),
  'DEMO-ELE-5002': cyl(80, 56, 'Ø 68 × 42', true),
  'DEMO-ELE-5003': housing(),
  // Cable ties
  'DEMO-ELE-5004': tie(100, 2.5, '100 × 2.5'),
  'DEMO-ELE-5005': tie(200, 3.6, '200 × 3.6'),
  'DEMO-ELE-5006': tie(300, 4.8, '300 × 4.8'),
  // Trunking
  'DEMO-ELE-5007': trunk(150, 94, '40 × 25', 14),
  'DEMO-ELE-5008': trunk(230, 153, '60 × 40', 17),
  // Flexible conduit
  'DEMO-ELE-5009': conduit(26, 'Ø 16 × 50 m'),
  'DEMO-ELE-5010': conduit(32, 'Ø 20 × 50 m'),
  'DEMO-ELE-5011': conduit(40, 'Ø 25 × 50 m'),
  // Cable glands
  'DEMO-ELE-5012': gland(28, 'M16'),
  'DEMO-ELE-5013': gland(34, 'M20'),
  'DEMO-ELE-5014': gland(42, 'M25'),
  // Terminal blocks
  'DEMO-ELE-5015': tblock(100, 6, '1.5 mm²'),
  'DEMO-ELE-5016': tblock(120, 7, '2.5 mm²'),
  'DEMO-ELE-5017': tblock(140, 9, '4 mm²'),
  'DEMO-ELE-5018': tblock(160, 11, '6 mm²'),
  // Wire ferrules
  'DEMO-ELE-5019': ferrule(14, '0.75 mm²'),
  'DEMO-ELE-5020': ferrule(18, '1.5 mm²'),
  'DEMO-ELE-5021': ferrule(24, '2.5 mm²'),
  // Connector
  'DEMO-ELE-5022': connector(),
  // Hand tools
  'DEMO-ELE-6001': plier({ jaw: 'strip', grip: A, text: '160 mm' }),
  'DEMO-ELE-6002': plier({ jaw: 'auto', grip: C.body, tail: { len: 44, fill: A }, text: '160 mm' }),
  'DEMO-ELE-6003': plier({ jl: 68, js: 22, hl: 172, hs: 34, jaw: 'crimp', grip: A, gripW: 32, text: '200 mm' }),
  'DEMO-ELE-6004': plier({
    jaw: 'cut', grip: A, tail: { len: 50, fill: C.dark }, text: '160 mm',
    extra: label(256, 28, 120, 26, '1000 V', A, 14),
  }),
  'DEMO-ELE-6005': plier({
    jl: 68, js: 22, hl: 172, hs: 34, jaw: 'cut', grip: A, gripW: 32, tail: { len: 56, fill: C.dark }, text: '200 mm',
    extra: label(256, 28, 120, 26, '1000 V', A, 14),
  }),
  'DEMO-ELE-6006': tester(),
  'DEMO-ELE-6007': phaseTester(),
  'DEMO-ELE-6008': multimeter(),
  'DEMO-ELE-6009': screwdrivers(),
  'DEMO-ELE-6010': sheathStripper('165 mm'),
  'DEMO-ELE-6011': plier({ jl: 74, js: 24, hl: 182, hs: 40, jaw: 'beak', grip: C.body, gripW: 40, text: '250 mm' }),
  'DEMO-ELE-1013': coil('1 × 6 mm²'),
  'DEMO-ELE-3020': emergency(),
  'DEMO-ELE-4014': mainSwitch(),
  'DEMO-ELE-5023': bigFerrule('4 mm²'),
  'DEMO-ELE-6012': cableKnife('180 mm'),
};
