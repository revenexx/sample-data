"""Office pack: desk accessories. Also the example for every other model module.

A module lists its products in SKUS: sku -> (builder, kwargs) or
(builder, kwargs, camera). Camera keys: yaw (default -30), pitch (18) and
fill (0.74, how much of the frame the product fills). Variants that only
differ in size share a builder call; colour variants pass their colour.
HINTS (optional) adds words to the AI prompt where the product name alone
could be misread.
"""

PEN = {'blue': '#2E5FA8', 'red': '#C7362F', 'black': '#2B2E33', 'green': '#2F8A57'}


def tape_dispenser(k):
    """Desk tape dispenser, metal, for 19 mm tape. Base 160 x 60 x 40 mm."""
    k.box((160, 60, 34), (0, 0, 17), 'metal', bevel=6, metal=0.35, rough=0.35)        # weighted base
    k.box((150, 50, 3), (0, 0, 35), 'dark', bevel=1)                                    # rubber top inlay
    k.box((150, 2, 14), (0, -30.2, 16), 'light', bevel=1)                               # front strip
    k.cyl(36, 19, (-10, 0, 74), '#E9EEF2', rot=(90, 0, 0), alpha=0.5, rough=0.15)      # tape roll
    k.cyl(24, 19.4, (-10, 0, 74), '#D9C9A8', rot=(90, 0, 0))                            # cardboard core
    k.cyl(5, 26, (-10, 0, 74), 'dark', rot=(90, 0, 0))                                  # spindle
    k.box((10, 26, 40), (-10, 0, 52), 'mid', bevel=2)                                   # spindle post
    k.box((20, 26, 18), (66, 0, 44), 'body', bevel=3)                                   # cutter block
    k.box((22, 22, 1.5), (72, 0, 54), 'steel', metal=1, rough=0.2)                      # serrated blade


def pen_holder(k, colour='blue'):
    """Pen holder with 3 compartments: two tubes and a low tray, a few pens."""
    c = PEN[colour]
    k.box((168, 60, 4), (0, 0, 2), c, bevel=1, rough=0.35)                               # shared base
    for x in (-52, 0, 52):                                                               # three cups in one row
        k.cyl(24, 95, (x, 0, 47.5), c, rough=0.35, bevel=1.5)
        k.cyl(21, 0.6, (x, 0, 95.2), '#1A1C20')                                          # openings
    for x, col in ((-52, '#F2F2F2'), (0, '#E8C21A'), (52, '#2B2E33')):                    # one pen per cup
        k.cyl(4, 150, (x, 0, 85), col, rot=(8, 0, 0))


SKUS = {
    'DEMO-OFF-4005': (tape_dispenser, {}),
    'DEMO-OFF-4001': (pen_holder, {'colour': 'blue'}),
    **{f'DEMO-OFF-4001-{c.upper()}': (pen_holder, {'colour': c}) for c in PEN},
}

HINTS = {
    'DEMO-OFF-4001': 'A desk pen holder with three compartments in a row: one matt plastic body with three cups side by side, each cup holding one pen: a white pen, a yellow pencil and a black pen, nothing else. No scissors, no ruler, no printed scale. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-4005': 'A heavy metal desk tape dispenser with a roll of clear adhesive tape and a serrated cutter.',
}
