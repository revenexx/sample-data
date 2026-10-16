"""STEP models for the industrial pack, built from our own dimensions.

Development tool only (the STEP files are committed; seed.sh never runs it):

    pip install cadquery
    python tools/cad/industrial.py

The parts are simplified on purpose: correct outer dimensions, no modelled
thread. That is enough for a 3D preview and AR at real size.
"""
import math
from pathlib import Path

import cadquery as cq

OUT = Path(__file__).resolve().parents[2] / "packs" / "industrial" / "assets" / "cad"


def hex_bolt(d=8.0, length=40.0, across_flats=13.0, head_h=5.3):
    """ISO 4017-style hex bolt M8 x 40 (sizes per the standard's table)."""
    head = cq.Workplane("XY").polygon(6, across_flats / math.cos(math.pi / 6)).extrude(head_h)
    head = head.edges(">Z or <Z").chamfer(0.6)
    shank = cq.Workplane("XY").workplane(offset=head_h).circle(d / 2).extrude(length)
    return head.union(shank).faces(">Z").edges().chamfer(0.8)


def wood_screw(d=4.0, length=40.0, head_d=8.0):
    """Countersunk wood screw 4 x 40: 90 degree head, shank, conical tip."""
    head_h = (head_d - d) / 2  # a 90 degree countersink
    head = cq.Workplane("XY").circle(head_d / 2).workplane(offset=head_h).circle(d / 2).loft()
    tip = 4.0
    shank = cq.Workplane("XY").workplane(offset=head_h).circle(d / 2).extrude(length - head_h - tip)
    point = (cq.Workplane("XY").workplane(offset=length - tip).circle(d / 2)
             .workplane(offset=tip).circle(0.2).loft())
    drive = cq.Workplane("XY").rect(2.2, 2.2).extrude(1.5)  # a simple square recess
    return head.union(shank).union(point).cut(drive)


def cutting_disc(outer=125.0, thickness=1.0, bore=22.23):
    """Flat cutting disc 125 x 1.0 x 22.23."""
    return cq.Workplane("XY").circle(outer / 2).circle(bore / 2).extrude(thickness)


PARTS = {
    "demo-ind-2002-hex-bolt-m8x40": hex_bolt,
    "demo-ind-2001-wood-screw-4x40": wood_screw,
    "demo-ind-2003-cutting-disc-125": cutting_disc,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in PARTS.items():
        path = OUT / f"{name}.step"
        cq.exporters.export(build(), str(path))
        print(f"  {path.name}")
