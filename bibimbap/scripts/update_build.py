# Build "perfect answer" edited IFCs for the 15 BIBIMBAP update tasks.
# Answers are derived from the prompt + model geometry (see comments), not from the tests.
import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ifcopenshell, ifcopenshell.util.element as ue, ifcopenshell.util.placement as up
from edits import world, set_world, translate, rotate_z_about
from common import bbox

D = "/tmp/bib/olddata/data/ifc/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def body_rep(e):
    for r in e.Representation.Representations:
        if r.RepresentationIdentifier == "Body":
            return r


def unmap_rep(f, e, ident="Body"):
    """Give e an occurrence-specific copy of a mapped representation (the type map stays untouched)."""
    reps = list(e.Representation.Representations)
    for i, r in enumerate(reps):
        if r.RepresentationIdentifier != ident:
            continue
        if r.RepresentationType != "MappedRepresentation":
            return r
        items = []
        for mi in r.Items:
            src = mi.MappingSource
            # all MappingOrigin / MappingTarget in these files are identity (checked)
            for it in src.MappedRepresentation.Items:
                items.append(ue.copy_deep(f, it))
            rtype = src.MappedRepresentation.RepresentationType
        nr = f.createIfcShapeRepresentation(r.ContextOfItems, r.RepresentationIdentifier, rtype, items)
        reps[i] = nr
        e.Representation.Representations = reps
        return nr


def center_world_mm(e):
    mn, mx = bbox(e)
    return (mn + mx) / 2 * 1000.0


def save(f, name):
    p = os.path.join(OUT, name + ".ifc")
    f.write(p)
    return p


# ---------------------------------------------------------------- basic_tasks.ifc
def t11(variant="center"):
    """Rotate wall 22hyxv... by +90deg about z. Natural: rotate in place about the wall's own centre."""
    f = ifcopenshell.open(D + "basic_tasks.ifc")
    w = f.by_guid("22hyxvAPr65PFt9WZfHSP3")
    if variant == "center":
        c = center_world_mm(w)
    elif variant == "origin":   # about the wall's own placement origin (its local z axis)
        c = world(w)[:3, 3]
    else:                       # about the global Z axis
        c = np.zeros(3)
    rotate_z_about(f, w, 90.0, c)
    return save(f, f"test_11_{variant}")


def t12(sign=+1):
    """Move the door in wall SDYu by 1 m in x. Door is hosted: move its opening, door follows (placement child)."""
    f = ifcopenshell.open(D + "basic_tasks.ifc")
    door = f.by_guid("11kJIqz$n2Jf_DfJV1SDY7")
    op = ue.get_filled_void(door)
    translate(f, op, [sign * 1000.0, 0, 0])
    return save(f, f"test_12_{'plus' if sign > 0 else 'minus'}x")


def _stretch_up(f, e, dz_of_world_z):
    """Stretch element geometry vertically: every vertex gets world dz = dz_of_world_z(world z mm).
    Handles IfcFacetedBrep and IfcExtrudedAreaSolid (polyline profiles in a vertical plane, or whole-item shift)."""
    rep = unmap_rep(f, e)
    M = world(e)
    R = M[:3, :3]
    Rinv = R.T

    def to_world(p_local):
        return M @ np.append(p_local, 1.0)

    for it in rep.Items:
        if it.is_a("IfcFacetedBrep"):
            pts = {p.id(): p for p in f.traverse(it) if p.is_a("IfcCartesianPoint")}
            for p in pts.values():
                pl = np.array(p.Coordinates, float)
                dz = dz_of_world_z(to_world(pl)[2])
                if dz:
                    p.Coordinates = tuple(float(x) for x in pl + Rinv @ np.array([0, 0, dz]))
        elif it.is_a("IfcExtrudedAreaSolid"):
            P = np.array(up.get_axis2placement(it.Position))
            # z range of this item in world
            import ifcopenshell.geom as G
            sh = G.create_shape(G.settings(), it)
            v = np.array(sh.verts).reshape(-1, 3) * 1000.0
            wz = [(M @ np.append(x, 1))[2] for x in v]
            dzs = {dz_of_world_z(z) for z in wz}
            if len(dzs) == 1:
                dz = dzs.pop()
                if dz:
                    loc = np.array(it.Position.Location.Coordinates, float) + Rinv @ np.array([0, 0, dz])
                    it.Position.Location = f.createIfcCartesianPoint([float(x) for x in loc])
                continue
            sa = it.SweptArea
            assert sa.is_a("IfcArbitraryClosedProfileDef") and sa.OuterCurve.is_a("IfcPolyline"), it
            # world dz expressed in profile coordinates (must lie in the profile plane)
            Rp = P[:3, :3]
            pts = {p.id(): p for p in sa.OuterCurve.Points}
            for p in pts.values():
                xy = np.array(p.Coordinates, float)
                wpt = to_world((P @ np.array([xy[0], xy[1], 0, 1.0]))[:3])
                dz = dz_of_world_z(wpt[2])
                if dz:
                    d = Rp.T @ (Rinv @ np.array([0, 0, dz]))
                    assert abs(d[2]) < 1e-6
                    p.Coordinates = (float(xy[0] + d[0]), float(xy[1] + d[1]))
        else:
            raise RuntimeError(it)


