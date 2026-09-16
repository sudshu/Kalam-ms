---
name: km-audio
description: Spoken MP3 rendition of a Kalam manuscript via edge-tts — resolves the draft from metadata.yaml, cleans it into listenable prose, splits main text vs Methods+back matter, and writes MP3 + transcript + SRT subtitles to output/audio/. Use when the user asks for an audio version, a read-aloud, or an MP3 of the manuscript.
---

> **Manuscript writing rules note.** This skill never alters manuscript prose.
> The transcript is the manuscript text verbatim, cleaned only of markup
> (citations, markdown, URLs, editorial markers). Do not "improve" wording for
> the ear — scientific content, numbers and claim strength must pass through
> exactly.

# km-audio — manuscript → spoken MP3 (edge-tts)

Produces a listenable audio rendition of the current draft, for proof-listening
(hearing errors the eye skips) and for review on the move.

## Output rule (always)

**Audio never goes loose into the manuscript directory.** The engine always
creates (or reuses) the dedicated subfolder `<manuscript>/output/audio/` and
writes there: one `.mp3` per part plus its cleaned `.txt` transcript and an
`.srt` subtitle file (produced by default — timed from edge-tts word-boundary
events during synthesis, so subtitles cannot be added to an existing MP3
afterwards; `--no-srt` skips it for a run and removes a stale matching
sidecar). Output files are git-ignored build artifacts (regenerable), like
the PDFs in `output/`.

## Run

```bash
"${KALAM_PYTHON:-python3}" \
  skills/km-audio/scripts/make_audio.py manuscripts/<name> \
  [--file drafts/other.md] [--whole] [--only main_text|methods_backmatter] \
  [--voice en-US-ChristopherNeural] [--rate +0%] [--name STEM] [--no-srt]
```

(`$KALAM_PYTHON` is the project interpreter — see
`resources/conventions/tooling.md`. `edge-tts` must be importable by it; if the
chosen interpreter's `bin/` is not on `PATH`, prefix
`PATH="$(dirname "${KALAM_PYTHON:-$(command -v python3)}"):$PATH"`.)

Behaviour:

1. Resolves the **main-text file** from `metadata.yaml → current_draft`
   (first comma-separated entry; fallback `drafts/manuscript.md`).
   `--file` overrides (e.g. the SI or a cover letter).
2. **Splits** into `<stem>_main_text` (title → before `## Methods`) and
   `<stem>_methods_backmatter` (`## Methods` → before `## References`);
   `--whole` makes a single MP3 instead. References are never spoken.
3. **Cleaning** (identical core to the user-level `tts-mp3` skill):
   `\cite{}`/`[@…]`/`[VERIFY…]` and URLs stripped; headings become sentence
   breaks; tables → "Table omitted"; `0.43–0.45` → "0.43 to 0.45";
   `u₁₀`/`m s⁻¹`/`r~anom~` → `u10`/`m s-1`/`r anom`; `Fig.` → "Figure".
4. Writes `.mp3` + `.txt` + `.srt` per part and prints a JSON summary (words,
   MB, duration, voice, srt path) — `"srt": null` means subtitles were skipped
   (`--no-srt`) or failed (re-synthesize the part in that case).

## Defaults

- Voice `en-US-ChristopherNeural` (house default; American male with a
  reliable, authoritative delivery); rate `+0%` (`+10%` is comfortable for
  dense Methods).
- A full manuscript takes a few minutes to synthesize — run in the background
  (`run_in_background`) rather than blocking; expect roughly 1 MB and ~65–70 s
  of audio per 150 words.

## After the run

1. Check the JSON: duration ≈ words/150 min; nonzero bytes for every part.
2. Report the absolute path of each MP3 on its own line.
3. Append one dated line to the manuscript's `logfile.md` (word counts per
   part, voice, output paths). No `notes.md` entry needed — audio is a build
   artifact, not a decision.
4. Send via Telegram ONLY if explicitly asked (rule R5): file path first line,
   caption after.

## Delegation (do not duplicate)

| Concern | Owner |
|---|---|
| Which draft file is current | `metadata.yaml → current_draft` (`resources/conventions/manuscript_files.md`) |
| Prose quality of what is spoken | the writing/editing skills — never fix prose here |
| General non-manuscript files → MP3 | user-level `tts-mp3` skill |
| PDF/DOCX builds | `build.sh` / `/km-export-docx` |
