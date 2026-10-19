// A one-page A4 product data sheet written straight to PDF, with no browser:
// the built-in Helvetica fonts, and the product photo embedded as the JPEG it is.
// Used by tools/build-docs.mjs. Text is WinAnsi (Latin-1 plus dashes and quotes).

// Advance widths (1/1000 em) of the standard Helvetica fonts for ASCII 32..126.
const W = {
  regular: [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556,
    556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556, 278, 556, 556,
    222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584],
  bold: [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556,
    556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778,
    667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556, 333, 611, 611,
    278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584],
};
const WIDE = { '—': 1000, '–': 556, '·': 278, '°': 400, '×': 584, '±': 584, 'µ': 556, 'Ä': 667, 'Ö': 778, 'Ü': 722, 'ß': 611 };
const WIN = { '€': 0x80, '…': 0x85, '‘': 0x91, '’': 0x92, '“': 0x93, '”': 0x94, '•': 0x95, '–': 0x96, '—': 0x97 };

const width = (s, size, bold) => [...s].reduce((sum, ch) => {
  const c = ch.codePointAt(0);
  return sum + (c >= 32 && c <= 126 ? W[bold ? 'bold' : 'regular'][c - 32] : WIDE[ch] ?? 556);
}, 0) * size / 1000;

// A PDF string literal in WinAnsi; anything outside it fails loudly instead of printing garbage.
function str(s) {
  const bytes = [...s].map((ch) => {
    const c = ch.codePointAt(0);
    if (WIN[ch]) return WIN[ch];
    if ((c >= 32 && c <= 126) || (c >= 160 && c <= 255)) return c;
    throw new Error(`character ${JSON.stringify(ch)} is not in WinAnsi`);
  });
  return '(' + Buffer.from(bytes).toString('latin1').replace(/[\\()]/g, (m) => '\\' + m) + ')';
}

function wrap(text, size, maxWidth, bold = false) {
  const lines = [];
  let line = '';
  for (const word of text.split(/\s+/)) {
    const next = line ? `${line} ${word}` : word;
    if (line && width(next, size, bold) > maxWidth) { lines.push(line); line = word; } else line = next;
  }
  if (line) lines.push(line);
  return lines;
}

const rgb = (hex) => [1, 3, 5].map((i) => (parseInt(hex.slice(i, i + 2), 16) / 255).toFixed(3)).join(' ');

// Pixel size of a baseline or progressive JPEG, read from its SOF marker.
function jpegSize(buf) {
  for (let i = 2; i < buf.length;) {
    const marker = buf[i + 1], len = buf.readUInt16BE(i + 2);
    if (marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker)) {
      return { height: buf.readUInt16BE(i + 5), width: buf.readUInt16BE(i + 7), comps: buf[i + 9] };
    }
    i += 2 + len;
  }
  throw new Error('no JPEG frame header');
}

// sheet: { maker, title, subtitle, jpeg (Buffer), rows: [[label, value]], paragraphs: [text], footer, accent }
export function dataSheetPdf(sheet) {
  const PW = 595.28, PH = 841.89, M = 34;           // A4 in points, 12 mm margin
  const ink = '#1f2329', grey = '#5b6270', red = '#b42318';
  const ops = [];
  const text = (s, x, y, size, color = ink, bold = false) =>
    ops.push(`BT /${bold ? 'F2' : 'F1'} ${size} Tf ${rgb(color)} rg ${x.toFixed(2)} ${y.toFixed(2)} Td ${str(s)} Tj ET`);
  const rule = (x1, x2, y, w, color) => ops.push(`${rgb(color)} RG ${w} w ${x1.toFixed(2)} ${y.toFixed(2)} m ${x2.toFixed(2)} ${y.toFixed(2)} l S`);

  ops.push(`1 1 1 rg 0 0 ${PW} ${PH} re f`);                                    // white page
  let y = PH - M - 12;
  text(sheet.maker, M, y, 12, ink, true);                                            // header
  const sample = 'SAMPLE — fictional product';
  text(sample, PW - M - width(sample, 12, true), y, 12, red, true);
  y -= 9;
  rule(M, PW - M, y, 2.25, sheet.accent);

  y -= 13.5 + 18;                                                                    // title and subtitle
  text(sheet.title, M, y, 18, ink, true);
  y -= 6 + 11.25;
  text(sheet.subtitle, M, y, 11.25, grey);
  y -= 13.5;

  const img = 195, top = y;                                                          // photo left, values right
  ops.push(`q ${img} 0 0 ${img} ${M} ${(top - img).toFixed(2)} cm /Im1 Do Q`);
  const tx = M + img + 21, tw = PW - M - tx, size = 9.75;
  let ty = top;
  for (const [label, value] of sheet.rows) {
    const lines = wrap(String(value), size, tw * 0.55 - 4);
    const labels = wrap(String(label), size, tw * 0.45 - 6);
    const h = 10.5 + Math.max(lines.length, labels.length) * size * 1.2;
    labels.forEach((l, i) => text(l, tx, ty - 5.25 - size - i * size * 1.2, size, grey));
    lines.forEach((l, i) => text(l, tx + tw * 0.45, ty - 5.25 - size - i * size * 1.2, size));
    ty -= h;
    rule(tx, tx + tw, ty, 0.75, '#e3e5e8');
  }
  y = Math.min(top - img, ty) - 9.75;

  for (const p of sheet.paragraphs) {                                                // descriptions
    for (const l of wrap(p, 9.75, PW - 2 * M)) { y -= 14.6; text(l, M, y, 9.75); }
    y -= 9.75;
  }
  y -= 21 - 9.75;
  for (const l of wrap(sheet.footer, 8.25, PW - 2 * M)) { y -= 11; text(l, M, y, 8.25, grey); }

  const content = Buffer.from(ops.join('\n'), 'latin1');
  const { width: iw, height: ih, comps } = jpegSize(sheet.jpeg);
  const objects = [
    '<< /Type /Catalog /Pages 2 0 R >>',
    '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${PW} ${PH}] /Contents 4 0 R /Resources << /Font << /F1 5 0 R /F2 6 0 R >> /XObject << /Im1 7 0 R >> >> >>`,
    [`<< /Length ${content.length} >>`, content],
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>',
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>',
    [`<< /Type /XObject /Subtype /Image /Width ${iw} /Height ${ih} /ColorSpace /${comps === 1 ? 'DeviceGray' : 'DeviceRGB'} /BitsPerComponent 8 /Filter /DCTDecode /Length ${sheet.jpeg.length} >>`, sheet.jpeg],
  ];
  const parts = [Buffer.from('%PDF-1.4\n%\xe2\xe3\xcf\xd3\n', 'latin1')];
  const offsets = [];
  let pos = parts[0].length;
  objects.forEach((o, i) => {
    const chunk = Array.isArray(o)
      ? Buffer.concat([Buffer.from(`${i + 1} 0 obj\n${o[0]}\nstream\n`, 'latin1'), o[1], Buffer.from('\nendstream\nendobj\n', 'latin1')])
      : Buffer.from(`${i + 1} 0 obj\n${o}\nendobj\n`, 'latin1');
    offsets.push(pos);
    parts.push(chunk);
    pos += chunk.length;
  });
  const xref = `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n` + offsets.map((o) => `${String(o).padStart(10, '0')} 00000 n \n`).join('')
    + `trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${pos}\n%%EOF\n`;
  parts.push(Buffer.from(xref, 'latin1'));
  return Buffer.concat(parts);
}
