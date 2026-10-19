#!/usr/bin/env node
// Automatic one-page data sheets (PDF) for every parent product of one pack that
// has no hand-made sheet. Written from the pack's own product data by
// tools/sheet-pdf.mjs: no browser, no network, the same bytes for the same input.
//
//   node tools/build-datasheets.mjs industrial
//
// Output: packs/<pack>/assets/downloads/<sku lowercase>-data-sheet.pdf
// tools/build-pack.py links each one to its parent and to the parent's variants.
// Reads packs/<pack>/products.json, attributes.json, attribute-options.json,
// manufacturers.json and the photo packs/<pack>/assets/images/<sku>.jpg.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dataSheetPdf } from './sheet-pdf.mjs';
import { ACCENT, FOOTER } from './sheet-style.mjs';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const pack = process.argv[2];
if (!pack || !ACCENT[pack]) { console.error('usage: node tools/build-datasheets.mjs <industrial|electrical|office|lab>'); process.exit(2); }
const PACK = join(ROOT, 'packs', pack);
const read = (file) => JSON.parse(readFileSync(join(PACK, file), 'utf8'));

const products = read('products.json');
const attrs = Object.fromEntries(read('attributes.json').map((a) => [a.code, a]));
const options = Object.fromEntries(read('attribute-options.json').map((o) => [`${o.attribute}|${o.code}`, o.labels['en-US']]));
const makers = Object.fromEntries(read('manufacturers.json').map((m) => [m.code, m.name]));
const bySku = Object.fromEntries(products.map((p) => [p.sku, p]));

// SKUs with a hand-made sheet keep it (their file is named the same way, so they must be skipped).
const { datasheets: handMade } = await import(`./docs/${pack}.mjs`);
const hand = new Set(Object.values(handMade).map((d) => d.sku));
const spec = readFileSync(join(ROOT, 'tools', 'packs', `${pack}.py`), 'utf8');
for (const m of spec.matchAll(/"datasheets":\s*\{([^}]*)\}/g)) for (const v of m[1].matchAll(/"([A-Z0-9-]+)"/g)) hand.add(v[1]);

// Unit codes of the metric attributes as they are printed on the sheet.
const UNIT = {
  AMPERE: 'A', AMPERE_HOUR: 'Ah', CENTIMETER: 'cm', DECIBEL: 'dB', GRAM: 'g', DEGREE: '°', GRAM_PER_SQUARE_METER: 'g/m²', KELVIN: 'K', KILOGRAM: 'kg',
  LITER: 'l', LUMEN: 'lm', METER: 'm', MICROLITER: 'µl', MILLILITER: 'ml', MILLIMETER: 'mm', REVOLUTIONS_PER_MINUTE: 'rpm',
  VOLT: 'V', WATT: 'W',
};
// Attributes that are not printed: names, texts and media, and the CAD flag (its label is not in this pack).
const SKIP = new Set(['name', 'description', 'image', 'demo_has_cad']);

// 21000 -> "21,000"; decimals are kept as they are in the data.
const grouped = (n) => String(n).replace(/^(-?\d+)/, (d) => d.replace(/\B(?=(\d{3})+(?!\d))/g, ','));

function valueText(code, v) {
  const attr = attrs[code];
  if (!attr) throw new Error(`${pack}: no attribute ${code}`);
  switch (attr.type) {
    case 'metric': {
      const unit = UNIT[v.unit];
      if (!unit) throw new Error(`${pack}: no label for unit ${v.unit}`);
      return `${grouped(v.amount)}${unit === '°' ? '' : ' '}${unit}`;
    }
    case 'select': {
      const label = options[`${code}|${v}`];
      if (!label) throw new Error(`${pack}: no option ${code}|${v}`);
      return label;
    }
    case 'boolean': return v === true || v === 'true' ? 'Yes' : 'No';
    case 'number': return grouped(v);
    default: return String(v);
  }
}

const labelOf = (code) => {
  const label = attrs[code]?.labels['en-US'];
  if (!label) throw new Error(`${pack}: no en-US label for ${code}`);
  return label;
};

// The rows of one parent: its own attribute values in attribute order, then its variants (their axis option labels).
function rowsFor(p, variants) {
  const common = p.attribute_values.common;
  const codes = Object.keys(common)
    .filter((code) => !SKIP.has(code) && attrs[code]?.type !== 'asset_collection')
    .filter((code) => common[code] !== null && common[code] !== undefined && common[code] !== '')
    .sort((a, b) => (attrs[a]?.position ?? 0) - (attrs[b]?.position ?? 0));
  const rows = codes.map((code) => [labelOf(code), valueText(code, common[code])]);
  if (variants.length) {
    const labels = variants.map((vp) => {
      const axis = Object.keys(vp.attribute_values.common).filter((k) => !(k in common));
      if (axis.length !== 1) throw new Error(`${vp.sku}: expected one variant axis, got ${axis.join(',')}`);
      return valueText(axis[0], vp.attribute_values.common[axis[0]]);
    });
    rows.push(['Variants', labels.join(', ')]);
  }
  return rows;
}

const outDir = join(PACK, 'assets', 'downloads');
mkdirSync(outDir, { recursive: true });
let written = 0, skipped = 0;
for (const p of products) {
  if (p.parent) continue;                                               // variants share their parent's sheet
  if (hand.has(p.sku)) { skipped++; continue; }
  const en = p.attribute_values.locale_specific['en-US'];
  const de = p.attribute_values.locale_specific['de-DE'];
  const maker = makers[p.manufacturer];
  if (!maker) throw new Error(`${p.sku}: no manufacturer ${p.manufacturer}`);
  const photo = join(PACK, 'assets', 'images', `${p.sku.toLowerCase()}.jpg`);
  if (!existsSync(photo)) throw new Error(`${p.sku}: no photo ${photo}`);
  const variants = products.filter((v) => v.parent === p.sku);
  const pdf = dataSheetPdf({
    maker,
    title: en.name,
    subtitle: `${de.name} · ${p.sku}`,
    jpeg: readFileSync(photo),
    rows: rowsFor(p, variants),
    paragraphs: [en.description, de.description],
    footer: FOOTER,
    accent: ACCENT[pack],
  });
  writeFileSync(join(outDir, `${p.sku.toLowerCase()}-data-sheet.pdf`), pdf);
  written++;
}
console.log(`${pack}: ${written} data sheets written, ${skipped} hand-made kept`);
