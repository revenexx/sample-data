"""Industrial pack, series 2: fasteners, cutting discs, cable ties and an assortment case.

Plain unprinted cardboard boxes with the loose parts on the floor in front of them.
Zinc-plated steel reads as silver, stainless as a brighter steel, plastic in grey and black.
Units mm; products stand on z=0 with the front facing -Y.
"""
import math

CARD = '#C9AE86'      # plain kraft cardboard, unprinted
ZINC = '#B8BEC6'      # zinc-plated steel
STAINLESS = '#D9DDE2'
BLACK = '#1E1F22'
RECESS = '#2B2E33'
PLASTIC = '#B5BCC4'
CASE = '#D5D9DE'
DISC = '#8A919C'
FLAT = {'pitch': 50}  # camera for parts lying on the floor

# head radius and head height, as multiples of the diameter d, and the head shape
HEAD = {
    'csk': (1.0, 0.5, 'cone'),
    'pan': (0.95, 0.55, 'cyl'),
    'hex': (0.87, 0.66, 'hex'),
    'cheese': (0.9, 0.9, 'cyl'),
    'nail': (1.4, 0.4, 'cyl'),
    'plug': (0.75, 0.3, 'cyl'),
}


BOX_T = 3.0              # cardboard wall and floor thickness
BOX_Y = 10               # the box centre on the floor, behind the loose parts
INNER_X, INNER_Y = 120 - 2 * BOX_T, 90 - 2 * BOX_T


def carton(k, size=(120, 90, 40), y=BOX_Y):
    """Open plain cardboard box: floor, four walls and the back lid flap raised open."""
    sx, sy, sz = size
    rough = 0.85
    k.box((sx, sy, BOX_T), (0, y, BOX_T / 2), CARD, bevel=1, rough=rough)                    # floor
    k.box((sx, BOX_T, sz), (0, y - sy / 2 + BOX_T / 2, sz / 2), CARD, bevel=1, rough=rough)  # front
    k.box((sx, BOX_T, sz), (0, y + sy / 2 - BOX_T / 2, sz / 2), CARD, bevel=1, rough=rough)  # back
    k.box((BOX_T, sy, sz), (-sx / 2 + BOX_T / 2, y, sz / 2), CARD, bevel=1, rough=rough)     # left
    k.box((BOX_T, sy, sz), (sx / 2 - BOX_T / 2, y, sz / 2), CARD, bevel=1, rough=rough)      # right
    # back lid flap, hinged on the back top edge and raised to 110 degrees
    beta = 180 - 110                                  # box rotation about X that points the flap up and back
    dx, dy, dz = 0.0, math.cos(math.radians(beta)), math.sin(math.radians(beta))
    hinge = (0, y + sy / 2, sz)
    c = (hinge[0] + dx * sy / 2, hinge[1] + dy * sy / 2, hinge[2] + dz * sy / 2)
    k.box((sx, sy, BOX_T), c, CARD, bevel=1, rot=(beta, 0, 0), rough=rough)


