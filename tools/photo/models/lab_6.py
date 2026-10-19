"""Lab pack, series 6: racks, boxes and storage. Tube racks for 1.5 ml, 2 ml, 15 x 50 ml
and 24 tubes, a 96-place rack, cryo and sample boxes (polycarbonate, polypropylene,
card), stackable storage boxes (5 l and 25 l), a wall pipette holder, glass storage
jar, a wide-neck bottle and a sheet of cryo labels. Racks are empty: the holes show as
dark openings. Units mm, product stands on z=0, front faces -Y.
"""

BODY = '#4A515C'
MID = '#7B838F'
LIGHT = '#C9CED6'
WHITE = '#F7F7F5'
PAPER = '#E6DCCB'
PAPER_DARK = '#CDBFA6'
HOLE = '#1A1C20'
BLUE = '#2F5FA8'
RED = '#C7362F'
GLASS = 'glass'


def _grid_holes(k, cols, rows, pitch, r, z):
    """Dark openings on a top surface, centred on x and y."""
    for i in range(cols):
        for j in range(rows):
            x = (i - (cols - 1) / 2) * pitch
            y = (j - (rows - 1) / 2) * pitch
            k.cyl(r, 0.6, (x, y, z), HOLE)


def _open_rack(k, L, W, H, nx, ny, pitch, r):
    """Open test tube rack: lower deck as a floor, upper deck with round openings, two end walls.
    Open at the front and back so the tubes can be seen through it."""
    k.box((L, W, 3), (0, 0, 1.5), LIGHT, bevel=1)                                          # lower deck (floor)
    k.box((L, W, 3), (0, 0, H - 1.5), LIGHT, bevel=1)                                      # upper deck
    _grid_holes(k, nx, ny, pitch, r, H + 0.2)                                               # openings in the upper deck
    for x in (-L / 2 + 3, L / 2 - 3):
        k.box((6, W, H), (x, 0, H / 2), LIGHT, bevel=1)                                    # end walls


def rack_24(k):
    """Open polypropylene test tube rack for 24 tubes: two perforated decks held by end walls, open front and back."""
    _open_rack(k, 230, 110, 85, 6, 4, 32, 9)


def rack_15_50ml(k):
    """Open rack for 15 centrifuge tubes of 50 ml: two perforated decks held by end walls, open front and back, standing taller."""
    _open_rack(k, 220, 120, 95, 5, 3, 40, 14)


def rack_96_15ml(k):
    """Rack for 96 tubes of 1.5 ml: a flat block with a 12 x 8 grid of small openings."""
    k.box((200, 130, 34), (0, 0, 17), BODY, bevel=3)
    _grid_holes(k, 12, 8, 14.5, 3.6, 34.2)


def rack_48_2ml(k):
    """Rack for 48 tubes of 2 ml: a low block with 48 openings in 8 x 6."""
    k.box((220, 110, 36), (0, 0, 18), BODY, bevel=3)
    _grid_holes(k, 8, 6, 24, 5.5, 36.2)


def cryo_box_81(k, body=MID, lid=BODY, recess=False):
    """Cryo box for 81 vessels: a square box with a 9 x 9 grid of compartments, lid on top.
    recess=True makes the centre well a larger round finger recess."""
    k.box((130, 130, 42), (0, 0, 21), body, bevel=3)
    k.box((132, 132, 8), (0, 0, 46), lid, bevel=2)
    _grid_holes(k, 9, 9, 12.5, 3.8, 50.2)
    if recess:
        k.cyl(7, 0.6, (0, 0, 50.5), HOLE)                                                 # finger recess in the centre


def sample_box_100(k):
    """Sample box, 100 positions: a white polypropylene box, snap-on lid, 10 x 10 grid."""
    k.box((130, 130, 46), (0, 0, 23), WHITE, bevel=3)
    k.box((132, 132, 10), (0, 0, 51), WHITE, bevel=2)
    _grid_holes(k, 10, 10, 11, 2.9, 56.2)


def sample_box_25_poly(k):
    """Polycarbonate sample box, 25 positions: a clear box with a 5 x 5 grid inside."""
    k.box((130, 130, 50), (0, 0, 25), GLASS, bevel=4, alpha=0.4, rough=0.1)
    k.box((120, 120, 3), (0, 0, 4), MID, bevel=1)                                       # base grid plate
    _grid_holes(k, 5, 5, 20, 6, 6.2)


