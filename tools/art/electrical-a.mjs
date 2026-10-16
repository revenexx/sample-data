// More electrical illustrations, keyed by SKU (part a). Same style as electrical.mjs.
// Flat shapes only, neutral product colours, one accent. No brand or certification marks.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.electrical;
const FONT = 'font-family="Helvetica, Arial, sans-serif"';
const HOLES = C.mid;

const T = (x, y, size, txt, weight = 400) =>
  `<text x="${x}" y="${y}" text-anchor="middle" ${FONT} font-size="${size}" font-weight="${weight}" fill="${C.dark}">${txt}</text>`;

// Colour variants: the family name suffix -> face colour.
const COLOURS = [
  ['WHITE', '#FFFFFF'],
  ['BLACK', '#2A2D33'],
  ['ANTHRACITE', '#3E434A'],
  ['ALUMINIUM', '#B8BEC6'],
  ['STAINLESS', '#CFD3D8'],
];

// Insulation colours for cable ends (natural cable colours, no brand scheme).
const CORE = ['#8B5A2B', '#2E5FA8', '#6FA76B', '#E9C23F', '#B8BEC6'];
const CORE_DATA = ['#C47A4A', '#E9C23F', '#6FA76B', '#2E5FA8'];

// ---------- cables ----------

// Core positions on a circle inside the cable end (one core sits in the middle).
const corePos = (n, cx, cy, r) =>
  n === 1
    ? [[cx, cy]]
    : Array.from({ length: n }, (_, i) => [
      cx + r * Math.cos((2 * Math.PI * i) / n - Math.PI / 2),
      cy + r * Math.sin((2 * Math.PI * i) / n - Math.PI / 2),
    ]);

// The cut end of the cable, seen from the front: jacket plus its cores.
const cableEnd = (n, cols) => {
  const x = 340;
  const y = 262;
  if (n === 1) {
    return `<circle cx="${x}" cy="${y}" r="13" fill="#C47A4A"/>`;
  }
  return `<circle cx="${x}" cy="${y}" r="30" fill="${C.dark}"/>` +
    corePos(n, x, y, 13).map(([a, b], i) =>
      `<circle cx="${a.toFixed(1)}" cy="${b.toFixed(1)}" r="6.5" fill="${cols[i % cols.length]}"/>`).join('');
};

// A cable coil on a ring: rx sets the coil size (longer cable, bigger ring).
const coil = ({ rx, layers, spec, length, cores, cols = CORE, flange = false, wire = false }) => {
  const ry = rx * 0.42;
  const cy0 = 206;
  const bottom = cy0 + layers * 7;
  const stack = Array.from({ length: layers }, (_, i) =>
    `<ellipse cx="200" cy="${cy0 + i * 7}" rx="${rx}" ry="${ry}" fill="${C.body}"/>`).join('');
  const fl = flange
    ? `<ellipse cx="200" cy="${bottom + 4}" rx="${rx + 12}" ry="${ry + 9}" fill="${C.dark}"/>`
    : '';
  const lead = wire
    ? `<path d="M${200 + rx - 6} 200 Q ${200 + rx + 26} 206 330 262" fill="none" stroke="#C47A4A" stroke-width="7" stroke-linecap="round"/>`
    : `<path d="M${200 + rx - 6} 196 Q ${200 + rx + 30} 200 330 262" fill="none" stroke="${C.body}" stroke-width="22" stroke-linecap="round"/>`;
  return tile(
    fl +
    `<ellipse cx="200" cy="${bottom}" rx="${rx - 4}" ry="${ry - 4}" fill="${C.dark}"/>` +
    stack +
    `<ellipse cx="200" cy="200" rx="${rx}" ry="${ry}" fill="${C.mid}"/>` +
    `<ellipse cx="200" cy="200" rx="${rx * 0.42}" ry="${ry * 0.42}" fill="${C.dark}"/>` +
    lead + cableEnd(cores, cols) +
    label(150, 118, 100, 34, spec, A, 18) +
    label(150, 292, 100, 28, length, A, 16),
  );
};

// ---------- switches and plates ----------

