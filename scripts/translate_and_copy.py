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

보강 사항:
- 문서 전체가 코드펜스(``` 또는 ~~~)로 감싸진 경우 자동 언랩
- LLM이 본문에 임의 Front matter(---)를 재생성하면 제거
- title/description 번역 결과에서 코드펜스/---/개행 찌꺼기 제거
- Front matter 정규식이 BOM/선행 공백 허용
- translated_at은 KST(UTC+9) 고정
- Free tier 레이트리밋 대응: 사전 쓰로틀 + 429/일시오류 지수 백오프 + (옵션) 실패시 계속
- 상세 로깅 추가: 진행/스킵/대기/재시도/요약/실패 목록
"""

import os
import re
import json
import sys
import shutil
import hashlib
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
import time
from collections import deque
from typing import List, Dict, Tuple

import yaml
import google.generativeai as genai
import logging

# =========================
# Logging setup
# =========================
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_JSON = os.environ.get("LOG_JSON", "0") == "1"
LOG_COLOR = os.environ.get("LOG_COLOR", "0") == "1"

class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            payload.update(record.extra)
        # include common extras
        for k in ("file", "stage", "wait", "attempt", "rpm", "retry_delay", "model"):
            if hasattr(record, k):
                payload[k] = getattr(record, k)
        return json.dumps(payload, ensure_ascii=False)

class _ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[90m",
        "INFO": "\033[36m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"
    BASE = "%(asctime)s [%(levelname)s] %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        color = self.COLORS.get(record.levelname, "")
        reset = self.RESET if color else ""
        return f"{color}{msg}{reset}"

def _setup_logger():
    logger = logging.getLogger("translate")
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
    handler = logging.StreamHandler(sys.stdout)
    if LOG_JSON:
        fmt = _JsonFormatter()
    elif LOG_COLOR:
        fmt = _ColorFormatter(fmt=_ColorFormatter.BASE, datefmt="%H:%M:%S")
    else:
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
    handler.setFormatter(fmt)
    logger.handlers = [handler]
    logger.propagate = False
    return logger

log = _setup_logger()

# =========================
# Paths & Config
# =========================
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
MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")  # 필요시 변경
if not API_KEY:
    log.error("GEMINI_API_KEY is not set")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL)

# Rate-limit / Retry
RPM = int(os.environ.get("GEMINI_RPM", "12"))          # free tier 15 → 12 권장
MAX_RETRY = int(os.environ.get("GEMINI_MAX_RETRY", "5"))
STRICT_FAIL = os.environ.get("STRICT_FAIL", "0") == "1"
_request_times = deque()  # 최근 60초 내 호출 TS

# Summary counters
summary = {
    "files_total": 0,
    "kr_written": 0,
    "en_written": 0,
    "en_skipped": 0,
    "errors": 0,
    "throttle_waits": 0,
    "retries": 0,
}
failures: List[Tuple[str, str]] = []

# =========================
# Regex
# =========================
FRONT_MATTER_RE = re.compile(r"^\s*\ufeff?---\n(.*?)\n---\n", re.DOTALL)
CODE_FENCE_WHOLE_RE = re.compile(
    r"^\s*(?P<fence>(`{3,}|~{3,}))(?P<lang>[a-zA-Z0-9+-]*)\s*\n(?P<body>.*)\n(?P=fence)\s*$",
    re.DOTALL
)

# =========================
# Utils
# =========================
def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_git_file_info(file_path: Path) -> dict:
    try:
        cmd = ['git', 'log', '-1', '--format=%H|%an|%ae|%ci|%s', '--', str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=True)
        if result.stdout.strip():
            commit_hash, author_name, author_email, commit_date, commit_message = result.stdout.strip().split('|', 4)
            if ' +' in commit_date:
                commit_date_clean = commit_date.rsplit(' +', 1)[0]
            elif ' -' in commit_date:
                commit_date_clean = commit_date.rsplit(' -', 1)[0]
            else:
                commit_date_clean = commit_date
            return {
                'commit_hash': commit_hash[:7],
                'commit_hash_full': commit_hash,
                'author_name': author_name,
                'author_email': author_email,
                'commit_date': commit_date_clean,
                'commit_message': commit_message.strip()
            }
    except Exception as e:
        log.warning("Git info extraction failed for %s: %s", file_path, e, extra={"file": str(file_path), "stage":"git"})
    return {
        'commit_hash': 'unknown',
        'commit_hash_full': 'unknown',
        'author_name': 'unknown',
        'author_email': 'unknown',
        'commit_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'commit_message': 'unknown'
    }

