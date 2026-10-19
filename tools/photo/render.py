"""Render product models to studio images with Blender (step 1 of the photos).

Run through tools/build-photos.py, which calls:

    blender -b -P tools/photo/render.py -- <pack> hashes <out.json>
    blender -b -P tools/photo/render.py -- <pack> render <out dir> <SKU> ...

`hashes` writes {sku: {hash, hint}} for every SKU the pack's model modules list, so
the build can skip unchanged products. `preview <dir> [SKU ...]` is a quick
Workbench render for checking models. `render` writes <out dir>/<sku>.png,
800 x 800 with a transparent background and the floor shadow in alpha.

The look: white studio, soft key light, strong front light, camera from the
front left and a little above, the product framed by its projected outline.
"""
import hashlib, importlib.util, inspect, json, math, os, sys
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lib  # noqa: E402

pack, mode, *rest = sys.argv[sys.argv.index('--') + 1:]


def load_models():
    """All SKUS tables of models/<pack>*.py: sku -> (module, builder, kwargs, camera)."""
    table = {}
    for path in sorted((HERE / 'models').glob(f'{pack}*.py')):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for sku, entry in mod.SKUS.items():
            fn, kw, cam = (tuple(entry) + ({}, {}))[:3]
            if sku in table:
                raise SystemExit(f'{sku} is listed twice ({table[sku][0].__name__} and {mod.__name__})')
            table[sku] = (mod, fn, kw, cam)
    return table


MODELS = load_models()


def model_hash(sku):
    mod, fn, kw, cam = MODELS[sku]
    h = hashlib.sha256()
    # Only this product's own builder counts (plus its arguments, the kit and this file), so editing
    # one builder in a module no longer marks every product of that module as changed. A change to
    # a module-level helper is not seen: rebuild those products with --force.
    source = inspect.getsource(fn)
    for part in (source, json.dumps(kw, sort_keys=True), json.dumps(cam, sort_keys=True),
                 (HERE / 'lib.py').read_text(), Path(__file__).read_text()):
        h.update(part.encode())
    return h.hexdigest()[:16]


def area(scene, name, energy, rot, size, centre, radius):
    L = bpy.data.lights.new(name, 'AREA')
    L.size = radius * size
    L.energy = energy * (radius * 4) ** 2 * 0.5
    o = bpy.data.objects.new(name, L)
    scene.collection.objects.link(o)
    o.rotation_euler = [math.radians(a) for a in rot]
    o.location = centre + (o.rotation_euler.to_matrix() @ Vector((0, 0, 1))) * radius * 4


def render(sku, out, preview=False):
    mod, fn, kw, cam = MODELS[sku]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    lib._mats.clear()
    fn(lib, **kw)
    scene = bpy.context.scene
    bpy.context.view_layer.update()
    objs = [o for o in scene.objects if o.type in ('MESH', 'FONT')]
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector([min(p[i] for p in pts) for i in range(3)])
    hi = Vector([max(p[i] for p in pts) for i in range(3)])
    centre, radius = (lo + hi) / 2, (hi - lo).length / 2

    # Camera: aim, then move it until the projected outline fills `fill` of the frame.
    yaw, pitch, fill = cam.get('yaw', -30), cam.get('pitch', 18), cam.get('fill', 0.74)
    cd = bpy.data.cameras.new('cam'); cd.lens = 85
    camo = bpy.data.objects.new('cam', cd); scene.collection.objects.link(camo); scene.camera = camo
    yr, pr = math.radians(yaw), math.radians(pitch)
    d = Vector((math.sin(yr) * math.cos(pr), -math.cos(yr) * math.cos(pr), math.sin(pr)))
    camo.location = centre + d * radius * 6
    camo.rotation_euler = (-d).to_track_quat('-Z', 'Y').to_euler()
    cd.clip_end = radius * 200
    for _ in range(4):
        bpy.context.view_layer.update()
        inv = camo.matrix_world.inverted()
        cs = [inv @ p for p in pts]
        xs, ys = [c.x / -c.z for c in cs], [c.y / -c.z for c in cs]
        cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
        ext = max(max(xs) - min(xs), max(ys) - min(ys))
        R = camo.matrix_world.to_3x3()
        depth = (inv @ centre).length
        camo.location += R @ Vector((cx * depth, cy * depth, 0))
        camo.location += R @ Vector((0, 0, depth * (ext / (2 * math.tan(cd.angle / 2) * fill) - 1)))

    if preview:  # a quick check of shape and colour (about 2 s), not the final look
        r = scene.render
        r.engine = 'BLENDER_WORKBENCH'
        r.resolution_x = r.resolution_y = 400
        sh = scene.display.shading
        sh.light, sh.color_type, sh.show_shadows, sh.show_cavity = 'STUDIO', 'MATERIAL', True, True
        r.film_transparent = True
        r.filepath = str(out)
        bpy.ops.render.render(write_still=True)
        return

    # A floor that only catches shadows, a white world, four soft area lights.
    bpy.ops.mesh.primitive_plane_add(size=radius * 40, location=(centre.x, centre.y, lo.z))
    bpy.context.object.is_shadow_catcher = True
    r = scene.render
    r.engine = 'CYCLES'
    scene.cycles.samples, scene.cycles.use_denoising = 64, True
    if os.environ.get('PHOTO_DEVICE') == 'CPU':   # leaves the GPU to the AI step running alongside
        scene.cycles.device = 'CPU'
        r.threads_mode, r.threads = 'FIXED', int(os.environ.get('PHOTO_THREADS', '6'))
    else:
        scene.cycles.device = 'GPU'
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'METAL'; prefs.get_devices()
        for dv in prefs.devices:
            dv.use = True
    r.resolution_x = r.resolution_y = 800
    r.film_transparent = True
    scene.view_settings.view_transform = 'Standard'
    scene.view_settings.exposure = 0.2
    w = bpy.data.worlds.new('w'); scene.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.8
    area(scene, 'key', 5, (45, 0, -40), 3, centre, radius)
    area(scene, 'fill', 1.4, (60, 0, 70), 6, centre, radius)
    area(scene, 'top', 1.0, (0, 0, 0), 5, centre, radius)
    area(scene, 'front', 6, (90 - pitch - 12, 0, yaw), 5, centre, radius)
    r.filepath = str(out)
    bpy.ops.render.render(write_still=True)


if mode == 'hashes':
    hints = {}
    for mod, *_ in MODELS.values():
        hints.update(getattr(mod, 'HINTS', {}))
    Path(rest[0]).write_text(json.dumps({sku: {'hash': model_hash(sku), 'hint': hints.get(sku, '')} for sku in sorted(MODELS)}, indent=1))
elif mode in ('render', 'preview'):
    out_dir = Path(rest[0]); out_dir.mkdir(parents=True, exist_ok=True)
    for sku in rest[1:] or sorted(MODELS):
        render(sku, out_dir / f'{sku.lower()}.png', preview=mode == 'preview')
        print(f'RENDERED {sku}', flush=True)
else:
    raise SystemExit(f'unknown mode {mode}')
