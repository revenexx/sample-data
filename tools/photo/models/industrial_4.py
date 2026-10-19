"""Industrial pack, series 4: hand tools (DEMO-BRAKKWERK).

Grips are burgundy (#7A1F2B) or anthracite (#2F343C); steel parts are chrome or
dark steel; wooden handles are beech. Most tools lie flat on the floor, seen from
above (pitch 50). Units mm; products stand on z=0 with the front facing -Y.
"""
import math

BURG = '#7A1F2B'
ANTH = '#2F343C'
CHROME = '#CFD3D8'
DSTEEL = '#5A616B'
BEECH = '#D9B88A'
KEY = '#26282C'      # black oxide steel


def rot_pt(x, y, a):
    r = math.radians(a)
    return (x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r))


def rot_pts(pts, a):
    return [rot_pt(x, y, a) for x, y in pts]


def screwdriver_set(k):
    """Six screwdrivers lying side by side, handles burgundy and anthracite alternating."""
    for i, r in enumerate((10, 9.5, 9, 9, 8.5, 8.5)):
        y = -75 + i * 30                                                                  # six rows, clearly apart
        col = BURG if i % 2 == 0 else ANTH
        k.cyl(r, 90, (-40, y, r), col, rot=(0, 90, 0), verts=40, bevel=1.5, rough=0.4)   # handle
        k.cyl(2.6, 115, (50, y, r), CHROME, rot=(0, 90, 0), metal=1, rough=0.2)           # shaft
        if i % 2 == 0:                                                                    # slotted tip
            k.box((4, 9, 1.2), (110, y, r), CHROME, metal=1, rough=0.2)
        else:                                                                             # cross tip
            k.box((4, 7, 1.2), (110, y, r), CHROME, metal=1, rough=0.2)
            k.box((4, 1.2, 7), (110, y, r), CHROME, metal=1, rough=0.2)


