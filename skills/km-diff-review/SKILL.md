---
name: km-diff-review
description: "Use when the user wants to see what changed in the manuscript since the last commit or a specific commit. Summarizes additions, deletions, rewordings, citation changes, figure changes, and word count deltas in a human-readable format suitable for co-author communication. Invoke with /km-diff-review. Optional arguments: a commit hash to diff against, or --since <date> to diff from a date. Use this whenever the user says 'what changed', 'show changes', 'revision summary', 'diff the manuscript', 'what did I change', or 'summarize edits'."
---

# Manuscript Diff Review

Show what changed in the manuscript since the last commit (or a specified commit) and generate a human-readable revision summary for co-author communication.

## When to Use

- Before sending an updated draft to co-authors
- To review your own changes before committing
- When a co-author asks "what changed since the last version I saw?"
- After a major editing session, to produce revision notes

## Arguments

- **No arguments**: diff against the last commit (`HEAD~1`)
- **Commit hash**: diff against a specific commit (e.g., `/km-diff-review abc1234`)
- **`--since <date>`**: diff against the most recent commit on or before the given date (e.g., `/km-diff-review --since 2026-03-15`)

---

## Step 1: Detect Manuscript Directory

1. Check the current working directory for a `metadata.yaml` file. If found, this is the manuscript root.
2. If not found, look for `manuscripts/` subdirectories and ask the user which manuscript to review.
3. Read `metadata.yaml` to get the manuscript title and target journal for context in the summary header.

## Step 2: Determine the Base Commit

1. **No arguments provided**: use `HEAD~1` as the base commit.
2. **Commit hash provided**: validate it exists with `git rev-parse --verify <hash>`. If invalid, report the error and ask the user for a valid hash.
3. **`--since <date>` provided**: find the most recent commit on or before that date using:
   ```bash
   git log --before="<date>" --format="%H" -1
   ```
   If no commit is found before that date, report the error.
4. Store the base commit hash and its date for the summary header.

## Step 3: Run Git Diff

Run `git diff` on the manuscript files between the base commit and the current working tree:

```bash
git diff <base_commit> -- drafts/*.md figures/figure_index.md
```

Also check for any new untracked files in `drafts/` and `figures/` using `git status`.

If the diff is empty (no changes), report "No manuscript changes found since <base>" and stop.

## Step 4: Parse the Diff

Analyze the diff output and categorize changes:

### 4a: Section-Level Changes

- Identify which manuscript sections were modified by looking for Markdown heading patterns (`## Section Name`) in the diff context.
- For each modified section, provide a brief (1-2 sentence) description of what changed: additions, deletions, rewordings.
- Note any sections that were added or removed entirely.

### 4b: Citation Changes

- Extract all citation keys (`@AuthorYear`) from added lines (lines starting with `+`).
- Extract all citation keys from removed lines (lines starting with `-`).
- Compute: new citations added, citations removed, citations that appear in both (unchanged).
- List new and removed citations by key.

### 4c: Figure Changes

- Check for changes to figure references in the text (`Fig.`, `Figure`, `Supplementary Fig.`).
- Check for changes to `figures/figure_index.md` if it exists.
- Report: figures added, figures removed, figures reordered, caption changes.

### 4d: Word Count Change

- Count words in the manuscript files at the base commit (resolve paths from `metadata.yaml` → `current_draft`, see `resources/conventions/manuscript_files.md`; example uses the single-file fallback):
  ```bash
  git show <base_commit>:drafts/manuscript.md | wc -w
  ```
- Count words in the current manuscript files:
  ```bash
  wc -w drafts/manuscript.md
  ```
- Report: word count before, word count after, net change (e.g., "+142 words" or "-89 words").
- If a cover letter exists, report its word count change separately.

## Step 5: Generate Revision Summary

Assemble a human-readable revision summary with this structure:

```markdown
# Revision Summary

**Manuscript:** <title from metadata.yaml>
**Comparing:** <base commit hash (short)> (<date>) → current working copy
**Date generated:** <today's date>

## Sections Modified

- **Introduction**: Expanded discussion of background context; added reference to Smith et al. (2024).
- **Results**: Rewrote paragraph on sensitivity analysis; updated quantitative results.
- ...

## Citations

- **Added:** @Smith2024, @Jones2025
- **Removed:** @OldRef2020

## Figures

- **Figure 2**: Caption updated to reflect revised analysis period.
- **Supplementary Figure S3**: Added.

## Word Count

| File | Before | After | Change |
|------|--------|-------|--------|
| manuscript.md | 4,523 | 4,665 | +142 |
| cover_letter.md | 387 | 412 | +25 |
```

Present this summary to the user in the conversation.

## Step 6: Optionally Write to File

Ask the user: "Would you like me to save this revision summary to `output/revision_notes_<YYYY-MM-DD>.md`?"

If yes:
1. Create the `output/` directory if it does not exist.
2. Write the summary to `output/revision_notes_<date>.md`.
3. Confirm the file path.

## Notes

- If the manuscript uses `.tex` instead of `.md`, adjust the file patterns accordingly.
- For very large diffs, focus the section summaries on substantive changes (not whitespace or formatting).
- Do not include the raw diff in the summary -- the point is a human-readable description, not a code review.
