#!/usr/bin/env python
"""km-deep-read inventory helper (read-only).

Emits a JSON inventory of a Kalam manuscript so the deep-read coordinator can
build the global cross-reference/citation maps and hand each subagent a clean,
addressable unit (one paragraph, or one figure + caption).

Usage:
    python inventory.py <manuscript_dir>

Looks for the draft files named in <manuscript_dir>/metadata.yaml (current_draft,
a comma-separated list of manuscript-relative paths; see
resources/conventions/manuscript_files.md), falling back to
drafts/v2/{cover_letter,main_text,methods,extended_data_SI}.md.
Prints JSON to stdout. Makes no changes.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

DEFAULT_DRAFTS = ["cover_letter.md", "main_text.md", "methods.md", "extended_data_SI.md"]


def _load_kalam_core():
    """Return the shared kalam_core.metadata module, or None if unavailable.

    Kept optional so this script still runs standalone if copied out of the
    framework tree. See resources/conventions/tooling.md.
    """
    try:
        lib = Path(__file__).resolve().parents[3] / "lib"
        if str(lib) not in sys.path:
            sys.path.insert(0, str(lib))
        from kalam_core import metadata as _md
        return _md
    except Exception:
        return None


def find_files(mdir: Path) -> list[Path]:
    """Resolve this manuscript's draft files.

    Delegates to kalam_core.metadata with the canonical full-path semantics, so a
    current_draft entry such as drafts/v6/main_text.md resolves in place. The older
    legacy=True mode kept only basenames and searched a fixed list of directories
    (drafts/v2, drafts, the manuscript root), which silently returned nothing for
    any manuscript drafting under drafts/<other-version>/.
    """
    _md = _load_kalam_core()
    if _md is not None:
        return _md.resolve_draft_files(mdir, legacy=False)

    # Fallback: original inline implementation (kept identical).
    meta = mdir / "metadata.yaml"
    names: list[str] = []
    if meta.exists():
        txt = meta.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"current_draft:\s*\"?([^\"\n]+)", txt)
        if m:
            names = [n.strip() for n in m.group(1).split(",") if n.strip().endswith(".md")]
    if not names:
        names = DEFAULT_DRAFTS
    out = []
    for n in names:
        # A relative path in current_draft is authoritative; the basename search is
        # only a fallback for older manuscripts that listed bare filenames.
        cands = [mdir / n] if "/" in n else []
        base = Path(n).name
        cands += [mdir / "drafts" / "v2" / base, mdir / "drafts" / base, mdir / base]
        for cand in cands:
            if cand.exists():
                out.append(cand)
                break
    return out


def split_blocks(text: str):
    """Yield (kind, heading, block_text) for each blank-line-separated block."""
    heading = "(front matter)"
    for raw in re.split(r"\n[ \t]*\n", text):
        block = raw.strip("\n")
        s = block.strip()
        if not s:
            continue
        if s.startswith("#"):
            heading = s.lstrip("# ").strip()
            yield ("heading", heading, s)
            continue
        if s.startswith("!["):
            yield ("image", heading, s)
            continue
        # "Fig" must follow "Figure" in the alternation, and the \b keeps it from
        # swallowing "Figure"; without it, captions written "**Fig. 1 | …**" (the
        # Nature house style) were never recognised as display items at all.
        # "Fig(ure)" must be one alternative rather than two, or the \b after a bare
        # "Fig" falls inside "Figure" and "**Supplementary Figure S1 |**" is never
        # classified as a caption at all.
        if re.match(r"\*\*(Supplementary\s+Fig(?:ure)?|Supplementary\s+Tables?"
                    r"|Fig(?:ure)?|Tables?|Extended Data)\b", s):
            yield ("caption", heading, s)
            continue
        if s.startswith("\\") or s.startswith(":::") or s == "---":
            yield ("directive", heading, s)
            continue
        if s.startswith(("- ", "* ", "+ ")):
            yield ("list", heading, s)
            continue
        yield ("paragraph", heading, s)


def panel_letters(caption: str) -> list[str]:
    # Two house styles occur: "**a,**" and the parenthesised "**(a)**" / "**(a, g)**"
    # / "**(a–f)**". Only the first was matched before, so panel-to-caption checks
    # silently saw zero panels on parenthesised captions.
    out = set(re.findall(r"\*\*([a-z]),\*\*", caption))
    for grp in re.findall(r"\*\*\(([a-z][^)]*)\)\*\*", caption):
        out.update(re.findall(r"[a-z]", grp))
    return sorted(out)


def word_count(s: str) -> int:
    s = re.sub(r"\[@[^\]]+\]", "", s)            # citations
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)\{[^}]*\}", "", s)  # images
    s = re.sub(r"[*_`#]", "", s)
    return len(s.split())


# reference patterns (each captures the number/letters)
# A citation number: "3", "3b", "1, 2", "1 and 2", "2–4". The old class
# [0-9][0-9a-z,\s and-]* admitted every lowercase letter AND whitespace, so a
# single "Fig. 3b" ran on across the rest of the sentence and every stray number
# it swallowed ("73%", "1992–2023") was reported as a dangling figure reference.
_NUM = r"([0-9]+[a-z]?(?:\s*(?:,|and|–|—|-)\s*[0-9]+[a-z]?)*)"

# A supplementary item's number carries an "S" (S1, S2), and the Nature house
# style cites it WITHOUT the word "Supplementary" — "Fig. S1", "Figs. S1 and S2".
# Requiring the word meant those forms matched no pattern at all: the citation was
# invisible, so the item was reported uncited while a genuinely uncited one could
# not be told apart. Treat the leading S as the supplementary marker, accept it
# with or without the word, and allow it on every number in a list.
#
# The bare form uses a lookahead so it only fires when an S-number follows, which
# keeps "Fig. 2" out of supp_fig. "table" therefore drops its old trailing S?,
# which would otherwise match "Table S1" as main-text Table 1 as well.
_SNUM = r"(S?[0-9]+[a-z]?(?:\s*(?:,|and|–|—|-)\s*S?[0-9]+[a-z]?)*)"
_FIGW = r"Fig(?:ure)?s?\.?"
_TABW = r"Tables?"

REF_PATTERNS = {
    "supp_fig": rf"(?:Supplementary\s+{_FIGW}\s*|{_FIGW}\s*(?=S[0-9])){_SNUM}",
    "supp_table": rf"(?:Supplementary\s+{_TABW}\s*|{_TABW}\s*(?=S[0-9])){_SNUM}",
    "figure": rf"(?<!Supplementary ){_FIGW}\s*" + _NUM,
    "table": rf"(?<!Supplementary ){_TABW}\s*" + _NUM,
    "equation": r"Eq(?:s|\.|uation)?\.?\s*" + _NUM,
    "section": r"§\s*([0-9][0-9.]*)",
}


def main() -> None:
    mdir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files = find_files(mdir)

    paragraphs, figures, crossrefs = [], [], []
    existing = {"figure": set(), "supp_fig": set(), "supp_table": set(), "table": set()}
    cite_keys = set()
    pidx = 0
    last_image = None

    for f in files:
        fname = f.name
        text = f.read_text(encoding="utf-8", errors="replace")
        for kind, heading, block in split_blocks(text):
            if kind == "image":
                last_image = re.search(r"\(([^)]+)\)", block)
                last_image = last_image.group(1) if last_image else None
            elif kind == "caption":
                label = re.match(r"\*\*([^|]+?)\s*\|", block)
                label = label.group(1).strip() if label else block[:40]
                # register existing display item
                # S? because supplementary items are numbered S1, S2, … — without it
                # no supplementary figure or table was ever registered as existing.
                # Same rule as REF_PATTERNS: the word "Supplementary" OR an "S"
                # before the number marks the item supplementary. Without this,
                # "**Supplementary Figure S1 |**" was misfiled as main-text Figure 1
                # (colliding with the real Figure 1), and "**Table S1 |**" was
                # registered as main-text Table 1 while the text cited it as
                # "Supplementary Table S1", leaving a false dangling reference.
                mnum = re.search(
                    r"(Supplementary\s+)?(Fig(?:ure)?s?|Tables?)\.?\s*(S)?([0-9]+)", label)
                if mnum:
                    is_supp = bool(mnum.group(1)) or bool(mnum.group(3))
                    is_fig = mnum.group(2).lower().startswith("fig")
                    if is_supp:
                        key = "supp_fig" if is_fig else "supp_table"
                    else:
                        key = "figure" if is_fig else "table"
                    existing[key].add(mnum.group(4))
                figures.append({
                    "file": fname, "label": label, "image": last_image,
                    "panels": panel_letters(block),
                    "caption_words": word_count(block),
                    "caption_preview": block[:160],
                })
                last_image = None
                # captions also cite refs/keys. The lookbehind keeps an email
                # address (name@institution.edu) from being read as a citation key.
                for k in re.findall(r"(?<![\w.])@([A-Za-z][\w:-]+)", block):
                    cite_keys.add(k)
            elif kind == "paragraph":
                pidx += 1
                topic = block.split(". ")[0][:140]
                paragraphs.append({
                    "n": pidx, "file": fname, "section": heading,
                    "words": word_count(block), "topic_sentence": topic,
                    "text": block,
                })
                for k in re.findall(r"(?<![\w.])@([A-Za-z][\w:-]+)", block):
                    cite_keys.add(k)
                for rtype, pat in REF_PATTERNS.items():
                    for m in re.finditer(pat, block):
                        nums = re.findall(r"[0-9]+", m.group(1))
                        for num in nums:
                            crossrefs.append({"type": rtype, "num": num,
                                              "file": fname, "para": pidx})

    # bib keys
    bib_keys = set()
    bib = mdir / "references.bib"
    if bib.exists():
        bib_keys = set(re.findall(r"@\w+\{\s*([^,\s]+)\s*,",
                                  bib.read_text(encoding="utf-8", errors="replace")))
    missing_cites = sorted(k for k in cite_keys if k not in bib_keys)

    # dangling cross-refs (referenced number has no matching existing item)
    dangling = []
    for cr in crossrefs:
        if cr["type"] in existing and cr["num"] not in existing[cr["type"]]:
            dangling.append(cr)
    uncited = {t: sorted(existing[t] - {c["num"] for c in crossrefs if c["type"] == t})
               for t in existing}

    out = {
        "manuscript_dir": str(mdir),
        "files": [f.name for f in files],
        "counts": {
            "paragraphs": len(paragraphs), "figures": len(figures),
            "crossrefs": len(crossrefs), "cite_keys": len(cite_keys),
            "bib_keys": len(bib_keys),
        },
        "existing_display_items": {k: sorted(v, key=lambda x: int(x)) for k, v in existing.items()},
        "uncited_display_items": uncited,
        "dangling_crossrefs": dangling,
        "missing_cite_keys": missing_cites,
        "paragraphs": paragraphs,
        "figures": figures,
        "crossrefs": crossrefs,
        "cite_keys": sorted(cite_keys),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
