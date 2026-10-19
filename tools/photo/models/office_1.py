"""Office pack, series 1: copy paper, ring and lever arch binders, clip folders, wallets,
clipboards, index dividers, suspension files, sleeves and divider sheets.

Units mm, products stand on z=0 with the front facing -Y. Binders stand on their bottom
edge (cover facing -Y, spine on the -X side). Flat items (paper, folders, wallets, the
divider pile) lie flat and are shot from a higher pitch.
A model product (kind model) uses the kwargs of its first variant.
"""

BLUE = '#2E5FA8'
RED = '#C2403A'
BLACK = '#2A2D33'
GREEN = '#3E8E5A'
GREY = '#9AA1AB'
LIGHT = '#D9DDE3'
FLAT = {'pitch': 50}


def _rect(w, h, r=14, n=5):
    """Rounded rectangle outline (corner radius r, n points per corner)."""
    import math
    pts = []
    for cx, cy, a0 in ((w / 2 - r, -h / 2 + r, -90), (w / 2 - r, h / 2 - r, 0),
                       (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180)):
        for i in range(n + 1):
            a = math.radians(a0 + 90 * i / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ream(k, long=305, wide=215, thick=55, colour='#FBFBFA'):
    """Copy paper ream: a wrapper box lying flat, with a teal band across the label face on top."""
    k.box((wide, long, thick), (0, 0, thick / 2), colour, bevel=1.5)                    # wrapper box
    k.box((wide + 0.6, 46, 1.4), (0, 0, thick + 0.4), k.ACCENT['off'], bevel=0.3)       # band on the label face


def binder(k, colour=BLUE, w=235, h=300, spine=75, lever=False, rings=2):
    """Ring binder (lever=False) or lever arch file, standing: cover to the front, spine on the left."""
    k.box((w, spine, h), (0, 0, h / 2), colour, bevel=3, rough=0.4)                     # closed binder
    k.box((150, 1.2, 66), (12, -spine / 2 - 0.6, 0.6 * h), '#FFFFFF', bevel=0.4)        # cover label field
    k.box((6, 1.4, 66), (12 - 75, -spine / 2 - 0.9, 0.6 * h), k.ACCENT['off'])          # small teal strip on the field
    k.box((1.2, spine * 0.7, h * 0.5), (-w / 2 - 0.6, 0, 0.5 * h), '#FFFFFF', bevel=0.3)  # spine label
    if lever:
        k.box((w - 30, 40, 6), (0, 0, h + 3), 'metal', bevel=1.5)                       # lever mechanism plate
        k.box((w - 70, 14, 12), (0, 0, h + 11), 'dark', bevel=2)                        # lever arm
    else:
        k.box((150, 34, 6), (0, 0, h + 3), 'metal', bevel=1.5)                          # ring mechanism plate
        for rx in ((-60, -20, 20, 60) if rings == 4 else (-30, 30)):
            k.cyl(7, 14, (rx, 0, h + 13), 'metal', verts=24)                            # rings in a row


def clip_folder(k, colour=BLUE):
    """Clip folder A4, lying: a plastic cover with a metal clip strip on the far edge."""
    k.slab(_rect(232, 312), 4, 0, colour, smooth=0)                                    # cover
    k.box((120, 14, 8), (0, 146, 8), 'metal', bevel=2)                                  # clip strip


def wallet(k, colour=BLUE):
    """Document wallet A4, lying: a thick card body with a flap on the far half and an elastic band."""
    k.slab(_rect(232, 312), 14, 0, colour, smooth=0)                                    # closed body
    k.slab(_rect(232, 150), 3, 14, colour, smooth=0)                                    # flap, half-length
    k.box((232, 8, 18), (0, 20, 9), 'dark', bevel=1)                                    # elastic band


def clipboard(k, colour=BLUE):
    """Clipboard folder A4, standing: a board with a metal clip on the top edge and a front pocket."""
    k.box((230, 6, 318), (0, 0, 159), colour, bevel=2)                                  # board
    k.box((212, 2, 200), (0, -4, 128), 'light', bevel=0.5)                              # front pocket
    k.box((86, 26, 8), (0, -6, 322), 'metal', bevel=2)                                  # top clip


def index_dividers(k):
    """Plastic index dividers A4, standing: one sheet with ten coloured tabs across the top edge."""
    k.box((210, 2, 297), (0, 0, 148.5), '#FFFFFF', bevel=0.5)
    tabs = [BLUE, RED, GREEN, GREY]
    for i in range(10):
        k.box((20, 2.4, 22), (-94.5 + 21 * i, 0, 297 + 9), tabs[i % 4], bevel=0.6)


def suspension_files(k):
    """Suspension files: five cardboard folders standing in a row, each with a tab on top."""
    for i in range(5):
        y = -8 + 4 * i
        k.box((236, 1.6, 300), (0, y, 150), 'paper', bevel=0.4)                         # folder
        k.box((60, 1.8, 22), (-60, y, 311), 'paperDark', bevel=0.4)                     # tab card
        k.cyl(2.5, 262, (0, y, 296), 'steel', rot=(0, 90, 0), metal=1, rough=0.3)       # hanging rail
        for sx in (-1, 1):                                                              # hooks past the sides
            k.cyl(2, 14, (sx * 124, y, 290), 'steel', metal=1, rough=0.3)


def sleeves(k):
    """Document sleeves: three clear sleeves stacked in a bundle, a coloured punched bar at the bottom."""
    for i in range(3):
        k.box((216, 1.2, 296), (0, -6 + 6 * i, 150), '#E8F0F4', alpha=0.45, rough=0.1)  # clear sleeve
    k.box((216, 16, 6), (0, 0, 3), k.ACCENT['off'], bevel=1)                             # punched bar


def divider_sheets(k):
    """Divider sheets, cardboard: four sheets stepped down the stack, each with a tab on the top right."""
    for i in range(4):
        h = 297 - 12 * i
        y = -6 + 4.5 * i
        k.box((210, 1.5, h), (0, y, h / 2), 'paper', bevel=0.3)                         # sheet
        k.box((34, 1.8, 14), (62, y, h - 7), 'paperDark', bevel=0.3)                    # tab


HINTS = {
    'DEMO-OFF-1001': 'A flat rectangular wrapper box of copy paper lying on its side, plain white wrapping with a single thin teal band across the top face, the band plain with no printed words. Not a stack of loose sheets, not a printer. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1002': 'A blue ring binder standing on its bottom edge with the spine on the left: a thick blue plastic cover with a blank white panel on the front and four metal rings in a row along the top edge (four rings, not two). Not a lever arch file and not a folder. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1002-BLUE': 'A blue ring binder standing on its bottom edge with the spine on the left: a thick blue plastic cover with a white label field on the front and two metal rings visible on the top edge. Not a lever arch file and not a folder.',
    'DEMO-OFF-1002-RED': 'A red ring binder standing on its bottom edge with the spine on the left: a thick red plastic cover with a blank white panel on the front and four metal rings in a row along the top edge (four rings, not two). Not a lever arch file and not a folder. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1002-BLACK': 'A black ring binder standing on its bottom edge with the spine on the left: a thick black plastic cover with a blank white panel on the front and four metal rings in a row along the top edge (four rings, not two). Not a lever arch file and not a folder. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1003': 'A classic European lever arch file (Ordner) in light grey with an 8 cm spine, standing upright and closed, seen from the front left: a rectangular board cover, a blank white label field on the front, a wide spine on the left with a blank white spine label, and a metal lever mechanism plate with a dark lever arm across the top edge. Not a ring binder, not a box file.',
    'DEMO-OFF-1004': 'A flat rectangular wrapper box of copy paper lying on its side, plain white wrapping with a single thin teal band across the top face, slightly thinner than a full ream. Not a stack of loose sheets.',
    'DEMO-OFF-1005': 'A flat rectangular wrapper box of copy paper lying on its side, plain white wrapping with a single thin teal band across the top face, slightly thicker than a standard ream, with a clean plain side panel. Not a stack of loose sheets. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1006': 'A flat wide rectangular wrapper box of A3 copy paper lying on its side, plain white wrapping with a single thin teal band across the top face, wider and longer than an A4 ream. Not an A4 ream.',
    'DEMO-OFF-1007': 'A flat rectangular wrapper box of recycled paper lying on its side, plain off-white wrapping with a single thin teal band across the top face, greyer and creamier than a bright white ream. Not a stack of loose sheets.',
    'DEMO-OFF-1008': 'A low flat wrapper box of heavy 100 g paper lying on its side, plain white wrapping with a single thin teal band across the top face, shorter in height than a standard ream. Not a stack of loose sheets.',
    'DEMO-OFF-1009': 'A small mid-grey ring binder standing on its bottom edge with the spine on the left: a narrow A5 cover, a grey plastic body, a blank white panel on the front and four metal rings in a row along the top edge (four rings, not two). Not a lever arch file. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1010': 'A slim European lever arch file (Ordner) with a 5 cm spine in blue plastic-covered board, standing upright and closed, seen from the front left: a plain rectangular cover, the spine on the left with a round finger hole near the bottom and a blank white spine panel. The lever mechanism is inside and not visible. Not a ring binder, not a clipboard. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1010-BLUE': 'A blue lever arch file standing on its bottom edge with the spine on the left: a slim blue plastic cover with a white label field on the front, a metal lever mechanism plate and a dark lever arm across the top edge. Not a ring binder.',
    'DEMO-OFF-1010-BLACK': 'A black lever arch file standing on its bottom edge with the spine on the left: a slim black plastic cover with a white label field on the front, a metal lever mechanism plate and a dark lever arm across the top edge. Not a ring binder.',
    'DEMO-OFF-1010-GREY': 'A grey lever arch file standing on its bottom edge with the spine on the left: a slim grey plastic cover with a white label field on the front, a metal lever mechanism plate and a dark lever arm across the top edge. Not a ring binder.',
    'DEMO-OFF-1011': 'A thin flat A4 clip folder lying flat: a blue plastic cover with a metal clip strip along the far edge. Not a document wallet, which has a flap and an elastic band.',
    'DEMO-OFF-1011-BLUE': 'A thin flat A4 clip folder lying flat: a blue plastic cover with a metal clip strip along the far edge. Not a document wallet, which has a flap and an elastic band.',
    'DEMO-OFF-1011-RED': 'A thin flat A4 clip folder lying flat: a red plastic cover with a metal clip strip along the far edge. Not a document wallet, which has a flap and an elastic band.',
    'DEMO-OFF-1011-BLACK': 'A thin flat A4 clip folder lying flat: a black plastic cover with a metal clip strip along the far edge. Not a document wallet, which has a flap and an elastic band.',
    'DEMO-OFF-1011-GREEN': 'A thin flat A4 clip folder lying flat: a green plastic cover with a metal clip strip along the far edge. Not a document wallet, which has a flap and an elastic band.',
    'DEMO-OFF-1012': 'A thick flat A4 document wallet lying flat: a blue card body with a flap folded over the far half and a dark elastic band across the near edge. Not a clip folder, which has a metal clip strip.',
    'DEMO-OFF-1012-BLUE': 'A thick flat A4 document wallet lying flat: a blue card body with a flap folded over the far half and a dark elastic band across the near edge. Not a clip folder, which has a metal clip strip.',
    'DEMO-OFF-1012-RED': 'A thick flat A4 document wallet lying flat: a red card body with a flap folded over the far half and a dark elastic band across the near edge. Not a clip folder, which has a metal clip strip.',
    'DEMO-OFF-1012-BLACK': 'A thick flat A4 document wallet lying flat: a black card body with a flap folded over the far half and a dark elastic band across the near edge. Not a clip folder, which has a metal clip strip.',
    'DEMO-OFF-1013': 'A blue clipboard folder standing on its bottom edge: a stiff board with a metal clip on the top edge and a light front pocket visible on the front. Not a clip folder lying flat, and not a ring binder.',
    'DEMO-OFF-1013-BLUE': 'A blue clipboard folder standing on its bottom edge: a stiff board with a metal clip on the top edge and a light front pocket visible on the front. Not a clip folder lying flat, and not a ring binder.',
    'DEMO-OFF-1013-RED': 'A red clipboard folder standing on its bottom edge: a stiff board with a metal clip on the top edge and a light front pocket visible on the front. Not a clip folder lying flat, and not a ring binder.',
    'DEMO-OFF-1013-GREEN': 'A green clipboard folder standing on its bottom edge: a stiff board with a metal clip on the top edge and a light front pocket visible on the front. Not a clip folder lying flat, and not a ring binder.',
    'DEMO-OFF-1014': 'A single thin white plastic index divider sheet standing upright, with exactly ten coloured tabs side by side in one row along its top edge, all the same size, alternating blue, red, green and grey, plain with no lettering. Not a cardboard divider and not a folder. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-1015': "Five cardboard suspension folders standing side by side in a row. Each folder has a metal hanging rail across its top edge, and the rail's hooked ends stick out past both sides of the folder. Each folder also has a small card tab on its top edge. Plain buff-coloured card. Not a single folder, not a binder and not a file box. No labels or printing.",
    'DEMO-OFF-1016': 'Thin, nearly transparent plastic sleeves open at the top, stacked in a bundle.',
    'DEMO-OFF-1017': 'Stiff cardboard divider sheets with a tab each, stepped in a stack.',
}

SKUS = {
    'DEMO-OFF-1001': (ream, {}, FLAT),
    'DEMO-OFF-1002': (binder, {'colour': BLUE, 'rings': 4}),
    'DEMO-OFF-1002-BLUE': (binder, {'colour': BLUE, 'rings': 4}),
    'DEMO-OFF-1002-RED': (binder, {'colour': RED, 'rings': 4}),
    'DEMO-OFF-1002-BLACK': (binder, {'colour': BLACK, 'rings': 4}),
    'DEMO-OFF-1003': (binder, {'colour': LIGHT, 'spine': 80, 'lever': True}),
    'DEMO-OFF-1004': (ream, {'thick': 50}, FLAT),
    'DEMO-OFF-1005': (ream, {'thick': 58}, FLAT),
    'DEMO-OFF-1006': (ream, {'long': 420, 'wide': 297, 'thick': 55}, FLAT),
    'DEMO-OFF-1007': (ream, {'colour': 'paper'}, FLAT),
    'DEMO-OFF-1008': (ream, {'thick': 30}, FLAT),
    'DEMO-OFF-1009': (binder, {'colour': 'mid', 'w': 155, 'h': 215, 'spine': 50, 'rings': 4}),
    'DEMO-OFF-1010': (binder, {'colour': BLUE, 'spine': 50, 'lever': True}),
    'DEMO-OFF-1010-BLUE': (binder, {'colour': BLUE, 'spine': 50, 'lever': True}),
    'DEMO-OFF-1010-BLACK': (binder, {'colour': BLACK, 'spine': 50, 'lever': True}),
    'DEMO-OFF-1010-GREY': (binder, {'colour': GREY, 'spine': 50, 'lever': True}),
    'DEMO-OFF-1011': (clip_folder, {'colour': BLUE}, FLAT),
    'DEMO-OFF-1011-BLUE': (clip_folder, {'colour': BLUE}, FLAT),
    'DEMO-OFF-1011-RED': (clip_folder, {'colour': RED}, FLAT),
    'DEMO-OFF-1011-BLACK': (clip_folder, {'colour': BLACK}, FLAT),
    'DEMO-OFF-1011-GREEN': (clip_folder, {'colour': GREEN}, FLAT),
    'DEMO-OFF-1012': (wallet, {'colour': BLUE}, FLAT),
    'DEMO-OFF-1012-BLUE': (wallet, {'colour': BLUE}, FLAT),
    'DEMO-OFF-1012-RED': (wallet, {'colour': RED}, FLAT),
    'DEMO-OFF-1012-BLACK': (wallet, {'colour': BLACK}, FLAT),
    'DEMO-OFF-1013': (clipboard, {'colour': BLUE}),
    'DEMO-OFF-1013-BLUE': (clipboard, {'colour': BLUE}),
    'DEMO-OFF-1013-RED': (clipboard, {'colour': RED}),
    'DEMO-OFF-1013-GREEN': (clipboard, {'colour': GREEN}),
    'DEMO-OFF-1014': (index_dividers, {}),
    'DEMO-OFF-1015': (suspension_files, {}),
    'DEMO-OFF-1016': (sleeves, {}),
    'DEMO-OFF-1017': (divider_sheets, {}),
}
