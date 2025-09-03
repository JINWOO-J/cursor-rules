---
lang: en
source_lang: kr
source_sha: f741ab7a1397d0c1a55cd3adcc8cb9f3f30720b2f8b638e07847abddd0f407f8
---
# UI/Tailwind Defaults

## Tailwind
- Use internal `iris` palette tokens first.  Proposing new colors is prohibited; include a token mapping table if necessary.
- Maintain a utility-first approach. Adhere to naming conventions when extracting components.

## Component Design Principles
- Design components with **reusability** in mind.
- Define **props** clearly and intuitively.
- Ensure **accessibility** so that all users can use them.

## Styling Conventions
- **Class names** follow the `BEM` convention. (e.g., `block__element--modifier`)
- Use Tailwind's responsive utilities for **responsive design**.
- Minimize **custom styles** and maximize the use of default utilities.
