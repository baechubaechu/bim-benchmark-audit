"""Score wrong-answer IFCs with BIBIMBAP's own tests. Run with ifcopenshell 0.8.3.post2 on PYTHONPATH.
Usage: python3 -I score.py manifest.json result.json   (manifest: list of {task, variant, src, path, why})"""
import sys, json, importlib, traceback, io, contextlib
pass
sys.path.insert(1, "/tmp/bib/bibimbap")
import ifcopenshell
assert ifcopenshell.version == "0.8.3.post2", ifcopenshell.version
man = json.load(open(sys.argv[1]))
res = []
for m in man:
    mod = importlib.import_module(f"data.tests.{m['task']}")
    r = dict(m)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            met = mod.execute_test(m["src"], m["path"], m.get("model_output", "Done. The edit was applied successfully."))
        r["metrics"] = {k: (float(v) if isinstance(v, (bool, int, float)) else v) for k, v in met.items()}
        r["score"] = sum(float(v) for v in met.values()) / len(met) if met else 0.0
    except Exception as ex:
        r["metrics"] = {"EXCEPTION": type(ex).__name__ + ": " + str(ex)[:150]}
        r["score"] = 0.0
    res.append(r)
    print(f"{m['task']:22s} {m['variant']:28s} {r['score']:.3f} {r['metrics']}", flush=True)
json.dump({"ifcopenshell": ifcopenshell.version, "results": res}, open(sys.argv[2], "w"), indent=1)
