"""Office pack, series 2: pens, pencils, stationery and desk tools.

Same format as office_example.py. Angles in degrees; rot=(x, y, z) is passed
straight to the kit. A pen lying on the floor runs along X, rot (0, 90, a)
turns it by a about Z.
"""
import math

BLUE = '#2E5FA8'
RED = '#C2403A'
BLACK = '#2A2D33'
GREEN = '#3E8E5A'
TEAL = '#14998C'


def _pen(k, cx, cy, L, r, a, color, z0=0.0, clip=False, tip_r=1.2):
    """A round pen lying on the floor (or on z0), long axis at angle a."""
    dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
    k.cyl(r, L, (cx, cy, z0 + r), color, rot=(0, 90, a), rough=0.3)
    k.cyl(r, 12, (cx + (L / 2 + 6) * dx, cy + (L / 2 + 6) * dy, z0 + r), color,
          rot=(0, 90, a), r2=tip_r, rough=0.3)
    if clip:
        k.box((L * 0.4, 1.8, 1.2), (cx - dx * L * 0.2, cy - dy * L * 0.2, z0 + 2 * r - 0.3),
              '#1A1C20', rot=(0, 0, a))


def pen_box(k):
    """Open cardboard box packed with blue ballpoint pens in three layers (about 50 pens)."""
    c = '#E6DCCB'
    k.box((160, 90, 1.5), (0, 0, 0.75), c, bevel=0.5)                                 # floor
    k.box((160, 3, 26), (0, -43.5, 13), c, bevel=1)                                   # front wall
    k.box((160, 3, 26), (0, 43.5, 13), c, bevel=1)                                    # back wall
    k.box((3, 90, 26), (-78.5, 0, 13), c, bevel=1)                                    # left wall
    k.box((3, 90, 26), (78.5, 0, 13), c, bevel=1)                                     # right wall
    for layer in range(3):
        z0 = 1.5 + 8 * layer
        ys = [-36 + 9 * i + 4.5 * layer for i in range(9 - layer % 2)]
        for y in ys:
            _pen(k, 0, y, 130, 4, 0, BLUE, z0=z0, clip=True)


def pen_box_standing(k):
    """Open box of rollerball pens with pens standing up, tilted towards the viewer."""
    k.box((160, 80, 36), (0, 0, 18), 'paper', bevel=4)
    k.box((150, 70, 2), (0, 0, 36.5), '#8C7556', bevel=0.5)
    for x in (-40, -13, 14, 41):
        k.cyl(5, 130, (x, 8, 62), BLACK, rot=(18, 0, 0), rough=0.3)


def pencil_cup(k, cup='#4A515C'):
    """Dark plastic cup with six wooden pencils standing in it."""
    k.cyl(36, 92, (0, 0, 46), cup, bevel=1.5, rough=0.4)
    for x, y in ((-12, -6), (0, -12), (12, -6), (12, 8), (-12, 8), (0, 4)):
        sx = 1 if x > 0 else -1
        sy = 1 if y > 0 else -1
        k.cyl(3.6, 170, (x, y, 95), '#E9B73E', verts=6, rot=(-5 * sy, 5 * sx, 0), rough=0.5)


def highlighters(k):
    """Four chisel-tip highlighters lying side by side."""
    for y, col in zip((-33, -11, 11, 33), ('#F2DF3A', '#7FD36B', '#F28BB5', '#7CB7E8')):
        k.box((125, 13, 11), (0, y, 5.5), col, bevel=3, rough=0.4)
        k.box((14, 13, 8), (67, y, 4), '#E8E4D8', bevel=1)


def sticky_pads(k):
    """Twelve square pads stacked in a slightly offset tower."""
    cols = ('#F7E58A', '#B9E6C9', '#F7B9CB', '#B7D8F2', '#F9CFA0', '#E0D3F3')
    for i in range(12):
        x = ((i * 7) % 5 - 2) * 0.6
        y = ((i * 3) % 5 - 2) * 0.5
        k.box((76, 76, 2.6), (x, y, 1.3 + i * 2.6), cols[i % len(cols)], bevel=0.6, rough=0.7)


def stapler(k):
    """Desk stapler on a rubber base: raised back arm, low front."""
    pts = [(-78, 0), (78, 0), (80, 8), (76, 12), (36, 16), (-8, 38), (-44, 44), (-72, 36), (-78, 22)]
    k.profile(pts, 38, 0, 'body', round_=3)
    k.box((120, 30, 2), (0, 0, 1.0), '#1A1C20', bevel=0.5, rough=0.8)
    k.box((150, 8, 2), (0, 0, 0.5), '#1A1C20', bevel=0.5, rough=0.8)


