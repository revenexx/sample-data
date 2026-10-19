#!/usr/bin/env python3
"""Build the category images of one pack: three of the category's products in one group photo.

Development tool only: the images are committed, the seeder never runs this.

    python3 tools/build-categories.py lab                  # changed and missing categories
    python3 tools/build-categories.py lab DEMO-LAB-SAFETY  # just these
    python3 tools/build-categories.py lab --force          # everything

Runs after tools/build-photos.py and uses its finished photos as references: the
FLUX.2-klein-4B edit model puts three product photos of the category together into
one styled group shot. A subcategory takes three of its own models (first, middle,
last, or the picks in PICKS); the top category takes the first model of three of its
subcategories. Output: packs/<pack>/assets/categories/<code>.jpg, linked as the
category's `values.image` by tools/build-pack.py. tools/photo/state/<pack>-categories.json
records what each image was built from, so a re-run only rebuilds what changed.
"""
import hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / 'tools' / 'photo'
VENV_PY = os.environ.get('MFLUX_PYTHON', str(PHOTO / '.venv' / 'bin' / 'python'))
CACHE = PHOTO / '.cache'

spec = importlib.util.spec_from_file_location('build_photos', ROOT / 'tools' / 'build-photos.py')
build_photos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_photos)
names, parents = build_photos.names, build_photos.parents

# Where the group stands, per pack.
SETTING = {
    'industrial': 'on a clean steel workbench in a bright, tidy workshop',
    'electrical': "on a clean light workbench in a bright electrician's workshop",
    'office': 'on a clean light wooden desk in a bright, modern office',
    'lab': 'on a clean white lab bench in a bright, modern laboratory',
}
# category code -> the three model SKUs to show, where the automatic choice is weak.
PICKS = {
    'DEMO-ELE': ['DEMO-ELE-1001', 'DEMO-ELE-6001', 'DEMO-ELE-6007'],
    'DEMO-ELE-SWITCHES': ['DEMO-ELE-2001', 'DEMO-ELE-2012', 'DEMO-ELE-2013'],
    'DEMO-ELE-LIGHTING': ['DEMO-ELE-3010', 'DEMO-ELE-3019', 'DEMO-ELE-3020'],
    'DEMO-ELE-PROTECTION': ['DEMO-ELE-4001', 'DEMO-ELE-4006', 'DEMO-ELE-4009'],
    'DEMO-IND-POWER-TOOLS': ['DEMO-IND-1001', 'DEMO-IND-1003', 'DEMO-IND-1007'],
    'DEMO-IND-SAFETY': ['DEMO-IND-3004', 'DEMO-IND-3001', 'DEMO-IND-3002'],
    'DEMO-IND-HAND-TOOLS': ['DEMO-IND-4001', 'DEMO-IND-4006', 'DEMO-IND-4010'],
    'DEMO-OFF-MAIL': ['DEMO-OFF-6001', 'DEMO-OFF-6004', 'DEMO-OFF-6006'],
    'DEMO-LAB-INSTRUMENTS': ['DEMO-LAB-1001', 'DEMO-LAB-1007', 'DEMO-LAB-1012'],
}
# Categories built from the products' close-ups (installed, in use) instead of their studio photos.
FROM_CLOSE_UPS = {'DEMO-ELE-PROTECTION'}
# category code -> where the group is, where the pack's bench is wrong: installed products are
# shown installed, large ones on the floor.
WHERE = {
    'DEMO-ELE-SWITCHES': ('installed in a smooth white plastered wall, flush-mounted: only the flat cover frames show, '
                          'lying on the wall surface a few millimetres proud, seen nearly front-on'),
    'DEMO-ELE-LIGHTING': 'mounted on a smooth light wall of a bright modern room, switched on',
    'DEMO-ELE-PROTECTION': ('as narrow modular DIN-rail devices (each 90 mm tall with a stepped side profile, '
                            'a raised middle with the toggle lever, screw terminals top and bottom), snapped onto a metal DIN rail in an open control cabinet, wired with grey and blue wires, '
                            'with grey slotted wiring ducts above and below'),
    'DEMO-IND-WORKSHOP': 'standing on the floor of a bright, tidy workshop',
    'DEMO-OFF-CLEAN': 'in a bright, tidy cleaning cupboard of a modern office',
}

