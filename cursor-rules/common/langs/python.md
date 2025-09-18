---
lang: kr
title: Python 규칙
description: Python 언어 전반에서 일관성과 품질을 유지하기 위한 기본 규칙 모음
tags: [python, style, lint, typing, test, security]
---

# Python 규칙

Python 프로젝트에서 공통적으로 지켜야 할 규칙을 정의한다.  
프레임워크(FastAPI, Django 등) 특화 규칙은 `stacks/`에 별도로 둔다.

---

## 1) 버전 & 런타임

- 기본 런타임은 **Python 3.11 이상**을 사용한다.
- 프로젝트 루트에 `.python-version` 또는 `pyproject.toml`의 `requires-python`로 명시한다.
- 표준 라이브러리를 우선 사용하고, 외부 의존성은 최소화한다.

```toml
# pyproject.toml (발췌)
[project]
requires-python = ">=3.11"
```

---

## 2) 프로젝트 레이아웃

- **src 레이아웃**을 권장한다.
- 테스트는 `tests/` 디렉토리에 모은다.

```
project/
├─ pyproject.toml
├─ src/
│  └─ pkgname/
│     ├─ __init__.py
│     └─ ...
└─ tests/
   └─ test_*.py
```

---

## 3) 코드 스타일

- **PEP 8** 준수.
- 자동 포맷터 **black** 사용.
- **isort**로 import 정렬.
- **ruff**로 린트(가능하면 flake8 대체).
- 문자열은 기본 **f-string** 사용.

```python
# good
name = "Alice"
print(f"Hello {name}")

# bad
print("Hello %s" % name)
```

---

## 4) 타입 힌트

- 모든 공개 함수/메서드에 타입 힌트를 작성한다.
- `mypy` 또는 `pyright`로 정적 타입 검사.
- `Any` 사용은 최소화한다.

```python
from typing import Iterable

def total(xs: Iterable[int]) -> int:
    return sum(xs)
```

---

## 5) 패키징 & 의존성

- 의존성 관리는 **poetry** 또는 **uv**를 권장한다.
- 버전은 **고정(pinned)** 한다. (semver 범위는 팀 정책에 맞춘다)
- `requirements.txt`는 배포/런타임 산출물로만 사용한다.

```toml
# pyproject.toml (발췌)
[tool.poetry.dependencies]
python = ">=3.11,<3.13"
pydantic = "^2.7"

[tool.poetry.group.dev.dependencies]
black = "^24.0"
ruff = "^0.5"
mypy = "^1.10"
pytest = "^8.2"
pytest-cov = "^5.0"
isort = "^5.13"
```

---

## 6) 테스트

- 테스트 러너는 **pytest**.
- 새 기능/버그 수정에는 테스트를 동반한다.
- 커버리지는 **80% 이상** 유지.

```ini
# pytest.ini
[pytest]
addopts = -q --maxfail=1 --disable-warnings
testpaths = tests
```

---

## 7) 문서화

- 공개 함수/클래스에 **docstring** 작성(구글/NumPy 스타일 중 택1).
- 예시는 실행 가능한 최소 코드로 유지한다.

```python
def add(a: int, b: int) -> int:
    """두 정수를 더한다.

    Args:
        a: 첫 번째 정수
        b: 두 번째 정수
    Returns:
        합계
    """
    return a + b
```

---

## 8) 예외 처리 & 로깅

- 예외는 **가까운 곳에서 처리**하고 의미 있는 메시지로 감싼다.
- `print` 대신 **logging**을 사용한다.

```python
import logging

logger = logging.getLogger(__name__)

def load_user(user_id: str):
    try:
        ...
    except TimeoutError as e:
        logger.warning("load_user timeout: %s", user_id)
        raise RuntimeError("User service timeout") from e
```

---

## 9) 보안 & 품질

- 정적 분석: **ruff**, 타입: **mypy/pyright**.
- 보안: **bandit**, 의존성 취약점: **pip-audit** 또는 **poetry export + pip-audit**.
- 외부 입력은 반드시 검증(validation)한다.

```bash
bandit -q -r src
pip-audit
```

---

## 10) 환경변수 & 설정

- `.env`는 개발용으로만 사용하고, 비밀은 비공개 시크릿 매니저를 사용한다.
- 설정은 **pydantic-settings** 등으로 구조화한다.

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    env: str = "dev"
    db_url: str

    class Config:
        env_file = ".env"
        env_prefix = "APP_"

settings = Settings()
```

---

## 11) 직렬화 & 데이터 모델

- 데이터 모델은 **pydantic v2** 또는 표준 `dataclasses`를 사용한다.
- JSON 직렬화는 표준 라이브러리 `json`을 우선 사용.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
```

---

## 12) 동시성 & 성능

- 비동기는 **asyncio** 기본. 블로킹 I/O는 스레드풀로 넘긴다.
- 캐싱은 필요 최소한으로, 만료(예: TTL) 정책을 명확히 한다.
- 성능 이슈는 우선 **프로파일링**으로 확인한다.

```python
from functools import lru_cache

@lru_cache(maxsize=256)
def heavy(x: int) -> int:
    ...
```

---

## 13) 스크립트 실행 규약

- 엔트리포인트는 `if __name__ == "__main__":` 패턴을 따른다.
- 재사용 가능한 로직은 모듈 함수로 분리한다.

```python
def main() -> int:
    ...

if __name__ == "__main__":
    raise SystemExit(main())
```

---

## 14) 사전 훅(pre-commit)

- 포맷/린트/타입검사를 **pre-commit**으로 자동화한다.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.8.0
    hooks: [{id: black}]
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.5.7
    hooks: [{id: ruff, args: ["--fix"]}]
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks: [{id: isort}]
```

---

## 15) CI (권장 예시)

- PR마다 포맷/린트/타입/테스트를 실행한다.

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  py:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -U pip
      - run: pip install poetry && poetry install --no-interaction
      - run: poetry run black --check .
      - run: poetry run ruff check .
      - run: poetry run mypy src
      - run: poetry run pytest --maxfail=1 --disable-warnings -q
```

---

## 16) 예시 규칙의 우선순위

1. 보안/안전 (취약점, 비밀 유출 방지)
2. 정확성 (타입, 테스트)
3. 유지보수성 (스타일, 구조)
4. 성능 (프로파일링 후 최적화)

---

