// More office illustrations, keyed by SKU (part a). Same style as office.mjs.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.office;

// Small helpers, copied from office.mjs (not imported).
const R = (x, y, w, h, fill, rx = 4, extra = '') =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" ${extra}/>`;
const P = (d, fill, extra = '') => `<path d="${d}" fill="${fill}" ${extra}/>`;
const E = (cx, cy, rx, ry, fill, extra = '') => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${fill}" ${extra}/>`;
const Ln = (x1, y1, x2, y2, stroke, w = 2) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round"/>`;
const EDGE = `stroke="${C.light}" stroke-width="2"`;

// A ream of copy paper: a top face for the thickness, a front face with a wrap band and spec labels.
const ream = ({ w = 180, t = 20, fill = '#FFFFFF', text, sub }) => {
  const h = 170;
  const x = 200 - w / 2;
  const y = 318 - h - t;
  const fy = y + t;
  return tile(
    P(`M${x} ${fy} L${x + 26} ${y} L${x + w + 26} ${y} L${x + w} ${fy} Z`, '#FBFBFA', EDGE) +
    P(`M${x + w} ${fy} L${x + w + 26} ${y} L${x + w + 26} ${y + h} L${x + w} ${fy + h} Z`, '#E4E7EB', EDGE) +
    R(x, fy, w, h, fill, 4, EDGE) +
    R(x, fy + h - 24, w, 24, A, 0) +
    label(x + 14, fy + 40, w - 28, 44, text, A, 20) +
    label(x + 14, fy + 96, w - 28, 34, sub, A, 16)
  );
};

// Ring binder seen from the front, spine on the left. Lever arch adds a metal lever over the spine.
const binder = ({ cover, spine, w, h, spineW, lever = false, text, sub }) => {
  const x0 = 200 - (spineW + w) / 2;
  const cx = x0 + spineW;
  const y0 = 322 - h;
  return tile(
    R(x0, y0, spineW, h, spine, 6) +
    R(cx, y0, w, h, cover, 8) +
    R(x0 + 6, y0 + 28, spineW - 12, 8, C.light, 3) +
    R(x0 + 6, y0 + h - 36, spineW - 12, 8, C.light, 3) +
    R(cx + 22, y0 + h / 2 - 34, w - 44, 68, '#FFFFFF', 5) +
    R(cx + 22, y0 + h / 2 - 34, 8, 68, A, 3) +
    label(cx + 36, y0 + h / 2 - 22, w - 60, 40, text, A, 20) +
    label(cx + 36, y0 + h / 2 + 22, w - 60, 28, sub, A, 15) +
    (lever
      ? R(x0 - 8, y0 - 16, spineW + 56, 16, C.metal, 6) + R(x0 + 6, y0 - 6, spineW - 12, 10, C.dark, 2)
      : R(x0 - 8, y0 - 12, spineW + 16, 14, C.metal, 6) +
        `<circle cx="${x0 + spineW / 2}" cy="${y0 - 5}" r="4" fill="${C.dark}"/>`)
  );
};

// A folder with a metal clip on the top edge.
const clipFolder = (cover, edge, text) => tile(
  R(108, 132, 184, 196, cover, 6, `stroke="${edge}" stroke-width="2"`) +
  R(108, 132, 184, 12, edge, 6) +
  R(146, 110, 108, 28, C.metal, 8) +
  R(160, 122, 80, 6, C.dark, 3) +
  R(108, 304, 184, 8, A, 0) +
  label(136, 214, 128, 46, text, A, 22)
);

// A document wallet: flap with an elastic band across it.
const wallet = (cover, flap, text) => tile(
  R(120, 140, 160, 182, cover, 6, EDGE) +
  P('M120 140 L200 214 L280 140 Z', flap, EDGE) +
  Ln(120, 262, 280, 262, A, 6) +
  `<circle cx="200" cy="262" r="6" fill="${C.dark}"/>` +
  label(146, 280, 108, 34, text, A, 20)
);

// A clipboard: board, metal clip at the top, a sheet with ruled lines.
const clipboard = (cover, text) => tile(
  R(128, 124, 144, 196, cover, 8) +
  R(146, 146, 108, 150, '#FFFFFF', 3, EDGE) +
  [0, 1, 2, 3].map((i) => Ln(158, 170 + i * 20, 242, 170 + i * 20, C.light, 4)).join('') +
  R(168, 104, 64, 34, C.metal, 8) +
  R(180, 116, 40, 8, C.dark, 3) +
  R(128, 300, 144, 10, A, 0) +
  label(152, 252, 96, 30, text, A, 16)
);

