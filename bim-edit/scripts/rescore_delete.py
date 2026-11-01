"""삭제 과제 semantics를 '평가기가 제거 대상을 정답과 짝지었는가(n_matched=1)'로 바꿔 재채점한 민감도 분석."""
import pandas as pd
d = pd.read_csv('analysis/eval_flat.csv')
d['sem_fix'] = d.sem_score
m = d.op == 'delete'; d.loc[m, 'sem_fix'] = (d.loc[m, 'n_matched'] >= 1).astype(float)
d['final_fix'] = (d.geo + d.sem_fix + d.topo) / 3
sv = lambda g, s: ((g.geo >= .98) & (g[s] >= .98) & (g.topo >= .98))
out = d.groupby('model').apply(lambda g: pd.Series({
    'mean_orig': g.final.mean(), 'mean_fix': g.final_fix.mean(),
    'solved_orig': sv(g, 'sem_score').sum(), 'solved_fix': sv(g, 'sem_fix').sum(),
    'delete_solved_fix': sv(g[g.op == 'delete'], 'sem_fix').sum()}), include_groups=False).round(3)
out['rank_orig'] = out.mean_orig.rank(ascending=False).astype(int); out['rank_fix'] = out.mean_fix.rank(ascending=False).astype(int)
print(out.sort_values('mean_fix', ascending=False).to_string())
out.to_csv('analysis/rescore_delete.csv', encoding='utf-8-sig')
