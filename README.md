# Cursor Rules 프로젝트

[![cursor-rules](https://github.com//actions/workflows/cursor-rules.yml/badge.svg)](https://github.com//actions/workflows/cursor-rules.yml)

이 프로젝트는 팀 내에서 일관된 코드 품질, 보안 준수 및 개발 속도를 유지하기 위해 Cursor Rules를 정의하고 관리합니다.

## 목차

- [프로젝트 소개](#프로젝트-소개)
- [프로젝트 구조](#프로젝트-구조)
- [빠른 시작](#빠른-시작)
- [사용 방법](#사용-방법)
- [규칙 추가 방법](#규칙-추가-방법)
- [Prompt Recipes](#prompt-recipes)
- [웹 기반 Builder 도구](#웹-기반-builder-도구)
- [CI/CD 통합](#cicd-통합)
- [기여하기](#기여하기)
- [라이선스](#라이선스)

## 프로젝트 소개

Cursor는 강력한 AI 기반 코드 편집기입니다. 하지만 팀 내에서 일관된 코드 스타일, 보안 정책, 개발 관행을 유지하기 위해서는 명확한 규칙이 필요합니다. 이 프로젝트는 이러한 규칙을 정의하고, 관리하며, Cursor가 이를 활용할 수 있도록 합니다. 이를 통해 다음과 같은 이점을 얻을 수 있습니다:

- **일관된 코드 품질**: 팀원 모두가 동일한 코딩 스타일과 모범 사례를 따릅니다.
- **보안 강화**: 민감한 정보(시크릿, 토큰 등)가 코드베이스에 유입되는 것을 방지합니다.
- **개발 속도 향상**: AI가 팀의 규칙에 맞는 코드를 제안함으로써, 개발자는 더 빠르게 작업할 수 있습니다.
- **온보딩 시간 단축**: 새로운 팀원이 팀의 규칙을 빠르게 이해하고 따를 수 있습니다.

## 프로젝트 구조

```
.cursorrules/
├── common/              # 조직 전체에 적용되는 공통 규칙
│   ├── 00-core.md       # 핵심 규칙 (응답 방식, 코드 리뷰 원칙 등)
│   ├── 10-security.md   # 보안 규칙 (시크릿 관리, 의존성 관리 등)
│   ├── 20-git-style.md  # Git 관련 규칙 (커밋 메시지, 브랜치 네이밍 등)
│   └── stacks/          # 각 기술 스택별 규칙 팩
│       ├── docker-devops.md
│       ├── node-react.md
│       ├── python-fastapi.md
│       ├── ui-tailwind.md
│       ├── db-prisma.md
│       └── prompt-recipes.md  # 팀에서 자주 사용하는 Prompt Recipes
├── project/             # 현재 프로젝트에 특화된 규칙
│   └── 00-overrides.md
├── generated/           # 자동 생성된 규칙 파일
│   └── _merged.md
└──.md                 # 루트에 위치한 규칙 합본 (코드 리뷰 시 가시성을 위해 커밋됨)
```

## 빠른 시작

1. **의존성 설치**:
   이 프로젝트는 `make`와 `pre-commit`을 사용합니다. 시스템에 설치되어 있지 않다면 설치해주세요.
   ```bash
   # macOS (Homebrew)
   brew install make pre-commit

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install make
   pip install pre-commit
   ```

2. **개발 환경 설정**:
   ```bash
   make dev-setup
   ```
   이 명령어는 `pre-commit` 훅을 설치하고, Cursor Rules를 병합 및 검증합니다.

3. **규칙 확인**:
   `.cursorrules.md` 파일을 열어 현재 정의된 규칙을 확인할 수 있습니다.

## 사용 방법

1. **규칙 병합 및 검증**:
   ```bash
   make rules-merge  # 규칙을 병합하여 .cursorrules.md 파일을 생성합니다.
   make rules-check  # 병합된 규칙을 검증합니다.
   ```

2. **Cursor에서 규칙 사용**:
   Cursor 에디터에서 `.cursorrules.md` 파일을 열고, 우측 사이드바의 "Rules" 탭에 고정(Pin)합니다. 이제 Cursor는 이 규칙을 바탕으로 코드를 제안하고 리뷰합니다.

## 규칙 추가 방법

1. **공통 규칙**: 모든 프로젝트에 적용되는 규칙은 `.cursorrules/common/` 디렉토리에 추가합니다.
2. **기술 스택 규칙**: 특정 기술 스택에 적용되는 규칙은 `.cursorrules/common/stacks/` 디렉토리에 추가합니다.
3. **프로젝트 특정 규칙**: 현재 프로젝트에 특화된 규칙은 `.cursorrules/project/` 디렉토리에 추가합니다.

규칙을 추가하거나 수정한 후에는 반드시 `make rules-merge`와 `make rules-check`를 실행하여 규칙이 올바르게 적용되었는지 확인하세요.

## Prompt Recipes

`.cursorrules/common/stacks/prompt-recipes.md` 파일에는 팀에서 자주 사용하는 Prompt Recipes가 정의되어 있습니다. Cursor에서 다음과 같이 사용할 수 있습니다:

- **Docker 이미지 경량화**: "우리 표준 Dockerfile 템플릿(멀티스테이지+alpine)으로 리라이트하고, 불필요 패키지 제거·캐시 전략·--platform 적용·docker inspect 사이즈 리포트까지 한 번에 제안해줘."
- **React 청크 최적화**: "폰트/아이콘 리소스는 분리 로딩, unicons는 TTF/EOT 제외, WOFF2 우선. 전/후 번들 사이즈 표와 타임라인 하이라이트를 보여줘."
- **Prisma 마이그레이션 검토**: "컴포지트 키/관계 명명 규칙 준수 여부, 다운 마이그레이션 경로, 위험도(High/Medium/Low) 3단계로 리뷰 요약."
- **Python 3.13 FastAPI 보일러플레이트**: "mypy --strict 통과, pydantic v2, 동기/비동기 혼용 금지, 라우터/스키마/서비스 레이어 모듈 분리 스캐폴딩 생성."

## 웹 기반 Builder 도구

이 프로젝트는 웹 기반 Builder 도구를 제공하여, Markdown 형식의 규칙 파일을 `.mdc` 형식으로 쉽게 변환하고 관리할 수 있습니다. 이 도구는 정적 웹 페이지로 제공되며, GitHub Actions를 통해 자동으로 배포됩니다.

### 작동 방식

1.  **md 수정**: 팀원이 `.cursorrules` 디렉토리 내의 Markdown 파일을 수정합니다.
2.  **github repo push**: 수정된 파일을 GitHub 저장소에 푸시합니다.
3.  **static 웹 배포**: GitHub Actions 워크플로우가 자동으로 실행되어 `web/files.json` 파일을 생성하고, GitHub Pages를 통해 웹 페이지를 배포합니다.
4.  **사용자 선택**: 사용자가 웹 페이지에 접속하여 필요한 Markdown 파일을 선택합니다.
5.  **복붙**: Builder 도구가 선택된 파일의 내용을 기반으로 `.mdc` 형식의 규칙을 생성하고, 사용자는 이를 복사하여 사용할 수 있습니다.

### 웹 페이지 사용법

1.  GitHub Pages URL (예: `https://<username>.github.io/cursor-rules/`)로 접속합니다.
2.  "규칙 추가" 버튼을 클릭하여 새로운 규칙 카드를 생성합니다.
3.  파일 선택 드롭다운에서 원하는 Markdown 파일을 선택합니다.
4.  "파일 내용 불러오기" 버튼을 클릭하여 파일의 내용을 불러옵니다.
5.  필요에 따라 설명, Scope, globs 등을 수정합니다.
6.  "미리보기" 버튼을 클릭하여 생성된 `.mdc` 파일의 내용을 확인합니다.
7.  "내용 복사" 또는 ".mdc 저장" 버튼을 사용하여 결과물을 가져옵니다.

### GitHub Actions 워크플로우

`.github/workflows/generate-file-list.yml` 파일은 다음과 같은 역할을 합니다:

-   `main` 브랜치에 변경 사항이 푸시되거나, 수동으로 실행되면 작동합니다.
-   `.cursorrules` 디렉토리 및 하위 디렉토리에서 `.md` 파일을 찾아 `web/files.json` 파일을 생성합니다.
-   생성된 `web/files.json` 파일을 커밋하고 푸시합니다.
-   GitHub Pages 설정이 되어 있다면, 웹 페이지가 자동으로 업데이트됩니다.

## CI/CD 통합

GitHub Actions를 통해 모든 PR과 푸시 시 규칙이 자동으로 검증됩니다. `.github/workflows/cursor-rules.yml` 파일을 확인할 수 있습니다.

## 기여하기

이 프로젝트에 기여하고 싶으시다면, [`CONTRIBUTING.md`](CONTRIBUTING.md) 파일을 참고해주세요. 새로운 규칙을 추가하거나 기존 규칙을 개선하는 방법이 설명되어 있습니다.

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.