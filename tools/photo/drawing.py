"""Technical drawing sheets for model SKUs: front, left side and top views in first angle.

Run inside Blender (driven by tools/build-drawings.py):
    blender -b -P tools/photo/drawing.py -- <pack> <out_dir> SKU...

Each SKU is built in an empty scene. Lines are feature edges (dihedral > 30 deg),
boundary edges and silhouettes of the view. Hidden lines are removed by splitting
each edge into pieces of about 1 mm and dropping the pieces whose midpoint a ray
towards the viewer hits geometry for. Writes <out_dir>/<sku lowercase>-drawing.svg.

Axes: X right, Y depth (front faces -Y), Z up, mm, product on z=0.
Views: front looks along +Y (screen x = X, up = Z); left side looks along +X
(screen x = -Y, so the front of the product is on the right, as in first angle);
top looks down (screen x = X, up = +Y, so the front edge is at the bottom).
"""
import bmesh
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from xml.sax.saxutils import escape

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import lib  # noqa: E402

PACK, OUT_DIR, *WANTED = sys.argv[sys.argv.index('--') + 1:]

# Sheet geometry (px), the same frame and title block as tools/build-docs.mjs.
W_SHEET, H_SHEET = 1188, 840
AREA = (40, 40, 1100, 640)            # x, y, width, height of the drawing area
GAP = 70                              # gap between views, also the room for dimensions
import importlib.util as _iu
_ds = _iu.spec_from_file_location('drawings', Path(__file__).with_name('drawings.py')); _dm = _iu.module_from_spec(_ds); _ds.loader.exec_module(_dm)
SIZE_SCALE = getattr(_dm, 'SIZE_SCALE', {})
PIECE = 1.0                           # mm, hidden-line test resolution
INK = '#1f2329'
FONT = 'Helvetica, Arial, sans-serif'
ARROW, TICK = 9, 3


def load_skus():
    """sku -> (builder, kwargs, camera) for every models/<pack>_*.py table."""
    table = {}
    for path in sorted((HERE / 'models').glob(f'{PACK}_*.py')):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for sku, entry in mod.SKUS.items():
            fn, kw, cam = (tuple(entry) + ({}, {}))[:3]
            table[sku] = (fn, kw, cam)
    return table


def product_name(sku):
    for p in json.loads((ROOT / 'packs' / PACK / 'products.json').read_text()):
        if p['sku'] == sku:
            return p['attribute_values']['locale_specific']['en-US']['name']
    raise SystemExit(f'{sku} is not in packs/{PACK}/products.json')


def collect(depsgraph):
    """Edges and vertices of all mesh objects in world space.

    Each edge: (p0, p1, n0, n1, feature); n0/n1 are the face normals (None on a boundary).
    """
    edges, verts = [], []
    for o in [o for o in bpy.context.scene.objects if o.type == 'MESH']:
        bm = bmesh.new()
        bm.from_object(o, depsgraph)
        bm.transform(o.matrix_world)
        bm.normal_update()
        verts += [v.co.copy() for v in bm.verts]
        for ed in bm.edges:
            faces = ed.link_faces
            if len(faces) == 2:
                feature = ed.calc_face_angle(0) > math.radians(30)
                n0, n1 = faces[0].normal.copy(), faces[1].normal.copy()
            else:
                feature, n0, n1 = True, None, None
            edges.append((ed.verts[0].co.copy(), ed.verts[1].co.copy(), n0, n1, feature))
        bm.free()
    return edges, verts


# view name -> (screen u from a point, screen v from a point, direction towards the viewer)
VIEWS = {
    'front': (lambda p: p.x, lambda p: p.z, Vector((0, -1, 0))),
    'side': (lambda p: -p.y, lambda p: p.z, Vector((-1, 0, 0))),
    'top': (lambda p: p.x, lambda p: p.y, Vector((0, 0, 1))),
}


def visible(scene, depsgraph, mid, to_viewer):
    """True when nothing lies between the point and the viewer."""
    hit = scene.ray_cast(depsgraph, mid + to_viewer * 0.02, to_viewer, distance=100000.0)[0]
    return not hit


def view_lines(name, edges, scene, depsgraph, bounds, scale, origin):
    """Visible pieces of one view as merged straight runs in sheet px."""
    fu, fv, to_viewer = VIEWS[name]
    umin, vmax = bounds[name]
    ox, oy = origin

    def px(p):
        return (ox + (fu(p) - umin) * scale, oy + (vmax - fv(p)) * scale)

    out = []
    for p0, p1, n0, n1, feature in edges:
        if not feature:
            # Smooth-surface silhouette: the two faces face opposite ways to the viewer.
            if n0 is None or (n0.dot(to_viewer) * n1.dot(to_viewer)) >= 0:
                continue
        length = (p1 - p0).length
        n = min(1500, max(1, math.ceil(length / PIECE)))
        vis = [visible(scene, depsgraph, p0 + (p1 - p0) * ((k + 0.5) / n), to_viewer) for k in range(n)]
        k = 0
        while k < n:
            if not vis[k]:
                k += 1
                continue
            end = k
            while end + 1 < n and vis[end + 1]:
                end += 1
            a, b = px(p0 + (p1 - p0) * (k / n)), px(p0 + (p1 - p0) * ((end + 1) / n))
            out.append((a, b))
            k = end + 1
    return out


def line_svg(a, b, width):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke-width="{width}"/>'