// A ballpoint or highlighter lying at an angle; the tip is at the origin.
const pen = (x, y, angle, body, len = 120, w = 12) =>
  `<g transform="translate(${x} ${y}) rotate(${angle})">` +
  R(0, -w / 2, len, w, body, w / 2) +
  P(`M0 ${-w / 2} L-14 0 L0 ${w / 2} Z`, C.dark) +
  R(len - 22, -w / 2, 22, w, C.dark, w / 2) +
  `</g>`;

// A pencil with an eraser, a ferrule and a wooden tip; the eraser is at the origin.
const pencil = (x, y, angle, body = '#E9C23F') =>
  `<g transform="translate(${x} ${y}) rotate(${angle})">` +
  R(0, -7, 20, 14, '#EE9AB0', 3) +
  R(20, -7, 12, 14, C.metal, 1) +
  R(32, -7, 120, 14, body, 1) +
  P('M152 -7 L172 0 L152 7 Z', '#EBCB9B') +
  P('M166 -2.5 L172 0 L166 2.5 Z', C.dark) +
  `</g>`;

// A tea box: a top face, a front face and a spec label; the tag is a plain card on a string.
const teaBox = (fill, top, text, extra = '') => tile(
  Ln(190, 222, 190, 196, C.mid, 2) +
  R(178, 188, 24, 22, '#FFFFFF', 3, EDGE) +
  P('M124 240 L150 214 L326 214 L300 240 Z', top) +
  R(124, 240, 176, 80, fill, 6) +
  extra +
  label(144, 266, 136, 36, text, A, 18)
);

// A cup seen from the side: a trapezoid with a rim and an accent band.
const cup = (top, bottom, h, text) => {
  const hw = (y) => (bottom + (top - bottom) * ((320 - y) / h)) / 2;
  const y1 = 320 - h * 0.5;
  const y2 = 320 - h * 0.36;
  return tile(
    P(`M${200 - top / 2} ${320 - h} L${200 + top / 2} ${320 - h} L${200 + bottom / 2} 320 L${200 - bottom / 2} 320 Z`, '#FFFFFF', EDGE) +
    E(200, 320 - h, top / 2, 7, '#EDEFF2', EDGE) +
    P(`M${200 - hw(y1)} ${y1} L${200 + hw(y1)} ${y1} L${200 + hw(y2)} ${y2} L${200 - hw(y2)} ${y2} Z`, A) +
    label(160, 320 - h * 0.8, 80, 30, text, A, 16)
  );
};

// A bean inside a jar or on a tile: a dark oval with a crease.
const bean = (x, y, r) =>
  `<g transform="translate(${x} ${y}) rotate(${r})"><ellipse rx="12" ry="8" fill="#5A3E2B"/>` +
  `<path d="M-8 0 Q0 -3 8 0" stroke="#3A271B" stroke-width="2" fill="none"/></g>`;

// A bottle of still water: glass-like body, cap and a neck.
const bottle = (x) =>
  R(x - 24, 176, 48, 146, '#BFD9EA', 12, `opacity="0.85" ${EDGE}`) +
  R(x - 9, 160, 18, 18, '#BFD9EA', 3, `opacity="0.85" ${EDGE}`) +
  R(x - 11, 146, 22, 18, C.dark, 3);

// A cone coffee filter.
const cone = (top, bottomW) => P(`M${200 - top / 2} 160 L${200 + top / 2} 160 L${200 + bottomW / 2} 322 L${200 - bottomW / 2} 322 Z`, '#F6F1E7', EDGE);

const A_BINDER = { cover: '#FFFFFF', spine: C.light, w: 170, h: 230, spineW: 44, lever: true, text: 'A4', sub: '50 mm' };
const BLUE_BINDER = { ...A_BINDER, cover: '#2E5FA8', spine: '#244D8A' };
const BLACK_BINDER = { ...A_BINDER, cover: '#2A2D33', spine: '#1C1F24' };
const GREY_BINDER = { ...A_BINDER, cover: '#8A9099', spine: '#6F7580' };