def t13(variant="resize"):
    """Increase the window height by 0.5 m. Natural: sill stays, head goes up 0.5 m (1500 -> 2000 mm).
    The window assembly = window + its opening + the Revit nested trim & muntin proxies."""
    f = ifcopenshell.open(D + "basic_tasks.ifc")
    win = f.by_guid("11kJIqz$n2Jf_DfJV1SDbS")
    op = ue.get_filled_void(win)
    trim = f.by_guid("11kJIqz$n2Jf_DfJV1SDbO")
    mun = f.by_guid("11kJIqz$n2Jf_DfJV1SDbP")
    if variant == "move":
        # alternative reading: raise the window by 0.5 m
        for e in (op, trim, mun):
            translate(f, e, [0, 0, 500.0])
        return save(f, "test_13_move")
    zmid = world(win)[2, 3] + 750.0   # window mid-height (world mm) = 1650

    def dz(z):
        if z > zmid + 50:
            return 500.0          # head / upper part goes up 0.5 m
        if abs(z - zmid) <= 50:
            return 250.0          # mid muntin bar stays centred
        return 0.0
    _stretch_up(f, win, dz)
    _stretch_up(f, trim, dz)
    _stretch_up(f, mun, dz)
    # opening: profile x == vertical; 1500 -> 2000, bottom fixed
    sol = body_rep(op).Items[0]
    pr = sol.SweptArea
    assert abs(pr.XDim - 1500) < 1e-6
    loc = pr.Position.Location.Coordinates
    sol.SweptArea = f.createIfcRectangleProfileDef(pr.ProfileType, pr.ProfileName,
        f.createIfcAxis2Placement2D(f.createIfcCartesianPoint((loc[0] + 250.0, loc[1])), pr.Position.RefDirection),
        2000.0, pr.YDim)
    win.OverallHeight = 2000.0
    return save(f, "test_13_resize")


def t14():
    """'Decrease the height by 0.5 m' of a 300 mm slab: thickness cannot drop by 0.5 m, so the slab level is lowered 0.5 m."""
    f = ifcopenshell.open(D + "basic_tasks.ifc")
    translate(f, f.by_guid("11kJIqz$n2Jf_DfJV1SCVP"), [0, 0, -500.0])
    return save(f, "test_14_down")


def t15():
    f = ifcopenshell.open(D + "basic_tasks.ifc")
    translate(f, f.by_guid("22hyxvAPr65PFt9WZfHSMu"), [0, -3000.0, 0])
    return save(f, "test_15")


# ---------------------------------------------------------------- 01/01 geometry
def g11():
    """2nd storey = L2 (L1, L2, L3). All 6 L2 walls: top lowered 0.5 m (extrusion 3500 -> 3000), base stays."""
    f = ifcopenshell.open(D + "01/01/01_01_011.ifc")
    st = [s for s in f.by_type("IfcBuildingStorey") if s.Name == "L2"][0]
    walls = [e for e in ue.get_decomposition(st) if e.is_a("IfcWall")]
    for w in walls:
        s = body_rep(w).Items[0]
        s.Depth = float(s.Depth) - 500.0
    print("g11 walls", sorted(w.GlobalId for w in walls))
    return save(f, "geometry_test_11")


def g12():
    """Wall parallel to 1$zx...N40 (runs along Y) = N6K (the other Y-running wall). Rotate +45deg about its centre."""
    f = ifcopenshell.open(D + "01/01/01_01_012.ifc")
    ref = f.by_guid("1$zxNs50z3OeFBpABtoN40")
    rx = world(ref)[:3, 0]
    cands = [w for w in f.by_type("IfcWall") if w != ref and abs(abs(np.dot(world(w)[:3, 0], rx)) - 1) < 1e-6]
    assert len(cands) == 1, cands
    w = cands[0]
    print("g12 target", w.GlobalId)
    rotate_z_about(f, w, 45.0, center_world_mm(w))
    return save(f, "geometry_test_12")


