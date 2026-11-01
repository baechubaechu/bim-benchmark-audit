import ifcopenshell, ifcopenshell.geom, ifcopenshell.util.element as ue, ifcopenshell.util.shape as us, ifcopenshell.util.unit as uu
import numpy as np
D = '/tmp/bib/olddata/data/ifc/'

def open_(p, strip=True):
    f = ifcopenshell.open(D + p)
    if strip:  # in-memory only: keep Body reps so the iterator does not pick Axis/FootPrint curves
        for pr in f.by_type('IfcProductDefinitionShape'):
            reps = [r for r in pr.Representations if r.RepresentationIdentifier in ('Body', None, 'Facetation')]
            if reps and len(reps) != len(pr.Representations):
                pr.Representations = reps
    return f

_settings = ifcopenshell.geom.settings()
_settings.set('use-world-coords', True)
_settings_nodisc = ifcopenshell.geom.settings()
_settings_nodisc.set('use-world-coords', True)
_settings_nodisc.set('disable-opening-subtractions', True)

def shape(e, openings=True):
    try:
        return ifcopenshell.geom.create_shape(_settings if openings else _settings_nodisc, e)
    except Exception as ex:
        return None

def verts(sh):
    return np.array(sh.geometry.verts).reshape(-1, 3)

def faces(sh):
    return np.array(sh.geometry.faces).reshape(-1, 3)

def bbox(sh):
    v = verts(sh)
    return v.min(0), v.max(0)

def volume(sh):
    return us.get_volume(sh.geometry)

def scale(f):
    return uu.calculate_unit_scale(f)  # to metres

def mesh_area_by_normal(sh):
    v = verts(sh); F = faces(sh)
    out = []
    for a, b, c in F:
        n = np.cross(v[b] - v[a], v[c] - v[a])
        ar = np.linalg.norm(n) / 2
        if ar > 0:
            out.append((n / np.linalg.norm(n), ar, (v[a] + v[b] + v[c]) / 3))
    return out

def psets(e):
    return ue.get_psets(e)

def summary(f, types=('IfcWall', 'IfcSpace', 'IfcSlab', 'IfcColumn', 'IfcOpeningElement', 'IfcDoor', 'IfcWindow', 'IfcBuildingStorey', 'IfcRoof', 'IfcCovering')):
    s = scale(f)
    for t in types:
        for e in f.by_type(t):
            sh = shape(e)
            line = f"{t:18s} {e.GlobalId} {e.Name!r}"
            if sh:
                lo, hi = bbox(sh)
                line += f" bbox_m={np.round(lo*1,3).tolist()}..{np.round(hi*1,3).tolist()} vol={volume(sh):.4f}"
            print(line)

def axis_info(e):
    """Axis polyline length (file units) and Body extrusion profile dims."""
    out = {}
    for r in e.Representation.Representations:
        for it in r.Items:
            if r.RepresentationIdentifier == 'Axis' and it.is_a('IfcPolyline'):
                p = np.array([pt.Coordinates for pt in it.Points], float)
                out['axis_len'] = float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())
            if it.is_a('IfcExtrudedAreaSolid'):
                prof = it.SweptArea
                out['extr_depth'] = it.Depth
                out['profile'] = prof.is_a()
                if prof.is_a('IfcRectangleProfileDef'):
                    out['xdim'] = prof.XDim; out['ydim'] = prof.YDim
                elif prof.is_a('IfcArbitraryClosedProfileDef'):
                    c = prof.OuterCurve
                    if c.is_a('IfcPolyline'):
                        out['poly'] = [tuple(pt.Coordinates) for pt in c.Points]
                    elif c.is_a('IfcIndexedPolyCurve'):
                        out['poly'] = [tuple(x) for x in c.Points.CoordList]
    return out

def poly_area(pts):
    p = np.array(pts, float)[:, :2]
    if np.allclose(p[0], p[-1]): p = p[:-1]
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

def poly_perim(pts):
    p = np.array(pts, float)[:, :2]
    if not np.allclose(p[0], p[-1]): p = np.vstack([p, p[:1]])
    return float(np.linalg.norm(np.diff(p, axis=0), axis=1).sum())

def qtos(e):
    return {k: v for k, v in ue.get_psets(e, qtos_only=True).items()}
