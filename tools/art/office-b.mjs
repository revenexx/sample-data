// More office illustrations, keyed by SKU (part b). Same style as office.mjs.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.office;

// Helpers, copied from office.mjs (not imported from it).
const R = (x, y, w, h, fill, rx = 4, extra = '') =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" ${extra}/>`;
const P = (d, fill, extra = '') => `<path d="${d}" fill="${fill}" ${extra}/>`;
const E = (cx, cy, rx, ry, fill, extra = '') =>
  `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}" ${extra}/>`;
const L = (x1, y1, x2, y2, stroke, w = 3) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round"/>`;
const OUT = `stroke="${C.light}" stroke-width="2"`;

// Colour pairs [face, shade] for colour variants and the neutral model.
const COL = {
  grey: ['#8A9099', '#6E7580'],
  blue: ['#2E5FA8', '#244D8A'],
  red: ['#C2403A', '#9E302B'],
  green: ['#3E8E5A', '#2F7046'],
  black: ['#2A2D33', '#1C1F24'],
  yellow: ['#E2B93B', '#C49A2A'],
  white: ['#FFFFFF', C.light],
};

// Plastic cup with three compartments, pens standing in it.
const penHolder = ([body]) => tile(
  L(160, 132, 154, 200, C.dark, 7) + L(200, 118, 202, 200, C.mid, 7) + L(240, 138, 246, 200, C.dark, 7) +
  R(130, 180, 140, 140, body, 10) +
  R(176, 192, 5, 126, 'rgba(0,0,0,0.22)', 2) + R(219, 192, 5, 126, 'rgba(0,0,0,0.22)', 2) +
  R(122, 172, 156, 14, C.light, 6) +
  label(142, 256, 116, 32, '3 slots', A, 16),
);

// Desk pad seen in perspective, a stitched writing surface.
const deskPad = () => tile(
  P('M60 304 L92 258 L338 258 L306 304 Z', '#3B4250') +
  P('M78 296 L104 266 L326 266 L302 296 Z', '#EEF1F4') +
  label(150, 270, 104, 22, '60 × 40 cm', A, 13),
);

// Clear A4 holder standing in front of a sheet of paper.
const docHolder = () => tile(
  R(146, 104, 108, 150, '#FFFFFF', 2, OUT) +
  R(132, 150, 136, 172, '#BFD9EA', 8, 'opacity="0.85"') +
  R(132, 150, 136, 12, C.mid, 4) +
  label(152, 228, 96, 32, 'A4', A, 18),
);

// Tape roll seen face-on: a clear ring with a core and a loose tail.
const tapeRoll = () => tile(
  E(200, 236, 84, 84, '#D9E4EC', OUT) +
  E(200, 236, 30, 30, C.tile) +
  label(272, 280, 96, 28, '19 mm', A, 14),
);

// Metal tape dispenser: a round top with the roll window and a cutting blade.
const tapeDispenser = () => tile(
  R(118, 282, 164, 38, C.mid, 6) +
  R(118, 240, 164, 46, C.metal, 22) +
  E(200, 262, 40, 20, C.light) +
  R(262, 252, 16, 20, C.dark, 2) +
  label(136, 288, 120, 24, '19 mm', A, 13),
);

// Cuboid helper: front face plus a top and a side in perspective.
const cuboid = (x, bottom, w, h, d, front, side, top) => {
  const y = bottom - h;
  return P(`M${x} ${y} L${x + d} ${y - d * 0.6} L${x + w + d} ${y - d * 0.6} L${x + w} ${y} Z`, top) +
    P(`M${x + w} ${y} L${x + w + d} ${y - d * 0.6} L${x + w + d} ${bottom - d * 0.6} L${x + w} ${bottom} Z`, side) +
    R(x, y, w, h, front, 3);
};

// Staple boxes share one drawing; the size sets the proportions and the spec label.
const stapleBox = (w, h, d, spec) => {
  const x = 200 - (w + d) / 2;
  return tile(
    cuboid(x, 320, w, h, d, C.body, C.dark, C.mid) +
    label(x + 12, 320 - h / 2 - 13, w - 24, 26, spec, A, 13),
  );
};

// Paper clips: three loose clips over an open tin.
const clip = (x, y, r) =>
  `<g transform="translate(${x} ${y}) rotate(${r})"><path d="M-8 -26 V 18 A8 8 0 0 0 8 18 V -20 A5 5 0 0 0 -2 -20 V 12" fill="none" stroke="${C.mid}" stroke-width="4" stroke-linecap="round"/></g>`;
