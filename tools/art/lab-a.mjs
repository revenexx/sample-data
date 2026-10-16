// More lab illustrations, keyed by SKU (part a). Same style as lab.mjs.
import { C, ACCENT, tile, label } from './style.mjs';

const A = ACCENT.lab;
const FONT = 'font-family="Helvetica, Arial, sans-serif"';
const WHITE = '#FFFFFF';
const GLASS = '#BFD9EA';

// Corner badge for a volume range such as "0.1–2 µl": wider than the shared badge.
const badgeTag = (text) => {
  const w = Math.max(118, text.length * 13 + 40);
  return `<g><rect x="${376 - w}" y="24" width="${w}" height="40" rx="20" fill="${A}"/>` +
    `<text x="${376 - w / 2}" y="51" text-anchor="middle" ${FONT} font-size="21" font-weight="700" fill="#fff">${text}</text></g>`;
};
const badged = (make, text) => make().replace('</svg>', badgeTag(text) + '</svg>');

const tag = (x, y, w, text, size = 20) => label(x, y, w, 30, text, A, size);

// A grid of small ellipses (wells, holes), centred on (cx, cy).
const grid = (cols, rows, cx, cy, dx, dy, rx, ry, fill) => {
  let s = '';
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      s += `<ellipse cx="${cx + (c - (cols - 1) / 2) * dx}" cy="${cy + (r - (rows - 1) / 2) * dy}" rx="${rx}" ry="${ry}" fill="${fill}"/>`;
    }
  }
  return s;
};

// ---------- Equipment (1005–1018) ----------

const heatingBlock = (text, shaking) => {
  const shake = shaking
    ? [246, 258, 270].map((y) =>
        `<line x1="58" y1="${y}" x2="76" y2="${y}" stroke="${C.mid}" stroke-width="4" stroke-linecap="round"/>` +
        `<line x1="324" y1="${y}" x2="342" y2="${y}" stroke="${C.mid}" stroke-width="4" stroke-linecap="round"/>`).join('')
    : '';
  return tile(
    shake +
    `<rect x="92" y="236" width="216" height="34" rx="6" fill="${C.light}"/>` +
    grid(8, 3, 200, 253, 24, 9, 7, 3.5, C.dark) +
    `<rect x="92" y="270" width="216" height="56" rx="6" fill="${C.body}"/>` +
    `<rect x="92" y="318" width="216" height="4" fill="${A}"/>` +
    tag(118, 278, 164, text, 20),
  );
};

const magneticStirrer = () => tile(
  `<rect x="80" y="268" width="240" height="24" rx="6" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="280" rx="48" ry="8" fill="${C.dark}"/>` +
  `<rect x="186" y="277" width="28" height="6" rx="3" fill="${C.mid}"/>` +
  `<rect x="80" y="292" width="240" height="34" rx="6" fill="${C.body}"/>` +
  `<circle cx="112" cy="309" r="8" fill="${C.dark}"/>` +
  `<circle cx="146" cy="309" r="8" fill="${A}"/>` +
  tag(176, 296, 120, '340 °C', 18),
);

// Overhead stirrer: stand rod on a base plate, a clamp holding the motor head
// over a beaker, and the stirring shaft running down into the beaker.
const overheadStirrer = () => tile(
  `<rect x="70" y="318" width="220" height="12" rx="4" fill="${C.dark}"/>` +
  `<rect x="88" y="60" width="12" height="258" fill="${C.dark}"/>` +
  `<rect x="80" y="104" width="28" height="26" rx="4" fill="${C.mid}"/>` +
  `<rect x="104" y="112" width="52" height="11" rx="4" fill="${C.body}"/>` +
  `<rect x="150" y="96" width="82" height="54" rx="16" fill="${C.body}"/>` +
  `<rect x="150" y="136" width="82" height="14" rx="6" fill="${A}"/>` +
  `<rect x="186" y="150" width="8" height="106" fill="${C.metal}"/>` +
  `<rect x="168" y="250" width="44" height="6" rx="3" fill="${C.mid}"/>` +
  `<path d="M140 206 L140 306 Q140 318 152 318 L248 318 Q260 318 260 306 L260 206 Z" fill="${GLASS}" fill-opacity="0.85" stroke="${C.light}" stroke-width="2"/>` +
  `<path d="M143 262 L143 306 Q143 315 152 315 L248 315 Q257 315 257 306 L257 262 Z" fill="${GLASS}" fill-opacity="0.5"/>` +
  `<rect x="140" y="200" width="120" height="6" rx="3" fill="${C.light}"/>` +
  tag(268, 150, 116, '2000 rpm', 17),
);

