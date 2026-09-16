#!/usr/bin/env python3
"""km-bump-version engine.

Rolls a Kalam manuscript's version forward (major/integer or minor/dot),
sweeps superseded build artifacts (.pdf/.docx) to a trash folder, optionally
archives explicitly-named version-specific source files, and keeps every
version reference in sync (metadata.yaml + hardcoded build-script VERSION lines).

Safety model
------------
- Default is a DRY RUN: it prints a JSON plan and changes nothing.
- ``--apply`` performs the changes. It first pre-flights every write target;
  if anything is not writable it aborts before mutating. Mutations run in a
  recover-friendly order (file moves + build-script edits first, then metadata
  and the log), so a mid-run failure never leaves metadata advanced past the
  files it describes.
- Build outputs (.pdf/.docx) are MOVED to ``output/trash/<old>_<date>/`` — never
  deleted. They are git-ignored and regenerable from sources, so this is safe.
- Source files are archived ONLY when explicitly listed with ``--archive`` and
  are MOVED to ``archive/<old>/``. Living drafts (main_text.md, methods.md, ...)
  are refused unless ``--force-archive`` is given.
- Files already at the new version, and files with no parseable version tag,
  are left in place.

Version model: ``v<major>[.<minor>]`` (e.g. v4.1, also tolerates v4 -> v4.1).
Patch-level versions (v4.1.2) are rejected explicitly rather than truncated.
  major/integer bump:  v4.1 -> v5.0
  minor/dot bump:      v4.1 -> v4.2   (v4 -> v4.1)
  explicit set:        --set v5.3     (warns if not greater than current)

Usage
-----
  bump_version.py --metadata PATH (--bump {major,minor} | --set vX.Y)
                  [--date YYYY-MM-DD] [--archive SRC ...] [--force-archive]
                  [--apply]
"""

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import sys

VERSION_RE = re.compile(r"v(\d+)(?:\.(\d+))?")
PATCH_RE = re.compile(r"v\d+\.\d+\.\d+")
# A hardcoded build-script version line, e.g. `VERSION=v4.1`, `VERSION="v4.1"`,
# or `VERSION=v4.1  # comment`. Captures the prefix, the (optional) quote char,
# and any trailing whitespace/comment so they can be preserved on rewrite.
# Deliberately does NOT match parameterized lines like
# `VERSION="${VERSION:-$(grep ...)}"`, which auto-follow metadata.
HARDCODED_VERSION_LINE = re.compile(
    r'^(?P<prefix>\s*VERSION=)(?P<q>["\']?)v\d+(?:\.\d+)?(?P=q)(?P<rest>\s*(?:#.*)?)$'
)
# Living-draft basenames that must never be silently archived.
LIVING_DRAFTS = {
    "main_text.md", "methods.md", "extended_data_SI.md", "cover_letter.md",
    "abstract.md", "ideation.md", "skeleton.md", "response_to_reviewers.md",
    "supplementary_information.md", "manuscript.md",
}


def parse_version(s):
    """Return (major, minor) from a version string like 'v4.1' or 'v4'.

    Patch-level versions (v4.1.2) are rejected rather than silently truncated.
    """
    s = (s or "").strip()
    if PATCH_RE.search(s):
        raise ValueError(f"patch-level versions are not supported: {s!r} (use vMAJOR.MINOR)")
    m = VERSION_RE.search(s)
    if not m:
        raise ValueError(f"cannot parse a vMAJOR.MINOR version from {s!r}")
    return int(m.group(1)), int(m.group(2) or 0)


def fmt_version(major, minor):
    return f"v{major}.{minor}"


def compute_new_version(current, bump=None, explicit=None):
    cur = parse_version(current)
    if explicit is not None:
        new = parse_version(explicit)
        return fmt_version(*new), new, cur
    if bump == "major":
        new = (cur[0] + 1, 0)
    elif bump == "minor":
        new = (cur[0], cur[1] + 1)
    else:
        raise ValueError("must pass --bump or --set")
    return fmt_version(*new), new, cur


def _load_kalam_core():
    """Return the shared kalam_core.metadata module, or None if unavailable."""
    try:
        from pathlib import Path as _P
        lib = _P(__file__).resolve().parents[3] / "lib"
        if str(lib) not in sys.path:
            sys.path.insert(0, str(lib))
        from kalam_core import metadata as _md
        return _md
    except Exception:
        return None


