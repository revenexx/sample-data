// More lab illustrations, keyed by SKU (part b). Same style as lab.mjs:
// flat shapes, neutral colours, one accent detail per drawing, spec text only.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.lab;
const BOTTOM = 326;
const G = '#BFD9EA'; // borosilicate / glass
const GLASS = `fill="${G}" fill-opacity="0.85" stroke="${C.light}" stroke-width="2"`;
const COPPER = '#C47A4A';

const rect = (x, y, w, h, fill, rx = 0) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}"/>`;
const glassRect = (x, y, w, h, rx = 6) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" ${GLASS}/>`;
const glassPath = (d) => `<path d="${d}" ${GLASS}/>`;
const line = (x1, y1, x2, y2, stroke, w = 3) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round"/>`;
const dot = (cx, cy, r, fill) => `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${fill}"/>`;

// Measuring cylinder: glass tube on a foot, liquid in the lower part, graduation marks.
const cylinder = (text, w, h) => {
  const x = 200 - w / 2, top = BOTTOM - h, liquid = h * 0.35;
  let marks = '';
  for (let i = 1; i <= 4; i++) {
    const y = BOTTOM - 16 - ((h - 60) * i) / 5;
    marks += line(x + w - 26, y, x + w - 8, y, C.mid, 3);
  }
  const lw = Math.min(96, w - 8);
  return tile(
    glassRect(x, top, w, h - 10, 8) +
    rect(x + 3, BOTTOM - 10 - liquid, w - 6, liquid, C.light, 2) +
    marks +
    rect(x - 12, BOTTOM - 10, w + 24, 10, C.body, 4) +
    rect(x - 4, top - 6, w + 8, 8, C.light, 3) +
    label(200 - lw / 2, 196, lw, 34, text, A, lw < 90 ? 15 : 18),
  );
};

// Erlenmeyer flask: square-shouldered cone on a flat base, short neck.
const erlenmeyer = (text, bodyW, bodyH, neckW, neckH) => {
  const bt = BOTTOM - bodyH, nt = bt - neckH, hb = bodyW / 2, nw = neckW / 2;
  const d = `M${200 - nw} ${nt} V${bt} L${200 - hb} ${BOTTOM} H${200 + hb} L${200 + nw} ${bt} V${nt} Z`;
  return tile(
    glassPath(d) +
    rect(200 - nw - 5, nt - 6, neckW + 10, 8, C.light, 3) +
    label(150, Math.round((bt + BOTTOM) / 2) - 17, 100, 34, text, A, 18),
  );
};

const roundFlask = () => tile(
  `<circle cx="200" cy="250" r="76" ${GLASS}/>` +
  glassRect(182, 130, 36, 56, 3) +
  rect(170, 110, 60, 22, C.body, 4) +
  label(150, 233, 100, 34, '500 ml', A, 18),
);

const beakerLow = () => tile(
  glassRect(110, 206, 180, 120, 6) +
  rect(104, 200, 192, 8, C.light, 3) +
  line(246, 240, 270, 240, C.mid) + line(246, 270, 270, 270, C.mid) + line(246, 300, 270, 300, C.mid) +
  label(150, 249, 100, 34, '250 ml', A, 18),
);

const beakerTall = () => tile(
  glassRect(126, 120, 148, 206, 6) +
  rect(120, 114, 160, 8, C.light, 3) +
  [150, 190, 230, 270].map((y) => line(240, y, 264, y, C.mid)).join('') +
  label(152, 210, 96, 34, '1000 ml', A, 16),
);

// Pack of 10 test tubes with a sleeve band.
const testTubes = () => tile(
  [140, 170, 200, 230, 260].map((x) =>
    `<path d="M${x - 11} 130 V315 A11 11 0 0 0 ${x + 11} 315 V130 Z" ${GLASS}/>` +
    rect(x - 13, 126, 26, 6, C.light, 2)).join('') +
  label(122, 236, 156, 36, 'pack of 10', A, 18),
);

const volFlask = () => tile(
  glassPath('M150 326 H250 C282 300 262 250 232 226 V150 H168 V226 C138 250 118 300 150 326 Z') +
  rect(160, 116, 80, 36, C.dark, 6) +
  rect(168, 196, 64, 3, A) +
  label(150, 262, 100, 34, '100 ml', A, 18),
);

