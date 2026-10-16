// Drawing geometry and data-sheet content for the electrical pack. Every
// number matches the product data (products.json) and the CAD models.
// Front and side views; 1 mm = 2 units at 2:1, 1 mm = 0.5 unit at 1:2.

// A horizontal dimension: extension lines, an arrowed line, the value above.
const dimH = (x1, x2, y, from, text) =>
  `<line x1="${x1}" y1="${from}" x2="${x1}" y2="${y + 8}" stroke-width="1"/><line x1="${x2}" y1="${from}" x2="${x2}" y2="${y + 8}" stroke-width="1"/>` +
  `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}" stroke-width="1" marker-start="url(#a)" marker-end="url(#a)"/>` +
  `<text x="${(x1 + x2) / 2}" y="${y - 8}" font-size="18" text-anchor="middle" stroke="none" fill="#1f2329">${text}</text>`;
const dimV = (y1, y2, x, from, text) =>
  `<line x1="${from}" y1="${y1}" x2="${x + 8}" y2="${y1}" stroke-width="1"/><line x1="${from}" y1="${y2}" x2="${x + 8}" y2="${y2}" stroke-width="1"/>` +
  `<line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}" stroke-width="1" marker-start="url(#a)" marker-end="url(#a)"/>` +
  `<text x="${x - 10}" y="${(y1 + y2) / 2 + 6}" font-size="18" text-anchor="end" stroke="none" fill="#1f2329">${text}</text>`;
const arrow = `<defs><marker id="a" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0 2 L10 5 L0 8 z" fill="#1f2329" stroke="none"/></marker></defs>`;
const centre = (x1, y1, x2, y2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke-width="1" stroke-dasharray="18 4 3 4"/>`;

// Surface-mounted junction box IP55, 100 × 100 × 55 mm at 2:1. Front and side.
const junctionBox = (() => {
  const s = 2, x0 = 200, y0 = 260, w = 100 * s, h = 100 * s, d = 55 * s, sx = 560;
  return arrow +
    `<rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="10"/>` +
    `<rect x="${x0 + 14}" y="${y0 + 14}" width="${w - 28}" height="28"/>` +
    `<circle cx="${x0 + w / 2}" cy="${y0 + h - 40}" r="14"/>` +
    centre(x0 - 30, y0 + h / 2, x0 + w + 30, y0 + h / 2) + centre(x0 + w / 2, y0 - 30, x0 + w / 2, y0 + h + 30) +
    dimH(x0, x0 + w, y0 + h + 60, y0 + h + 6, '100') +
    dimV(y0, y0 + h, x0 - 60, x0 - 6, '100') +
    `<rect x="${sx}" y="${y0}" width="${d}" height="${h}" rx="10"/>` +
    `<line x1="${sx + 14}" y1="${y0 + 14}" x2="${sx + d - 14}" y2="${y0 + 14}"/>` +
    dimH(sx, sx + d, y0 + h + 60, y0 + h + 6, '55') +
    `<text x="${sx}" y="${y0 - 16}" font-size="18" stroke="none" fill="#1f2329">IP55 · side</text>`;
})();

// LED panel 620 × 620 × 12 mm at 1:2. Front and edge.
const ledPanel = (() => {
  const s = 0.5, x0 = 120, y0 = 200, w = 620 * s, d = 12 * s, sx = 580;
  return arrow +
    `<rect x="${x0}" y="${y0}" width="${w}" height="${w}"/>` +
    `<rect x="${x0 + 16}" y="${y0 + 16}" width="${w - 32}" height="${w - 32}" stroke-dasharray="4 3"/>` +
    centre(x0 - 30, y0 + w / 2, x0 + w + 30, y0 + w / 2) + centre(x0 + w / 2, y0 - 30, x0 + w / 2, y0 + w + 30) +
    dimH(x0, x0 + w, y0 + w + 60, y0 + w + 6, '620') +
    dimV(y0, y0 + w, x0 - 60, x0 - 6, '620') +
    `<rect x="${sx}" y="${y0}" width="${d}" height="${w}"/>` +
    dimH(sx, sx + d, y0 + w + 60, y0 + w + 6, '12') +
    `<text x="${x0}" y="${y0 - 16}" font-size="18" stroke="none" fill="#1f2329">Front view · edge view</text>`;
})();

// Schuko socket outlet, plate 80 × 80 mm, 40 mm deep, at 2:1. Front and side.
const socketOutlet = (() => {
  const s = 2, x0 = 240, y0 = 260, w = 80 * s, d = 40 * s, sx = 540;
  return arrow +
    `<rect x="${x0}" y="${y0}" width="${w}" height="${w}" rx="14"/>` +
    `<circle cx="${x0 + 60}" cy="${y0 + 70}" r="10"/><circle cx="${x0 + w - 60}" cy="${y0 + 70}" r="10"/>` +
    `<circle cx="${x0 + w / 2}" cy="${y0 + 110}" r="12"/>` +
    centre(x0 - 30, y0 + w / 2, x0 + w + 30, y0 + w / 2) + centre(x0 + w / 2, y0 - 30, x0 + w / 2, y0 + w + 30) +
    dimH(x0, x0 + w, y0 + w + 60, y0 + w + 6, '80') +
    dimV(y0, y0 + w, x0 - 60, x0 - 6, '80') +
    `<rect x="${sx}" y="${y0}" width="${d}" height="${w}" rx="8"/>` +
    dimH(sx, sx + d, y0 + w + 60, y0 + w + 6, '40') +
    `<text x="${x0}" y="${y0 - 16}" font-size="18" stroke="none" fill="#1f2329">Front view · side view</text>`;
})();

export const drawings = {
  'demo-ele-2004-junction-box-ip55': { sku: 'DEMO-ELE-2004', scale: '2:1', svg: junctionBox },
  'demo-ele-3001-led-panel-62x62': { sku: 'DEMO-ELE-3001', scale: '1:2', svg: ledPanel },
  'demo-ele-2003-socket-outlet': { sku: 'DEMO-ELE-2003', scale: '2:1', svg: socketOutlet },
};

export const datasheets = {
  'demo-ele-1001-data-sheet': {
    sku: 'DEMO-ELE-1001',
    rows: [
      ['Cores / Adern', '3 × 1.5 mm²'], ['Conductor / Leiter', 'Copper / Kupfer'], ['Rated voltage / Nennspannung', '300 V'],
      ['Length / Länge', '100 m ring / Ring'], ['Weight / Gewicht', '9.4 kg (ring / Ring)'], ['Insulation / Isolierung', 'PVC'],
    ],
  },
};
