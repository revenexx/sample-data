#!/usr/bin/env python3
"""Automatic technical drawings: one SVG sheet and one PDF per model SKU.

Usage: python3 tools/build-drawings.py <pack> [SKU ...]

Without SKUs it draws every SKU listed in tools/photo/drawings.py (DRAW[pack]). With SKUs
it draws only those. SKUs that already have a hand-made drawing (the "drawings" table in
tools/packs/<pack>.py) are skipped. Blender (tools/photo/drawing.py) runs once for all SKUs,
then rsvg-convert makes each PDF. Output: packs/<pack>/assets/drawings/<sku>-drawing.{svg,pdf}.
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLENDER = '/opt/homebrew/bin/blender'
RSVG = 'rsvg-convert'


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv):
    if not argv:
        raise SystemExit('usage: build-drawings.py <pack> [SKU ...]')
    pack, explicit = argv[0], [s.upper() for s in argv[1:]]
    draw = load(ROOT / 'tools' / 'photo' / 'drawings.py', 'drawings_list').DRAW
    if pack not in draw:
        raise SystemExit(f'no DRAW entry for pack {pack}')
    hand = set(load(ROOT / 'tools' / 'packs' / f'{pack}.py', f'pack_{pack}').PACK.get('drawings', {}).values())
    wanted = explicit or list(draw[pack])
    skus = [s for s in wanted if s not in hand]
    for s in wanted:
        if s in hand:
            print(f'skip {s}: hand-made drawing exists')
    if not skus:
        return
    out = ROOT / 'packs' / pack / 'assets' / 'drawings'
    out.mkdir(parents=True, exist_ok=True)
    cmd = [BLENDER, '-b', '-P', str(ROOT / 'tools' / 'photo' / 'drawing.py'), '--', pack, str(out), *skus]
    subprocess.run(cmd, check=True)
    for s in skus:
        svg = out / f'{s.lower()}-drawing.svg'
        pdf = out / f'{s.lower()}-drawing.pdf'
        if not svg.exists():
            raise SystemExit(f'Blender wrote no drawing for {s}')
        # SOURCE_DATE_EPOCH fixes the PDF dates, so the same SVG gives the same PDF bytes.
        subprocess.run([RSVG, '-f', 'pdf', '-o', str(pdf), str(svg)], check=True,
                       env={**os.environ, 'SOURCE_DATE_EPOCH': '1767225600'})
        print(f'drawings/{svg.name} + .pdf')


if __name__ == '__main__':
    main(sys.argv[1:])
