"""Electrical pack, series 5: installation accessories.

Units mm. Everything stands or lies on z=0 with its front toward -Y. Boxes and
housings are plastic in light greys and whites; cable ties come in natural and
black; the ferrules and the conduit use plain light colours. No lettering on the
models. Flat items (ties, ferrule trays, trunking) are shot from above at a
steep pitch.
"""
import math

HOUSING = '#E4E7EA'
WHITE = '#F4F4F2'
MID = '#B9C0C8'
GREY = '#9AA1AB'
DARK = '#2B2E33'
TRAY = '#D8CBB0'
STEEL = '#A9AFB7'
TIE_NATURAL = '#E2DCC6'
TIE_BLACK = '#2B2E33'
FERRULE = {'grey': '#8E959E', 'red': '#C7362F', 'blue': '#2E5FA8', 'white': '#E4E7EA'}

FLAT = {'pitch': 50}


def flush_box(k, r=30, h=60):
    """Round flush-mounted device box lying on its side with the open front toward the camera."""
    k.cyl(r, h, (0, 0, r), HOUSING, rot=(90, 0, 0), bevel=1.5)
    k.cyl(r - 4, 1.5, (0, -h / 2 - 0.5, r), MID, rot=(90, 0, 0))                     # open front ring


def cavity_box(k):
    """Round cavity wall box with two fixing clamp bars on its sides."""
    r, h = 34, 42
    k.cyl(r, h, (0, 0, r), HOUSING, rot=(90, 0, 0), bevel=1.5)
    k.cyl(r - 4, 1.5, (0, -h / 2 - 0.5, r), MID, rot=(90, 0, 0))                     # open front ring
    for x in (-34, 34):
        k.box((8, 16, 6), (x, 0, r), MID, bevel=1)                                    # fixing clamp


def surface_housing(k):
    """Square surface-mounted single housing, IP44: white body, a recessed front panel."""
    k.box((84, 44, 84), (0, 0, 42), HOUSING, bevel=5, rough=0.4)
    k.box((70, 2, 70), (0, -22.5, 42), WHITE, bevel=2, rough=0.35)                  # recessed front panel
    for x in (-20, 20):
        k.cyl(5, 6, (x, 0, 84), MID, verts=24)                                       # knock-out nubs on top


def cable_ties(k, length=100, colour=TIE_NATURAL, width=7):
    """Sealed clear bag with a dense stack of ties inside, and three loose ties lying in front.
    Each loose tie is a flat strap with a locking head at one end, the head turned with the strap."""
    k.box((length + 14, 40, 14), (0, -22, 7), '#DDE3E8', alpha=0.3, rough=0.2, bevel=2)   # clear bag
    k.box((length - 10, 30, 8), (0, -22, 6), colour, bevel=0.8, rough=0.45)               # stack of ties inside
    for i, a in enumerate((-4, 0, 4)):
        y = 24 + i * (width + 2)
        k.box((length - 6, width, 1.5), (0, y, 0.75), colour,
              rot=(0, 0, a), bevel=0.4, rough=0.45)                                       # loose tie strap
        xh = -(length - 6) / 2 + 6                                                        # locking head, local x
        r = math.radians(a)
        k.box((9, width + 3, 4), (xh * math.cos(r), y + xh * math.sin(r), 2), colour,
              rot=(0, 0, a), bevel=0.8, rough=0.45)                                       # head on the strap


def trunking(k, w=40, h=25, length=420, colour=WHITE):
    """Straight cable trunking lying on its back: base, two walls and a snap-on lid."""
    k.box((length, w, 2), (0, 0, 1), colour, bevel=0.6, rough=0.4)                  # base
    for y in (-w / 2 + 1, w / 2 - 1):
        k.box((length, 2, h), (0, y, h / 2), colour, bevel=0.6, rough=0.4)          # walls
    k.box((length, w + 1, 3), (0, 0, h + 1.5), colour, bevel=1.2, rough=0.4)        # lid
    k.box((length - 40, 1, 0.8), (0, 0, h + 3.1), MID, rough=0.4)                   # lid groove


