---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
# Core Rules

## How to behave (global)
- Responses should be polite Korean, prioritizing **factual accuracy**, and providing a summary of logical steps.
- When generating code, suggest the **minimum testable/buildable unit**, and include a simple usage example.
- In case of conflicts with existing code, first present a **three-line summary** of the differences, alternatives, and migration steps.

## Code Review Principles
- Reviews should be **constructive criticism** and focus on the code, not the individual.
- Clearly explain the **"Why"** and **"How"**.  Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing this will have the effect of ~~~".
- Review comments should be **actionable**. Avoid vague or abstract points.
- **Don't forget praise.** Explicitly praise what's done well to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** must have clear and concise documentation.
- Explain **complex logic** or **business rules** through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main features.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII are forbidden from being printed, copied, or hardcoded.
- When a secret pattern is detected: (1) Immediately stop/mask (2) Safe replacement (ENV/secret manager) (3) Suggest a correction patch.
- Tasks presumed to involve external transmission/learning should be put on hold and an internal alternative procedure should be presented.

## Dependency Management
- Regularly perform security vulnerability scans on **dependency libraries**. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries, and find safe alternatives.
- Check **licenses** and only use libraries with licenses suitable for the project.

## Access Control
- Access to **production servers** or **databases** follows the principle of least privilege.
- **SSH keys** and **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review permissions changes and sensitive setting changes through **code review**.
# Prisma DB Defaults

## Prisma
- Adhere to composite key/relationship naming conventions.
- Apply migrations **after review**.
- Down migration paths are required.

## Schema Design
- Use `camelCase` for **field names**.
- Use `PascalCase` for **model names**.
- Clearly define **relationships**, and add comments if necessary.

## Query Optimization
- Use `include` or `select` appropriately to prevent the **N+1 problem**.
- Consider pre-compiled queries or raw queries for **complex queries**.
- Create **indexes** appropriately to improve query performance.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfiles should be based on **multi-stage + alpine**.  Reflect Buildx and caching strategies (branch scope).
- docker-compose should be designed assuming `.env.local`.  Avoid hard dependencies on `.env`.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically run for all branches.
- **Builds** must succeed before merging into the `main` branch.
- **Deployment** is automatically triggered after merging into the `main` branch.
- **Environment variables** are managed using the secret features of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed and version-controlled as code.
- Use tools such as **Terraform** or **CloudFormation** to define the infrastructure.
- Review infrastructure changes through **code review**.
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` by default, dynamic import splitting recommended.
- Route-level chunking, prioritize WOFF2 for fonts/icons.
- Separate loading of fonts/icons during build, automatic generation of preload hints.

## Testing
- Use `jest` for **unit tests**.
- Use `cypress` for **E2E tests**.
- Aim for over 80% **test coverage**.

## State Management
- Use `Redux Toolkit` or `Zustand` for **global state management**.
- Use `useState` and `useReducer` appropriately for **local state**.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries like `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker 이미지 경량화
"Rewrite using our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply caching strategies and `--platform`, and provide a docker inspect size report."

## React 청크 최적화
"Separate loading for font/icon resources, exclude unicons TTF/EOT, prioritize WOFF2. Show a table comparing before/after bundle sizes and highlight the timeline."

## Prisma 마이그레이션 검토
"Review summary in three levels of risk (High/Medium/Low): Adherence to composite key/relationship naming conventions, down migration paths."

## Python 3.13 FastAPI 보일러플레이트
"Generate scaffolding with `mypy --strict` passing, pydantic v2, prohibition of synchronous/asynchronous mixing, and separate modules for router/schema/service layers."

## API 문서 생성
"Automatically generate OpenAPI 3.0 specification documentation based on the FastAPI app's paths and Pydantic models, including Swagger UI settings."

## 코드 스타일 개선
"Refactor this Python code to conform to PEP 8 standards.  In particular, change variable, function, and class names to be clear and descriptive, and remove unnecessary comments."

## 성능 분석
"Analyze the bottlenecks of this Node.js Express app using profiling tools, and provide concrete suggestions and code modifications to improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, `mypy --strict` passing standard.
- FastAPI scaffolding based on pydantic v2.
- Enforce separation of router/schema/service layer modules.

## Testing
- Use `pytest` for **unit tests**.
- **Integration tests** test using mocks for actual databases or external APIs.
- Aim for over 80% **test coverage**.

## Database
- Use `SQLAlchemy` 2.0 for **ORM**.
- Use `Alembic` for **migrations**.
- Use a **connection pool** to efficiently manage database connections.

## Security
- Use **JWT tokens** for authentication.
- Hash **passwords** using `bcrypt`.
- Use **CORS** settings to allow access only from permitted domains.
# UI/Tailwind Defaults

## Tailwind
- Prioritize the use of in-house `iris` palette tokens.  Prohibition of new color suggestions, include a token mapping table if necessary.
- Maintain a utility-first approach, adhere to naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Adhere to **accessibility** so that all users can use them.

## Styling Conventions
- Use the **BEM** method for **class names**. (e.g., `block__element--modifier`)
- Use Tailwind's responsive utilities for **responsive design**.
- Minimize **custom styles** and maximize the use of default utilities.
# Project Specific Overrides

## Project Overrides
- This project defines and manages Cursor Rules themselves.
- Therefore, project-specific rules are defined in the `.cursorrules/project` directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version Control**: The `.cursorrules.md` file is version-controlled with Git.
- **Rule Generation Script**: Use the `rules-merge` target in `Makefile` to generate rules.

