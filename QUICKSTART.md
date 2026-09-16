# Quickstart — your first twenty minutes with Kalam

This walks you through the bundled demo manuscript, then starts you on your own paper.
Everything in the demo is synthetic, so you can break it freely.

**Before you start:** open this directory with your agent (`claude`, `codex`, `gemini`)
and run `/km-onboard` if you have not already. The rest of this assumes Kalam knows who
you are.

Lines you type at your agent are shown as `/km-something`. Lines for your shell are
shown in code blocks.

---

## Part 1 — Look around (3 minutes)

### 1. Ask Kalam where you are

```
/km-orient
```

It reads the registry, finds the demo manuscript, reports its stage and version, and
**stops**. That last part is deliberate: `/km-orient` never starts work on its own. You
will open most sessions this way.

### 2. Read the demo's own README

```bash
cat manuscripts/demo-carbon-debt/README.md
```

It explains what the demo argues and — importantly — the three things Kalam's checks are
*meant* to flag in it. A demo that passed every check would teach you nothing.

### 3. Understand `metadata.yaml`

```bash
cat manuscripts/demo-carbon-debt/metadata.yaml
```

This file is how every skill finds its way around. Two fields matter most:

- **`current_draft`** — the comma-separated list of draft files, in order. Skills read
  *this*, never a directory listing, so you can restructure `drafts/` freely as long as
  you update this line.
- **`stage`** — where the manuscript is in the workflow. Skills refuse work that skips a
  stage, which is what stops a paper being drafted before its story is agreed.

---

## Part 2 — Run the checks (7 minutes)

### 4. Count the words against the journal's real limit

```bash
python skills/km-wordcount/scripts/count_words.py \
       manuscripts/demo-carbon-debt/drafts/main_text.md
```

Abstract 149 words against *Nature Communications*' 150-word limit; main text 1,376.
Note what the counter **excludes** — captions, citations, Methods, references — because
counting those overstates a manuscript by 5–6% and is how people end up trimming prose
they did not need to trim.

Or ask the skill, which also reads the limit from the journal profile rather than
assuming one:

```
/km-wordcount
```

### 5. Get the structural inventory

```bash
python skills/km-deep-read/scripts/inventory.py manuscripts/demo-carbon-debt
```

Read-only JSON: resolved draft files, ordered paragraphs, figures with their panel
letters, every internal cross-reference, dangling references, uncited display items, and
citation keys missing from the `.bib`. Four checking skills consume this instead of
re-deriving it by grep. On the demo it should report **no dangling cross-references and
no uncited display items**.

### 6. Let Kalam audit the prose

```
/km-deep-read
```

This is where Kalam earns its keep. It goes paragraph by paragraph and asks what each
one is *for* — context, gap, question, test, result, interpretation, limitation — then
flags paragraphs with no role, claims wider than their evidence, repetition across
sections, and captions that do not match their panels.

### 7. Watch the reference check find the placeholders

```
/km-ref-check
```

It should flag all five entries in the demo's `references.bib`: generic author names and
no DOIs. That is intentional. Kalam must never invent a reference, so its own demo ships
placeholders rather than plausible-looking fabrications.

### 8. Run the full pre-submission audit

```
/km-presubmit-audit
```

The orchestrator. It owns typos, acronyms, structure and placeholders, and *delegates*
everything else — counting to `/km-wordcount`, references to `/km-ref-check`, figures to
`/km-figures`. It should catch the unfilled `[FUNDING STATEMENT]` in `methods.md`.

This non-overlapping ownership is the design: six checking skills carry a "Delegation
(do not duplicate)" table naming the owner of every adjacent concern, so two skills
never report the same problem in different words.

---

## Part 3 — Build it (5 minutes)

### 9. Regenerate the figures

Needs `matplotlib` and `numpy`; skip if you do not have them.

```bash
cd manuscripts/demo-carbon-debt
python figures/make_demo_figures.py
```

Open `figures/make_demo_figures.py`. Every plotted statistic comes from one `RESULTS`
dictionary that mirrors the numbers in the text, so a figure cannot silently drift away
from the prose. The script warns you if it stops reproducing the 73% quoted in the
Results. This is the pattern worth copying into your own figure code.

### 10. Build the PDFs

Needs `pandoc` and `xelatex`.

```bash
./build.sh
```

Two PDFs land in `output/`: cover letter + main text, and Methods + SI. The Nature-family
split is the default because that is how these journals want the files.

### 11. Export to Word for your coauthors

```
/km-export-docx
```

Because coauthors comment in Word, whatever you prefer.

---

## Part 4 — Your own paper (5 minutes)

### 12. Scaffold it

```
/km-new-manuscript
```

Kalam asks for a short name, title, target journal and article type; copies
`resources/manuscript_template/`; pre-fills the author block from your profile; registers
it in `manuscripts/registry.yaml`; and sets `stage: setup`.

If the journal you named has no profile in `resources/journal_profiles/`, Kalam will say
so. Write one from the journal's author guidelines before relying on word-limit checks —
do not let it guess.

### 13. Start at the beginning

```
/km-ideation
```

Resist skipping to `/km-full-manuscript`. Stage 1 settles the question, the
one-sentence answer, the figure plan and which claims rest on which evidence. Look at
`manuscripts/demo-carbon-debt/drafts/ideation.md` for what a finished Stage 1 looks
like — including its "known weaknesses to state, not hide" section.

The stage gates exist because drafting prose around an unsettled story is the single
most expensive mistake in paper writing, and an agent will happily do it for you.

### 14. Clean up

When the demo has served its purpose:

```bash
rm -rf manuscripts/demo-carbon-debt
```

Then remove its entry from `manuscripts/registry.yaml`. Nothing else depends on it.

---

## Where to go next

| Question | Read |
|---|---|
| How is Kalam meant to write? | `resources/conventions/writing_style.md` |
| How do figures work? | `resources/conventions/figures.md` |
| What does every metadata field mean? | `resources/conventions/metadata_schema.md` |
| How do the skills divide the work? | `AGENTS.md`, "Review pipeline" |
| What does my journal require? | `resources/journal_profiles/<journal>.md` |

## Habits worth forming

1. **Open with `/km-orient`.** It costs nothing and stops the agent re-deriving context.
2. **Log decisions in the manuscript's `notes.md`**, and let skills log actions to its
   `logfile.md`. Six weeks later you will want to know why you cut that figure.
3. **Let `/km-bump-version` handle versions.** Manual renaming is how three stale PDFs
   end up in `output/`.
4. **Approve the story before the audit.** Checking skills sharpen a settled argument;
   they cannot rescue an unsettled one.
5. **Believe the audits over the agent's summary** — including the parts that say a
   claim outruns its evidence.
