---
lang: kr
title: Naming 규칙 (강화판)
description: 파일/디렉토리, 코드, API, 데이터베이스, 인프라 전반에서 일관성과 명확성을 극대화하는 엄격한 네이밍 규칙
tags: [naming, convention, style, consistency, database, api, infra]
---

# Naming 규칙 (강화판)

본 문서는 **명확성(clarity)**, **일관성(consistency)**, **예측가능성(predictability)**을 최우선으로 하는 팀 네이밍 규칙의 강화판이다.  
모든 구성원은 아래 규칙을 **기본값으로 준수**하며, 예외는 ADR에 문서화하여 승인한다.

---

## 0) 우선순위 & 의사결정 트리

1. **의도 명확성** > 일관성 > 간결성 > 구현 편의성
2. 팀 표준을 따르며, 충돌 시 다음 순서로 결정:
   - (1) 이 문서의 규칙
   - (2) 언어/플랫폼 공식 가이드
   - (3) 기존 레거시와의 호환(최소화)
3. **약어/줄임말 금지** (공통 약어는 허용: `id`, `api`, `url`, `db`, `ip`, `ui`, `cpu`, `tls`)

---

## 1) 파일 · 디렉토리 · 저장소 이름

- **디렉토리/파일**: `kebab-case`  
  예) `user-service`, `payment-worker`, `api-gateway`, `readme.md`
- **프로그래밍 언어별 소스 파일 확장자**는 표준 유지 (예: `.py`, `.ts`, `.go`)
- **리포지토리**: `kebab-case` + 도메인접두어(선택)  
  예) `app-user-service`, `infra-terraform-modules`, `web-frontend`
- 금지: 공백, 대문자 시작, 특수문자(`@ # $ % ^ & *`)  
- 허용: 숫자, 하이픈(-), 점(`.`) (확장자), 언더스코어는 **파일 내부 식별자**에서만 권장

```
# good
core-utils/
core-utils/CHANGELOG.md
data-migrations/2025-09-04_add_user_index.sql

# bad
CoreUtils/
data migrations/
migrations/addIndex.sql
```

`.dockerignore`/`.gitignore`/`README.md`와 같은 업계 표준 파일명은 예외적으로 Pascal/Upper를 허용.

---

## 2) 코드 네이밍 (언어 공통 규칙)

- **클래스/타입/인터페이스**: `PascalCase`  
- **함수/메서드/변수**:  
  - Python, Rust: `snake_case`  
  - JS/TS, Go, Java/Kotlin: `camelCase`  
- **상수**: `UPPER_SNAKE_CASE`
- **불리언**: `is_`, `has_`, `can_`, `should_`, `allow_` 접두사  
- **이벤트 핸들러**: `on<Event>` (예: `onUserCreated`)  
- **비동기 함수**(JS/TS): `verbAsync` 금지, 대신 **반환 타입으로 비동기 표현** (표준 권장)

```python
# good (Python)
class UserProfile: ...
MAX_RETRY = 3
def get_user_name(user_id: int) -> str: ...
is_active = True

# bad
class user_profile: ...
MaxRetry = 3
def GetUserName(UserId): ...
activeFlag = True
```

```ts
// good (TypeScript)
class UserProfile {}
const MAX_RETRY = 3;
function getUserName(userId: number): string { ... }
const isActive = true;

// bad
class user_profile {}
const MaxRetry = 3;
function GetUserName(UserID: number) { ... }
const active_flag = true;
```

---

## 3) 패키지/모듈/네임스페이스

- 패키지/모듈: **짧은 `kebab-case` 또는 언어 권장 표기**  
  - Python 패키지: `snake_case` (PEP 8), **모두 소문자**
  - npm 패키지: `kebab-case`, 범위(scope)는 조직 규칙 적용 (`@org/user-service`)
- 루트 네임스페이스는 **도메인 또는 바운디드 컨텍스트** 기준으로 설계

---

## 4) API 설계 (REST/HTTP)

- 경로: **소문자 + 복수형 + kebab-case**  
  예) `/v1/users`, `/v1/user-orders/{order-id}`
- **행위는 동사 아님**: 경로에 동사 금지. 행위는 **HTTP 메서드**로 표현
- 버전: **접두사** `/v1` (URL 버전), 헤더 버전 병행 금지
- 쿼리 파라미터: `snake_case` 금지, **`kebab-case` 또는 `camelCase`** 중 팀 통일 (권장: kebab-case)
- 에러 코드: `kebab-case` + 영역 접두사  
  예) `auth/invalid-credentials`, `orders/out-of-stock`