def read_current_version(meta_path):
    """Read current_version, accepting vN or vN.M (this engine's historical shape).

    Scalar extraction is shared via kalam_core.metadata; the accepted shapes and
    the ValueError contract are unchanged.
    """
    _md = _load_kalam_core()
    if _md is not None:
        from pathlib import Path as _P
        val = _md.read_scalar(_md.read_text(_P(meta_path).parent), "current_version") or ""
        m = re.match(r'(v\d+(?:\.\d+)?)', val)
        if m:
            return m.group(1).strip()
        raise ValueError(f"no current_version field in {meta_path}")

    # Fallback: original inline implementation (kept identical).
    with open(meta_path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r'^current_version:\s*"?(v\d+(?:\.\d+)?)"?', line)
            if m:
                return m.group(1).strip()
    raise ValueError(f"no current_version field in {meta_path}")


def file_version_tag(name):
    """Extract the version token from an output filename, or None.

    Accepts a token bounded by '_' or the start/end of the stem (extension
    stripped), so both 'manuscript_v4.1_main_2026-06-12.pdf' and a terminal
    'supp_v4.0.docx' resolve. To avoid mistaking a year-like '_v2024_' for a
    version, the bare (no-dot) form is limited to 1-2 digits; dotted forms
    (v4.1, v10.2) are accepted at any width.
    """
    stem = os.path.splitext(name)[0]
    m = re.search(r"(?:^|_)(v\d+\.\d+|v\d{1,2})(?=_|$)", stem)
    return m.group(1) if m else None


def _rel(root, path):
    return os.path.relpath(path, root)


def scan_outputs(root, new_tuple):
    """Classify build artifacts under output/ into trash / kept / skipped.

    Comparison is on parsed (major, minor) tuples so 'v4' and 'v4.0' match.
    Excludes anything already under output/archive/ or output/trash/.
    """
    out_dir = os.path.join(root, "output")
    to_trash, kept, skipped = [], [], []
    if not os.path.isdir(out_dir):
        return to_trash, kept, skipped
    for dirpath, dirnames, filenames in os.walk(out_dir):
        parts = set(_rel(out_dir, dirpath).split(os.sep))
        if "archive" in parts or "trash" in parts:
            dirnames[:] = []
            continue
        for fn in filenames:
            if not fn.lower().endswith((".pdf", ".docx")):
                continue
            full = os.path.join(dirpath, fn)
            tag = file_version_tag(fn)
            if tag is None:
                skipped.append(_rel(root, full))
                continue
            try:
                tag_tuple = parse_version(tag)
            except ValueError:
                skipped.append(_rel(root, full))
                continue
            (kept if tag_tuple == new_tuple else to_trash).append(_rel(root, full))
    return sorted(to_trash), sorted(kept), sorted(skipped)


def scan_build_scripts(root, new_version):
    """Find build scripts with a hardcoded VERSION= line that needs updating."""
    hits, candidates = [], []
    for base in (root, os.path.join(root, "drafts")):
        if not os.path.isdir(base):
            continue
        for dirpath, _dn, filenames in os.walk(base):
            for fn in filenames:
                if fn.startswith("build") and fn.endswith(".sh"):
                    candidates.append(os.path.join(dirpath, fn))
    for path in sorted(set(candidates)):
        with open(path, encoding="utf-8") as fh:
            for i, line in enumerate(fh, 1):
                m = HARDCODED_VERSION_LINE.match(line.rstrip("\n"))
                if m:
                    new_line = f'{m.group("prefix")}{m.group("q")}{new_version}{m.group("q")}{m.group("rest")}'
                    hits.append({"path": _rel(root, path), "line": i,
                                 "from": line.strip(), "to": new_line.strip()})
    return hits


def _retag(value, old_version, new_version):
    """Replace genuine '_vOLD' filename tags only, leaving path segments alone.

    Matches an old-version token that is preceded by '_' and followed by a
    boundary (_ . / whitespace or end), so 'manuscript_v4.1_main' is retagged
    while 'drafts/v2/' (no leading '_') and 'v4.12' (no boundary) are not.
    """
    pat = re.compile(r"_" + re.escape(old_version) + r"(?=[_./\s]|$)")
    return pat.sub("_" + new_version, value)


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def plan_metadata_changes(meta_path, old_version, new_version, date):
    changes = []
    text = _read(meta_path)
    for field, newval in (
        ("current_version", f'"{new_version}"'),
        ("prior_version", f'"{old_version} ({date})"'),
        ("last_updated", f'"{date}"'),
    ):
        m = re.search(rf'^{field}:[ \t]*([^\n#]*)(#.*)?$', text, re.M)
        if m and m.group(1).strip() != newval:
            changes.append({"field": field, "from": m.group(1).strip(), "to": newval})
    for field in _retaggable_fields(text):
        m = re.search(rf'^{field}:[ \t]*(.*)$', text, re.M)
        if m:
            retagged = _retag(m.group(1), old_version, new_version)
            if retagged != m.group(1):
                changes.append({"field": field, "from": m.group(1).strip(),
                                "to": retagged.strip(),
                                "note": "version filename-tag only; rebuild to produce files"})
    return changes


