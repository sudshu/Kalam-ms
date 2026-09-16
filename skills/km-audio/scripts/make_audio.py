#!/usr/bin/env python3
"""km-audio — spoken MP3 rendition of a Kalam manuscript via edge-tts.

Resolves the main-text file from <manuscript>/metadata.yaml (current_draft,
first entry), cleans it into listenable prose, splits it into
  <name>_main_text        (title .. before '## Methods')
  <name>_methods_backmatter ('## Methods' .. before '## References')
and synthesizes each with edge-tts. Output always goes to a dedicated
subfolder inside the manuscript: <manuscript>/output/audio/ (created if
missing) — mp3, cleaned .txt transcript and .srt subtitles for each part.

Usage:
  python make_audio.py <manuscript_dir> [--file DRAFT.md] [--whole]
                       [--voice en-US-ChristopherNeural] [--rate +0%]
                       [--name STEM] [--outdir DIR]
"""
import argparse, json, pathlib, re, shutil, subprocess, sys

SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")


def clean_markdown(text: str) -> str:
    """Markdown/LaTeX-flavoured manuscript text -> listenable plain text."""
    t = text
    t = re.sub(r"\A---\n.*?\n---\n", "", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"^\s*(---+|\*\*\*+)\s*$", "", t, flags=re.M)
    t = re.sub(r"```.*?```", " Code block omitted. ", t, flags=re.S)
    t = re.sub(r"(?:^\|.*\|\s*$\n?)+", " Table omitted. ", t, flags=re.M)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
    t = re.sub(r"\\cite[tp]?\{[^}]*\}", "", t)
    t = re.sub(r"\[@[^\]]*\]", "", t)
    t = re.sub(r"\[VERIFY[^\]]*\]|\[CHECK[^\]]*\]|\[TBD[^\]]*\]|\[PENDING[^\]]*\]", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"^#{1,6}\s*(.+?)\s*$", lambda m: m.group(1).rstrip(".") + ".", t, flags=re.M)
    t = re.sub(r"\*\*([^*]+)\*\*|\*([^*]+)\*|__([^_]+)__", lambda m: next(g for g in m.groups() if g), t)
    t = re.sub(r"\^([^^\s]{1,12})\^", r"\1", t)
    t = re.sub(r"~([A-Za-z0-9]{1,12})~", r" \1", t)
    t = t.translate(SUB).translate(SUP)
    t = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", t)
    t = t.replace("{", "").replace("}", "").replace("\\", "")
    t = re.sub(r"(\d)\s*[–—-]\s*(\d)", r"\1 to \2", t)
    t = re.sub(r"\bFigs?\.\s*", "Figure ", t)
    t = re.sub(r"\(\s*[;,]?\s*\)", "", t)
    t = re.sub(r"\s+([,;.])", r"\1", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def _load_kalam_core():
    """Return the shared kalam_core.metadata module, or None if unavailable."""
    try:
        lib = pathlib.Path(__file__).resolve().parents[3] / "lib"
        if str(lib) not in sys.path:
            sys.path.insert(0, str(lib))
        from kalam_core import metadata as _md
        return _md
    except Exception:
        return None


def resolve_draft(mdir: pathlib.Path, override: str | None) -> pathlib.Path:
    """Resolve the main-text file, honouring an explicit --file override.

    Uses the canonical current_draft semantics (full manuscript-relative paths)
    shared via kalam_core.metadata.
    """
    if override:
        return (mdir / override) if not pathlib.Path(override).is_absolute() else pathlib.Path(override)
    _md = _load_kalam_core()
    if _md is not None:
        return _md.first_draft(mdir, default="drafts/manuscript.md")

    # Fallback: original inline implementation (kept identical).
    meta = (mdir / "metadata.yaml").read_text(encoding="utf-8")
    m = re.search(r'^current_draft:\s*"?([^"#\n]+)"?', meta, flags=re.M)
    first = m.group(1).split(",")[0].strip() if m else "drafts/manuscript.md"
    return mdir / first


def split_manuscript(raw: str) -> dict[str, str]:
    """title..Methods and Methods..References, on the RAW text (headings intact)."""
    parts = {}
    m = re.search(r"^## Methods\s*$", raw, flags=re.M)
    r = re.search(r"^## References\s*$", raw, flags=re.M)
    end = r.start() if r else len(raw)
    if m:
        parts["main_text"] = raw[:m.start()]
        parts["methods_backmatter"] = raw[m.start():end]
    else:
        parts["main_text"] = raw[:end]
    return parts


def synthesize(txt: pathlib.Path, mp3: pathlib.Path, srt: pathlib.Path | None, voice: str, rate: str) -> None:
    cmd = ["edge-tts", "--voice", voice, "--file", str(txt), "--write-media", str(mp3)]
    if srt is not None:
        cmd += ["--write-subtitles", str(srt)]
    if rate and rate != "+0%":
        cmd += ["--rate", rate]
    subprocess.run(cmd, check=True, capture_output=True, text=True)


def duration_s(mp3: pathlib.Path) -> float | None:
    if not shutil.which("ffprobe"):
        return None
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "json", str(mp3)],
            capture_output=True, text=True, check=True)
        return round(float(json.loads(out.stdout)["format"]["duration"]), 1)
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manuscript", help="manuscript directory (contains metadata.yaml)")
    ap.add_argument("--file", default=None, help="draft file override (relative to manuscript dir)")
    ap.add_argument("--whole", action="store_true", help="one MP3 for the whole text (no split)")
    ap.add_argument("--voice", default="en-US-ChristopherNeural")
    ap.add_argument("--rate", default="+0%")
    ap.add_argument("--name", default=None, help="output stem prefix (default: manuscript dir name)")
    ap.add_argument("--outdir", default=None, help="override the output/audio subfolder")
    ap.add_argument("--no-srt", action="store_true",
                    help="skip the .srt subtitle sidecar (and remove a stale matching one)")
    ap.add_argument("--only", choices=["main_text", "methods_backmatter"], default=None,
                    help="synthesize just one part of the split")
    a = ap.parse_args()

    mdir = pathlib.Path(a.manuscript).resolve()
    draft = resolve_draft(mdir, a.file)
    if not draft.exists():
        sys.exit(f"draft not found: {draft}")
    raw = draft.read_text(encoding="utf-8")

    outdir = pathlib.Path(a.outdir) if a.outdir else mdir / "output" / "audio"
    outdir.mkdir(parents=True, exist_ok=True)
    stem = a.name or mdir.name.replace("-", "_")

    parts = {"full": re.split(r"^## References\s*$", raw, flags=re.M)[0]} if a.whole else split_manuscript(raw)
    if a.only:
        parts = {k: v for k, v in parts.items() if k == a.only}
        if not parts:
            sys.exit(f"part '{a.only}' not found in the split (use without --whole)")

    results = []
    for label, chunk in parts.items():
        cleaned = clean_markdown(chunk)
        if not cleaned:
            continue
        txt = outdir / f"{stem}_{label}.txt"
        mp3 = outdir / f"{stem}_{label}.mp3"
        srt = outdir / f"{stem}_{label}.srt"
        if a.no_srt:
            srt.unlink(missing_ok=True)  # a stale sidecar would desync with the new mp3
        txt.write_text(cleaned, encoding="utf-8")
        synthesize(txt, mp3, None if a.no_srt else srt, a.voice, a.rate)
        if not mp3.exists() or mp3.stat().st_size == 0:
            sys.exit(f"edge-tts produced no audio for part '{label}'")
        results.append({"part": label, "mp3": str(mp3), "transcript": str(txt),
                        "srt": str(srt) if srt.exists() and srt.stat().st_size else None,
                        "words": len(cleaned.split()), "mp3_bytes": mp3.stat().st_size,
                        "duration_s": duration_s(mp3), "voice": a.voice, "rate": a.rate,
                        "source": str(draft)})
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
