---
name: verify
description: 코드 변경이 끝난 뒤 결과를 검증할 때 사용한다. pytest 실행, 마지막 커밋 이후 diff 확인, 테스트 약화 여부와 신규 동작의 테스트 존재 여부를 점검해 PASS/FAIL로 보고한다.
---

# 변경 결과 검증

1. `.venv`의 파이썬으로 pytest를 실행한다: `.venv/Scripts/python -m pytest -q`
2. `git diff HEAD --stat`과 `git diff HEAD`로 마지막 커밋 이후 바뀐 파일을 모두 확인한다. 추적되지 않는 새 파일은 `git status --short`로 함께 본다.
3. `tests/` 변경이 있으면 테스트가 약화됐는지 점검한다:
   - 테스트 삭제
   - assert 제거 또는 완화
   - skip/xfail 처리
   - 기대값을 구현에 맞춰 바꾼 경우
4. 새로 추가된 동작에 대응하는 테스트가 있는지 확인한다.
5. 결과를 **PASS** 또는 **FAIL**로 보고한다. 근거로 pytest 결과 요약(통과/실패 수)과, 문제가 된 diff 줄(파일:줄 번호와 해당 내용)을 붙인다.

pytest 실패, 테스트 약화, 신규 동작의 테스트 누락 중 하나라도 있으면 FAIL이다.
