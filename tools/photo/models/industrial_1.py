"""Industrial pack, series 1: cordless and corded power tools, batteries, charger, vacuum.

Neutral greys and dark bodies only; the accent is never used on the tools.
Units mm, products stand on z=0 with the front facing -Y.
"""

ABRASIVE_BLUE = '#6F7A88'   # grinding disc, grey-blue abrasive
SANDPAPER = '#A8642E'      # sanding sheet and belt, brown corundum
WOOD = '#C9A36B'           # timber board for the jigsaw photo
BURG = '#7A1F2B'           # Brakkwerk burgundy housing
ANTH = '#33373F'           # anthracite trim
import math

BAT = {'dark': '#2A2E35', 'mid': '#4A515C', 'mid': '#7B838F', 'light': '#C9CED6'}


def cordless_drill(k, impact=False):
    """Compact cordless drill driver (impact=True: impact driver with hex nose), side profile."""
    front = 52 if impact else 74
    k.profile([(-38, 48), (-6, 48), (4, 90), (16, 96), (front, 98), (front + 2, 140), (-30, 146),
               (-56, 134), (-60, 112), (-46, 96), (-42, 80)], 48, 0, 'mid', round_=12)       # housing with grip
    k.box((74, 60, 44), (-22, 0, 26), 'dark', bevel=6)                                       # battery, closing up to the grip
    k.box((12, 14, 20), (10, 0, 84), 'dark', bevel=3)                                        # trigger
    if impact:
        k.cyl(20, 22, (front + 12, 0, 119), 'dark', rot=(0, 90, 0), bevel=2)                 # nose
        k.cyl(9, 22, (front + 34, 0, 119), 'steel', rot=(0, 90, 0), verts=6, metal=0.8)       # hex chuck
        k.box((30, 8, 22), (-12, -28, 66), 'dark', bevel=2)                                  # bit holder, near side
        k.box((30, 8, 22), (-12, 28, 66), 'dark', bevel=2)                                   # bit holder, far side
    else:
        k.cyl(22, 14, (front + 8, 0, 119), 'dark', rot=(0, 90, 0), bevel=2)                  # torque collar
        k.cyl(18, 34, (front + 31, 0, 119), 'dark', rot=(0, 90, 0), r2=13, bevel=1)          # keyless chuck body
        for a in (90, 210, 330):                                                             # three chuck jaws round the bit
            t = math.radians(a)                                                              # (cyl, not box: box() bakes its location)
            k.cyl(3, 12, (front + 52, 6 * math.cos(t), 119 + 6 * math.sin(t)), 'steel', rot=(0, 90, 0), metal=0.8, rough=0.3)
        k.cyl(4, 20, (front + 56, 0, 119), 'steel', rot=(0, 90, 0), metal=0.8)               # bit


def battery(k, size=(92, 58, 42), contacts=True):
    """Slide-on battery pack, a rounded block with a rail on top."""
    x, y, z = size
    k.box((x, y, z), (0, 0, z / 2), 'dark', bevel=4)                                         # shell
    k.box((x - 22, y - 16, 4), (0, 0, z + 0.5), 'mid', bevel=1)                              # top rail
    k.box((x - 30, 22, 2), (0, -y / 2 - 0.5, z / 2 - 4), 'light', bevel=0.5)               # charge indicator strip
    if contacts:
        k.box((22, 8, 2.5), (0, 0, z + 2.3), 'light', bevel=0.5)                              # contact plate


