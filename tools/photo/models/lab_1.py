"""Lab pack, series 1: benchtop lab devices (centrifuges, mixers, stirrers,
balances, meters, baths, ovens, fridge).

Light grey or white housings with dark control panels. Shapes follow the 2D
drawings in tools/art/lab*.mjs; a few drawings share one builder with
different sizes (centrifuges, heating blocks, stirrers, ovens).
Units mm, product stands on z=0, front faces -Y.
"""


def dome_centrifuge(k, w, d, h, dome, hub):
    """Benchtop or microcentrifuge: box housing with a domed lid and a dark hub."""
    k.box((w, d, h), (0, 0, h / 2), 'light', bevel=6)                                  # housing
    k.sphere(1, (0, 0, h), 'light', scale=(w / 2, d / 2, dome))                        # domed lid (top half above)
    k.cyl(hub, 6, (0, 0, h + dome - 1), 'dark')                                        # rotor hub on top
    k.box((w * 0.5, 3, 16), (0, -d / 2 - 1, 22), 'dark', bevel=1)                      # control panel


def vortex(k):
    """Vortex mixer: compact box-shaped base, round black rubber cup on top, round speed knob on the front."""
    k.box((130, 160, 70), (0, 0, 35), 'light', bevel=10)                               # box base, rounded edges
    k.cyl(25, 12, (0, -30, 76), 'dark', bevel=2)                                       # round rubber cup near the front
    k.cyl(12, 8, (0, -81, 35), 'mid', rot=(90, 0, 0))                                  # speed knob on the front face



def timer(k):
    """Digital lab timer: flat upright housing on a fold-out stand, LCD window and a row of small buttons."""
    k.box((70, 40, 4), (0, 12, 2), 'dark', bevel=1)                                    # fold-out stand plate
    k.box((70, 20, 90), (0, 0, 51), 'light', bevel=4)                                  # flat housing, upright
    k.box((56, 1.5, 34), (0, -10.5, 68), 'mid', bevel=1)                               # large grey LCD window, upper half
    for x in (-20, 0, 20):
        k.box((12, 2, 8), (x, -10.5, 26), 'dark', bevel=1)                             # three small buttons: MIN, SEC, START/STOP



def heating_block(k, shaking=False):
    """Dry block for tubes. Plain: light housing, steel block on top, front panel.
    Shaking (thermomixer): low white housing, silver block with 24 tube holes, display and two knobs on the front."""
    if shaking:
        k.box((200, 260, 110), (0, 0, 55), 'light', bevel=6)                           # low white housing
        k.box((180, 200, 14), (0, 0, 117), 'steel', bevel=2, metal=0.3, rough=0.3)     # silver aluminium heating block
        for i in range(6):
            for j in range(4):
                k.cyl(7, 1, ((i - 2.5) * 28, (j - 1.5) * 40, 124.5), 'dark')          # 24 tube holes
        k.box((60, 2, 24), (-40, -131, 66), 'dark', bevel=1)                           # display on the sloped front
        for x in (35, 65):
            k.cyl(9, 10, (x, -132, 66), 'mid', rot=(90, 0, 0))                         # two knobs
        return
    k.box((200, 150, 50), (0, 0, 25), 'light', bevel=5)                                # housing
    k.box((190, 140, 14), (0, 0, 57), 'steel', bevel=2, metal=0.3, rough=0.3)         # block
    for i in range(6):
        for j in range(4):
            k.cyl(7, 0.6, ((i - 2.5) * 28, (j - 1.5) * 32, 64.2), 'dark')             # 24 wells: 6 across, 4 rows deep
    k.box((120, 4, 16), (0, -76, 30), 'dark', bevel=1)                                 # panel



