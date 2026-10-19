"""STEP models for the electrical pack, built from our own dimensions.

Development tool only (the STEP files are committed; the seeder never runs it):

    pip install cadquery
    python tools/cad/electrical.py

The parts are simplified on purpose: correct outer dimensions, no wiring,
no terminals. That is enough for a 3D preview and AR at real size.
"""
import sys
from pathlib import Path

import cadquery as cq

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lib  # noqa: E402

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


def surface_switch(w=80.0, h=45.0, rocker=48.0, rocker_h=6.0):
    """Surface-mounted IP44 switch: closed block with a rocker on the front (front at +Z)."""
    b = cq.Workplane("XY").box(w, w, h, centered=(True, True, False)).edges("|Z").fillet(6.0)
    r = cq.Workplane("XY").box(rocker, rocker, rocker_h, centered=(True, True, False)).translate((0, 0, h)).edges(">Z").fillet(2.0)
    return b.union(r)


def usb_socket():
    """Schuko flush socket outlet with two USB charging ports (rectangular openings left and right of the round socket)."""
    out = lib.sockets(1)
    for y in (-28.0, 28.0):
        out = out.cut(cq.Workplane("XY").workplane(offset=2.0).center(0, y).rect(14.0, 7.0).extrude(2.0))
    return out


def gland_part(thread, af, total, thread_len, bore):
    return lambda: lib.gland(thread, af, total, thread_len, bore, hex_h=7.0)


def din(modules, **kw):
    return lambda: lib.din_device(modules, **kw)


