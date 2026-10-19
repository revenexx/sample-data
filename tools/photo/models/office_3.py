"""Office pack, series 3: coffee, tea, paper goods, soap and water.

Plain, unprinted packaging in realistic colours. Packs and bags are boxes with
rounded edges, cups are cones, bottles are cylinders. Same-model products share
a builder call; colour and size variants pass their own arguments.
"""

COFFEE = {'medium': '#8A5A34', 'dark': '#2B1D15'}
TEA = {'black': '#E6DCCB', 'peppermint': '#7FB58A', 'fruit': '#C9574A'}


def bean_bag(k, colour='#8A5A34'):
    """Upright 1 kg coffee bean pouch: soft box with a sealed top strip."""
    k.box((150, 70, 220), (0, 0, 110), colour, bevel=8, rough=0.55)                      # pouch body
    k.box((154, 74, 16), (0, 0, 222), 'dark', bevel=3, rough=0.5)                        # top seal
    k.cyl(9, 4, (0, -36, 150), '#2F343C', rot=(90, 0, 0))                                 # valve


def coffee_brick(k, colour='#8A5A34'):
    """Vacuum-sealed brick of ground coffee, upright, rounded edges."""
    k.box((120, 75, 190), (0, 0, 95), colour, bevel=14, rough=0.5)
    k.box((90, 4, 12), (0, -37.5, 175), 'dark', bevel=2)                                  # seal crimp


def towel_carton(k):
    """Kraft carton of paper towel packs, a few white packs stacked on top."""
    k.box((320, 220, 190), (0, 0, 95), '#C9B48F', bevel=4, rough=0.7)                    # carton
    for x in (-100, 0, 100):
        k.box((96, 190, 30), (x, 0, 205), '#F7F7F5', bevel=3, rough=0.6)                 # towel packs


def soap_canister(k):
    """Plain pale plastic refill canister with a white screw cap."""
    k.box((150, 100, 210), (0, 0, 105), '#DDE6E2', bevel=14, rough=0.4)                  # flat-sided refill bottle
    k.cyl(16, 22, (0, 0, 221), '#F4F4F2', verts=32)                                       # neck collar
    k.cyl(6, 14, (0, 0, 233), '#F4F4F2', verts=24)                                        # pump stem
    k.box((50, 22, 12), (-8, 0, 244), '#F4F4F2', bevel=3)                                 # pump head


def sugar_sack(k):
    """1 kg paper sugar sack, white, with a folded top."""
    k.box((150, 55, 230), (0, 0, 115), '#F2F2EF', bevel=8, rough=0.7)                    # sack
    k.box((152, 57, 14), (0, 0, 237), '#E4E4E0', bevel=3, rough=0.7)                     # folded top


def paper_cups(k, bottom=28, top=39, height=80):
    """Three plain white paper cups, two in front and one behind."""
    for x, y in ((-top - 6, -6), (top + 6, -6), (0, 26)):
        k.cyl(bottom, height, (x, y, height / 2), '#F7F7F5', r2=top, rough=0.6)            # cup
        k.torus(top, 1.2, (x, y, height), '#F7F7F5')                                       # rim


def stirrer_bag(k):
    """Paper bag of untreated wooden stirrers, sticks poking out of the top."""
    k.box((110, 30, 170), (0, 0, 85), '#D6C3A0', bevel=3, rough=0.7)                     # bag
    for i in range(7):
        k.cyl(2.5, 110, (-39 + 13 * i, 0, 215), '#C8A06A', rot=(0, 4 * (i - 3), 0), rough=0.6)


def water_pack(k):
    """Six clear 1.5 l bottles, two rows of three, white caps."""
    for x in (-90, 0, 90):
        for y in (-48, 48):
            k.cyl(42, 280, (x, y, 140), '#CFE3F0', alpha=0.45, verts=40, rough=0.1)      # bottle
            k.cyl(14, 24, (x, y, 292), '#F4F4F2', verts=32)                               # cap


def filter_pack(k):
    """Flat paper pack of coffee filters, off-white, with a flap at the top."""
    k.box((120, 28, 165), (0, 0, 82.5), '#EFEBE2', bevel=4, rough=0.7)                   # pack
    k.box((122, 30, 12), (0, 0, 166), '#E2DBCB', bevel=2, rough=0.7)                     # top flap


def tea_box(k, colour='#E6DCCB', size=(100, 60, 130)):
    """Plain cardboard tea box, upright."""
    w, d, h = size
    k.box((w, d, h), (0, 0, h / 2), colour, bevel=3, rough=0.7)


