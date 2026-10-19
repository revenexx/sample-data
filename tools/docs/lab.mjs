// Drawing geometry and data-sheet content for the lab pack. Every number
// matches the product data (products.json) and the STEP models in tools/cad/lab.py.
// Drawings are side views along the horizontal axis: the open end (or cap) on the left.

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
const poly = (pts) => `<polygon points="${pts.map(([x, y]) => `${x},${y}`).join(' ')}"/>`;

// Microcentrifuge tube 1.5 ml at 8:1. Length 38.6, body Ø 10.4, cap Ø 11.4 x 7.0, tip Ø 2.4, cone 8.0.
const tube15 = (() => {
  const s = 8, x0 = 200, yc = 380;
  const X = (t) => x0 + t * s, Y = (r) => yc + r * s;
  const top = [[0, -5.7], [7, -5.7], [7, -5.2], [30.6, -5.2], [38.6, -1.2]];
  const pts = [...top, ...top.slice().reverse().map(([t, r]) => [t, -r])].map(([t, r]) => [X(t), Y(r)]);
  return arrow + poly(pts) +
    centre(X(-3), yc, X(38.6) + 14, yc) +
    dimH(X(0), X(38.6), Y(5.7) + 60, Y(5.7) + 6, '38.6') +
    dimH(X(0), X(7), Y(-5.7) - 50, Y(-5.7) - 6, '7.0') +
    dimV(Y(-5.7), Y(5.7), X(0) - 50, X(0) - 6, 'Ø 11.4') +
    dimV(Y(-5.2), Y(5.2), X(38.6) + 70, X(38.6) + 6, 'Ø 10.4');
})();

// Centrifuge tube 50 ml at 3:1. Length 115, body Ø 28, cap Ø 30 x 15, tip Ø 10, cone 20.
const tube50 = (() => {
  const s = 3, x0 = 200, yc = 380;
  const X = (t) => x0 + t * s, Y = (r) => yc + r * s;
  const top = [[0, 15], [15, 15], [15, 14], [95, 14], [115, 5]];
  const pts = [...top, ...top.slice().reverse().map(([t, r]) => [t, -r])].map(([t, r]) => [X(t), Y(r)]);
  return arrow + poly(pts) +
    centre(X(-8), yc, X(115) + 14, yc) +
    dimH(X(0), X(115), Y(15) + 60, Y(15) + 6, '115.0') +
    dimH(X(0), X(15), Y(-15) - 50, Y(-15) - 6, '15.0') +
    dimV(Y(-15), Y(15), X(0) - 50, X(0) - 6, 'Ø 30.0') +
    dimV(Y(-14), Y(14), X(115) + 70, X(115) + 6, 'Ø 28.0');
})();

// Pipette tip 200 µl at 8:1. Length 53, collar Ø 7.0 for 14.0, tapering to a Ø 1.0 orifice, 0.4 wall.
const tip200 = (() => {
  const s = 8, x0 = 200, yc = 380;
  const X = (t) => x0 + t * s, Y = (r) => yc + r * s;
  const outer = [[0, 3.5], [14, 3.5], [53, 0.5]];
  const pts = [...outer, ...outer.slice().reverse().map(([t, r]) => [t, -r])].map(([t, r]) => [X(t), Y(r)]);
  const inner = (sign) => `<polyline points="${[[0, 3.1], [14, 3.1], [52.6, 0.1]].map(([t, r]) => `${X(t)},${Y(sign * r)}`).join(' ')}" stroke-width="1"/>`;
  return arrow + poly(pts) + inner(1) + inner(-1) +
    centre(X(-3), yc, X(53) + 14, yc) +
    dimH(X(0), X(53), Y(3.5) + 60, Y(3.5) + 6, '53.0') +
    dimH(X(0), X(14), Y(-3.5) - 50, Y(-3.5) - 6, '14.0') +
    dimV(Y(-3.5), Y(3.5), X(0) - 50, X(0) - 6, 'Ø 7.0');
})();

export const drawings = {
  'demo-lab-3001-microcentrifuge-tube-1-5ml': { sku: 'DEMO-LAB-3001', scale: '8:1', svg: tube15 },
  'demo-lab-3002-centrifuge-tube-50ml': { sku: 'DEMO-LAB-3002', scale: '3:1', svg: tube50 },
  'demo-lab-2002-pipette-tip-200ul': { sku: 'DEMO-LAB-2002', scale: '8:1', svg: tip200 },
};

export const datasheets = {};
