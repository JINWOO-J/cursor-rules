# Python/FastAPI Defaults

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
- **CORS** 설정을 통해 허용된 도메인만 접근할 수 있도록 합니다.