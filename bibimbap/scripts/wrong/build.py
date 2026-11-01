"""Build deliberately wrong edited IFCs for the 45 BIBIMBAP CRUD edit tasks.
Run: python3 -I build.py [task ...]   (uses ifcopenshell 0.8.3.post2 from create/ios083 for building, like the create builds)
Writes out/<task>__<variant>.ifc and manifest.json."""
import sys, os, json, re, csv, traceback
B = "./work"
sys.path.insert(0, B + "/create/ios083")
sys.path.insert(1, B + "/create")
sys.path.insert(2, B + "/wrong")
import numpy as np
import ifcopenshell
import ifcopenshell.guid
import ifcopenshell.geom, ifcopenshell.util.shape as us
import ifcopenshell.util.element as ue
import ifcopenshell.util.placement as up
from lib import storey, column, wall, slab, door_in_wall, new, box_rep, body_context, mat, run
import wlib as W

D = "/tmp/bib/olddata/data/ifc/"
OUT = B + "/wrong/out"
os.makedirs(OUT, exist_ok=True)
SRC = {r["test"]: D + r["ifc-file"] for r in csv.DictReader(open("/tmp/bib/olddata/data/prompts/all_questions.csv", encoding="utf-8-sig"))}
PROMPT = {r["test"]: r["question"] for r in csv.DictReader(open("/tmp/bib/olddata/data/prompts/all_questions.csv", encoding="utf-8-sig"))}
CR = B + "/create/out/%s__A.ifc"
UP = B + "/upd/out/%s.ifc"
DEL = B + "/del_out/%s_%s.ifc"

UPD_BASE = {  # best-scoring correct answer from the update C1 check (used as base for collateral variants)
    "test_11": "test_11_center", "test_12": "test_12_minusx", "test_13": "test_13_resize", "test_14": "test_14_down",
    "test_15": "test_15", "geometry_test_11": "geometry_test_11", "geometry_test_12": "geometry_test_12",
    "geometry_test_13": "geometry_test_13", "geometry_test_14": "geometry_test_14_symmetric",
    "geometry_test_15": "geometry_test_15_tl", "topological_test_11": "topological_test_11",
    "topological_test_12": "topological_test_12_symmetric", "topological_test_13": "topological_test_13",
    "topological_test_14": "topological_test_14", "topological_test_15": "topological_test_15"}

UPD_TARGETS = {
    "test_11": ["22hyxvAPr65PFt9WZfHSP3"], "test_12": ["11kJIqz$n2Jf_DfJV1SDY7", "1U$$kq6emLyOkmIlVkRzzn"],
    "test_13": ["11kJIqz$n2Jf_DfJV1SDbS", "0APGbZXNKfgPNB$VQQZ0pi", "11kJIqz$n2Jf_DfJV1SDbO", "11kJIqz$n2Jf_DfJV1SDbP"],
    "test_14": ["11kJIqz$n2Jf_DfJV1SCVP"], "test_15": ["22hyxvAPr65PFt9WZfHSMu"],
    "geometry_test_11": ["3PQZwOmmD1hgPWgX4XFLJO", "3PQZwOmmD1hgPWgX4XFLJP", "3PQZwOmmD1hgPWgX4XFLJQ", "3PQZwOmmD1hgPWgX4XFLJR", "3PQZwOmmD1hgPWgX4XFLJV", "3PQZwOmmD1hgPWgX4XFLJU"],
    "geometry_test_12": ["1$zxNs50z3OeFBpABtoN6K"],
    "geometry_test_13": ["2KbOAL4v52mv2YJ6fTql5D", "2KbOAL4v52mv2YJ6fTql5C", "2KbOAL4v52mv2YJ6fTql5F", "2KbOAL4v52mv2YJ6fTql5A", "2FgYNxuD5JBSJ92imotdSQ"],
    "geometry_test_14": ["11kJIqz$n2Jf_DfJV1SCVP"],
    "geometry_test_15": ["3lOEkLxYb9$uRd50gnIDtk", "3lOEkLxYb9$uRd50gnIDtl", "3lOEkLxYb9$uRd50gnIDpA", "3lOEkLxYb9$uRd50gnIDqu"],
    "topological_test_11": ["0n4qMSuxfEFA0BeEfapSQB", "0n4qMSuxfEFA0BeEfapSHZ"],
    "topological_test_12": ["2c8iwp2JP1ox_Asrwk4CZr"],
    "topological_test_13": ["0HbU4cYqD2SBtSJYoQ_eW1"],
    "topological_test_14": [],  # all beams, filled below
    "topological_test_15": ["0CJwXarnHAeA7eFXxxI_is"]}

