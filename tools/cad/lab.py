"""STEP models for the lab pack, built from our own dimensions.

Development tool only (the STEP files are committed; seed.sh never runs it):

    pip install cadquery
    python tools/cad/lab.py

Each part is a revolved profile along Z (origin at the tip or orifice, the
open end at the top). Outer dimensions match the technical drawings; the
tubes are solid, the pipette tip is hollow. No threads, no text.
"""
from pathlib import Path

import cadquery as cq

OUT = Path(__file__).resolve().parents[2] / "packs" / "lab" / "assets" / "cad"


def revolve(profile):
    """Revolve an (r, z) profile given as a closed polyline around the Z axis."""
    return cq.Workplane("XZ").polyline(profile).close().revolve(360, (0, 0, 0), (0, 1, 0))


def microcentrifuge_tube_1_5ml():
    """1.5 ml tube: length 38.6, body 10.4, cap 11.4 x 7.0, conical tip 2.4 wide."""
    return revolve([
        (0, 0), (1.2, 0),        # flat tip, Ø 2.4
        (5.2, 8.0),              # 8.0 cone up to the body
        (5.2, 31.6),             # body Ø 10.4
        (5.7, 31.6), (5.7, 38.6),  # cap Ø 11.4, 7.0 high
        (0, 38.6),
    ])


def centrifuge_tube_50ml():
    """50 ml tube: length 115, body 28, cap 30 x 15, conical tip 10 wide."""
    return revolve([
        (0, 0), (5.0, 0),        # flat tip, Ø 10
        (14.0, 20.0),            # 20 cone up to the body
        (14.0, 100.0),           # body Ø 28
        (15.0, 100.0), (15.0, 115.0),  # cap Ø 30, 15 high
        (0, 115.0),
    ])


def pipette_tip_200ul():
    """200 µl tip: length 53, collar Ø 7.0, conical body to a 1.0 orifice, hollow (0.4 wall)."""
    outer = revolve([(0, 0), (0.5, 0), (3.5, 39.0), (3.5, 53.0), (0, 53.0)])
    inner = revolve([(0, -1.0), (0.1, -1.0), (3.1, 39.0), (3.1, 54.0), (0, 54.0)])
    return outer.cut(inner)


PARTS = {
    "demo-lab-3001-microcentrifuge-tube-1-5ml": microcentrifuge_tube_1_5ml,
    "demo-lab-3002-centrifuge-tube-50ml": centrifuge_tube_50ml,
    "demo-lab-2002-pipette-tip-200ul": pipette_tip_200ul,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in PARTS.items():
        path = OUT / f"{name}.step"
        cq.exporters.export(build(), str(path))
        bb = build().val().BoundingBox()
        print(f"  {path.name}  x {bb.xlen:.2f}  y {bb.ylen:.2f}  z {bb.zlen:.2f}")
