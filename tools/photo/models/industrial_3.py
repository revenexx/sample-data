"""Industrial pack, series 3: workwear and safety.

Gloves lie flat, palm up, fingers pointing away from the camera and the cuff towards it.
Clothing lies flat too (vest, jacket, apron). Eye, ear and head protection stands upright.
Units mm; products stand on z=0 with the front facing -Y.
"""
import math

HI_VIS = '#F26B1D'      # fluorescent orange
YELLOW = '#F2C200'      # rain jacket yellow
REFLECT = '#D9DEE4'     # reflective strip, pale silver
GREY_KNIT = '#B9BEC5'   # grey knit liner
BLACK = '#2B2E33'       # black coating and plastic
GREEN_COAT = '#2E8B4A'  # green nitrile coating
BLUE = '#2A5DA8'        # blue nitrile
LEATHER = '#8B5A2B'     # cowhide
LEATHER_DARK = '#6E4422'
STEEL_MESH = '#CFD3D8'
PLASTIC_WHITE = '#F7F7F5'
GREY_PLASTIC = '#A9B0B9'
FOAM = '#E3A93B'        # foam ear plugs
FLAT = {'pitch': 50}    # camera for garments and gloves lying on the floor


def _ring_mesh(o, ring=4.0):
    """Give o a chainmail look in the studio render: a fine regular grid of bright
    steel rings round small dark holes, so the AI step starts from metal mesh and not from cloth."""
    import bpy
    m = o.data.materials[0].copy()
    o.data.materials[0] = m
    nt = m.node_tree
    b = nt.nodes['Principled BSDF']
    v = nt.nodes.new('ShaderNodeTexVoronoi')
    v.feature = 'DISTANCE_TO_EDGE'
    v.inputs['Scale'].default_value = 1.0 / ring
    v.inputs['Randomness'].default_value = 0.0                  # a regular grid, like woven rings
    tc = nt.nodes.new('ShaderNodeTexCoord')
    nt.links.new(tc.outputs['Object'], v.inputs['Vector'])
    ramp = nt.nodes.new('ShaderNodeValToRGB')
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.22, (0.86, 0.87, 0.89, 1)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.3, (0.12, 0.12, 0.13, 1)
    nt.links.new(v.outputs['Distance'], ramp.inputs['Fac'])
    nt.links.new(ramp.outputs['Color'], b.inputs['Base Color'])


