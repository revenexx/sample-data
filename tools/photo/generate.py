"""Turn Blender renders into product photos (step 2 of the photos).

Runs in the mflux virtualenv (see tools/build-photos.py), never inside Blender:

    tools/photo/.venv/bin/python tools/photo/generate.py <jobs.json>

jobs.json is a list of {"kind", "render" or "source", "prompt", "seed", "out"}; see main().
The model is FLUX.2-klein-4B (Apache-2.0), run locally with mflux on Apple
silicon, as image-to-image at low strength: the render only fixes the product
type, colours, composition and camera angle; the model draws a realistic
product. Photos with lettering (made-up brand names) are generated again with
the next seed, up to TRIES times. Afterwards the backdrop is mapped to white.
"""
import json, os, subprocess, sys, tempfile, threading, time
from pathlib import Path

import numpy as np
from PIL import Image

MODEL = 'black-forest-labs/FLUX.2-klein-4B'
SIZE = 800
STRENGTH = 0.3      # how much of the render survives; 4 steps make this 1 of 4
TRIES = 4
TEXTCHECK = Path(__file__).resolve().parent / '.cache' / 'textcheck'


def lettering(path):
    """Words Apple's Vision finds in the image ('' when clean)."""
    if not TEXTCHECK.exists():
        TEXTCHECK.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['swiftc', '-O', '-o', str(TEXTCHECK), str(TEXTCHECK.parent.parent / 'textcheck.swift')], check=True)
    out = subprocess.run([str(TEXTCHECK), str(path)], capture_output=True, text=True, check=True).stdout
    return out.rstrip('\n').split('\t', 1)[1] if '\t' in out else ''


def on_white(render_png, path):
    """The render on white. Near-transparent floor haze is dropped, the shadow kept."""
    im = Image.open(render_png).convert('RGBA')
    im.putalpha(im.getchannel('A').point(lambda v: max(0, round((v - 10) * 255 / 245))))
    tile = Image.new('RGBA', im.size, '#FFFFFF')
    tile.alpha_composite(im)
    tile.convert('RGB').save(path)


