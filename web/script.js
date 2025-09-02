// script.js

// DOM 요소 가져오기
const fileSelect = document.getElementById('file-select');
const loadBtn = document.getElementById('load-btn');
const markdownContent = document.getElementById('markdown-content');
const copyBtn = document.getElementById('copy-btn');

// 초기화: .cursorrules 디렉터리에서 md 파일 목록 가져오기
async function init() {
    try {
        const response = await fetch('/list-md-files');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const files = await response.json();
        
        // 파일 목록을 select 요소에 추가
        files.forEach(file => {
            const option = document.createElement('option');
            option.value = file;
            option.textContent = file;
            fileSelect.appendChild(option);
        });
    } catch (error) {
        console.error('파일 목록을 불러오는 중 오류 발생:', error);
        markdownContent.innerHTML = `<p style="color: red;">파일 목록을 불러오는 데 실패했습니다: ${error.message}</p>`;
    }
}

// Markdown 파일 불러오기
async function loadMarkdownFile(filename) {
    try {
        // 서버에서 Markdown 파일 내용 가져오기
        const response = await fetch(`/get-md-file?filename=${encodeURIComponent(filename)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const markdownText = await response.text();

        // Markdown을 HTML로 변환
        const htmlContent = marked.parse(markdownText);

        // HTML 내용을 표시
        markdownContent.innerHTML = htmlContent;

        // 복사 버튼 표시
        copyBtn.classList.remove('hidden');
    } catch (error) {
        console.error('Markdown 파일을 불러오는 중 오류 발생:', error);
        markdownContent.innerHTML = `<p style="color: red;">파일을 불러오는 데 실패했습니다: ${error.message}</p>`;
        copyBtn.classList.add('hidden');
    }
}

// Markdown 내용을 클립보드에 복사
function copyMarkdownToClipboard() {
    const range = document.createRange();
    range.selectNode(markdownContent);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            alert('내용이 클립보드에 복사되었습니다.');
        } else {
            alert('복사에 실패했습니다.');
        }
    } catch (err) {
        console.error('복사 중 오류 발생:', err);
        alert('복사 중 오류가 발생했습니다.');
    }

    // Selection 해제
    window.getSelection().removeAllRanges();
}

// 이벤트 리스너 등록
document.addEventListener('DOMContentLoaded', init);
loadBtn.addEventListener('click', () => {
    const selectedFile = fileSelect.value;
    if (selectedFile) {
        loadMarkdownFile(selectedFile);
    } else {
        alert('파일을 먼저 선택하세요.');
    }
});
copyBtn.addEventListener('click', copyMarkdownToClipboard);