"""인공(A) 장면 삭제 과제: 결과 IFC에 대상 GUID가 남았는지, 대상 외 같은 종류 객체 수 변화 → analysis/delete_check.csv"""
import json, glob, os, re, pandas as pd
T = [json.loads(l) for l in open('data/tasks/tasks.jsonl', encoding='utf-8')]
flat = pd.read_csv('analysis/eval_flat.csv')
TY = {'IfcWall': 'IFCWALL(?:STANDARDCASE)?', 'IfcSlab': 'IFCSLAB', 'IfcSpace': 'IFCSPACE', 'IfcDoor': 'IFCDOOR(?:STANDARDCASE)?', 'IfcColumn': 'IFCCOLUMN(?:STANDARDCASE)?', 'IfcWindow': 'IFCWINDOW(?:STANDARDCASE)?'}
txt = {}
def rd(p):
    if p not in txt: txt[p] = open(p, encoding='utf-8', errors='replace').read()
    return txt[p]
rows = []
for t in [t for t in T if t['operation'] == 'delete' and '-A-' in t['task_id']]:
    pat = re.compile(r'=\s*' + TY[t['target']['entity_type']] + r"\('([^']+)'")
    inp = rd('data/gt/simple/' + os.path.basename(t['input_ifc'])); gt = rd('data/gt/simple/' + os.path.basename(t['ground_truth_ifc']))
    gi, gg = set(pat.findall(inp)), set(pat.findall(gt)); tg = set(t['target']['guids'])
    for d in glob.glob(f"data/runs/*/edited/{t['task_id']}"):
        fs = glob.glob(d + '/*.ifc')
        if not fs: continue
        ge = set(pat.findall(rd(fs[0])))
        rows.append(dict(model=d.split('/')[2], task_id=t['task_id'], cat=t['category'], elem=t['target']['entity_type'],
            target_removed=not (tg & ge), gt_target_removed=not (tg & gg),
            other_same_type_removed=len((gi - tg) - ge), same_as_gt=(ge == gg)))
df = pd.DataFrame(rows).merge(flat[['model', 'task_id', 'geo', 'sem_score', 'topo', 'final', 'n_matched']], on=['model', 'task_id'], how='left')
df.to_csv('analysis/delete_check.csv', index=False, encoding='utf-8-sig')
print(len(df), 'runs; models:', sorted(df.model.unique()))
print('GT removes target in all tasks:', df.gt_target_removed.all())
print(pd.crosstab(df.target_removed, df.sem_score >= 0.98, rownames=['target_removed'], colnames=['sem=1']))
ok = df[df.same_as_gt]
print('runs whose element set equals GT exactly:', len(ok), '| their final score: max', ok.final.max(), 'mean', round(ok.final.mean(), 3))
