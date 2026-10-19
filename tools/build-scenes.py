#!/usr/bin/env python3
"""Build the second product image of one pack: the product in use, as a close-up.

Development tool only: the images are committed, the seeder never runs this.

    python3 tools/build-scenes.py lab                      # changed and missing products
    python3 tools/build-scenes.py lab DEMO-LAB-1007        # just these (and their variants)
    python3 tools/build-scenes.py lab --force              # everything

Runs after tools/build-photos.py and uses its finished photo as the reference:
the FLUX.2-klein-4B edit model places that exact product into the setting
written in tools/photo/scenes/<pack>.py, framed as a close-up. Colour variants
recolour their model's scene image, size variants copy it. Output:
packs/<pack>/assets/images/<sku>-2.jpg. tools/photo/state/<pack>-scenes.json
records what each image was built from, so a re-run only rebuilds what changed
(a new main photo or a new scene text).
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
SIZES, COLOURS, names, parents = build_photos.SIZES, build_photos.COLOURS, build_photos.names, build_photos.parents

CLOSE_UP = ('Close-up with a 100 mm macro lens from very near: the product fills the frame and may be cut off at the '
            'edges, very shallow depth of field, the background completely blurred.')
KEEP = ('Keep the product looking exactly the same: same model, colours, materials and details. Realistic natural '
        'daylight, professional product lifestyle photography. No people, no hands, no text, no logos, no brand names. '
        'Any mains plug or socket is European (Schuko).')


def digest(*parts):
    h = hashlib.sha256()
    for part in parts:
        h.update(part if isinstance(part, bytes) else part.encode())
    return h.hexdigest()[:16]


RESEED = 0
TINT_WORDS = {'white': 'pure white', 'black': 'matt black', 'anthracite': 'matt anthracite grey',
              'aluminium': 'brushed aluminium silver', 'stainless': 'brushed stainless steel', 'blue': 'medium blue',
              'red': 'signal red', 'green': 'medium green', 'grey': 'light grey', 'yellow': 'bright yellow'}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    pack, wanted, force = args[0], set(args[1:]), '--force' in sys.argv
    global RESEED
    RESEED = next((int(a.split('=', 1)[1]) for a in sys.argv if a.startswith('--reseed=')), 0)
    products, family = names(pack), parents(pack)
    spec = importlib.util.spec_from_file_location('scenes', PHOTO / 'scenes' / f'{pack}.py')
    scenes = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scenes)
    images = ROOT / 'packs' / pack / 'assets' / 'images'
    state_file = PHOTO / 'state' / f'{pack}-scenes.json'
    state = json.loads(state_file.read_text()) if state_file.exists() else {}

    jobs = []
    for sku in sorted(products):
        if wanted and sku not in wanted and family[sku] not in wanted:
            continue
        parent = family[sku]
        suffix = sku.rsplit('-', 1)[-1].lower() if parent != sku else ''
        out = images / f'{sku.lower()}-2.jpg'
        seed = int(hashlib.sha256(parent.encode()).hexdigest(), 16) % 1_000_000
        if sku in wanted or parent in wanted:
            seed += RESEED * 7919                       # --reseed N: a different take for a redo
        same = build_photos.MODEL_COLOUR.get(parent) == suffix      # the model's own colour: a copy
        tinted = not same and (pack in build_photos.TINT_PACKS or parent in build_photos.TINT_MODELS) and suffix in build_photos.TINT
        if parent != sku and '--parents-only' in sys.argv:
            continue
        if tinted:
            # A pixel-recoloured variant gets its model's close-up with only the product's colour changed:
            # the edit model takes the model's scene and the variant's photo as the two references.
            scene, photo = images / f'{parent.lower()}-2.jpg', images / f'{sku.lower()}.jpg'
            p = (f'Recolour the {products[parent][0]} in the first image to {TINT_WORDS[suffix]}, exactly like the product '
                 'in the second image: every part of the product that is coloured there gets that colour, metal parts stay '
                 'metal. Keep everything else in the first image exactly the same: the wall, the setting, the light, the '
                 'framing, the camera angle and the shape of the product. Only the product changes colour, nothing around it.')
            job = {'kind': 'scene', 'sources': [str(scene), str(photo)], 'source': str(scene), 'prompt': p}
            want = {'variant': digest(photo.read_bytes(), scenes.SCENES[parent]), 'prompt': digest(p)}
        elif suffix in SIZES or suffix in COLOURS:
            source = images / f'{parent.lower()}-2.jpg'
            base = digest((images / f'{parent.lower()}.jpg').read_bytes(), scenes.SCENES[parent])
            if suffix in SIZES or same:
                job, want = {'kind': 'copy', 'source': str(source)}, {'copy': base}
            else:
                p = (f'Change only the colour of the {products[parent][0]} to {COLOURS[suffix]}. Keep the shape, '
                     'every detail, the setting, the lighting and the camera angle exactly the same.')
                job, want = {'kind': 'recolour', 'source': str(source), 'prompt': p}, {'recolour': base, 'prompt': digest(p)}
        else:
            photo = images / f'{sku.lower()}.jpg'
            if not photo.exists():
                print(f'  {sku}: no main photo yet, skipped')
                continue
            text_ok = '[text ok]' in scenes.SCENES[sku]
            keep = KEEP.replace('No people, no hands, no text, no logos, no brand names.', 'No people, no hands, no logos, no brand names.') if text_ok else KEEP
            p = ' '.join((scenes.SCENES[sku].replace('[text ok]', '').strip(), CLOSE_UP, keep))
            job = {'kind': 'scene', 'source': str(photo), 'prompt': p, 'text_ok': text_ok}
            want = {'scene': digest(photo.read_bytes(), scenes.SCENES[sku]), 'prompt': digest(p)}
        if not force and out.exists() and state.get(sku) == want:
            continue
        jobs.append({**job, 'sku': sku, 'seed': seed, 'out': str(out), 'whiten': False, 'want': want})
    if not jobs:
        print(f'  {pack}: all scene images up to date')
        return

    jobs_file = CACHE / pack / 'scene-jobs.json'
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
            print(f'  scene {done}/{len(jobs)} {j["sku"]}' + (f'  ⚠ lettering: {text}' if text else ''), flush=True)
    if run.wait():
        sys.exit('the AI step failed (see above)')


if __name__ == '__main__':
    main()
