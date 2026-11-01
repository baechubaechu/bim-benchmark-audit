"""점검 기준 C1~C4를 BIM-Edit 공개 자료에 적용하고 7개 모델 해결 수를 재집계.
실행 위치: BIM-Edit 작업 폴더(아래 README 참고). 채점 기록 eval_cache.json, 과제 tasks.jsonl,
인공 장면 IFC(data/gt/simple), 독립 감사 analysis/delete_audit.csv 사용.
사용: python checklist_audit.py <결과.json>"""
import json, os, csv, sys, collections
sys.path.insert(0, 'scripts'); from ifc_lite import Model
TH = 0.98
T = {}
for l in open('data/tasks/tasks.jsonl', encoding='utf-8'):
    t = json.loads(l); T[t['task_id']] = t
models = [m for m in sorted(os.listdir('data/runs')) if os.path.exists(f'data/runs/{m}/eval/eval_cache.json')]
E = {m: json.load(open(f'data/runs/{m}/eval/eval_cache.json', encoding='utf-8')) for m in models}
out = {}

def guids(path):
    m = Model(path)
    return {s.split(',', 1)[0].strip().strip("'") for (_, s) in m.raw.values()}

# ---- C2 정답 파일 / C3 대상 ID (인공 장면, 파일 직접 확인)
c2, c3, miss = [], [], []
for tid, t in T.items():
    if '-A-' not in tid or t['operation'] == 'create': continue
    tg = set(t['target']['guids'])
    pi = 'data/gt/simple/' + os.path.basename(t['input_ifc']); pg = 'data/gt/simple/' + os.path.basename(t['ground_truth_ifc'])
    if not (os.path.exists(pi) and os.path.exists(pg)): miss.append(tid); continue
    gi, gg = guids(pi), guids(pg)
    if not tg or not tg <= gi: c3.append((tid, sorted(tg - gi)))
    if t['operation'] == 'delete' and tg & gg: c2.append((tid, 'delete target still in GT'))
    if t['operation'] == 'update' and not tg <= gg: c2.append((tid, 'update target missing in GT'))
out['C2_file'] = c2; out['C3_file'] = c3; out['missing_files'] = miss

# ---- C3 채점기 쪽: 대상이 있어야 하는 과제(수정·삭제)인데 채점 기록에 정답 객체 0개
ngt0 = collections.defaultdict(set)
for m in models:
    for tid, e in E[m].items():
        if e.get('operation') in ('update', 'delete') and (e.get('geometry_breakdown') or {}).get('n_gt') == 0:
            ngt0[tid].add(m)
out['C3_record_ngt0'] = {k: sorted(v) for k, v in sorted(ngt0.items())}

# ---- C1 만점 답안: 지운(채점기 기준 비교 대상 없음, n_gt>=1) 삭제 기록의 의미 점수, 연산별 해결 수
def solved(s): return s['geometry'] >= TH and s['semantics'] >= TH and s['topology'] >= TH
c1 = collections.Counter()
for m in models:
    for tid, e in E[m].items():
        op = e.get('operation'); s = e.get('scores') or {}
        if not s: continue
        c1[(op, 'records')] += 1
        c1[(op, 'solved')] += solved(s)
        if op == 'delete' and (e.get('geometry_breakdown') or {}).get('n_gt', 0) >= 1 and e.get('best_match_guid') is None:
            c1[('delete', 'removed')] += 1
            c1[('delete', 'removed_sem>0')] += s['semantics'] > 0
out['C1'] = {f'{a}/{b}': v for (a, b), v in sorted(c1.items())}

# ---- C4 독립 확인: 4개 모델 인공 장면 (delete_audit.csv)
aud = {(r['model'], r['task_id']): r for r in csv.DictReader(open('analysis/delete_audit.csv', encoding='utf-8-sig'))}
c4 = collections.Counter()
for (m, tid), r in aud.items():
    e = E[m][tid]; c4[(r['gt_valid'], r['target_removed'], 'sem1' if e['semantics'] >= TH else 'sem<1')] += 1
out['C4'] = {str(k): v for k, v in sorted(c4.items())}
# 대리 판정(채점 기록: 비교 대상 없음 & n_gt>=1 → 지움) 의 정확도: 독립 감사와 대조
agree = collections.Counter()
for (m, tid), r in aud.items():
    e = E[m][tid]; ngt = (e.get('geometry_breakdown') or {}).get('n_gt', 0)
    if ngt < 1: agree['n_gt0(excluded)'] += 1; continue
    proxy = e.get('best_match_guid') is None
    agree['agree' if proxy == (r['target_removed'] == 'True') else 'disagree'] += 1
out['proxy_vs_audit'] = dict(agree)

# ---- 재집계: 삭제 과제에서 대상이 지워졌으면(대리 판정) 의미 = 1 (원 논문 E.2 정의)
bad = {tid for tid, _ in c2} | set(ngt0)  # 정답 오류·대상 ID 오류 과제는 양쪽 집계에서 제외
rows = []
for m in models:
    for scene in ('A', 'R', 'all'):
        o = c = n = 0
        for tid, e in E[m].items():
            if scene != 'all' and f'-{scene}-' not in tid: continue
            s = e.get('scores')
            if not s or tid in bad: continue
            n += 1; o += solved(s)
            s2 = dict(s)
            if e.get('operation') == 'delete' and (e.get('geometry_breakdown') or {}).get('n_gt', 0) >= 1 and e.get('best_match_guid') is None:
                s2['semantics'] = 1.0
            c += solved(s2)
        rows.append(dict(model=m, scene=scene, records=n, solved_published=o, solved_corrected=c))
out['rescore'] = rows
out['excluded_tasks'] = sorted(bad)
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in out.items():
    if k != 'rescore': print(k, v)
for r in rows: print(r)
