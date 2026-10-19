"""Electrical pack, series 6: hand tools for cables and wires.

Units mm. Hand tools lie flat on the floor (pitch 50) with the jaws towards +X
and the handles towards -X; the pen-shaped tester and the screwdrivers lie
along X. The multimeter stands upright on its back. Grips are dark grey plastic
or a single insulating colour; metal parts are steel. No lettering on models.
"""

import math

DARK = '#2B2E33'
STEEL = '#A9AFB7'
MID = '#7B838F'
LIGHT = '#C9CED6'
RED = '#C94A3A'
SLATE = '#4C6E8F'
BODY = '#4A515C'
LCD = '#B7C9B0'
WINDOW = '#D9F0E6'

FLAT = {'pitch': 50}


def plier(k, hl=115, jl=45, jw=12, gw=26, grip=DARK, jaw=None, dial=False):
    """Flat pliers or cutters lying on the floor: pivot at the origin, jaws towards +X,
    two arms from the pivot, each ending in its own grip, side by side towards -X."""
    if jaw == 'cutter':
        head = [(jl, -jw / 2), (jl, jw / 2), (0, 5), (0, -5)]                             # blunt cutter jaws, flat nose
    else:
        head = [(jl, -jw * 0.2), (jl, jw * 0.2), (jl * 0.6, jw / 2), (0, 5), (0, -5), (jl * 0.6, -jw / 2)]
    k.slab(head, 5, 0, STEEL, metal=1, rough=0.3)                                        # steel jaw head
    for s_ in (-1, 1):
        k.slab([(0, s_ * 3), (0, s_ * 6), (-hl * 0.5, s_ * (gw * 0.5 + 3)), (-hl * 0.5, s_ * (gw * 0.5 - 3))],
               5, 0, STEEL, metal=1, rough=0.3)                                         # arm
        k.slab([(-hl, s_ * gw * 0.5 - gw * 0.25), (-hl, s_ * gw * 0.5 + gw * 0.25),
                (-hl * 0.3, s_ * gw * 0.5 + gw * 0.25), (-hl * 0.3, s_ * gw * 0.5 - gw * 0.25)],
               14, 0, grip, rough=0.5)                                                  # handle
    k.cyl(4, 6, (0, 0, 8), STEEL, verts=24)                                             # pivot bolt
    if jaw == 'crimp':
        k.box((jl * 0.45, jw + 8, 10), (jl * 0.7, 0, 9), MID, bevel=2)                  # stout crimp head
    if dial:
        k.cyl(12, 7, (-hl * 0.6, 0, 17.5), MID)                                         # cable diameter dial


def wire_stripper(k):
    """Manual wire stripper, 160 mm: dark grip, steel jaws with stripping notches, adjusting knob."""
    plier(k, hl=115, jl=45, jw=12, gw=26)
    k.cyl(5, 4, (-40, 0, 19), LIGHT)                                                    # adjusting knob


def auto_stripper(k):
    """Automatic wire stripper, 160 mm: slate-blue grips and a small box mechanism on the handle."""
    plier(k, hl=110, jl=50, jw=12, gw=26, grip=SLATE)
    k.box((34, 14, 10), (-62, 13, 19), BODY, bevel=2)                                   # automatic mechanism on the upper grip


def crimp_tool(k):
    """Ferrule crimping tool, 200 mm: dark grips and a stout steel crimp head at the tip."""
    plier(k, hl=135, jl=65, jw=22, gw=30, jaw='crimp')


def side_cutter(k, hl=115, jl=45):
    """Insulated side cutters: fully red insulated handles, thin steel cutting jaws."""
    plier(k, hl=hl, jl=jl, jw=10, gw=26, grip=RED, jaw='cutter')


YELLOW = '#E8B820'


