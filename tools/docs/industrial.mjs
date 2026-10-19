// Drawing geometry and data-sheet content for the industrial pack. Every
// number matches the product data (products.json) and the STEP models.

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

// Hex bolt M8 × 40 at 8:1 (1 mm = 8 px). Side view and head view.
const bolt = (() => {
  const s = 8, x0 = 200, y0 = 330, head = 5.3 * s, len = 40 * s, d = 8 * s, af = 13 * s, ac = 15.01 * s;
  return arrow +
    `<rect x="${x0}" y="${y0 - ac / 2}" width="${head}" height="${ac}"/>` +
    `<line x1="${x0}" y1="${y0 - af / 2}" x2="${x0 + head}" y2="${y0 - af / 2}" stroke-width="1"/><line x1="${x0}" y1="${y0 + af / 2}" x2="${x0 + head}" y2="${y0 + af / 2}" stroke-width="1"/>` +
    `<path d="M${x0 + head} ${y0 - d / 2} h${len - 6} l6 6 v${d - 12} l-6 6 h-${len - 6}"/>` +
    centre(x0 - 30, y0, x0 + head + len + 30, y0) +
    dimH(x0 + head, x0 + head + len, y0 + ac / 2 + 70, y0 + d / 2 + 6, '40') +
    dimH(x0, x0 + head, y0 - ac / 2 - 40, y0 - ac / 2 - 6, '5.3') +
    dimV(y0 - d / 2, y0 + d / 2, x0 + head + len + 80, x0 + head + len + 6, 'M8') +
    // head view
    `<polygon points="${[0, 1, 2, 3, 4, 5].map((i) => { const a = Math.PI / 3 * i; return `${880 + (ac / 2) * Math.cos(a)},${y0 + (ac / 2) * Math.sin(a)}`; }).join(' ')}"/>` +
    `<circle cx="880" cy="${y0}" r="${af / 2}" stroke-width="1"/>` + centre(800, y0, 960, y0) + centre(880, y0 - 80, 880, y0 + 80) +
    dimV(y0 - af / 2, y0 + af / 2, 760, 860, 'SW 13');
})();

// Wood screw 4 × 40 at 8:1, countersunk 90°.
const screw = (() => {
  const s = 8, x0 = 220, y0 = 330, d = 4 * s, hd = 8 * s, hh = 2 * s, len = 40 * s, tip = 4 * s;
  return arrow +
    `<path d="M${x0} ${y0 - hd / 2} l${hh} ${(hd - d) / 2} h${len - hh - tip} l${tip} ${d / 2} l-${tip} ${d / 2} h-${len - hh - tip} l-${hh} ${(hd - d) / 2} z"/>` +
    centre(x0 - 30, y0, x0 + len + 30, y0) +
    dimH(x0, x0 + len, y0 + hd / 2 + 70, y0 + d / 2 + 6, '40') +
    dimV(y0 - hd / 2, y0 + hd / 2, x0 - 50, x0 - 6, 'Ø 8') +
    dimV(y0 - d / 2, y0 + d / 2, x0 + len + 80, x0 + len - tip, 'Ø 4') +
    `<text x="${x0 + 30}" y="${y0 - hd / 2 - 30}" font-size="18" stroke="none" fill="#1f2329">90°, T20</text>`;
})();

// Cutting disc 125 × 1.0 × 22.23 at 3:1, face view and section.
const disc = (() => {
  const s = 3, cx = 380, cy = 360, r = 62.5 * s, b = 11.115 * s;
  return arrow +
    `<circle cx="${cx}" cy="${cy}" r="${r}"/><circle cx="${cx}" cy="${cy}" r="${b}"/>` + centre(cx - r - 30, cy, cx + r + 30, cy) + centre(cx, cy - r - 30, cx, cy + r + 30) +
    dimH(cx - r, cx + r, cy + r + 60, cy + 10, 'Ø 125') +
    dimH(cx - b, cx + b, cy - r - 50, cy - b, 'Ø 22.23') +
    `<rect x="760" y="${cy - r}" width="${1 * s * 4}" height="${2 * r}" fill="#d9dde3"/>` +
    `<text x="790" y="${cy}" font-size="18" stroke="none" fill="#1f2329">1.0 (drawn at 12:1)</text>`;
})();

export const drawings = {
  'demo-ind-2002-hex-bolt-m8x40': { sku: 'DEMO-IND-2002', scale: '8:1', svg: bolt },
  'demo-ind-2001-wood-screw-4x40': { sku: 'DEMO-IND-2001', scale: '8:1', svg: screw },
  'demo-ind-2003-cutting-disc-125': { sku: 'DEMO-IND-2003', scale: '3:1', svg: disc },
};

export const datasheets = {};
