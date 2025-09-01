# Node.js/React Defaults

## Node/React/Vite
- Node 22, `eslint + typescript-eslint` 기본, dynamic import 분할 권장.
- route-level 청킹, 폰트/아이콘 WOFF2 우선.
- 빌드 시 폰트/아이콘 분리 로딩, 프리로드 힌트 자동 생성.

## Testing
- **단위 테스트**는 `jest`를 사용합니다.
- **E2E 테스트**는 `cypress`를 사용합니다.
- **테스트 커버리지**는 80% 이상을 목표로 합니다.

## State Management
- **전역 상태 관리**는 `Redux Toolkit` 또는 `Zustand`를 사용합니다.
- **로컬 상태**는 `useState`와 `useReducer`를 적절히 사용합니다.

## Performance Optimization
- **불필요한 렌더링**을 방지하기 위해 `React.memo`, `useMemo`, `useCallback`을 사용합니다.
- **이미지 최적화**를 위해 `next/image` 또는 `gatsby-image` 같은 라이브러리를 사용합니다.