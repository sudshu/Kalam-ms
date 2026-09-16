---
name: km-presubmit-audit
description: "Use when the user wants a deep pre-submission check of their manuscript. Orchestrates audits covering typos, journal limits, acronyms, cross-references, numerical consistency, repetition, unsupported categorical claims, characterization of prior work, references, SI completeness, and final Word export verification. Invoke with /km-presubmit-audit."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Flag any number reported as a finding that in fact follows from the definitions, any nominal parameter described as an equilibrium, and any threshold that changes meaning between sections.

# Pre-Submission Manuscript Audit

A systematic, checklist-driven audit that catches the issues reviewers and editors will flag — before they see the paper. This skill runs through every check that matters for a Nature-family journal submission, fixes what it can, flags what needs the user's input, and produces share-ready Word files at the end.

## When to Use

- Before submission to a journal
- Before circulating to co-authors for final sign-off
- After major revisions (reframing, figure changes, section restructuring)
- When the user asks for a "deep check", "final review", or "is this ready?"

## Prerequisites

- Manuscript in Markdown, resolved from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`)
- `metadata.yaml` with target journal and bibliography path
- Journal profile in `resources/journal_profiles/` (for word limits, formatting rules)
- `pandoc` and `python-docx` installed (for DOCX export step)

---

## Phase 1: Load Context

1. Read `metadata.yaml` to get: target journal, journal profile path, bibliography file, analysis directory, and `current_draft` (resolve the manuscript files per `resources/conventions/manuscript_files.md`)
2. Read the journal profile to extract hard limits:
   - Main text word count (excluding abstract, Methods, references, figure legends)
   - Abstract word count
   - Methods word count
   - Max display items
   - Max references
   - Structural requirements (headings, section order)
   - SI citation rules (e.g., "each SI item cited at least once with the word 'Supplementary'")
3. Read the full manuscript (the file(s) resolved from `current_draft`; a split manuscript has separate main-text/methods files)
4. Read the full SI (the SI file resolved from `current_draft`, e.g. `drafts/supplementary_information.md` or `drafts/extended_data_SI.md`) if it exists
5. Read the cover letter (`cover_letter.md`, per `current_draft`) if it exists
6. List all figure files in `figures/main/` and `figures/si/`

---

## Phase 2: Run Audit Checks

Run all checks below. For each, record PASS / FLAG / FAIL with the specific location (line number) and a one-line description. Collect all results into a structured audit report.

### A. Spelling and Typos

Scan the full manuscript text for misspellings. Common scientific manuscript typos to watch for:
- "systamatic" / "systamatically" (systematic)
- "sufficently" (sufficiently)
- "dependant" (dependent)
- "occured" (occurred)
- "seperately" (separately)
- Double words ("the the", "of of")
- Missing words (e.g., "imbalance of PgC yr-1" where a number was dropped)

Report every instance with line number and suggested fix.

### B. Word Counts

**Delegated to `/km-wordcount`** (do not re-implement the exclusion rules here — its engine `skills/km-wordcount/scripts/count_words.py` is the single counting authority). Resolve the manuscript files from `current_draft` and run:

```bash
python skills/km-wordcount/scripts/count_words.py <main_text.md> [<methods.md> ...]
```

Present its per-section table (abstract / main body / Methods, with the sub-section breakdown) against the profile limits, flagging any section over limit with the exact count, limit, and margin. For guidance on which text to cut when over, hand off to `/km-wordcount` Steps 4–5.

### C. Structural Compliance

Check against the journal profile's structural requirements:

- [ ] Correct section order (e.g., for Nature Geoscience: Opening paragraph → Results → Discussion → Methods)
- [ ] No forbidden headings (e.g., no "Introduction" or "Conclusions" for Nature Geoscience)
- [ ] Abstract is unreferenced (no `[@...]` citations)
- [ ] Abstract is a single paragraph
- [ ] No footnotes
- [ ] Data Availability and Code Availability statements present
- [ ] Acknowledgements and Author Contributions sections present (even if placeholder)

### D. Acronym Audit

Find all acronyms (2+ consecutive uppercase letters) used in the body text. For each, check whether it is expanded on first use. Common acronyms to verify:

- Agency names: NOAA, NASA, ESA, WMO
- Units: PgC, GtC, ppm
- Statistical terms: RMS, RMSE, OLS, LOO, IQR
- Hemispheres: NH, SH
- Chemical/technical: XCO2, STE, MBL, ENSO, PBL

Report any acronym used before its expansion. Note: chemical formulas (CO2, CH4) and standard SI units typically don't need expansion.

### E. Citation and Reference Audit

Run the full `/km-ref-check` workflow here. This invokes the reference validation skill which:

1. Extracts all cited keys and verifies they exist in the .bib file
2. **Web-validates** every cited entry: cross-checks DOIs, journal names, author names, titles, and years against online sources
3. Catches Mendeley artifacts, malformed journal names, broken/fabricated DOIs
4. Flags abbreviated vs full journal name inconsistencies
5. Reports duplicate BibTeX keys, missing fields, bloat fields
6. Checks citation syntax (comma vs semicolon separators, missing `@` prefix)
7. Counts unique cited keys and compares against the journal's reference limit

Invoke by following the steps in `skills/km-ref-check/SKILL.md`. Present the reference validation report as part of the overall audit report.

### F. Display Item Cross-References

This is a critical check — journals reject manuscripts where SI items are not cited.

> **Preferred: use the shared inventory helper** rather than manual grep. Run `python skills/km-deep-read/scripts/inventory.py <manuscript_dir>` — its JSON gives `existing_display_items`, `uncited_display_items`, `crossrefs`, and `dangling_crossrefs`, which directly answer F1/F4/F5.

#### F1. Main figures
For each figure file in `figures/main/`, verify it is cited at least once in the body text (not just in its own legend). Check for "Fig. N" pattern.

#### F2. SI figures / F3. SI tables
**Delegated to `/km-supplementary`** (owns SI citation coverage, family-correct SI prefix, and sequential SI numbering). Run its Steps 2–4 and fold the result in here; do not re-derive the prefix rules.

#### F4. Sequential citation order
Verify figures are first cited in numerical order (Fig. 1 before Fig. 2, etc.; S1 before S2, etc.). Flag out-of-order citations.

#### F5. Display item count
Count main display items (figures + tables in main text) and compare against journal limit.

### G. Figure Quality Review

**Delegated to `/km-figures`** (owns DPI/fonts/colours/layout and caption quality). Run its figure-quality review (Step 3) over `figures/main/` and the SI figures, and fold the flagged issues into this audit's report. Do not re-implement the visual checks here.

### H. Numerical Consistency

Cross-check key statistics reported in multiple places:

1. Build a table of key numbers (R values, RMSE, percentages, year counts, etc.) and where they appear (abstract, results, discussion, figure captions, SI tables, figure insets)
2. Flag any mismatches
3. Verify unit conversion math (e.g., ppm * 2.124 = PgC)

### I. Information Repetition

**Delegated to `/km-deep-read`** (owns per-paragraph wordiness/repetition and inter-paragraph flow). If a deep read has not been run recently, invoke it for the repetition check; surface any over-repeated claim (the same fact in opening AND results AND discussion) or near-verbatim Results/Discussion passages it reports.

### J. Cover Letter Consistency

If a cover letter exists, verify all numbers and claims match the manuscript.

### K. Placeholder Check

Scan for common placeholder patterns:
- "[To be added]", "[TBD]", "[TODO]"
- "et al." in author list (incomplete)
- Empty sections
- "XX" or "??" placeholder numbers

### L. Comparative Tone and Characterization of Prior Work

**Delegated to `/km-deep-read`**, which owns the contextual paragraph-level check. Run its comparative-tone and prior-work-characterization sweep and surface every statement that portrays cited work as having *failed*, being *unable* to do something, or *requiring* a method when that framing is stronger than the source supports or when a neutral comparison of regime, data or method is more accurate. Strong negative claims about prior studies must be checked against the cited paper, not inferred from its title or from a different experimental setting. Do not flag negative words mechanically, weaken genuine negative results, or remove scientifically necessary limitations.

### M. Categorical Claims and Evidence Scope

Delegate the local paragraph-to-evidence check to `/km-deep-read` and the manuscript-wide recurrence check to `/km-polish-audit`. Surface every flagged title, abstract sentence, assertion-led caption opening, central Results or Discussion sentence, and concluding synthesis. For each item, report its location, claim class, evidence domain, missing or excessive scope, priority, and smallest scope-based revision.

- **FAIL / Critical** — a central universal or causal claim exceeds its supporting model, dataset, population, region, period, experimental design, or assumptions; suppresses uncertainty or heterogeneity that changes the interpretation; or presents a controlled/model result as an observed real-world fact. Any unresolved HIGH-priority item in this category blocks a **READY** submission status.
- **FLAG / Important** — the result is supported only within a limited domain, but the sentence or immediate context leaves that domain ambiguous.
- **PASS** — definitions, verified settings or methods, established relationships, and direct results within an explicit evidence domain.

Judge complete sentences in their paragraph context. Do not flag absolute-looking words mechanically, require scope to be repeated in every sentence, or replace precision with generic *may*, *might*, or *could*.

---

## Phase 3: Present Audit Report

Present findings as a prioritized table:

### Critical (must fix before submission)
| # | Category | Issue | Location |
|---|----------|-------|----------|

### Important (should fix)
| # | Category | Issue | Location |
|---|----------|-------|----------|

### Placeholders (need co-author input)
| # | Category | Issue | Location |
|---|----------|-------|----------|

### Passed checks
Brief summary of what looks good (gives confidence the audit was thorough).

---

## Phase 4: Fix Issues

Ask the user which issues to fix now. For issues that need user input (ambiguous numbers, missing values, preference choices), use AskUserQuestion to batch the questions efficiently.

Then apply fixes in this order:
1. Typos and spelling
2. Missing numbers and factual errors
3. Unsupported categorical claims or missing evidence scope
4. Unsupported or unnecessarily negative characterization of prior work
5. Citation syntax
6. Numerical inconsistencies (reconcile text vs SI)
7. Word count trimming (abstract first, then body)
8. Acronym expansions
9. Cross-reference fixes (figure citation order, missing SI citations)
10. Reference cleanup (remove duplicates)
11. Paragraph splitting (readability)
12. Repetition consolidation

After each category, briefly report what was changed.

### Figure fixes
If figures need re-plotting (embedded titles, unit inconsistencies), locate the plotting script using `Figure_remake_instructions.md` or by searching the analysis directory. Read the exact run command from the remake instructions (including any `--suffix` or other arguments). Make the minimal code changes, re-run the script with the correct arguments, and copy the output to the manuscript figures directory.

---

## Phase 5: Recount and Verify

After all fixes:
1. Recount word counts (abstract, body, methods) and confirm within limits
2. Re-verify all cross-references still intact
3. Re-run the categorical-claim and evidence-scope check on the title, abstract, caption leads, central Results/Discussion statements, and conclusion
4. Confirm that no HIGH-priority categorical claim remains unresolved
5. Report final word counts vs limits

---

## Phase 6: Export to Word

Invoke the `/km-export-docx` workflow:
1. Run pandoc to convert manuscript and SI to .docx
2. Post-process with python-docx formatting (11pt, line numbers, margins, tables)
3. Verify exported files:
   - All figures embedded
   - No raw `[@...]` brackets remain
   - References section present with numbered bibliography
   - Tables render cleanly
   - Math renders (subscripts, superscripts, equations)

Report file sizes and verification results.

---

## Phase 7: Final Summary

```
PRE-SUBMISSION AUDIT COMPLETE