// Volumetric pipette: long thin tube with a bulb, tip at the floor.
const volPipette = () => tile(
  glassRect(192, 60, 16, 250, 3) +
  `<ellipse cx="200" cy="200" rx="30" ry="50" ${GLASS}/>` +
  `<path d="M192 306 H208 L202 326 H198 Z" fill="${C.light}"/>` +
  rect(192, 132, 16, 3, A) +
  label(232, 140, 120, 34, '10 ml', A, 20),
);

const burette = () => tile(
  glassRect(188, 60, 24, 226, 3) +
  [100, 130, 160, 190, 220, 250].map((y) => line(188, y, 200, y, C.mid, 3)).join('') +
  rect(178, 284, 44, 20, C.body, 4) +
  rect(218, 292, 30, 6, A, 3) +
  `<path d="M196 304 H204 L201 326 H199 Z" fill="${C.light}"/>` +
  label(230, 120, 120, 34, '50 ml', A, 20),
);

// Separating funnel: pear-shaped body, stopper on top, stopcock below.
const sepFunnel = () => tile(
  rect(176, 84, 48, 20, C.dark, 4) +
  glassRect(192, 102, 16, 30, 2) +
  glassPath('M150 130 H250 C272 190 252 246 214 276 H186 C148 246 128 190 150 130 Z') +
  glassRect(195, 272, 10, 14, 2) +
  rect(180, 284, 40, 14, C.body, 4) +
  rect(218, 278, 24, 8, A, 3) +
  rect(193, 296, 14, 28, C.body, 3) +
  label(150, 190, 100, 34, '500 ml', A, 18),
);

// Desiccator: wide glass bowl with a domed lid on a base plate, perforated shelf inside.
const desiccator = () => tile(
  rect(96, 310, 208, 14, C.body, 4) +
  glassRect(100, 212, 200, 98, 6) +
  rect(108, 252, 184, 6, C.light, 2) +
  `<path d="M96 212 Q96 166 200 166 Q304 166 304 212 Z" fill="${G}" fill-opacity="0.85" stroke="${C.light}" stroke-width="2"/>` +
  dot(200, 158, 10, C.dark) +
  label(150, 266, 100, 32, '250 mm', A, 18),
);

// Liebig condenser on a clamp: jacket with nipples, inner tube with hose ends.
const condenser = () => tile(
  rect(184, 96, 12, 222, C.metal, 3) +
  rect(132, 318, 136, 8, C.dark, 3) +
  rect(62, 194, 34, 6, C.mid, 3) + rect(304, 194, 34, 6, C.mid, 3) +
  rect(92, 189, 216, 10, C.light, 3) +
  glassRect(112, 176, 176, 36, 14) +
  rect(138, 212, 12, 18, C.body, 2) + rect(248, 158, 12, 18, C.body, 2) +
  rect(176, 204, 24, 22, C.body, 3) + rect(176, 204, 24, 4, A, 2) +
  label(228, 232, 104, 30, '300 mm', A, 16),
);

const funnel = () => tile(
  glassPath('M120 150 H280 L220 262 H180 Z') +
  glassRect(182, 262, 36, 62, 3) +
  label(290, 200, 90, 30, '75 mm', A, 16),
);

// Pack of 10 glass stirring rods lying on the bench.
const rods = () => tile(
  [0, 1, 2, 3, 4].map((i) =>
    `<line x1="${90 + i * 6}" y1="${296 - i * 12}" x2="${318 - i * 6}" y2="${262 - i * 12}" stroke="${C.light}" stroke-width="11" stroke-linecap="round"/>` +
    `<line x1="${90 + i * 6}" y1="${296 - i * 12}" x2="${318 - i * 6}" y2="${262 - i * 12}" stroke="${G}" stroke-width="7" stroke-linecap="round"/>`).join('') +
  label(134, 150, 132, 30, '10 × 200 mm', A, 16),
);

// Safety glasses: clear lenses with side shields, temples running down to the floor.
const safetyGlasses = () => tile(
  `<path d="M96 256 L76 326 M304 256 L324 326" stroke="${C.dark}" stroke-width="9" stroke-linecap="round" fill="none"/>` +
  `<rect x="92" y="196" width="100" height="62" rx="26" fill="#FFFFFF" fill-opacity="0.7" stroke="${C.dark}" stroke-width="9"/>` +
  `<rect x="208" y="196" width="100" height="62" rx="26" fill="#FFFFFF" fill-opacity="0.7" stroke="${C.dark}" stroke-width="9"/>` +
  rect(186, 212, 28, 8, C.dark, 3) +
  rect(80, 208, 14, 40, C.dark, 4) + rect(306, 208, 14, 40, C.dark, 4) +
  rect(190, 216, 20, 3, A, 1),
);

