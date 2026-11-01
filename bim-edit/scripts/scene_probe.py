import json, re, sys, ifcopenshell, ifcopenshell.geom, numpy as np
D='./data/gt/simple/'
S=ifcopenshell.geom.settings(); S.set('use-world-coords', True); S.set('context-identifiers',['Body'])
TYPES=('IfcWall','IfcWallStandardCase','IfcDoor','IfcWindow','IfcSlab','IfcSpace','IfcColumn','IfcOpeningElement')
def bbox(f,e):
    try:
        sh=ifcopenshell.geom.create_shape(S,e); v=np.array(sh.geometry.verts).reshape(-1,3)
        return np.round(v.min(0),3).tolist(), np.round(v.max(0),3).tolist()
    except Exception:
        try:
            import ifcopenshell.util.placement as up
            rep=[r for r in e.Representation.Representations if r.RepresentationIdentifier=='Body'][0]
            sh=ifcopenshell.geom.create_shape(ifcopenshell.geom.settings(),rep)
            v=np.array(sh.verts).reshape(-1,3); M=up.get_local_placement(e.ObjectPlacement)
            v=(M[:3,:3]@v.T).T+M[:3,3]
            return np.round(v.min(0),3).tolist(), np.round(v.max(0),3).tolist()
        except Exception as ex: return 'ERR '+str(ex)[:60]
cache={}
def load(p):
    if p not in cache: cache[p]=ifcopenshell.open(D+p)
    return cache[p]
rows=[json.loads(l) for l in open(sys.argv[1])]
for r in rows:
    if r['operation']!='create' or r['category']=='direct' or '-A-' not in r['task_id']: continue
    i=load(r['input_ifc'].split('/')[-1]); g=load(r['ground_truth_ifc'].split('/')[-1])
    ig={e.GlobalId for e in i.by_type('IfcRoot')}
    new=[e for t in TYPES for e in g.by_type(t) if e.GlobalId not in ig and e.is_a()==t or (e.is_a(t) and e.GlobalId not in ig and t=='IfcWall')]
    seen=set(); new=[e for e in new if not (e.GlobalId in seen or seen.add(e.GlobalId))]
    print('==',r['task_id'],'|',r['prompt'][:160])
    for e in new: print('  NEW',e.is_a(),e.GlobalId,e.Name,bbox(g,e))
    for gid in sorted(set(re.findall(r'[0-9A-Za-z_$]{22}',r['prompt']))):
        try: e=i.by_guid(gid); print('  REF',e.is_a(),gid,bbox(i,e))
        except Exception: print('  REF missing',gid)
# wall thickness census in inputs (bbox min horizontal extent)
import collections
for p in sorted(cache):
    if 'input' not in p: continue
    th=collections.Counter()
    for w in cache[p].by_type('IfcWall'):
        b=bbox(cache[p],w)
        if b: th[round(min(b[1][0]-b[0][0], b[1][1]-b[0][1]),3)]+=1
    print('THK',p,dict(th))