const plate = (inner, w = 144, h = 168, x = 128, y = 112) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="16" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<circle cx="200" cy="${y + 20}" r="4" fill="${C.light}"/><circle cx="200" cy="${y + h - 20}" r="4" fill="${C.light}"/>` +
  inner;

const rocker = (x, y, w = 48, h = 84) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="${C.body}"/>` +
  `<rect x="${x + w / 2 - 10}" y="${y + 8}" width="20" height="7" rx="3" fill="${A}"/>`;

const sw2005 = () => tile(
  plate(rocker(176, 164)) + label(140, 300, 120, 30, '2-way', A, 18),
);
const sw2006 = () => tile(
  plate(
    `<rect x="172" y="160" width="56" height="44" rx="10" fill="${C.body}"/>` +
    `<rect x="172" y="208" width="56" height="44" rx="10" fill="${C.mid}"/>` +
    `<rect x="186" y="172" width="28" height="7" rx="3" fill="${A}"/>`,
  ) + label(140, 300, 120, 30, 'interm.', A, 18),
);
const doorbell = () => tile(
  `<circle cx="200" cy="200" r="72" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<circle cx="200" cy="200" r="38" fill="${C.body}"/>` +
  `<circle cx="200" cy="200" r="16" fill="${C.mid}"/>` +
  `<circle cx="200" cy="200" r="46" fill="none" stroke="${A}" stroke-width="5"/>` +
  label(140, 300, 120, 30, '24 V', A, 18),
);
const sw2008 = () => tile(
  plate(rocker(146, 164) + rocker(206, 164)) + label(140, 300, 120, 30, 'double', A, 18),
  { },
);
const swSurface = () => tile(
  `<rect x="120" y="116" width="160" height="150" rx="18" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="130" y="126" width="140" height="130" rx="12" fill="none" stroke="${A}" stroke-width="3"/>` +
  rocker(176, 160, 48, 84) + label(140, 300, 120, 30, 'IP44', A, 18),
);
const blind = () => tile(
  plate(
    `<rect x="160" y="132" width="80" height="60" rx="12" fill="${C.body}"/>` +
    `<polygon points="200,144 214,166 186,166" fill="#fff"/>` +
    `<rect x="160" y="206" width="80" height="60" rx="12" fill="${C.body}"/>` +
    `<polygon points="200,256 214,234 186,234" fill="#fff"/>`,
  ),
);
const dimmer = () => tile(
  `<circle cx="200" cy="200" r="78" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<circle cx="200" cy="200" r="52" fill="${C.body}"/>` +
  `<rect x="194" y="150" width="12" height="30" rx="4" fill="${A}"/>` +
  label(140, 300, 120, 30, '400 W', A, 18),
);

// ---------- sockets and cover frames ----------

const socketFace = (face, holes = HOLES) =>
  `<rect x="126" y="110" width="148" height="148" rx="18" fill="${face}" stroke="${C.light}" stroke-width="2"/>` +
  `<circle cx="176" cy="184" r="10" fill="${holes}"/><circle cx="224" cy="184" r="10" fill="${holes}"/>` +
  `<circle cx="200" cy="222" r="12" fill="${holes}"/>` +
  `<rect x="182" y="244" width="36" height="6" rx="3" fill="${A}"/>`;

const socketSurface = (face) =>
  `<rect x="112" y="232" width="176" height="26" rx="8" fill="${C.light}"/>` +
  `<rect x="118" y="100" width="164" height="140" rx="18" fill="${face}" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="130" y="112" width="140" height="116" rx="12" fill="none" stroke="${A}" stroke-width="3"/>` +
  `<circle cx="176" cy="172" r="10" fill="${HOLES}"/><circle cx="224" cy="172" r="10" fill="${HOLES}"/>` +
  `<circle cx="200" cy="210" r="12" fill="${HOLES}"/>`;

const socketDouble = (face) =>
  `<rect x="96" y="110" width="208" height="148" rx="18" fill="${face}" stroke="${C.light}" stroke-width="2"/>` +
  [152, 248].map((cx) =>
    `<circle cx="${cx - 20}" cy="184" r="9" fill="${HOLES}"/><circle cx="${cx + 20}" cy="184" r="9" fill="${HOLES}"/>` +
    `<circle cx="${cx}" cy="222" r="11" fill="${HOLES}"/>` +
    `<rect x="${cx - 16}" y="244" width="32" height="6" rx="3" fill="${A}"/>`).join('');