DEL_TARGETS = {
    "test_16": ["22hyxvAPr65PFt9WZfHS2x"], "test_17": ["11kJIqz$n2Jf_DfJV1SDY7"], "test_18": ["0APGbZXNKfgPNB$VQQZ0pi"],
    "test_19": ["2UsXAbj6n0fwEWqdkVuHyn"], "test_20": ["2UsXAbj6n0fwEWqdkVuHyo"],
    "geometry_test_16": ["1g0NIEjcH1lfGqbYWRqt6L"],
    "geometry_test_17": ["1G$Ejw1Tn27RsUWQGSEz6r", "1G$Ejw1Tn27RsUWQGSEz6s", "1G$Ejw1Tn27RsUWQGSEz59", "1G$Ejw1Tn27RsUWQGSEz58", "1u4oG4Ltr15fMWjwJ4pN4F", "1u4oG4Ltr15fMWjwJ4pNPJ", "1u4oG4Ltr15fMWjwJ4pNUQ", "1u4oG4Ltr15fMWjwJ4pN5R", "1u4oG4Ltr15fMWjwJ4pNOG", "1u4oG4Ltr15fMWjwJ4pNV8"],
    "geometry_test_18": ["1xzI3PuNvF1RRUjZb8YIP1", "1xzI3PuNvF1RRUjZb8YIP0", "1xzI3PuNvF1RRUjZb8YIUz", "1xzI3PuNvF1RRUjZb8YINv", "1xzI3PuNvF1RRUjZb8YINr", "1xzI3PuNvF1RRUjZb8YINu"],
    "geometry_test_19": ["1mRYVM4YfFFBRkcbz1hH$F", "1mRYVM4YfFFBRkcbz1hH_L"],
    "geometry_test_20": ["0lwZAgQMb7yAIJTmmcGloi"],
    "topological_test_16": ["3cmsjRvPb4wf9t15K203Cj"],
    "topological_test_17": ["2IIWDJ6bzEPxU4iXeUX9_B", "2IIWDJ6bzEPxU4iXeUX9ow", "2IIWDJ6bzEPxU4iXeUX9rM", "2IIWDJ6bzEPxU4iXeUX9rK", "2IIWDJ6bzEPxU4iXeUX9ti"],
    "topological_test_18": ["3Vyqk8cSj8TOuAk6zHUwK5"],
    "topological_test_19": ["251vDGWZj4fBEsYpTPQwFu"],
    "topological_test_20": ["0dc_dU7Cj6aRLiY5JtJ$t0", "0dc_dU7Cj6aRLiY5JtJ$qt", "0Ub9$WlTH44eNTzbw3KFF4", "251vDGWZj4fBEsYpTPQwFu"]}

GUID_RE = re.compile(r"[0-9A-Za-z_$]{22}")


def protected(task):
    txt = open(f"/tmp/bib/bibimbap/data/tests/{task}.py").read() + PROMPT[task]
    return set(GUID_RE.findall(txt))


_bb = {}
def bbox(el):
    sh = ifcopenshell.geom.create_shape(ifcopenshell.geom.settings(), el)
    v = us.get_shape_vertices(sh, sh.geometry)
    return v[:, 0].min(), v[:, 0].max(), v[:, 1].min(), v[:, 1].max(), v[:, 2].min(), v[:, 2].max()


def pick_unrelated(f, task, extra_protect=(), classes=("IfcColumn", "IfcWall", "IfcSlab", "IfcBeam", "IfcWindow", "IfcDoor", "IfcBuildingElementProxy")):
    prot = protected(task) | set(extra_protect)
    for cls in classes:
        for el in f.by_type(cls):
            if el.GlobalId in prot or el.is_a("IfcOpeningElement"):
                continue
            if getattr(el, "HasOpenings", None) or getattr(el, "FillsVoids", None):
                continue
            if el.Representation is None:
                continue
            return el
    return None


MAN = []


def emit(task, variant, f, family, why, src=None):
    path = f"{OUT}/{task}__{variant}.ifc"
    f.write(path)
    MAN.append(dict(task=task, variant=variant, family=family, why=why, src=src or SRC[task], path=path))


def emit_path(task, variant, path, family, why):
    MAN.append(dict(task=task, variant=variant, family=family, why=why, src=SRC[task], path=path))


def op(path):
    return ifcopenshell.open(path)


def new_guids(base, src, cls="IfcProduct"):
    o = {e.GlobalId for e in src.by_type(cls)}
    return [e for e in base.by_type(cls) if e.GlobalId not in o and not e.is_a("IfcOpeningElement")] or \
           [e for e in base.by_type(cls) if e.GlobalId not in o]


def fake_move_set(f, els, d):
    """Placement-only move: roots get the new placement, every element's geometry is shifted back."""
    pls = {e.ObjectPlacement for e in els}
    for e in els:
        if e.ObjectPlacement.PlacementRelTo not in pls:
            W.gmove(f, e, d)
    for e in els:
        W.rep_shift(f, e, -np.array(d, float))


def real_move_set(f, els, d):
    pls = {e.ObjectPlacement for e in els}
    for e in els:
        if e.ObjectPlacement.PlacementRelTo not in pls:
            W.gmove(f, e, d)


# ---------------------------------------------------------------- CREATE
CREATE = ["test_01", "test_02", "test_03", "test_04", "test_05", "geometry_test_01", "geometry_test_02",
          "geometry_test_03", "geometry_test_04", "geometry_test_05", "topological_test_01", "topological_test_02",
          "topological_test_03", "topological_test_04", "topological_test_05"]
MAINCLS = {"test_01": "IfcDoor", "test_02": "IfcSlab", "test_03": "IfcOpeningElement", "test_04": "IfcColumn", "test_05": "IfcWall",
           "geometry_test_01": "IfcSlab", "geometry_test_02": "IfcColumn", "geometry_test_03": "IfcDoor", "geometry_test_04": "IfcSpace",
           "geometry_test_05": "IfcWall", "topological_test_01": "IfcWall", "topological_test_02": "IfcColumn",
           "topological_test_03": "IfcWall", "topological_test_04": "IfcSlab", "topological_test_05": "IfcDoor"}
# classes the create test reads in full -> not used as "unrelated" collateral targets
CREATE_READS = {"geometry_test_01": ("IfcColumn",), "geometry_test_02": ("IfcWall",), "geometry_test_03": ("IfcWall", "IfcWallStandardCase")}


