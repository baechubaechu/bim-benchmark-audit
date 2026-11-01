# BIBIMBAP C1 (perfect-answer) check: clean-delete targets, score with BIBIMBAP's own delete tests.
import sys, os, csv, importlib, json, tempfile
REPO, DATA = sys.argv[1], sys.argv[2]
sys.path.insert(0, REPO)
import ifcopenshell, ifcopenshell.api, ifcopenshell.util.element as ue
import data.tests.delete_integrity as di
import data.tests.integrity_utils as iu

rows = [r for r in csv.DictReader(open(f"{DATA}/prompts/all_questions.csv")) if r["CRUD"] == "delete"]

_g = {}
def gutted(src):
    if src in _g: return _g[src]
    f = ifcopenshell.open(src)
    for el in list(f.by_type("IfcElement")) + list(f.by_type("IfcSpace")):
        try: ifcopenshell.api.run("root.remove_product", f, product=el)
        except Exception: pass
    out = os.path.join(tempfile.mkdtemp(), "gutted.ifc"); f.write(out); _g[src] = out
    return out

def targets_of(mod, src):
    rec = {}
    orig_nt = mod.non_target_elements_unchanged
    orig_ri = mod.run_delete_integrity_check
    mod.non_target_elements_unchanged = lambda *a, **k: False
    def cap(i, e, t): rec["t"] = list(t); return False
    mod.run_delete_integrity_check = cap
    try:
        for cand in (src, gutted(src)):
            mod.execute_test(src, cand, "")
            if rec.get("t"): break
    finally:
        mod.non_target_elements_unchanged, mod.run_delete_integrity_check = orig_nt, orig_ri
    return rec.get("t")

def make_edit(src, targets, variant, out):
    f = ifcopenshell.open(src)
    for g in targets:
        try: el = f.by_guid(g)
        except RuntimeError: continue
        extra = []
        if variant == "B":
            v = ue.get_filled_void(el)
            if v is not None: extra.append(v)
            for rel in getattr(el, "ConnectedTo", ()) + getattr(el, "ConnectedFrom", ()):
                extra.append(rel)
        if variant == "C":
            f.remove(el); continue
        ifcopenshell.api.run("root.remove_product", f, product=el)
        for x in extra:
            try:
                if x.is_a("IfcProduct"): ifcopenshell.api.run("root.remove_product", f, product=x)
                else: f.remove(x)
            except Exception: pass
    f.write(out)

def subchecks(src, out, targets):
    o, e = ifcopenshell.open(src), ifcopenshell.open(out)
    res = {}
    for g in targets:
        res[g] = dict(
            wall_conn=di.wall_connections_deleted(o, e, g),
            containment=di.spatial_containment_deleted(o, e, g),
            openings=di.openings_deleted(o, e, g),
            aggregation=di.aggregations_deleted(o, e, g))
    old = iu._rooted_elements_by_guid(o); new = iu._rooted_elements_by_guid(e)
    missing = sorted({old[g].is_a() for g in old if g not in new and g not in targets})
    res["non_target_unchanged"] = iu.non_target_elements_unchanged(o, e, targets)
    res["non_target_missing_classes"] = missing
    return res

PRE = {x["test"]: x["targets"] for x in json.load(open(sys.argv[4]))} if len(sys.argv) > 4 else None
results = []
tmp = os.environ.get("OUTDIR") or tempfile.mkdtemp(); os.makedirs(tmp, exist_ok=True)
for r in rows:
    name = r["test"]; src = os.path.join(DATA, "ifc", r["ifc-file"])
    mod = importlib.import_module(f"data.tests.{name}")
    t = PRE[name] if PRE else targets_of(mod, src)
    exist = [g for g in t if g in iu._rooted_elements_by_guid(ifcopenshell.open(src))]
    entry = dict(test=name, ifc=r["ifc-file"], targets=t, targets_in_file=len(exist),
                 classes=[ifcopenshell.open(src).by_guid(g).is_a() for g in exist])
    for v in ("A", "B", "C"):
        out = os.path.join(tmp, f"{name}_{v}.ifc")
        make_edit(src, t, v, out)
        try:
            m = mod.execute_test(src, out, "")
            sc = sum(m.values()) / len(m)
        except Exception as ex:
            m = {"CRASH": f"{type(ex).__name__}: {ex}"[:120]}; sc = None
        def safe(fn):
            try: return fn()
            except Exception as ex: return f"CRASH {type(ex).__name__}"
        sub = {}
        for g in t:
            o, e = ifcopenshell.open(src), ifcopenshell.open(out)
            sub[g] = {k: safe(lambda f=f: f(o, e, g)) for k, f in dict(wall_conn=di.wall_connections_deleted, containment=di.spatial_containment_deleted, openings=di.openings_deleted, aggregation=di.aggregations_deleted).items()}
        o, e = ifcopenshell.open(src), ifcopenshell.open(out)
        old = iu._rooted_elements_by_guid(o); new = iu._rooted_elements_by_guid(e)
        sub["non_target_missing_classes"] = sorted({old[g].is_a() for g in old if g not in new and g not in t})
        sub["non_target_unchanged"] = iu.non_target_elements_unchanged(o, e, t)
        entry[v] = dict(metrics=m, score=sc, sub=sub)
    results.append(entry)
    print(name, entry["classes"], "A", entry["A"]["metrics"], "B", entry["B"]["metrics"], "C", entry["C"]["metrics"],
          "A-missing", entry["A"]["sub"]["non_target_missing_classes"], "B-missing", entry["B"]["sub"]["non_target_missing_classes"], flush=True)
json.dump(results, open(sys.argv[3], "w"), indent=1, default=str)
