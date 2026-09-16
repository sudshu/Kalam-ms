---
name: km-figures
description: "Use when the user needs help with figure reading, interpretation, quality review, captioning, remaking, or organization for a manuscript. Reads figure image files visually, runs publication-quality checks against journal standards, drafts captions, links to remake scripts, and updates the figure index. Invoke with /km-figures."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Figure Reading, Quality Review, and Captioning

## Process

### Step 1: Locate Figures and Context

1. Read `metadata.yaml` to identify the active manuscript and `target_journal`
2. Read the journal profile from `resources/journal_profiles/` to get figure requirements
3. List files in `figures/main/` and `figures/si/`
4. Read `figures/figure_index.md` for current status and captions
5. Check for `figures/Figure_remake_instructions.md` — if it exists, read it to understand figure-making scripts and data pipelines

   > **Preferred: use the shared inventory helper** to pair figures with their captions and citations. Run `python skills/km-deep-read/scripts/inventory.py <manuscript_dir>`; its JSON `figures` field lists each figure's image path, caption preview, and detected panel letters, and `uncited_display_items` flags any figure never cited in the text.

### Step 2: Read and Classify Each Figure

For each image file (PNG, JPG, PDF):

1. **Read the image file visually** using the Read tool
2. **Classify the figure type** (see §Figure Type Guide below)
3. Describe what you observe:
   - Panel structure (single or multi-panel)
   - Axes labels and units
   - Data patterns, trends, outliers
   - Color scheme and legend
   - Spatial or temporal scope
   - Statistical information (R, RMSE, p-values, error bars, confidence intervals)
   - Font sizes (estimate vs. journal minimum)
   - Spine visibility, gridlines, whitespace
4. **Ask the user to confirm or correct** your interpretation

### Step 3: Publication-Quality Review

Run a structured quality check against the target journal's figure standards. Apply the general checklist first, then the figure-type-specific checks from §Figure Type Guide.

#### General Checklist (all figure types, all journals)

| Criterion | What to check |
|-----------|---------------|
| **Panel labels** | Present, consistent position across all panels, **clearly visible** — not obscured by tick labels, data, or dense annotations; correct style for journal. If hidden inside the axes, move outside (above-left using `ax.text(-0.10, 1.02, "a", transform=ax.transAxes, va="bottom", ha="left")`). Add a translucent white `bbox` if the label sits over a busy background. |
| **Axis labels** | All axes labeled with units; no missing labels |
| **Font floor** | Smallest text ≥ journal minimum (estimate from tick labels, annotations, legend) |
| **Font family** | Matches journal requirement (usually sans-serif) |
| **Spines** | Top/right removed unless journal requires them |
| **Legend** | Symbols match actual data representation; no orphan legend entries for absent data |
| **Color** | Colorblind-safe; sequential data uses sequential palette, categorical uses distinct hues |
| **DPI** | ≥ 300 for raster output |
| **Gridlines** | None or very faint (alpha ≤ 0.4) |
| **Data-ink ratio** | Minimal non-data elements; no heavy borders, drop shadows, 3D effects |
| **Whitespace** | No excessive margins; panel spacing balanced |

#### Output format — vector PDF only

Save manuscript figures as **vector PDF only; do not also emit PNG**. Manuscripts embed `.pdf`, and a vector PDF is typically ~7–8× smaller on disk than a 300-dpi PNG of the same figure. In matplotlib scripts, write a single `fig.savefig(path_with_suffix_pdf, bbox_inches="tight")` and drop any `for ext in ("png", "pdf")` loop. DPI still applies only to raster content embedded inside the PDF (`imshow`, dense scatter, maps). To inspect a figure visually, rasterize the PDF to a temporary PNG outside the manuscript tree rather than saving a PNG alongside it.

#### Journal-Specific Requirements

**Nature family (NCC, Nature Comms, Nature)**

