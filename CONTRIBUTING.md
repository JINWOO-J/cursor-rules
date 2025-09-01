# Contributing to Cursor Rules

이 프로젝트에 기여해 주셔서 감사합니다! 이 문서는 프로젝트에 새로운 규칙을 추가하거나 기존 규칙을 수정하는 방법을 설명합니다.

## 규칙 추가 방법

1.  **공통 규칙**: 모든 프로젝트에 적용되는 규칙은 `.cursorrules/common/` 디렉토리에 추가합니다.
    *   핵심 원칙은 `00-core.md`에, 보안 관련 규칙은 `10-security.md`에 추가합니다.
2.  **기술 스택 규칙**: 특정 기술 스택에 적용되는 규칙은 `.cursorrules/common/stacks/` 디렉토리에 추가합니다.
    *   파일 이름은 `기술이름.md` 형식을 따릅니다. (예: `node-react.md`, `python-fastapi.md`)
3.  **프로젝트 특정 규칙**: 현재 프로젝트에 특화된 규칙은 `.cursorrules/project/` 디렉토리에 추가합니다.

## Pull Request 제출

1.  변경 사항을 포함하는 새로운 브랜치를 생성합니다.
2.  변경 사항에 대한 명확하고 간결한 설명을 포함하는 Pull Request를 생성합니다.
3.  Pull Request는 코드 리뷰를 거쳐 병합됩니다.

## 코드 검증

`make rules-merge` 및 `make rules-check` 명령어를 사용하여 규칙이 올바르게 병합되고 검증되는지 확인합니다.