const socketUsb = (face) =>
  socketFace(face) +
  `<rect x="160" y="128" width="30" height="18" rx="4" fill="${HOLES}"/>` +
  `<rect x="210" y="128" width="30" height="18" rx="4" fill="${HOLES}"/>`;

const powerStrip = (face) =>
  `<rect x="60" y="262" width="290" height="44" rx="12" fill="${face}" stroke="${C.light}" stroke-width="2"/>` +
  [110, 170, 230, 290].map((cx) =>
    `<rect x="${cx - 18}" y="270" width="36" height="28" rx="5" fill="${C.light}"/>` +
    `<circle cx="${cx - 7}" cy="284" r="3" fill="${C.dark}"/><circle cx="${cx + 7}" cy="284" r="3" fill="${C.dark}"/>`).join('') +
  `<rect x="72" y="272" width="18" height="24" rx="4" fill="${A}"/>` +
  `<path d="M350 284 Q 380 284 380 322" fill="none" stroke="${C.dark}" stroke-width="7" stroke-linecap="round"/>` +
  label(110, 196, 100, 28, '4-way', A, 16);

const coverFrame1 = (face) => tile(
  `<rect x="140" y="112" width="120" height="150" rx="18" fill="${face}" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="160" y="140" width="80" height="94" rx="10" fill="${C.light}"/>` +
  `<circle cx="200" cy="127" r="4" fill="${C.light}"/><circle cx="200" cy="247" r="4" fill="${C.light}"/>` +
  `<rect x="222" y="252" width="26" height="6" rx="3" fill="${A}"/>`,
);
const coverFrame3 = () => tile(
  `<rect x="80" y="122" width="240" height="150" rx="18" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  [104, 170, 236].map((x) => `<rect x="${x}" y="150" width="60" height="94" rx="10" fill="${C.light}"/>`).join('') +
  `<rect x="262" y="252" width="30" height="6" rx="3" fill="${A}"/>`,
);

// ---------- lighting ----------

const panel = (w, h, x, y, text) => tile(
  `<rect x="${x - 10}" y="${y - 10}" width="${w + 20}" height="${h + 20}" rx="12" fill="${C.light}"/>` +
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff" stroke="${C.mid}" stroke-width="2"/>` +
  `<rect x="${x + 12}" y="${y + 12}" width="${w - 24}" height="${h - 24}" rx="4" fill="none" stroke="${C.light}" stroke-width="3"/>` +
  label(150, 300, 100, 28, text, A, 16),
);

const tube = (w, text) => tile(
  `<rect x="${200 - w / 2}" y="184" width="${w}" height="32" rx="16" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="${200 - w / 2 - 12}" y="180" width="14" height="40" rx="4" fill="${C.body}"/>` +
  `<rect x="${200 + w / 2 - 2}" y="180" width="14" height="40" rx="4" fill="${C.body}"/>` +
  `<rect x="${200 - 40}" y="196" width="80" height="8" rx="4" fill="${A}" opacity="0.35"/>` +
  label(150, 262, 100, 28, text, A, 16),
);

const downlight = (face) => tile(
  `<ellipse cx="200" cy="216" rx="104" ry="58" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="206" rx="104" ry="58" fill="${face}" stroke="${C.light}" stroke-width="3"/>` +
  `<ellipse cx="200" cy="206" rx="70" ry="38" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="206" rx="70" ry="38" fill="none" stroke="${A}" stroke-width="4"/>` +
  label(150, 300, 100, 28, '8 W', A, 16),
);

const wallLamp = (face) => tile(
  `<rect x="104" y="90" width="26" height="210" rx="4" fill="${C.light}"/>` +
  `<rect x="130" y="180" width="184" height="44" rx="22" fill="${face}" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="150" y="214" width="144" height="5" rx="2" fill="${A}"/>` +
  label(150, 262, 100, 28, '12 W', A, 16),
);

