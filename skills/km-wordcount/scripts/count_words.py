#!/usr/bin/env python3
"""
Count words in a Kalam manuscript following Nature-family journal rules.

Sections are identified by Markdown headings. Word counts exclude:
- Abstract
- Methods (## Methods and everything after it)
- References
- Figure/table captions (lines starting with **Fig. or **Table)
- Markdown image links ![...](...)
- Citation markers [@...]
- Author-year citations written as plain text, e.g. (Smith et al., 2024) or
  (A et al., 2013; B and C, 2019), and the year in narrative citations such as
  Smith et al. (2024). These render as superscript numerals in the submitted PDF,
  so counting them as prose overstates a manuscript by roughly 5-6%.
- Heading markers (# ## ###)
- LaTeX math expressions

Usage:
    python count_words.py <path_to_manuscript.md> [<more.md> ...]

If one file is given, it is parsed section-aware (abstract / main text / Methods)
for the classic single-file layout. If several files are given (the Nature-family
split: main_text.md, methods.md, ...), each file is counted as prose and a combined
total is reported under "files"/"total_prose_words", alongside the section-aware
parse of the first file for convenience.

Output: JSON with section-level word counts.
"""

import re
import sys
import json
from pathlib import Path


# A name token inside a citation: a capitalised surname or initial, a lowercase
# nobiliary particle ("van der Werf", "de Laat"), or the "et al." / "and" glue.
_CITE_NAME = (
    r"(?:[A-Z\u00C0-\u00DE][\w.'\u2019\u00C0-\u024F-]*"
    r"|van|von|de|der|den|del|della|di|du|dos|da|la|le|el|and|&|et|al\.)"
)
# One citation inside a group: name tokens, then a comma and one or more years.
#   "Friedlingstein et al., 2026"   "Wolter and Timlin, 2011"   "Bolton, 1980"
#   "van der Werf et al., 2025"     "Humphrey et al., 2018, 2021"
_CITE_SEGMENT = re.compile(
    r"^\s*(?:" + _CITE_NAME + r"\s*)+,\s*\d{4}[a-z]?(?:\s*,\s*\d{4}[a-z]?)*\s*$"
)
# Narrative form: keep the author, drop the year. "Yun et al. (2025)" prints as
# "Yun et al.25", so the name is prose and only the parenthesis disappears.
_NARRATIVE_CITE = re.compile(
    r"(et\s+al\.|[A-Z\u00C0-\u00DE][\w'\u2019\u00C0-\u024F-]+)"
    r"\s*\(\s*\d{4}[a-z]?(?:\s*,\s*\d{4}[a-z]?)*\s*\)"
)


def strip_author_year_citations(text: str) -> str:
    """Drop plain-text author-year citations, keeping non-citation parentheticals.

    A parenthetical may mix the two, as in "(Kaiser et al., 2012; Supplementary
    Note 1)". Only the citation segments are removed; what is left is kept and the
    brackets are dropped only when nothing survives. Parentheticals without a
    trailing year -- "(Fig. 3c)", "(Methods)", "(95% interval, 42-65%)" -- are
    never touched.
    """
    text = _NARRATIVE_CITE.sub(r"\1", text)

    def replace_group(match: "re.Match[str]") -> str:
        kept = [seg.strip() for seg in match.group(1).split(";")
                if not _CITE_SEGMENT.match(seg)]
        return "(" + "; ".join(kept) + ")" if kept else ""

    text = re.sub(r"\(([^()]*)\)", replace_group, text)
    # Removing "(Smith, 2019)" from "decades (Smith, 2019), and" strands the comma as
    # its own token; reattach trailing punctuation so it is not counted as a word.
    text = re.sub(r"[ \t]+([,.;:!?\)\]])", r"\1", text)
    text = re.sub(r"([\(\[])[ \t]+", r"\1", text)
    return re.sub(r"[ \t]{2,}", " ", text)


def strip_markdown(text: str) -> str:
    """Remove markdown/LaTeX artifacts, keeping only prose words."""
    # Remove image links ![...](...)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Remove citation markers [@...]
    text = re.sub(r'\[@[^\]]*\]', '', text)
    # Remove plain-text author-year citations, which render as superscript numerals
    text = strip_author_year_citations(text)
    # Remove inline LaTeX $...$
    text = re.sub(r'\$[^$]+\$', 'X', text)
    # Remove heading markers but keep heading words
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*{1,3}', '', text)
    # Remove horizontal rules
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    return text


def is_caption_line(line: str) -> bool:
    """Check if a line is a figure or table caption."""
    stripped = line.strip()
    # Matches **Fig. or **Table or (a)** panel descriptions within captions
    return bool(re.match(r'\*{0,2}Fig\.|^\*{0,2}Table\s', stripped))


