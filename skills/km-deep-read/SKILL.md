---
name: km-deep-read
description: "Use when the user wants a deep, paragraph-by-paragraph and figure-by-figure read of a manuscript, driven by subagents that fan out across the main text, Methods and Supplementary Information. For each paragraph it checks role, wordiness, repetition, narrative flow, local claim-to-evidence scope, and unnecessarily negative characterization of cited prior work; it verifies that figures and internal cross-references resolve; and it reviews each figure with its caption. Invoke with /km-deep-read."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Flag any number reported as a finding that in fact follows from the definitions, any nominal parameter described as an equilibrium, and any threshold that changes meaning between sections.

# Deep Read — paragraph-by-paragraph and figure-by-figure manuscript audit

A granular, **agent-driven** read of a manuscript. A coordinator builds an inventory and the global cross-reference/citation maps, then **fans out subagents** — one per main-text paragraph and one per figure — each of which reads its unit closely and reports. Additional subagents cover Methods and Supplementary Information. The coordinator aggregates everything into a prioritized report and offers to apply fixes.

This skill is deliberately **complementary** to the other Kalam audit skills and must **delegate, not duplicate** (see "Delegation" at the end):
- deep bibliographic correctness (DOIs, journal names, web validation) → `/km-ref-check`
- terminology consistency and manuscript-wide recurrence of prose patterns or unscoped categorical claims → `/km-polish-audit`
- figure publication-quality standards and caption drafting from scratch → `/km-figures`
- word counts vs limits, typos, journal structure, Word export → `/km-presubmit-audit`

What this skill uniquely adds: **per-paragraph role / wordiness / local-repetition review**, **local claim-to-evidence scope review**, **inter-paragraph transition and narrative-flow checking**, **tone and prior-work-characterization review**, and **per-figure caption-to-panel review**, all via **subagent fan-out**, plus a **complete internal cross-reference and citation-resolution map**.

## Model