export const illustrations = {
  // Copy paper: thickness and the sheet count tell the reams apart.
  'DEMO-OFF-1004': ream({ w: 180, t: 20, text: 'A4 · 70 g', sub: '500 sheets' }),
  'DEMO-OFF-1005': ream({ w: 180, t: 26, text: 'A4 · 90 g', sub: '500 sheets' }),
  'DEMO-OFF-1006': ream({ w: 230, t: 22, text: 'A3 · 80 g', sub: '500 sheets' }),
  'DEMO-OFF-1007': ream({ w: 180, t: 20, fill: C.paper, text: 'A4 · 80 g', sub: 'recycled · 500' }),
  'DEMO-OFF-1008': ream({ w: 180, t: 12, text: 'A4 · 100 g', sub: '250 sheets' }),

  // Ring binder A5: narrower and shorter than the A4 lever arch.
  'DEMO-OFF-1009': binder({ cover: C.mid, spine: C.body, w: 120, h: 170, spineW: 26, text: 'A5', sub: '50 mm' }),

  // Lever arch file A4, 50 mm: model white, then blue, black and grey.
  'DEMO-OFF-1010': binder(A_BINDER),
  'DEMO-OFF-1010-BLUE': binder(BLUE_BINDER),
  'DEMO-OFF-1010-BLACK': binder(BLACK_BINDER),
  'DEMO-OFF-1010-GREY': binder(GREY_BINDER),

  // Clip folder A4, plastic: model white, then blue, red, black and green.
  'DEMO-OFF-1011': clipFolder('#FFFFFF', C.light, 'A4'),
  'DEMO-OFF-1011-BLUE': clipFolder('#2E5FA8', '#244D8A', 'A4'),
  'DEMO-OFF-1011-RED': clipFolder('#C2403A', '#A3322D', 'A4'),
  'DEMO-OFF-1011-BLACK': clipFolder('#2A2D33', '#1C1F24', 'A4'),
  'DEMO-OFF-1011-GREEN': clipFolder('#3E8E5A', '#2F6E45', 'A4'),

  // Document wallet A4 with elastic band: cardboard model, then blue, red and black.
  'DEMO-OFF-1012': wallet(C.paper, C.paperDark, 'A4'),
  'DEMO-OFF-1012-BLUE': wallet('#2E5FA8', '#244D8A', 'A4'),
  'DEMO-OFF-1012-RED': wallet('#C2403A', '#A3322D', 'A4'),
  'DEMO-OFF-1012-BLACK': wallet('#2A2D33', '#1C1F24', 'A4'),

  // Clipboard folder A4 with clip: grey model, then blue, red and green.
  'DEMO-OFF-1013': clipboard(C.mid, 'A4'),
  'DEMO-OFF-1013-BLUE': clipboard('#2E5FA8', 'A4'),
  'DEMO-OFF-1013-RED': clipboard('#C2403A', 'A4'),
  'DEMO-OFF-1013-GREEN': clipboard('#3E8E5A', 'A4'),

  // Index dividers: ten tabs across the top edge of one sheet.
  'DEMO-OFF-1014': tile(
    R(122, 128, 156, 190, '#FFFFFF', 4, EDGE) +
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => R(128 + i * 14, 104, 12, 26, [A, C.mid, C.light, C.metal][i % 4], 3)).join('') +
    label(134, 214, 132, 40, '10 tabs', A, 20)
  ),

  // Suspension files: a box with hanging folder tops peeking out.
  'DEMO-OFF-1015': tile(
    [0, 1, 2, 3, 4].map((i) => R(150 + i * 26, 164, 22, 26, '#FBFBFA', 3, EDGE)).join('') +
    P('M112 210 L140 186 L316 186 L288 210 Z', '#E0D4BE') +
    R(112, 210, 176, 110, C.paper, 6, EDGE) +
    label(136, 248, 128, 40, 'A4 · 25 pcs', A, 17)
  ),

  // Document sleeves: a bundle of clear sleeves with a punched top edge.
  'DEMO-OFF-1016': tile(
    [2, 1, 0].map((i) => R(120 + i * 6, 130 + i * 6, 160, 186, '#FFFFFF', 4, `opacity="${0.45 + (2 - i) * 0.15}" ${EDGE}`)).join('') +
    [0, 1, 2].map((i) => `<circle cx="${144 + i * 56}" cy="144" r="4" fill="${C.light}"/>`).join('') +
    R(126, 290, 160, 8, A, 0) +
    label(146, 236, 120, 40, 'A4 · 100', A, 18)
  ),

  // Divider sheets: four cardboard sheets with a tab each, stepped down the stack.
  'DEMO-OFF-1017': tile(
    [0, 1, 2, 3].map((i) => R(118 + i * 4, 128 + i * 10, 164, 170 - i * 4, C.paper, 3, EDGE)).join('') +
    [0, 1, 2, 3].map((i) => R(260 + i * 4, 136 + i * 10, 24, 14, C.paperDark, 2)).join('') +
    label(146, 258, 108, 36, '100 pcs', A, 18)
  ),

  // Pencils HB and 2B: a cup with twelve pencils in it, cup colour and label tell them apart.
  'DEMO-OFF-2005': tile(
    [-78, -66, -54, -42, -30].map((a) => pencil(200, 250, a)).join('') +
    P('M150 240 L250 240 L242 322 L158 322 Z', C.body) +
    label(160, 276, 80, 30, 'HB × 12', A, 16)
  ),
  'DEMO-OFF-2006': tile(
    [-74, -62, -50, -38, -26].map((a) => pencil(200, 250, a)).join('') +
    P('M150 240 L250 240 L242 322 L158 322 Z', C.mid) +
    label(160, 276, 80, 30, '2B × 12', A, 16)
  ),

  // Double-hole sharpener, metal.
  'DEMO-OFF-2007': tile(
    R(118, 230, 164, 90, C.metal, 12) +
    R(128, 222, 144, 16, C.light, 6) +
    `<circle cx="176" cy="254" r="22" fill="${C.dark}"/><circle cx="176" cy="254" r="12" fill="${C.mid}"/>` +
    `<circle cx="224" cy="254" r="22" fill="${C.dark}"/><circle cx="224" cy="254" r="12" fill="${C.mid}"/>` +
    R(118, 300, 164, 10, A, 0)
  ),

  // Gel pens: a long retractable pen with a clip; white model, then coloured bodies.
  'DEMO-OFF-2008': tile(
    `<g transform="translate(110 300) rotate(-32)">` +
    R(0, -10, 210, 20, '#FFFFFF', 10, EDGE) + P('M0 -10 L-30 0 L0 10 Z', C.dark) +
    R(40, -14, 90, 4, C.metal, 2) + R(200, -10, 10, 20, A, 4) +
    `</g>`
  ),
  'DEMO-OFF-2008-BLUE': tile(
    `<g transform="translate(110 300) rotate(-32)">` +
    R(0, -10, 210, 20, '#2E5FA8', 10) + P('M0 -10 L-30 0 L0 10 Z', C.dark) +
    R(40, -14, 90, 4, C.metal, 2) + R(200, -10, 10, 20, A, 4) +
    `</g>`
  ),
  'DEMO-OFF-2008-RED': tile(
    `<g transform="translate(110 300) rotate(-32)">` +
    R(0, -10, 210, 20, '#C2403A', 10) + P('M0 -10 L-30 0 L0 10 Z', C.dark) +
    R(40, -14, 90, 4, C.metal, 2) + R(200, -10, 10, 20, A, 4) +
    `</g>`
  ),
  'DEMO-OFF-2008-BLACK': tile(
    `<g transform="translate(110 300) rotate(-32)">` +
    R(0, -10, 210, 20, '#2A2D33', 10) + P('M0 -10 L-30 0 L0 10 Z', C.dark) +
    R(40, -14, 90, 4, C.metal, 2) + R(200, -10, 10, 20, A, 4) +
    `</g>`
  ),
  'DEMO-OFF-2008-GREEN': tile(
    `<g transform="translate(110 300) rotate(-32)">` +
    R(0, -10, 210, 20, '#3E8E5A', 10) + P('M0 -10 L-30 0 L0 10 Z', C.dark) +
    R(40, -14, 90, 4, C.metal, 2) + R(200, -10, 10, 20, A, 4) +
    `</g>`
  ),

  // Fineliners: ten thin pens lying side by side.
  'DEMO-OFF-2009': tile(
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) =>
      `<g transform="translate(110 ${206 + i * 7}) rotate(-14)">` +
      R(0, -3, 170, 6, '#1F2329', 3) + P('M0 -3 L-14 0 L0 3 Z', '#1F2329') + `</g>`).join('') +
    label(132, 292, 140, 30, '0.4 mm × 10', A, 15)
  ),

  // Felt-tip pens: six thick markers fanned out of one point, twelve colours in the set.
  'DEMO-OFF-2010': tile(
    [['#D0453B', -124], ['#E98A3C', -102], ['#E9C23F', -80], ['#3E8E5A', -58], ['#2E5FA8', -36], ['#8E5BB0', -14]]
      .map(([c, a]) => pen(200, 304, a, c, 130, 22)).join('') +
    label(146, 304, 108, 28, '12 colours', A, 14)
  ),

  // Correction roller: a tape dispenser with the roll in view.
  'DEMO-OFF-2011': tile(
    R(116, 210, 184, 90, C.body, 20) +
    E(160, 252, 38, 38, '#FFFFFF', EDGE) +
    `<circle cx="160" cy="252" r="14" fill="${C.dark}"/>` +
    P('M286 226 L316 226 L316 252 L286 262 Z', '#FFFFFF', EDGE) +
    R(116, 292, 184, 8, A, 0) +
    label(200, 226, 92, 30, '5 mm × 8 m', A, 13)
  ),

  // Two-hole punch: a raised lever and a base.
  'DEMO-OFF-2012': tile(
    R(96, 278, 208, 40, C.dark, 8) +
    R(104, 218, 192, 40, C.body, 14) +
    R(124, 232, 60, 8, C.light, 3) +
    label(150, 226, 100, 26, '25 sheets', A, 14)
  ),

  // Ruler 30 cm: a long plastic strip with ticks.
  'DEMO-OFF-2013': tile(
    R(58, 292, 284, 30, '#EFF6FA', 3, EDGE) +
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
      .map((i) => Ln(58 + i * 9.5, 292, 58 + i * 9.5, 292 + (i % 5 === 0 ? 14 : 8), C.mid, 1.5)).join('') +
    label(150, 294, 92, 24, '30 cm', A, 14)
  ),

  // Office scissors 21 cm: two blades crossing at a pivot, ring handles.
  'DEMO-OFF-2014': tile(
    P('M140 250 L186 196 L298 116 L304 126 L194 206 L150 262 Z', C.metal, EDGE) +
    P('M140 150 L186 204 L298 284 L304 274 L194 194 L150 138 Z', C.metal, EDGE) +
    `<circle cx="118" cy="256" r="22" fill="none" stroke="${C.body}" stroke-width="10"/>` +
    `<circle cx="118" cy="144" r="22" fill="none" stroke="${C.body}" stroke-width="10"/>` +
    `<circle cx="196" cy="200" r="8" fill="${C.dark}"/>` +
    R(184, 170, 14, 60, A, 4)
  ),

  // Glue stick 20 g: white body with an accent cap.
  'DEMO-OFF-2015': tile(
    R(146, 180, 108, 140, '#FFFFFF', 6, EDGE) +
    R(146, 156, 108, 34, A, 6) +
    label(156, 240, 88, 34, '20 g', A, 20)
  ),

  // Notepad A5: a card back with a wire spiral along the top and ruled sheets.
  'DEMO-OFF-2016': tile(
    R(118, 160, 164, 22, C.body, 6) +
    R(122, 176, 156, 140, '#FFFFFF', 3, EDGE) +
    [0, 1, 2, 3, 4].map((i) => Ln(136, 206 + i * 20, 264, 206 + i * 20, C.light, 2)).join('') +
    [0, 1, 2, 3, 4, 5, 6].map((i) => `<circle cx="${132 + i * 22}" cy="171" r="5" fill="none" stroke="${C.metal}" stroke-width="3"/>`).join('') +
    label(148, 284, 104, 28, 'A5 · 100', A, 15)
  ),

  // Notebook A5 with a hard cover, spine, page edge and a bookmark ribbon.
  'DEMO-OFF-2017': tile(
    R(132, 140, 136, 180, C.mid, 8) +
    R(132, 140, 14, 180, C.dark, 6) +
    R(266, 146, 6, 168, '#FFFFFF', 2, EDGE) +
    R(236, 318, 10, 18, A, 2) +
    label(162, 220, 96, 40, 'A5 · 96', A, 16)
  ),

  // Index cards A6: a stack of cards seen from the front.
  'DEMO-OFF-2018': tile(
    [0, 1, 2, 3].map((i) => R(136 + i * 2, 300 - i * 12, 128, 20, '#FBF8F1', 3, EDGE)).join('') +
    R(150, 210, 100, 66, '#FFFFFF', 4, EDGE) +
    [0, 1, 2].map((i) => Ln(160, 230 + i * 14, 240, 230 + i * 14, C.light, 2)).join('') +
    label(158, 240, 84, 24, 'A6 · 100', A, 13)
  ),

  // Rollerball pens: a box with pens standing out of it.
  'DEMO-OFF-2019': tile(
    [-40, -28, -16].map((a, i) => pen(150 + i * 10, 250 + i * 6, a, '#2A2D33', 110, 10)).join('') +
    P('M120 236 L144 214 L304 214 L280 236 Z', '#D9CBB0') +
    R(120, 236, 160, 84, C.paper, 6, EDGE) +
    label(138, 262, 124, 36, 'black × 12', A, 16)
  ),

  // Espresso beans: a glass jar with a dark lid and beans in it.
  'DEMO-OFF-3004': tile(
    R(132, 128, 136, 22, C.dark, 6) +
    R(138, 150, 124, 170, '#BFD9EA', 14, `opacity="0.85" ${EDGE}`) +
    [[156, 296, 20], [186, 302, -10], [218, 298, 30], [244, 292, -20], [170, 270, 10], [204, 276, -30], [236, 268, 14], [196, 250, 0]]
      .map(([x, y, r]) => bean(x, y, r)).join('') +
    label(156, 200, 88, 40, '1 kg', A, 20)
  ),

  // Filter coffee: a flat brick pouch with a sealed top.
  'DEMO-OFF-3005': tile(
    R(124, 176, 152, 150, '#6B4A33', 8) +
    R(124, 176, 152, 16, '#4A3324', 4) +
    Ln(132, 200, 268, 200, '#4A3324', 2) +
    label(150, 226, 100, 40, '500 g', A, 20) +
    R(124, 300, 152, 8, A, 0)
  ),

  // Tea boxes: same box, colour and label tell them apart.
  'DEMO-OFF-3006': teaBox(C.paper, '#D6C8AE', '100 bags'),
  'DEMO-OFF-3007': teaBox('#6FA76B', '#5A9158', '25 bags',
    P('M236 286 Q254 262 274 280 Q256 302 236 286 Z', '#FFFFFF')),
  'DEMO-OFF-3014': teaBox('#D0453B', '#B73A3A', '20 bags', R(124, 262, 176, 8, '#E9C23F', 0)),

  // Sugar: a paper bag with a crimped top and an accent band.
  'DEMO-OFF-3008': tile(
    P('M132 150 L268 150 L282 322 L118 322 Z', '#FFFFFF', EDGE) +
    R(132, 150, 136, 14, C.paperDark, 2) +
    R(118, 226, 164, 8, A, 0) +
    label(148, 250, 104, 40, '1 kg', A, 20)
  ),

  // Paper cups: the 300 ml cup is wider and taller than the 200 ml one.
  'DEMO-OFF-3009': cup(120, 92, 120, '200 ml'),
  'DEMO-OFF-3010': cup(150, 110, 160, '300 ml'),

  // Wooden stirrers: a bundle of stirrers standing out of a paper pack.
  'DEMO-OFF-3011': tile(
    [-2, -1, 0, 1, 2].map((i) => Ln(200 + i * 5, 206, 200 + i * 14, 96, '#C8A27A', 6)).join('') +
    R(150, 200, 100, 120, C.paper, 6, EDGE) +
    label(158, 246, 84, 34, '1000 pcs', A, 14)
  ),

  // Still mineral water: six bottles, three in view, on a shrink tray.
  'DEMO-OFF-3012': tile(
    bottle(150) + bottle(200) + bottle(250) +
    R(122, 300, 156, 22, C.light, 4) +
    label(128, 298, 144, 22, '6 × 1.5 l', A, 14)
  ),

  // Coffee filters, size 4: a cone filter with a light rim.
  'DEMO-OFF-3013': tile(
    cone(128, 84) +
    E(200, 160, 64, 10, '#EDE5D4', EDGE) +
    label(156, 232, 88, 34, 'Size 4', A, 18)
  ),
};
