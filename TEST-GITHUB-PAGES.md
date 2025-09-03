# 🧪 GitHub Pages 로컬 테스트 가이드

GitHub Pages 배포 전에 로컬에서 경로 문제를 미리 테스트할 수 있는 방법입니다.

## 🚀 빠른 시작

### 1. 테스트 서버 실행
```bash
# GitHub Pages 환경 시뮬레이션 서버 시작
node test-github-pages.js
```

### 2. 브라우저에서 테스트
```
http://localhost:3000/cursor-rules/
```

실제 GitHub Pages와 동일한 `/cursor-rules/` 경로에서 서빙됩니다.

## 🔍 테스트 체크리스트

### ✅ 기본 기능 테스트
- [ ] 페이지 로딩 성공
- [ ] 버전 정보 표시
- [ ] 프리셋 선택기 초기화 (6개 프리셋)

### ✅ 경로 문제 확인
개발자 도구 Console에서 다음 로그 확인:

**정상적인 경우:**
```
Detected base path: ./ for location: /cursor-rules/
GitHub Pages project site: true
프리셋 선택기 초기화 완료: 6 개 프리셋
GitHub Pages path fix: cursor-rules/common/10-security.kr.md -> common/10-security.kr.md
urlFor: cursor-rules/common/10-security.kr.md -> ./common/10-security.kr.md
```

**❌ 문제가 있는 경우:**
```
Path adjusted: cursor-rules/common/10-security.kr.md -> cursor-rules/cursor-rules/common/10-security.kr.md
GET http://localhost:3000/cursor-rules/cursor-rules/cursor-rules/common/10-security.kr.md 404 (Not Found)
```

### ✅ 프리셋 로딩 테스트
1. "🔒 필수 기본 규칙" → "보안 & Git 기본팩" 선택
2. 자동으로 2개 규칙 카드 생성 확인
3. 각 카드에 KR/EN 내용 로딩 확인

### ✅ 파일 로딩 테스트
1. "+ 규칙 추가" 클릭
2. 파일 선택 드롭다운에서 파일 검색
3. 파일 선택 시 자동 내용 로딩 확인

## 🛠 문제 해결

### 404 오류가 발생하는 경우
1. **이중 경로 문제**: `cursor-rules/cursor-rules/` 형태로 요청되는지 확인
2. **BASE_PATH 확인**: Console에서 `BASE_PATH` 값 확인
3. **files.json 경로**: `cursor-rules/` 접두사가 올바르게 제거되는지 확인

### 로그 분석 방법
```javascript
// Console에서 직접 테스트
console.log('Current path:', window.location.pathname);
console.log('Is GitHub Pages:', window.location.pathname.includes('/cursor-rules/'));

// 특정 파일 경로 테스트
const testEntry = { path: 'cursor-rules/common/10-security.kr.md' };
console.log('URL result:', urlFor(testEntry));
```

## 📋 배포 전 최종 확인

### 1. 로컬 테스트 통과
```bash
# 서버 시작
node test-github-pages.js

# 다른 터미널에서 curl 테스트
curl -I http://localhost:3000/cursor-rules/common/10-security.kr.md
# 응답: 200 OK (404가 아님)
```

### 2. 실제 파일 존재 확인
```bash
# web 디렉토리 구조 확인
find web/cursor-rules -name "*.md" | head -5
```

### 3. files.json 검증
```bash
# files.json의 경로가 올바른지 확인
jq '.[] | .path' web/files.json | head -5
# 예상 결과: "cursor-rules/common/00-core.en.md"
```

## 🚀 배포 후 검증

GitHub Pages 배포 후 실제 사이트에서:
```
https://jinwoo-j.github.io/cursor-rules/
```

1. 개발자 도구 Console 확인
2. 프리셋 로딩 테스트
3. 파일 자동 로딩 테스트

## 💡 팁

- **캐시 문제**: 브라우저에서 강력 새로고침 (Ctrl+Shift+R)
- **CORS 문제**: 로컬 서버는 CORS 헤더를 자동으로 추가함
- **실시간 디버깅**: Console에서 `urlFor()` 함수를 직접 호출해서 테스트

---

이 테스트 환경으로 GitHub Pages 배포 전에 모든 경로 문제를 미리 발견하고 해결할 수 있습니다! 🎯