| Criterion | Requirement |
|-----------|-------------|
| Width | Single column: 88 mm (3.46 in), double: 180 mm (7.09 in) |
| Font floor | ≥ 5 pt after scaling; 7 pt recommended |
| Font family | Sans-serif (Helvetica, Arial, DejaVu Sans) |
| Panel labels | Bold lowercase: **a**, **b**, **c** |
| DPI | 300 for halftone, 600 for line art |

**AGU family (GRL, JGR, AGU Advances)**

| Criterion | Requirement |
|-----------|-------------|
| Width | Single: 95 mm, full: 190 mm |
| Font floor | ≥ 6 pt |
| Panel labels | Parenthesized lowercase: (a), (b), (c) |

**Other journals** — Read the journal profile in `resources/journal_profiles/`. If none exists, default to Nature family as the most stringent.

#### Review Output Format

Present the review as:

```
## Publication-Quality Review — Figure N

**Target journal:** [journal name]
**Figure type:** [map / time series / scatter / bar / multi-panel / ...]
**Overall verdict:** Ready / Close but not ready / Needs significant work

| # | Issue | Severity | Fix |
|---|-------|----------|-----|
| 1 | [description] | Must fix | [specific action] |
| 2 | [description] | Should fix | [specific action] |
| 3 | [description] | Nice to have | [specific action] |
```

Severity levels:
- **Must fix** — will be flagged by journal production or reviewers
- **Should fix** — improves scientific clarity or readability
- **Nice to have** — polish for maximum visual impact

### Step 4: Identify Key Messages

For each figure, determine:
- What is the ONE main scientific point?
- How does this figure support the paper's core claim?
- Where is it assigned in `drafts/evidence_placement.md`: Main, Methods, Extended Data, Supplementary Information, or Omit?
- Is this a candidate "hero figure" for maximum reuse/citation?

### Step 5: Draft Captions

Write standalone captions following the target journal's convention and the descriptive or assertion-led stance recorded in `research/style_refs/style_profile.md`. Neither stance is a universal default.

#### Nature family format (NCC, Nature Comms, Nature)
```
**Fig. N | Title in the manuscript's selected stance and sentence case.**
**(a)** Panel A description. **(b)** Panel B description.
[Data source, time period, key methodological note.]
[One sentence highlighting the main finding.]
```

#### AGU family format (GRL, JGR)
```
**Figure N.** Title in the manuscript's selected stance. (a) Panel A description. (b) Panel B description.
Data source and methods note. Main finding sentence.
```

#### Caption requirements (all journals)
- Must be understandable without reading the main text
- All symbols, colors, line styles, and abbreviations defined
- Data source and time period stated
- Units explicit
- State the result needed to interpret the figure without forcing an assertion-led punchline when descriptive captions were selected
- **Maps:** projection type, reference lines, coordinate system
- **Scatter plots:** regression method, N, R or R², RMSE, p-value if relevant
- **Time series:** temporal resolution, smoothing/filtering if applied
- **Bar/box plots:** what bars/boxes represent, error bar definition (1σ, 95% CI, etc.)

### Step 6: Link to Remake Scripts

If `figures/Figure_remake_instructions.md` exists, check whether the figure's script and data pipeline are documented. If not, identify the generating script by:

1. Searching `analysis_dir` (from `metadata.yaml`) for scripts containing the figure filename
2. Reading the script to understand inputs, outputs, and key functions
3. Adding the script info to `Figure_remake_instructions.md`

When the user asks to **remake** or **fix** a figure:
1. Read the generating script
2. Identify the specific function/section to modify
3. Make targeted edits (not full rewrites)
4. Run the script to regenerate
5. Read the output image visually to verify the fix
6. Iterate until the user is satisfied

### Step 7: Update Figure Index

Update `figures/figure_index.md`:

1. **Summary table row** — update status, key message, section assignment
2. **Figure Captions section** — add or update the full caption text
3. **Update timestamp** at top of file

### Step 8: Narrative Flow Check