def grinder(k, disc=125, cordless=False):
    """Angle grinder, lying on its side on the guard edge, with a grinding disc fitted and one side handle.
    Corded: mains cable out of the rear cap. Cordless: the battery slides onto the rear end of the body."""
    r = disc / 2
    k.cyl(28, 130, (-20, 0, 34), 'mid', rot=(0, 90, 0), bevel=2)                             # motor
    k.box((50, 52, 62), (50, 0, 40), 'mid', bevel=6)                                        # gear head
    k.box((56, 10, 12), (-20, 0, 66), 'dark', bevel=2)                                       # top rib
    k.cyl(r, 3, (62, 0, r), ABRASIVE_BLUE, rot=(90, 0, 0), metal=0.3, rough=0.6)             # grinding disc
    guard = ([(round(62 + (r + 9) * math.cos(math.radians(t)), 2), round(r + (r + 9) * math.sin(math.radians(t)), 2))
              for t in range(0, 181, 10)]
             + [(round(62 + (r + 3) * math.cos(math.radians(t)), 2), round(r + (r + 3) * math.sin(math.radians(t)), 2))
                for t in range(180, -1, -10)])
    k.profile(guard, 14, 0, 'mid')                                                           # guard: half shell over the top half of the disc
    k.cyl(10, 28, (62, 0, r), 'steel', rot=(90, 0, 0), metal=1)                              # flange nut
    k.box((14, 14, 34), (40, -26, 70), 'dark', bevel=3)                                      # side handle post (the only handle)
    k.box((16, 66, 14), (40, -58, 88), 'dark', bevel=4)                                      # side handle bar
    if cordless:
        k.box((36, 50, 40), (-103, 0, 34), 'dark', bevel=4)                                  # battery pack, slid onto the rear end
    else:
        k.cyl(22, 10, (-89, 0, 34), 'dark', rot=(0, 90, 0), bevel=1)                         # flat rear end cap
        k.cyl(4, 80, (-100, 0, 14), '#1A1C20', rot=(0, 90, 0))                                # cable stub


def grinder_cordless(k, disc=115):
    """Cordless angle grinder resting level on its disc, as real ones are shown: the body horizontal along X,
    the gear head at the front with the spindle pointing down, the grinding disc horizontal under the gear
    head, a half-shell guard over the rear half of the disc (towards the body), no side handle fitted, a slide
    switch on top, and the 18 V battery slid on under the rear end."""
    r = disc / 2
    zb = 58                                                                                    # body axis height
    xg = 40                                                                                    # spindle axis (x)
    k.cyl(29, 112, (-44, 0, zb), BURG, rot=(0, 90, 0), bevel=3)                               # motor housing
    k.cyl(25, 56, (-128, 0, zb), ANTH, rot=(0, 90, 0), bevel=3)                               # rear grip
    k.box((84, 60, 34), (-130, 0, 17), ANTH, bevel=5)                                         # battery pack under the rear end
    k.box((40, 16, 10), (-50, 0, zb + 31), ANTH, bevel=3)                                     # slide switch on top
    k.box((56, 54, 46), (xg - 6, 0, zb + 2), 'mid', bevel=7, metal=0.4, rough=0.4)            # gear head
    k.cyl(6, 8, (xg, 0, zb + 29), 'dark')                                                     # spindle lock button
    k.cyl(9, zb - 23 - 9, (xg, 0, 9 + (zb - 23 - 9) / 2), 'steel', metal=1)                    # spindle, pointing down
    k.cyl(r, 3, (xg, 0, 8.5), ABRASIVE_BLUE, metal=0.3, rough=0.6, verts=96)                  # grinding disc, horizontal
    k.cyl(11, 4, (xg, 0, 5), 'steel', metal=1, verts=6)                                       # clamping nut under the disc
    half = [(round(xg + (r + 7) * math.cos(math.radians(t)), 2), round((r + 7) * math.sin(math.radians(t)), 2))
            for t in range(90, 271, 10)]
    k.slab(half, 2, 13, 'metal', round_=0.8, metal=0.8, rough=0.3)                            # guard: top plate over the rear half
    rim = ([(round(xg + (r + 7) * math.cos(math.radians(t)), 2), round((r + 7) * math.sin(math.radians(t)), 2))
            for t in range(90, 271, 10)]
           + [(round(xg + (r + 4) * math.cos(math.radians(t)), 2), round((r + 4) * math.sin(math.radians(t)), 2))
              for t in range(270, 89, -10)])
    k.slab(rim, 11, 4, 'metal', round_=1, metal=0.8, rough=0.3)                               # guard: rim round the rear half
    # No side handle fitted (2026-10-19): it ships loose in the box, and the photo, close-up and drawing all show the tool without it.


