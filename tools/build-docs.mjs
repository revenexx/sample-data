#!/usr/bin/env node
// Technical drawings (SVG + PDF) and data sheets (PDF) for one pack, generated
// from our own numbers and the pack's product data. Development tool only:
// the files are committed, the seeder never runs this.
//
//   node tools/build-docs.mjs industrial            # drawings and data sheets
//   node tools/build-docs.mjs industrial --sheets   # data sheets only
//
// The drawing PDFs need Google Chrome (CHROME=/path/to/chrome to override); the
// data sheets are written directly (tools/sheet-pdf.mjs) from the pack's product
// photos: run tools/build-photos.py first.
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dataSheetPdf } from './sheet-pdf.mjs';
import { ACCENT, FOOTER } from './sheet-style.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

const pack = process.argv[2];
if (!pack) { console.error('usage: node tools/build-docs.mjs <pack> [--sheets]'); process.exit(2); }
const sheetsOnly = process.argv.includes('--sheets');
const { drawings, datasheets } = await import(`./docs/${pack}.mjs`);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PACK = join(ROOT, 'packs', pack);
const products = JSON.parse(readFileSync(join(PACK, 'products.json'), 'utf8'));
const bySku = Object.fromEntries(products.map((p) => [p.sku, p]));
const makers = Object.fromEntries(JSON.parse(readFileSync(join(PACK, 'manufacturers.json'), 'utf8')).map((m) => [m.code, m.name]));
const esc = (v) => String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const tmp = join(tmpdir(), `sample-data-docs-${process.pid}`);
mkdirSync(tmp, { recursive: true });

// Chrome stamps the print time into the PDF; a fixed stamp of the same length
// (byte offsets stay valid) makes a rebuild without changes byte-identical, so
// the seeder does not upload it again.
function pdf(html, file) {
  const page = join(tmp, 'page.html');
  writeFileSync(page, html);
  rmSync(file, { force: true });
  execFileSync(CHROME, ['--headless=new', '--disable-gpu', `--user-data-dir=${join(tmp, 'profile')}`, '--no-pdf-header-footer',
    `--print-to-pdf=${file}`, pathToFileURL(page).href], { stdio: 'ignore' });
  if (!existsSync(file)) throw new Error(`Chrome wrote no ${file}`);
  const bytes = readFileSync(file).toString('latin1').replace(/\/(CreationDate|ModDate) \(D:\d{14}/g, '/$1 (D:20260101000000');
  writeFileSync(file, Buffer.from(bytes, 'latin1'));
}

const page = (body, landscape) => `<!doctype html><html><head><meta charset="utf-8"><style>
  @page { size: A4 ${landscape ? 'landscape' : 'portrait'}; margin: 12mm; }
  body { font-family: Helvetica, Arial, sans-serif; color: #1f2329; margin: 0; }
  .sample { color: #b42318; font-weight: 700; letter-spacing: .04em; }
</style></head><body>${body}</body></html>`;

const drawingsDir = join(PACK, 'assets', 'drawings');
mkdirSync(drawingsDir, { recursive: true });
for (const [name, d] of sheetsOnly ? [] : Object.entries(drawings)) {
  const p = bySku[d.sku];
  const title = esc(p.attribute_values.locale_specific['en-US'].name);
  // Title block: what a drawing sheet carries, plus the sample marking.
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1188 840" width="1188" height="840" font-family="Helvetica, Arial, sans-serif">
  <rect x="10" y="10" width="1168" height="820" fill="#fff" stroke="#1f2329" stroke-width="2"/>
  <g stroke="#1f2329" fill="none" stroke-width="2">${d.svg}</g>
  <g transform="translate(748 700)">
    <rect width="420" height="120" fill="#fff" stroke="#1f2329" stroke-width="2"/>
    <line x1="0" y1="40" x2="420" y2="40" stroke="#1f2329"/><line x1="0" y1="80" x2="420" y2="80" stroke="#1f2329"/>
    <line x1="280" y1="40" x2="280" y2="120" stroke="#1f2329"/>
    <text x="12" y="27" font-size="17" font-weight="700">${title}</text>
    <text x="12" y="66" font-size="14">${esc(d.sku)}</text><text x="292" y="66" font-size="14">Not to scale</text>
    <text x="12" y="106" font-size="13" fill="#b42318" font-weight="700">SAMPLE — fictional product</text><text x="292" y="106" font-size="14">mm</text>
  </g></svg>`;
  writeFileSync(join(drawingsDir, `${name}.svg`), svg);
  pdf(page(svg.replace('width="1188" height="840"', 'width="100%"'), true), join(drawingsDir, `${name}.pdf`));
  console.log(`  drawings/${name}.svg + .pdf`);
}

const downloadsDir = join(PACK, 'assets', 'downloads');
mkdirSync(downloadsDir, { recursive: true });
for (const [name, sheet] of Object.entries(datasheets)) {
  const p = bySku[sheet.sku];
  const en = p.attribute_values.locale_specific['en-US'];
  const de = p.attribute_values.locale_specific['de-DE'];
  writeFileSync(join(downloadsDir, `${name}.pdf`), dataSheetPdf({
    maker: makers[p.manufacturer],
    title: en.name,
    subtitle: `${de.name} · ${p.sku}`,
    jpeg: readFileSync(join(PACK, 'assets', 'images', `${sheet.sku.toLowerCase()}.jpg`)),
    rows: sheet.rows,
    paragraphs: [en.description, de.description],
    footer: FOOTER,
    accent: ACCENT[pack],
  }));
  console.log(`  downloads/${name}.pdf`);
}
