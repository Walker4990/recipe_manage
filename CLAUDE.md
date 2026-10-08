# 레시피 관리 API (실습용)

## 기술 스택

- Python 3.11+, FastAPI, pytest
- 가상환경은 .venv를 쓰고, 의존성은 requirements.txt에 기록한다.

## 구조

- 앱 진입점은 app/main.py
- 라우터는 app/routers/에 리소스당 파일 하나 (예: app/routers/recipes.py)
- 데이터 모델(Pydantic)은 app/schemas.py
- 테스트는 tests/test\_<모듈명>.py로 작성한다.

## 작업 규칙

- 코드를 수정한 뒤에는 pytest를 실행하고 통과/실패 결과를 보고한다. 실패하면 고친 뒤 다시 실행한다.
- 저장소는 DB 대신 메모리(dict)를 쓴다.
- 새 패키지를 추가하면 requirements.txt에도 반영한다.