def percussion(k):
    """Corded percussion drill 710 W standing on its grip foot: one-piece burgundy body with a pistol grip at
    the rear, anthracite grip, keyless chuck, a side handle clamped behind the chuck, and exactly ONE mains
    cable: it leaves the bottom rear of the grip through a bend protector and ends in a Schuko plug."""
    k.profile([(-112, 150), (-96, 166), (52, 162), (72, 152), (76, 112), (60, 100), (-36, 100), (-44, 90),
               (-50, 24), (-40, 10), (-40, 0), (-112, 0), (-116, 22), (-118, 100)], 58, 0, BURG, round_=10)   # body with pistol grip
    k.profile([(-114, 96), (-40, 96), (-48, 24), (-40, 8), (-40, 0), (-112, 0), (-117, 22)], 60, 0, ANTH, round_=10)  # anthracite grip
    k.box((14, 18, 30), (-32, 0, 80), ANTH, bevel=3)                                          # trigger
    k.cyl(24, 22, (86, 0, 132), ANTH, rot=(0, 90, 0), bevel=2)                                # gear neck
    k.cyl(21, 40, (117, 0, 132), 'dark', rot=(0, 90, 0), r2=16, bevel=1)                      # keyless chuck
    k.cyl(28, 14, (88, 0, 132), 'dark', rot=(0, 90, 0), bevel=2)                              # side handle clamp ring
    k.cyl(15, 96, (88, -22, 72), 'dark', rot=(160, 0, 0), bevel=3)                             # side handle, hanging down from the clamp
    k.cyl(9, 34, (-118, 0, 14), 'dark', rot=(0, 90, 0), r2=5)                                 # bend protector at the grip foot
    cable(k, [(-136, 0, 12), (-156, -4, 4), (-180, -14, 2.6), (-206, -18, 2.6), (-236, -18, 2.6)])   # the one mains cable, on the floor
    k.box((30, 22, 16), (-251, -18, 8), '#1A1C20', bevel=3)                                    # Schuko plug body (no rot: box() bakes its location)
    for py in (-24, -12):                                                                     # two round pins
        k.cyl(2.4, 16, (-274, py, 8), 'steel', rot=(0, 90, 0), metal=1)


def cable(k, pts, r=2.6, color='#1A1C20'):
    """Flexible cable through the points: round joints and straight segments between them."""
    for p in pts:
        k.sphere(r, p, color)
    for a, b in zip(pts, pts[1:]):
        d = [b[i] - a[i] for i in range(3)]
        length = math.sqrt(sum(c * c for c in d))
        mid = [(a[i] + b[i]) / 2 for i in range(3)]
        tilt = math.degrees(math.acos(max(-1.0, min(1.0, d[2] / length))))
        yaw = math.degrees(math.atan2(d[1], d[0]))
        k.cyl(r, length, mid, color, rot=(0, tilt, yaw), verts=16)


def jigsaw(k, cordless=False):
    """Jigsaw on its own, shoe level and blade pointing straight down under the base plate (no board).
    Burgundy and anthracite housing. Corded: the mains cable leaves the back of the rear grip, drops to the
    floor and lies there in a loose curve, ending in a Schuko plug. Cordless: battery at the back."""
    Z = 40                                                                                    # shoe height above the ground
    k.box((96, 74, 6), (0, 0, Z + 3), 'light', bevel=2)                                      # shoe
    k.box((2, 4, 28), (14, 0, Z - 14), 'steel', metal=1, rough=0.2)                          # blade going down
    # One connected body (2026-10-19, for the drawing): motor body on the shoe, a closed D-handle whose top bar
    # rests on the body and whose rear post comes down behind it, leaving the hand opening between them.
    k.box((60, 40, 90), (-8, 0, Z + 51), BURG, bevel=6)                                     # motor body, standing on the shoe
    k.box((80, 28, 20), (-30, 0, Z + 106), ANTH, bevel=6)                                   # D-handle top bar, on the body
    k.box((16, 26, 76), (-62, 0, Z + 78), ANTH, bevel=4)                                    # D-handle rear post (the grip)
    if cordless:
        k.box((50, 46, 36), (-62, 0, Z + 22), ANTH, bevel=4)                                 # battery pack under the rear post
    else:
        cable(k, [(-70, 0, Z + 46), (-70, 0, 70), (-86, 0, 30), (-100, 0, 6), (-120, 0, 2.6), (-170, 0, 2.6)])   # drops to the floor and runs back
        k.box((30, 22, 16), (-185, 0, 8), '#1A1C20', bevel=3)                                 # Schuko plug body (no rot: box() bakes its location)
        for py in (-6, 6):                                                                    # two round pins
            k.cyl(2.4, 16, (-208, py, 8), 'steel', rot=(0, 90, 0), metal=1)