def g13():
    """Window wider than 1.50 m = 5A (OverallWidth 1600). Move it +3 m in x with its opening and its nested trim/muntin proxies."""
    f = ifcopenshell.open(D + "01/01/01_01_013.ifc")
    wins = [w for w in f.by_type("IfcWindow") if w.OverallWidth and w.OverallWidth > 1500]
    assert len(wins) == 1
    win = wins[0]
    op = ue.get_filled_void(win)
    mn, mx = bbox(win)
    translate(f, op, [3000.0, 0, 0])          # window is placed relative to its opening -> follows
    # nested proxies belonging to this window: x-extent within the window span (excludes the other window's proxies)
    proxies = []
    for p in f.by_type("IfcBuildingElementProxy"):
        pmn, pmx = bbox(p)  # proxies are not placement children of the window, so still at original spot
        if pmn[0] > mn[0] - 0.1 and pmx[0] < mx[0] + 0.1:
            proxies.append(p)
    print("g13 window", win.GlobalId, "opening", op.GlobalId, "proxies", [p.GlobalId for p in proxies])
    for p in proxies:
        translate(f, p, [3000.0, 0, 0])
    return save(f, "geometry_test_13")


def g14(variant="one_edge"):
    """Slab 10.0 x 8.5 m -> square 10 x 10: lengthen the short (Y) side by 1.5 m.
    one_edge: extend the +Y edge (other edges stay) ; symmetric: grow 0.75 m on both Y edges."""
    f = ifcopenshell.open(D + "01/01/01_01_014.ifc")
    s = f.by_guid("11kJIqz$n2Jf_DfJV1SCVP")
    sol = body_rep(s).Items[0]
    pr = sol.SweptArea
    assert abs(pr.XDim - 8500) < 1e-6  # profile X == world Y (RefDirection (0,1,0))
    if variant == "one_edge":
        loc = list(sol.Position.Location.Coordinates)
        loc[1] += 750.0
        sol.Position = f.createIfcAxis2Placement3D(f.createIfcCartesianPoint(loc), sol.Position.Axis, sol.Position.RefDirection)
    sol.SweptArea = f.createIfcRectangleProfileDef(pr.ProfileType, pr.ProfileName, pr.Position, 10000.0, pr.YDim)
    return save(f, f"geometry_test_14_{variant}")


def g15(which="tl"):
    """Columns at (-0.1,0.1) (-0.1,4.35) (-6.4,0.1) (-6.4,3.6): move ONE column so the four form a rectangle."""
    f = ifcopenshell.open(D + "01/01/01_01_015.ifc")
    if which == "tl":
        translate(f, f.by_guid("3lOEkLxYb9$uRd50gnIDtl"), [0, 750.0, 0])   # (-6.4,3.6) -> (-6.4,4.35)
    else:
        translate(f, f.by_guid("3lOEkLxYb9$uRd50gnIDqu"), [0, -750.0, 0])  # (-0.1,4.35) -> (-0.1,3.6)
    return save(f, f"geometry_test_15_{which}")


# ---------------------------------------------------------------- 01/02 topological
def p11():
    """All columns (2 in file) extended from 1.5 m to the underside of slab ...PMM (z = 2.695 m); base stays."""
    f = ifcopenshell.open(D + "01/02/01_02_011.ifc")
    slab = f.by_guid("0dxtXCDSn2mfP92h$AiPMM")
    zb = bbox(slab)[0][2] * 1000.0
    for c in f.by_type("IfcColumn"):
        rep = unmap_rep(f, c)
        sol = rep.Items[0]
        base = world(c)[2, 3] + sol.Position.Location.Coordinates[2]
        sol.Depth = float(zb - base)
    print("p11 columns", [c.GlobalId for c in f.by_type("IfcColumn")], "slab bottom", zb)
    return save(f, "topological_test_11")


def p12(variant="free_end"):
    """Wall outside the 6 perimeter walls = 2c8i...CZr (x 7.5-7.7, y 0.19-2.19), 2 m long, starts at column QB.
    free_end: keep the end at the column, cut 1 m off the free end. symmetric: cut 0.5 m from each end."""
    f = ifcopenshell.open(D + "01/02/01_02_012.ifc")
    w = f.by_guid("2c8iwp2JP1ox_Asrwk4CZr")
    sol = body_rep(w).Items[0]
    pr = sol.SweptArea
    L = pr.XDim
    cx = pr.Position.Location.Coordinates[0] if variant == "symmetric" else pr.Position.Location.Coordinates[0] - 500.0
    sol.SweptArea = f.createIfcRectangleProfileDef(pr.ProfileType, pr.ProfileName,
        f.createIfcAxis2Placement2D(f.createIfcCartesianPoint((cx, pr.Position.Location.Coordinates[1])), pr.Position.RefDirection),
        L - 1000.0, pr.YDim)
    for r in w.Representation.Representations:
        if r.RepresentationIdentifier == "Axis":
            a, b = r.Items[0].Points
            if variant == "symmetric":
                pa = (a.Coordinates[0] + 500.0, a.Coordinates[1]); pb = (b.Coordinates[0] - 500.0, b.Coordinates[1])
            else:
                pa = a.Coordinates; pb = (b.Coordinates[0] - 1000.0, b.Coordinates[1])
            r.Items = [f.createIfcPolyline([f.createIfcCartesianPoint(pa), f.createIfcCartesianPoint(pb)])]
    return save(f, f"topological_test_12_{variant}")


