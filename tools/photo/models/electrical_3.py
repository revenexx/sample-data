"""Electrical pack, series 3: LED ceiling panels and tubes, sensors, luminaires, lamps, a strip reel.

Units mm. Standing products (sensors on walls, luminaires, lamps, the emergency light)
stand on z=0 with their front toward -Y. Flat products (panels, tubes, the downlight,
the ceiling disc and the reel) lie on the floor and are shot from a high camera.
"""
import math

WHITE = '#F4F4F2'
FRAME = '#DCE0E4'
DIFFUSER = '#FBFBF9'
GLASS = '#F1F2F0'
CAP = '#D8DADD'
LENS = '#D5DCE2'
DARK = '#2B2E33'
BLACK = '#1E1F22'
ANTH = '#3A3D42'
ALU = '#B9BDC2'
REEL = '#D0D4D8'
STRIP = '#E6DFC8'

BODY = {'white': WHITE, 'black': BLACK, 'anthracite': ANTH}


def ceiling_panel(k, w=600, d=600, yaw=0):
    """Flat LED ceiling panel lying face up at angle yaw: a light grey frame round a bright white diffuser."""
    k.box((w, d, 12), (0, 0, 6), FRAME, bevel=2, rot=(0, 0, yaw), rough=0.35)
    k.box((w - 24, d - 24, 1.5), (0, 0, 12.6), DIFFUSER, bevel=0.5, rot=(0, 0, yaw), rough=0.2)


def tube(k, length, yaw=0):
    """T8 LED tube lying on the floor at angle yaw: a milky glass body with a white cap at each end."""
    d = math.radians(yaw)
    ux, uy = math.cos(d), math.sin(d)
    k.cyl(13, length, (0, 0, 13), GLASS, rot=(0, 90, yaw), rough=0.25)
    for s in (-1, 1):
        k.cyl(13.6, 14, (s * (length / 2 - 7) * ux, s * (length / 2 - 7) * uy, 13), CAP,
              rot=(0, 90, yaw), rough=0.5)
        for p in (-6.5, 6.5):                                   # G13 bi-pin base: two pins per end
            ax = s * (length / 2 + 4)
            k.cyl(1.6, 12, (ax * ux - p * uy, ax * uy + p * ux, 13), '#C9CDD2',
                  rot=(0, 90, yaw), rough=0.3, metal=1.0)


def motion_wall(k):
    """Surface-mounted motion sensor: a white box with a grey Fresnel lens band on the front."""
    k.box((64, 40, 64), (0, -20, 32), WHITE, bevel=4, rough=0.4)
    k.box((52, 2, 40), (0, -41, 34), LENS, bevel=1, rough=0.2)
    for i in range(6):                                          # Fresnel facet ridges on the lens
        k.box((52, 1.6, 2.2), (0, -42.5, 16 + 6 * i), LENS, bevel=0.4, rough=0.2)


def downlight(k, colour='white'):
    """Recessed downlight lying face up: a round trim with a dark ring round the lens."""
    k.cyl(50, 6, (0, 0, 3), BODY[colour], bevel=1.5, rough=0.35)
    k.cyl(42, 1.2, (0, 0, 6.6), DARK, rough=0.3)
    k.cyl(38, 1.5, (0, 0, 7.5), GLASS, rough=0.2)


def wall_luminaire(k, colour='white', w=240, h=70, d=40):
    """Wall luminaire standing upright: a box with a white diffuser strip on its front."""
    k.box((w, d, h), (0, -d / 2, h / 2), BODY[colour], bevel=6, rough=0.4)
    k.box((w - 30, 3, h - 24), (0, -d - 1.5, h / 2), DIFFUSER, bevel=1.5, rough=0.2)


def pendant(k):
    """Round pendant shade standing on its wide rim, with a small canopy on top."""
    k.cyl(200, 110, (0, 0, 55), WHITE, r2=120, bevel=4, rough=0.4)
    k.cyl(202, 4, (0, 0, 2), ALU, metal=0.6, rough=0.3)
    k.cyl(35, 30, (0, 0, 125), ALU, metal=0.6, rough=0.3)
    k.cyl(1.8, 260, (0, 0, 280), '#1A1C20', rough=0.5)          # suspension cord up to the ceiling