def circular(k, d, cordless=False):
    """Circular hand saw resting on its base plate. The blade stands in a slot in the plate: the plate is two
    strips, one either side of the blade, with no plate under the blade. A steel guard covers the top half of
    the blade. Battery (cordless) or mains cable at the rear."""
    # Rebuilt 2026-10-19 after real saws: ONE flat toothed blade (a single extruded outline, truly round), a fixed
    # upper guard over its top half, a retracting lower guard swung back over the rear lower quarter (so the
    # front lower teeth show), a full sole plate with a slot, the motor on the far side, a loop handle on top.
    r = d / 2
    yb = -40                                                                                 # blade plane, on the camera side of the plate
    zc = 6 + r                                                                               # blade centre: lowest tooth 6 mm above the floor
    pz = 24                                                                                  # underside of the sole plate
    W = d + 80
    k.box((W, 70 - (yb + 4), 4), (10, ((yb + 4) + 70) / 2, pz + 2), 'light', metal=0.6, rough=0.35, bevel=1)   # sole plate, motor side of the slot
    k.box((W, (yb - 4) + 62, 4), (10, (-62 + (yb - 4)) / 2, pz + 2), 'light', metal=0.6, rough=0.35, bevel=1)  # sole plate, front strip
    n = 24 if d >= 180 else 20                                                               # carbide teeth
    blade = []
    for i in range(n):
        a = 2 * math.pi * i / n
        for rr, da in ((r - 7, 0.0), (r - 1, 0.55), (r, 0.72)):                             # gullet, tooth back, tooth tip
            t = a + da * 2 * math.pi / n
            blade.append((round(rr * math.cos(t), 2), round(zc + rr * math.sin(t), 2)))
    k.profile(blade, 2.2, yb, 'steel', round_=0.4, smooth=0, metal=1, rough=0.22)            # the blade: one round toothed disc
    k.cyl(r * 0.2, 4, (0, yb - 3, zc), 'steel', rot=(90, 0, 0), metal=1, rough=0.3)           # outer arbor flange
    k.cyl(7, 6, (0, yb - 6, zc), 'dark', rot=(90, 0, 0), verts=6)                             # arbor bolt
    def band(r_in, r_out, a0, a1, step=6):
        outer = [(round(r_out * math.cos(math.radians(t)), 2), round(zc + r_out * math.sin(math.radians(t)), 2))
                 for t in range(a0, a1 + 1, step)]
        inner = [(round(r_in * math.cos(math.radians(t)), 2), round(zc + r_in * math.sin(math.radians(t)), 2))
                 for t in range(a1, a0 - 1, -step)]
        return outer + inner
    k.profile(band(r + 2, r + 8, -12, 192), 14, yb + 1, 'body', round_=1.5, metal=0.3, rough=0.4)   # fixed upper guard: rim over the top half
    k.profile(band(r * 0.8, r + 8, -12, 192), 2, yb - 6, 'body', round_=0.8, metal=0.3, rough=0.4)  # upper guard: outer side wall
    k.profile(band(r + 1, r + 5, 196, 276), 10, yb, 'dark', round_=1.2)                       # lower guard, swung back: rim
    k.profile(band(r * 0.84, r + 5, 196, 276), 1.6, yb - 4.5, 'dark', round_=0.6)              # lower guard: side wall
    k.box((10, 6, 20), (-(r * 0.72), yb - 7, zc - r * 0.62), 'dark', bevel=2)              # lower guard retracting lever
    k.cyl(36, 86, (-8, 12, zc - 4), BURG, rot=(90, 0, 0), bevel=4)                            # motor, axis across the blade, far side
    k.cyl(32, 12, (-8, 60, zc - 4), ANTH, rot=(90, 0, 0), bevel=3)                            # motor end cap
    k.box((96, 64, zc - 4 - pz - 10), (-20, 14, pz + 4 + (zc - 4 - pz - 10) / 2), BURG, bevel=6)   # housing down to the plate
    cable(k, [(-112, 12, zc - 18), (-104, 12, zc + 42), (-72, 12, zc + 66), (0, 12, zc + 66), (24, 12, zc + 34)],
          r=13, color=BURG)                                                                   # closed loop handle on top
    k.box((16, 14, 24), (-70, 12, zc + 46), 'dark', bevel=3)                                  # trigger in the handle
    k.sphere(17, (r * 0.62, 20, pz + 36), ANTH)                                               # front knob
    k.box((26, 22, 30), (r * 0.62, 20, pz + 18), BURG, bevel=4)                              # front knob post
    if cordless:
        k.box((70, 60, 42), (-124, 12, zc - 30), ANTH, bevel=5)                               # 18 V battery pack behind the handle
    else:
        k.cyl(7, 30, (-124, 12, zc - 22), 'dark', rot=(0, 90, 0), r2=4)                       # bend protector
        cable(k, [(-139, 12, zc - 22), (-158, 16, zc - 34), (-172, 22, zc - 58), (-182, 28, 30), (-194, 34, 6), (-218, 44, 2.6), (-252, 50, 2.6)])     # the one mains cable


