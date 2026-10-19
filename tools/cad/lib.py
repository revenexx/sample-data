"""Shared parametric builders for the STEP models (development tool only).

Every builder returns a CadQuery Workplane, units mm. Parts are simplified on
purpose: correct outer dimensions and shape, no modelled thread, no text.
Fasteners and tubes stand along Z (head / open end at the top or at z=0 as
noted in each function); DIN-rail devices have the rail along X, height along
Y and the front face towards +Z.
"""
import math

import cadquery as cq


def revolve(profile):
    """Revolve a closed (r, z) polyline around the Z axis."""
    return cq.Workplane("XZ").polyline(profile).close().revolve(360, (0, 0, 0), (0, 1, 0))


def hollow_revolve(outer, inner):
    return revolve(outer).cut(revolve(inner))


# ---------------------------------------------------------------- fasteners
def hex_bolt(d, length, s, k):
    """ISO 4017 hex bolt: head on z 0..k, shank down is +Z from the head (as the existing M8 model)."""
    head = cq.Workplane("XY").polygon(6, s / math.cos(math.pi / 6)).extrude(k).edges(">Z or <Z").chamfer(0.05 * s)
    shank = cq.Workplane("XY").workplane(offset=k).circle(d / 2).extrude(length)
    return head.union(shank).faces(">Z").edges().chamfer(0.08 * d)


def countersunk_screw(d, length, head_d, drive="cross", tip=None):
    """Countersunk wood screw, 90 degree head, length measured from the flat top."""
    head_h = (head_d - d) / 2
    tip = tip or d
    head = cq.Workplane("XY").circle(head_d / 2).workplane(offset=head_h).circle(d / 2).loft()
    shank = cq.Workplane("XY").workplane(offset=head_h).circle(d / 2).extrude(length - head_h - tip)
    point = cq.Workplane("XY").workplane(offset=length - tip).circle(d / 2).workplane(offset=tip).circle(0.2).loft()
    body = head.union(shank).union(point)
    recess = cq.Workplane("XY").rect(d * 0.55, d * 0.55).extrude(d * 0.4)
    return body.cut(recess)


def pan_screw(d, length, head_d, head_h, point_tip=0.0):
    """Pan head screw (ISO 7045 / ISO 7049): rounded head on top, shank below; total length = head_h + length."""
    head = (cq.Workplane("XY").circle(head_d / 2).extrude(head_h)).edges("<Z").fillet(head_h * 0.45)
    shank = cq.Workplane("XY").workplane(offset=head_h).circle(d / 2).extrude(length)
    body = head.union(shank)
    if point_tip:
        body = body.faces(">Z").edges().chamfer(point_tip)
    recess = cq.Workplane("XY").rect(head_d * 0.5, 0.8).extrude(head_h * 0.5).union(
        cq.Workplane("XY").rect(0.8, head_d * 0.5).extrude(head_h * 0.5))
    return body.cut(recess)


def cheese_screw(d, length, head_d, head_h, socket):
    """DIN 912 / ISO 4762 socket cap (cheese) head screw."""
    head = cq.Workplane("XY").circle(head_d / 2).extrude(head_h).edges("<Z").chamfer(0.04 * head_d)
    shank = cq.Workplane("XY").workplane(offset=head_h).circle(d / 2).extrude(length)
    sock = cq.Workplane("XY").polygon(6, socket / math.cos(math.pi / 6)).extrude(head_h * 0.55)
    return head.union(shank).faces(">Z").edges().chamfer(0.08 * d).cut(sock)


def grub_screw(d, length, socket):
    """ISO 4029 set screw, cup point: a headless cylinder with hex socket."""
    body = cq.Workplane("XY").circle(d / 2).extrude(length).faces("<Z or >Z").edges().chamfer(0.1 * d)
    sock = cq.Workplane("XY").polygon(6, socket / math.cos(math.pi / 6)).extrude(d * 0.5)
    return body.cut(sock)


def hex_nut(d, s, m):
    """ISO 4032 hex nut with bore d."""
    n = cq.Workplane("XY").polygon(6, s / math.cos(math.pi / 6)).extrude(m).edges(">Z or <Z").chamfer(0.05 * s)
    return n.cut(cq.Workplane("XY").circle(d / 2).extrude(m))


