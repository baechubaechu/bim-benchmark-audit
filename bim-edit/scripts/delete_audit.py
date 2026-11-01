"""삭제 과제 독립 감사 (채점기 매칭 결과를 쓰지 않음).
각 결과 IFC를 입력·정답 IFC와 직접 비교:
  target_removed   : 지시된 대상 GUID가 결과의 어떤 엔티티로도 남아 있지 않은가
  gt_valid         : 정답 IFC가 대상을 실제로 제거했는가
  products_equal_gt: 건물요소(전 종류) GUID 집합이 정답과 같은가
  extra_removed / missing_removed : 정답 대비 더 지운 요소 수 / 덜 지운 요소 수
  moved_remaining  : 남은 요소 중 경계상자가 입력 대비 1mm 넘게 바뀐 수(근사, ifc_lite)
verified_correct = gt_valid & target_removed & products_equal_gt & moved_remaining==0
"""
import json, glob, os, re, sys, numpy as np, pandas as pd
sys.path.insert(0, 'scripts'); from ifc_lite import Model
PROD = {'IFCWALL','IFCWALLSTANDARDCASE','IFCSLAB','IFCSPACE','IFCDOOR','IFCDOORSTANDARDCASE','IFCWINDOW','IFCWINDOWSTANDARDCASE',
        'IFCCOLUMN','IFCCOLUMNSTANDARDCASE','IFCBEAM','IFCOPENINGELEMENT','IFCCOVERING','IFCROOF','IFCSTAIR','IFCSTAIRFLIGHT',
        'IFCRAILING','IFCMEMBER','IFCPLATE','IFCFURNISHINGELEMENT','IFCBUILDINGELEMENTPROXY','IFCCURTAINWALL','IFCFOOTING'}
T = [json.loads(l) for l in open('data/tasks/tasks.jsonl', encoding='utf-8')]
flat = pd.read_csv('analysis/eval_flat.csv')
cache = {}
def M(p):
    if p not in cache: cache[p] = Model(p)
    return cache[p]
def prods(m): return {m.guid(i): i for i in m.by_type(*PROD)}
def anyguid(m): return {a for (t, a) in [(t, s.split(',', 1)[0].strip()) for t, s in m.raw.values()] if a.startswith("'")}
def bb(m, i):
    try: return m.bbox(i)
    except Exception: return None
rows = []
for t in [t for t in T if t['operation'] == 'delete' and '-A-' in t['task_id']]:
    inp = M('data/gt/simple/' + os.path.basename(t['input_ifc'])); gt = M('data/gt/simple/' + os.path.basename(t['ground_truth_ifc']))
    tg = set(t['target']['guids']); pin, pgt = prods(inp), prods(gt)
    gt_valid = not (tg & {g.strip("'") for g in anyguid(gt)})
    for d in sorted(glob.glob(f"data/runs/*/edited/{t['task_id']}")):
        fs = glob.glob(d + '/*.ifc')
        if not fs: continue
        e = M(fs[0]); ped = prods(e)
        target_removed = not (tg & {g.strip("'") for g in anyguid(e)})
        extra = len((set(pgt) - set(ped)))            # 정답엔 있는데 결과엔 없음 = 더 지움
        missing = len((set(ped) - set(pgt)) & set(pin)) # 정답엔 없는데 결과엔 남음 = 덜 지움
        added = len(set(ped) - set(pin))
        moved = 0
        for g in set(ped) & set(pin):
            a, b = bb(inp, pin[g]), bb(e, ped[g])
            if a is None or b is None: continue
            if np.abs(a[0] - b[0]).max() > 1e-3 or np.abs(a[1] - b[1]).max() > 1e-3: moved += 1
        rows.append(dict(model=d.split('/')[2], task_id=t['task_id'], gt_valid=gt_valid, target_removed=target_removed,
                         products_equal_gt=(set(ped) == set(pgt)), extra_removed=extra, missing_removed=missing,
                         added=added, moved_remaining=moved))
df = pd.DataFrame(rows)
df['verified_correct'] = df.gt_valid & df.target_removed & df.products_equal_gt & (df.moved_remaining == 0)
df = df.merge(flat[['model','task_id','geo','sem_score','topo','final','n_matched']], on=['model','task_id'], how='left')
df.to_csv('analysis/delete_audit.csv', index=False, encoding='utf-8-sig')
print(len(df), 'runs | GT-invalid tasks:', sorted(df[~df.gt_valid].task_id.unique()))
print('verified_correct:', df.verified_correct.sum())
v = df[df.verified_correct]
print('  their semantics: ', v.sem_score.round(2).value_counts().to_dict(), '| final max', round(v.final.max(),3), 'mean', round(v.final.mean(),3))
print('  their geo>=.98:', (v.geo>=.98).sum(), ' topo>=.98:', (v.topo>=.98).sum(), ' n_matched>=1:', (v.n_matched>=1).sum())
nv = df[df.gt_valid & ~df.target_removed]
print('target NOT removed (valid GT):', len(nv), '| sem=1:', (nv.sem_score>=.98).sum())
print(pd.crosstab(df.target_removed, df.sem_score>=.98, rownames=['target_removed'], colnames=['sem=1']))
print('moved_remaining>0 among target_removed:', ((df.moved_remaining>0)&df.target_removed).sum(), '| extra_removed>0:', ((df.extra_removed>0)&df.target_removed).sum())
