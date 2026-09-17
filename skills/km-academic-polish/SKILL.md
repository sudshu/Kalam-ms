---
name: km-academic-polish
description: "Use when the user wants manuscript prose polished to read like published academic writing — e.g. 'polish the writing', 'make it sound more academic', 'academic writing polish', 'improve the prose', 'language pass', 'smooth the text'. Walks the abstract, main text and figure captions LINE BY LINE and rewrites sentences for register, flow and concision — never changing a number, claim, citation or work marker. Calibrates against real exemplar papers downloaded from the target journal (style profile cached per manuscript). Distinct from /km-polish-audit (detects style problems, does not rewrite) and /km-polish-terms (harmonizes one term). Invoke with /km-academic-polish [abstract|main|captions|all] [--dry-run]."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Academic Writing Polish (line-by-line, journal-calibrated)

Rewrites manuscript prose so it reads like the target journal's published papers. The unit
of work is the **sentence**: every line of the abstract, main text and figure captions is
read and either kept or rewritten, with each change recorded in a before/after ledger.
Content is inviolable — this skill changes *how* things are said, never *what* is said.

## Hard invariants (check these BEFORE and AFTER — Step 5)

Never change, delete, move or reformat:
1. **Numbers** — every value, unit, CI, percentage, p-value, sample size, figure/table number.
2. **Citations** — `\cite{...}` / `[@...]` commands and their keys, and where they attach.
3. **Work markers** — `[CHECK: ...]`, `[PENDING: ...]`, `[TBD ...]`, HTML comments.
4. **Claims** — the scientific content, hedging *level* (a "suggests" must not become a
   "demonstrates" or vice versa), and the logical order of arguments.
5. **Format budgets** — abstract word limit, heading text, and the manuscript's recorded
   descriptive or assertion-led caption stance.
6. **Spelling convention** — detect whether the manuscript uses British or American spelling
   and stay with it.

If a sentence cannot be improved without touching an invariant, leave it and flag it in the
ledger under "needs-author" instead.

## Step 0: Load context and back up

1. Read `metadata.yaml` → `target_journal`, manuscript stage, paths; load
   `resources/journal_profiles/<journal>.md` if present (word limits, abstract format).
   Read `resources/conventions/writing_style.md`, the **canonical house ruleset**, and
   `research/style_refs/style_profile.md`, which should have been approved before the
   skeleton. Apply its reader contract, title/caption stance, and evidence policy. Match
   the author voice recorded in the profile: when approved samples exist, weight the lead
   author and principal coauthor equally.
2. Resolve the three text sources:
   - **Abstract + main text**: `drafts/manuscript.md` (or the stage-appropriate draft).
   - **Figure captions**: the caption blocks in `figures/figure_index.md` (and, if captions
     are duplicated inside the manuscript, note that both copies must receive identical edits).
3. Scope from the invocation argument: `abstract`, `main`, `captions`, or `all` (default).
   Methods is included only if the user asks (`methods`) — its register is deliberately drier.
4. **Back up before editing**: copy each file to be edited to
   `agent-reviews/backups/<file>_<YYYYMMDD_HHMM>.md`. If the repo is clean, note the HEAD
   commit in the ledger instead. Never edit without one of the two.

## Step 1: Style calibration — real exemplars from the target journal

Goal: a concrete, cached style profile derived from how the target journal actually reads,
not from generic "academic writing" intuition.

1. Check for a cached profile at `research/style_refs/style_profile.md`. If present and the
   target journal has not changed, reuse it and skip to Step 2. A missing profile at this
   stage is a workflow warning: create it now, but record that calibration occurred after
   drafting rather than before the skeleton.
2. Otherwise gather **3–5 recent papers from the target journal in a neighbouring field**
   (close enough to share register, distant enough not to bias content):
   - Find candidates with the built-in WebSearch/WebFetch tools (the standing rule for online
     search since 2026-08-12); do not shell out to the Codex or Gemini CLI unless the user
     explicitly asks for Codex.
   - Prefer open-access full text (Nature Communications, Science Advances and npj titles
     are OA; fetch the article HTML directly, e.g.
     `curl -sL https://www.nature.com/articles/s41467-<...> -o research/style_refs/<slug>.html`).
   - If downloads fail (no network, paywall), fall back to any already-downloaded papers in
     `research/` / `knowledge_bank/references/`, and say so in the ledger header.
