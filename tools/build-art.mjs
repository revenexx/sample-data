#!/usr/bin/env node
// Render the product illustrations of one pack to PNG (800 × 800) with
// rsvg-convert (librsvg; no browser). Development tool only: the PNGs are
// committed, seed.sh never runs this.
//
//   node tools/build-art.mjs industrial
//
// Needs rsvg-convert (macOS: brew install librsvg; RSVG=/path/to/rsvg-convert
// to override). A PNG is rendered again only when its SVG changed or is new.
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

const pack = process.argv[2];
if (!pack) { console.error('usage: node tools/build-art.mjs <pack>'); process.exit(2); }
const { illustrations } = await import(`./art/${pack}.mjs`);
const RSVG = process.env.RSVG || 'rsvg-convert';
const out = join(ROOT, 'packs', pack, 'assets', 'images');
mkdirSync(out, { recursive: true });

for (const [sku, svg] of Object.entries(illustrations)) {
  const name = sku.toLowerCase();
  const svgPath = join(out, `${name}.svg`), png = join(out, `${name}.png`);
  if (existsSync(png) && existsSync(svgPath) && readFileSync(svgPath, 'utf8') === svg) continue;
  writeFileSync(svgPath, svg);
  // Render beside the target and move it in, so a failed run never leaves a
  // product without its picture.
  execFileSync(RSVG, ['-w', '800', '-h', '800', svgPath, '-o', `${png}.tmp`], { stdio: 'inherit' });
  renameSync(`${png}.tmp`, png);
  console.log(`  ${name}.png`);
}