// Goggles: one wide vented lens with an elastic strap, standing on its straps.
const goggles = () => tile(
  rect(22, 236, 356, 16, C.mid, 8) +
  rect(22, 236, 16, 16, A, 4) +
  `<rect x="72" y="206" width="256" height="98" rx="46" fill="${G}" fill-opacity="0.85" stroke="${C.dark}" stroke-width="14"/>` +
  `<rect x="90" y="216" width="220" height="22" rx="11" fill="#FFFFFF" fill-opacity="0.4"/>` +
  [[112, 246], [112, 272], [288, 246], [288, 272]].map(([x, y]) => dot(x, y, 4, C.dark)).join(''),
);

// Lab coat, drawn at a scale per size; the bottom hem stays on the floor line.
const labCoat = (size, s) => tile(
  `<g transform="translate(200 ${BOTTOM}) scale(${s}) translate(-200 -${BOTTOM})">` +
  `<path d="M150 130 L250 130 L290 160 L302 290 L290 300 L280 300 L272 214 L270 326 L130 326 L128 214 L120 300 L110 300 L98 290 L110 160 Z" fill="#FFFFFF" stroke="${C.light}" stroke-width="3" stroke-linejoin="round"/>` +
  `<path d="M168 130 L200 168 L232 130 Z" fill="${C.light}"/>` +
  `<line x1="200" y1="168" x2="200" y2="326" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="218" y="236" width="36" height="34" rx="4" fill="none" stroke="${C.light}" stroke-width="3"/>` +
  [200, 230, 260, 290].map((y) => dot(190, y, 3.5, C.mid)).join('') +
  `<rect x="102" y="292" width="20" height="6" rx="2" fill="${A}"/><rect x="278" y="292" width="20" height="6" rx="2" fill="${A}"/>` +
  `</g>` +
  label(146, 300, 108, 28, `size ${size}`, A, 16),
);

// Cut-resistant or heat-resistant glove: fingers, palm, thumb, cuff.
const glove = (fill, cuffTop, text, short = 0) => {
  const finger = (x, y, h) => rect(x, y + short, 20, h - short, fill, 10);
  return tile(
    finger(150, 150, 70) + finger(174, 136, 84) + finger(198, 140, 80) + finger(222, 156, 64) +
    rect(146, 196, 108, 96, fill, 26) +
    `<rect x="120" y="208" width="34" height="20" rx="10" fill="${fill}" transform="rotate(-30 137 218)"/>` +
    rect(144, cuffTop, 112, BOTTOM - cuffTop, fill === COPPER ? COPPER : C.dark, 8) +
    rect(144, cuffTop + 10, 112, 6, A, 3) +
    label(250, 110, 120, 30, text, A, 16),
  );
};

// Apron folded in a pack of 100, one apron laid on top.
const apron = () => tile(
  rect(110, 300, 180, 26, C.light, 4) +
  rect(118, 276, 164, 24, C.metal, 4) +
  rect(126, 252, 148, 24, C.light, 4) +
  glassPath('M150 168 H250 L262 206 V252 H138 V206 Z') +
  `<path d="M158 168 Q200 112 242 168" fill="none" stroke="${C.dark}" stroke-width="4"/>` +
  line(138, 206, 118, 190, C.mid, 3) + line(262, 206, 282, 190, C.mid, 3) +
  label(146, 280, 108, 28, '×100', A, 18),
);

// Face shield: clear visor on a headband, held on a short stand.
const faceShield = () => tile(
  `<path d="M92 120 Q200 40 308 120" fill="none" stroke="${C.dark}" stroke-width="12" stroke-linecap="round"/>` +
  rect(186, 72, 28, 12, A, 4) +
  `<path d="M100 122 Q200 98 300 122 L300 248 Q200 330 100 248 Z" fill="${G}" fill-opacity="0.7" stroke="${C.light}" stroke-width="2"/>` +
  `<path d="M122 150 Q132 200 126 240" fill="none" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="6" stroke-linecap="round"/>`,
);

