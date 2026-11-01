"""ifcopenshell 없이 IFC(STEP) 파일에서 객체의 월드좌표 bounding box를 근사 계산하는 최소 파서.
지원: LocalPlacement/Axis2Placement3D, ExtrudedAreaSolid(Rectangle/ArbitraryClosed/Polyline 프로파일),
MappedItem, BooleanClippingResult(첫 피연산자), FacetedBrep/PolyLoop. 그 외는 참조된 CartesianPoint로 근사."""
import re, numpy as np
ENT = re.compile(r"#(\d+)\s*=\s*([A-Z0-9_]+)\s*\((.*)\)\s*;\s*$", re.S)
def _split(s):
    out, depth, cur, inq = [], 0, '', False
    i = 0
    while i < len(s):
        c = s[i]
        if inq:
            cur += c
            if c == "'":
                if i+1 < len(s) and s[i+1] == "'": cur += "'"; i += 1
                else: inq = False
        elif c == "'": inq = True; cur += c
        elif c == '(': depth += 1; cur += c
        elif c == ')': depth -= 1; cur += c
        elif c == ',' and depth == 0: out.append(cur.strip()); cur = ''
        else: cur += c
        i += 1
    if cur.strip() or out: out.append(cur.strip())
    return out
def _val(t):
    if t.startswith('#'): return ('ref', int(t[1:]))
    if t.startswith("'"): return t[1:-1]
    if t.startswith('('): return [_val(x) for x in _split(t[1:-1])] if t[1:-1].strip() else []
    if t in ('$', '*'): return None
    if t.startswith('.'): return t
    m = re.match(r'([A-Z0-9_]+)\((.*)\)$', t, re.S)
    if m: return (m.group(1), [_val(x) for x in _split(m.group(2))])
    try: return float(t)
    except ValueError: return t
class Model:
    def __init__(self, path):
        txt = open(path, encoding='utf-8', errors='replace').read()
        data = txt.split('DATA;', 1)[1].split('ENDSEC;', 1)[0]
        self.raw = {}
        for stmt in re.split(r';\s*\n', data):
            m = ENT.match(stmt.strip() + ';')
            if m: self.raw[int(m.group(1))] = (m.group(2), m.group(3))
        self.cache = {}
    def get(self, i):
        if i not in self.cache:
            t, a = self.raw[i]; self.cache[i] = (t, [_val(x) for x in _split(a)])
        return self.cache[i]
    def by_type(self, *types):
        types = {t.upper() for t in types}
        return [i for i, (t, _) in self.raw.items() if t in types]
    def guid(self, i): return self.get(i)[1][0]
    # ---- geometry ----
    def _pt(self, r): return np.array((self.get(r[1])[1][0] + [0, 0, 0])[:3], float)
    def _dir(self, r, d):
        if r is None: return np.array(d, float)
        v = np.array((self.get(r[1])[1][0] + [0, 0, 0])[:3], float); n = np.linalg.norm(v); return v / n if n else np.array(d, float)
    def axis_mat(self, r):
        M = np.eye(4)
        if r is None: return M
        t, a = self.get(r[1])
        loc = self._pt(a[0])
        if t == 'IFCAXIS2PLACEMENT2D':
            x = self._dir(a[1] if len(a) > 1 else None, (1, 0, 0)); z = np.array([0, 0, 1.])
        else:
            z = self._dir(a[1] if len(a) > 1 else None, (0, 0, 1)); x = self._dir(a[2] if len(a) > 2 else None, (1, 0, 0))
        x = x - z * x.dot(z); x = x / (np.linalg.norm(x) or 1); y = np.cross(z, x)
        M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x, y, z, loc
        return M
    def placement(self, r):
        if r is None: return np.eye(4)
        t, a = self.get(r[1])
        if t != 'IFCLOCALPLACEMENT': return np.eye(4)
        return self.placement(a[0]) @ self.axis_mat(a[1])
    def _profile_pts(self, r):
        t, a = self.get(r[1])
        if t == 'IFCRECTANGLEPROFILEDEF':
            P = self.axis_mat(a[2]); hx, hy = a[3] / 2, a[4] / 2
            pts = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
            return [(P @ np.array([x, y, 0, 1]))[:3] for x, y in pts]
        if t in ('IFCARBITRARYCLOSEDPROFILEDEF', 'IFCARBITRARYPROFILEDEFWITHVOIDS'):
            return self._curve_pts(a[2])
        return self._all_pts(r)
    def _curve_pts(self, r):
        t, a = self.get(r[1])
        if t == 'IFCPOLYLINE': return [self._pt(p) for p in a[0]]
        if t == 'IFCINDEXEDPOLYCURVE':
            pl = self.get(a[0][1])[1][0]; return [np.array((p + [0, 0])[:3], float) for p in pl]
        return self._all_pts(r)
    def _all_pts(self, r, seen=None):
        seen = seen or set(); out = []
        stack = [r[1]]
        while stack:
            i = stack.pop()
            if i in seen: continue
            seen.add(i); t, a = self.get(i)
            if t == 'IFCCARTESIANPOINT': out.append(np.array((a[0] + [0, 0, 0])[:3], float)); continue
            if t == 'IFCCARTESIANPOINTLIST3D': out += [np.array(p, float) for p in a[0]]; continue
            def walk(v):
                if isinstance(v, tuple) and v[0] == 'ref': stack.append(v[1])
                elif isinstance(v, list): [walk(x) for x in v]
            walk(a)
        return out
    def item_pts(self, r, M):
        t, a = self.get(r[1])
        if t == 'IFCEXTRUDEDAREASOLID':
            P = M @ self.axis_mat(a[1]); d = self._dir(a[2], (0, 0, 1)) * a[3]
            base = self._profile_pts(a[0]); pts = base + [p + d for p in base]
        elif t in ('IFCBOOLEANCLIPPINGRESULT', 'IFCBOOLEANRESULT'):
            return self.item_pts(a[1], M)
        elif t == 'IFCMAPPEDITEM':
            src = self.get(a[0][1])[1]; O = self.axis_mat(src[0])
            T = self._cto(a[1]); pts = []
            for it in self.get(src[1][1])[1][3]: pts += self.item_pts(it, M @ T @ O)
            return pts
        else:
            P = M; pts = self._all_pts(r)
        return [(P @ np.append(p, 1))[:3] for p in pts]
    def _cto(self, r):
        t, a = self.get(r[1]); M = np.eye(4)
        x = self._dir(a[0], (1, 0, 0)); y = self._dir(a[1], (0, 1, 0)); o = self._pt(a[2]); s = a[3] if len(a) > 3 and a[3] else 1.0
        z = self._dir(a[4], (0, 0, 1)) if len(a) > 4 else np.cross(x, y)
        M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = x * s, y * s, z * s, o
        return M
    def bbox(self, i):
        t, a = self.get(i)
        if len(a) < 7 or a[6] is None: return None
        M = self.placement(a[5]); pts = []
        for rep in self.get(a[6][1])[1][2]:
            rt, ra = self.get(rep[1])
            if ra[1] not in ('Body', 'Facetation', 'Reference', None) and len(ra[3]) and ra[1] != 'Body': continue
            for it in ra[3]: pts += self.item_pts(it, M)
        if not pts: return None
        P = np.array(pts); return P.min(0), P.max(0)
