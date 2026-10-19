"""Electrical pack, series 1: installation cable rings, flange drum, wire spool.

Cable on a ring lies flat on the floor (axis vertical), so its camera pitch
is about 30 like the 2D drawing. Cables leave the ring on the floor with a
short copper or sheath lead. The wire spool stands on its flange.
"""
import math

CORE_COLS = ['#7A4A2A', '#2B2E33', '#8E9399', '#3E6FA8', '#E3E0D8']  # brown, black, grey, blue, white
CORES3 = ['#7A4A2A', '#3E6FA8', '#B8C42B']                 # L brown, N blue, PE green-yellow
CORES5 = ['#7A4A2A', '#2B2E33', '#8E9399', '#3E6FA8', '#B8C42B']  # L1 brown, L2 black, L3 grey, N blue, PE green-yellow


def ring(k, R=92, layers=3, lead=6, sheath='body', cores=1, flange=False, copper=False, colours=None):
    """Cable ring lying flat: wound body as a torus, dark hole, lead out on the floor.

    R outer radius (mm), layers sets the height (6 mm per layer). flange adds a dark
    bottom flange and hub (25 m drum, open on top). cores > 1 shows the coloured cores at the lead end.
    """
    H = 6 + 6 * layers                      # ring height
    minor = H / 2
    z0 = 4 if flange else 0                 # floor line of the wound body
    if flange:
        k.cyl(R + 12, 4, (0, 0, 2), 'dark', bevel=1)                              # bottom flange
        k.cyl(R * 0.35, H + 4, (0, 0, (H + 4) / 2), 'dark', bevel=1)               # drum hub
    else:
        k.cyl(R * 0.42, 1.0, (0, 0, 0.5), 'dark')                                 # dark hole (shadow)
    k.torus(R - minor, minor, (0, 0, z0 + minor), sheath, rough=0.6)              # wound cable
    lead_col = '#C47A4A' if copper else sheath
    k.cyl(lead, 42, (R + 19, 0, lead), lead_col, rot=(0, 90, 0), bevel=0.5, rough=0.5)  # lead on floor
    if cores > 1:
        for i in range(cores):
            a = 2 * math.pi * i / cores
            cols = colours or CORE_COLS
            rad = max(lead * 0.6, cores * lead / (2 * math.pi))  # cores touch, not overlap
            k.cyl(lead * 0.5, 14, (R + 47, rad * math.cos(a),
                                   lead + rad * math.sin(a)),
                  cols[i % len(cols)], rot=(0, 90, 0))


def spool(k, flange=45, width=100, drum=36):
    """Small wire spool standing on one flange: axis along X, flanges at both ends."""
    cz = flange
    k.cyl(drum, width, (0, 0, cz), 'light', rot=(0, 90, 0), rough=0.4)          # wound wire
    k.cyl(20, width + 12, (0, 0, cz), 'dark', rot=(0, 90, 0))                    # core
    for x in (-width / 2 - 3, width / 2 + 3):
        k.cyl(flange, 6, (x, 0, cz), 'body', rot=(0, 90, 0), bevel=1.5)          # flanges
    k.cyl(3, 40, (width / 2 + 10, 0, 6), 'light', rot=(0, 90, 0))                # wire end on floor


# Cable rings: R and layers from the 2D drawing (rx / layers), lead by cable size.
SKUS = {
    'DEMO-ELE-1001': (ring, {'R': 132, 'layers': 4, 'lead': 6, 'sheath': 'body', 'cores': 3, 'colours': CORES3}, {'pitch': 30}),
    'DEMO-ELE-1002': (ring, {'R': 108, 'layers': 6, 'lead': 7, 'sheath': 'body', 'cores': 5, 'colours': CORES5}, {'pitch': 30}),
    'DEMO-ELE-1003': (spool, {}),
    'DEMO-ELE-1004': (ring, {'R': 92, 'layers': 5, 'lead': 7, 'sheath': 'body', 'cores': 3, 'colours': CORES3}, {'pitch': 30}),
    'DEMO-ELE-1005': (ring, {'R': 74, 'layers': 3, 'lead': 6, 'sheath': 'body', 'cores': 3}, {'pitch': 30}),
    'DEMO-ELE-1006': (ring, {'R': 92, 'layers': 5, 'lead': 7, 'sheath': 'body', 'cores': 5, 'colours': CORES5}, {'pitch': 30}),
    'DEMO-ELE-1007': (ring, {'R': 74, 'layers': 3, 'lead': 9, 'sheath': 'body', 'cores': 5, 'colours': CORES5}, {'pitch': 30}),
    'DEMO-ELE-1008': (ring, {'R': 74, 'layers': 3, 'lead': 7, 'sheath': 'body', 'cores': 3, 'colours': CORES3}, {'pitch': 30}),
    'DEMO-ELE-1009': (ring, {'R': 92, 'layers': 2, 'lead': 3, 'sheath': 'body', 'cores': 1, 'copper': True}, {'pitch': 30}),
    'DEMO-ELE-1010': (ring, {'R': 92, 'layers': 2, 'lead': 4, 'sheath': 'body', 'cores': 1, 'copper': True}, {'pitch': 30}),
    'DEMO-ELE-1011': (ring, {'R': 60, 'layers': 3, 'lead': 6, 'sheath': 'body', 'cores': 3, 'flange': True}, {'pitch': 30}),
    'DEMO-ELE-1012': (ring, {'R': 92, 'layers': 4, 'lead': 5, 'sheath': 'mid', 'cores': 4}, {'pitch': 30}),
    'DEMO-ELE-1013': (ring, {'R': 124, 'layers': 5, 'lead': 9, 'sheath': 'body', 'cores': 1, 'copper': True}, {'pitch': 30}),
}


