"""Lab pack, series 5: personal protection and spill kit. Safety glasses, goggles,
over-spectacle goggles, lab coats (sizes 50 and 54), cut-resistant and heat-resistant
gloves, a vinyl glove box, a polyethylene apron pack, a face shield, a spill tray,
a broken-glass container, a pack of hair covers.

Glove pairs are laid flat, side by side. Clear plastics are alpha 0.4 to 0.6. Lab
coats are white with a grey pocket and buttons. No lettering. Units mm, product
stands on z=0, front faces -Y.
"""

GLASS = 'glass'
WHITE = '#F7F7F5'
FRAME = '#2F343C'
CUFF_DARK = '#2F343C'


def safety_glasses(k):
    """Safety glasses: two clear lenses in dark frames, a bridge, side shields and temples."""
    for x in (-30, 30):
        k.box((56, 3, 40), (x, 0, 24), FRAME, bevel=2)                                  # lens frame
        k.box((48, 1.5, 32), (x, -2.2, 24), GLASS, alpha=0.4, rough=0.1)                 # clear lens
        k.box((4, 30, 40), (54 if x > 0 else -54, -8, 24), GLASS, alpha=0.4, rough=0.1)  # side shield
    k.box((20, 3, 6), (0, 0, 36), FRAME, bevel=1)                                        # bridge
    for x in (-58, 58):
        k.box((3, 110, 4), (x, 55, 2), FRAME, bevel=1)                                    # temple


def goggles(k):
    """Indirectly vented goggles: a soft dark seal around one wide clear lens, a strap."""
    k.box((130, 12, 56), (0, 6, 30), FRAME, bevel=12)                                    # frame body
    k.box((116, 3, 40), (0, -3, 30), GLASS, alpha=0.45, rough=0.1, bevel=3)              # clear lens
    for x in (-30, -10, 10, 30):
        k.cyl(2.5, 1.6, (x, -4.6, 52), '#1A1C20', rot=(90, 0, 0))                        # vent openings
    for x in (-68, 68):
        k.box((8, 30, 8), (x, 4, 30), '#4A515C', bevel=2)                                # strap ends


def _lab_coat_outline(s):
    """SVG front-view outline of the coat, mapped flat on the floor (collar at the back)."""
    pts = [(150, 130), (200, 168), (250, 130), (290, 160), (302, 290), (290, 300),
           (280, 300), (272, 214), (270, 326), (130, 326), (128, 214), (120, 300),
           (110, 300), (98, 290), (110, 160)]
    return [((x - 200) * 3.0 * s, (200 - y) * 4.4 * s) for x, y in pts]


def lab_coat(k, s=1.0):
    """White lab coat laid flat, sleeves spread out, V-neck, snap buttons, chest pocket."""
    k.slab(_lab_coat_outline(s), 26, 0, WHITE, round_=8, smooth=1)
    for y in (-60, -150, -240, -330):
        k.cyl(5, 2, (0, y * s, 28), 'mid')                                               # snap buttons
    k.box((90, 4, 4), (100 * s, -250 * s, 28), 'light', bevel=1)                         # chest pocket


def _hand(k, dx, s, fill, cuff, dy=0.0, **mk):
    """One glove laid flat: palm, four fingers, thumb, optional cuff. s=-1 mirrors it."""
    def P(pts):
        return [(dx + s * x, dy + y) for x, y in pts]
    outline = [(-46, -80), (-46, 20), (-46, 66), (-35, 74), (-24, 66), (-24, 30),
               (-22, 30), (-22, 80), (-12, 90), (-2, 80), (-2, 30), (0, 30), (0, 76),
               (10, 86), (20, 76), (20, 30), (22, 30), (22, 62), (32, 70), (42, 62),
               (42, 20), (70, 22), (84, 36), (78, 48), (60, 36), (46, 26), (46, -80)]
    k.slab(P(outline), 12, 0, fill, round_=3, smooth=1, **mk)
    if cuff:
        k.slab(P([(-50, -150), (50, -150), (50, -78), (-50, -78)]), 16, 0, cuff,
               round_=4, smooth=0, **mk)


def gloves(k, fill, cuff):
    """A pair of gloves laid flat side by side (the right one mirrored)."""
    _hand(k, -72, 1, fill, cuff)
    _hand(k, 72, -1, fill, cuff)