const pendant = () => tile(
  `<rect x="197" y="40" width="6" height="110" fill="${C.dark}"/>` +
  `<ellipse cx="200" cy="150" rx="46" ry="14" fill="${C.dark}"/>` +
  `<path d="M108 178 Q 200 112 292 178 L 262 300 Q 200 318 138 300 Z" fill="${C.body}"/>` +
  `<ellipse cx="200" cy="300" rx="62" ry="13" fill="${C.dark}"/>` +
  `<rect x="186" y="178" width="28" height="7" rx="3" fill="${A}"/>`,
);

const ceilingDisc = () => tile(
  `<ellipse cx="200" cy="262" rx="130" ry="44" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="250" rx="130" ry="44" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<ellipse cx="200" cy="250" rx="82" ry="26" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="250" rx="82" ry="26" fill="none" stroke="${A}" stroke-width="4"/>` +
  label(150, 98, 100, 28, 'Ø 30 cm', A, 16),
);

const motion = () => tile(
  `<ellipse cx="200" cy="300" rx="112" ry="22" fill="${C.light}"/>` +
  `<path d="M122 300 Q 122 176 200 176 Q 278 176 278 300 Z" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  [[180, 224], [200, 212], [220, 224], [170, 252], [230, 252]].map(([x, y]) =>
    `<circle cx="${x}" cy="${y}" r="7" fill="${C.body}"/>`).join('') +
  `<rect x="186" y="284" width="28" height="6" rx="3" fill="${A}"/>`,
);

const presence = () => tile(
  `<ellipse cx="200" cy="300" rx="112" ry="22" fill="${C.light}"/>` +
  `<rect x="112" y="184" width="176" height="116" rx="58" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<circle cx="200" cy="242" r="26" fill="${C.body}"/>` +
  `<circle cx="200" cy="242" r="9" fill="${A}"/>` +
  [[150, 214], [250, 214], [150, 270], [250, 270]].map(([x, y]) =>
    `<circle cx="${x}" cy="${y}" r="4" fill="${C.mid}"/>`).join(''),
);

// An E27 LED lamp: a bulb of size r on an E27 screw base.
const bulb = (r, text) => tile(
  `<circle cx="200" cy="${200 - r * 0.2}" r="${r}" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  `<rect x="${200 - r * 0.46}" y="${200 + r * 0.72}" width="${r * 0.92}" height="22" rx="4" fill="${C.metal}"/>` +
  `<rect x="${200 - r * 0.5}" y="${200 + r * 0.72 + 22}" width="${r}" height="${r * 0.9}" rx="6" fill="${C.metal}"/>` +
  `<line x1="${200 - r * 0.5}" y1="${200 + r * 0.72 + 40}" x2="${200 + r * 0.5}" y2="${200 + r * 0.72 + 40}" stroke="${C.mid}" stroke-width="3"/>` +
  `<line x1="${200 - r * 0.5}" y1="${200 + r * 0.72 + 58}" x2="${200 + r * 0.5}" y2="${200 + r * 0.72 + 58}" stroke="${C.mid}" stroke-width="3"/>` +
  label(150, 300, 100, 28, text, A, 16),
);

const strip = () => tile(
  `<circle cx="150" cy="250" r="62" fill="${C.body}"/>` +
  `<circle cx="150" cy="250" r="30" fill="${C.light}"/>` +
  `<circle cx="150" cy="250" r="48" fill="none" stroke="${A}" stroke-width="6" stroke-dasharray="14 8"/>` +
  `<path d="M206 300 Q 260 330 340 300 T 382 262" fill="none" stroke="${A}" stroke-width="7" stroke-linecap="round"/>` +
  label(120, 120, 130, 30, '5 m · 24 V', A, 15),
);

const mirror = () => tile(
  `<rect x="120" y="196" width="160" height="128" rx="10" fill="${C.light}" stroke="${C.mid}" stroke-width="3"/>` +
  `<rect x="136" y="212" width="128" height="96" rx="6" fill="#fff"/>` +
  `<rect x="90" y="150" width="220" height="34" rx="17" fill="#fff" stroke="${C.light}" stroke-width="3"/>` +
  [140, 200, 260].map((x) => `<circle cx="${x}" cy="167" r="6" fill="${A}"/>`).join('') +
  label(150, 98, 100, 28, '14 W', A, 16),
);

// ---------- assemble ----------

const out = {};