```http
# good
GET /v1/users?sort=created-at&order=desc
GET /v1/users/{user-id}

# bad
GET /v1/getUsers
GET /v1/user_list
```

### JSON 필드 네이밍
- 공개 API: `camelCase` 권장 (웹/모바일 친화)  
- 내부 서비스 간: 언어 지배적 컨벤션에 맞춰 통일 (Python 중심이면 `snake_case` 가능)  
- 하나의 API 내 혼용 금지

---

## 5) 이벤트/메시지/큐 토픽

- 이벤트명: `domain.action` (점 구분, **소문자**)  
  예) `user.created`, `order.cancelled`  
- 메시지 키/헤더: `kebab-case`  
- 큐/토픽: `kebab-case` + 환경 접두사(optional)  
  예) `prod-user-events`, `dev-order-jobs`

---

## 6) 데이터베이스 네이밍 (SQL 중심)

- **테이블**: 복수형 `snake_case` → `users`, `order_items`  
- **컬럼**: `snake_case` → `user_id`, `created_at`, `is_active`  
- **PK**: `id` (단일키), 복합키 지양하고 **대리키 + 유니크 인덱스** 권장  
- **FK**: `<참조테이블단수>_id` → `user_id`, `order_id`  
- **인덱스**: `idx_<테이블>__<컬럼1>__<컬럼2>` (더블 언더스코어로 다중컬럼 구분)  
  예) `idx_users__email`, `idx_order_items__order_id__product_id`  
- **유니크 제약**: `uq_<테이블>__<컬럼...>`  
- **체크 제약**: `ck_<테이블>__<의미>`  
- **FK 제약**: `fk_<테이블>__<참조테이블>`  
- **시퀀스**: `seq_<테이블>__<의미>`
- **마이그레이션 파일**: `YYYY-MM-DD_HHMM_<의미>.sql`  
  예) `2025-09-04_1030_add_users_email_unique.sql`

```sql
-- good
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE UNIQUE INDEX uq_users__email ON users(email);
CREATE INDEX idx_users__created_at ON users(created_at);

-- bad
CREATE TABLE User (
  UserID BIGINT PRIMARY KEY,
  EmailAddress VARCHAR(255),
  ActiveFlag INT
);
```

---

## 7) 환경 변수/설정/시크릿

- **환경 변수**: `UPPER_SNAKE_CASE` + 도메인 접두사  
  예) `APP_ENV`, `APP_PORT`, `DB_HOST`, `AWS_REGION`  
- **시크릿 키 이름**: `UPPER_SNAKE_CASE` + `_SECRET`/`_KEY`/`_TOKEN`  
  예) `DB_PASSWORD`(허용), `GITHUB_TOKEN`, `JWT_SIGNING_KEY`
- 금지: 모模糊한 이름 (`PASSWORD`, `TOKEN` 등 단독)

---

## 8) 로그/메트릭/트레이스

- **로그 필드 키**: `snake_case` (머신 가공 친화)  
- **메트릭 이름**: `<domain>_<resource>_<action>[_unit]` (소문자 + 언더스코어)  
  예) `auth_login_success_total`, `orders_created_total`, `orders_amount_sum_usd`  
- **레이블/태그**: `snake_case`  
- **트레이스 스팬 이름**: `kebab-case` + 동사  
  예) `fetch-user-profile`, `create-order`

---

## 9) 시간/통화/단위/로캘 키

- 시간 필드명: `_at` 접미 (`created_at`, `updated_at`, `expires_at`)  
- 기간/만료: `_ttl`, `_timeout_ms` (단위 접미 명시)  
- 금액: `_amount` + 통화는 별도 필드 (`amount`, `currency`) 또는 단위 접미(`_usd`)  
- 로캘 문자열 키(i18n): `dot.separated.keys` (소문자)

---

## 10) 접근제어/권한/역할

- 역할명: `kebab-case` → `admin`, `read-only`, `billing-manager`  
- 권한 스코프: `domain:action` → `users:read`, `orders:write`

---

## 11) 에러/상태/이넘

- 에러 코드: `kebab-case` + 영역 접두사  
  예) `auth/invalid-credentials`, `payment/insufficient-funds`  
- 상태값: `snake_case` 또는 `kebab-case`로 고정 (데이터베이스/JSON 간 일관성 유지)  
  예) `pending`, `in_progress`, `completed`, `failed`  
