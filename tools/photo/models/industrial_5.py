"""Industrial pack, series 5: abrasives and consumables (DEMO-BRAKKWERK).

Abrasives in their real colours: corundum is brown or tan, the fleece is grey,
the sponge is pale green-grey, cutting discs are grey steel with a blue label area
left blank, the diamond disc has a steel body with dark segments. No lettering.
Most items lie flat on the floor, seen from above (pitch 50). Units mm; products
stand on z=0 with the front facing -Y.
"""
import math

CORUNDUM_BROWN = '#A8642E'
CORUNDUM_TAN = '#C9A36B'
CORUNDUM_DARK = '#7E4B26'
PAPER_CREAM = '#EFE6D6'
PAPER_TAN = '#D9C7A6'
CARD = '#C9AE86'
HUB = '#6B7078'
STEEL_BODY = '#A9B0B8'
SEGMENT = '#3E4248'
DISC_GREY = '#8E949C'
LABEL_BLUE = '#B9BEC5'   # label area on the cutting disc: plain light grey (no blue, reserved for tool makers)
FLEECE = '#B9B6AC'
FOAM = '#EAE3D0'
SPONGE = '#C9D3C2'
BORE = '#2A2D32'
FLAT = {'pitch': 50, 'fill': 0.8}


def flap_disc(k, colour=CORUNDUM_BROWN, n=2):
    """Flap disc, 125 mm, lying flat: a round fibreglass backing with a centre hole, and two overlapping rings of
    rectangular abrasive flaps laid like fish scales, each flap almost flat with its outer edge lifted slightly."""
    import math
    k.cyl(62.5, 1.6, (0, 0, 0.8), CARD, verts=96, rough=0.6)                          # fibreglass backing disc
    k.cyl(22, 0.6, (0, 0, 1.9), HUB, verts=48, rough=0.5)                              # centre hole ring
    k.cyl(9, 0.7, (0, 0, 2.0), BORE, verts=32, rough=0.6)                             # centre hole
    m = 32                                                                             # flaps per ring
    for layer, (dz, off) in enumerate(((2.8, 0.0), (3.6, 0.5))):
        for i in range(m):
            a = 360.0 * (i + off) / m
            R = 45
            x, y = R * math.cos(math.radians(a)), R * math.sin(math.radians(a))
            k.box((34, 14, 0.8), (x, y, dz), colour, rot=(0, -4, a), rough=0.7)     # one flat flap, outer edge lifted


def sanding_roll_layers(k, width, r):
    """Paper layers visible at both ends of the roll."""
    for sx in (-1, 1):
        x = sx * (width / 2 + 0.7)
        for rr in (r * 0.9, r * 0.72, r * 0.56):
            k.cyl(rr, 0.4, (x, 0, r), PAPER_TAN, rot=(0, 90, 0), verts=48, rough=0.9)


def belt_stack(k, colour=CORUNDUM_BROWN, n=5):
    """Five sanding belts, flat loops of abrasive cloth, lying as a neat pile."""
    pts = [(-305, -50), (305, -50), (305, 50), (-305, 50)]
    for i in range(n):
        dx, dy = (i - (n - 1) / 2) * 22, (i % 2) * 14 - 7                      # each belt shifted, so the five read as five
        k.slab([(x + dx, y + dy) for x, y in pts], 1.2, 1.2 * i, colour, smooth=0, round_=0.5)


def sheet_stack(k, colour=PAPER_CREAM):
    """A block of sanding sheets, 230 x 280 mm, stacked flat with the top sheet slightly turned."""
    k.box((230, 280, 11), (0, 0, 5.5), colour, bevel=0.6, rough=0.9)                # sheet pile
    k.box((228, 278, 0.5), (0, 0, 11.3), colour, bevel=0.2, rot=(0, 0, 4), rough=0.9)  # top sheet


def sanding_roll(k, width=115, r=36, colour=CORUNDUM_TAN):
    """Sanding paper on a cardboard core, lying on its side. Visible card core at both ends."""
    k.cyl(r, width, (0, 0, r), colour, rot=(0, 90, 0), verts=64, rough=0.8)
    for sx in (-1, 1):
        x = sx * (width / 2 + 0.4)
        k.cyl(r * 0.42, 1.0, (x, 0, r), CARD, rot=(0, 90, 0), verts=40, rough=0.9)  # core end
        k.cyl(r * 0.2, 1.2, (x, 0, r), BORE, rot=(0, 90, 0), verts=32, rough=0.9)   # core hole
    sanding_roll_layers(k, width, r)


def fleece_roll(k):
    """A roll of grey-beige abrasive fleece, 150 mm wide, lying on its side."""
    sanding_roll(k, width=150, r=50, colour=FLEECE)


def steel_cutting_discs(k, n=8, r=57.5, t=1.0):
    """A pile of thin grey cutting discs, the top one with a blue label area left blank."""
    for j in range(n):
        dx, dy = 0.9 * (j % 3 - 1), 0.6 * (j % 2)
        k.cyl(r, t, (dx, dy, j * t + t / 2), DISC_GREY, verts=72, metal=0.5, rough=0.4)
    dx, dy = 0.9 * ((n - 1) % 3 - 1), 0.6 * ((n - 1) % 2)
    z = n * t
    k.cyl(50, 0.15, (dx, dy, z + 0.05), LABEL_BLUE, verts=72, rough=0.6)            # label area, blank
    k.cyl(11, 0.25, (dx, dy, z + 0.12), BORE, verts=32, rough=0.6)                 # centre bore


