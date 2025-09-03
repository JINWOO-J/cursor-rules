# Cursor Rules 프로젝트

[![Build & Deploy](https://github.com/JINWOO-J/cursor-rules/actions/workflows/build-web.yml/badge.svg)](https://github.com/JINWOO-J/cursor-rules/actions/workflows/build-web.yml)
[![Web Builder](https://img.shields.io/badge/Web_Builder-Live-brightgreen?logo=github-pages)](https://jinwoo-j.github.io/cursor-rules/)

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

## 📁 프로젝트 구조

```
cursor-rules/            # 📝 규칙 작성 (소스)
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
│       └── prompt-recipes.md
├── project/             # 현재 프로젝트에 특화된 규칙
│   └── 00-overrides.md
├── generated/           # 자동 생성된 규칙 파일
│   └── _merged.md
├── presets.json         # 🎯 프리셋 정의 (개발환경별 규칙 조합)
└── glossary.kr-en.json  # 🌍 번역 용어집

web/                     # 🌐 동적 빌드 결과 (커밋하지 않음!)
├── index.html          # Builder UI (GitHub Pages)
├── files.json          # 동적 생성된 파일 인덱스
├── version-info.json   # 빌드 메타데이터
└── cursor-rules/       # 번역된 규칙들 (KR/EN 쌍)
```

### 🔄 동적 빌드 구조의 장점
- **📝 Source of Truth**: `cursor-rules/`만 수정하면 모든 것이 자동 처리
- **🚫 No Git Conflicts**: `web/` 폴더는 빌드 결과물이므로 커밋하지 않음
- **🌍 자동 번역**: KR → EN 번역이 빌드 시 자동 수행
- **⚡ 즉시 반영**: 수정 즉시 웹사이트에 반영

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

## 🌐 웹 기반 Builder 도구

**🔗 바로 사용: [https://jinwoo-j.github.io/cursor-rules/](https://jinwoo-j.github.io/cursor-rules/)**

이 프로젝트는 웹 기반 Builder 도구를 제공하여, Markdown 형식의 규칙 파일을 `.mdc` 형식으로 쉽게 변환하고 관리할 수 있습니다. 이 도구는 **완전 동적으로 빌드**되어 rebase 지옥을 피하면서도 최신 내용을 제공합니다.

### 🔄 동적 빌드 방식

1.  **📝 규칙 작성**: `cursor-rules/` 디렉토리 내의 Markdown 파일을 수정합니다.
2.  **🚀 Push**: 수정된 파일을 GitHub 저장소에 푸시합니다.
3.  **⚡ 실시간 빌드**: GitHub Actions가 자동으로:
    - KR → EN 번역 (Google Gemini AI)
    - `files.json`, `version-info.json` 생성
    - GitHub Pages에 직접 배포 (커밋 없음!)
4.  **🎯 즉시 사용**: 웹 페이지에서 최신 파일들을 바로 불러와 `.mdc` 생성

### ✨ 주요 특징

- **🚫 No Git Conflicts**: `web/` 폴더에 커밋하지 않아 rebase 지옥 방지
- **🌏 다국어 지원**: 한국어 ↔ 영어 동시 편집 및 번역
- **📦 개발환경별 프리셋**: Python, React, 풀스택, DevOps 등 6가지 프리셋 제공  
- **🔍 검색 가능**: 대량의 규칙 파일에서 빠른 검색
- **📱 반응형**: 모바일에서도 편리하게 사용 가능

### 🎯 웹 페이지 사용법

#### 방법 1: 프리셋 사용 (추천)
1.  **🎯 개발환경별 프리셋** 드롭다운에서 원하는 환경 선택
   - 🔒 **필수 기본 규칙**: 보안, Git 스타일, AI 프롬프팅
   - 🔧 **Python 백엔드 개발팩**: FastAPI + Prisma + 보안
   - 🎨 **React 프론트엔드 개발팩**: React + Tailwind + UI
   - 🌐 **풀스택 웹앱 개발팩**: 전체 스택 통합 규칙
   - ⚙️ **DevOps & 인프라팩**: Docker + 컨테이너 + 배포
2.  선택 즉시 자동으로 해당 환경의 모든 규칙이 로드됩니다.
3.  각 규칙 카드에서 **"내용 복사"** 또는 **".mdc 저장"** 사용

#### 방법 2: 개별 규칙 추가
1.  **"+ 규칙 추가"** 버튼 클릭
2.  **파일명 (.mdc)** 드롭다운에서 원하는 Markdown 파일 선택
3.  **"파일 내용 불러오기"** 버튼으로 KR/EN 내용 자동 로드
4.  필요시 설명, Scope, globs 수정
5.  **"미리보기"** → **"내용 복사"** 또는 **".mdc 저장"**

### ⚙️ GitHub Actions 워크플로우 (동적 빌드)

`.github/workflows/build-web.yml`은 **rebase 지옥을 피하는 동적 빌드** 방식을 사용합니다:

#### 🔄 동작 과정
1.  **트리거**: `cursor-rules/**` 파일 변경 시 자동 실행
2.  **번역**: Google Gemini AI로 KR → EN 자동 번역
3.  **인덱스 생성**: `files.json`, `version-info.json` 동적 생성
4.  **직접 배포**: GitHub Pages에 바로 배포 (**커밋 없음!**)

#### 🎯 장점
- **🚫 Git 충돌 방지**: `web/` 폴더에 커밋하지 않음
- **⚡ 빠른 배포**: 빌드와 동시에 즉시 반영
- **🔄 항상 최신**: 소스 변경 시 자동으로 웹사이트 업데이트
- **🌍 다국어 자동화**: 번역과 배포를 한 번에 처리

```yaml
# 기존 방식 (문제): 커밋 후 rebase 지옥
# - name: Commit & push web/ changes (❌ 주석 처리됨)

# 새로운 방식 (해결): 동적 빌드 후 직접 배포  
- name: Upload Pages artifact
  uses: actions/upload-pages-artifact@v3
  with:
    path: web
```

## CI/CD 통합

GitHub Actions를 통해 모든 PR과 푸시 시 규칙이 자동으로 검증됩니다. `.github/workflows/cursor-rules.yml` 파일을 확인할 수 있습니다.

## 기여하기

이 프로젝트에 기여하고 싶으시다면, [`CONTRIBUTING.md`](CONTRIBUTING.md) 파일을 참고해주세요. 새로운 규칙을 추가하거나 기존 규칙을 개선하는 방법이 설명되어 있습니다.

## 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.