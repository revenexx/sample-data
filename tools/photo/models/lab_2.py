"""Lab pack, series 2: pipettes, pipette tips and racks, a pipette stand and a
pipette controller.

Pipettes stand upright on the tip of their shaft, as on the 2D drawings in
tools/art/lab*.mjs. Tip racks are 8 x 12 grids of tips (96) on a low frame.
White or light grey bodies with dark details; the accent pink (#C0397B) only
on plunger buttons and buttons. Units mm, product stands on z=0, front faces -Y.
"""

ACC = '#C0397B'


def pipette(k, tip=50, slim=False, display=False):
    """Single-channel pipette, upright on its tip: a conical tip, a grey ejector
    sleeve, a light barrel with a dark volume ring, a rounded handle and a
    dark top cap with a pink plunger button."""
    r = 13 if slim else 18
    k.cyl(1.4, tip, (0, 0, tip / 2), 'light', r2=3.6 if not slim else 3.0, verts=24)  # tip cone, point down
    k.cyl(r * 0.45, 30, (0, 0, tip + 15), 'mid', bevel=1)                              # ejector sleeve
    k.cyl(r * 0.7, 110, (0, 0, tip + 30 + 55), 'light', r2=r, bevel=2)               # barrel, wider at top
    k.cyl(r + 0.5, 14, (0, 0, tip + 80), 'dark', bevel=1)                              # dark volume ring
    k.cyl(r * 1.1, 90, (0, 0, tip + 140 + 45), 'white', bevel=4)                       # handle
    if display:
        k.box((r * 0.9, 2, 22), (0, -r * 1.1 - 0.5, tip + 185), 'dark', bevel=1)       # display window
    k.cyl(r * 0.8, 22, (0, 0, tip + 230 + 11), 'dark', bevel=2)                        # top cap
    k.cyl(9, 14, (0, 0, tip + 252 + 7), ACC, bevel=2)                                  # plunger button


def bottle_dispenser(k):
    """Bottle-top dispenser on a brown glass reagent bottle: a threaded adapter on the
    bottle neck, a clear graduated cylinder with a piston, a volume slider and a long
    curved discharge tube running out to the side."""
    brown = '#5A3418'
    k.cyl(40, 100, (0, 0, 50), brown, bevel=3)                                         # brown glass reagent bottle
    k.cyl(15, 16, (0, 0, 108), brown, bevel=1)                                         # bottle neck
    k.cyl(22, 16, (0, 0, 123), 'dark', bevel=1)                                        # threaded bottle adapter
    k.cyl(18, 100, (0, 0, 150), 'glass', alpha=0.5, rough=0.1)                         # clear graduated cylinder
    for i in range(5):
        k.box((10, 0.8, 0.8), (-18.5, -18.4, 145 + i * 16), 'dark')                    # volume ticks
    k.cyl(24, 30, (0, 0, 215), 'light', bevel=3)                                       # piston housing
    k.cyl(28, 16, (0, 0, 243), 'dark', bevel=3)                                        # top cap
    k.cyl(7, 8, (0, 0, 257), ACC, bevel=1)                                             # plunger button
    k.box((4, 4, 36), (21, -6, 175), 'dark', bevel=1)                                  # volume setting slider
    k.cyl(3, 80, (18 + 40, 0, 136), 'mid', rot=(0, 90, 0), verts=24)                   # discharge tube, out to the side
    k.sphere(3.5, (98, 0, 136), 'mid')                                                 # bend
    k.cyl(3, 80, (98, 0, 96), 'mid', verts=24)                                         # tube down to the beaker


def pipette_eight(k, tip=60):
    """8-channel pipette, upright: a slim handle on top with a plunger button, a
    wide horizontal manifold below it, and eight tip cones in one row pointing down."""
    h0 = tip + 25                                                                      # top of the manifold
    for i in range(8):
        x = (i - 3.5) * 9
        k.cyl(1.2, tip, (x, 0, tip / 2), 'light', r2=3.2, verts=16)                    # tip cone, point down
    k.box((80, 20, 25), (0, 0, tip + 12.5), 'dark', bevel=2)                           # wide horizontal manifold
    k.box((34, 36, 120), (0, 0, h0 + 60), 'light', bevel=6)                            # slim vertical handle
    k.box((44, 40, 16), (0, 0, h0 + 128), 'white', bevel=5)                            # handle top
    k.cyl(9, 10, (0, 0, h0 + 141), ACC, bevel=2)                                       # plunger button



