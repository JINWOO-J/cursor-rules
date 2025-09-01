당신은 한국어 비서입니다. 앞으로의 모든 출력은 예외 없이 한국어로만 작성합니다.
중국어(한자/간체/번체)와 중국어 구두점(，。、「」等)은 절대 사용하지 않습니다.
입력에 중국어가 포함되어도, 내용을 이해한 뒤 자연스러운 한국어로만 답변합니다.
인용이 필요할 때도 한국어 번역문만 제공합니다(고유명사 제외).


래 제안은 팀 전체가 “Cursor Rules(이하 CR)”를 일관되게 활용해 생산성과 품질을 올리기 위한 운영안입니다. 요청하신 대로 깊게 생각(THINK HARD) 해서, 의사결정 과정을 Tree of Thought(3인 전문가 협업) 형식으로 간단 요약 → 최종 실행안 순서로 드립니다.

Tree of Thought 협업 요약

전문가 A – 엔지니어링 매니저 관점
1단계: 규칙은 “조직 공통 → 언어/스택별 → 리포지토리별” 3계층으로 나눠야 충돌이 적고 유지보수가 쉽다.
2단계: 규칙은 문서가 아니라 운영 아티팩트여야 한다(버전, 리뷰, 릴리스 노트, 회귀 테스트).
3단계: 품질 지표(리뷰 코멘트 수 감소, PR 리드타임 단축, AI 제안 수용률)를 측정해 개선 루프를 만든다.

전문가 B – Dev Productivity 관점
1단계: 규칙만으로는 부족, 프롬프트 레시피/매크로와 샘플 스캐폴딩을 같이 배포해야 학습곡선을 줄인다.
2단계: Make/CI와 연동해 “규칙 드리프트 감지”와 “샌드박스 검증 프롬프트”를 자동화한다.
3단계: 온보딩은 30분 내 끝나야 한다(IDE 원클릭 설정, 단일 README).

전문가 C – 보안/컴플라이언스 관점
1단계: 규칙에 비밀정보 차단 행동(시크릿 감지 시 즉시 중단/정정)을 명시.
2단계: 외부 전송/학습 관련 데이터 분류와 금지 항목을 구체 문장으로 포함.
3단계: 레드팀 프롬프트로 탈규칙 시나리오를 정기 점검.

상호 검토 결과: C의 보안 항목은 필수. B의 온보딩/자동화도 필수. A의 계층화·버저닝은 기반. 세 관점 모두 채택(제거 없음).

최종 실행안
1) 목표와 성공 지표

목표: 코드 품질 표준화, PR 리드타임↓, 재작업↓, 보안 사고 0건.

지표(분기별):

리뷰 수정 코멘트/PR 평균 20%↓

AI 제안 적용 비율 30%↑

릴리즈 파이프라인 실패율 10%↓

시크릿 노출 사고 0건 유지

2) 규칙 아키텍처(3계층)
/.cursorrules/                     # 단일 소스 저장소(하위 모듈로 각 repo에 포함 가능)
  org/                             # 조직 공통 규칙(최상위)
    00-core.md
    10-security.md
    20-git-style.md
  stacks/                          # 언어/스택 팩
    node-react.md
    python-fastapi.md
    docker-devops.md
    db-prisma.md
    nginx-ops.md
    ui-tailwind.md
  projects/                        # 리포지토리별 오버라이드
    repo-frontend.md
    repo-backend.md
    repo-infra.md


각 리포지토리에는 .cursorrules.md를 두되, 원본을 include/붙여넣기(Cursor는 텍스트 기반 컨텍스트이므로 합본 생성 스크립트로 해결).

3) 베이스라인 Cursor Rules (샘플 .cursorrules.md)

아래는 귀팀 현실(React/Vite, Node 22, FastAPI 3.13, Prisma, Docker Buildx, Nginx, OpenSearch, Postgres/Mongo, Tailwind “iris” 팔레트, Makefile 파이프라인, Git sentence-style 커밋)에 맞춘 실전 규칙 일부입니다. 그대로 시작 가능한 수준으로 구성했습니다.

# Cursor Rules – Organization Baseline (v0.1.0)

## 0. How to behave (global)
- 답변은 한국어 공손체, **사실 정확도 우선**, 논리적 단계 요약 제공.
- 코드 생성 시 **테스트·빌드 가능한 최소 단위**로 제안하고, 간단한 사용 예시 포함.
- 기존 코드와 충돌 시, 차이·대안·마이그레이션 단계를 **3줄 요약**으로 먼저 제시.

