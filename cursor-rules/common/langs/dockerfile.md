---
lang: kr
title: Dockerfile 규칙
description: 재현 가능하고 안전하며 빠른 컨테이너 이미지를 만들기 위한 Dockerfile 베스트 프랙티스
tags: [docker, dockerfile, container, devops, security, performance]
---

# Dockerfile 규칙

Dockerfile을 작성할 때 일관성과 보안, 캐시 효율, 빌드 재현성(reproducibility)을 높이기 위한 팀 규칙을 정의한다.  
런타임/오케스트레이션 규칙(Kubernetes, Compose 등)은 별도 문서에서 다룬다.

---

## 1) 베이스 이미지 선택

- **공식 이미지** 또는 **검증된 내부 베이스**만 사용한다.
- 용량 최소화를 위해 `-slim` 또는 `alpine`을 우선 고려하되, **네이티브 빌드/글리브 문제**를 확인한다.
- **고정 태그** 사용: `:latest` 금지, **메이저/마이너+digest** 권장.

```dockerfile
# good
FROM python:3.11-slim@sha256:...

# bad
FROM python:latest
```

---

## 2) 멀티 스테이지 빌드

- 빌드 의존성과 런타임을 분리하여 최종 이미지를 최소화한다.
- `--target`으로 단계적 빌드를 지원한다.

```dockerfile
# build stage
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# runtime stage
FROM nginx:1.27-alpine AS runtime
COPY --from=build /app/dist /usr/share/nginx/html
```

---

## 3) 레이어 & 캐시 최적화

- 변경 빈도 낮은 파일을 **먼저** 복사한다(`package.json`, `poetry.lock` 등).
- `RUN` 명령은 가능한 **한 줄로** 묶되, **논리적 단계**는 나누어 캐시 효율과 가독성 균형을 맞춘다.
- `--mount=type=cache` (BuildKit)로 의존성 캐시를 활용한다.

```dockerfile
# Node 예시
FROM node:20-slim AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    npm ci --no-audit --no-fund

COPY . .
RUN npm run build
```

---

## 4) 패키지 설치 (APT/APK)

- 비대화식 모드와 고정 버전 사용, 설치 후 **캐시/리스트 정리**.
- 필요 패키지만 설치하고 사용 후 제거(빌드용 도구는 build stage에서만).

```dockerfile
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      curl=7.88.* ca-certificates=2023* \
 && rm -rf /var/lib/apt/lists/*
```

---

## 5) 비루트(Non-root) 실행

- 런타임 이미지에서는 반드시 **비루트 사용자**로 실행.
- 파일/디렉터리 소유권을 적절히 설정.

```dockerfile
RUN addgroup --system app && adduser --system --ingroup app app
USER app
WORKDIR /app
```

---

## 6) 환경변수 / ARG / 시크릿

- 빌드 시 값은 `ARG`, 런타임 설정은 `ENV` 사용.
- 시크릿은 **BuildKit 시크릿 마운트** 또는 오케스트레이터(예: K8s Secret) 사용. Dockerfile에 **직접 하드코딩 금지**.

```dockerfile
ARG APP_VERSION
ENV NODE_ENV=production

# BuildKit secret 사용 예시
# docker build --secret id=npmrc,src=$HOME/.npmrc .
RUN --mount=type=secret,id=npmrc \
    npm ci
```

---

## 7) 메타데이터(OCI Labels)

- 이미지에 유지보수자, 소스, 버전, 설명 등 **OCI 라벨**을 포함한다.

```dockerfile
LABEL org.opencontainers.image.title="my-service" \
      org.opencontainers.image.version="$APP_VERSION" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.description="Awesome service" \
      org.opencontainers.image.licenses="Apache-2.0"
```

---

## 8) ENTRYPOINT / CMD

- **exec form**을 사용해 신호 전달과 PID 1 문제를 방지한다.
- 초기화가 필요하면 `tini`/`dumb-init`를 활용한다.

```dockerfile
# good
ENTRYPOINT ["tini","--"]
CMD ["python","-m","app"]

# bad (shell form)
CMD python -m app
```

---

## 9) Healthcheck