def build_create(task):
    srcp = SRC[task]
    emit_path(task, "correct_A", CR % task, "reference", "correct answer from the create C1 check")
    emit_path(task, "noop", srcp, "1 no-op", "unchanged file, model_output claims success")
    base = op(CR % task); src = op(srcp)
    ne = [e for e in base.by_type(MAINCLS[task]) if e.GlobalId not in {x.GlobalId for x in src.by_type(MAINCLS[task])}]
    # duplicate the new element
    f = op(CR % task); n = f.by_guid(ne[0].GlobalId); W.dup(f, n)
    emit(task, "two_new_elements", f, "4 duplicate", "correct element plus a coincident second copy (two created instead of one)")
    f = op(CR % task)
    excl = [c for c in CREATE_READS.get(task, ())]
    cls = tuple(c for c in ("IfcColumn", "IfcWall", "IfcSlab", "IfcBeam", "IfcWindow", "IfcDoor") if c not in excl)
    u = pick_unrelated(f, task, [x.GlobalId for x in ne], classes=cls)
    if u is not None:
        ug = u.GlobalId
        f = op(CR % task); W.dup(f, f.by_guid(ug))
        emit(task, "junk_duplicate_of_unrelated", f, "4 duplicate", f"correct + coincident duplicate of unrelated {u.is_a()} {ug}")
        f = op(CR % task); W.gmove(f, f.by_guid(ug), (1.0, 0, 0))
        emit(task, "collateral_move_unrelated", f, "5 collateral", f"correct + unrelated {u.is_a()} {ug} moved +1 m in x")
        f = op(CR % task); W.remove(f, f.by_guid(ug))
        emit(task, "collateral_delete_unrelated", f, "5 collateral", f"correct + unrelated {u.is_a()} {ug} deleted")
    SPEC_CREATE[task](task)


def from_src(task, fn, variant, family, why):
    f = op(SRC[task]); fn(f); emit(task, variant, f, family, why)


def c_test_01(t):
    def no_op(f):
        d = [x for x in f.by_type("IfcDoor") if x.GlobalId not in {y.GlobalId for y in op(SRC[t]).by_type("IfcDoor")}][0]
        W.strip_fill_void(f, d)
    f = op(CR % t); no_op(f); emit(t, "door_without_opening", f, "3 wrong geometry/semantics", "door block placed in the wall with no opening/void/fill, so the wall is not cut")
    from_src(t, lambda f: door_in_wall(f, f.by_guid("22hyxvAPr65PFt9WZfHSKC"), u=5.1, width=1.0, height=2.0),
             "door_in_other_wall", "2 wrong target", "2x1 door in wall 22hy..SKC instead of 2UsX..Hvf")
    from_src(t, lambda f: door_in_wall(f, f.by_guid("2UsXAbj6n0fwEWqdkVuHvf"), u=5.1, width=2.0, height=1.0),
             "door_2m_wide_1m_high", "3 wrong size (by-design leniency)", "door 2.0 m wide x 1.0 m high (prompt: 2 by 1 m door; a 1 m high door; test accepts both orders)")
    from_src(t, lambda f: door_in_wall(f, f.by_guid("2UsXAbj6n0fwEWqdkVuHvf"), u=5.1, width=0.9, height=2.1),
             "door_0.9x2.1", "3 wrong size", "standard 0.9x2.1 door instead of 1x2")


def c_test_02(t):
    from_src(t, lambda f: slab(f, -35, -2.5, -25, 2.5, 0.75, 0.2, storey(f, "L1")),
             "slab_floating_0.75m", "3 wrong position", "slab bottom at z=+0.75 m instead of 0 (prompt: bottom at (-30,0))")
    from_src(t, lambda f: slab(f, -35, -2.5, -25, 2.5, 0.0, 0.4, storey(f, "L1")),
             "slab_0.4_thick", "3 wrong size", "slab 0.4 m thick instead of 0.2")
    from_src(t, lambda f: slab(f, -34.6, -2.1, -24.6, 2.9, 0.0, 0.2, storey(f, "L1")),
             "slab_centre_off_0.4m", "3 wrong position (tolerance)", "slab centre at (-29.6, 0.4) instead of (-30, 0)")


def c_test_03(t):
    def opening_nv(f, dx=0.0, z0=3.8, void=True):
        s = f.by_guid("11kJIqz$n2Jf_DfJV1SCVP"); ctx = body_context(f)
        o = new(f, "IfcOpeningElement", "Opening 5x5", box_rep(f, ctx, 5.0, 5.0, 0.3), mat(5.0 + dx, 5.0125, z0), None,
                predefined_type="OPENING")
        if void:
            run("feature.add_feature", f, feature=o, element=s)
    from_src(t, lambda f: opening_nv(f, void=False), "opening_without_void_rel", "3 wrong semantics",
             "5x5 opening box at the slab centre but not linked by IfcRelVoidsElement (slab is not cut)")
    from_src(t, lambda f: opening_nv(f, dx=2.0), "opening_off_centre_2m", "3 wrong position", "opening 2 m off centre")
    from_src(t, lambda f: opening_nv(f, dx=0.2), "opening_off_centre_0.2m", "3 wrong position (tolerance)", "opening 0.2 m off centre")


def c_test_04(t):
    from_src(t, lambda f: column(f, 12.0, 8.0, 10.0, 3.0, 0.3, 0.3, storey(f, "L1")),
             "column_floating_z10", "3 wrong position", "3 m column at (12,8) but base at z=10 m (floating 10 m above the floor)")
    from_src(t, lambda f: column(f, 8.0, 12.0, 0.0, 3.0, 0.3, 0.3, storey(f, "L1")),
             "column_at_8_12", "3 wrong position (by-design leniency)", "column at (8,12) instead of (12,8)")
    from_src(t, lambda f: column(f, 12.0, 8.0, 0.0, 6.0, 0.3, 0.3, storey(f, "L1")),
             "column_6m", "3 wrong size", "6 m column instead of 3 m")


