---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
```md
# Core Rules

## How to behave (global)
- Answers should be in polite Korean, **prioritizing accuracy**, and provide a summary of logical steps.
- When generating code, suggest it in the **smallest testable and buildable units**, including simple usage examples.
- When conflicts with existing code arise, first present a **3-line summary** of the differences, alternatives, and migration steps.

## Code Review Principles
- Reviews should be **constructive criticism**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**. Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing it this way has the effect of ~~~."
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget to praise.** Explicitly praise the good parts to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** must provide clear and concise documentation.
- Explain **complex logic** or **business rules** through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main features.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII are prohibited from being output, copied, or hardcoded.
- When a secret pattern is detected: (1) Immediately stop and mask (2) Safe replacement (ENV/secret manager) (3) Suggest correction patch.
- Suspend operations suspected of external transmission/learning and suggest internal replacement procedures.

## Dependency Management
- **Dependency libraries** are regularly scanned for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries, and find alternative safe libraries.
- Check the **license** and use only libraries with licenses suitable for the project.

## Access Control
- Access to **operational servers** or **databases** follows the principle of least privilege.
- **SSH keys** or **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review code for permission changes or sensitive configuration changes.
# Prisma DB Defaults

## Prisma
- Adhere to composite key/relationship naming conventions
- Apply migrations **after review**
- Down migration path required

## Schema Design
- Use `camelCase` for **field names**.
- Use `PascalCase` for **model names**.
- Define **relationships** clearly and add comments if necessary.

## Query Optimization
- Use `include` or `select` appropriately to prevent the **N+1 problem**.
- Consider precompiled queries or raw queries for **complex queries**.
- Create **indexes** appropriately to improve query performance.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile is **multi-stage + alpine** by default. Reflect Buildx and caching strategies (branch scope).
- docker-compose is designed with `.env.local` as a premise. Prohibit hard dependency on `.env`.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically executed for all branches.
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
- Separate loading of fonts/icons during build, automatic generation of preload hints.

## Testing
- Use `jest` for **unit tests**.
- Use `cypress` for **E2E tests**.
- Aim for a **test coverage** of 80% or higher.

## State Management
- Use `Redux Toolkit` or `Zustand` for **global state management**.
- Use `useState` and `useReducer` appropriately for **local state**.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries like `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker image slimming
"Rewrite with our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply cache strategy and --platform, and suggest a docker inspect size report all at once."

## React chunk optimization
"Font/icon resources should be loaded separately, unicons should exclude TTF/EOT, and WOFF2 should be preferred. Show before/after bundle size table and timeline highlights."

## Prisma migration review
"Summarize the review in 3 stages (High/Medium/Low) for compliance with composite key/relationship naming conventions, down migration path, and risk level."

## Python 3.13 FastAPI boilerplate
"Pass mypy --strict, pydantic v2, prohibit mixing synchronous/asynchronous, and create router/schema/service layer module separation scaffolding."

## API documentation generation
"Automatically generate OpenAPI 3.0 spec documentation based on the paths and Pydantic models of the FastAPI app, and include Swagger UI settings."

## Code style improvement
"Refactor this Python code to conform to PEP 8 standards. In particular, change variable names, function names, and class names to be clear and descriptive, and remove unnecessary comments."

## Performance analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools, and provide concrete suggestions and code modifications to improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, based on `mypy --strict` passing.
- pydantic v2 standard when FastAPI scaffolding.
- Force separation of router/schema/service layer modules.

## Testing
- Use `pytest` for **unit tests**.
- **Integration tests** mock real databases or external APIs for testing.
- Aim for a **test coverage** of 80% or higher.

## Database
- Use `SQLAlchemy` 2.0 for **ORM**.
- Use `Alembic` for **migrations**.
- Manage database connections efficiently using a **connection pool**.

## Security
- Use **JWT tokens** to handle authentication.
- Hash **passwords** using `bcrypt`.
- Allow access only to permitted domains through **CORS** settings.
# UI/Tailwind Defaults

## Tailwind
- Prioritize the use of the company's `iris` palette tokens. Prohibit suggesting new colors, and include a token mapping table if necessary.
- Maintain a utility-first approach and adhere to naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **Props** clearly and intuitively.
- Comply with **Accessibility** so that all users can use it.

## Styling Conventions
- Follow the `BEM` method for **class names**. (e.g., `block__element--modifier`)
- Utilize Tailwind's responsive utilities for **responsive design**.
- Minimize **custom styles** and utilize basic utilities as much as possible.
# Project Specific Overrides

## Project Overrides
- This project is a project that defines and manages Cursor Rules themselves.
- Therefore, project-specific rules are defined in the .cursorrules/project directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version control**: The `.cursorrules.md` file is version controlled with Git.
- **Rule generation script**: Generate rules using the `rules-merge` target in `Makefile`.
```