Run the **subagents on a capable model** (the Agent tool's default workflow subagent is fine; pass `model: "opus"` for the per-paragraph judgement if depth matters). The **coordinator** runs on the session model. Use the **Agent tool** for fan-out: issue several `Agent` calls in a single message so they run in parallel (the harness caps concurrency and queues the rest). For a very large manuscript you may instead use the Workflow tool, but only if the user has opted into it.

## Step 1 — Setup and inventory (coordinator)

1. Read `metadata.yaml` to find the manuscript files (`current_draft` lists them, e.g. `drafts/v2/cover_letter.md`, `main_text.md`, `methods.md`, `extended_data_SI.md`) and the `bibliography` and `journal_profile`.
2. Read the journal profile (for section expectations) and `figures/figure_index.md`.
3. Run the inventory helper from the manuscript directory:
   ```bash
   python <skill_base_dir>/scripts/inventory.py <manuscript_dir>
   ```
   (Use the project Python interpreter — whichever `python`/`python3` is on `PATH` for this workspace; do not hardcode an absolute environment path.) It prints JSON with: ordered paragraphs per file (numbered, with section headings), the figure list (image path + caption text + panel letters found in the caption), every internal cross-reference (`Fig. N`, `Table N`, `§`/section numbers, `Eq.`, `Supplementary Fig./Table N`) with the referencing location, the figures/tables/SI items that exist, and all cited `@keys` plus the bib keys.
4. Report the counts to the user: "*N* main-text paragraphs, *M* figures, *K* internal cross-references, *C* cited keys — fanning out subagents."

## Step 2 — Global cross-reference and citation map (coordinator, before fan-out)

Using the inventory (no subagents needed — this is a whole-manuscript view):
- **Figure/table/SI coverage:** every display item that *exists* is cited at least once in the text, and first citations appear in order (flag any never-cited item, and any out-of-order first mention).
- **Cross-reference resolution:** every in-text `Fig. N` / `Table N` / `§N` / `Eq. N` / `Supplementary Fig./Table N` points to an item that exists (flag dangling references, duplicated numbers, and main↔SI mismatches — e.g. logical vs physical SI figure numbers).
- **Citation existence:** every `@key` in the text exists in the `.bib`. Do **not** re-validate DOIs/journals/authors here — that is `/km-ref-check`'s job; note "deep bibliographic validation delegated to /km-ref-check."

Produce a compact cross-reference & citation integrity table.

### Step 2b — Comparative tone and prior-work characterization (coordinator)

Sweep all prose-bearing draft files for deficit-oriented descriptions of earlier studies, including context-dependent uses of terms such as *failed*, *could not*, *unable*, *required*, *only*, *limited to*, *lacked*, *did not*, *inferior* and *unlike prior work*. Do not flag these mechanically: read the complete sentence and paragraph and evaluate whether the language:

1. is necessary to establish a scientifically relevant distinction;
2. is directly supported by the cited paper rather than inferred from a different regime, experiment or objective; and
3. could be stated more accurately and collegially as a neutral difference in atmospheric regime, input data, observing system, or inference method.

When a sentence makes a strong negative claim about cited work, inspect the cited paper itself, preferably the published abstract and relevant Results or Conclusions, before recommending a change. Flag unsupported or unnecessarily adversarial framing, especially when a citation documents success in a different setting rather than failure in the setting claimed. Also flag repeated defensive negations about the present study when one precise limitation statement would suffice. Do **not** weaken genuine negative results, erase scientifically material limitations, or replace precise criticism with vague praise.

## Step 3 — Paragraph subagents (main text)

Fan out **one subagent per main-text paragraph** (introduction paragraphs + each Results-subsection paragraph + each Discussion paragraph). Batch the `Agent` calls a dozen-or-so at a time. Give each subagent (a) the exact paragraph text, (b) its section heading and position, (c) the global inventory (figure list, cross-ref targets, and the abstract + adjacent paragraph topics so it can judge repetition), (d) the **final sentence of the preceding paragraph and the opening sentence of the following paragraph**, so it can judge how this paragraph connects to its neighbours, and (e) the caption, Methods detail, or reported result directly cited by the paragraph, when available, so it can judge the evidence domain. Ask each to return a structured verdict:

> You are reviewing ONE paragraph of a manuscript. Paragraph text: «…». Section: «…». For context, the abstract and the topic sentence of every other paragraph are: «…». The figures/tables that exist are: «…». Report, concisely:
> 1. **Role** — in one phrase, what job this paragraph is supposed to do; and does it actually do it (yes / partly / no, with why).
> 2. **Wordiness** — quote any specific phrases/sentences that can be cut or tightened with no loss of meaning; give a one-line tighter rewrite only if clearly better.
> 3. **Repetition** — list any claim, number or sentence that repeats information already stated in the abstract or another paragraph (name where).
> 4. **Transition / flow** — does this paragraph's opening connect to the preceding paragraph (picks up its thread, with a logical connective), and does its ending set up the next? Flag abrupt jumps, missing connectives, and openings that merely re-state the previous paragraph or section instead of advancing.
> 5. **Cross-references / citations in this paragraph** — does every `Fig./Table/§/Eq./Supplementary` reference and every `@key` here look correct and resolve? Flag anything suspicious.
> 6. **Tone / prior-work characterization** — flag any unnecessarily negative, adversarial or defensive language. If the paragraph says that earlier work failed, could not do something, or required a particular method, state whether the cited source directly supports that characterization and suggest a neutral factual comparison when appropriate. Do not weaken genuine limitations.
> 7. **Categorical claim / evidence scope** — quote any interpretation framed as universally true, absolutely causal, or slogan-like. Classify it as a definition, verified setting or method, direct result, established relationship, or interpretation/generalization. For an interpretation/generalization, state whether its model, dataset, population, spatial, temporal, experimental, and assumption scope is clear from the sentence or immediate paragraph context and supported by the supplied evidence. If not, give the smallest scope-based revision; do not add generic hedging. Do not flag definitions, verified settings, established relationships, or direct findings within an explicit domain, and do not search mechanically for absolute words.
> 8. **Numerical clutter** — count the numbers in this paragraph. Flag it if the values crowd out the argument: quote only the numbers the argument turns on and name which of the rest belong in Methods, a table or the SI. Applies to the abstract and Results most of all.
> 9. **One-line verdict** — keep as-is / tighten / restructure, with the single highest-value change.
> Return raw findings, not prose. Do not rewrite the whole paragraph.

(If using the `schema` option, force a JSON object with these fields.)

**Coordinator narrative-flow read.** A per-paragraph subagent sees only its own boundaries, so the coordinator additionally reads each section as an *ordered sequence* to catch whole-arc problems single-paragraph views miss: redundant re-openings (a paragraph or section restating what was just established rather than advancing), repeated topic-sentence structures across sections (e.g. two sections both opening "X is accompanied by increasing …"), repeated slogan-like categorical openings or endings, and any break or non-sequitur in the argument's progression. Fold these into the flow findings. Leave manuscript-wide pattern counts and recurrence analysis to `/km-polish-audit`.

## Step 4 — Figure subagents

Fan out **one subagent per figure** (main + SI). Give each the figure image **path** (so it reads the image) and the caption text. Ask it to check:
- caption is **standalone** (every panel a, b, c… named and described; every symbol, colour, line and unit defined);
- caption **matches the panels actually shown** (no described panel missing from the image; no panel in the image undocumented);
- numbers in the caption are **consistent with the main text**;
- the figure is **cited** in the text (from the inventory);
- panel letters in the caption exist in the image and vice-versa.
Defer deep publication-quality (DPI, fonts, colour-blind safety, layout) to `/km-figures` — note it, don't redo it.

## Step 5 — Section subagents (Methods, Supplementary Information)

Run the same paragraph-level review on **Methods** and **Supplementary Information**, batching by subsection (each subagent takes one subsection and reviews its paragraphs one by one) to keep the fan-out manageable. Add SI-specific checks: every SI figure/table is cited from the main text; SI numbering is contiguous; Methods reproducibility statements are not placeholders.

## Step 6 — Aggregate and report

Merge all subagent returns. **Deduplicate repetition findings** across paragraphs (if two subagents both flag the same repeated fact, report it once, naming both locations). Write a prioritized report to `<manuscript_dir>/deep_read_report_<YYYY-MM-DD>.md`:

```
# Deep Read — <short_title> — <date>
Scope: <N paragraphs, M figures> across main text / Methods / SI.
Delegated: bibliographic correctness → /km-ref-check; terminology and manuscript-wide prose-pattern recurrence → /km-polish-audit; figure publication quality → /km-figures; word counts/typos/structure → /km-presubmit-audit.

## A. Cross-reference & citation integrity
<table: every figure/table/SI item — cited? in order? | every in-text reference — resolves? | every @key — in bib?>

## B. Paragraph findings (by section)
<per paragraph: role ✓/✗ | wordiness | repetition | transition/flow | local cross-ref/cite issues | claim scope | numerical clutter>
<plus a short 'Narrative flow' note per section: weak transitions, redundant re-openings, repeated topic-sentence structures, arc breaks>

## C. Categorical claims and evidence scope
<each flagged sentence | claim class | evidence domain | missing or excessive scope | minimal scoped revision | priority>

## D. Tone and prior-work characterization
<each flagged negative/comparative statement | cited support checked? | retain or neutral rewrite | rationale>

## E. Figure findings
<per figure: caption standalone? | panels match? | numbers match text? | cited?>

## F. Top issues, ranked
<the highest-value fixes first>
```

## Step 7 — Offer fixes

Present the top issues in chat. Offer to apply them in **batches with the user's approval** (wordiness trims, repetition cuts, broken cross-reference fixes) — the same report-then-fix pattern as `/km-ref-check` and `/km-presubmit-audit`. Apply with the Edit tool only after approval. **Never fabricate** a number, citation or figure detail; if a subagent is unsure, surface the uncertainty rather than asserting.

## Delegation (do not duplicate)

| Concern | Owner skill |
|---|---|
| DOI / journal / author / title correctness, duplicate keys, Mendeley artifacts | `/km-ref-check` |
| Terminology consistency and manuscript-wide recurrence of prose patterns or unscoped categorical claims | `/km-polish-audit` |
| Figure DPI/fonts/colours/layout, caption drafting from scratch, figure narrative | `/km-figures` |
| Word counts vs journal limits, typos/spelling, journal structure, Word export | `/km-presubmit-audit` |

This skill resolves cross-references; judges per-paragraph role, wordiness, repetition, local claim-to-evidence scope, inter-paragraph transition/flow, and prior-work characterization; and reviews caption-to-panel correspondence. It points the user to the skills above for everything else.
