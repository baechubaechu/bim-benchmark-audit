# BIBIMBAP 개념(conceptual) 조회 20과제: 정답 키 점검 (기준 ② ③)
정답이 주관적("밝아 보이는 방", "내향적인 방")이라 정답 자체의 옳고 그름은 판단하지 않음. 점검한 것: 정답 키 GUID가 파일에 있는가, 키의 객체 종류가 질문과 맞는가, 답안 형식이 질문과 맞는가.
데이터: 공개 저장소 커밋 a0291d6(3/13) IFC, 채점 코드 커밋 667004e(4/7).

| 과제 | 결과 |
|---|---|
| conceptual_12 "더 밝아 보이는 방의 ID" | **정답 키 2YBG8$weL8dfjf3ERiESW$ 가 파일에 없음.** 파일의 방은 2개(3LaxXmfID1XOBT9i9ZV$uk, 3SgOC3kuHAO8aUyVlDj0yC). 어떤 답도 맞을 수 없음 |
| conceptual_16 "보조실들(rooms)의 ID들" | 질문은 복수형인데 답안 형식은 ID 1개(global_id), 정답 키도 방 1개. 문장과 형식 불일치(경미) |
| conceptual_11 "1층과 2층을 시각·공간적으로 잇는 요소" | 정답 키는 벽의 개구부(IfcOpeningElement, 채움 없음). 판단은 주관적이라 보류 |
| 나머지 17개 | 키 GUID 존재, 객체 종류가 질문과 일치(방→IfcSpace, 벽→IfcWall, 문→IfcDoor). 수치형 2개(04, 18)는 판단 보류 |
