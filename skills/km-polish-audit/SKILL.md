---
name: km-polish-audit
description: "Use when the user wants to audit terminology and reader-facing prose before submission. Scans manuscript text and plotting code for inconsistent scientific terms, field-inappropriate jargon, concentrated em dashes, metadiscourse, repeated constructions, defensive caveat chains, and categorical interpretations whose scope exceeds the evidence. Produces a prioritized report without rewriting. Invoke with /km-polish-audit."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Flag any number reported as a finding that in fact follows from the definitions, any nominal parameter described as an equilibrium, and any threshold that changes meaning between sections.

# Terminology Consistency Audit

Reviewers notice when the same concept appears under different names in the text vs. figures vs. Methods. This skill systematically scans all manuscript files and figure-generation code to find inconsistent terminology and produces an actionable report the user can work through — either manually or by invoking `/km-polish-terms` for each term.

## When to Use

- Before submission or co-author circulation
- After a journal reframe (terminology may have shifted in some places but not others)
- After merging contributions from multiple co-authors
- When the user asks "is everything consistent?" or "audit my terminology"
- As part of a broader `/km-advisor` review

## Step 1: Load Manuscript Context

1. Read `metadata.yaml` to get `analysis_dir`, `target_journal`, and manuscript path
2. Read the journal profile to understand naming conventions (some journals prefer abbreviated forms)
3. Read `figures/figure_index.md` for the current figure inventory

## Step 2: Collect All Term-Bearing Text

Gather text from these sources — use Grep and Read, not Bash:

### Manuscript text
- `drafts/skeleton.md` or `drafts/manuscript.tex` — all sections including abstract, results, discussion, methods, cover letter
- `figures/figure_index.md` — figure table descriptions and all captions
- `notes.md` — may reveal intended terminology

### Figure code
- Read `analysis_dir` path from metadata, then:
  - Search for a centralized style/config file (glob for `*style*.py`, `*config*.py`, `*constants*.py`)
  - Search all `.py` files in the analysis directory for `label=`, `set_title`, `set_xlabel`, `set_ylabel`, `ax.text`, `ax.annotate`, and string literals in f-strings

### Supplementary Table definitions
- Table S1 or similar in the skeleton — predictor names, column headers, target-error definitions

## Step 3: Identify Key Scientific Terms

Extract all noun phrases that refer to:

1. **Data products and datasets** — e.g., "NOAA MBL", "NOAA Marine Boundary Layer", "MBL product", "surface network"
2. **Derived quantities** — e.g., "growth rate", "atmospheric growth rate", "AGR", "$G_{ATM}$", "CO₂ growth rate"
3. **Reference datasets used for comparison** — e.g., "inversion median", "GCB inversions", "in situ inversions", "inversion ensemble"
4. **Methods and models** — e.g., "five-predictor regression", "OLS model", "k=5 model", "multivariate regression"
5. **Budget terms** — e.g., "carbon budget imbalance", "BIM", "$B_{IM}$", "missing carbon", "budget residual"
6. **Satellite products** — e.g., "OCO-2 XCO2", "the satellite product", "satellite growth rate", "whole-atmosphere growth rate"
7. **Error/bias terminology** — e.g., "representativeness error", "representativeness bias", "sampling error", "structured error", "systematic bias"
8. **Conversion factors and constants** — e.g., "2.124 PgC ppm⁻¹", "fixed CF", "conversion factor", "mass-conversion factor"
9. **Statistical metrics** — e.g., "RMSE", "RMS", "R", "R²", "correlation"

## Step 4: Cluster Variants

For each concept, group all the different phrasings found across text and code. A "cluster" is a set of strings that refer to the same thing.

Example cluster:
```
Concept: "GCB inversion reference product"
Variants found:
  - "inversion median" (skeleton.md ×6, figure_index.md ×3)
  - "in situ inversion median" (skeleton.md ×2)
  - "GCP 2025 inversion ensemble median" (skeleton.md ×1)
  - "GCP inversion median" (skeleton.md ×1)
  - "in situ inversions" (skeleton.md ×1)
  - "Inversion median" (figure_style.py ×1, label in legend)
  - "GCB in situ inversions" (plot_budget_imbalance.py ×2)
  - "GCP 2025 inversion ensemble median" (plot_figure4.py ×1)
Locations: 17 total across 6 files
```