- Enum 식별자는 **언어 규칙에 맞춤** (Python: `PascalCase` 멤버 금지 → 상수형 `UPPER_SNAKE_CASE` 권장, TS: `PascalCase` 타입 + `camelCase` 값 또는 `UPPER_SNAKE_CASE` 값)

---

## 12) 금지/경고 패턴

- 금지: `data`, `info`, `value`, `flag`, `tmp`, `test`, `final`, `misc`  
- 약어 금지(예외 제외): `cfg`(→`config`), `usr`(→`user`), `svc`(→`service`)  
- 의미 중복 접미/접두: `userModel`, `UserClass`, `ServiceService`
- 다국어 혼용 금지: 한국어/영어 혼용 이름 금지

---

## 13) 팀 간 매핑 규칙 (Cross-language Mapping)

| 개념 | Python | JS/TS | SQL | REST JSON |
|---|---|---|---|---|
| 클래스/타입 | PascalCase | PascalCase | - | - |
| 함수/변수 | snake_case | camelCase | snake_case | camelCase (공개 API 권장) |
| 상수 | UPPER_SNAKE_CASE | UPPER_SNAKE_CASE | - | UPPER_SNAKE_CASE (필요시) |
| 테이블/컬럼 | - | - | snake_case | snake_case ↔ camelCase 변환 가능 |
| 경로/리소스 | - | - | - | kebab-case (복수형) |

---

## 14) 자동 검사(린트) 가이드

- **pre-commit** 훅으로 이름 규칙 정적 검사:
  - 파일/디렉토리: `^[a-z0-9]+(-[a-z0-9]+)*$`
  - SQL 마이그레이션: `^\d{4}-\d{2}-\d{2}_[0-2]\d[0-5]\d_[a-z0-9-]+\.sql$`
  - 브랜치명: `^(feature|fix|chore|docs|refactor|perf|test)\/[a-z0-9-]+$`

```yaml
# .pre-commit-config.yaml (발췌)
repos:
  - repo: local
    hooks:
      - id: check-filenames
        name: Check filenames (kebab-case)
        entry: bash -c 'git diff --cached --name-only | xargs -I{} bash -c "[[ \"{}\" =~ ^[a-z0-9./_-]+$ ]] && exit 0 || (echo Invalid name: {}; exit 1)"'
        language: system
      - id: check-branch
        name: Check branch naming
        entry: bash -c '[[ "${BRANCH_NAME:-$CI_COMMIT_REF_NAME}" =~ ^(feature|fix|chore|docs|refactor|perf|test)\/[a-z0-9-]+$ ]] || (echo Invalid branch: ${BRANCH_NAME:-$CI_COMMIT_REF_NAME}; exit 1)'
        language: system
```

---

## 15) 리팩터링/리네임 절차

1. 영향 범위 식별(코드/DB/문서/대시보드/권한)  
2. **검색 가능 패턴** 정의(정규식) 후 대체 계획 수립  
3. 마이그레이션 스크립트 준비 (DB: 기존 컬럼 **동시 지원 기간** 부여)  
4. 배포 단계적 전환(읽기→쓰기 순서)  
5. 텔레메트리/알람 대체 키 동기화  
6. 최종 제거 시점 ADR 기록

---

## 16) 결정 체크리스트

- [ ] 이름만 보고 역할이 이해되는가?  
- [ ] 동일 계층에서 일관된 케이스 사용 중인가?  
- [ ] 단위/통화/시간이 명시됐는가? (`_ms`, `_sec`, `_usd`, `_at`)  
- [ ] 약어/내부용어/외래어를 최소화했는가?  
- [ ] 외부/내부 API 간 케이스 변환 규칙이 문서화됐는가?  
- [ ] 린트/테스트/모니터링 규칙과 충돌하지 않는가?

---

## 17) 예시 모음 (Good vs Bad)

```
# 디렉토리
good:  user-service, access-logs
bad:   UserService, AccessLogs, userSvc

# REST
good:  /v1/order-items/{item-id}
bad:   /v1/getOrderItems, /v1/orderItems

# SQL
good:  idx_order_items__order_id__product_id
bad:   order_items_order_id_idx, idxOrderItemsOnOrderId

# Env
good:  APP_ENV=production, DB_HOST=..., JWT_SIGNING_KEY=...
bad:   ENV=prod, HOST=..., SECRET=...
```

---

본 문서는 **프로젝트 전 영역에서 네이밍을 통합**하기 위한 기준이다.  
예외가 필요한 경우 반드시 ADR에 근거와 영향도를 기록하고, **타임라인을 포함한 수습 계획**을 제시한다.

---