const precisionBalance = () => tile(
  `<rect x="150" y="236" width="100" height="12" rx="3" fill="${C.light}"/>` +
  `<rect x="192" y="246" width="16" height="16" fill="${C.mid}"/>` +
  `<rect x="80" y="262" width="240" height="64" rx="10" fill="${C.body}"/>` +
  `<rect x="80" y="262" width="240" height="5" fill="${A}"/>` +
  `<rect x="236" y="290" width="64" height="24" rx="3" fill="${C.dark}"/>` +
  tag(104, 288, 118, '3200 g', 18),
);

const analyticalBalance = () => tile(
  `<rect x="140" y="118" width="120" height="14" rx="4" fill="${C.dark}"/>` +
  `<rect x="146" y="130" width="108" height="150" rx="6" fill="${GLASS}" opacity="0.85" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="168" y="258" width="64" height="8" fill="${C.mid}"/>` +
  `<rect x="194" y="266" width="12" height="14" fill="${C.dark}"/>` +
  `<rect x="94" y="280" width="212" height="46" rx="8" fill="${C.body}"/>` +
  `<circle cx="276" cy="303" r="7" fill="${A}"/>` +
  tag(110, 290, 116, '220 g', 18),
);

const labBalance = () => tile(
  `<ellipse cx="200" cy="256" rx="72" ry="12" fill="${C.light}"/>` +
  `<rect x="192" y="262" width="16" height="12" fill="${C.mid}"/>` +
  `<rect x="110" y="272" width="180" height="54" rx="10" fill="${C.body}"/>` +
  tag(150, 286, 100, '500 g', 17),
);

const phMeter = () => tile(
  `<rect x="226" y="100" width="48" height="12" rx="4" fill="${C.dark}"/>` +
  `<rect x="244" y="112" width="12" height="120" rx="6" fill="${C.mid}"/>` +
  `<rect x="240" y="228" width="20" height="98" rx="8" fill="${GLASS}" opacity="0.85" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="240" y="312" width="20" height="6" fill="${A}"/>` +
  `<rect x="100" y="268" width="160" height="58" rx="8" fill="${C.body}"/>` +
  `<rect x="116" y="280" width="60" height="34" rx="4" fill="${C.dark}"/>` +
  `<text x="146" y="304" text-anchor="middle" ${FONT} font-size="20" font-weight="700" fill="#fff">pH</text>`,
);

const diaphragmPump = () => tile(
  `<rect x="96" y="304" width="208" height="18" rx="6" fill="${C.dark}"/>` +
  `<path d="M296 257 C340 257 340 300 310 300" fill="none" stroke="${C.dark}" stroke-width="8" stroke-linecap="round"/>` +
  `<rect x="138" y="170" width="100" height="60" rx="22" fill="${C.dark}"/>` +
  `<rect x="120" y="230" width="150" height="74" rx="14" fill="${C.body}"/>` +
  `<rect x="270" y="250" width="26" height="14" rx="4" fill="${C.mid}"/>` +
  `<rect x="130" y="284" width="40" height="6" rx="3" fill="${A}"/>`,
);