def square_nut(d, s, m):
    n = cq.Workplane("XY").rect(s, s).extrude(m)
    return n.cut(cq.Workplane("XY").circle(d / 2).extrude(m))


def washer(d_in, d_out, t):
    return cq.Workplane("XY").circle(d_out / 2).circle(d_in / 2).extrude(t)


def rod(d, length):
    return cq.Workplane("XY").circle(d / 2).extrude(length).faces("<Z or >Z").edges().chamfer(0.05 * d)


def plug(d, length, collar_d, collar_t=1.0, bore=None):
    """Expansion plug: hollow sleeve with a flat collar, a slit pair at the tip."""
    bore = bore or d * 0.55
    body = cq.Workplane("XY").circle(collar_d / 2).extrude(collar_t).union(
        cq.Workplane("XY").circle(d / 2).extrude(length))
    body = body.cut(cq.Workplane("XY").circle(bore / 2).extrude(length))
    slit = cq.Workplane("XY").workplane(offset=length * 0.45).rect(d + 1, 1.2).extrude(length * 0.6)
    return body.cut(slit)


def nail(d, length, head_d, head_t=0.8):
    head = cq.Workplane("XY").circle(head_d / 2).extrude(head_t)
    shank = cq.Workplane("XY").workplane(offset=head_t).circle(d / 2).extrude(length - head_t - 3 * d)
    point = cq.Workplane("XY").workplane(offset=length - 3 * d).circle(d / 2).workplane(offset=3 * d).circle(0.1).loft()
    return head.union(shank).union(point)


def cable_tie(length, width, thick=1.0, head=(7.5, 5.5, 3.5)):
    strap = cq.Workplane("XY").box(length - head[0], width, thick, centered=(False, True, False)).translate((head[0], 0, 0))
    hd = cq.Workplane("XY").box(head[0], head[1], head[2], centered=(False, True, False))
    hole = cq.Workplane("XY").box(head[0] * 0.5, head[1] + 1.0, thick + 0.4, centered=(False, True, False)).translate((head[0] * 0.25, 0, 0.8))
    return strap.union(hd).cut(hole)


def disc(outer, thickness, bore=22.23):
    return cq.Workplane("XY").circle(outer / 2).circle(bore / 2).extrude(thickness)


def flap_disc(outer=115.0, bore=22.23, height=13.0):
    """Conical flap disc (type 29): backing hub, flaps sloping outwards; overall height `height`."""
    ro, ri = outer / 2, 30.0
    return revolve([(bore / 2, height - 3.0), (bore / 2, height), (ri, height), (ro, 4.0), (ro, 0.0),
                    (ro - 7.0, 0.0), (ri - 5.0, height - 4.0), (bore / 2 + 4.0, height - 4.0), (bore / 2 + 4.0, height - 3.0)])


# -------------------------------------------------------------- DIN-rail devices
MODULE = 17.5


def din_device(modules, poles=None, depth=68.0, nose_from=45.0, lever=True, test_button=False, width=None):
    """Modular DIN-rail device (EN 60715 TH35 rail, 90 mm high, 17.5 mm per module, 45 mm wide front nose).
    Rail along X, height along Y, mounting face at z=0, front towards +Z; overall depth = `depth` (lever included)."""
    w = width or modules * MODULE
    lever_h = 6.0 if lever else 0.0
    body = cq.Workplane("XY").box(w, 90.0, nose_from, centered=(True, True, False)).edges("|X").fillet(1.0)
    nose = (cq.Workplane("XY").workplane(offset=nose_from).box(w - 0.8, 45.0, depth - lever_h - nose_from, centered=(True, True, False))
            .edges("|X").fillet(2.0))
    dev = body.union(nose)
    dev = dev.cut(cq.Workplane("XY").box(w + 2, 35.4, 2.2, centered=(True, True, False)))  # TH35 rail groove, 2.2 deep
    dev = dev.cut(cq.Workplane("XY").box(w * 0.6, 4.0, 1.5, centered=(True, True, False)).translate((0, 24.5, 0)))
    if lever:
        n = poles or modules
        pitch = w / n
        for i in range(n):
            x = -w / 2 + pitch * (i + 0.5)
            dev = dev.union(cq.Workplane("XY").box(min(pitch * 0.55, 9.0), 13.0, lever_h + 0.5, centered=(True, True, False))
                            .translate((x, 6.0, depth - lever_h - 0.5)))
    if test_button:
        dev = dev.union(cq.Workplane("XY").circle(3.5).extrude(1.5).translate((0, -10.0, depth - 6.0 - 0.2)))
    return dev


