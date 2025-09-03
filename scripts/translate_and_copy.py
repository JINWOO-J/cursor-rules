#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KR 원문을 기반으로 web/cursor-rules/** 아래에만 산출물을 생성합니다.
규칙:
- *.kr.md  : web/.../*.kr.md (복사) + web/.../*.en.md (번역 생성)
- *.en.md  : web/.../*.en.md (복사)                           # 원문이 영어인 경우
- *.md     : web/.../*.kr.md (이름 변환) + web/.../*.en.md (번역 생성)
- EN 산출물에는 source_sha(front matter)로 재번역 방지
- glossary.kr-en.json이 있으면 용어를 강제 적용
"""

import os
import re
import json
import sys
import shutil
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
import yaml
import google.generativeai as genai

# -------- Paths & Config --------
ROOT = Path(__file__).resolve().parents[1]  # repo root
SRC_DIRS = [
    "cursor-rules/common/stacks",
    "cursor-rules/common",
    "cursor-rules/project",
    "cursor-rules/generated",
    "cursor-rules",
]
SRC_ROOTS = [ROOT / d for d in SRC_DIRS]
OUT_ROOT = ROOT / "web" / "cursor-rules"

GLOSSARY_PATH = ROOT / "cursor-rules" / "glossary.kr-en.json"  # optional
API_KEY = os.environ.get("GEMINI_API_KEY")
# MODEL = "gemini-2.0-flash"  # 필요시 pro로 변경
MODEL = 'gemini-1.5-flash-8b'
# MODEL = 'gemini-1.5-flash-8b'

if not API_KEY:
    print("GEMINI_API_KEY is not set", file=sys.stderr)
    sys.exit(1)

genai.configure(api_key=API_KEY)
# for m in genai.list_models():
#     print(m.name, getattr(m, "supported_generation_methods", []))

model = genai.GenerativeModel(MODEL)

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


# -------- Utils --------
def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_git_file_info(file_path: Path) -> dict:
    """파일의 Git 커밋 정보를 가져옵니다."""
    try:
        cmd = [
            'git', 'log', '-1', '--format=%H|%an|%ae|%ci|%s', 
            '--', str(file_path)
        ]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            cwd=ROOT,
            check=True
        )
        
        if result.stdout.strip():
            commit_hash, author_name, author_email, commit_date, commit_message = result.stdout.strip().split('|', 4)
            

            if ' +' in commit_date:
                commit_date_clean = commit_date.rsplit(' +', 1)[0]
            elif ' -' in commit_date:
                commit_date_clean = commit_date.rsplit(' -', 1)[0]
            else:
                commit_date_clean = commit_date
            
            return {
                'commit_hash': commit_hash[:7],  # 짧은 해시
                'commit_hash_full': commit_hash,
                'author_name': author_name,
                'author_email': author_email,
                'commit_date': commit_date_clean,  # 원본 형식 유지
                'commit_message': commit_message.strip()
            }
    except (subprocess.CalledProcessError, ValueError, IndexError) as e:
        print(f"[warn] Git info extraction failed for {file_path}: {e}", file=sys.stderr)
    
    # Git 정보 추출 실패 시 기본값 반환
    return {
        'commit_hash': 'unknown',
        'commit_hash_full': 'unknown',
        'author_name': 'unknown',
        'author_email': 'unknown',
        'commit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'commit_message': 'unknown'
    }

def split_front_matter(md: str):
    m = FRONT_MATTER_RE.match(md)
    if m:
        fm_text = m.group(1)
        body = md[m.end():]
        fm = yaml.safe_load(fm_text) or {}
    else:
        fm, body = {}, md
    return fm, body

def build_front_matter(fm: dict) -> str:
    yaml_content = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    # yaml.safe_dump는 None이나 bytes를 반환할 수 있으므로 안전하게 처리
    if yaml_content is None:
        yaml_content = ""
    elif isinstance(yaml_content, bytes):
        yaml_content = yaml_content.decode('utf-8')
    return "---\n" + yaml_content + "---\n"

def load_glossary() -> dict:
    if GLOSSARY_PATH.exists():
        try:
            return json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[warn] failed to parse glossary: {e}", file=sys.stderr)
    return {}

GLOSSARY = load_glossary()


# -------- Prompt builders --------
PROMPT_SYSTEM = """You are a professional technical translator (Korean → English).
Translate the Korean text to clear, concise, developer-friendly English.
Absolutely preserve:
- Markdown structure, headings, tables, lists, links, images
- Code blocks and inline code (do NOT translate code)
- Front matter keys and values except `title`/`description` which should be translated
- Anchor links and IDs
Terminology rules:
- Use the provided glossary strictly when applicable.
- Keep product/library names as-is.
Formatting:
- Keep line breaks and spacing where meaningful; wrap lines naturally otherwise.
- Do not add explanations or commentary.
"""

def build_user_prompt(kr_body: str, glossary: dict) -> str:
    glossary_lines = "\n".join([f"- {k} → {v}" for k, v in glossary.items()])
    return f"""Glossary (KR→EN):
{glossary_lines if glossary_lines else "- (none)"}

Task:
Translate the following Markdown content from Korean to English.

<CONTENT>
{kr_body}
</CONTENT>
"""

def translate_inline(text: str) -> str:
    if not text:
        return text
    glossary_lines = "\n".join([f"- {k} → {v}" for k, v in GLOSSARY.items()]) or "(none)"
    r = model.generate_content([
        PROMPT_SYSTEM,
        f"Glossary:\n{glossary_lines}\n\nTranslate this short text (title/description) to English:\n\n{text}"
    ])
    return (r.text or "").strip()


# -------- Core translation --------
def translate_markdown(kr_md: str, src_file: Path) -> str:
    fm, body = split_front_matter(kr_md)
    src_sha = sha256_text(kr_md)

    # Git 정보 추출
    git_info = get_git_file_info(src_file)

    # front matter 업데이트 (본문 번역 별도)
    fm_en = dict(fm)
    fm_en["lang"] = "en"
    fm_en["source_lang"] = fm.get("lang", "kr")
    fm_en["source_sha"] = src_sha
    
    # Git 정보 추가
    fm_en["source_commit"] = git_info["commit_hash"]
    fm_en["source_author"] = git_info["author_name"]
    fm_en["source_date"] = git_info["commit_date"]
    fm_en["translated_at"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 제목/설명만 번역
    if "title" in fm_en:
        fm_en["title"] = translate_inline(fm_en["title"])
    if "description" in fm_en:
        fm_en["description"] = translate_inline(fm_en["description"])

    # 본문 번역
    user_prompt = build_user_prompt(body, GLOSSARY)
    resp = model.generate_content([PROMPT_SYSTEM, user_prompt])
    en_body = resp.text or ""

    return build_front_matter(fm_en) + en_body


# -------- Path mapping (to OUT_ROOT) --------
def out_path_for(src: Path, lang_suffix: str | None, rename_plain_to_kr: bool) -> Path:
    """
    src: absolute path under one of SRC_ROOTS
    lang_suffix: None keeps suffix; "en" forces .en.md; "" with rename_plain_to_kr=True rewrites *.md → *.kr.md
    
    디렉토리 구조를 보존하여 매핑:
    cursor-rules/common/stacks/foo.md → web/cursor-rules/common/stacks/foo.kr.md
    cursor-rules/common/bar.md → web/cursor-rules/common/bar.kr.md
    cursor-rules/project/baz.md → web/cursor-rules/project/baz.kr.md
    """
    # cursor-rules/ 루트를 기준으로 상대 경로 계산
    cursor_rules_root = ROOT / "cursor-rules"
    
    try:
        # cursor-rules/ 루트 기준 상대 경로
        rel = src.relative_to(cursor_rules_root)
    except ValueError:
        # cursor-rules/ 외부 파일인 경우 fallback (일반적으로 발생하지 않음)
        rel = Path(src.name)

    # *.md(plain) → *.kr.md 로 바꾸는 경우
    name = rel.name
    if rename_plain_to_kr and name.endswith(".md") and not name.endswith(".kr.md") and not name.endswith(".en.md"):
        rel = rel.with_name(rel.stem + ".kr.md")

    dest = OUT_ROOT / rel

    # lang_suffix 강제 (.kr.md → .en.md 등)
    if lang_suffix:
        if dest.name.endswith(".kr.md"):
            dest = dest.with_name(dest.name.replace(".kr.md", f".{lang_suffix}.md"))
        elif dest.name.endswith(".md") and not dest.name.endswith(".en.md"):
            dest = dest.with_name(dest.stem + f".{lang_suffix}.md")

    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest


# -------- Processing --------
def process_file(src: Path):
    """
    - *.kr.md      → copy KR,   translate to EN
    - *.en.md      → copy EN
    - *.md (plain) → write KR (renamed), translate to EN
    """
    text = src.read_text(encoding="utf-8")
    fm, body = split_front_matter(text)
    src_sha = sha256_text(text)

    # Git 정보 추출 (모든 파일에 공통 적용)
    git_info = get_git_file_info(src)

    is_en = src.name.endswith(".en.md")
    is_kr = src.name.endswith(".kr.md")
    is_plain = (src.suffix == ".md" and not is_en and not is_kr)

    # 1) KR 산출
    if is_kr:
        kr_out = out_path_for(src, lang_suffix=None, rename_plain_to_kr=False)
        # 기존 KR 파일에도 Git 정보 추가
        fm_kr = dict(fm)
        if "source_commit" not in fm_kr:  # 이미 Git 정보가 없는 경우만 추가
            fm_kr["source_commit"] = git_info["commit_hash"]
            fm_kr["source_author"] = git_info["author_name"] 
            fm_kr["source_date"] = git_info["commit_date"]
            kr_text = build_front_matter(fm_kr) + body
            kr_out.write_text(kr_text, encoding="utf-8")
            print(f"[write] KR (with git info) → {kr_out}")
        else:
            shutil.copy2(src, kr_out)
            print(f"[copy] KR  → {kr_out}")
    elif is_plain:
        kr_out = out_path_for(src, lang_suffix=None, rename_plain_to_kr=True)
        # plain → kr로 저장하면서 lang + Git 정보 보강
        fm2 = dict(fm)
        if fm2.get("lang") != "kr":
            fm2["lang"] = "kr"
        
        # Git 정보 추가
        fm2["source_commit"] = git_info["commit_hash"]
        fm2["source_author"] = git_info["author_name"]
        fm2["source_date"] = git_info["commit_date"]
        
        kr_text = build_front_matter(fm2) + body if fm else text
        kr_out.write_text(kr_text, encoding="utf-8")
        print(f"[write] KR  → {kr_out}")

    # 2) EN 산출
    if is_en:
        en_out = out_path_for(src, lang_suffix=None, rename_plain_to_kr=False)
        shutil.copy2(src, en_out)
        print(f"[copy] EN  → {en_out}")
    else:
        # kr 또는 plain 기준으로 EN 생성
        en_out = out_path_for(src, lang_suffix="en", rename_plain_to_kr=is_plain)
        # 재번역 방지: 기존 EN의 source_sha 확인
        if en_out.exists():
            exist_fm, _ = split_front_matter(en_out.read_text(encoding="utf-8"))
            if exist_fm.get("source_sha") == src_sha:
                print(f"[skip] EN up-to-date: {en_out}")
                return
        en_text = translate_markdown(text, src)  # src 파일 경로 전달
        en_out.write_text(en_text, encoding="utf-8")
        print(f"[write] EN  → {en_out}")


def main():
    # clean output root for deterministic build
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)

    # cursor-rules/ 루트에서 모든 *.md 파일을 한 번만 처리
    cursor_rules_root = ROOT / "cursor-rules"
    processed_files = set()
    
    if cursor_rules_root.exists():
        for path in cursor_rules_root.rglob("*.md"):
            # 소스 트리 안의 *.md만 처리 (산출물 트리 제외)
            if "web/cursor-rules" in str(path):
                continue
            
            # 중복 처리 방지
            if path.resolve() in processed_files:
                continue
            processed_files.add(path.resolve())
            
            process_file(path)

if __name__ == "__main__":
    sys.exit(main())
