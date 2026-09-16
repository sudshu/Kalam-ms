#!/usr/bin/env python3
"""Insert page breaks at a manuscript's logical section boundaries.

Breaks go into the *draft markdown*, not into a rendered file, so both the PDF and
the DOCX pick them up from one edit. Each break is a pair of raw blocks:

    ```{=latex}
    \\clearpage
    ```

    ```{=openxml}
    <w:p><w:r><w:br w:type="page"/></w:r></w:p>
    ```

The LaTeX writer ignores the openxml block and the docx writer ignores the LaTeX
one, so a single break definition serves both. This matters because a DOCX export
that strips raw LaTeX (as km-export-docx does, since Word cannot embed PDF figures)
would otherwise silently drop a `\\clearpage`-only break, leaving page breaks in the
PDF and none in the Word file.

Boundaries, each on by default and individually suppressible:

  after-abstract      after the abstract, before the opening paragraph
  before-methods      before Methods, whether a heading or the head of methods.md
  before-references   before the reference list; if the bibliography is generated at
                      build time (pandoc --citeproc with no `# References` heading in
                      the source) the break goes at the end of the last main-text
                      file, which is where the generated heading is appended
  before-si           before the Supplementary Information

Idempotent: a boundary that already carries a break is left alone, so it is safe to
re-run after editing. `--remove` strips every break this script inserts.

Usage:
    python add_page_breaks.py <manuscript_dir> [--dry-run] [--remove]
                              [--no-after-abstract] [--no-before-methods]
                              [--no-before-references] [--no-before-si]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LATEX = "```{=latex}\n\\clearpage\n```"
OPENXML = '```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```'
BREAK = f"{LATEX}\n\n{OPENXML}\n"
BREAK_RE = re.compile(
    r"```\{=latex\}\n\\clearpage\n```\n+```\{=openxml\}\n"
    r'<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n*'
)


def _load_kalam_core():
    here = Path(__file__).resolve()
    for parent in here.parents:
        lib = parent / "lib"
        if (lib / "kalam_core").is_dir():
            sys.path.insert(0, str(lib))
            try:
                from kalam_core import metadata  # type: ignore
                return metadata
            except ImportError:
                return None
    return None


def resolve(mdir: Path):
    """Return (cover, main_files, si_files) using the canonical draft resolution."""
    md = _load_kalam_core()
    if md is None:
        raise SystemExit("kalam_core not importable; cannot resolve current_draft")
    files = md.resolve_draft_files(mdir, legacy=False)
    cover, main, si = None, [], []
    for f in files:
        kind = md.classify(f.name)
        if kind == "cover_letter":
            cover = f
        elif kind == "si":
            si.append(f)
        else:
            main.append(f)
    return cover, main, si


def _has_break_adjacent(text: str, idx: int) -> bool:
    """True if a break already sits at, just before, or just after `idx`.

    Both sides matter: a break inserted before Methods leaves the heading *after* it,
    so the boundary index falls behind the break, while a break inserted after the
    abstract leaves the boundary index pointing *at* the break itself.
    """
    before = text[max(0, idx - 400):idx]
    after = text[idx:idx + 400]
    return bool(BREAK_RE.search(before) or BREAK_RE.match(after.lstrip("\n")))


def _insert(text: str, idx: int) -> str:
    return text[:idx] + BREAK + "\n" + text[idx:]


def _heading(text: str, *words: str):
    """Index of the first top-level heading whose title starts with any of `words`."""
    for m in re.finditer(r"^#{1,2}[ \t]+(.+)$", text, re.M):
        title = m.group(1).strip().lstrip("*").strip()
        if any(title.lower().startswith(w.lower()) for w in words):
            return m.start()
    return None


def after_abstract(text: str):
    """Index of the first body paragraph after the abstract."""
    m = re.search(r"^#{1,3}[ \t]*Abstract[ \t]*$", text, re.M | re.I)
    if not m:
        return None
    rest = text[m.end():]
    # the abstract ends at the next heading or the next horizontal rule
    end = re.search(r"^(?:#{1,6}[ \t]|---[ \t]*$)", rest, re.M)
    if not end:
        return None
    pos = m.end() + end.end()
    nxt = re.search(r"\n(?=\S)", text[pos:])
    return pos + nxt.start() + 1 if nxt else None


def plan(mdir: Path, opts) -> list[tuple[Path, int, str]]:
    cover, main, si = resolve(mdir)
    jobs: list[tuple[Path, int, str]] = []

    if main and opts.after_abstract:
        t = main[0].read_text(encoding="utf-8")
        i = after_abstract(t)
        if i is not None and not _has_break_adjacent(t, i):
            jobs.append((main[0], i, "after the abstract"))

    if opts.before_methods:
        for f in main:
            t = f.read_text(encoding="utf-8")
            i = _heading(t, "Methods", "Online Methods")
            if i is not None:
                if not _has_break_adjacent(t, i):
                    jobs.append((f, i, "before Methods"))
                break

    if opts.before_references:
        target = None
        for f in main:
            t = f.read_text(encoding="utf-8")
            i = _heading(t, "References", "Bibliography")
            if i is not None:
                target = (f, i)
                break
        if target is None and main:
            # generated at build time: the heading is appended to the last main file
            f = main[-1]
            t = f.read_text(encoding="utf-8")
            target = (f, len(t.rstrip("\n")))
        if target:
            f, i = target
            t = f.read_text(encoding="utf-8")
            if not _has_break_adjacent(t, i):
                jobs.append((f, i, "before the reference list"))

    if opts.before_si:
        for f in si:
            t = f.read_text(encoding="utf-8")
            i = _heading(t, "Supplementary")
            i = 0 if i is None else i
            if not _has_break_adjacent(t, i) and i > 0:
                jobs.append((f, i, "before the Supplementary Information"))
            break

    return jobs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manuscript_dir")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--remove", action="store_true", help="strip every inserted break")
    for name in ("after-abstract", "before-methods", "before-references", "before-si"):
        ap.add_argument(f"--no-{name}", dest=name.replace("-", "_"),
                        action="store_false", help=f"skip the {name.replace('-', ' ')} break")
    args = ap.parse_args()
    mdir = Path(args.manuscript_dir).resolve()

    if args.remove:
        cover, main, si = resolve(mdir)
        for f in [*main, *si]:
            t = f.read_text(encoding="utf-8")
            new = BREAK_RE.sub("", t)
            n = len(BREAK_RE.findall(t))
            if n and not args.dry_run:
                f.write_text(new, encoding="utf-8")
            if n:
                print(f"{'would remove' if args.dry_run else 'removed'} {n} from {f.name}")
        return

    jobs = plan(mdir, args)
    if not jobs:
        print("no breaks to add; every boundary already has one")
        return
    # apply back-to-front per file so earlier offsets stay valid
    for f in {j[0] for j in jobs}:
        t = f.read_text(encoding="utf-8")
        for _, idx, label in sorted([j for j in jobs if j[0] is f],
                                    key=lambda j: j[1], reverse=True):
            t = _insert(t, idx)
            print(f"{'would add' if args.dry_run else 'added'}: {label} ({f.name})")
        if not args.dry_run:
            f.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    main()