def din_enclosure(w, h, d, wall=2.5):
    """Distribution board housing (open at the front, lid left off): rounded shell with a hinge-less frame."""
    body = cq.Workplane("XY").box(w, h, d, centered=(True, True, False)).edges("|Z").fillet(6.0)
    return body.faces(">Z").shell(-wall)


def terminal_block(w, h=42.0, depth=36.0, wire=2.5):
    """Feed-through terminal block on a TH35 rail: thin slice w wide (along rail X), h tall, depth above the rail seat."""
    b = cq.Workplane("XY").box(w, h, depth, centered=(True, True, False)).edges("|X").fillet(1.0)
    b = b.cut(cq.Workplane("XY").box(w + 1, 35.4, 1.8, centered=(True, True, False)))  # rail seat
    bore = min(w * 0.55, 1.1 * math.sqrt(wire) + 1.0)
    for sgn in (1, -1):  # wire entries at both ends, holes run along Y
        b = b.cut(cq.Workplane("XY").box(bore, 9.0, bore, centered=(True, True, True)).translate((0, sgn * (h / 2 - 4.5), depth * 0.35)))
    b = b.cut(cq.Workplane("XY").workplane(offset=depth - 1.5).circle(min(w * 0.3, 2.0)).extrude(2.0))  # screw recess
    return b


def gland(thread, af, total, thread_len, bore, hex_h=6.0):
    """Cable gland: thread, hex body, dome nut; bore through."""
    th = cq.Workplane("XY").circle(thread / 2).extrude(thread_len)
    hx = cq.Workplane("XY").workplane(offset=thread_len).polygon(6, af / math.cos(math.pi / 6)).extrude(hex_h).edges(">Z or <Z").chamfer(0.5)
    nut_h = total - thread_len - hex_h
    nut = cq.Workplane("XY").workplane(offset=thread_len + hex_h).circle(af / 2 - 0.5).extrude(nut_h).faces(">Z").edges().fillet(2.0)
    g = th.union(hx).union(nut)
    return g.cut(cq.Workplane("XY").circle(bore / 2).extrude(total))


def cup_box(dia, depth, wall=1.8, flange=None):
    """Flush-mounted round device box, open at the top (z = depth)."""
    b = cq.Workplane("XY").circle(dia / 2).extrude(depth)
    b = b.faces(">Z").shell(-wall)
    # two internal screw bosses
    for x in (-dia * 0.3, dia * 0.3):
        b = b.union(cq.Workplane("XY").workplane(offset=wall).center(x, 0).circle(3.0).extrude(depth - wall - 3.0))
    return b


def surface_housing(w, h, d, wall=2.5, entries=True):
    b = cq.Workplane("XY").box(w, h, d, centered=(True, True, False)).edges("|Z").fillet(6.0).faces(">Z").shell(-wall)
    return b


def trunking(w, h, length=2000.0, wall=1.4):
    """Cable trunking with lid, closed hollow rectangle (lid seam as a 0.4 mm groove on the front)."""
    o = cq.Workplane("XY").rect(w, h).extrude(length)
    o = o.cut(cq.Workplane("XY").rect(w - 2 * wall, h - 2 * wall).extrude(length))
    return o


def ferrule(copper_d, bore, contact_len, collar_d, collar_len):
    """Insulated wire end ferrule (DIN 46228-4): copper sleeve plus plastic collar."""
    cu = cq.Workplane("XY").circle(copper_d / 2).extrude(contact_len + collar_len)
    col = cq.Workplane("XY").workplane(offset=contact_len).circle(collar_d / 2).extrude(collar_len)
    return cu.union(col).cut(cq.Workplane("XY").circle(bore / 2).extrude(contact_len + collar_len))


