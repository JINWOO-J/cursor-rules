# Docker/DevOps Defaults

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
- **코드 리뷰**를 통해 인프라 변경 사항을 검토합니다.