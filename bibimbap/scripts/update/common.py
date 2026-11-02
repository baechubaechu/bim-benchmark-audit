import numpy as np
import ifcopenshell.geom

_S = ifcopenshell.geom.settings()
_S.set(_S.USE_WORLD_COORDS, True)


def bbox(e):
    """World bounding box of e's geometry in metres: (min xyz, max xyz)."""
    sh = ifcopenshell.geom.create_shape(_S, e)
    v = np.array(sh.geometry.verts).reshape(-1, 3)
    return v.min(0), v.max(0)