def magnetic_stirrer(k, hotplate=True, vessel=False):
    """Magnetic stirrer: flat housing, dark ceramic top with a hotplate, or a beaker."""
    k.box((170, 150, 40), (0, 0, 20), 'light', bevel=5)                                # housing
    if hotplate:
        k.box((160, 140, 3), (0, 0, 41.5), 'dark', bevel=1)                            # ceramic top
    else:
        k.box((160, 140, 6), (0, 0, 43), 'steel', bevel=1, metal=0.3, rough=0.3)       # plain top plate
    for x in (-50, 50):
        k.cyl(9, 12, (x, -80, 25), 'dark', rot=(90, 0, 0))                             # knobs
    if vessel:
        k.cyl(50, 110, (0, 0, 98), 'glass', alpha=0.5, rough=0.1)                      # 1 l beaker


def overhead_stirrer(k):
    """Overhead stirrer on a stand: base, upright mast, arm, motor and a beaker below."""
    k.box((200, 200, 8), (0, 0, 4), 'dark', bevel=2)                                   # base
    k.box((16, 16, 312), (-100, 0, 164), 'dark')                                       # mast
    k.box((100, 14, 14), (-55, 0, 300), 'dark')                                        # arm
    k.box((30, 30, 22), (-100, 0, 300), 'mid', bevel=2)                                # clamp
    k.cyl(30, 70, (-10, 0, 265), 'light', bevel=2)                                     # motor
    k.cyl(28, 12, (-10, 0, 306), 'dark')                                               # motor cap
    k.cyl(60, 120, (-10, 0, 68), 'glass', alpha=0.5, rough=0.1)                        # beaker
    k.cyl(3, 190, (-10, 0, 135), 'steel', metal=1, rough=0.2)                          # shaft
    k.cyl(25, 4, (-10, 0, 40), 'steel', metal=1, rough=0.2)                            # impeller


def precision_balance(k):
    """Precision balance: wide low housing, a post and a round pan on top."""
    k.box((300, 230, 70), (0, 0, 35), 'light', bevel=5)                                # housing
    k.box((110, 4, 26), (-60, -117, 40), 'dark', bevel=1)                              # display
    k.box((50, 4, 26), (90, -117, 40), 'dark', bevel=1)                                # keys
    k.cyl(8, 40, (0, 0, 90), 'steel', metal=1)                                         # post
    k.cyl(95, 8, (0, 0, 114), 'steel', bevel=1, metal=1, rough=0.25)                   # pan


def analytical_balance(k):
    """Analytical balance: white base, tall glass draft shield with a slim grey frame, round pan inside."""
    k.box((240, 260, 50), (0, 0, 25), 'light', bevel=4)                                # base
    k.box((120, 3, 22), (-45, -131.5, 30), 'dark', bevel=1)                            # display
    for x in (-72, 72):
        for y in (-72, 72):
            k.box((6, 6, 260), (x, y, 180), 'mid')                                     # slim grey frame posts
    k.box((156, 156, 260), (0, 0, 180), 'glass', alpha=0.35, rough=0.1)                # glass walls and top of the draft shield
    for y in (-75, 75):
        k.box((156, 6, 6), (0, y, 310), 'mid')                                         # top frame bars
    k.cyl(45, 3, (0, 0, 53.5), 'steel', metal=1, rough=0.25)                           # round stainless pan



def lab_balance(k):
    """Lab balance: low housing, short post and a wide flat pan."""
    k.box((220, 200, 50), (0, 0, 25), 'light', bevel=5)                                # housing
    k.box((70, 4, 18), (-45, -102, 30), 'dark', bevel=1)                               # display
    k.cyl(12, 12, (0, 0, 56), 'dark')                                                  # post
    k.cyl(88, 8, (0, 0, 66), 'steel', bevel=1, metal=1, rough=0.25)                    # pan