const paperClips = () => tile(
  R(118, 282, 164, 38, '#D9DDE3', 6) +
  clip(170, 250, 8) + clip(214, 256, -14) + clip(246, 268, 20) +
  label(138, 290, 124, 24, '28 mm', A, 13),
);

// Letter scale: a display on a pillar over a flat platform.
const letterScale = () => tile(
  R(110, 290, 180, 30, C.dark, 6) +
  R(130, 236, 140, 56, C.body, 8) +
  R(130, 262, 140, 5, A, 2) +
  R(186, 214, 28, 24, C.mid, 4) +
  R(158, 184, 84, 34, '#DDE7EE', 4) +
  label(168, 189, 64, 24, '5 kg', A, 14),
);

// Letter tray: three trays stacked, the top one labelled.
const letterTray = () => tile(
  [282, 244, 206].map((y) => R(110, y, 180, 34, C.body, 4) + R(110, y + 26, 180, 8, C.dark, 3)).join('') +
  label(136, 210, 76, 22, 'A4', A, 13),
);

// Desk calculator: solar strip, display and a key grid.
const calculator = () => tile(
  R(118, 262, 164, 58, C.body, 8) +
  R(128, 246, 144, 16, C.dark, 4) +
  R(118, 262, 164, 4, A, 2) +
  label(150, 268, 100, 22, '12-digit', A, 13) +
  [0, 1].map((r) => [0, 1, 2, 3].map((c) => R(136 + c * 33, 298 + r * 10, 26, 7, C.light, 2)).join('')).join(''),
);

// Name plates: three tent cards, the middle one labelled.
const tent = (x) => P(`M${x - 44} 320 L${x - 44} 252 L${x} 206 L${x + 44} 252 L${x + 44} 320 Z`, '#FFFFFF', OUT);
const namePlates = () => tile(
  tent(120) + tent(280) + tent(200) +
  R(96, 284, 48, 6, C.light, 3) + R(256, 284, 48, 6, C.light, 3) +
  label(164, 262, 72, 24, 'A6 ×10', A, 13),
);

// Folded microfibre cloths: a stack of two layers, one labelled.
const cloths = ([face, shade]) => tile(
  R(112, 276, 176, 44, shade, 6) +
  R(120, 258, 176, 44, face, 6) +
  R(120, 258, 8, 44, A, 3) +
  label(146, 266, 112, 26, '40 × 40 cm', A, 13),
);

// One-litre cleaner bottle: short body, neck and cap.
const cleanerBottle = () => tile(
  R(160, 206, 80, 124, '#DDE7EE', 18) +
  R(184, 186, 32, 24, '#DDE7EE', 6) +
  R(184, 166, 32, 20, C.dark, 5) +
  label(162, 250, 76, 30, '1 l', A, 16),
);

// Five-litre canister: wide body with a carry handle.
const canister = () => tile(
  P('M170 190 Q200 150 230 190', 'none', `stroke="${C.dark}" stroke-width="8"`) +
  R(124, 190, 152, 130, '#DDE7EE', 12) +
  R(176, 176, 48, 16, C.dark, 4) +
  label(150, 240, 100, 30, '5 l', A, 18),
);

// Spray bottle: translucent body with a trigger head and nozzle.
const sprayBottle = () => tile(
  R(158, 210, 84, 118, '#BFD9EA', 14, 'opacity="0.85"') +
  R(168, 190, 58, 22, C.dark, 6) +
  R(222, 184, 36, 10, C.dark, 4) +
  label(166, 262, 68, 28, '750 ml', A, 13),
);

// Toilet cleaner: tall narrow bottle with a long neck.
const toiletBottle = () => tile(
  R(170, 200, 60, 130, C.body, 12) +
  R(186, 176, 28, 30, C.body, 4) +
  R(180, 160, 40, 18, C.mid, 4) +
  label(170, 262, 60, 28, '750 ml', A, 13),
);

// Waste bags: a bag with a tied top; size sets the width and height.
const wasteBags = (w, h, spec) => {
  const x = 200 - w / 2, top = 320 - h;
  return tile(
    P(`M${x} ${top + 12} Q200 ${top - 6} ${x + w} ${top + 12} L${x + w + 6} 320 Q200 332 ${x - 6} 320 Z`, '#3E434A') +
    P(`M188 ${top + 2} Q200 ${top - 22} 212 ${top + 2}`, 'none', `stroke="${C.dark}" stroke-width="5"`) +
    label(200 - 60, 320 - h / 2 - 13, 120, 26, spec, A, 13),
  );
};