def sharpener(k):
    """Metal double-hole sharpener: two holes in the top, dark front strip."""
    k.box((90, 42, 26), (0, 0, 13), 'metal', bevel=3, metal=0.6, rough=0.3)
    k.box((90, 2, 8), (0, -21, 9), 'dark', bevel=0.5)
    k.cyl(5.5, 1, (-18, 0, 26.5), '#1A1C20')
    k.cyl(5.5, 1, (18, 0, 26.5), '#1A1C20')
    k.cyl(4.5, 1.6, (-18, 0, 26.2), 'mid')
    k.cyl(4.5, 1.6, (18, 0, 26.2), 'mid')


def gel_pen(k, colour=BLUE):
    """One retractable gel pen lying flat: barrel, clip, tip and back clicker."""
    _pen(k, 0, 0, 140, 5.5, -30, colour, clip=True, tip_r=1.6)
    dx, dy = math.cos(math.radians(-30)), math.sin(math.radians(-30))
    k.cyl(3.5, 4, (-(70 + 2) * dx, -(70 + 2) * dy, 5.5), colour, rot=(0, 90, -30))  # push button, same colour


def fineliners(k):
    """Ten black fineliners lying side by side."""
    for i in range(10):
        _pen(k, 0, -31.5 + i * 7, 130, 3.2, 0, BLACK, tip_r=0.8)


def felt_row(k):
    """Twelve felt-tip pens of equal thickness lying side by side in one row, round barrels, round tips."""
    cols = ('#D0453B', '#F08A24', '#F2D03B', '#3E8E5A', '#2E5FA8', '#7A4FA0',
            '#F28BB5', '#7A4E2D', '#1F2226', '#9AA1AB', '#8CC8F0', '#14553A')
    for i, col in enumerate(cols):
        _pen(k, 0, -99 + 18 * i, 130, 8, 0, col, tip_r=4)


def correction_roller(k):
    """Dry correction roller: slim light blue body, a small window on top, a white roller tip at the front."""
    k.box((110, 34, 24), (-6, 0, 22), '#BFE0F2', bevel=8, rough=0.4)                    # slim body
    k.box((40, 22, 2), (-12, 0, 34.5), '#8FA9BE', bevel=0.8)                             # top window frame
    k.cyl(10, 4, (48, 0, 22), 'mid', rot=(0, 90, 0), rough=0.4)                          # collar
    k.cyl(9, 20, (58, 0, 22), '#FFFFFF', rot=(0, 90, 0), rough=0.5)                      # roller tip with tape


def two_hole_punch(k):
    """Two-hole punch: wide base, body, dark lever on the front, two pins."""
    k.box((130, 70, 8), (0, 0, 4), 'dark', bevel=2)
    k.box((118, 56, 26), (0, -4, 21), 'body', bevel=5)
    k.box((120, 20, 14), (0, -30, 40), 'dark', bevel=4)                                  # lever at the front
    for x in (-40, 40):
        k.cyl(9, 14, (x, 6, 41), 'light', verts=32)                                      # punch head on the body
        k.cyl(5, 0.6, (x, 6, 8.3), '#1A1C20')                                            # die hole in the base


def ruler(k):
    """Transparent 30 cm plastic ruler lying flat."""
    th = -8
    k.box((300, 36, 2.0), (0, 0, 1.0), '#E4F0F6', bevel=0.4, rot=(0, 0, th), alpha=0.4, rough=0.15)
    t = math.radians(th)
    for mm in range(0, 301, 5):
        ln = 8 if mm % 10 == 0 else 4
        x = -150 + mm                                                                  # local x, along the ruler
        y = -18 + ln / 2                                                               # ticks along the top edge
        wx = x * math.cos(t) - y * math.sin(t)
        wy = x * math.sin(t) + y * math.cos(t)
        k.box((0.4, ln, 0.1), (wx, wy, 2.05), '#23303A', rot=(0, 0, th))


def scissors(k):
    """Office scissors lying flat: two crossing blades, ring handles."""
    for hx, hy, tx, ty in ((-80, 30, 90, -28), (-80, -30, 90, 28)):
        L = math.hypot(tx - hx, ty - hy)
        a = math.degrees(math.atan2(ty - hy, tx - hx))
        k.box((L, 7, 3), ((hx + tx) / 2, (hy + ty) / 2, 1.5), 'metal', bevel=1, rot=(0, 0, a), metal=1, rough=0.25)
        k.torus(17, 4.5, (hx, hy, 4.5), 'dark')
    k.cyl(3, 2, (0, 0, 3), 'dark')


