---
name: km-editor-review
description: "Use when the user wants journal handling-editor feedback on the manuscript — e.g. 'editor feedback', 'ask the editors', 'ask an agent as NC editor', 'editor panel', 'desk-reject risk', 'is the story defensible'. Runs TWO independent editor-persona reviews in parallel — a fresh Claude agent (Fable 5 or the strongest session model) AND the Codex CLI (model and reasoning effort taken from the user's standing review rule, not hardcoded) — each role-playing the handling editor of the TARGET JOURNAL, both reading the figures visually, then synthesizes the two into one verdict + convergent must-fix list. Journal-adaptable via metadata.yaml target_journal. Distinct from /km-advisor (internal mentor). Invoke with /km-editor-review."
---

# Journal Handling-Editor Panel (dual independent reviews + synthesis)

Every time the user asks for **editor feedback**, run BOTH reviewers below — never just one — then synthesize.
Rationale: run on a live manuscript, the two reviewers independently converged on the same
gating items — which is what makes those items high-confidence — while each also caught
problems the other missed. The convergence/divergence structure is the product, so one
reviewer alone loses most of the value.

## The two reviewers (always both, launched in parallel)

**Reviewer A — Claude agent (Fable 5 or the strongest model available to the session):**
- Spawn a **fresh** Agent (general-purpose/claude type) — **never a fork**: the reviewer must not inherit this
  conversation's framing. Omit the model override so it inherits the session model; note the model identity in
  the report metadata line.
- It must **Read the figure PNGs visually** (list each figure path explicitly in the prompt) and read the
  manuscript materials itself. Instruct it: read-only — no file creation/edit/move.

**Reviewer B — Codex CLI:**

Do **not** hardcode a model or effort level here. Take both from the user's
standing feedback/review rule in `~/.claude/CLAUDE.md` ("use the CODEX CLI for
feedback, review, critique or a second opinion"), which names the current model
and default reasoning effort. If the user names a model or provider explicitly in
the request, that selection wins over the standing rule.

```bash
codex exec -C <manuscript_dir> --model <MODEL> -c model_reasoning_effort="<EFFORT>" \
  -i figures/main/fig1_*.png -i figures/main/fig2_*.png [... every main figure ...] \
  -o <scratch>/codex_editor_report.md "$(cat <scratch>/editor_prompt.txt)" > <scratch>/codex_run.log 2>&1
```
- If the API rejects the requested effort, fall back to the next-highest supported
  level and **record the model and effort actually used** (check the run-log
  header: `model:` / `reasoning effort:` lines).
- Attach ALL main-figure PNGs with `-i` so Codex judges the figures visually too.
- Keep the default read-only sandbox. Run in background (xhigh takes 10–20+ min); collect via `-o` file.
- If the user says "gemini", add the Gemini CLI as an optional third editor with the same prompt.

## Journal adaptation (required)
- Persona = **senior handling editor at the TARGET JOURNAL**, remit matched to the manuscript's field.
- Resolve the journal from `manuscripts/<active>/metadata.yaml` → `target_journal` (and load
  `resources/journal_profiles/<journal>.md` if it exists for word/display-item limits to judge against).
- If metadata is unset/ambiguous or the user names a different journal in the ask, **ask which journal**.
- Journal-specific knobs to thread into the prompt: format limits (words, display items, abstract length),
  the journal's significance bar (e.g. Nature Comms = multidisciplinary advance; NGeo = geoscience depth;
  NMI = ML novelty), and desk-screen style.

## Materials (stage-adaptive; same list to BOTH reviewers)
1. `metadata.yaml` (title, claims, datasets, methods).
2. Stage ideation/skeleton: `drafts/ideation.md`, `drafts/skeleton.md`, `figures/figure_index.md`
   (captions + QC ledger). Stage drafting+: the current main text (+ SI) and latest PDF instead.
3. Every built main figure PNG — read visually by both reviewers.
4. Recent load-bearing findings in `research/background_research/` (anything bearing on a headline claim).
5. `references.bib` — skim for coverage/balance only (state DOIs are pre-verified; do not re-verify).

**Anchoring guard (critical):** both reviewers are BARRED from reading the `agent-reviews/` folder, any
`review_report*.md` (wherever located), any `action_plan*.md`, and the `notes.md` decision log — prior
advisor opinions must not anchor them. State this in both prompts.

## Report structure (identical 8 sections for both, so the synthesis can align them)
1. **Desk decision simulation** — send to review / borderline / reject, with a clearly-labeled SUBJECTIVE
   desk-reject probability band ("my judgment, not a journal statistic"); biggest factor each direction.
2. **Fit and significance** for the target journal (altitude: principle vs application).
3. **Story arc** — result ordering, redundancy, missing beats, abstract plan defensibility.
4. **Novelty and defensibility** — does the narrowed claim survive; simulate the hostile domain reviewer AND
   the hostile methods/ML reviewer; is each pre-empted?
5. **Figures one-by-one** — standalone message, visual honesty (regime labels, axis choices, significance
   marks), Nature-family production readiness; flag anything an editor would bounce.
6. **Known open items** — rank the package's own pending analyses: gating vs deferrable to revision.
7. **Ranked must-fix list** — numbered, one-line rationale, effort class (text-only / figure-rebuild /
   new-analysis).
8. **Title and abstract** — react; up to 3 alternatives only if genuinely stronger.

Both reports must begin with a metadata line: persona, model identity + reasoning effort actually used,
date, materials reviewed. Final message = the report ONLY (saved verbatim).

## Synthesis (the deliverable)
After both return, write the synthesis in the reply (and nowhere else — do not auto-edit the manuscript):
1. **Verdict table** — decision + subjective band per reviewer, both labeled subjective.
2. **Convergent findings** — items both raised independently → present as *settled must-fixes*.
3. **Divergences** — where verdicts/rankings differ and WHY (usually one weighs a known flaw harder);
   translate into a practical instruction.
4. **Unique catches per reviewer** — worth having, lower confidence than convergent items.
5. **Bottom line** — the single next action the panel implies, mapped onto the manuscript's operational queue.

## Persistence + hygiene
- Save each report verbatim to `<manuscript root>/agent-reviews/` (create the folder if it does not exist —
  ALL agent reviews live there, never in the manuscript root) with a provenance header (commissioning
  session, exact model + effort from the run log, figures attached y/n, anchoring guard applied):
  `agent-reviews/review_report_<journal-slug>_editor_<model>_<YYYYMMDD>.md` (e.g. `..._fable5_20260702.md`,
  `agent-reviews/review_report_codex_nc_editor_20260702.md`). Add a stage tag to the name when the same
  panel runs more than once per day (e.g. `..._draft1_20260702.md`).
- One `logfile.md` entry per review + one for the synthesis (date+time; verdict band; top convergent fixes).
- Give absolute paths for both saved reports in the reply.
- Coordinate: reviews are read-only and report files are new, so no collision with a live primary-author
  session — but never write into files that session owns (figure scripts, figure_index.md).

## Rules
- Never fabricate DOIs, journal metrics, or acceptance rates; all risk numbers are labeled subjective.
- Feedback only — surface the panel's asks; the user chooses what to apply (then /km-* skills or the
  analysis workspace execute them).
- Novelty/scooping claims: cross-check with the built-in WebSearch/WebFetch tools before asserting
  (standing rule since 2026-08-12 — no Codex/Gemini CLI for research unless the user asks for Codex).
  Reviewer B below still runs on the Codex CLI; that is a review task, not online research.
