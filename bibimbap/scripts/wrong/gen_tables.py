"""Generate markdown tables + flagged list from results.json and verify.json."""
import json, collections
import os
B = os.environ.get("WORK", os.path.abspath("work")) + "/wrong/"
R = json.load(open(B + "results.json"))["results"]
V = {(v["task"], v["variant"]): v for v in json.load(open(B + "verify.json"))}
ABBR = {"object_exists": "OE", "object_not_exists": "ONE", "right_location": "RL", "right_dimensions": "RD", "integrity_constraint": "IC"}
ORDER = ["OE", "ONE", "RL", "RD", "IC"]


def met(m):
    if "EXCEPTION" in m:
        return "exception → 0 (" + m["EXCEPTION"][:60] + ")"
    d = {ABBR.get(k, k): v for k, v in m.items()}
    return " ".join(f"{k}={d[k]:g}" for k in ORDER if k in d)


def borderline(r):
    return any(s in r["family"] for s in ("by-design", "tolerance", "geometrically identical"))


by = collections.OrderedDict()
for r in R:
    by.setdefault(r["task"], []).append(r)

ref = {}
for t, rows in by.items():
    rr = [r for r in rows if r["family"] == "reference" and not r["variant"].startswith("ref_C")]
    ref[t] = rr[0]["score"]

flag, full = [], []
stats = collections.Counter()
for t, rows in by.items():
    for r in rows:
        if r["family"] in ("reference", "control"):
            full.append(f"| {t} | *{r['variant']}* ({r['family']}) | {r['why']} | {met(r['metrics'])} | {r['score']:.3f} |")
            continue
        stats["wrong"] += 1
        hi = r["score"] >= 0.9 - 1e-9 or (r["score"] >= ref[t] - 1e-9 and r["score"] > 0)
        if hi:
            stats["flag"] += 1
            if borderline(r):
                stats["flag_border"] += 1
            flag.append((t, r))
        mark = " **⚑**" if hi else ""
        full.append(f"| {t} | {r['variant']}{mark} | {r['why']} | {met(r['metrics'])} | {r['score']:.3f} |")

with open(B + "tables.md", "w") as f:
    f.write("FLAGGED\n\n| task | correct score | wrong variant | why it's wrong | metrics | score |\n|---|---|---|---|---|---|\n")
    for t, r in flag:
        b = " (borderline)" if borderline(r) else ""
        f.write(f"| {t} | {ref[t]:.3f} | {r['variant']}{b} | {r['why']} | {met(r['metrics'])} | {r['score']:.3f} |\n")
    f.write("\nFULL\n\n| task | variant | why | metrics | score |\n|---|---|---|---|---|\n" + "\n".join(full) + "\n")
    # verify evidence for flagged
    f.write("\nEVIDENCE\n\n")
    for t, r in flag:
        v = V.get((t, r["variant"]))
        if v:
            ch = {g: (c["cls"], c["before"], c["after"]) for g, c in v["changed"].items()}
            f.write(f"- {t} / {r['variant']}: added={[(a[0], a[1]) for a in v['added'].values()]} removed={list(v['removed'].values())} changed={ch}\n")
print(dict(stats))
pt = collections.OrderedDict()
for t, rows in by.items():
    w = [r for r in rows if r["family"] not in ("reference", "control")]
    hi = [r for r in w if r["score"] >= 0.9 - 1e-9 or (r["score"] >= ref[t] - 1e-9 and r["score"] > 0)]
    pt[t] = (ref[t], len(w), len(hi), max([r["score"] for r in w] or [0]), [r["variant"] for r in hi])
    print(f"{t:22s} ref={ref[t]:.3f} wrong={len(w):2d} flagged={len(hi):2d} max={pt[t][3]:.3f} {pt[t][4]}")
json.dump(pt, open(B + "per_task.json", "w"), indent=1)