// Spill tray: shallow tray with a raised rim and a recess.
const spillTray = () => tile(
  rect(60, 282, 280, 44, C.body, 8) +
  rect(74, 292, 252, 22, C.dark, 4) +
  rect(60, 282, 280, 6, A, 3) +
  label(150, 236, 100, 30, '600 mm', A, 16),
);

// Broken-glass container: tall body, lid with a slot.
const brokenGlass = () => tile(
  rect(128, 124, 144, 202, C.body, 14) +
  rect(120, 104, 160, 22, C.dark, 6) +
  rect(180, 110, 40, 8, C.mid, 3) +
  rect(128, 296, 144, 8, A, 2) +
  label(150, 200, 100, 34, '10 l', A, 20),
);

// Disposable hair covers: a cap rising out of a pouch.
const hairCovers = () => tile(
  `<path d="M150 266 Q200 150 250 266 Z" fill="#FFFFFF" stroke="${C.light}" stroke-width="3"/>` +
  rect(122, 262, 156, 64, C.paper, 8) +
  label(150, 288, 100, 28, '×100', A, 18),
);

// Test tube rack: tubes stand in the holes of a front board.
const rack24 = () => {
  const xs = [92, 120, 148, 176, 204, 232, 260, 288];
  return tile(
    xs.map((x, i) => `<path d="M${x - 8} ${176 + (i % 2) * 14} V300 H${x + 8} V${176 + (i % 2) * 14} Z" ${GLASS}/>`).join('') +
    rect(74, 272, 252, 54, C.body, 8) +
    xs.map((x) => dot(x, 284, 7, C.dark)).join('') +
    label(134, 298, 132, 24, '24 places', A, 14),
  );
};

// 50 ml tube rack: four white conical tubes, board with the spec on it.
const rack15 = () => {
  const tubeAt = (x) =>
    `<path d="M${x - 13} 132 V246 L${x - 6} 300 H${x + 6} L${x + 13} 246 V132 Z" fill="#FFFFFF" stroke="${C.light}" stroke-width="2"/>` +
    rect(x - 15, 118, 30, 14, C.dark, 3);
  return tile(
    [110, 165, 220, 275].map(tubeAt).join('') +
    rect(60, 290, 280, 36, C.body, 8) +
    dot(90, 308, 7, C.dark) + dot(310, 308, 7, C.dark) +
    label(120, 296, 160, 26, '15 × 50 ml', A, 16),
  );
};

// A box seen from the front-right: front face, right face, a grid of positions on the lid.
const gridBox = ({ x, yF, w, h, dx, dy, cols, rows, r, front, right, top, dots, text, size = 18 }) => {
  const P = (u, v) => [x + u * w + v * dx, yF - v * dy];
  const pt = (u, v) => P(u, v).join(' ');
  const [frx, fry] = P(1, 0), [brx, bry] = P(1, 1);
  let holes = '';
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      const [cx, cy] = P((i + 0.5) / cols, (j + 0.5) / rows);
      holes += dot(cx, cy, r, dots);
    }
  }
  return tile(
    `<path d="M${pt(0, 0)} L${pt(1, 0)} L${pt(1, 1)} L${pt(0, 1)} Z" fill="${top}"/>` +
    `<path d="M${frx} ${fry} L${brx} ${bry} V${bry + h} L${frx} ${fry + h} Z" fill="${right}"/>` +
    rect(x, yF, w, h, front) +
    holes +
    label(x + w / 2 - 50, yF + h / 2 - 17, 100, 34, text, A, size),
  );
};

// Stackable 5 l box with a handle cut-out.
const storage5 = () => tile(
  rect(110, 236, 180, 90, C.body, 8) +
  rect(102, 220, 196, 20, C.mid, 6) +
  rect(168, 262, 64, 16, C.dark, 6) +
  label(150, 292, 100, 28, '5 l', A, 18),
);

// Stackable 25 l box: larger, with a lid and a wide grip.
const storage25 = () => tile(
  rect(78, 190, 244, 136, C.body, 8) +
  rect(70, 170, 260, 24, C.mid, 8) +
  rect(150, 206, 100, 14, C.dark, 6) +
  label(150, 262, 100, 34, '25 l', A, 18),
);

// Wall-mounted holder: a metal plate with four pipette slots on a base.
const wallHolder = () => tile(
  rect(132, 140, 136, 156, C.metal, 8) +
  [0, 1, 2, 3].map((i) => rect(146, 160 + i * 32, 108, 10, C.dark, 5)).join('') +
  rect(110, 296, 180, 30, C.body, 6) +
  label(150, 300, 100, 22, '4 places', A, 14),
);

