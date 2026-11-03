# bim-benchmark-audit

AI의 BIM(IFC) 편집 벤치마크 **BIM-Edit**와 **BIBIMBAP**을 네 가지 점검 기준으로 점검한 코드, 결과, 과제별 판정 근거입니다.

> 박지훈·고영선, 「AI의 BIM 편집 성능 평가를 위한 벤치마크 점검 기준 - BIM-Edit와 BIBIMBAP 적용 사례 -」, 한국문화공간건축학회 2026 추계학술대회논문집, 2026. 11.

Code, results and per-task evidence for auditing two public AI-based IFC editing benchmarks (BIM-Edit, BIBIMBAP) with four criteria: (1) perfect answer, (2) ground truth, (3) target ID, (4) independent check. Notes are in Korean; table and file names map to the paper below.

## 점검 기준

| 기준 | 묻는 것 |
|---|---|
| ① 만점 답안 | 맞게 편집한 답이 만점인가 |
| ② 정답 | 정답 파일·값이 지시와 맞는가 |
| ③ 대상 ID | 지시·채점의 대상 객체(GlobalId)가 입력 파일에 있는가 |
| ④ 독립 확인 | 결과 파일을 직접 본 판정과 점수가 맞는가, 틀린 답을 걸러 내는가 |

## 논문과 파일 대응

| 논문 | 파일 |
|---|---|
| <표 2> BIM-Edit 기준별 결과 | `bim-edit/scripts/checklist_audit.py`, `bim-edit/results/checklist-results.md` |
| 삭제 채점 방식(기록에서 추론) | `bim-edit/scripts/delete_scoring_mechanism.py`, `bim-edit/results/delete-scoring-mechanism.md` |
| <그림 2> 직접 판정별 의미 점수, ④ | `bim-edit/scripts/delete_audit.py` → `bim-edit/results/delete_audit.csv` |
| <표 3> 정정 전후 해결 건수 | `bim-edit/results/delete_audit.csv` + `bim-edit/results/eval_flat.csv` (아래 "정정 규칙") |
| VeriBIM 사례 | `veribim/` |
| <표 4> BIBIMBAP 결과 | `bibimbap/results/README.md`(요약), 과제별 문서, 재실행 결과 `bibimbap/results/rerun-2026-11-02/` |

## 사용한 자료와 버전

- **BIM-Edit**: Hugging Face 공개 데이터셋 `BIM-Edit/BIM-Edit`, `BIM-Edit/BIM-Edit-runs`, `BIM-Edit/BIM-Edit-Tasks` (2026년 10월 초 내려받음). 원 논문: arXiv:2606.20146v3. 채점 프로그램은 공개되지 않아, 채점 방식은 공개 채점 기록(`eval_cache.json`)에서 추론했습니다.
- **BIBIMBAP**: github.com/nbharathik/bibimbap. 채점 코드는 커밋 `667004e`(2026-04-07), IFC·질문 파일은 커밋 `a0291d6`(2026-03-13). 문제가 나온 과제의 IFC는 Hugging Face 최신본과 내용이 같음을 확인했습니다(줄바꿈만 다름).
- **IfcOpenShell**: BIBIMBAP 채점은 저장소가 지정한 `0.8.3.post2`. 0.9.0에서는 충돌 검사 단계 오류로 대부분의 편집 과제가 0점이 되므로 쓰지 않습니다.
- 원 벤치마크의 IFC와 채점 기록은 이 저장소에 다시 올리지 않았습니다. 위 출처에서 받아 아래 폴더 구조로 두면 됩니다.

## 판정 기준

### BIM-Edit 삭제 과제 (`delete_audit.py`)
결과 IFC를 입력·정답 IFC와 직접 비교합니다(채점기의 매칭 결과는 쓰지 않음).
- `target_removed`: 지시된 대상 GlobalId가 결과 파일의 어떤 엔티티에도 없음
- `gt_valid`: 정답 IFC에서도 대상이 실제로 사라졌음 (아니면 기준 ② 오류)
- `products_equal_gt`: 건물요소 23종(벽·슬래브·공간·문·창·기둥·보·개구부 등, 스크립트의 `PROD`)의 GlobalId 집합이 정답과 같음
- `moved_remaining`: 남은 건물요소 중 경계상자가 입력 대비 1 mm 넘게 바뀐 수
- **맞는 삭제**(`verified_correct`) = `gt_valid` 그리고 `target_removed` 그리고 `products_equal_gt` 그리고 `moved_remaining == 0`

