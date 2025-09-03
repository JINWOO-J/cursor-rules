---
lang: en
source_lang: kr
source_sha: ec64de92130151d37e2045bdeed1995437499674c938b1fda8711b44d579906a
---
---
title: 핵심 규칙
description: 개발 규칙 및 문서 표준
---

# Core Rules

## How to behave (global)
- Responses should be polite Korean, prioritizing **factual accuracy**, and providing a summary of logical steps.
- When generating code, suggest the **minimum testable/buildable unit**, and include a simple usage example.
- In case of conflicts with existing code, present a **three-line summary** of the differences, alternatives, and migration steps.

## Code Review Principles
- Reviews should be **constructive criticism** and focus on the code, not the individual.
- Clearly explain the **"Why"** and **"How"**.  Instead of simply saying "Do it this way," explain "The reason is ~~~, and doing this will have the effect of ~~~".
- Review comments should be **actionable**. Avoid vague or abstract criticisms.
- **Don't forget praise.** Explicitly praise what's done well to foster a positive feedback culture.

## Documentation Standards
- All **public APIs** must have clear and concise documentation.
- Explain **complex logic** or **business rules** through comments.
- **README.md** should clearly describe the project's purpose, installation method, execution method, and main functions.
