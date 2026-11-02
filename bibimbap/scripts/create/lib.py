"""Builders for the CREATE answers (ifcopenshell.api, pinned 0.8.3.post2).
Coordinates and sizes are given in metres (world); placements are written with is_si=True,
geometry is converted to the file's length unit."""
import numpy as np
import ifcopenshell, ifcopenshell.api, ifcopenshell.util.unit as uu, ifcopenshell.util.representation as ur
import ifcopenshell.util.placement as up, ifcopenshell.util.element as ue


def run(usecase, f, **kw):
    return ifcopenshell.api.run(usecase, f, **kw)


def _u(f):
    """metres -> file length unit"""
    return 1.0 / uu.calculate_unit_scale(f)


def body_context(f):
    ctx = ur.get_context(f, "Model", "Body", "MODEL_VIEW")
    if ctx is None:
        model = ur.get_context(f, "Model") or next((c for c in f.by_type("IfcGeometricRepresentationContext")
                                                     if not c.is_a("IfcGeometricRepresentationSubContext")), None)
        if model is None:
            model = run("context.add_context", f, context_type="Model")
        ctx = run("context.add_context", f, context_type="Model", context_identifier="Body",
                  target_view="MODEL_VIEW", parent=model)
    return ctx


def storey(f, name=None):
    ss = f.by_type("IfcBuildingStorey")
    if name is not None:
        for s in ss:
            if s.Name == name:
                return s
    return ss[0]


def storey_elevation(s):
    """world z (m) of a storey"""
    return up.get_local_placement(s.ObjectPlacement)[2, 3] * uu.calculate_unit_scale(s.file) if s.ObjectPlacement else 0.0


def mat(x, y, z, xdir=(1.0, 0.0, 0.0)):
    """4x4 placement matrix in metres; local x along xdir (horizontal), local z up."""
    xd = np.array(xdir, float); xd /= np.linalg.norm(xd)
    zd = np.array([0.0, 0.0, 1.0]); yd = np.cross(zd, xd)
    m = np.eye(4); m[:3, 0], m[:3, 1], m[:3, 2], m[:3, 3] = xd, yd, zd, (x, y, z)
    return m


def box_rep(f, ctx, dx, dy, dz, ox=None, oy=None):
    """Extruded rectangle dx*dy (m), height dz (m), bottom at local z=0.
    The rectangle is centred on the local origin unless (ox, oy) gives its centre offset (m)."""
    k = _u(f)
    cx = 0.0 if ox is None else ox
    cy = 0.0 if oy is None else oy
    prof_pos = f.createIfcAxis2Placement2D(f.createIfcCartesianPoint((cx * k, cy * k)), f.createIfcDirection((1.0, 0.0)))
    prof = f.createIfcRectangleProfileDef("AREA", None, prof_pos, dx * k, dy * k)
    pos = f.createIfcAxis2Placement3D(f.createIfcCartesianPoint((0.0, 0.0, 0.0)),
                                      f.createIfcDirection((0.0, 0.0, 1.0)), f.createIfcDirection((1.0, 0.0, 0.0)))
    solid = f.createIfcExtrudedAreaSolid(prof, pos, f.createIfcDirection((0.0, 0.0, 1.0)), dz * k)
    return f.createIfcShapeRepresentation(ctx, "Body", "SweptSolid", [solid])


def new(f, cls, name, rep, matrix, container, contain=True, predefined_type=None):
    """Create an element with a Body representation and an absolute placement.
    container: storey (or None). contain=True -> IfcRelContainedInSpatialStructure,
    contain=False -> IfcRelAggregates (the standard relation for IfcSpace)."""
    kw = dict(ifc_class=cls, name=name)
    if predefined_type:
        kw["predefined_type"] = predefined_type
    el = run("root.create_entity", f, **kw)
    run("geometry.edit_object_placement", f, product=el, matrix=matrix, is_si=True)
    if rep is not None:
        run("geometry.assign_representation", f, product=el, representation=rep)
    if container is not None:
        if contain:
            run("spatial.assign_container", f, products=[el], relating_structure=container)
        else:
            run("aggregate.assign_object", f, products=[el], relating_object=container)
    return el


