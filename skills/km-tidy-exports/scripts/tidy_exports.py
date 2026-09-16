#!/usr/bin/env python3
"""Move superseded-version PDF/DOCX exports to output/trash/ (never delete).

Reads current_version from metadata.yaml, scans the manuscript's export
directories for .pdf/.docx artifacts carrying an OLDER version filename-tag
(_vN.M), and moves them to output/trash/<their_version>_<today>/.

Rules:
  - Only files with a parseable _vN.M tag different from current_version move.
  - Files tagged with the current version stay (including dated copies).
  - Untagged files (review copies, workspace files, non-PDF/DOCX) stay.
  - Nothing under output/trash/ or archive/ or output/archive/ is touched.
  - Nothing is ever deleted; moves are recoverable until the trash is emptied.

Usage:
  python tidy_exports.py --manuscript <dir> [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path

VER_RE = re.compile(r"_v(\d+)\.(\d+)")
SCAN_SUBDIRS = ("exports", "output", "output/share_ready")
EXTS = {".pdf", ".docx"}


def _load_kalam_core():
    """Return the shared kalam_core.metadata module, or None if unavailable."""
    try:
        import sys
        lib = Path(__file__).resolve().parents[3] / "lib"
        if str(lib) not in sys.path:
            sys.path.insert(0, str(lib))
        from kalam_core import metadata as _md
        return _md
    except Exception:
        return None


def read_current_version(meta_path: Path) -> str:
    """Read current_version, requiring the dotted vN.M shape this engine compares on.

    Scalar extraction is shared via kalam_core.metadata; the vN.M shape
    requirement and the SystemExit contract are unchanged.
    """
    _md = _load_kalam_core()
    if _md is not None:
        val = _md.read_scalar(_md.read_text(meta_path.parent), "current_version") or ""
        m = re.match(r'(v\d+\.\d+)', val)
        if m:
            return m.group(1)
        raise SystemExit(f"could not read current_version from {meta_path}")

    # Fallback: original inline implementation (kept identical).
    m = re.search(r'current_version:\s*"?(v\d+\.\d+)', meta_path.read_text())
    if not m:
        raise SystemExit(f"could not read current_version from {meta_path}")
    return m.group(1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manuscript", default=".", help="manuscript root (contains metadata.yaml)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.manuscript).resolve()
    meta = root / "metadata.yaml"
    if not meta.exists():
        raise SystemExit(f"no metadata.yaml in {root}")
    current = read_current_version(meta)
    today = date.today().isoformat()

    moves = []
    for sub in SCAN_SUBDIRS:
        d = root / sub
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if not f.is_file() or f.suffix.lower() not in EXTS:
                continue
            rel = f.relative_to(root)
            if any(str(rel).startswith(p) for p in ("output/trash", "output/archive", "archive")):
                continue
            m = VER_RE.search(f.name)
            if not m:
                continue
            ver = f"v{m.group(1)}.{m.group(2)}"
            if ver == current:
                continue
            dest_dir = root / "output" / "trash" / f"{ver}_{today}"
            moves.append((f, dest_dir / f.name))

    if not moves:
        print(f"tidy-exports: nothing to trash (current {current})")
        return

    for src, dst in moves:
        print(f"  {'DRY ' if args.dry_run else ''}{src.relative_to(root)} -> {dst.relative_to(root)}")
        if not args.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                dst = dst.with_name(dst.stem + "_dup" + dst.suffix)
            shutil.move(str(src), str(dst))

    if not args.dry_run:
        log = root / "logfile.md"
        if log.exists():
            from datetime import datetime
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            with open(log, "a") as fh:
                fh.write(f"- {stamp} [tidy-exports] Moved {len(moves)} superseded export(s) "
                         f"(≠ {current}) to output/trash/ (recoverable).\n")
    print(f"tidy-exports: {'would move' if args.dry_run else 'moved'} {len(moves)} file(s); current {current} kept")


if __name__ == "__main__":
    main()
