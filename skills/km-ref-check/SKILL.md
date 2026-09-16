---
name: km-ref-check
description: "Use when the user wants to verify that bibliography references are correct before submission. Validates every cited BibTeX entry by cross-checking DOIs, journal names, author names, titles, and publication years against web sources. Catches Mendeley artifacts (e.g., 'Science (80-. ).'), fabricated DOIs, abbreviated vs full journal names, missing fields, duplicate keys, and bloat fields. Invoke with /km-ref-check. Use this whenever the user says 'check references', 'verify bibliography', 'are the DOIs correct', 'check bib file', 'validate citations', 'reference audit', or any request to verify that cited papers are correctly recorded."
---

# Reference Validation

Reviewers and production editors will catch wrong journal names, broken DOIs, and missing metadata. This skill validates every cited reference against web sources so those problems are fixed before submission.

The key principle: **never trust the bib file at face value.** Mendeley, Zotero, and manual entry all introduce errors. The only way to know a reference is correct is to verify it against the actual publication.

## When to Use

- Before submission or co-author circulation
- After importing references from a reference manager
- After manually adding entries
- When the user says "check references", "verify DOIs", "are my citations correct"
- As part of `/km-presubmit-audit`

## Step 1: Identify Cited References

1. Read `metadata.yaml` to find the bibliography file (usually `references.bib`)
2. Resolve the manuscript file(s) from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`) and extract all cited keys across them using the pattern `@Key` inside `[@...]` blocks

   > **Preferred: use the shared inventory helper** for extraction. Run `python skills/km-deep-read/scripts/inventory.py <manuscript_dir>`; its JSON `cite_keys` lists every cited `@key` and `missing_cite_keys` flags citations with no matching `.bib` entry — start from those instead of re-grepping. (This skill still owns the *correctness* validation of each entry.)
3. Report: "Found N unique cited keys. Starting validation."

## Step 2: Parse Each Cited Entry

For each cited BibTeX key, read its entry from the bib file and extract:

- Entry type (`@article`, `@misc`, `@book`, etc.)
- `author`
- `title`
- `journal` (for articles)
- `year`
- `doi`
- `volume`, `pages`, `number`
- Any bloat fields: `abstract`, `file`, `isbn`, `issn`, `keywords`, `pmid`, `publisher`, `url`, `annote`

Flag immediately if:
- The key is cited but not found in the bib file
- Required fields are missing (`author`, `title`, `year` always required; `journal` required for `@article`)
- Year in the entry doesn't match the year implied by the key name (e.g., `Smith2024` with `year = {2025}`)

## Step 3: Validate Against Web Sources

This is the critical step. For each cited entry, use **WebSearch** to verify metadata is correct. This catches errors that static bib-file checks cannot.

### What to search for

For each entry, search: `"[first author last name]" [year] "[key words from title]" doi`

### What to verify

For each entry, cross-check these fields against the search results:

#### 3a. Journal name
- Is it the correct journal? (e.g., the paper actually appeared in Nature, not Nature Communications)
- Is the name well-formed? Watch for Mendeley artifacts:
  - `Science (80-. ).` should be `Science`
  - `Proc. Natl. Acad. Sci.` should be `Proceedings of the National Academy of Sciences`
  - `Nat. Clim. Chang.` should be `Nature Climate Change`
  - `Atmos. Meas. Tech.` should be `Atmospheric Measurement Techniques`
  - `Atmos. Chem. Phys.` should be `Atmospheric Chemistry and Physics`
  - `J. Geophys. Res.` should be `Journal of Geophysical Research: Atmospheres`
  - `Geophys. Res. Lett.` should be `Geophysical Research Letters`
  - `Environ. Res. Lett.` should be `Environmental Research Letters`
  - `Phil. Trans. R. Soc.` variations should be standardized
- Are all journal names using the same convention? (All full names, or all abbreviated — pick one and flag inconsistencies)

#### 3b. DOI
- Is the DOI present?
- Is it well-formed? (Should start with `10.` — not a full URL like `http://...`)
- Does it resolve to the correct paper? (Check the DOI against the title/journal from web results)
- For preprints: is the DOI a preprint DOI (e.g., ESS Open Archive, arXiv) and is this noted?

#### 3c. Author names
- Does the first author match between the bib entry and the web result?
- Is the author field well-formed? (`Last, First and Last, First` format)
- Watch for `{others}` vs `and others` — both work in BibTeX but flag if inconsistent

#### 3d. Title
- Does the title match the actual publication? (Minor differences in capitalization are OK; completely different titles are a problem)

#### 3e. Year
- Does the year match the actual publication year?
- For papers published online in one year and in print in another, the year should match the version cited

#### 3f. Volume and pages
- Are these present for published articles? (Missing is acceptable for recent/in-press articles)
- For in-review or preprint papers, is this status noted? (`note = {in review}` or `note = {preprint}`)

### Batching strategy

