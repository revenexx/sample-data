#!/usr/bin/env node
// Render the product illustrations of one pack to PNG (800 × 800) with a
// headless Chrome. Development tool only: the PNGs are committed, seed.sh
// never runs this.
//
//   node tools/build-art.mjs industrial
//
// Needs Google Chrome (CHROME=/path/to/chrome to override).
import { existsSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

const pack = process.argv[2];
if (!pack) { console.error('usage: node tools/build-art.mjs <pack>'); process.exit(2); }
const { illustrations } = await import(`./art/${pack}.mjs`);
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const out = join(ROOT, 'packs', pack, 'assets', 'images');
mkdirSync(out, { recursive: true });
const tmp = join(tmpdir(), `sample-data-art-${process.pid}`);
mkdirSync(tmp, { recursive: true });

for (const [sku, svg] of Object.entries(illustrations)) {
  const name = sku.toLowerCase();
  writeFileSync(join(out, `${name}.svg`), svg);
  const html = join(tmp, `${name}.html`);
  writeFileSync(html, `<!doctype html><html><body style="margin:0">${svg}</body></html>`);
  const png = join(out, `${name}.png`);
  rmSync(png, { force: true });
  execFileSync(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', `--user-data-dir=${join(tmp, 'profile')}`,
    '--window-size=800,800', `--screenshot=${png}`, pathToFileURL(html).href], { stdio: 'ignore' });
  if (!existsSync(png)) throw new Error(`Chrome wrote no ${png}`);
  console.log(`  ${name}.png`);
}
