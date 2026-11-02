#!/usr/bin/env bash
# BIBIMBAP 점검 전체 재실행. 필요: ifcopenshell==0.8.3.post2, numpy, shapely
#   BIBIMBAP 저장소(커밋 667004e)  -> /tmp/bib/bibimbap
#   BIBIMBAP 데이터(커밋 a0291d6)  -> /tmp/bib/olddata   (git worktree add /tmp/bib/olddata a0291d6)
# 결과는 $WORK(기본 ./work) 아래에 생김.
set -e
PY=${PY:-python3}
HERE=$(cd "$(dirname "$0")" && pwd)
export WORK=${WORK:-$PWD/work}; mkdir -p "$WORK"
REPO=/tmp/bib/bibimbap; DATA=/tmp/bib/olddata/data
# ① 삭제: 맞는 답 3종(A 표준 삭제, B +개구부·연결관계, C 불완전 삭제)
OUTDIR=$WORK/del_out $PY "$HERE/delete/bibimbap_c1.py" $REPO $DATA "$WORK/delete_c1.json" "$HERE/delete/targets.json"
# ① 생성: 맞는 답과 변형
(cd "$HERE/create" && $PY build.py "$WORK/create/out" && $PY score.py "$WORK/create/out" "$WORK/create_metrics.json")
# ① 수정: 맞는 답과 다른 해석
(cd "$HERE/update" && $PY build.py && $PY score.py)
# ④ 틀린 답 (편집 45과제)
(cd "$HERE/wrong" && $PY build.py && $PY score.py "$WORK/wrong/manifest.json" "$WORK/wrong/results.json")