def multi_tool(k):
    """Cordless oscillating multi-tool, horizontal body, battery under the grip, triangular blade."""
    k.cyl(22, 130, (0, 0, 46), BURG, rot=(0, 90, 0), bevel=2)                               # burgundy body
    k.cyl(23, 50, (-40, 0, 46), ANTH, rot=(0, 90, 0), bevel=2)                               # anthracite rear grip
    k.box((30, 30, 22), (58, 0, 38), 'mid', bevel=3, metal=0.4)                              # metal gear head
    k.cyl(9, 6, (-20, 23, 50), '#1F2226', rot=(90, 0, 0))                                    # speed dial on the far side
    k.slab([(50, -32), (116, -10), (128, 0), (116, 10), (50, 32)], 2, 30, 'steel', round_=1.0, metal=1, rough=0.2)  # flat triangular blade, wide, fixed at the head
    k.box((22, 16, 6), (-30, 0, 66), 'dark', bevel=2)                                        # switch
    k.box((46, 40, 26), (-44, 0, 13), ANTH, bevel=4)                                         # battery


def orbital_sander(k):
    """Random orbital sander standing upright on a full round 125 mm sanding disc that lies flat on the floor.
    The disc is brown with a ring of dust holes; the pad is under the body; the knob is on top; a dust port on the side."""
    k.cyl(62.5, 1.5, (0, 0, 0.75), SANDPAPER, metal=0, rough=0.9)                            # full sanding disc on the floor
    for i in range(12):                                                                       # dust holes near the rim
        a = math.radians(30 * i)
        k.cyl(2, 1.8, (60 * math.cos(a), 60 * math.sin(a), 0.9), '#2F343C', verts=16)
    k.cyl(60, 9, (0, 0, 6), '#1F2226', bevel=1)                                              # black backing pad, on the disc
    k.cyl(50, 12, (0, 0, 16), ANTH, bevel=2)                                                 # anthracite skirt over the pad
    k.cyl(46, 52, (0, 0, 48), BURG, bevel=4)                                                 # burgundy motor body
    k.sphere(48, (0, 0, 74), ANTH, scale=(1, 1, 0.62))                                       # anthracite palm-grip dome on top
    k.box((22, 8, 12), (0, -45, 60), '#1F2226', bevel=2)                                     # on/off switch on the front
    k.cyl(15, 40, (62, 0, 38), ANTH, rot=(0, 90, 0), bevel=2)                                # dust port at the rear
    k.box((50, 44, 46), (104, 0, 40), ANTH, bevel=6)                                         # dust box on the port


def detail_sander(k):
    """Detail sander: triangular pad under a long body with a handle on top, and a ribbed vacuum hose
    lying on the floor from a socket at the back."""
    k.cyl(54, 8, (0, 0, 4), 'mid', verts=3, bevel=2, rot=(0, 0, 0))                          # triangle pad
    k.box((112, 46, 48), (0, 0, 34), 'mid', bevel=10)                                       # body
    k.box((60, 40, 20), (-20, 0, 66), 'dark', bevel=6)                                       # handle top
    k.cyl(14, 14, (44, 0, 40), 'dark', rot=(0, 90, 0))                                       # dust outlet
    k.cyl(16, 12, (-62, 0, 20), 'dark', rot=(0, 90, 0))                                      # hose socket at the back
    k.cyl(14, 130, (-130, 0, 14), '#2B2E33', rot=(0, 90, 0), verts=24)                       # vacuum hose on the floor, from the socket


def hot_air_gun(k):
    """Pistol-shaped hot air gun standing on its grip: a short round heater housing on top, a narrow
    tapered nozzle pointing forward, a grip under the rear and a trigger in front of the grip."""
    k.cyl(30, 110, (-5, 0, 80), 'mid', rot=(0, 90, 0), bevel=3)                             # heater housing
    k.cyl(16, 70, (95, 0, 80), 'dark', rot=(0, 90, 0), r2=11)                               # narrow nozzle
    k.box((34, 36, 74), (-40, 0, 42), 'dark', bevel=6)                                      # pistol grip
    k.box((12, 10, 26), (-18, -20, 46), 'mid', bevel=2)                                     # trigger
    k.box((16, 14, 10), (-30, -24, 92), 'mid', bevel=2)                                     # switch


