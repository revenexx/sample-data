// Drawing geometry and data-sheet content for the office pack. Every number
// matches the product data (products.json); the cover size is drawing-only.

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

// Ring binder and lever arch file at 1.6:1 (1 mm = 1.6 px). Front view on the
// left (cover 245 × 300 mm), spine view on the right (spine width from the data).
const binder = (spineMm, { lever = false } = {}) => {
  const s = 1.6, x0 = 150, y0 = 120, w = 245 * s, h = 300 * s, sx = 600, sw = spineMm * s;
  return arrow +
    `<rect x="${x0}" y="${y0}" width="${w}" height="${h}" rx="6"/>` +
    `<rect x="${x0 + 40}" y="${y0 + 70}" width="${w - 80}" height="${h * 0.3}" rx="4"/>` +
    centre(x0 - 20, y0 + h / 2, x0 + w + 20, y0 + h / 2) + centre(x0 + w / 2, y0 - 20, x0 + w / 2, y0 + h + 20) +
    dimH(x0, x0 + w, y0 - 40, y0 - 6, '245') +
    dimV(y0, y0 + h, x0 - 72, x0 - 6, '300') +
    // spine view
    `<rect x="${sx}" y="${y0}" width="${sw}" height="${h}" rx="6"/>` +
    (lever
      ? `<rect x="${sx - 10}" y="${y0 - 14}" width="${sw + 20}" height="14" rx="4"/>`
      : `<circle cx="${sx + sw / 2}" cy="${y0 + 28}" r="10"/><circle cx="${sx + sw / 2}" cy="${y0 + h - 28}" r="10"/>`) +
    centre(sx + sw / 2, y0 - 20, sx + sw / 2, y0 + h + 20) +
    dimH(sx, sx + sw, y0 - 40, y0 - 6, String(spineMm));
};

export const drawings = {
  'demo-off-1002-ring-binder-a4': { sku: 'DEMO-OFF-1002', scale: '1.6:1', svg: binder(75) },
  'demo-off-1003-lever-arch-80': { sku: 'DEMO-OFF-1003', scale: '1.6:1', svg: binder(80, { lever: true }) },
};

export const datasheets = {
  'demo-off-1001-data-sheet': {
    sku: 'DEMO-OFF-1001',
    rows: [
      ['Format / Format', 'A4 (210 × 297 mm)'], ['Paper weight / Grammatur', '80 g/m²'],
      ['Sheets per pack / Blatt pro Packung', '500'], ['Weight / Gewicht', '2.5 kg'],
    ],
  },
};
