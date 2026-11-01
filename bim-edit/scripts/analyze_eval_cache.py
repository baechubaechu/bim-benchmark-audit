"""7개 모델 eval_cache.json을 하나의 표로 펼쳐 analysis/eval_flat.csv 저장 + 요약 출력."""
import json, os, pandas as pd
base='data/runs'; rows=[]
for m in sorted(os.listdir(base)):
    p=f'{base}/{m}/eval/eval_cache.json'
    if not os.path.exists(p): continue
    ec=json.load(open(p,encoding='utf-8'))
    for tid,e in ec.items():
        gb=e.get('geometry_breakdown',{}) or {}; sb=e.get('semantics_breakdown',{}) or {}
        om=e.get('other_metrics',{}) or {}
        rows.append(dict(model=m,task_id=e.get('task_id',tid),op=e.get('operation'),cat=e.get('category'),
            scene='A' if '-A-' in tid else 'R', elem=tid.split('-')[0],
            geo=e.get('geometry'),sem_score=e.get('semantics'),topo=e.get('topology'),final=e.get('final_score'),
            class_match_top=e.get('class_match'),sem_class=sb.get('class_match'),sem_prop=sb.get('properties'),
            n_gt=gb.get('n_gt'),n_matched=gb.get('n_matched'),n_unmatched=gb.get('n_unmatched_candidates'),
            code_executed=om.get('execution.code_executed'),inst_recall=om.get('instance.instance_recall')))
df=pd.DataFrame(rows); os.makedirs('analysis',exist_ok=True); df.to_csv('analysis/eval_flat.csv',index=False,encoding='utf-8-sig')
print(len(df),'rows')
d=df[df.op=='delete']
print('\n[delete] top-level class_match vs sem score (all models, all scenes)')
print(pd.crosstab(d.class_match_top,(d.sem_score>=0.98).map({True:'sem=1',False:'sem<1'})))
print(pd.crosstab([d.n_matched],(d.sem_score>=0.98).map({True:'sem=1',False:'sem<1'})))
print('max final delete:',d.final.max())
c=df[df.op=='create']
print('\n[create] all-zero runs:',((c.final<=0.02)).sum(),'/',len(c))
z=c[c.final<=0.02]
print(pd.crosstab(z.n_unmatched.fillna(-1),z.n_matched.fillna(-1)))
print('\nsolved(all>=.98) by op:\n',df.assign(s=(df.geo>=.98)&(df.sem_score>=.98)&(df.topo>=.98)).groupby('op').s.agg(['sum','count']))
