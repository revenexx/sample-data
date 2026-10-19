"""Industrial pack, series 6: workshop equipment (DEMO-BRAKKWERK).

Burgundy (#7A1F2B) and anthracite (#2F343C) painted steel for the maker's
frames, cases and stands; grey steel for the vise screw and wheel hubs; black
rubber castors and wheels. Units mm; products stand on z=0 with the front
facing -Y. No lettering. The LED work light has a European earthed plug.
"""

BURG = '#7A1F2B'
ANTH = '#2F343C'
ANTH_LIGHT = '#4A515C'
STEEL = '#A7AEB8'
GREY = '#7B838F'
RUBBER = '#1E2024'
WHITE = '#F7F7F5'
FLAT = {'pitch': 50, 'fill': 0.8}


def workbench(k):
    """Workbench 1500 x 750 x 900: anthracite work top and lower shelf on four burgundy legs."""
    k.box((1500, 750, 40), (0, 0, 880), ANTH, bevel=3, rough=0.4)                      # work top
    k.box((1440, 700, 25), (0, 0, 160), ANTH, bevel=2, rough=0.5)                      # lower shelf
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.box((50, 50, 860), (sx * 700, sy * 325, 430), BURG, bevel=2, rough=0.4)  # legs
    k.box((1500, 40, 60), (0, -340, 820), BURG, bevel=2, rough=0.4)                    # front apron


def bench_vise(k):
    """Bench vise 125 mm: round swivel base, anthracite body with a fixed jaw, burgundy T-handle screw."""
    k.cyl(75, 14, (0, 0, 7), GREY, verts=64, metal=0.6, rough=0.4)                     # swivel base
    k.box((140, 95, 60), (0, 0, 44), ANTH, bevel=4, rough=0.4)                         # body
    k.box((125, 26, 72), (0, 45, 58), ANTH_LIGHT, bevel=2, rough=0.5)                  # fixed jaw, at the back
    k.box((125, 26, 72), (0, -45, 58), ANTH_LIGHT, bevel=2, rough=0.5)                 # movable jaw, at the front
    k.cyl(10, 168, (0, -26, 60), STEEL, rot=(90, 0, 0), metal=0.8, rough=0.3)           # screw along Y, from the fixed jaw to the T-handle
    k.cyl(7, 130, (0, -110, 60), BURG, rot=(0, 90, 0), rough=0.4)                      # T-handle across the front end
    for sx in (-1, 1):
        k.sphere(11, (sx * 65, -110, 60), BURG, rough=0.4)                             # handle grips


def workshop_trolley(k):
    """Workshop trolley 900 x 450 x 920: three anthracite shelves in a burgundy frame, four castors."""
    for z in (150, 450, 750):
        k.box((880, 430, 18), (0, 0, z), ANTH, bevel=2, rough=0.5)                    # shelves
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.box((30, 30, 895), (sx * 430, sy * 205, 472), BURG, bevel=2, rough=0.4)  # uprights
            k.cyl(30, 25, (sx * 420, sy * 190, 12.5), RUBBER, verts=48, rough=0.8)     # castors
    k.box((900, 25, 25), (0, 205, 920), BURG, bevel=3, rough=0.4)                      # top handle bar


def extraction_unit(k):
    """Mobile extraction unit, 50 litre: tall anthracite tank on four castors, burgundy motor cap, side hose inlet."""
    k.cyl(190, 560, (0, 0, 360), ANTH, verts=64, bevel=3, rough=0.35)                 # tank, z 80..640
    k.cyl(195, 30, (0, 0, 655), BURG, verts=64, bevel=2, rough=0.4)                    # lid
    k.box((240, 200, 120), (0, -10, 730), BURG, bevel=8, rough=0.4)                    # motor housing
    k.cyl(42, 90, (0, -220, 360), ANTH_LIGHT, rot=(90, 0, 0), verts=40, rough=0.5)     # hose inlet
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.cyl(30, 80, (sx * 130, sy * 130, 40), RUBBER, verts=40, rough=0.8)       # castors


def air_compressor(k):
    """Oil-free air compressor 24 litre: horizontal anthracite receiver on two feet, burgundy pump block, pressure gauge."""
    k.cyl(115, 520, (0, 0, 200), ANTH, rot=(0, 90, 0), verts=64, bevel=3, rough=0.35)  # receiver
    for sx in (-1, 1):
        k.box((40, 320, 85), (sx * 180, 0, 42.5), RUBBER, bevel=3, rough=0.7)          # feet
    k.box((220, 170, 150), (-70, 0, 390), BURG, bevel=10, rough=0.4)                   # pump block
    k.cyl(22, 12, (150, -106, 260), WHITE, rot=(90, 0, 0), verts=40, rough=0.2)        # pressure gauge
    k.cyl(12, 50, (285, 0, 200), GREY, rot=(0, 90, 0), verts=32, metal=0.6, rough=0.4)  # outlet, out through the end cap


