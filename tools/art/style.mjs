// One visual style for every product illustration in the sample data:
// flat shapes, neutral product colours, one small accent in the pack colour,
// a soft floor shadow, on a light tile. Drawn from scratch; nothing traced.
export const C = {
  tile: '#F4F3F1',
  shadow: 'rgba(24, 28, 36, 0.10)',
  dark: '#2F343C',
  body: '#4A515C',
  mid: '#7B838F',
  light: '#C9CED6',
  metal: '#A7AEB8',
  paper: '#E6DCCB',
  paperDark: '#CDBFA6',
  white: '#FFFFFF',
};

export const ACCENT = { industrial: '#E8930C', electrical: '#2F6FE0', office: '#14998C', lab: '#C0397B' };

/** A 400×400 tile: background, floor shadow, the drawing, an optional corner badge. */
export function tile(inner, { badge, accent } = {}) {
  const b = badge
    ? `<g><rect x="300" y="24" width="76" height="40" rx="20" fill="${accent}"/>` +
      `<text x="338" y="51" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="22" font-weight="700" fill="#fff">${badge}</text></g>`
    : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="800" height="800">` +
    `<rect width="400" height="400" fill="${C.tile}"/>` +
    `<ellipse cx="200" cy="338" rx="128" ry="12" fill="${C.shadow}"/>` +
    inner + b + `</svg>`;
}

/** A plain label as drawn on packaging: no brand marks, just the spec. */
export function label(x, y, w, h, text, accent, size = 20) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff"/>` +
    `<rect x="${x}" y="${y}" width="8" height="${h}" rx="3" fill="${accent}"/>` +
    `<text x="${x + w / 2 + 4}" y="${y + h / 2 + size / 3}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="${size}" font-weight="700" fill="${C.dark}">${text}</text>`;
}
