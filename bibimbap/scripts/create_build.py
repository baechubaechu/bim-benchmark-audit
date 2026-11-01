"""Build 'perfect answer' edited IFCs for the 15 BIBIMBAP CREATE tasks.
Usage: python3 build.py OUTDIR      (run with the pinned ifcopenshell 0.8.3.post2 on PYTHONPATH)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ifcopenshell
import ifcopenshell.util.element as ue
from lib import run, body_context, storey, mat, box_rep, new, wall, slab, column, door_in_wall

D = "/tmp/bib/olddata/data/ifc"
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SRC = {
    "test_01": "basic_tasks.ifc", "test_02": "basic_tasks.ifc", "test_03": "basic_tasks.ifc",
    "test_04": "basic_tasks.ifc", "test_05": "basic_tasks.ifc",
    "geometry_test_01": "01/01/01_01_001.ifc", "geometry_test_02": "01/01/01_01_002.ifc",
    "geometry_test_03": "01/01/01_01_003.ifc", "geometry_test_04": "01/01/01_01_004.ifc",
    "geometry_test_05": "empty.ifc",
    "topological_test_01": "01/02/01_02_001.ifc", "topological_test_02": "01/02/01_02_002.ifc",
    "topological_test_03": "01/02/01_02_003.ifc", "topological_test_04": "01/02/01_02_004.ifc",
    "topological_test_05": "01/02/01_02_005.ifc",
}
BUILDERS = {}


def task(name, variant="A"):
    def deco(fn):
        BUILDERS[(name, variant)] = fn
        return fn
    return deco


# ---------------- basic tasks (basic_tasks.ifc) ----------------
@task("test_01")
def t01(f, style="box"):
    # 2 m high x 1 m wide door, centred along wall 2UsXAbj6n0fwEWqdkVuHvf (x 19.2..29.4, y 15.0..15.2), on floor
    w = f.by_guid("2UsXAbj6n0fwEWqdkVuHvf")
    door_in_wall(f, w, u=5.1, width=1.0, height=2.0, door_style=style)


@task("test_01", "B_bonsai_door")
def t01b(f):
    t01(f, style="bonsai")


@task("test_02")
def t02(f):
    # 10 x 5 m slab, 0.2 m thick, plan centre (-30,0), bottom at z=0
    slab(f, -35, -2.5, -25, 2.5, 0.0, 0.2, storey(f, "L1"))


@task("test_03")
def t03(f, ext=0.0):
    s = f.by_guid("11kJIqz$n2Jf_DfJV1SCVP")  # bbox x -0.2..10.2, y -0.175..10.2, z 3.8..4.1
    ctx = body_context(f)
    cx, cy = (-0.2 + 10.2) / 2, (-0.175 + 10.2) / 2
    op = new(f, "IfcOpeningElement", "Opening 5x5", box_rep(f, ctx, 5.0, 5.0, 0.3 + 2 * ext),
             mat(cx, cy, 3.8 - ext), None, predefined_type="OPENING")
    run("feature.add_feature", f, feature=op, element=s)


@task("test_03", "B_opening_oversized_z")
def t03b(f):
    t03(f, ext=0.01)


@task("test_04")
def t04(f):
    column(f, 12.0, 8.0, 0.0, 3.0, 0.3, 0.3, storey(f, "L1"))


@task("test_05")
def t05(f):
    # 15 m wall starting at (0,-10), running +X (direction not given), 200 mm, full storey height 3.6 m
    wall(f, 0, -10, 15, -10, 3.6, 0.2, storey(f, "L1"))


# ---------------- geometry tasks ----------------
@task("geometry_test_01")
def g01(f, cont="L2"):
    # columns at the corners of 0..3 x 0..3, tops at z=3.0 -> slab 0..3 x 0..3, z 3.0..3.2
    slab(f, 0, 0, 3.0, 3.0, 3.0, 0.2, storey(f, cont))


@task("geometry_test_01", "B_contained_L1")
def g01b(f):
    g01(f, cont="L1")


@task("geometry_test_02")
def g02(f):
    # walls enclose 0..5 x 0..5 -> centroid (2.5,2.5); column 300x300, full storey height 3.0
    column(f, 2.5, 2.5, 0.0, 3.0, 0.3, 0.3, storey(f, "L1"))


@task("geometry_test_03")
def g03(f):
    # wall north of 3YQ$..$hw (y -1.0..-0.8) is 3YQ$..$ig (y 1.5..1.7); 0.9 x 2.1 door at its middle
    w = f.by_guid("3YQ$1CPXD2Mh2vQ18vV$ig")
    import ifcopenshell.util.placement as up
    print("   wall $ig placement", up.get_local_placement(w.ObjectPlacement)[:3, :].round(2).tolist())
    door_in_wall(f, w, u=3.25, width=0.9, height=2.1)


@task("geometry_test_04")
def g04(f, contain=False, x1=6.35):
    # room left (-X) of column 3A5G..: bounded by walls x 0.2..6.35, y 0.2..6.7, height 3.0
    ctx = body_context(f)
    sp = new(f, "IfcSpace", "Room left of column", box_rep(f, ctx, x1 - 0.2, 6.5, 3.0),
             mat((0.2 + x1) / 2, (0.2 + 6.7) / 2, 0.0), storey(f, "L1"), contain=contain,
             predefined_type="SPACE" if f.schema != "IFC2X3" else None)
    if f.schema == "IFC2X3":
        sp.CompositionType = "ELEMENT"; sp.InteriorOrExteriorSpace = "INTERNAL"


@task("geometry_test_04", "B_aggregated_AND_hand_contained")
def g04b(f):
    # the api refuses spatial.assign_container for IfcSpace (no ContainedInStructure inverse in IFC2X3),
    # so add an IfcRelContainedInSpatialStructure by hand (violates IFC2X3 WR31 of that relationship)
    g04(f, contain=False)
    sp = [x for x in f.by_type("IfcSpace")][-1]
    import ifcopenshell.guid
    f.createIfcRelContainedInSpatialStructure(ifcopenshell.guid.new(), f.by_type("IfcOwnerHistory")[0] if f.by_type("IfcOwnerHistory") else None,
        None, None, [sp], storey(f, "L1"))


@task("geometry_test_05")
def g05(f):
    wall(f, 10, 5, 15, 5, 3.0, 0.2, storey(f))


# ---------------- topological tasks ----------------
@task("topological_test_01")
def p01(f):
    # room 3_DH..4s: x 0.2..4.85, y 0.2..6.2; walls W,S,N exist; east wall missing.
    # New east wall: axis x=4.95, y 0.2..6.2 (between N and S walls), 200 mm, h 2.7 (floor top to ceiling slab)
    wall(f, 4.95, 0.2, 4.95, 6.2, 2.7, 0.2, storey(f, "L1"))


@task("topological_test_02")
def p02(f):
    # inner space of the 4 walls: x 0.2..4.85, y 0.2..6.2; column at its centre, floor (z=0) to slab soffit (2.7)
    column(f, (0.2 + 4.85) / 2, (0.2 + 6.2) / 2, 0.0, 2.7, 0.3, 0.3, storey(f, "L1"))


@task("topological_test_03")
def p03(f, full=False):
    # rooms 133 (y 3.3..6.2) and 134 (y 0.2..3.1) are already separated by wall stubs
    # 0rMM..Rcx (x 0.2..1.7) and 0rMM..RaK (x 3.35..4.85) at y 3.1..3.3; fill the gap x 1.7..3.35
    if full:
        wall(f, 0.2, 3.2, 4.85, 3.2, 2.7, 0.2, storey(f, "L1"))
    else:
        wall(f, 1.7, 3.2, 3.35, 3.2, 2.7, 0.2, storey(f, "L1"))


@task("topological_test_03", "B_full_length_wall")
def p03b(f):
    p03(f, full=True)


@task("topological_test_04")
def p04(f):
    # ceiling slab (z 2.7..3.0) exists; floor slab missing -> 300 mm floor slab under the 4 walls, 0..5.05 x 0..6.4
    slab(f, 0.0, 0.0, 5.05, 6.4, -0.3, 0.3, storey(f, "L1"))


@task("topological_test_05")
def p05(f):
    # exterior south wall 3Vyq..AwAc (x 0.2..7.7, y 0..0.2); 0.9 x 2.1 door at x=1.5 (into the room x 0.2..4.9)
    w = f.by_guid("3Vyqk8cSj8TOuAk6zHUwAc")
    import ifcopenshell.util.placement as up
    print("   wall AwAc placement", up.get_local_placement(w.ObjectPlacement)[:3, :].round(2).tolist())
    m = up.get_local_placement(w.ObjectPlacement)
    # local x along wall; find u such that world x = 1.5
    u = (1500.0 - m[0, 3]) / m[0, 0] / 1000.0
    door_in_wall(f, w, u=u, width=0.9, height=2.1)


def finalize(f):
    """Schema hygiene for what ifcopenshell.api 0.8.3 leaves unset."""
    for c in (f.by_type("IfcIndexedPolyCurve") if f.schema == "IFC4X3" else []):
        if c.SelfIntersect is None:
            c.SelfIntersect = False
    if f.schema == "IFC2X3" and f.by_type("IfcOwnerHistory"):
        oh = f.by_type("IfcOwnerHistory")[0]
        for r in f.by_type("IfcRoot"):
            if r.OwnerHistory is None:
                r.OwnerHistory = oh


if __name__ == "__main__":
    only = sys.argv[2:] or None
    for (name, var), fn in BUILDERS.items():
        if only and name not in only:
            continue
        f = ifcopenshell.open(os.path.join(D, SRC[name]))
        print(name, var)
        fn(f)
        finalize(f)
        f.write(os.path.join(OUT, f"{name}__{var}.ifc"))