3. From each exemplar extract: the abstract, one Results paragraph, one Discussion paragraph,
   and two figure captions. Distill into `research/style_refs/style_profile.md`:
   - sentence-length distribution (typical mean and the long/short alternation pattern);
   - voice and person, including how active and passive constructions are used;
   - tense conventions (present for what figures show, past for what was done);
   - how numbers are woven into sentences (value-first vs claim-first);
   - hedging verbs actually used and their frequency;
   - caption grammar in the manuscript's selected descriptive or assertion-led stance;
     panel-sentence, statistics, and Methods-pointer conventions;
   - connector inventory (how paragraphs open; how contrast/consequence is signalled);
   - anything the journal does NOT do (rhetorical questions? em-dash asides? italics?).
4. Add approved lead-author and principal-coauthor passages as equal voice anchors when they
   are available. The profile is a **calibration target, not a straitjacket**: preserve a
   deliberate authorial voice while meeting the journal's reader expectations. Note any
   unresolved tension in the ledger rather than silently choosing one person's style.

## Step 2: Inventory the text units

Build the worklist in reading order: abstract sentences → main-text paragraphs by section →
caption blocks (Fig. 1..N). For each paragraph record its section role (opening claim,
evidence, caveat, transition) — the role determines which rewrites are appropriate.

## Step 3: Line-by-line polish pass

Work sentence by sentence. For each, ask in order:

