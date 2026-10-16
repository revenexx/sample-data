#!/usr/bin/env node
// Write ASSETS.md: every file under packs/*/assets with how it was made, so
// the provenance of each image, drawing, PDF and CAD model is on record.
//
//   node tools/build-assets-md.mjs
import { existsSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

const METHOD = {
  images: ['Illustration', 'Drawn as code in `tools/art/<pack>.mjs`, rendered to PNG by `tools/build-art.mjs`. The `.svg` next to it is the source.'],
  drawings: ['Technical drawing', 'Generated from the product dimensions by `tools/build-docs.mjs` (`tools/docs/<pack>.mjs`).'],
  downloads: ['Data sheet', 'Generated from the product data by `tools/build-docs.mjs`.'],
  cad: ['3D model (STEP)', 'Built from our own dimensions with CadQuery by `tools/cad/<pack>.py`. Simplified: correct outer dimensions, no modelled thread.'],
};

const lines = [
  '# Assets and where they come from',
  '',
  'Every image, drawing, data sheet and 3D model in this repository was made for it by revenexx, from scratch, by the scripts named below. Nothing is copied, traced or downloaded from a manufacturer, a CAD portal or a stock library. All products, makers and companies are fictional; every PDF says so on the page.',
  '',
  'Licence: the same as the rest of the data, see [LICENSE-DATA](LICENSE-DATA).',
  '',
];
for (const pack of readdirSync(join(ROOT, 'packs')).sort()) {
  const root = join('packs', pack, 'assets');
  if (!existsSync(join(ROOT, root))) continue;
  const kinds = readdirSync(join(ROOT, root)).sort();
  lines.push(`## ${pack}`, '');
  for (const kind of kinds) {
    const [title, how] = METHOD[kind] ?? [kind, ''];
    const files = readdirSync(join(ROOT, root, kind)).filter((f) => statSync(join(ROOT, root, kind, f)).isFile()).sort();
    lines.push(`### ${title}`, '', how.replace('<pack>', pack), '', '| File | Size |', '| --- | --- |');
    for (const f of files) lines.push(`| \`${join(root, kind, f)}\` | ${Math.ceil(statSync(join(ROOT, root, kind, f)).size / 1024)} KB |`);
    lines.push('');
  }
}
writeFileSync(join(ROOT, 'ASSETS.md'), lines.join('\n'));
console.log('  ASSETS.md');
