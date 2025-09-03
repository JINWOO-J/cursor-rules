---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
```md
# Core Rules

## How to behave (global)
- Answers should be in polite Korean, **prioritizing factual accuracy**, and provide a logical step-by-step summary.
- When generating code, suggest it in **the smallest testable and buildable units**, including simple usage examples.
- If there are conflicts with existing code, present the differences, alternatives, and migration steps in a **3-line summary** first.

## Code Review Principles
- Reviews should be **constructive criticism**, focusing on the code, not the individual.
- Clearly explain **"Why"** and **"How"**. Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing it this way has the effect of ~~~."
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget to praise.** Explicitly praise good parts to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** must provide clear and concise documentation.
- **Complex logic** or **business rules** should be explained through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main functions.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII are prohibited from being printed, copied, or hardcoded.
- When a secret pattern is detected: (1) Immediately stop and mask (2) Secure replacement (ENV/secret manager) (3) Suggest a corrective patch.
- Suspend tasks that are presumed to be externally transmitted/learned and suggest internal replacement procedures.

## Dependency Management
- **Dependency libraries** should be scanned regularly for security vulnerabilities (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries, and find safe, replaceable libraries.
- Check the **license** and use only libraries with licenses suitable for the project.

## Access Control
- Access to **operational servers** or **databases** should follow the principle of least privilege.
- **SSH keys** and **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review code to check for permission changes or sensitive configuration changes.
# Prisma DB Defaults

## Prisma
- Adhere to composite key/relationship naming conventions
- Apply migrations **after review**
- Down migration path required

## Schema Design
- **Field names** should use `camelCase`.
- **Model names** should use `PascalCase`.
- **Relationships** should be clearly defined, with comments added as needed.

## Query Optimization
- Use `include` or `select` appropriately to prevent the **N+1 problem**.
- Consider precompiled or raw queries for **complex queries**.
- Improve query performance by creating appropriate **indexes**.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile defaults to **multi-stage + alpine**. Reflect Buildx, and cache strategies (branch scope).
- docker-compose is designed with `.env.local` as a premise. Prohibit hard dependency on `.env`.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically run on all branches.
- **Builds** must succeed before being merged into the `main` branch.
- **Deployment** is automatically executed after merging into the `main` branch.
- **Environment variables** are managed using the secret features of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed as code and version controlled.
- Define infrastructure using tools like **Terraform** or **CloudFormation**.
- Review infrastructure changes through **code reviews**.
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` default, dynamic import splitting recommended.
- Route-level chunking, font/icon WOFF2 preferred.
- Separate loading of fonts/icons during build, and automatic generation of preload hints.

## Testing
- **Unit tests** use `jest`.
- **E2E tests** use `cypress`.
- **Test coverage** aims for 80% or higher.

## State Management
- **Global state management** uses `Redux Toolkit` or `Zustand`.
- **Local state** uses `useState` and `useReducer` appropriately.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries such as `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker image optimization
"Rewrite with our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply cache strategy & --platform, and suggest a docker inspect size report all at once."

## React chunk optimization
"Font/icon resources are loaded separately, unicons excludes TTF/EOT, WOFF2 preferred. Show before/after bundle size chart and timeline highlights."

## Prisma Migration Review
"Summarize the review in 3 stages: whether composite key/relationship naming conventions are followed, down migration path, and risk level (High/Medium/Low)."

## Python 3.13 FastAPI Boilerplate
"Passes mypy --strict, pydantic v2, prohibits mixing synchronous/asynchronous code, and generates router/schema/service layer module separation scaffolding."

## API documentation generation
"Automatically generate an OpenAPI 3.0 specification document based on the paths and Pydantic models of the FastAPI app, and include Swagger UI settings."

## Code style improvement
"Refactor this Python code to conform to PEP 8 standards. In particular, change variable names, function names, and class names to be clear and descriptive, and remove unnecessary comments."

## Performance analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools, and provide specific suggestions and code modifications that can improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, based on `mypy --strict` passing.
- pydantic v2 standard when scaffolding FastAPI.
- Force router/schema/service layer module separation.

## Testing
- **Unit tests** use `pytest`.
- **Integration tests** test by mocking real databases or external APIs.
- **Test coverage** aims for 80% or higher.

## Database
- **ORM** uses `SQLAlchemy` 2.0.
- **Migrations** use `Alembic`.
- Efficiently manage database connections using **connection pooling**.

## Security
- Handle authentication using **JWT tokens**.
- Hash **passwords** using `bcrypt`.
- Allow only permitted domains to access through **CORS** settings.
# UI/Tailwind Defaults

## Tailwind
- Use the company's `iris` palette tokens first. Prohibit suggesting new colors, include a token mapping table if necessary.
- Maintain utility-first approach, and adhere to naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Comply with **accessibility** standards so that all users can use it.

## Styling Conventions
- **Class names** follow the `BEM` method. (e.g., `block__element--modifier`)
- **Responsive design** utilizes Tailwind's responsive utilities.
- Minimize **custom styles** and utilize basic utilities as much as possible.
# Project Specific Overrides

## Project Overrides
- This project is a project that defines and manages Cursor Rules itself.
- Therefore, project-specific rules are defined in the .cursorrules/project directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version control**: The `.cursorrules.md` file is version controlled with Git.
- **Rule generation script**: Rules are generated using the `rules-merge` target in the `Makefile`.
```