def ph_meter(k):
    """Benchtop pH meter: sloped housing with display and keys, a rod on its side with an electrode arm,
    and a slim electrode hanging into a glass beaker beside the meter."""
    k.box((150, 110, 40), (0, 0, 20), 'light', bevel=4)                                # housing
    k.box((120, 70, 4), (0, -12, 44), 'dark', bevel=1, rot=(-15, 0, 0))                # sloped display and keypad panel
    for x in (-40, -13, 13, 40):
        k.box((14, 8, 2), (x, -22, 47), 'mid', bevel=0.5, rot=(-15, 0, 0))             # keys on the slope
    k.box((30, 40, 6), (88, 0, 3), 'dark', bevel=1)                                    # rod foot
    k.cyl(5, 200, (88, 0, 106), 'steel', metal=1, rough=0.25)                          # vertical rod on the side
    k.cyl(4, 100, (88, -47, 170), 'steel', metal=1, rough=0.25, rot=(90, 0, 0))        # horizontal electrode arm
    k.cyl(35, 90, (88, -95, 45), 'glass', alpha=0.3, rough=0.1)                        # glass beaker beside the meter
    k.cyl(4, 120, (88, -95, 110), 'glass', alpha=0.6, rough=0.1)                       # slim electrode, glass body
    k.cyl(6, 16, (88, -95, 172), 'dark', bevel=1)                                      # black electrode cap



def diaphragm_pump(k):
    """Compact diaphragm vacuum pump: a rectangular light grey motor housing on a low base frame, a dark
    pump head at its front end with two steel hose barbs pointing forward (inlet and exhaust), and a
    carrying handle on top. No cylinder, no end disc."""
    k.box((200, 100, 8), (0, 0, 4), 'dark', bevel=2)                                   # low base frame
    k.box((130, 100, 70), (-20, 0, 43), 'light', bevel=8)                              # motor housing, rounded box
    k.box((34, 80, 50), (62, 0, 43), 'dark', bevel=4)                                  # pump head at the front
    for y in (-20, 20):
        k.cyl(4.5, 22, (90, y, 43), 'steel', rot=(0, 90, 0))                           # hose barb pointing forward
    k.box((100, 10, 8), (-25, 0, 95), 'dark', bevel=2)                                 # carrying handle bar
    for x in (-70, 20):
        k.box((8, 10, 22), (x, 0, 84), 'dark', bevel=1)                                # handle posts



def ultrasonic_bath(k):
    """Ultrasonic bath: light housing with a stainless steel tank set into its top, water inside,
    a front control panel with display, timer knob and heater switch, and a steel drain valve."""
    k.box((300, 200, 50), (0, 0, 25), 'light', bevel=5)                                # housing
    k.box((260, 6, 40), (0, -97, 70), 'steel', bevel=1, metal=1, rough=0.25)           # tank walls, open top
    k.box((260, 6, 40), (0, 97, 70), 'steel', bevel=1, metal=1, rough=0.25)
    k.box((6, 188, 40), (-127, 0, 70), 'steel', bevel=1, metal=1, rough=0.25)
    k.box((6, 188, 40), (127, 0, 70), 'steel', bevel=1, metal=1, rough=0.25)
    k.box((248, 188, 4), (0, 0, 52), 'steel', metal=1, rough=0.25)                     # tank floor
    k.box((248, 188, 30), (0, 0, 67), 'glass', alpha=0.5, rough=0.1)                   # water in the tank
    k.box((110, 3, 36), (-50, -101.5, 30), 'dark', bevel=1)                            # control panel
    k.box((40, 2, 14), (-70, -103, 36), 'mid', bevel=1)                                # small display
    k.cyl(7, 10, (0, -104, 30), 'dark', rot=(90, 0, 0))                                # timer knob
    k.box((12, 2, 8), (30, -103, 24), 'dark', bevel=1)                                 # heater switch
    k.cyl(5, 10, (110, -101, 12), 'steel', metal=1, rot=(90, 0, 0))                    # drain valve


def drying_oven(k, w=410, d=360, h=560):
    """Drying oven: tall light cabinet with a glass door window and a small panel."""
    k.box((w, d, h), (0, 0, h / 2), 'light', bevel=8)                                  # cabinet
    k.box((330, 3, 320), (0, -d / 2 - 1, 300), 'glass', alpha=0.5, rough=0.1)          # door window
    k.box((150, 3, 30), (-90, -d / 2 - 1, h - 70), 'dark', bevel=1)                    # panel


