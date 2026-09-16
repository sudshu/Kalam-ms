---
name: km-ideation
description: "Use when starting Stage 1 (Ideation) for a manuscript. Works with the user to identify key figures, core messages, main claims, and narrative arc. Reads figure images, discusses significance, and produces an ideation document plus discussion slides. Invoke with /km-ideation."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Stage 1: Ideation

Build the paper's core story through its figures.

## Prerequisites

- Manuscript folder exists in `manuscripts/<name>/`
- Read `metadata.yaml` — verify `stage` is `setup` or `ideation`
- Update stage to `ideation`
- Read `../../resources/User/USER.md` for user context
- Read the target journal profile from `../../resources/journal_profiles/`

## Process

### Phase 0: Reader and voice contract

Before proposing a story:

1. Confirm the target journal and article type.
2. Record the primary reader, adjacent-field reader, and what each can be assumed to know.
3. Inspect three to five recent target-journal papers and create or refresh `research/style_refs/style_profile.md`. Record the exemplars, reader level, paragraph-role patterns, field terminology, sentence/rhythm observations, caption stance, and how essential versus supporting evidence is distributed. Treat these as observations, not mechanical quotas.
4. When approved prose is available, record equal voice anchors from the lead author and principal coauthor. Do not block work if it is unavailable.
5. Ask the user to choose descriptive or assertion-led titles/captions for this manuscript.
6. Record that the main-text evidence budget will be decided for this manuscript rather than inherited from a global quota.

Pause for user confirmation of this contract before finalizing the narrative arc.

### Phase 1: Figure Discovery

1. List all files in `figures/main/` and `figures/si/`
2. For each figure, **read the image file visually**
3. Describe what you see — axes, data, patterns, panels
4. Ask the user to confirm or correct each interpretation
5. If no figures exist yet, ask the user what figures they plan to create. If `analysis_dir` is set, suggest running `/km-analysis` to generate figures.

### Phase 2: Core Story Extraction (Interactive Q&A)

Ask the user these questions (2–3 at a time):

1. What is the central or unifying finding?
2. What question was unanswered before this work?
3. Why should someone outside your subfield care?
4. What is the "one sentence takeaway" you want people to cite?
5. Who is the primary reader, and which adjacent community should also understand it?
6. What are the 3–5 key messages, one per figure?

### Phase 3: Narrative Arc Design

1. Map figures to a story sequence
2. Propose 2–3 framing angles:
   - **Discovery-first**: Lead with the main finding, then explain methods
   - **Methods-first**: Present the new approach, then show what it reveals
   - **Implications-first**: Start with the broader problem, narrow to your contribution
3. Recommend one angle based on the target journal audience
4. For broad Nature- or Science-level readership, make the context → question → test → finding → consequence chain explicit
5. Get user's choice

### Phase 4: Write Ideation Document

Write `drafts/ideation.md` with this structure:

```markdown
# [Title] — Ideation Document

Created: [DATE]
Target Journal: [JOURNAL]

## Reader and Voice Contract
- Article type: [TYPE]
- Primary reader: [READER]
- Adjacent-field reader: [READER]
- Assumed knowledge: [WHAT CAN / CANNOT BE ASSUMED]
- Voice anchors: [LEAD AUTHOR + PRINCIPAL COAUTHOR, OR NOT AVAILABLE]
- Title/caption stance: [DESCRIPTIVE | ASSERTION-LED]
- Evidence placement: [MANUSCRIPT-SPECIFIC PRINCIPLE]

## Core Claim
[The one-sentence takeaway]

## Key Figures and Messages

### Figure 1: [Title]
- **What it shows**: [description]
- **Key message**: [one sentence]
- **Status**: [exists | planned | needs revision]

[Repeat for each figure]

## Narrative Arc
[Selected framing angle and how the scientific logic flows figure-to-figure]

## Target Audience and Significance
- Primary audience: [community]
- Broader relevance: [why others should care]
- What was unknown: [the gap this fills]

## Framing Angle
[The chosen approach and why]

## Open Questions for Co-authors
1. [Question]
```

### Phase 5: Generate Discussion Slides

Run `/km-slides` (read `../../skills/km-slides/SKILL.md`) to create a 5–8 slide deck:
- Title + authors + "Discussion Draft"
- Research question and motivation
- One key figure per slide with message bullets
- Proposed narrative arc
- Open questions for co-authors

Save to `slides/ideation_slides/`

### Phase 6: Confirm and Transition

1. Present the ideation document to the user
2. Ask: "Share this with co-authors and come back when ready for Stage 2 (Skeleton)"
3. When user confirms, update `metadata.yaml` stage to `ideation_complete`

## Citation Strategy Reminders

Read `../../resources/conventions/citation_optimizer.md` and apply:
- Title with discoverable field terms, in the selected descriptive or assertion-led stance
- Core claim should be "quotable" — crisp, self-contained, quantitative
- Identify the hero figure for maximum reuse
