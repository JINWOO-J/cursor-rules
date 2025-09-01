# PRD: 팀 단위 Cursor Rules 도입 및 운영 (v1.0)

## 0. 문서 정보

- **버전**: v1.0 (초안)
- **문서 소유**: AI Enablement PM
- **이해관계자**: Eng Manager, Dev Productivity(Platform), Security/Compliance, Frontend Lead, Backend Lead, DevOps Lead
- **최종 목표일**: 2025-10-15 (Phase 2 완료)

## 1. 배경 & 문제정의

### 1.1 배경

팀은 Cursor를 적극 활용 중이나, 개개인의 프롬프트/룰 편차로 인해 코드 품질, 보안 준수, 리뷰 리드타임이 일정하지 않음.

문서형 가이드만으로는 **운영 가능한 표준화(버저닝·검증·분석)**가 어렵고, 드리프트가 빈번.

### 1.2 문제

- 룰이 산발적·비가시적 → 재사용/검증/학습 부하 ↑
- 보안·시크릿 노출 리스크 상존
- 온보딩 시간 장기화(>2h), AI 제안 수용률 저조

## 2. 목적 & 측정지표 (Success Metrics)

### 2.1 목적(What)

Cursor Rules(이하 CR)를 조직-스택-프로젝트 3계층으로 제품화하여 일관된 코드/보안/속도를 확보

룰의 버전 관리·CI 검증·자동 병합과 프롬프트 레시피 번들로 온보딩을 30분 이내로 단축

### 2.2 측정지표(So What) — 분기별

- PR당 리뷰 수정 코멘트 수 ≥20% 감소
- AI 제안 적용률(Accepted/Total) ≥30%p 증가
- 빌드/릴리즈 파이프라인 실패율 ≥10% 감소
- 시크릿 노출 사고 0건 유지
- 신규 인원 온보딩 완료시간 ≤30분

### 2.3 비목표(Non-Goals)

- Cursor 외 모든 IDE/AI 도구 표준화(범위 외)
- 전사형 LLM 거버넌스 수립(본 PRD는 팀 단위)

## 3. Tree of Thought 협업(요약)

- **전문가 A(엔지니어링 매니저)**: 3계층(조직/스택/프로젝트) 구조 + 릴리스/회귀 테스트 필요
- **전문가 B(Dev Productivity)**: 룰만으론 부족 → 프롬프트 레시피/스캐폴딩 묶음 + 원클릭 온보딩
- **전문가 C(Security/Compliance)**: 시크릿 차단 행동/데이터 분류·금지항목을 문장으로 강제, 레드팀 점검

상호 검토 결과: 세 관점 모두 채택, 충돌 없음. 제거 대상 없음.

## 4. 페르소나 & 주요 시나리오

### 4.1 페르소나

- **FE/BE 개발자**: 실전 스캐폴딩·청킹/성능/보안 레시피 필요
- **DevOps/플랫폼**: CI·Make 연계 검증, 드리프트 탐지
- **보안담당**: 시크릿/반출 방지, 월간 레드팀 체크
- **신규입사자**: 30분 온보딩, 단일 README·원클릭 스크립트

### 4.2 핵심 사용자 스토리(요약)

- **신규 입사자**로서, `make dev-setup` 한 번으로 CR·확장·pre-commit을 설치하고, 30분 내 첫 PR을 올리고 싶다.
- **FE 개발자**로서, “번들 사이즈 최적화” 레시피를 실행하면 전/후 비교표와 선택 가이드가 자동으로 생성되길 원한다.
- **보안담당**으로서, 시크릿 패턴 탐지 시 즉시 중단·마스킹·가이드가 규칙에 따라 자동 제안되길 원한다.

## 5. 요구사항

### 5.1 기능 요구사항(FR)

- **규칙 계층화 저장소**
  - 구조: `.cursorrules/{org,stacks,projects}` + 각 리포의 합본 `.cursorrules.md`
  - 스크립트로 다중 파일 → 단일 합본 자동 생성
- **CI 통합 검증**
  - 병합된 룰에 필수 섹션 존재 검증(보안 등)
  - 아티팩트 업로드(감사/감리 용)
- **프롬프트 레시피 번들**
  - Docker 경량화, React 청크 최적화, Prisma 마이그레이션 리뷰, FastAPI 3.13 보일러플레이트 등 팀 표준 레시피 제공
- **pre-commit 훅 제공**
  - 시크릿 패턴 차단, Python/Node 정적분석, 규칙 합본 최신화 체크
- **원클릭 온보딩**
  - `make dev-setup`으로 편의 기능 설치/구성
  - 5분 사용 가이드 제공
- **보안/컴플라이언스 준수 동작**
  - 금지/허용 예시 문장 포함(시크릿·PII·3rd party IP)
  - 월 1회 레드팀 시나리오 점검 체크리스트 포함

### 5.2 비기능 요구사항(NFR)

- **가시성**: 룰 버전·변경이력·릴리스 노트 제공
- **신뢰성**: CI·pre-commit 실패 시 명확한 메시지
- **확장성**: 스택 팩 추가가 1일 내 가능
- **보안성**: 시크릿 패턴 지속 업데이트·테스트
- **개발자 경험**: 온보딩 ≤30분, 문서 단일 진입점

## 6. 정보 구조(IA) & 산출물

```
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
```

## 7. 콘텐츠 원칙(요약)

