#!/usr/bin/env bash
set -euo pipefail

echo "Building web/"
rm -rf web/cursor-rules
rm -rf web/files.json
rm -rf web/version-info.json
mkdir -p web

# 1) files.json
MD_DIRS=("cursor-rules" "cursor-rules/common" "cursor-rules/project" "cursor-rules/generated" "cursor-rules/common/stacks")
{
  echo "["
  first=true
  # 정렬 후 중복 제거
  while IFS= read -r -d '' file; do
    base="$(basename "$file")"
    lang="und"
    [[ "$base" =~ \.kr\.md$ ]] && lang="kr"
    [[ "$base" =~ \.en\.md$ ]] && lang="en"
    $first || echo ","
    first=false
    RAW_URL="https://raw.githubusercontent.com/${GITHUB_REPOSITORY}/${GITHUB_REF_NAME}/${file}"
    printf '{"path":"%s","raw_url":"%s","lang":"%s"}' "$file" "$RAW_URL" "$lang"
  done < <(find web/cursor-rules -type f -name "*.md" -print0 \
          | sort -zu | uniq -z)
  echo
  echo "]"
} > web/files.json

cp -rv cursor-rules web/ || true

cat > web/version-info.json <<JSON
{
  "last_commit_id": "$(git rev-parse HEAD)",
  "last_commit_message": "$(git log -1 --pretty=%B | sed ':a;N;$!ba;s/\n/\\n/g' | sed 's/"/\\"/g')",
  "branch": "${GITHUB_REF#refs/heads/}",
  "committed_at": "$(git log -1 --format=%cI)",
  "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON

echo "web/ built"

