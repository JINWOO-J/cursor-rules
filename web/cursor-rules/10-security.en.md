---
lang: en
source_lang: kr
source_sha: bb708c9c15001c9a3c3d6d19c27b8c1cd477b5aaa0f8ddd9912c4ed579a69238
---
# Security & Secrets

## Security & Secrets
- Secrets/tokens/credentials/PII must not be printed, copied, or hardcoded.
- If a secret pattern is detected: (1) Immediately stop and mask (2) Securely replace (ENV/secret manager) (3) Suggest a corrective patch.
- Tasks suspected of external transmission/learning should be put on hold and an internal alternative procedure should be presented.

## Dependency Management
- **Dependency libraries** are regularly scanned for security vulnerabilities. (e.g., `npm audit`, `safety`).
- Avoid using **outdated or unmaintained** libraries and find secure alternatives.
- Check **licenses** and use only libraries with licenses suitable for the project.

## Access Control
- Access to **production servers** or **databases** follows the principle of least privilege.
- **SSH keys** and **API keys** must be managed using secret management tools such as **Vault** or **AWS Secrets Manager**.
- **Code reviews** are used to check for permission changes or sensitive setting changes.