const ultrasonicBath = () => tile(
  `<rect x="76" y="196" width="248" height="124" rx="8" fill="${C.metal}"/>` +
  `<rect x="88" y="208" width="224" height="104" rx="4" fill="${GLASS}" opacity="0.85"/>` +
  `<ellipse cx="200" cy="208" rx="112" ry="6" fill="${WHITE}" opacity="0.5"/>` +
  `<circle cx="270" cy="281" r="7" fill="${A}"/>` +
  tag(112, 268, 112, '5 l', 20),
);

const dryingOven = () => tile(
  `<rect x="110" y="60" width="180" height="266" rx="14" fill="${C.body}"/>` +
  `<rect x="130" y="72" width="140" height="12" rx="4" fill="${C.dark}"/>` +
  `<rect x="130" y="100" width="140" height="156" rx="8" fill="${GLASS}" opacity="0.85" stroke="${C.dark}" stroke-width="3"/>` +
  tag(150, 266, 100, '53 l', 20) +
  `<rect x="140" y="306" width="120" height="8" rx="4" fill="${C.metal}"/>`,
);

const orbitalShaker = () => tile(
  `<ellipse cx="200" cy="282" rx="124" ry="20" fill="${C.light}"/>` +
  `<ellipse cx="200" cy="282" rx="78" ry="12" fill="none" stroke="${C.mid}" stroke-width="3"/>` +
  `<path d="M58 246 Q42 266 58 286" fill="none" stroke="${C.mid}" stroke-width="4" stroke-linecap="round"/>` +
  `<path d="M342 246 Q358 266 342 286" fill="none" stroke="${C.mid}" stroke-width="4" stroke-linecap="round"/>` +
  `<rect x="86" y="286" width="228" height="36" rx="8" fill="${C.body}"/>` +
  tag(150, 296, 100, '300 rpm', 18),
);

const penetrationThermometer = () => tile(
  `<rect x="190" y="50" width="20" height="170" rx="10" fill="${C.metal}"/>` +
  `<rect x="166" y="216" width="68" height="104" rx="14" fill="${C.body}"/>` +
  `<rect x="180" y="230" width="40" height="24" rx="3" fill="${C.dark}"/>` +
  tag(158, 264, 84, '300 °C', 16),
);

const miniCentrifuge = () => tile(
  `<rect x="186" y="204" width="28" height="14" rx="6" fill="${C.dark}"/>` +
  `<path d="M122 262 A78 46 0 0 1 278 262 Z" fill="${C.light}"/>` +
  `<rect x="110" y="260" width="180" height="60" rx="20" fill="${C.body}"/>` +
  `<rect x="110" y="262" width="180" height="6" fill="${A}"/>` +
  tag(128, 284, 144, '6 × 2.0 ml', 16),
);

// ---------- Pipettes (2003–2006) and their volume variants ----------

const pipetteSingle = () => tile(
  `<rect x="186" y="58" width="28" height="24" rx="8" fill="${C.dark}"/>` +
  `<rect x="192" y="80" width="16" height="30" fill="${C.mid}"/>` +
  `<rect x="174" y="108" width="52" height="150" rx="14" fill="${C.body}"/>` +
  `<rect x="174" y="140" width="52" height="8" fill="${A}"/>` +
  `<rect x="170" y="200" width="60" height="12" rx="4" fill="${C.dark}"/>` +
  `<rect x="186" y="258" width="28" height="26" fill="${C.mid}"/>` +
  `<path d="M186 284 L214 284 L204 326 L196 326 Z" fill="${C.light}"/>`,
);

