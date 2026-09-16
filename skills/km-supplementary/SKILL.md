---
name: km-supplementary
description: "Use when the user wants to assemble, validate, or update the supplementary information (SI) document for a manuscript. Verifies all SI items are cited in the main text with correct prefix conventions, checks sequential numbering, reads SI figures visually, drafts captions and structure, and cross-references everything. Invoke with /km-supplementary. Use this whenever the user says 'supplementary', 'SI document', 'supporting information', 'assemble SI', 'check SI figures', 'supplementary information', or 'are all SI items cited'."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Assemble and Validate Supplementary Information

Build a complete supplementary information document, validate cross-references between the main text and SI, and ensure all items are correctly numbered and cited.

## When to Use

- When assembling SI for the first time
- Before submission, to verify SI completeness
- After adding or removing SI figures/tables
- When switching journals (SI prefix conventions change)
- As part of `/km-presubmit-audit`

## Prerequisites

- Main manuscript, resolved from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`/`.tex`)
- `metadata.yaml` with target journal
- Figure index at `figures/figure_index.md` (if it exists)
- SI figure files in `figures/si/` directory
- Journal profile in `resources/journal_profiles/`

---

## Step 1: Inventory SI Items from Figure Index

1. Read `figures/figure_index.md` to identify all figures and tables designated as supplementary.
   - SI figures are typically marked with "S" prefix (e.g., "Figure S1", "Table S1") or tagged as supplementary.
2. If `figure_index.md` does not exist, scan `figures/si/` for image files and ask the user to confirm which are SI items.
3. Build an inventory list:
   - SI Figures: S1, S2, S3, ... (with file paths)
   - SI Tables: S1, S2, ... (with source data paths if known)
4. Report the inventory to the user: "Found N SI figures and M SI tables."

## Step 2: Read the Main Manuscript

1. Resolve and read the main manuscript file(s) from `metadata.yaml` → `current_draft` (see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`) in their entirety.

   > **Preferred: use the shared inventory helper** instead of hand-rolled regex. Run `python skills/km-deep-read/scripts/inventory.py <manuscript_dir>`; its JSON `crossrefs` field already lists every `Supplementary Fig./Table N` (with the referencing location) and `existing_display_items`/`uncited_display_items` cover SI coverage. Fall back to the patterns below only if the helper is unavailable.
2. Extract every reference to supplementary material using regex patterns:
   - `Supplementary Fig. S\d+`, `Supplementary Figure S\d+`, `Fig. S\d+`, `Figure S\d+`
   - `Supplementary Table S\d+`, `Table S\d+`
   - `Supplementary Methods`, `Supplementary Text`, `Supplementary Note`
   - `Supplementary Information`, `SI`
3. Build a citation list: every SI item referenced in the main text, with the section where it appears.

## Step 3: Verify SI Prefix Conventions

Read the target family from `metadata.yaml → target_journal` and apply the correct main-text prefix. **The per-family SI-prefix table is single-sourced in `resources/conventions/journal_families.md` (§ Supplementary / Supporting Information prefix conventions); the journal profile in `resources/journal_profiles/` is authoritative if it differs.** In brief:

- **Nature** (Nature, NGeo, NCC, NComms): "Supplementary Fig. S1", "Supplementary Table 1", "Supplementary Note 1"; SI is a separate PDF.
- **AGU** (AGU Advances, GRL, JGR, GBC): "Figure S1" (no "Supplementary" prefix), "Table S1", "Text S1"; SI called "Supporting Information".
- **Copernicus** (ACP, BG, GMD): "Fig. S1"/"Figure S1", "Table S1"; SI called "Supplement".
- **PNAS**: "SI Appendix, Fig. S1", "SI Appendix, Table S1".

Check that all references in the main text use the correct prefix for the target journal. Flag any inconsistencies (e.g., mixing "Supplementary Fig." and "Figure S" in the same manuscript).

## Step 4: Verify Sequential Numbering

1. Check that SI figures are numbered sequentially: S1, S2, S3, ... with no gaps and no duplicates.
2. Check that SI tables are numbered sequentially: S1, S2, S3, ... (separate sequence from figures).
3. Check that the order of first citation in the main text matches the numbering:
   - The first SI figure cited should be S1, the second should be S2, etc.
   - If the order does not match, flag this and suggest renumbering.
4. Report any gaps, duplicates, or out-of-order citations.

## Step 5: Check SI Figure Files Exist

