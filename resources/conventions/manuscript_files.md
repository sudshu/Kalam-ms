# Resolving a manuscript's draft files (single source of truth)

Manuscripts do **not** all use `drafts/manuscript.md`. Some use a Nature-family
4-file split under `drafts/` or `drafts/v2/` (`cover_letter.md` + `main_text.md` +
`methods.md` + `extended_data_SI.md`); others use `drafts/manuscript.md` +
`drafts/supplementary_information.md`. Any skill that reads, counts, checks, or
exports "the manuscript" MUST resolve the files at runtime from `metadata.yaml`
instead of hardcoding a path.

## The `current_draft` schema (canonical)

`current_draft` is a **comma-separated list of manuscript-relative file paths**, in
reading order. Examples:

```yaml
current_draft: "drafts/manuscript.md, drafts/supplementary_information.md"
current_draft: "drafts/v2/cover_letter.md, drafts/v2/main_text.md, drafts/v2/methods.md, drafts/v2/extended_data_SI.md"
```

Role of each file is inferred from its name:
- **cover letter** — filename contains `cover_letter`
- **SI** — filename contains `supplementary`, `extended_data`, or `_SI`
- **main text** — everything else (the first such file is the primary main text)

## Resolution procedure (Step 0 for every manuscript-consuming skill)

1. Read `current_draft` from the manuscript's `metadata.yaml` and split on commas.
   Treat each entry as a path relative to the manuscript directory.
2. Keep the entries that exist on disk; classify them (cover letter / main text / SI)
   by the name rules above.
3. **Fallbacks** if `current_draft` is absent or none of its files exist, try in order:
   - main text: `drafts/manuscript.md` → `drafts/main_text.md` → `drafts/v2/main_text.md`
   - SI: `drafts/supplementary_information.md` → `drafts/extended_data_SI.md` → `drafts/v2/extended_data_SI.md`
   - cover letter: `drafts/cover_letter.md` → `drafts/v2/cover_letter.md`
4. Report which files were resolved before proceeding, so the user can catch a
   mis-set `current_draft`.

## Programmatic helper

The single implementation lives in **`lib/kalam_core/metadata.py`**:

- `current_draft_entries(text)` — **canonical**: comma-separated,
  manuscript-relative paths kept whole, exactly as specified above.
- `resolve_draft_files(mdir)` — canonical resolution to existing paths.
- `first_draft(mdir)` — the first entry (what `/km-audio` uses).
- `classify(name)` — cover letter / SI / main text, per the name rules above.

`skills/km-deep-read/scripts/inventory.py` consumes it and emits the JSON
inventory. Skills may shell out to that script, import `kalam_core.metadata`
directly, or apply the rule above by hand.

### One divergence you must know about

`inventory.py` calls the resolver with `legacy=True`, which reproduces its
historical token scan: it matches only `[A-Za-z0-9_]+\.md` and therefore
**discards any subdirectory** in a `current_draft` entry, then searches
`drafts/v2/` → `drafts/` → the manuscript root.

Consequence: if a manuscript declares `current_draft` with a subdirectory — say
`drafts/nature_rebuild/{main_text,methods,extended_data_SI}.md` — while an older
`drafts/v2/` still exists on disk, the legacy scan reduces those entries to bare
filenames and finds the `drafts/v2/` copies first. The inventory-consuming audit
skills (`/km-deep-read`, `/km-figures`, `/km-ref-check`, `/km-supplementary`,
`/km-presubmit-audit`) then read a **stale draft**, while skills using the canonical
resolver read the right one. If an audit reports content you do not recognise, check
this first: delete or rename the superseded directory.

Switching `inventory.py` to `legacy=False` fixes this but changes which files
those audits read, so it is an explicit user decision, not a silent change.
`lib/kalam_core/validate.py` reports the condition as `resolver-divergence`.
