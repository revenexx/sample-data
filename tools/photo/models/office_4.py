"""Office pack, series 4: desk pad, document holder, tape, staples, clips, scale,
trays, calculator, name tents, push pins and letter opener.

Plain, unprinted desk and office items in realistic colours. Boxes for packs and
devices, slabs for flat items (pad, tin, opener), a rotated pair of plates for
the name tents. Variants of one product share a builder call with their own size
or colour. DEMO-OFF-4001 and DEMO-OFF-4005 live in office_example.py.
"""

import math

STAPLE = {'kraft': '#C7B08A', 'slate': '#5E6B7A', 'sand': '#D8D0C0'}


def desk_pad(k):
    """Desk pad 600 x 400 mm: dark felt base with a pale calendar sheet on top."""
    k.slab([(-300, -200), (300, -200), (300, 200), (-300, 200)], 4, 0, '#3B4250', round_=1.5, smooth=0)
    k.slab([(-282, -150), (282, -150), (282, 178), (-282, 178)], 1.2, 4, '#F4F4F2', round_=0.4, smooth=0)
    k.slab([(-282, 150), (282, 150), (282, 178), (-282, 178)], 1.4, 4, '#14998C', round_=0.4, smooth=0)


def document_holder(k):
    """A4 document holder: a light grey base, a clear front pocket, a clip bar."""
    k.box((240, 110, 6), (0, 10, 3), '#D7DEE6', bevel=2, rough=0.4)                      # base
    k.box((210, 2, 297), (0, -2, 6 + 148.5), 'white', rough=0.7)                          # A4 sheet behind the pocket
    k.box((230, 4, 270), (0, -30, 6 + 135), '#CFE3F0', bevel=2, rough=0.2, alpha=0.5)     # clear front pocket
    k.box((236, 10, 8), (0, -34, 6 + 262), 'mid', bevel=2, metal=0.4, rough=0.3)          # clip bar


def tape_roll(k):
    """Clear adhesive tape roll, 19 mm wide, standing on its edge face-on."""
    k.cyl(33, 19, (0, 0, 33), '#E9EEF2', rot=(90, 0, 0), alpha=0.5, rough=0.15)          # tape
    k.cyl(14, 19.4, (0, 0, 33), '#D9C9A8', rot=(90, 0, 0), rough=0.7)                    # cardboard core


def _staple(k, cx, cy, z, a):
    """One U-shaped staple lying flat: flat crown 10 mm, two 8 mm legs, wire 1 mm, turned by a degrees."""
    c, s = math.cos(math.radians(a)), math.sin(math.radians(a))
    def at(u, v):
        return (cx + u * c - v * s, cy + u * s + v * c)
    k.box((10, 0.8, 1.0), (cx, cy, z), '#D9DEE6', rot=(0, 0, a), rough=0.55)
    for u in (-4.6, 4.6):
        px, py = at(u, 4)
        k.box((0.8, 8, 1.0), (px, py, z), '#D9DEE6', rot=(0, 0, a), rough=0.55)


def staple_box(k, size=(120, 36, 60), colour=STAPLE['kraft']):
    """Open cardboard staple box, size (x, y, z): four walls and a floor, filled with U-shaped staples in two layers."""
    x, y, z = size
    t = 3
    k.box((x, y, t), (0, 0, t / 2), colour, bevel=1, rough=0.6)                          # floor
    k.box((x, t, z), (0, -y / 2 + t / 2, z / 2), colour, bevel=1, rough=0.6)            # front wall
    k.box((x, t, z), (0, y / 2 - t / 2, z / 2), colour, bevel=1, rough=0.6)             # back wall
    k.box((t, y, z), (-x / 2 + t / 2, 0, z / 2), colour, bevel=1, rough=0.6)            # left wall
    k.box((t, y, z), (x / 2 - t / 2, 0, z / 2), colour, bevel=1, rough=0.6)             # right wall
    nx = int((x - 14) / 14)
    ny = max(2, int((y - 14) / 11))
    for layer in (0, 1):
        sx, sy = (x - 2 * t - 8) / nx, (y - 2 * t - 8) / ny
        for i in range(nx):
            for j in range(ny):
                cx = -x / 2 + t + 4 + (i + 0.5 + 0.5 * layer) * sx
                cy = -y / 2 + t + 4 + (j + 0.5) * sy
                _staple(k, cx, cy, t + 0.5 + 2.2 * layer, 15 * ((i + 2 * j + 3 * layer) % 5) - 30)