def extract_caption_block(text: str) -> tuple[str, str]:
    """
    Extract caption blocks from text, returning (text_without_captions, captions_only).

    Captions start with **Fig. or **Table and continue until a blank line
    or a new heading.
    """
    lines = text.split('\n')
    caption_lines = []
    non_caption_lines = []
    in_caption = False

    for line in lines:
        stripped = line.strip()

        # Caption starts
        if re.match(r'\*{0,2}Fig\.\s|^\*{0,2}Table\s\d', stripped):
            in_caption = True
            caption_lines.append(line)
            continue

        # Caption ends at blank line or new heading
        if in_caption:
            if stripped == '' or stripped.startswith('#'):
                in_caption = False
                non_caption_lines.append(line)
            else:
                caption_lines.append(line)
            continue

        non_caption_lines.append(line)

    return '\n'.join(non_caption_lines), '\n'.join(caption_lines)


def count_words(text: str) -> int:
    """Count words in cleaned text."""
    cleaned = strip_markdown(text)
    return len(cleaned.split())


def prose_words(text: str) -> int:
    """Count prose words in a whole file, excluding figure/table caption blocks."""
    body, _captions = extract_caption_block(text)
    return count_words(body)


def parse_manuscript(filepath: str) -> dict:
    """
    Parse a Kalam manuscript and return section-level word counts.

    Returns dict with:
        abstract_words: int
        main_text_words: int  (opening + Results + Discussion, no captions)
        caption_words: int
        methods_words: int
        main_text_with_captions: int
        sections: dict of section_name -> word_count
    """
    text = Path(filepath).read_text(encoding='utf-8')
    lines = text.split('\n')

    # Locate the structure by whole lines, not by the raw '---' substring: a
    # manuscript that marks its abstract with a '## Abstract' heading and closes
    # it with a single horizontal rule yields only two substring parts, which
    # previously swept the entire body into abstract_section and reported a
    # main text of zero.
    seps = [i for i, l in enumerate(lines) if l.strip() == '---']
    abs_head = next((i for i, l in enumerate(lines)
                     if re.match(r'^##\s*Abstract\b', l.strip(), flags=re.IGNORECASE)), None)

    if abs_head is not None:
        stop = next((j for j in range(abs_head + 1, len(lines))
                     if lines[j].strip() == '---' or re.match(r'^##\s+', lines[j].strip())),
                    len(lines))
        abstract_section = '\n'.join(lines[abs_head + 1:stop])
        rest_start = stop + 1 if stop < len(lines) and lines[stop].strip() == '---' else stop
        rest = '\n'.join(lines[rest_start:])
    elif len(seps) >= 2:
        # Classic: title --- abstract --- rest
        abstract_section = '\n'.join(lines[seps[0] + 1:seps[1]])
        rest = '\n'.join(lines[seps[1] + 1:])
    elif len(seps) == 1:
        abstract_section = '\n'.join(lines[:seps[0]])
        rest = '\n'.join(lines[seps[0] + 1:])
    else:
        abstract_section = ''
        rest = text

    # Count abstract words (strip the ## Abstract heading if present)
    abstract_text = re.sub(r'^##\s*Abstract\s*$', '', abstract_section, flags=re.MULTILINE)
    abstract_words = count_words(abstract_text)

    # Split rest into main text and Methods
    methods_split = re.split(r'^##\s+Methods\b', rest, maxsplit=1, flags=re.MULTILINE)
    main_text_raw = methods_split[0]
    methods_raw = methods_split[1] if len(methods_split) > 1 else ''
    # Methods stops where the back matter starts, so availability statements,
    # acknowledgements and the reference list are not billed to the Methods limit.
    methods_raw = re.split(
        r'^##\s+(?:Data Availability|Code Availability|Acknowledge?ments?|'
        r'Author Contributions|Competing Interests|References)\b',
        methods_raw, maxsplit=1, flags=re.MULTILINE | re.IGNORECASE)[0]

    # Separate captions from main text
    main_no_captions, captions_only = extract_caption_block(main_text_raw)

    main_text_words = count_words(main_no_captions)
    caption_words = count_words(captions_only)
    methods_words = count_words(methods_raw)

    # Section-level breakdown of main text
    sections = {}
    current_section = "Opening"
    current_text = []

    for line in main_no_captions.split('\n'):
        heading_match = re.match(r'^(#{2,3})\s+(.+)', line)
        if heading_match:
            # Save previous section
            if current_text:
                sections[current_section] = count_words('\n'.join(current_text))
            current_section = heading_match.group(2).strip()
            current_text = []
        else:
            current_text.append(line)

    # Save last section
    if current_text:
        sections[current_section] = count_words('\n'.join(current_text))

    return {
        'abstract_words': abstract_words,
        'main_text_words': main_text_words,
        'caption_words': caption_words,
        'methods_words': methods_words,
        'main_text_with_captions': main_text_words + caption_words,
        'sections': sections,
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <manuscript.md> [<more.md> ...]", file=sys.stderr)
        sys.exit(1)

    paths = sys.argv[1:]
    if len(paths) == 1:
        result = parse_manuscript(paths[0])
    else:
        # Split-manuscript mode: per-file prose counts + combined total, plus the
        # section-aware parse of the first file for convenience.
        per_file = {}
        total = 0
        for p in paths:
            w = prose_words(Path(p).read_text(encoding='utf-8'))
            per_file[Path(p).name] = w
            total += w
        result = {
            'files': per_file,
            'total_prose_words': total,
            'first_file_parse': parse_manuscript(paths[0]),
        }

    print(json.dumps(result, indent=2))
