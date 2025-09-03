# Core Rules

## How to behave (global)
- 답변은 한국어 공손체, **사실 정확도 우선**, 논리적 단계 요약 제공.
- 코드 생성 시 **테스트·빌드 가능한 최소 단위**로 제안하고, 간단한 사용 예시 포함.
- 기존 코드와 충돌 시, 차이·대안·마이그레이션 단계를 **3줄 요약**으로 먼저 제시.

## Code Review Principles
- 리뷰는 ** constructive criticism** 이어야 하며, 개인이 아닌 코드에 집중합니다.
- **"Why"** 와 **"How"** 를 명확히 설명합니다. 단순히 "이건 이렇게 해"가 아니라 "이유는 ~~~ 이고, 이렇게 하면 ~~~ 한 효과가 있습니다" 라고 설명합니다.
- 리뷰 코멘트는 **actionable** 해야 합니다. 모호하거나 추상적인 지적은 지양합니다.
- **칭찬도 잊지 않습니다.** 잘한 부분은 명시적으로 칭찬하여 긍정적인 피드백 문화를 조성합니다.

## Documentation Standards
- 모든 **public API** 는 명확하고 간결한 문서를 제공해야 합니다.
- **복잡한 로직**이나 **비즈니스 규칙**은 주석을 통해 설명합니다.
- **README.md** 는 프로젝트의 목적, 설치 방법, 실행 방법, 주요 기능을 명확히 기술합니다.
# Security & Secrets

## Security & Secrets
- 시크릿/토큰/자격증명/PII는 출력·복사·하드코딩 금지.
- 시크릿 패턴 감지 시: (1) 즉시 중단·마스킹 (2) 안전대체(ENV/시크릿 매니저) (3) 정정 패치 제안.
- 외부 전송/학습이 추정되는 작업은 보류하고 내부 대체 절차 제시.

## Dependency Management
- **의존성 라이브러리**는 정기적으로 보안 취약점 스캔을 수행합니다. (예: `npm audit`, `safety`).
- **오래되거나 유지보수가 중단된** 라이브러리는 사용을 피하고, 대체 가능한 안전한 라이브러리를 찾습니다.
- **라이선스**를 확인하여, 프로젝트에 적합한 라이선스를 가진 라이브러리만 사용합니다.

## Access Control
- **운영 서버**나 **데이터베이스**에 대한 접근은 최소 권한 원칙을 따릅니다.
- **SSH 키**나 **API 키**는 반드시 **Vault**나 **AWS Secrets Manager** 같은 시크릿 관리 툴을 사용하여 관리합니다.
- **코드 리뷰**를 통해 권한 변경이나 민감한 설정 변경이 있는지 검토합니다.# Prisma DB Defaults

## Prisma
- 컴포지트 키/관계 명명 규칙 준수
- 마이그레이션은 **리뷰 후** 적용
- 다운 마이그레이션 경로 필수

## Schema Design
- **필드 이름**은 `camelCase`를 사용합니다.
- **모델 이름**은 `PascalCase`를 사용합니다.
- **관계**는 명확하게 정의하고, 필요시 주석을 추가합니다.

## Query Optimization
- **N+1 문제**를 방지하기 위해 `include`나 `select`를 적절히 사용합니다.
- **복잡한 쿼리**는 미리 컴파일된 쿼리나 raw 쿼리를 고려합니다.
- **인덱스**를 적절히 생성하여 쿼리 성능을 향상시킵니다.# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile은 **멀티스테이지 + alpine** 기본. Buildx, 캐시 전략(브랜치 스코프) 반영.
- docker-compose는 `.env.local` 전제로 설계. `.env` 하드 의존 금지.
- 이미지 최적화(패키지 제거, 압축) 및 `--platform` 표기 유지.

## CI/CD Pipelines
- **테스트**는 모든 브랜치에 대해 자동으로 실행됩니다.
- **빌드**는 `main` 브랜치에 머지되기 전에 성공해야 합니다.
- **배포**는 `main` 브랜치에 머지된 후 자동으로 실행됩니다.
- **환경 변수**는 CI/CD 플랫폼의 시크릿 기능을 사용하여 관리합니다.

## Infrastructure as Code (IaC)
- **Infrastructure**는 코드로 관리되며, 버전 관리됩니다.
- **Terraform**이나 **CloudFormation** 같은 도구를 사용하여 인프라를 정의합니다.
- **코드 리뷰**를 통해 인프라 변경 사항을 검토합니다.# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` 기본, dynamic import 분할 권장.
- route-level 청킹, 폰트/아이콘 WOFF2 우선.
- 빌드 시 폰트/아이콘 분리 로딩, 프리로드 힌트 자동 생성.

