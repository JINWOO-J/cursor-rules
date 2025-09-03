---
lang: en
source_lang: kr
source_sha: 008809e669d25471ab2a4146e164960ad382298243a3469f347d298bfd80185d
---
```markdown
# Project Specific Overrides

## Project Overrides
- This project is for defining and managing Cursor Rules themselves.
- Therefore, project-specific rules are defined in the `.cursorrules/project` directory.

## Specific to this project
- **Documentation**: All rule changes must be reflected in `PRD.md` and `README.md`.
- **Version Control**: The `.cursorrules.md` file is version controlled with Git.
- **Rule Generation Script**: Use the `rules-merge` target in the `Makefile` to generate rules.
```