1. For each SI figure in the inventory, verify that the corresponding image file exists in `figures/si/`.
2. Check common extensions: `.png`, `.pdf`, `.jpg`, `.jpeg`, `.tiff`, `.eps`, `.svg`.
3. Report:
   - Files found with their paths and formats
   - Missing files (item in inventory but no file on disk)
   - Orphaned files (file on disk but not in inventory)

## Step 6: Draft SI Document Structure

Build the SI document with the following structure:

### Header
```markdown
# Supplementary Information

**<Manuscript Title>**

<Author list (mirror main manuscript)>

*Correspondence to: <corresponding author email>*
```

### Supplementary Figures Section

For each SI figure (S1, S2, S3, ...):

1. **Read the figure visually** using the Read tool on the image file.
2. Draft a descriptive caption that:
   - Starts with a bold title (e.g., "**Supplementary Figure S1 | Sensitivity analysis of...**")
   - Describes what the figure shows
   - Explains panels (a, b, c, ...) if present
   - Notes data sources, time periods, or methods as relevant
   - Matches the tone and detail level of main-text figure captions
3. If a caption already exists in `figure_index.md`, use it as the starting point and refine.

### Supplementary Tables Section

For each SI table:
1. Include the table title and description.
2. If the table data is available, format it in Markdown.
3. If the table is too large for Markdown, note that it will be provided as a separate Excel file.

### Supplementary Methods Section

1. Check the main manuscript's Methods section word count against the journal limit.
2. If Methods exceeds the limit, or if the user has flagged content for SI Methods:
   - Identify method details that can be moved to SI.
   - Draft a "Supplementary Methods" section with this content.
3. If no overflow is needed, skip this section.

## Step 7: Cross-Reference Check

Run a comprehensive cross-reference verification:

### 7a: Every SI item cited in main text
- For each SI figure and table in the inventory, verify it is cited at least once in the main manuscript.
- Report uncited items as "orphaned SI items."

### 7b: Every main-text SI reference has a corresponding item
- For each SI reference found in Step 2, verify the corresponding item exists in the SI document.
- Report references to non-existent items (e.g., text says "Fig. S5" but only S1-S4 exist).

### 7c: Summary table
```
| Item | Cited in Main Text? | File Exists? | Caption Drafted? |
|------|---------------------|--------------|------------------|
| Fig. S1 | Yes (Results, L142) | Yes | Yes |
| Fig. S2 | Yes (Discussion, L298) | Yes | Yes |
| Fig. S3 | NO | Yes | Yes |
| Table S1 | Yes (Methods, L401) | N/A | Yes |
```

Flag any row with a "NO" for user attention.

## Step 8: Write the SI Document

1. Check if `drafts/supplementary_information.md` already exists.
2. If it exists, show proposed changes and ask before overwriting.
3. Write the complete SI document to `drafts/supplementary_information.md`.
4. Confirm the file path and contents.

## Step 9: Final Report

Present a summary to the user:

```
## SI Assembly Report

- **SI Figures:** N (S1-SN)
- **SI Tables:** M (S1-SM)
- **Supplementary Methods:** Yes/No
- **All items cited in main text:** Yes / No (list orphaned items)
- **All main-text references resolved:** Yes / No (list broken references)
- **Numbering:** Sequential and correct / Issues found
- **Prefix convention:** Correct for <journal> / Issues found
- **Missing files:** None / List
```

If any issues were found, provide specific instructions for how to fix each one.

## Notes

- When reading SI figures visually, focus on what the figure communicates scientifically. Draft captions that help the reader understand the figure without needing to read the main text.
- For journals that use "Supporting Information" instead of "Supplementary Information" (AGU), adjust all terminology accordingly.
- If the SI is very large (>10 figures), consider suggesting the user group related figures and add subsection headings.
- Do not move content from the main text to SI without asking the user first.

## Delegation (do not duplicate)

This skill owns **SI assembly and integrity**: SI item citation coverage, family-correct SI prefix conventions, sequential SI numbering, and SI caption drafting. Everything else belongs to:

| Concern | Owner skill |
|---|---|
| SI figure image quality (DPI, fonts, colours, layout) | `/km-figures` |
| Word counts vs journal limits, typos/spelling, main-text structure, Word export | `/km-presubmit-audit` |
| DOI/journal/author/title correctness, duplicate keys | `/km-ref-check` |
| Terminology consistency and manuscript-level prose patterns | `/km-polish-audit` |
