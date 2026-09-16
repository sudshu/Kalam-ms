---
name: km-export-docx
description: "Use when the user wants to export manuscript Markdown files (.md) to publication-ready Word documents (.docx). Two modes: (1) Quick export (/km-export-docx quick) — pandoc-only conversion with citations resolved, no formatting or verification, fast for iteration; (2) Full export (/km-export-docx or /km-export-docx full) — adds 11pt double-spaced body text, page and line numbers, 2cm margins, resized figures, figure-caption separators, three-line tables, and programmatic verification. Output goes to output/share_ready/. Invoke with /km-export-docx."
---

# Export Manuscript to Share-Ready Word Documents

Convert `.md` manuscript files to formatted `.docx` files ready for co-author sharing.

## Prerequisites

- `pandoc` installed
- `python-docx` Python package installed
- A Nature-family CSL file (downloaded automatically if missing)

## Modes

This skill has two modes. Choose based on the user's argument or context:

- **`/km-export-docx quick`** — Quick export. Pandoc conversion only with citations resolved. No python-docx post-processing, no verification. Use when iterating fast and the user just needs a readable DOCX to check content.
- **`/km-export-docx`** or **`/km-export-docx full`** — Full export. Pandoc + post-processing (formatting, separators, tables) + programmatic verification. Use before sharing with co-authors or submitting.

If the user says "quick", "fast", "just export", or "no formatting", use Quick mode. Otherwise default to Full.

## Submission DOCX mode and combined-document manuscripts (check FIRST)

Before using a combined builder, read `metadata.yaml → submission_docx_mode`:

- **`separate`**: main manuscript and SI must be exported as independent DOCX files, even if a
  legacy combined builder exists. Prefer a manuscript-specific split builder — example-paper's
  `drafts/v6/build_v6.sh docx` is the worked example (one source list drives both formats, so each
  DOCX ships with a content-identical PDF twin in `output/share_ready/`), or demo-carbon-debt's
  `drafts/build_exports/build_submission_docx.py`; otherwise use the per-file recipes below.
  Verify that the main DOCX contains no Supplementary Information heading and that the SI DOCX
  retains its own title, figures, tables and references.
- **`combined` or absent**: apply the combined-builder check below.

Before exporting per-file, check whether the manuscript builds a **combined document** (SI bundled
into the main deliverable) — indicated by a combined builder under `drafts/` (e.g. demo-carbon-debt's
legacy `drafts/build_exports/build_combined_docx.py`). If so, follow the share-ready layout convention
(`resources/conventions/export.md`, "Share-ready folder layout", user decision 2026-07-23):

1. Run the manuscript's combined builder → one DOCX in `output/share_ready/`.
2. Do **NOT** export a separate `supplementary_information.docx` (and do not save a separate
   supplementary PDF) — the SI lives inside the combined document.
3. Post-process (Step 4) and verify (Step 5) that single DOCX.
4. Ensure the matching combined PDF sits beside it in `output/share_ready/`, identically named
   apart from the extension (the manuscript's `build_full.sh` copies it there on every PDF build;
   rebuild if stale).
5. The cover letter, if present, is still exported as its own file.

End state: `output/share_ready/` holds the identically-named PDF + DOCX pair (plus cover letter),
nothing else. The per-file recipes below apply only to manuscripts without a combined builder.

---

## Quick Export

Run pandoc from the `drafts/` directory for each file that exists. No post-processing, no verification.

```bash
cd drafts/
# Manuscript (with citations)
pandoc manuscript.md --bibliography=../references.bib --citeproc --csl=../nature.csl -o ../output/share_ready/manuscript.docx

# SI (if exists)
pandoc supplementary_information.md --bibliography=../references.bib --citeproc --csl=../nature.csl -o ../output/share_ready/supplementary_information.docx

# Cover letter (if exists, no citeproc needed)
pandoc cover_letter.md -o ../output/share_ready/cover_letter.docx
```

Report file sizes and done. Skip all remaining steps.

---

## Full Export Process

### Step 1: Read Manuscript Context

