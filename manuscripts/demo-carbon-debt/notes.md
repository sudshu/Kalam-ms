# Notes — demo-carbon-debt

Newest entries at the top.

## 2026-09-16 — Demo manuscript assembled

Built as the bundled teaching manuscript for the public Kalam release. Everything in it
is synthetic. It sits at `stage: draft_complete` on purpose: a new user can run every
review skill against it immediately and see real output, which an empty manuscript at
`stage: setup` cannot give them.

Deliberate choices worth knowing if you edit this demo:

- **The bibliography is placeholder, with no DOIs.** Fabricating plausible references
  for a demo would seed real bibliographies with work that does not exist. The cost is
  that `/km-ref-check` flags them — which is the point, and is documented in
  `references.bib` and `README.md`.
- **The pooled 95% interval spans zero and the text says so.** A demo that hid its own
  weakest point would teach the wrong lesson about how Kalam handles uncertainty.
- **Figures read their numbers from one `RESULTS` dictionary** rather than resampling,
  so no figure can contradict the text. An earlier draft resampled and printed a pooled
  median of 2.25 against the text's 1.9.
- **`[FUNDING STATEMENT]` in `methods.md` is left unfilled**, so `/km-presubmit-audit`
  has a genuine placeholder to catch.
