"""Score built answers with BIBIMBAP's own tests. Usage: python3 score.py OUTDIR RESULT.json
Run with the desired ifcopenshell on PYTHONPATH. Also records debugging detail (new element bbox, clash partners, sub-checks)."""
import sys, os, json, glob, importlib, traceback
sys.path.insert(0, "/tmp/bib/bibimbap")
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
import ifcopenshell
from data.tests.utils import create_utils as cu, clash_utils as cl
from build import SRC, D

OUT, RES = sys.argv[1], sys.argv[2]
NEWTYPE = {"test_01": "IfcDoor", "test_02": "IfcSlab", "test_03": "IfcOpeningElement", "test_04": "IfcColumn",
           "test_05": "IfcWall", "geometry_test_01": "IfcSlab", "geometry_test_02": "IfcColumn",
           "geometry_test_03": "IfcDoor", "geometry_test_04": "IfcSpace", "geometry_test_05": "IfcWall",
           "topological_test_01": "IfcWall", "topological_test_02": "IfcColumn", "topological_test_03": "IfcWall",
           "topological_test_04": "IfcSlab", "topological_test_05": "IfcDoor"}
results = {"ifcopenshell": ifcopenshell.version, "runs": {}}
for path in sorted(glob.glob(os.path.join(OUT, "*.ifc"))):
    key = os.path.basename(path)[:-4]
    name = key.split("__")[0]
    src = os.path.join(D, SRC[name])
    mod = importlib.import_module(f"data.tests.{name}")
    r = {"src": src}
    try:
        m = mod.execute_test(src, path, "")
        r["metrics"] = {k: (float(v) if isinstance(v, (bool, int, float)) else v) for k, v in m.items()}
        r["score"] = sum(float(v) for v in m.values()) / len(m)
    except Exception as ex:
        r["exception"] = traceback.format_exc()[-600:]
        r["score"] = 0.0
    # debug
    try:
        o, e = ifcopenshell.open(src), ifcopenshell.open(path)
        new = cu.find_new_elements(o, e, NEWTYPE[name])
        r["new"] = [x.GlobalId for x in new]
        dbg = {}
        for x in new:
            try:
                b = cu.get_bbox(x); dbg["bbox"] = [round(b[k], 3) for k in ("x_min", "x_max", "y_min", "y_max", "z_min", "z_max")]
                dbg["shape_dims"] = [round(v, 3) for v in cu.get_shape_dims(x)]
            except Exception as ex:
                dbg["bbox_err"] = str(ex)[:120]
            dbg["spatial_containment"] = cu.check_spatial_containment(e, x)
            dbg["elements_preserved"] = cu.check_elements_preserved(o, e)
            pairs = cl._collect_geom_tree_clash_pairs(e, focus_guids={x.GlobalId})
            partners = []
            for a, b2 in pairs:
                other = b2 if a == x.GlobalId else a
                try:
                    oe = e.by_guid(other); partners.append(f"{oe.is_a()} {other} {oe.Name}")
                except Exception:
                    partners.append(other)
            dbg["clash_partners"] = partners
            recs = [c for c in cl.debug_clashes(e) if x.GlobalId in (c["a_guid"], c["b_guid"])]
            dbg["clash_records"] = [{k: (round(v, 4) if isinstance(v, float) else v) for k, v in c.items() if k in ("a_guid", "b_guid", "clash_type", "distance")} for c in recs]
        r["debug"] = dbg
    except Exception as ex:
        r["debug_err"] = str(ex)[:300]
    results["runs"][key] = r
    print(f"{key:45s} score={r['score']:.3f} {r.get('metrics', r.get('exception','')[-200:])}")
    print("    ", {k: v for k, v in r.get("debug", {}).items() if k != "clash_records"})
json.dump(results, open(RES, "w"), indent=1)