- **언어/톤**: 한국어 공손체, 사실 정확도 우선, 단계 요약
- **Python**: 3.13, 타입힌트·`mypy --strict`, pydantic v2
- **Node/React/Vite**: Node 22, `eslint/ts-eslint`, route-level 청킹, 폰트/아이콘 WOFF2
- **Tailwind**: 사내 `iris` 토큰만 사용, 신규 컬러는 토큰 PR 경로
- **Prisma**: 관계명·복합키 명명 규칙, 다운 마이그레이션 필수
- **Docker/DevOps**: 멀티스테이지+alpine, buildx 캐시(브랜치 스코프), `docker inspect`로 사이즈/아키 리포트
- **Nginx**: JSON 로그+logrotate 스니펫, `/healthz`

## 8. 거버넌스 & 운영 프로세스

- **Owner**: AI Enablement(주), 각 스택 대표(리뷰)
- **변경 프로세스**: PR 기반 → CI 회귀 테스트(샌드박스 프롬프트) → 릴리스 태그(v0.x) → CHANGELOG
- **레드팀 점검**: 월 1회, 시나리오 기반(시크릿 유출·데이터 반출·권한 상승 유도)
- **교육**: 분기 1회 30분 세션(신규 룰/레시피 소개)

## 9. 롤아웃 계획 & 일정

- **Phase 1 (D+14)**: 코어 룰 v0.1.0 + FE/BE 스택 팩 + 3개 리포 시범, 온보딩 스크립트
  - **Gate**: 온보딩 30분 테스트 통과, CI 규칙 검증 100% 통과
- **Phase 2 (D+42)**: DevOps/DB/디자인 팩 추가, 레드팀 1회, 메트릭 수집·대시보드
- **Phase 3 (지속)**: 월간 릴리스·회귀 테스트, 메트릭 기반 개선

## 10. 수용 기준(샘플, Gherkin)

### 룰 병합/검증

```gherkin
Given 저장소에 CR 원본이 존재할 때
When make rules-merge && make rules-check를 실행하면
Then _merged.md가 생성되고 "Security & Secrets" 섹션 검증을 통과한다.
```

### 온보딩

```gherkin
Given 신규 개발자 환경에서
When make dev-setup 실행 시
Then pre-commit, 에디터 확장, 규칙 합본이 설치되고 README 가이드가 열린다.
```

### 보안 차단

```gherkin
Given 커밋에 시크릿 패턴이 포함될 때
When pre-commit 훅이 실행되면
Then 커밋이 거부되고 마스킹/대체 가이드가 출력된다.
```

## 11. 리스크 & 대응

- **룰 과도화로 개발속도 저하** → 최소 코어만 강제, 스택/프로젝트는 가이드+권장
- **CI 잡 불안정** → 메시지 명확화·재시도 정책·로컬 `rules-check` 안내
- **레시피 노화** → 월간 릴리스·회귀 프롬프트 테스트 체계 유지

## 12. 의존성 & 제한사항

- GitHub Actions, pre-commit 사용 가능
- 팀 표준 런타임: Node 22, Python 3.13
- 보안: 사내 시크릿 패턴 정의/갱신 채널 필요

## 13. 성공 시그널(초기)

- 첫 2주 내 3개 시범 리포 100% 적용
- 온보딩 30분 SLA 만족(샘플 PR 생성·CI 통과)
- 레드팀 점검에서 고위험 이슈 0건

## 14. 첨부(실행 산출물 초안)

### 14.1 Makefile (핵심 타깃)

```makefile
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
```

### 14.2 GitHub Actions (룰 검증)

```yaml
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
```

### 14.3 pre-commit (요지)

```yaml
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
```

### 14.4 .cursorrules/org/10-security.md (핵심 절)

```markdown
## Security & Secrets

- 시크릿/토큰/자격증명/PII는 출력·복사·하드코딩 금지.
- 시크릿 패턴 감지 시: (1) 즉시 중단·마스킹 (2) 안전대체(ENV/시크릿 매니저) (3) 정정 패치 제안.
- 외부 전송/학습이 추정되는 작업은 보류하고 내부 대체 절차 제시.
```

### 14.5 프롬프트 레시피 샘플(요약)

- **Docker 경량화**: “멀티스테이지+alpine로 리라이트, 불필요 패키지 제거, buildx 캐시, docker inspect 사이즈 리포트 포함.”
- **React 청킹 최적화**: “폰트/아이콘 WOFF2만 번들, route-level 동적 import, 전/후 번들 표+선택 기준.”
- **Prisma 마이그레이션 리뷰**: “관계명/복합키 규칙 검사, 다운 마이그레이션, 위험도 3단계.”
- **FastAPI 3.13 스캐폴딩**: “mypy --strict, pydantic v2, 라우터/스키마/서비스 분리.”

## 15. 오픈 이슈

- 사내 시크릿 패턴 표준(정규식) 최종 확정
- 메트릭 수집(“AI 제안 적용률”)의 정의·수집 방법 합의
- 레드팀 시나리오 저장·결과 공유 채널 확정

## 16. 승인 필요 사항

- 전 리포의 `.cursorrules/` 도입 동의
- GitHub Actions·pre-commit 사용 동의
- 보안팀의 금지/허용 예시최종 문구 승인

## 결론

본 PRD는 CR를 제품처럼 운영하기 위한 최소 단위(계층화·자동화·보안)를 규정합니다. Phase 1(2주) 내 시범 리포 적용 및 온보딩 SLA(≤30분)를 달성하면 Phase 2로 확장합니다. 필요 시, 바로 초기 템플릿 세트를 커밋 가능한 형태로 제공하겠습니다.