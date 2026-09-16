---
name: km-skeleton
description: "Use when starting Stage 2 (Skeleton) for a manuscript. Builds a paragraph-by-paragraph bullet outline with integrated references, organizes all figures with draft captions, and outputs a LaTeX skeleton. Invoke with /km-skeleton."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Stage 2: Skeleton

Build a paragraph-level outline with integrated references and organized figures.

## Prerequisites

- Read `drafts/ideation.md` — this is the confirmed Stage 1 output
- Read `metadata.yaml` — verify `stage` is `ideation_complete` or `skeleton`
- Update stage to `skeleton`
- Read `../../resources/User/USER.md` for user context and publication list
- Read the target journal profile from `../../resources/journal_profiles/`
- Read `research/style_refs/style_profile.md`; if it is missing, return to `/km-ideation` and establish the reader/voice contract before outlining
- Read `references.bib`
- Read `figures/figure_index.md`

## Process

### Phase 1: Section Outline (Interactive, Section by Section)

For each section required by the journal profile and the approved manuscript contract:

1. Propose paragraph-by-paragraph bullet points
2. Each paragraph bullet includes:
   - Paragraph role: context, gap, question, test, result, interpretation, limitation, or implication
   - Reader takeaway and opening-sentence idea
   - Key claims or points to make
   - Figure references (if applicable)
   - Citations from `references.bib` using `\cite{key}` format
   - Evidence item and proposed destination: Main, Methods, Extended Data, Supplementary Information, or Omit
3. Present to user for feedback
4. Revise based on feedback
5. Move to next section only after user confirms

**Section-specific guidance (adapt to the journal and paper):**

**Introduction or opening paragraphs:**
- Establish only the context needed by the recorded readers
- Define the unresolved question and why its answer matters
- State the approach and contribution without recounting the analysis chronology
- For broad Nature/Science readership, make the context → question → test → finding → consequence chain explicit

**Methods:**
- Overview of approach
- Data sources with versions and time periods
- Model/algorithm description
- Validation approach

**Results:**
- One paragraph per key finding, tied to a figure
- Lead normally with the comparison, measurement, or finding
- Quantitative statements with the uncertainty needed for interpretation

**Discussion:**
- Organize around interpretation, relationship to previous work, consequences, and material limitations
- State each limitation where it matters and normally once
- Do not build an imagined objection–rebuttal sequence

**Conclusions, when required by the journal:**
- Synthesize the central implications in the form and length specified by the journal profile

### Phase 2: Evidence-placement ledger

Create `drafts/evidence_placement.md` using the project template. For every result, control, sensitivity test, and limitation, record:

- the claim it supports;
- destination: Main, Methods, Extended Data, Supplementary Information, or Omit;
- whether it is load-bearing; and
- a one-line placement rationale.

Keep a test in the main text when it changes the sign, magnitude, mechanism, scope, or credibility of the central claim. Do not promote supporting checks merely because they exist, and do not hide a load-bearing check in the supplement.

Review the ledger with the user before writing prose.

### Phase 3: Reference Integration

1. Scan `references.bib` for essential citations
2. Read `../../resources/User/publications.md` for self-citation candidates, if the user has added one
3. Apply citation strategy from `../../resources/conventions/citation_optimizer.md`:
   - Strategic self-citations (3–7)
   - Bridge references to adjacent fields
   - Must-cite foundational papers
4. Identify gaps — papers that should be cited but are missing
5. If gaps found, suggest running `/km-research` to find them

### Phase 4: Figure Organization

1. Finalize Main, Methods, Extended Data, SI, or Omit assignment for each figure using the evidence ledger
2. Draft each figure caption using the protocol from `/km-figures`
3. Update `figures/figure_index.md` with all figures, captions, and section assignments
4. Check narrative flow: does Figure 1 → N tell the story from ideation?

### Phase 5: Write LaTeX Skeleton

Write `drafts/skeleton.tex` with:

1. **Preamble**: Journal-appropriate document class (see AGENTS.md export table)
2. **Section structure**: Standard sections with `\section{}` commands
3. **Paragraph comments**: `% PARAGRAPH [ROLE]: [reader takeaway / opening idea]` before each planned paragraph
4. **Bullet points**: Under each paragraph comment, key points, evidence destination, and citations as LaTeX comments
5. **Figure environments**: `\begin{figure}` with `\includegraphics` pointing to `../figures/main/`
6. **Draft captions**: `\caption{}` for each figure
7. **Citations**: `\cite{key}` integrated into bullet points
8. **Abstract skeleton**: Sentence-by-sentence plan as comments

Example structure:
```latex
\section{Results}

% PARAGRAPH: Main finding about methane emissions
% - Global methane emissions increased by X Tg/yr \cite{key1}
% - Our satellite-derived estimate shows Y ± Z
% - This is consistent with / differs from previous work \cite{key2}

\begin{figure}[ht]
\centering
\includegraphics[width=\textwidth]{../figures/main/fig1_map.png}
\caption{Global distribution of methane emissions...}
\label{fig:global_map}
\end{figure}
```

### Phase 6: Generate Discussion Slides

Run `/km-slides` (read `../../skills/km-slides/SKILL.md`) to create an 8–12 slide deck:
- Title + authors + "Skeleton Review"
- Core claim + target journal
- Paper structure overview
- One figure per slide with draft caption and result bullets
- Reference strategy (key must-cites)
- Open questions / feedback needed
- Timeline to submission

Save to `slides/skeleton_slides/`

### Phase 7: Confirm and Transition

1. Present the skeleton and evidence-placement ledger to the user
2. Ask: "Share with co-authors and come back when ready for Stage 3 (Full Manuscript)"
3. When confirmed, update `metadata.yaml` stage to `skeleton_complete`
