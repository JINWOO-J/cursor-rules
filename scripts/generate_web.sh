#!/usr/bin/env bash
set -euo pipefail
echo "Building web/ indexes (preserving web/cursor-rules)"

mkdir -p web
cp index.html web/index.html
cp cursor-rules/presets.json web/cursor-rules/presets.json


# GH 환경변수 안전 처리
GITHUB_REF=${GITHUB_REF:-"undefined"}
GITHUB_REPOSITORY=${GITHUB_REPOSITORY:-"undefined"}
ref_name="${GITHUB_REF_NAME:-${GITHUB_REF#refs/heads/}}"

# 산출물 존재 확인
if [ ! -d "web/cursor-rules" ]; then
  echo "ERROR: web/cursor-rules not found. Did translate_and_copy.py run?" >&2
  exit 1
fi

{
  echo "["
  first=true
  while IFS= read -r -d '' file; do
    # "web/" 접두어 제거 → 저장소 루트 기준 경로로 변환
    rel_path="${file#web/}"

    base="$(basename "$rel_path")"
    lang="und"
    [[ "$base" =~ \.en\.md$ ]] && lang="en"
    [[ "$base" =~ \.kr\.md$ ]] && lang="kr"

    $first || echo ","
    first=false

    RAW_URL="https://raw.githubusercontent.com/${GITHUB_REPOSITORY}/${ref_name}/${rel_path}"
    printf '{"path":"%s","raw_url":"%s","lang":"%s"}' "$rel_path" "$RAW_URL" "$lang"
  done < <(find "web/cursor-rules" -type f -name "*.md" -print0 | sort -z)
  echo
  echo "]"
} > web/files.json

last_commit_id="$(git rev-parse HEAD)"
committed_at="$(git log -1 --format=%cI)"

# 커밋 메시지를 JSON-safe 문자열로 인코딩 (따옴표/개행 포함)
last_commit_message_json="$(
python3 - <<'PY'
import sys, json, subprocess
msg = subprocess.check_output(["git","log","-1","--pretty=%B"], text=True)
print(json.dumps(msg.rstrip()))
PY
)"

# presets.json 복사 (authoring: cursor-rules/ → serving: web/cursor-rules/)
if [ -f "cursor-rules/presets.json" ]; then
  mkdir -p web/cursor-rules
  cp cursor-rules/presets.json web/cursor-rules/presets.json
  echo "Copied cursor-rules/presets.json → web/cursor-rules/presets.json"
fi


cat > web/version-info.json <<JSON
{
  "last_commit_id": "${last_commit_id}",
  "last_commit_message": ${last_commit_message_json},
  "branch": "${ref_name}",
  "committed_at": "${committed_at}",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON

echo "web/ indexes built"
