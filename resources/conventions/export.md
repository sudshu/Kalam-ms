# Export & build commands

Build/export reference for manuscripts. The `/km-export-docx` skill owns Word export; this file is the LaTeX/PDF and journal-class reference. For the Nature-family two-PDF markdown build, each manuscript ships its own `drafts/.../build*.sh` (see `resources/manuscript_template/build.sh`).

## Share-ready folder layout

The DOCX bundling mode is manuscript-specific and is read from
`metadata.yaml → submission_docx_mode`:

- **`separate`**: create one main-manuscript DOCX and one Supplementary Information DOCX. The
  main file must not contain the SI heading, figures, tables or reference list. The SI file keeps
  its own title and bibliography. This mode supersedes the presence of any legacy combined-DOCX
  builder (COMPASS user decision 2026-08-21).
- **`combined` or absent**: use the combined layout below when the manuscript provides a combined
  builder.

### Combined layout (user decision 2026-07-23)

`output/share_ready/` is the single grab-and-share folder: it holds exactly one combined PDF
(main text + SI in one document) and its matching combined DOCX, named identically apart from
the extension (e.g. `<LastName>_<slug>_vX.Y.pdf` + `.docx`). Rules:

- When the SI is bundled inside the combined document, do **not** save separate supplementary
  artifacts (no standalone supplementary PDF or DOCX) — the SI PDF may still be built as a
  temporary intermediate for `pdfunite`, but it is not written to `exports/` or `output/`.
- The manuscript's build script copies the combined PDF into `output/share_ready/` on every
  build (the manuscript's own `drafts/build_exports/build_full.sh`, where it has one);
  the canonical build target in `exports/` (pointed to by `metadata.yaml → current_pdf`) is
  unchanged, so `/km-bump-version` and tidy-exports keep working.
- Versioned filenames in `output/share_ready/` are swept to `output/trash/` by the version-bump
  engine like any other output artifact.

## Page breaks at the logical boundaries

Owned by `/km-export-docx` (`skills/km-export-docx/scripts/add_page_breaks.py`). Breaks go into
the **draft markdown**, never into a rendered file, as a LaTeX `\clearpage` plus an OOXML
`<w:br w:type="page"/>` pair — each writer ignores the other's block — so the PDF and the Word
file paginate alike. One break each after the abstract and before Methods, the reference list
and the Supplementary Information. A `\clearpage`-only break is dropped from Word, because the
DOCX path strips raw LaTeX (Word cannot embed vector PDF figures).

The script is idempotent and `--remove` round-trips. A manuscript with its own build script
should invoke it there rather than by hand, running it before every target and honouring
`KM_PAGE_BREAKS=0` so the breaks can be skipped for a draft build.

## LaTeX to PDF
```bash
cd manuscripts/<name>/output
pdflatex ../drafts/manuscript.tex && bibtex manuscript && pdflatex ../drafts/manuscript.tex && pdflatex ../drafts/manuscript.tex
```

## LaTeX to Word
```bash
cd manuscripts/<name>
pandoc drafts/manuscript.tex --bibliography=references.bib --citeproc -o output/manuscript.docx
```

## Document classes by journal

| Journal Family | Document class | Bibliography style |
|---------------|---------------|-------------------|
| AGU (GRL, JGR, AGU Advances) | `agujournal2019` | `agufull08.bst` |
| Copernicus (ACP) | `copernicus` | `copernicus.bst` |
| PNAS | `pnasresearcharticle` | `pnas.bst` |
| Elsevier (RSE) | `elsarticle` | `elsarticle-harv.bst` |
| ACS (ES&T) | `achemso` | (built-in) |
| Nature / Nature Comms | `article` | `naturemag.bst` |