def c_test_05(t):
    from_src(t, lambda f: wall(f, -7.5, -10, 7.5, -10, 3.6, 0.2, storey(f, "L1")),
             "wall_centred_on_point", "3 wrong position", "15 m wall centred on (0,-10) (runs -7.5..7.5) instead of beginning there")
    from_src(t, lambda f: wall(f, 0, -10, 10, -10, 3.6, 0.2, storey(f, "L1")),
             "wall_10m", "3 wrong size", "10 m wall instead of 15 m")


def c_g01(t):
    from_src(t, lambda f: slab(f, -0.45, -0.45, 3.45, 3.45, 3.0, 0.2, storey(f, "L2")),
             "slab_overhang_0.45", "3 wrong size (tolerance)", "slab overhangs the outer column edges by 0.45 m on every side")
    from_src(t, lambda f: slab(f, 0, 0, 3.0, 3.0, 3.5, 0.2, storey(f, "L2")),
             "slab_floating_0.5", "3 wrong position", "slab 0.5 m above the column tops")


def c_g02(t):
    from_src(t, lambda f: column(f, 2.5, 2.5, 10.0, 3.0, 0.3, 0.3, storey(f, "L1")),
             "column_floating_z10", "3 wrong position", "column at the centroid in plan but base at z=10 m (floating)")
    from_src(t, lambda f: column(f, 2.5, 2.5, 0.0, 1.2, 0.3, 0.3, storey(f, "L1")),
             "column_1.2m_stub", "3 wrong size", "1.2 m stub column in a 3 m storey")


def c_g03(t):
    f = op(CR % t)
    d = [x for x in f.by_type("IfcDoor")][-1]
    W.strip_fill_void(f, d)
    emit(t, "door_without_opening", f, "3 wrong semantics", "door block in the north wall with no opening/void/fill")
    from_src(t, lambda f: door_in_wall(f, f.by_guid("3YQ$1CPXD2Mh2vQ18vV$hw"), u=3.25, width=0.9, height=2.1),
             "door_in_reference_wall", "2 wrong target", "door in the reference wall $hw itself instead of the wall north of it")
    from_src(t, lambda f: door_in_wall(f, f.by_guid("3YQ$1CPXD2Mh2vQ18vV$iC"), u=3.25, width=0.9, height=2.1),
             "door_in_far_north_wall", "2 wrong target", "door in the second wall north ($iC), not the adjacent one ($ig)")


def c_g04(t):
    def sp(f, x0, x1, y0=0.2, y1=6.7):
        ctx = body_context(f)
        s = new(f, "IfcSpace", "Room", box_rep(f, ctx, x1 - x0, y1 - y0, 3.0), mat((x0 + x1) / 2, (y0 + y1) / 2, 0.0),
                storey(f, "L1"), contain=False)
        s.CompositionType = "ELEMENT"; s.InteriorOrExteriorSpace = "INTERNAL"
        s.OwnerHistory = f.by_type("IfcOwnerHistory")[0]
    from_src(t, lambda f: sp(f, 0.2, 12.7), "space_whole_floor", "3 wrong extent", "space covers the whole floor including the area right of the column")
    from_src(t, lambda f: sp(f, 6.55, 12.7), "space_right_of_column", "2 wrong target", "space in the area RIGHT of the column")


def c_g05(t):
    from_src(t, lambda f: wall(f, 10, 5, 10, 10, 3.0, 0.2, storey(f)), "wall_direction_+y", "3 wrong direction",
             "5 m wall from (10,5) pointing (0,1) instead of (1,0)")
    from_src(t, lambda f: wall(f, 10, 5, 14.6, 5, 3.0, 0.2, storey(f)), "wall_4.6m", "3 wrong size", "4.6 m wall instead of 5 m")
    from_src(t, lambda f: wall(f, 10, 5, 15.45, 5, 3.0, 0.2, storey(f)), "wall_5.45m", "3 wrong size", "5.45 m wall instead of 5 m")
    from_src(t, lambda f: wall(f, 10, 5, 5, 5, 3.0, 0.2, storey(f)), "wall_direction_-x", "3 wrong direction", "wall pointing (-1,0)")


def c_p01(t):
    from_src(t, lambda f: wall(f, -0.2, 0.2, -0.2, 6.2, 2.7, 0.2, storey(f, "L1")), "wall_outside_west_wall", "2 wrong target/position",
             "new wall parallel to and outside the existing west wall (x -0.3..-0.1); east side of the room stays open")
    from_src(t, lambda f: wall(f, 0.2, 3.2, 4.85, 3.2, 2.7, 0.2, storey(f, "L1")), "wall_across_room", "3 wrong position",
             "wall across the middle of the room; east side stays open")


def c_p02(t):
    from_src(t, lambda f: column(f, 5.45, 3.2, 0.0, 2.7, 0.3, 0.3, storey(f, "L1")), "column_outside_east_wall", "3 wrong position",
             "column 0.25 m outside the east wall (x 5.3..5.6), i.e. not in the inner space")


def c_p03(t):
    from_src(t, lambda f: wall(f, 2.2, 3.2, 2.85, 3.2, 2.7, 0.2, storey(f, "L1")), "wall_0.65m_in_gap", "3 wrong size",
             "0.65 m wall in the middle of the 1.65 m gap, leaving 0.5 m gaps on both sides (rooms not separated)")
    emit_path(t, "full_length_duplicate_stubs", B + "/create/out/topological_test_03__B_full_length_wall.ifc", "4 duplicate",
              "full-length wall that coincides with both existing wall stubs (from create C1)")


