---
lang: en
source_lang: kr
source_sha: bb708c9c15001c9a3c3d6d19c27b8c1cd477b5aaa0f8ddd9912c4ed579a69238
---
```markdown
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII must not be output, copied, or hardcoded.
- Upon detection of secret patterns: (1) Immediately stop and mask (2) Safe replacement (ENV/secret manager) (3) Suggest corrective patch.
- Suspend tasks presumed to involve external transmission/learning and suggest internal replacement procedures.

## Dependency Management
- Regularly scan **dependency libraries** for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries and find safe, replaceable alternatives.
- Check **licenses** to ensure that only libraries with licenses suitable for the project are used.

## Access Control
- Follow the principle of least privilege for access to **operation servers** or **databases**.
- **SSH keys** or **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review **code reviews** for permission changes or sensitive configuration changes.
```