HINTS = {
    'DEMO-ELE-1001': 'A fixed installation cable, 3 x 1.5 mm2 with exactly three cores, grey PVC sheath, wound into a neat flat round ring lying on the floor, with one sheathed lead running out from the ring edge. At the cut end exactly three insulated cores are visible: brown, blue and green-yellow earth. Not a hose: a stiff cable in a tight ring, with no braid and no cuff. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-1002': 'A grey PVC-sheathed installation cable, 5 x 2.5 mm2 with exactly five cores, wound into a neat flat round ring lying on the floor, with the lead running out from the ring edge. At the cut end exactly five insulated cores are visible: brown L1, black L2, grey L3, blue N and green-yellow PE earth. Not a hose: a stiff round cable in a tight ring. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-1003': 'A neat ring of single-core installation wire, 100 m coiled in a loose round ring, about 30 cm across, held together with two thin ties, one end sticking out with a short stripped copper tip; thin round wire with grey-blue PVC insulation, about 3 mm thick. No spool, no drum, no tube. Not a hose.',
    'DEMO-ELE-1004': 'A grey PVC-sheathed installation cable, 3 x 2.5 mm2 with exactly three cores, wound into a neat flat round ring lying on the floor, with the lead running out from the ring edge. At the cut end exactly three insulated cores are visible: brown, blue and green-yellow earth. Not a hose: a stiff round cable in a tight ring. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-1005': 'A grey PVC-sheathed installation cable wound into a small, flat round ring on the floor, with three coloured cores visible at the cut end of the lead: brown, black and grey. Not a hose: a stiff cable, a smaller and thinner ring than a 100 m coil.',
    'DEMO-ELE-1006': 'A grey PVC-sheathed installation cable, 5 x 1.5 mm2 with exactly five cores, wound into a neat flat round ring lying on the floor, with the lead running out from the ring edge. At the cut end exactly five separately insulated cores are visible, not a sealed tip: brown L1, black L2, grey L3, blue N and green-yellow PE earth. Not a hose: a stiff round cable in a tight ring. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-1007': 'A thicker grey PVC-sheathed installation cable, 5 x 4 mm2 with exactly five cores, wound into a neat flat round ring lying on the floor, with the lead running out from the ring edge. At the cut end exactly five insulated cores are visible: brown L1, black L2, grey L3, blue N and green-yellow PE earth. Not a hose: a stiff round cable in a tight ring. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-1008': 'A grey PVC-sheathed installation cable, 3 x 4 mm2 with exactly three cores, wound into a neat flat round ring lying on the floor, with the lead running out from the ring edge. At the cut end exactly three insulated cores are visible: brown, blue and green-yellow earth. Not a hose: a stiff round cable in a tight ring. No text, no numbers, no logos, no labels anywhere on the product.',
    'DEMO-ELE-1009': 'A neat ring of single-core installation wire, 100 m coiled in a loose round ring, about 30 cm across, one end sticking out with a short stripped copper tip only a few millimetres long; thin round wire with grey PVC insulation, about 4 mm thick. Not a copper pipe, not a hose.',
    'DEMO-ELE-1010': 'A neat ring of single-core installation wire, 100 m coiled in a loose round ring, about 30 cm across, one end sticking out with a short stripped copper tip only a few millimetres long; round wire with dark grey PVC insulation, about 5 mm thick. Not a copper pipe, not a hose.',
    'DEMO-ELE-1011': 'A flexible grey cable on a 25 m drum: a dark round drum open on top with a dark flange at the bottom and a central hub, the cable wound inside it and three coloured cores at the lead end. Not a ring on the floor: the cable sits in a drum with flanges.',
    'DEMO-ELE-1012': 'A mid-grey data cable wound into a flat round ring on the floor, with four coloured cores visible at the cut end of the lead. Not a power cable: it is thinner than an installation cable and carries signal wires.',
    'DEMO-ELE-1013': 'A single-core installation wire wound into a flat round ring on the floor, dark grey sheath, with a thick bare copper-coloured conductor at the cut end of a short lead. Not a hose: a stiff round ring with one thick copper end.',
}
