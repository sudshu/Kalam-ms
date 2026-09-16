"""The single home for reading a Kalam manuscript's ``metadata.yaml``.

Before 2026-09-09 four bundled scripts each carried their own regex for this
(``inventory.py``, ``make_audio.py``, ``tidy_exports.py``, ``bump_version.py``)
and they had **diverged**. This module keeps one implementation of each parsing
primitive and, critically, makes the surviving divergence explicit instead of
hidden.

Deliberately standard-library only: no PyYAML dependency, matching the
regex-based behaviour the callers already relied on.

Two draft-resolution semantics exist
------------------------------------
``current_draft_entries`` — **canonical**. Comma-separated, manuscript-relative
paths, kept whole, exactly as specified by
``resources/conventions/manuscript_files.md``.

``draft_tokens_legacy_basename`` — **legacy**, reproducing ``inventory.py``'s
historical token scan. It matches only ``[A-Za-z0-9_]+\\.md`` and therefore
**discards any subdirectory** in a ``current_draft`` entry. Kept so the existing
inventory output stays bit-identical.

Known consequence of the legacy behaviour (recorded 2026-09-09, not yet
resolved): for ``manuscripts/example-paper``, ``current_draft`` names
``drafts/nature_editorial_rebuild/{main_text,methods,extended_data_SI}.md`` but
the legacy scan reduces these to bare filenames and the search order finds
``drafts/v2/*.md`` first — so the inventory-consuming audit skills read a stale
v2 draft. ``make_audio.py``, which uses the canonical semantics, resolves the
same manuscript correctly. Switching ``inventory.py`` to the canonical function
fixes this but changes which files those audits read, so it is a deliberate
decision for the user rather than a silent change.
"""
from __future__ import annotations

import re
from pathlib import Path

#: Fallback draft names used by the inventory helper when ``current_draft`` is absent.
DEFAULT_DRAFTS = ["cover_letter.md", "main_text.md", "methods.md", "extended_data_SI.md"]

#: Search order applied to a bare draft filename, relative to the manuscript root.
DEFAULT_SEARCH_SUBDIRS = (("drafts", "v2"), ("drafts",), ())


def read_text(mdir: Path | str) -> str:
    """Return the raw text of ``<mdir>/metadata.yaml``, or ``""`` if absent."""
    meta = Path(mdir) / "metadata.yaml"
    if not meta.exists():
        return ""
    return meta.read_text(encoding="utf-8", errors="replace")


def read_scalar(text: str, key: str) -> str | None:
    """Return the first top-level scalar value for *key*.

    Strips surrounding quotes and any trailing ``#`` comment — the pattern every
    caller previously reimplemented.
    """
    m = re.search(rf'^{re.escape(key)}:\s*(.*)$', text, flags=re.M)
    if not m:
        return None
    val = m.group(1).strip()
    if val.startswith(('"', "'")):
        quote = val[0]
        end = val.find(quote, 1)
        if end != -1:
            return val[1:end]
        val = val[1:]
    val = val.split("#", 1)[0].strip()
    return val or None


def current_draft_entries(text: str) -> list[str]:
    """Canonical resolution: comma-separated manuscript-relative paths, kept whole.

    Implements ``resources/conventions/manuscript_files.md``.
    """
    raw = read_scalar(text, "current_draft")
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def draft_tokens_legacy_basename(text: str) -> list[str]:
    """Legacy resolution used by ``inventory.py``: bare ``*.md`` tokens only.

    Discards subdirectories. See the module docstring for why this is retained.
    """
    m = re.search(r"current_draft:\s*\"?([^\"\n]+)", text)
    if not m:
        return []
    return re.findall(r"[A-Za-z0-9_]+\.md", m.group(1))


def locate(mdir: Path | str, names, search_subdirs=DEFAULT_SEARCH_SUBDIRS) -> list[Path]:
    """Resolve each name in *names* to the first existing candidate path.

    A name containing a separator is honoured as-is relative to the manuscript
    root; a bare filename is looked up through *search_subdirs* in order.
    """
    mdir = Path(mdir)
    out: list[Path] = []
    for n in names:
        if "/" in n:
            cand = mdir / n
            if cand.exists():
                out.append(cand)
            continue
        for sub in search_subdirs:
            cand = mdir.joinpath(*sub, n) if sub else mdir / n
            if cand.exists():
                out.append(cand)
                break
    return out


def resolve_draft_files(mdir: Path | str, legacy: bool = False) -> list[Path]:
    """Resolve a manuscript's draft files.

    *legacy=True* reproduces ``inventory.py``'s historical behaviour exactly
    (basename tokens + ``DEFAULT_DRAFTS`` fallback). *legacy=False* uses the
    canonical full-path semantics.
    """
    text = read_text(mdir)
    if legacy:
        names = draft_tokens_legacy_basename(text) or DEFAULT_DRAFTS
    else:
        names = current_draft_entries(text) or DEFAULT_DRAFTS
    return locate(mdir, names)


def first_draft(mdir: Path | str, default: str = "drafts/manuscript.md") -> Path:
    """Return the first ``current_draft`` entry as a path (``make_audio`` semantics)."""
    entries = current_draft_entries(read_text(mdir))
    return Path(mdir) / (entries[0] if entries else default)


def classify(name: str) -> str:
    """Classify a draft filename per ``manuscript_files.md``.

    Returns ``"cover_letter"``, ``"si"`` or ``"main_text"``.
    """
    stem = Path(name).name.lower()
    if "cover_letter" in stem:
        return "cover_letter"
    if "supplementary" in stem or "extended_data" in stem or "_si" in stem:
        return "si"
    return "main_text"