def unwrap_monolithic_code_fence(md: str) -> tuple[str, bool]:
    m = CODE_FENCE_WHOLE_RE.match(md)
    if m:
        return m.group("body"), True
    return md, False

def strip_spurious_front_matter(md: str) -> str:
    m = FRONT_MATTER_RE.match(md)
    if m:
        return md[m.end():]
    return md

def clean_yaml_scalar(s: str) -> str:
    if not s:
        return s
    s = re.sub(r"^\s*\ufeff?---\n.*?\n---\n", "", s, flags=re.DOTALL)
    s = re.sub(r"^\s*(`{3,}|~{3,})[a-zA-Z0-9+-]*\s*\n", "", s)
    s = re.sub(r"\n(`{3,}|~{3,})\s*$", "", s)
    s = re.sub(r"\s*\n\s*", " ", s).strip()
    if (s.startswith(("'", '"')) and s.endswith(("'", '"')) and len(s) >= 2):
        s = s[1:-1].strip()
    return s

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
            log.warning("failed to parse glossary: %s", e, extra={"stage":"glossary"})
    return {}

GLOSSARY = load_glossary()

# =========================
# Prompts
# =========================
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
Output rules:
- Output MUST be ONLY the translated Markdown BODY.
- Do NOT output any YAML front matter (--- blocks) in your answer.
- Do NOT wrap the whole output in code fences.
"""

def build_user_prompt(kr_body: str, glossary: dict) -> str:
    glossary_lines = "\n".join([f"- {k} → {v}" for k, v in glossary.items()])
    return f"""Glossary (KR→EN):
{glossary_lines if glossary_lines else "- (none)"}

Task:
Translate the following Markdown BODY from Korean to English.
Remember: Do NOT include YAML front matter in the output.