const pipetteEight = () => {
  let tips = '';
  for (let i = 0; i < 8; i++) {
    const x = 158 + i * 12;
    tips += `<path d="M${x - 4} 274 L${x + 4} 274 L${x + 1} 322 L${x - 1} 322 Z" fill="${C.light}"/>`;
  }
  return tile(
    `<rect x="170" y="40" width="60" height="38" rx="10" fill="${C.dark}"/>` +
    `<rect x="150" y="76" width="100" height="124" rx="16" fill="${C.body}"/>` +
    `<rect x="150" y="130" width="100" height="8" fill="${A}"/>` +
    `<rect x="178" y="200" width="44" height="62" fill="${C.mid}"/>` +
    `<rect x="144" y="262" width="112" height="12" rx="4" fill="${C.dark}"/>` +
    tips,
  );
};

const pipetteDispensing = () => tile(
  `<rect x="164" y="60" width="72" height="26" rx="8" fill="${C.dark}"/>` +
  `<rect x="180" y="86" width="40" height="206" rx="6" fill="${GLASS}" opacity="0.85" stroke="${C.mid}" stroke-width="3"/>` +
  `<rect x="180" y="110" width="40" height="10" fill="${A}"/>` +
  [140, 160, 180, 200].map((y) => `<line x1="180" y1="${y}" x2="192" y2="${y}" stroke="${C.mid}" stroke-width="2"/>`).join('') +
  `<rect x="168" y="288" width="64" height="10" rx="3" fill="${C.dark}"/>` +
  `<rect x="192" y="298" width="16" height="24" fill="${C.mid}"/>`,
);

const pipetteDigital = () => tile(
  `<rect x="176" y="70" width="48" height="44" rx="12" fill="${C.dark}"/>` +
  `<rect x="168" y="110" width="64" height="130" rx="16" fill="${C.body}"/>` +
  `<rect x="180" y="134" width="40" height="28" rx="4" fill="#CFD3D8"/>` +
  `<line x1="186" y1="144" x2="214" y2="144" stroke="${C.dark}" stroke-width="2"/>` +
  `<line x1="186" y1="152" x2="206" y2="152" stroke="${C.dark}" stroke-width="2"/>` +
  `<circle cx="200" cy="190" r="7" fill="${A}"/>` +
  `<rect x="186" y="240" width="28" height="22" fill="${C.mid}"/>` +
  `<path d="M186 262 L214 262 L204 326 L196 326 Z" fill="${C.light}"/>`,
);

// ---------- Tips, stands and bags (2007–2013) ----------

const cone = (x, y, h, fill) =>
  `<path d="M${x - 6} ${y} L${x + 6} ${y} L${x + 2} ${y + h} L${x - 2} ${y + h} Z" fill="${fill}"/>`;

const tipRack = ({ front, back, h, plate = C.dark, filter = false, sterile = false, text }) => {
  let s = '';
  for (let i = 0; i < 10; i++) s += cone(200 + (i - 5) * 18 + 9, 244, h, back);
  for (let i = 0; i < 11; i++) {
    const x = 200 + (i - 5) * 18;
    s += cone(x, 244, h, front);
    if (filter) s += `<rect x="${x - 5}" y="244" width="10" height="9" fill="${C.dark}"/>`;
  }
  s += `<rect x="92" y="226" width="216" height="18" rx="4" fill="${plate}"/>`;
  if (sterile) {
    s += `<rect x="84" y="222" width="232" height="106" rx="8" fill="${WHITE}" opacity="0.35" stroke="${C.light}" stroke-width="2"/>`;
  }
  return tile(s + tag(120, 290, 160, text, 18));
};

const tipBag = () => {
  let tips = '';
  for (let i = 0; i < 5; i++) tips += cone(150 + i * 25, 196, 60, GLASS);
  return tile(
    tips +
    `<path d="M110 322 Q102 258 126 246 L274 246 Q298 258 290 322 Q200 332 110 322 Z" fill="${C.light}"/>` +
    `<rect x="126" y="240" width="148" height="12" rx="5" fill="${A}"/>` +
    tag(150, 272, 100, '200 µl', 18),
  );
};

