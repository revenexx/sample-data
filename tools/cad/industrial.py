"""STEP models for the industrial pack, built from our own dimensions.

Development tool only (the STEP files are committed; seed.sh never runs it):

    pip install cadquery
    python tools/cad/industrial.py

The parts are simplified on purpose: correct outer dimensions, no modelled
thread. That is enough for a 3D preview and AR at real size.
"""
import math
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402

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


def diamond_disc(outer=230.0, thickness=2.6, bore=22.23, rim=10.0, segments=16):
    """Segmented diamond cutting disc: steel core 1.8 mm, segment rim `rim` mm wide at full thickness, slots between segments."""
    core = cq.Workplane("XY").workplane(offset=(thickness - 1.8) / 2).circle(outer / 2).circle(bore / 2).extrude(1.8)
    ring = cq.Workplane("XY").circle(outer / 2).circle(outer / 2 - rim).extrude(thickness)
    for k in range(segments):
        slot = cq.Workplane("XY").box(rim * 0.8, 3.0, thickness, centered=(False, True, False)).translate((outer / 2 - rim * 0.8, 0, 0))
        ring = ring.cut(slot.rotate((0, 0, 0), (0, 0, 1), 360.0 * k / segments))
    return core.union(ring)


# (builder, expected bounding box x, y, z in mm; compared sorted, so the axis order does not matter)
# Dimensions: ISO 4017 / ISO 4032 / ISO 7089 / ISO 4762 / ISO 4029 / ISO 7045 / ISO 7049 / DIN 557 tables.
MORE = {
    "demo-ind-2004-wood-screw-3-5x30": (lambda: lib.countersunk_screw(3.5, 30, 7.0), (7.0, 7.0, 30)),
    "demo-ind-2005-wood-screw-5x60": (lambda: lib.countersunk_screw(5.0, 60, 10.0), (10.0, 10.0, 60)),
    "demo-ind-2006-wood-screw-5x80-stainless": (lambda: lib.countersunk_screw(5.0, 80, 10.0), (10.0, 10.0, 80)),
    "demo-ind-2007-hex-bolt-m6x30": (lambda: lib.hex_bolt(6, 30, 10.0, 4.0), (11.547, 10.0, 34.0)),
    "demo-ind-2008-hex-bolt-m10x60": (lambda: lib.hex_bolt(10, 60, 16.0, 6.4), (18.475, 16.0, 66.4)),
    "demo-ind-2009-hex-nut-m8": (lambda: lib.hex_nut(8, 13.0, 6.8), (15.011, 13.0, 6.8)),
    "demo-ind-2010-hex-nut-m6": (lambda: lib.hex_nut(6, 10.0, 5.2), (11.547, 10.0, 5.2)),
    "demo-ind-2011-flat-washer-m8": (lambda: lib.washer(8.4, 16.0, 1.6), (16.0, 16.0, 1.6)),
    "demo-ind-2012-threaded-rod-m8x1000": (lambda: lib.rod(8.0, 1000.0), (8.0, 8.0, 1000.0)),
    "demo-ind-2013-expansion-plug-8x40": (lambda: lib.plug(8.0, 40.0, 11.0), (11.0, 11.0, 40.0)),
    "demo-ind-2014-cable-tie-200x3-6": (lambda: lib.cable_tie(200.0, 3.6, 1.0, (8.5, 5.5, 3.5)), (200.0, 5.5, 3.5)),
    "demo-ind-2015-wire-nail-2-8x60": (lambda: lib.nail(2.8, 60.0, 5.5), (5.5, 5.5, 60.0)),
    "demo-ind-2016-grub-screw-m6x20": (lambda: lib.grub_screw(6.0, 20.0, 3.0), (6.0, 6.0, 20.0)),
    "demo-ind-2017-cheese-head-screw-m5x16": (lambda: lib.cheese_screw(5.0, 16.0, 8.5, 5.0, 4.0), (8.5, 8.5, 21.0)),
    "demo-ind-2018-pan-head-screw-m4x12": (lambda: lib.pan_screw(4.0, 12.0, 8.0, 3.1), (8.0, 8.0, 15.1)),
    "demo-ind-2019-sheet-metal-screw-4-2x19": (lambda: lib.pan_screw(4.2, 19.0, 8.0, 3.1, point_tip=1.5), (8.0, 8.0, 22.1)),
    "demo-ind-2021-square-nut-m10": (lambda: lib.square_nut(10, 17.0, 8.0), (17.0, 17.0, 8.0)),
    "demo-ind-2022-hex-bolt-m12x80": (lambda: lib.hex_bolt(12, 80, 18.0, 7.5), (20.785, 18.0, 87.5)),
    "demo-ind-2023-flat-washer-m10": (lambda: lib.washer(10.5, 20.0, 2.0), (20.0, 20.0, 2.0)),
    "demo-ind-5001-flap-disc-115-p80": (lambda: lib.flap_disc(115.0, 22.23, 13.0), (115.0, 115.0, 13.0)),
    "demo-ind-5002-flap-disc-115-p120": (lambda: lib.flap_disc(115.0, 22.23, 13.0), (115.0, 115.0, 13.0)),
    "demo-ind-5007-cutting-disc-115-inox": (lambda: lib.disc(115.0, 1.0), (115.0, 115.0, 1.0)),
    "demo-ind-5008-diamond-cutting-disc-230": (lambda: diamond_disc(), (230.0, 230.0, 2.6)),
}

PARTS = {
    "demo-ind-2002-hex-bolt-m8x40": hex_bolt,
    "demo-ind-2001-wood-screw-4x40": wood_screw,
    "demo-ind-2003-cutting-disc-125": cutting_disc,
}
EXPECT = {k: v[1] for k, v in MORE.items()}
EXPECT.update({"demo-ind-2002-hex-bolt-m8x40": (15.011, 13.0, 45.3), "demo-ind-2001-wood-screw-4x40": (8.0, 8.0, 40.0),
               "demo-ind-2003-cutting-disc-125": (125.0, 125.0, 1.0)})
PARTS.update({k: v[0] for k, v in MORE.items()})

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in PARTS.items():
        path = OUT / f"{name}.step"
        lib.export_step(build(), path)
        print(f"  {path.name}")
