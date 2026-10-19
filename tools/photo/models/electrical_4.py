"""Electrical pack, series 4: distribution and installation equipment.

Units mm. Everything stands on z=0 with its front toward -Y. The DIN-rail devices
(circuit breakers, residual current devices, the surge protector and the main
switch) stand as they sit on a rail: 18 mm per module, 88 mm high, front face
toward the camera. The distribution boards stand on their base. Colours are light
and mid greys with white doors; no lettering on the models.
"""

HOUSING = '#EEEEEA'   # the usual near-white of modular devices
DOOR = '#F4F4F2'
LEVER = '#5A616B'
TERMINAL = '#9AA1AB'
DARK = '#2B2E33'
BUTTON = '#3A3D42'
GLASS = '#DCE8EE'
INDICATOR = '#3DB36B'
HANDLE = '#8A929D'
LABEL = '#F4F4F2'

MODULE = 18  # mm per DIN-rail module


def _housing(k, w, poles):
    """A modular DIN-rail housing in its real profile: the rear body 90 mm tall with a shoulder at
    top and bottom (terminal screws on the shoulders), the narrow front nose 45 mm tall in the
    middle, standing upright as on a rail, front toward -Y. One body per 18 mm module."""
    for i in range(poles):
        x = -w / 2 + MODULE / 2 + MODULE * i
        k.box((MODULE - 0.6, 52, 90), (x, -26, 45), HOUSING, bevel=1.2, rough=0.4)          # rear body with shoulders
        k.box((MODULE - 0.6, 18, 45), (x, -61, 45), HOUSING, bevel=1.5, rough=0.4)          # front nose
        for z in (11, 79):
            k.cyl(3.6, 1.5, (x, -52.6, z), DARK, rot=(90, 0, 0))                            # screw well on the shoulder
            k.cyl(2.6, 1.6, (x, -52.9, z), TERMINAL, rot=(90, 0, 0), metal=0.8, rough=0.3)  # screw head
            k.box((MODULE - 7, 10, 1.2), (x, -40, 90.4 if z > 45 else -0.2), DARK)         # wire entry
    for i in range(1, poles):
        x = -w / 2 + MODULE * i
        k.box((0.6, 52.4, 89), (x, -26.2, 45), DARK, rough=0.5)                           # joint between modules
        k.box((0.6, 18.4, 44), (x, -61, 45), DARK, rough=0.5)                             # ...and through the nose
    k.box((min(w, 30) * 0.5, 4, 3), (0, -2, 1.5), TERMINAL, metal=0.6, rough=0.35)       # rail clip at the back


def _toggle(k, x, width):
    """Toggle lever standing out of the nose, in the upper half (switched on)."""
    k.box((width, 3, 16), (x, -70.5, 52), DARK, rough=0.5)                                # slot in the nose
    k.box((width - 2, 9, 9), (x, -74, 55), LEVER, bevel=1.5, rough=0.35)                  # lever


def mcb(k, poles=1):
    """Miniature circuit breaker, 18 mm per pole: the real modular profile, one toggle across the poles."""
    w = MODULE * poles
    _housing(k, w, poles)
    _toggle(k, 0, w - 5)
    k.box((w - 6, 0.6, 9), (0, -70.3, 33), LABEL, rough=0.3)                             # blank label field


def rcd(k, poles=2, breaker=False):
    """Residual current device (breaker=True: RCBO, 1 pole + N in two modules): the real modular
    profile, a toggle on the nose and a small round test button beside it."""
    w = MODULE * poles
    _housing(k, w, poles)
    if breaker:
        _toggle(k, -MODULE / 2, MODULE - 5)
        k.cyl(3.2, 3, (MODULE / 2, -71.5, 55), BUTTON, rot=(90, 0, 0), bevel=0.8)        # test button
    else:
        _toggle(k, -MODULE / 2 if poles > 2 else 0, MODULE * (poles - 1) - 5)
        k.cyl(3.2, 3, (w / 2 - MODULE / 2 if poles > 2 else w / 2 - 5, -71.5, 34), BUTTON, rot=(90, 0, 0), bevel=0.8)  # test button
    k.box((w - 6, 0.6, 7), (0, -70.3, 30 if breaker else 26), LABEL, rough=0.3)


def surge(k):
    """Surge protective device, two modules: the real profile, two plug-in protection inserts in the
    nose, each with a small status window showing green."""
    _housing(k, 36, 2)
    for x in (-9, 9):
        k.box((MODULE - 2.5, 4, 43), (x, -71, 45), HOUSING, bevel=1, rough=0.4)          # plug-in insert
        k.box((8, 0.8, 5), (x, -73.2, 58), INDICATOR, rough=0.3)                          # status window


def main_switch(k):
    """Three-pole main load-break switch: the real modular profile with one wide handle on the nose."""
    w = MODULE * 3
    _housing(k, w, 3)
    k.box((w - 4, 3, 20), (0, -70.5, 50), DARK, rough=0.5)
    k.box((w - 10, 14, 12), (0, -76, 54), DARK, bevel=2, rough=0.35)                    # wide handle


def surface_board(k, w=260, h=320, d=115):
    """Surface-mounted distribution board standing on its base: a light grey plastic box, a white door and a grip on the door."""
    k.box((w, d, h), (0, -d / 2, h / 2), HOUSING, bevel=5, rough=0.4)
    k.box((w - 16, 4, h - 16), (0, -d - 2, h / 2), DOOR, bevel=2, rough=0.3)
    k.box((6, 4, 46), (w / 2 - 26, -d - 6, h / 2), HANDLE, bevel=1.5, rough=0.35)


