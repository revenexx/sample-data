"""Check and preview the STEP models of one pack (development tool only).

    tools/cad/.venv/bin/python tools/cad/check.py <pack> [OUT_DIR]

Builds every part, compares its bounding box with the expected outer
dimensions (EXPECT in the pack script), renders an isometric SVG, converts it
with rsvg-convert (no browser) and writes one contact sheet per pack.
"""
import importlib
import subprocess
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parent))
pack = sys.argv[1]
out = Path(sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-501/cadwork") / pack
out.mkdir(parents=True, exist_ok=True)
mod = importlib.import_module(pack)
bad = 0
tiles = []
for stem, build in mod.PARTS.items():
    shape = build()
    solids = shape.val().Solids() if hasattr(shape.val(), "Solids") else []
    bb = shape.val().BoundingBox()
    got = sorted((bb.xlen, bb.ylen, bb.zlen))
    exp = sorted(mod.EXPECT[stem])
    ok = all(abs(g - e) <= max(0.25, 0.004 * e) for g, e in zip(got, exp))
    valid = shape.val().isValid() and len(solids) >= 1 and shape.val().Volume() > 0
    if not (ok and valid):
        bad += 1
    print(("OK  " if ok and valid else "BAD ") + stem, " got %.2f x %.2f x %.2f" % (bb.xlen, bb.ylen, bb.zlen),
          " exp %s" % (mod.EXPECT[stem],), "" if valid else " INVALID", " solids=%d" % len(solids))
    svg = out / f"{stem}.svg"
    cq.exporters.export(shape, str(svg), opt={"width": 420, "height": 340, "marginLeft": 20, "marginTop": 20,
                                              "showAxes": False, "projectionDir": (1.0, -1.3, 0.9),
                                              "strokeWidth": 0.6, "strokeColor": (30, 30, 30), "hiddenColor": (200, 200, 200),
                                              "showHidden": False})
    subprocess.run(["rsvg-convert", "-b", "white", "-w", "420", "-h", "340", "-o", str(out / f"{stem}.png"), str(svg)], check=True)
    tiles.append((stem, "%.1f x %.1f x %.1f mm" % (bb.xlen, bb.ylen, bb.zlen), ok and valid))
print("bad:", bad)

from PIL import Image, ImageDraw, ImageOps  # noqa: E402

per = 12
for n in range(0, len(tiles), per):
    chunk = tiles[n:n + per]
    cols = 4
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 420, rows * 385), "white")
    d = ImageDraw.Draw(sheet)
    for i, (stem, dims, ok) in enumerate(chunk):
        x, y = (i % cols) * 420, (i // cols) * 385
        sheet.paste(ImageOps.flip(Image.open(out / f"{stem}.png")), (x, y))
        d.text((x + 8, y + 345), stem, fill=(0, 0, 0) if ok else (200, 0, 0))
        d.text((x + 8, y + 362), dims, fill=(60, 60, 60))
    sheet.save(out / f"sheet-{n // per + 1}.png")
print("sheets in", out)
sys.exit(1 if bad else 0)
