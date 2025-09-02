// server.js

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// 포트 설정
const PORT = 3000;

// 프로젝트 루트 디렉터리 경로
const projectRoot = __dirname;

// 웹 디렉터리 경로
const webDir = path.join(projectRoot, 'web');

// MIME 타입 매핑
const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.md': 'text/markdown',
    '.txt': 'text/plain'
};

// 서버 생성
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = decodeURIComponent(parsedUrl.pathname);
    let filePath = path.join(webDir, pathname);

    // 기본 경로 처리
    if (pathname === '/' || pathname === '/index.html') {
        filePath = path.join(webDir, 'index.html');
    }
    
    // Builder 페이지 처리
    if (pathname === '/builder.html') {
        filePath = path.join(webDir, 'builder.html');
    }

    // 정적 파일 제공
    serveStaticFile(filePath, res);
});

// 정적 파일 제공 함수
function serveStaticFile(filePath, res) {
    fs.access(filePath, fs.constants.F_OK, (err) => {
        if (err) {
            // 파일이 존재하지 않으면 404 반환
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Not Found');
            return;
        }

        // 파일의 확장자에 따라 MIME 타입 설정
        const extname = String(path.extname(filePath)).toLowerCase();
        const contentType = mimeTypes[extname] || 'application/octet-stream';

        // 파일 읽기
        fs.readFile(filePath, (err, data) => {
            if (err) {
                console.error('파일 읽기 오류:', err);
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('Internal Server Error');
            } else {
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(data);
            }
        });
    });
}

// 서버 시작
server.listen(PORT, () => {
    console.log(`서버가 http://localhost:${PORT} 에서 실행 중입니다.`);
});