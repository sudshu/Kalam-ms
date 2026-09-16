---
name: km-analysis
description: "Use when the user wants to run data analysis, process data, or generate figures from an external analysis folder linked to a manuscript. Can explore code, run Python scripts, modify plots, and copy figures to the manuscript. Invoke with /km-analysis."
---

# Analysis Folder Integration

Run code in an external analysis folder to process data and generate publication-quality figures.

## Setup

1. Read `metadata.yaml` to get `analysis_dir`
2. If `analysis_dir` is empty, ask the user for the full path to their analysis folder
3. Update `metadata.yaml` with the path

The analysis folder can be anywhere on the filesystem — it does not need to be inside the Kalam project.

## Capabilities

### Explore
- List directory structure of the analysis folder
- Read Python scripts, Jupyter notebooks, config files, README files
- Identify data files, intermediate outputs, and figure outputs

### Understand
- Read existing code to understand:
  - Data loading and preprocessing pipelines
  - Variable names and data structures
  - Plotting functions and figure generation code
  - Dependencies and environment requirements

### Run Code
- Execute Python scripts: `python3 <script.py>`
- Run specific functions or cells from notebooks
- Process data to generate intermediate or final outputs

**Safety rule**: Always show the user the command that will be executed and get confirmation before running. Never run code silently.

### Modify Code
- Adjust plot aesthetics for publication quality:
  - Colors, colormaps, line styles
  - Font sizes, axis labels, tick marks
  - Figure dimensions and DPI
  - Legend placement and formatting
  - Panel layout and spacing
- Add or modify error bars, annotations, scale bars
- Adjust data filtering or processing parameters

### Generate and Copy Figures
1. Run plotting scripts in the analysis folder
2. Identify output figure files (PNG, PDF, SVG)
3. Copy figures to the manuscript folder:
   ```bash
   cp <analysis_dir>/output/fig1.png figures/main/
   ```
4. Ask before overwriting existing figures
5. Update `figures/figure_index.md`

### Create New Scripts
- Write new analysis or plotting scripts in the analysis folder when needed
- Follow existing code conventions (imports, naming, style)

## Workflow

1. **Explore**: List and read the analysis folder contents
2. **Report**: Tell the user what you found (scripts, data, existing figures)
3. **Plan**: Discuss with user what needs to be run or modified
4. **Execute**: Run code with user confirmation
5. **Copy**: Move generated figures to manuscript folder
6. **Index**: Update `figures/figure_index.md`
7. **Suggest**: Recommend running `/km-figures` to read and caption the new figures
