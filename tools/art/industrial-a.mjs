// More industrial illustrations, keyed by SKU (part a). Same style as industrial.mjs.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.industrial;
const FONT = 'font-family="Helvetica, Arial, sans-serif"';
const STAINLESS = '#CFD3D8';
const LEATHER = '#8B5E3C';
const NITRILE_BLUE = '#2E5FA8';
const GREEN = '#3E8E5A';
const RED = '#D0453B';

// ---- primitives (flat shapes only) ----
const rect = (x, y, w, h, fill, rx = 0, extra = '') =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}"${extra}/>`;
const ell = (cx, cy, rx, ry, fill, extra = '') =>
  `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}"${extra}/>`;
const shape = (d, fill, extra = '') => `<path d="${d}" fill="${fill}"${extra}/>`;
const line = (d, color, w) =>
  `<path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
const text = (x, y, s, size = 18, fill = '#fff') =>
  `<text x="${x}" y="${y}" text-anchor="middle" ${FONT} font-size="${size}" font-weight="700" fill="${fill}">${s}</text>`;
const shift = (dx, inner) => `<g transform="translate(${dx} 0)">${inner}</g>`;
const hexPts = (cx, cy, r, rot = 30) =>
  Array.from({ length: 6 }, (_, i) => {
    const a = ((60 * i + rot) * Math.PI) / 180;
    return `${(cx + r * Math.cos(a)).toFixed(1)},${(cy + r * Math.sin(a)).toFixed(1)}`;
  }).join(' ');

// ---- power tools (lying on the floor, bottoms near y=320) ----
const percussion = () => tile(shift(-20,
  line('M122 262 C 96 268 92 300 66 318', C.dark, 6) +
  rect(126, 240, 28, 40, C.dark, 10) +
  rect(150, 228, 124, 56, C.body, 26) +
  rect(262, 234, 46, 44, C.dark, 10) +
  rect(302, 242, 20, 28, C.metal, 4) +
  rect(318, 250, 56, 10, C.metal, 2) +
  line('M268 234 Q 292 196 324 226', C.dark, 9) +
  shape('M196 280 h56 v28 q0 10 -10 10 h-36 q-10 0 -10 -10 z', C.dark) +
  rect(166, 240, 14, 40, A, 3) +
  label(184, 240, 84, 28, '710 W', A, 16),
));

// Jigsaw: motor body on a flat base plate (shoe) on the floor, closed D-handle on top,
// the blade hanging down through the plate in front. No stand.
const jigsaw = (cordless = false) => {
  const teeth = Array.from({ length: 8 }, (_, i) => `${i % 2 ? 133 : 138},${318 + i * 2}`).join(' ');
  return tile(
    rect(116, 304, 136, 12, C.light, 3) +
    rect(138, 316, 7, 18, C.metal) +
    `<polyline points="${teeth}" fill="none" stroke="${C.mid}" stroke-width="2"/>` +
    rect(160, 250, 96, 54, C.body, 20) +
    line('M170 256 V228 Q170 214 186 214 H236 Q252 214 252 228 V256', C.dark, 10) +
    (cordless
      ? rect(236, 262, 36, 34, C.dark, 8) + rect(244, 270, 20, 6, A, 2) + label(170, 262, 60, 26, '18 V', A, 14)
      : line('M256 270 C 280 262 296 286 330 292', C.dark, 6) + label(172, 262, 66, 26, '650 W', A, 15)),
  );
};

// Circular saw: motor on the left, blade disc on the right, battery at the back when cordless.
const circular = (d, cordless = false) => {
  const r = d / 3;
  return tile(shift(-20,
    (cordless ? rect(94, 232, 26, 48, C.dark, 7) : line('M120 236 C 96 230 90 200 60 196', C.dark, 6)) +
    rect(110, 284, 200, 12, C.light, 3) +
    rect(118, 218, 136, 66, C.body, 24) +
    rect(130, 196, 96, 14, C.dark, 6) +
    ell(296, 262, r, r, C.metal) +
    ell(296, 262, r * 0.72, r * 0.72, 'none', ` stroke="${C.mid}" stroke-width="3" stroke-dasharray="6 7"`) +
    ell(296, 262, 12, 12, C.dark) +
    label(140, 240, 84, 26, `${d} mm`, A, 15),
  ));
};

const multiTool = () => tile(shift(-10,
  rect(106, 250, 24, 38, C.dark, 7) +
  rect(126, 254, 150, 30, C.body, 15) +
  rect(160, 280, 40, 38, C.dark, 12) +
  rect(266, 256, 44, 24, C.dark, 5) +
  shape('M302 260 L 352 268 L 302 276 Z', C.metal) +
  label(176, 257, 64, 24, '12 V', A, 14),
));

const orbital = () => tile(
  ell(200, 306, 62, 14, C.dark) +
  rect(180, 198, 40, 106, C.body, 16) +
  ell(200, 198, 42, 16, C.mid) +
  rect(222, 244, 32, 16, C.dark, 6) +
  label(168, 232, 64, 26, '125', A, 16),
);

// Detail sander: iron-shaped sanding pad flat on the floor, point forward; body and handle on top.
const detail = () => tile(
  shape('M112 322 V296 L300 322 Z', '#B98D5E') +
  shape('M128 302 V254 Q128 250 132 250 H248 Q252 250 252 254 V312 Z', C.body) +
  line('M158 252 Q 168 212 208 212 Q 240 212 248 252', C.dark, 12) +
  rect(248, 266, 26, 18, C.dark, 6) +
  label(150, 262, 68, 24, '280 W', A, 14),
);

const hotAir = () => tile(shift(-20,
  rect(136, 228, 112, 48, C.body, 16) +
  rect(246, 238, 80, 26, C.dark, 8) +
  rect(312, 232, 24, 38, C.metal, 6) +
  shape('M168 270 h44 l-8 48 h-36 z', C.dark) +
  label(150, 238, 80, 26, '2000 W', A, 14),
));

const belt = () => tile(shift(-20,
  rect(104, 262, 200, 46, C.dark, 23) +
  line('M122 280 H 270', C.mid, 3) +
  ell(122, 285, 14, 14, C.metal) +
  ell(286, 285, 14, 14, C.metal) +
  rect(136, 204, 136, 50, C.body, 22) +
  rect(152, 192, 104, 14, C.mid, 6) +
  label(170, 218, 100, 26, '1010 W', A, 14),
));

const charger = () => tile(shift(-10,
  line('M286 300 C 330 300 344 316 368 318', C.dark, 6) +
  rect(116, 232, 170, 86, C.body, 16) +
  rect(156, 252, 88, 24, C.dark, 6) +
  ell(268, 270, 6, 6, '#7CD08A') +
  label(132, 284, 84, 24, '18 V', A, 15),
));

const batteryLong = () => tile(shift(-10,
  rect(120, 258, 160, 60, C.dark, 14) +
  rect(146, 244, 108, 18, C.body, 6) +
  rect(166, 252, 60, 5, C.mid, 2) +
  label(138, 284, 124, 24, '12 V · 2.0 Ah', A, 14),
));

const wetDry = () => tile(shift(-20,
  line('M280 300 C 320 300 330 250 356 232', C.mid, 12) +
  rect(126, 196, 150, 112, C.body, 26) +
  rect(116, 186, 170, 22, C.dark, 10) +
  line('M170 186 Q 200 146 232 186', C.dark, 10) +
  ell(156, 316, 12, 12, C.dark) +
  ell(252, 316, 12, 12, C.dark) +
  label(158, 262, 84, 26, '20 L', A, 16),
));

const grinderCordless = () => tile(shift(-10,
  rect(106, 254, 26, 46, C.dark, 8) +
  rect(116, 238, 144, 44, C.body, 20) +
  rect(246, 226, 50, 70, C.dark, 12) +
  ell(312, 266, 12, 46, C.metal) +
  rect(168, 280, 42, 38, C.dark, 12) +
  label(146, 244, 84, 26, '115 mm', A, 14),
));

// ---- fasteners (screws and bolts standing on the floor, boxes with a spec label) ----
const screwDraw = (cx, top, len, hw, head, mat) => {
  const hh = head === 'cheese' ? 16 : head === 'hex' ? 14 : 10;
  const sx = hw * 0.45;
  let s = '';
  if (head === 'hex') s += rect(cx - hw * 1.3, top, hw * 2.6, hh, C.mid, 2);
  else if (head === 'cheese') s += rect(cx - hw, top, hw * 2, hh, C.mid, 5) + rect(cx - hw * 0.35, top + 5, hw * 0.7, 6, C.dark, 1);
  else {
    s += rect(cx - hw, top, hw * 2, hh, C.mid, 4);
    if (head === 'cross') s += rect(cx - hw * 0.6, top + 4, hw * 1.2, 2, C.dark) + rect(cx - 1, top + 1, 2, 8, C.dark);
  }
  s += rect(cx - sx, top + hh, sx * 2, len, mat);
  for (let y = top + hh + 10; y < top + hh + len - 6; y += 9) s += line(`M${cx - sx} ${y} l${sx * 2} -4`, C.mid, 2);
  const y0 = top + hh + len;
  s += shape(`M${cx - sx} ${y0} L${cx} ${y0 + hw * 1.1} L${cx + sx} ${y0} Z`, mat);
  return s;
};

// bottom = where the tip ends up; the head sits above it
const screwAt = (cx, bottom, len, hw, head = 'pan', mat = C.metal, tipH = 1.1) => {
  const hh = head === 'cheese' ? 16 : head === 'hex' ? 14 : 10;
  const top = bottom - (hh + len + hw * tipH);
  return screwDraw(cx, top, len, hw, head, mat);
};

const grub = (cx, bottom, len = 40) =>
  rect(cx - 8, bottom - len, 16, len, STAINLESS, 3) +
  `<polygon points="${hexPts(cx, bottom - len + 6, 4.5)}" fill="${C.dark}"/>`;

const hexNut = (cx, cy, r, fill = C.metal) =>
  `<polygon points="${hexPts(cx, cy, r)}" fill="${fill}"/>` + ell(cx, cy, r * 0.42, r * 0.42, C.tile);

const squareNut = (cx, cy, r) =>
  `<polygon points="${cx - r},${cy - r} ${cx + r},${cy - r} ${cx + r},${cy + r} ${cx - r},${cy + r}" fill="${C.metal}"/>` +
  ell(cx, cy, r * 0.42, r * 0.42, C.tile);

const washer = (cx, cy, r) => ell(cx, cy, r, r, C.metal) + ell(cx, cy, r * 0.45, r * 0.45, C.tile);

const plug = (cx, bottom) =>
  rect(cx - 9, bottom - 50, 18, 50, C.body, 6) +
  rect(cx - 15, bottom - 56, 30, 8, C.dark, 3) +
  line(`M${cx} ${bottom - 42} v22`, C.dark, 2);

const tie = (cx, cy, rot) =>
  `<g transform="rotate(${rot} ${cx} ${cy})">` +
  `<ellipse cx="${cx}" cy="${cy}" rx="30" ry="18" fill="none" stroke="${C.dark}" stroke-width="7"/>` +
  rect(cx - 8, cy + 14, 16, 12, C.dark, 2) + `</g>`;

// A carton with a spec label, as on the existing fastener packs.
const box = (lbl, contents) => tile(
  `<path d="M96 170 L200 130 L304 170 L200 210 Z" fill="${C.paper}"/>` +
  `<path d="M96 170 L200 210 V320 L96 280 Z" fill="${C.paperDark}"/>` +
  `<path d="M304 170 L200 210 V320 L304 280 Z" fill="${C.paper}"/>` +
  `<g transform="translate(214 222) skewY(-21)">${label(0, 0, 80, 34, lbl, A, 17)}</g>` +
  contents,
);

const tray = () => tile(
  rect(70, 262, 260, 60, C.body, 8) +
  [0, 1, 2, 3].map((i) => rect(84 + i * 62, 272, 50, 22, C.dark, 4)).join('') +
  hexNut(109, 283, 9) + screwAt(134, 292, 6, 3, 'pan', C.metal, 1) +
  hexNut(171, 283, 12) + screwAt(260, 292, 12, 4, 'pan', C.metal, 1) +
  screwAt(232, 292, 6, 3, 'cross', C.metal, 1) +
  label(150, 300, 100, 20, 'M4–M8', A, 13),
);

const rod = () => tile(
  rect(30, 300, 340, 12, C.metal, 6) +
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
    .map((i) => line(`M${40 + i * 10} 300 l4 12`, C.mid, 2)).join('') +
  label(150, 250, 100, 30, 'M8 × 1000', A, 15),
);

// ---- safety ----
const helmet = () => tile(
  shape('M100 300 C 100 170 300 170 300 300 Z', '#FFFFFF', ` stroke="${C.light}" stroke-width="4"`) +
  rect(90, 290, 220, 22, '#FFFFFF', 11, ` stroke="${C.light}" stroke-width="4"`) +
  rect(184, 214, 32, 10, A, 5),
);

const earPlugs = () => tile(
  rect(140, 184, 120, 134, C.paper, 10) +
  ell(200, 184, 60, 14, C.paperDark) +
  rect(140, 296, 120, 22, C.paperDark, 10) +
  ell(176, 170, 16, 11, A) +
  ell(224, 170, 16, 11, A) +
  label(156, 236, 88, 28, '35 dB', A, 15),
);

const glassesTinted = () => tile(
  line('M70 196 L30 208', C.dark, 8) +
  line('M330 196 L370 208', C.dark, 8) +
  shape('M70 196 Q200 150 330 196 L316 238 Q200 262 84 238 Z', '#5C6470', ' opacity="0.9"') +
  shape('M70 196 Q200 150 330 196 L316 238 Q200 262 84 238 Z', 'none', ` stroke="${C.dark}" stroke-width="8"`),
);

const faceShield = () => tile(
  line('M58 160 Q200 84 342 160', C.dark, 12) +
  shape('M84 146 Q200 104 316 146 L334 236 Q200 292 66 236 Z', '#BFD9EA', ' opacity="0.6"') +
  shape('M84 146 Q200 104 316 146 L334 236 Q200 292 66 236 Z', 'none', ` stroke="${C.light}" stroke-width="4"`) +
  rect(166, 212, 68, 10, A, 4),
);

const vest = () => tile(
  shape('M140 170 L 170 150 L 200 190 L 230 150 L 260 170 L 264 300 L 224 316 L 200 290 L 176 316 L 136 300 Z', A) +
  rect(136, 226, 128, 12, C.light, 2) +
  rect(136, 276, 128, 12, C.light, 2),
);

const apron = () => tile(
  line('M150 176 Q200 96 250 176', LEATHER, 10) +
  shape('M150 176 h100 v130 q0 14 -14 14 h-72 q-14 0 -14 -14 z', LEATHER) +
  rect(150, 236, 100, 8, C.dark, 2) +
  rect(186, 280, 28, 12, A, 3),
);

// ---- gloves: one drawing per family, sizes keep it and add a badge ----
const glove = ({ fill, cuff, mesh = false, long = false, badge }) => {
  const cuffTop = long ? 246 : 268;
  const cuffBottom = long ? 326 : 316;
  let s = '';
  [[150, 96], [174, 82], [198, 88], [222, 108]].forEach(([x, top]) => { s += rect(x, top, 20, 110, fill, 10); });
  s += rect(122, 206, 44, 20, fill, 10, ' transform="rotate(-28 144 216)"');
  s += rect(150, 176, 90, 100, fill, 22);
  s += rect(146, cuffTop, 98, cuffBottom - cuffTop, cuff, 10);
  s += rect(146, cuffTop + 10, 98, 6, A, 2);
  if (mesh) {
    for (let x = 158; x < 240; x += 9) s += line(`M${x} 100 V 262`, C.mid, 1.5);
    for (let y = 110; y < 260; y += 9) s += line(`M150 ${y} H 240`, C.mid, 1.5);
  }
  return tile(s, badge ? { badge, accent: A } : {});
};

const gloveFamily = (sku, opts) => ({
  [sku]: glove(opts),
  [`${sku}-S`]: glove({ ...opts, badge: 'S' }),
  [`${sku}-M`]: glove({ ...opts, badge: 'M' }),
  [`${sku}-L`]: glove({ ...opts, badge: 'L' }),
  [`${sku}-XL`]: glove({ ...opts, badge: 'XL' }),
});

// ---- knee pads and barrier tape ----
const kneePads = () => tile(
  shape('M130 236 Q130 146 200 146 Q270 146 270 236 L 262 296 Q 200 326 138 296 Z', C.dark) +
  ell(200, 218, 46, 28, '#BFD9EA', ' opacity="0.85"') +
  rect(150, 286, 100, 8, A, 3),
);

const barrierTape = () => tile(
  shape('M214 300 C 250 296 280 326 330 318 L 330 330 C 280 338 250 312 214 318 Z', RED) +
  ell(200, 250, 70, 70, RED) +
  ell(200, 250, 58, 58, 'none', ' stroke="#FFFFFF" stroke-width="14" stroke-dasharray="36 36"') +
  ell(200, 250, 22, 22, C.tile) +
  label(276, 206, 84, 28, '500 m', A, 16),
);

export const illustrations = {
  // power tools
  'DEMO-IND-1005': percussion(),
  'DEMO-IND-1006': jigsaw(false),
  'DEMO-IND-1007': circular(190, false),
  'DEMO-IND-1008': jigsaw(true),
  'DEMO-IND-1009': circular(165, true),
  'DEMO-IND-1010': multiTool(),
  'DEMO-IND-1011': orbital(),
  'DEMO-IND-1012': detail(),
  'DEMO-IND-1013': hotAir(),
  'DEMO-IND-1014': belt(),
  'DEMO-IND-1015': charger(),
  'DEMO-IND-1016': batteryLong(),
  'DEMO-IND-1017': wetDry(),
  'DEMO-IND-1018': grinderCordless(),
  // fasteners
  'DEMO-IND-2004': box('3.5 × 30', screwAt(70, 322, 60, 6) + screwAt(94, 322, 60, 6)),
  'DEMO-IND-2005': box('5 × 60', screwAt(66, 322, 120, 8) + screwAt(92, 322, 120, 8)),
  'DEMO-IND-2006': box('5 × 80', screwAt(66, 322, 160, 8, 'pan', STAINLESS) + screwAt(92, 322, 160, 8, 'pan', STAINLESS)),
  'DEMO-IND-2007': box('M6 × 30', screwAt(70, 322, 60, 6, 'hex') + screwAt(104, 322, 60, 6, 'hex')),
  'DEMO-IND-2008': box('M10 × 60', screwAt(66, 322, 120, 9, 'hex') + screwAt(100, 322, 120, 9, 'hex')),
  'DEMO-IND-2009': box('M8', hexNut(70, 306, 22) + hexNut(112, 318, 22) + hexNut(92, 262, 20)),
  'DEMO-IND-2010': box('M6', hexNut(72, 306, 16) + hexNut(106, 318, 16) + hexNut(96, 266, 14)),
  'DEMO-IND-2011': box('M8', washer(70, 300, 22) + washer(108, 314, 22) + washer(92, 262, 18)),
  'DEMO-IND-2012': rod(),
  'DEMO-IND-2013': box('8 × 40', plug(70, 322) + plug(104, 322)),
  'DEMO-IND-2014': box('200 mm', tie(66, 292, -20) + tie(104, 300, 10) + tie(84, 262, 30)),
  'DEMO-IND-2015': tile(
    shape('M116 200 L 284 200 L 300 322 L 100 322 Z', C.paper) +
    [[140, 150], [160, 140], [186, 146], [214, 138], [240, 150], [258, 160]]
      .map(([x, y]) => line(`M${x + 14} 206 L ${x} ${y}`, C.metal, 4)).join('') +
    label(150, 252, 100, 30, '60 mm', A, 16),
  ),
  'DEMO-IND-2016': box('M6 × 20', grub(70, 322) + grub(104, 322)),
  'DEMO-IND-2017': box('M5 × 16', screwAt(70, 322, 32, 8, 'cheese', STAINLESS) + screwAt(104, 322, 32, 8, 'cheese', STAINLESS)),
  'DEMO-IND-2018': box('M4 × 12', screwAt(70, 322, 24, 6, 'cross') + screwAt(100, 322, 24, 6, 'cross')),
  'DEMO-IND-2019': box('4.2 × 19', screwAt(70, 322, 38, 7, 'pan', C.metal, 1.6) + screwAt(100, 322, 38, 7, 'pan', C.metal, 1.6)),
  'DEMO-IND-2020': tray(),
  'DEMO-IND-2021': box('M10', squareNut(70, 302, 22) + squareNut(112, 316, 22) + squareNut(92, 260, 18)),
  'DEMO-IND-2022': box('M12 × 80', screwAt(96, 322, 150, 11, 'hex') + screwAt(128, 322, 150, 11, 'hex')),
  // safety
  'DEMO-IND-3004': helmet(),
  'DEMO-IND-3005': earPlugs(),
  'DEMO-IND-3006': glassesTinted(),
  'DEMO-IND-3007': faceShield(),
  'DEMO-IND-3008': vest(),
  'DEMO-IND-3009': apron(),
  ...gloveFamily('DEMO-IND-3010', { fill: NITRILE_BLUE, cuff: NITRILE_BLUE }),
  ...gloveFamily('DEMO-IND-3011', { fill: LEATHER, cuff: LEATHER }),
  ...gloveFamily('DEMO-IND-3012', { fill: STAINLESS, cuff: C.metal, mesh: true }),
  ...gloveFamily('DEMO-IND-3013', { fill: GREEN, cuff: GREEN }),
  ...gloveFamily('DEMO-IND-3014', { fill: '#A0683E', cuff: LEATHER, long: true }),
  'DEMO-IND-3015': kneePads(),
  'DEMO-IND-3016': barrierTape(),
};