def vacuum_oven(k):
    """Vacuum drying oven: square light cabinet, round window, hose out the right side."""
    k.box((300, 260, 300), (0, 0, 150), 'light', bevel=6)                              # cabinet
    k.cyl(70, 3, (-20, -131.5, 160), 'glass', alpha=0.5, rot=(90, 0, 0), rough=0.1)    # round window
    k.box((80, 3, 22), (-60, -131.5, 50), 'dark', bevel=1)                             # panel
    k.cyl(6, 70, (160, 0, 120), 'dark', rot=(0, 90, 0))                                # vacuum hose


def orbital_shaker(k):
    """Orbital shaker: square base with a sloped front panel, a square rubber-mat platform and two clamping bars."""
    k.box((260, 260, 60), (0, 0, 30), 'dark', bevel=6)                                 # square base
    k.box((260, 30, 8), (0, -125, 50), 'light', bevel=1, rot=(-20, 0, 0))              # sloped front panel, flush with the base front
    k.box((80, 2, 22), (-60, -131, 36), 'mid', bevel=1)                                # display
    k.cyl(8, 10, (70, -121, 40), 'mid', rot=(90, 0, 0))                                # knob
    k.box((300, 300, 10), (0, 0, 65), 'light', bevel=2)                                # rectangular platform
    k.box((280, 280, 2), (0, 0, 71), 'dark', bevel=1)                                  # black rubber mat
    for x in (-135, 135):
        k.box((10, 280, 10), (x, 0, 77), 'mid', bevel=1)                               # clamping bars along the edges



def thermometer(k):
    """Digital probe thermometer standing on its handle: a short plastic stem and a sharp steel probe."""
    k.box((46, 34, 70), (0, 0, 35), 'light', bevel=4)                                  # handle
    k.box((30, 2, 20), (0, -18, 45), 'dark', bevel=1)                                  # display
    k.cyl(6, 40, (0, 0, 90), 'white', metal=0, rough=0.4)                              # plastic stem collar
    k.cyl(2.5, 70, (0, 0, 145), 'steel', metal=1, rough=0.25)                          # steel probe
    k.cyl(2.5, 10, (0, 0, 215), 'steel', r2=0.4, metal=1, rough=0.25)                  # sharp tip


def water_bath(k, lid=True):
    """Water bath: open stainless steel tank set into a white housing, water inside,
    a flat lid lying beside it, and a front control panel with a display and a knob."""
    k.box((280, 220, 110), (0, 0, 55), 'white', bevel=5)                               # white housing
    k.box((240, 6, 40), (0, -87, 130), 'steel', bevel=1)                               # tank walls, open top
    k.box((240, 6, 40), (0, 87, 130), 'steel', bevel=1)
    k.box((6, 180, 40), (-117, 0, 130), 'steel', bevel=1)
    k.box((6, 180, 40), (117, 0, 130), 'steel', bevel=1)
    k.box((228, 168, 34), (0, 0, 120), 'glass', alpha=0.5, rough=0.1)                  # water in the tank
    k.box((110, 3, 36), (-50, -111.5, 75), 'dark', bevel=1)                            # front control panel
    k.box((40, 2, 14), (-50, -113, 80), 'mid', bevel=1)                                # display
    k.cyl(9, 10, (40, -116, 72), 'dark', rot=(90, 0, 0), bevel=1)                      # control knob
    if lid:
        k.box((150, 200, 8), (-265, 0, 4), 'mid', bevel=2)                             # flat lid lying beside the tank
        k.box((16, 16, 8), (-265, 0, 12), 'dark', bevel=2)                             # lid handle


def fridge(k):
    """Laboratory fridge: tall white cabinet, split doors and two handles."""
    k.box((460, 470, 820), (0, 0, 410), 'white', bevel=10)                             # cabinet
    k.box((456, 4, 4), (0, -236, 430), 'mid')                                          # door seam
    k.box((14, 16, 140), (170, -243, 650), 'mid', bevel=2)                             # upper handle
    k.box((14, 16, 140), (170, -243, 300), 'mid', bevel=2)                             # lower handle