GROUP = ('A styled group photo of exactly these three products together, side by side, {where}: {items}. '
         'All three are fully visible, sharp and at a believable size relative to each other, nothing else in front of them. '
         'Keep each product looking exactly the same as in its picture: same shape, colours, materials and details. '
         'Packaging stays plain and unprinted exactly as in its picture: no pictures of fruit or food, no labels, no lettering. '
         'Wide shot at eye level, realistic natural daylight, the background softly blurred, professional catalogue photography. '
         'No people, no hands, no text, no logos, no brand names. Any mains plug or socket is European (Schuko).')


def digest(*parts):
    h = hashlib.sha256()
    for part in parts:
        h.update(part if isinstance(part, bytes) else part.encode())
    return h.hexdigest()[:16]


def choose(pack):
    """category code -> up to three model SKUs."""
    cats = json.loads((ROOT / 'packs' / pack / 'categories.json').read_text())
    family = parents(pack)
    members = {}
    for link in json.loads((ROOT / 'packs' / pack / 'product-categories.json').read_text()):
        sku = link['product']
        if family.get(sku, sku) == sku and sku not in members.get(link['category'], []):
            members.setdefault(link['category'], []).append(sku)
    out = {}
    for c in cats:
        if c['code'] in PICKS:
            out[c['code']] = PICKS[c['code']]
        elif c.get('parent'):
            m = members.get(c['code'], [])
            out[c['code']] = list(dict.fromkeys([m[0], m[len(m) // 2], m[-1]])) if m else []
        else:
            subs = [s['code'] for s in cats if s.get('parent') == c['code'] and members.get(s['code'])]
            out[c['code']] = [members[s][0] for s in subs[:3]]
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    pack, wanted, force = args[0], set(args[1:]), '--force' in sys.argv
    reseed = next((int(a.split('=', 1)[1]) for a in sys.argv if a.startswith('--reseed=')), 0)
    products = names(pack)
    images = ROOT / 'packs' / pack / 'assets' / 'images'
    out_dir = ROOT / 'packs' / pack / 'assets' / 'categories'
    out_dir.mkdir(parents=True, exist_ok=True)
    state_file = PHOTO / 'state' / f'{pack}-categories.json'
    state = json.loads(state_file.read_text()) if state_file.exists() else {}

    jobs = []
    for i, (code, skus) in enumerate(choose(pack).items()):
        if wanted and code not in wanted:
            continue
        tail = '-2' if code in FROM_CLOSE_UPS else ''
        photos = [images / f'{s.lower()}{tail}.jpg' for s in skus]
        if not photos or not all(p.exists() for p in photos):
            print(f'  {code}: product photos missing, skipped')
            continue
        items = '; '.join(f'{n + 1}. {products[s][0]}' for n, s in enumerate(skus))
        p = GROUP.format(where=WHERE.get(code, SETTING[pack]), items=items)
        want = {'photos': digest(*[x.read_bytes() for x in photos]), 'prompt': digest(p)}
        out = out_dir / f'{code.lower()}.jpg'
        if not force and out.exists() and state.get(code) == want:
            continue
        jobs.append({'kind': 'scene', 'sources': [str(x) for x in photos], 'source': str(photos[0]), 'prompt': p,
                     'sku': code, 'seed': 100 + i + reseed * 1000, 'out': str(out), 'whiten': False, 'want': want})
    if not jobs:
        print(f'  {pack}: all category images up to date')
        return

    jobs_file = CACHE / pack / 'category-jobs.json'
    jobs_file.parent.mkdir(parents=True, exist_ok=True)
    jobs_file.write_text(json.dumps(jobs, indent=1))
    run = subprocess.Popen([VENV_PY, str(PHOTO / 'generate.py'), str(jobs_file)], stdout=subprocess.PIPE, text=True)
    by_name = {Path(j['out']).name: j for j in jobs}
    done = 0
    for line in run.stdout:
        if line.startswith('PHOTO '):
            fname, _, text = line[6:].rstrip('\n').partition('\t')
            j = by_name[fname]
            state[j['sku']] = j['want']
            done += 1
            state_file.parent.mkdir(parents=True, exist_ok=True)
            state_file.write_text(json.dumps(dict(sorted(state.items())), indent=1) + '\n')
            print(f'  category {done}/{len(jobs)} {j["sku"]}' + (f'  ⚠ lettering: {text}' if text else ''), flush=True)
    if run.wait():
        sys.exit('the AI step failed (see above)')


if __name__ == '__main__':
    main()