# Keys whose values may carry a version filename-tag. current_pdf and current_draft are the
# documented ones; x_-prefixed extension keys (metadata_schema.md) routinely hold sibling
# artifact paths such as x_current_supplementary_pdf, and were previously left stale.
def _retaggable_fields(text):
    fields = ["current_pdf", "current_draft"]
    fields += [m.group(1) for m in re.finditer(r'^(x_[A-Za-z0-9_]*(?:pdf|docx|draft)[A-Za-z0-9_]*):',
                                               text, re.M)]
    seen, out = set(), []
    for f in fields:
        if f not in seen:
            seen.add(f); out.append(f)
    return out


def apply_metadata(meta_path, old_version, new_version, date):
    text = _read(meta_path)

    def repl_field(field, newval):
        # preserve any trailing inline comment
        return lambda m: f'{field}: {newval}' + (f'  {m.group(2)}' if m.group(2) else '')

    for field, newval in (
        ("current_version", f'"{new_version}"'),
        ("prior_version", f'"{old_version} ({date})"'),
        ("last_updated", f'"{date}"'),
    ):
        text = re.sub(rf'^({field}):[ \t]*[^\n#]*?[ \t]*(#.*)?$',
                      repl_field(field, newval), text, flags=re.M)
    for field in _retaggable_fields(text):
        def _sub(m, field=field):
            return f'{field}:' + _retag(m.group(1), old_version, new_version)
        text = re.sub(rf'^{field}:(.*)$', _sub, text, flags=re.M)
    with open(meta_path, "w", encoding="utf-8") as fh:
        fh.write(text)


def apply_build_scripts(root, hits, new_version):
    for hit in hits:
        path = os.path.join(root, hit["path"])
        with open(path, encoding="utf-8") as fh:
            lines = fh.readlines()
        idx = hit["line"] - 1
        m = HARDCODED_VERSION_LINE.match(lines[idx].rstrip("\n"))
        if m:
            lines[idx] = f'{m.group("prefix")}{m.group("q")}{new_version}{m.group("q")}{m.group("rest")}\n'
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(lines)


def _safe_move(src, dest_dir, root):
    os.makedirs(dest_dir, exist_ok=True)
    base = os.path.basename(src)
    dest = os.path.join(dest_dir, base)
    stem, ext = os.path.splitext(base)
    n = 1
    while os.path.exists(dest):
        dest = os.path.join(dest_dir, f"{stem}_{n}{ext}")
        n += 1
    shutil.move(src, dest)
    return _rel(root, dest)


def apply_moves(root, rel_paths, dest_dir_rel):
    dest_dir = os.path.join(root, dest_dir_rel)
    moved = []
    for rel in rel_paths:
        src = os.path.join(root, rel)
        if os.path.exists(src):
            moved.append(_safe_move(src, dest_dir, root))
    return moved


def append_log(root, line):
    log_path = os.path.join(root, "logfile.md")
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(line if line.endswith("\n") else line + "\n")