def diamond_disc(k):
    """Diamond cutting disc, 230 mm: steel body, a central hub with bore and a ring of dark segments."""
    k.cyl(110, 2.2, (0, 0, 1.1), STEEL_BODY, verts=96, metal=0.9, rough=0.3)        # steel body
    k.cyl(22, 5.0, (0, 0, 4.7), STEEL_BODY, verts=48, metal=0.9, rough=0.3)         # hub
    k.cyl(10, 0.4, (0, 0, 7.3), BORE, verts=32, rough=0.6)                           # bore
    for i in range(10):
        a = 36 * i
        r = math.radians(a)
        x, y = 112 * math.cos(r), 112 * math.sin(r)
        k.box((28, 12, 9), (x, y, 4.5), SEGMENT, bevel=1.0, rot=(0, 0, a), rough=0.8)


def foam_pads(k):
    """Five foam polishing pads, 150 mm, each with a plastic backing hub, lying flat in two rows."""
    spots = [(-160, -60), (0, -60), (160, -60), (-80, 80), (80, 80)]
    for x, y in spots:
        k.cyl(75, 22, (x, y, 11), FOAM, verts=72, rough=0.95, bevel=2.0)            # foam pad
        k.cyl(22, 6, (x, y, 25), HUB, verts=48, rough=0.5, bevel=0.8)                # backing hub


def sanding_sponge(k):
    """A block of fine sanding sponge, 115 x 70 x 25 mm, soft rounded edges."""
    k.box((115, 70, 25), (0, 0, 12.5), SPONGE, bevel=5, rough=0.95)


SKUS = {
    'DEMO-IND-5001': (flap_disc, dict(colour=CORUNDUM_BROWN), {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-5002': (flap_disc, dict(colour=CORUNDUM_TAN), {'pitch': 50, 'fill': 0.8}),
    'DEMO-IND-5003': (belt_stack, {}, FLAT),
    'DEMO-IND-5004': (sheet_stack, dict(colour=PAPER_CREAM), {'pitch': 30, 'fill': 0.74}),
    'DEMO-IND-5005': (sheet_stack, dict(colour=PAPER_TAN), {'pitch': 30, 'fill': 0.74}),
    'DEMO-IND-5006': (sanding_roll, dict(width=115, r=36, colour=CORUNDUM_TAN), FLAT),
    'DEMO-IND-5007': (steel_cutting_discs, {}, {'pitch': 40, 'fill': 0.8}),
    'DEMO-IND-5008': (diamond_disc, {}, FLAT),
    'DEMO-IND-5009': (fleece_roll, {}, FLAT),
    'DEMO-IND-5010': (foam_pads, {}, FLAT),
    'DEMO-IND-5011': (sanding_roll, dict(width=93, r=34, colour=CORUNDUM_DARK), FLAT),
    'DEMO-IND-5012': (sanding_sponge, {}, {'pitch': 30, 'fill': 0.74}),
}

HINTS = {
    'DEMO-IND-5001': 'A flap disc 125 mm across lying flat: a round disc with a small centre hole, its face covered by two staggered rings of overlapping rectangular brown abrasive flaps, each flap lying flat and overlapping the next like roof tiles. Flaps are the defining feature, not a solid disc. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5002': 'A conical flap disc about 115 mm across, lying flat: a ring of overlapping tan abrasive flaps, each flap angled up from a grey plastic backing, around a small centre bore. The defining feature is the overlapping abrasive flaps, not a solid fibre disc. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5003': 'Five endless sanding belts, each a flat loop of brown abrasive cloth about 610 by 100 mm, with a visible butt-joint seam on the back, stacked neatly and slightly offset on the floor. Not a strip of paper and not a flat sheet: a closed loop. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5004': 'A block of fine sanding sheets, about 230 by 280 mm, a stack of cream paper-backed sheets, the top sheet slightly turned, each sheet face covered in a visible fine mineral grit texture. Not plain paper or card: the abrasive grit is visible on the face. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5005': 'A block of coarse sanding sheets, about 230 by 280 mm, a stack of tan paper-backed sheets, the top sheet slightly turned, each face covered in visible coarse P80 grit. Tan, not cream. Not plain kraft paper: the grit is visible on the face. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5006': 'A roll of brown-tan sanding paper about 115 mm wide, lying on its side on the floor: a tight roll of many paper layers, with the layer edges visible at each end and a cardboard core in the middle of each end. A single roll, no packaging, no printed text.',
    'DEMO-IND-5007': 'A stack of about eight thin grey steel cutting discs about 115 mm across, each with a small centre bore, the top disc with a plain light grey label area. Grey steel only, no blue colour anywhere. Not a saw blade. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5008': 'A diamond cutting disc 230 mm across, lying flat: a flat steel disc with a centre hole and a ring of separate dark diamond segments standing around the rim with clear gaps between them. The segments are separate raised blocks, not a solid disc with slots. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5009': 'A roll of grey-beige abrasive fleece about 150 mm wide, a soft fibrous non-woven pad material, lying on its side on the floor with a cardboard core visible at each end. Not a sponge: it is a rolled sheet with a flat fibrous surface.',
    'DEMO-IND-5010': 'Exactly five cream foam polishing pads about 150 mm across, each a thick round foam pad with a small grey plastic backing hub on top, lying flat in two rows (three and two). Count exactly five, not six. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-5011': 'A roll of dark brown coarse sanding paper about 93 mm wide, lying on its side on the floor, with a visible cardboard core at each end. Not a tape roll: the surface is a coarse abrasive grit and the core is open.',
    'DEMO-IND-5012': 'A single block of pale green-grey fine sanding sponge, about 115 by 70 by 25 mm, a soft rounded rectangular block with a slightly open textured surface, standing on the floor. Not a foam pad: it is a rectangular block with rounded edges.',
}