def paper_clip_tin(k):
    """Shallow steel tin with a few loose galvanised paper clips on top."""
    k.box((110, 40, 24), (0, 0, 12), '#D9DDE3', bevel=2, metal=0.4, rough=0.35)          # tin
    for x, y in ((-25, -5), (5, 4), (30, -6)):
        k.torus(9, 0.8, (x, y, 25), '#C9CED6', metal=0.6, rough=0.3)                     # clip


def letter_scale(k):
    """Desk letter scale: flat platform in front, display head on a pillar behind."""
    k.box((200, 150, 10), (0, 0, 5), 'dark', bevel=3, rough=0.4)                         # platform
    k.box((30, 30, 70), (0, 55, 45), 'body', bevel=2, rough=0.4)                          # pillar
    k.box((130, 40, 50), (0, 50, 108), 'light', bevel=3, rough=0.4)                       # display head
    k.box((100, 2, 30), (0, 29, 110), 'dark', rough=0.2)                                   # display window


def letter_tray(k):
    """Three stacked plastic letter trays, open at the front, a sheet on top."""
    for i in range(3):
        z = 18 + i * 44
        k.box((260, 330, 36), (0, 0, z), 'light', bevel=2, rough=0.5)                    # tray
    k.box((240, 300, 2), (0, 0, 18 + 2 * 44 + 19), '#F7F7F5', rough=0.7)                  # sheet on top


def calculator(k):
    """Desk calculator: dark body, a grid of light keys in front, display at the back."""
    k.box((120, 150, 26), (0, 0, 13), 'body', bevel=4, rough=0.5)                        # body
    k.box((104, 38, 5), (0, 46, 28), 'dark', bevel=1, rough=0.2)                          # display
    k.box((104, 14, 2), (0, 26, 28), 'mid', bevel=1, rough=0.4)                           # solar strip
    for r in range(4):
        for c in range(4):
            x = -36 + c * 24
            y = 2 - r * 19
            k.box((18, 14, 4), (x, y, 28), 'light', bevel=1, rough=0.4)                   # key


def name_tents(k, colour='#F7F7F5', w=100):
    """Ten blank folded desk tent cards in two rows of five, A-frame plates, 105 mm high."""
    for n in range(10):
        x = (n % 5 - 2) * 110
        yc = -45 if n < 5 else 45
        k.box((w, 2, 105), (x, yc - 22, 47.6), colour, rot=(-25, 0, 0), rough=0.6)       # front face
        k.box((w, 2, 105), (x, yc + 22, 47.6), colour, rot=(25, 0, 0), rough=0.6)        # back face


def push_pin_box(k):
    """Small plain cardboard box with push pins stuck in its top."""
    k.box((160, 40, 60), (0, 0, 30), '#E6DCCB', bevel=3, rough=0.7)                      # box
    k.box((160, 40, 2), (0, 0, 61), '#CDBFA6', bevel=0.5, rough=0.7)                     # closed lid line
    for y, head in ((-12, '#E8930C'), (0, '#2F8A57'), (12, '#2F6FE0')):                   # three loose pins on the desk
        k.cyl(0.7, 22, (110, y, 1.5), 'metal', metal=1, rough=0.2, rot=(0, 90, 0))        # steel point
        k.sphere(3, (123, y, 1.5), head, rough=0.3)                                       # plastic head


def letter_opener(k):
    """Letter opener lying flat: a narrow steel blade and a dark wide handle."""
    k.slab([(-120, -12), (0, -12), (0, 12), (-120, 12)], 9, 0, 'dark', round_=4)          # handle
    k.slab([(-2, -5), (100, -4.5), (112, 0), (100, 4.5), (-2, 5)], 1.2, 3.5, 'metal', metal=1, rough=0.2)  # blade


