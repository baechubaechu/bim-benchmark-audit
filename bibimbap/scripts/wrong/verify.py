"""Independent evidence of what each wrong variant actually changed: world bboxes (ifcopenshell 0.8.3 geometry)
of every product in source vs edited file. Reports added/removed products and products whose bbox moved > 5 mm.
Usage: python3 -I verify.py manifest.json verify.json"""
import sys, json
import numpy as np, ifcopenshell, ifcopenshell.geom, ifcopenshell.util.shape as us
st = ifcopenshell.geom.settings()
cache = {}


def boxes(path):
    if path in cache:
        return cache[path]
    f = ifcopenshell.open(path); out = {}
    for p in f.by_type("IfcProduct"):
        if not p.Representation or p.is_a("IfcSpatialStructureElement") and not p.is_a("IfcSpace"):
            continue
        try:
            sh = ifcopenshell.geom.create_shape(st, p); v = us.get_shape_vertices(sh, sh.geometry)
            out[p.GlobalId] = (p.is_a(), [round(float(x), 3) for x in (v[:, 0].min(), v[:, 0].max(), v[:, 1].min(), v[:, 1].max(), v[:, 2].min(), v[:, 2].max())])
        except Exception as e:
            out[p.GlobalId] = (p.is_a(), None)
    cache[path] = out
    return out


man = json.load(open(sys.argv[1])); res = []
for m in man:
    a, b = boxes(m["src"]), boxes(m["path"])
    added = {g: b[g] for g in b if g not in a}
    removed = {g: a[g][0] for g in a if g not in b}
    changed = {}
    for g in a:
        if g in b and a[g][1] and b[g][1] and max(abs(x - y) for x, y in zip(a[g][1], b[g][1])) > 0.005:
            changed[g] = {"cls": a[g][0], "before": a[g][1], "after": b[g][1]}
    r = dict(task=m["task"], variant=m["variant"], added=added, removed=removed, changed=changed)
    res.append(r)
    print(m["task"], m["variant"], "added", [(v[0], v[1]) for v in added.values()], "removed", list(removed.values()),
          "changed", {g: (c["cls"], c["before"], c["after"]) for g, c in changed.items()}, flush=True)
json.dump(res, open(sys.argv[2], "w"), indent=1)
