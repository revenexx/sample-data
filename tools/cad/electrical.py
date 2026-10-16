"""STEP models for the electrical pack, built from our own dimensions.

Development tool only (the STEP files are committed; seed.sh never runs it):

    pip install cadquery
    python tools/cad/electrical.py

The parts are simplified on purpose: correct outer dimensions, no wiring,
no terminals. That is enough for a 3D preview and AR at real size.
"""
from pathlib import Path

import cadquery as cq

OUT = Path(__file__).resolve().parents[2] / "packs" / "electrical" / "assets" / "cad"


def junction_box(w=100.0, d=100.0, h=55.0, wall=3.0):
    """Surface-mounted junction box IP55, 100 x 100 x 55 mm: a shell, open at the top."""
    body = cq.Workplane("XY").rect(w, d).extrude(h).edges("|Z").fillet(8.0)
    return body.faces(">Z").shell(-wall)


def led_panel(size=620.0, thickness=12.0, frame=20.0):
    """Flat LED ceiling panel 620 x 620 x 12 mm: a solid frame with a light face inset."""
    panel = cq.Workplane("XY").rect(size, size).extrude(thickness).edges("|Z").fillet(6.0)
    recess = cq.Workplane("XY").workplane(offset=thickness - 2.0).rect(size - 2 * frame, size - 2 * frame).extrude(3.0)
    return panel.cut(recess)


def socket_outlet(w=80.0, depth=36.0, plate=4.0):
    """Schuko socket outlet 80 x 80 mm, 40 mm deep (4 mm plate, 36 mm body): plate with contact holes, body behind."""
    face = cq.Workplane("XY").rect(w, w).extrude(plate).edges("|Z").fillet(7.0)
    body = cq.Workplane("XY").workplane(offset=-depth).rect(w - 12, w - 12).extrude(depth).edges("|Z").fillet(4.0)
    holes = (cq.Workplane("XY").workplane(offset=-1.0).pushPoints([(-20.0, 10.0), (20.0, 10.0), (0.0, -2.0)])
             .circle(4.0).extrude(plate + 2.0))
    return face.union(body).cut(holes)


PARTS = {
    "demo-ele-2004-junction-box-ip55": junction_box,
    "demo-ele-3001-led-panel-62x62": led_panel,
    "demo-ele-2003-socket-outlet": socket_outlet,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in PARTS.items():
        path = OUT / f"{name}.step"
        cq.exporters.export(build(), str(path))
        print(f"  {path.name}")
