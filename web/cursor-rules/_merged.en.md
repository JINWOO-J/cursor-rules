---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
```md
# Core Rules

## How to behave (global)
- Answers should be in polite Korean, **prioritizing factual accuracy**, and provide a summary of logical steps.
- When generating code, suggest it in **the smallest testable and buildable units**, including simple usage examples.
- If there are conflicts with existing code, present a **3-line summary** of the differences, alternatives, and migration steps first.

## Code Review Principles
- Reviews should be **constructive criticism**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**. Don't just say "Do it this way," but explain "The reason is ~~~, and doing it this way has the effect of ~~~."
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget to praise.** Explicitly praise the well-done parts to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** should provide clear and concise documentation.
- **Complex logic** or **business rules** should be explained through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main functions.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII must not be printed, copied, or hardcoded.
- When a secret pattern is detected: (1) Immediately stop and mask (2) Secure replacement (ENV/secret manager) (3) Suggest corrective patch.
- Suspend any operation that is presumed to involve external transmission/learning and suggest an internal replacement procedure.

## Dependency Management
- Regularly scan **dependency libraries** for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **old or unsupported** libraries and find safe, replaceable libraries.
- Check the **license** and only use libraries with licenses suitable for the project.

## Access Control
- Access to **production servers** or **databases** should follow the principle of least privilege.
- **SSH keys** or **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review code for permission changes or sensitive configuration changes through **code review**.
# Prisma DB Defaults

## Prisma
- Comply with composite key/relationship naming conventions
- Apply migrations **after review**
- Down migration path required

## Schema Design
- Use `camelCase` for **field names**.
- Use `PascalCase` for **model names**.
- Define **relationships** clearly and add comments when necessary.

## Query Optimization
- Use `include` or `select` appropriately to prevent **N+1 problems**.
- Consider precompiled queries or raw queries for **complex queries**.
- Create **indexes** appropriately to improve query performance.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile should default to **multi-stage + alpine**. Reflect Buildx, and cache strategies (branch scope).
- docker-compose should be designed with `.env.local` as a prerequisite. No hard dependency on `.env`.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically run for all branches.
- **Builds** must succeed before being merged into the `main` branch.
- **Deployment** is automatically executed after being merged into the `main` branch.
- **Environment variables** are managed using the secret features of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed as code and version controlled.
- Define infrastructure using tools such as **Terraform** or **CloudFormation**.
- Review infrastructure changes through **code review**.
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` default, dynamic import splitting recommended.
- Route-level chunking, font/icon WOFF2 preferred.
- Separate font/icon loading during build, automatic generation of preload hints.

## Testing
- **Unit tests** use `jest`.
- **E2E tests** use `cypress`.
- **Test coverage** aims for 80% or higher.

## State Management
- **Global state management** uses `Redux Toolkit` or `Zustand`.
- Use `useState` and `useReducer` appropriately for **local state**.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries such as `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker image slimming
"Rewrite to our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply cache strategies and --platform, and provide a Docker inspect size report all at once."

## React chunk optimization
"Font/icon resources are loaded separately, unicons exclude TTF/EOT, WOFF2 is preferred. Show before/after bundle size table and timeline highlights."

## Prisma migration review
"Summarize the review in three levels of risk (High/Medium/Low), including whether composite key/relationship naming conventions are followed and the down migration path."

## Python 3.13 FastAPI boilerplate
"mypy --strict pass, pydantic v2, no synchronous/asynchronous mixing, router/schema/service layer module separation scaffolding."

## API documentation generation
"Automatically generate an OpenAPI 3.0 spec document based on the paths and Pydantic models of the FastAPI app, and include Swagger UI settings."

## Code style improvement
"Refactor this Python code to conform to PEP 8 standards. In particular, change variable names, function names, and class names to be clear and descriptive, and remove unnecessary comments."

## Performance analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools, and provide specific suggestions and code modifications to improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, `mypy --strict` pass as standard.
- pydantic v2 standard when scaffolding FastAPI.
- Router/schema/service layer module separation enforced.

## Testing
- **Unit tests** use `pytest`.
- **Integration tests** mock real databases or external APIs for testing.
- **Test coverage** aims for 80% or higher.

## Database
- **ORM** uses `SQLAlchemy` 2.0.
- **Migration** uses `Alembic`.
- Efficiently manage database connections using **connection pooling**.

## Security
- Handle authentication using **JWT tokens**.
- Hash **passwords** using `bcrypt`.
- Ensure that only allowed domains can access through **CORS** settings.
# UI/Tailwind Defaults

## Tailwind
- Prioritize the use of the company's `iris` palette tokens. Do not suggest new colors; include a token mapping table if necessary.
- Maintain a utility-first approach and comply with naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Adhere to **accessibility** so that all users can use it.

## Styling Conventions
- Follow the `BEM` method for **class names**. (e.g., `block__element--modifier`)
- Use Tailwind's responsive utilities for **responsive design**.
- Minimize **custom styles** and utilize basic utilities as much as possible.
# Project Specific Overrides

## Project Overrides
- This project is a project that defines and manages Cursor Rules itself.
- Therefore, project-specific rules are defined in the .cursorrules/project directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version control**: The `.cursorrules.md` file is version-controlled with Git.
- **Rule generation script**: Use the `rules-merge` target in the `Makefile` to generate rules.
```