1. Read `metadata.yaml` to identify the manuscript name, bibliography file, and `current_draft` (resolve the manuscript files per `resources/conventions/manuscript_files.md`)
2. Locate the main manuscript file(s) named in `current_draft` (fallback `drafts/manuscript.md`)
3. Locate the SI document from `current_draft` (fallback `drafts/supplementary_information.md`)
4. Locate the cover letter from `current_draft` (fallback `drafts/cover_letter.md`)
5. Check for `references.bib` (bibliography)
6. Create `output/share_ready/` directory if it doesn't exist

### Step 2: Ensure Citation Style File

Check if `nature.csl` exists in the manuscript root. If not, download it:

```bash
curl -sL "https://raw.githubusercontent.com/citation-style-language/styles/master/nature.csl" -o nature.csl
```

This gives Nature-style numbered superscript citations with full author names in the bibliography (no em-dash author substitution).

### Step 2b: Insert Logical Page Breaks

Run this whenever the user asks for page breaks — and by default on any full export, since
the breaks are what makes the Word file paginate like the PDF. It is idempotent, so running
it on a manuscript that already has them is a no-op.

```bash
python <skill_base_dir>/scripts/add_page_breaks.py <manuscript_dir>
```

The script edits the **draft Markdown**, not the rendered file, so one edit serves both the
PDF and the DOCX. Each break is a pair of raw blocks — a LaTeX `\clearpage` and an OOXML
`<w:br w:type="page"/>` — and each writer ignores the other's block. Both are required: a
`\clearpage`-only break is silently dropped from Word (this skill strips raw LaTeX, because
Word cannot embed vector PDF figures), and an OOXML-only break is dropped from the PDF.

Breaks go at four boundaries, each on by default:

| Boundary | Where |
|---|---|
| `after-abstract` | after the abstract, before the opening paragraph |
| `before-methods` | at the Methods heading, wherever it lives |
| `before-references` | at the reference list; when the bibliography is generated at build time (`--citeproc` with no `# References` in the source), at the end of the last main-text file, which is where the generated heading is appended |
| `before-si` | at the Supplementary Information heading |

Options: `--dry-run` reports the plan without writing; `--remove` strips every break the
script inserted (add + remove round-trips the file byte-for-byte); `--no-after-abstract`,
`--no-before-methods`, `--no-before-references`, `--no-before-si` skip individual boundaries.

Because the breaks live in the source, they also appear in a Quick export and in every PDF
built from the same files. A manuscript with its own build script should call this from the
script so the two formats cannot drift — see `manuscripts/example-paper/drafts/v6/build_v6.sh`,
which runs it before every target and honours `KM_PAGE_BREAKS=0` to skip.

### Step 3: Convert Markdown to Word via Pandoc

#### Main manuscript

Run pandoc from the `drafts/` directory so that relative figure paths (`../figures/`) resolve correctly:

```bash
cd drafts/
pandoc manuscript.md --bibliography=../references.bib --citeproc --csl=../nature.csl -o ../output/share_ready/manuscript.docx
```

#### Supplementary Information

If `drafts/supplementary_information.md` exists:

```bash
cd drafts/
pandoc supplementary_information.md --bibliography=../references.bib --citeproc --csl=../nature.csl -o ../output/share_ready/supplementary_information.docx
```

If the SI has no citations, the `--bibliography` and `--citeproc` flags are harmless.

#### Cover Letter

If `drafts/cover_letter.md` exists:

```bash
cd drafts/
pandoc cover_letter.md -o ../output/share_ready/cover_letter.docx
```

The cover letter typically has no citations so `--citeproc` is not needed; add it if the letter does reference the bibliography.

### Step 4: Post-Process Word Documents

Apply formatting preferences using the `format_docx.py` script. Run this on **each** exported `.docx` file (manuscript, SI, and cover letter). For manuscripts and SI, the script applies: 2cm margins, continuous line numbers, centred footer page numbers, 11pt double-spaced body text (headings untouched), three-line academic table styling, and figure-caption separator lines. Main-manuscript figures span the usable text width; SI figures retain the 14x16 cm maximum.

For the **main manuscript**:

```bash
python <skill_base_dir>/scripts/format_docx.py <filepath> --full-width-figures
```

For the **SI**:

```bash
python <skill_base_dir>/scripts/format_docx.py <filepath>
```