const pipetteStand = () => {
  let shafts = '';
  for (let i = 0; i < 6; i++) {
    const x = 110 + i * 36;
    shafts += `<rect x="${x - 9}" y="176" width="18" height="124" rx="8" fill="${C.light}"/>` +
      `<rect x="${x - 7}" y="168" width="14" height="10" rx="3" fill="${C.body}"/>`;
  }
  return tile(
    shafts +
    `<rect x="84" y="296" width="232" height="30" rx="8" fill="${C.dark}"/>` +
    tag(124, 300, 152, '6 pipettes', 18),
  );
};

// ---------- Tubes, plates, boats, paper and caps (3005–3018) ----------

// Tube with a conical bottom; yb is the bottom tip, x the centre line.
const tube = (x, yb, w, h, body, cap) =>
  `<rect x="${x - w / 2}" y="${yb - h}" width="${w}" height="${h - w / 2}" rx="3" fill="${body}" stroke="${C.light}" stroke-width="2"/>` +
  `<path d="M${x - w / 2} ${yb - w / 2} L${x - w * 0.12} ${yb} L${x + w * 0.12} ${yb} L${x + w / 2} ${yb - w / 2} Z" fill="${body}" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="${x - w / 2 - 2}" y="${yb - h - 8}" width="${w + 4}" height="14" rx="4" fill="${cap}"/>`;

// Tube with a round bottom.
const roundTube = (x, yb, w, h, body, cap) =>
  `<path d="M${x - w / 2} ${yb - h} L${x - w / 2} ${yb - w / 2} A${w / 2} ${w / 2} 0 0 0 ${x + w / 2} ${yb - w / 2} L${x + w / 2} ${yb - h} Z" fill="${body}" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="${x - w / 2 - 2}" y="${yb - h - 8}" width="${w + 4}" height="14" rx="4" fill="${cap}"/>`;

// Sealed pouch with a top seal; n caps poke out of the top edge.
const pouch = (x, y, w, h, n, capFill) => {
  let s = `<path d="M${x} ${y + 8} Q${x} ${y} ${x + 12} ${y} L${x + w - 12} ${y} Q${x + w} ${y} ${x + w} ${y + 8} L${x + w} ${y + h - 14} Q${x + w} ${y + h} ${x + w - 14} ${y + h} L${x + 14} ${y + h} Q${x} ${y + h} ${x} ${y + h - 14} Z" fill="${C.paper}"/>`;
  s += `<rect x="${x}" y="${y}" width="${w}" height="10" rx="4" fill="${C.paperDark}"/>`;
  for (let i = 0; i < n; i++) {
    const cx = x + (w * (i + 1)) / (n + 1);
    s += `<rect x="${cx - 7}" y="${y - 18}" width="14" height="26" rx="4" fill="${capFill}"/>`;
  }
  return s;
};

// Round-bottom plate: a flat stack behind, a plate with a grid of wells in front.
const microplate = (cols, rows, wellR, text) => tile(
  `<rect x="92" y="164" width="220" height="122" rx="8" fill="${C.light}"/>` +
  `<rect x="84" y="176" width="232" height="122" rx="8" fill="${WHITE}" stroke="${C.light}" stroke-width="2"/>` +
  `<rect x="84" y="176" width="14" height="14" rx="3" fill="${A}"/>` +
  grid(cols, rows, 200, 240, 200 / cols, 100 / rows, wellR, wellR, C.light) +
  tag(128, 306, 144, text, 18),
);

// Stacked weighing boats: each trapezoid nests on the one below.
const boatStack = (n, w, h, gap, text) => {
  let s = '';
  for (let i = 0; i < n; i++) {
    const yb = 302 - i * gap;
    const yt = yb - h;
    const inset = w * 0.12;
    s += `<path d="M${200 - w / 2} ${yt} L${200 + w / 2} ${yt} L${200 + w / 2 - inset} ${yb} L${200 - w / 2 + inset} ${yb} Z" fill="${WHITE}" stroke="${C.light}" stroke-width="2"/>`;
  }
  return tile(s + tag(120, 296, 160, text, 18));
};

