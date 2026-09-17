---
name: km-tidy-exports
description: Use after building a manuscript PDF or DOCX (or when the user asks to "clean up old PDFs", "trash old versions", "tidy exports"). Moves every .pdf/.docx export whose _vN.M filename tag is OLDER than metadata.yaml current_version into output/trash/<version>_<date>/ — recoverable, never deleted. Runs automatically at the end of any export/build flow; also invocable standalone. Invoke with /km-tidy-exports [--dry-run].
---

# Tidy Manuscript Exports

Keep `exports/` (and `output/`, `output/share_ready/`) holding **only the current version** of the manuscript PDF/DOCX. Everything with an older `_vN.M` filename tag moves to `output/trash/<version>_<date>/` — the same recoverable-trash convention as `/km-bump-version`. Nothing is ever `rm`-ed.

## When to run

1. **Automatically, at the end of every export build** (user standing instruction, 2026-07-04: "when the PDF or DOCX is made, the older versions are pushed into trash"). Any flow that produces a PDF/DOCX — `build_full.sh`, `/km-export-docx`, a manual pandoc render — should finish by running this skill's engine. Build scripts can embed the call directly (see below).
2. Standalone, when the user asks to clean up / delete / trash old PDFs. Prefer this skill over `rm`: it is recoverable.

## How

```bash
# dry run (prints the plan, moves nothing)
python <skill_base_dir>/scripts/tidy_exports.py --manuscript <manuscript_dir> --dry-run

# apply
python <skill_base_dir>/scripts/tidy_exports.py --manuscript <manuscript_dir>
```

The engine:
- reads `current_version` from `metadata.yaml` (single source of truth — bump first via `/km-bump-version`, then build, then tidy);
- scans `exports/`, `output/`, `output/share_ready/` for `.pdf`/`.docx` files carrying a `_vN.M` tag;
- moves files whose tag ≠ current version to `output/trash/<their_version>_<today>/`;
- **keeps** current-version files (including dated copies), untagged files (review copies, workspace files), and anything already under `output/trash/`, `output/archive/`, or `archive/`;
- appends a dated line to the manuscript's `logfile.md`.

## Embedding in a build script

Append to the end of the manuscript's build script (e.g. `drafts/build_exports/build_full.sh`):

```bash
python3 "$MS/../../skills/km-tidy-exports/scripts/tidy_exports.py" --manuscript "$MS"
```

(Resolve the Kalam root robustly — the skill lives at `<kalam_root>/skills/km-tidy-exports/`.)

## Safety

- Moves only; emptying `output/trash/` is a separate, deliberate act the user must request explicitly.
- If the user says "delete permanently", confirm once, then remove the trash contents — never skip the trash stage on the first pass.
- Version detection is filename-based (`_vN.M`); a file without a tag is assumed precious and left alone. If the user wants dated duplicates of the *current* version cleaned too, do that by hand — the engine deliberately keeps them.

## Origin

Written after a version bump left three stale PDFs of the previous version, plus a stale SI PDF, sitting in `exports/` alongside the new ones. Superseded builds should be swept automatically on every new build rather than accumulating until someone notices.