## Step 5: Score and Prioritize

Rate each cluster by:

1. **Variant count** — more variants = higher priority (3+ variants is a red flag)
2. **Cross-domain spread** — does the inconsistency span text AND figures? (worst case: the figure legend says one thing and the caption says another)
3. **Reader-facing impact** — is the term in the abstract, figure legend, or main results? (high impact) Or only in Methods/notes? (lower impact)
4. **Potential for reviewer confusion** — could a reviewer think these are different things? (e.g., "representativeness bias" vs "representativeness error" vs "sampling error" — a reviewer might ask "are these the same?")

Priority levels:
- **HIGH** — 3+ variants, appears in both text and figure code, reader-facing
- **MEDIUM** — 2 variants, or only in text, or only in lower-visibility sections
- **LOW** — minor stylistic differences (e.g., "CO₂" vs "CO2" in code comments), or in non-reader-facing locations

## Step 6: Present the Audit Report

Output a structured report:

```markdown
# Terminology Consistency Audit — [Manuscript Short Name]

**Date**: YYYY-MM-DD
**Files scanned**: [list]
**Terms audited**: [count]
**Issues found**: [count by priority]

## HIGH Priority

### 1. [Concept name]

| Variant | File | Count | Context |
|---------|------|-------|---------|
| "inversion median" | skeleton.md | 6 | running text |
| "in situ inversion median" | skeleton.md | 2 | running text |
| "Inversion median" | figure_style.py | 1 | legend label |
| "GCB in situ inversions" | plot_bim.py | 2 | legend + stats |

**Recommendation**: Define canonical forms — e.g., "GCB inversions" (text), "GCB inversion (in situ)" (figures). Use `/km-polish-terms` to apply.

### 2. [Next concept]
...

## MEDIUM Priority
...

## LOW Priority
...

## Text–Figure Cross-Check

| Figure | Legend label | Caption term | Skeleton term | Match? |
|--------|------------|--------------|---------------|--------|
| Fig. 2 | "Inversion median" | "inversion median" | "GCB inversions" | NO |
| Fig. 4 | "GCP 2025 inversion ensemble median" | "GCB inversion (in situ)" | "GCB inversions" | NO |

## Quick Wins
[List any single-edit fixes, like a lone typo variant or a style file label that would cascade to multiple figures]
```

## Step 6b: Punctuation and reader-flow audit

Beyond terminology, inspect patterns that impede the intended reader or obscure the scientific argument. Judge every instance in context. Do not use detector scores, lists of supposedly model-associated vocabulary, or an overall risk label.

### Em dash overuse

Count all em dashes (—) in the manuscript body text, excluding references. Use the canonical diagnostic of roughly one per 150 words or more than one in a sentence to identify passages for inspection; this is not a pass/fail quota.

For each em dash, classify its function:
- **Parenthetical aside** ("X — which does Y — means Z") → usually better as commas or parentheses
- **List introduction** ("three factors — A, B, and C — contribute") → colon or parentheses
- **Dramatic pause / consequence** ("the error peaks in 2024 — the record year") → keep only where the pause improves emphasis
- **Appositive definition** ("the MBL product — the standard in the GCB — is biased") → commas

Report the count, locations, functions, and only those replacements that make the passage clearer.

### Prose checks

Inspect for:

- **Metadiscourse and internal process**: sentences that announce importance, narrate what the writer considered, or walk through manuscript order instead of stating the scientific relationship.
- **Repeated constructions**: clusters of identical paragraph openings, sentence frames, or symmetrical contrasts that make the prose monotonous or overly staged.
- **Defensive structure**: repeated objection–rebuttal–reassurance sequences, duplicated caveats, or limitations that do not alter interpretation.
- **Field fit**: generic ML/CS terms where a more exact disciplinary term would help the recorded reader.
- **Claim language**: promotional or vague wording that obscures the result actually reported.
- **Evidence placement**: supporting audits interrupting the main narrative, or load-bearing tests missing from it, relative to `drafts/evidence_placement.md`.
- **Caption stance**: departures from the manuscript's recorded descriptive or assertion-led choice.

Present findings as:

