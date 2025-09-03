---
lang: en
source_lang: kr
source_sha: d7b546e5eefe136fbb6ab1e8895562ed36fcbac9fe3a9cbaa2e1890fbea5f60b
---
# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` enabled by default, dynamic import splitting recommended.
- Route-level chunking, WOFF2 preferred for fonts/icons.
- Separate loading of fonts/icons during build, automatic generation of preload hints.

## Testing
- **Unit tests** use `jest`.
- **E2E tests** use `cypress`.
- **Test coverage** targets 80% or higher.

## State Management
- **Global state management** uses `Redux Toolkit` or `Zustand`.
- **Local state** uses `useState` and `useReducer` appropriately.

## Performance Optimization
- To prevent **unnecessary rendering**, use `React.memo`, `useMemo`, and `useCallback`.
- For **image optimization**, use libraries like `next/image` or `gatsby-image`.