def belt_sander(k):
    """Belt sander like a real one: a long low body. The sanding belt loops round a front and a rear drum
    along the whole underside, no base plate. A burgundy housing sits over the belt, a closed rear handle
    rises at the back, a round front knob sits on the nose, and a dust spigot sticks out at the rear."""
    for x in (-105, 105):
        k.cyl(30, 80, (x, 0, 30), SANDPAPER, rot=(90, 0, 0), rough=0.9)                        # belt round each drum
        k.cyl(22, 84, (x, 0, 30), 'dark', rot=(90, 0, 0), bevel=1)                             # drum ends
    k.box((210, 80, 4), (0, 0, 2), SANDPAPER, metal=0, rough=0.9)                                # bottom run of the belt
    k.box((210, 80, 4), (0, 0, 58), SANDPAPER, metal=0, rough=0.9)                               # top run, under the housing
    k.box((250, 92, 44), (0, 0, 70), BURG, bevel=8)                                             # housing over the belt
    k.box((90, 70, 40), (-70, 0, 108), ANTH, bevel=10)                                         # motor cap at the back
    k.profile([(-150, 88), (-150, 160), (-40, 160), (-40, 128), (-62, 128), (-62, 140), (-128, 140), (-128, 88)],
              30, y=0, color=ANTH, round_=8)                                                   # closed rear handle
    k.cyl(24, 30, (95, 0, 104), ANTH, bevel=6)                                                 # front knob
    k.cyl(14, 50, (-140, 50, 66), 'dark', rot=(90, 0, 0))                                      # dust spigot at the rear side


def charger(k):
    """Fast charger: block with a slide-in slot on the front face (the 18 V pack goes in from the front) and a status panel on top of it."""
    k.box((104, 70, 46), (0, 0, 23), 'mid', bevel=6)                                        # block
    k.box((74, 1.5, 24), (0, -35.5, 22), 'dark', bevel=0.5)                                  # front slot for the battery rail
    k.box((46, 1.5, 10), (0, -35.5, 40), 'dark', bevel=0.5)                                  # status panel, above the slot
    k.cyl(4, 8, (-20, -35, 42), 'light', rot=(90, 0, 0))                                     # led


def wet_dry_vac(k):
    """Wet and dry vacuum: round 20 litre tank with a motor head on top and a hose socket."""
    k.cyl(132, 300, (0, 0, 160), 'mid', bevel=4, verts=64)                                  # tank
    k.cyl(140, 80, (0, 0, 340), 'dark', bevel=4)                                             # motor head
    k.cyl(120, 30, (0, 0, 396), 'dark', bevel=3, r2=110)                                     # lid
    k.cyl(22, 80, (110, 0, 300), 'mid', rot=(0, 90, 0))                                      # hose socket
    for x, y in ((-90, -90), (90, -90), (-90, 90), (90, 90)):
        k.cyl(12, 12, (x, y, 6), 'dark')                                                    # feet
    k.cyl(16, 10, (0, -141, 352), 'light', rot=(90, 0, 0), bevel=2)                         # power button, proud of the motor head




