#!/bin/bash
# Generic Kalam two-PDF build (Nature-family 4-file layout). Copyable as-is — it
# derives its own location, finds pandoc on PATH, and reads VERSION from the env
# or metadata.yaml. Produces:
#   1) cover_letter + main_text         -> output/<name>_main_<date>.pdf
#   2) methods + extended_data_SI       -> output/<name>_methods_SI_<date>.pdf
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
DRAFTS="$ROOT/drafts"
OUT="$ROOT/output"; mkdir -p "$OUT"
DATE=$(date +%Y-%m-%d)
PANDOC="$(command -v pandoc || echo pandoc)"
# version: $VERSION env wins; else current_version from metadata.yaml; else v1.0
VERSION="${VERSION:-$(grep -E '^current_version:' "$ROOT/metadata.yaml" 2>/dev/null | sed -E 's/.*"([^"]+)".*/\1/')}"
VERSION="${VERSION:-v1.0}"
CSL="$DRAFTS/nature.csl"; CSLOPT=""; [ -f "$CSL" ] && CSLOPT="--csl=$CSL"

build () {            # $1 = output stem ; remaining args = input .md files (in order)
  local out="$1"; shift
  cat "$@" > "$DRAFTS/_${out}.md"
  "$PANDOC" "$DRAFTS/_${out}.md" \
    --pdf-engine=xelatex --citeproc $CSLOPT \
    --bibliography="$ROOT/references.bib" \
    --resource-path="$ROOT:$DRAFTS" \
    -V documentclass=article -V classoption=11pt \
    -V geometry:margin=2.5cm -V colorlinks=true \
    -o "$OUT/${out}_${VERSION}_${DATE}.pdf"
  echo "BUILT: $OUT/${out}_${VERSION}_${DATE}.pdf"
}

build manuscript_main       "$DRAFTS/cover_letter.md" "$DRAFTS/main_text.md"
build manuscript_methods_SI "$DRAFTS/methods.md"      "$DRAFTS/extended_data_SI.md"