이 판정은 속성·관계까지 포함한 IFC 전체의 무결성을 보증하지 않습니다.

### 정정 규칙 (<표 3>)
- 해결 = 형상·의미·위상 점수가 모두 0.98 이상 (원 논문 정의)
- 정정: 4개 모델 인공 장면 삭제 결과 중 `verified_correct`인 것의 의미 점수만 원 정의("대상이 사라졌으면 1")대로 1로 바꿈. 형상·위상 점수는 공개값 그대로.
- ②·③에 걸린 과제는 정정 전후 모두 집계에서 뺌(`checklist_audit.py`의 `bad`).
- 기존 보조 감사에서 통과였던 110건 중 경계상자 계산이 실패한 1건(`claude-sonnet / SLB-DEL-DIR-A-003`)은 판정 불가로 정정에서 뺌.
- 결과: 648건 중 해결 5건(0.77%) → 65건(10.03%).

### 채점 기록만으로 본 "지워짐" (7개 모델, 기준 ①·③)
정답 객체가 있고(`n_gt ≥ 1`) 채점기가 비교 대상을 찾지 못했으면(`best_match_guid = null`) 지운 것으로 봅니다. 결과 파일이 있는 4개 모델에서 위 직접 판정과 200건 중 200건 일치했습니다. 결과 파일이 없는 모델에는 보존 확인을 할 수 없으므로 이 값은 상한입니다.

### BIBIMBAP (`bibimbap/`)
- ① 삭제 (`scripts/delete/`): 세 가지 답을 만들어 원 채점 스크립트로 채점합니다. A = IfcOpenShell 표준 함수 `root.remove_product`로 대상만 삭제, B = A + 채운 개구부와 벽 연결 관계까지 삭제, C = 엔티티만 지우고 속성·관계를 남긴 불완전 삭제.
- ① 생성 (`scripts/create/`): `ifcopenshell.api`로 클래스, 층 소속, 압출 형상, 문의 개구부(IfcRelVoidsElement·IfcRelFillsElement)까지 만든 맞는 답과, 똑같이 맞는 다른 모델링 방식(변형)을 채점합니다.
- ① 수정 (`scripts/update/`): 지시대로 고친 답과, 지시가 여러 뜻으로 읽힐 때의 다른 해석을 채점합니다.
- ④ 틀린 답 (`scripts/wrong/`): 편집 45과제마다 지시를 분명히 어긴 답(총 401개)과 기준 답을 채점합니다. 판정 근거는 `results/wrong-flagged-evidence.md`(0.9점 이상 받은 틀린 답), 전체 표는 `results/wrong-full-table.md`.
- ② 조회 정답 (`scripts/retrieve/`): `results/retrieve-check.md`, `results/retrieve-values.json` (IFC에서 다시 계산한 값)
- ③ 대상 ID: `scripts/c3_ids.py` → `results/c3_ids.json`
- 과제별 설명: `results/create-c1.md`, `results/update-c1.md`, `results/bibimbap-c1.md`, `results/wrong-answers.md`

## 재현 순서

```
# BIM-Edit: 작업 폴더 구조
data/tasks/tasks.jsonl
data/runs/<model>/eval/eval_cache.json
data/runs/<model>/edited/<task_id>/*.ifc
data/gt/simple/*.ifc
analysis/                      # 결과가 저장되는 곳

python bim-edit/scripts/analyze_eval_cache.py     # → analysis/eval_flat.csv
python bim-edit/scripts/delete_audit.py           # → analysis/delete_audit.csv
python bim-edit/scripts/checklist_audit.py out.json
python bim-edit/scripts/delete_scoring_mechanism.py

# BIBIMBAP: ①·④ 전체 (결과는 $WORK, 기본 ./work)
git clone https://github.com/nbharathik/bibimbap /tmp/bib/bibimbap        # 채점 코드: 커밋 667004e
git -C /tmp/bib/bibimbap worktree add /tmp/bib/olddata a0291d6           # IFC·질문 데이터
pip install ifcopenshell==0.8.3.post2 numpy shapely
bash bibimbap/scripts/run_all.sh
```

