---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
```md
# Core Rules

## How to behave (global)
- Answers should be in polite Korean, **prioritizing factual accuracy**, and provide a summary of logical steps.
- When generating code, propose it in **the smallest testable and buildable unit** and include a simple usage example.
- In case of conflicts with existing code, present a **3-line summary** of the differences, alternatives, and migration steps first.

## Code Review Principles
- Reviews should be **constructive criticism**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**. Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing it this way has the effect of ~~~."
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget to praise.** Explicitly praise well-done parts to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** should provide clear and concise documentation.
- **Complex logic** or **business rules** should be explained through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main features.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII are prohibited from being printed, copied, or hardcoded.
- Upon detection of a secret pattern: (1) immediately stop and mask (2) safely replace (ENV/secret manager) (3) propose a corrective patch.
- Suspend tasks suspected of external transmission/learning and suggest internal replacement procedures.

## Dependency Management
- **Dependency libraries** should be regularly scanned for security vulnerabilities (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries and find safe, replaceable libraries.
- Check the **license** and use only libraries with licenses suitable for the project.

## Access Control
- Access to **production servers** or **databases** should follow the principle of least privilege.
- **SSH keys** and **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review code for permission changes or sensitive configuration changes through **code reviews**.
# Prisma DB Defaults

## Prisma
- Comply with composite key/relationship naming conventions
- Apply migrations **after review**
- Down migration path is required

## Schema Design
- Use `camelCase` for **field names**.
- Use `PascalCase` for **model names**.
- Define **relationships** clearly and add comments as needed.

## Query Optimization
- Use `include` or `select` appropriately to prevent the **N+1 problem**.
- Consider pre-compiled queries or raw queries for **complex queries**.
- Improve query performance by creating appropriate **indexes**.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile is based on **multi-stage + alpine**. Reflect Buildx and cache strategy (branch scope).
- docker-compose is designed on the premise of `.env.local`. Hard dependency on `.env` is prohibited.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically run for all branches.
- **Builds** must succeed before being merged into the `main` branch.
- **Deployment** is automatically executed after merging into the `main` branch.
- **Environment variables** are managed using the secret function of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed as code and version controlled.
- Define infrastructure using tools such as **Terraform** or **CloudFormation**.
- Review infrastructure changes through **code review**.
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` is the default, dynamic import splitting is recommended.
- Route-level chunking, font/icon WOFF2 preferred.
- Separate loading of fonts/icons during build, automatic generation of preload hints.

## Testing
- **Unit tests** use `jest`.
- **E2E tests** use `cypress`.
- Aim for a **test coverage** of 80% or higher.

## State Management
- **Global state management** uses `Redux Toolkit` or `Zustand`.
- **Local state** uses `useState` and `useReducer` appropriately.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries such as `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker image slimming
"Rewrite with our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply cache strategy & --platform, and suggest a docker inspect size report all at once."

## React chunk optimization
"Font/icon resources are loaded separately, unicons exclude TTF/EOT, WOFF2 preferred. Show before/after bundle size table and timeline highlights."

## Prisma Migration Review
"Summarize the review in 3 stages: whether composite key/relationship naming conventions are followed, down migration path, and risk level (High/Medium/Low)."

## Python 3.13 FastAPI Boilerplate
"Create scaffolding with mypy --strict passing, pydantic v2, no mixing of synchronous/asynchronous code, and router/schema/service layer module separation."

## API documentation generation
"Automatically generate an OpenAPI 3.0 specification document based on the paths and Pydantic models of the FastAPI app, and include Swagger UI settings."

## Code style improvement
"Refactor this Python code to conform to PEP 8 standards. In particular, change variable names, function names, and class names to be clear and descriptive, and remove unnecessary comments."

## Performance analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools, and provide specific suggestions and code modifications to improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, based on `mypy --strict` passing.
- pydantic v2 standard when scaffolding FastAPI.
- Mandatory separation of router/schema/service layer modules.

## Testing
- **Unit tests** use `pytest`.
- **Integration tests** are performed by mocking the actual database or external API.
- Aim for a **test coverage** of 80% or higher.

## Database
- **ORM** uses `SQLAlchemy` 2.0.
- **Migrations** use `Alembic`.
- Efficiently manage database connections using a **connection pool**.

## Security
- Handle authentication using **JWT tokens**.
- Hash **passwords** using `bcrypt`.
- Ensure that only allowed domains can access through **CORS** settings.
# UI/Tailwind Defaults

## Tailwind
- Prioritize the use of the company's `iris` palette tokens. New color suggestions are prohibited; include a token mapping table if necessary.
- Maintain a utility-first approach and comply with naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Comply with **accessibility** so that all users can use it.

## Styling Conventions
- Follow the **BEM** method for **class names**. (e.g., `block__element--modifier`)
- Utilize Tailwind's responsive utilities for **responsive design**.
- Minimize **custom styles** and make the most of basic utilities.
# Project Specific Overrides

## Project Overrides
- This project is a project that defines and manages Cursor Rules itself.
- Therefore, project-specific rules are defined in the .cursorrules/project directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version Control**: The `.cursorrules.md` file is version controlled with Git.
- **Rule Creation Script**: Create rules using the `rules-merge` target in the `Makefile`.
```