## 1. Security & Secrets
- .env, 시크릿 키, 토큰, 인증정보는 **절대 출력/복사/하드코딩 금지**.
- 시크릿 문자열 패턴 감지 시:
  1) 즉시 중단 및 마스킹, 2) 노출 방지 가이드(환경변수/시크릿 매니저) 제시, 3) 안전 대체 코드 제공.
- 외부 서비스 전송이 추정되는 작업은 수행하지 말고, **대체 오프라인 절차** 우선 제안.

## 2. Git & Commit
- 커밋 메시지는 **문장형·간결체**(Conventional Commits 미사용).
  예: `Fix PS1 prompt escaping for zsh.`
- PR 설명에 변경 요약, 영향 범위, 롤백 방법 **3줄 규약** 준수.

## 3. Language/Framework Defaults
- **Python**: 3.13, 타입힌트 필수, `mypy --strict` 통과 기준. FastAPI 스캐폴딩 시 pydantic v2 기준.
- **Node/React/Vite**: Node 22, `eslint + typescript-eslint` 기본, dynamic import 분할 권장.
- **Tailwind**: 사내 `iris` 팔레트 토큰 우선 사용. 새 색상 제안 금지, 필요 시 토큰 맵핑 테이블 포함.
- **Prisma**: 컴포지트 키/관계 명명 규칙 준수, 마이그레이션은 **리뷰 후** 적용.

## 4. Docker/DevOps
- Dockerfile은 **멀티스테이지 + alpine** 기본. Buildx, 캐시 전략(브랜치 스코프) 반영.
- docker-compose는 `.env.local` 전제로 설계. `.env` 하드 의존 금지.
- 이미지 최적화(패키지 제거, 압축) 및 `--platform` 표기 유지.

## 5. Nginx & Logging
- JSON 로그 포맷 우선, logrotate 설정 스니펫 동봉.
- 헬스체크/리다이렉트 규칙은 site 템플릿에 주석으로 항상 포함.

## 6. Prompt Recipes (how to ask me)
- “**스캐폴딩 생성**”: `<스택> + <테스트> + <빌드 명령> + <실행 방법>` 4요소를 포함해 생성.
- “**성능 개선**”: 번들 사이즈 표로 전/후 비교, 3가지 대안, 선택 기준 3줄.
- “**보안 개선**”: 시크릿 제거 체크리스트 5항, 환경변수 예시, CI 검증 훅.

## 7. Project Overrides
- [repo-frontend] Vite 빌드 시 폰트/아이콘 분리 로딩, 프리로드 힌트 자동 생성.
- [repo-backend] FastAPI 라우팅/의존성 주입 샘플, pydantic 모델/스키마 폴더링 강제.
- [infra] GitHub Actions 캐시 키 정책(브랜치 스코프 + main fallback) 설명 주석 포함.

## 8. What not to do
- “추측성 API 엔드포인트·스키마” 생성 금지. 문서/스키마 없으면 **계약서 초안**부터 제안.
- 팀 합의 없는 새 도구 도입 제안 금지(대안 목록·비교표 형태로만 제안).

4) 프롬프트 레시피/매크로(팀이 자주 쓰게 될 것)

Docker 이미지 경량화:
“우리 표준 Dockerfile 템플릿(멀티스테이지+alpine)으로 리라이트하고, 불필요 패키지 제거·캐시 전략·--platform 적용·docker inspect 사이즈 리포트까지 한 번에 제안해줘.”

React 청크 최적화:
“폰트/아이콘 리소스는 분리 로딩, unicons는 TTF/EOT 제외, WOFF2 우선. 전/후 번들 사이즈 표와 타임라인 하이라이트를 보여줘.”

Prisma 마이그레이션 검토:
“컴포지트 키/관계 명명 규칙 준수 여부, 다운 마이그레이션 경로, 위험도(High/Medium/Low) 3단계로 리뷰 요약.”

Python 3.13 FastAPI 보일러플레이트:
“mypy --strict 통과, pydantic v2, 동기/비동기 혼용 금지, 라우터/스키마/서비스 레이어 모듈 분리 스캐폴딩 생성.”


#PRD: 팀 단위 Cursor Rules 도입 및 운영 (THINK HARD)
0. 문서 정보

버전: v1.0 (초안)