def conduit_coil(k, d=16, length=50):
    """Coil of corrugated flexible conduit: a flat drum of ribbed tube wound on itself, no hub.
    Each layer is a smooth tube with short ribs (rings round the tube, 6 degrees apart)."""
    r = d / 2
    layers = {16: 6, 20: 5, 25: 4}[d]
    colour = '#C9CED4'
    for i in range(layers):
        z = r + i * d
        k.torus(100, r, (0, 0, z), colour, rot=None)
        for j in range(60):
            t = j * 6
            tr = math.radians(t)
            k.cyl(r + 0.9, 3.0, (100 * math.cos(tr), 100 * math.sin(tr), z), colour,
                  rot=(90, 0, t + 180), verts=16)                                          # rib ring


def cable_gland(k, across=22, shank=8):
    """Plastic cable gland with a hex nut and a domed cap nut, standing upright, no cable."""
    cap_r = across / 2 * 0.9
    r_hex = across / 2 / math.cos(math.radians(30))
    k.cyl(shank, 24, (0, 0, 12), MID, verts=32)                                      # thread
    k.cyl(r_hex, 12, (0, 0, 12), GREY, verts=6, bevel=0.8, rough=0.35)               # hex nut
    k.cyl(cap_r, 22, (0, 0, 29), HOUSING, r2=cap_r * 0.7, bevel=1.5, rough=0.35)    # domed cap
    k.sphere(cap_r * 0.7, (0, 0, 40), HOUSING, scale=(1, 1, 0.45), rough=0.35)        # rounded top


def terminal_blocks(k, w=5.2, n=10):
    """Grey feed-through terminal blocks clipped side by side on a short top-hat rail lying on the
    floor, with a grey end plate. Each block is a thin slice in the real stepped profile: a foot that
    clips over the rail, a raised middle with a test opening, lower ends with the wire entry on the
    end face and the push-in opening on top."""
    rail_len = n * w + 2 + 40
    k.box((rail_len, 35, 1), (0, 0, 7.5), STEEL, metal=1, rough=0.3)                 # rail top
    for y in (-17, 17):
        k.box((rail_len, 1, 8), (0, y, 4), STEEL, metal=1, rough=0.3)               # rail sides
    x0 = -(n * w + 2) / 2
    for i in range(n + 1):
        end = i == n
        t = 2 if end else w - 0.3
        x = x0 + i * w + t / 2
        g = '#9EA4AC' if end else '#B4B9C0'
        k.box((t, 30, 6), (x, 0, 11), g, bevel=0.4, rough=0.5)                       # foot over the rail
        k.box((t, 56, 20), (x, 0, 24), g, bevel=0.6, rough=0.5)                      # body
        k.box((t, 24, 12), (x, 0, 40), g, bevel=0.6, rough=0.5)                      # raised middle
        if end:
            continue
        for y in (-1, 1):
            k.box((t * 0.6, 1, 6), (x, y * 28.2, 22), DARK, rough=0.6)              # wire entry, end face
            k.box((t * 0.6, 5, 1), (x, y * 19, 34.3), DARK, rough=0.6)              # push-in opening, top
        k.box((t * 0.45, 3, 1), (x, 0, 46.3), DARK, rough=0.6)                     # test opening