def terminal_strip(poles, pitch, width, height):
    """Screw terminal strip (Luesterklemme)."""
    L = poles * pitch
    b = cq.Workplane("XY").box(L, width, height, centered=(True, True, False)).edges("|Z").fillet(0.8)
    for i in range(poles):
        x = -L / 2 + pitch * (i + 0.5)
        b = b.union(cq.Workplane("XY").workplane(offset=height).center(x, 0).circle(pitch * 0.3).extrude(0.8))
        for y in (-1, 1):
            b = b.cut(cq.Workplane("XY").box(pitch * 0.5, 3.0, 3.0, centered=(True, True, False)).translate((x, y * width / 2, 2.5)))
    return b


def device_insert(plate=55.0, plate_t=3.0, body=50.0, body_depth=28.0, rocker=44.0, rocker_h=6.0, knob_d=None, rockers=1):
    """Flush-mounted switch insert with cover plate 55 x 55 (front at +Z). Body behind the plate."""
    p = cq.Workplane("XY").box(plate, plate, plate_t, centered=(True, True, False)).edges("|Z").fillet(3.0)
    b = cq.Workplane("XY").box(body, body, body_depth, centered=(True, True, False)).translate((0, 0, -body_depth)).edges("|Z").fillet(3.0)
    dev = p.union(b)
    if knob_d:
        dev = dev.union(cq.Workplane("XY").workplane(offset=plate_t).circle(knob_d / 2).extrude(rocker_h).faces(">Z").edges().fillet(1.5))
    elif rockers == 2:
        for y in (-1, 1):
            dev = dev.union(cq.Workplane("XY").box(rocker, rocker / 2 - 1.5, rocker_h, centered=(True, True, False))
                            .translate((0, y * rocker / 4, plate_t)).edges("|X and >Z").fillet(1.5))
    else:
        dev = dev.union(cq.Workplane("XY").box(rocker, rocker, rocker_h, centered=(True, True, False))
                        .translate((0, 0, plate_t)).edges(">Z").fillet(2.0))
    return dev


def cover_frame(gangs, pitch=71.0, size=80.5, t=9.0, window=55.0):
    """Cover frame for 1..3 gang (80.5 mm frame, 71 mm centre spacing, 55 mm windows)."""
    L = size + pitch * (gangs - 1)
    f = cq.Workplane("XY").box(L, size, t, centered=(True, True, False)).edges("|Z").fillet(6.0).edges(">Z").fillet(1.5)
    for i in range(gangs):
        x = -pitch * (gangs - 1) / 2 + pitch * i
        f = f.cut(cq.Workplane("XY").box(window, window, t, centered=(True, True, False)).translate((x, 0, 0)))
    return f


def sockets(gangs, plate_w=80.0, pitch=71.0, depth=36.0, plate=4.0):
    """Schuko flush socket outlets (1 or 2 gang): cover plate with a round recess per socket, body behind. Front at +Z."""
    L = plate_w + pitch * (gangs - 1)
    out = cq.Workplane("XY").box(L, plate_w, plate, centered=(True, True, False)).edges("|Z").fillet(7.0)
    for i in range(gangs):
        x = -pitch * (gangs - 1) / 2 + pitch * i
        out = out.union(cq.Workplane("XY").box(plate_w - 12, plate_w - 12, depth, centered=(True, True, False))
                        .translate((x, 0, -depth)).edges("|Z").fillet(4.0))
    for i in range(gangs):
        x = -pitch * (gangs - 1) / 2 + pitch * i
        out = out.cut(cq.Workplane("XY").workplane(offset=plate - 2.0).center(x, 0).circle(19.0).extrude(2.0))
        for dx in (-10.0, 10.0):
            out = out.cut(cq.Workplane("XY").workplane(offset=plate - 6.0).center(x + dx, 0).circle(2.4).extrude(6.0))
    return out


def surface_socket(w=80.0, d=50.0):
    b = surface_housing(w, w, d, wall=3.0)
    lid = cq.Workplane("XY").box(w, w, 4.0, centered=(True, True, False)).edges("|Z").fillet(6.0)
    lid = lid.cut(cq.Workplane("XY").circle(19.5).extrude(4.0))
    return b.union(lid.translate((0, 0, d - 4.0))).union(
        cq.Workplane("XY").workplane(offset=d - 4.0).circle(23.0).circle(19.5).extrude(4.0))