// Cables
out['DEMO-ELE-1004'] = coil({ rx: 92, layers: 5, spec: '3 × 2.5', length: '100 m', cores: 3 });
out['DEMO-ELE-1005'] = coil({ rx: 74, layers: 3, spec: '3 × 1.5', length: '50 m', cores: 3 });
out['DEMO-ELE-1006'] = coil({ rx: 92, layers: 5, spec: '5 × 1.5', length: '100 m', cores: 5 });
out['DEMO-ELE-1007'] = coil({ rx: 74, layers: 3, spec: '5 × 4', length: '50 m', cores: 5 });
out['DEMO-ELE-1008'] = coil({ rx: 74, layers: 3, spec: '3 × 4', length: '50 m', cores: 3 });
out['DEMO-ELE-1009'] = coil({ rx: 92, layers: 2, spec: '1 × 2.5', length: '100 m', cores: 1, wire: true });
out['DEMO-ELE-1010'] = coil({ rx: 92, layers: 2, spec: '1 × 4', length: '100 m', cores: 1, wire: true });
out['DEMO-ELE-1011'] = coil({ rx: 60, layers: 3, spec: '3 × 1.5', length: '25 m', cores: 3, flange: true });
out['DEMO-ELE-1012'] = coil({ rx: 92, layers: 4, spec: '4 × 2 × 0.5', length: '100 m', cores: 4, cols: CORE_DATA });

// Switches and plates
out['DEMO-ELE-2005'] = sw2005();
out['DEMO-ELE-2006'] = sw2006();
out['DEMO-ELE-2007'] = doorbell();
out['DEMO-ELE-2008'] = sw2008();

// Cover frames
out['DEMO-ELE-2009'] = coverFrame1('#FFFFFF');
for (const [name, hex] of COLOURS) out[`DEMO-ELE-2009-${name}`] = coverFrame1(hex);
out['DEMO-ELE-2010'] = coverFrame3();

// Sockets and strips: model plus colour variants
const withVariants = (key, draw) => {
  out[key] = draw('#FFFFFF');
  for (const [name, hex] of COLOURS.slice(0, 3)) out[`${key}-${name}`] = draw(hex);
};
withVariants('DEMO-ELE-2011', (f) => tile(socketSurface(f), { }));
withVariants('DEMO-ELE-2012', (f) => tile(socketDouble(f)));
withVariants('DEMO-ELE-2013', (f) => tile(socketUsb(f)));
withVariants('DEMO-ELE-2014', (f) => tile(powerStrip(f)));

// Other switches
out['DEMO-ELE-2015'] = dimmer();
out['DEMO-ELE-2017'] = swSurface();
out['DEMO-ELE-2018'] = blind();

// LED panels and tubes
out['DEMO-ELE-3004'] = panel(176, 176, 112, 112, '4000 K');
out['DEMO-ELE-3005'] = panel(176, 176, 112, 112, '3000 K');
out['DEMO-ELE-3006'] = panel(280, 96, 60, 172, '36 W');
out['DEMO-ELE-3007'] = tube(150, '600 mm');
out['DEMO-ELE-3008'] = tube(290, '1200 mm');

// Downlights, wall, pendant, ceiling
out['DEMO-ELE-3009'] = downlight('#FFFFFF');
for (const [name, hex] of COLOURS.slice(0, 3)) out[`DEMO-ELE-3009-${name}`] = downlight(hex);
out['DEMO-ELE-3010'] = wallLamp('#FFFFFF');
for (const [name, hex] of COLOURS.slice(0, 3)) out[`DEMO-ELE-3010-${name}`] = wallLamp(hex);
out['DEMO-ELE-3011'] = pendant();
out['DEMO-ELE-3012'] = ceilingDisc();

// Sensors
out['DEMO-ELE-3013'] = motion();
out['DEMO-ELE-3014'] = presence();

// E27 lamps
out['DEMO-ELE-3015'] = bulb(40, '6 W');
out['DEMO-ELE-3016'] = bulb(48, '9 W');
out['DEMO-ELE-3017'] = bulb(56, '13 W');

// Strip and mirror light
out['DEMO-ELE-3018'] = strip();
out['DEMO-ELE-3019'] = mirror();

export const illustrations = out;
