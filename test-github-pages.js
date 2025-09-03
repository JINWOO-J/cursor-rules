#!/usr/bin/env node

/**
 * GitHub Pages 환경을 시뮬레이션하는 로컬 테스트 서버
 * 실제 GitHub Pages처럼 /cursor-rules/ 경로에서 서빙합니다
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3000;
const WEB_ROOT = path.join(__dirname, 'web');

// MIME 타입 매핑
const mimeTypes = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.md': 'text/markdown',
  '.ico': 'image/x-icon'
};

function serveFile(filePath, res) {
  const ext = path.extname(filePath);
  const contentType = mimeTypes[ext] || 'text/plain';
  
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      console.log(`❌ 404: ${filePath}`);
      return;
    }
    
    res.writeHead(200, { 
      'Content-Type': contentType,
      'Access-Control-Allow-Origin': '*'
    });
    res.end(data);
    console.log(`✅ 200: ${filePath}`);
  });
}

const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url);
  let pathname = parsedUrl.pathname;
  
  console.log(`📥 Request: ${pathname}`);
  
  // GitHub Pages 스타일 라우팅: /cursor-rules/로 시작하는 요청 처리
  if (pathname === '/cursor-rules/' || pathname === '/cursor-rules') {
    // 메인 index.html 서빙
    serveFile(path.join(WEB_ROOT, 'index.html'), res);
    return;
  }
  
  if (pathname.startsWith('/cursor-rules/')) {
    // /cursor-rules/ 접두사 제거하고 web/ 디렉토리에서 파일 찾기
    const relativePath = pathname.substring('/cursor-rules/'.length);
    const filePath = path.join(WEB_ROOT, relativePath);
    
    console.log(`🔄 GitHub Pages simulation: ${pathname} -> ${filePath}`);
    serveFile(filePath, res);
    return;
  }
  
  // 루트 요청은 /cursor-rules/로 리다이렉트
  if (pathname === '/' || pathname === '') {
    res.writeHead(302, { 'Location': '/cursor-rules/' });
    res.end();
    console.log(`🔄 Redirect: / -> /cursor-rules/`);
    return;
  }
  
  // 기타 요청은 404
  res.writeHead(404, { 'Content-Type': 'text/plain' });
  res.end('404 Not Found - Use /cursor-rules/ path');
  console.log(`❌ 404: ${pathname} (not in /cursor-rules/)`);
});

server.listen(PORT, () => {
  console.log('🚀 GitHub Pages 시뮬레이션 서버 시작됨');
  console.log(`📍 URL: http://localhost:${PORT}/cursor-rules/`);
  console.log(`📁 Web root: ${WEB_ROOT}`);
  console.log('');
  console.log('📋 테스트 방법:');
  console.log('  1. 브라우저에서 http://localhost:3000/cursor-rules/ 접속');
  console.log('  2. 개발자 도구 Console에서 경로 로그 확인');
  console.log('  3. 프리셋 로딩 테스트');
  console.log('');
  console.log('🛑 서버 종료: Ctrl+C');
});

// 우아한 종료 처리
process.on('SIGINT', () => {
  console.log('\n🛑 서버 종료 중...');
  server.close(() => {
    console.log('✅ 서버가 종료되었습니다.');
    process.exit(0);
  });
});
