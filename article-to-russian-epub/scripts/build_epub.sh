#!/usr/bin/env bash
# Build an EPUB from a Russian Markdown translation.
# Usage: build_epub.sh input.md "Author" [output.epub]
# Expects: first line "# Title", sections as "##", images referenced relative to input.md.
set -euo pipefail

if [ $# -lt 2 ]; then
  echo 'Usage: build_epub.sh input.md "Author" [output.epub]' >&2
  exit 2
fi

input=$1
author=$2
output=${3:-${input%.md}.epub}

[ -f "$input" ] || { echo "Error: file '$input' not found" >&2; exit 1; }
command -v pandoc >/dev/null || { echo "Error: pandoc is not installed" >&2; exit 1; }

title=$(grep -m1 '^# ' "$input" | sed 's/^# //')
[ -n "$title" ] || { echo "Error: '$input' has no '# Title' line" >&2; exit 1; }

command -v python3 >/dev/null || { echo "Error: python3 is not installed" >&2; exit 1; }
typograph="$(cd "$(dirname "$0")" && pwd)/typograph.py"

# Drop the "# Title" line: pandoc renders the title page from metadata.
# Add non-breaking spaces to the copy only, so the source .md stays easy to edit.
# Shift "##" sections to level 1 so each becomes its own chapter.
awk -v t="# $title" 'done || $0 != t { print; next } { done = 1 }' "$input" |
  python3 -I "$typograph" |
  pandoc -f markdown -o "$output" \
    --resource-path="$(dirname "$input")" \
    --shift-heading-level-by=-1 \
    --split-level=1 --toc --toc-depth=2 \
    --metadata title="$title" \
    --metadata author="$author" \
    --metadata lang=ru \
    --metadata toc-title="Оглавление" \
    --metadata date="$(date +%Y-%m-%d)"

echo "Created: $output"