def _bar(p0, p1, w):
    """Rectangle of width w along the segment p0 -> p1 (an outline for k.slab)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    return [(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny),
            (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)]


def _ell(cx, cy, a, b, n=32):
    return [(cx + a * math.cos(2 * math.pi * i / n), cy + b * math.sin(2 * math.pi * i / n)) for i in range(n)]


def _arch(r_out, r_in, cz, n=24):
    """Half ring over the floor: outline (x, z) for a headband, centred on (0, cz)."""
    outer = [(r_out * math.cos(math.pi * i / n), cz + r_out * math.sin(math.pi * i / n)) for i in range(n + 1)]
    inner = [(r_in * math.cos(math.pi * i / n), cz + r_in * math.sin(math.pi * i / n)) for i in range(n, -1, -1)]
    return outer + inner


# ---------------------------------------------------------------- gloves

def glove(k, back, coat=None, cuff=None, cuff_len=30, metal=0.0, rough=0.5, gap=110, single=False, rings=False):
    """A pair of gloves lying flat side by side, seen from above: each a palm, four fingers,
    a thumb on the inner side and a cuff band. The right hand is the mirror image of the left.
    coat paints a layer over the palm and fingers (nitrile coating). gap is each glove's distance from the
    middle; the thumbs point inward, so below about 150 they nearly touch. single draws one glove in the
    middle (gloves sold one at a time). rings gives it a chainmail texture."""
    mk = dict(metal=metal, rough=rough)
    palm = [(0, -120), (44, -120), (46, -60), (48, -30), (46, 0), (44, 50), (0, 56)]
    full_palm = palm + [(-x, y) for x, y in reversed(palm) if x > 0]
    fingers = ((33, 72), (11, 82), (-11, 78), (-33, 66))
    thumb = _bar((40, -20), (100, 40), 22)
    for ox, flip in ((0, 1),) if single else ((-gap, 1), (gap, -1)):
        def T(pts, ox=ox, flip=flip):
            return [(ox + flip * x, y) for x, y in pts]
        parts = [k.slab(T(full_palm), 8, 0, back, **mk)]
        for x, length in fingers:
            parts.append(k.slab(T(_bar((x, 45), (x, 45 + length), 19)), 8, 0.3, back, round_=4, **mk))
        parts.append(k.slab(T(thumb), 8, 0.3, back, round_=5, **mk))
        if coat:
            k.slab(T(full_palm), 2.5, 7.5, coat, round_=1.2)
            for x, length in fingers:
                k.slab(T(_bar((x, 45), (x, 45 + length), 17)), 2.5, 7.5, coat, round_=1.2)
        if cuff_len:
            parts.append(k.slab(T(_bar((0, -119), (0, -120 - cuff_len), 84)), 8, 0, cuff or back, round_=3, **mk))
        for o in parts if rings else ():
            _ring_mesh(o)


def _family(base, kw):
    out = {base: (glove, kw, FLAT)}
    for size in ('S', 'M', 'L', 'XL'):
        out[f'{base}-{size}'] = (glove, kw, FLAT)
    return out


# ---------------------------------------------------------------- eyes, ears, head, face

def safety_glasses(k, tint=None):
    """Glasses standing on their temple arms, lens plane facing -Y."""
    lens, alpha = ('#CFE3F0', 0.3) if tint is None else (tint, 0.55)
    for s in (-1, 1):
        x = 40 * s
        k.sphere(38, (x, 1, 44), BLACK, scale=(1, 0.05, 0.66))                     # rim
        k.sphere(34, (x, -1, 44), lens, scale=(1, 0.06, 0.62), alpha=alpha)        # lens
        k.box((4, 120, 4), (78 * s, 60, 44), BLACK)                                 # temple arm
        k.box((4, 8, 40), (78 * s, 116, 24), BLACK)                                 # tip down to floor
    k.box((12, 4, 4), (0, 0, 50), BLACK)                                            # bridge
    for s in (-1, 1):
        k.box((4, 34, 62), (88 * s, 22, 44), BLACK, bevel=1)                        # moulded side shield at each temple


def ear_defenders(k):
    """Ear defenders shaped like big over-ear headphones, standing upright: two oval cups whose
    axis is horizontal (facing each other, cushions inward), each standing on its lower edge, and
    one padded headband arching high over the top from cup to cup."""
    for s in (-1, 1):
        cup = k.cyl(42, 34, (62 * s, 0, 58), '#3B3E43', rot=(0, 90, 0), bevel=4)       # shell, axis along X
        cup.scale = (1, 0.82, 1.3)                                                      # oval: taller than wide
        cush = k.cyl(36, 14, (40 * s, 0, 58), BLACK, rot=(0, 90, 0), bevel=5)          # black cushion, inward
        cush.scale = (1, 0.82, 1.3)
        k.box((8, 14, 40), (70 * s, 0, 122), GREY_PLASTIC, bevel=2)                    # slider into the band
    k.profile(_arch(74, 62, 138), 26, y=0, color=BLACK, round_=10)                    # one padded headband


def helmet(k):
    """A white hard shell, dome-shaped in side view, with a ridge along the top."""
    dome = [(115 * math.cos(math.pi * i / 24), 115 * math.sin(math.pi * i / 24)) for i in range(25)]
    k.profile(dome, 180, y=0, color=PLASTIC_WHITE, round_=45)
    k.box((14, 150, 14), (0, 0, 112), PLASTIC_WHITE, bevel=3)                       # ridge


def face_shield(k):
    """A clear visor hung in front of a headband arch that stands on the floor."""
    k.profile(_arch(110, 100, 0), 12, y=60, color=BLACK, round_=4)                  # headband
    visor = [(-100, 20), (100, 20), (100, 120), (0, 140), (-100, 120)]
    k.profile(visor, 1.5, y=-40, color='#E6F2F7', alpha=0.3)                        # visor sheet


def earplug_box(k):
    """A grey plastic dispenser, open at the top, with orange foam plugs and cords."""
    k.box((130, 80, 60), (0, 0, 30), GREY_PLASTIC, bevel=3)
    k.box((110, 60, 2), (0, 0, 60.5), BLACK)
    for x in (-40, 0, 40):
        for y in (-15, 15):
            k.cyl(8, 12, (x, y, 64), FOAM, bevel=1)
    for y in (-15, 15):
        k.cyl(0.8, 110, (0, y, 70.5), '#E8E8E8', rot=(0, 90, 0))                    # cords


# ---------------------------------------------------------------- garments

def hi_vis_vest(k):
    """Sleeveless vest, lying flat: front zip line, two reflective strips."""
    body = [(0, -150), (130, -150), (132, -100), (128, 20), (100, 90), (60, 130), (30, 150), (0, 140)]
    k.slab(body, 4, 0, HI_VIS, mirror=True, round_=1.5)
    k.box((236, 12, 2), (0, -40, 5), REFLECT)
    k.box((236, 12, 2), (0, -80, 5), REFLECT)
    k.box((2.5, 280, 1), (0, -5, 4.5), '#A9AFB7')                                    # zip


def rain_jacket(k):
    """Hooded rain jacket, lying flat with sleeves spread out and the hood at the top."""
    k.slab([(0, -190), (125, -190), (128, -60), (125, 60), (0, 70)], 10, 0, YELLOW, mirror=True, round_=3)
    k.slab([(0, 60), (95, 70), (118, 150), (100, 230), (40, 262), (0, 255)], 10, 0.6, YELLOW,
           mirror=True, round_=3)
    k.slab(_bar((95, 50), (215, -160), 92), 10, 0.6, YELLOW, round_=3)
    k.slab(_bar((-95, 50), (-215, -160), 92), 10, 0.6, YELLOW, round_=3)


def welding_apron(k):
    """Leather welding apron, lying flat: bib, long neck strap, two waist ties."""
    k.slab([(0, -330), (235, -330), (240, -260), (240, 240), (120, 300), (0, 300)], 6, 0, LEATHER,
           mirror=True, round_=2)
    k.slab(_bar((-60, 300), (-60, 420), 22), 6, 0, LEATHER, round_=2)
    k.slab(_bar((60, 300), (60, 420), 22), 6, 0, LEATHER, round_=2)
    k.slab(_bar((230, -250), (330, -250), 18), 6, 0, LEATHER, round_=2)
    k.slab(_bar((-230, -250), (-330, -250), 18), 6, 0, LEATHER, round_=2)


def knee_pads(k):
    """A pair of hard plastic knee caps with grey gel inside and straps."""
    for s in (-1, 1):
        cx = 95 * s
        k.slab(_ell(cx, 0, 75, 85), 24, 0, BLACK, round_=10)
        k.slab(_ell(cx, 0, 55, 60), 6, 24, '#6B7480', round_=2)                    # gel cushion
        k.slab(_bar((cx + 70 * s, 0), (cx + 200 * s, 0), 26), 4, 0, GREY_PLASTIC, round_=1)


# ---------------------------------------------------------------- other

def barrier_tape(k):
    """A 500 m roll of red-white barrier tape (80 mm wide) standing on its round edge, wound on a cardboard core,
    with a short length unrolled flat along the floor. Like real tape (Absperrband, "schraffiert"): diagonal red
    and white stripes at 45 degrees across the tape, on the outside of the roll and on the loose end."""
    import bpy
    R, rc, w = 82, 38, 80                                                           # roll radius, core radius, tape width
    zc = R

    def striped(name, coord):
        """Material: 45 degree red/white stripes, 30 mm period, from a coordinate expression on object space."""
        m = bpy.data.materials.new(name); m.use_nodes = True
        nt = m.node_tree; b = nt.nodes['Principled BSDF']; b.inputs['Roughness'].default_value = 0.45
        tc = nt.nodes.new('ShaderNodeTexCoord'); sx = nt.nodes.new('ShaderNodeSeparateXYZ')
        nt.links.new(tc.outputs['Object'], sx.inputs[0])
        u = coord(nt, sx)
        P = 2 * math.pi * R / 11                                                    # period about 47 mm, a whole number round the roll (no seam)
        f = nt.nodes.new('ShaderNodeMath'); f.operation = 'WRAP'; f.inputs[1].default_value = 0; f.inputs[2].default_value = P
        nt.links.new(u, f.inputs[0])
        g = nt.nodes.new('ShaderNodeMath'); g.operation = 'GREATER_THAN'; g.inputs[1].default_value = P / 2
        nt.links.new(f.outputs[0], g.inputs[0])
        mix = nt.nodes.new('ShaderNodeMix'); mix.data_type = 'RGBA'
        mix.inputs[6].default_value = lib_rgb('#D9342B'); mix.inputs[7].default_value = lib_rgb('#F4F4F2')
        nt.links.new(g.outputs[0], mix.inputs[0]); nt.links.new(mix.outputs[2], b.inputs['Base Color'])
        m.diffuse_color = lib_rgb('#E08A84')
        return m

    def lib_rgb(h):
        return k.rgb(h)

    def add(nt, a, b_, op='ADD'):
        n = nt.nodes.new('ShaderNodeMath'); n.operation = op
        nt.links.new(a, n.inputs[0])
        if isinstance(b_, (int, float)): n.inputs[1].default_value = b_
        else: nt.links.new(b_, n.inputs[1])
        return n.outputs[0]

    def around(nt, sx):                                                             # arc length round the roll + position across the tape
        at = nt.nodes.new('ShaderNodeMath'); at.operation = 'ARCTAN2'
        nt.links.new(sx.outputs[1], at.inputs[0]); nt.links.new(sx.outputs[0], at.inputs[1])   # local circle plane is X-Y
        return add(nt, add(nt, at.outputs[0], R, 'MULTIPLY'), sx.outputs[2])

    def flat(nt, sx):
        return add(nt, sx.outputs[0], sx.outputs[1])

    roll = k.cyl(R, w, (0, 0, 0), '#F4F4F2', rot=(90, 0, 0), verts=128)          # the roll, axis across (Y)
    roll.data.materials.clear(); roll.data.materials.append(striped('tape_roll', around))
    roll.location = (0, 0, zc)
    for sgn in (-1, 1):
        k.cyl(R - 1.5, 0.6, (0, sgn * (w / 2 + 0.3), zc), '#EEE6E4', rot=(90, 0, 0), verts=128)   # side face: the wound tape edges
        k.cyl(rc + 5, 0.8, (0, sgn * (w / 2 + 0.6), zc), '#B98A55', rot=(90, 0, 0), verts=64)    # cardboard core rim
        k.cyl(rc, 1.0, (0, sgn * (w / 2 + 0.8), zc), '#3A3530', rot=(90, 0, 0), verts=64)        # the open bore
    tail = k.box((300, w, 0.4), (-150, 0, 0.2), '#F4F4F2')                        # the loose end, unrolled flat on the floor
    tail.data.materials.clear(); tail.data.materials.append(striped('tape_flat', flat))


def dust_masks(k):
    """A plain white box with two flat cup-shaped FFP2 masks lying in front, each with a metal nose clip and no valve."""
    k.box((220, 110, 50), (0, 60, 25), PLASTIC_WHITE, bevel=2)
    for cx in (-80, 80):
        k.slab(_ell(cx, -80, 68, 62, 24), 10, 0, '#EEF1F4', round_=4)
        k.box((50, 6, 6), (cx, -96, 60), GREY_PLASTIC, bevel=1)                    # metal nose clip along the top edge


# ---------------------------------------------------------------- SKU table

SKUS = {
    'DEMO-IND-3002': (safety_glasses, {}),
    'DEMO-IND-3003': (ear_defenders, {}),
    'DEMO-IND-3004': (helmet, {}),
    'DEMO-IND-3005': (earplug_box, {}),
    'DEMO-IND-3006': (safety_glasses, {'tint': '#4A4E55'}),
    'DEMO-IND-3007': (face_shield, {}),
    'DEMO-IND-3008': (hi_vis_vest, {}, FLAT),
    'DEMO-IND-3009': (welding_apron, {}, FLAT),
    'DEMO-IND-3015': (knee_pads, {}, FLAT),
    'DEMO-IND-3016': (barrier_tape, {}, {'pitch': 24, 'yaw': -38}),
    'DEMO-IND-3017': (rain_jacket, {}, FLAT),
    'DEMO-IND-3018': (dust_masks, {}, FLAT),
}
SKUS.update(_family('DEMO-IND-3001', dict(back=GREY_KNIT, coat=BLACK, cuff=GREY_KNIT)))
SKUS.update(_family('DEMO-IND-3010', dict(back=BLUE, coat='#1F4A8A', cuff=BLUE)))
SKUS.update(_family('DEMO-IND-3011', dict(back=LEATHER, cuff=LEATHER)))
SKUS.update(_family('DEMO-IND-3012', dict(back=STEEL_MESH, cuff=STEEL_MESH, metal=0.9, rough=0.3, single=True, rings=True)))
SKUS.update(_family('DEMO-IND-3013', dict(back=GREY_KNIT, coat=GREEN_COAT, cuff=GREY_KNIT)))
SKUS.update(_family('DEMO-IND-3014', dict(back=LEATHER, cuff=LEATHER_DARK, cuff_len=160)))

_GLOVE_3001 = ('A pair of cut-resistant work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: a grey knit liner on the back '
               'of the hand and fingers, a black nitrile coating across the palm and fingers, and a short knit cuff. '
               'Not a leather glove: the back is visibly knitted. No logo, no emblem on the cuff.')
_GLOVE_3010 = ('A pair of thin blue nitrile assembly gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: smooth close-fitting blue '
               'material with a darker textured grip coating on the palm and fingers, and a short cuff. Not a leather '
               'glove: thin and smooth. No logo, no emblem on the cuff.')
_GLOVE_3011 = ('A pair of brown cowhide leather work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: leather back and palm, '
               'slightly darker reinforced fingertips, and a short leather cuff. Not a welding glove: no long gauntlet. '
               'No logo, no emblem.')
_GLOVE_3012 = ('A pair of silver stainless steel chainmail mesh gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions and a short mesh cuff. '
               'Shiny interlinked metal rings, not fabric. Not a leather glove.')
_GLOVE_3013 = ('A pair of cut-resistant work gloves, grey knit liner with a bright green nitrile coating across the palm '
               'and fingers, and a short knit cuff, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions. Not the black coated gloves: the '
               'coating is green. No logo, no emblem on the cuff.')
_GLOVE_3014 = ('A pair of long welding gauntlets in brown cowhide leather, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions, with a very '
               'long leather cuff reaching far up the wrist. Not a short work glove: the gauntlet is very long. No logo.')

HINTS = {
    'DEMO-IND-3002': 'A pair of clear safety glasses standing on their temple arms: two transparent colourless lenses, one per eye, in a thin dark frame with a bridge, and a moulded black side shield at each temple where the arm joins. Not sunglasses: the lenses are clear. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-3003': 'Ear defenders shaped like a pair of large over-ear headphones, standing upright on the two cups, seen from the front left: two big oval padded ear cups in anthracite grey with thick black cushions facing each other, joined by one curved padded headband arching over the top, with small sliders where the band meets each cup. Passive hearing protection, so no cable and no buttons. No labels or printing.',
    'DEMO-IND-3004': 'A white safety helmet standing upright: a smooth hard shell, dome-shaped, with a raised ridge '
                     'along the top. Not a bicycle helmet: no vents and no visor. No logo, no emblem.',
    'DEMO-IND-3005': 'A grey plastic dispenser box, open at the top, with orange foam ear plugs standing in it and '
                     'thin cords hanging over the rim. Not earbuds: the plugs are tapered orange foam cylinders.',
    'DEMO-IND-3006': 'A pair of safety glasses with exactly two smoky grey tinted lenses, one per eye, joined by a bridge, with moulded black side shields at each temple. Dark thin frame, standing on the temple arms. Not fashion sunglasses: sporty and wrapped around the eyes. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-3007': 'A face shield standing upright: a clear polycarbonate visor sheet hung in front of a black '
                     'headband arch that rests on the floor. The visor is a flat transparent sheet. Not a mask: no '
                     'fabric and no mouth cover.',
    'DEMO-IND-3008': 'A high-visibility vest in fluorescent orange, lying flat, sleeveless with armholes and a V-neck, '
                     'with a front zip line and two horizontal pale silver reflective strips across the body. No logo, '
                     'no emblem on the chest, no lettering.',
    'DEMO-IND-3009': 'A welding apron in brown cowhide leather, lying flat: a rectangular bib with a long neck strap '
                     'and two waist ties, stitched edges. Not a kitchen apron: heavy leather, no pockets. No logo, no '
                     'emblem.',
    'DEMO-IND-3010': 'A pair of thin blue nitrile assembly gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: smooth close-fitting blue material with a darker textured grip coating on the palm and fingers, and a short cuff. Not a leather glove: thin and smooth. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3011': 'A pair of brown cowhide leather work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: leather back and palm, slightly darker reinforced fingertips, and a short leather cuff. Not a welding glove: no long gauntlet. No logo, no emblem. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3012': "One single stainless steel chainmail butcher's glove, sold individually and fitting either hand, lying flat on its own, palm down, seen from above: a limp glove made entirely of thousands of tiny interlinked steel rings that drapes like fabric, with a short mesh cuff. It has exactly five separate fingers: one thumb and four fingers, anatomically correct, slightly spread so all five are clearly visible and countable. Only one glove, no second glove, no hand or arm inside it. Not a rigid metal hand, not a robot hand, no leather, no fabric parts, no plates. No labels or printing.",
    'DEMO-IND-3013': 'A pair of cut-resistant work gloves, grey knit liner with a bright green nitrile coating across the palm and fingers, and a short knit cuff, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions. Not the black coated gloves: the coating is green. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3014': 'A pair of long welding gauntlets in brown cowhide leather, lying flat side by side and not overlapping, palms down, seen from above at an angle. Each gauntlet is straight, not folded or bent: a glove with five fingers ending in one long, slightly flared leather cuff reaching far up the forearm. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing.',
    'DEMO-IND-3015': 'A pair of black knee pads lying flat on the floor, ready to use, with the straps opened and laid out straight to the side: '
                     'two hard rounded caps with a grey gel cushion inside. Not a sports brace: no sleeve, no person, no logo.',
    'DEMO-IND-3016': 'A large roll of red and white plastic barrier tape (warning tape), 80 mm wide, standing on its round edge on the floor, wound tightly on a brown cardboard core with an open round hole in the middle, and a length of the tape unrolled flat along the floor towards the front. The tape has evenly spaced diagonal red and white stripes at 45 degrees across its width, exactly like real hazard barrier tape, on the outside of the roll and on the unrolled end. The flat side of the roll shows the thin wound tape edges. Thin shiny polyethylene film, not fabric and not a ribbon. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-3017': 'A yellow waterproof rain jacket lying flat with its long sleeves spread out to the sides and the '
                     'hood folded at the top. Smooth nylon, taped seams. Not a vest: it has full sleeves. No logo, no '
                     'emblem on the chest, no lettering.',
    'DEMO-IND-3018': 'A plain white cardboard box of disposable FFP2 dust masks, with two flat white cup-shaped masks lying in front. Each mask has a metal nose clip along its top edge and no valve. The box is plain white with no lettering. Not a surgical mask: stiff cup shape. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-3001': 'A pair of cut-resistant knit work gloves lying flat side by side, one palm up and one palm down so the coated palm shows: a grey knit back with a grey ribbed cuff, and a palm coated with a dipped nitrile layer with a sandy foam finish, clearly different from the knit back. Each glove has exactly five fingers. Not soft-shell, not thermal, not ski gloves. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-3001-S': 'A pair of cut-resistant work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: a grey knit liner on the back of the hand and fingers, a black nitrile coating across the palm and fingers, and a short knit cuff. Not a leather glove: the back is visibly knitted. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3001-M': 'A pair of cut-resistant work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: a grey knit liner on the back of the hand and fingers, a black nitrile coating across the palm and fingers, and a short knit cuff. Not a leather glove: the back is visibly knitted. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3001-L': 'A pair of cut-resistant work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: a grey knit liner on the back of the hand and fingers, a black nitrile coating across the palm and fingers, and a short knit cuff. Not a leather glove: the back is visibly knitted. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3001-XL': 'A pair of cut-resistant work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: a grey knit liner on the back of the hand and fingers, a black nitrile coating across the palm and fingers, and a short knit cuff. Not a leather glove: the back is visibly knitted. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3010-S': 'A pair of thin blue nitrile assembly gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: smooth close-fitting blue material with a darker textured grip coating on the palm and fingers, and a short cuff. Not a leather glove: thin and smooth. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3010-M': 'A pair of thin blue nitrile assembly gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: smooth close-fitting blue material with a darker textured grip coating on the palm and fingers, and a short cuff. Not a leather glove: thin and smooth. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3010-L': 'A pair of thin blue nitrile assembly gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: smooth close-fitting blue material with a darker textured grip coating on the palm and fingers, and a short cuff. Not a leather glove: thin and smooth. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3010-XL': 'A pair of thin blue nitrile assembly gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: smooth close-fitting blue material with a darker textured grip coating on the palm and fingers, and a short cuff. Not a leather glove: thin and smooth. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3011-S': 'A pair of brown cowhide leather work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: leather back and palm, slightly darker reinforced fingertips, and a short leather cuff. Not a welding glove: no long gauntlet. No logo, no emblem. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3011-M': 'A pair of brown cowhide leather work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: leather back and palm, slightly darker reinforced fingertips, and a short leather cuff. Not a welding glove: no long gauntlet. No logo, no emblem. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3011-L': 'A pair of brown cowhide leather work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: leather back and palm, slightly darker reinforced fingertips, and a short leather cuff. Not a welding glove: no long gauntlet. No logo, no emblem. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3011-XL': 'A pair of brown cowhide leather work gloves, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions: leather back and palm, slightly darker reinforced fingertips, and a short leather cuff. Not a welding glove: no long gauntlet. No logo, no emblem. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3013-S': 'A pair of cut-resistant work gloves, grey knit liner with a bright green nitrile coating across the palm and fingers, and a short knit cuff, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions. Not the black coated gloves: the coating is green. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3013-M': 'A pair of cut-resistant work gloves, grey knit liner with a bright green nitrile coating across the palm and fingers, and a short knit cuff, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions. Not the black coated gloves: the coating is green. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3013-L': 'A pair of cut-resistant work gloves, grey knit liner with a bright green nitrile coating across the palm and fingers, and a short knit cuff, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions. Not the black coated gloves: the coating is green. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3013-XL': 'A pair of cut-resistant work gloves, grey knit liner with a bright green nitrile coating across the palm and fingers, and a short knit cuff, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions. Not the black coated gloves: the coating is green. No logo, no emblem on the cuff. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3014-S': 'A pair of long welding gauntlets in brown cowhide leather, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions, with a very long leather cuff reaching far up the wrist. Not a short work glove: the gauntlet is very long. No logo. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3014-M': 'A pair of long welding gauntlets in brown cowhide leather, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions, with a very long leather cuff reaching far up the wrist. Not a short work glove: the gauntlet is very long. No logo. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3014-L': 'A pair of long welding gauntlets in brown cowhide leather, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions, with a very long leather cuff reaching far up the wrist. Not a short work glove: the gauntlet is very long. No logo. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-IND-3014-XL': 'A pair of long welding gauntlets in brown cowhide leather, lying flat side by side, palms down, each with exactly five fingers (thumb plus four fingers) in anatomically correct proportions, with a very long leather cuff reaching far up the wrist. Not a short work glove: the gauntlet is very long. No logo. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
}
# The stab-resistant glove is sold singly: its sizes show the same single glove.
HINTS.update({f'DEMO-IND-3012-{z}': HINTS['DEMO-IND-3012'] for z in ('S', 'M', 'L', 'XL')})