// Waste bin with a lid. The white model has a light outline.
const wasteBin = ([body, lid]) => tile(
  P('M140 200 L260 200 L250 322 L150 322 Z', body, OUT) +
  R(132, 184, 136, 20, lid, 6) +
  label(164, 240, 72, 26, '15 l', A, 15),
);

// Mop head cover: a flat sleeve with strip ends.
const mopCover = () => tile(
  R(108, 268, 184, 44, C.paper, 10) +
  R(108, 268, 184, 10, C.paperDark, 4) +
  R(108, 300, 184, 8, C.paperDark, 3) +
  label(146, 282, 108, 24, '40 cm', A, 13),
);

// Mop bucket with a wringer on top.
const mopBucket = () => tile(
  P('M136 218 Q200 150 264 218', 'none', `stroke="${C.mid}" stroke-width="8"`) +
  P('M124 222 L276 222 L256 322 L144 322 Z', C.body) +
  R(120, 214, 160, 14, C.light, 6) +
  R(150, 186, 100, 24, C.mid, 4) +
  L(176, 192, 176, 208, C.dark, 4) + L(224, 192, 224, 208, C.dark, 4) +
  R(130, 268, 140, 8, A, 3) +
  label(160, 280, 80, 24, '10 l', A, 14),
);

// Scouring sponges: a stack of yellow sponges with grey scrub pads.
const sponges = () => tile(
  R(96, 284, 96, 26, '#E9C23F', 6) + R(96, 272, 96, 14, '#8A9099', 4) +
  R(122, 276, 156, 44, '#E9C23F', 8) + R(122, 262, 156, 16, '#8A9099', 5) +
  label(150, 280, 100, 24, '5 pcs', A, 13),
);

// Concentrate in a jug with a side handle and a cap.
const jugConcentrate = () => tile(
  P('M262 236 Q292 236 292 268 Q292 300 262 300', 'none', `stroke="${C.mid}" stroke-width="8"`) +
  R(138, 214, 124, 108, C.paper, 18) +
  R(160, 196, 80, 20, C.body, 5) +
  label(156, 250, 88, 30, '2 l', A, 16),
);

// Wall paper towel dispenser: a white box, a slot and a towel out of it.
const towelDispenser = () => tile(
  R(120, 150, 160, 170, '#FFFFFF', 10, OUT) +
  R(120, 150, 160, 8, C.light, 4) +
  R(146, 296, 108, 8, C.dark, 4) +
  R(176, 300, 48, 22, C.paper, 2) +
  R(190, 226, 20, 14, C.mid, 4),
);

// Wall soap dispenser: translucent body, pump head and nozzle.
const soapWall = () => tile(
  R(156, 218, 88, 104, '#BFD9EA', 14, 'opacity="0.85"') +
  R(144, 196, 112, 22, C.dark, 8) +
  R(226, 196, 38, 10, C.dark, 4) +
  R(256, 196, 10, 22, C.dark, 3) +
  label(170, 256, 60, 26, '500 ml', A, 13),
);

// Broom: long handle, collar and a head with bristles.
const broom = () => tile(
  R(194, 40, 12, 250, C.mid, 6) +
  R(188, 270, 24, 18, C.metal, 4) +
  R(140, 286, 120, 26, C.body, 6) +
  R(140, 290, 120, 6, A, 2) +
  [0, 1, 2, 3, 4, 5].map((i) => L(152 + i * 20, 312, 152 + i * 20, 326, C.paperDark, 4)).join('') +
  label(136, 180, 128, 26, '120 cm', A, 14),
);

// Envelopes: C5 landscape with a window, DL long and plain, C4 portrait.
const envC5 = () => tile(
  R(116, 164, 192, 128, '#F2F0EB', 3, OUT) +
  R(104, 176, 192, 128, '#FFFFFF', 3, OUT) +
  P('M104 176 L200 246 L296 176', 'none', OUT) +
  R(120, 262, 72, 30, '#E6F0F7', 3) +
  label(214, 262, 72, 28, 'C5', A, 15),
);
const envDL = () => tile(
  R(100, 220, 200, 100, C.paper, 3, OUT) +
  P('M100 220 L200 282 L300 220', 'none', OUT) +
  label(156, 286, 88, 26, 'DL', A, 15),
);
const envC4 = () => tile(
  R(125, 120, 150, 200, '#FFFFFF', 3, OUT) +
  P('M125 120 L200 190 L275 120', 'none', OUT) +
  label(150, 250, 100, 28, 'C4', A, 16),
);