def vde_side_cutter(k, hl=158, jl=36):
    """VDE side cutters 200 mm, 1000 V, lying flat and closed (checked against real VDE cutters, 2026-10-19):
    a bare chrome steel head with short blunt jaws whose cutting edges meet along the middle, a pivot rivet,
    and two long insulated handles, each a red sleeve with a yellow inlay, and a raised red finger guard
    collar just behind the head. Nothing else: no spring, no stripping notch, no lock."""
    k.slab([(jl, -5), (jl + 3, 0), (jl, 5), (8, 13), (-10, 11), (-10, -11), (8, -13)], 7, 0, STEEL,
           metal=1, rough=0.22, round_=2)                                                 # chrome head, closed jaws
    k.box((jl - 6, 0.8, 7.4), (jl / 2 + 2, 0, 3.5), '#6E747C', metal=1)                   # the line where the two cutting edges meet
    k.cyl(5.5, 8, (0, 0, 3.5), '#8E949C', verts=24, metal=1)                              # pivot rivet
    for s_ in (-1, 1):
        k.slab([(-10, s_ * 2), (-10, s_ * 11), (-24, s_ * 14), (-24, s_ * 2)], 7, 0, STEEL, metal=1, rough=0.3)   # steel arm into the sleeve
        k.slab([(-22, s_ * 1.5), (-22, s_ * 19), (-32, s_ * 19), (-32, s_ * 1.5)], 18, -2, RED, round_=3)      # finger guard collar
        k.slab([(-32, s_ * 2), (-32, s_ * 14), (-hl, s_ * 24), (-hl, s_ * 9)], 13, -1, RED, round_=5)          # red insulated sleeve
        k.slab([(-48, s_ * 5.5), (-48, s_ * 11), (-hl + 14, s_ * 19.5), (-hl + 14, s_ * 13.5)], 13.6, -1.1, YELLOW,
               round_=2.5)                                                                # yellow inlay along the grip


def two_pole_tester(k):
    """Two-pole voltage tester: slim dark pen body, grey finger guard, two steel probes, lit window."""
    k.cyl(10, 120, (0, 0, 10), DARK, rot=(0, 90, 0), bevel=1.5)                         # pen body
    k.cyl(12, 12, (-50, 0, 10), MID, rot=(0, 90, 0), bevel=1)                           # finger guard
    k.box((30, 10, 2), (-25, 0, 20.5), WINDOW, bevel=0.5)                               # indicator window
    for y in (-3, 3):
        k.cyl(1.8, 40, (80, y, 10), STEEL, rot=(0, 90, 0))                              # probe tips


def phase_tester(k):
    """Phase tester in screwdriver form: dark handle with a clear window at the end, steel shank."""
    k.cyl(13, 70, (-55, 0, 13), DARK, rot=(0, 90, 0), bevel=2)                          # handle
    k.cyl(6, 4, (-92, 0, 13), '#9FD8E8', rot=(0, 90, 0))                                # clear window
    k.cyl(4, 6, (-20, 0, 13), MID, rot=(0, 90, 0))                                      # collar
    k.cyl(2.5, 80, (20, 0, 13), STEEL, rot=(0, 90, 0))                                  # shank
    k.cyl(2.5, 10, (65, 0, 13), STEEL, rot=(0, 90, 0), r2=0.8)                          # pointed tip


def multimeter(k):
    """Digital multimeter standing upright: dark housing, LCD, rotary dial, two input sockets at the bottom,
    and a black and a red test lead plugged in, the leads running out and lying on the floor."""
    k.box((90, 40, 180), (0, 0, 90), BODY, bevel=6, rough=0.4)                          # housing
    k.box((52, 1.5, 26), (0, -20.5, 140), LCD, bevel=1)                                 # LCD
    k.cyl(14, 4, (0, -20.5, 90), LIGHT, rot=(90, 0, 0))                                 # rotary dial
    for x in (-25, 25):
        k.box((10, 2, 6), (x, -20.5, 118), MID, bevel=1)                                # buttons
    # One black and one red test lead (2026-10-19): socket ring, plug, lead and probe all in the lead's colour.
    for x, col, dx in ((-18, '#151618', -60), (22, '#C8241C', 60)):
        k.cyl(5.5, 2, (x, -21.5, 14), col, rot=(90, 0, 0))                              # coloured socket ring
        k.cyl(3.4, 18, (x, -31, 14), col, rot=(90, 0, 0))                               # shrouded plug in the socket
        k.cyl(2.2, 12, (x, -41, 8.5), col)                                              # lead down to the floor
        pts = [(x, -41, 2.2), (x + dx * 0.3, -90, 2.2), (x + dx * 0.8, -130, 2.2), (x + dx, -165, 2.2)]
        for a, b in zip(pts, pts[1:]):                                                  # lead on the floor, fanning out
            L = math.dist(a, b); yaw = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            k.cyl(2.2, L, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 2.2), col, rot=(0, 90, yaw))
            k.sphere(2.2, b, col)
        ex, ey = pts[-1][0], pts[-1][1]
        k.cyl(5, 70, (ex, ey - 35, 5), col, rot=(90, 0, 0), bevel=1)                    # probe handle
        k.cyl(6.5, 4, (ex, ey - 72, 5), col, rot=(90, 0, 0))                            # probe finger guard
        k.cyl(1.2, 18, (ex, ey - 83, 5), STEEL, rot=(90, 0, 0), metal=1)                # probe tip