## Testing
- **단위 테스트**는 `jest`를 사용합니다.
- **E2E 테스트**는 `cypress`를 사용합니다.
- **테스트 커버리지**는 80% 이상을 목표로 합니다.

## State Management
- **전역 상태 관리**는 `Redux Toolkit` 또는 `Zustand`를 사용합니다.
- **로컬 상태**는 `useState`와 `useReducer`를 적절히 사용합니다.

## Performance Optimization
- **불필요한 렌더링**을 방지하기 위해 `React.memo`, `useMemo`, `useCallback`을 사용합니다.
- **이미지 최적화**를 위해 `next/image` 또는 `gatsby-image` 같은 라이브러리를 사용합니다.# Prompt Recipes

## Docker 이미지 경량화
"우리 표준 Dockerfile 템플릿(멀티스테이지+alpine)으로 리라이트하고, 불필요 패키지 제거·캐시 전략·--platform 적용·docker inspect 사이즈 리포트까지 한 번에 제안해줘."

## React 청크 최적화
"폰트/아이콘 리소스는 분리 로딩, unicons는 TTF/EOT 제외, WOFF2 우선. 전/후 번들 사이즈 표와 타임라인 하이라이트를 보여줘."

## Prisma 마이그레이션 검토
"컴포지트 키/관계 명명 규칙 준수 여부, 다운 마이그레이션 경로, 위험도(High/Medium/Low) 3단계로 리뷰 요약."

## Python 3.13 FastAPI 보일러플레이트
"mypy --strict 통과, pydantic v2, 동기/비동기 혼용 금지, 라우터/스키마/서비스 레이어 모듈 분리 스캐폴딩 생성."

## API 문서 생성
"FastAPI 앱의 경로와 Pydantic 모델을 기반으로 OpenAPI 3.0 스펙 문서를 자동 생성하고, Swagger UI 설정을 포함시켜줘."

## 코드 스타일 개선
"이 Python 코드를 PEP 8 표준에 맞게 리팩토링해줘. 특히, 변수명, 함수명, 클래스명이 명확하고 설명적이도록 변경하고, 불필요한 주석은 제거해줘."

## 성능 분석
"이 Node.js Express 앱의 병목 지점을 프로파일링 도구를 사용하여 분석하고, 성능을 개선할 수 있는 구체적인 제안과 코드 수정 사항을 제시해줘."# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, 타입힌트 필수, `mypy --strict` 통과 기준.
- FastAPI 스캐폴딩 시 pydantic v2 기준.
- 라우터/스키마/서비스 레이어 모듈 분리 강제.

## Testing
- **단위 테스트**는 `pytest`를 사용합니다.
- **통합 테스트**는 실제 데이터베이스나 외부 API를 모킹하여 테스트합니다.
- **테스트 커버리지**는 80% 이상을 목표로 합니다.

## Database
- **ORM**은 `SQLAlchemy` 2.0을 사용합니다.
- **마이그레이션**은 `Alembic`을 사용합니다.
- **연결 풀**을 사용하여 데이터베이스 연결을 효율적으로 관리합니다.

## Security
- **JWT 토큰**을 사용하여 인증을 처리합니다.
- **비밀번호**는 `bcrypt`를 사용하여 해시합니다.
- **CORS** 설정을 통해 허용된 도메인만 접근할 수 있도록 합니다.# UI/Tailwind Defaults

## Tailwind
- 사내 `iris` 팔레트 토큰 우선 사용. 새 색상 제안 금지, 필요 시 토큰 맵핑 테이블 포함.
- Utility-first 접근법 유지, 컴포넌트 추출 시 네이밍 규칙 준수.

## Component Design Principles
- **재사용성**을 고려하여 컴포넌트를 설계합니다.
- **Props**는 명확하고 직관적으로 정의합니다.
- **접근성**(Accessibility)을 준수하여, 모든 사용자가 사용할 수 있도록 합니다.

## Styling Conventions
- **클래스명**은 `BEM` 방식을 따릅니다. (예: `block__element--modifier`)
- **반응형 디자인**은 Tailwind의 반응형 유틸리티를 활용합니다.
- **커스텀 스타일**은 최소화하고, 기본 유틸리티를 최대한 활용합니다.# Project Specific Overrides

## Project Overrides
- 이 프로젝트는 Cursor Rules 자체를 정의하고 관리하는 프로젝트입니다.
- 따라서 프로젝트 특정 규칙은 .cursorrules/project 디렉터리에 정의됩니다.

## Specific to this project
- **문서화**: 모든 규칙 변경은 `PRD.md`와 `README.md`에 반영되어야 합니다.
- **버전 관리**: `.cursorrules.md` 파일은 Git으로 버전 관리됩니다.
- **규칙 생성 스크립트**: `Makefile`의 `rules-merge` 타겟을 사용하여 규칙을 생성합니다.