- 애플리케이션의 실질적인 준비상태를 확인하는 경량 엔드포인트를 사용한다.
- 과도한 빈도/타임아웃은 피하고 지표로 활용한다.

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:8080/health || exit 1
```

---

## 10) 포트 / 네트워킹

- `EXPOSE`는 **문서적 의미**이며 실제 포트를 바인딩하지는 않음을 이해한다.
- 여러 환경에서 충돌이 없도록 **환경변수 기반 포트** 사용을 고려한다.

```dockerfile
EXPOSE 8080
```

---

## 11) 파일 복사 & 권한

- `COPY --chown=`으로 권한을 명시적으로 설정한다.
- 불필요한 파일이 포함되지 않도록 **.dockerignore**를 철저히 관리.

```dockerfile
COPY --chown=app:app ./dist/ /app/
```

`.dockerignore` 예시:
```
.git
.gitignore
node_modules
__pycache__
*.log
*.pyc
.env
dist/
build/
```

---

## 12) 재현 가능한 빌드

- 의존성은 **lock 파일**을 사용하고, 빌드 아규먼트/환경 변수를 **명시**한다.
- 가능한 한 **시계(time)**, **랜덤(seed)**에 의존하지 않게 작성한다.
- CI에서 **동일한 빌드 옵션**을 강제한다.

```dockerfile
ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}
```

---

## 13) 이미지 스캔 & SBOM

- CI에서 이미지 취약점 스캔(예: Trivy, Grype)을 실행한다.
- SBOM(예: `syft`)을 생성해 아티팩트로 보관한다.

```bash
trivy image --exit-code 1 --severity HIGH,CRITICAL my-image:tag
syft my-image:tag -o spdx-json > sbom.spdx.json
```

---

## 14) 플랫폼 / QEMU

- 멀티 아키텍처가 필요하면 **Buildx**로 `--platform`을 명시하고, 크로스 빌드 시 QEMU를 설정한다.
- 네이티브와 크로스 빌드 결과의 차이를 확인한다.

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t org/app:1.0 --push .
```

---

## 15) 성능 팁

- 런타임 이미지는 **최소 계층** + **최소 바이너리**만 포함.
- 압축(예: `--compress`)과 캐시 전략으로 **CI 시간을 단축**.
- 대형 아티팩트는 **외부 저장소/릴리스**를 활용하고 이미지에 불필요하게 포함하지 않는다.

---

## 16) 언어별 패턴 (요약)

- **Node.js**: `npm ci`/`pnpm fetch` + cache mount, `node:slim`, `corepack enable`.
- **Python**: multi-stage에서 빌드(`pip wheel`), 런타임은 `python:*-slim` + `venv` 또는 `uv`.
- **Go**: static 빌드 후 `scratch`/`distroless`로 최종 이미지.
- **Java**: JDK stage와 JRE/`distroless/java` 런타임 분리.

```dockerfile
# Go 예시
FROM golang:1.22 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM gcr.io/distroless/static:nonroot
COPY --from=build /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

---

## 17) Compose/런타임 힌트(요약)

- 구성은 코드에서 분리하고, 런타임 환경변수로 주입한다.
- 읽기 전용 루트, 최소 권한 원칙을 지킨다.

```yaml
# docker-compose.yml (발췌)
services:
  web:
    image: org/app:1.0
    environment:
      - APP_ENV=prod
    read_only: true
    tmpfs:
      - /tmp
    ports:
      - "8080:8080"
```

---

## 18) CI 예시 (Buildx + 캐시)

- Buildx 레이어 캐시로 빌드 시간을 단축한다.
- 취약점 스캔을 파이프라인에 포함한다.

```yaml
# .github/workflows/docker.yml
name: Docker
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push (with cache)
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ghcr.io/org/app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          build-args: |
            APP_VERSION=${{ github.sha }}

      - name: Scan
        uses: aquasecurity/trivy-action@0.24.0
        with:
          image-ref: ghcr.io/org/app:${{ github.sha }}
          severity: 'HIGH,CRITICAL'
          exit-code: '1'
```

---

## 19) 규칙 우선순위

1. **보안/안전**: 비루트, 시크릿 하드코딩 금지, 스캔 필수
2. **재현성**: 고정 태그/버전, 멀티 스테이지, 동일 빌드 파라미터
3. **성능**: 최소 이미지, 캐시 활용, 레이어 최적화
4. **운영성**: 라벨/메타데이터, healthcheck, 로깅/신호처리

---