def insulated_screwdrivers(k):
    """Six insulated screwdrivers side by side: dark insulated handles, steel shanks of several lengths."""
    for i in range(6):
        y = -50 + i * 20
        k.cyl(9, 75, (-70, y, 9), DARK, rot=(0, 90, 0), bevel=1.5)                      # handle
        k.cyl(9.5, 4, (-32.5, y, 9), LIGHT, rot=(0, 90, 0))                             # end cap
        shank = 130 - i * 8 - 10
        k.cyl(2.5, shank, (-32.5 + shank / 2, y, 9), STEEL, rot=(0, 90, 0))             # shank
        xe = -32.5 + shank
        if i % 2 == 0:
            k.box((10, 5, 1.4), (xe + 5, y, 9), STEEL, metal=1, rough=0.3)              # slotted blade
        else:
            k.box((10, 1.4, 5), (xe + 5, y, 9), STEEL, metal=1, rough=0.3)              # Phillips tip: cross
            k.box((10, 5, 1.4), (xe + 5, y, 9), STEEL, metal=1, rough=0.3)


def sheath_stripper(k):
    """Cable sheath stripper with a diameter dial: dark grips, steel jaws, round dial on the handle."""
    plier(k, hl=120, jl=45, jw=14, gw=30, dial=True)


def cable_cutter(k):
    """Cable cutter with long levers, 250 mm: dark grips and wide steel jaws."""
    plier(k, hl=180, jl=70, jw=16, gw=34, jaw='cutter')


def cable_knife(k):
    """Cable knife, 180 mm: straight steel blade and a two-shell dark grey handle."""
    k.box((76, 22, 14), (-48, 0, 7), DARK, bevel=4, rough=0.4)                          # handle shells
    k.slab([(-12, -8), (82, -8), (96, 0), (82, 8), (24, 8), (21.66, 2.34), (16, 0), (10.34, 2.34), (8, 8), (-12, 8)],
           2, 0, STEEL, metal=1, rough=0.25)                                              # blade with a round cutout in the spine


SKUS = {
    'DEMO-ELE-6001': (wire_stripper, {}, FLAT),
    'DEMO-ELE-6002': (auto_stripper, {}, FLAT),
    'DEMO-ELE-6003': (crimp_tool, {}, FLAT),
    'DEMO-ELE-6004': (side_cutter, {'hl': 115, 'jl': 45}, FLAT),
    'DEMO-ELE-6005': (vde_side_cutter, {}, FLAT),
    'DEMO-ELE-6006': (two_pole_tester, {}, {'pitch': 40}),
    'DEMO-ELE-6007': (phase_tester, {}, FLAT),
    'DEMO-ELE-6008': (multimeter, {}),
    'DEMO-ELE-6009': (insulated_screwdrivers, {}, FLAT),
    'DEMO-ELE-6010': (sheath_stripper, {}, FLAT),
    'DEMO-ELE-6011': (cable_cutter, {}, FLAT),
    'DEMO-ELE-6012': (cable_knife, {}, FLAT),
}

