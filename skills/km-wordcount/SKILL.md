---
name: km-wordcount
description: "Use when the user wants to check manuscript word counts against journal limits, or needs to cut words to meet a target. Counts main-text words following Nature-family rules (excluding abstract, Methods, references, figure legends). If over the limit, identifies specific text to cut with prioritized recommendations. Invoke with /km-wordcount. Also use when the user says 'how many words', 'check word count', 'too long', 'cut 300 words', 'reduce word count', 'trim the manuscript', 'are we within the limit', or any request about manuscript length."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Manuscript Word Count and Reduction

Count words in a Kalam manuscript following journal-specific rules, then help the user cut to target if needed.

## Step 1: Gather Context

1. Read `metadata.yaml` to get `target_journal` and `journal_profile` path
2. Read the journal profile to extract:
   - Standard word limit for the paper type
   - Extended/discretionary limit (if any)
   - What is excluded from the count (typically: abstract, Methods, references, figure legends)
   - Abstract word limit
3. Resolve the manuscript file(s) from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`). Count the main-text file; if the manuscript is split, count each content file and sum. Fallback: `drafts/manuscript.md`.

## Step 2: Count Words

Run the bundled counting script on each resolved main-text file (pass multiple paths for a split manuscript):

```bash
python <skill_base_dir>/scripts/count_words.py <manuscript_dir>/<resolved_main_text.md>
```

This returns JSON with:
- `abstract_words` — abstract only
- `main_text_words` — opening + Results + Discussion, excluding captions
- `caption_words` — figure/table legends
- `methods_words` — Methods section
- `main_text_with_captions` — for reference
- `sections` — per-section breakdown

### Citations are not prose

Both citation styles are excluded before counting:

- pandoc markers, `[@Key2024]`;
- **plain-text author-year citations**, `(Smith et al., 2024)`,
  `(A et al., 2013; B and C, 2019, 2021)`, `(van der Werf et al., 2025)`, and the year
  in narrative form, `Smith et al. (2024)` → the name stays, the year goes.

This matters because several Kalam manuscripts write citations as author-year text and
convert them to numbered references only at build time. In the submitted PDF each one
prints as a superscript numeral, so counting the author-year string as prose overstates
the manuscript — by about 190 words, or 6%, on a 3,000-word Nature Article. Before this
was handled, example-paper v6.2 counted 3,180 against a ~3,000 limit and appeared over;
the true figure is 2,990.

Mixed parentheticals are handled segment by segment: `(Kaiser et al., 2012;
Supplementary Note 1)` keeps the cross-reference and drops only the citation. A
parenthetical with no trailing year is never touched, so `(Fig. 3d)`, `(Methods)`,
`(2001–2010 and 2015–2024)` and `(95% interval, 42–65%)` all still count.

## Step 3: Report

Present a clear summary table:

```
| Component         | Count | Limit | Status |
|-------------------|-------|-------|--------|
| Main text         |   NNN | X,XXX | over/under by N |
| Abstract          |   NNN |   200 | ok |
| Figure legends    |   NNN |   n/a | (not counted) |
| Methods           |   NNN | X,XXX | ok |
```

Include the per-section breakdown so the user can see where the words are concentrated.

If the manuscript is within limits, say so and stop (unless the user asked for cuts anyway).

## Step 4: Identify Cuts (if over limit or user requests)

Calculate how many words need to be cut to reach the standard limit. Then read the full main text carefully and identify cuts in four categories, ordered by priority:

### Category A — Repetitions
Same idea stated in multiple places (e.g., intro and Results both describe the network's tropical coverage). These are the highest-value cuts because removing them loses zero information.

**How to find them:** Compare each paragraph in the opening section against Results and Discussion. Flag any concept that appears in substantially similar wording in two or more places.

### Category B — Methods-level detail in main text
Quantitative specifics, predictor enumerations, diagnostic statistics, or caveats that belong in Methods or SI. The main text should state the result; the how belongs in Methods.

**How to find them:** Look for sentences that describe *how* something was computed rather than *what* was found. Enumerated lists of parameters, filter thresholds, or validation diagnostics are strong signals.

### Category C — Prior-work recaps
Detailed summaries of findings from cited papers. A single sentence with a citation is usually sufficient; multi-sentence recaps of prior results can be condensed.

**How to find them:** Look for passages that cite a specific paper and then spend 2+ sentences describing that paper's findings rather than the current manuscript's results.

### Category D — Methodological caveats
Defensive paragraphs addressing potential concerns (e.g., "a potential concern is X, but this does not affect Y because..."). These are important but often belong in Methods or SI, with a one-line reference in the main text.

**How to find them:** Look for sentences starting with "A potential concern...", "One limitation...", "This does not affect..." patterns in Results.

## Step 5: Present Cuts for Approval

Present each proposed cut individually in this format:

```
### Cut N — [Category] [Brief label] (~XX words)

**Current text:**
> [exact quote from manuscript]

**Why it can be cut:** [one sentence]

**Proposed replacement:**
> [shorter version, or "Delete entirely"]

Approve?
```

Wait for user approval before applying each edit. Apply using the Edit tool.

After each cut, do NOT recount words — keep a running tally by subtracting the estimated savings. Only rerun the counting script at the end or if the user asks for an updated count.

## Step 6: Final Count

After all approved cuts are applied, rerun the counting script and present an updated summary table showing before/after.

## Important Notes

- The word-counting script handles Markdown-specific artifacts (both citation styles, image
  links, LaTeX math, heading markers). Trust its output over manual estimates.
- If a count looks surprisingly high, check how the manuscript writes its citations before
  proposing cuts. A manuscript that is over only because of author-year citation text does
  not need trimming.
- Different journals have different exclusion rules. Always read the journal profile rather than assuming Nature-family defaults.
- When proposing replacement text, avoid em-dash-heavy phrasing. Match the author's voice — read a few paragraphs first to calibrate.
- Never cut scientific content or weaken claims. The goal is to say the same thing in fewer words, or move detail to Methods where it belongs.
- If the user specifies a target number of words to cut (e.g., "cut 300 words"), aim for that target plus a small buffer (~10%) to give room for adjustments.

## Delegation (do not duplicate)

This skill owns **counting narrative prose against journal limits** (via `scripts/count_words.py`) and proposing prioritized cuts. Everything else belongs to:

| Concern | Owner skill |
|---|---|
| Typos/spelling, acronyms, journal structure, cross-references, placeholders, Word export | `/km-presubmit-audit` |
| Terminology consistency and manuscript-level prose patterns | `/km-polish-audit` |
| Per-paragraph wordiness/repetition and inter-paragraph flow | `/km-deep-read` |
| DOI/journal/author/title correctness, duplicate keys | `/km-ref-check` |
| SI assembly, SI citation/prefix/numbering | `/km-supplementary` |