def sack_truck(k):
    """Sack truck 200 kg: anthracite steel frame with two large black rubber wheels, flat nose plate, burgundy grips."""
    k.box((380, 240, 12), (0, -20, 25), GREY, bevel=2, metal=0.5, rough=0.4)           # nose plate
    for sx in (-1, 1):
        k.box((28, 28, 1080), (sx * 170, 60, 560), ANTH, bevel=2, rough=0.4)           # frame rails
        k.cyl(130, 40, (sx * 200, 60, 130), RUBBER, rot=(0, 90, 0), verts=64, rough=0.8)  # wheels
        k.cyl(40, 44, (sx * 200, 60, 130), ANTH_LIGHT, rot=(0, 90, 0), verts=40, rough=0.4)  # hubs
    k.cyl(10, 420, (0, 60, 130), STEEL, rot=(0, 90, 0), metal=0.8, rough=0.3)          # axle
    k.cyl(24, 380, (0, 40, 1100), BURG, rot=(0, 90, 0), verts=40, rough=0.5)           # grip bar across the two rails
    for sx in (-1, 1):
        k.cyl(26, 70, (sx * 170, 60, 1080), BURG, verts=40, rough=0.5)                  # grip sleeve on each rail, two handles


def storage_shelf(k):
    """Steel storage shelf 900 x 400 x 1800: four anthracite bays, burgundy uprights."""
    for z in (60, 520, 980, 1440):
        k.box((900, 400, 20), (0, 0, z), ANTH, bevel=2, rough=0.5)                     # shelves
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.box((30, 30, 1800), (sx * 435, sy * 185, 900), BURG, bevel=2, rough=0.4)  # uprights
            k.box((40, 40, 10), (sx * 435, sy * 185, 5), RUBBER, bevel=2, rough=0.8)   # feet


def assortment_box(k):
    """Plastic assortment box with three removable compartments: anthracite case, burgundy inserts."""
    k.box((330, 240, 40), (0, 0, 20), ANTH, bevel=4, rough=0.5)                        # case base
    for x in (-105, 0, 105):
        k.box((100, 220, 80), (x, 0, 80), BURG, bevel=3, rough=0.5)                    # compartment inserts


def work_light(k):
    """LED work light 20 W: anthracite rectangular head with a white LED panel, on a tripod base and a stand pole, cable with European earthed plug."""
    k.cyl(120, 12, (0, 0, 6), ANTH, verts=64, bevel=2, rough=0.5)                     # base disc
    k.cyl(12, 1400, (0, 0, 712), ANTH_LIGHT, verts=32, rough=0.4)                      # pole
    k.box((280, 70, 170), (0, 0, 1480), ANTH, bevel=8, rough=0.45)                     # head
    k.box((250, 6, 150), (0, -36, 1480), WHITE, bevel=2, rough=0.2)                    # LED panel
    k.cyl(4, 800, (520, 0, 6), RUBBER, rot=(0, 90, 0), verts=24, rough=0.9)            # cable
    k.box((48, 22, 40), (944, 0, 20), WHITE, bevel=3, rough=0.4)                       # plug body
    for py in (-9.5, 9.5):
        k.cyl(4.0, 19, (977.5, py, 20), '#C9CDD2', rot=(0, 90, 0), verts=24, metal=0.8, rough=0.3)  # two round Schuko pins
    for py in (-12.5, 12.5):
        k.box((20, 3, 14), (944, py, 20), '#C9CDD2', metal=0.8, rough=0.3)                  # earth clips on the sides


def air_hose(k):
    """Compressed air hose 10 m: burgundy hose coiled flat on the floor, with a quick coupling at one end."""
    for i, (dx, dy) in enumerate(((0, 0), (25, -15), (-15, 20))):
        k.torus(220, 9, (dx, dy, 9 + 18 * i), BURG, rough=0.7)                         # coils
    k.cyl(12, 42, (-250, 0, 9), ANTH, rot=(0, 90, 0), verts=40, metal=0.6, rough=0.4)  # quick coupling


def assembly_stand(k):
    """Height-adjustable assembly stand: anthracite work surface on four burgundy steel legs, lower shelf, side crank."""
    k.box((900, 600, 30), (0, 0, 905), ANTH, bevel=3, rough=0.4)                       # work surface
    k.box((800, 500, 15), (0, 0, 200), ANTH_LIGHT, bevel=2, rough=0.5)                 # lower shelf
    for sx in (-1, 1):
        for sy in (-1, 1):
            k.box((40, 40, 890), (sx * 420, sy * 270, 445), BURG, bevel=2, rough=0.4)  # legs
    k.cyl(8, 120, (460, 0, 500), STEEL, rot=(90, 0, 0), metal=0.8, rough=0.3)          # crank
    k.sphere(14, (460, -60, 500), BURG, rough=0.4)                                     # crank knob


