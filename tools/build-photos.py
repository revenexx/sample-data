#!/usr/bin/env python3
"""Build the product photos of one pack: Blender render, then a local AI edit.

Development tool only: the photos are committed, seed.sh never runs this.

    python3 tools/build-photos.py industrial            # changed and missing products
    python3 tools/build-photos.py industrial DEMO-IND-1005 DEMO-IND-3001   # just these
    python3 tools/build-photos.py industrial --force    # everything
    python3 tools/build-photos.py lab --restamp        # after a change to render.py or lib.py:
        # record the new model hashes without rebuilding anything
    PHOTO_DEVICE=CPU python3 tools/build-photos.py lab --render-only   # Blender on the CPU only,
        # e.g. while another pack's AI step has the GPU

Needs Blender on the PATH (macOS: brew install --cask blender) and the mflux
virtualenv for the AI step, once:

    uv venv -p 3.12 tools/photo/.venv && uv pip install -p tools/photo/.venv mflux

The first AI run downloads FLUX.2-klein-4B (Apache-2.0, about 15 GB) from
Hugging Face. On an M4 Pro a product takes about 15 s in Blender and 10–40 s in
the AI step (more when lettering forces a retry). tools/photo/state/<pack>.json remembers what each photo was
built from (model source and prompt), so a re-run only rebuilds what changed.
"""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHOTO = ROOT / 'tools' / 'photo'
BLENDER = os.environ.get('BLENDER', 'blender')
VENV_PY = os.environ.get('MFLUX_PYTHON', str(PHOTO / '.venv' / 'bin' / 'python'))
CACHE = PHOTO / '.cache'

# Variant SKU suffixes: sizes reuse the model's photo, colours recolour it.
SIZES = {'s', 'm', 'l', 'xl'}
# Colour variants recoloured pixel by pixel (tools/photo/recolour.py), not by the AI: the shape stays
# exactly the model's. Needed where the edit model fails (white products to dark colours, or extra
# objects that change between colours). Whole packs, or single model SKUs.
TINT_PACKS = {'electrical'}
# The model's own colour: the variant in that colour shows the model's photo unchanged (a copy, like a size).
MODEL_COLOUR = {f'DEMO-OFF-{n}': 'blue' for n in ('1002', '1010', '1011', '1013', '2008', '4001', '5001')}
TINT_MODELS = set()
TINT = {'black': '#1E1F22', 'white': '#F2F2EF', 'anthracite': '#3B3E43', 'aluminium': '#B9BDC3', 'stainless': '#C8CCD1',
        'blue': '#2B55B8', 'red': '#C4302B', 'green': '#2F8A4F', 'grey': '#9A9EA4', 'yellow': '#F2C81F'}
COLOURS = {'black': 'matt black', 'blue': 'medium blue', 'red': 'signal red', 'green': 'medium green',
           'grey': 'light grey', 'white': 'pure white', 'yellow': 'bright yellow', 'anthracite': 'anthracite grey',
           'aluminium': 'brushed aluminium', 'stainless': 'brushed stainless steel', 'natural': 'natural translucent white'}

BASE = ('Photorealistic materials and details as the real product has them, seamless pure white background, soft '
        'studio light, sharp focus, e-commerce catalogue photo, three-quarter view from the front left. Plain unbranded '
        'product: no logo, no lettering, no emblem, no sticker, no printed text. Any mains plug or socket is European '
        '(Schuko type F, two round pins), never an American or British one.')


def blender(*args, tolerate=False):
    """Run render.py in Blender. With tolerate=True a crash is returned, not fatal
    (Blender's Metal shader cache crashes now and then)."""
    run = subprocess.run([BLENDER, '-b', '-P', str(PHOTO / 'render.py'), '--', *args], capture_output=True, text=True)
    failed = run.returncode or 'Traceback' in run.stdout + run.stderr
    if failed and not tolerate:
        sys.exit(f'blender failed:\n{run.stdout[-3000:]}\n{run.stderr[-3000:]}')
    if failed and 'Traceback' in run.stdout + run.stderr:
        sys.exit(f'blender failed (Python error):\n{run.stdout[-3000:]}\n{run.stderr[-3000:]}')
    return run.stdout


def names(pack):
    """sku -> (English name, description) from the pack's products.json."""
    out = {}
    for p in json.loads((ROOT / 'packs' / pack / 'products.json').read_text()):
        en = p['attribute_values']['locale_specific']['en-US']
        out[p['sku']] = (en['name'], en.get('description', ''))
    return out


def parents(pack):
    """sku -> its model's SKU (itself when it has none)."""
    return {p['sku']: p.get('parent', p['sku']) for p in json.loads((ROOT / 'packs' / pack / 'products.json').read_text())}


TEXT_OK = '[text ok]'   # put this in a hint where the product should show text or numbers


def prompt(name, text, hint):
    base = BASE
    if TEXT_OK in hint:
        hint = hint.replace(TEXT_OK, '').strip()
        base = BASE.replace('no lettering, no emblem, no sticker, no printed text.', 'no brand names.')
    return ' '.join(x for x in (f'Professional studio product photograph of a real {name}.', text, hint, base) if x)