def ferrule_tray(k, colour='grey', r=2.4, length=14, metal_r=1.3):
    """Shallow open box of loose insulated wire ferrules, about a dozen lying in a loose heap."""
    w, d, h = 80, 56, 12
    k.box((w, d, 2), (0, 0, 1), TRAY, bevel=0.5, rough=0.5)                          # tray floor
    k.box((w, 2, h), (0, -d / 2, h / 2), TRAY, bevel=0.5, rough=0.5)                  # front wall
    k.box((w, 2, h), (0, d / 2, h / 2), TRAY, bevel=0.5, rough=0.5)                   # back wall
    for x in (-w / 2, w / 2):
        k.box((2, d, h), (x, 0, h / 2), TRAY, bevel=0.5, rough=0.5)                   # side walls
    sleeve = FERRULE[colour]
    pieces = [(-22, -15), (0, -16), (22, -14), (-30, 0), (-8, 0), (12, 2), (30, 1),
              (-20, 15), (2, 15), (24, 16), (-4, -2), (16, -4)]
    for i, (x, y) in enumerate(pieces):
        a = (i * 37) % 180
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        zc = 2 + r + (3 if i % 5 == 0 else 0)
        s = length * 0.6
        k.cyl(r, s, (x, y, zc), sleeve, rot=(0, 90, a), rough=0.4, bevel=0.3)        # insulating sleeve
        mx, my = x + ca * length * 0.5, y + sa * length * 0.5
        k.cyl(metal_r, length * 0.4, (mx, my, zc), STEEL, rot=(0, 90, a), metal=1, rough=0.2)  # metal tube


def connector_5(k):
    """Five-pole push-in junction connector: grey base, transparent cover, five lever clamps on top,
    one wire opening per pole on the front. About 60 x 30 x 22 mm, no rail, no bracket."""
    k.box((60, 30, 10), (0, 0, 5), HOUSING, bevel=1.5, rough=0.4)                        # grey base
    k.box((60, 30, 12), (0, 0, 16), '#D8DEE4', bevel=1.5, rough=0.15, alpha=0.45)         # transparent cover
    for i in range(5):
        x = -24 + 12 * i
        k.box((8, 6, 14), (x, -2, 27), MID, rot=(-30, 0, 0), bevel=1, rough=0.35)         # lever clamp, tilted
        k.box((6, 1, 6), (x, -15.2, 7), DARK, rough=0.5)                                  # wire opening, front


SKUS = {
    'DEMO-ELE-5001': (flush_box, {}),
    'DEMO-ELE-5002': (cavity_box, {}),
    'DEMO-ELE-5003': (surface_housing, {}),
    'DEMO-ELE-5004': (cable_ties, {'length': 100, 'colour': TIE_NATURAL, 'width': 6}, FLAT),
    'DEMO-ELE-5005': (cable_ties, {'length': 200, 'colour': TIE_BLACK, 'width': 8}, FLAT),
    'DEMO-ELE-5006': (cable_ties, {'length': 300, 'colour': TIE_NATURAL, 'width': 10}, FLAT),
    'DEMO-ELE-5007': (trunking, {'w': 40, 'h': 25}, {'pitch': 40}),
    'DEMO-ELE-5008': (trunking, {'w': 60, 'h': 40}, {'pitch': 40}),
    'DEMO-ELE-5009': (conduit_coil, {'d': 16}),
    'DEMO-ELE-5010': (conduit_coil, {'d': 20}),
    'DEMO-ELE-5011': (conduit_coil, {'d': 25}),
    'DEMO-ELE-5012': (cable_gland, {'across': 22, 'shank': 8}),
    'DEMO-ELE-5013': (cable_gland, {'across': 26, 'shank': 10}),
    'DEMO-ELE-5014': (cable_gland, {'across': 32, 'shank': 12.5}),
    'DEMO-ELE-5015': (terminal_blocks, {'w': 5.2}, {'yaw': -72, 'pitch': 22}),
    'DEMO-ELE-5016': (terminal_blocks, {'w': 5.2}, {'yaw': -72, 'pitch': 22}),
    'DEMO-ELE-5017': (terminal_blocks, {'w': 6.2}, {'yaw': -72, 'pitch': 22}),
    'DEMO-ELE-5018': (terminal_blocks, {'w': 8.2}, {'yaw': -72, 'pitch': 22}),
    'DEMO-ELE-5019': (ferrule_tray, {'colour': 'grey', 'r': 2.4, 'length': 14, 'metal_r': 1.3}, FLAT),
    'DEMO-ELE-5020': (ferrule_tray, {'colour': 'red', 'r': 2.4, 'length': 14, 'metal_r': 1.3}, FLAT),
    'DEMO-ELE-5021': (ferrule_tray, {'colour': 'blue', 'r': 2.4, 'length': 14, 'metal_r': 1.3}, FLAT),
    'DEMO-ELE-5022': (connector_5, {}),
    'DEMO-ELE-5023': (ferrule_tray, {'colour': 'white', 'r': 3.4, 'length': 18, 'metal_r': 2.0}, FLAT),
}

