# Changelog

## v0.1.0 — 2026-09-16

First public release.

### What is in it

- **28 `/km-*` skills** covering the three-stage workflow (ideation → skeleton → full
  manuscript), writing and polishing, a non-overlapping review pipeline, expert advice,
  and export to PDF, Word, slides and audio.
- **`/km-onboard`** — a first-run interview that writes the user's own
  `resources/User/USER.md`. `AGENTS.md` detects an unconfigured profile and offers it at
  session start.
- **9 convention files**, with `resources/conventions/writing_style.md` as the single
  source of truth for reader-facing prose, inherited by every writing skill.
- **12 journal profiles** — Nature, Nature Geoscience, Nature Climate Change, Nature
  Communications, Nature Machine Intelligence, PNAS, AGU Advances, GRL, JGR Atmospheres,
  ACP, Environmental Science & Technology, Remote Sensing of Environment.
- **`lib/kalam_core`** — path resolution, `metadata.yaml`/`current_draft` parsing, and an
  advisory (never gating) metadata validator. Standard library only.
- **A bundled synthetic demo manuscript** at `manuscripts/demo-carbon-debt/`, complete
  from ideation to built PDF, so a new user can exercise every skill on their first day.
- **`README.md`** and **`QUICKSTART.md`** — install, first session, and a twenty-minute
  guided walkthrough.

### Fixed while preparing this release

Three latent bugs in `skills/km-deep-read/scripts/inventory.py`, the shared structural
parser that four checking skills consume:

- A caption written `**Supplementary Figure S1 | ...**` was not classified as a caption
  at all, and where it was matched it was misfiled as main-text *Figure 1* — colliding
  with the real Figure 1 and producing wrong dangling-reference and uncited-display-item
  reports. The word-boundary after a bare `Fig` fell inside `Figure`. Both the classifier
  and the declaration parser now accept `Fig`, `Fig.` and `Figure`, with `Supplementary`
  tried first.
- Email addresses in captions were parsed as citation keys, previously worked around by
  special-casing one institutional domain. The paragraph parser's existing lookbehind is
  now applied to captions too, so the special case is gone.
- The supplementary citation patterns required the literal word "Supplementary", so the
  Nature house-style short forms `Fig. S1`, `Figure S3` and `Figs. S1 and S2` matched no
  pattern at all. Those citations were invisible: the item was reported uncited, and a
  genuinely uncited supplementary item could not be told apart from a cited one. An `S`
  before the number is now the supplementary marker, accepted with or without the word
  and on every number in a list. `Table S1` consequently registers as a supplementary
  table rather than main-text Table 1. Declarations and citations share the rule, so a
  caption and the text that cites it can no longer disagree.

`tests/framework/test_kalam_core.py` no longer requires a grouped (depth-2) manuscript to
exist in the live tree; that check skips when none is present, since depth-2 resolution is
covered unconditionally by the temp-dir fixtures.

### Known limitations

- Journal profiles were written from author guidelines at a point in time. Verify limits
  against the journal before submitting.
- `/km-ref-check` validates reference format and internal consistency, not whether a
  reference supports the claim citing it.
- The demo's bibliography is deliberately placeholder — no DOIs, generic author names —
  so `/km-ref-check` has something genuine to flag.