// Padded mailers: kraft bag with a seam flap; size sets width and height.
const mailer = (w, h, spec) => {
  const top = 320 - h;
  return tile(
    R(200 - w / 2, top, w, h, '#D8BE95', 14) +
    P(`M${200 - w / 2 + 10} ${top + 10} L200 ${top + h / 2} L${200 + w / 2 - 10} ${top + 10}`, 'none', `stroke="${C.paperDark}" stroke-width="3"`) +
    label(144, 320 - h / 2 + 12, 112, 26, spec, A, 13),
  );
};

// Clear packing tape roll standing on its edge.
const packingTape = () => tile(
  R(140, 206, 120, 114, '#CFE3EE', 6, 'opacity="0.9"') +
  E(200, 206, 60, 14, '#A9C8DA') +
  E(200, 320, 60, 14, '#9DBDD0') +
  E(200, 206, 18, 6, C.tile) +
  label(152, 256, 96, 28, '50 mm', A, 14),
);

// Kraft paper roll lying on its side, the end showing the core.
const kraftRoll = () => tile(
  R(104, 232, 186, 84, '#B98B5C', 10) +
  E(290, 274, 16, 42, '#D9B88E') +
  E(290, 274, 6, 14, '#8A6440') +
  label(140, 256, 96, 28, '100 m', A, 14),
);

// Carton: a cuboid with a tape stripe and the size as a label.
const carton = (w, h, d, spec) => {
  const x = 200 - (w + d) / 2, bottom = 320;
  return tile(
    cuboid(x, bottom, w, h, d, '#CDA878', '#A9824F', '#DDBC8E') +
    R(x + w / 2 - 8, bottom - h, 16, h, '#E9D3AE', 2) +
    label(x + 10, bottom - h / 2 - 13, w - 20, 26, spec, A, 12),
  );
};

// Bubble wrap: a sheet with a grid of bubbles and a roll under it.
const bubbleWrap = () => tile(
  R(120, 186, 160, 116, '#E6F0F7', 6, OUT) +
  [0, 1, 2, 3].map((i) => [0, 1, 2].map((j) =>
    `<circle cx="${140 + i * 38}" cy="${206 + j * 34}" r="11" fill="none" stroke="#BFD9EA" stroke-width="3"/>`).join('')).join('') +
  R(100, 302, 192, 22, C.light, 11) +
  label(150, 262, 100, 26, '1 m × 10 m', A, 12),
);

// Label sheets: a grid of label cells on an A4 sheet, cols and rows set the pitch.
const labelSheet = (cols, rows, spec) => {
  const x = 115, y = 70, w = 170, h = 210, pad = 8;
  const cw = (w - pad * 2) / cols, ch = (h - pad * 2) / rows;
  let cells = '';
  for (let i = 0; i < cols; i++) {
    for (let j = 0; j < rows; j++) {
      cells += R(x + pad + i * cw + 3, y + pad + j * ch + 3, cw - 6, ch - 6, '#EEF1F4', 2);
    }
  }
  return tile(
    R(x + 8, y - 8, w, h, '#E3E7EC', 3) +
    R(x, y, w, h, '#FFFFFF', 3, OUT) +
    cells +
    label(130, 292, 140, 26, spec, A, 13),
  );
};

// Full-sheet labels: one cell covers the whole A4 sheet.
const fullSheet = () => tile(
  R(120, 62, 170, 210, '#E3E7EC', 3) +
  R(115, 70, 170, 210, '#FFFFFF', 3, OUT) +
  R(123, 78, 154, 194, '#EEF1F4', 2) +
  R(123, 78, 154, 6, A, 2) +
  label(130, 292, 140, 26, 'A4 · 100', A, 13),
);

const penHolderVariants = {
  'DEMO-OFF-4001': penHolder(COL.grey),
  'DEMO-OFF-4001-BLUE': penHolder(COL.blue),
  'DEMO-OFF-4001-RED': penHolder(COL.red),
  'DEMO-OFF-4001-BLACK': penHolder(COL.black),
  'DEMO-OFF-4001-GREEN': penHolder(COL.green),
};

