"""Electrical pack, series 2: flush and surface wall devices, a power strip.

Wall devices stand upright on z=0 with their face toward -Y, so the camera
sees the front. A flush plate is 6 mm deep with its front at y=-3; a surface
box is deeper and its front sits further out. Holes and rockers are thin
parts stuck on the front. The power strip lies flat on the floor with its
cable leaving the left end, and is shot from a high camera.
"""

COL = {
    'white': '#F4F4F2', 'black': '#1E1F22', 'anthracite': '#3A3D42',
    'aluminium': '#B9BDC2', 'stainless': '#CFD3D8',
}
HOLE = '#1A1C20'
CABLE = '#2A2D33'
BODY_GREY = '#E8EAED'


def _hex(name):
    return COL.get(name, name)


def _fin(name):
    """Metal finish for the aluminium and stainless frames, matte plastic otherwise."""
    return dict(metal=0.7, rough=0.3) if name in ('aluminium', 'stainless') else dict(rough=0.4)


def plate(k, w, h, colour, y_front=-3.0, depth=6.0):
    """Wall plate w x h (x by z), standing on z=0, front face at y_front."""
    k.box((w, depth, h), (0, y_front + depth / 2, h / 2), _hex(colour), bevel=1.5, **_fin(colour))


def hole(k, x, z, r, y=-3.0):
    """Round contact hole, a dark disc on the front face."""
    k.cyl(r, 0.6, (x, y - 0.3, z), HOLE, rot=(90, 0, 0))


def rocker(k, colour, w, h, z, y=-3.0):
    """Rectangular rocker lever standing 2.5 mm proud of the front face."""
    k.box((w, 2.5, h), (0, y - 1.25, z), _hex(colour), bevel=1.2, **_fin(colour))


def earth_clip(k, x, z, y=-3.0):
    k.box((3, 1.0, 10), (x, y - 0.5, z), '#CFD3D8', metal=1.0, rough=0.25)


def socket_holes(k, cx, z, y=-3.0, colour='white'):
    """Round recessed Schuko face: a thin dark rim, the face, two round contacts side by side,
    and one earth clip at the top and one at the bottom of the recess."""
    k.cyl(25, 0.5, (cx, y - 0.25, z), HOLE, rot=(90, 0, 0))
    k.cyl(24, 0.6, (cx, y - 0.6, z), _hex(colour), rot=(90, 0, 0), **_fin(colour))
    hole(k, cx - 10, z, 4.0, y - 0.6)
    hole(k, cx + 10, z, 4.0, y - 0.6)
    for dz in (22, -22):
        k.box((9, 1.0, 3), (cx, y - 1.0, z + dz), '#CFD3D8', metal=1.0, rough=0.25)


def rocker_switch(k, colour='white', w=80, h=80, rocker_w=56, rocker_h=40):
    """Flush rocker switch: one lever on a square plate."""
    plate(k, w, h, colour)
    rocker(k, colour, rocker_w, rocker_h, h / 2)


def rocker_surface(k, colour='white'):
    """Surface rocker switch: a 26 mm deep box with a splash-proof cover on the front."""
    plate(k, 80, 80, colour, y_front=-13.0, depth=26.0)
    rocker(k, colour, 52, 34, 40, y=-13.0)


def cover_frame(k, gangs=1, colour='white', socket=False):
    """Cover frame for 1, 2 or 3 device inserts. Each opening has a thin dark gap round a flush insert.
    socket=True fills the 1-gang opening with a white Schuko socket face, so the frame visibly covers a socket."""
    w = {1: 80, 2: 146, 3: 226}[gangs]
    plate(k, w, 80, colour)
    pitch = w / gangs
    for i in range(gangs):
        x = -w / 2 + pitch * (i + 0.5)
        k.box((pitch - 8, 0.6, 68), (x, -3.3, 40), HOLE)
        if socket:
            k.box((pitch - 10, 0.6, 66), (x, -3.9, 40), _hex('white'), bevel=0.4, rough=0.4)
            socket_holes(k, x, 40, y=-4.2, colour='white')
        else:
            k.box((pitch - 10, 0.6, 66), (x, -3.9, 40), _hex(colour), bevel=0.6, **_fin(colour))


def socket_face(k, gangs=1, colour='white', usb=False):
    """Flush earthed socket. usb=True puts two USB ports above the socket."""
    w = {1: 80, 2: 146}[gangs]
    plate(k, w, 80, colour)
    pitch = w / gangs
    for i in range(gangs):
        cx = -w / 2 + pitch * (i + 0.5)
        if usb:
            socket_holes(k, cx, 30, colour=colour)
            for dx in (-11, 11):
                k.box((12, 0.6, 6), (cx + dx, -3.3, 60), HOLE)
        else:
            socket_holes(k, cx, 40, colour=colour)


