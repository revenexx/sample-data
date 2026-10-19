#!/usr/bin/env python3
"""Make the manufacturer logos: one flat vector wordmark per fictional maker.

    python3 tools/build-logos.py                 # every pack
    python3 tools/build-logos.py industrial     # one pack

Writes packs/<pack>/assets/logos/<code lowercase>.svg and a 512 px wide PNG
beside it (rsvg-convert). Deterministic: the shapes and the colours come from a
SHA-256 of the maker code, never from Python's per-run hash seed, so a re-run
writes the same bytes. build-pack.py links both files as assets.

Design: a bold sans-serif wordmark (Helvetica, Arial, sans-serif) next to a
mark of three basic shapes (square, circle, triangle, diagonal bar). Colours
come from one fixed palette per pack. Generic on purpose: no real brand scheme
(no yellow-black, no red-white bold, no green-yellow) and no real logo shapes.
"""
import hashlib
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ANTHRACITE = "#2F343C"

# One or two flat colours per pack; a maker takes its colour from this list.
PALETTE = {
    "industrial": ["#7A1F2B", "#2F343C"],   # burgundy and anthracite
    "electrical": ["#4A6078", "#2F3E4E"],   # blue-grey
    "office": ["#1F6F6B", "#2B3B3A"],       # teal
    "lab": ["#9B2C6B", "#3A2A35"],          # magenta
}
SHAPES = ["square", "circle", "triangle", "bar"]
# Three slots in a 160 x 112 mark box (slot 0 is the big one).
SLOTS = [(0, 0, 96), (112, 0, 48), (112, 64, 48)]


def digest(code):
    return hashlib.sha256(code.encode("utf-8")).digest()


def shape_svg(kind, x, y, s, fill):
    if kind == "square":
        return f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{fill}"/>'
    if kind == "circle":
        r = s / 2
        return f'<circle cx="{x + r}" cy="{y + r}" r="{r}" fill="{fill}"/>'
    if kind == "triangle":
        pts = [(x, y + s), (x + s / 2, y), (x + s, y + s)]
    else:  # diagonal bar: a parallelogram running corner to corner
        pts = [(x, y + s * 0.75), (x + s * 0.75, y), (x + s, y + s * 0.25), (x + s * 0.25, y + s)]
    points = " ".join(f"{px:g},{py:g}" for px, py in pts)
    return f'<polygon points="{points}" fill="{fill}"/>'


def logo_svg(pack, code, name):
    h = digest(code)
    palette = PALETTE[pack]
    colours = [palette[0], palette[-1]]
    parts = []
    for i, (x, y, s) in enumerate(SLOTS):
        kind = SHAPES[h[i] % len(SHAPES)]
        # Slot 0 in the first colour; the small slots alternate by a hash bit.
        fill = colours[0] if i == 0 else colours[(h[3] >> i) & 1]
        parts.append(shape_svg(kind, x, y, s, fill))
    mark = "\n  ".join(parts)
    # Wordmark: starts at x=200, cap height about 52 px, vertically centred on the mark.
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="200" viewBox="0 0 640 200">
  <title>{escape(name)}</title>
  <g transform="translate(20 44)">
  {mark}
  </g>
  <text x="200" y="120" font-family="Helvetica, Arial, sans-serif" font-weight="700" font-size="76" fill="{ANTHRACITE}">{escape(name)}</text>
</svg>
'''


def load_makers(pack):
    path = ROOT / "tools" / "packs" / f"{pack}.py"
    spec = importlib.util.spec_from_file_location(f"pack_{pack}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return [(m["code"], m["name"]) for m in mod.PACK["makers"]]


def build(pack):
    if pack not in PALETTE:
        sys.exit(f"no palette for pack '{pack}'")
    out = ROOT / "packs" / pack / "assets" / "logos"
    out.mkdir(parents=True, exist_ok=True)
    if not shutil.which("rsvg-convert"):
        sys.exit("rsvg-convert not found (brew install librsvg)")
    for code, name in load_makers(pack):
        stem = code.lower()
        svg = out / f"{stem}.svg"
        svg.write_text(logo_svg(pack, code, name), encoding="utf-8")
        subprocess.run(["rsvg-convert", "-w", "512", "-o", str(out / f"{stem}.png"), str(svg)], check=True)
        print(f"  packs/{pack}/assets/logos/{stem}.svg + .png ({name})")


if __name__ == "__main__":
    packs = sys.argv[1:] or sorted(PALETTE)
    for pack in packs:
        build(pack)
