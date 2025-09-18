---
lang: kr
title: Bash 규칙
description: 안전하고 유지보수 가능한 Bash 스크립트를 작성하기 위한 규칙 모음
tags: [bash, shell, scripting, cli, devops, security]
---

# Bash 규칙

Bash 스크립트를 작성할 때의 기본 원칙과 팀 규약을 정의한다.  
단순 실행 명령어 모음이 아니라, **재현 가능하고 안전한 스크립트**를 작성하는 것을 목표로 한다.

---

## 1) 셸 지정

- 항상 shebang을 명시한다.
- `/bin/bash` 고정 사용 (POSIX sh 호환 스크립트는 별도 문서화).

```bash
#!/usr/bin/env bash
```

---

## 2) 안전 옵션 설정

- `set -euo pipefail`을 기본으로 한다.
  - `-e` : 에러 발생 시 즉시 종료
  - `-u` : 선언되지 않은 변수 사용 시 에러
  - `-o pipefail` : 파이프라인 중간 단계 에러 감지
- 필요 시 `set -x`로 디버깅 출력.

```bash
set -euo pipefail
```

---

## 3) 함수화 및 구조화

- 긴 스크립트는 **함수 단위**로 쪼갠다.
- `main` 함수를 두고, 마지막에 `main "$@"` 실행.

```bash
main() {
  echo "Hello, $1"
}

main "$@"
```

---

## 4) 변수 관리

- 변수는 로컬 스코프(`local`)로 한정한다.
- 상수는 대문자 스네이크케이스(`MY_CONST`)로 작성.
- 문자열은 항상 따옴표로 감싼다.

```bash
local name="$1"
echo "User: ${name}"
```

---

## 5) 입력 & 인자 처리

- 스크립트 인자는 `$1`, `$2` 직접 쓰지 말고 변수로 바인딩.
- 복잡한 경우 `getopts` 또는 `argparse` 라이브러리를 사용.
- 입력 검증 필수.

```bash
while getopts "f:o:" opt; do
  case $opt in
    f) FILE="$OPTARG";;
    o) OUT="$OPTARG";;
    *) exit 1;;
  esac
done
```

---

## 6) 명령 실행 & 에러 처리

- `command || exit 1` 형태로 에러 처리를 명시.
- `trap`으로 종료/에러 시 클린업 처리.

```bash
trap 'echo "Error occurred"; exit 1' ERR
```

---

## 7) 파일 & 디렉토리

- 파일 경로는 항상 따옴표로 감싼다.
- 임시 파일은 `mktemp` 사용.
- 절대경로 기반으로 동작하도록 `SCRIPT_DIR`를 잡는다.

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

---

## 8) 외부 명령 호출

- 필수 도구는 스크립트 상단에서 체크한다.

```bash
command -v jq >/dev/null 2>&1 || {
  echo "jq is required" >&2
  exit 1
}
```

---

## 9) 포맷 & 스타일

- 들여쓰기 2스페이스 또는 4스페이스 일관 유지.
- 함수/조건문/루프에는 `{}` 또는 `do/done`를 명확히 쓴다.

```bash
if [[ -f "$FILE" ]]; then
  echo "found"
else
  echo "missing"
fi
```

---

## 10) 보안

- 사용자 입력은 반드시 검증하거나 escape 처리.
- `eval` 사용 금지.
- root 권한 필요 시 명확히 경고.

---

## 11) 테스트 & 린트

- `shellcheck`로 정적 분석.
- `bats`로 단위 테스트 가능.

```bash
shellcheck script.sh
```

---

## 12) CI/CD 예시

```yaml
# .github/workflows/bash-ci.yml
name: Bash CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run shellcheck
        run: shellcheck scripts/*.sh
```

---

## 13) 우선순위

1. 안전성 (`set -euo pipefail`, 입력 검증)
2. 유지보수성 (함수화, 스타일 일관성)
3. 이식성 (`#!/usr/bin/env bash`, 표준 유틸 사용)
4. 성능 (필요 시 awk/sed 등 조합)

