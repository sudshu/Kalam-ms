---
name: km-full-manuscript
description: "Use when starting Stage 3 (Full Manuscript). Writes complete paper text section-by-section, following the skeleton outline. Drafts each section interactively, integrates citations, and exports to PDF and Word. Adapts to journal-specific structure (NGeo, NComms, AGU, etc.). Invoke with /km-full-manuscript."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Stage 3: Full Manuscript

Write the complete paper following the confirmed skeleton.

## Prerequisites

1. Read `metadata.yaml` — verify `stage` is `skeleton_complete` or `drafting`
2. Update stage to `drafting`
3. Read `../../resources/User/USER.md` for writing style and impact claims
4. Read the target journal profile from `../../resources/journal_profiles/`
5. Read the skeleton (`drafts/skeleton.md` or `drafts/skeleton.tex`)
6. Read `figures/figure_index.md` for finalized figures and captions
7. Read `references.bib` — know what citation keys are available
8. Inventory existing section drafts (e.g., `drafts/methods.md`) — do NOT re-draft sections that already exist unless the user requests revisions
9. Read `notes.md` for decision log and support material
10. Read `research/style_refs/style_profile.md` for the reader, voice, narrative, and title/caption contract
11. Read `drafts/evidence_placement.md`; do not draft until every central result and control has an assigned destination

## Detect Format

Check `metadata.yaml` field `format`:
- `markdown_latex` → draft in Markdown (`.md`) with `\cite{}` references, convert to LaTeX later
- `latex` → draft directly in LaTeX (`.tex`)
- If absent, ask the user

## Output Layout

Write to the files named in `metadata.yaml` → `current_draft` (see `resources/conventions/manuscript_files.md`). The template default is the Nature-family 4-file split (`cover_letter.md` + `main_text.md` + `methods.md` + `extended_data_SI.md`); a single-file manuscript uses `drafts/manuscript.md`. The layout snippets below use `drafts/manuscript.md` as shorthand for "the main-text file" — write to whatever `current_draft` specifies.

## Journal-Adaptive Structure

Read the journal profile and determine the article structure. Do NOT impose a generic template.

### Nature Family (Nature Geoscience, Nature Climate Change, Nature Communications)

```
drafts/manuscript.md (or .tex):
  - Opening paragraphs (NO "Introduction" heading — NGeo/NCC format)
  - Results (with subheadings)
  - Discussion (NO subheadings)
  - Online Methods (length and placement from the current journal profile; may already be drafted as methods.md)
  - Data Availability
  - Code Availability
  - Acknowledgements
  - Author Contributions

Abstract: format, length and citation convention from the current journal profile
No "Conclusions" section
```

**Drafting order for Nature family:**
1. Opening paragraphs ("Introduction")
2. Results (section by section, matching skeleton §1–§N)
3. Discussion
4. Abstract (LAST — it summarizes the final paper)
5. Online Methods — if already drafted, review and integrate; if not, draft
6. Supporting sections (Acknowledgements, Author Contributions, Data/Code Availability)

### AGU Family (AGU Advances, GRL, JGR)

```
drafts/manuscript.tex:
  - Abstract + Plain Language Summary + Key Points
  - Introduction
  - Methods / Data
  - Results
  - Discussion
  - Conclusions
  - Acknowledgements
  - Data Availability
```

**Drafting order for AGU:**
1. Introduction
2. Methods / Data
3. Results
4. Discussion
5. Conclusions
6. Abstract + Key Points + Plain Language Summary (LAST)

### Other journals

Read the journal profile and adapt. When in doubt, ask the user about the expected section structure.

## Writing Style Rules

From `../../resources/User/USER.md` and the manuscript style profile:
- **Reader-centred**: Write at the recorded readers' level and make the argument explicit for a broad Nature/Science audience
- **Field-native**: Name the scientific process or quantity instead of defaulting to ML/CS language
- **Direct**: Use concrete verbs and visible actors where useful; passive voice remains available when the scientific object is the natural topic
- **Quantitative**: Numbers with uncertainties ("reduced by 40% ± 5%", not "substantially reduced")
- **Minimal hedging**: On well-supported claims, be direct. Hedge only where evidence is genuinely uncertain.
- **Honest about limitations**: State each material limitation where it affects interpretation, normally once
- **Concise**: Every sentence must earn its place (especially for word-limited journals)
- **No code-style names**: Use plain-English descriptors in running text; code variable names belong in SI tables only
- **No internal process prose**: Remove guided-tour, agent-reasoning, and imagined-review language

## Process

### Phase 1: Pre-Draft Inventory

Before writing anything:

1. **List existing drafts** — check for pre-drafted sections:
   - `drafts/methods.md` or methods sections in `drafts/skeleton.md`
   - Any other partial drafts
2. **List sections still needed** — compare skeleton structure against existing drafts
3. **Check the contract and ledger** — report the readers, central contribution, narrative arc, caption stance, and Main/Methods/Extended Data/SI placement decisions
4. **Present the drafting plan to the user:**
   ```
   Existing:  methods.md (2,240 words) — Online Methods ✅
   To draft:  Opening paragraphs, Results §1–§5, Discussion, Abstract
   Order:     Opening → Results §1 → §2 → §3 → §4 → §5 → Discussion → Abstract
   ```
5. Get user confirmation before starting

### Phase 2: Section-by-Section Drafting

Draft ONE section at a time. For each section:

1. Read the skeleton bullet points for this section
2. Read the corresponding figure(s) visually — understand what the reader will see
3. Expand bullet points into polished scientific prose
4. Integrate `\cite{key}` commands — verify each key exists in `references.bib`
5. Reference figures using the journal's convention (e.g., "Fig. 1", "Supplementary Fig. S1")
6. Check word count against the section's target from the skeleton
7. Check every supporting test against `drafts/evidence_placement.md`; keep load-bearing evidence in Main and supporting diagnostics in their assigned destination
8. Present the drafted section to the user
9. Get feedback and revise
10. **Only proceed to the next section after user approval**

**Section-specific guidance:**

**Opening paragraphs (Nature family):**
- No heading. Start directly with the broad context.
- Build the recorded context → unresolved question → decisive test → finding → consequence narrative; the exact paragraph count is manuscript-specific
- Begin at the broad reader's level and define specialist terms only when they become necessary
- State the paper's contribution and its quantitative basis without recounting the analysis chronology
- Cite sparingly and follow the current journal profile; save detailed citations for Results and Methods where appropriate
- Target: word count approved in the skeleton

**Results:**
- One subsection per skeleton §, each tied to a figure
- Normally lead with the comparison, measurement, or finding; cite the figure where it naturally supports the sentence
- Use numbers, uncertainties, and comparisons where they are needed to interpret the claim
- Refer to supporting material briefly and only where it helps the reader assess the claim
- Keep interpretation minimal — save mechanism arguments for Discussion
- Target: word count from skeleton per subsection

**Discussion:**
- No subheadings (Nature family) — but clear paragraph structure
- Organize around interpretation, relation to previous work, consequence, and the material boundary of the claim; choose the order that serves this paper
- State each material limitation once and do not stage the prose as objection, rebuttal, and reassurance
- End with a precise scientific conclusion, not a slogan

**Abstract:**
- Draft LAST, after all other sections are finalized
- Follow the sentence plan from the skeleton
- Check length and citation convention against the current journal profile
- Include one quotable claim
- Draft 2 versions if the user wants options

### Phase 3: Integrate Online Methods

If `drafts/methods.md` already exists:
1. Read it
2. Check consistency with the main text just drafted (numbers, terminology, figure references)
3. Flag any discrepancies
4. Ask user if any updates are needed

If Methods not yet drafted:
1. Draft following the skeleton's Methods outline
2. Follow the same interactive one-section-at-a-time process

### Phase 4: Assemble and Write

**For Markdown-first workflow (`format: markdown_latex`):**

1. Write `drafts/manuscript.md` — the complete assembled paper:
   - Abstract
   - Opening paragraphs
   - Results (all subsections)
   - Discussion
   - Online Methods (copied from methods.md or drafted fresh)
   - Data Availability, Code Availability
   - Acknowledgements, Author Contributions
   - References (as `\cite{}` keys — resolved at LaTeX/pandoc stage)

2. Each figure placement marked with:
   ```markdown
   ![Fig. 1](../figures/main/Figure_1.png)
   **Fig. 1 | Caption title.** Caption text...
   ```

**For LaTeX workflow (`format: latex`):**

1. Write `drafts/manuscript.tex` using the journal-appropriate document class
2. Include `\begin{figure}` environments with `\includegraphics`
3. Embed references with `\cite{}`
4. Include `\bibliography{references}` or inline `.bbl`

### Phase 5: Quality Checks

Before declaring the draft complete, verify:

| Check | How |
|-------|-----|
| **Word count** | Count main text (excl. abstract, methods, refs, captions) against journal limit |
| **Figure count** | Verify against the current journal profile |
| **Reference count** | Verify against the current journal profile |
| **All `\cite{}` keys** | Grep for `\cite{` and verify each key exists in `references.bib` |
| **All SI cross-refs** | Every SI figure/table cited at least once in main text or Methods |
| **Terminology consistency** | No code-style names in text; plain-English throughout |
| **Field-native language** | Generic ML/CS terms replaced where a more accurate disciplinary term exists |
| **Number consistency** | Key numbers (R, RMSE, years, ppm values) match between abstract, results, methods, and captions |
| **Figure numbering** | Skeleton, figure_index table, and captions all use same SI numbering |
| **Self-citations** | Count and verify 3–7 range |
| **Evidence placement** | Every result follows the ledger; no load-bearing test is hidden and supporting audits do not interrupt the main narrative |
| **Reader flow** | Paragraph roles are clear; no internal-process narration or repeated defensive caveats |

Report the results to the user as a compliance table. Then obtain human approval of the assembled narrative before running a global line-by-line polish or submission audit.

### Phase 6: Export

**Build commands are single-sourced** in `resources/conventions/export.md` (PDF via the manuscript's `build.sh` / pandoc + LaTeX document class per journal). Do not carry divergent pandoc incantations here.

- **PDF**: run the manuscript's `build.sh` (or the commands in `resources/conventions/export.md`) to produce the submission PDF(s).
- **Word (.docx)**: delegate to `/km-export-docx` (owns the pandoc + python-docx formatting and verification). Do not hand-roll the pandoc command.

Report:
- Word count, figure count, reference count
- Journal compliance summary
- Files created

Update `metadata.yaml` stage to `draft_complete`

### Phase 7: Post-Draft

Suggest next steps:
- Run `/km-advisor` for simulated peer review (full manuscript mode — 3-reviewer panel)
- Run `/km-polish-audit` for terminology consistency check
- Share draft with co-authors
- After revisions, update stage to `submitted` when paper is submitted