def c_p04(t):
    from_src(t, lambda f: slab(f, 0.0, 0.0, 5.05, 6.4, -1.1, 0.3, storey(f, "L1")), "slab_0.8m_below_walls", "3 wrong position",
             "floor slab 0.8 m below the wall bases (gap; does not close the walls)")
    from_src(t, lambda f: slab(f, 0.0, 0.0, 5.05, 6.4, 2.7, 0.3, storey(f, "L1")), "slab_duplicate_of_ceiling", "4 duplicate",
             "new slab coincident with the existing ceiling slab (floor stays open)")


def c_p05(t):
    from_src(t, lambda f: door_in_wall(f, f.by_guid("3Vyqk8cSj8TOuAk6zHUwBs"), u=2.0, width=0.9, height=2.1),
             "door_in_interior_wall", "2 wrong target", "door in interior wall 3Vyq..wBs (connects two inner rooms, not to outdoors)")
    f = op(CR % t); d = [x for x in f.by_type("IfcDoor")][-1]; W.strip_fill_void(f, d)
    emit(t, "door_without_opening", f, "3 wrong semantics", "door block in the exterior wall with no opening/void/fill")


SPEC_CREATE = {"test_01": c_test_01, "test_02": c_test_02, "test_03": c_test_03, "test_04": c_test_04, "test_05": c_test_05,
               "geometry_test_01": c_g01, "geometry_test_02": c_g02, "geometry_test_03": c_g03, "geometry_test_04": c_g04,
               "geometry_test_05": c_g05, "topological_test_01": c_p01, "topological_test_02": c_p02,
               "topological_test_03": c_p03, "topological_test_04": c_p04, "topological_test_05": c_p05}

# ---------------------------------------------------------------- UPDATE
UPDATE = list(UPD_BASE)


def build_update(task):
    basep = UP % UPD_BASE[task]
    emit_path(task, "correct_" + UPD_BASE[task], basep, "reference", "correct answer from the update C1 check (best-scoring accepted reading)")
    emit_path(task, "noop", SRC[task], "1 no-op", "unchanged file, model_output claims success")
    f = op(basep)
    tg = UPD_TARGETS[task] or [b.GlobalId for b in f.by_type("IfcBeam")]
    readers = {"topological_test_11": ["0dxtXCDSn2mfP92h$AiPMM"], "topological_test_14": ["1A1LNnHqHFQwR1jv6PQkyv"]}.get(task, [])
    u = pick_unrelated(f, task, tg + readers)
    if u is not None:
        ug, uc = u.GlobalId, u.is_a()
        f = op(basep); W.gmove(f, f.by_guid(ug), (1.0, 0, 0))
        emit(task, "collateral_move_unrelated_placement", f, "5 collateral", f"correct + unrelated {uc} {ug} moved +1 m x via its ObjectPlacement")
        f = op(basep); W.rep_shift(f, f.by_guid(ug), (1.0, 0, 0))
        emit(task, "collateral_move_unrelated_geometry", f, "5 collateral", f"correct + unrelated {uc} {ug} moved +1 m x via its Body geometry (placement untouched)")
        f = op(basep); W.rep_scale(f, f.by_guid(ug), 1.0, 1.0, 0.5)
        emit(task, "collateral_halve_unrelated_height", f, "5 collateral", f"correct + unrelated {uc} {ug} squashed to half its local-z size (geometry only)")
        f = op(basep); W.remove(f, f.by_guid(ug))
        emit(task, "collateral_delete_unrelated", f, "5 collateral", f"correct + unrelated {uc} {ug} deleted")
        f = op(basep); W.dup(f, f.by_guid(ug))
        emit(task, "junk_duplicate_of_unrelated", f, "4 duplicate", f"correct + coincident duplicate of unrelated {uc} {ug}")
    else:
        # nothing unrelated in the file: junk duplicate of an element the edit already handled
        jg = {"geometry_test_14": "11kJIqz$n2Jf_DfJV1SCVP", "geometry_test_15": "3lOEkLxYb9$uRd50gnIDpA"}.get(task)
        if jg:
            f = op(basep); W.dup(f, f.by_guid(jg))
            emit(task, "junk_duplicate_of_target_class", f, "4 duplicate", f"correct + coincident duplicate (new GUID) of {jg}")
    SPEC_UPDATE.get(task, lambda t: None)(task)


def u_from(task, base, fn, variant, family, why):
    f = op(base); fn(f); emit(task, variant, f, family, why)


def centre(el):
    b = bbox(el); return ((b[0] + b[1]) / 2, (b[2] + b[3]) / 2)


def u_test_11(t):
    g = "22hyxvAPr65PFt9WZfHSP3"
    u_from(t, SRC[t], lambda f: W.grotate_about(f, f.by_guid(g), 45, centre(f.by_guid(g))), "rotate_+45", "3 wrong magnitude", "rotated +45 instead of +90")
    u_from(t, SRC[t], lambda f: W.grotate_about(f, f.by_guid(g), -90, centre(f.by_guid(g))), "rotate_-90", "3 wrong direction (geometrically identical box)",
           "rotated -90 instead of +90 about the centre (same occupied volume for a symmetric box wall; only the axis direction flips)")
    u_from(t, SRC[t], lambda f: W.grotate_about(f, f.by_guid("22hyxvAPr65PFt9WZfHSKC"), 90, centre(f.by_guid("22hyxvAPr65PFt9WZfHSKC"))),
           "rotate_other_wall", "2 wrong target", "wall 22hy..SKC rotated instead")


