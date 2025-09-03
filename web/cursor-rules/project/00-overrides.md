# Project Specific Overrides

## Project Overrides
- 이 프로젝트는 Cursor Rules 자체를 정의하고 관리하는 프로젝트입니다.
- 따라서 프로젝트 특정 규칙은 .cursorrules/project 디렉터리에 정의됩니다.

## Specific to this project
- **문서화**: 모든 규칙 변경은 `PRD.md`와 `README.md`에 반영되어야 합니다.
- **버전 관리**: `.cursorrules.md` 파일은 Git으로 버전 관리됩니다.
- **규칙 생성 스크립트**: `Makefile`의 `rules-merge` 타겟을 사용하여 규칙을 생성합니다.