"""Depth-agnostic path resolution for the Kalam framework.

Manuscripts may sit at either depth under ``manuscripts/``::

    manuscripts/<name>/                 # depth 1 (e.g. demo-carbon-debt)
    manuscripts/<group>/<name>/         # depth 2 (e.g. coauthor/example-review)

Nothing here assumes a fixed number of ``..`` hops, which is what previously
broke for depth-2 manuscripts. Standard library only.
"""
from __future__ import annotations

from pathlib import Path

#: Marker that identifies a Kalam framework root.
_ROOT_MARKERS = ("AGENTS.md", "skills", "resources")

#: Directory names under ``manuscripts/`` that are not themselves manuscripts.
_NON_MANUSCRIPT_DIRS = {"archive", "_archive"}

#: Maximum grouping levels supported under ``manuscripts/`` (1 = one group dir).
MAX_GROUP_DEPTH = 1


def kalam_root(start: Path | str | None = None) -> Path:
    """Return the framework root by walking upward from *start*.

    Works from a bundled script (``skills/km-x/scripts/y.py``), from a
    manuscript directory at either depth, or from the root itself.
    """
    here = Path(start) if start is not None else Path(__file__)
    here = here.resolve()
    if here.is_file():
        here = here.parent
    for cand in (here, *here.parents):
        if all((cand / m).exists() for m in _ROOT_MARKERS):
            return cand
    raise RuntimeError(
        f"could not locate the Kalam root (looked for {', '.join(_ROOT_MARKERS)}) above {here}"
    )


def manuscripts_dir(root: Path | str | None = None) -> Path:
    """Return ``<root>/manuscripts``."""
    return (kalam_root() if root is None else Path(root)) / "manuscripts"


def is_manuscript_dir(path: Path | str) -> bool:
    """A manuscript directory is any directory holding a ``metadata.yaml``."""
    return (Path(path) / "metadata.yaml").is_file()


def iter_manuscript_dirs(root: Path | str | None = None, include_archive: bool = False):
    """Yield every manuscript directory, at depth 1 and depth 2, sorted.

    Set *include_archive* to also yield manuscripts under ``manuscripts/archive/``
    (excluded by default, since that tree holds superseded snapshots).
    """
    base = manuscripts_dir(root)
    if not base.is_dir():
        return
    seen: list[Path] = []
    for lvl1 in sorted(p for p in base.iterdir() if p.is_dir()):
        archived = lvl1.name in _NON_MANUSCRIPT_DIRS
        if archived and not include_archive:
            continue
        if is_manuscript_dir(lvl1):
            seen.append(lvl1)
            continue
        if MAX_GROUP_DEPTH >= 1:
            for lvl2 in sorted(p for p in lvl1.iterdir() if p.is_dir()):
                if is_manuscript_dir(lvl2):
                    seen.append(lvl2)
    yield from seen


def manuscript_name(mdir: Path | str, root: Path | str | None = None) -> str:
    """Return a manuscript's registry name: its path relative to ``manuscripts/``.

    Depth-1 manuscripts give ``"demo-carbon-debt"``; depth-2 give
    ``"coauthor/example-review"``.
    """
    return Path(mdir).resolve().relative_to(manuscripts_dir(root).resolve()).as_posix()


def add_lib_to_syspath(script_file: Path | str) -> Path:
    """Put ``<root>/lib`` on ``sys.path`` from inside a bundled skill script.

    Lets a script do ``from kalam_core import metadata`` regardless of the
    working directory it was invoked from.
    """
    import sys

    lib = kalam_root(script_file) / "lib"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    return lib