def ceiling_disc(k):
    """Flat round ceiling luminaire lying face up: a white disc with a diffuser on top."""
    k.cyl(150, 40, (0, 0, 20), WHITE, bevel=4, rough=0.4)
    k.cyl(132, 2, (0, 0, 41), DIFFUSER, bevel=0.8, rough=0.2)


def motion_ceiling(k):
    """Round ceiling motion sensor lying face up: a white base with a grey dome lens on top."""
    k.cyl(50, 22, (0, 0, 11), WHITE, bevel=3, rough=0.4)
    k.cyl(38, 14, (0, 0, 29), LENS, r2=30, bevel=2, rough=0.2)


def presence_ceiling(k):
    """Round ceiling presence detector lying face up: a flat white disc, a dark window and a thin ring."""
    k.cyl(50, 14, (0, 0, 7), WHITE, bevel=2, rough=0.4)
    k.cyl(20, 1.5, (0, 0, 14.8), DARK, rough=0.2)
    k.torus(34, 1.2, (0, 0, 14.5), '#E9EEF2', rough=0.3)


def lamp(k, r=30):
    """E27 LED lamp standing upright: a screw base, a short neck and a round bulb that tapers into the neck."""
    k.cyl(13.5, 27, (0, 0, 13.5), ALU, metal=0.7, rough=0.3)
    k.cyl(15, 4, (0, 0, 29), ALU, metal=0.7, rough=0.3)
    k.cyl(16, 17, (0, 0, 37.5), ALU, r2=21, metal=0.2, rough=0.4)
    k.sphere(r, (0, 0, 66), WHITE, scale=(1, 1, 1.1), rough=0.3)


def strip_reel(k):
    """Reel of LED strip lying flat: two white flanges, the strip wound into a thick drum and a grey core."""
    k.cyl(120, 4, (0, 0, 2), WHITE, bevel=1, rough=0.4)
    k.cyl(120, 4, (0, 0, 50), WHITE, bevel=1, rough=0.4)
    k.cyl(104, 44, (0, 0, 26), STRIP, rough=0.5)
    k.cyl(55, 46, (0, 0, 26), REEL, rough=0.4)


def mirror_light(k):
    """Horizontal LED mirror light standing upright: a long white bar with a diffuser strip on its front."""
    k.box((600, 50, 60), (0, -25, 30), WHITE, bevel=5, rough=0.4)
    k.box((560, 3, 36), (0, -51.5, 30), DIFFUSER, bevel=1, rough=0.2)


def emergency_light(k):
    """Surface-mounted emergency light standing upright: a white box with a pale window on the front."""
    k.box((200, 50, 70), (0, -25, 35), WHITE, bevel=4, rough=0.4)
    k.box((150, 2, 36), (0, -51, 36), '#E3F0EA', bevel=1, rough=0.2)