def flush_board(k, w=360, h=440):
    """Flush-mounted distribution board standing on its base: a light grey frame that sits flush with the wall, a white door inside it."""
    k.box((w, 16, h), (0, -8, h / 2), HOUSING, bevel=4, rough=0.4)
    k.box((w - 40, 4, h - 40), (0, -18, h / 2), DOOR, bevel=2, rough=0.3)
    k.box((6, 4, 50), (w / 2 - 40, -21, h / 2), HANDLE, bevel=1.5, rough=0.35)


SKUS = {
    'DEMO-ELE-4001': (mcb, {'poles': 1}),
    'DEMO-ELE-4002': (mcb, {'poles': 1}),
    'DEMO-ELE-4003': (mcb, {'poles': 1}),
    'DEMO-ELE-4004': (mcb, {'poles': 3}),
    'DEMO-ELE-4005': (mcb, {'poles': 3}),
    'DEMO-ELE-4006': (rcd, {'poles': 2}),
    'DEMO-ELE-4007': (rcd, {'poles': 4}),
    'DEMO-ELE-4008': (rcd, {'poles': 4}),
    'DEMO-ELE-4009': (rcd, {'poles': 2, 'breaker': True}),
    'DEMO-ELE-4010': (surge, {}),
    'DEMO-ELE-4011': (surface_board, {'w': 260, 'h': 320, 'd': 115}),
    'DEMO-ELE-4012': (surface_board, {'w': 340, 'h': 430, 'd': 125}),
    'DEMO-ELE-4013': (flush_board, {'w': 360, 'h': 440}),
    'DEMO-ELE-4014': (main_switch, {}),
}

HINTS = {
    'DEMO-ELE-4001': 'A 1-pole miniature circuit breaker, 18 mm wide: one modular DIN-rail device standing upright, front toward the camera. Slim white housing with a stepped profile, one grey toggle lever on the front nose, exactly one terminal screw on the top shoulder and one on the bottom shoulder. It is a single module, not a multi-pole device. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-4002': 'A 1-pole miniature circuit breaker, 18 mm wide: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box, not a light switch.',
    'DEMO-ELE-4003': 'A 1-pole miniature circuit breaker, 18 mm wide: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box, not a light switch.',
    'DEMO-ELE-4004': 'A 3-pole miniature circuit breaker, 54 mm wide (three 18 mm modules joined), one wide toggle lever across all three: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box.',
    'DEMO-ELE-4005': 'A 3-pole miniature circuit breaker, 54 mm wide (three 18 mm modules joined), one wide toggle lever across all three: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box.',
    'DEMO-ELE-4006': 'A 2-pole residual current device, 36 mm wide, with a small round test button beside the toggle lever: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box.',
    'DEMO-ELE-4007': 'A 4-pole residual current device, four modules wide (72 mm): one long slim DIN-rail device standing upright, front toward the camera. Slim white housing with a stepped profile, one grey toggle lever across the top of the front nose, a small round test button beside the lever, and four terminal pairs, one screw on the top and one on the bottom of each module. It is long and flat, not a cube, and has no rotary handle. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-4008': 'A 4-pole main residual current device, four modules wide (72 mm): one long slim DIN-rail device standing upright, front toward the camera. Slim white housing with a stepped profile, one grey toggle lever across the top of the front nose, a small round test button beside the lever, and four terminal pairs, one screw on the top and one on the bottom of each module. It is long and flat, not a cube, and has no rotary handle. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-4009': 'A combined RCD and circuit breaker (RCBO), 36 mm wide, with a toggle lever and a small round test button: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box.',
    'DEMO-ELE-4010': 'A surge protective device, two modules (36 mm) wide: one DIN-rail module standing upright, front toward the camera. Slim white housing with a stepped profile, two plug-in grey protection inserts side by side on the front nose, each with a small green status window. No toggle lever and no switch of any kind. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-4011': 'A surface-mounted plastic distribution board, 26 by 32 cm, standing on its base: a light grey box with a white door on the front, a small grey grip on the right edge of the door, and a shallow depth. The whole board visible, standing out clearly from the white background with a soft shadow. Not a fuse box made of metal, not a wall socket, not a cabinet with glass doors.',
    'DEMO-ELE-4012': 'A large surface-mounted plastic distribution board, 34 by 43 cm, standing on its base: a light grey box with a white door on the front, a small grey grip on the right edge of the door, and a slightly deeper body than a small board. The whole board visible, standing out clearly from the white background with a soft shadow. Not a metal cabinet, not a server rack, not a wall socket.',
    'DEMO-ELE-4013': 'A flush-mounted distribution board, 36 by 44 cm, standing on its base: a light grey frame that sits flush with a wall, with a white door set inside the frame and a small grey grip on the right side of the door. The whole board visible, standing out clearly from the white background with a soft shadow. Not a surface box, not a picture frame, not a mirror.',
    'DEMO-ELE-4014': 'A 3-pole main load-break switch, 54 mm wide, with one large dark grey rotary-style or wide toggle handle on the front: a modular DIN-rail device standing upright, seen from the front left: a slim white plastic housing 90 mm tall with the typical stepped profile of modular DIN-rail devices: a raised front nose 45 mm tall in the middle, shoulders above and below it carrying the terminal screws, a dark grey toggle lever in the middle of the front face, screw terminals at top and bottom, a metal rail clip at the back bottom. No printed text, no logo. Not a box, not a light switch.',
}