def card_archive_box(k):
    """Card archive box, 100 positions: a paper-coloured carton, lid lifted off and lying beside it,
    the top showing a 10 x 10 grid of card cells, and a hand hole in the front."""
    k.box((130, 130, 50), (0, 0, 25), PAPER, bevel=2)
    _grid_holes(k, 10, 10, 11.5, 4.5, 50.2)                                              # 100 card cells
    k.box((132, 132, 6), (-150, 0, 3), PAPER_DARK, bevel=1)                              # lid, lifted off
    k.box((34, 4, 14), (0, -66, 30), PAPER_DARK, bevel=1)                                # hand hole


def storage_box_5l(k):
    """Stackable 5 l storage box: a grey box with a lid strip and a handle cut-out."""
    k.box((240, 170, 110), (0, 0, 55), BODY, bevel=6)
    k.box((246, 176, 14), (0, 0, 117), MID, bevel=3)                                    # lid
    k.box((70, 6, 14), (0, -86, 62), HOLE, bevel=2)                                     # handle cut-out


def storage_box_25l(k):
    """Stackable 25 l storage box: a larger grey box with a lid and a wide grip."""
    k.box((400, 300, 190), (0, 0, 95), BODY, bevel=8)
    k.box((408, 308, 22), (0, 0, 201), MID, bevel=4)                                    # lid
    k.box((130, 6, 26), (0, -151, 120), HOLE, bevel=3)                                  # wide grip


def wall_pipette_holder(k):
    """Stainless steel wall holder: an upright plate with four round clamp rings for pipettes."""
    k.box((120, 6, 170), (0, 0, 85), 'steel', bevel=2, metal=1, rough=0.25)
    for z in (35, 70, 105, 140):
        k.torus(12, 3, (0, -8, z), 'steel', rot=(90, 0, 0), metal=1, rough=0.25)


def storage_jar_1000(k):
    """Glass storage jar with a screw cap: clear glass body with a blue plastic cap."""
    k.cyl(50, 130, (0, 0, 75), GLASS, bevel=3, alpha=0.5, rough=0.1)
    k.cyl(53, 24, (0, 0, 152), BLUE, bevel=2)


def wide_neck_bottle(k):
    """Wide-neck polyethylene bottle, white, with a red screw cap."""
    pts = [(0, 0), (40, 0), (42, 10), (42, 120), (36, 138), (32, 142), (32, 150), (0, 150)]
    k.profile(pts, 84, y=0, color=WHITE, round_=3, mirror=True)
    k.cyl(35, 26, (0, 0, 163), RED, bevel=2)


def cryo_label_sheet(k):
    """Sheet of cryo labels: one flat A4-proportion backing sheet with a regular grid of small
    rectangular labels with thin gaps, a few labels peeled off."""
    k.box((210, 297, 1.2), (0, 0, 0.6), '#C4CAD3', bevel=0.3)
    gone = {(3, 4), (10, 2), (7, 8)}
    for i in range(16):
        for j in range(10):
            if (i, j) in gone:
                continue
            x = (i - 7.5) * 12
            y = (j - 4.5) * 27
            k.box((10, 25, 0.6), (x, y, 1.5), '#FFFFFF')
    k.box((10, 25, 0.6), (-100, -120, 6), '#FFFFFF', rot=(0, 0, 25))                         # one label peeled off


SKUS = {
    'DEMO-LAB-6001': (rack_24, {}, {'pitch': 35}),
    'DEMO-LAB-6002': (rack_15_50ml, {}, {'pitch': 35}),
    'DEMO-LAB-6003': (rack_96_15ml, {}, {'pitch': 35}),
    'DEMO-LAB-6004': (cryo_box_81, {'body': '#F2F2F0', 'lid': BODY}, {'pitch': 30}),
    'DEMO-LAB-6005': (sample_box_100, {}, {'pitch': 30}),
    'DEMO-LAB-6006': (storage_box_5l, {}, {'pitch': 18}),
    'DEMO-LAB-6007': (wall_pipette_holder, {}),
    'DEMO-LAB-6008': (storage_jar_1000, {}),
    'DEMO-LAB-6009': (wide_neck_bottle, {}),
    'DEMO-LAB-6010': (cryo_label_sheet, {}, {'pitch': 50}),
    'DEMO-LAB-6011': (storage_box_25l, {}, {'pitch': 22}),
    'DEMO-LAB-6012': (sample_box_25_poly, {}, {'pitch': 30}),
    'DEMO-LAB-6013': (rack_48_2ml, {}, {'pitch': 35}),
    'DEMO-LAB-6014': (cryo_box_81, {'body': LIGHT, 'lid': BODY, 'recess': True}, {'pitch': 30}),
    'DEMO-LAB-6015': (card_archive_box, {}, {'pitch': 30}),
}

