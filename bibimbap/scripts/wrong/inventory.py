import sys, json, ifcopenshell, ifcopenshell.geom, ifcopenshell.util.shape as us
D="/tmp/bib/olddata/data/ifc/"
files=sys.argv[1:]
st=ifcopenshell.geom.settings()
out={}
for fn in files:
    f=ifcopenshell.open(D+fn); rows=[]
    for p in f.by_type("IfcProduct"):
        if not p.Representation: continue
        try:
            sh=ifcopenshell.geom.create_shape(st,p); v=us.get_shape_vertices(sh,sh.geometry)
            bb=[round(float(x),3) for x in (v[:,0].min(),v[:,0].max(),v[:,1].min(),v[:,1].max(),v[:,2].min(),v[:,2].max())]
        except Exception as e: bb=str(e)[:40]
        par=p.ObjectPlacement.PlacementRelTo if p.ObjectPlacement else None
        owner=[x for x in f.get_inverse(par) if x.is_a("IfcProduct")] if par else []
        rows.append((p.is_a(),p.GlobalId,(p.Name or "")[:30],bb,[o.GlobalId for o in owner if o.ObjectPlacement==par][:1]))
    out[fn]=rows
    print("####",fn, f.schema)
    for r in rows: print(" ",r)
