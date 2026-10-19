"""Model SKUs that get an automatic technical drawing (tools/build-drawings.py).

Parents only: no size (-S/-M/-L/-XL) or colour variants. A SKU with a hand-made drawing
(the "drawings" table in tools/packs/<pack>.py) is skipped by build-drawings.py.
"""

def _skus(prefix, *numbers):
    return [f'DEMO-{prefix}-{n}' for n in numbers]

DRAW = {
    # Excluded: wearables (glasses, helmet, ear defenders, gloves, rain jacket, masks), barrier tape,
    # abrasives and cutting discs (consumables), cable ties, nails and screw assortments (piles).
    'industrial': (
        _skus('IND', *[f'{n}' for n in (1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011,
                                         1012, 1013, 1014, 1015, 1016, 1017, 1018)])
        + _skus('IND', *[f'{n}' for n in (2002, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                                           2016, 2017, 2018, 2019, 2021, 2022, 2023)])
        + _skus('IND', *[f'{n}' for n in range(4001, 4019)])
        + _skus('IND', *[f'{n}' for n in (6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6011, 6012)])
    ),
    # Excluded: cables on rings and drums, LED strip reel, cable ties, conduit rolls, ferrule packs,
    # wire end ferrules (piles), labels, and the paper-like items.
    'electrical': (
        _skus('ELE', *[f'{n}' for n in (3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010, 3011,
                                         3012, 3013, 3014, 3015, 3016, 3017, 3019, 3020)])
        + _skus('ELE', *[f'{n}' for n in (2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011,
                                           2012, 2013, 2014, 2015, 2017, 2018)])
        + _skus('ELE', *[f'{n}' for n in range(6001, 6013)])
        + _skus('ELE', *[f'{n}' for n in (5001, 5002, 5003, 5007, 5008, 5012, 5013, 5014, 5015, 5016, 5017,
                                           5018, 5022)])
        + _skus('ELE', *[f'{n}' for n in range(4001, 4015)])
    ),
    # Excluded: paper, envelopes, mailers, bags, wrapping paper, tapes, labels, pens, pencils, notes,
    # notebooks, cards, glue, coffee, tea, water and other food, cleaning cloths, sponges, cleaners.
    'office': (
        _skus('OFF', *[f'{n}' for n in (4001, 4002, 4003, 4005, 4010, 4011, 4012, 4015)])
        + _skus('OFF', *[f'{n}' for n in (1009, 1010, 1011, 1012, 1013)])
        + _skus('OFF', *[f'{n}' for n in (6008, 6009, 6010)])
        + _skus('OFF', *[f'{n}' for n in (2004, 2007, 2012, 2013, 2014)])
        + _skus('OFF', *[f'{n}' for n in (5008, 5010, 5013, 5014, 5015)])
    ),
    # Excluded: pipette tips, racks of tips, tubes and plates in bags, PPE, labels and cryo labels,
    # and the consumable packs.
    'lab': (
        _skus('LAB', *[f'{n}' for n in range(1001, 1023)])
        + _skus('LAB', *[f'{n}' for n in (2001, 2003, 2004, 2005, 2006, 2007, 2016)])
        + _skus('LAB', *[f'{n}' for n in range(4001, 4022)])
        + _skus('LAB', *[f'{n}' for n in (6001, 6002, 6003, 6004, 6005, 6006, 6007, 6008, 6009, 6011,
                                           6012, 6013, 6014, 6015)])
    ),
}


# Not drawn (checked 2026-10-18): the model is shortened or rotated for the photo, or its line drawing is
# unreadable (sets of many small parts): DEMO-ELE-3002, DEMO-ELE-3006, DEMO-ELE-3007, DEMO-ELE-3008, DEMO-ELE-5007, DEMO-ELE-5008, DEMO-IND-4002, DEMO-IND-4003, DEMO-IND-4009, DEMO-IND-4013, DEMO-IND-4014, DEMO-IND-4017, DEMO-OFF-2013.

SKIP = {'DEMO-ELE-3002', 'DEMO-ELE-3006', 'DEMO-ELE-3007', 'DEMO-ELE-3008', 'DEMO-ELE-5007', 'DEMO-ELE-5008',
        'DEMO-IND-4002', 'DEMO-IND-4003', 'DEMO-IND-4009', 'DEMO-IND-4013',
        'DEMO-IND-4014', 'DEMO-IND-4017', 'DEMO-OFF-2013'}
DRAW = {pack: [s for s in skus if s not in SKIP] for pack, skus in DRAW.items()}

# The model is smaller than the product: dimension labels are scaled to the nominal length (W, D, H alike).
SIZE_SCALE = {'DEMO-IND-4005': 250 / 348, 'DEMO-IND-4006': 200 / 150, 'DEMO-IND-4007': 160 / 119,
              'DEMO-IND-4008': 250 / 195, 'DEMO-IND-4011': 200 / 255}