HINTS = {
    'DEMO-LAB-6001': 'An empty open polypropylene test tube rack for exactly 24 tubes, white or light grey: two horizontal perforated decks held by end walls, the upper deck with exactly 24 round openings of one size in a 6 by 4 grid, open at the front and back so the tubes can be seen through it. Not a box, not a tray with a lid, no tubes inside. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-6002': 'An empty open polypropylene test tube rack for exactly 15 tubes of 50 ml, white or light grey: two horizontal perforated decks held by end walls, the upper deck with exactly 15 equal large round openings in 3 rows of 5, one hole size only, open at the front and back. Not a box, no tubes inside. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-6003': 'An empty flat dark grey rack for 96 small tubes of 1.5 ml: a wide, shallow block with a straight 12 by 8 grid of identical small round openings on its top face, all the same size and evenly spaced. Standing flat, no tubes inside. Not a microplate with wells and not a box with a lid.',
    'DEMO-LAB-6004': 'A square cryo box with a white polycarbonate body and a dark grey lid on top, the lid showing a 9 by 9 grid of small round compartments, about as wide as it is deep. Only the lid is coloured; the body is white. Not a freezer and not a tube rack: it is one closed square box.',
    'DEMO-LAB-6005': 'A square white polypropylene sample box with a snap-on white lid, its top showing a 10 by 10 grid of small round positions. Standing on a plain surface, no tubes visible. Not a cardboard box: it is plastic with a smooth matt finish and sharp corners.',
    'DEMO-LAB-6006': 'A stackable dark grey plastic storage box, wider than it is high, with a flat lid strip along the top edge and a dark handle cut-out in the front wall. Standing alone, no contents visible. Not a drawer and not a basket.',
    'DEMO-LAB-6007': 'A stainless steel wall-mounted pipette holder: a flat upright plate with four round clamp rings in a column, each ring standing out from the plate towards the viewer. Brushed steel with a soft shine, no pipettes inside. Not a rack on a bench.',
    'DEMO-LAB-6008': 'A clear glass storage jar with a straight cylindrical body and a blue plastic screw cap on top, standing alone. The glass shows a faint grey-green tint, no label. Not a bottle with a narrow neck and not a drinking glass.',
    'DEMO-LAB-6009': 'A white wide-neck polyethylene bottle with a plain body, rounded shoulders, a short wide neck and a red screw cap on top. No label, no printing. Not a narrow glass bottle, not a jar with a lid and not a sprayer.',
    'DEMO-LAB-6010': 'A single flat A4-proportion white backing sheet of cryo labels lying on the surface, a regular grid of small white rectangular labels in straight rows and columns with thin gaps, a few labels peeled off the sheet. Not a diamond pattern, not a tilted grid. No labels or printing.',
    'DEMO-LAB-6011': 'A large stackable dark grey plastic storage box, wider and deeper than it is high, with a flat lid along the top, and a wide dark grip recess in the front wall. Standing alone, no contents visible. Not a suitcase and not a pallet box.',
    'DEMO-LAB-6012': 'A square clear polycarbonate sample box with a grey base plate inside and a 5 by 5 grid of round positions visible at the bottom, the walls and lid transparent. Empty, standing alone. Not a glass case and not a solid grey box.',
    'DEMO-LAB-6013': 'An empty dark grey rack for 48 small tubes of 2 ml: a low block with a straight 8 by 6 grid of identical round openings on its top face, all the same size and evenly spaced, standing flat. No tubes inside. Not the 96 position rack: fewer and larger openings.',
    'DEMO-LAB-6014': 'A square light grey polycarbonate cryo box with a dark grey lid: the lid has exactly 81 small round wells in a 9 by 9 grid, evenly spaced over the whole lid, and one larger round finger recess in the centre of the grid. Not 12 by 12, not 100 wells. No tubes, no vials inside. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-6015': 'A square paper-coloured card archive box with its lid lifted off and lying flat beside it: the box top shows a 10 by 10 grid of 100 dark card cells, evenly spaced in straight rows, and a round hand hole in the front face. Plain carton, no printing, no labels. No text, no numbers, no logos, no labels anywhere on the product.',
}