SKUS = {
    # 1001 compact drill driver, 1002 impact driver with hex chuck
    'DEMO-IND-1001': (cordless_drill, {'impact': False}),
    'DEMO-IND-1002': (cordless_drill, {'impact': True}),
    # 1003 corded 125 mm grinder, 1018 cordless 115 mm grinder
    'DEMO-IND-1003': (grinder, {'disc': 125, 'cordless': False}),
    'DEMO-IND-1018': (grinder_cordless, {'disc': 115}, {'pitch': 24}),
    # 1004 18 V battery pack, 1016 12 V battery pack (longer, smaller)
    'DEMO-IND-1004': (battery, {'size': (92, 58, 42)}),
    'DEMO-IND-1016': (battery, {'size': (72, 44, 30)}),
    'DEMO-IND-1005': (percussion, {}, {'yaw': -20, 'pitch': 10}),                          # side view: chuck, side handle and the one cable all readable
    # 1006 corded jigsaw, 1008 cordless jigsaw
    'DEMO-IND-1006': (jigsaw, {'cordless': False}),
    'DEMO-IND-1008': (jigsaw, {'cordless': True}),
    # 1007 corded 190 mm circular saw, 1009 cordless 165 mm circular saw
    'DEMO-IND-1007': (circular, {'d': 190, 'cordless': False}, {'yaw': -14, 'pitch': 12}),  # nearly square onto the blade: a round disc
    'DEMO-IND-1009': (circular, {'d': 165, 'cordless': True}, {'yaw': -14, 'pitch': 12}),
    'DEMO-IND-1010': (multi_tool, {}, {'yaw': 145}),                                       # from the far side, the blade towards the camera
    'DEMO-IND-1011': (orbital_sander, {}),
    'DEMO-IND-1012': (detail_sander, {}),
    'DEMO-IND-1013': (hot_air_gun, {}),
    'DEMO-IND-1014': (belt_sander, {}),
    'DEMO-IND-1015': (charger, {}),
    'DEMO-IND-1017': (wet_dry_vac, {}),
}


