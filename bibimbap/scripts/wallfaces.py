"""Axis-aligned wall face classifier: samples each vertical face of box-shaped walls on a grid,
classifies sample points (offset 1 mm outward) as hidden (inside another wall), inner (inside a room
interior box), outer (else); points inside an opening box are voids (net)."""
from lib import *

def boxes(f, t):
    out = {}
    for e in f.by_type(t):
        s = shape(e, openings=False)
        if s is not None:
            lo, hi = bbox(s); out[e.GlobalId] = (lo, hi)
    return out

def classify(path, gids, interior, step=0.005):
    f = open_(path)
    W = boxes(f, 'IfcWall'); O = boxes(f, 'IfcOpeningElement')
    res = {}
    for g in gids:
        lo, hi = W[g]
        acc = {k: 0. for k in ('inner_net', 'outer_net', 'inner_gross', 'outer_gross', 'hidden')}
        zs = np.arange(lo[2] + step / 2, hi[2], step)
        sides = [  # (axis fixed, value, normal sign, along-axis)
            (0, lo[0], -1, 1), (0, hi[0], 1, 1), (1, lo[1], -1, 0), (1, hi[1], 1, 0)]
        for ax, val, sg, al in sides:
            ts = np.arange(lo[al] + step / 2, hi[al], step)
            for t in ts:
                p = np.zeros(2); p[ax] = val + sg * 0.001; p[al] = t
                hidden = any(o != g and W[o][0][0] < p[0] < W[o][1][0] and W[o][0][1] < p[1] < W[o][1][1] for o in W)
                if hidden:
                    acc['hidden'] += step * (hi[2] - lo[2]); continue
                side = 'inner' if any(b[0] < p[0] < b[2] and b[1] < p[1] < b[3] for b in interior) else 'outer'
                acc[side + '_gross'] += step * (hi[2] - lo[2])
                # net: remove points in openings (face point itself, slightly inside wall)
                q = p.copy(); q[ax] = val - sg * 0.001
                void = 0
                for olo, ohi in O.values():
                    if olo[0] - 1e-6 <= q[0] <= ohi[0] + 1e-6 and olo[1] - 1e-6 <= q[1] <= ohi[1] + 1e-6:
                        void += np.sum((zs > olo[2]) & (zs < ohi[2])) * step
                acc[side + '_net'] += step * ((hi[2] - lo[2]) - void)
        res[g] = {k: round(v, 3) for k, v in acc.items()}
    tot = {k: round(sum(r[k] for r in res.values()), 3) for k in acc}
    return res, tot