문서 소유: AI Enablement PM

이해관계자: Eng Manager, Dev Productivity(Platform), Security/Compliance, Frontend Lead, Backend Lead, DevOps Lead

최종 목표일: 2025-10-15 (Phase 2 완료)

1. 배경 & 문제정의
1.1 배경

팀은 Cursor를 적극 활용 중이나, 개개인의 프롬프트/룰 편차로 인해 코드 품질, 보안 준수, 리뷰 리드타임이 일정하지 않음.

문서형 가이드만으로는 **운영 가능한 표준화(버저닝·검증·분석)**가 어렵고, 드리프트가 빈번.

1.2 문제

룰이 산발적·비가시적 → 재사용/검증/학습 부하 ↑

보안·시크릿 노출 리스크 상존

온보딩 시간 장기화(>2h), AI 제안 수용률 저조

2. 목적 & 측정지표 (Success Metrics)
2.1 목적(What)

Cursor Rules(이하 CR)를 조직-스택-프로젝트 3계층으로 제품화하여 일관된 코드/보안/속도를 확보

룰의 버전 관리·CI 검증·자동 병합과 프롬프트 레시피 번들로 온보딩을 30분 이내로 단축

2.2 측정지표(So What) — 분기별

PR당 리뷰 수정 코멘트 수 ≥20% 감소

AI 제안 적용률(Accepted/Total) ≥30%p 증가

빌드/릴리즈 파이프라인 실패율 ≥10% 감소

시크릿 노출 사고 0건 유지

신규 인원 온보딩 완료시간 ≤30분

2.3 비목표(Non-Goals)

Cursor 외 모든 IDE/AI 도구 표준화(범위 외)

전사형 LLM 거버넌스 수립(본 PRD는 팀 단위)

3. Tree of Thought 협업(요약)

전문가 A(엔지니어링 매니저): 3계층(조직/스택/프로젝트) 구조 + 릴리스/회귀 테스트 필요

전문가 B(Dev Productivity): 룰만으론 부족 → 프롬프트 레시피/스캐폴딩 묶음 + 원클릭 온보딩

전문가 C(Security/Compliance): 시크릿 차단 행동/데이터 분류·금지항목을 문장으로 강제, 레드팀 점검

상호 검토 결과: 세 관점 모두 채택, 충돌 없음. 제거 대상 없음.

4. 페르소나 & 주요 시나리오
4.1 페르소나

FE/BE 개발자: 실전 스캐폴딩·청킹/성능/보안 레시피 필요

DevOps/플랫폼: CI·Make 연계 검증, 드리프트 탐지

보안담당: 시크릿/반출 방지, 월간 레드팀 체크

신규입사자: 30분 온보딩, 단일 README·원클릭 스크립트

4.2 핵심 사용자 스토리(요약)

신규 입사자로서, make dev-setup 한 번으로 CR·확장·pre-commit을 설치하고, 30분 내 첫 PR을 올리고 싶다.

FE 개발자로서, “번들 사이즈 최적화” 레시피를 실행하면 전/후 비교표와 선택 가이드가 자동으로 생성되길 원한다.

보안담당으로서, 시크릿 패턴 탐지 시 즉시 중단·마스킹·가이드가 규칙에 따라 자동 제안되길 원한다.

5. 요구사항
5.1 기능 요구사항(FR)

규칙 계층화 저장소

구조: .cursorrules/{org,stacks,projects} + 각 리포의 합본 .cursorrules.md

스크립트로 다중 파일 → 단일 합본 자동 생성

CI 통합 검증

병합된 룰에 필수 섹션 존재 검증(보안 등)

아티팩트 업로드(감사/감리 용)

프롬프트 레시피 번들

Docker 경량화, React 청크 최적화, Prisma 마이그레이션 리뷰, FastAPI 3.13 보일러플레이트 등 팀 표준 레시피 제공

pre-commit 훅 제공

시크릿 패턴 차단, Python/Node 정적분석, 규칙 합본 최신화 체크

원클릭 온보딩

make dev-setup으로 편의 기능 설치/구성

5분 사용 가이드 제공

보안/컴플라이언스 준수 동작

금지/허용 예시 문장 포함(시크릿·PII·3rd party IP)

월 1회 레드팀 시나리오 점검 체크리스트 포함

5.2 비기능 요구사항(NFR)

가시성: 룰 버전·변경이력·릴리스 노트 제공

