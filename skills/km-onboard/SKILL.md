---
name: km-onboard
description: "Use on a fresh Kalam install, when `resources/User/USER.md` still carries the `KALAM_PROFILE: NOT_CONFIGURED` marker, or when the user says 'onboard me', 'set up Kalam', 'I'm new here', '/km-onboard', or asks to update their author profile. Interviews the user in four short rounds, checks which export tools are installed, and writes their own `resources/User/USER.md`. Invoke with /km-onboard."
---

# Onboard (first run)

A fresh clone of Kalam knows nothing about its user. This skill fixes that in about
three minutes, then points them at their first real task.

**What you are producing:** `resources/User/USER.md`, written from the user's own
answers. Every `/km-*` skill reads that file to fill author blocks, calibrate prose,
and choose journal conventions, so the quality of this interview sets the quality of
everything afterwards.

## Ground rules

- **Never invent an answer.** If the user skips a question, write `[not specified]`
  in that field. A blank field is honest; a guessed affiliation ends up on a
  submitted paper.
- **One round per message.** Four rounds, grouped as below. Do not fire fifteen
  questions at once, and do not stretch one question into fifteen messages.
- **Every round after the first is skippable.** Say so. `skip` is a valid answer to
  any single question and to any whole round.
- **Offer defaults out loud.** For every preference question, name what Kalam will do
  if they say nothing, so silence is an informed choice rather than a gap.
- **Do not lecture.** They are trying to write a paper, not read a manual.

## Round 1 — Who you are (required)

Open with one sentence of orientation, then ask for these together:

1. **Name**, exactly as it should appear in an author list (e.g. `A. B. Lastname` or `Ana Lastname`).
2. **Affiliation**, as it appears on your papers — the full institutional string, including department, city and country.
3. **Email** for correspondence.
4. **Career stage** — PhD student / postdoc / staff scientist / faculty / other. This
   only calibrates how `/km-advisor` pitches feedback; it is not a judgement.

This round is required because a manuscript cannot be built without an author block.
If the user resists, take the name alone and mark the rest `[not specified]`.

## Round 2 — What you work on (required, brief)

1. **Field, in one sentence** — how you would describe your research to a scientist in
   an adjacent field.
2. **Three to five recurring themes** — the topics your papers keep returning to.
   These drive literature search framing and terminology checks.
3. **Journals you usually target** — name them plainly. Then tell the user which of
   those already have profiles in `resources/journal_profiles/` (list the matching
   filenames), and which would need one written before `/km-wordcount` and
   `/km-presubmit-audit` can check limits for them. Do not write a new profile now —
   just flag the gap.

## Round 3 — How you like to write (optional)

Say plainly that Kalam already has a complete default writing policy in
`resources/conventions/writing_style.md`, and this round only records departures
from it. Offer these, and accept "defaults are fine":

1. **Register** — do you want the prose spare and quantitative, or more expansive and
   narrative for a broad readership?
2. **Hedging** — minimal hedging on well-supported claims, or a more cautious voice?
3. **Captions and titles** — descriptive, or assertion-led? (Kalam's default is to
   decide this per manuscript with the journal in view.)
4. **Voice anchors** — is there a paper of yours, or a coauthor's, whose prose Kalam
   should imitate? If yes, ask for the path or DOI and record it; do not go find it.
5. **Anything that reliably annoys you** in AI-drafted scientific prose. Record their
   words verbatim under a `Do not` heading — this is the single most useful field in
   the profile.

## Round 4 — Standing boilerplate (optional)

The sentences that must appear, unchanged, on every paper from their institution.
Getting these on file once saves re-typing them on every manuscript:

1. **Funding / acknowledgement sentence** — verbatim, including any grant or contract
   number. Warn them that Kalam will reproduce it exactly and will not reword it.
2. **Copyright or institutional notice**, if their employer requires one, and the rule
   for which variant applies when.
3. **ORCID**, if they want it in exports.

## Environment check (do this yourself — do not ask)

Run the checks and report the result as a short table. Each row should say what the
tool unlocks, so a missing tool is an informed choice rather than a mystery failure:

```bash
python3 --version
pandoc --version   | head -1
xelatex --version  | head -1
python3 -c "import yaml; print('pyyaml', yaml.__version__)"
```

| Tool | Needed for | If missing |
|---|---|---|
| `python3` ≥ 3.9 | every bundled script; `/km-wordcount`, `/km-deep-read`, `/km-bump-version` | required — stop and tell the user |
| `pyyaml` | `metadata.yaml` parsing in `lib/kalam_core` | `pip install pyyaml` |
| `pandoc` | `/km-export-docx`, Markdown→PDF builds | `/km-export-docx` will not run; drafting and review still work |
| `xelatex` (TeX Live / MacTeX) | PDF builds of LaTeX manuscripts | Markdown drafting and Word export still work |
| `edge-tts` | `/km-audio` spoken drafts | optional; `pip install edge-tts` |

Report honestly what is missing. Do not install anything without asking, and do not
claim a tool is present because the command merely exists — check that it ran.

## Write the profile

1. Copy `resources/User/USER.template.md` to `resources/User/USER.md`, overwriting the
   placeholder.
2. Fill it in from the answers. **Delete the `<!-- KALAM_PROFILE: NOT_CONFIGURED ... -->`
   marker line** — its presence is what triggers onboarding, so leaving it in makes
   Kalam ask again every session.
3. Set `Last updated` to today's date.
4. Show the user the finished profile and ask them to correct anything wrong. It is
   their identity; they get the last word on it.
5. Append one dated line to the root `logfile.md` recording that onboarding completed.

## Hand off

Close by offering exactly three next steps, and let them choose:

1. **Take the tour** — walk through `manuscripts/demo-carbon-debt/`, the bundled
   synthetic paper, following `QUICKSTART.md`. Best if they have never used Kalam.
2. **Start a real manuscript** — run `/km-new-manuscript`. Best if they arrived with a
   paper already in mind.
3. **Bring in a draft they already have** — `/km-new-manuscript`, then copy their text
   into `drafts/` and run `/km-deep-read` for a first assessment.

Then stop and wait. Do not begin any of the three unprompted.

## Re-running

Safe to re-run whenever the user's details change — a new institution, a new grant
number, a shift in target journals. On a re-run, read the existing profile first, show
the current values, and ask only what they want to change. Never blank a field they
did not mention.
