---
name: km-orient
description: "Use at the start of a session or when the user opens with 'hello', 'continue', 'where are we', 'continue from where you left off', or asks for current status. Reads the active manuscript's metadata, logfile, notes, and latest PDF, then gives a short status summary and WAITS for instructions before doing heavy work. Invoke with /km-orient."
---

# Orient (session start)

The user opens almost every session with a bare "hello" / "continue" and expects you to self-orient and then
**wait**. This skill does exactly that — no heavy work until they say so.

## Steps
1. **Find the active manuscript.** Read `manuscripts/<active>/metadata.yaml` (current_version, stage, current_pdf).
   If several manuscripts exist and none is clearly active, pick the most recently modified and say which.
2. **Read recent state:**
   - `logfile.md` — newest entries are at the **bottom**; read the last ~30–50 lines.
   - `manuscripts/<active>/notes.md` — newest at the **top**; read the top.
   - The latest build under `manuscripts/<active>/output/*.pdf` (most recent mtime) — skim for the current state.
3. **Summarize in ≤6 bullets:** active manuscript + version + stage; last action taken; latest results/decisions;
   open TODOs / blockers; what (if anything) is running.
4. **STOP and wait.** Do not launch builds, reviews, training, or edits until the user instructs. End with a short
   "what would you like to do?".

## Rules
- Read-only. No edits, no builds, no external calls during orientation.
- Give absolute paths for the manuscript directory and the latest PDF.
- Keep it tight — this is a status read, not an analysis.