SKUS = {
    'DEMO-OFF-3001': (bean_bag, {'colour': COFFEE['medium']}),
    'DEMO-OFF-3004': (bean_bag, {'colour': COFFEE['dark']}),
    'DEMO-OFF-3005': (coffee_brick, {'colour': COFFEE['medium']}),
    'DEMO-OFF-3002': (towel_carton, {}),
    'DEMO-OFF-3003': (soap_canister, {}),
    'DEMO-OFF-3008': (sugar_sack, {}),
    'DEMO-OFF-3009': (paper_cups, {'bottom': 28, 'top': 39, 'height': 80}),
    'DEMO-OFF-3010': (paper_cups, {'bottom': 33, 'top': 46, 'height': 100}),
    'DEMO-OFF-3011': (stirrer_bag, {}),
    'DEMO-OFF-3012': (water_pack, {}, {'pitch': 38, 'yaw': -35}),
    'DEMO-OFF-3013': (filter_pack, {}),
    'DEMO-OFF-3006': (tea_box, {'colour': TEA['black'], 'size': (100, 60, 130)}),
    'DEMO-OFF-3007': (tea_box, {'colour': TEA['peppermint'], 'size': (80, 50, 95)}),
    'DEMO-OFF-3014': (tea_box, {'colour': TEA['fruit'], 'size': (80, 50, 95)}),
}

HINTS = {
    'DEMO-OFF-3001': 'A 1 kg coffee bean pouch standing upright: a matte medium-brown foil bag with a darker sealed top strip and a small round valve on the front. Plain and unprinted, not a glass jar and not a tin.',
    'DEMO-OFF-3004': 'A 1 kg coffee bean pouch standing upright, the same shape as a bean bag but very dark brown, almost black-brown, with a darker sealed top strip. Plain and unprinted, not a glass jar and not a tin.',
    'DEMO-OFF-3005': 'A rectangular vacuum-sealed brick of ground coffee, medium-brown matte packaging with rounded edges and a crimped seal along the top, standing upright. Not a jar, not a bean bag, not a tea box.',
    'DEMO-OFF-3002': 'A kraft-brown cardboard carton of paper towel packs, with a few plain white towel packs stacked on top. Not a roll of towels and not a wall dispenser.',
    'DEMO-OFF-3003': 'A plain pale grey-green refill bottle for a wall dispenser, about 5 litres: a flat-sided plastic bottle with a white pump head on a short neck on top. Unlabelled. Not a jerrycan, no carry handle, not a paper bag. The whole product visible, standing out clearly from the white background with a soft shadow. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-3008': 'A white paper sugar sack, 1 kg, standing upright with a folded top, soft paper texture. Plain and unprinted, not a bag of sweetener and not a sugar cube box. The whole product visible, standing out clearly from the white background with a soft shadow.',
    'DEMO-OFF-3009': 'Three plain white paper cups of 200 ml, two in front and one behind, straight tapered sides with a thin rim and no lids. Not a glass and not a mug. The whole product visible, standing out clearly from the white background with a soft shadow.',
    'DEMO-OFF-3010': 'Three plain white paper cups of 300 ml, taller than a small cup, two in front and one behind, tapered sides with a thin rim and no lids. Not a glass and not a mug. The whole product visible, standing out clearly from the white background with a soft shadow.',
    'DEMO-OFF-3011': 'A flat kraft-paper bag full of untreated wooden stirrers, with many thin pale wooden sticks poking out of the top. Not a spoon, not a pencil, not a single stick.',
    'DEMO-OFF-3012': 'Six clear plastic 1.5 litre still-water bottles in exactly two rows of three, each with a white screw cap, filled with pale blue-tinted water. Exactly six bottles and six caps, no seventh bottle. Not a single bottle and not a glass bottle. The whole product visible, standing out clearly from the white background with a soft shadow. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-OFF-3013': 'A flat paper pack of coffee filters, off-white, standing upright with a folded flap across the top. Plain and unprinted, not a single cone filter and not a coffee machine. The whole product visible, standing out clearly from the white background with a soft shadow.',
    'DEMO-OFF-3006': 'A plain rectangular cardboard tea box in cream paper colour, about 100 tea bags, standing upright with a flat top. Unprinted, not a metal tin and not a tea caddy.',
    'DEMO-OFF-3007': 'A small plain rectangular cardboard tea box in muted sage green, 25 tea bags, standing upright. Unprinted, not a metal tin and not a tea caddy.',
    'DEMO-OFF-3014': 'A small plain rectangular cardboard tea box in muted brick red, 20 fruit tea bags, standing upright. Unprinted, not a metal tin and not a tea caddy.',
}