<CONTENT>
{kr_body}
</CONTENT>
"""

# =========================
# Rate limit & Retry
# =========================
def _throttle_before_call():
    """최근 60초 창에서 RPM을 넘으면 대기."""
    now = time.time()
    while _request_times and now - _request_times[0] >= 60:
        _request_times.popleft()
    if len(_request_times) >= RPM:
        wait = 60 - (now - _request_times[0]) + 0.05
        summary["throttle_waits"] += 1
        log.info("throttle: waiting %.2fs (rpm=%d)", wait, RPM, extra={"wait": round(wait,2), "rpm": RPM, "stage":"throttle"})
        time.sleep(max(wait, 0))
    _request_times.append(time.time())

def gemini_generate(parts):
    """model.generate_content 호출을 안전하게 감싸는 래퍼(레이트리밋 + 백오프)."""
    backoff = 1.5
    for attempt in range(1, MAX_RETRY + 1):
        try:
            _throttle_before_call()
            return model.generate_content(parts)
        except Exception as e:
            msg = str(e)
            retry_after = getattr(getattr(e, "retry_delay", None), "seconds", None)
            # 429 등 쿼터 오류
            if "ResourceExhausted" in msg or "429" in msg:
                delay = retry_after if retry_after is not None else backoff
                reason = "quota"
            else:
                delay = backoff
                reason = "transient"
            summary["retries"] += 1
            log.warning("retry %d/%d (%s) in %.1fs", attempt, MAX_RETRY, reason, delay,
                        extra={"attempt": attempt, "retry_delay": delay, "stage":"retry", "model": MODEL})
            if attempt >= MAX_RETRY:
                raise
            time.sleep(min(max(delay, 1.0), 60))
            backoff = min(backoff * 2, 30)

# =========================
# Core translation
# =========================
def translate_inline(text: str) -> str:
    if not text:
        return text
    glossary_lines = "\n".join([f"- {k} → {v}" for k, v in GLOSSARY.items()]) or "(none)"
    try:
        r = gemini_generate([
            PROMPT_SYSTEM,
            f"Glossary:\n{glossary_lines}\n\nTranslate this short text (title/description) to English as a single-line YAML-safe scalar. Do NOT add code fences or front matter:\n\n{text}"
        ])
        return clean_yaml_scalar((r.text or "").strip())
    except Exception as e:
        log.warning("inline translation failed: %s (keep original)", e, extra={"stage":"inline"})
        return clean_yaml_scalar(text)

def translate_markdown(kr_md: str, src_file: Path) -> str:
    # 0) 문서가 전체 코드펜스로 감싸져 있으면 언랩
    kr_md_unwrapped, wrapped = unwrap_monolithic_code_fence(kr_md)
    if wrapped:
        log.debug("unwrapped code fence for %s", src_file, extra={"file": str(src_file), "stage":"unwrap"})

    # 1) FM/Body 파싱
    fm, body = split_front_matter(kr_md_unwrapped)
    src_sha = sha256_text(kr_md)  # 원문 전체 해시(랩 포함)로 추적

    # 2) Git 정보
    git_info = get_git_file_info(src_file)

    # 3) EN FM 구성
    fm_en = dict(fm)
    fm_en["lang"] = "en"
    fm_en["source_lang"] = fm.get("lang", "kr")
    fm_en["source_sha"] = src_sha
    fm_en["source_commit"] = git_info["commit_hash"]
    fm_en["source_author"] = git_info["author_name"]
    fm_en["source_date"] = git_info["commit_date"]

    KST = timezone(timedelta(hours=9))
    fm_en["translated_at"] = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')

    # 4) 제목/설명 번역 (있는 경우에만)
    if "title" in fm_en:
        fm_en["title"] = clean_yaml_scalar(translate_inline(fm_en["title"]))
    if "description" in fm_en:
        fm_en["description"] = clean_yaml_scalar(translate_inline(fm_en["description"]))

    # 5) 본문 번역
    user_prompt = build_user_prompt(body, GLOSSARY)
    resp = gemini_generate([PROMPT_SYSTEM, user_prompt])
    en_body = (resp.text or "").strip()

    # 6) 모델이 혹시 본문 앞에 front matter를 생성했으면 제거
    en_body = strip_spurious_front_matter(en_body)

    # 7) (안전망) 모델이 전체 코드펜스로 감싸버렸다면 벗겨냄
    en_body, post_wrapped = unwrap_monolithic_code_fence(en_body)
    if post_wrapped:
        log.debug("removed whole code fence from output for %s", src_file, extra={"file": str(src_file), "stage":"unwrap"})

    return build_front_matter(fm_en) + en_body

# =========================
# Path mapping
# =========================
def out_path_for(src: Path, lang_suffix: str | None, rename_plain_to_kr: bool) -> Path:
    cursor_rules_root = ROOT / "cursor-rules"
    try:
        rel = src.relative_to(cursor_rules_root)
    except ValueError:
        rel = Path(src.name)

    name = rel.name
    if rename_plain_to_kr and name.endswith(".md") and not name.endswith(".kr.md") and not name.endswith(".en.md"):
        rel = rel.with_name(rel.stem + ".kr.md")

    dest = OUT_ROOT / rel

    if lang_suffix:
        if dest.name.endswith(".kr.md"):
            dest = dest.with_name(dest.name.replace(".kr.md", f".{lang_suffix}.md"))
        elif dest.name.endswith(".md") and not dest.name.endswith(".en.md"):
            dest = dest.with_name(dest.stem + f".{lang_suffix}.md")

    dest.parent.mkdir(parents=True, exist_ok=True)
    return dest

# =========================
# Processing
# =========================
def process_file(src: Path):
    raw = src.read_text(encoding="utf-8")
    text, wrapped = unwrap_monolithic_code_fence(raw)
    fm, body = split_front_matter(text)
    src_sha = sha256_text(raw)

    git_info = get_git_file_info(src)

    is_en = src.name.endswith(".en.md")
    is_kr = src.name.endswith(".kr.md")
    is_plain = (src.suffix == ".md" and not is_en and not is_kr)

    summary["files_total"] += 1
    log.info("processing: %s", src, extra={"file": str(src), "stage":"start"})

    # 1) KR 산출
    if is_kr:
        kr_out = out_path_for(src, lang_suffix=None, rename_plain_to_kr=False)
        fm_kr = dict(fm)
        if "source_commit" not in fm_kr:
            fm_kr["source_commit"] = git_info["commit_hash"]
            fm_kr["source_author"] = git_info["author_name"]
            fm_kr["source_date"] = git_info["commit_date"]
            kr_text = build_front_matter(fm_kr) + body
            kr_out.write_text(kr_text, encoding="utf-8")
            log.info("write KR → %s", kr_out, extra={"file": str(src), "stage":"write"})
        else:
            shutil.copy2(src, kr_out)
            log.info("copy KR  → %s", kr_out, extra={"file": str(src), "stage":"write"})
        summary["kr_written"] += 1
    elif is_plain:
        kr_out = out_path_for(src, lang_suffix=None, rename_plain_to_kr=True)
        fm2 = dict(fm)
        if fm2.get("lang") != "kr":
            fm2["lang"] = "kr"
        fm2["source_commit"] = git_info["commit_hash"]
        fm2["source_author"] = git_info["author_name"]
        fm2["source_date"] = git_info["commit_date"]
        kr_text = build_front_matter(fm2) + body if fm else text
        kr_out.write_text(kr_text, encoding="utf-8")
        log.info("write KR  → %s", kr_out, extra={"file": str(src), "stage":"write"})
        summary["kr_written"] += 1

    # 2) EN 산출
    if is_en:
        en_out = out_path_for(src, lang_suffix=None, rename_plain_to_kr=False)
        shutil.copy2(src, en_out)
        log.info("copy EN → %s", en_out, extra={"file": str(src), "stage":"write"})
        summary["en_written"] += 1
    else:
        en_out = out_path_for(src, lang_suffix="en", rename_plain_to_kr=is_plain)
        if en_out.exists():
            exist_fm, _ = split_front_matter(en_out.read_text(encoding="utf-8"))
            if exist_fm.get("source_sha") == src_sha:
                log.info("skip EN (up-to-date) → %s", en_out, extra={"file": str(src), "stage":"skip"})
                summary["en_skipped"] += 1
                return
        try:
            en_text = translate_markdown(raw, src)
            en_out.write_text(en_text, encoding="utf-8")
            log.info("write EN → %s", en_out, extra={"file": str(src), "stage":"write"})
            summary["en_written"] += 1
        except Exception as e:
            summary["errors"] += 1
            msg = f"EN translate failed: {e}"
            failures.append((str(src), str(e)))
            if STRICT_FAIL:
                log.error("%s", msg, extra={"file": str(src), "stage":"error"})
                raise
            else:
                log.error("%s (skip and continue)", msg, extra={"file": str(src), "stage":"error"})
                fail_mark = str(en_out) + ".failed.txt"
                Path(fail_mark).write_text(str(e), encoding="utf-8")

def main():
    # clean output root for deterministic build
    if OUT_ROOT.exists():
        shutil.rmtree(OUT_ROOT)
        log.debug("cleaned output root %s", OUT_ROOT, extra={"stage":"clean"})

    cursor_rules_root = ROOT / "cursor-rules"
    processed_files = set()

    files = list(cursor_rules_root.rglob("*.md")) if cursor_rules_root.exists() else []
    # 산출물 트리 제외
    files = [p for p in files if "web/cursor-rules" not in str(p)]
    total = len(files)
    log.info("start: %d markdown files found", total, extra={"stage":"start"})

    for path in files:
        if path.resolve() in processed_files:
            continue
        processed_files.add(path.resolve())
        try:
            process_file(path)
        except Exception as e:
            summary["errors"] += 1
            failures.append((str(path), str(e)))
            if STRICT_FAIL:
                raise

    # Summary
    log.info(
        "summary: files=%d, kr_written=%d, en_written=%d, en_skipped=%d, retries=%d, throttle_waits=%d, errors=%d",
        summary["files_total"], summary["kr_written"], summary["en_written"], summary["en_skipped"],
        summary["retries"], summary["throttle_waits"], summary["errors"],
        extra={"stage":"summary"}
    )
    if failures:
        log.warning("failed files (%d):", len(failures), extra={"stage":"summary"})
        for f, err in failures:
            log.warning(" - %s :: %s", f, err, extra={"file": f, "stage":"summary"})

    return 0 if summary["errors"] == 0 or not STRICT_FAIL else 1

if __name__ == "__main__":
    sys.exit(main())