def p13():
    """Window W1 sits in east wall XK (x-axis -Y). Seen from inside (looking +X) its right side is the -Y edge (y=0.7 m).
    The outside end face of wall XK is y = 0 -> move window+opening by -0.7 m in Y."""
    f = ifcopenshell.open(D + "01/02/01_02_013.ifc")
    win = f.by_guid("0HbU4cYqD2SBtSJYoQ_eW1")
    wall = f.by_guid("0HbU4cYqD2SBtSJYoQ_eXK")
    op = ue.get_filled_void(win)
    right_edge = bbox(op)[0][1] * 1000.0          # opening -Y face (window side in the wall)
    wall_end = bbox(wall)[0][1] * 1000.0          # outside end of the wall
    dy = wall_end - right_edge
    print("p13 dy", dy)
    translate(f, op, [0, dy, 0])
    return save(f, "topological_test_13")


def p14():
    """Beams run in +Y from y=0 through wall kyv (y 4.6-4.8) to 6.06. Trim their far ends to the wall's near face y=4.6."""
    f = ifcopenshell.open(D + "01/02/01_02_014.ifc")
    wall = f.by_guid("1A1LNnHqHFQwR1jv6PQkyv")
    yface = bbox(wall)[0][1] * 1000.0
    for b in f.by_type("IfcBeam"):
        rep = unmap_rep(f, b)
        sol = rep.Items[0]
        M = world(b)
        # extrusion runs along local +X (Position.Axis = -X, ExtrudedDirection = -Z)
        start_local_x = sol.Position.Location.Coordinates[0]
        start_world_y = (M @ np.array([start_local_x, 0, 0, 1]))[1]
        assert abs(M[1, 0] - 1) < 1e-9
        sol.Depth = float(yface - start_world_y)
        ax = unmap_rep(f, b, "Axis")
        tc = ax.Items[0]
        end_local_x = yface - M[1, 3]
        tc.Trim2 = [f.createIfcCartesianPoint((float(end_local_x), 0.0, tc.Trim2[0].Coordinates[2]))]
    print("p14 wall face", yface)
    return save(f, "topological_test_14")


def p15():
    """Slab _is (z 3.05-3.35) overlaps slab hO (top z 3.0) in plan -> lower it 50 mm so it rests on hO."""
    f = ifcopenshell.open(D + "01/02/01_02_015.ifc")
    s = f.by_guid("0CJwXarnHAeA7eFXxxI_is")
    dz = bbox(f.by_guid("0CJwXarnHAeA7eFXxxI_hO"))[1][2] * 1000.0 - bbox(s)[0][2] * 1000.0
    print("p15 dz", dz)
    translate(f, s, [0, 0, dz])
    return save(f, "topological_test_15")


BUILDS = {
    "test_11": [("center", lambda: t11("center")), ("alt_origin", lambda: t11("origin")), ("alt_globalZ", lambda: t11("global"))],
    "test_12": [("plus_x", lambda: t12(+1)), ("alt_minus_x", lambda: t12(-1))],
    "test_13": [("resize", lambda: t13("resize")), ("alt_move_up", lambda: t13("move"))],
    "test_14": [("move_down", t14)],
    "test_15": [("move", t15)],
    "geometry_test_11": [("lower_tops", g11)],
    "geometry_test_12": [("rotate_center", g12)],
    "geometry_test_13": [("move_assembly", g13)],
    "geometry_test_14": [("one_edge", lambda: g14("one_edge")), ("alt_symmetric", lambda: g14("symmetric"))],
    "geometry_test_15": [("move_tl", lambda: g15("tl")), ("alt_move_tr", lambda: g15("tr"))],
    "topological_test_11": [("extend", p11)],
    "topological_test_12": [("free_end", lambda: p12("free_end")), ("alt_symmetric", lambda: p12("symmetric"))],
    "topological_test_13": [("move", p13)],
    "topological_test_14": [("trim", p14)],
    "topological_test_15": [("lower", p15)],
}

if __name__ == "__main__":
    import json
    paths = {}
    for t, vs in BUILDS.items():
        for v, fn in vs:
            paths[f"{t}:{v}"] = fn()
    json.dump(paths, open(os.path.join(OUT, "paths.json"), "w"), indent=1)
    print(json.dumps(paths, indent=1))
