---
lang: en
source_lang: kr
source_sha: 37e0b2cfeb94a72ea5e2d54a0cadde4b329d3e689600edb2f6229dc0e3a505e5
---
# Prisma DB Defaults

## Prisma
- Composite key/relationship naming conventions followed
- Migrations applied **after review**
- Down migration path required

## Schema Design
- **Field names** use `camelCase`.
- **Model names** use `PascalCase`.
- **Relationships** are clearly defined, and comments are added when necessary.

## Query Optimization
- Use `include` or `select` appropriately to prevent **N+1 problems**.
- Consider pre-compiled queries or raw queries for **complex queries**.
- Create **indexes** appropriately to improve query performance.