def glue_stick(k):
    """Glue stick standing upright: white body, teal cap."""
    k.cyl(13, 74, (0, 0, 37), '#F4F4F2', bevel=1, rough=0.3)
    k.cyl(13.6, 22, (0, 0, 85), TEAL, bevel=1, rough=0.35)


def notepad(k):
    """Flat A5 notepad with a card back and a glued top binding (a pale glue strip, no wire)."""
    k.box((152, 214, 3), (0, 0, 1.5), 'body', bevel=0.8)
    k.box((146, 206, 20), (0, 0, 13), '#FFFFFF', bevel=1)
    k.box((146, 5, 20.4), (0, 101.5, 13), '#E4E0D4', bevel=0.6)                          # glued top binding


def notebook(k, cover='mid'):
    """Flat A5 hard-cover notebook: spine strip, page edge, ribbon bookmark."""
    k.box((148, 210, 8), (0, 0, 4), cover, bevel=3)
    k.box((142, 202, 5), (2, 0, 10.5), '#FFFFFF', bevel=0.5)
    k.box((6, 210, 8), (-71, 0, 4), 'dark', bevel=1.5)
    k.box((4, 16, 1.2), (18, 112, 0.6), TEAL, bevel=0.3)


def index_cards(k):
    """Short stack of A6 ruled cards lying flat: cream cards, white top card."""
    k.box((105, 148, 10), (0, 0, 5), '#FBF8F1', bevel=1)
    k.box((105, 148, 0.8), (1.5, -1, 10.4), '#FFFFFF', bevel=0.3)
    for ry in range(-60, 61, 12):                                                        # blue ruling on the top card
        k.box((95, 0.5, 0.2), (1.5, ry, 10.9), '#6E9BD6')


SKUS = {
    'DEMO-OFF-2001': (pen_box, {}, {'pitch': 30}),
    'DEMO-OFF-2002': (highlighters, {}, {'pitch': 50}),
    'DEMO-OFF-2003': (sticky_pads, {}, {'pitch': 40}),
    'DEMO-OFF-2004': (stapler, {}, {'pitch': 25}),
    'DEMO-OFF-2005': (pencil_cup, {'cup': '#4A515C'}, {'pitch': 25}),
    'DEMO-OFF-2006': (pencil_cup, {'cup': '#7B838F'}, {'pitch': 25}),
    'DEMO-OFF-2007': (sharpener, {}, {'pitch': 25}),
    'DEMO-OFF-2008': (gel_pen, {'colour': BLUE}, {'pitch': 50}),
    'DEMO-OFF-2008-BLUE': (gel_pen, {'colour': BLUE}, {'pitch': 50}),
    'DEMO-OFF-2008-RED': (gel_pen, {'colour': RED}, {'pitch': 50}),
    'DEMO-OFF-2008-BLACK': (gel_pen, {'colour': BLACK}, {'pitch': 50}),
    'DEMO-OFF-2008-GREEN': (gel_pen, {'colour': GREEN}, {'pitch': 50}),
    'DEMO-OFF-2009': (fineliners, {}, {'pitch': 50}),
    'DEMO-OFF-2010': (felt_row, {}, {'pitch': 50}),
    'DEMO-OFF-2011': (correction_roller, {}, {'pitch': 20}),
    'DEMO-OFF-2012': (two_hole_punch, {}, {'pitch': 25}),
    'DEMO-OFF-2013': (ruler, {}, {'pitch': 50}),
    'DEMO-OFF-2014': (scissors, {}, {'pitch': 50}),
    'DEMO-OFF-2015': (glue_stick, {}, {'pitch': 18}),
    'DEMO-OFF-2016': (notepad, {}, {'pitch': 50}),
    'DEMO-OFF-2017': (notebook, {}, {'pitch': 50}),
    'DEMO-OFF-2018': (index_cards, {}, {'pitch': 40}),
    'DEMO-OFF-2019': (pen_box_standing, {}, {'pitch': 25}),
}

