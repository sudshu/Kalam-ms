---
name: km-bump-version
description: "Use when the user wants to roll a manuscript's version number forward and tidy up the files the old version left behind. Supports an integer/major bump (v4.1 -> v5.0), a dot/minor bump (v4.1 -> v4.2), or an explicit set (--set v5.3). It updates every place the version lives (metadata.yaml current_version/prior_version/current_pdf, and any hardcoded VERSION= line in build scripts), moves superseded build artifacts (.pdf/.docx) into a recoverable output/trash/ folder, and archives explicitly-named version-specific source files into archive/. Always previews a dry-run plan and asks before changing anything. Invoke with /km-bump-version. Triggers: 'bump version', 'new version', 'increment version', 'version up', 'roll the version', 'cut v5', 'major/minor version bump'."
---

# Bump the Manuscript Version

Roll a manuscript's version forward and sweep up after the previous version in one safe, previewable step. This skill keeps every version reference in sync, moves stale build artifacts to a recoverable trash folder, and archives version-specific source files on request.

## When to Use

- After a round of edits that warrants a new version label (before a fresh build, a co-author circulation, or a submission).
- When `output/` has accumulated PDFs/DOCX from several past versions and you want only the current version visible.
- When `metadata.yaml` and a build script's hardcoded `VERSION=` have drifted out of sync.

Do **not** use this to *build* the PDF/DOCX: that is `build.sh` / `/km-export-docx`. This skill changes the version label and cleans up; you rebuild afterwards.

## Prerequisites

- A manuscript folder with `metadata.yaml` containing a `current_version` field (format `v<major>.<minor>`, e.g. `v4.1`).
- Python 3 on `PATH` (invoke as `python`; do not hardcode an environment path).
- The engine: `<skill_base_dir>/scripts/bump_version.py`.

## Version model

Version strings are `v<major>.<minor>` (a bare `v4` is read as `v4.0`). Patch-level versions (`v4.1.2`) are rejected with a clear error rather than silently truncated.

| Argument | Meaning | Example |
|---|---|---|
| `/km-bump-version` *(no arg)* or `minor` / `dot` / `point` | **minor / dot bump** — increment the dot | v4.1 → v4.2 |
| `/km-bump-version major` (or `integer` / `int`) | **major / integer bump** — increment the integer, reset the dot to 0 | v4.1 → v5.0 |
| `/km-bump-version v5.3` | **explicit set** — set exactly this version (warns if not greater than current) | → v5.3 |

Map the user's words to a flag: "integer"/"major" → `--bump major`; "dot"/"minor"/"point" → `--bump minor`; a literal `vX.Y` → `--set vX.Y`. If the user just says "bump the version" with no qualifier, default to a **minor (dot)** bump and say so.

## What gets touched (and what never does)

**Updated in place:**
- `metadata.yaml`: `current_version` (→ new), `last_updated` (→ today), and the version *filename-tag* inside `current_pdf` / `current_draft` strings. `prior_version` is normalized to `"<old> (<date>)"`; any prior locator annotation (e.g. `(drafts/v2/, ...)`) is dropped. Only genuine `_vN.M_` filename tags are retagged, so a draft-folder path like `drafts/v2/` is never rewritten, and inline `# comments` on these fields are preserved.
- Any build script under the manuscript with a **hardcoded** `VERSION=v...` line (e.g. `drafts/v2/build_v2.sh`), including one with surrounding quotes or a trailing comment, which are preserved. Parameterized lines that read from metadata (e.g. `VERSION="${VERSION:-$(grep ...)}"` in the template `build.sh`) are left alone; they follow metadata automatically.

**Moved to `output/trash/<old_version>_<date>/` (recoverable, never deleted):**
- Every `.pdf`/`.docx` under `output/` whose version tag is **not** the new version. These are git-ignored and regenerable from sources, so trashing them is safe. Files already at the new version are kept; files with no parseable version tag are left in place; anything already under `output/archive/` or `output/trash/` is ignored.

**Moved to `archive/<old_version>/` only when explicitly listed:**
- Version-specific *source* files you name (e.g. a `vX.Y_reset_instructions.md`, a version-stamped plan note, a frozen draft snapshot). The skill proposes candidates; you confirm. The engine itself refuses to archive a living draft (`main_text.md`, `methods.md`, `extended_data_SI.md`, `cover_letter.md`, …) unless you pass `--force-archive`, so a mis-typed `--archive` cannot strand a precious source.