BIM-Edit 스크립트는 `pandas`, `numpy`가 필요합니다. `ifc_lite.py`는 경계상자 계산용 간이 IFC 리더입니다.

## 다시 판정해 보려면 (재판정 안내)

이 점검의 판정은 연구자 1인이 했습니다. 다른 사람이 같은 자료로 판정을 확인할 수 있도록 아래 순서를 권합니다.

**1. BIM-Edit: 사람 판단이 들어가지 않는 부분**
삭제 결과의 "지웠는가·다른 객체를 건드렸는가"는 `delete_audit.py`가 GlobalId와 경계상자로 기계적으로 판정합니다(위 "판정 기준"). 같은 공개 데이터로 다시 돌려 `bim-edit/results/delete_audit.csv`와 같은지 보면 됩니다. 몇 건을 골라 IFC 뷰어에서 대상 객체가 정말 사라졌는지 눈으로 확인할 수도 있습니다.

**2. BIBIMBAP: 사람 판단이 들어간 부분**
"이 답이 지시대로 맞게 고친 것인가 / 분명히 틀린 것인가"는 사람이 정한 것입니다. 확인 순서는 다음과 같습니다.
1. `bash bibimbap/scripts/run_all.sh`로 답안 IFC를 모두 만듭니다(`$WORK/create/out`, `$WORK/upd/out`, `$WORK/del_out`, `$WORK/wrong/out`).
2. `bibimbap/rejudge_template.csv`를 엽니다. 답안 하나가 한 줄이고(463줄: 기준 답과 틀린 답 401개), 과제·변형 이름, 연구자가 적은 이유(`why`), 채점 점수, 답안 파일 위치가 들어 있습니다.
3. 원 과제 지시문(`/tmp/bib/olddata/data/prompts/all_questions.csv`의 `question`)을 읽고, 답안 파일을 IFC 뷰어(예: Bonsai, BIMvision)로 열어 `판정` 칸에 **맞음 / 틀림 / 애매** 중 하나를, `이유` 칸에 근거를 적습니다. 연구자의 `why`를 먼저 보지 않고 판정한 뒤 비교하면 독립 판정이 됩니다.
4. 연구자 판정은 `구분` 칸(기준 답 = 맞는 답, 틀린 답)과 같습니다. 일치하지 않는 줄이 재판정 결과입니다.

과제별로 왜 그 답을 맞다고 보았는지는 `bibimbap/results/create-c1.md`, `update-c1.md`, `bibimbap-c1.md`에, 0.9점 이상 받은 틀린 답의 근거는 `wrong-flagged-evidence.md`에 있습니다. 표에서 `(borderline)`이 붙은 변형은 허용 오차나 해석에 따라 맞다고 볼 여지가 있는 답이라 따로 표시했습니다.

## 알림

- 2026-11-02에 `run_all.sh`로 BIBIMBAP 점검을 처음부터 다시 돌려 저장된 결과와 비교했습니다(`bibimbap/results/rerun-2026-11-02/RERUN.md`). 한 과제(geometry_test_12, 45° 회전)를 빼고 모두 같았습니다. 이 과제의 예전 감점은 재현되지 않아, 맞는 답이 감점되거나 정답이 틀린 과제는 **23개**로 고쳤습니다.
- 생성·수정 답안 스크립트의 보조 모듈(`create/lib.py`, `update/edits.py`, `update/common.py`, `update/run.py`)은 처음 작업 환경에서 보존되지 않아 다시 작성했고, 위 재실행으로 같은 점수가 나오는 것을 확인했습니다.
- 결과 폴더의 `.md` 파일은 점검하면서 남긴 기록입니다.
- 삭제 채점 불일치는 VeriBIM(github.com/NTUZZH/VeriBIM)이, BIM-Edit 인공 장면 문·창 삭제 4과제의 대상 ID 오류는 Hugging Face `BIM-Edit-Tasks` 토론(2026년 8월)이 먼저 지적했습니다.