def drip_tray(k):
    """Oil drip tray 20 litre: shallow burgundy plastic tray with a raised rim and a dark recessed well."""
    k.box((520, 400, 80), (0, 0, 40), BURG, bevel=8, rough=0.55)                       # tray body
    k.box((470, 350, 2), (0, 0, 81), RUBBER, bevel=0.5, rough=0.6)                     # recessed well


SKUS = {
    'DEMO-IND-6001': (workbench, {}, {'fill': 0.7}),
    'DEMO-IND-6002': (bench_vise, {}),
    'DEMO-IND-6003': (workshop_trolley, {}),
    'DEMO-IND-6004': (extraction_unit, {}),
    'DEMO-IND-6005': (air_compressor, {}),
    'DEMO-IND-6006': (sack_truck, {}),
    'DEMO-IND-6007': (storage_shelf, {}),
    'DEMO-IND-6008': (assortment_box, {}, {'pitch': 35, 'fill': 0.75}),
    'DEMO-IND-6009': (work_light, {}),
    'DEMO-IND-6010': (air_hose, {}, FLAT),
    'DEMO-IND-6011': (assembly_stand, {}),
    'DEMO-IND-6012': (drip_tray, {}, {'pitch': 35, 'fill': 0.78}),
}

HINTS = {
    'DEMO-IND-6001': 'A heavy workbench with a thick anthracite steel work top and a lower anthracite shelf, standing on four burgundy painted steel legs with a burgundy front apron. Not a table: the frame is sturdy welded steel with a flat, rectangular top.',
    'DEMO-IND-6002': 'A bench vise with a round grey steel swivel base, an anthracite cast body, a fixed jaw at the back and a movable jaw at the front, both flat and anthracite. A steel screw runs along the middle from the fixed jaw to the front, with a burgundy T-handle across its front end and two burgundy grips. Not a clamp: it is a bench vise with two jaws and a screw. No logo, no printed text.',
    'DEMO-IND-6003': 'A mobile workshop trolley with three flat anthracite steel shelves in a burgundy painted frame, a burgundy bar across the top and four black rubber castors. Not a shopping cart: the shelves are solid steel plate and the frame is a rigid rectangle.',
    'DEMO-IND-6004': 'A mobile dust extraction unit: a tall anthracite steel tank on four black castors, a burgundy motor housing and lid on top, and a short anthracite hose inlet on the front side. Not a vacuum cleaner: it is an upright drum on wheels with a squared motor box.',
    'DEMO-IND-6005': 'A small horizontal air compressor: a long anthracite steel receiver tank lying on two black rubber feet, a burgundy pump block on top, a round white pressure gauge on the front and a grey outlet fitting through the end cap. Not a gas cylinder: the tank is wide and flat-ended with a visible pump housing.',
    'DEMO-IND-6006': 'A two-wheeled sack truck: an upright anthracite steel frame with two large black rubber wheels at the bottom, a flat grey steel nose plate at floor level and a burgundy grip bar across the top and a burgundy grip sleeve on each rail, two handles. Not a trolley with four castors: it is tilted back on two big wheels.',
    'DEMO-IND-6007': 'A tall steel storage shelf with four anthracite shelves dividing four open bays, and burgundy upright posts at the corners with small black feet. Not a cabinet: it is open, with no doors and no sides.',
    'DEMO-IND-6008': 'A plastic assortment box: an open anthracite plastic case holding three burgundy compartment inserts side by side, all with flat tops. Not a toolbox: there is no lid and no handle, just the three removable compartments.',
    'DEMO-IND-6009': 'A portable LED work light: a rectangular anthracite head with a bright white LED panel facing forward, on a slim anthracite pole standing on a round tripod-style base, with a black cable running from the base to a European Schuko plug at the end: a white plug body with two round metal pins and two earth clips on the sides. Not a flashlight and not a lamp shade. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-IND-6010': 'A compressed air hose coiled loosely on the floor, several rings of dark burgundy rubber hose lying flat, with a dark anthracite quick coupling fitting at one end. Not a garden hose: it is a stiff industrial air hose with a metal coupling.',
    'DEMO-IND-6011': 'A height-adjustable assembly stand: a flat anthracite steel work surface on four burgundy steel legs, with a lower anthracite shelf between the legs and a short steel crank with a burgundy knob at one side. Not a bench with a drawer: it is an open steel frame.',
    'DEMO-IND-6012': 'A shallow oil drip tray: a low burgundy plastic tray with a raised rim and a dark recessed well inside, standing flat on the floor. Not a bucket or a basin: it is a wide, flat tray with no handles and no lid.',
}