// A stack of round filter discs drawn as a short cylinder.
const discStack = (r, H, top, text) => {
  let s = `<rect x="${200 - r}" y="${top}" width="${2 * r}" height="${H}" fill="${C.paper}"/>`;
  s += `<ellipse cx="200" cy="${top + H}" rx="${r}" ry="${r * 0.28}" fill="${C.paperDark}"/>`;
  for (let k = 1; k <= 3; k++) {
    const y = top + (H * k) / 4;
    s += `<path d="M${200 - r} ${y} A${r} ${r * 0.28} 0 0 0 ${200 + r} ${y}" fill="none" stroke="${C.paperDark}" stroke-width="2"/>`;
  }
  s += `<ellipse cx="200" cy="${top}" rx="${r}" ry="${r * 0.28}" fill="${C.paper}" stroke="${C.paperDark}" stroke-width="2"/>`;
  return tile(s + tag(130, 300, 140, text, 18));
};

// A screw cap: body with vertical grip ridges and an accent band on top.
const screwCap = (x, y, w, h) => {
  let s = `<rect x="${x - w / 2}" y="${y}" width="${w}" height="${h}" rx="${h * 0.3}" fill="${C.body}"/>` +
    `<rect x="${x - w / 2}" y="${y}" width="${w}" height="6" rx="3" fill="${A}"/>`;
  for (let i = 1; i < 12; i++) {
    const lx = x - w / 2 + (i * w) / 12;
    s += `<line x1="${lx}" y1="${y + 10}" x2="${lx}" y2="${y + h - 6}" stroke="${C.dark}" stroke-width="2"/>`;
  }
  return s;
};

