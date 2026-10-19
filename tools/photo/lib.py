"""Modelling kit for the product photos. Runs inside Blender (bpy).

Units are millimetres; a product stands on z=0 with its front facing -Y.
Each builder in tools/photo/models/ is called as build(k, **kwargs), where
k is this module. Shapes only need the right silhouette, proportions and
colours: the AI step adds the surface detail.
"""
import math
import bpy

C = {
    'dark': '#2F343C', 'body': '#4A515C', 'mid': '#7B838F', 'light': '#C9CED6',
    'metal': '#A7AEB8', 'steel': '#CFD3D8', 'paper': '#E6DCCB', 'paperDark': '#CDBFA6',
    'white': '#F7F7F5', 'glass': '#CFE3F0',
}
ACCENT = {'ind': '#E8930C', 'ele': '#2F6FE0', 'off': '#14998C', 'lab': '#C0397B'}
_mats = {}


def rgb(hex_):
    c = [int(hex_[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c] + [1.0]


def mat(color, metal=0.0, rough=0.45, alpha=1.0):
    """A material from a palette name or '#hex'. metal>0 for metal parts."""
    hex_ = C.get(color, color)
    key = (hex_, metal, rough, alpha)
    if key in _mats:
        return _mats[key]
    m = bpy.data.materials.new(f'm{len(_mats)}')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = rgb(hex_)
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if alpha < 1:
        b.inputs['Alpha'].default_value = alpha
        b.inputs['Transmission Weight'].default_value = 0.6
    m.diffuse_color = rgb(hex_)  # workbench / solid colour
    m['hex'] = hex_
    _mats[key] = m
    return m


def _finish(o, color, bevel, rot, **mk):
    o.data.materials.append(mat(color, **mk))
    if rot:
        o.rotation_euler = [math.radians(a) for a in rot]
    if bevel:
        bv = o.modifiers.new('bv', 'BEVEL')
        bv.width, bv.segments, bv.limit_method = bevel, 3, 'ANGLE'
    for p in o.data.polygons:
        p.use_smooth = True
    o.modifiers.new('ws', 'WEIGHTED_NORMAL') if bevel else None
    return o


def box(size, loc, color='body', bevel=0.0, rot=None, **mk):
    """Box of size (x, y, z) centred at loc."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    return _finish(o, color, bevel, rot, **mk)


def cyl(r, h, loc, color='body', bevel=0.0, rot=None, verts=48, r2=None, **mk):
    """Cylinder (or cone with r2) along local Z, centred at loc."""
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=h, location=loc)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=h, location=loc)
    return _finish(bpy.context.object, color, bevel, rot, **mk)


def sphere(r, loc, color='body', scale=(1, 1, 1), **mk):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24)
    o = bpy.context.object
    o.scale = scale
    return _finish(o, color, 0, None, **mk)


def torus(R, r, loc, color='body', rot=None, **mk):
    bpy.ops.mesh.primitive_torus_add(major_radius=R, minor_radius=r, location=loc)
    return _finish(bpy.context.object, color, 0, rot, **mk)


def label(text, loc, size, color='dark', rot=(90, 0, 0), depth=0.2):
    """Raised text, by default standing upright facing -Y (the camera side)."""
    bpy.ops.object.text_add(location=loc)
    o = bpy.context.object
    o.data.body = text
    o.data.size = size
    o.data.extrude = depth
    o.data.align_x, o.data.align_y = 'CENTER', 'CENTER'
    o.data.materials.append(mat(color))
    o.rotation_euler = [math.radians(a) for a in rot]
    return o


def _chaikin(pts, n):
    for _ in range(n):
        q = []
        for i, (x0, y0) in enumerate(pts):
            x1, y1 = pts[(i + 1) % len(pts)]
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        pts = q
    return pts


def slab(points, thick, z=0.0, color='body', round_=None, mirror=False, smooth=2, **mk):
    """A padded flat shape from a 2D outline (list of (x, y)), lying on the floor.

    mirror=True takes a right half (x >= 0) and mirrors it, for symmetric
    garments. round_ is the edge rounding (default: half the thickness).
    """
    if mirror:
        points = list(points) + [(-x, y) for x, y in reversed(points) if x > 0]
    points = _chaikin(list(points), smooth)
    cu = bpy.data.curves.new('slab', 'CURVE')
    cu.dimensions, cu.fill_mode = '2D', 'BOTH'
    sp = cu.splines.new('POLY')
    sp.points.add(len(points) - 1)
    for p, (x, y) in zip(sp.points, points):
        p.co = (x, y, 0, 1)
    sp.use_cyclic_u = True
    r = thick / 2 if round_ is None else round_
    cu.extrude = max(thick / 2 - r, 0.01)
    cu.bevel_depth, cu.bevel_resolution = r, 4
    o = bpy.data.objects.new('slab', cu)
    bpy.context.collection.objects.link(o)
    o.location = (0, 0, z + thick / 2)
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.convert(target='MESH')
    o = bpy.context.object
    o.data.materials.append(mat(color, **mk))
    for f in o.data.polygons:
        f.use_smooth = True
    return o


def profile(points, depth, y=0.0, color='body', round_=None, mirror=False, smooth=2, **mk):
    """A side silhouette (list of (x, z), z up) extruded `depth` mm towards the
    camera and rounded: the natural way to model tools, devices and bottles
    from a side view. The body is centred on y."""
    o = slab(points, depth, 0, color, round_, mirror, smooth, **mk)
    o.rotation_euler = (math.radians(90), 0, 0)
    o.location = (0, y + depth / 2, 0)
    return o