def whiten(img):
    """Map the studio backdrop (sampled at the border) to #FFFFFF, keep shadows."""
    a = np.asarray(img.convert('RGB')).astype(np.float32)
    b = max(4, a.shape[0] // 40)
    border = np.concatenate([a[:b].reshape(-1, 3), a[-b:].reshape(-1, 3), a[:, :b].reshape(-1, 3), a[:, -b:].reshape(-1, 3)])
    a = a * (255.0 / np.percentile(border, 60, axis=0))
    lift = np.clip((a.mean(axis=2, keepdims=True) - 225) / 22, 0, 1)   # 225..247 fades into white
    a = a * (1 - lift) + 255 * lift
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def tint(source, colour, out, keep_light=True):
    """Recolour a product photo on white without AI: every product pixel gets the target
    hue and saturation, its brightness scaled so the shading stays. Shape and details stay
    identical to the model's photo. Very bright highlights (lit lenses) are kept."""
    im = Image.open(source).convert('RGB')
    hsv = np.asarray(im.convert('HSV')).astype(np.float32)
    rgb = np.asarray(im).astype(np.float32) / 255
    lum = rgb.mean(axis=2)
    # The backdrop is what a flood fill from the corners reaches (it stops at the product's
    # outline), so white products on white are still found; the soft shadow counts as backdrop.
    from PIL import ImageDraw, ImageFilter
    probe = im.copy()
    w, h = probe.size
    for xy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1), (w // 2, 0), (w // 2, h - 1)):
        if probe.getpixel(xy) != (255, 0, 255):
            ImageDraw.floodfill(probe, xy, (255, 0, 255), thresh=18)
    bg = np.all(np.asarray(probe) == (255, 0, 255), axis=2)
    mask = Image.fromarray((~bg * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
    product = np.asarray(mask).astype(np.float32) / 255
    v = hsv[..., 2] / 255
    ref = np.median(v[product > 0.9]) if (product > 0.9).any() else 0.8
    t = np.asarray(Image.new('RGB', (1, 1), colour).convert('HSV')).astype(np.float32)[0, 0]
    new = hsv.copy()
    new[..., 0], new[..., 1] = t[0], t[1]
    new[..., 2] = np.clip(v * (t[2] / 255) / max(ref, 0.05), 0, 1) * 255
    tinted = np.asarray(Image.fromarray(new.astype(np.uint8), 'HSV').convert('RGB')).astype(np.float32)
    keep = np.zeros_like(lum) if keep_light is False else np.clip((lum - 0.985) / 0.01, 0, 1)   # lit lenses stay
    m = (product * (1 - keep))[..., None]
    outimg = tinted * m + rgb * 255 * (1 - m)
    Image.fromarray(np.clip(outimg, 0, 255).astype(np.uint8)).save(out, 'JPEG', quality=85, optimize=True, progressive=True)


def best_of(make, stem, tmp, seed, text_ok=False):
    """Up to TRIES images from make(seed); the first without lettering, else the one with least."""
    best = None
    for t in range(TRIES):
        raw = tmp / f'{stem}-{t}.png'   # mflux never overwrites, so one name per try
        make(seed + t).save(path=str(raw))
        text = '' if text_ok else lettering(raw)
        if best is None or len(text) < len(best[1]):
            best = (raw, text)
        if not text:
            break
    return best


class Queue:
    """Jobs in order; a job is handed out only when the image it starts from is
    not still being made in this run (a variant waits for its model)."""

    def __init__(self, jobs):
        self.jobs, self.pending = list(jobs), {j['out'] for j in jobs}
        self.cv = threading.Condition()

    def take(self, kinds):
        with self.cv:
            while True:
                waiting = False
                for i, j in enumerate(self.jobs):
                    if j.get('kind', 'photo') not in kinds:
                        continue
                    if any(s in self.pending for s in j.get('sources', [j.get('source')])):
                        waiting = True
                        continue
                    return self.jobs.pop(i)
                if not waiting and not any(j.get('kind', 'photo') in kinds for j in self.jobs):
                    return None
                self.cv.wait(5)

    def done(self, job):
        with self.cv:
            self.pending.discard(job['out']); self.cv.notify_all()

    def give_back(self, job):
        with self.cv:
            self.jobs.insert(0, job); self.cv.notify_all()


def save(job, raw, text, lock):
    out = Path(job['out'])
    img = Image.open(raw)
    (whiten(img) if job.get('whiten', True) else img.convert('RGB')).save(out, 'JPEG', quality=85, optimize=True, progressive=True)
    with lock:
        print(f'PHOTO {out.name}\t{text}', flush=True)


def remote_worker(url, queue, tmp, lock):
    """Jobs on a remote HTTP worker: 'photo' (image-to-image from the render, with
    "strength"), 'scene' and 'recolour' (edit mode, the images as references)."""
    import base64, time, urllib.request
    while True:
        job = queue.take({'photo', 'scene', 'recolour'})
        if job is None:
            return
        stem = Path(job['out']).stem
        extra = {}
        if job.get('kind', 'photo') == 'photo':
            src = tmp / f'in-{stem}-r.png'
            on_white(job['render'], src)
            images, extra = [base64.b64encode(src.read_bytes()).decode()], {'strength': STRENGTH}
        else:
            images = [base64.b64encode(Path(s).read_bytes()).decode() for s in job.get('sources', [job['source']])]

        def make(seed, job=job, images=images, extra=extra):
            body = json.dumps({'prompt': job['prompt'], 'seed': seed, 'steps': 4, 'width': SIZE, 'height': SIZE,
                               'images': images, **extra}).encode()
            req = urllib.request.Request(f'{url}/edit', body, {'Content-Type': 'application/json'})
            r = json.loads(urllib.request.urlopen(req, timeout=180).read())   # a job takes ~10-20 s
            if 'error' in r:
                raise RuntimeError(r['error'])
            return r['image']

        try:
            best = None
            for t in range(TRIES):
                raw = tmp / f'{stem}-r{t}.jpg'
                raw.write_bytes(base64.b64decode(make(job['seed'] + t)))
                text = '' if job.get('text_ok') else lettering(raw)
                if best is None or len(text) < len(best[1]):
                    best = (raw, text)
                if not text:
                    break
        except Exception as e:                    # the remote is gone: its job goes back, and we wait for it
            with lock:
                print(f'remote {url} failed ({e}); its job goes back, waiting for it to return', file=sys.stderr, flush=True)
            queue.give_back(job)
            failures = getattr(remote_worker, 'failures', {})
            failures[url] = failures.get(url, 0) + 1
            remote_worker.failures = failures
            if failures[url] >= 3:                # answers /health but no jobs: give up on it
                with lock:
                    print(f'remote {url} failed three times; this machine takes over', file=sys.stderr, flush=True)
                return
            deadline = time.time() + 900
            while time.time() < deadline and queue.jobs:
                try:
                    if json.loads(urllib.request.urlopen(f'{url}/health', timeout=5).read()).get('ready'):
                        break
                except Exception:
                    pass
                time.sleep(15)
            else:
                return
            continue
        save(job, *best, lock)
        queue.done(job)


def main():
    """Jobs run in order: 'photo' (img2img from the render), 'scene' (the edit
    model puts a finished photo into a setting), 'copy' (a size variant gets its
    model's image) and 'recolour' (a colour variant is its model's image with
    only the colour changed, by the edit model). With PHOTO_WORKERS set (URLs of
    HTTP workers that serve the same model, comma-separated), those take 'photo',
    'scene' and 'recolour' jobs in parallel; PHOTO_LOCAL=0 leaves the AI jobs to them."""
    import gc
    import shutil
    import mlx.core as mx
    from mflux.models.common.resolution.config_resolution import ConfigResolution
    from mflux.models.flux2.variants import Flux2Klein, Flux2KleinEdit

    jobs = json.loads(Path(sys.argv[1]).read_text())
    jobs.sort(key=lambda j: ['photo', 'scene', 'copy', 'tint', 'recolour'].index(j.get('kind', 'photo')))
    queue, lock = Queue(jobs), threading.Lock()
    config = ConfigResolution.resolve_restricted(None, 'flux2-klein-4b')
    tmp = Path(tempfile.mkdtemp())
    remotes = [threading.Thread(target=remote_worker, args=(u.strip().rstrip('/'), queue, tmp, lock), daemon=True)
               for u in os.environ.get('PHOTO_WORKERS', '').split(',') if u.strip()]
    for r in remotes:
        r.start()
    model, loaded = None, None
    rounds = 0
    # PHOTO_LOCAL=0: this machine only copies; the AI jobs go to PHOTO_WORKERS (it steps in
    # only when they are gone and their jobs come back).
    local_kinds = {'copy', 'tint'} if remotes and os.environ.get('PHOTO_LOCAL') == '0' else {'photo', 'scene', 'copy', 'recolour'}
    while True:
        job = queue.take(local_kinds if any(r.is_alive() for r in remotes) else {'photo', 'scene', 'copy', 'tint', 'recolour'})
        if job is None:
            # A failing remote hands its job back and then waits for its worker to return:
            # take that job at once instead of waiting with it.
            while any(r.is_alive() for r in remotes) and not queue.jobs:
                time.sleep(1)
            if queue.jobs and any(r.is_alive() for r in remotes):
                local_kinds = {'photo', 'scene', 'copy', 'tint', 'recolour'}
                continue
            rounds += 1
            if queue.jobs and rounds < 3:
                continue
            break
        kind = job.get('kind', 'photo')
        stem, out = Path(job['out']).stem, Path(job['out'])
        out.parent.mkdir(parents=True, exist_ok=True)
        if kind == 'tint':
            from recolour import recolour             # the model's photo recoloured pixel by pixel, no AI
            recolour(job['source'], job['colour'], out)
            with lock:
                print(f'PHOTO {out.name}\t', flush=True)
            queue.done(job)
            continue
        if kind == 'copy':
            shutil.copyfile(job['source'], out)
            with lock:
                print(f'PHOTO {out.name}\t', flush=True)
            queue.done(job)
            continue
        want = Flux2Klein if kind == 'photo' else Flux2KleinEdit
        if loaded is not want:            # one model in memory at a time
            model = None; gc.collect(); mx.clear_cache()
            model, loaded = want(model_config=config, quantize=8), want
        if kind == 'photo':
            src = tmp / f'in-{stem}.png'
            on_white(job['render'], src)
            make = lambda seed: model.generate_image(seed=seed, prompt=job['prompt'], width=SIZE, height=SIZE, guidance=1.0,
                                                     image_path=str(src), image_strength=STRENGTH, num_inference_steps=4,
                                                     scheduler='flow_match_euler_discrete')
        else:
            make = lambda seed: model.generate_image(seed=seed, prompt=job['prompt'], width=SIZE, height=SIZE, guidance=1.0,
                                                     image_paths=[Path(x) for x in job.get('sources', [job['source']])], num_inference_steps=4,
                                                     scheduler='flow_match_euler_discrete')
        raw, text = best_of(make, stem, tmp, job['seed'], job.get('text_ok', False))
        save(job, raw, text, lock)
        queue.done(job)

if __name__ == '__main__':
    main()
