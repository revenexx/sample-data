"""Office pack, series 6: shipping and mailing supplies.

Envelopes and labels lie flat (camera pitch 50). Tape and wrapping rolls
stand or lie with their hole or end towards the camera. Cartons stand upright.
"""

FLAT = {'pitch': 50, 'fill': 0.8}


def envelope_stack(k, w, h, thick, color='#F4F1EA', window=None):
    """A stack of envelopes lying flat. window = (x, y, w, h) on the top one."""
    k.box((w, h, thick), (0, 0, thick / 2), color, bevel=0.8)
    if window:
        wx, wy, ww, wh = window
        k.box((ww, wh, 0.5), (wx, wy, thick + 0.25), '#CFDCE6', bevel=0)


def padded_mailer(k, w, h, thick, color='#DCD2BE'):
    """A stack of padded mailers lying flat, with a sealing strip on top."""
    k.box((w, h, thick), (0, 0, thick / 2), color, bevel=4)
    k.box((w - 12, 12, 0.6), (0, h / 2 - 18, thick + 0.3), '#B9A98A', bevel=0)


def packing_tape(k):
    """One roll of clear packing tape, standing on its edge with the core facing the camera."""
    k.cyl(75, 50, (0, 0, 75), '#DCE9F0', rot=(90, 0, 0), rough=0.3)
    k.cyl(38, 52, (0, 0, 75), '#C9A97A', rot=(90, 0, 0))


def kraft_roll(k):
    """Brown kraft paper on one roll lying on its side, with cardboard core ends."""
    k.cyl(100, 500, (0, 0, 100), '#B98B57', rot=(0, 90, 0), rough=0.8)
    k.cyl(38, 510, (0, 0, 100), '#D8C3A0', rot=(0, 90, 0))


def bubble_roll(k):
    """Bubble wrap roll lying on its side: pale blue-white film, cardboard core."""
    k.cyl(130, 1000, (0, 0, 130), '#CFE3EE', rot=(0, 90, 0), rough=0.4)
    k.cyl(40, 1010, (0, 0, 130), '#E9E0CE', rot=(0, 90, 0))


def carton(k, w, d, h, color='#C29B6D'):
    """One assembled corrugated carton standing upright, with a tape strip on top."""
    k.box((w, d, h), (0, 0, h / 2), color, bevel=1.5, rough=0.8)
    k.box((48, d, 0.6), (0, 0, h + 0.3), '#D9C29A', bevel=0)


def label_sheet(k, lw, lh, cols, rows=7):
    """A4 label sheet lying flat: a grid of white labels on a paper sheet."""
    k.box((210, 297, 10), (0, 0, 5), '#F4F4F2', bevel=0.5)
    for i in range(cols):
        for j in range(rows):
            x = (i - (cols - 1) / 2) * lw
            y = (j - (rows - 1) / 2) * lh
            k.box((lw - 3, lh - 3, 0.4), (x, y, 10.2), '#FFFFFF', bevel=0)


def full_sheet(k):
    """A stack of A4 full-sheet label paper lying flat."""
    k.box((210, 297, 10), (0, 0, 5), '#FFFFFF', bevel=0.5)


SKUS = {
    'DEMO-OFF-6001': (envelope_stack, {'w': 229, 'h': 162, 'thick': 60, 'window': (60, -10, 90, 35)}, FLAT),
    'DEMO-OFF-6002': (envelope_stack, {'w': 220, 'h': 110, 'thick': 20}, FLAT),
    'DEMO-OFF-6003': (envelope_stack, {'w': 324, 'h': 229, 'thick': 35}, FLAT),
    'DEMO-OFF-6004': (padded_mailer, {'w': 170, 'h': 110, 'thick': 22}, FLAT),
    'DEMO-OFF-6005': (padded_mailer, {'w': 240, 'h': 170, 'thick': 28}, FLAT),
    'DEMO-OFF-6006': (packing_tape, {}),
    'DEMO-OFF-6007': (kraft_roll, {}),
    'DEMO-OFF-6008': (carton, {'w': 200, 'd': 140, 'h': 80}),
    'DEMO-OFF-6009': (carton, {'w': 300, 'd': 200, 'h': 150}),
    'DEMO-OFF-6010': (carton, {'w': 400, 'd': 300, 'h': 200}),
    'DEMO-OFF-6011': (bubble_roll, {}),
    'DEMO-OFF-6012': (label_sheet, {'lw': 105, 'lh': 37, 'cols': 2, 'rows': 8}, FLAT),
    'DEMO-OFF-6013': (label_sheet, {'lw': 70, 'lh': 37, 'cols': 3}, FLAT),
    'DEMO-OFF-6014': (full_sheet, {}, FLAT),
}