def apron_pack(k):
    """Pack of 100 polyethylene aprons: a translucent folded block, one apron laid on top."""
    k.box((300, 220, 40), (0, 0, 20), '#D8E6F2', bevel=4, alpha=0.6, rough=0.2)           # folded stack
    pts = [(-125, 110), (125, 110), (138, -110), (-138, -110)]
    k.slab(pts, 3, 40, '#EAF3F8', round_=1, smooth=1, alpha=0.6, rough=0.2)             # apron on top


def face_shield(k):
    """Face shield: a clear visor held inside a black headband hoop, standing upright."""
    k.torus(95, 5, (0, 0, 100), FRAME, rot=(90, 0, 0), metal=0.4, rough=0.4)            # headband hoop
    k.box((176, 1.5, 150), (0, -2, 100), GLASS, alpha=0.35, rough=0.1)                   # visor
    k.box((180, 8, 10), (0, 0, 172), FRAME, bevel=2)                                     # top bar


def spill_tray(k, L=600, W=400, H=40, wall=25):
    """Polypropylene spill tray: a shallow grey tray with a raised rim and a dark base."""
    grey = '#C9CED6'
    k.box((L, W, 12), (0, 0, 6), grey, bevel=2)
    k.box((L, wall, H), (0, W / 2 - wall / 2, H / 2), grey, bevel=4)
    k.box((L, wall, H), (0, -(W / 2 - wall / 2), H / 2), grey, bevel=4)
    k.box((wall, W, H), (L / 2 - wall / 2, 0, H / 2), grey, bevel=4)
    k.box((wall, W, H), (-(L / 2 - wall / 2), 0, H / 2), grey, bevel=4)
    k.box((L - 2 * wall, W - 2 * wall, 1), (0, 0, 12.5), FRAME)                          # dark inner base


def broken_glass(k):
    """Broken-glass container: an upright off-white square body with a dark lid and a slot."""
    k.box((230, 230, 190), (0, 0, 95), '#D9DDE2', bevel=10)                              # body
    k.box((240, 240, 22), (0, 0, 201), FRAME, bevel=6)                                   # lid
    k.box((120, 18, 4), (0, 0, 212.5), 'mid', bevel=1)                                   # lid slot


def hair_covers(k):
    """Three disposable bouffant caps stacked: light blue non-woven domes, each with an elastic band round its open edge."""
    blue = '#BFD9EE'
    for i in range(3):
        z = 21 + i * 17
        k.sphere(60, (0, 0, z), blue, scale=(1, 1, 0.35), rough=0.7)                     # cap crown
        k.torus(60, 2.5, (0, 0, z), 'mid', rough=0.5)                                    # elastic band at the edge


def vinyl_box(k):
    """Box of 100 vinyl gloves: a white carton with an opening, one clear glove in front."""
    k.box((240, 150, 120), (0, 0, 60), WHITE, bevel=3)                                   # carton
    k.box((150, 80, 2), (0, 0, 121), FRAME)                                               # dispenser opening
    _hand(k, 0, 1, '#D6E4EE', None, dy=-190, alpha=0.5, rough=0.2)                       # loose glove


def over_goggles(k):
    """Over-spectacle goggles: a dark frame with a clear lens, rims of spectacles, side shields."""
    k.box((230, 10, 92), (0, 6, 46), FRAME, bevel=12)                                    # frame body
    k.box((200, 2, 66), (0, -4, 46), GLASS, alpha=0.45, rough=0.1)                       # clear lens
    for x in (-60, 60):
        k.torus(36, 2.5, (x, -8, 46), '#7B838F', rot=(90, 0, 0))                         # spectacle rim
    for x in (-112, 112):
        k.box((6, 40, 86), (x, -6, 46), GLASS, alpha=0.4, rough=0.1)                     # side shield


SKUS = {
    'DEMO-LAB-5001': (safety_glasses, {}),
    'DEMO-LAB-5002': (goggles, {}),
    'DEMO-LAB-5003': (lab_coat, {'s': 1.0}, {'pitch': 50}),
    'DEMO-LAB-5004': (gloves, {'fill': '#7B838F', 'cuff': CUFF_DARK}, {'pitch': 50}),
    'DEMO-LAB-5005': (gloves, {'fill': '#C9CED6', 'cuff': CUFF_DARK}, {'pitch': 50}),
    'DEMO-LAB-5006': (apron_pack, {}, {'pitch': 50}),
    'DEMO-LAB-5007': (face_shield, {}),
    'DEMO-LAB-5008': (spill_tray, {}, {'pitch': 40}),
    'DEMO-LAB-5009': (broken_glass, {}),
    'DEMO-LAB-5010': (gloves, {'fill': '#B9733B', 'cuff': '#8A4B1E'}, {'pitch': 50}),
    'DEMO-LAB-5011': (lab_coat, {'s': 1.06}, {'pitch': 50}),
    'DEMO-LAB-5012': (hair_covers, {}, {'pitch': 30}),
    'DEMO-LAB-5013': (vinyl_box, {}, {'pitch': 40}),
    'DEMO-LAB-5014': (over_goggles, {}),
}

