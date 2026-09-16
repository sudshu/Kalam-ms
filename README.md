# Kalam

**A manuscript-preparation agent for scientific papers.** Kalam turns a coding agent
into a writing collaborator that knows how scientific papers are actually built: from
the question and the figures, through a skeleton, to a submitted draft — with the
journal's limits, your citation strategy, and a real pre-submission audit in the loop.

Kalam is **prompts, conventions and small scripts** — not a service, not a model, not a
wrapper around an API. There is nothing to sign up for and nothing phones home. It runs
inside the agent you already use.

```
Stage 1: IDEATION  →  Stage 2: SKELETON  →  Stage 3: FULL MANUSCRIPT
 figures, claims,      paragraph-by-           drafted sections,
 the story arc         paragraph outline,      audits, PDF + Word
                       evidence ledger         export
```

## Why it exists

Asking a general-purpose agent to "write my paper" produces prose that reads like an
agent wrote it: promotional, hedged in the wrong places, and confident about things the
data cannot support. Kalam's core is a writing policy that forbids exactly those habits,
plus 28 focused skills that each own one job and delegate the rest instead of
duplicating it.

It will not invent a result, a citation, or a claim about your track record.

## Requirements

| | Needed for | |
|---|---|---|
| **An agent that reads local files** | everything | Claude Code, OpenAI Codex, Gemini CLI, or similar |
| **Python 3.9+** | the bundled scripts | standard library only — nothing to `pip install` |
| `pandoc` | Word export, Markdown→PDF builds | optional |
| `xelatex` (TeX Live / MacTeX) | PDF builds | optional |
| `matplotlib`, `numpy` | regenerating the demo figures | optional |
| `python-docx`, `python-pptx` | `/km-export-docx`, `/km-slides` | optional |
| `edge-tts` | `/km-audio` spoken drafts | optional |

Drafting, reviewing and auditing work with Python alone. The optional tools only affect
what you can *export*.

## Install

```bash
git clone https://github.com/sudshu/Kalam-ms.git
cd Kalam-ms
python tests/framework/test_skill_registry.py   # optional: confirm the install is intact
```

The repository is `Kalam-ms` (*ms* for manuscript); the tool itself is just **Kalam**.

That is the whole installation. Now open the directory with your agent:

```bash
claude          # Claude Code  — reads CLAUDE.md
codex           # OpenAI Codex — reads AGENTS.md
gemini          # Gemini CLI   — reads GEMINI.md
```

All three files are the same brief; `CLAUDE.md` and `GEMINI.md` are symlinks to
`AGENTS.md`.

## Your first session

Say **hello**. Kalam will notice that `resources/User/USER.md` is unconfigured and offer
to onboard you. Say yes, or ask for it directly:

```
/km-onboard
```

It interviews you for about three minutes — name and affiliation as they should appear
in an author list, your field, the journals you target, how you like your prose, and any
standing funding sentence your institution requires — then writes your own
`resources/User/USER.md`. Every skill reads that file afterwards, so author blocks,
acknowledgements and writing calibration stop being guesswork. It also checks which
export tools you have installed and tells you what each one unlocks.

Skip it if you like; Kalam will just ask you the same things later, one at a time.

Then pick one:

- **New to Kalam?** → [`QUICKSTART.md`](QUICKSTART.md) walks you through the bundled
  demo manuscript in about twenty minutes.
- **Have a paper in mind?** → `/km-new-manuscript`
- **Have a draft already?** → `/km-new-manuscript`, paste your text into `drafts/`, then
  `/km-deep-read` for a first assessment.

## The skills

Ask for these by name in your agent. Each reads its own `skills/<name>/SKILL.md`.

**Getting started** · `/km-onboard` first-run interview · `/km-orient` session-start
status read · `/km-new-manuscript` scaffold a manuscript

**The three stages** · `/km-ideation` figures, claims, story · `/km-skeleton`
paragraph outline + evidence ledger · `/km-full-manuscript` drafted sections

**Writing** · `/km-abstract` · `/km-academic-polish` line-by-line rewrite ·
`/km-polish-terms` terminology harmonization · `/km-cover-letter` ·
`/km-supplementary` · `/km-response-to-reviewers`

**Checking** — non-overlapping ownership; `/km-presubmit-audit` orchestrates the rest ·
`/km-presubmit-audit` · `/km-wordcount` against journal limits · `/km-ref-check`
bibliography correctness · `/km-deep-read` paragraph-by-paragraph audit ·
`/km-polish-audit` terminology consistency · `/km-figures` · `/km-diff-review`

**Advice** · `/km-advisor` expert critique · `/km-editor-review` dual editor panel ·
`/km-research` literature work · `/km-analysis` drive an external analysis folder

**Output** · `/km-export-docx` · `/km-slides` · `/km-audio` spoken draft ·
`/km-bump-version` · `/km-tidy-exports` · `/km-wordcount`

## What is where

```
AGENTS.md                     the agent's brief — read this to understand Kalam
skills/km-*/SKILL.md          28 skills, one job each
resources/
  conventions/                the rules: writing style, figures, export, metadata
  journal_profiles/           12 journals: limits, structure, submission specifics
  manuscript_template/        what /km-new-manuscript copies
  User/USER.md                you (written by /km-onboard)
manuscripts/
  demo-carbon-debt/           bundled synthetic demo — delete when done
  registry.yaml               name → path → stage index
lib/kalam_core/               path resolution, metadata parsing, validation
tests/framework/              structural checks on the framework itself
```

`resources/conventions/writing_style.md` is the single source of truth for
reader-facing prose. Every writing and editing skill inherits from it. If you change one
thing about Kalam, change that file.

## Making it yours

Kalam ships opinionated because a vague writing policy is worthless. Disagreeing with it
is expected:

| To change | Edit |
|---|---|
| How prose should read | `resources/conventions/writing_style.md` |
| Figure defaults | `resources/conventions/figures.md` |
| Your journal's limits | `resources/journal_profiles/<journal>.md` — or add one |
| What a new manuscript starts as | `resources/manuscript_template/` |
| Your own details | `resources/User/USER.md`, or re-run `/km-onboard` |

To add a journal, copy the closest existing profile and edit it from the journal's own
author guidelines. Do not let an agent guess a word limit — put the real number in the
profile.

## Limitations, honestly

- **It is a writing framework, not a scientist.** It will not check whether your science
  is right, and it cannot tell a real result from an artefact.
- **Journal profiles drift.** The 12 bundled profiles were written from author
  guidelines at a point in time. Verify limits against the journal before submitting.
- **`/km-ref-check` validates format and internal consistency**, not whether a reference
  says what you claim it says.
- **The demo's numbers are invented.** See `manuscripts/demo-carbon-debt/README.md`.
- **v0.1.** The skills are in daily use on real manuscripts, but this is the first
  public release; expect rough edges in the paths less travelled.

## Contributing

Bug reports and new journal profiles are the most useful contributions. See
[`CONTRIBUTING.md`](CONTRIBUTING.md).

## Credit and license

Kalam was created by **Sudhanshu Pandey**.

Licensed under MIT — see [`LICENSE`](LICENSE).

"Kalam" (क़लम / قلم) means *pen*.
