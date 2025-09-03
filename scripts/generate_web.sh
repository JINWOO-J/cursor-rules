#!/usr/bin/env bash
set -euo pipefail

echo "Building web/"
rm -rf web
mkdir -p web

# 1) files.json
MD_DIRS=("cursor-rules" "cursor-rules/common" "cursor-rules/project" "cursor-rules/generated" "cursor-rules/common/stacks")
{
  echo "["
  first=true
  for dir in "${MD_DIRS[@]}"; do
    [ -d "$dir" ] || continue
    # 안정적 순서
    while IFS= read -r -d '' file; do
      # lang 추론
      base="$(basename "$file")"
      lang="und"
      [[ "$base" =~ \.en\.md$ ]] && lang="en"
      [[ "$base" =~ \.kr\.md$ ]] && lang="kr"
      $first || echo ","
      first=false
      RAW_URL="https://raw.githubusercontent.com/${GITHUB_REPOSITORY}/${GITHUB_REF_NAME}/${file}"
      printf '{"path":"%s","raw_url":"%s","lang":"%s"}' "$file" "$RAW_URL" "$lang"
    done < <(find "$dir" -type f -name "*.md" -print0 | sort -z)
  done
  echo
  echo "]"
} > web/files.json

# 2) 원본 디렉터리 복사
cp -rv cursor-rules web/ || true

# 3) version-info.json
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