```markdown
## Prose Style Flags

| Issue | Count | Locations | Reader effect | Priority |
|-------|------:|-----------|---------------|----------|
| Em-dash concentration | N | L12, L16, ... | [effect] | HIGH/MEDIUM/LOW |
| Repeated paragraph frame | N | L45, L82 | [effect] | HIGH/MEDIUM/LOW |
| Defensive caveat chain | N | L23 | [effect] | HIGH/MEDIUM/LOW |
| ... | | | |
```

Do not flag a word or construction in isolation. Explain the reader-facing problem and recommend a change only when context supports it.

### Categorical-claim and evidence-scope check

Inspect the title, abstract, assertion-led caption openings, central Results and Discussion sentences, and concluding synthesis for interpretations presented as universal facts, absolute causal statements, binary slogans, or general principles. For each candidate:

1. Classify it as a **definition**, **verified setting or method**, **direct result**, **established relationship**, or **interpretation/generalization**.
2. For an interpretation or generalization, identify the evidence domain: model, dataset, population, region or sites, period, experimental design, and any assumption material to the inference.
3. Read the whole paragraph and trace the statement to the cited result, figure, or analysis. The scope may be established in the sentence or its immediate context; do not require every sentence to repeat it.
4. Flag the statement only when its wording exceeds that evidence domain. Do not search mechanically for words such as *is*, *all*, *never*, or causal verbs.
5. Give the smallest scope-based revision that preserves the scientific point. Prefer naming the actual model, dataset, population, place, period, design, or uncertainty over adding generic *may*, *might*, or *could*.

Report these findings separately:

```markdown
## Categorical Claims and Evidence Scope

| Sentence / location | Claim class | Evidence domain | Scope problem | Priority | Minimal scoped revision |
|---|---|---|---|---|---|
```

Assign priority as follows:

- **HIGH** — a central title, abstract, caption lead, or conclusion makes a universal or causal claim that the evidence does not support, or conceals uncertainty or heterogeneity that changes the interpretation.
- **MEDIUM** — the claim is supported only in a limited domain, but that scope is omitted or ambiguous enough to invite a broader reading.
- **LOW** — slogan-like compression could be misread, although the surrounding context mostly bounds it.

## Step 7: Offer Next Steps

After presenting the report:

1. "Want me to fix the HIGH-priority items now? I'll use `/km-polish-terms` for terminology and `/km-academic-polish` for approved prose revisions."
2. "Want to discuss any of these before I make changes?" (some may be intentional — e.g., the abstract uses a longer form deliberately)
3. "Should I save this report to `notes.md` or a separate audit file?"

## What NOT to Flag

- **Intentional register differences**: It's normal for the abstract to use a longer form than the results section. Only flag if the *concept* is named differently, not if the *length* varies appropriately.
- **LaTeX math vs prose**: `$G_{ATM}$` and "atmospheric growth rate" are complementary, not inconsistent.
- **Citation keys**: `\cite{Friedlingstein2025}` is a citation key, not a term to harmonize.
- **Python variable names**: `inv_agr`, `bim_inv` are code internals. Only flag string literals that appear in figure output.
- **Historical/legacy files**: Files marked as "legacy" or "archive" in the figure index don't need to match current terminology.
- **Properly scoped direct statements**: Do not weaken definitions, verified settings or methods, established relationships, or exact findings whose evidence domain is explicit in the sentence or immediate context.

## Delegation (do not duplicate)

This skill owns **terminology consistency and manuscript-level prose-pattern checks** (field fit, em-dash concentration, metadiscourse, repeated constructions, defensive structure, evidence-placement drift, and recurrence of categorical claims that exceed their evidence domain). Everything else belongs to:

| Concern | Owner skill |
|---|---|
| Renaming/harmonizing a specific flagged term across text + figures | `/km-polish-terms` |
| Word counts vs journal limits, typos/spelling, structure, cross-references, Word export | `/km-presubmit-audit` |
| Per-paragraph wordiness/repetition, local claim-to-evidence scope, and inter-paragraph flow | `/km-deep-read` |
| Figure caption drafting, figure quality | `/km-figures` |
| DOI/journal/author/title correctness, duplicate keys | `/km-ref-check` |

Composition: after this audit, invoke `/km-polish-terms` for each flagged term and `/km-academic-polish` for approved sentence-level prose revisions; `/km-advisor` may call this audit as part of a pre-submission review; `/km-figures` caption review can reference the canonical terms from a recent audit.
