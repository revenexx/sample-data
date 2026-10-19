"""Office pack, series 5: cleaning and facility products (cloths, bottles, bags,
bins, mop gear, sponges, dispensers, broom). Models in mm, standing on z=0.

Colour variants pass their colour; a model SKU gets the same builder call as
its first variant (so 5001 is blue cloth, 5008 is the black bin).
"""
import math

CLOTH ={'blue': '#2F6FE0', 'red': '#C7362F', 'green': '#2F8A57', 'yellow': '#F2C94C'}
BIN = {'black': '#2B2E33', 'grey': '#8C929C', 'blue': '#2F6FE0'}


def _square(h):
    return [(-h, -h), (h, -h), (h, h), (-h, h)]


def cloth_stack(k, colour='blue'):
    """Ten folded microfibre cloths: a neat stack of six layers, a second short stack beside."""
    c = CLOTH[colour]
    for z, a in [(0, 0), (5, 4), (10, -3), (15, 7), (20, -5), (25, 2)]:
        o = k.slab(_square(100), 5, z, c, round_=2, smooth=0)
        o.rotation_euler[2] = math.radians(a)
    for z, a in [(0, 14), (4, -9), (8, 20)]:
        o = k.slab(_square(80), 4, z, c, round_=2, smooth=0)
        o.location.x += 230
        o.location.y -= 10
        o.rotation_euler[2] = math.radians(a)


def bottle(k, col, w, d, h, cap='dark', neck_r=None, cap_r=18, cap_h=22):
    """Plain plastic bottle: rounded body, neck and screw cap, no label."""
    body_top = h * 0.82
    nr = neck_r if neck_r else min(w, d) * 0.2
    k.box((w, d, body_top), (0, 0, body_top / 2), col, bevel=min(w, d) * 0.1)
    k.cyl(nr, h - body_top, (0, 0, body_top + (h - body_top) / 2), col, rough=0.3)
    k.cyl(cap_r, cap_h, (0, 0, h + cap_h / 2), cap, bevel=1.5)


def cleaner_bottle(k, col='#7FC2E0'):
    """1 l all-purpose cleaner bottle, light blue, plain."""
    bottle(k, col, 72, 52, 250, cap='dark', cap_r=17, cap_h=24)


def canister(k):
    """5 l white canister: square body, carry handle on top, small cap."""
    k.box((200, 140, 280), (0, 0, 140), '#E9ECEF', bevel=8)
    k.box((190, 130, 12), (0, 0, 286), '#D0D5DB', bevel=2)
    k.box((150, 12, 16), (0, 0, 318), '#D0D5DB', bevel=3)           # carry handle
    k.box((12, 12, 26), (-70, 0, 300), '#D0D5DB')                    # handle posts
    k.box((12, 12, 26), (70, 0, 300), '#D0D5DB')
    k.cyl(22, 24, (30, 0, 298), '#2B2E33', bevel=1.5)                 # screw cap


def spray_bottle(k, col='#7FC2E0'):
    """750 ml glass cleaner: bottle with a dark trigger spray head and forward nozzle."""
    k.box((70, 50, 185), (0, 0, 92.5), col, bevel=7, rough=0.3)
    k.cyl(16, 12, (0, 0, 191), '#2B2E33')                             # collar
    k.box((50, 40, 36), (0, 0, 210), '#2B2E33', bevel=4)              # trigger head
    k.cyl(7, 36, (0, -38, 214), '#2B2E33', rot=(90, 0, 0))           # nozzle


def toilet_bottle(k, col='#2F6FE0'):
    """750 ml slim toilet gel bottle: tall, narrow neck, dark cap."""
    bottle(k, col, 58, 58, 230, cap='dark', neck_r=12, cap_r=15, cap_h=30)


def waste_bags(k, r=80, length=150, col='#2B2E33'):
    """Roll of black waste bags lying on its side, axis along X."""
    k.cyl(r, length, (0, 0, r), col, rot=(0, 90, 0), bevel=2, rough=0.6)
    k.cyl(r * 0.32, 2, (length / 2 + 1, 0, r), '#E8E4D8', rot=(0, 90, 0))                 # white cardboard core, end face


def waste_bin(k, colour='black'):
    """15 l round tapered waste bin with a finger grip notch on the front rim."""
    c = BIN[colour]
    k.cyl(110, 250, (0, 0, 125), c, r2=125, rough=0.4, bevel=2)
    k.torus(125, 4, (0, 0, 250), c, rot=None)                          # rim
    k.box((50, 10, 12), (0, -122, 240), '#1A1C20')                     # finger grip


def jug(k, col='#3BA56B'):
    """2 l floor cleaner concentrate jug: wide squat body, side handle, cap."""
    k.box((150, 100, 240), (0, 0, 120), col, bevel=8, rough=0.35)
    k.cyl(22, 26, (0, 0, 253), '#2B2E33', bevel=1.5)
    k.torus(38, 8, (75, 0, 150), col, rot=(90, 0, 0))                 # side handle


