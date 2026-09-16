---
name: km-slides
description: "Use when the user needs discussion slides for co-author review. Generates a short presentation summarizing the current manuscript stage. Can produce PowerPoint (.pptx) via python-pptx or LaTeX Beamer. Invoke with /km-slides."
---

# Discussion Slides for Co-author Review

Generate a short slide deck summarizing the current manuscript stage.

## Setup

1. Read `metadata.yaml` to determine stage and manuscript details
2. Read `figures/figure_index.md` for available figures
3. Ask user: **PowerPoint** (default) or **LaTeX Beamer**?

## Stage 1 (Ideation) Deck — 5–8 slides

| Slide | Content |
|-------|---------|
| 1 | Title + authors + "Discussion Draft — Ideation" |
| 2 | Research question and motivation (1–2 bullet points) |
| 3–6 | One key figure per slide with key message bullets |
| 7 | Proposed narrative arc / story flow diagram |
| 8 | Open questions for co-authors (numbered list) |

## Stage 2 (Skeleton) Deck — 8–12 slides

| Slide | Content |
|-------|---------|
| 1 | Title + authors + "Skeleton Review" |
| 2 | Core claim + target journal |
| 3 | Paper structure overview (section list with 1-line summaries) |
| 4–9 | One figure per slide with draft caption and result bullets |
| 10 | Reference strategy (key must-cites, self-citations) |
| 11 | Open questions / feedback needed from co-authors |
| 12 | Timeline to submission |

## PowerPoint Generation (Default)

Generate a python-pptx script and execute it:

1. Create a Python script at `slides/<stage>_slides/build_slides.py`
2. Base it on the template at `../../skills/km-slides/scripts/build_slides_template.py`
3. Customize with manuscript-specific content:
   - Title, authors from `metadata.yaml`
   - Figures from `figures/main/`
   - Content from `drafts/ideation.md` or `drafts/skeleton.tex`
4. Execute: `python3 slides/<stage>_slides/build_slides.py`
5. Output: `slides/<stage>_slides/<stage>_deck.pptx`

## LaTeX Beamer Generation (Alternative)

Write a Beamer .tex file:

```latex
\documentclass{beamer}
\usetheme{Madrid}
\usecolortheme{default}

\title{[Paper Title]}
\subtitle{[Stage] Discussion Draft}
\author{[Authors]}
\date{\today}

\begin{document}
\maketitle

\begin{frame}{Research Question}
\begin{itemize}
\item [motivation]
\item [gap]
\end{itemize}
\end{frame}

\begin{frame}{[Figure Title]}
\begin{figure}
\includegraphics[width=0.85\textwidth]{../../figures/main/[filename]}
\end{figure}
\begin{itemize}
\item [key message]
\end{itemize}
\end{frame}

% ... more slides

\end{document}
```

Compile: `pdflatex slides/<stage>_slides/<stage>_deck.tex`

## Figure Handling

- Copy figures from `figures/main/` to the slides directory if needed for standalone packaging
- Scale figures to fit slides (width = 85–90% of slide width)
- Ensure figures are high enough resolution for presentation (300+ DPI)