RESEED = 0


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    pack, wanted, force = args[0], set(args[1:]), '--force' in sys.argv
    global RESEED
    RESEED = next((int(a.split('=', 1)[1]) for a in sys.argv if a.startswith('--reseed=')), 0)
    products = names(pack)
    family = parents(pack)
    with tempfile.TemporaryDirectory() as tmp:
        hashes_file = Path(tmp) / 'hashes.json'
        blender(pack, 'hashes', str(hashes_file))
        models = json.loads(hashes_file.read_text())
    missing = sorted(set(products) - set(models))
    extra = sorted(set(models) - set(products))
    if missing:
        print(f'  no model yet for {len(missing)} products: {" ".join(missing[:12])}{" …" if len(missing) > 12 else ""}')
    if extra:
        sys.exit(f'models list SKUs that are not products: {" ".join(extra)}')

    state_file = PHOTO / 'state' / f'{pack}.json'
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    if '--restamp' in sys.argv:
        # Swap each product's recorded model hash for the current one, wherever it
        # appears (variants record their model's), and keep the prompt hashes, so
        # products with a changed description are still rebuilt by the next run.
        swap = {state[sku]['model']: models[sku]['hash'] for sku in models if 'model' in state.get(sku, {})}
        def renew(v):
            return {k: renew(x) for k, x in v.items()} if isinstance(v, dict) else swap.get(v, v)
        state = {sku: renew(v) for sku, v in state.items()}
        state_file.write_text(json.dumps(dict(sorted(state.items())), indent=1) + '\n')
        print(f'  {pack}: restamped {len(swap)} model hashes')
        return
    images = ROOT / 'packs' / pack / 'assets' / 'images'
    def photo_want(sku):
        p = prompt(*products[sku], models[sku]['hint'])
        return p, {'model': models[sku]['hash'], 'prompt': hashlib.sha256(p.encode()).hexdigest()[:16]}

    jobs = []
    for sku in sorted(models):
        if wanted and sku not in wanted and family[sku] not in wanted:
            continue
        out = images / f'{sku.lower()}.jpg'
        parent = family[sku]
        suffix = sku.rsplit('-', 1)[-1].lower() if parent != sku else ''
        seed = int(hashlib.sha256(parent.encode()).hexdigest(), 16) % 1_000_000
        if sku in wanted or parent in wanted:
            seed += RESEED * 7919                       # --reseed N: a different take for a redo
        if suffix in SIZES or suffix in COLOURS:
            # A size variant shows its model's photo; a colour variant is that
            # photo recoloured, so the variants of one product match exactly.
            source = images / f'{parent.lower()}.jpg'
            base = photo_want(parent)[1]
            if suffix in SIZES or MODEL_COLOUR.get(parent) == suffix:
                job = {'kind': 'copy', 'source': str(source)}
                want = {'copy': base}
            elif (pack in TINT_PACKS or parent in TINT_MODELS) and suffix in TINT:
                job = {'kind': 'tint', 'source': str(source), 'colour': TINT[suffix]}
                want = {'tint': base, 'photo': hashlib.sha256(source.read_bytes()).hexdigest()[:16] if source.exists() else '',
                        'colour': TINT[suffix]}
            else:
                p = (f'Change only the colour of the {products[parent][0]} to {COLOURS[suffix]}. Keep the shape, '
                     'every detail, the lighting, the camera angle and the white background exactly the same.')
                job = {'kind': 'recolour', 'source': str(source), 'prompt': p}
                want = {'recolour': base, 'prompt': hashlib.sha256(p.encode()).hexdigest()[:16]}
        else:
            p, want = photo_want(sku)
            if parent != sku:
                want['seed'] = seed
            job = {'kind': 'photo', 'render': str(CACHE / pack / f'{sku.lower()}.png'), 'prompt': p, 'model': want['model'],
                   'text_ok': TEXT_OK in models[sku]['hint']}
        if not force and out.exists() and state.get(sku) == want:
            continue
        jobs.append({**job, 'sku': sku, 'seed': seed, 'out': str(out), 'want': want})
    if not jobs:
        print(f'  {pack}: all photos up to date')
        return

    # Step 1: render what has no current render in the cache.
    stamp = CACHE / pack / 'renders.json'
    rendered = json.loads(stamp.read_text()) if stamp.exists() else {}
    todo = [j['sku'] for j in jobs if j['kind'] == 'photo' and (rendered.get(j['sku']) != j['model'] or not Path(j['render']).exists())]
    tries = 0
    while todo:
        out = blender(pack, 'render', str(CACHE / pack), *todo[:20], tolerate=True)
        done = [line.split()[1] for line in out.splitlines() if line.startswith('RENDERED ')]
        for sku in done:
            rendered[sku] = models[sku]['hash']
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.write_text(json.dumps(rendered, indent=1))
        if len(done) < len(todo[:20]):
            tries += 1
            print(f'  blender stopped after {len(done)} renders, resuming ({tries}/3)', flush=True)
            if tries > 3:
                sys.exit('blender keeps crashing')
        todo = [sku for sku in todo if sku not in done]
        print(f'  rendered, {len(todo)} to go', flush=True)

    if '--render-only' in sys.argv:
        return

    # Step 2: the AI edit, one process for the whole list (the model loads once).
    jobs_file = CACHE / pack / 'jobs.json'
    jobs_file.write_text(json.dumps(jobs, indent=1))
    run = subprocess.Popen([VENV_PY, str(PHOTO / 'generate.py'), str(jobs_file)], stdout=subprocess.PIPE, text=True)
    done = 0
    by_name = {Path(j['out']).name: j for j in jobs}
    for line in run.stdout:
        if line.startswith('PHOTO '):
            fname, _, text = line[6:].rstrip('\n').partition('\t')
            j = by_name[fname]
            if text:
                print(f'  ⚠ {j["sku"]}: lettering left after all tries: {text}', flush=True)
            state[j['sku']] = j['want']
            done += 1
            state_file.parent.mkdir(parents=True, exist_ok=True)
            state_file.write_text(json.dumps(dict(sorted(state.items())), indent=1) + '\n')
            print(f'  photo {done}/{len(jobs)} {j["sku"]}', flush=True)
    if run.wait():
        sys.exit('the AI step failed (see above)')


if __name__ == '__main__':
    main()
