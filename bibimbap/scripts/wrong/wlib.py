"""Operations for building deliberately WRONG edited IFCs (criterion 4).
All deltas are given in metres (SI) in GLOBAL coordinates; converted to project units here."""
import numpy as np
import ifcopenshell
import ifcopenshell.api
import ifcopenshell.guid
import ifcopenshell.util.unit as uu
import ifcopenshell.util.placement as up
import ifcopenshell.util.element as ue

run = ifcopenshell.api.run


def S(f):
    return 1.0 / uu.calculate_unit_scale(f)  # SI -> project units


def body_rep(el):
    for r in el.Representation.Representations:
        if r.RepresentationIdentifier == "Body":
            return r
    return el.Representation.Representations[0]


def _mat(el):
    return np.array(up.get_local_placement(el.ObjectPlacement), dtype=float)


def _parent_mat(el):
    rel = el.ObjectPlacement.PlacementRelTo
    return np.eye(4) if rel is None else np.array(up.get_local_placement(rel), dtype=float)


def gmove(f, el, d):
    """Move element's ObjectPlacement by global delta d (m). Children placed relative to it follow."""
    d = np.array(d, float) * S(f)
    P = _parent_mat(el)
    dl = P[:3, :3].T @ d
    lp = el.ObjectPlacement
    rp = lp.RelativePlacement
    loc = list(rp.Location.Coordinates) + [0.0] * (3 - len(rp.Location.Coordinates))
    newloc = f.createIfcCartesianPoint(tuple(float(a + b) for a, b in zip(loc, dl)))
    lp.RelativePlacement = f.createIfcAxis2Placement3D(newloc, rp.Axis, rp.RefDirection)


def grotate_about(f, el, deg, centre_xy_m):
    """Rotate element's placement about global vertical axis through centre (m)."""
    s = S(f)
    M = _mat(el)
    a = np.radians(deg)
    R = np.array([[np.cos(a), -np.sin(a), 0, 0], [np.sin(a), np.cos(a), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    c = np.array([centre_xy_m[0] * s, centre_xy_m[1] * s, 0])
    T1 = np.eye(4); T1[:3, 3] = -c
    T2 = np.eye(4); T2[:3, 3] = c
    Mn = T2 @ R @ T1 @ M
    P = _parent_mat(el)
    L = np.linalg.inv(P) @ Mn
    el.ObjectPlacement.RelativePlacement = f.createIfcAxis2Placement3D(
        f.createIfcCartesianPoint(tuple(float(x) for x in L[:3, 3])),
        f.createIfcDirection(tuple(float(x) for x in L[:3, 2])),
        f.createIfcDirection(tuple(float(x) for x in L[:3, 0])))


def _wrap_body(f, el, op):
    """Replace the element's Body representation with a mapped item of the old one using operator op."""
    old = body_rep(el)
    origin = f.createIfcAxis2Placement3D(f.createIfcCartesianPoint((0.0, 0.0, 0.0)), None, None)
    rmap = f.createIfcRepresentationMap(origin, old)
    item = f.createIfcMappedItem(rmap, op)
    new = f.createIfcShapeRepresentation(old.ContextOfItems, "Body", "MappedRepresentation", [item])
    pds = el.Representation
    # own copy of the product definition shape so shared shapes are not touched
    reps = [new if r == old else r for r in pds.Representations]
    el.Representation = f.createIfcProductDefinitionShape(pds.Name, pds.Description, reps)


def rep_shift(f, el, d):
    """Shift the element's Body geometry by global delta d (m) WITHOUT touching its ObjectPlacement."""
    d = np.array(d, float) * S(f)
    dl = _mat(el)[:3, :3].T @ d
    op = f.createIfcCartesianTransformationOperator3D(None, None,
                                                       f.createIfcCartesianPoint(tuple(float(x) for x in dl)), 1.0, None)
    _wrap_body(f, el, op)


def rep_scale(f, el, sx, sy, sz, about_local=(0.0, 0.0, 0.0)):
    """Non-uniform scale of Body geometry in the element's LOCAL axes about a local point (m)."""
    s = S(f)
    c = np.array(about_local, float) * s
    origin = c - np.array([sx * c[0], sy * c[1], sz * c[2]])
    op = f.createIfcCartesianTransformationOperator3DnonUniform(
        f.createIfcDirection((1.0, 0.0, 0.0)), f.createIfcDirection((0.0, 1.0, 0.0)),
        f.createIfcCartesianPoint(tuple(float(x) for x in origin)), float(sx), f.createIfcDirection((0.0, 0.0, 1.0)),
        float(sy), float(sz))
    _wrap_body(f, el, op)


def fake_move(f, el, d):
    """Placement says 'moved by d' but geometry is shifted back by -d, so the element stays where it was."""
    gmove(f, el, d)
    rep_shift(f, el, -np.array(d, float))


def dup(f, el):
    """Coincident duplicate of an element: new GUID, same placement/geometry, same container."""
    new = f.create_entity(el.is_a(), ifcopenshell.guid.new())
    for i in range(len(el)):
        name = el.attribute_name(i)
        if name in ("GlobalId",):
            continue
        try:
            setattr(new, name, el[i])
        except Exception:
            pass
    new.Name = (el.Name or "") + " (copy)"
    lp = el.ObjectPlacement
    new.ObjectPlacement = f.createIfcLocalPlacement(lp.PlacementRelTo, lp.RelativePlacement)
    c = ue.get_container(el)
    if c is not None:
        run("spatial.assign_container", f, products=[new], relating_structure=c)
    else:
        agg = ue.get_aggregate(el)
        if agg is not None:
            run("aggregate.assign_object", f, products=[new], relating_object=agg)
    return new


def remove(f, el):
    run("root.remove_product", f, product=el)


def dirty_remove(f, el):
    f.remove(el)


def strip_fill_void(f, door):
    """Remove the door's opening + fills/voids relations (door stays, wall is not cut)."""
    for rel in list(f.by_type("IfcRelFillsElement")):
        if rel.RelatedBuildingElement == door:
            op = rel.RelatingOpeningElement
            f.remove(rel)
            run("root.remove_product", f, product=op)
