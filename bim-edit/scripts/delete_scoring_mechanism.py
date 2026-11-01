"""삭제 과제 의미 점수와 채점기가 찾은 비교 대상(best_match_guid)의 관계 집계.
실행 위치: BIM-Edit 작업 폴더  (python delete_scoring_mechanism.py)
"""
import collections
import csv
import json
import os

T = {}
for line in open('data/tasks/tasks.jsonl', encoding='utf-8'):
    t = json.loads(line)
    T[t['task_id']] = t
aud = {(r['model'], r['task_id']): r
       for r in csv.DictReader(open('analysis/delete_audit.csv', encoding='utf-8-sig'))}

# 1) 4개 모델 인공 장면: 우리 감사(target_removed) x 채점기 비교 대상 x 의미 점수
tab = collections.Counter()
for m in ['claude-sonnet', 'gemini-flash-3.0', 'gpt-5.4', 'gpt-5.4-mini']:
    d = json.load(open(f'data/runs/{m}/eval/eval_cache.json', encoding='utf-8'))
    for tid, e in d.items():
        a = aud.get((m, tid))
        if e.get('operation') != 'delete' or a is None:
            continue
        bm = e.get('best_match_guid')
        where = 'none' if bm is None else ('target' if bm in T[tid]['target']['guids'] else 'other')
        n_gt = e.get('geometry_breakdown', {}).get('n_gt')
        tab[(a['target_removed'], a['gt_valid'], where, e['semantics'],
             json.dumps(e.get('semantics_breakdown')), n_gt)] += 1
for k, v in sorted(tab.items(), key=lambda x: -x[1]):
    print(v, k)

# 2) 7개 모델 전체 삭제 기록: 의미>0 <=> 비교 대상 찾음
c = collections.Counter()
for m in sorted(os.listdir('data/runs')):
    p = f'data/runs/{m}/eval/eval_cache.json'
    if not os.path.exists(p):
        continue
    for tid, e in json.load(open(p, encoding='utf-8')).items():
        if e.get('operation') == 'delete':
            c[(m, e.get('best_match_guid') is not None, (e.get('semantics') or 0) > 0)] += 1
for k, v in sorted(c.items()):
    print(k, v)
