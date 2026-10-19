"""Lab pack, series 3: consumables. Tubes in sealed bags and racks, petri dishes,
nitrile gloves, microplates, weighing boats, filter paper, sealing film,
markers, lab wipes and silicone stoppers.

Clear plastic is drawn as 'glass' with alpha 0.5; caps use plain colours
(blue, green, red, orange or white); bags and boxes are plain white, unprinted.
Units mm, product stands on z=0, front faces -Y.
"""

CAP_BLUE = '#2F6FE0'
CAP_GREEN = '#2F8A57'
CAP_RED = '#C7362F'
CAP_ORANGE = '#E8930C'
GLOVE_BLUE = '#2E5FA8'
GLOVE_VIOLET = '#6E4BC4'
INK = {'black': '#2B2E33', 'blue': '#2E5FA8', 'red': '#C7362F', 'green': '#2F8A57'}


def tube(k, x, y, d, h, cap, cap_h, base=0.0, cone=0.2, snap=False):
    """Clear tube standing on z=base: a tapered tip, a clear body and a coloured cap.
    snap=True: a flip-top snap lid, closed, with a small hinge strap to the tube."""
    r = d / 2
    body = h - cap_h
    ct = body * cone
    k.cyl(r * 0.3, ct, (x, y, base + ct / 2), 'glass', r2=r, alpha=0.5, rough=0.1, verts=32)
    k.cyl(r, body - ct, (x, y, base + ct + (body - ct) / 2), 'glass', alpha=0.5, rough=0.1, verts=32)
    if snap:
        k.cyl(r * 1.04, cap_h, (x, y, base + body + cap_h / 2), cap, bevel=2, verts=32)  # snap lid, closed
        k.box((r * 0.5, 1.0, cap_h * 0.6), (x, y + r * 1.02, base + body + cap_h * 0.4), cap)  # hinge strap
    else:
        k.cyl(r * 1.04, cap_h, (x, y, base + body + cap_h / 2), cap, bevel=1, verts=32)


def pouch(k, w, d, h):
    """Sealed white bag lying flat on the floor, rounded pillow edges, at the left of the frame."""
    k.box((w, d, h), (-40, 0, h / 2), 'white', bevel=min(8, h * 0.3))


def tube_bag(k, d, h, cap, cap_h, n=2, snap=False, cone=0.2):
    """Bag of loose tubes: a sealed white bag with n clear tubes standing beside it."""
    pouch(k, 120, 80, 34)
    for i in range(n):
        tube(k, 62 + i * (d + 10), -12 if i % 2 == 0 else 14, d, h, cap, cap_h, snap=snap, cone=cone)


def lying_tube(k, x0, y, d, length, cap, cap_len):
    """Round-bottom tube lying on the floor along X, starting at x0: a clear
    body with a rounded end and a coloured cap at the open end."""
    r = d / 2
    body = length - r - cap_len
    k.sphere(r, (x0 + r, y, r), 'glass', alpha=0.5, rough=0.1)
    k.cyl(r, body, (x0 + r + body / 2, y, r), 'glass', alpha=0.5, rough=0.1, rot=(0, 90, 0), verts=32)
    k.cyl(r * 1.04, cap_len, (x0 + r + body + cap_len / 2, y, r), cap, rot=(0, 90, 0), bevel=1, verts=32)


def round_bag(k):
    """Bag of round-bottom sample tubes: a sealed white bag with four tubes lying beside it."""
    pouch(k, 120, 80, 34)
    for y in (-30, -10, 10, 30):
        lying_tube(k, 40, y, 15, 78, 'white', 14)


def pipette_bag(k):
    """Bag of transfer pipettes: a sealed white bag with two long pipettes lying beside it."""
    pouch(k, 120, 80, 34)
    for y in (-20, 10):
        k.cyl(2.5, 120, (40 + 60, y, 2.5), 'glass', alpha=0.5, rot=(0, 90, 0), verts=24)   # stem
        k.cyl(5.5, 18, (40 + 129, y, 5.5), 'white', rot=(0, 90, 0), verts=32, bevel=1)     # bulb