## Workflow

The correct order is **bump → rebuild → (export)**, because build scripts read the new version *after* the bump.

### Step 1: Read context and pick the bump type

1. Read the manuscript's `metadata.yaml` (`current_version`, `current_pdf`, `current_draft`).
2. Resolve the user's argument to `--bump major`, `--bump minor`, or `--set vX.Y` (see the table above).

### Step 2: Dry run (changes nothing) and propose source archives

Run the engine in dry-run mode (no `--apply`):

```bash
python <skill_base_dir>/scripts/bump_version.py \
  --metadata <manuscript>/metadata.yaml --bump minor
```

It prints a JSON plan: `old_version → new_version`, the metadata line edits, the build-script `VERSION=` lines that will change, and the list of output artifacts that will move to trash (`outputs_to_trash`), plus any `warnings`.

Separately, scan the manuscript for **version-specific source files** that belong with the old version (filenames containing the old version token, version-stamped instruction/plan/reset notes, or a frozen draft snapshot directory). Propose these to the user as archive candidates — do not assume.

### Step 3: Present the plan and confirm

Show the user a concise summary:

```
Bump: v4.1 → v4.2 (minor)
  metadata.yaml: current_version, prior_version, last_updated, current_pdf
  build script:  drafts/v2/build_v2.sh  (VERSION=v4.1 → v4.2)
  → trash (recoverable): 10 artifacts → output/trash/v4.1_2026-06-12/
  → archive (you choose): drafts/v2/v4.1_reset_instructions.md  [archive? y/n]
```

Use `AskUserQuestion` if the archive selection or the bump type is ambiguous. Get explicit confirmation before applying — this step moves files.

### Step 4: Apply

Re-run with `--apply`, adding `--archive <path> ...` for each source file the user approved (omit `--archive` if none):

```bash
python <skill_base_dir>/scripts/bump_version.py \
  --metadata <manuscript>/metadata.yaml --bump minor --apply \
  --archive drafts/v2/v4.1_reset_instructions.md
```

The engine performs the metadata + build-script edits, moves the superseded outputs to trash, moves the named sources to `archive/`, and appends a dated+timed line to the manuscript's `logfile.md`.

### Step 5: Rebuild at the new version

`output/` no longer holds current PDFs (they moved to trash). Rebuild so it reflects the new version:

```bash
bash <manuscript>/drafts/v2/build_v2.sh      # or the manuscript's build.sh
```

If the user wants Word files too, run `/km-export-docx`.

### Step 6: Report

Tell the user: the new version, how many artifacts went to trash and where (recoverable), what was archived, which build script lines changed, and the reminder that a rebuild populates `output/` at the new version. Confirm the `logfile.md` entry was written.

## Safety notes

- **Nothing is destroyed.** Outputs go to `output/trash/` (recoverable until you empty it); sources go to `archive/`. Neither is ever `rm`-ed by this skill.
- **Dry run first, always.** The engine changes nothing without `--apply`.
- **Source files are opt-in.** Only files passed via `--archive` move; living drafts are never auto-touched.
- **Legacy `output/archive/`** (older manual habit) is left untouched; this skill routes superseded outputs to `output/trash/` going forward.
- If `--set` targets a version not greater than the current one, the engine emits a warning; relay it and reconfirm before applying.
- Emptying the trash is a separate, deliberate act, never bundled into a bump.

## Notes

- `output/trash/` and `archive/` are created on demand. Output artifacts are already git-ignored (`*.pdf`, `*.docx`); `output/trash/` is additionally ignored so nothing regenerable is ever committed. Archived `.md`/`.tex` sources stay visible to git (commit them to track the snapshot); an archived `.pdf`/`.docx` snapshot is git-ignored by the global rules, so `git add -f` it if you want it tracked.
- The engine is deterministic and idempotent-safe: re-running a dry run never alters state, and applying twice will not re-trash files already in trash.
- Keep `current_version` as the single conceptual source of truth. The one place that legitimately *also* holds the literal version is a hardcoded build script (`build_v2.sh`), which the engine keeps in sync; prefer parameterized build scripts that read `current_version` from metadata where possible.
