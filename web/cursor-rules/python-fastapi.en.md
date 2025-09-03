---
lang: en
source_lang: kr
source_sha: 7860f5ed58b98eb1254adddb12960ea627f6c19e0d5b1859daa9411bca87ac55
---
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, must pass `mypy --strict`.
- FastAPI scaffolding based on pydantic v2.
- Strict separation of router/schema/service layer modules.

## Testing
- **Unit tests** use `pytest`.
- **Integration tests** mock real databases and external APIs.
- Aim for **test coverage** of 80% or more.

## Database
- **ORM** uses `SQLAlchemy` 2.0.
- **Migrations** use `Alembic`.
- Uses a **connection pool** for efficient database connection management.

## Security
- Uses **JWT tokens** for authentication.
- **Passwords** are hashed using `bcrypt`.
- **CORS** settings restrict access to allowed domains only.