HEX = 1 / 0.8660254  # across corners per across flats
M = lib.MODULE
# (builder, expected bounding box). DIN devices: width = modules x 17.5 (EN 60715 / DIN 43880 module), 90 mm high, 69 mm deep.
# Distribution boards, boxes, trunking and housings use typical catalogue sizes (see the report), the rest EN/DIN tables.
MORE = {
    "demo-ele-2001-light-switch-flush-single-pole": (lambda: lib.device_insert(), (55.0, 55.0, 37.0)),
    "demo-ele-2005-two-way-switch-flush": (lambda: lib.device_insert(), (55.0, 55.0, 37.0)),
    "demo-ele-2006-intermediate-switch-flush": (lambda: lib.device_insert(), (55.0, 55.0, 37.0)),
    "demo-ele-2008-light-switch-flush-double-pole": (lambda: lib.device_insert(), (55.0, 55.0, 37.0)),
    "demo-ele-2007-doorbell-push-button-flush": (lambda: lib.device_insert(knob_d=20.0, rocker_h=5.0), (55.0, 55.0, 36.0)),
    "demo-ele-2015-rotary-dimmer-flush": (lambda: lib.device_insert(knob_d=36.0, rocker_h=12.0), (55.0, 55.0, 43.0)),
    "demo-ele-2018-blind-control-push-button-flush": (lambda: lib.device_insert(rockers=2), (55.0, 55.0, 37.0)),
    "demo-ele-2009-cover-frame-1-gang": (lambda: lib.cover_frame(1), (80.5, 80.5, 9.0)),
    "demo-ele-2002-cover-frame-2-gang": (lambda: lib.cover_frame(2), (151.5, 80.5, 9.0)),
    "demo-ele-2010-cover-frame-3-gang": (lambda: lib.cover_frame(3), (222.5, 80.5, 9.0)),
    "demo-ele-2011-socket-outlet-surface-ip44": (lambda: lib.surface_socket(80.0, 50.0), (80.0, 80.0, 50.0)),
    "demo-ele-2012-double-socket-outlet-flush": (lambda: lib.sockets(2), (151.0, 80.0, 40.0)),
    "demo-ele-2013-socket-outlet-usb-flush": (usb_socket, (80.0, 80.0, 40.0)),
    "demo-ele-2017-light-switch-surface-ip44": (surface_switch, (80.0, 80.0, 51.0)),
    "demo-ele-4001-circuit-breaker-1p-b10": (din(1, depth=69.0), (M, 90.0, 69.0)),
    "demo-ele-4002-circuit-breaker-1p-b16": (din(1, depth=69.0), (M, 90.0, 69.0)),
    "demo-ele-4003-circuit-breaker-1p-c16": (din(1, depth=69.0), (M, 90.0, 69.0)),
    "demo-ele-4004-circuit-breaker-3p-b16": (din(3, depth=69.0), (3 * M, 90.0, 69.0)),
    "demo-ele-4005-circuit-breaker-3p-b32": (din(3, depth=69.0), (3 * M, 90.0, 69.0)),
    "demo-ele-4006-rcd-2p-40a-30ma": (din(2, poles=1, depth=69.0, test_button=True), (2 * M, 90.0, 69.0)),
    "demo-ele-4007-rcd-4p-40a-30ma": (din(4, poles=1, depth=69.0, test_button=True), (4 * M, 90.0, 69.0)),
    "demo-ele-4008-rcd-4p-63a-300ma": (din(4, poles=1, depth=69.0, test_button=True), (4 * M, 90.0, 69.0)),
    "demo-ele-4009-rcbo-1pn-b16-30ma": (din(2, poles=1, depth=69.0, test_button=True), (2 * M, 90.0, 69.0)),
    "demo-ele-4010-surge-protective-device-type-2": (din(2, depth=69.0, lever=False), (2 * M, 90.0, 69.0)),
    "demo-ele-4014-main-switch-3p-63a": (din(3, poles=1, depth=69.0), (3 * M, 90.0, 69.0)),
    "demo-ele-4011-distribution-board-surface-12": (lambda: lib.din_enclosure(240.0, 192.0, 68.0), (240.0, 192.0, 68.0)),
    "demo-ele-4012-distribution-board-surface-24": (lambda: lib.din_enclosure(285.0, 419.0, 118.0), (285.0, 419.0, 118.0)),
    "demo-ele-4013-distribution-board-flush-24": (lambda: lib.din_enclosure(255.0, 390.0, 100.0), (255.0, 390.0, 100.0)),
    "demo-ele-5001-flush-box-d60": (lambda: lib.cup_box(60.0, 60.0), (60.0, 60.0, 60.0)),
    "demo-ele-5002-cavity-wall-box-d68": (lambda: lib.cup_box(68.0, 42.0), (68.0, 68.0, 42.0)),
    "demo-ele-5003-surface-housing-1-gang-ip44": (lambda: lib.surface_housing(80.0, 80.0, 45.0), (80.0, 80.0, 45.0)),
    "demo-ele-5004-cable-tie-100x2-5": (lambda: lib.cable_tie(100.0, 2.5, 0.9, (5.5, 3.8, 2.6)), (100.0, 3.8, 2.6)),
    "demo-ele-5005-cable-tie-200x3-6": (lambda: lib.cable_tie(200.0, 3.6, 1.0, (8.5, 5.5, 3.5)), (200.0, 5.5, 3.5)),
    "demo-ele-5006-cable-tie-300x4-8": (lambda: lib.cable_tie(300.0, 4.8, 1.3, (9.5, 6.5, 4.5)), (300.0, 6.5, 4.5)),
    "demo-ele-5007-cable-trunking-40x25-2m": (lambda: lib.trunking(40.0, 25.0), (40.0, 25.0, 2000.0)),
    "demo-ele-5008-cable-trunking-60x40-2m": (lambda: lib.trunking(60.0, 40.0), (60.0, 40.0, 2000.0)),
    "demo-ele-5012-cable-gland-m16": (gland_part(16.0, 22.0, 30.0, 8.0, 10.0), (22.0 * HEX, 22.0, 30.0)),
    "demo-ele-5013-cable-gland-m20": (gland_part(20.0, 24.0, 33.0, 10.0, 13.0), (24.0 * HEX, 24.0, 33.0)),
    "demo-ele-5014-cable-gland-m25": (gland_part(25.0, 30.0, 38.0, 10.0, 18.0), (30.0 * HEX, 30.0, 38.0)),
    "demo-ele-5015-terminal-block-1-5mm2": (lambda: lib.terminal_block(4.2, wire=1.5), (4.2, 42.0, 36.0)),
    "demo-ele-5016-terminal-block-2-5mm2": (lambda: lib.terminal_block(5.2, wire=2.5), (5.2, 42.0, 36.0)),
    "demo-ele-5017-terminal-block-4mm2": (lambda: lib.terminal_block(6.2, wire=4.0), (6.2, 42.0, 36.0)),
    "demo-ele-5018-terminal-block-6mm2": (lambda: lib.terminal_block(8.2, wire=6.0), (8.2, 42.0, 36.0)),
    "demo-ele-5019-wire-ferrule-0-75mm2": (lambda: lib.ferrule(1.6, 1.2, 8.0, 2.8, 6.0), (2.8, 2.8, 14.0)),
    "demo-ele-5020-wire-ferrule-1-5mm2": (lambda: lib.ferrule(2.2, 1.7, 8.0, 3.5, 6.0), (3.5, 3.5, 14.0)),
    "demo-ele-5021-wire-ferrule-2-5mm2": (lambda: lib.ferrule(2.8, 2.3, 8.0, 4.2, 6.0), (4.2, 4.2, 14.0)),
    "demo-ele-5023-wire-ferrule-4mm2": (lambda: lib.ferrule(3.4, 2.9, 10.0, 4.8, 7.0), (4.8, 4.8, 17.0)),
    "demo-ele-5022-connector-terminal-5-pole": (lambda: lib.terminal_strip(5, 6.0, 12.0, 10.0), (30.0, 12.0, 10.8)),
}

PARTS = {
    "demo-ele-2004-junction-box-ip55": junction_box,
    "demo-ele-3001-led-panel-62x62": led_panel,
    "demo-ele-2003-socket-outlet": socket_outlet,
}
EXPECT = {k: v[1] for k, v in MORE.items()}
EXPECT.update({"demo-ele-2004-junction-box-ip55": (100.0, 100.0, 55.0), "demo-ele-3001-led-panel-62x62": (620.0, 620.0, 12.0),
               "demo-ele-2003-socket-outlet": (80.0, 80.0, 40.0)})
PARTS.update({k: v[0] for k, v in MORE.items()})

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in PARTS.items():
        path = OUT / f"{name}.step"
        lib.export_step(build(), path)
        print(f"  {path.name}")
