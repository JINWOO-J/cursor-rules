---
lang: en
source_lang: kr
source_sha: bb708c9c15001c9a3c3d6d19c27b8c1cd477b5aaa0f8ddd9912c4ed579a69238
---
```markdown
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII must not be printed, copied, or hardcoded.
- When a secret pattern is detected: (1) immediately stop & mask (2) secure replacement (ENV/secret manager) (3) suggest a corrective patch.
- Suspend tasks that are presumed to involve external transmission/learning, and propose an internal replacement procedure.

## Dependency Management
- Regularly scan **dependency libraries** for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries, and find safe, replaceable libraries.
- Check the **license** and only use libraries with licenses suitable for the project.

## Access Control
- Access to **operation servers** or **databases** should follow the principle of least privilege.
- **SSH keys** or **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review **code reviews** for permission changes or sensitive configuration changes.
```