def preflight(root, meta_path, build_hits, to_trash, archive_sources, trash_dir_rel, archive_dir_rel):
    """Return a list of writability problems; empty means safe to apply."""
    problems = []

    def writable(path):
        return os.access(path, os.W_OK)

    if not writable(meta_path):
        problems.append(f"metadata.yaml not writable: {_rel(root, meta_path)}")
    log_path = os.path.join(root, "logfile.md")
    if os.path.exists(log_path) and not writable(log_path):
        problems.append("logfile.md not writable")
    elif not writable(root):
        problems.append("manuscript root not writable (cannot create logfile.md)")
    for hit in build_hits:
        if not writable(os.path.join(root, hit["path"])):
            problems.append(f"build script not writable: {hit['path']}")
    for group, dest in ((to_trash, trash_dir_rel), (archive_sources, archive_dir_rel)):
        for rel in group:
            src = os.path.join(root, rel)
            if os.path.exists(src) and not writable(os.path.dirname(src)):
                problems.append(f"source dir not writable, cannot move: {rel}")
        if group:
            anchor = os.path.join(root, dest)
            while not os.path.exists(anchor):
                anchor = os.path.dirname(anchor)
            if not writable(anchor):
                problems.append(f"destination not writable: {dest}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Kalam version bump engine")
    ap.add_argument("--metadata", required=True, help="path to manuscript metadata.yaml")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--bump", choices=["major", "minor"], help="major/integer or minor/dot bump")
    g.add_argument("--set", dest="explicit", help="set an explicit version, e.g. v5.3")
    ap.add_argument("--date", default=None, help="date stamp YYYY-MM-DD (default: today)")
    ap.add_argument("--archive", nargs="*", default=[],
                    help="explicit version-specific SOURCE files/dirs to archive (relative to manuscript root)")
    ap.add_argument("--force-archive", action="store_true",
                    help="allow archiving files whose names match living drafts (use with care)")
    ap.add_argument("--apply", action="store_true", help="perform changes (default: dry run)")
    args = ap.parse_args(argv)

    meta_path = os.path.abspath(args.metadata)
    if not os.path.isfile(meta_path):
        ap.error(f"metadata not found: {meta_path}")
    root = os.path.dirname(meta_path)
    date = args.date or _dt.date.today().isoformat()

    try:
        current = read_current_version(meta_path)
        new_version, new_tuple, cur_tuple = compute_new_version(
            current, bump=args.bump, explicit=args.explicit)
    except ValueError as e:
        ap.error(str(e))

    warnings = []
    if args.explicit and new_tuple < cur_tuple:
        warnings.append(f"requested {new_version} is lower than current {current} (downgrade)")
    if new_tuple == cur_tuple:
        warnings.append(f"new version equals current ({current}); nothing to bump")

    bump_type = args.bump or "explicit"
    to_trash, kept, skipped = scan_outputs(root, new_tuple)
    build_hits = scan_build_scripts(root, new_version)
    meta_changes = plan_metadata_changes(meta_path, current, new_version, date)

    trash_dir_rel = os.path.join("output", "trash", f"{current}_{date}")
    archive_dir_rel = os.path.join("archive", current)

    archive_sources, refused = [], []
    for a in args.archive:
        full = os.path.join(root, a)
        if not os.path.exists(full):
            warnings.append(f"archive source not found, skipped: {a}")
        elif os.path.basename(a) in LIVING_DRAFTS and not args.force_archive:
            refused.append(a)
            warnings.append(f"refused to archive living draft {a} (pass --force-archive to override)")
        else:
            archive_sources.append(a)

    plan = {
        "applied": False,
        "old_version": current,
        "new_version": new_version,
        "bump_type": bump_type,
        "date": date,
        "metadata_changes": meta_changes,
        "build_scripts": build_hits,
        "outputs_to_trash": to_trash,
        "outputs_kept_current": kept,
        "outputs_skipped_no_tag": skipped,
        "sources_to_archive": archive_sources,
        "sources_refused_living_draft": refused,
        "trash_dir": trash_dir_rel,
        "archive_dir": archive_dir_rel if archive_sources else None,
        "warnings": warnings,
    }

    if args.apply:
        if new_tuple == cur_tuple:
            print(json.dumps(plan, indent=2))
            print("ABORT: new version equals current; nothing applied.", file=sys.stderr)
            return 2
        problems = preflight(root, meta_path, build_hits, to_trash, archive_sources,
                             trash_dir_rel, archive_dir_rel)
        if problems:
            plan["warnings"].extend(problems)
            print(json.dumps(plan, indent=2))
            print("ABORT: targets not writable; nothing applied:\n  " + "\n  ".join(problems),
                  file=sys.stderr)
            return 3
        # recover-friendly order: moves + build edits first, metadata + log last
        done = []
        try:
            apply_build_scripts(root, build_hits, new_version); done.append("build_scripts")
            trashed = apply_moves(root, to_trash, trash_dir_rel); done.append("trash")
            archived = apply_moves(root, archive_sources, archive_dir_rel) if archive_sources else []
            done.append("archive")
            apply_metadata(meta_path, current, new_version, date); done.append("metadata")
            now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bits = [f"Version bump {current} -> {new_version} ({bump_type})"]
            if trashed:
                bits.append(f"moved {len(trashed)} superseded output(s) to {trash_dir_rel}/")
            if archived:
                bits.append(f"archived {len(archived)} source file(s) to {archive_dir_rel}/")
            if build_hits:
                bits.append(f"updated VERSION in {len(build_hits)} build script(s)")
            append_log(root, f"- {now} — " + "; ".join(bits) + "."); done.append("log")
        except Exception as e:  # noqa: BLE001 - report partial progress, don't mask
            plan["error"] = str(e)
            plan["completed_steps"] = done
            print(json.dumps(plan, indent=2))
            print(f"ERROR after completing {done}: {e}", file=sys.stderr)
            return 4
        plan["applied"] = True
        plan["trashed"] = trashed
        plan["archived"] = archived

    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