def cap_bag(k, r, h, n, color):
    """Bag of loose caps: a sealed white bag with a small heap of caps on the floor beside it."""
    pouch(k, 120, 80, 34)
    for i in range(n):
        x = 60 + (i % 3) * (2 * r + 6)
        y = -20 + (i // 3) * (2 * r + 6)
        k.cyl(r, h, (x, y, h / 2), color, bevel=1, verts=40)


def tube_rack(k, cols, rows, pitch, d, h, cap, cap_h, cone=0.2):
    """Rack of standing tubes on a light grey base plate."""
    rack_h = 20
    w, dep = cols * pitch, rows * pitch
    k.box((w + 8, dep + 8, rack_h), (0, 0, rack_h / 2), 'light', bevel=3)
    for i in range(cols):
        for j in range(rows):
            x = (i - (cols - 1) / 2) * pitch
            y = (j - (rows - 1) / 2) * pitch
            tube(k, x, y, d, h, cap, cap_h, base=rack_h, cone=cone)


def petri_pack(k):
    """Stack of about 20 flat clear petri dishes (90 mm, 14 mm pitch, slightly larger lids) in a clear sleeve."""
    k.box((115, 115, 6), (0, 0, 3), 'white', bevel=1)
    for i in range(20):
        z = 6 + i * 14
        k.cyl(45, 11, (0, 0, z + 5.5), 'glass', alpha=0.5, rough=0.1, bevel=0.5, verts=64)   # dish
        k.cyl(46.5, 3, (0, 0, z + 12.5), 'glass', alpha=0.5, rough=0.1, bevel=0.5, verts=64)  # slightly larger lid
    for x in (-46, 46):
        for y in (-46, 46):
            k.box((4, 4, 284), (x, y, 148), 'glass', alpha=0.6, rough=0.1)                # clear sleeve, four corner posts


def rect(cx, cy, w, h):
    return [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]


def glove(k, cx, cy, color):
    """Nitrile glove lying flat on the floor, fingers towards +Y: a palm,
    four fingers, a thumb and a cuff, as thin padded outlines."""
    t = 3.5

    def part(pts):
        k.slab([(cx + px, cy + py) for px, py in pts], t, 0, color, smooth=3)

    part(rect(0, 0, 96, 85))                                  # palm
    for fx, length in ((-39, 62), (-13, 72), (13, 68), (39, 56)):
        part(rect(fx, 30 + length / 2, 15, length + 8))       # fingers, spread with clear gaps, rooted in the palm
    part(rect(56, 6, 20, 52))                                 # thumb, joined to the palm, apart from the fingers
    part(rect(0, -62, 80, 40))                                # cuff


def glove_box(k):
    """Open plain white cardboard box of gloves: four walls and a floor, a stack of blue
    gloves inside, and one loose glove lying flat beside it."""
    x, y, z, t = 260, 130, 95, 3
    k.box((x, y, t), (0, 0, t / 2), 'white', bevel=1)                                   # floor
    k.box((x, t, z), (0, -y / 2 + t / 2, z / 2), 'white', bevel=1)                      # front wall
    k.box((x, t, z), (0, y / 2 - t / 2, z / 2), 'white', bevel=1)                       # back wall
    k.box((t, y, z), (-x / 2 + t / 2, 0, z / 2), 'white', bevel=1)                      # left wall
    k.box((t, y, z), (x / 2 - t / 2, 0, z / 2), 'white', bevel=1)                       # right wall
    k.box((x - 2 * t - 10, y - 2 * t - 10, 40), (0, 0, t + 20), GLOVE_BLUE, bevel=4, rough=0.5)  # gloves inside
    glove(k, -215, -30, GLOVE_BLUE)


def plate_stack(k, n, h, w=128, d=86, wells=False, grid=(8, 12, 9.0, 3.4)):
    """Stack of flat-bottomed white polystyrene microplates; wells=True draws a regular 8 x 12 grid on the top plate."""
    for i in range(n):
        k.box((w, d, h), (0, 0, h / 2 + i * h), 'white', bevel=1.5)
    if wells:
        rows, cols, pitch, wr = grid
        for i in range(cols):
            for j in range(rows):
                k.cyl(wr, 0.6, ((i - (cols - 1) / 2) * pitch, (j - (rows - 1) / 2) * pitch, n * h + 0.2), 'dark')


def boat_stack(k, side, h, n=4):
    """Nested square weighing boats: shallow white trays with walls flaring out strongly."""
    for i in range(n):
        z = i * h * 0.45
        k.cyl(side * 0.45, h, (0, 0, z + h / 2), 'white', r2=side * 0.75, verts=4, rot=(0, 0, 45), bevel=0.6)


def filter_pile(k, r, h=20):
    """Flat pile of round off-white filter papers on a grey shadow plate, edges kept visible."""
    k.cyl(r * 1.04, 0.6, (0, 0, 0.3), '#A9A59C', verts=64)                              # soft contact shadow
    k.cyl(r, h, (0, 0, h / 2), '#E3E0D7', verts=64, bevel=0.6)


def film_roll(k):
    """Roll of clear sealing film lying on its side, the round end facing the camera."""
    k.cyl(42, 100, (0, 0, 42), 'glass', alpha=0.5, rough=0.2, rot=(90, 0, 0), verts=64)
    k.cyl(20, 102, (0, 0, 42), 'paperDark', rot=(90, 0, 0), verts=48)


def markers(k):
    """Four permanent markers lying side by side: white bodies, caps in ink colours at the front."""
    for i, c in enumerate(INK.values()):
        x = (i - 1.5) * 16
        k.cyl(6, 120, (x, 0, 6), 'white', rot=(90, 0, 0), verts=32, bevel=1)
        k.cyl(6.3, 34, (x, -43, 6), c, rot=(90, 0, 0), verts=32, bevel=1)


def wipes_box(k):
    """Plain white dispenser box with a slot on top and wipes pulled up through it."""
    k.box((150, 100, 96), (0, 0, 48), 'white', bevel=3)
    k.box((120, 30, 2), (0, 0, 97), 'dark')
    k.box((96, 22, 14), (0, 0, 106), 'white', bevel=1)


def stoppers(k):
    """Shallow white tray with 20 tapered silicone stoppers: five sizes (one per column),
    four of each standing upright on the narrow end, the top end wider than the base."""
    k.box((200, 130, 8), (0, 0, 4), 'white', bevel=1.5)
    sizes = ((5, 7, 12), (6, 8.5, 14), (7, 9.5, 16), (8, 11, 18), (9.5, 12.5, 20))
    for i, (rb, rt, h) in enumerate(sizes):
        for j in range(4):
            x = -80 + i * 40
            y = -39 + j * 26
            k.cyl(rb, h, (x, y, 8 + h / 2), 'paper', r2=rt, bevel=1, verts=40)


FLAT = {'pitch': 35}

SKUS = {
    'DEMO-LAB-3001': (tube_bag, {'d': 11, 'h': 40, 'cap': CAP_BLUE, 'cap_h': 10, 'n': 4, 'snap': True, 'cone': 0.35}),
    'DEMO-LAB-3002': (tube_rack, {'cols': 5, 'rows': 5, 'pitch': 36, 'd': 29, 'h': 115, 'cap': 'white', 'cap_h': 18, 'cone': 0.4}),
    'DEMO-LAB-3003': (petri_pack, {}, {'pitch': 30}),
    'DEMO-LAB-3004': (glove_box, {}, {'pitch': 45}),
    'DEMO-LAB-3005': (tube_bag, {'d': 11, 'h': 40, 'cap': '#EEF0F2', 'cap_h': 4, 'snap': True, 'n': 3, 'cone': 0.35}),
    'DEMO-LAB-3006': (tube_bag, {'d': 8, 'h': 34, 'cap': CAP_RED, 'cap_h': 8, 'snap': True, 'cone': 0.35}),
    'DEMO-LAB-3007': (tube_rack, {'cols': 10, 'rows': 5, 'pitch': 24, 'd': 17, 'h': 120, 'cap': CAP_BLUE, 'cap_h': 14, 'cone': 0.4}),
    'DEMO-LAB-3008': (tube_rack, {'cols': 5, 'rows': 5, 'pitch': 36, 'd': 29, 'h': 115, 'cap': 'white', 'cap_h': 18, 'cone': 0.4}),
    'DEMO-LAB-3009': (tube_bag, {'d': 12, 'h': 47, 'cap': CAP_ORANGE, 'cap_h': 13}),
    'DEMO-LAB-3010': (round_bag, {}, FLAT),
    'DEMO-LAB-3011': (plate_stack, {'n': 3, 'h': 14.4, 'wells': True}),
    'DEMO-LAB-3012': (plate_stack, {'n': 4, 'h': 14.4, 'w': 127.8, 'd': 85.5, 'wells': True, 'grid': (16, 24, 4.5, 1.7)}),
    'DEMO-LAB-3013': (boat_stack, {'side': 80, 'h': 25, 'n': 4}),
    'DEMO-LAB-3014': (pipette_bag, {}, FLAT),
    'DEMO-LAB-3015': (filter_pile, {'r': 62.5, 'h': 20}, {'pitch': 30}),
    'DEMO-LAB-3016': (filter_pile, {'r': 35, 'h': 20}, {'pitch': 30}),
    'DEMO-LAB-3017': (cap_bag, {'r': 16, 'h': 14, 'n': 3, 'color': 'white'}),
    'DEMO-LAB-3018': (boat_stack, {'side': 40, 'h': 12, 'n': 4}),
    'DEMO-LAB-3019': (film_roll, {}, {'pitch': 25}),
    'DEMO-LAB-3020': (cap_bag, {'r': 6.5, 'h': 6, 'n': 6, 'color': CAP_BLUE}),
    'DEMO-LAB-3021': (markers, {}, FLAT),
    'DEMO-LAB-3022': (tube_bag, {'d': 15, 'h': 62, 'cap': 'white', 'cap_h': 13}),
    'DEMO-LAB-3023': (wipes_box, {}),
    'DEMO-LAB-3024': (stoppers, {}),
}

HINTS = {
    'DEMO-LAB-3001': 'A sealed white plastic bag of 1.5 ml microcentrifuge tubes: a flat pillow-shaped pouch with four short clear tubes standing beside it. Each tube is short, about 38 mm, with a narrow conical bottom and a closed flat snap-cap lid in blue on top, joined by a small hinge strap. Not long straight tubes, not screw caps, not flip caps. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3002': 'A rack of 25 clear 50 ml conical centrifuge tubes with white screw caps in an even 5 by 5 grid on a light grey base plate, every hole filled. Each tube is wide, about 29 mm across, straight in the upper body and tapering to a conical tip at the bottom, all the same height. Not slim straight test tubes, not rounded bottoms. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3003': 'A stack of about 20 flat clear polystyrene petri dishes, 90 mm across and only about 14 mm tall each, with slightly larger lids, standing as a tall stack inside a clear plastic sleeve on a flat white base. Flat dishes, not bowls, not a single dish. No labels or printing.',
    'DEMO-LAB-3004': 'A plain white cardboard box of 100 powder-free nitrile gloves, open on top with its flaps folded back, a stack of blue gloves visible inside, and one single loose blue nitrile glove lying flat on the floor beside the box, palm down, fingers spread. No lettering on the box. The loose glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, with clear gaps between them so all five are clearly visible and countable. Only one loose glove. No mittens, no extra or missing fingers. No labels or printing on the glove.',
    'DEMO-LAB-3005': 'A sealed white bag of 2.0 ml microcentrifuge tubes with three short clear tubes standing beside it. Each tube is about 40 mm long with a narrow conical bottom and a flat push-fit snap lid in cream-white on top, joined by a small plastic hinge strap. Not long straight tubes, not screw caps. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3006': 'A sealed white bag of 0.5 ml microcentrifuge tubes with two short clear tubes standing beside it. Each tube is about 34 mm long and narrow, with a conical bottom and a flat snap-cap lid in red on top, joined by a small hinge strap. Not long straight tubes, not screw caps. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3007': 'A full rack of 50 clear 15 ml conical centrifuge tubes with blue screw caps: a 10 by 5 grid (10 columns, 5 rows), every hole filled, on a light grey base plate. Each tube is about 17 mm wide, straight in the upper body and tapering to a conical tip at the bottom. Not straight-bottomed tubes. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3008': 'A clear plastic sleeve sealed around a rack of exactly 25 sterile 50 ml conical centrifuge tubes with white screw caps in a 5 by 5 grid, every hole filled. Each tube is wide, about 29 mm, straight in the upper body and tapering to a conical tip at the bottom, not a pedestal foot. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3009': 'A sealed white bag of 2 ml cryo tubes: a flat pouch with two clear cryo tubes standing beside it, each with a wide orange screw cap. The clear tubes stand out clearly from the white background with a soft shadow. Not a freezer box.',
    'DEMO-LAB-3010': 'A sealed white bag of 5 ml round-bottom sample tubes: a flat pouch with two clear tubes lying on the floor beside it, each with a rounded closed end and a white cap at the open end. The clear tubes stand out clearly from the white background with a soft shadow. Not a standing tube.',
    'DEMO-LAB-3011': 'A stack of three flat rectangular polystyrene 96-well microplates with lids, about 128 by 86 mm each. The top plate has open wells: exactly 96 round recesses in 8 rows and 12 columns, each with a flat bottom. Not a perforated cover, not a tray with holes, not 384 wells. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3012': 'A stack of four flat rectangular clear polystyrene 384-well microplates with lids, about 128 by 86 mm each. The top plate shows a fine regular grid of exactly 384 small round open wells in 16 rows and 24 columns, flat bottom. Not 96 wells, not square cells, not a coarse grid. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3013': 'A nested stack of four square white polystyrene weighing boats, about 80 by 80 mm at the top, very shallow trays about 25 mm deep with walls flaring outward strongly. The boats stand out clearly from the white background with a soft shadow. No labels or printing.',
    'DEMO-LAB-3014': 'A sealed white bag of 3 ml transfer pipettes: a flat pouch with two clear polyethylene pipettes lying on the floor beside it, each a long thin stem with a rounded bulb at one end. The clear pipettes stand out clearly from the white background with a soft shadow. Not a glass pipette.',
    'DEMO-LAB-3015': 'A flat pile of about 100 round white filter papers, 125 mm in diameter, thin with a clean edge, stacked on the floor. Flat discs in a stack, not folded filters and not a cone. The pile stands out clearly from the white background with a soft shadow.',
    'DEMO-LAB-3016': 'A flat pile of about 100 round off-white filter papers, 70 mm in diameter and the same stack height as a 125 mm pile but narrower, on a light grey surface with a soft shadow under the stack, each disc edge visible as a thin line. Flat discs in a stack, not folded filters and not a cone.',
    'DEMO-LAB-3017': 'A sealed white bag of replacement screw caps for 50 ml tubes: a flat pouch with three loose white screw caps on the floor beside it, each a wide ribbed cap with a flat top. The caps stand out clearly from the white background with a soft shadow. Not a tube.',
    'DEMO-LAB-3018': 'A nested stack of four small square white polystyrene weighing boats, about 40 by 40 mm at the top, very shallow trays about 12 mm deep with walls flaring outward strongly. The boats stand out clearly from the white background with a soft shadow. No labels or printing.',
    'DEMO-LAB-3019': 'A roll of clear polyethylene sealing film around a pale cardboard core, lying on its side with the round end facing the camera. The clear film stands out clearly from the white background with a soft shadow. Not a tape roll.',
    'DEMO-LAB-3020': 'A sealed white bag of snap-on caps for tubes: a flat pouch with a small heap of loose blue snap-on caps on the floor beside it. The caps stand out clearly from the white background with a soft shadow. Not a tube with caps fitted.',
    'DEMO-LAB-3021': 'Four plain permanent markers lying side by side, each a smooth white barrel with a cap at the near end and a plain round tip at the far end. The caps are, from left to right, black, blue, red and green: exactly four markers, no others. Barrels completely unprinted. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-3022': 'A sealed white bag of 4 ml screw-cap tubes: a flat pouch with two tall clear tubes standing beside it, each with a white screw cap. The clear tubes stand out clearly from the white background with a soft shadow. Not a 50 ml conical tube: these have straight walls and a flat bottom.',
    'DEMO-LAB-3023': 'A plain white cardboard dispenser box of 200 lint-free lab wipes, standing on its base with a slot on top and white wipes pulled up through the slot. No printing on the box. Not a tissue box.',
    'DEMO-LAB-3024': 'A shallow white tray holding twenty tapered translucent off-white silicone stoppers standing upright in four rows of five, in five sizes, each stopper wider at the top than at the base. Solid stoppers, not spools, not coils, not caps. No labels or printing.',
}
