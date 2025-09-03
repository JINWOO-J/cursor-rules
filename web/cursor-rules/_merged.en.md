---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
```md
# Core Rules

## How to behave (global)
- Answers should be in polite Korean, **prioritizing accuracy**, and provide a summary of logical steps.
- When generating code, suggest in **testable and buildable minimum units**, including simple usage examples.
- In case of conflicts with existing code, present a **3-line summary** of the differences, alternatives, and migration steps first.

## Code Review Principles
- Reviews should be **constructive criticism**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**. Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing it this way has the effect of ~~~."
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget to praise.** Explicitly praise well-done parts to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** should provide clear and concise documentation.
- Explain **complex logic** or **business rules** through comments.
- **README.md** should clearly describe the project's purpose, installation instructions, execution methods, and main features.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII are prohibited from being printed, copied, or hardcoded.
- Upon detecting a secret pattern: (1) Immediately stop and mask (2) Secure replacement (ENV/Secret Manager) (3) Propose corrective patch.
- Suspend operations presumed to involve external transmission/learning and present an internal replacement procedure.

## Dependency Management
- **Dependency libraries** should be regularly scanned for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries and find alternative, secure libraries.
- Check the **license** and use only libraries with licenses suitable for the project.

## Access Control
- Access to **operation servers** or **databases** should follow the principle of least privilege.
- **SSH keys** or **API keys** must be managed using secret management tools like **Vault** or **AWS Secrets Manager**.
- Review code for permission changes or sensitive configuration changes through **code reviews**.
# Prisma DB Defaults

## Prisma
- Adhere to composite key/relationship naming conventions
- Apply migrations **after review**
- Down migration path required

## Schema Design
- Use `camelCase` for **field names**.
- Use `PascalCase` for **model names**.
- Define **relationships** clearly and add comments as needed.

## Query Optimization
- Use `include` or `select` appropriately to prevent **N+1 problems**.
- Consider precompiled queries or raw queries for **complex queries**.
- Create **indexes** appropriately to improve query performance.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile should be **multi-stage + alpine** by default. Reflect Buildx and caching strategy (branch scope).
- docker-compose should be designed with `.env.local` as a prerequisite. Prohibit hard dependency on `.env`.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically run for all branches.
- **Builds** must succeed before being merged into the `main` branch.
- **Deployment** is automatically executed after merging into the `main` branch.
- **Environment variables** are managed using the secret features of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed as code and version-controlled.
- Define infrastructure using tools like **Terraform** or **CloudFormation**.
- Review infrastructure changes through **code reviews**.
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` by default, dynamic import splitting recommended.
- Route-level chunking, font/icon WOFF2 preferred.
- Separate loading of fonts/icons during build, automatic generation of preload hints.

## Testing
- **Unit tests** use `jest`.
- **E2E tests** use `cypress`.
- **Test coverage** should aim for 80% or higher.

## State Management
- **Global state management** uses `Redux Toolkit` or `Zustand`.
- **Local state** uses `useState` and `useReducer` appropriately.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries like `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker image optimization
"Rewrite with our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply caching strategy and --platform, and provide a docker inspect size report all at once."

## React chunk optimization
"Font/icon resources should be loaded separately, unicons should exclude TTF/EOT, WOFF2 preferred. Show before/after bundle size chart and timeline highlights."

## Prisma migration review
"Summarize the review in 3 levels (High/Medium/Low) regarding compliance with composite key/relationship naming conventions, down migration path."

## Python 3.13 FastAPI boilerplate
"Pass mypy --strict, pydantic v2, no mixing of synchronous/asynchronous code, create scaffolding for router/schema/service layer module separation."

## API documentation generation
"Automatically generate an OpenAPI 3.0 specification document based on the paths and Pydantic models of the FastAPI app, and include Swagger UI settings."

## Code style improvement
"Refactor this Python code to comply with PEP 8 standards. In particular, change variable names, function names, and class names to be clear and descriptive, and remove unnecessary comments."

## Performance analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools and provide concrete suggestions and code modifications to improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, based on `mypy --strict` pass.
- pydantic v2 standard when scaffolding FastAPI.
- Forced separation of router/schema/service layer modules.

## Testing
- **Unit tests** use `pytest`.
- **Integration tests** test by mocking real databases or external APIs.
- **Test coverage** should aim for 80% or higher.

## Database
- **ORM** uses `SQLAlchemy` 2.0.
- **Migration** uses `Alembic`.
- Efficiently manage database connections using **connection pools**.

## Security
- Handle authentication using **JWT tokens**.
- Hash **passwords** using `bcrypt`.
- Ensure that only allowed domains can access through **CORS** settings.
# UI/Tailwind Defaults

## Tailwind
- Prioritize the use of the company's `iris` palette tokens. Do not suggest new colors; include a token mapping table if necessary.
- Maintain the utility-first approach and adhere to naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Adhere to **accessibility** standards so that all users can use it.

## Styling Conventions
- Follow the **BEM** method for **class names**. (e.g., `block__element--modifier`)
- Utilize Tailwind's responsive utilities for **responsive design**.
- Minimize **custom styles** and maximize the use of basic utilities.
# Project Specific Overrides

## Project Overrides
- This project is a project that defines and manages Cursor Rules itself.
- Therefore, project-specific rules are defined in the .cursorrules/project directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version Control**: The `.cursorrules.md` file is version controlled with Git.
- **Rule Generation Script**: Use the `rules-merge` target in the `Makefile` to generate rules.
```