SKUS = {
    'DEMO-LAB-1001': (dome_centrifuge, dict(w=210, d=230, h=120, dome=50, hub=38)),
    'DEMO-LAB-1002': (dome_centrifuge, dict(w=340, d=340, h=200, dome=70, hub=60)),
    'DEMO-LAB-1003': (vortex, {}),
    'DEMO-LAB-1004': (timer, {}),
    'DEMO-LAB-1005': (heating_block, {'shaking': False}),
    'DEMO-LAB-1006': (heating_block, {'shaking': True}),
    'DEMO-LAB-1007': (magnetic_stirrer, {'hotplate': True}),
    'DEMO-LAB-1008': (overhead_stirrer, {}),
    'DEMO-LAB-1009': (precision_balance, {}),
    'DEMO-LAB-1010': (analytical_balance, {}),
    'DEMO-LAB-1011': (lab_balance, {}),
    'DEMO-LAB-1012': (ph_meter, {}),
    'DEMO-LAB-1013': (diaphragm_pump, {}),
    'DEMO-LAB-1014': (ultrasonic_bath, {}),
    'DEMO-LAB-1015': (drying_oven, {}),
    'DEMO-LAB-1016': (orbital_shaker, {}),
    'DEMO-LAB-1017': (thermometer, {}),
    'DEMO-LAB-1018': (dome_centrifuge, dict(w=150, d=150, h=70, dome=40, hub=26)),
    'DEMO-LAB-1019': (magnetic_stirrer, {'hotplate': False, 'vessel': True}),
    'DEMO-LAB-1020': (water_bath, {'lid': True}),
    'DEMO-LAB-1021': (vacuum_oven, {}),
    'DEMO-LAB-1022': (fridge, {}),
}