def u_test_12(t):
    op_g, door = "1U$$kq6emLyOkmIlVkRzzn", "11kJIqz$n2Jf_DfJV1SDY7"
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(op_g), f.by_guid(door)], (-2.0, 0, 0)), "move_-2m", "3 wrong magnitude", "door+opening moved 2 m instead of 1 m")
    u_from(t, SRC[t], lambda f: fake_move_set(f, [f.by_guid(op_g), f.by_guid(door)], (-1.0, 0, 0)), "placement_only_move", "3 no real change",
           "placements say -1 m but geometry shifted back: door and opening do not move in space")
    u_from(t, SRC[t], lambda f: W.rep_shift(f, f.by_guid(door), (-1.0, 0, 0)) if False else W.gmove(f, f.by_guid(door), (-1.0, 0, 0)),
           "door_moved_opening_left", "3 wrong semantics", "door moved -1 m but its opening left behind (door now sits in solid wall)")


def u_test_13(t):
    tg = UPD_TARGETS[t]
    u_from(t, SRC[t], lambda f: fake_move_set(f, [f.by_guid(g) for g in tg], (0, 0, 0.5)), "placement_only_move_up", "3 no real change",
           "window assembly placements raised 0.5 m, geometry shifted back: nothing moves or grows in space")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g) for g in tg], (0, 0, 1.0)), "move_up_1m", "3 wrong magnitude", "assembly moved up 1.0 m")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(tg[0])], (0, 0, 0.5)), "window_only_up", "3 wrong semantics", "only the window raised, opening/trims left")


def u_test_14(t):
    g = UPD_TARGETS[t][0]
    u_from(t, SRC[t], lambda f: fake_move_set(f, [f.by_guid(g)], (0, 0, -0.5)), "placement_only_move_down", "3 no real change",
           "slab placement lowered 0.5 m, geometry shifted back: slab stays where it was")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g)], (0, 0, 0.5)), "move_up_0.5", "3 wrong direction", "slab moved UP 0.5 m")


def u_test_15(t):
    g = UPD_TARGETS[t][0]
    u_from(t, SRC[t], lambda f: fake_move_set(f, [f.by_guid(g)], (0, -3.0, 0)), "placement_only_move", "3 no real change",
           "column placement moved -3 m y, geometry shifted back: column stays")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g)], (0, 3.0, 0)), "move_+3", "3 wrong direction", "moved +3 m")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid("22hyxvAPr65PFt9WZfHSMv")], (0, -3.0, 0)), "move_other_column", "2 wrong target", "column 22hy..SMv moved instead")


def u_g11(t):
    tg = UPD_TARGETS[t]
    u_from(t, SRC[t], lambda f: [W.rep_scale(f, f.by_guid(g), 1, 1, 2.5 / 3.5) for g in tg], "lower_by_1m", "3 wrong magnitude", "L2 walls lowered by 1.0 m")
    l1 = ["3PQZwOmmD1hgPWgX4XFLB1", "3PQZwOmmD1hgPWgX4XFL8K", "3PQZwOmmD1hgPWgX4XFL94", "3PQZwOmmD1hgPWgX4XFLMM", "3PQZwOmmD1hgPWgX4XFLKr", "3PQZwOmmD1hgPWgX4XFLIP"]
    u_from(t, SRC[t], lambda f: [W.rep_scale(f, f.by_guid(g), 1, 1, 2.2 / 2.7) for g in l1], "lower_storey1_walls", "2 wrong target", "the six ground-floor walls lowered 0.5 m instead")
    u_from(t, SRC[t], lambda f: [W.rep_scale(f, f.by_guid(g), 1, 1, 3.0 / 3.5, about_local=(0, 0, 3.5)) for g in tg], "raise_base_0.5", "3 wrong edit",
           "L2 walls shortened from the bottom (base raised 0.5 m, gap above slab)")


def u_g12(t):
    g = "1$zxNs50z3OeFBpABtoN6K"
    u_from(t, UP % UPD_BASE[t], lambda f: None, "control_resave_correct", "control", "correct answer re-opened and re-written unchanged (control, not wrong)")
    for deg, fam, why in [(-45, "3 wrong direction", "rotated -45 instead of +45"), (50.8, "3 wrong magnitude", "rotated +50.8 instead of +45"),
                          (51.0, "3 wrong magnitude", "rotated +51 instead of +45"), (90, "3 wrong magnitude", "rotated +90")]:
        u_from(t, SRC[t], lambda f, deg=deg: W.grotate_about(f, f.by_guid(g), deg, centre(f.by_guid(g))), f"rotate_{deg:+g}", fam, why)
    u_from(t, SRC[t], lambda f: W.grotate_about(f, f.by_guid("1$zxNs50z3OeFBpABtoN54"), 45, centre(f.by_guid("1$zxNs50z3OeFBpABtoN54"))),
           "rotate_other_wall", "2 wrong target", "wall N54 (perpendicular) rotated +45 instead")


def u_g13(t):
    ok = ["2FgYNxuD5JBSJ92imotdSQ", "2KbOAL4v52mv2YJ6fTql5D", "2KbOAL4v52mv2YJ6fTql5C", "2KbOAL4v52mv2YJ6fTql5F", "2KbOAL4v52mv2YJ6fTql5A"]
    other = ["2GJoUje5nL3kaGklEevVbI", "2KbOAL4v52mv2YJ6fTqlO_", "2KbOAL4v52mv2YJ6fTqlOn", "2KbOAL4v52mv2YJ6fTqlOm", "2KbOAL4v52mv2YJ6fTqlOz"]
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g) for g in other], (3.0, 0, 0)), "move_narrow_window", "2 wrong target", "the 0.6 m window moved instead")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g) for g in ok], (-3.0, 0, 0)), "move_-3", "3 wrong direction", "moved -3 m")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g) for g in ok], (3.0, 0, 0.5)), "move_3_and_up", "3 wrong edit", "moved +3 m x and also +0.5 m z")


