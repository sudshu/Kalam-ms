# Demo manuscript — read this first

**Every number in this manuscript is invented.** It is a teaching fixture: a complete,
realistic paper built so you can run Kalam's skills against something real on your first
day. Nothing here is a scientific result. Do not cite it, and do not carry a value from
it into a manuscript of your own.

The paper argues that repeated hot-dry extremes leave modelled tropical forests with
less carbon after 20 years even though their carbon *fluxes* recover within months — so
the standard recovery metric measures the wrong quantity. It is a plausible-shaped
paper with a real argument, which is what makes it useful to practise on.

## What is here

| Path | What it shows you |
|---|---|
| `metadata.yaml` | Every field Kalam reads. `current_draft` is what resolves the draft files |
| `drafts/ideation.md` | What Stage 1 produces *before* any prose exists |
| `drafts/evidence_placement.md` | The main-text evidence budget, decided explicitly |
| `drafts/main_text.md` | A finished draft in Kalam's writing style |
| `drafts/methods.md`, `drafts/extended_data_SI.md` | The Nature-family 4-file split |
| `drafts/cover_letter.md` | A cover letter that states the paper's limits rather than hiding them |
| `figures/make_demo_figures.py` | The shape of a Kalam figure script |
| `notes.md` | Why this demo is built the way it is |

## Try these, roughly in this order

```bash
# 1. Does the toolchain work end to end? (needs pandoc + xelatex)
./build.sh

# 2. Are the figures reproducible? (needs matplotlib + numpy)
python figures/make_demo_figures.py

# 3. How long is it, against the journal's limit? (stdlib only)
python ../../skills/km-wordcount/scripts/count_words.py drafts/main_text.md
```

Then ask your agent for these, which is where Kalam actually earns its keep:

- `/km-orient` — the session-start status read
- `/km-deep-read` — a paragraph-by-paragraph audit of the draft
- `/km-presubmit-audit` — the full pre-submission checklist
- `/km-ref-check` — reference validation
- `/km-abstract` — rewrite the abstract and compare

## Three things it will find, on purpose

A demo that passed every check would teach you nothing about the checks.

1. **`references.bib` is placeholder** — generic author names, no DOIs. Kalam must never
   invent references, so its own demo does not either. `/km-ref-check` should flag them.
2. **`[FUNDING STATEMENT]` in `methods.md` is unfilled** — `/km-presubmit-audit` should
   catch it as a reader-facing placeholder.
3. **The pooled 95% interval spans zero, and the text says so out loud** — this is not a
   defect. It is what honest uncertainty reporting looks like, and it is worth reading
   how the Results and Discussion handle it.

## When you are done

Delete this whole directory and remove its entry from `manuscripts/registry.yaml`.
Nothing else depends on it.

```bash
rm -rf manuscripts/demo-carbon-debt
```
