"""Placement edits for the UPDATE answers. Matrices and offsets are in the file's length unit (mm in these files).
An element's own IfcLocalPlacement is rewritten in place, so its placement children (e.g. a door in its opening) follow."""
import numpy as np
import ifcopenshell.util.placement as up


def world(e):
    """4x4 world matrix of e's ObjectPlacement (file units)."""
    return up.get_local_placement(e.ObjectPlacement)


def set_world(f, e, M):
    """Give e the world matrix M, keeping its PlacementRelTo parent."""
    lp = e.ObjectPlacement
    P = up.get_local_placement(lp.PlacementRelTo) if lp.PlacementRelTo else np.eye(4)
    L = np.linalg.inv(P) @ M
    lp.RelativePlacement = f.createIfcAxis2Placement3D(
        f.createIfcCartesianPoint(tuple(float(v) for v in L[:3, 3])),
        f.createIfcDirection(tuple(float(v) for v in L[:3, 2])),
        f.createIfcDirection(tuple(float(v) for v in L[:3, 0])))


def translate(f, e, d):
    M = world(e).copy()
    M[:3, 3] += np.asarray(d, float)
    set_world(f, e, M)


def rotate_z_about(f, e, deg, c):
    """Rotate e by deg about the vertical axis through world point c (file units)."""
    a = np.radians(deg)
    R = np.eye(4); R[:2, :2] = [[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]
    T = np.eye(4); T[:3, 3] = np.asarray(c, float)[:3]
    Ti = np.eye(4); Ti[:3, 3] = -np.asarray(c, float)[:3]
    set_world(f, e, T @ R @ Ti @ world(e))