// Screw-cap glass storage jar.
const jar = () => tile(
  glassPath('M130 176 Q130 150 150 150 H250 Q270 150 270 176 V300 Q270 326 240 326 H160 Q130 326 130 300 Z') +
  rect(138, 118, 124, 34, C.dark, 6) +
  line(170, 124, 170, 146, C.mid, 2) + line(230, 124, 230, 146, C.mid, 2) +
  label(150, 226, 100, 34, '1000 ml', A, 18),
);

// Wide-neck PE bottle, white, with a dark screw cap.
const bottle = () => tile(
  `<path d="M150 326 V196 Q150 178 166 170 V150 H234 V170 Q250 178 250 196 V326 Z" fill="#FFFFFF" stroke="${C.light}" stroke-width="3"/>` +
  rect(160, 122, 80, 30, C.dark, 4) +
  label(150, 236, 100, 34, '500 ml', A, 18),
);

// Sheet of cryo labels lying flat: 20 cells on a skewed sheet, one in the accent.
const labelSheet = () => {
  const FL = [96, 300], FR = [304, 300], BL = [136, 200];
  const P = (u, v) => [FL[0] + u * (FR[0] - FL[0]) + v * (BL[0] - FL[0]), FL[1] + u * (FR[1] - FL[1]) + v * (BL[1] - FL[1])];
  const poly = (pts, fill, stroke = 'none') =>
    `<path d="M${pts.map((p) => p.join(' ')).join(' L')} Z" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
  let cells = '';
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 4; j++) {
      const u0 = 0.08 + i * 0.168, v0 = 0.12 + j * 0.2;
      cells += poly([P(u0, v0), P(u0 + 0.148, v0), P(u0 + 0.148, v0 + 0.16), P(u0, v0 + 0.16)],
        i === 0 && j === 0 ? A : '#FFFFFF');
    }
  }
  return tile(
    poly([P(0, 0), P(1, 0), P(1, 1), P(0, 1)], C.paper, C.paperDark) + cells +
    label(24, 150, 118, 30, '100 labels', A, 14),
  );
};

// ---- Batch 2 (SKUs added with the 125-record build): one drawing per SKU ----
const nSvg = (x, y, w, h, fill, rx = 0, extra = '') =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" ${extra}/>`;
const nWhite = (x, y, w, h, rx) => nSvg(x, y, w, h, '#FFFFFF', rx, `stroke="${C.light}" stroke-width="2"`);

// Magnetic stirrer without heating: plain plate, one knob, a stir bar in a beaker.
const nStirrer = () => tile(
  rect(112, 290, 176, 36, C.dark, 8) +
  rect(100, 274, 200, 18, C.metal, 6) +
  glassRect(150, 186, 100, 88, 6) +
  rect(168, 256, 64, 10, C.dark, 4) +
  dot(256, 310, 7, A) +
  label(146, 293, 84, 24, '1 l', A, 16),
);

// Laboratory water bath: tank with a glass window, a lid on top.
const nBath = () => tile(
  rect(96, 200, 208, 126, C.body, 10) +
  glassRect(116, 224, 168, 62, 6) +
  rect(84, 186, 232, 16, C.mid, 8) +
  rect(186, 170, 28, 16, C.dark, 6) +
  label(150, 294, 100, 24, '10 l', A, 16),
);

// Vacuum drying oven: box with a round door window and a hose to the pump port.
const nVacOven = () => tile(
  rect(104, 176, 192, 150, C.body, 8) +
  rect(104, 176, 192, 14, C.mid, 6) +
  `<circle cx="200" cy="240" r="36" ${GLASS}/>` +
  `<path d="M296 214 C 336 186, 344 256, 320 300" fill="none" stroke="${C.dark}" stroke-width="7" stroke-linecap="round"/>` +
  dot(296, 214, 9, C.light) +
  label(150, 284, 100, 26, '23 l', A, 16),
);

// Laboratory refrigerator: white two-door cabinet with a split line and handles.
const nFridge = () => tile(
  `<rect x="128" y="120" width="144" height="206" rx="12" fill="#FFFFFF" stroke="${C.light}" stroke-width="3"/>` +
  line(130, 200, 270, 200, C.light, 3) +
  rect(244, 150, 8, 36, C.mid, 4) +
  rect(244, 226, 8, 44, C.mid, 4) +
  rect(128, 120, 144, 8, A, 3) +
  label(142, 290, 100, 26, '85 l', A, 16),
);

// Pipette tips in a rack: tall tip, optional dark filter band near the top.
const nTipRack = (tipH, text, band) => {
  const RT = 250;
  let tips = '';
  [96, 136, 176, 216, 256, 296].forEach((x) => {
    tips += `<path d="M${x - 14} ${RT - tipH} H${x + 14} L${x + 4} ${RT} H${x - 4} Z" fill="#FFFFFF" stroke="${C.light}" stroke-width="2"/>`;
    if (band) tips += rect(x - 12, RT - tipH + 14, 24, 10, C.dark, 3);
  });
  return tile(
    tips +
    rect(64, RT - 4, 272, 10, C.mid, 4) +
    rect(72, RT + 6, 256, 64, C.body, 6) +
    label(150, 282, 100, 26, text, A, 16),
  );
};

// Electronic pipette controller: rounded handset with a display, buttons and one accent button.
const nController = () => tile(
  rect(140, 142, 120, 184, C.body, 44) +
  rect(154, 162, 92, 44, C.dark, 8) +
  dot(172, 240, 9, C.mid) + dot(200, 240, 9, C.mid) + dot(228, 240, 9, C.mid) +
  dot(200, 282, 16, A) +
  label(150, 300, 100, 22, '0.4 kg', A, 14),
);

// Sealing film: a roll standing on its edge, seen face-on, with a hollow core.
const nRoll = () => tile(
  `<circle cx="200" cy="236" r="88" fill="#FFFFFF" stroke="${C.light}" stroke-width="3"/>` +
  `<circle cx="200" cy="236" r="60" fill="none" stroke="${C.light}" stroke-width="2"/>` +
  dot(200, 236, 30, C.body) +
  label(150, 268, 100, 30, '10 m', A, 17),
);

// Snap-on caps: a bag with three domed caps standing out of it.
const nCaps = () => tile(
  [146, 200, 254].map((x) =>
    `<path d="M${x - 24} 280 V262 Q${x - 24} 232 ${x} 232 Q${x + 24} 232 ${x + 24} 262 V280 Z" fill="#FFFFFF" stroke="${C.light}" stroke-width="2"/>`).join('') +
  rect(120, 276, 160, 50, C.light, 6) +
  label(150, 290, 100, 26, '100', A, 16),
);

// Permanent markers: four pens standing side by side, each with its own cap colour.
const nMarkers = () => tile(
  [[124, C.dark], [168, C.body], [212, '#FFFFFF'], [256, C.mid]].map(([x, c]) =>
    `<rect x="${x - 15}" y="150" width="30" height="30" rx="8" fill="${c}" stroke="${C.light}" stroke-width="2"/>` +
    `<rect x="${x - 13}" y="176" width="26" height="150" rx="8" fill="${c}" stroke="${C.light}" stroke-width="2"/>` +
    rect(x - 13, 230, 26, 8, A, 2)).join('') +
  label(150, 96, 100, 30, '1 mm', A, 17),
);

// Screw-cap tube: translucent body with a flat-topped ribbed cap.
const nScrewTube = () => tile(
  `<path d="M164 186 H236 V306 Q236 326 216 326 H184 Q164 326 164 306 Z" fill="#FFFFFF" fill-opacity="0.6" stroke="${C.light}" stroke-width="3"/>` +
  rect(154, 160, 92, 34, C.body, 6) +
  [166, 180, 194, 208, 222, 236].map((x) => line(x, 166, x, 188, C.mid, 2)).join('') +
  label(150, 240, 100, 30, '4 ml', A, 17),
);

// Lab wipes: a dispenser box with a sheet pulled up through the slot.
const nWipes = () => tile(
  `<rect x="150" y="170" width="100" height="100" fill="#FFFFFF" stroke="${C.light}" stroke-width="2"/>` +
  line(160, 196, 240, 196, C.light, 2) + line(160, 220, 240, 220, C.light, 2) +
  rect(112, 258, 176, 68, C.body, 8) +
  rect(132, 250, 136, 14, C.dark, 5) +
  label(150, 286, 100, 26, '200', A, 16),
);

// Silicone stoppers: five truncated cones, wide head up, growing in size.
const nStoppers = () => tile(
  [[70, 44, 60], [134, 54, 70], [198, 64, 80], [262, 74, 90], [326, 84, 100]].map(([x, w, h]) => {
    const top = 326 - h;
    return `<path d="M${x - w / 2} ${top} H${x + w / 2} L${x + w * 0.36} 326 H${x - w * 0.36} Z" fill="#E3DCCD" stroke="${C.light}" stroke-width="2"/>` +
      rect(x - w / 2, top, w, 8, C.paperDark, 3);
  }).join('') +
  label(150, 96, 100, 26, '× 20', A, 16),
);

// Round-bottom flask with a standard ground joint on the neck.
const nRoundFlask = (text, r, neckW) => {
  const top = BOTTOM - 2 * r;
  return tile(
    `<circle cx="200" cy="${BOTTOM - r}" r="${r}" ${GLASS}/>` +
    glassRect(200 - neckW / 2, top - 46, neckW, 60, 3) +
    rect(200 - neckW / 2 - 6, top - 56, neckW + 12, 12, C.light, 3) +
    label(150, BOTTOM - r - 17, 100, 34, text, A, 18),
  );
};

// Glass vial with a dark screw cap; three standing, the middle one labelled.
const nVial = (x, h, w) => {
  const top = BOTTOM - h, l = x - w / 2, r = x + w / 2;
  return `<path d="M${l} ${top} V${BOTTOM - 12} Q${l} ${BOTTOM} ${x} ${BOTTOM} Q${r} ${BOTTOM} ${r} ${BOTTOM - 12} V${top} Z" ${GLASS}/>` +
    rect(l - 3, top - 14, w + 6, 20, C.dark, 4);
};
const nVials = () => tile(
  nVial(124, 150, 56) + nVial(276, 150, 56) + nVial(200, 190, 56) +
  label(150, 262, 100, 30, '20 ml', A, 17),
);

// Vinyl gloves: one glove standing out of a dispenser box.
const nGloveBox = () => tile(
  nWhite(164, 118, 16, 70, 8) + nWhite(184, 108, 16, 80, 8) + nWhite(204, 112, 16, 76, 8) + nWhite(222, 130, 14, 58, 7) +
  nWhite(160, 170, 80, 80, 22) +
  rect(100, 246, 200, 80, C.body, 8) +
  rect(96, 238, 208, 14, C.mid, 6) +
  label(150, 286, 100, 26, '100', A, 16),
);

// Over-spectacle goggles: a thick frame over two thin spectacle outlines.
const nOverGoggles = () => tile(
  `<rect x="112" y="210" width="84" height="56" rx="24" fill="none" stroke="${C.mid}" stroke-width="4"/>` +
  `<rect x="204" y="210" width="84" height="56" rx="24" fill="none" stroke="${C.mid}" stroke-width="4"/>` +
  `<rect x="90" y="192" width="220" height="92" rx="42" fill="${G}" fill-opacity="0.5" stroke="${C.dark}" stroke-width="14"/>` +
  label(140, 296, 120, 26, '0.2 kg', A, 14),
);

// Rack for 48 tubes: a tray with a 8 x 6 grid of openings.
const nRack48 = () => {
  let holes = '';
  for (let i = 0; i < 8; i++) for (let j = 0; j < 6; j++) holes += dot(104 + i * 26, 232 + j * 15, 5.5, C.dark);
  return tile(
    rect(80, 218, 240, 106, C.body, 10) + holes +
    label(150, 178, 100, 26, '48', A, 16),
  );
};

// Card archive box: paper-coloured carton with a hand hole and a lid flap.
const nCardBox = () => tile(
  rect(104, 196, 192, 130, C.paper, 6) +
  rect(100, 186, 200, 16, C.paperDark, 5) +
  rect(170, 218, 60, 14, C.paperDark, 6) +
  label(150, 262, 100, 30, '100', A, 17),
);

export const illustrations = {
  'DEMO-LAB-4001': cylinder('100 ml', 74, 170),
  'DEMO-LAB-4002': cylinder('250 ml', 92, 230),
  'DEMO-LAB-4003': cylinder('1000 ml', 124, 290),
  'DEMO-LAB-4004': erlenmeyer('250 ml', 150, 110, 44, 90),
  'DEMO-LAB-4005': erlenmeyer('500 ml', 196, 140, 52, 100),
  'DEMO-LAB-4006': roundFlask(),
  'DEMO-LAB-4007': beakerLow(),
  'DEMO-LAB-4008': beakerTall(),
  'DEMO-LAB-4009': testTubes(),
  'DEMO-LAB-4010': volFlask(),
  'DEMO-LAB-4011': volPipette(),
  'DEMO-LAB-4012': burette(),
  'DEMO-LAB-4013': sepFunnel(),
  'DEMO-LAB-4014': desiccator(),
  'DEMO-LAB-4015': condenser(),
  'DEMO-LAB-4016': funnel(),
  'DEMO-LAB-4017': rods(),
  'DEMO-LAB-5001': safetyGlasses(),
  'DEMO-LAB-5002': goggles(),
  'DEMO-LAB-5003': labCoat('50', 1),
  'DEMO-LAB-5004': glove(C.mid, 282, 'level 5'),
  'DEMO-LAB-5005': glove(C.light, 282, 'level 3', 10),
  'DEMO-LAB-5006': apron(),
  'DEMO-LAB-5007': faceShield(),
  'DEMO-LAB-5008': spillTray(),
  'DEMO-LAB-5009': brokenGlass(),
  'DEMO-LAB-5010': glove(COPPER, 230, '250 °C'),
  'DEMO-LAB-5011': labCoat('54', 1.06),
  'DEMO-LAB-5012': hairCovers(),
  'DEMO-LAB-6001': rack24(),
  'DEMO-LAB-6002': rack15(),
  'DEMO-LAB-6003': gridBox({ x: 100, yF: 252, w: 200, h: 70, dx: 40, dy: 40, cols: 12, rows: 8, r: 3.2, front: C.body, right: C.dark, top: C.light, dots: C.mid, text: '96' }),
  'DEMO-LAB-6004': gridBox({ x: 110, yF: 256, w: 170, h: 64, dx: 46, dy: 46, cols: 9, rows: 9, r: 4, front: C.mid, right: C.body, top: C.light, dots: C.dark, text: '81' }),
  'DEMO-LAB-6005': gridBox({ x: 96, yF: 250, w: 180, h: 76, dx: 30, dy: 50, cols: 10, rows: 10, r: 3.4, front: C.paper, right: C.paperDark, top: '#FFFFFF', dots: C.mid, text: '100' }),
  'DEMO-LAB-6006': storage5(),
  'DEMO-LAB-6007': wallHolder(),
  'DEMO-LAB-6008': jar(),
  'DEMO-LAB-6009': bottle(),
  'DEMO-LAB-6010': labelSheet(),
  'DEMO-LAB-6011': storage25(),
  'DEMO-LAB-6012': gridBox({ x: 120, yF: 268, w: 160, h: 54, dx: 50, dy: 30, cols: 5, rows: 5, r: 6, front: C.body, right: C.dark, top: G, dots: C.mid, text: '25' }),
  'DEMO-LAB-1019': nStirrer(),
  'DEMO-LAB-1020': nBath(),
  'DEMO-LAB-1021': nVacOven(),
  'DEMO-LAB-1022': nFridge(),
  'DEMO-LAB-2014': nTipRack(70, '2 µl', false),
  'DEMO-LAB-2015': nTipRack(120, '1000 µl', true),
  'DEMO-LAB-2016': nController(),
  'DEMO-LAB-3019': nRoll(),
  'DEMO-LAB-3020': nCaps(),
  'DEMO-LAB-3021': nMarkers(),
  'DEMO-LAB-3022': nScrewTube(),
  'DEMO-LAB-3023': nWipes(),
  'DEMO-LAB-3024': nStoppers(),
  'DEMO-LAB-4018': erlenmeyer('100 ml', 100, 96, 34, 44),
  'DEMO-LAB-4019': nRoundFlask('250 ml', 66, 30),
  'DEMO-LAB-4020': cylinder('10 ml', 64, 150),
  'DEMO-LAB-4021': nVials(),
  'DEMO-LAB-5013': nGloveBox(),
  'DEMO-LAB-5014': nOverGoggles(),
  'DEMO-LAB-6013': nRack48(),
  'DEMO-LAB-6014': gridBox({ x: 116, yF: 250, w: 150, h: 70, dx: 40, dy: 40, cols: 9, rows: 9, r: 3, front: C.body, right: C.dark, top: G, dots: C.mid, text: '81' }),
  'DEMO-LAB-6015': nCardBox(),
};