// Push pins standing up out of a small card box, one accent-coloured head each.
const pushPins = () => tile(
  [[146, 222], [178, 216], [210, 224], [242, 218], [274, 226]].map(([x, top]) =>
    L(x, top + 9, x, 268, C.metal, 4) + E(x, top + 6, 9, 9, A)).join('') +
  R(118, 262, 164, 60, C.paper, 6) + R(118, 262, 164, 10, C.paperDark, 4) +
  label(138, 290, 124, 24, '50 pcs', A, 13),
);

// Letter opener lying flat: a metal blade, a dark handle with an accent band and a hole.
const letterOpener = () => tile(
  P('M206 286 L316 290 Q334 298 336 302 Q334 306 316 312 L206 318 Z', C.metal) +
  R(100, 282, 120, 38, C.dark, 19) + R(156, 282, 12, 38, A, 0) +
  E(124, 301, 7, 7, C.white) +
  label(140, 232, 120, 28, '210 mm', A, 16),
);

export const illustrations = {
  ...penHolderVariants,
  'DEMO-OFF-4002': deskPad(),
  'DEMO-OFF-4003': docHolder(),
  'DEMO-OFF-4004': tapeRoll(),
  'DEMO-OFF-4005': tapeDispenser(),
  'DEMO-OFF-4006': stapleBox(120, 60, 36, '24/6 · 1000'),
  'DEMO-OFF-4007': stapleBox(190, 120, 60, '26/6 · 5000'),
  'DEMO-OFF-4008': stapleBox(150, 80, 30, '23/10 · 1000'),
  'DEMO-OFF-4009': paperClips(),
  'DEMO-OFF-4010': letterScale(),
  'DEMO-OFF-4011': letterTray(),
  'DEMO-OFF-4012': calculator(),
  'DEMO-OFF-4013': namePlates(),
  'DEMO-OFF-4014': pushPins(),
  'DEMO-OFF-4015': letterOpener(),
  'DEMO-OFF-5001': cloths(COL.grey),
  'DEMO-OFF-5001-BLUE': cloths(COL.blue),
  'DEMO-OFF-5001-RED': cloths(COL.red),
  'DEMO-OFF-5001-GREEN': cloths(COL.green),
  'DEMO-OFF-5001-YELLOW': cloths(COL.yellow),
  'DEMO-OFF-5002': cleanerBottle(),
  'DEMO-OFF-5003': canister(),
  'DEMO-OFF-5004': sprayBottle(),
  'DEMO-OFF-5005': toiletBottle(),
  'DEMO-OFF-5006': wasteBags(150, 170, '60 l · 20'),
  'DEMO-OFF-5007': wasteBags(190, 230, '120 l · 10'),
  'DEMO-OFF-5008': wasteBin(COL.white),
  'DEMO-OFF-5008-BLACK': wasteBin(COL.black),
  'DEMO-OFF-5008-GREY': wasteBin(COL.grey),
  'DEMO-OFF-5008-BLUE': wasteBin(COL.blue),
  'DEMO-OFF-5009': mopCover(),
  'DEMO-OFF-5010': mopBucket(),
  'DEMO-OFF-5011': sponges(),
  'DEMO-OFF-5012': jugConcentrate(),
  'DEMO-OFF-5013': towelDispenser(),
  'DEMO-OFF-5014': soapWall(),
  'DEMO-OFF-5015': broom(),
  'DEMO-OFF-6001': envC5(),
  'DEMO-OFF-6002': envDL(),
  'DEMO-OFF-6003': envC4(),
  'DEMO-OFF-6004': mailer(170, 110, 'Size 2'),
  'DEMO-OFF-6005': mailer(240, 170, 'Size 4'),
  'DEMO-OFF-6006': packingTape(),
  'DEMO-OFF-6007': kraftRoll(),
  'DEMO-OFF-6008': carton(120, 80, 36, '200 × 140 × 80'),
  'DEMO-OFF-6009': carton(170, 120, 50, '300 × 200 × 150'),
  'DEMO-OFF-6010': carton(230, 170, 60, '400 × 300 × 200'),
  'DEMO-OFF-6011': bubbleWrap(),
  'DEMO-OFF-6012': labelSheet(2, 7, '105 × 37 mm'),
  'DEMO-OFF-6013': labelSheet(3, 7, '70 × 37 mm'),
  'DEMO-OFF-6014': fullSheet(),
};
