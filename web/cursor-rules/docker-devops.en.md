---
lang: en
source_lang: kr
source_sha: ab9aae917eeaf1cd5858469688e8d98de5453b3413c1f62548376c02c0759fb4
---
# Docker and DevOps Defaults

## Docker and DevOps
- Dockerfiles use a **multi-stage + alpine** base. Buildx and a branch-scoped caching strategy are implemented.
- `docker-compose` is designed to use `.env.local`. Hard dependencies on `.env` are prohibited.
- Image optimization (package removal, compression) and `--platform` specification are maintained.

## CI/CD Pipelines
- **Tests** are automatically run for all branches.
- **Builds** must succeed before merging into the `main` branch.
- **Deployment** is automatically triggered after merging into the `main` branch.
- **Environment variables** are managed using the secret management features of the CI/CD platform.

## Infrastructure as Code (IaC)
- **Infrastructure** is managed and version-controlled as code.
- Tools like **Terraform** or **CloudFormation** are used to define infrastructure.
- **Code reviews** are conducted for infrastructure changes.
