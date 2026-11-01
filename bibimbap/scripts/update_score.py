# Score built answers with BIBIMBAP execute_test under ifcopenshell 0.8.3.post2 (pinned version), + diagnostics.
import sys, os
IOS = "./work/create/ios083"
if len(sys.argv) > 1 and sys.argv[1] == "--v09": sys.argv.pop(1)
else: sys.path.insert(0, IOS)
sys.path.insert(1, "/tmp/bib/bibimbap")
import json, importlib, io, contextlib, csv, ifcopenshell
import data.tests.integrity_utils as iu
sys.path.insert(2, os.path.dirname(os.path.abspath(__file__))); from run import TARGETS
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/tmp/bib/olddata/data"
rows = {r["test"]: r for r in csv.DictReader(open(f"{DATA}/prompts/all_questions.csv")) if r["CRUD"].strip() == "update"}
paths = json.load(open(os.path.join(HERE, "out", "paths.json")))

def run(test, src, edited):
    mod = importlib.import_module(f"data.tests.{test}")
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): m = mod.execute_test(src, edited, "")
        err = None
    except Exception as ex: m, err = None, repr(ex)[:200]
    return dict(metrics={k: bool(v) for k, v in m.items()} if m else None,
                score=(sum(bool(v) for v in m.values()) / len(m)) if m else 0.0, error=err)

def diag(src, edited, targets):
    o, e = ifcopenshell.open(src), ifcopenshell.open(edited)
    ob, eb = iu._rooted_elements_by_guid(o), iu._rooted_elements_by_guid(e)
    changed = []
    for g, el in ob.items():
        if g in targets: continue
        ne = eb.get(g)
        if ne is None: changed.append((g, el.is_a(), "missing")); continue
        if iu._element_signature(el) != iu._element_signature(ne): changed.append((g, el.is_a(), "sig"))
    cls = lambda f, g: f.by_guid(g).is_a() + ":" + g + ":" + str(f.by_guid(g).Name)[:30]
    out = dict(changed_non_targets=changed[:10])
    for at in (False, True):
        try:
            old = iu._collect_geom_tree_clash_pairs(o, focus_guids=set(targets), allow_touching=at)
            new = iu._collect_geom_tree_clash_pairs(e, focus_guids=set(targets), allow_touching=at)
            out[f"new_clashes_allow_touching={at}"] = [[cls(e, a), cls(e, b)] for a, b in sorted(new - old)]
        except Exception as ex: out[f"new_clashes_allow_touching={at}"] = repr(ex)[:150]
    return out

if __name__ == "__main__":
    only = sys.argv[1:]
    tag = ifcopenshell.version
    res = {}
    for key, edited in paths.items():
        test, variant = key.split(":")
        if only and test not in only: continue
        src = os.path.join(DATA, "ifc", rows[test]["ifc-file"])
        r = dict(test=test, variant=variant, prompt=rows[test]["question"], edited=edited, ifcopenshell=tag,
                 result=run(test, src, edited), unedited=run(test, src, src))
        if not tag.startswith("0.9"): r["diag"] = diag(src, edited, TARGETS[test])
        res[key] = r
        print(key, "\n   ", r["result"], "\n    unedited:", r["unedited"]["metrics"], "\n    diag:", r.get("diag"), flush=True)
    out = os.path.join(HERE, f"update-c1_metrics_{tag}.json")
    old = json.load(open(out)) if (only and os.path.exists(out)) else {}
    old.update(res); json.dump(old, open(out, "w"), indent=1)