HINTS = {
    'DEMO-ELE-5001': 'A round flush-mounted device box made of light grey plastic, about 6 cm across and 6 cm deep, lying on its side so its open front faces the camera, with a slightly darker grey ring inside the opening and a flat rounded back. The whole product visible, standing out clearly from the white background with a soft shadow. Not a surface housing, not a cable gland, not a tin can.',
    'DEMO-ELE-5002': 'A round grey plastic cavity wall box, shaped like a short cup: a flat round rim around a deep round opening, lying on its side with the opening facing the camera, and two small fixing clamp wings sticking out at the sides. The whole product visible, standing out clearly from the white background with a soft shadow. Not a flush box without clamps, not a surface housing, not a tin can.',
    'DEMO-ELE-5003': 'A square surface-mounted housing for one switch, made of white plastic, about 8 by 8 cm and 4 cm deep, standing on its back on the floor, with a slightly recessed front panel and two small knock-out nubs on top. The whole product visible, standing out clearly from the white background with a soft shadow. Not a flush-mounted box, not a distribution board, not a wall socket.',
    'DEMO-ELE-5004': 'A pack of 100 natural cream-white nylon cable ties, 100 mm long: a clear sachet with a dense stack of ties inside, and three loose ties lying in front. Each tie is a flat strap with a locking head at one end and a pointed tip at the other. Not rods, not straws, not hook-and-loop. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-5005': 'A pack of 100 black nylon cable ties, 200 mm long: a clear sachet with a dark stack of ties inside, and three loose black ties lying in front. Each tie is a flat strap with a locking head at one end. Not rods, not foam tubing. The whole pack visible from above. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-5006': 'A pack of 100 natural nylon cable ties, 300 mm long and 10 mm wide: a clear sachet with a stack of ties inside, and three loose long broad ties lying in front. Each tie is a flat strap with a locking head at one end. Not a hook-and-loop strap, not a fabric strap. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-5007': 'A straight length of white plastic cable trunking, about 4 by 2.5 cm in section, lying on its back on the floor with a flat snap-on lid on top and a thin groove along the lid. The whole length visible from one end, standing out clearly from the white background with a soft shadow. Not a wooden board, not a cable, not a metal rail.',
    'DEMO-ELE-5008': 'A straight length of white plastic cable trunking, about 6 by 4 cm in section, lying on its back on the floor with a flat snap-on lid on top and a thin groove along the lid. The whole length visible from one end, standing out clearly from the white background with a soft shadow. Not a wooden board, not a cable, not a metal rail. Larger than the small trunking.',
    'DEMO-ELE-5009': 'A coil of corrugated grey plastic flexible conduit, 16 mm tube, 50 m: a ribbed tube wound flat into a round drum with a hollow centre, the ribs visible all round the tube. No hub, no sleeve, no smooth tube. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-5010': 'A coil of corrugated grey plastic flexible conduit, 20 mm tube, 50 m: a ribbed tube wound flat into a round drum with a hollow centre, the ribs visible all round the tube. No hub, no sleeve, no smooth tube. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-5011': 'A coil of corrugated grey plastic flexible conduit, 25 mm tube, 50 m: a ribbed tube wound flat into a round drum with a hollow centre, the ribs visible all round the tube. No hub, no sleeve, no smooth tube. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-5012': 'A plastic cable gland for a 16 mm thread, standing upright: a light grey threaded base, a grey hex nut and a light grey domed cap nut on top, with no cable inserted. The whole product visible, standing out clearly from the white background with a soft shadow. Not a metal fitting, not a valve, not a bolt.',
    'DEMO-ELE-5013': 'A plastic cable gland for a 20 mm thread, standing upright: a light grey threaded base, a grey hex nut and a light grey domed cap nut on top, with no cable inserted. The whole product visible, standing out clearly from the white background with a soft shadow. Not a metal fitting, not a valve, not a bolt. Larger than the 16 mm gland.',
    'DEMO-ELE-5014': 'A plastic cable gland for a 25 mm thread, standing upright: a light grey threaded base, a grey hex nut and a light grey domed cap nut on top, with no cable inserted. The whole product visible, standing out clearly from the white background with a soft shadow. Not a metal fitting, not a valve, not a bolt. The largest of the three glands.',
    'DEMO-ELE-5015': 'Ten identical thin grey terminal blocks clipped side by side on a steel top-hat rail, seen from the side: each block is a very thin slice only 5 mm wide and taller than it is wide, a slim plastic plate with a small clip foot, so the row is long and narrow with clear gaps of shadow between the slices. No bulky housing, no ribs, no chunky box. No labels or printing.',
    'DEMO-ELE-5016': 'Ten identical thin grey terminal blocks clipped side by side on a steel top-hat rail, seen from the side: each block is a very thin slice only 5 mm wide and taller than it is wide, a slim plastic plate with a small clip foot, so the row is long and narrow with clear gaps of shadow between the slices. No bulky housing, no ribs, no chunky box. No labels or printing.',
    'DEMO-ELE-5017': 'Ten identical thin grey terminal blocks clipped side by side on a steel top-hat rail, seen from the side: each block is a very thin slice only 6 mm wide and taller than it is wide, a slim plastic plate with a small clip foot, so the row is long and narrow with clear gaps of shadow between the slices. No bulky housing, no ribs, no chunky box. No labels or printing.',
    'DEMO-ELE-5018': 'Ten identical thin grey terminal blocks clipped side by side on a steel top-hat rail, seen from the side: each block is a thin slice 8 mm wide and taller than it is wide, a slim plastic plate with a small clip foot, so the row is long and narrow with clear gaps of shadow between the slices. No bulky housing, no ribs, no chunky box. No labels or printing.',
    'DEMO-ELE-5019': 'A shallow open cardboard-coloured tray of loose insulated wire ferrules, a dozen lying in a loose heap: each a short grey plastic sleeve with a small shiny metal tube at one end. The whole tray visible from above, standing out clearly from the white background with a soft shadow. Not a screw, not a pin, not a wire, not a rivet.',
    'DEMO-ELE-5020': 'A shallow open cardboard-coloured tray of loose insulated wire ferrules, a dozen lying in a loose heap: each a short red plastic sleeve with a small shiny metal tube at one end. The whole tray visible from above, standing out clearly from the white background with a soft shadow. Not a screw, not a pin, not a wire, not a rivet.',
    'DEMO-ELE-5021': 'A shallow open cardboard-coloured tray of loose insulated wire ferrules, a dozen lying in a loose heap: each a short blue plastic sleeve with a small shiny metal tube at one end. The whole tray visible from above, standing out clearly from the white background with a soft shadow. Not a screw, not a pin, not a wire, not a rivet.',
    'DEMO-ELE-5022': 'A five-pole push-in junction connector: a compact light grey block about 6 cm long and 3 cm wide, with a transparent cover, five small lever clamps in a row on top and one wire opening per pole on the front face. Not a DIN-rail terminal, not a comb, no rail, no bracket. Standing alone on the floor, the whole product visible and standing out clearly from the white background with a soft shadow. Not a fuse, not a plug, not a single screw terminal. No labels or printing.',
    'DEMO-ELE-5023': 'A pack of wire end ferrules, a shallow open cardboard-coloured tray of loose white plastic-insulated ferrules, a dozen lying in a loose heap, each a short white sleeve with a small shiny metal tube at one end, bigger than the small ferrules. The whole tray visible from above, standing out clearly from the white background with a soft shadow. Not a screw, not a pin, not a wire, not a rivet.',
}