export const illustrations = {
  // Equipment
  'DEMO-LAB-1005': heatingBlock('24 wells', false),
  'DEMO-LAB-1006': heatingBlock('2000 rpm', true),
  'DEMO-LAB-1007': magneticStirrer(),
  'DEMO-LAB-1008': overheadStirrer(),
  'DEMO-LAB-1009': precisionBalance(),
  'DEMO-LAB-1010': analyticalBalance(),
  'DEMO-LAB-1011': labBalance(),
  'DEMO-LAB-1012': phMeter(),
  'DEMO-LAB-1013': diaphragmPump(),
  'DEMO-LAB-1014': ultrasonicBath(),
  'DEMO-LAB-1015': dryingOven(),
  'DEMO-LAB-1016': orbitalShaker(),
  'DEMO-LAB-1017': penetrationThermometer(),
  'DEMO-LAB-1018': miniCentrifuge(),

  // Pipettes: models without a badge, volume variants with the range badge
  'DEMO-LAB-2003': pipetteSingle(),
  'DEMO-LAB-2003-2UL': badged(pipetteSingle, '0.1–2 µl'),
  'DEMO-LAB-2003-20UL': badged(pipetteSingle, '2–20 µl'),
  'DEMO-LAB-2004': pipetteEight(),
  'DEMO-LAB-2004-20UL': badged(pipetteEight, '2–20 µl'),
  'DEMO-LAB-2004-200UL': badged(pipetteEight, '20–200 µl'),
  'DEMO-LAB-2004-1000UL': badged(pipetteEight, '100–1000 µl'),
  'DEMO-LAB-2005': pipetteDispensing(),
  'DEMO-LAB-2005-5ML': badged(pipetteDispensing, '1–5 ml'),
  'DEMO-LAB-2005-10ML': badged(pipetteDispensing, '2–10 ml'),
  'DEMO-LAB-2006': pipetteDigital(),
  'DEMO-LAB-2006-10UL': badged(pipetteDigital, '0.5–10 µl'),
  'DEMO-LAB-2006-200UL': badged(pipetteDigital, '20–200 µl'),
  'DEMO-LAB-2006-1000UL': badged(pipetteDigital, '100–1000 µl'),

  // Stands, tips and bags
  'DEMO-LAB-2007': pipetteStand(),
  'DEMO-LAB-2008': tipRack({ front: WHITE, back: C.light, h: 44, text: '10 µl × 96' }),
  'DEMO-LAB-2009': tipRack({ front: C.metal, back: C.mid, h: 80, text: '1000 µl × 96' }),
  'DEMO-LAB-2010': tipRack({ front: C.mid, back: C.light, h: 54, text: '20 µl × 96' }),
  'DEMO-LAB-2011': tipRack({ front: GLASS, back: C.light, h: 68, filter: true, text: '200 µl × 96' }),
  'DEMO-LAB-2012': tipBag(),
  'DEMO-LAB-2013': tipRack({ front: WHITE, back: C.light, h: 44, plate: C.body, sterile: true, text: '10 µl × 96' }),

  // Tubes, bags and plates
  'DEMO-LAB-3005': tile(pouch(110, 200, 180, 120, 5, C.body) + tag(140, 262, 120, '2.0 ml', 20)),
  'DEMO-LAB-3006': tile(pouch(135, 224, 130, 90, 3, C.mid) + tag(150, 258, 100, '0.5 ml', 18)),
  'DEMO-LAB-3007': tile(
    [134, 168, 200, 232, 266].map((x) => tube(x, 300, 32, 170, WHITE, C.dark)).join('') +
    `<rect x="110" y="282" width="180" height="30" rx="6" fill="${C.body}"/>` +
    tag(130, 286, 140, '15 ml', 18),
  ),
  'DEMO-LAB-3008': tile(
    [140, 200, 260].map((x) => tube(x, 300, 46, 210, WHITE, C.mid)).join('') +
    `<rect x="110" y="282" width="180" height="30" rx="6" fill="${C.body}"/>` +
    `<rect x="110" y="282" width="180" height="5" fill="${A}"/>` +
    tag(130, 288, 140, '50 ml', 18),
  ),
  'DEMO-LAB-3009': tile(
    [160, 200, 240].map((x) => tube(x, 300, 24, 90, WHITE, A)).join('') +
    pouch(130, 262, 140, 60, 0, A) +
    tag(150, 282, 100, '2 ml', 18),
  ),
  'DEMO-LAB-3010': tile(
    roundTube(160, 320, 40, 190, WHITE, C.body) +
    roundTube(240, 320, 40, 190, WHITE, C.body) +
    tag(120, 56, 160, '5 ml', 20),
  ),
  'DEMO-LAB-3011': microplate(12, 8, 5, '96 wells'),
  'DEMO-LAB-3012': microplate(24, 16, 2.6, '384 wells'),
  'DEMO-LAB-3013': boatStack(3, 200, 44, 16, '80 × 80 mm'),
  'DEMO-LAB-3014': tile(
    [150, 200, 250].map((x, i) =>
      `<rect x="${x - 4}" y="146" width="8" height="170" fill="${WHITE}" stroke="${C.light}" stroke-width="2"/>` +
      `<path d="M${x - 3} 316 L${x + 3} 316 L${x} 328 Z" fill="${C.light}"/>` +
      `<ellipse cx="${x}" cy="128" rx="16" ry="26" fill="${i === 1 ? A : C.light}"/>`).join('') +
    tag(130, 40, 140, '3 ml', 20),
  ),
  'DEMO-LAB-3015': discStack(100, 40, 230, '125 mm'),
  'DEMO-LAB-3016': discStack(56, 40, 230, '70 mm'),
  'DEMO-LAB-3017': tile(
    screwCap(130, 274, 84, 52) +
    screwCap(270, 274, 84, 52) +
    screwCap(200, 226, 84, 52) +
    tag(150, 300, 100, '50 ml', 18),
  ),
  'DEMO-LAB-3018': boatStack(4, 120, 30, 10, '40 × 40 mm'),
};