HINTS = {
    'DEMO-OFF-6001': 'A neat stack of white C5 envelopes lying flat, the whole stack visible and centred in the frame, about 6 cm high, the top envelope with a clear rectangular address window. Plain paper envelopes, not a sealed bag and not a folder.',
    'DEMO-OFF-6002': 'A stack of white DL envelopes without any window, lying flat in a neat pile about 2 cm high. Plain self-adhesive paper envelopes, not a card and not a notepad.',
    'DEMO-OFF-6003': 'A stack of white C4 envelopes, large and flat, in a pile about 3.5 cm high, lying on a desk. Plain paper envelopes without window, bigger than a DIN A5 sheet, not a poster.',
    'DEMO-OFF-6004': 'A stack of about ten small padded mailers lying flat, pale beige-grey paper bags with a soft air-bubble lining visible at the edges and a darker sealing strip along the top. Not a cardboard box and not a book.',
    'DEMO-OFF-6005': 'A stack of about ten larger padded mailers lying flat, beige-grey paper with an air-bubble lining showing at the edges and a darker sealing strip on top. Bigger and thicker than a small mailer, not a box.',
    'DEMO-OFF-6006': 'One roll of clear packing tape standing on its edge, the core hole facing the camera, with a pale transparent tape wound around a cardboard core. Not a coloured tape and not a sticky label.',
    'DEMO-OFF-6007': 'One large roll of brown kraft wrapping paper lying on its side, plain matt brown paper wound tightly, with a cardboard core visible at both ends. Not a box and not a sheet of printed gift wrap.',
    'DEMO-OFF-6008': 'One small assembled shipping carton standing upright, plain brown corrugated cardboard box with a flat strip of tape across the top, square-cornered and closed. Not a gift box and not a wooden crate; one carton only.',
    'DEMO-OFF-6009': 'One medium assembled shipping carton standing upright, plain brown corrugated cardboard with a strip of tape across the top, closed and square. Not a gift box and not a wooden crate; one carton only.',
    'DEMO-OFF-6010': 'One large assembled shipping carton standing upright, plain brown corrugated cardboard with a strip of tape on the top flaps, closed and square. Not a gift box and not a wooden crate; one carton only.',
    'DEMO-OFF-6011': 'One large roll of clear bubble wrap lying on its side, pale blue-white plastic film wound around a cardboard core, with small round air bubbles visible on the wound surface. Not a sheet of paper and not a foam roll.',
    'DEMO-OFF-6012': 'A small stack of A4 label sheets lying flat at an angle, the top sheet showing a neat grid of 16 blank white labels in exactly two columns by eight rows, each label a wide strip about 105 by 37 mm, separated by thin grey cut lines on a slightly off-white backing. Not a notepad. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-6013': 'A small stack of A4 label sheets lying flat at an angle, the top sheet showing a neat grid of 21 blank white labels (three columns by seven rows) separated by clearly visible thin grey cut lines on a slightly off-white backing, with a soft shadow so the stack stands out from the white background. No printed text or logos. Not a notepad.',
    'DEMO-OFF-6014': 'A small stack of plain A4 full-sheet label paper lying flat at an angle, one corner of the top sheet slightly peeled back to show the glossy backing paper, with a soft shadow so the white stack stands out from the white background. No printed text. Not a notepad, not a printed form.',
}