def surface_socket(k, colour='white'):
    """Surface earthed socket for damp rooms: a 34 mm deep box with a rubber lip, and a clear
    cover hinged on the top edge and flipped up and open at about 45 degrees."""
    plate(k, 84, 84, colour, y_front=-17.0, depth=34.0)
    socket_holes(k, 0, 42, y=-17.0, colour=colour)
    k.box((88, 3, 10), (0, -18.5, 6), _hex(colour), bevel=1.0, **_fin(colour))
    # cover: 56 mm long, hinge at (y -17, z 84), turned -135 degrees about X so it stands up and out
    # no cover: Alex wants the socket face shown plainly (2026-10-17)


def doorbell(k, colour='white'):
    """Flush push button: one flat square key in the upper middle of a square plate, no knob."""
    plate(k, 80, 80, colour)
    rocker(k, colour, 44, 44, 40)


def dimmer(k, colour='white'):
    """Flush rotary dimmer: a large conical knob in the middle of a square plate."""
    plate(k, 80, 80, colour)
    k.cyl(24, 12, (0, -9, 40), _hex(colour), rot=(90, 0, 0), r2=21, bevel=1.5, **_fin(colour))


def blind_control(k, colour='white'):
    """Flush two-button blind control: two flat rectangular keys, up and down, stacked on a square plate."""
    plate(k, 80, 80, colour)
    for z in (58, 22):
        rocker(k, colour, 56, 28, z)


def junction_box(k, colour=BODY_GREY):
    """Surface junction box IP55, 100 x 100 mm, 52 mm deep, with a gasketed lid and cable entries."""
    k.box((100, 52, 100), (0, 0, 50), colour, bevel=5, rough=0.4)
    k.box((92, 1.5, 92), (0, -26.75, 50), '#2A2D33', rough=0.6)                    # gasket
    k.box((88, 1.5, 88), (0, -27.75, 50), colour, bevel=0.6, rough=0.4)            # lid
    for x in (-38, 38):
        for z in (12, 88):
            k.cyl(3, 1.5, (x, -29.5, z), '#9AA0A8', rot=(90, 0, 0), metal=0.6, rough=0.3)  # lid screws
    k.cyl(7, 8, (-25, 0, 104), colour, bevel=0.5)                                  # top entries
    k.cyl(7, 8, (25, 0, 104), colour, bevel=0.5)
    for x in (-54, 54):
        k.cyl(7, 8, (x, 0, 30), colour, rot=(0, 90, 0), bevel=0.5)                  # side entries


def power_strip(k, colour='white'):
    """Power strip lying on the floor: four earthed outlets on top, a rocker switch
    at one end, and a cable with a plug leaving the other end."""
    c = _hex(colour)
    k.box((230, 52, 30), (0, 0, 15), c, bevel=4, rough=0.4)
    for x in (-86, -29, 29, 86):
        for dx in (-7, 7):
            k.cyl(3.6, 0.6, (x + dx, 0, 30.3), HOLE)
    k.box((16, 10, 3), (104, 0, 31.5), c, bevel=1.0, rough=0.4)                    # rocker switch
    k.cyl(4.5, 110, (-170, 0, 4.5), CABLE, rot=(0, 90, 0), bevel=0.5, rough=0.5)   # cable, the visible part
    k.box((34, 26, 22), (-235, 0, 11), CABLE, bevel=3, rough=0.5)                  # plug