def dispensing(k, big=False):
    """Dispensing pipette: a clear barrel with volume ticks on a short nozzle,
    a light piston housing and a dark cap with a pink button on top."""
    r = 22 if big else 18
    k.cyl(3.5, 12, (0, 0, 6), 'metal', metal=1, rough=0.25, verts=24)                  # nozzle
    k.cyl(r, 170, (0, 0, 12 + 85), 'glass', alpha=0.5, rough=0.1)                      # clear barrel
    for i in range(5):
        k.box((r * 0.6, 0.8, 0.8), (0, -r - 0.4, 40 + i * 25), 'dark')                 # volume ticks
    k.cyl(r + 6, 60, (0, 0, 182 + 30), 'light', bevel=3)                               # piston housing
    k.cyl(r + 10, 30, (0, 0, 242 + 15), 'dark', bevel=3)                               # top cap
    k.cyl(7, 10, (0, 0, 272 + 5), ACC, bevel=1)                                        # plunger button


def pipette_stand(k):
    """Benchtop stand: a dark base plate with six light upright posts, each with
    a body-grey cap, for single-channel pipettes."""
    k.box((240, 90, 18), (0, 0, 9), 'dark', bevel=4)                                   # base
    for i in range(6):
        x = (i - 2.5) * 36
        k.cyl(7, 130, (x, 0, 18 + 65), 'light', bevel=1)                               # post
        k.cyl(9, 10, (x, 0, 18 + 130 + 5), 'body', bevel=1)                            # cap


def tip_rack(k, tip=60, colour='white', base='mid', filter=False, sterile=False):
    """Pipette tip rack: 96 tips hang point down through a flat top plate, so only
    their round open tops show as small rings; the tip bodies are inside the box,
    whose walls are translucent. A hinged clear lid stands open at the back.
    Filter tips show a small white disc inside each top; sterile racks get a
    thin clear film over the tips."""
    k.box((125, 85, 4), (0, 0, 2), base, bevel=1)                                      # bottom frame
    k.box((125, 85, 52), (0, 0, 30), 'glass', alpha=0.35, rough=0.1)                   # translucent box walls
    k.box((125, 85, 4), (0, 0, 58), base, bevel=1)                                     # flat perforated top plate
    k.box((125, 2, 70), (0, 44, 35), 'glass', alpha=0.4, rough=0.1)                    # hinged lid, open at the back
    length = min(tip, 46)                                                              # tips stay inside the 60 mm box
    for i in range(8):
        for j in range(12):
            x = (j - 5.5) * 9
            y = (i - 3.5) * 9
            k.cyl(1.0, length, (x, y, 60.5 - length / 2), colour, r2=3.0, verts=12)  # tip, open top just above the plate
            k.torus(2.6, 0.45, (x, y, 60.3), 'dark')                                   # dark rim: each of the 96 holes shows
            if filter:
                k.cyl(2.2, 1.2, (x, y, 59.5), 'white', verts=12)                       # white filter disc in the top
    if sterile:
        k.box((130, 88, 3), (0, 0, 63), 'glass', alpha=0.5, rough=0.1)                 # sealing film over the tops



def tip_bag(k):
    """Bag of loose tips: a clear soft bag with a sealed top strip, and several
    tips poking out of the top."""
    k.box((120, 56, 80), (0, 0, 40), 'glass', alpha=0.5, rough=0.2, bevel=6)           # bag
    k.box((122, 58, 6), (0, 0, 80), 'mid', bevel=1)                                    # sealed top
    for i in range(5):
        x = (i - 2) * 22
        k.cyl(1.0, 100, (x, 0, 60), 'light', r2=3.0, verts=12)                         # loose tips


def controller(k):
    """Pistol-shaped pipette controller: a grip pointing down at the back, a body
    on top with two trigger buttons on the front of the grip, a round nose cone
    at the front and a long thin clear serological pipette pointing down at an angle."""
    k.box((40, 40, 90), (0, 20, 70), 'light', bevel=6)                                 # grip, pointing down
    for x in (-9, 9):
        k.box((12, 4, 14), (x, -2, 82), 'mid', bevel=1)                                # two trigger buttons on the grip
    k.box((44, 80, 50), (0, -5, 132), 'light', bevel=6)                                # body on top
    k.cyl(18, 30, (0, -50, 130), 'light', bevel=2, rot=(90, 0, 0))                     # round nose cone at the front
    k.cyl(2.5, 180, (0, -155, 130), 'glass', alpha=0.5, rot=(90, 0, 0))                # pipette shaft fitted into the nose, straight ahead