For the **cover letter** (uses 1.15 line spacing and omits manuscript page numbers):

```bash
python <skill_base_dir>/scripts/format_docx.py <filepath> --cover-letter
```

Replace `<skill_base_dir>` with the absolute path to the `km-export-docx` skill directory, and `<filepath>` with the path to the `.docx` file (e.g., `output/share_ready/manuscript.docx`).

### Step 5: Verify Rendered Output

After formatting, run the `verify_docx.py` script on each exported `.docx` to catch rendering problems before the user opens the file. The script checks: embedded image count and optional full-text-width placement, unresolved `[@...]` citations, bibliography presence, raw LaTeX fragments, table count, file size, line numbers, double spacing, footer page numbers, and figure-caption separators. It prints results as JSON to stdout. For cover letters, pass `--cover-letter` so manuscript spacing and pagination are not required.

```bash
python <skill_base_dir>/scripts/verify_docx.py <filepath> --expected-images N --expect-full-width-images
```

Replace `<skill_base_dir>` with the absolute path to the `km-export-docx` skill directory, `<filepath>` with the `.docx` path, and `N` with the expected minimum number of embedded figures (use 0 if unknown). Use `--expect-full-width-images` for the main manuscript and omit it for SI and cover-letter verification.

Present the verification results as a table:

| Check | manuscript.docx | supplementary_information.docx |
|-------|:-:|:-:|
| File size | X.X MB | X.X MB |
| Images embedded | N | N |
| Full-width main figures | Yes | N/A |
| Raw `[@...]` remaining | 0 | 0 |
| Bibliography entries | N | N |
| Tables | N | N |
| Line numbers configured | Yes | Yes |
| Double spacing | Yes | Yes |
| Footer page numbers | Yes | Yes |
| Figure-caption separators | N | N |
| Raw LaTeX fragments | 0 | 0 |
| Issues | None | None |

If any issues are found, report them and attempt to fix. If all checks pass, proceed to the report.

### Step 6: Report to User

```
Exported to output/share_ready/:
  - manuscript.docx (X.X MB) — main text + Online Methods + N figures + references
  - supplementary_information.docx (X.X MB) — N SI figures + N tables
  - cover_letter.docx (XX KB) — submission cover letter

Formatting:
  - 11pt body text, headings unchanged
  - Double-spaced manuscript and SI text
  - Nature-style numbered citations (N bibliography entries)
  - Continuous line numbers
  - Centred footer page numbers
  - 2cm margins
  - Main figures span the usable text width; SI figures fit within 14×16 cm
  - Figure-caption separator lines
  - Tables: three-line academic style, 8pt text
  - Page breaks after the abstract and before Methods, the references and the SI

Verification: all checks passed
```

## Formatting Summary

| Property | Value |
|----------|-------|
| Body font size | 11pt |
| Main/SI line spacing | Double |
| Table font size | 8pt (header bold) |
| Heading font size | Unchanged (pandoc default) |
| Line numbers | Continuous |
| Page numbers | Centred footer |
| Margins | 2cm all sides |
| Citation style | Nature (numbered superscript) |
| Table style | Three-line academic (top, header-bottom, table-bottom) |
| Main-manuscript images | Full usable text width |
| SI image max size | 14cm wide × 16cm tall |
| Figure-caption separator | Light grey rule (0.5pt) with 6pt gap |
| Page breaks | After abstract, before Methods, before references, before SI |
| Output folder | `output/share_ready/` |

## Notes

- The Nature CSL file is downloaded once and cached in the manuscript root as `nature.csl`
- The `\cite{key}` LaTeX syntax must be converted to pandoc `[@key]` syntax before export. If the manuscript still uses `\cite{}`, convert first:
  ```python
  # Convert \cite{key1, key2} -> [@key1; @key2]
  import re
  def convert_cite(match):
      keys = [k.strip() for k in match.group(1).split(',')]
      return '[@' + '; @'.join(keys) + ']'
  text = re.sub(r'\\cite\{([^}]+)\}', convert_cite, text)
  ```
- If the manuscript uses `format: latex`, this skill does not apply — use the LaTeX export pipeline instead