SKUS = {
    'DEMO-ELE-2001': (rocker_switch, {'colour': 'white'}),
    'DEMO-ELE-2002': (cover_frame, {'gangs': 2, 'colour': 'white'}),
    'DEMO-ELE-2003': (socket_face, {'colour': 'white'}),
    **{f'DEMO-ELE-2003-{c.upper()}': (socket_face, {'colour': c}) for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-2004': (junction_box, {}),
    'DEMO-ELE-2005': (rocker_switch, {'colour': 'white'}),
    'DEMO-ELE-2006': (rocker_switch, {'colour': 'white'}),
    'DEMO-ELE-2007': (doorbell, {'colour': 'white'}),
    'DEMO-ELE-2008': (rocker_switch, {'colour': 'white', 'rocker_w': 64, 'rocker_h': 44}),
    'DEMO-ELE-2009': (cover_frame, {'gangs': 1, 'colour': 'white', 'socket': True}),
    **{f'DEMO-ELE-2009-{c.upper()}': (cover_frame, {'gangs': 1, 'colour': c, 'socket': True})
       for c in ('white', 'black', 'anthracite', 'aluminium', 'stainless')},
    'DEMO-ELE-2010': (cover_frame, {'gangs': 3, 'colour': 'white'}),
    'DEMO-ELE-2011': (surface_socket, {'colour': 'white'}),
    **{f'DEMO-ELE-2011-{c.upper()}': (surface_socket, {'colour': c}) for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-2012': (socket_face, {'gangs': 2, 'colour': 'white'}),
    **{f'DEMO-ELE-2012-{c.upper()}': (socket_face, {'gangs': 2, 'colour': c}) for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-2013': (socket_face, {'colour': 'white', 'usb': True}),
    **{f'DEMO-ELE-2013-{c.upper()}': (socket_face, {'colour': c, 'usb': True}) for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-2014': (power_strip, {'colour': 'white'}, {'pitch': 50}),
    **{f'DEMO-ELE-2014-{c.upper()}': (power_strip, {'colour': c}, {'pitch': 50}) for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-2015': (dimmer, {'colour': 'white'}),
    'DEMO-ELE-2017': (rocker_surface, {'colour': 'white'}),
    'DEMO-ELE-2018': (blind_control, {'colour': 'white'}),
}

# Shared wording for the colour variants of one product.
_SOCKET = ('An earthed socket outlet for flush mounting, in one uniform {c} colour all over: the square face, the round '
           'recessed socket and the rim are all {c}, with no white or other colour anywhere. Two round contact holes side by side, '
           'and an earth clip at the top and one at the bottom of the recess. Not a switch; not a USB socket.')
_FRAME = ('A cover frame in {c} for one device insert: a flat square 80 mm frame in {c} with a square opening in the middle, '
          'and a white Schuko socket insert filling the opening, with two round holes and an earth clip at the top and bottom. '
          'Only the frame is {c}; the insert is white. Not a blank plate; not a switch.')
_SURFACE = ('A surface-mounted earthed socket outlet with splash protection, in {c}: a box about 84 mm square that stands '
            '34 mm off the wall, with a rubber lip along the bottom, a clear colourless transparent cover hinged on the top edge '
            'and flipped up and open, and a round socket face with two round contact holes side by side and an earth clip at the '
            'top and bottom of the recess. Not a flush socket.')
_DOUBLE = ('A double socket outlet for flush mounting in {c}: a plate about 146 by 80 mm with two round recessed socket faces '
           'side by side, each with exactly two round contact holes side by side and an earth clip at the top and one at the bottom. '
           'No third hole, no earth pin, no slot. Not a single socket.')
_USB = ('A flush socket outlet with two USB charging ports in {c}: a square 80 mm face with an earthed socket '
        '(two round holes side by side, an earth clip at the top and one at the bottom) in the lower half and two small '
        'rectangular USB ports in the upper half. No third hole, no earth pin. Not a plain socket.')
_STRIP = ('A power strip lying flat on the floor in {c} plastic, about 230 by 52 mm and 30 mm high, with four '
          'earthed socket outlets on top, a small rocker switch at one end and a short dark grey cable with a '
          'plug leaving the other end. Not a wall socket.')

HINTS = {
    'DEMO-ELE-2001': ('A flush-mounted single-pole light switch: a square white plate about 80 mm with one '
                      'large rectangular rocker in the middle, flat to the wall. Not a socket; no holes.'),
    'DEMO-ELE-2002': ('A flush cover frame for two device inserts in white: a rectangular plate about 146 by '
                      '80 mm with two flush square inserts side by side. Not a socket and not a switch; no holes or rockers.'),
    'DEMO-ELE-2003': 'A flush-mounted earthed socket outlet in pure white plastic, seen from the front left, upright as on a wall: a square cover frame around a European Schuko socket: one round recessed socket face with exactly two round pin holes side by side and two small metal earthing clips at the top and bottom edge of the recess. No third hole, no earth pin, no slots. Not a French, Swiss, British or American socket.',
    'DEMO-ELE-2003-WHITE': _SOCKET.format(c='white'),
    'DEMO-ELE-2003-BLACK': _SOCKET.format(c='black'),
    'DEMO-ELE-2003-ANTHRACITE': _SOCKET.format(c='anthracite (dark grey)'),
    'DEMO-ELE-2004': ('A surface-mounted junction box in light grey plastic, about 100 by 100 mm and 52 mm deep, '
                      'with a flat lid, a thin dark gasket round the lid edge, four lid screws and round cable '
                      'entries on the top and sides. It stands on its base like a box on the wall. Not a socket or a switch.'),
    'DEMO-ELE-2005': ('A flush-mounted two-way light switch in white: a square white plate about 80 mm with one '
                      'rectangular rocker in the middle, flat to the wall. Looks like a single switch; no socket holes.'),
    'DEMO-ELE-2006': ('A flush-mounted intermediate light switch in white: a square white plate about 80 mm with one '
                      'rectangular rocker in the middle, flat to the wall. Looks like a single switch; no socket holes.'),
    'DEMO-ELE-2007': 'A flush-mounted doorbell push button in white: a square white 80 mm plate with one flat square push key in the upper middle, the key about 44 mm square and only a few millimetres proud of the plate. Not a rotary knob, no dial, no socket holes, not a rocker switch. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-2008': ('A flush-mounted double-pole light switch in white: a square white plate about 80 mm with one '
                      'wide rectangular rocker that spans most of the face. Not a socket.'),
    'DEMO-ELE-2009': 'A 1-gang cover frame for flush-mounted sockets in pure white plastic: a flat square frame about 8 cm with a square opening in the middle, and a white Schuko socket insert (two round holes, an earth clip at the top and one at the bottom) sitting in the opening, so the frame visibly covers a socket. Not a blank plate; not a switch.',
    'DEMO-ELE-2009-WHITE': _FRAME.format(c='white'),
    'DEMO-ELE-2009-BLACK': _FRAME.format(c='black'),
    'DEMO-ELE-2009-ANTHRACITE': _FRAME.format(c='anthracite (dark grey)'),
    'DEMO-ELE-2009-ALUMINIUM': _FRAME.format(c='brushed aluminium (silver-grey metal)'),
    'DEMO-ELE-2009-STAINLESS': _FRAME.format(c='polished stainless steel (bright silver metal)'),
    'DEMO-ELE-2010': ('A cover frame for three device inserts in white: a rectangular plate about 226 by 80 mm '
                      'with three flush square inserts side by side. Not a two-gang frame; no holes.'),
    'DEMO-ELE-2011': 'A surface-mounted splash-proof IP44 Schuko socket outlet in white plastic: a box about 84 mm square standing slightly off the wall, its front showing one round recessed socket face with exactly two round pin holes side by side at the same height and two small metal earthing clips at the top and bottom of the recess. No lid, no cover, no flap, no cap. Not a French, Swiss, British or American socket.',
    'DEMO-ELE-2011-WHITE': _SURFACE.format(c='white'),
    'DEMO-ELE-2011-BLACK': _SURFACE.format(c='black'),
    'DEMO-ELE-2011-ANTHRACITE': _SURFACE.format(c='anthracite (dark grey)'),
    'DEMO-ELE-2012': _DOUBLE.format(c='white') + ' The base colour is white.',
    'DEMO-ELE-2012-WHITE': _DOUBLE.format(c='white'),
    'DEMO-ELE-2012-BLACK': _DOUBLE.format(c='black'),
    'DEMO-ELE-2012-ANTHRACITE': _DOUBLE.format(c='anthracite (dark grey)'),
    'DEMO-ELE-2013': 'A flush-mounted Schuko socket outlet in white plastic with a square frame: at the top two small rectangular USB-A ports side by side; below them one round recessed socket face with exactly two round pin holes side by side at the same height and two small metal earthing clips at its top and bottom edge. Nothing else: no third hole, no earth pin, no slot. German socket, not British or American.',
    'DEMO-ELE-2013-WHITE': _USB.format(c='white'),
    'DEMO-ELE-2013-BLACK': _USB.format(c='black'),
    'DEMO-ELE-2013-ANTHRACITE': _USB.format(c='anthracite (dark grey)'),
    'DEMO-ELE-2014': _STRIP.format(c='white') + ' The base colour is white.',
    'DEMO-ELE-2014-WHITE': _STRIP.format(c='white'),
    'DEMO-ELE-2014-BLACK': _STRIP.format(c='black'),
    'DEMO-ELE-2014-ANTHRACITE': _STRIP.format(c='anthracite (dark grey)'),
    'DEMO-ELE-2015': ('A flush-mounted rotary dimmer in white: a square white 80 mm plate with a large round '
                      'conical knob in the middle, standing about 12 mm proud. Not a push button; not a rocker switch.'),
    'DEMO-ELE-2017': ('A surface-mounted light switch with splash protection for damp rooms, in white: a box about '
                      '80 mm square that stands 26 mm off the wall, with one rectangular rocker on its front. '
                      'It sits proud of the wall, unlike a flush switch.'),
    'DEMO-ELE-2018': 'A flush-mounted two-button blind control in white: a square white 80 mm plate with two flat rectangular push keys stacked one above the other, one for up and one for down, each about 56 by 28 mm and only a few millimetres proud of the plate. Not round knobs, no dials, no rotary parts, not a rocker switch, no socket holes. No text, no numbers, no logos, no labels anywhere on the product.',
}