SKUS = {
    'DEMO-ELE-3001': (ceiling_panel, {'w': 620, 'd': 620}, {'pitch': 50}),
    'DEMO-ELE-3002': (tube, {'length': 1500, 'yaw': 25}, {'pitch': 40, 'fill': 0.9}),
    'DEMO-ELE-3003': (motion_wall, {}),
    'DEMO-ELE-3004': (ceiling_panel, {'w': 600, 'd': 600}, {'pitch': 50}),
    'DEMO-ELE-3005': (ceiling_panel, {'w': 600, 'd': 600}, {'pitch': 50}),
    'DEMO-ELE-3006': (ceiling_panel, {'w': 1200, 'd': 300, 'yaw': 20}, {'pitch': 50, 'fill': 0.9}),
    'DEMO-ELE-3007': (tube, {'length': 600, 'yaw': 10}, {'pitch': 40}),
    'DEMO-ELE-3008': (tube, {'length': 1200, 'yaw': 20}, {'pitch': 40, 'fill': 0.9}),
    'DEMO-ELE-3009': (downlight, {'colour': 'white'}, {'pitch': 50}),
    **{f'DEMO-ELE-3009-{c.upper()}': (downlight, {'colour': c}, {'pitch': 50})
       for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-3010': (wall_luminaire, {'colour': 'white'}),
    **{f'DEMO-ELE-3010-{c.upper()}': (wall_luminaire, {'colour': c}) for c in ('white', 'black', 'anthracite')},
    'DEMO-ELE-3011': (pendant, {}),
    'DEMO-ELE-3012': (ceiling_disc, {}, {'pitch': 45}),
    'DEMO-ELE-3013': (motion_ceiling, {}, {'pitch': 40}),
    'DEMO-ELE-3014': (presence_ceiling, {}, {'pitch': 40}),
    'DEMO-ELE-3015': (lamp, {'r': 28}),
    'DEMO-ELE-3016': (lamp, {'r': 31}),
    'DEMO-ELE-3017': (lamp, {'r': 34}),
    'DEMO-ELE-3018': (strip_reel, {}, {'pitch': 35}),
    'DEMO-ELE-3019': (mirror_light, {}),
    'DEMO-ELE-3020': (emergency_light, {}),
}

HINTS = {
    'DEMO-ELE-3001': 'A flat square LED ceiling panel, 62 by 62 cm, lying face up on the floor: a light grey frame round a bright, evenly lit white diffuser. The whole panel visible, standing out clearly from the white background with a soft shadow. Not a tile, not a mirror.',
    'DEMO-ELE-3002': 'A slim T8 LED tube, 1500 mm long and about 26 mm thick, lying diagonally on the floor: a milky white glass tube with a white plastic end cap at each end. Each end cap carries two straight metal G13 bi-pins sticking out, so four pins in total, two at each end, clearly visible. Not a plain tube with domed caps. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-3003': 'A small white surface-mounted PIR motion sensor on a wall, standing upright: a flat square white housing with a dark wide-angle lens band across the front, the lens band a segmented Fresnel window with raised horizontal facet ridges. Not a flat plate and not a light switch or push button: a sensor with a visible lens. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-3004': 'A flat square LED ceiling panel, 60 by 60 cm, neutral white light, lying face up on the floor: a light grey frame round a white diffuser. The whole panel visible, standing out clearly from the white background with a soft shadow. Not a floor tile, not a light box.',
    'DEMO-ELE-3005': 'A square recessed LED ceiling panel, 60 x 60 cm, lying flat on the floor seen from above at an angle: a thin flat aluminium frame in white with a uniform opal white diffuser surface, about 1 cm thick, perfectly straight edges. Not a mirror, not a picture frame.',
    'DEMO-ELE-3006': 'A long narrow recessed LED ceiling panel, 30 x 120 cm, lying flat on the floor diagonally across the frame seen from above at an angle: a thin flat white aluminium frame with a uniform opal white diffuser surface, about 1 cm thick, perfectly straight edges. Not standing up, not a shelf.',
    'DEMO-ELE-3007': 'A short T8 LED tube, 600 mm long, lying on the floor: a milky white glass tube with a white plastic end cap at each end. Each end has two straight metal G13 bi-pins sticking out of the cap, four pins in total, clearly visible. Not a hollow metal collar, not a plain domed cap. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-3008': 'A T8 LED tube, 1200 mm long, lying diagonally on the floor: a milky white glass tube with a white plastic end cap at each end. Each end has two straight metal G13 bi-pins sticking out of the cap, four pins in total, clearly visible. Not a hollow metal collar, not a plain domed cap. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-3009': 'A round recessed LED downlight, about 10 cm across, lying face up on the floor: a white round trim with a white lens in the centre and a thin dark ring round the lens. The whole product visible, standing out clearly from the white background with a soft shadow. Not a dome, not a plate.',
    'DEMO-ELE-3009-WHITE': 'A round recessed LED downlight, white, about 10 cm across, lying face up on the floor: a white round trim with a white lens in the centre and a thin dark ring round the lens. The whole product visible, standing out clearly from the white background with a soft shadow. Not a dome, not a plate.',
    'DEMO-ELE-3009-BLACK': 'A round recessed LED downlight, black, about 10 cm across, lying face up on the floor: a black round trim with a white lens in the centre and a thin dark ring round the lens. The whole product visible, standing out clearly from the white background with a soft shadow. Not a dome, not a plate.',
    'DEMO-ELE-3009-ANTHRACITE': 'A round recessed LED downlight, anthracite (dark grey), about 10 cm across, lying face up on the floor: an anthracite round trim with a white lens in the centre and a thin dark ring round the lens. The whole product visible, standing out clearly from the white background with a soft shadow. Not a dome, not a plate.',
    'DEMO-ELE-3010': 'A wall luminaire standing upright: a long white box about 24 cm wide and 7 cm tall, with a white diffuser strip on its front. The whole product visible, standing out clearly from the white background with a soft shadow. Not a shelf, not a switch.',
    'DEMO-ELE-3010-WHITE': 'A wall luminaire, white, standing upright: a long white box about 24 cm wide and 7 cm tall, with a white diffuser strip on its front. The whole product visible, standing out clearly from the white background with a soft shadow. Not a shelf, not a switch.',
    'DEMO-ELE-3010-BLACK': 'A wall luminaire, black, standing upright: a long black box about 24 cm wide and 7 cm tall, with a white diffuser strip on its front. The whole product visible, standing out clearly from the white background with a soft shadow. Not a shelf, not a switch.',
    'DEMO-ELE-3010-ANTHRACITE': 'A wall luminaire, anthracite (dark grey), standing upright: a long anthracite box about 24 cm wide and 7 cm tall, with a white diffuser strip on its front. The whole product visible, standing out clearly from the white background with a soft shadow. Not a shelf, not a switch.',
    'DEMO-ELE-3011': 'A round LED pendant luminaire, about 40 cm across, standing on its wide rim: a white shade wider at the bottom and narrower at the top, with a small round canopy on top, and a black suspension cord rising straight up from the canopy, out of the frame, which hangs the shade from the ceiling. Not a ceiling light: the cord must be visible. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-3012': 'A flat round ceiling luminaire, about 30 cm across, lying face up on the floor: a white round body about 4 cm thick with a white diffuser on top. The whole product visible, standing out clearly from the white background with a soft shadow. Not a plate, not a bowl.',
    'DEMO-ELE-3013': 'A small round white motion sensor for ceiling mounting, lying face up on the floor: a white round base with a grey dome-shaped lens on top. The whole product visible, standing out clearly from the white background with a soft shadow. Not a smoke detector, not a speaker.',
    'DEMO-ELE-3014': 'A small round white presence detector for ceiling mounting, lying face up on the floor: a flat white disc with a dark sensor window in the centre and a thin light ring around it. The whole product visible, standing out clearly from the white background with a soft shadow. Not a dome, not a smoke detector.',
    'DEMO-ELE-3015': 'An LED lamp with an E27 screw base, standing upright: a frosted white pear-shaped bulb on a silver aluminium base. A small lamp, shorter than the 9 W and 13 W lamps. The whole lamp visible, standing out clearly from the white background with a soft shadow. Not a candle, not a halogen lamp.',
    'DEMO-ELE-3016': 'An LED lamp with an E27 screw base, standing upright: a frosted white round bulb that tapers evenly into a short neck on a silver aluminium screw base, like a classic A-shape bulb. A medium lamp, taller than the 6 W lamp. The whole lamp visible, standing out clearly from the white background with a soft shadow. Not a candle, not a halogen lamp.',
    'DEMO-ELE-3017': 'A classic A60 pear-shaped LED light bulb, upright and symmetric: a smooth frosted opal glass bulb centred exactly above a short white plastic neck and a metal E27 screw base, all on one vertical axis, not tilted, not lopsided, not egg-shaped. Not a clear filament bulb. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-3018': 'A reel of flexible LED strip lying flat on the floor, seen from above at an angle: two white plastic flanges, the warm white LED strip wound into a thick solid drum between them, and a small grey core in the middle. The whole reel visible, standing out clearly from the white background with a soft shadow. Not a rope light, not a cable drum.',
    'DEMO-ELE-3019': 'A horizontal LED mirror light for above a bathroom mirror, standing upright: a long white bar about 60 cm wide with a white diffuser strip on its front. The whole product visible, standing out clearly from the white background with a soft shadow. Not a shelf, not a round wall light.',
    'DEMO-ELE-3020': 'A surface-mounted emergency light standing upright: a white box with a pale translucent window on its front. The whole product visible, standing out clearly from the white background with a soft shadow. Not a switch, not a green exit sign, no lettering.',
}
