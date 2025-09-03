---
lang: en
source_lang: kr
source_sha: 0702b1ed62e8eb41ead7b8df2e76e8a7bbb01446d873d0df637b6b87ddca8f55
---
```md
# Core Rules

## How to behave (global)
- Answers should be in polite Korean, **prioritizing factual accuracy**, and provide a logical step summary.
- When generating code, suggest the **smallest testable and buildable unit** and include simple usage examples.
- In case of conflicts with existing code, present a **3-line summary** of the differences, alternatives, and migration steps first.

## Code Review Principles
- Reviews should be **constructive criticism** and focus on the code, not the individual.
- Clearly explain **"Why"** and **"How"**. Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing it this way has the effect of ~~~."
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget to praise.** Explicitly praise the well-done parts to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** must provide clear and concise documentation.
- **Complex logic** or **business rules** should be explained through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main functions.
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII are prohibited from being output, copied, or hardcoded.
- When a secret pattern is detected: (1) immediately stop and mask (2) provide a safe alternative (ENV/Secret Manager) (3) suggest a corrective patch.
- Suspend any operations suspected of external transmission/learning and suggest internal alternative procedures.

## Dependency Management
- **Dependency libraries** should be regularly scanned for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries and find safe, replaceable alternatives.
- Check the **license** and only use libraries with licenses suitable for the project.

## Access Control
- Access to **production servers** or **databases** should follow the principle of least privilege.
- **SSH keys** or **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review code for permission changes or sensitive configuration changes.
# Prisma DB Defaults

## Prisma
- Adhere to composite key/relationship naming conventions
- Apply migrations **after review**
- Down migration path is required

## Schema Design
- Use `camelCase` for **field names**.
- Use `PascalCase` for **model names**.
- Define **relationships** clearly and add comments when necessary.

## Query Optimization
- Use `include` or `select` appropriately to prevent the **N+1 problem**.
- Consider precompiled queries or raw queries for **complex queries**.
- Improve query performance by creating appropriate **indexes**.
# Docker/DevOps Defaults

## Docker/DevOps
- Dockerfile is **multi-stage + alpine** by default. Reflect Buildx and cache strategy (branch scope).
- docker-compose is designed with `.env.local` as a premise. Prohibit hard dependency on `.env`.
- Maintain image optimization (package removal, compression) and `--platform` notation.

## CI/CD Pipelines
- **Tests** are automatically run for all branches.
- **Builds** must succeed before being merged into the `main` branch.
- **Deployment** is automatically executed after merging into the `main` branch.
- **Environment variables** are managed using the secret features of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed as code and version-controlled.
- Define infrastructure using tools like **Terraform** or **CloudFormation**.
- Review infrastructure changes through **code review**.
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` by default, dynamic import splitting recommended.
- Route-level chunking, font/icon WOFF2 preferred.
- Separate loading of fonts/icons during build, automatic generation of preload hints.

## Testing
- Use `jest` for **unit tests**.
- Use `cypress` for **E2E tests**.
- Aim for a **test coverage** of 80% or more.

## State Management
- Use `Redux Toolkit` or `Zustand` for **global state management**.
- Use `useState` and `useReducer` appropriately for **local state**.

## Performance Optimization
- Use `React.memo`, `useMemo`, and `useCallback` to prevent **unnecessary rendering**.
- Use libraries like `next/image` or `gatsby-image` for **image optimization**.
# Prompt Recipes

## Docker image optimization
"Rewrite with our standard Dockerfile template (multi-stage + alpine), remove unnecessary packages, apply cache strategy and --platform, and suggest a docker inspect size report all at once."

## React chunk optimization
"Separate loading of font/icon resources, exclude TTF/EOT for unicons, WOFF2 preferred. Show the before/after bundle size table and timeline highlights."

## Prisma migration review
"Summarize the review in three levels of risk (High/Medium/Low), checking compliance with composite key/relationship naming conventions and down migration path."

## Python 3.13 FastAPI boilerplate
"Generate scaffolding with mypy --strict passing, pydantic v2, no synchronous/asynchronous mixing, and separate router/schema/service layer modules."

## API documentation generation
"Automatically generate an OpenAPI 3.0 specification document based on the paths and Pydantic models of the FastAPI app, and include Swagger UI settings."

## Code style improvement
"Refactor this Python code to conform to the PEP 8 standard. In particular, change variable names, function names, and class names to be clear and descriptive, and remove unnecessary comments."

## Performance analysis
"Analyze the bottlenecks of this Node.js Express app using profiling tools and provide specific suggestions and code modifications to improve performance."
# Python/FastAPI Defaults

## Python/FastAPI
- Python 3.13, type hints required, `mypy --strict` pass criteria.
- pydantic v2 standard for FastAPI scaffolding.
- Enforce separation of router/schema/service layer modules.

## Testing
- Use `pytest` for **unit tests**.
- **Integration tests** should mock real databases or external APIs for testing.
- Aim for a **test coverage** of 80% or more.

## Database
- Use `SQLAlchemy` 2.0 for **ORM**.
- Use `Alembic` for **migrations**.
- Manage database connections efficiently using **connection pools**.

## Security
- Use **JWT tokens** to handle authentication.
- Hash **passwords** using `bcrypt`.
- Allow access only to permitted domains through **CORS** settings.
# UI/Tailwind Defaults

## Tailwind
- Use the company's `iris` palette tokens first. Do not suggest new colors, and include a token mapping table if necessary.
- Maintain a utility-first approach, and adhere to naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Comply with **accessibility** standards to ensure that all users can use the components.

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
- **Version control**: The `.cursorrules.md` file is version-controlled with Git.
- **Rule generation script**: Use the `rules-merge` target in the `Makefile` to generate the rules.
```