HINTS = {
    'DEMO-LAB-5001': 'One pair of safety glasses with a clear lens, a dark frame, side shields at both sides and thin temples, lying with the lenses facing the camera. Not goggles: there is no elastic strap and no seal around the eyes.',
    'DEMO-LAB-5002': 'One pair of indirectly vented laboratory goggles: a soft dark frame around one wide clear lens, a row of small vent openings along the top edge and a short dark strap at each end. Not spectacles: the frame is a closed seal around the eyes.',
    'DEMO-LAB-5003': 'A white knee-length lab coat laid flat, long sleeves spread out to the sides, a V-neck collar, a front with four snap buttons down the centre, one grey chest pocket on the left and a straight hem. Blended fabric, no logo, no emblem. Not a jacket and not a dress.',
    'DEMO-LAB-5004': 'A pair of cut-resistant knit gloves in mid grey, laid flat side by side with fingers and thumbs spread out and a short dark cuff at each wrist. No logo, no emblem. Not mittens: each glove has five separate fingers. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves. The two gloves lie clearly apart with white space between them, never overlapping or stacked, each one fully visible from cuff to fingertips.',
    'DEMO-LAB-5005': 'A pair of cut-resistant knit gloves in light grey, laid flat side by side with fingers and thumbs spread out and a short dark cuff at each wrist. No logo, no emblem. Not mittens: each glove has five separate fingers. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-LAB-5006': 'A translucent pale blue block of about 100 folded thin polyethylene aprons, with one loose clear apron laid flat on top: a thin sheet with a straight top edge and a slightly wider rounded bottom. No ties visible, no logo. Not a fabric apron.',
    'DEMO-LAB-5007': 'One face shield standing upright: a wide clear polycarbonate visor held inside a black headband hoop, with a short dark bar across the top of the visor. No logo, no emblem. Not a helmet and not a face mask.',
    'DEMO-LAB-5008': 'One grey polypropylene spill tray lying flat, a rectangle about 60 by 40 cm, shallow, with a raised rim all around and a dark inner base. No lettering, no lid. Not a box with a lid.',
    'DEMO-LAB-5009': 'One square off-white polypropylene container of about 10 litres, standing upright, with a dark lid and a narrow slot in the middle of the lid for broken glass. No lettering, no foot pedal. Not a bin with a pedal.',
    'DEMO-LAB-5010': 'A pair of heat-resistant gloves in tan-orange aramid, laid flat side by side, with five fingers, a thumb and a thick darker cuff at each wrist. No logo, no emblem. Not oven mitts: each glove has separate fingers. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves. The two gloves lie clearly apart with white space between them, never overlapping or stacked, each one fully visible from cuff to fingertips.',
    'DEMO-LAB-5011': 'A white knee-length lab coat laid flat, long sleeves spread out to the sides, a V-neck collar, a front with four snap buttons down the centre, one grey chest pocket on the left and a straight hem. Slightly larger than a standard coat. Blended fabric, no logo, no emblem. Not a jacket and not a dress.',
    'DEMO-LAB-5012': 'A small stack of three disposable light-blue non-woven bouffant caps lying one on another, each a pleated dome crown with a thin elastic band round its open edge. No stitched seams, no fabric folds, no ties, no pouch. Not a shower cap with print, not a cloth. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-5013': 'A white cardboard dispenser box with an oval opening on top, with one clear disposable vinyl glove pulled halfway out and draped over the box, soft shadow so the clear glove stands out from the white background. No print on the box. Every glove has exactly five separate fingers: one thumb and four fingers, anatomically correct, lying flat with the fingers slightly spread so all five are clearly visible and countable. No mittens, no extra or missing fingers. No labels or printing on the gloves.',
    'DEMO-LAB-5014': 'One pair of over-spectacle goggles standing upright: a dark frame with a clear lens, a larger closed frame than ordinary goggles, with side shields at both sides. No logo. Not ordinary goggles: the frame sits over spectacles.',
}
