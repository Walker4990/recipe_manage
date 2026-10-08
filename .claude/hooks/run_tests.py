"""Stop 훅: 턴이 끝나기 전에 pytest를 실행하고, 실패하면 종료를 막는다."""

import json
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
VENV_PYTHON = PROJECT_DIR / ".venv" / "Scripts" / "python.exe"
MAX_OUTPUT_CHARS = 4000

# pytest 종료 코드 5 = 수집된 테스트 없음. 실패로 보지 않는다.
PASS_CODES = {0, 5}


def main() -> int:
    sys.stderr.reconfigure(encoding="utf-8")

    try:
        hook_input = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except json.JSONDecodeError:
        hook_input = {}

    if hook_input.get("stop_hook_active"):
        return 0

    if not VENV_PYTHON.exists():
        print(f"가상환경 파이썬을 찾을 수 없습니다: {VENV_PYTHON}", file=sys.stderr)
        return 2

    result = subprocess.run(
        [str(VENV_PYTHON), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=PROJECT_DIR,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode in PASS_CODES:
        return 0

    output = (result.stdout + result.stderr).strip()
    if len(output) > MAX_OUTPUT_CHARS:
        output = "...(앞부분 생략)...\n" + output[-MAX_OUTPUT_CHARS:]
    print(
        f"pytest가 실패했습니다 (exit {result.returncode}). 테스트를 고친 뒤 다시 실행하세요.\n\n{output}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