def _inside(n_items, pitch_x, pitch_y):
    """Floor positions inside the open box for up to n_items, row by row, centred.
    Always leaves at least two items outside. Returns (positions, number left outside)."""
    cols = max(1, int((INNER_X - 4) // pitch_x))
    rows = max(1, int((INNER_Y - 4) // pitch_y))
    m = min(max(n_items - 2, 0), cols * rows)
    pos = []
    for i in range(m):
        row, col = divmod(i, cols)
        pos.append(((col - (cols - 1) / 2) * pitch_x, BOX_Y + (rows - 1) / 2 * pitch_y - row * pitch_y))
    return pos, n_items - m


def _grid(i, cols, pitch, y0=-70):
    row, col = divmod(i, cols)
    return (col - (cols - 1) / 2) * pitch, y0 - row * pitch


def _piece(k, cx, cy, a, kind, d, L, color, metal=0.8, tip=False, socket=None, z0=0.0):
    """A screw, bolt, nail or plug lying flat (on z0). The shank is centred on (cx, cy)
    with its axis at angle a; the head sits at the -L/2 end, the tip at the +L/2 end."""
    ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
    rot = (0, 90, a)
    r = d / 2

    def put(rad, h, s, z, col, r2=None, verts=48, m=None, rough=0.35, bevel=0.0):
        k.cyl(rad, h, (cx + ux * s, cy + uy * s, z0 + z), col, rot=rot, r2=r2, verts=verts,
              metal=metal if m is None else m, rough=rough, bevel=bevel)

    if kind == 'grub':                               # no head: a socket in the end
        put(r, L, 0, r, color)
        if socket:
            put(0.4 * d, 0.3 * d, -L / 2, r, BLACK, verts=socket, m=0, rough=0.5)
        return
    hr_f, hh_f, shape = HEAD[kind]
    hr, hh = hr_f * d, hh_f * d
    put(r, L, 0, r, color)                           # shank
    if shape == 'cone':                              # countersunk: wide at the top
        put(hr, hh, -L / 2 - hh / 2, hr, color, r2=r)
    else:
        put(hr, hh, -L / 2 - hh / 2, hr, color, verts=6 if shape == 'hex' else 48,
            bevel=0.9 if kind == 'cheese' else 0.0)                 # cheese head: rounded top edge
    if socket:
        put(0.4 * d, 0.3 * d, -L / 2 - hh, hr, BLACK, verts=socket, m=0, rough=0.5)
    if tip:                                          # drill point
        put(r, 0.9 * d, L / 2 + 0.45 * d, r, color, r2=0.15 * r)


def fastener_box(k, kind='pan', d=4.0, L=12.0, color=ZINC, n=10, metal=0.8, tip=False,
                 socket=None, per=None):
    """Open box with screws, bolts, nails or plugs lying inside it, a few loose in front. per = items per row outside."""
    carton(k)
    inside, outside = _inside(n, L + 8, 2 * d + 8)
    for i, (cx, cy) in enumerate(inside):
        a = (-8, 6, -4, 10, -12, 3, 8, -6)[i % 8]
        _piece(k, cx, cy, a, kind, d, L, color, metal, tip, socket, z0=BOX_T)
    if per is None:
        per = max(1, min(4, int(180 // (L + 16))))
    for j in range(outside):
        row, col = divmod(j, per)
        cx = (col - (per - 1) / 2) * (L + 16)
        cy = -62 - row * (2 * d + 16)
        a = (-8, 6, -4, 10, -12, 3, 8, -6)[j % 8]
        _piece(k, cx, cy, a, kind, d, L, color, metal, tip, socket)


def hex_nuts(k, d=8.0, af=13.0, h=6.5, n=8, pitch=22.0, cols=4):
    """Hex nuts lying flat, bore dark on top: most inside the open box, a few loose in front."""
    carton(k)
    rc = af / math.sqrt(3)
    inside, outside = _inside(n, pitch, pitch)
    items = [(x, y, BOX_T) for x, y in inside] + [(*_grid(j, cols, pitch), 0.0) for j in range(outside)]
    for i, (x, y, z0) in enumerate(items):
        k.cyl(rc, h, (x, y, z0 + h / 2), ZINC, verts=6, rot=(0, 0, 15 * (i % 3)), metal=0.8, rough=0.35)
        k.cyl(d / 2, 0.2, (x, y, z0 + h + 0.1), RECESS, verts=32, metal=0)


def square_nuts(k, d=10.0, s=16.0, h=8.0, n=6, pitch=24.0, cols=3):
    """Square nuts lying flat: most inside the open box, a few loose in front."""
    carton(k)
    inside, outside = _inside(n, pitch, pitch)
    items = [(x, y, BOX_T) for x, y in inside] + [(*_grid(j, cols, pitch), 0.0) for j in range(outside)]
    for i, (x, y, z0) in enumerate(items):
        k.box((s, s, h), (x, y, z0 + h / 2), ZINC, bevel=0.5, metal=0.8, rough=0.35)
        k.cyl(d / 2, 0.2, (x, y, z0 + h + 0.1), RECESS, verts=32, metal=0)


def _washer(k, od, t, x, y, layer=0, bore=None, z0=0.0):
    z = z0 + layer * t
    k.cyl(od / 2, t, (x, y, z + t / 2), ZINC, verts=48, metal=0.8, rough=0.35)
    if bore:                                         # dark hole on the top face
        k.cyl(bore / 2, 0.2, (x, y, z + t + 0.1), RECESS, verts=32, metal=0)


def washers(k, od=16.0, idia=8.4, t=1.6, n=10, pitch=22.0, cols=4, stack=0):
    """Flat washers lying flat, most inside the open box, a few loose in front, plus an optional stack."""
    carton(k)
    inside, outside = _inside(n, pitch, pitch)
    for x, y in inside:
        _washer(k, od, t, x, y, 0, bore=idia, z0=BOX_T)
    for j in range(outside):
        x, y = _grid(j, cols, pitch)
        _washer(k, od, t, x, y, 0, bore=idia)
    for j in range(stack):
        _washer(k, od, t, 95, -70, j, bore=idia if j == stack - 1 else None)


def threaded_rod(k, d=8.0, length=1000.0):
    """A straight threaded rod lying on the floor along the X axis, no box."""
    k.cyl(d / 2, length, (0, 0, d / 2), ZINC, rot=(0, 90, 0), verts=32, metal=0.8, rough=0.35)


def cutting_discs(k, n=10, r=62.5, t=1.0):
    """A pile of thin metal discs stacked flat, each slightly offset, a dark bore on top."""
    for j in range(n):
        dx, dy = 0.8 * (j % 3 - 1), 0.5 * (j % 2)
        k.cyl(r, t, (dx, dy, j * t + t / 2), DISC, verts=72, metal=0.4, rough=0.5)
    k.cyl(11, 0.2, (dx, dy, n * t + 0.1), RECESS, verts=32, metal=0)


def cable_ties(k, n=10):
    """Black cable ties lying loose, two layers of five, each strip with a small head at one end."""
    for i in range(n):
        a = (-4, 2, -2, 3, -3)[i % 5]
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        cx, cy = 0.0, -20 - 10 * (i % 5)
        z = 0.6 + 1.3 * (i // 5)
        k.box((200, 4.8, 1.2), (cx, cy, z), BLACK, bevel=0.3, rot=(0, 0, a), metal=0, rough=0.5)
        k.box((10, 9, 3.4), (cx - ux * 104, cy - uy * 104, z + 1.1), BLACK, bevel=0.5,
              rot=(0, 0, a), metal=0, rough=0.5)


def _nut(k, x, y, z0, d=6.0, af=10.0, h=5.2):
    """A zinc hex nut lying flat on z0, bore dark on top."""
    k.cyl(af / math.sqrt(3), h, (x, y, z0 + h / 2), ZINC, verts=6, rot=(0, 0, 15), metal=0.8, rough=0.35)
    k.cyl(d / 2, 0.2, (x, y, z0 + h + 0.1), RECESS, verts=32, metal=0)


def assortment_case(k, n=12):
    """Open grey plastic assortment tray: a 3 x 2 grid of compartments, screws lying in them."""
    sx, sy, sz = 240, 170, 30
    rough = 0.5
    k.box((sx, sy, BOX_T), (0, 0, BOX_T / 2), CASE, bevel=1, metal=0, rough=rough)           # floor
    k.box((sx, BOX_T, sz), (0, -sy / 2 + BOX_T / 2, sz / 2), CASE, bevel=1, metal=0, rough=rough)
    k.box((sx, BOX_T, sz), (0, sy / 2 - BOX_T / 2, sz / 2), CASE, bevel=1, metal=0, rough=rough)
    k.box((BOX_T, sy, sz), (-sx / 2 + BOX_T / 2, 0, sz / 2), CASE, bevel=1, metal=0, rough=rough)
    k.box((BOX_T, sy, sz), (sx / 2 - BOX_T / 2, 0, sz / 2), CASE, bevel=1, metal=0, rough=rough)
    for x in (-40, 40):                                                                   # dividers
        k.box((BOX_T, sy, sz * 0.9), (x, 0, sz * 0.45), CASE, bevel=1, metal=0, rough=rough)
    k.box((sx, BOX_T, sz * 0.9), (0, 0, sz * 0.45), CASE, bevel=1, metal=0, rough=rough)  # cross divider
    kinds = (('hex', 6, 20), ('cheese', 5, 16), ('csk', 4, 20), ('nut', 6, 0))   # the fourth kind is a hex nut
    cells = [(cx, cy) for cy in (42.5, -42.5) for cx in (-80, 0, 80)]   # 3 x 2 compartments
    m = min(max(n - 2, 0), 2 * len(cells))                               # two per compartment
    for i in range(m):
        kind, d, L = kinds[i % 4]
        cx, cy = cells[i // 2]
        color = ZINC if i % 2 else STAINLESS
        if kind == 'nut':
            _nut(k, cx, cy + (18 if i % 2 else -18), BOX_T)
        else:
            _piece(k, cx, cy + (18 if i % 2 else -18), (0, 20, -15, 40)[i % 4], kind, d, L, color,
                   z0=BOX_T)
    outside = n - m
    for j in range(outside):
        kind, d, L = kinds[j % 4]
        if kind == 'nut':
            _nut(k, -60 + 120 * j, -115, 0.0)
        else:
            _piece(k, -60 + 120 * j, -115, (0, 20)[j % 2], kind, d, L, ZINC)


SKUS = {
    'DEMO-IND-2001': (fastener_box, dict(kind='csk', d=4, L=40, color=ZINC, n=10, socket=6), FLAT),
    'DEMO-IND-2002': (fastener_box, dict(kind='hex', d=8, L=40, color=ZINC, n=8), FLAT),
    'DEMO-IND-2003': (cutting_discs, {}, FLAT),
    'DEMO-IND-2004': (fastener_box, dict(kind='csk', d=3.5, L=30, color=ZINC, n=12), FLAT),
    'DEMO-IND-2005': (fastener_box, dict(kind='csk', d=5, L=60, color=ZINC, n=8), FLAT),
    'DEMO-IND-2006': (fastener_box, dict(kind='pan', d=5, L=80, color=STAINLESS, n=6, per=2, tip=True, socket=4), FLAT),
    'DEMO-IND-2007': (fastener_box, dict(kind='hex', d=6, L=30, color=ZINC, n=10), FLAT),
    'DEMO-IND-2008': (fastener_box, dict(kind='hex', d=10, L=60, color=ZINC, n=6), FLAT),
    'DEMO-IND-2009': (hex_nuts, dict(d=8, af=13, h=6.5, n=8), FLAT),
    'DEMO-IND-2010': (hex_nuts, dict(d=6, af=10, h=5.2, n=8, pitch=18), FLAT),
    'DEMO-IND-2011': (washers, dict(od=16, idia=8.4, t=1.6, n=10), FLAT),
    'DEMO-IND-2012': (threaded_rod, dict(d=8, length=1000), FLAT),
    'DEMO-IND-2013': (fastener_box, dict(kind='plug', d=8, L=40, color=PLASTIC, n=10, metal=0), FLAT),
    'DEMO-IND-2014': (cable_ties, {}, FLAT),
    'DEMO-IND-2015': (fastener_box, dict(kind='nail', d=3, L=60, color=ZINC, n=9, per=3, tip=True), FLAT),
    'DEMO-IND-2016': (fastener_box, dict(kind='grub', d=6, L=20, color=STAINLESS, n=10, socket=6), FLAT),
    'DEMO-IND-2017': (fastener_box, dict(kind='cheese', d=5, L=16, color=STAINLESS, n=12, socket=6), FLAT),
    'DEMO-IND-2018': (fastener_box, dict(kind='pan', d=4, L=12, color=ZINC, n=12, socket=4), FLAT),
    'DEMO-IND-2019': (fastener_box, dict(kind='pan', d=4.2, L=19, color=ZINC, n=12, tip=True), FLAT),
    'DEMO-IND-2020': (assortment_case, {}, FLAT),
    'DEMO-IND-2021': (square_nuts, dict(d=10, s=16, h=8, n=6), FLAT),
    'DEMO-IND-2022': (fastener_box, dict(kind='hex', d=12, L=80, color=ZINC, n=4, per=2), FLAT),
    'DEMO-IND-2023': (washers, dict(od=20, idia=10.5, t=2.0, n=6, stack=6), FLAT),
}

HINTS = {
    'DEMO-IND-2001': 'Countersunk wood screws about 40 mm long, zinc-plated silver, each with a flat conical head and a six-lobe star recess (T20 hexalobular) in the top of the head, a smooth shank under the head and thread on the lower part. Lying loose and in an open box. Not a cross-recess screw: the recess has six lobes. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2002': 'Hex head bolts about 40 mm long, zinc-plated silver, with an intact six-sided head and a fully threaded shank, none bent or broken. Not a screw: the head is a hexagon with no slot. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2003': 'Five thin flat metal cutting discs for an angle grinder, 125 mm diameter and only 1 mm thick, spread out overlapping like a fan of cards on the floor so their thin edges and flat faces are clearly visible: dark grey-blue abrasive face, a small steel ring around the 22 mm centre hole. Each disc thin like a cardboard coaster. Plain, no printed label. Not a puck, not a thick wheel.',
    'DEMO-IND-2004': 'Countersunk wood screws about 30 mm long, zinc-plated silver with a flat conical head and a fully threaded shank. Not a bolt: no hexagon head and no nut. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2005': 'Countersunk wood screws about 60 mm long, zinc-plated silver, with a flat countersunk head and a partly threaded shank. Not a bolt: no hexagon head. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2006': 'Stainless wood screws, about 80 mm long, each with a broad pan head with a Phillips cross recess and a sharp pointed thread on a plain shank. Only screws: no bolts, no square necks, no nuts. Bright cool silver stainless steel. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text. No labels or printing.',
    'DEMO-IND-2007': 'Hex head bolts about 30 mm long, zinc-plated silver, each with a plain six-sided hexagon head with no recess, no slot and no cross mark on the top, and a fully threaded shank. Not a screw: the head is a hexagon only. A small plain cardboard box with loose bolts in front. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2008': 'Hex head bolts about 60 mm long, zinc-plated silver, each with a large plain six-sided head with no drive recess on top, a shank threaded at the tip and plain (unthreaded) under the head. Visibly thicker than an M6 bolt. Not a stud, not a screw. A small plain cardboard box with loose bolts in front. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2009': 'Hex nuts about 8 mm, zinc-plated silver, flat six-sided rings with a round bore visible on top. Not a washer: they are thick and six-sided. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2010': 'Small hex nuts for M6, zinc-plated silver: each a flat six-sided nut with a round threaded bore visible on top, and no other shape. Not a washer, not a sleeve, not a bushing: no external thread and no round body. A small plain cardboard box with loose hex nuts in front. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2011': 'Flat washers for M8, zinc-plated silver thin rings about 16 mm across with a round hole. Not a nut: no hexagon, just a plain thin ring. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2012': 'A straight threaded rod about 8 mm thick and 1 metre long, zinc-plated silver, lying flat along the floor with no box. Not a bolt: no head at either end, threaded along its full length.',
    'DEMO-IND-2013': 'Grey plastic expansion plugs about 40 mm long, each a slotted plastic sleeve with a small flange at one end. Not a screw: no thread and no head. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2014': 'A bundle of about twenty black nylon cable ties, 200 mm long and thin, lying loosely fanned out diagonally so the individual flat strips with their small square heads are visible. Not a single black bar, not a belt.',
    'DEMO-IND-2015': 'Smooth wire nails about 60 mm long, zinc-plated silver, each a plain round shank with a pointed tip and a flat round head at the top, all complete with head and shank together. Lying loose and in a small plain box. Nothing detached: no loose heads, no dome-shaped parts, nothing floating. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2016': 'Headless set screws M6 x 20 in stainless steel: each a short plain threaded cylinder, threaded along its full length, with a hex socket in one end and no head at all. Not a bolt, not a stud, not a spacer or pin: nothing sticks out at the ends apart from the socket. A small plain cardboard box with loose set screws in front. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2017': 'Cheese head screws in stainless steel, about 16 mm long: each with a short domed cylindrical head with a hex socket in its top and a plain threaded shank below. Not spacers, not sleeves, not hex bolts, no plain tubes. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text. No labels or printing.',
    'DEMO-IND-2018': 'Pan head screws about 12 mm long, zinc-plated silver, with a low round domed head and a cross recess on top. Not a bolt: the head is round and the drive is a cross. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2019': 'Sheet metal screws about 19 mm long, zinc-plated silver, with a round pan head, a fully threaded shank and a sharp drill point at the end. Not a wood screw: the tip is a drill point. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
    'DEMO-IND-2020': 'An open shallow grey plastic assortment tray with six compartments in a 3 by 2 grid, each compartment holding a few items lying flat: hex-head screws, cheese-head screws, countersunk screws and hex nuts, all zinc-plated or stainless, all clearly visible. No washers, no other parts. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2021': 'Square nuts about 10 mm, zinc-plated silver: each a flat square block with four straight flat sides, sharp chamfered corners and a round hole through the middle. Not hexagonal. Lying loose on the table and in a small plain box. Nothing set into the walls of the box. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2022': 'Hex head bolts about 80 mm long, zinc-plated silver: each a large plain six-sided head with no recess, and a shank with thread on its lower part and a plain unthreaded section under the head. Every item is a hex bolt: no wooden handles, no sticks, no hybrid parts. A small plain cardboard box with loose bolts in front. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-2023': 'Flat washers about 20 mm across with a round hole, zinc-plated silver, and a neat stack of six standing beside the box. Not a nut: a plain ring with no hexagon. The small plain cardboard box stands fully in frame with its lid open, filled with the parts, a few loose ones lying on the floor beside it. The box is completely plain and unprinted: no label, no size marking, no text.',
}