def _socket_case(k, sizes, cols, pitch, rfn):
    rows = -(-len(sizes) // cols)
    W, D = cols * pitch + 30, rows * pitch + 30
    k.box((W, D, 24), (0, 0, 12), ANTH, bevel=4, rough=0.5)                              # case base
    k.box((W - 14, D - 14, 3), (0, 0, 25.5), '#3B414B', bevel=1, rough=0.5)              # insert tray
    for i, s in enumerate(sizes):
        x = (i % cols - (cols - 1) / 2) * pitch
        y = ((rows - 1) / 2 - i // cols) * pitch
        k.cyl(rfn(s), 20, (x, y, 27 + 10), CHROME, verts=6, metal=1, rough=0.2, bevel=1)  # socket
    k.box((36, 5, 9), (0, -D / 2 - 2, 18), BURG, bevel=2)                                # latch
    return W, D


def socket_set_quarter(k):
    """1/4 inch socket set, 26 hex sockets in an anthracite plastic case."""
    sizes = [4 + 0.5 * i for i in range(19)] + [6, 7, 8, 9, 10, 11, 12]
    _socket_case(k, sizes, 7, 26, lambda s: s / 2 + 3)


def socket_set_half(k):
    """1/2 inch socket set, 20 pieces: 18 sockets in the case, an extension bar and a ratchet handle beside it."""
    sizes = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 27, 30, 32, 34, 36]   # 18 sockets
    W, D = _socket_case(k, sizes, 6, 46, lambda s: s / 2 + 4)
    k.cyl(6, 125, (-30, -D / 2 - 26, 6), CHROME, rot=(0, 90, 0), metal=1, rough=0.2)     # extension bar
    k.cyl(20, 18, (-W / 2 + 60, -D / 2 - 80, 9), CHROME, metal=1, rough=0.25)              # ratchet head
    k.box((12.7, 12.7, 12), (-W / 2 + 60, -D / 2 - 80, 24), CHROME, metal=1, rough=0.25)   # 1/2 drive
    k.cyl(11, 130, (-W / 2 + 145, -D / 2 - 80, 12), BURG, rot=(0, 90, 0), bevel=2, rough=0.5)  # grip, starts at the ratchet head


def spanner_set(k):
    """Eight double open-end spanners 8 to 19 mm, chrome-plated, lying side by side, parallel.
    Each one flat outline: a C-shaped round head at both ends (the open jaw, a straight slot of the
    nut size, angled 15 degrees) joined by a slim shank."""
    import math
    y = -120

    def head(cx, cy, R, slot, ang, direction):
        """Outline of a round head with a slot opening towards `direction` (+1 right, -1 left)."""
        t0 = math.radians(ang) + (0 if direction > 0 else math.pi)
        half = math.asin(min(0.95, slot / 2 / R))
        pts = []
        for i in range(41):                                     # outer arc, the long way round
            t = t0 + half + (2 * math.pi - 2 * half) * i / 40
            pts.append((cx + R * math.cos(t), cy + R * math.sin(t)))
        depth = R * 0.95
        ux, uy = math.cos(t0), math.sin(t0)
        nx, ny = -uy, ux
        mx, my = cx + ux * (R - depth), cy + uy * (R - depth)
        pts += [(mx - nx * slot / 2, my - ny * slot / 2), (mx + nx * slot / 2, my + ny * slot / 2)]
        return pts

    for i, size in enumerate((8, 10, 11, 13, 14, 16, 17, 19)):
        big, small = size + 1, size
        L = 140 + 9 * i
        R1, R2 = big * 1.15, small * 1.15
        sw = small * 0.55 + 3
        k.slab([(-L / 2 + R1 * 0.6, y - sw / 2), (L / 2 - R2 * 0.6, y - sw / 2 * 0.8),
                (L / 2 - R2 * 0.6, y + sw / 2 * 0.8), (-L / 2 + R1 * 0.6, y + sw / 2)], 4, 0, CHROME, metal=1, rough=0.2)  # shank
        k.slab(head(-L / 2, y, R1, big * 1.02, 15, -1), 4.5, 0, CHROME, metal=1, rough=0.2)                         # jaw, larger size
        k.slab(head(L / 2, y, R2, small * 1.02, -15, 1), 4.5, 0, CHROME, metal=1, rough=0.2)                         # jaw, smaller size
        y += 2 * R1 + 6


def pipe_wrench(k):
    """Pipe wrench 250 mm: serrated jaw head at one end, long steel handle with a grip sleeve."""
    k.slab([(-40, -12), (-40, 12), (210, 8), (210, -8)], 12, 0, DSTEEL, metal=0.8, rough=0.35)
    k.cyl(9, 130, (130, 0, 9), BURG, rot=(0, 90, 0), bevel=2, rough=0.5)                  # grip sleeve
    k.box((90, 44, 22), (-75, 0, 11), DSTEEL, bevel=4, metal=0.8, rough=0.35)             # head
    k.box((34, 22, 26), (-115, -6, 13), CHROME, bevel=1, metal=1, rough=0.25)               # fixed jaw
    k.box((34, 14, 24), (-115, 24, 12), DSTEEL, bevel=1, metal=0.8, rough=0.35)           # adjustable jaw
    k.cyl(6, 26, (-75, 0, 26), DSTEEL, metal=0.8, rough=0.35)                             # pivot pin


def _plier(k, jaw, grip, w_jaw, w_grip, ang, col_a, col_b, gr_r, thick=5, teeth=False):
    """Two crossed arms on a pivot at the origin; grips on each arm (colours col_a / col_b)."""
    for sgn, col, z0 in ((1, col_a, 0), (-1, col_b, thick + 1)):
        arm = [(-jaw, -w_jaw / 2), (-jaw, w_jaw / 2), (0, w_jaw * 0.45), (grip, w_grip / 2),
               (grip, -w_grip / 2), (0, -w_jaw * 0.45)]
        k.slab(rot_pts(arm, sgn * ang), thick, z0, CHROME, metal=1, rough=0.25)
        cx, cy = rot_pt((8 + grip) / 2, 0, sgn * ang)
        k.cyl(gr_r, grip - 8, (cx, cy, z0 + thick + gr_r - 1), col, rot=(0, 90, sgn * ang),
              bevel=2, rough=0.5)
        if teeth:
            tx, ty = rot_pt(-jaw * 0.6, 0, sgn * ang)
            k.box((jaw * 0.5, w_jaw * 0.8, 1.5), (tx, ty, z0 + thick + 0.8), DSTEEL, rot=(0, 0, sgn * ang))
    k.cyl(3, 9, (0, 0, thick + 0.5), DSTEEL, metal=0.8, rough=0.3)                           # pivot rivet


def combination_pliers(k):
    """Combination pliers 200 mm: flat jaws with grips, one grip burgundy and one anthracite."""
    _plier(k, 40, 105, 20, 16, 7, BURG, ANTH, 8.5, teeth=True)


def side_cutters(k):
    """Side cutters 160 mm: short cutting jaws, plastic-coated grips in burgundy and anthracite."""
    _plier(k, 22, 92, 12, 15, 6, BURG, BURG, 8)
    for sgn in (-1, 1):
        tx, ty = rot_pt(-22, 0, sgn * 6)
        k.box((3, 10, 2), (tx, ty, 6.5), DSTEEL, rot=(0, 0, sgn * 6))                 # cutting edges at the joint


def water_pump_pliers(k):
    """Water pump pliers 250 mm: long joint with an adjustable tongue, long grips."""
    _plier(k, 40, 150, 26, 18, 5, ANTH, BURG, 9.5, teeth=True)
    for i in range(4):
        k.box((20, 14, 2), (50 + i * 8, 0, 9 + i * 0.6), DSTEEL, rot=(0, 0, 5))           # adjusting slots on the lower arm


def engineers_hammer(k):
    """Engineer's hammer 500 g (DIN 1041 type) lying on its side: a steel head about 100 mm long set
    across the end of the handle, a flat square striking face at one end and a wedge-shaped cross peen
    at the other, on a 300 mm beech handle that passes through the head."""
    k.slab([(-12, 38), (12, 38), (12, -30), (2.5, -62), (-2.5, -62), (-12, -30)], 25, 0, DSTEEL,
           round_=1.5, metal=0.85, rough=0.3)                                                # head across the handle: face +Y, peen -Y
    k.box((26, 4, 27), (0, 40, 12.5), DSTEEL, bevel=1.2, metal=0.9, rough=0.2)               # striking face, polished
    k.cyl(12, 300, (-150, 0, 12.5), BEECH, rot=(0, 90, 0), verts=40, bevel=2, rough=0.55)   # beech handle
    k.cyl(12.5, 10, (0, 0, 12.5), BEECH, rot=(0, 90, 0), verts=40, rough=0.55)              # handle end in the eye


def rubber_mallet(k):
    """Rubber mallet 500 g: round plastic head across the handle, burgundy grip."""
    k.cyl(13, 200, (-20, 0, 13), BURG, rot=(0, 90, 0), bevel=2, rough=0.5)                 # grip, ends inside the head
    k.cyl(24, 80, (80, 0, 24), ANTH, rot=(90, 0, 0), bevel=3, rough=0.4)                   # head


def flat_file(k):
    """Flat file 200 mm, cut 2: long steel blade tapering to a tip, dark tang handle."""
    k.slab([(-100, 0), (-92, -9), (70, -10), (70, 10), (-92, 9)], 4, 0, CHROME, metal=1, rough=0.3)
    for i in range(34):                                                                    # cut 2 teeth across the blade
        k.box((1.2, 16, 0.8), (-84 + i * 4.6, 0, 4.6), DSTEEL, rot=(0, 0, 0))
    k.box((30, 4, 3), (85, 0, 6), CHROME, metal=1, rough=0.3)                              # tang
    k.cyl(14, 70, (120, 0, 14), ANTH, rot=(0, 90, 0), bevel=2, rough=0.5)                  # handle


def hacksaw(k):
    """Hacksaw 300 mm: steel bow frame in the upright plane, pistol grip at the rear, blade across."""
    k.cyl(6, 300, (0, 0, 110), CHROME, rot=(0, 90, 0), metal=1, rough=0.25)                 # top bar
    k.cyl(5, 80, (150, 0, 70), DSTEEL, metal=0.8, rough=0.35)                               # front post
    k.cyl(6, 80, (-150, 0, 70), CHROME, metal=1, rough=0.25)                                # rear post
    k.box((290, 1.5, 14), (-5, 0, 40), CHROME, metal=1, rough=0.3)                          # blade
    k.box((44, 34, 74), (-150, 0, 104), BURG, bevel=12, rough=0.5)                          # ergonomic pistol grip, chunky and rounded


def _rect(k, cx, cy, w, h, a, thick, z, color, **mk):
    """A flat rectangle centred on (cx, cy), turned by a degrees, as a rounded slab."""
    pts = rot_pts([(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)], a)
    return k.slab([(x + cx, y + cy) for x, y in pts], thick, z, color, **mk)


def spirit_level(k):
    """Spirit level 600 mm, aluminium bar with three vial windows, lying flat, slightly diagonal."""
    a = 18
    _rect(k, 0, 0, 600, 40, a, 22, 0, DSTEEL, round_=2, metal=1, rough=0.3)               # bar
    for x in (-180, 0, 180):
        cx, cy = rot_pt(x, 0, a)
        _rect(k, cx, cy, 46, 14, a, 3, 22, '#CFE3F0', alpha=0.5, rough=0.1)                  # vial
    for x in (-296, 296):
        cx, cy = rot_pt(x, 0, a)
        _rect(k, cx, cy, 8, 42, a, 24, 0, ANTH, round_=1, rough=0.5)                          # end cap


def tape_measure(k):
    """Pocket tape measure 5 m: round anthracite housing, steel blade pulled out, burgundy belt clip."""
    k.cyl(32, 26, (0, 0, 13), ANTH, bevel=3, verts=64, rough=0.45)                          # housing
    k.box((180, 13, 1.5), (122, 0, 14), CHROME, metal=1, rough=0.3)                         # blade
    k.box((34, 6, 6), (-6, -36, 10), BURG, bevel=1, rough=0.5)                              # belt clip


def centre_punch(k):
    """Centre punch 150 mm: burgundy grip at the back, steel body and a long tapering point."""
    k.cyl(9, 60, (-35, 0, 9), BURG, rot=(0, 90, 0), bevel=2, verts=40, rough=0.5)           # grip
    k.cyl(5, 50, (20, 0, 5), CHROME, rot=(0, 90, 0), metal=1, rough=0.25)                   # body
    k.cyl(5, 30, (60, 0, 5), CHROME, rot=(0, 90, 0), r2=0.6, metal=1, rough=0.25)           # point


def hex_key_set(k):
    """Nine L-shaped hex keys 1.5 to 10 mm in black oxide steel, lying flat and nested inside each
    other like a catalogue shot: the largest outside, each smaller key tucked into the corner of the
    next, so every L shape stays visible and countable from above."""
    corner_x, corner_y = 0.0, 0.0
    for i, s in enumerate((10, 8, 6, 5, 4, 3, 2.5, 2, 1.5)):
        r = s / 1.732
        L, h = 150 - 9 * i, 52 - 3.5 * i
        z = r * 0.87
        k.cyl(r, L, (corner_x + L / 2, corner_y, z), KEY, rot=(0, 90, 0), verts=6, metal=0.6, rough=0.35)   # long leg
        k.cyl(r, h, (corner_x, corner_y + h / 2, z), KEY, rot=(90, 0, 0), verts=6, metal=0.6, rough=0.35)   # short leg
        k.sphere(r * 1.05, (corner_x, corner_y, z), KEY, metal=0.6, rough=0.35)                            # the bend
        corner_x += s / 2 + 6
        corner_y += s / 2 + 6


def locking_pliers(k):
    """Locking pliers 180 mm: curved steel jaws, burgundy and anthracite grips, adjusting screw at the tip."""
    _plier(k, 56, 96, 13, 17, 6, BURG, ANTH, 9, teeth=True)
    k.cyl(2.5, 30, (-62, 0, 16), DSTEEL, rot=(0, 90, 0), metal=0.8, rough=0.3)               # screw
    k.box((84, 7, 7), (70, -14, 40), DSTEEL, metal=0.8, rough=0.3)                           # toggle lock lever on the fixed handle
    k.cyl(4, 14, (26, -14, 40), DSTEEL, rot=(90, 0, 0), metal=0.8, rough=0.3)                 # lever pivot


def ratchet_handle(k):
    """Reversible ratchet 1/2 inch, 72 teeth: round steel head with a square drive, burgundy grip."""
    k.cyl(24, 22, (0, 0, 11), CHROME, verts=72, metal=1, rough=0.25, bevel=1)              # toothed head
    k.box((12.7, 12.7, 12), (0, 0, 27), CHROME, metal=1, rough=0.25)                       # square drive
    k.box((44, 10, 5), (30, 0, 25), DSTEEL, metal=0.8, rough=0.3)                          # reverse lever on the head top
    k.cyl(11, 200, (120, 0, 11), BURG, rot=(0, 90, 0), bevel=2, rough=0.5)                  # grip


SKUS = {
    'DEMO-IND-4001': (screwdriver_set, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4002': (socket_set_quarter, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4003': (socket_set_half, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4004': (spanner_set, {}, {'pitch': 70, 'fill': 0.8}),
    'DEMO-IND-4005': (pipe_wrench, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4006': (combination_pliers, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4007': (side_cutters, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4008': (water_pump_pliers, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4009': (engineers_hammer, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4010': (rubber_mallet, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4011': (flat_file, {}, {'pitch': 50, 'fill': 0.85}),
    'DEMO-IND-4012': (hacksaw, {}, {'pitch': 18, 'fill': 0.8}),
    'DEMO-IND-4013': (spirit_level, {}, {'pitch': 50, 'fill': 0.85}),
    'DEMO-IND-4014': (tape_measure, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4015': (centre_punch, {}, {'pitch': 50, 'fill': 0.85}),
    'DEMO-IND-4016': (hex_key_set, {}, {'pitch': 70, 'fill': 0.8}),
    'DEMO-IND-4017': (locking_pliers, {}, {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-4018': (ratchet_handle, {}, {'pitch': 50, 'fill': 0.8}),
}

HINTS = {
    'DEMO-IND-4001': 'A set of six separate screwdrivers lying side by side in one neat row: burgundy and anthracite handles alternating, three with slotted tips and three with cross tips, chrome steel shafts. Not a single screwdriver and not a tool box. Exactly six, count them. No labels or printing.',
    'DEMO-IND-4002': 'A 1/4 inch socket set in a flat anthracite plastic case with a burgundy latch: exactly 26 short chrome hex sockets standing upright in the tray, in rows of seven, sizes graded from small to large. Only sockets in the case, no ratchet and no bar inside. Not a loose pile and not a power tool. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4003': 'A 1/2 inch socket set: an anthracite plastic case with a burgundy latch holding exactly 18 chrome hex sockets in rows, graded from small to large, and beside the case a long chrome extension bar and a chrome ratchet handle with a square drive and a burgundy grip. Exactly 20 pieces in total. Not a loose pile. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4004': 'Eight double open-end spanners lying in one neat row side by side, each with an open U-shaped jaw at both ends, sizes graded from 8 mm to 19 mm, chrome-plated steel. No ring ends, no closed eyes, not fanned out. Exactly eight spanners, count them. No labels or printing.',
    'DEMO-IND-4005': 'A pipe wrench lying flat: a dark steel head with a fixed serrated jaw at one end, a sliding adjustable jaw beside it, and a long steel handle with a burgundy grip sleeve at the other end. Not an adjustable spanner and not a plumbing pipe.',
    'DEMO-IND-4006': 'Combination pliers lying flat, crossed at the pivot: short broad jaws with flat serrated gripping faces at one end, a wire cutter notch near the pivot, and long handles with a burgundy grip on one arm and an anthracite grip on the other. Not long-nose pliers: the jaws are short and broad, not slim and pointed. No labels or printing.',
    'DEMO-IND-4007': 'A pair of diagonal side cutters lying flat, crossed at the pivot: short flat-faced cutting jaws with sharp cutting edges at the joint, and straight plastic-coated grips in burgundy. Smooth steel jaws, no serrations, not long-nose pliers and no bent nose. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4008': 'Water pump pliers lying flat, crossed at the pivot: wide steel jaws with serrated teeth, a tongue-and-groove slip joint, and long anthracite and burgundy grips with a row of small adjusting slots on the lower arm. Wide jaws, not long narrow nose. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4009': "An engineer's hammer (machinist's hammer, DIN 1041) lying on its side: a forged steel head about 10 cm long fitted crosswise at the end of a straight 30 cm beech wood handle, with a flat square striking face on one end of the head and a wedge-shaped cross peen tapering to a narrow edge on the other end. The handle passes through the eye of the head. Not a sledge hammer, not a claw hammer, not a mallet, the head is not in line with the handle. No labels or printing.",
    'DEMO-IND-4010': 'A rubber mallet lying flat: a round anthracite plastic head across the end of a burgundy grip handle. Not a steel hammer and not a metal mallet.',
    'DEMO-IND-4011': 'A flat file lying flat on the floor: a long steel blade with parallel edges that tapers to a point, its face covered in fine transverse file teeth (cut 2), and a dark anthracite tang handle at the wide end. Not a knife and not a scraper: the teeth are visible across the blade. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4012': 'A hacksaw standing upright: a thin chrome steel frame with a chunky, rounded burgundy pistol grip at the rear, shaped to fit the hand, a thin steel blade across the frame, and a steel front post. Not a bow saw and not a coping saw.',
    'DEMO-IND-4013': 'A long aluminium spirit level lying flat, slightly diagonal, with exactly three glass vial windows on the top face (one horizontal and two vertical) and dark anthracite end caps. Exactly three vials, not four. Plain aluminium bar with no lettering. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4014': 'A compact tape measure: a rounded rectangular case in burgundy and anthracite rubberised plastic with a belt clip and a lock button, the yellow steel tape pulled out about 20 cm with its metal end hook, lying at an angle. Plain unmarked case, no logo; the tape shows only plain tick marks. Not a disc, not a yo-yo.',
    'DEMO-IND-4015': 'A centre punch lying flat: a burgundy grip at the back, a steel body and a long tapering point with a sharp tip. Not a nail punch and not a screwdriver.',
    'DEMO-IND-4016': 'A set of exactly nine L-shaped hex keys in matt black oxide steel lying flat on the floor, seen from above and nested so every key is visible: nine separate L shapes in graded sizes from the largest to the smallest, all nine countable. Not eight: exactly nine. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4017': 'Locking pliers lying flat, crossed at the pivot: curved steel jaws with teeth, a burgundy grip on one arm and an anthracite grip on the other, a toggle lock lever on the fixed handle and an adjusting screw at the end of the handle. Locking pliers, not combination pliers. Plain steel, no readable lettering. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-4018': 'A reversible ratchet lying flat: a round chrome head with a square drive on top and a small reverse lever on the top of the head, joined to a long burgundy plastic grip. Not a breaker bar: the head is round and has the reverse lever. No text, no numbers, no logos, no labels anywhere on the product.',
}