def sponges(k):
    """Five scouring sponges lying flat: three in a front row, two behind, none stacked."""
    for (x, y) in [(-110, -45), (0, -45), (110, -45), (-55, 45), (55, 45)]:
        k.box((100, 70, 40), (x, y, 20), '#F2C94C', bevel=2, rough=0.8)
        k.box((100, 70, 4), (x, y, 42), '#3E8E5A', bevel=1, rough=0.9)


def mop_cover(k):
    """Flat cotton mop cover, 40 cm wide, with a sewn pocket band across the middle."""
    k.slab([(0, -60), (200, -60), (200, 60), (0, 60)], 8, 0, '#E4DFD2', mirror=True, round_=3)
    k.slab([(0, -60), (190, -60), (190, 60), (0, 60)], 3, 8, '#CDC6B3', mirror=True, round_=1.2, smooth=0)


def mop_bucket(k, col='#2F6FE0'):
    """10 l blue bucket with a dark wringer frame and a handle bar across the top."""
    k.cyl(105, 250, (0, 0, 125), col, r2=135, rough=0.4, bevel=2)
    k.box((230, 130, 14), (0, 0, 262), '#2B2E33', bevel=3)            # wringer frame
    for y in (-50, -25, 0, 25, 50):                                    # press grid bars on top of the frame
        k.box((226, 4, 3), (0, y, 270), '#2B2E33', bevel=0.5)
    k.cyl(18, 230, (0, -35, 275), '#6B7280', rot=(0, 90, 0), bevel=1) # wringer rollers
    k.cyl(18, 230, (0, 35, 275), '#6B7280', rot=(0, 90, 0), bevel=1)
    k.cyl(9, 300, (0, 0, 300), '#2B2E33', rot=(0, 90, 0))              # handle bar


def towel_dispenser(k):
    """White wall-mounted towel dispenser shown upright: front viewing window and bottom slot."""
    k.box((280, 110, 320), (0, 0, 160), '#F7F7F5', bevel=6, rough=0.35)
    k.box((200, 2, 120), (0, -56, 200), '#8F98A3', bevel=1, rough=0.1)   # viewing window
    k.box((220, 2, 10), (0, -56, 60), '#2B2E33', bevel=1)                 # bottom slot


def soap_dispenser(k):
    """White wall-mounted soap dispenser shown upright: rounded body, pump nozzle at the bottom front."""
    k.box((100, 75, 230), (0, 0, 135), '#F2F2F0', bevel=18, rough=0.35)
    k.box((70, 2, 150), (0, -38, 150), '#C9D1D9', bevel=1, rough=0.2)    # level window
    k.box((40, 40, 40), (0, -20, 25), '#2B2E33', bevel=4)                 # pump head
    k.cyl(6, 30, (0, -32, 8), '#2B2E33', rot=(90, 0, 0))                  # nozzle


def broom(k):
    """Broom standing on its bristle head, 120 cm long, wooden handle vertical."""
    k.box((320, 48, 56), (0, 0, 28), '#3A6EA5', bevel=6, rough=0.7)     # bristle head
    k.box((70, 40, 36), (0, 0, 70), '#2B2E33', bevel=4)                  # joint
    k.cyl(14, 1100, (0, 0, 620), '#B88A57', rough=0.5)                  # handle


FLAT = {'pitch': 50}          # cloths, sponges and the mop cover lie flat
LOW = {'pitch': 14}           # waste-bag rolls lie on the floor, seen from low

SKUS = {
    'DEMO-OFF-5001': (cloth_stack, {'colour': 'blue'}, FLAT),
    'DEMO-OFF-5001-BLUE': (cloth_stack, {'colour': 'blue'}, FLAT),
    'DEMO-OFF-5001-RED': (cloth_stack, {'colour': 'red'}, FLAT),
    'DEMO-OFF-5001-GREEN': (cloth_stack, {'colour': 'green'}, FLAT),
    'DEMO-OFF-5001-YELLOW': (cloth_stack, {'colour': 'yellow'}, FLAT),
    'DEMO-OFF-5002': (cleaner_bottle, {}),
    'DEMO-OFF-5003': (canister, {}),
    'DEMO-OFF-5004': (spray_bottle, {}),
    'DEMO-OFF-5005': (toilet_bottle, {}),
    'DEMO-OFF-5006': (waste_bags, {'r': 80, 'length': 150}, LOW),
    'DEMO-OFF-5007': (waste_bags, {'r': 95, 'length': 200}, LOW),
    'DEMO-OFF-5008': (waste_bin, {'colour': 'black'}),
    'DEMO-OFF-5008-BLACK': (waste_bin, {'colour': 'black'}),
    'DEMO-OFF-5008-GREY': (waste_bin, {'colour': 'grey'}),
    'DEMO-OFF-5008-BLUE': (waste_bin, {'colour': 'blue'}),
    'DEMO-OFF-5009': (mop_cover, {}, FLAT),
    'DEMO-OFF-5010': (mop_bucket, {}),
    'DEMO-OFF-5011': (sponges, {}, FLAT),
    'DEMO-OFF-5012': (jug, {}),
    'DEMO-OFF-5013': (towel_dispenser, {}),
    'DEMO-OFF-5014': (soap_dispenser, {}),
    'DEMO-OFF-5015': (broom, {}),
}


