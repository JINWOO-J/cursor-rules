---
lang: en
source_lang: kr
source_sha: bb708c9c15001c9a3c3d6d19c27b8c1cd477b5aaa0f8ddd9912c4ed579a69238
---
```markdown
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII must not be output, copied, or hardcoded.
- When a secret pattern is detected: (1) immediately stop and mask (2) safe replacement (ENV/secret manager) (3) propose a corrective patch.
- Suspend operations presumed to involve external transmission/learning and propose an internal replacement procedure.

## Dependency Management
- Regularly scan **dependency libraries** for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries, and find safe, replaceable libraries.
- Check the **license** and use only libraries with licenses suitable for the project.

## Access Control
- Access to **production servers** or **databases** should follow the principle of least privilege.
- **SSH keys** or **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- Review **code reviews** for permission changes or sensitive configuration changes.
```