HINTS = {
    'DEMO-IND-1001': 'A compact cordless drill driver with a burgundy and anthracite housing, a black rubber grip under the body and a slim battery pack below the grip. At the front a round keyless chuck with three visible steel jaws gripping a short bit. Not an impact driver: the nose is round, not a hex shank. Plain unmarked housing: no lettering, no logo, no sticker, no rating plate anywhere. No labels or printing.',
    'DEMO-IND-1002': 'A cordless impact driver with a burgundy and anthracite housing and a black rubber grip, a battery pack under the grip, a short stubby nose with a 1/4 inch hex chuck and a small dark bit holder on each side of the housing. Not a drill driver: there is no round keyless chuck, the nose is a hex shank. Plain unmarked housing: no lettering, no logo, no sticker, no rating plate anywhere.',
    'DEMO-IND-1003': 'A corded 125 mm angle grinder lying on its side: a long burgundy and anthracite motor body with a flat rear end cap and the mains cable leaving the back, a gear head at the front end with a black rubber side handle screwed into it, and a grinding disc fitted at the gear head end, its metal guard a half shell over the top half of the disc. The disc is fully behind the guard, the bottom half of the disc is open. Not a cordless tool: no battery. Plain unmarked housing. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1004': 'A slide-on 18 V battery pack resting on its flat base with its long side along the floor, a rounded block about one and a half times as long as it is deep, in burgundy and anthracite, with a raised rail on top, a small metal contact plate and a charge indicator strip on the front. Not a charger: there is no slot and no cable. Plain unmarked housing: no lettering, no logo, no sticker, no rating plate anywhere.',
    'DEMO-IND-1005': 'A corded 710 W percussion drill standing upright on the flat foot of its pistol grip: a compact burgundy one-piece housing with the motor on top, an anthracite rubber pistol grip with a trigger at the rear, a black keyless chuck at the front, and a black rubber side handle clamped round the neck behind the chuck, hanging down. Exactly ONE mains cable: it leaves the bottom rear of the grip through a short black bend protector, lies on the floor and ends in one European Schuko plug with two round pins. There is no second cable, no cable from the barrel or the top, no port and no socket. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1006': 'A corded orbital jigsaw standing on its flat shoe: a maroon housing with a dark grip, a closed D-handle on top, a silver aluminium base plate (shoe) with a bevel scale of plain unnumbered tick marks, the thin steel blade pointing straight down out of the shoe, and a mains cable with a European Schuko plug at the rear. Plain housing with no lettering and no marking on the body. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1007': 'A hand-held 190 mm circular saw standing on its flat steel sole plate, seen from the blade side: ONE perfectly round, flat steel saw blade with sharp carbide teeth evenly round its whole rim and a hex arbor bolt with a round flange in its centre; a fixed dark grey upper blade guard covering the top half of the blade; a black spring-loaded lower blade guard swung back over the rear lower part of the blade so the front lower teeth show; a burgundy motor housing behind the blade; a burgundy closed loop handle on top with a trigger; a round anthracite front knob; one mains cable leaving the rear of the handle. The blade is a single circular disc, not two discs, not an oval, not a grinding disc. No table, no frame. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1008': 'A cordless orbital jigsaw standing on its flat shoe: a burgundy and anthracite housing with a dark grip, a closed D-handle on top, an 18 V battery pack slid onto the rear of the body, a silver base plate with a bevel scale of plain unnumbered tick marks, and the thin steel blade going down out of the shoe. Plain housing with no lettering and no marking on the body. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1009': 'A cordless hand-held 165 mm circular saw standing on its flat steel sole plate, seen from the blade side: ONE perfectly round, flat steel saw blade with sharp carbide teeth evenly round its whole rim and a hex arbor bolt with a round flange in its centre; a fixed dark grey upper blade guard covering the top half of the blade; a black spring-loaded lower blade guard swung back over the rear lower part of the blade so the front lower teeth show; a burgundy motor housing behind the blade; a burgundy closed loop handle on top with a trigger; a round anthracite front knob; an anthracite 18 V battery pack slid onto the rear. No cable. The blade is a single circular disc, not two discs, not an oval. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1010': 'A cordless oscillating multi-tool lying on its side, seen from the head end: a slim horizontal burgundy body with an anthracite rear grip, a small black speed dial on the side, a metal gear head at the front, a flat wide triangular-ended steel blade clamped flat under the head and pointing towards the camera, and an anthracite battery pack under the rear grip. Not a jigsaw: no D-handle, no base plate. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1011': 'A random orbital sander with a burgundy and anthracite housing standing upright on its round 125 mm brown sanding disc, which lies flat on the floor and has a ring of small dust holes: a burgundy round motor body, an anthracite palm-grip dome on top, a black backing pad under an anthracite skirt, a small black switch on the front, and an anthracite dust port with a square anthracite dust box at the rear. The housing is burgundy and anthracite, not grey and not silver. Not an angle grinder: no spindle and no guard. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1012': 'A detail sander with a small triangular grey pad under a long burgundy and anthracite body, a handle on top, and a dust outlet on the side. A ribbed dark grey vacuum hose runs straight from the socket at the back and lies on the floor behind the tool. Not an orbital sander: the pad is triangular and the body is long and narrow. Plain unmarked housing: no lettering, no logo, no sticker, no rating plate anywhere.',
    'DEMO-IND-1013': 'A pistol-shaped hot air gun standing on its black grip, with a short round burgundy heater housing on top, a narrow tapered metal nozzle pointing forward and a trigger switch in front of the grip. Not a hair dryer and not a leaf blower: the nozzle is narrow and metal and the housing is short. Plain unmarked housing: no lettering, no logo, no sticker, no rating plate anywhere.',
    'DEMO-IND-1014': 'A professional handheld belt sander, seen from the side: a long low tool with a burgundy and anthracite housing, a closed loop handle at the rear and a round front grip knob on the nose. A continuous brown sanding belt runs round a front and a rear roller along the whole flat underside. A dust spigot at the rear. Not a toy, not a vehicle, no wheels. No labels or printing.',
    'DEMO-IND-1015': 'A fast charger: a square burgundy and anthracite block with a slide-in slot on its front face that takes the 18 V battery pack, a status panel with a small LED above the slot, and a mains cable with a European Schuko plug. Plain lid and plain front, with no lettering and no marking. Not a battery: it is a box with a slot. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1016': 'A slide-on 12 V battery pack standing on its base: a smaller and narrower burgundy and anthracite block than the 18 V pack, with a raised rail on top, contacts on the rail, and a charge indicator strip on the front. Plain housing with no lettering and no marking. Not a charger: there is no slot and no cable. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-1017': 'A wet and dry vacuum with a round 20 litre tank in burgundy, a motor head and lid in anthracite on top, a round light grey power button raised on the front of the motor head, a hose socket on the side and four small feet at the base. Not a hose: the hose socket is a short round port. Plain unmarked housing: no lettering, no logo, no sticker, no rating plate anywhere.',
    'DEMO-IND-1018': 'A cordless 115 mm angle grinder resting level on the floor: a long horizontal burgundy motor body with an anthracite rear grip and a small anthracite slide switch on top, a grey metal gear head at the front end, ONE grey-blue grinding disc lying flat and horizontal directly under the gear head on a short spindle, a metal half-shell guard over the rear half of that disc (the half towards the body), and a plain anthracite 18 V battery pack slid on under the rear grip. No side handle fitted. Exactly one disc, only at the front under the gear head; nothing round under the battery. The battery pack is a plain smooth block with no printing, no voltage figure, no lettering and no label. No cable. No text, no numbers, no logos, no labels anywhere on the product.',
}