_BIN_HINT = 'A {c} 15 litre plastic waste bin, round tapered bin standing upright, smooth plastic with a finger grip notch on the front rim. Empty, no lid, no label. Not a basket and not a metal bin.'

HINTS = {
    'DEMO-OFF-5001': 'Ten folded microfibre cloths in blue, one neat stack lying flat on the surface, square corners. Fine woven microfibre with a slightly fuzzy texture, plain colour, no print. Not a towel and not a sponge.',
    'DEMO-OFF-5001-BLUE': 'Ten folded microfibre cloths in blue, one neat stack lying flat on the surface, square corners. Fine woven microfibre with a slightly fuzzy texture, plain colour, no print. Not a towel and not a sponge.',
    'DEMO-OFF-5001-RED': 'Ten folded microfibre cloths in red, one neat stack lying flat on the surface, square corners. Fine woven microfibre with a slightly fuzzy texture, plain colour, no print. Not a towel and not a sponge.',
    'DEMO-OFF-5001-GREEN': 'Ten folded microfibre cloths in green, one neat stack lying flat on the surface, square corners. Fine woven microfibre with a slightly fuzzy texture, plain colour, no print. Not a towel and not a sponge.',
    'DEMO-OFF-5001-YELLOW': 'Ten folded microfibre cloths in yellow, one neat stack lying flat on the surface, square corners. Fine woven microfibre with a slightly fuzzy texture, plain colour, no print. Not a towel and not a sponge.',
    'DEMO-OFF-5002': 'A plain 1 litre plastic bottle of all-purpose cleaner in light blue, rectangular body with rounded shoulders and a dark screw cap, standing upright. Plain bottle without label. Not a spray bottle and not a jug.',
    'DEMO-OFF-5003': 'A plain white 5 litre plastic canister of all-purpose cleaner, square body with a carry handle across the top and a small dark screw cap in the middle. Plain canister without label, standing upright. Not a bottle and not a jug.',
    'DEMO-OFF-5004': 'A 750 ml spray bottle of glass cleaner in light blue, with a dark trigger spray head on top and a nozzle pointing forward. Plain bottle without label, standing upright. Not a wall-mounted dispenser.',
    'DEMO-OFF-5005': 'A slim blue 750 ml toilet cleaner gel bottle with a tall narrow neck and a dark screw cap, standing upright. Plain bottle without label. Not a spray bottle.',
    'DEMO-OFF-5006': 'A roll of black 60 litre waste bags lying on its side: a tightly wound, smooth cylinder about 16 cm across with its round end face and a small white cardboard core visible, the roll axis horizontal. Black plastic, plain. Not a box and not a loose pile of bags.',
    'DEMO-OFF-5007': 'A larger roll of black 120 litre waste bags lying on its side: a wide tightly wound cylinder about 19 cm across, the roll axis horizontal, 10 bags on the roll. Black plastic, plain. Not a box and not a loose pile of bags; clearly bigger than the 60 litre roll.',
    'DEMO-OFF-5008': _BIN_HINT.format(c='black'),
    'DEMO-OFF-5008-BLACK': _BIN_HINT.format(c='black'),
    'DEMO-OFF-5008-GREY': _BIN_HINT.format(c='grey'),
    'DEMO-OFF-5008-BLUE': _BIN_HINT.format(c='blue'),
    'DEMO-OFF-5009': 'A flat wet mop pad lying flat, seen from slightly above: a rectangular pad of off-white cotton loops with a short fringe along both long edges and a blue fabric trim band with two pockets for the mop holder; the cotton has visible texture and soft grey shadows so the pad stands out clearly from the white background. Not a towel, not a microfibre cloth.',
    'DEMO-OFF-5010': 'A blue 10 litre plastic mop bucket with a mop wringer: a dark grey press grid with two grey rollers is fixed across the top rim, and a carry handle bar sits on top. Round tapered bucket, empty. Not a wheeled trolley and not a plain bucket without a wringer. No labels or printing.',
    'DEMO-OFF-5011': 'Five rectangular scouring sponges lying flat, exactly five, in two rows: three in the front row and two behind. Each yellow foam sponge has a green scrub pad on top. Not a bar of soap and not a cloth. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-5012': 'A 2 litre green plastic jug of floor cleaner concentrate, a wide squat jug with a side handle and a dark screw cap, standing upright. Plain jug without label. Not a bottle with a trigger.',
    'DEMO-OFF-5013': 'A white plastic towel dispenser for folded hand towels, a flat rectangular box shown upright, with a clear viewing window on its front and a dark slot at the bottom. Plain, no label. Not a roll dispenser and not a soap dispenser.',
    'DEMO-OFF-5014': 'A white plastic soap dispenser for 500 ml refills, a tall rounded body with a small dark pump head and nozzle at the bottom front and a narrow level window. Plain, no label, shown upright. Not a bottle with a screw cap.',
    'DEMO-OFF-5015': 'A broom standing upright on its bristle head, bristles blue-grey plastic, a wooden handle held vertical, 120 cm long in total. Not a mop and not a brush with a short handle.',
}
