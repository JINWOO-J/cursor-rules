# UI/Tailwind Defaults

## Tailwind
- 사내 `iris` 팔레트 토큰 우선 사용. 새 색상 제안 금지, 필요 시 토큰 맵핑 테이블 포함.
- Utility-first 접근법 유지, 컴포넌트 추출 시 네이밍 규칙 준수.

## Component Design Principles
- **재사용성**을 고려하여 컴포넌트를 설계합니다.
- **Props**는 명확하고 직관적으로 정의합니다.
- **접근성**(Accessibility)을 준수하여, 모든 사용자가 사용할 수 있도록 합니다.

## Styling Conventions
- **클래스명**은 `BEM` 방식을 따릅니다. (예: `block__element--modifier`)
- **반응형 디자인**은 Tailwind의 반응형 유틸리티를 활용합니다.
- **커스텀 스타일**은 최소화하고, 기본 유틸리티를 최대한 활용합니다.