SKUS = {
    'DEMO-OFF-4002': (desk_pad, {}, {'pitch': 50, 'fill': 0.95}),
    'DEMO-OFF-4003': (document_holder, {}),
    'DEMO-OFF-4004': (tape_roll, {}),
    'DEMO-OFF-4006': (staple_box, {'size': (120, 36, 60), 'colour': STAPLE['kraft']}, {'pitch': 45}),
    'DEMO-OFF-4007': (staple_box, {'size': (190, 60, 120), 'colour': STAPLE['slate']}, {'pitch': 45}),
    'DEMO-OFF-4008': (staple_box, {'size': (150, 30, 80), 'colour': STAPLE['sand']}, {'pitch': 45}),
    'DEMO-OFF-4009': (paper_clip_tin, {}, {'pitch': 50}),
    'DEMO-OFF-4010': (letter_scale, {}),
    'DEMO-OFF-4011': (letter_tray, {}),
    'DEMO-OFF-4012': (calculator, {}),
    'DEMO-OFF-4013': (name_tents, {}),
    'DEMO-OFF-4014': (push_pin_box, {}),
    'DEMO-OFF-4015': (letter_opener, {}, {'pitch': 50}),
}

HINTS = {
    'DEMO-OFF-4002': 'A flat desk pad, about 60 by 40 cm, lying on the surface: a dark slate-grey felt mat with a pale white calendar sheet on top, near the back edge, the sheet blank with no printed numbers or words, and a thin teal strip along the back edge. Not a mouse pad and not a notebook. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4003': 'A plain clear-smoke plastic document holder standing upright: a front pocket of translucent grey plastic holding a blank white sheet of paper, a metal-grey clip bar across the top and a flat base. Nothing printed anywhere. Not a magazine file, not a folder, not a book stand.',
    'DEMO-OFF-4004': 'A roll of clear adhesive tape seen face-on, standing on its edge: a transparent-looking plastic ring, about 19 mm wide, with a pale cardboard core in the centre. Not a tape dispenser and not a sticker sheet.',
    'DEMO-OFF-4006': 'A small plain kraft-brown cardboard box of metal staples, about 12 by 6 cm, standing with its lid flaps folded back, the box open and a loose layer of silver U-shaped staples (flat crown, two legs) visible inside. Unprinted, not a stapler, no screws, no nails, no round heads. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4007': 'A larger plain blue-grey cardboard box of U-shaped staples, taller than a small staple box, open with its lid flaps folded back, silver flat-crowned staples with two legs visible inside, no nails and no screws. Plain box with no logo, no emblem and no icon. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4008': 'A flat plain pale grey-beige cardboard box of U-shaped staples, wider than it is tall, open with its lid flaps folded back, silver staples with flat crowns and two short legs visible inside. Not screws, not nails, not a stapler. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4009': 'A shallow open steel tin of paper clips: a flat grey metal tray with a few loose silver paper clips lying on top, made of thin galvanised wire. Not a closed box, not a single clip, not a paper clip holder.',
    'DEMO-OFF-4010': 'A desk letter scale: a flat dark grey weighing platform in front, and a light grey display head on a short pillar at the back, the digital window dark and blank with no digits. Not a kitchen scale and not a bathroom scale. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4011': 'Three stacked plastic letter trays in light grey, each a shallow box open at the front, with a single sheet of white A4 paper on the top tray. Not a drawer unit and not a single tray.',
    'DEMO-OFF-4012': 'A desk calculator: a dark grey rectangular body with a dark display window at the back, a narrow solar strip above it, and a grid of small light grey keys across the front, the keys plain with no printed symbols or numerals and the casing plain. Not a phone and not a keyboard. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4013': 'Ten blank white cardboard desk tent cards in two rows of five, each folded into a V shape like an upside-down book, the front face upright. Plain, no lettering and no name. Not a book, not a sign board. The whole product visible, standing out clearly from the white background with a soft shadow. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4014': 'A small plain pale cardboard box, closed, with no pins stuck into it, and three loose push pins lying beside it on the desk, each a thin steel point under a round plastic head in orange, green or blue. Not a pinboard, no pins in the box lid. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4015': 'A metal letter opener lying flat, seen from above: a narrow pointed steel blade on one end and a dark, wide rounded handle on the other. Not a knife, not a pen, not a ruler.',
}