To be efficient, batch entries by priority:
1. **First pass (high-value):** Validate entries that are most likely to have errors — those with missing DOIs, abbreviated journal names, entries imported from Mendeley (look for `file =` field as a Mendeley fingerprint), and entries for very recent papers (2025-2026)
2. **Second pass:** Validate remaining entries

Use parallel WebSearch calls where possible (multiple searches in one turn).

## Step 4: Check for Structural Issues

These don't require web searches:

### 4a. Duplicate BibTeX keys
Scan the entire bib file for keys that appear more than once. Report each duplicate with line numbers.

### 4b. Journal name consistency
Collect all journal names across cited entries. Flag if the same journal appears in both abbreviated and full forms.

### 4c. Bloat fields
Flag entries with fields that add file size but don't render: `abstract`, `file`, `isbn`, `issn`, `keywords`, `pmid`, `publisher`, `annote`. These are typically Mendeley artifacts.

### 4d. Entry type correctness
- Published journal articles should be `@article`, not `@misc`
- Datasets should be `@misc` with `howpublished`
- Preprints should be `@misc` with `note = {preprint}`
- Books should be `@book`
- WMO resolutions, government reports → `@misc`

### 4e. Orphan entries
Count entries in the bib file that are not cited in the manuscript. Report the count (not blocking, but good hygiene).

## Step 5: Present the Audit Report

```markdown
# Reference Validation Report — [Manuscript Short Name]

**Date**: YYYY-MM-DD
**Bibliography file**: references.bib
**Cited entries**: N
**Validated against web**: N
**Issues found**: N

## Critical Issues (will render incorrectly)

| # | Key | Issue | Current | Should be |
|---|-----|-------|---------|-----------|
| 1 | Cox2013 | DOI is a URL | `http://www.nature.com/...` | `10.1038/nature11882` |
| 2 | Chatterjee2017a | Malformed journal | `Science (80-. ).` | `Science` |

## Important Issues (inconsistent or incomplete)

| # | Key | Issue | Details |
|---|-----|-------|---------|
| 3 | Birner2023 | Abbreviated journal | `Nat. Clim. Chang.` → `Nature Climate Change` |
| 4 | Friedlingstein2025 | Missing DOI | Paper in review at ESSD |

## Verified Correct

| Key | Journal | DOI | Status |
|-----|---------|-----|--------|
| Keeling1960 | Tellus | 10.1111/... | OK |
| Conway1994 | J. Geophys. Res. | 10.1029/... | OK |
| ... | ... | ... | OK |

## Structural Issues

- **Duplicate keys**: [list or "None"]
- **Journal name inconsistencies**: [list]
- **Bloat entries**: N entries with abstract/file/isbn fields
- **Orphan entries**: N uncited entries in bib file
```

## Step 6: Fix Issues

After presenting the report, offer to fix:

1. **Malformed journal names** — Replace with correct full names
2. **Broken DOIs** — Replace URLs with proper DOIs, add missing DOIs where found
3. **Duplicate keys** — Remove the redundant entry (keep the one with better metadata)
4. **Abbreviated journal names** — Standardize to full names
5. **Entry type corrections** — Change `@article` to `@misc` for preprints, etc.
6. **Add missing metadata** — Volume, pages, DOI where available

Do NOT:
- Fabricate DOIs or metadata that you cannot verify
- Guess volume/pages for papers you can't confirm
- Remove bloat fields without asking (some users want to keep abstracts for their own reference)

If a DOI cannot be confirmed via web search, say so: "Could not verify DOI for [Key] — please check manually."

## Important: Epistemic Honesty for References

This skill previously led to fabricated DOIs being added to the bib file. To prevent this:

1. **Never invent a DOI.** If you cannot find a DOI via web search, leave the field empty and flag it.
2. **Never guess volume/pages.** If the paper is in press, mark it as such rather than fabricating page numbers.
3. **Always verify DOIs you add.** After adding a DOI, search for it specifically to confirm it resolves to the right paper.
4. **For preprints and in-review papers**, use the preprint DOI (e.g., ESS Open Archive, arXiv) and mark with `note = {preprint}` or `note = {in review}`. Do not claim a final journal DOI exists when it doesn't.
5. **If web search is unavailable**, skip the web validation step and only perform structural checks (Steps 2 and 4). Report that web validation was not performed.

## Delegation (do not duplicate)

This skill owns **bibliography validation**: DOI/journal/author/title/year correctness, duplicate keys, Mendeley artifacts, missing/bloat fields, and citation syntax. Everything else belongs to:

| Concern | Owner skill |
|---|---|
| Word counts vs journal limits, typos/spelling, structure, cross-references, Word export | `/km-presubmit-audit` |
| Terminology consistency and manuscript-level prose patterns | `/km-polish-audit` |
| Per-paragraph role/wordiness/repetition, cross-reference resolution, citation *existence* (not correctness) | `/km-deep-read` |
| Figure quality, caption drafting | `/km-figures` |

Composition: `/km-presubmit-audit` calls this skill as part of its citation/reference audit; run after `/km-full-manuscript` or after importing references from a reference manager.
