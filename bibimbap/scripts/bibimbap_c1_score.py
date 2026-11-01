import sys, os, csv, json, importlib
REPO, DATA, OUT = sys.argv[1:4]; sys.path.insert(0, REPO)
import ifcopenshell; print("ifcopenshell", ifcopenshell.version)
res = {}
for r in csv.DictReader(open(f"{DATA}/prompts/all_questions.csv", encoding="utf-8-sig")):
    if r["CRUD"] != "delete": continue
    mod = importlib.import_module(f"data.tests.{r['test']}")
    for v in "ABC":
        try: m = mod.execute_test(os.path.join(DATA, "ifc", r["ifc-file"]), f"{OUT}/{r['test']}_{v}.ifc", ""); sc = sum(m.values()) / len(m)
        except Exception as ex: m = {"CRASH": type(ex).__name__}; sc = 0
        res[f"{r['test']}_{v}"] = (m, sc)
for v in "ABC":
    s = [res[k][1] for k in res if k.endswith(v)]
    print(v, "full", sum(1 for a in s if a == 1), "avg", round(sum(s) / len(s) * 100, 1))
json.dump(res, open(sys.argv[4], "w"), indent=1)