Read through all figures in sequence:
1. Does a coherent scientific story emerge?
2. Are there gaps in the narrative?
3. Should figures be reordered?
4. Are any figures redundant (move to SI)?
5. Are any critical figures missing?

Present the narrative flow as: `Introduction → Fig 1 (purpose) → Fig 2 (purpose) → ... → SI (purpose)`

---

## Figure Type Guide

Classify each figure and apply the type-specific checks in addition to the general checklist.

### Map Figures

**Subtypes:** global projection (Mollweide, Robinson), regional (PlateCarree), polar stereographic

**Type-specific checks:**
- Projection appropriate for spatial extent (global → Mollweide/Robinson, regional → PlateCarree, polar → stereographic)
- Coastlines present, appropriate weight (0.3–0.6 pt)
- Reference lines (equator, tropics, Arctic/Antarctic circles) if scientifically relevant
- Color fill: land/ocean distinguishable but not dominant — data markers must stand out over the background
- Site/point markers sized appropriately; clustered points should be spread or explained in caption
- Coordinate labels (lat/lon) present on axes or as reference line annotations

**Common fixes:**
| Problem | Solution |
|---------|----------|
| Map too small in multi-panel layout | Projection aspect ratios constrain height (Mollweide 2:1, Robinson ~1.97:1). Give map panels full figure width via vertical stacking: `GridSpec(N, 1)` |
| Text labels unreadable over map features | Add translucent text box: `bbox=dict(boxstyle="square,pad=0.15", facecolor="white", alpha=0.55, edgecolor="none")` |
| Reference line labels hard to see inside map boundary | Place labels outside the map at the right edge using `ax.transAxes` coordinates with `clip_on=False` |
| Background color competes with data markers | Lighten ocean/land fills; ensure ≥ 30% luminance contrast between background and marker fill |
| Clustered markers overlap | Reduce marker size for secondary category; offset duplicates; or note nominal positions in caption |

### Time Series Figures

**Subtypes:** single line, multi-line, stacked/offset, anomaly, coverage/presence timeline

**Type-specific checks:**
- X-axis covers the intended temporal range with sensible tick spacing
- Y-axis labeled with units; zero baseline shown if meaningful
- Multiple lines distinguishable by both color AND line style (for B&W printing)
- Shading/confidence envelopes have sufficient transparency (alpha 0.2–0.4)
- Key events or thresholds annotated if relevant
- If showing data presence/absence: use tick marks or discrete blocks at actual times, not continuous bars through gaps

**Common fixes:**
| Problem | Solution |
|---------|----------|
| Lines overlap and are indistinguishable | Add line style variation (`--`, `-.`, `:`) in addition to color; increase linewidth difference |
| Continuous bars misrepresent gaps in data | Replace `barh` with `ax.vlines()` at actual observation times — gaps appear naturally as white space |
| Too many y-tick labels in site/category timelines | Reduce font size or show every Nth label; group into bands with boundary lines |
| Confidence envelope obscures data | Reduce alpha (0.15–0.25); plot mean line on top with higher zorder |

### Scatter Plots

**Subtypes:** simple scatter, regression, observed-vs-predicted, colored by third variable

**Type-specific checks:**
- 1:1 reference line if comparing observed vs. predicted (dashed, neutral color)
- Regression statistics displayed in a text box (R or R², RMSE, N, p-value)
- Axis ranges equal if comparing like quantities (square aspect ratio)
- Point labels (e.g., year annotations) legible and not overlapping
- Point sizes appropriate — not so large they merge, not so small they vanish

**Common fixes:**
| Problem | Solution |
|---------|----------|
| Year/category annotations overlap | Use `adjustText` library, or manually offset with `xytext` |
| Statistics box misplaced | Anchor with `transform=ax.transAxes` in a corner with no data |
| Axis ranges unequal for obs-vs-pred | Set `ax.set_aspect('equal')` or manually equalize xlim/ylim |
| Color bar for third variable unreadable | Increase colorbar width; use perceptually uniform colormap (viridis, cividis) |

### Bar / Box / Violin Plots