Word counts:
  Abstract:  XXX / 200  [OK/OVER]
  Main body: XXX / X,XXX [OK/OVER]
  Methods:   XXX / X,XXX [OK]
  References: XX / ~50   [OK]

Fixes applied: X critical, X important
Remaining placeholders: X (need co-author input)
Unresolved HIGH-priority categorical claims: X [0 required for READY]
Figure remakes: X
Submission status: READY / NOT READY

Exported to output/share_ready/:
  manuscript.docx (X.X MB)
  supplementary_information.docx (X.X MB)
```

---

## Delegation (do not duplicate)

This skill is the **pre-submission orchestrator**. It owns the mechanical-compliance checks that have no other home — typos/spelling, acronym expansion, journal structural compliance, display-item cross-reference coverage, placeholder scan, cover-letter consistency, and the final Word-export gate — and it invokes the owners below for everything specialized rather than re-implementing them:

| Concern | Owner skill |
|---|---|
| Word counts vs journal limits, prioritized trimming | `/km-wordcount` (engine: `scripts/count_words.py`) |
| DOI/journal/author/title correctness, duplicate keys, Mendeley artifacts, citation syntax | `/km-ref-check` |
| Figure DPI/fonts/colours/layout, caption quality | `/km-figures` |
| SI citation coverage, family-correct SI prefix, sequential SI numbering | `/km-supplementary` |
| Per-paragraph role/wordiness/repetition, local claim-to-evidence scope, inter-paragraph flow, cross-reference resolution, comparative tone and prior-work characterization | `/km-deep-read` |
| Terminology consistency and manuscript-wide recurrence of prose patterns or unscoped categorical claims | `/km-polish-audit` |
| Word/DOCX export mechanics | `/km-export-docx` |

## Notes

- This skill is designed for Nature-family journals but adapts to any journal profile in `resources/journal_profiles/`. The specific checks (section structure, SI citation rules, display item limits) are all read from the profile at runtime.
- The skill invokes `/km-polish-audit` for terminology and manuscript-wide prose patterns and pairs with `/km-advisor` for scientific-content review.
- A completed audit establishes compliance with the checks above; it does not predict editorial outcome.
