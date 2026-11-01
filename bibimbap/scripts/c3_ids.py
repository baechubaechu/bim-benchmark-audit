import csv, re, sys, os, json, ifcopenshell
REPO, DATA = sys.argv[1], sys.argv[2]
G = re.compile(r'''["']([0-9A-Za-z_$]{22})["']''')
GP = re.compile(r'(?<![0-9A-Za-z_$])([0-9A-Za-z_$]{22})(?![0-9A-Za-z_$])')
cache = {}
out = []
for r in csv.DictReader(open(f"{DATA}/prompts/all_questions.csv", encoding="utf-8-sig")):
    p = os.path.join(DATA, "ifc", r["ifc-file"])
    if p not in cache:
        f = ifcopenshell.open(p); cache[p] = {e.GlobalId: e.is_a() for e in f.by_type("IfcRoot")}
    ids = cache[p]
    src = open(f"{REPO}/data/tests/{r['test']}.py").read()
    tg = sorted(set(m for m in G.findall(src) if not m.isalpha() or any(c.isdigit() for c in m)))
    pg = sorted(set(m for m in GP.findall(r["question"]) if any(c.isdigit() for c in m)))
    miss_t = [g for g in tg if g not in ids]; miss_p = [g for g in pg if g not in ids]
    out.append(dict(test=r["test"], crud=r["CRUD"], ifc=r["ifc-file"], n_test_ids=len(tg), missing_test_ids=miss_t, n_prompt_ids=len(pg), missing_prompt_ids=miss_p))
    if miss_t or miss_p: print(r["test"], r["CRUD"], r["ifc-file"], "test ids", len(tg), "missing", miss_t, "| prompt ids", len(pg), "missing", miss_p)
json.dump(out, open(sys.argv[3], "w"), indent=1)
print("tasks", len(out), "with missing:", sum(1 for o in out if o["missing_test_ids"] or o["missing_prompt_ids"]))