# ---------------------------------------------------------------- lab
def tube(length, body_d, tip_d, cone_h, cap_d, cap_h):
    return revolve([(0, 0), (tip_d / 2, 0), (body_d / 2, cone_h), (body_d / 2, length - cap_h),
                    (cap_d / 2, length - cap_h), (cap_d / 2, length), (0, length)])


def pipette_tip(length, top_d, tip_d, wall=0.4, cone_len=None):
    """Hollow pipette tip, orifice at z=0. Cone to top_d over cone_len, then cylindrical collar."""
    cone_len = cone_len or length * 0.74
    outer = revolve([(0, 0), (tip_d / 2 + 0.1, 0), (top_d / 2, cone_len), (top_d / 2, length), (0, length)])
    inner = revolve([(0, -1.0), (tip_d / 2 - 0.1, -1.0), (top_d / 2 - wall, cone_len), (top_d / 2 - wall, length + 1), (0, length + 1)])
    return outer.cut(inner)


def plate_grid(length, width, height, nx, ny, x0, y0, pitch_x, pitch_y, well_d=None, well_sq=None, depth=10.0, corner=3.0):
    """Microplate / rack-like block: footprint length x width x height with a grid of wells cut from the top."""
    b = cq.Workplane("XY").box(length, width, height, centered=False).edges("|Z").fillet(corner)
    pts = [(x0 + i * pitch_x, y0 + j * pitch_y) for j in range(ny) for i in range(nx)]
    wp = cq.Workplane("XY").workplane(offset=height - depth).pushPoints(pts)
    cut = wp.circle(well_d / 2).extrude(depth + 1) if well_d else wp.rect(well_sq, well_sq).extrude(depth + 1)
    return b.cut(cut)


def tube_rack(length, width, height, nx, ny, pitch, hole_d, plate_t=3.0, foot_d=None):
    """Two-deck tube rack: top plate with holes, bottom plate with smaller holes, two end walls."""
    foot_d = foot_d or hole_d * 0.7
    x0 = (length - (nx - 1) * pitch) / 2
    y0 = (width - (ny - 1) * pitch) / 2
    pts = [(x0 + i * pitch, y0 + j * pitch) for j in range(ny) for i in range(nx)]
    top = cq.Workplane("XY").box(length, width, plate_t, centered=False).translate((0, 0, height - plate_t))
    top = top.cut(cq.Workplane("XY").workplane(offset=height - plate_t).pushPoints(pts).circle(hole_d / 2).extrude(plate_t))
    bot = cq.Workplane("XY").box(length, width, plate_t, centered=False)
    bot = bot.cut(cq.Workplane("XY").pushPoints(pts).circle(foot_d / 2).extrude(plate_t))
    walls = cq.Workplane("XY").box(plate_t, width, height, centered=False).union(
        cq.Workplane("XY").box(plate_t, width, height, centered=False).translate((length - plate_t, 0, 0)))
    return top.union(bot).union(walls)


def glass_revolve(outer_pts, wall):
    """outer_pts: [(r,z), ...] from the bottom centre up to the rim outer edge. Inner = same shape shrunk by wall (r only, z raised at bottom)."""
    top = outer_pts[-1][1]
    outer = revolve(outer_pts + [(0, top)])
    inner_pts = [(max(r - wall, 0.0) if i else 0.0, z + (wall if i == 0 else 0)) for i, (r, z) in enumerate(outer_pts)]
    inner_pts[-1] = (outer_pts[-1][0] - wall, top + 1)
    inner = revolve(inner_pts + [(0, top + 1)])
    return outer.cut(inner)


def arc_pts(cx, cz, r, a0, a1, n=10):
    return [(cx + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), cz + r * math.cos(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def export_step(wp, path):
    """Write a part as proper solids (a compound of its Solid objects), not as a surface model."""
    import cadquery as cq_
    solids = [s for v in wp.vals() for s in v.Solids()]
    cq_.exporters.export(cq_.Workplane(obj=cq_.Compound.makeCompound(solids)), str(path))