신뢰성: CI·pre-commit 실패 시 명확한 메시지

확장성: 스택 팩 추가가 1일 내 가능

보안성: 시크릿 패턴 지속 업데이트·테스트

개발자 경험: 온보딩 ≤30분, 문서 단일 진입점

6. 정보 구조(IA) & 산출물
/.cursorrules/
  org/
    00-core.md
    10-security.md
    20-git-style.md
  stacks/
    node-react.md
    python-fastapi.md
    docker-devops.md
    db-prisma.md
    nginx-ops.md
    ui-tailwind.md
  projects/
    repo-frontend.md
    repo-backend.md
    repo-infra.md
# 각 리포 루트:
.cursorrules.md        # 합본 결과(커밋 대상)
Makefile               # rules-merge / rules-check / dev-setup 포함
.pre-commit-config.yaml
.github/workflows/cursor-rules.yml

7. 콘텐츠 원칙(요약)

언어/톤: 한국어 공손체, 사실 정확도 우선, 단계 요약

Python: 3.13, 타입힌트·mypy --strict, pydantic v2

Node/React/Vite: Node 22, eslint/ts-eslint, route-level 청킹, 폰트/아이콘 WOFF2

Tailwind: 사내 iris 토큰만 사용, 신규 컬러는 토큰 PR 경로

Prisma: 관계명·복합키 명명 규칙, 다운 마이그레이션 필수

Docker/DevOps: 멀티스테이지+alpine, buildx 캐시(브랜치 스코프), docker inspect로 사이즈/아키 리포트

Nginx: JSON 로그+logrotate 스니펫, /healthz

8. 거버넌스 & 운영 프로세스

Owner: AI Enablement(주), 각 스택 대표(리뷰)

변경 프로세스: PR 기반 → CI 회귀 테스트(샌드박스 프롬프트) → 릴리스 태그(v0.x) → CHANGELOG

레드팀 점검: 월 1회, 시나리오 기반(시크릿 유출·데이터 반출·권한 상승 유도)

교육: 분기 1회 30분 세션(신규 룰/레시피 소개)

9. 롤아웃 계획 & 일정

Phase 1 (D+14): 코어 룰 v0.1.0 + FE/BE 스택 팩 + 3개 리포 시범, 온보딩 스크립트

Gate: 온보딩 30분 테스트 통과, CI 규칙 검증 100% 통과

Phase 2 (D+42): DevOps/DB/디자인 팩 추가, 레드팀 1회, 메트릭 수집·대시보드

Phase 3 (지속): 월간 릴리스·회귀 테스트, 메트릭 기반 개선

10. 수용 기준(샘플, Gherkin)

룰 병합/검증

Given 저장소에 CR 원본이 존재할 때
When make rules-merge && make rules-check를 실행하면
Then _merged.md가 생성되고 “Security & Secrets” 섹션 검증을 통과한다.

온보딩

Given 신규 개발자 환경에서
When make dev-setup 실행 시
Then pre-commit, 에디터 확장, 규칙 합본이 설치되고 README 가이드가 열린다.

보안 차단

Given 커밋에 시크릿 패턴이 포함될 때
When pre-commit 훅이 실행되면
Then 커밋이 거부되고 마스킹/대체 가이드가 출력된다.

11. 리스크 & 대응

룰 과도화로 개발속도 저하 → 최소 코어만 강제, 스택/프로젝트는 가이드+권장

CI 잡 불안정 → 메시지 명확화·재시도 정책·로컬 rules-check 안내

레시피 노화 → 월간 릴리스·회귀 프롬프트 테스트 체계 유지

12. 의존성 & 제한사항

GitHub Actions, pre-commit 사용 가능

팀 표준 런타임: Node 22, Python 3.13

보안: 사내 시크릿 패턴 정의/갱신 채널 필요

13. 성공 시그널(초기)

첫 2주 내 3개 시범 리포 100% 적용

온보딩 30분 SLA 만족(샘플 PR 생성·CI 통과)

레드팀 점검에서 고위험 이슈 0건

14. 첨부(실행 산출물 초안)
14.1 Makefile (핵심 타깃)
.PHONY: rules-merge rules-check dev-setup

