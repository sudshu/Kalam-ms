#!/usr/bin/env python3
"""Advisory validator for a Kalam manuscript's ``metadata.yaml``.

**This tool reports; it never rewrites.** It exits 0 even when it finds
something, unless ``--strict`` is passed. Nothing in the framework gates on it.

Design constraints (2026-09-09):

* **Backward compatible.** Manuscripts carry many project-specific keys
  (a manuscript in active revision can carry a few dozen). Unknown keys are reported as ``extension`` at
  INFO level and are never errors. New keys are *encouraged* to use an ``x_``
  prefix, but existing ones are not flagged for renaming.
* **No invented requirements.** It checks internal consistency only — that
  declared paths exist, that the ``stage`` value is one the framework documents.
  It does not check journal word limits or any other external requirement.
* **Unresolved policy stays unresolved.** A ``stage`` outside the documented set
  is reported as NOTICE with both options named; the tool does not pick one.

Usage::

    python lib/kalam_core/validate.py                       # every manuscript
    python lib/kalam_core/validate.py manuscripts/demo-carbon-debt
    python lib/kalam_core/validate.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from kalam_core import metadata, paths
else:
    from . import metadata, paths

#: Keys the template defines. Absence is a NOTICE, never an error.
CORE_KEYS = (
    "title", "short_title", "project_name", "authors", "target_journal",
    "journal_profile", "paper_type", "format", "stage", "current_version",
    "current_draft", "research_question", "core_finding", "analysis_dir",
    "bibliography", "created", "last_updated",
)

#: Keys the framework's own tooling reads. Absence breaks a specific tool.
TOOL_CRITICAL = {
    "current_draft": "inventory.py / km-wordcount / km-export-docx draft resolution",
    "current_version": "km-bump-version and km-tidy-exports version comparison",
}

#: The stage enum documented in AGENTS.md.
KNOWN_STAGES = (
    "setup", "ideation", "ideation_complete", "skeleton", "skeleton_complete",
    "drafting", "draft_complete", "submitted",
)


def check(mdir: Path) -> list[dict]:
    """Return a list of findings for one manuscript. Never mutates anything."""
    text = metadata.read_text(mdir)
    out: list[dict] = []

    def add(level, code, msg):
        out.append({"level": level, "code": code, "message": msg})

    if not text:
        add("ERROR", "no-metadata", "no metadata.yaml")
        return out

    present = {
        line.split(":", 1)[0]
        for line in text.splitlines()
        if line[:1].isalpha() and ":" in line
    }

    for key in CORE_KEYS:
        if key not in present:
            if key in TOOL_CRITICAL:
                add("NOTICE", "missing-tool-key",
                    f"'{key}' absent — needed by {TOOL_CRITICAL[key]}")
            else:
                add("INFO", "missing-core-key", f"'{key}' absent (template defines it)")

    stage = metadata.read_scalar(text, "stage")
    if stage and stage not in KNOWN_STAGES:
        add("NOTICE", "stage-outside-enum",
            f"stage='{stage}' is not in the documented set. UNRESOLVED: either add "
            f"'{stage}' to the enum in AGENTS.md, or map it to an existing value. "
            f"Left as-is deliberately; this tool does not change metadata.")

    ver = metadata.read_scalar(text, "current_version")
    if ver and not re.match(r"^v\d+(\.\d+)?$", ver):
        add("NOTICE", "version-shape",
            f"current_version='{ver}' is not the vN.M shape that /km-bump-version and "
            f"/km-tidy-exports compare on; both will decline to run here")

    prof = metadata.read_scalar(text, "journal_profile")
    if prof and prof.lower() not in ("null", "~", "none"):
        cand = prof if Path(prof).is_absolute() else paths.kalam_root() / prof.lstrip("./")
        if not Path(cand).exists():
            alt = mdir / prof
            if not alt.exists():
                add("NOTICE", "journal-profile-missing",
                    f"journal_profile '{prof}' does not resolve")
    elif prof:
        add("INFO", "journal-profile-null",
            "journal_profile is null — word-budget work needs a profile first")

    entries = metadata.current_draft_entries(text)
    for e in entries:
        if not (mdir / e).exists():
            add("NOTICE", "current-draft-missing",
                f"current_draft entry '{e}' does not exist on disk")

    legacy = metadata.resolve_draft_files(mdir, legacy=True)
    canonical = metadata.resolve_draft_files(mdir, legacy=False)
    if entries and sorted(legacy) != sorted(canonical):
        add("WARN", "resolver-divergence",
            "legacy (inventory.py) and canonical resolution disagree — "
            f"legacy={[p.name for p in legacy]} vs canonical={[str(p.relative_to(mdir)) for p in canonical]}. "
            "Audit skills using inventory.py may be reading different files than declared.")

    adir = metadata.read_scalar(text, "analysis_dir")
    if adir and not Path(adir).is_absolute() and not (mdir / adir).exists():
        add("INFO", "analysis-dir-unresolved",
            f"analysis_dir '{adir}' is relative and does not resolve under the manuscript")

    ext = sorted(k for k in present if k not in CORE_KEYS)
    if ext:
        add("INFO", "extension-keys",
            f"{len(ext)} project-specific key(s) — allowed. "
            f"Prefer an 'x_' prefix for NEW keys: {', '.join(ext[:6])}"
            + (" …" if len(ext) > 6 else ""))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Advisory Kalam metadata validator (never rewrites).")
    ap.add_argument("manuscripts", nargs="*", help="manuscript dirs (default: all)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any ERROR/WARN was found (default: always exit 0)")
    args = ap.parse_args(argv)

    targets = [Path(m) for m in args.manuscripts] or list(paths.iter_manuscript_dirs())
    report = {}
    for m in targets:
        report[paths.manuscript_name(m) if m.exists() else str(m)] = check(m)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for name, findings in report.items():
            if not findings:
                print(f"  OK    {name}")
                continue
            print(f"\n  {name}")
            for f in findings:
                print(f"    [{f['level']:<6}] {f['code']}: {f['message']}")
        counts: dict[str, int] = {}
        for findings in report.values():
            for f in findings:
                counts[f["level"]] = counts.get(f["level"], 0) + 1
        print("\n  " + (", ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "no findings")
              + f"  across {len(report)} manuscript(s)")
        print("  Advisory only — no file was modified.")

    if args.strict and any(f["level"] in ("ERROR", "WARN") for v in report.values() for f in v):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
