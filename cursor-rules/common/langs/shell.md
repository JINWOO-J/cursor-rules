---
lang: kr
title: Shell 스크립트 규칙
description: 안전하고 이식성 높은 Shell 스크립트를 작성하기 위한 팀 규칙 모음
tags: [shell, bash, sh, scripting, cli, devops, security]
---

# Shell 스크립트 규칙

Shell 스크립트를 작성할 때의 공통 원칙을 정의한다.  
**팀 표준은 Bash**를 권장하며, POSIX sh 호환이 필요한 경우는 별도 명시한다.  
zsh/fish 등 특화 기능은 개인 환경 설정에서만 허용한다.

---

## 1) 셸 지정

- 반드시 shebang을 명시한다.
- 기본 표준은 Bash:

```bash
#!/usr/bin/env bash
```

- POSIX 호환이 필요한 경우:

```sh
#!/bin/sh
```

---

## 2) 안전 옵션 설정

- Bash 스크립트는 반드시 `set -euo pipefail` 사용.
- POSIX sh는 `set -eu`를 기본으로 한다.
- 디버깅 시 `set -x`를 활용한다.

```bash
set -euo pipefail
```

---

## 3) 함수화 및 구조화

- 스크립트는 함수 단위로 나누어 작성한다.
- `main` 함수를 두고 마지막에 `main "$@"` 실행.

```bash
main() {
  echo "Hello, $1"
}

main "$@"
```

---

## 4) 변수 관리

- 변수를 사용할 때는 항상 따옴표로 감싼다.
- Bash에서는 `local` 키워드로 함수 스코프 제한.
- 상수는 대문자 스네이크케이스로 선언.

```bash
local name="$1"
echo "User: ${name}"
```

---

## 5) 입력 & 인자 처리

- 단순한 경우 `$1`, `$2`를 변수에 바인딩하여 사용.
- 복잡한 옵션은 `getopts`를 사용.
- 사용법을 명확히 출력하는 `usage` 함수를 작성한다.

```bash
usage() {
  echo "Usage: $0 -f FILE -o OUT"
  exit 1
}

while getopts "f:o:" opt; do
  case $opt in
    f) FILE="$OPTARG";;
    o) OUT="$OPTARG";;
    *) usage;;
  esac
done
```

---

## 6) 명령 실행 & 에러 처리

- 중요한 명령은 `|| exit 1` 또는 `trap`으로 처리.
- `trap`으로 종료 시점 클린업을 정의한다.

```bash
trap 'echo "Error occurred"; exit 1' ERR
```

---

## 7) 파일 & 디렉토리 관리

- 파일 경로는 항상 따옴표로 감싼다.
- 임시 파일은 `mktemp`를 사용한다.
- 실행 중 디렉토리는 `SCRIPT_DIR` 기준으로 설정한다.

```bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

---

## 8) 외부 명령 호출

- 필수 유틸리티는 스크립트 시작 시 확인한다.

```bash
command -v jq >/dev/null 2>&1 || {
  echo "jq is required" >&2
  exit 1
}
```

---

## 9) 스타일 & 포맷

- 들여쓰기는 공백 2칸 또는 4칸으로 일관성 유지.
- 조건문/루프는 명확히 구분.

```bash
if [ -f "$FILE" ]; then
  echo "found"
else
  echo "missing"
fi
```

---

## 10) 보안

- 사용자 입력은 반드시 검증/escape 처리.
- `eval` 사용 금지.
- 비밀번호, 토큰 등은 환경 변수나 시크릿 관리 시스템을 사용.

---

## 11) 테스트 & 린트

- 모든 스크립트는 **shellcheck**로 정적 분석.
- 복잡한 스크립트는 **bats** 테스트 프레임워크로 단위 테스트.

```bash
shellcheck scripts/*.sh
```

---

## 12) CI/CD 예시

```yaml
# .github/workflows/shell-ci.yml
name: Shell CI
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

1. 안전성 (에러 처리, 입력 검증)
2. 이식성 (POSIX 표준 우선, 팀 표준은 Bash)
3. 유지보수성 (함수화, 스타일 일관성)
4. 가시성 (로깅, usage 메시지)

---