CURSOR_RULES_DIR := .cursorrules
CURSOR_MERGED   := $(CURSOR_RULES_DIR)/_merged.md
RULE_PACKS      := $(CURSOR_RULES_DIR)/org/*.md $(CURSOR_RULES_DIR)/stacks/*.md $(CURSOR_RULES_DIR)/projects/*.md

rules-merge:
	@mkdir -p $(CURSOR_RULES_DIR)
	@cat $(RULE_PACKS) > $(CURSOR_MERGED)
	@echo "Merged Cursor Rules -> $(CURSOR_MERGED)"

rules-check:
	@grep -q "Security & Secrets" $(CURSOR_MERGED) || (echo "❌ Missing security section"; exit 1)
	@echo "✅ Rules basic checks passed"

dev-setup:
	@echo "Installing pre-commit & editor configs..."
	@command -v pre-commit >/dev/null || pipx install pre-commit || pip install pre-commit
	@pre-commit install -t pre-commit -t commit-msg || true
	@$(MAKE) rules-merge rules-check
	@echo "Open README for 5-min guide."

14.2 GitHub Actions (룰 검증)
name: cursor-rules
on: [pull_request, push]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: make rules-merge
      - run: make rules-check
      - uses: actions/upload-artifact@v4
        with:
          name: cursor-rules-merged
          path: .cursorrules/_merged.md

14.3 pre-commit (요지)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: detect-private-key
      - id: check-merge-conflict
  - repo: local
    hooks:
      - id: cursor-rules-merged-up-to-date
        name: Ensure merged rules is up to date
        entry: bash -c 'make rules-merge && make rules-check'
        language: system

14.4 .cursorrules/org/10-security.md (핵심 절)
## Security & Secrets
- 시크릿/토큰/자격증명/PII는 출력·복사·하드코딩 금지.
- 시크릿 패턴 감지 시: (1) 즉시 중단·마스킹 (2) 안전대체(ENV/시크릿 매니저) (3) 정정 패치 제안.
- 외부 전송/학습이 추정되는 작업은 보류하고 내부 대체 절차 제시.

14.5 프롬프트 레시피 샘플(요약)

Docker 경량화: “멀티스테이지+alpine로 리라이트, 불필요 패키지 제거, buildx 캐시, docker inspect 사이즈 리포트 포함.”

React 청킹 최적화: “폰트/아이콘 WOFF2만 번들, route-level 동적 import, 전/후 번들 표+선택 기준.”

Prisma 마이그레이션 리뷰: “관계명/복합키 규칙 검사, 다운 마이그레이션, 위험도 3단계.”

FastAPI 3.13 스캐폴딩: “mypy --strict, pydantic v2, 라우터/스키마/서비스 분리.”

15. 오픈 이슈

사내 시크릿 패턴 표준(정규식) 최종 확정

메트릭 수집(“AI 제안 적용률”)의 정의·수집 방법 합의

레드팀 시나리오 저장·결과 공유 채널 확정

16. 승인 필요 사항

전 리포의 .cursorrules/ 도입 동의

GitHub Actions·pre-commit 사용 동의

보안팀의 금지/허용 예시최종 문구 승인

결론

본 PRD는 CR를 제품처럼 운영하기 위한 최소 단위(계층화·자동화·보안)를 규정합니다. Phase 1(2주) 내 시범 리포 적용 및 온보딩 SLA(≤30분)를 달성하면 Phase 2로 확장합니다. 필요 시, 바로 초기 템플릿 세트를 커밋 가능한 형태로 제공하겠습니다.



--

Role: AI Enablement Architect

아래는 팀원이 실제로 **어떻게 쓰는지(시나리오)**와, 디렉터리 구조 **.cursorrules/common vs .cursorrules/project**를 어떻게 운용할지에 대한 결론/정책입니다. 요청하신 대로 THINK HARD & Tree of Thought(3인 협업) 요약 → 최종 운영안 순서로 드립니다.

Tree of Thought 요약

전문가 A(엔지니어링 매니저)

공통 규칙은 단일 소스 오브 트루스로 common에 둔다.

각 리포 특화 내용만 project로 제한한다.

병합 산출물(합본)은 루트의 .cursorrules.md 한 파일로 배포한다.

전문가 B(Dev Productivity)

/generate rules는 **자동 감지(언어/스택)**로 common에서 필요한 팩을 골라 담고, project 오버레이를 마지막에 얹는다.

중복/드리프트 방지를 위해 “동일 문단 감지 → 공통화(PR 제안)” 워크플로를 제공한다.

새 팀원은 30분 온보딩으로 즉시 사용 가능해야 한다.

전문가 C(Security/Compliance)

시크릿/반출 금지 조항은 반드시 common 소스에 위치(모든 리포에 강제 적용).

project에서 이를 약화시키는 오버라이드는 불허.

월 1회 레드팀 프롬프트로 위반 시나리오 점검.

상호 검토 결론: “공통은 common, 리포 특화는 project” 원칙 채택. /generate rules는 공통→스택팩→프로젝트 오버레이 순서로 합본 생성.

1) 팀원이 사용하는 대표 시나리오 (E2E)
시나리오 A — 신규 입사자 온보딩(30분)

리포 클론 후 make dev-setup 실행 → pre-commit, 에디터 설정, 규칙 합본 생성.

README의 5분 가이드로 Cursor 사이드바에 .cursorrules.md 고정.

“PR 템플릿 생성” 레시피 실행 → 팀 규칙 양식에 맞는 PR 본문 자동 작성.

첫 커밋 시 pre-commit 훅이 시크릿/포맷 검증. 실패 시 친절 메시지로 수정 가이드.

시나리오 B — FE 번들 최적화 요청

Cursor에 레시피: “React 청킹 최적화” 실행.

규칙은 common/ui-tailwind, common/node-react의 원칙을 바탕으로 전/후 번들 표와 청킹 전략 제안.

산출 PR은 문장형 커밋 메시지 규칙(common/git-style)을 자동 적용.

시나리오 C — Docker 이미지 경량화

레시피: “멀티스테이지+alpine로 리라이트, buildx 캐시, docker inspect 사이즈 리포트” 실행.

생성된 Dockerfile은 common/docker-devops 규칙에 맞춰 베이스/런타임/로그 정책 준수.

CI가 이미지 사이즈/아키 리포트를 PR 코멘트로 남김.

시나리오 D — Prisma 마이그레이션 리뷰

레시피: “관계명/복합키 규칙 준수 여부 + 다운 마이그레이션 + 위험도(3단계)” 실행.

common/db-prisma 표준에 위배된 부분은 자동 교정안 + 마이그레이션 스크립트 제시.

병합 전 pre-commit이 스키마 포맷/네이밍 체크.

시나리오 E — 보안 위반 탐지

커밋에 토큰/시크릿이 섞여 push 시도 → pre-commit이 차단.

common/security에 정의된 즉시 중단·마스킹·대체 가이드가 출력.

필요 시 /generate rules --remediate security 레시피로 안전한 ENV/시크릿 매니저 설정 패치까지 생성.

2) 디렉터리 구조와 운용 원칙
.cursorrules/
  common/                 # 조직 공통(Single Source of Truth)
    00-core.md
    10-security.md
    20-git-style.md
    stacks/
      node-react.md
      python-fastapi.md
      docker-devops.md
      db-prisma.md
      nginx-ops.md
      ui-tailwind.md
  project/                # 리포 특화(이 리포에서만 의미 있는 내용)
    00-overrides.md       # 공통을 약화/무력화하는 내용은 금지
    90-implementation.md  # 이 repo의 구체 구현/예외(서비스명, 경로 등)
  generated/
    _merged.md            # 생성물(커밋 가능, 인덱싱 용이)
.cursorrules.md           # 루트 합본(= generated/_merged.md의 사본)

결론(질문에 대한 답)

“.cursorrules/common → 공통으로 가져간다?” → 예.
보안/코딩 스타일/커밋 메시지/스택별 기본 원칙 등 모든 리포에 동일 적용되어야 하는 규칙은 반드시 common에 둡니다.

“.cursorrules/project → 해당 프로젝트 지침을 두자?” → 예, 단 “공통화 가능한 내용은 common으로 승격”.
project에는 이 리포에서만 의미 있는 구현 상세(예: 서비스 경로, 내부 엔드포인트, 폴더 구조 특이점)만 둡니다.
/generate rules로 생성된 문단 중 2개 이상 리포에서 동일/유사로 반복되면, 자동 제안으로 common 승격(RFC) 플로우를 트리거합니다.

3) 우선순위(병합 순서) & 충돌 규칙

common/00-core.md

common/10-security.md (보안 조항은 최상위 우선으로 덮어쓰기 불가)

common/stacks/*.md (스택 팩: node-react, python-fastapi, … 선택 포함)

project/*.md (리포 오버레이: 추가/구체화만 허용, 보안 약화는 거부)

병합 규칙: “약화 금지, 구체화 허용”. project 문단에 {override:deny} 메타 주석이 붙은 security 섹션에 대한 수정은 생성기에서 거부합니다.

4) /generate rules 동작 사양(실무용)

입력: (옵션) --stacks "node-react ui-tailwind", --promote, --dry-run

미지정 시 자동 감지(예: package.json, pyproject.toml, Dockerfile 등)

프로세스:

common 코어 + 보안 + 감지된 스택 팩 로드

project 오버레이 로드

제목/섹션 중복 정리, 보안 약화 시도 차단

generated/_merged.md와 루트 .cursorrules.md 생성(동일 내용)

중복/공통화 제안:

동일/유사 문단이 다수 리포에서 관찰되면 “Promote to common?” 제안(로컬 리포트).

--promote 사용 시 자동으로 common/stacks에 신규 문단 파일 생성 + 템플릿 PR 초안 작성.

DRY 가드:

project에 common과 동일 문단 발견 시 경고 + 삭제/링크 대체 제안.

5) “common vs project” 배치 기준(체크리스트)

common으로 가야 하는가? (YES면 common)

두 개 이상의 리포에서 동일 문구 또는 동일 정책이 반복되는가

보안/시크릿/데이터 반출/커밋 규칙/로그 정책 등 원칙 수준인가

특정 리포의 내부 경로·명·변수가 없어도 성립하는가

project로 남겨야 하는가? (YES면 project)

이 리포의 폴더 구조/엔드포인트/환경변수 키 등 구현 상세인가

공통 정책을 약화시키지 않고, 그 구체화만 수행하는가

타 리포로의 재사용 가능성이 낮은가

6) 최소 실행 템플릿 (요지)
Makefile
.PHONY: rules-generate rules-merge rules-check rules-promote dev-setup

CURSOR_RULES_DIR := .cursorrules
MERGED := $(CURSOR_RULES_DIR)/generated/_merged.md

rules-merge:
	@mkdir -p $(CURSOR_RULES_DIR)/generated
	@cat $(CURSOR_RULES_DIR)/common/00-core.md \
	     $(CURSOR_RULES_DIR)/common/10-security.md \
	     $(CURSOR_RULES_DIR)/common/stacks/*.md \
	     $(CURSOR_RULES_DIR)/project/*.md > $(MERGED)
	@cp $(MERGED) .cursorrules.md
	@echo "Merged -> .cursorrules.md"

rules-check:
	@grep -q "^## Security" $(MERGED) || (echo "❌ security section missing"; exit 1)
	@echo "✅ rules basic checks passed"

rules-generate: rules-merge rules-check

rules-promote:
	@echo "🔎 scanning for duplicate blocks…"
	@echo "(여기서 중복 탐지/승격 스크립트 연결)"

dev-setup:
	@command -v pre-commit >/dev/null || pipx install pre-commit || pip install pre-commit
	@pre-commit install -t pre-commit -t commit-msg || true
	@$(MAKE) rules-generate

pre-commit (요지)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: detect-private-key
      - id: check-merge-conflict
  - repo: local
    hooks:
      - id: cursor-rules
        name: Generate & Check Cursor Rules
        entry: bash -c 'make rules-generate'
        language: system

7) 자주 쓰는 질문에 대한 짧은 답

Q. project에 쓴 지침이 좋은 내용이면?
A. /generate rules --promote로 common 승격 PR 초안을 자동 생성하세요(템플릿 포함).

Q. project에서 보안 규칙을 완화하고 싶다?
A. 불가합니다. security 섹션은 override deny입니다. 보완/구체화만 허용됩니다.

Q. 합본 .cursorrules.md는 커밋해야 하나?
A. 네. 인덱싱 안정성과 코드리뷰 가시성을 위해 커밋합니다. 원본은 common/project가 SSoT이며, 합본은 배포물로 봅니다.

8) 결론

질문 요지대로 정리하면: **공통은 common, 리포 특화는 project**가 맞고, /generate rules는 common → stacks → project 순으로 합본 생성합니다.

project에서 반복되는 내용은 **승격 기준(≥2 리포 반복)**을 충족하는 즉시 common으로 올리는 자동 제안을 둬서 DRY & 일관성을 유지합니다.

이 구조로 팀원 시나리오(온보딩·최적화·보안·데브옵스)가 30분 내 가동되며, 규칙은 “문서”가 아니라 **운영되는 제품(버전/검증/승격)**이 됩니다.