SKUS = {
    'DEMO-LAB-2001': (pipette, {'tip': 40}),
    'DEMO-LAB-2001-10UL': (pipette, {'tip': 40}),
    'DEMO-LAB-2001-200UL': (pipette, {'tip': 50}),
    'DEMO-LAB-2001-1000UL': (pipette, {'tip': 60}),
    'DEMO-LAB-2002': (tip_rack, {'tip': 60, 'colour': 'light', 'base': 'body'}),
    'DEMO-LAB-2003': (pipette, {'tip': 40, 'slim': True}),
    'DEMO-LAB-2003-2UL': (pipette, {'tip': 36, 'slim': True}),
    'DEMO-LAB-2003-20UL': (pipette, {'tip': 46, 'slim': True}),
    'DEMO-LAB-2004': (pipette_eight, {'tip': 45}),
    'DEMO-LAB-2004-20UL': (pipette_eight, {'tip': 45}),
    'DEMO-LAB-2004-200UL': (pipette_eight, {'tip': 60}),
    'DEMO-LAB-2004-1000UL': (pipette_eight, {'tip': 80}),
    'DEMO-LAB-2005': (dispensing, {'big': False}),
    'DEMO-LAB-2005-5ML': (dispensing, {'big': False}),
    'DEMO-LAB-2005-10ML': (dispensing, {'big': True}),
    'DEMO-LAB-2006': (pipette, {'tip': 40, 'display': True}),
    'DEMO-LAB-2006-10UL': (pipette, {'tip': 40, 'display': True}),
    'DEMO-LAB-2006-200UL': (pipette, {'tip': 50, 'display': True}),
    'DEMO-LAB-2006-1000UL': (pipette, {'tip': 60, 'display': True}),
    'DEMO-LAB-2007': (pipette_stand, {}),
    'DEMO-LAB-2008': (tip_rack, {'tip': 44, 'colour': 'white', 'base': 'light'}),
    'DEMO-LAB-2009': (tip_rack, {'tip': 80, 'colour': 'mid', 'base': 'light'}),
    'DEMO-LAB-2010': (tip_rack, {'tip': 54, 'colour': 'mid', 'base': 'light'}),
    'DEMO-LAB-2011': (tip_rack, {'tip': 68, 'colour': 'glass', 'base': 'light', 'filter': True}),
    'DEMO-LAB-2012': (tip_bag, {}),
    'DEMO-LAB-2013': (tip_rack, {'tip': 44, 'colour': 'white', 'base': 'light', 'sterile': True}),
    'DEMO-LAB-2014': (tip_rack, {'tip': 70, 'colour': 'white', 'base': 'body'}),
    'DEMO-LAB-2015': (tip_rack, {'tip': 120, 'colour': 'white', 'base': 'body', 'filter': True}),
    'DEMO-LAB-2016': (controller, {}),
}

_PIPETTE = (
    'A single-channel laboratory pipette standing upright on the tip of its shaft: '
    'a white barrel with a dark volume ring low down, a white rounded handle, a dark top cap '
    'and a small pink plunger button on top. A thin grey ejector sleeve sits below the barrel '
    'with a clear-grey conical tip at the bottom. No printed text. Not a syringe, not a pen.'
)

