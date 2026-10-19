#!/usr/bin/env python3
"""Contact sheet of rendered PNGs, for checking models by eye.

    python3 tools/photo/sheet.py <dir with PNGs> <out.png> [columns]
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

src, out = Path(sys.argv[1]), sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 6
files = sorted(src.glob('*.png'))
W = 260
sheet = Image.new('RGB', (cols * W, ((len(files) + cols - 1) // cols) * (W + 22)), 'white')
draw = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGBA')
    tile = Image.new('RGBA', im.size, '#FFFFFF'); tile.alpha_composite(im)
    x, y = (i % cols) * W, (i // cols) * (W + 22)
    sheet.paste(tile.convert('RGB').resize((W, W)), (x, y))
    draw.text((x + 6, y + W + 4), f.stem.upper(), fill='#333')
sheet.save(out)
print(f'{len(files)} images -> {out}')