def u_g14(t):
    g = UPD_TARGETS[t][0]
    def sc(f, fx, fy):
        el = f.by_guid(g); M = W._mat(el); b = bbox(el); s = W.S(f)
        c = np.linalg.inv(M) @ np.array([(b[0] + b[1]) / 2 * s, (b[2] + b[3]) / 2 * s, b[4] * s, 1])
        # map global x/y scale to local axes (axis-aligned placements)
        R = np.abs(M[:3, :3]).round()
        lf = R.T @ np.array([fx, fy, 1.0])
        W.rep_scale(f, el, lf[0], lf[1], lf[2], about_local=tuple(c[:3] / s))
    b0 = bbox(op(SRC[t]).by_guid(g)); xl, yl = b0[1] - b0[0], b0[3] - b0[2]
    print("   g14 slab", xl, yl)
    long_is_x = xl > yl
    u_from(t, SRC[t], lambda f: sc(f, (yl / xl) if long_is_x else 1, 1 if long_is_x else (xl / yl)), "square_by_shrinking", "3 wrong direction",
           "made square by SHORTENING the long side (prompt: increase)")
    u_from(t, SRC[t], lambda f: sc(f, 1 if long_is_x else (xl + 3) / xl, ((yl + 3) / yl) if long_is_x else 1), "extend_short_side_3m", "3 wrong magnitude",
           "short side increased 3 m (not a square)")


def u_g15(t):
    pass


def u_p11(t):
    slabg = "0dxtXCDSn2mfP92h$AiPMM"
    u_from(t, SRC[t], lambda f: W.rep_shift(f, f.by_guid(slabg), (0, 0, -1.195)), "slab_geometry_lowered_to_columns", "2 wrong target",
           "columns unchanged; instead the slab's geometry is lowered 1.195 m so its underside meets the 1.5 m columns")
    u_from(t, SRC[t], lambda f: W.rep_scale(f, f.by_guid("0n4qMSuxfEFA0BeEfapSQB"), 1, 1, 2.6952 / 1.5), "only_one_column", "3 incomplete",
           "only one of the two columns extended")
    u_from(t, SRC[t], lambda f: [W.rep_scale(f, f.by_guid(g), 1, 1, 3.5 / 1.5) for g in UPD_TARGETS[t]], "columns_through_slab", "3 wrong magnitude",
           "columns extended to 3.5 m, piercing through the slab")


def u_p12(t):
    tg = UPD_TARGETS[t][0]
    f0 = op(SRC[t]); w = f0.by_guid(tg); b = bbox(w)
    print("   p12 wall bbox", b)
    other = [x for x in f0.by_type("IfcWall") if x.GlobalId not in protected(t)]
    print("   p12 other walls", [(x.GlobalId, [round(v, 2) for v in bbox(x)]) for x in other][:4])
    if other:
        og = other[0].GlobalId
        ob = bbox(other[0]); L = max(ob[1] - ob[0], ob[3] - ob[2])
        def shorten_other(f):
            el = f.by_guid(og); M = W._mat(el); s = W.S(f); bb = bbox(el)
            c = np.linalg.inv(M) @ np.array([(bb[0] + bb[1]) / 2 * s, (bb[2] + bb[3]) / 2 * s, bb[4] * s, 1])
            R = np.abs(M[:3, :3]).round(); along_x = (bb[1] - bb[0]) > (bb[3] - bb[2])
            lf = R.T @ np.array([(L - 1) / L if along_x else 1, 1 if along_x else (L - 1) / L, 1.0])
            W.rep_scale(f, el, lf[0], lf[1], lf[2], about_local=tuple(c[:3] / s))
        u_from(t, SRC[t], shorten_other, "shorten_other_wall", "2 wrong target", f"wall {og} shortened 1 m instead of CZr")


def u_p13(t):
    g = "0HbU4cYqD2SBtSJYoQ_eW1"
    f0 = op(SRC[t]); w = f0.by_guid(g); o = w.FillsVoids[0].RelatingOpeningElement
    dy = (900.0 - float(up.get_local_placement(w.ObjectPlacement)[1][3])) / 1000.0
    print("   p13 dy", dy, "window parent is opening:", w.ObjectPlacement.PlacementRelTo == o.ObjectPlacement)
    og = o.GlobalId
    u_from(t, SRC[t], lambda f: fake_move_set(f, [f.by_guid(g), f.by_guid(og)], (0, dy, 0)), "placement_only_move", "3 no real change",
           "window+opening placements moved to y=900 mm, geometry shifted back: window stays")
    u_from(t, UP % UPD_BASE[t], lambda f: W.rep_scale(f, f.by_guid(g), 0.5, 0.5, 0.5), "correct_move_window_shrunk", "5 collateral (on target)",
           "correct move, but the window body is shrunk to half size (OverallWidth/Height attributes left unchanged)")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g)], (0, dy, 0)) if w.ObjectPlacement.PlacementRelTo != o.ObjectPlacement else
           real_move_set(f, [f.by_guid(og)], (0, dy, 0)), "move_by_window_only_or_assembly", "control", "real move of the assembly root by dy")


def u_p14(t):
    u_from(t, SRC[t], lambda f: W.rep_shift(f, f.by_guid("1A1LNnHqHFQwR1jv6PQkyv"), (0, 6.06 - 4.6, 0)), "wall_geometry_moved_to_beam_ends", "2 wrong target",
           "beams untouched; the reference wall's geometry is moved 1.46 m so its face meets the beam ends")