HINTS = {
    'DEMO-LAB-2001': 'An adjustable single-channel pipette: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2001-10UL': 'An adjustable single-channel pipette: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2001-200UL': 'An adjustable single-channel pipette: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2001-1000UL': 'An adjustable single-channel pipette: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2002': 'A pipette tip rack in light grey: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small round open top of a clear-grey tip inside it, and a clear lid standing open at the back. The tips hang point down inside the box and never stick up out of the rack. Not a box of loose tips, not a tip bag. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2003': 'A precision single-channel pipette for very small volumes, with a slim shaft: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2003-2UL': 'A precision single-channel pipette for very small volumes, with a slim shaft: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2003-20UL': 'A precision single-channel pipette for very small volumes, with a slim shaft: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2004': 'A single-channel style pipette with a slim upright handle and a plunger button on top, and at its bottom a wide horizontal manifold with eight tips in one row pointing down, each tip a white cone. Not a fork, not a comb, and no more than eight tips. No labels or printing.',
    'DEMO-LAB-2004-20UL': 'An 8-channel laboratory pipette standing upright, the whole pipette visible: a slim white handle with a round plunger button on top, and at the bottom a horizontal manifold, a flat bar with EXACTLY EIGHT plastic tips in one straight row (count them: eight, not seven, not nine, not ten), evenly spaced and all pointing straight down. Not a single-channel pipette, not a comb.',
    'DEMO-LAB-2004-200UL': 'An 8-channel laboratory pipette standing upright, the whole pipette visible: a slim white handle with a round plunger button on top, and at the bottom a horizontal manifold, a flat bar with EXACTLY EIGHT plastic tips in one straight row (count them: eight, not seven, not nine, not ten), evenly spaced and all pointing straight down. Not a single-channel pipette, not a comb.',
    'DEMO-LAB-2004-1000UL': 'An 8-channel laboratory pipette standing upright, the whole pipette visible: a slim white handle with a round plunger button on top, and at the bottom a horizontal manifold, a flat bar with EXACTLY EIGHT plastic tips in one straight row (count them: eight, not seven, not nine, not ten), evenly spaced and all pointing straight down. Not a single-channel pipette, not a comb.',
    'DEMO-LAB-2005': 'A dispensing pipette for larger volumes: a tall, clear glass barrel with thin white graduation lines only and no numerals, standing upright on a short steel nozzle, topped by a light piston housing and a dark cap with a small pink plunger button. Not a bottle and not a syringe with a needle. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2005-5ML': (
        'A dispensing pipette for larger volumes: a tall, clear glass barrel with volume ticks, standing upright '
        'on a short steel nozzle, topped by a light piston housing and a dark cap with a pink button. '
        'The barrel is slim, for the 1 to 5 ml range. No printed text. Not a bottle.'
    ),
    'DEMO-LAB-2005-10ML': (
        'A dispensing pipette for larger volumes: a tall, clear glass barrel with volume ticks, standing upright '
        'on a short steel nozzle, topped by a light piston housing and a dark cap with a pink button. '
        'The barrel is wider than the small version, for the 2 to 10 ml range. No printed text. Not a bottle.'
    ),
    'DEMO-LAB-2006': 'A digital single-channel pipette with a small blank grey display instead of a volume window: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2006-10UL': 'A digital single-channel pipette with a small blank grey display instead of a volume window: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2006-200UL': 'A digital single-channel pipette with a small blank grey display instead of a volume window: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2006-1000UL': 'A digital single-channel pipette with a small blank grey display instead of a volume window: an ergonomic handheld air-displacement laboratory pipette about 25 cm long, shown standing vertically upright as a catalogue cut-out, plunger button at the top and tip pointing down, the whole pipette visible: a curved white and light grey plastic handle with a finger hook, a plunger button on top with a small pink accent, a volume window on the handle, and a slim tapering shaft ending in a tip cone with one translucent disposable tip attached. Not a syringe, not a pen, not a stick. Exactly one pipette in the picture.',
    'DEMO-LAB-2007': (
        'A benchtop stand for six single-channel pipettes: a flat dark base plate with six light grey upright '
        'posts in a row, each with a grey cap, that hold the pipettes upright. Empty, no pipettes in it. '
        'Not a tip rack and not a shelf.'
    ),
    'DEMO-LAB-2008': 'A pipette tip rack in white: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small round open top of a white tip inside it, and a clear lid standing open at the back. Tips never stick up out of the rack. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2009': 'A pipette tip rack in mid grey: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small round open top of a grey tip inside it, and a clear lid standing open at the back. Tips never stick up out of the rack. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2010': 'A pipette tip rack in mid grey: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small round open top of a grey tip inside it, a flat top with no finger recess or notch, and a clear lid standing open at the back. Tips never stick up out of the rack. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2011': 'A filter pipette tip rack with clear tips: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small open top of a clear tip, a small white filter disc visible inside each tip top, and a clear lid standing open at the back. Tips never stick up out of the rack. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2012': 'A resealable clear plastic zip bag lying flat, filled with about a thousand small loose translucent disposable pipette tips, each tip only a few centimetres long. Not a bag of nails, not spikes.',
    'DEMO-LAB-2013': 'A sterile pipette tip rack in white: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small open top of a white tip standing in it, a thin clear sealing film over the tips, and a clear lid standing open at the back, hinged along the back edge of the box. Tips never stick up out of the rack. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2014': 'A pipette tip rack in white for 2 µl tips: a rectangular box with translucent walls and a flat top plate with exactly 96 round holes in an 8 by 12 grid (8 rows of 12, count them), each hole a dark ring with the small open top of a short white conical tip inside it, and a clear lid standing open at the back. Tips never stick up out of the rack. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2015': 'A white pipette tip box holding 96 long filter pipette tips: a rectangular box with translucent walls and a flat top plate with exactly 96 round openings in an 8 by 12 grid (8 rows, 12 columns), each opening showing a small white filter disc, the tips pointing down inside. A clear hinged lid stands open at the back. Not a bag, not 32 or 30 openings, not a dish. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-2016': 'A hand-held electronic pipette controller in white and light grey plastic: a pistol grip pointing down at the back, a body on top, two small trigger buttons on the front of the grip, a round nose cone at the front, and a straight clear glass pipette shaft fitted into the nose and pointing straight ahead, in line with the body. Not an angled pipette, no nozzle on top. No text, no numbers, no logos, no labels anywhere on the product.',
}
