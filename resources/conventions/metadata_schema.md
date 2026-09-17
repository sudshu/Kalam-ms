# `metadata.yaml` schema (advisory)

Every manuscript carries a `metadata.yaml`. This file records which keys the
framework's own tooling reads, and how project-specific keys should be named.

**This schema is advisory.** `lib/kalam_core/validate.py` reports deviations and
never rewrites a manuscript. No skill is gated on it. Manuscripts in flight are
expected to deviate; that is not an error to be "fixed" without the author.

## Core keys

Defined by `resources/manuscript_template/metadata.yaml`. Absence is reported at
INFO level, except where a specific tool depends on the key.

| Key | Read by | Notes |
|---|---|---|
| `title`, `short_title`, `project_name` | drafting + export skills | |
| `authors` | every drafting skill | list of `name`/`affiliation`/`email`/`corresponding` |
| `target_journal` | `/km-*` journal calibration | drives the SI-prefix family |
| `journal_profile` | journal calibration | path to `resources/journal_profiles/<j>.md`; may be repo-root-relative or manuscript-relative — both resolve |
| `paper_type`, `format` | export | |
| `stage` | `/km-orient`, stage tracking | see enum below |
| **`current_draft`** | `inventory.py`, `/km-wordcount`, `/km-export-docx`, `/km-audio` | **load-bearing** — comma-separated manuscript-relative paths, per `manuscript_files.md` |
| **`current_version`** | `/km-bump-version`, `/km-tidy-exports` | **load-bearing** — must be `vN.M`; those engines decline on any other shape |
| `current_pdf` | build scripts, `/km-bump-version` | |
| `research_question`, `core_finding` | drafting, advisor, editor panel | |
| `analysis_dir` | `/km-analysis` | absolute or manuscript-relative; both occur in practice |
| `bibliography` | `/km-ref-check` | |
| `created`, `last_updated` | provenance | |

## `stage` enum

```
setup → ideation → ideation_complete → skeleton → skeleton_complete
      → drafting → draft_complete → submitted
```

A value outside this set is reported as NOTICE, not corrected — the validator is
advisory and never rewrites your metadata. A manuscript sitting in coauthor review,
for instance, may carry `stage: "coauthor review"`, which is not in the enum. Either
add the state to the enum for your own workflow or map it onto `draft_complete`;
leaving it outside the enum is also fine, and only produces a NOTICE.

## Project-specific extension keys

Manuscripts legitimately accumulate their own keys. A manuscript in active coauthor
revision can easily carry a few dozen (`active_targeted_tracker`,
`v2_1_accepted_docx`, …) tracking state that matters only to it. **These are allowed
and are never flagged for renaming.**

For **new** keys, prefer an `x_` prefix (`x_active_review_tracker`) so core and
project-local fields stay visually distinct. Existing keys are grandfathered:
renaming them would break the manuscript-side scripts that read them.

## What the validator checks

Internal consistency only. It does **not** encode journal requirements — word
limits and similar live in `resources/journal_profiles/` and
`resources/conventions/journal_families.md`.

- core keys present; load-bearing keys called out separately
- `stage` within the documented enum
- `journal_profile` resolves (root-relative or manuscript-relative)
- every `current_draft` entry exists on disk
- **resolver divergence**: whether `inventory.py`'s legacy basename resolution
  and the canonical full-path resolution select the same files
- `analysis_dir` resolves when relative
- extension keys counted and listed

```bash
python lib/kalam_core/validate.py                       # all manuscripts
python lib/kalam_core/validate.py manuscripts/demo-carbon-debt --json
```

Exit status is 0 even with findings, unless `--strict` is passed.
