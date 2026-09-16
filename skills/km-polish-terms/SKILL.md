---
name: km-polish-terms
description: "Use when the user wants to rename, harmonize, or update a key term consistently across manuscript text AND figure plotting scripts. Handles the full workflow: defines canonical forms (short for running text, long for figure legends), finds every variant across skeleton, figure index, captions, Methods, cover letter, style files, and plotting scripts, then applies edits with artifact detection. Also flags which figures need regeneration. Invoke with /km-polish-terms. Use this whenever the user says things like 'rename X to Y everywhere', 'change the label in figures and text', 'harmonize terminology', 'use consistent naming for X', or 'update the term for X'."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Term Harmonization Across Text and Figures

Scientific manuscripts often use the same concept under multiple names — in running text, figure legends, table headers, captions, plotting code, and Methods. This skill enforces a single canonical term everywhere, preventing reviewer confusion and ensuring text-figure consistency.

## When to Use

- The user wants to rename a term across the manuscript (e.g., "inversion median" → "GCB inversions")
- The user wants different forms for text vs. figures (e.g., short form in prose, longer form in figure legends for standalone clarity)
- The user notices inconsistent terminology and wants to fix it
- After a journal reframe where product names or abbreviations change

## Step 1: Define the Term Convention

Ask the user (or extract from context) three things:

1. **Old variants** — all forms currently in use (e.g., "inversion median", "in situ inversion median", "GCP 2025 inversion ensemble median", "GCP inversion median", "in situ inversions")
2. **New canonical forms**:
   - **Figure label** — used in figure legends, table headers, and captions (standalone contexts where the reader may not have seen the definition). Should be self-explanatory. Example: `"GCB inversion (in situ)"`
   - **First-mention text** — full definition with parenthetical shorthand. Example: `"GCB 2025 in situ inversion ensemble median (hereafter GCB inversions)"`
   - **Running text** — the short form used after the first mention. Example: `"GCB inversions"`
3. **Exceptions** — terms that look similar but should NOT be changed (e.g., "GCP 2025" when referring to the organization, not the product)

Present the convention back to the user as a table for confirmation before proceeding:

```
| Context                  | Form                                                        |
|--------------------------|-------------------------------------------------------------|
| Figure legends & tables  | GCB inversion (in situ)                                     |
| First mention in text    | GCB 2025 in situ inversion ensemble median (hereafter GCB inversions) |
| Running text             | GCB inversions                                              |
| Exceptions               | "GCP 2025" when referring to the organization               |
```

## Step 2: Inventory All Occurrences

Read `metadata.yaml` to get `analysis_dir` and the manuscript path. Then scan systematically:

### Text files (in manuscript directory)
Search these files for every old variant using Grep:
- `drafts/skeleton.md` (or `drafts/manuscript.tex`)
- `drafts/ideation.md`
- `figures/figure_index.md`
- `notes.md`
- `review_report.md`
- `metadata.yaml`

### Figure plotting scripts (in analysis_dir)
Search for old variants in:
- **Style/config files first** — look for a centralized style file (e.g., `figure_style.py`, `plot_config.py`) that defines `label=` strings. This is the highest-leverage edit.
- **Individual plot scripts** — search all `.py` files for the old variants in `label=`, `set_title()`, `set_xlabel()`, `set_ylabel()`, `ax.text()`, `ax.annotate()`, legend handle constructors, f-strings in stats text, and docstrings.
- **Figure captions in both skeleton AND figure_index** — these are the text that appears in the paper.

Build a table of every occurrence:

```
| File | Line | Current text | Target form | Notes |
|------|------|-------------|-------------|-------|
| figure_style.py | 40 | label="Inversion median" | "GCB inversion (in situ)" | Central style — propagates to Fig 2 legend |
| plot_figure2_ncc.py | 153 | "NOAA MBL vs inversion median" | "NOAA MBL vs GCB inversion (in situ)" | Panel a title |
| skeleton.md | 58 | "GCP 2025 in situ inversion ensemble" | first-mention form | "Here we show" paragraph |
| skeleton.md | 90 | "in situ inversion median" | "GCB inversions" | Running text |
```

Present this table to the user before making edits.

## Step 3: Apply Edits

Work through the inventory in this order:

### 3a. First-mention definition
Find the earliest occurrence in the manuscript text (usually in the abstract or "Here we show" paragraph). Replace with the full first-mention form.

### 3b. Running text
Replace all subsequent occurrences in prose with the short running-text form. Be careful:
- Use `replace_all` only when the old string is unambiguous
- For strings that appear in multiple contexts (e.g., "inversion median" in both prose and captions), edit each occurrence individually
- Check for exceptions defined in Step 1

### 3c. Figure captions (in skeleton and figure_index)
Replace with the **figure label** form. Captions should use the longer figure-label form since they may be read independently of the text.

### 3d. Tables and table headers
Replace with the **figure label** form (same rationale as captions).

### 3e. Style/config files
Edit the centralized label definition. This is the single most impactful edit — it propagates to every figure that imports the style.

### 3f. Individual plotting scripts
Search for hardcoded labels that override the style file. These are common in:
- Custom legend handles (e.g., `label="GCP 2025 inversion ensemble median"`)
- Title strings
- Stats annotation text boxes
- Print statements (lower priority, but good to keep consistent)

### 3g. Methods section
Methods often use more formal terminology. Use the running-text form but ensure the first mention within Methods also has a brief definition if the Methods can be read standalone (common for Online Methods in Nature journals).

## Step 4: Detect Artifacts

After bulk replacements, grep for double-replacement artifacts. These happen when the old term appears inside a longer phrase that also contains part of the new term. Common patterns:
- `"GCB 2025 in situ GCB inversion (in situ)"` — the replace hit both the container and the substring
- `"the the"` — from phrase boundary collisions

Search for these with:
```
Grep: pattern="GCB.*GCB|in situ.*in situ|the the"
```

Fix any artifacts found.

## Step 5: Flag Figure Regeneration

List the plotting scripts that were modified and tell the user which figures need to be regenerated:

```
## Figures to regenerate

| Script | Output figure | What changed |
|--------|--------------|--------------|
| figure_style.py | All figures using INVERSION label | Central label: "Inversion median" → "GCB inversion (in situ)" |
| plot_figure2_ncc.py | Figure 2 | Panel a title, panel b legend |
| plot_figure4_combined_growthrate_bim_2015_2024.py | Figure 4 | Panel a legend label |
| plot_budget_imbalance_noaa_vs_inversions_1990_2024.py | Figure S7 | Legend + stats text |
```

Ask the user: "Want me to run these scripts now to regenerate the figures?"

If yes, run each script using the Python environment specified in the script's docstring or shebang line. Copy outputs to the manuscript figures directory.

## Step 6: Final Verification

After all edits:
1. Grep all manuscript text files for any remaining old variants
2. Grep all plotting scripts for any remaining old variants
3. Report: "All N occurrences updated. No remaining instances of old variants found." or flag any stragglers.

## Edge Cases

- **Cover letter**: Uses more formal language. May need the full form rather than the short form, especially on first use.
- **BibTeX/references**: Term changes should NOT touch citation keys or BibTeX fields.
- **Code variable names**: Do NOT rename Python variables (e.g., `inv_agr`, `bim_inv`) — only string literals that appear in figure output.
- **Comments and docstrings in code**: Update these for consistency, but they're lower priority than visible labels.
- **SI vs main text**: Both should use the same convention.