HINTS = {
    'DEMO-ELE-6001': 'A manual wire stripper about 16 cm long, lying flat on the floor, with two dark grey plastic grips, steel jaws with small stripping notches at the tip and a small light grey adjusting knob near the pivot. The whole tool visible from above. Not a plain plier and not an automatic stripper with a housing on the handle.',
    'DEMO-ELE-6002': 'An automatic wire stripper about 16 cm long, lying flat on the floor, with steel jaws at the tip, two slate-blue plastic grips side by side as on pliers, and a small dark grey box-shaped mechanism sitting on top of the upper grip. The whole tool visible from above. Not a manual stripper without a housing.',
    'DEMO-ELE-6003': 'A crimping tool for wire end ferrules about 20 cm long, lying flat on the floor, with two dark grey plastic grips side by side as on pliers and a stout steel crimp head at the tip with a round crimping die. The whole tool visible from above. Not a cutter and not a stripper; the head is much wider than the jaws of a plier.',
    'DEMO-ELE-6004': 'A pair of side cutters (diagonal cutters), 160 mm long, with red insulated handles: blunt jaws with cutting edges on the jaw sides, flush with one outer face, and no pointed nose. Not long-nose pliers, not needle-nose. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-6005': 'A pair of VDE insulated diagonal side cutters for live work up to 1000 V, 200 mm long, lying flat and closed, seen from above: a short, broad bare polished chrome steel head with a round pivot rivet; the two jaws are short and blunt with smooth sharp bevelled cutting edges that meet in one straight line along the middle, angled slightly to one side like real diagonal cutters. The jaws have NO serrations, NO gripping teeth, NO ridges and no flat gripping surface: it cuts wire, it does not grip. Two long insulated handles, each a moulded two-colour insulating sleeve, red with a yellow inlay along the grip, with a raised red finger guard collar just behind the head. Exactly two handles and one head; no spring, no lock, no stripping notch, no pointed nose. Not combination pliers, not long-nose pliers. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-6006': 'A two-pole voltage tester about 13 cm long, lying on the floor: a slim pen-shaped dark grey plastic body with a grey finger guard, two short steel probe tips at one end and a small lit indicator window on top. The whole tool visible. Not a screwdriver and not a multimeter.',
    'DEMO-ELE-6007': 'A phase tester in screwdriver form about 20 cm long, lying flat on the floor: a dark grey plastic handle with a clear round window at the end, a steel shank and a small pointed tip. The whole tool visible from above. Not a multimeter and not a plain screwdriver without a window.',
    'DEMO-ELE-6008': 'A handheld digital multimeter in dark grey rubberised plastic, standing upright: a large rotary dial in the middle of the front, a blank grey LCD window at the top, two input sockets at the bottom, and exactly two test leads plugged in: the left lead is BLACK (black plug, black cable, black probe) and the right lead is RED (red plug, red cable, red probe). Both leads run forward onto the floor and end in pointed test probes with finger guards. One black and one red, never two of the same colour. Plain front panel with no printed labels and no markings on the dial. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-6009': 'A set of six insulated screwdrivers lying side by side, evenly spaced: each has a thick dark grey insulated handle with a light grey end cap and a steel shaft with a real blade tip, alternating slotted (flat blade) and Phillips (cross tip). Six screwdrivers, no awls, no pointed probes. The whole set visible from above. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-6010': 'A cable sheath stripper about 16 cm long, lying flat: dark grey plastic grips, serrated steel jaws, and a round grey dial on the upper handle for setting the cable diameter. Clean smooth grips with no lines, arrows or marks. The whole tool visible from above. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-6011': 'A cable cutter, 250 mm long, lying flat: long dark grey insulated grips and wide steel shear jaws, blunt, with the cutting edges meeting in a V next to the pivot. Clean moulded surfaces with no marking at all. The whole tool visible from above. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-6012': 'A cable knife, 180 mm long, lying flat: a straight steel blade with a round cutout in the back edge near the handle and a pointed tip, and a dark grey handle made of two plastic shells. Plain blade, no emblem, no engraving. The whole knife visible from above. No text, no numbers, no logos, no labels anywhere on the product.',
}