def dimension(horizontal, start, end, offset, value_mm, edge):
    """Dimension line from start to end (sheet px) at sheet coordinate offset.

    horizontal: the dimension runs along x and offset is its y. Otherwise it runs along y
    and offset is its x. edge is the object's edge the extension lines leave from (y for a
    horizontal dimension, x for a vertical one), with a 3 px gap.
    """
    text = f'{round(value_mm)} mm'
    parts = []
    if horizontal:
        y = offset
        for x in (start, end):
            parts.append(line_svg((x, edge + TICK), (x, y + 5), 0.8))
        parts.append(line_svg((start, y), (end, y), 0.8))
        parts.append(f'<polygon points="{start:.1f},{y:.1f} {start + ARROW:.1f},{y - TICK:.1f} '
                     f'{start + ARROW:.1f},{y + TICK:.1f}" fill="{INK}"/>')
        parts.append(f'<polygon points="{end:.1f},{y:.1f} {end - ARROW:.1f},{y - TICK:.1f} '
                     f'{end - ARROW:.1f},{y + TICK:.1f}" fill="{INK}"/>')
        parts.append(f'<text x="{(start + end) / 2:.1f}" y="{y - 6:.1f}" font-size="13" '
                     f'text-anchor="middle" font-family="{FONT}">{text}</text>')
    else:
        x = offset
        for y in (start, end):
            parts.append(line_svg((edge - TICK, y), (x - 5, y), 0.8))
        parts.append(line_svg((x, start), (x, end), 0.8))
        parts.append(f'<polygon points="{x:.1f},{start:.1f} {x - TICK:.1f},{start + ARROW:.1f} '
                     f'{x + TICK:.1f},{start + ARROW:.1f}" fill="{INK}"/>')
        parts.append(f'<polygon points="{x:.1f},{end:.1f} {x - TICK:.1f},{end - ARROW:.1f} '
                     f'{x + TICK:.1f},{end - ARROW:.1f}" fill="{INK}"/>')
        parts.append(f'<text transform="translate({x - 8:.1f} {(start + end) / 2:.1f}) rotate(-90)" '
                     f'font-size="13" text-anchor="middle" font-family="{FONT}">{text}</text>')
    return ''.join(parts)


def sheet(sku, name, edges, verts, scene, depsgraph):
    xs = [v.x for v in verts]
    ys = [v.y for v in verts]
    zs = [v.z for v in verts]
    W, D, H = max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)
    ax, ay, aw, ah = AREA
    scale = min((aw - 2 * GAP) / (W + D), (ah - GAP) / (H + D))
    total_h = H * scale + GAP + D * scale
    # Column 1: front and top. Column 2: left side. Row 1: front and side, row 2: top.
    x1 = ax + (aw - (2 * GAP + (W + D) * scale)) / 2 + GAP
    y1 = ay + (ah - total_h) / 2
    x2 = x1 + W * scale + GAP
    y2 = y1 + H * scale + GAP
    origins = {'front': (x1, y1), 'side': (x2, y1), 'top': (x1, y2)}
    # (umin, vmax) of each view in model mm; the side view's u is -Y.
    bounds = {'front': (min(xs), max(zs)), 'side': (-max(ys), max(zs)), 'top': (min(xs), max(ys))}

    lines = []
    for view in ('front', 'side', 'top'):
        lines += view_lines(view, edges, scene, depsgraph, bounds, scale, origins[view])
    body = ''.join(line_svg(a, b, 1.4) for a, b in lines)

    yd = y1 + H * scale + GAP / 2
    k = SIZE_SCALE.get(sku, 1.0)   # the model is smaller than the product: label the real size
    dims = [dimension(True, x1, x1 + W * scale, yd, W * k, y1 + H * scale + TICK),
            dimension(True, x2, x2 + D * scale, yd, D * k, y1 + H * scale + TICK),
            dimension(False, y1, y1 + H * scale, x1 - GAP / 2, H * k, x1)]
    dims = ''.join(dims)

    title = escape(product_name(sku))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W_SHEET} {H_SHEET}" width="{W_SHEET}" height="{H_SHEET}" font-family="{FONT}">
  <rect x="10" y="10" width="1168" height="820" fill="#fff" stroke="{INK}" stroke-width="2"/>
  <g stroke="{INK}" fill="none" stroke-linecap="round">{body}</g>
  <g stroke="{INK}" fill="none">{dims}</g>
  <g transform="translate(748 700)">
    <rect width="420" height="120" fill="#fff" stroke="{INK}" stroke-width="2"/>
    <line x1="0" y1="40" x2="420" y2="40" stroke="{INK}"/><line x1="0" y1="80" x2="420" y2="80" stroke="{INK}"/>
    <line x1="280" y1="40" x2="280" y2="120" stroke="{INK}"/>
    <text x="12" y="27" font-size="17" font-weight="700">{title}</text>
    <text x="12" y="66" font-size="14">{escape(sku)}</text><text x="292" y="66" font-size="14">Not to scale</text>
    <text x="12" y="106" font-size="13" fill="#b42318" font-weight="700">SAMPLE — fictional product</text><text x="292" y="106" font-size="14">mm</text>
  </g></svg>
'''


def main():
    table = load_skus()
    out = Path(OUT_DIR)
    out.mkdir(parents=True, exist_ok=True)
    for sku in WANTED:
        if sku not in table:
            raise SystemExit(f'{sku} has no builder in models/{PACK}_*.py')
        t0 = time.time()
        fn, kw, _cam = table[sku]
        bpy.ops.wm.read_factory_settings(use_empty=True)
        lib._mats.clear()
        fn(lib, **kw)
        scene = bpy.context.scene
        depsgraph = bpy.context.evaluated_depsgraph_get()
        edges, verts = collect(depsgraph)
        svg = sheet(sku, sku, edges, verts, scene, depsgraph)
        target = out / f'{sku.lower()}-drawing.svg'
        target.write_text(svg)
        print(f'DRAWING {sku} {len(edges)} edges {time.time() - t0:.1f}s -> {target}', flush=True)


main()