def u_p15(t):
    g = UPD_TARGETS[t][0]
    u_from(t, SRC[t], lambda f: fake_move_set(f, [f.by_guid(g)], (0, 0, -0.05)), "placement_only_move", "3 no real change",
           "slab placement lowered 50 mm, geometry shifted back: slab still floats 50 mm above")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g)], (0, 0, -0.35)), "move_down_0.35", "3 wrong magnitude",
           "slab lowered 0.35 m: penetrates slab hO")
    u_from(t, SRC[t], lambda f: real_move_set(f, [f.by_guid(g)], (0, -0.2, -0.05)), "lower_and_shift_y", "3 wrong edit",
           "lowered 50 mm but also shifted 0.2 m in y")


SPEC_UPDATE = {"test_11": u_test_11, "test_12": u_test_12, "test_13": u_test_13, "test_14": u_test_14, "test_15": u_test_15,
               "geometry_test_11": u_g11, "geometry_test_12": u_g12, "geometry_test_13": u_g13, "geometry_test_14": u_g14,
               "geometry_test_15": u_g15, "topological_test_11": u_p11, "topological_test_12": u_p12,
               "topological_test_13": u_p13, "topological_test_14": u_p14, "topological_test_15": u_p15}

# ---------------------------------------------------------------- DELETE
DELETE = list(DEL_TARGETS)


def build_delete(task):
    tg = DEL_TARGETS[task]
    A, C = DEL % (task, "A"), DEL % (task, "C")
    emit_path(task, "correct_A_clean_delete", A, "reference", "clean delete via root.remove_product (del C1 variant A)")
    emit_path(task, "ref_C_dirty_delete", C, "reference", "entity-only delete leaving its psets/relations (del C1 variant C)")
    emit_path(task, "noop", SRC[task], "1 no-op", "unchanged file, model_output claims success")
    src = op(SRC[task])
    present = [g for g in tg if _has(src, g)]
    cls = src.by_guid(present[0]).is_a() if present else None
    prot = protected(task) | set(tg)
    if task == "geometry_test_20":
        prot.add("0lwZAgQMb7yAIJTmmcGlwc")
    wrong = [e for e in src.by_type(cls) if e.GlobalId not in prot] if cls else []
    if wrong:
        wg = wrong[0].GlobalId
        f = op(SRC[task]); W.remove(f, f.by_guid(wg))
        emit(task, "delete_wrong_element", f, "2 wrong target", f"clean delete of {cls} {wg} instead of the target")
        f = op(SRC[task]); [W.remove(f, f.by_guid(g)) for g in present]; W.remove(f, f.by_guid(wg))
        emit(task, "delete_target_plus_same_class", f, "6 extra delete", f"targets plus another {cls} {wg} deleted")
    u = pick_unrelated(src, task, tg)
    if u is not None:
        ug, uc = u.GlobalId, u.is_a()
        f = op(A); W.remove(f, f.by_guid(ug))
        emit(task, "A_plus_delete_unrelated", f, "6 extra delete", f"clean delete + unrelated {uc} {ug} deleted")
        for base, tag in ((A, "A"), (C, "C")):
            f = op(base); W.dup(f, f.by_guid(ug))
            emit(task, f"{tag}_plus_junk_duplicate", f, "4 duplicate", f"{tag}-delete + coincident duplicate of unrelated {uc} {ug}")
            f = op(base); W.rep_shift(f, f.by_guid(ug), (1.0, 0, 0))
            emit(task, f"{tag}_plus_unrelated_geometry_moved", f, "5 collateral", f"{tag}-delete + unrelated {uc} {ug} moved 1 m via geometry")
            f = op(base); W.rep_scale(f, f.by_guid(ug), 1, 1, 0.5)
            emit(task, f"{tag}_plus_unrelated_height_halved", f, "5 collateral", f"{tag}-delete + unrelated {uc} {ug} squashed to half height (geometry only)")
        f = op(C); W.gmove(f, f.by_guid(ug), (1.0, 0, 0))
        emit(task, "C_plus_unrelated_placement_moved", f, "5 collateral", f"C-delete + unrelated {uc} {ug} moved 1 m via placement")
    if present:
        def regid(f):
            for g in present:
                f.by_guid(g).GlobalId = ifcopenshell.guid.new()
        f = op(SRC[task]); regid(f)
        emit(task, "target_kept_guid_renamed", f, "1 no real change", "target NOT deleted: element kept in place, only its GlobalId replaced by a new one")
    if len(present) > 1:
        f = op(SRC[task]); [W.remove(f, f.by_guid(g)) for g in present[:-1]]
        emit(task, "partial_delete", f, "3 incomplete", f"only {len(present)-1} of {len(present)} present targets deleted")
        f = op(SRC[task]); [W.dirty_remove(f, f.by_guid(g)) for g in present[:-1]]
        emit(task, "partial_dirty_delete", f, "3 incomplete", f"only {len(present)-1} of {len(present)} present targets deleted (entity-only)")


def _has(f, g):
    try:
        f.by_guid(g); return True
    except RuntimeError:
        return False


if __name__ == "__main__":
    only = set(sys.argv[1:])
    for t in CREATE + UPDATE + DELETE:
        if only and t not in only:
            continue
        print("==", t, flush=True)
        try:
            (build_create if t in CREATE else build_update if t in UPDATE else build_delete)(t)
        except Exception:
            traceback.print_exc()
    name = "manifest.json" if not only else "manifest_partial.json"
    json.dump(MAN, open(B + "/wrong/" + name, "w"), indent=1)
    print(len(MAN), "entries")
