# Figure conventions

Canonical figure-handling rules for Kalam manuscripts. `AGENTS.md` points here.

These rules were extracted verbatim from the `## Figure Handling` section of
`AGENTS.md` on 2026-09-09 so that figure rules live in `resources/conventions/`
alongside the other five rule families. No rule was added, removed or reworded
in the move.

## Placement and registration

- Place figures in `figures/main/` and `figures/si/`
- Register every figure in `figures/figure_index.md`
- Read image files visually to understand content before writing captions
- Each figure needs: a title in the manuscript's selected descriptive or
  assertion-led style, panel descriptions, key message, caption draft, and link
  to the outline section

## Format

- **Save figures as vector PDF only — do not also emit PNG.** Manuscripts embed
  `.pdf`, which is typically ~7–8× smaller than a 300-dpi PNG of the same figure.
  In matplotlib scripts, write a single `.pdf` and drop any
  `for ext in ("png", "pdf")` loop. To inspect a figure, rasterize the PDF to a
  temporary PNG outside the manuscript tree.

## Global maps

- **Global-map default:** Use a Robinson projection for global manuscript maps
  unless the scientific purpose requires another projection. Regional maps should
  use a projection appropriate to their domain.
- **Global-map colour bars:** Place each colour bar immediately beside the map's
  actual projected boundary, not the nominal subplot rectangle. In
  Matplotlib/Cartopy, obtain `map_pos = ax.get_position()` after projection/aspect
  handling and use a vertical colour-bar gap of approximately `0.0025–0.004` in
  figure coordinates. Keep ticks and unit labels close to the bar and clear of
  enclosing panel borders. The reference implementation is
  `ml_wind_pblh/paper/figures/natcomms/fig1_concept_biorender_layout.py` in the
  COMPASS `analysis_dir`.

## Caption stance — owned elsewhere

Caption and title stance (descriptive versus assertion-led) is a
**per-manuscript decision** recorded with the journal and coauthor decision. It is
governed by `resources/conventions/writing_style.md` ("Titles and figure
captions"), which also requires a caption to identify what is shown, the data or
model, the metric where needed, **the result relevant to the figure**, and any
caveat needed to interpret the display.

Do not introduce a universal rule that captions must, or must not, state a result.