def wall(f, x1, y1, x2, y2, h, t, st):
    """Wall on the axis (x1,y1)->(x2,y2) (m), thickness t centred on the axis, height h from the storey elevation."""
    L = float(np.hypot(x2 - x1, y2 - y1))
    ctx = body_context(f)
    return new(f, "IfcWall", "Wall", box_rep(f, ctx, L, t, h, ox=L / 2, oy=0.0),
               mat(x1, y1, storey_elevation(st), xdir=(x2 - x1, y2 - y1, 0.0)), st)


def slab(f, x0, y0, x1, y1, z, thk, st):
    """Slab over the rectangle x0..x1, y0..y1 (m), bottom at world z (m)."""
    ctx = body_context(f)
    return new(f, "IfcSlab", "Slab", box_rep(f, ctx, x1 - x0, y1 - y0, thk),
               mat((x0 + x1) / 2, (y0 + y1) / 2, z), st, predefined_type="FLOOR")


def column(f, x, y, z, h, w, d, st):
    """Column w*d (m) centred at (x,y), from world z to z+h (m)."""
    ctx = body_context(f)
    return new(f, "IfcColumn", "Column", box_rep(f, ctx, w, d, h), mat(x, y, z), st, predefined_type="COLUMN")


def _container_of(el):
    c = ue.get_container(el)
    if c is None:
        for r in getattr(el, "Decomposes", ()) or ():
            return r.RelatingObject
    return c


def _wall_body_extent(w):
    """(ymin, ymax, zmin) of the wall Body in the wall's local placement, file units."""
    import ifcopenshell.geom
    s = ifcopenshell.geom.settings()
    sh = ifcopenshell.geom.create_shape(s, w)
    v = np.array(sh.geometry.verts).reshape(-1, 3) / uu.calculate_unit_scale(w.file)
    return v[:, 1].min(), v[:, 1].max(), v[:, 2].min()


def door_in_wall(f, w, u, width, height, door_style="box", depth=0.2):
    """Door of width*height (m) whose centre is u (m) along the wall's local x axis, sill at the wall body bottom.
    An IfcOpeningElement (wall thickness + 20 mm) voids the wall and the door fills it."""
    k = _u(f)
    ctx = body_context(f)
    W = up.get_local_placement(w.ObjectPlacement)          # file units
    ymin, ymax, zmin = _wall_body_extent(w)
    yc = (ymin + ymax) / 2.0
    thick = (ymax - ymin) / k
    local = np.array([u * k, yc, zmin, 1.0])
    p = W @ local                                           # world, file units
    xdir = W[:3, 0]
    M = mat(p[0] / k, p[1] / k, p[2] / k, xdir=(xdir[0], xdir[1], 0.0))
    op = new(f, "IfcOpeningElement", "Opening", box_rep(f, ctx, width, thick + 0.02, height), M, None,
             predefined_type="OPENING")
    run("feature.add_feature", f, feature=op, element=w)
    st = _container_of(w)
    if door_style == "bonsai":
        # Bonsai's parametric door: drawn from its corner on the wall face, lining as deep as the wall
        q = W @ np.array([u * k - width * k / 2, ymin, zmin, 1.0])
        Mb = mat(q[0] / k, q[1] / k, q[2] / k, xdir=(xdir[0], xdir[1], 0.0))
        d = new(f, "IfcDoor", "Door", None, Mb, st)
        rep = run("geometry.add_door_representation", f, context=ctx, overall_height=height * k, overall_width=width * k,
                  lining_properties={"LiningDepth": (ymax - ymin)})
        run("geometry.assign_representation", f, product=d, representation=rep)
    else:
        d = new(f, "IfcDoor", "Door", box_rep(f, ctx, width, depth, height), M, st)
    d.OverallWidth, d.OverallHeight = width * k, height * k
    run("feature.add_filling", f, opening=op, element=d)
    return d