HINTS = {
    'DEMO-LAB-1001': 'A benchtop microcentrifuge: a light grey box-shaped housing with a low domed lid on top, a small dark rotor hub at its centre and a dark control panel on the front. Not a vortex mixer and not a balance.',
    'DEMO-LAB-1002': 'A benchtop centrifuge: a large light grey box-shaped housing, wider than a microcentrifuge, with a big round domed lid taking most of the top, a dark rotor hub in its centre and a dark control panel on the front. Not a small microcentrifuge.',
    'DEMO-LAB-1003': 'A vortex mixer: a compact box-shaped light grey base with rounded edges, a round black rubber cup on top near the front edge, and a round grey speed knob on the front face. The housing is plain and unmarked: no wordmark, no logo, no pictogram, no panel print. Not a mushroom, not a lamp, not a centrifuge. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1004': 'A small digital countdown timer on a bench: a light grey upright housing on a dark fold-out stand plate, a large grey LCD window in its upper half showing the countdown 05:30 (seconds always below 60), and three small dark rectangular buttons below it with no printed labels. Not a thermometer, not a temperature controller, not a round dial. No text, no numbers, no logos, no labels anywhere on the product except the countdown on the LCD.',
    'DEMO-LAB-1005': 'A dry heating block: a rigid light grey rectangular housing with a flat steel block on top carrying exactly 24 large round wells in a 6 by 4 grid (6 across, 4 rows deep), each well a dark round hole sized for 1.5 or 2.0 ml tubes, and a dark control panel strip on the front. Count the wells: exactly 24, no more, no fewer. Not a heating pad or mat, not a water bath, no lid. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1006': 'A thermomixer: a low white rectangular housing with a flat silver aluminium heating block on top carrying exactly 24 large round tube holes in a 6 by 4 grid (6 across, 4 rows deep), a dark display window and two plain knobs with no markings on the sloped front. Count the holes: exactly 24, no more. Not a plain dry block without a display, not a water bath. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1007': 'A magnetic stirrer with a hotplate: a flat light grey housing with a flat dark ceramic top plate and two round dark knobs on the front edge. The top is empty, with no beaker. Not an overhead stirrer and not a balance.',
    'DEMO-LAB-1008': 'An overhead stirrer on a stand: a black flat base, a tall vertical mast with an arm, a light grey motor housing at the end of the arm and a thin steel shaft with a small steel impeller running down into a plain clear glass beaker with no graduation marks and no printing. Not a magnetic stirrer, which is a flat box. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1009': 'A precision balance: a wide, low light grey housing with a small dark display and keys on the front, and a round stainless steel weighing pan on a short post on top. Open pan, no glass case. Not an analytical balance.',
    'DEMO-LAB-1010': 'An analytical balance: a white base with a small dark display panel on its front, and a tall rectangular glass draft shield on top with slim grey frame posts, glass walls on all sides and on top, and a round stainless weighing pan inside. No black disc on top. Not a precision balance with an open pan. No labels or printing.',
    'DEMO-LAB-1011': 'A 500 g lab balance: a low light grey housing with a small dark display window on the front and a wide flat round steel pan on a short dark post, open to the air. The housing is plain, with no lettering or marking anywhere, including above the display. Not a precision balance with a tall post. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1012': 'A benchtop pH meter: a light grey housing with a sloped dark display and keypad on its top, a vertical steel rod on its right side carrying a horizontal electrode arm, a slim electrode with a black cap and a glass body hanging from the arm into a small glass beaker standing next to the meter on the bench. Not a balance. No labels or printing.',
    'DEMO-LAB-1013': 'A compact diaphragm vacuum pump: a light grey rectangular motor housing with rounded edges on a low dark base plate, at its front end a dark pump head with two short steel hose barbs pointing forward (one for vacuum inlet, one for exhaust), and a dark carrying handle on top. Not a centrifuge, not a hand compressor, not a bellows. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1014': 'An ultrasonic cleaning bath: a light grey rectangular housing with a stainless steel tank set into its top, the tank filled with pale water, a dark control panel on the front with a small display, a timer knob and a heater switch, and a small steel drain valve at the lower front. Not a water bath with a white housing and a lid. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1015': 'A laboratory drying oven: white box-shaped steel cabinet with one large flat front door with a rectangular window and a vertical handle, a dark control panel strip above the door with plain buttons and a small LCD. The cabinet is plain, with no wordmark and no logo anywhere. Not a washing machine, not a kitchen oven. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1016': 'An orbital shaker: a square dark base with a sloped light grey front panel carrying a small display and a knob, and a square light grey platform on top, about 300 by 300, covered with a black rubber mat, with two clamping bars along the edges. Not round, not a vortex mixer. No labels or printing.',
    'DEMO-LAB-1017': 'A handheld digital probe thermometer: a light grey handle with a small display, a short white plastic stem, and a thin stainless steel probe about 7 cm long ending in a sharp point, standing upright. Not a long rod, not a pen.',
    'DEMO-LAB-1018': 'A mini centrifuge: a small light grey box with a low domed lid, a small dark rotor hub on top and a dark control panel on the front. Smaller than a microcentrifuge. Not a vortex mixer.',
    'DEMO-LAB-1019': 'A magnetic stirrer without heating: a flat plain light grey box with a round steel top plate, a speed knob and an on/off switch on the front, and a 1 l plain glass beaker on the plate with a steel stir bar inside. No socket on the housing; the mains cable leaves the back edge. The plug end is out of frame. Not a hotplate, not a two-slot outlet. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1020': 'A laboratory water bath: an open rectangular stainless steel tank filled with water, set into a white rectangular housing, with the water surface visible from above. A flat lid lies beside the tank. A control panel with a small display and a round knob sits on the front of the housing. Not a closed cabinet, no side windows. No labels or printing.',
    'DEMO-LAB-1021': 'A square light grey vacuum drying oven: a boxy cabinet with a round glass window on the front, a small dark control panel below the window with only a simple power symbol and no lettering, a thick hose out of the right side, and a plain white side with no sticker or label. Not a drying oven with a rectangular door. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-LAB-1022': 'A tall white laboratory refrigerator: a single white cabinet with a thin seam across the front, two vertical grey handles on the right side at the top and the middle, and nothing on the top. The whole device visible, standing out clearly from the white background with a soft shadow. Not a freezer.',
}