**Type-specific checks:**
- Bar widths consistent; spacing between groups clear
- Error bars defined in caption (1σ, 2σ, 95% CI, IQR)
- Category labels readable (rotate if needed, 45° preferred over 90°)
- Baseline at zero unless there is a scientific reason otherwise
- Colors serve a purpose (grouping variable), not decoration

**Common fixes:**
| Problem | Solution |
|---------|----------|
| Category labels overlap | Rotate 45°: `ax.tick_params(axis='x', rotation=45, ha='right')` |
| Too many categories | Group into major categories with sub-bars; or switch to horizontal bars |
| Error bars invisible | Increase capsize (3–5 pt) and linewidth (1–1.5 pt) |

### Heatmap / Matrix Figures

**Type-specific checks:**
- Colormap appropriate: diverging for anomalies (centered on zero), sequential for magnitudes
- Colorbar present with label and units
- Cell labels (if shown) don't clash with background color
- Axis labels for rows and columns

### Schematic / Workflow Diagrams

**Type-specific checks:**
- Flow direction clear (arrows, numbering)
- Text legible at print size
- Consistent visual language (box shapes, colors, line styles)
- Not overly complex — if > 8 boxes, consider splitting

---

## Multi-Panel Layout Principles

| Layout | When to use | GridSpec pattern |
|--------|-------------|-----------------|
| Side-by-side (1×2) | Comparing two quantities with same y-axis | `GridSpec(1, 2, width_ratios=[1, 1])` |
| Stacked (2×1) | Panels share x-axis, or top panel has constrained aspect ratio (maps) | `GridSpec(2, 1, height_ratios=[...])` |
| Grid (2×2, 3×2, etc.) | Multi-variable comparison, predictor panels | `GridSpec(rows, cols)` |
| Mixed (map + plots) | Map panel needs full width; plots below can be side-by-side | Nested GridSpec or `GridSpecFromSubplotSpec` |

**Key rules:**
- Panel labels must be in the same relative position across ALL panels
- If a panel label is hidden by dense data (tick labels, annotations), move it outside the axes
- Shared axes: use `sharex=True` / `sharey=True` and remove redundant tick labels
- Constrained-aspect panels (maps, equal-axis scatter): adjust `height_ratios`/`width_ratios` so these panels get the space their aspect ratio demands

---

## Color Palette Recommendations

| Data type | Recommended | Avoid |
|-----------|-------------|-------|
| **Categorical** (2–3 groups) | Colorblind-safe pairs: blue `#2166ac` + orange `#e07a18`, or blue + red `#b2182b` | Red + green without shape/style distinction |
| **Categorical** (4+ groups) | Okabe-Ito palette, ColorBrewer Set2/Dark2 | Rainbow; too many similar hues |
| **Sequential** (magnitude) | viridis, cividis, YlOrRd, Blues | jet, rainbow |
| **Diverging** (anomaly) | RdBu, BrBG, PiYG (centered on white/neutral) | Non-symmetric colormaps for symmetric data |
| **Binary** (presence/absence) | Single hue vs. white background | Gradients for binary data |

Background colors should be light enough that all data colors maintain ≥ 30% luminance contrast.

---

## Annotation Best Practices

- **Statistics boxes:** Use `ax.text(..., transform=ax.transAxes, bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85, edgecolor="#cccccc"))` — anchor in axes coordinates so position is stable across data ranges
- **Year/point labels:** Offset from data points with `xytext=(4, 4), textcoords="offset points"` to avoid overlap with markers
- **Reference lines:** 1:1 lines, zero lines, threshold lines should be dashed, neutral color (`#333333`–`#888888`), behind data (lower zorder)
- **Band/region labels:** For right-margin labels on categorized y-axes, use `blended_transform_factory(ax.transAxes, ax.transData)` — x in axes fraction, y in data coordinates
- **Labels outside axes bounds:** Always set `clip_on=False`; use `ax.transAxes` with x > 1.0 or y > 1.0