1. **Register and field fit** — conversational phrasing → measured scientific phrasing;
   generic ML/CS language → the exact field-native process or quantity where appropriate.
   Rhetorical questions: convert to declaratives unless the section uses exactly one as a
   deliberate device. Contractions: expand. Colloquialisms and drama ("a striking result",
   "remarkably") → keep only when they add accurate meaning in context.
   **Say it, don't announce it:** sentences that flag that something is notable, next, or
   a result without stating the content are filler even when they sound academic — "The
   natural next question is…", "…is worth noting here", "…and is stated as such",
   label-fragments like "For positioning: …". Rewrite content-first so the scientific
   question or observation itself opens the sentence ("Tracer-specific tests identify which
   gas contributes most information…", "Recovery remains invariant to…"). Enumeration signposts that deliver ("Three results rule out X…")
   are not this class — keep them.
   **Repeated-construction tics:** count recurring sentence frames across the whole text
   ("…is itself a…", "The X is a Y:", identical paragraph openers). Keep only the
   instances doing real contrastive work; rewrite the rest with varied structure.
2. **Economy** — delete filler ("it is worth noting that", "in order to", "the fact that"),
   collapse doubled qualifiers, prefer one precise verb over verb+nominalization
   ("provides a demonstration of" → "demonstrates").
3. **Flow** — revise repeated sentence openings when the repetition becomes distracting;
   keep given-before-new information order; one idea per sentence — split sentences that
   stack three clauses with em-dashes (em-dash budget: ≤1 per sentence, and check the
   per-paragraph density against the exemplar profile).
4. **Precision** — replace vague verbs (get, show up, look at) with exact ones (obtain,
   appear, examine); attach every "this/these" to a noun ("this suggests" → "this
   partitioning suggests").
5. **Tense and voice** — present tense for what the paper/figures show and past for what was
   done; use active or passive voice according to agency, emphasis, and journal register.
6. **Captions specifically** — preserve the recorded descriptive or assertion-led stance;
   panel sentences may be telegraphic where the journal permits; definitions appear at first use within the caption
   (captions must stand alone); metric names match the main text exactly (if a term
   mismatch is found, do not silently fix it — flag it for /km-polish-terms).

Apply accepted rewrites directly with the Edit tool (or only record them, if `--dry-run`).
Record EVERY change in the ledger as: location (section ¶/sentence) · before · after ·
one-word reason tag (register/economy/flow/precision/tense/caption).

**Second pass (mandatory):** re-read every *modified paragraph in full*. Sentence-level
rewrites routinely break inter-sentence flow — fix transitions, de-duplicate sentence
openings introduced by the pass, and confirm the paragraph still makes its original argument.
Then re-run the full register checklist on every REPLACEMENT sentence: a rewrite can
introduce a new cliché or metadiscursive transition. This is not hypothetical — on a live
manuscript the pass itself wrote "The natural next question is…" and "…is worth noting
here", both metadiscourse, and both were caught only on a later sweep.

## Step 4: What NOT to "fix"

- Deliberate narrative devices that carry the argument (a one-sentence paragraph used as a
  turn; a designed antithesis). Polishing is not homogenizing.
- Hedging level and claim strength (invariant 4).
- Technical terms of art that sound awkward but are field-standard.
- Anything inside quotes, code, math, or file paths.
- Section structure, paragraph order, content — that is /km-editor-review or /km-advisor
  territory, not a language pass.

## Step 5: Verify invariants mechanically

Run these checks on each edited file against its backup; all must pass before reporting:

```bash
# numbers unchanged (multiset)
grep -oE '[0-9]+\.?[0-9]*' backup.md | sort | uniq -c > /tmp/nums_before
grep -oE '[0-9]+\.?[0-9]*' edited.md | sort | uniq -c > /tmp/nums_after
diff /tmp/nums_before /tmp/nums_after   # must be empty

# citation keys unchanged (multiset); adapt regex to \cite{} or [@key] style
grep -oE '\\cite\{[^}]*\}' backup.md | tr ',' '\n' | sort > /tmp/cites_before  # etc.

# markers unchanged
grep -c '\[CHECK' backup.md edited.md ; grep -c '\[PENDING' backup.md edited.md

# possible announce/filler phrases in the EDITED text; inspect each in context
grep -nE "worth noting|natural next question|is stated as such|It is important|is interesting to|Notably,|Importantly," edited.md
# repeated-construction tics: count frames, keep only earned uses
grep -oE "is itself an? [a-z]+" edited.md | sort | uniq -c | sort -rn
```

Plus: abstract word count within limit (report exact count), and total word-count delta per
section (a language pass should be roughly length-neutral or shorter; if a section grew
>3%, revisit it).

## Step 6: Report and log

1. Save the ledger to `agent-reviews/polish_report_academic_<YYYYMMDD>.md` (the standing
   convention: all review/report artifacts live in `agent-reviews/`). Structure: header
   (date, scope, style-profile provenance, files + backups, invariant-check results) →
   change table → "needs-author" flags → terms flagged for /km-polish-terms.
2. Append a dated entry to the manuscript `logfile.md` (session-tagged, with the report
   path and the number of changes per section).
3. Tell the user: changes applied vs flagged, word-count deltas, and that
   `/km-editor-review` or `/km-wordcount` are natural follow-ups. If captions changed,
   remind that figure PNGs themselves are untouched (captions live in text, not pixels) —
   no rebuild needed unless on-figure text was flagged.

## Failure modes to avoid (learned defaults)

- **Do not batch-rewrite whole sections in one Edit** — sentence-level edits keep the diff
  reviewable and the invariants checkable.
- **Do not run on a dirty file without a backup** (Step 0.4).
- **Do not "improve" the abstract over its word limit** — every abstract edit is followed
  by an immediate recount.
- **Do not let the exemplar profile inject journal clichés** ("Here we show" belongs in the
  abstract exactly once, not sprinkled through Results).
- **Your replacement can be the next cliché** — every rewritten sentence goes back through
  the context, field-language, and say-don't-announce checks before it counts as done (see the
  second-pass rule in Step 3; learned from the 2026-07-02 first run).
- If the manuscript is mid-edit by another session (check the logfile's most recent
  entries), coordinate before touching shared files.