HINTS = {
    'DEMO-OFF-2001': 'An open cardboard box of 50 blue ballpoint pens: a plain light cardboard box, open at the top and packed full with rows of blue ballpoint pens lying side by side in several layers, with the clips and tips visible. Blue barrels, not black. Not a single pen and not a pen holder. No labels or printing.',
    'DEMO-OFF-2002': 'A set of four separate chisel-tip highlighters lying side by side with clear gaps between them, none touching: yellow, green, pink and blue barrels, each with a wide angled tip of the same colour. Not round-tip markers and not pencils.',
    'DEMO-OFF-2003': 'A tower of twelve square sticky-note pads, 76 by 76 mm, in pastel yellow, mint, pink, blue, peach and lilac, stacked with the pads slightly offset. Not a single pad, not a notebook, no lettering.',
    'DEMO-OFF-2004': 'A dark grey metal desk stapler lying on a black rubber base: a raised arm at the back, a low flat front and a silver-grey top plate. Not a tape dispenser and not a hole punch.',
    'DEMO-OFF-2005': 'A small dark slate-grey plastic cup holding six wooden HB pencils with plain yellow hexagonal barrels (no lettering on the barrels) and sharpened tips with clean silver ferrules. Not coloured pencils, not a brush pot. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-2006': 'A small mid-grey plastic cup holding six wooden 2B pencils with yellow hexagonal barrels and sharpened tips. The cup is lighter grey than a dark slate cup. Not coloured pencils, not a brush pot.',
    'DEMO-OFF-2007': 'A small double-hole pencil sharpener, about 6 cm, made of dark grey plastic with a clear shavings container: two round conical holes side by side on its front face, one for pencils and one for thick coloured pencils. Not a pencil cup, not a desk organiser.',
    'DEMO-OFF-2008': 'A single retractable gel pen lying flat, with a royal blue barrel of one colour, a metal clip along the top and a small push button at the back end. One writing tip only, at the front. No second colour and no highlighter tip. Not a ballpoint with a thick barrel. No labels or printing.',
    'DEMO-OFF-2008-BLUE': 'A single retractable gel pen lying flat, with a royal blue barrel, a metal clip along the top and a small clicker at the back. Blue barrel only. Not a ballpoint with a thick barrel.',
    'DEMO-OFF-2008-RED': 'A single retractable gel pen lying flat, with a bright red barrel, a metal clip along the top and a small clicker at the back. Red barrel only. Not a ballpoint with a thick barrel.',
    'DEMO-OFF-2008-BLACK': 'A single retractable gel pen lying flat, with a glossy black barrel, a metal clip along the top and a small clicker at the back. Black barrel only. Not a fineliner, which has no clip.',
    'DEMO-OFF-2008-GREEN': 'A single retractable gel pen lying flat, with a green barrel, a metal clip along the top and a small clicker at the back. Green barrel only. Not a ballpoint with a thick barrel.',
    'DEMO-OFF-2009': 'Ten black fineliners lying side by side in one neat row, exactly ten pens counted left to right: slim round pens with plain black barrels, black caps and fine tips. Not a box, not packaging, not a brush pen. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-2010': 'Twelve felt-tip pens of equal thickness lying side by side in one row, exactly twelve pens: round chunky barrels in red, orange, yellow, green, blue, violet, pink, brown, black, grey, light blue and dark green, each with a broad round plastic tip and no metal ball. Not highlighters, not ballpoint pens, not chisel tips. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-2011': 'A handheld dry correction roller about 12 cm long: a slim light blue plastic body with a small window on top and a round white roller tip at the front end, with the tape visible on the roller. No tape reel sitting on top. Not a tape dispenser, not a stapler.',
    'DEMO-OFF-2012': 'A dark grey desktop two-hole punch lying on its wide base: a body with a dark lever on the front and two round silver punch heads on top of the body, 80 mm apart, with two round die holes in the base plate. Not a stapler, not a sharpener. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-2013': 'A transparent plastic ruler, 30 cm long, lying flat: a clear see-through strip, almost colourless, with a fine millimetre scale along its top edge. Not opaque and not metal. Long and thin. Not a set square and not a book. No labels or printing apart from the millimetre scale.',
    'DEMO-OFF-2014': 'A pair of office scissors lying flat, with two dark grey ring handles and long silver blades crossing at a screw pivot. Not a craft knife, not pliers.',
    'DEMO-OFF-2015': 'A glue stick standing upright: a white plastic stick with a flat top and a teal cap on top. Not a tube of glue, not a lipstick.',
    'DEMO-OFF-2016': 'A flat A5 ruled notepad lying on a plain card back, with a glued top binding (a pale glue strip along the top edge, no wire coil) and white ruled sheets showing on top. Not a hard-cover notebook, not a wire-bound pad. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-2017': 'A flat A5 notebook with a slate-grey hard cover, a dark spine strip on the left, white page edges on the right and a teal ribbon bookmark hanging from the top edge. Not a spiral notepad.',
    'DEMO-OFF-2018': 'A small stack of loose A6 index cards lying flat: white cards with blue horizontal ruling on the top card, no binding, no pad, not a notebook. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-2019': 'A cardboard box of rollerball pens: a light brown open box with twelve black rollerball pens standing upright and tilted out of the box mouth. Not single pens, no lettering.',
}
