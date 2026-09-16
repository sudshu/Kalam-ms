---
name: km-response-to-reviewers
description: "Use when the user needs to parse reviewer comments and draft structured point-by-point responses for a manuscript revision. Classifies each point as Major/Minor/Editorial, maps points to manuscript sections, drafts polite and specific responses with proposed manuscript changes, and generates a tracking checklist. Invoke with /km-response-to-reviewers. Use this whenever the user says 'respond to reviewers', 'reviewer comments', 'point-by-point response', 'revision response', 'address reviewer feedback', 'R1 comments', 'handle reviews', or 'draft rebuttal'."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Response to Reviewers

Parse reviewer comments, classify each point, draft structured point-by-point responses, and track manuscript changes needed for the revision.

## When to Use

- When the user receives reviewer comments and needs to prepare a response
- When revising a manuscript based on peer review
- When the user wants help organizing and prioritizing reviewer feedback
- When drafting a rebuttal letter

## Prerequisites

- Reviewer comments (pasted by user or provided as a file)
- Current manuscript, resolved from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`/`.tex`)
- `metadata.yaml` for context (journal, title)

---

## Step 1: Ingest Reviewer Comments

1. Ask the user to provide reviewer comments in one of these ways:
   - Paste them directly into the conversation
   - Provide a file path to a document containing the comments
   - Provide a file path to the decision letter from the editor
2. Read the comments in full.
3. Separate the editor's comments (if present) from individual reviewer comments.
4. Identify how many reviewers there are (Reviewer 1, Reviewer 2, etc.).
5. Report: "Received comments from the editor and N reviewers. Parsing into individual points."

## Step 2: Parse into Individual Points

For each reviewer, break their comments into discrete, addressable points:

1. **Numbering convention:** R1.1, R1.2, R1.3, ... for Reviewer 1; R2.1, R2.2, ... for Reviewer 2; E.1, E.2, ... for Editor points.
2. A "point" is a single concern, question, suggestion, or criticism that requires a distinct response.
3. Multi-part comments should be split into separate points if they address different issues.
4. Preserve the exact reviewer wording for each point (this will be quoted in the response document).
5. If a reviewer makes a general positive comment ("The paper is well-written"), include it as a point with classification "Acknowledgment."

Present the parsed points to the user: "Parsed N points from Reviewer 1, M points from Reviewer 2, ..." and ask for confirmation before proceeding.

## Step 3: Classify Each Point

For each parsed point, assign a classification:

### Major
- Requires new analysis, additional data, or new figures
- Requires significant rewriting of a section
- Challenges a core claim or methodology
- Requests additional experiments or validation
- Could block acceptance if not addressed satisfactorily

### Minor
- Requests clarification or additional explanation
- Suggests rewording for clarity
- Asks for additional references
- Requests moving content between sections
- Points out an inconsistency that can be resolved with text changes

### Editorial
- Typo, grammar, or spelling correction
- Formatting issue
- Style suggestion (e.g., "change 'which' to 'that'")
- Figure label or caption minor fix

### Acknowledgment
- Positive comment or compliment (no action needed beyond thanks)

Present the classification summary:
```
| Classification | Count |
|---------------|-------|
| Major         | 3     |
| Minor         | 8     |
| Editorial     | 4     |
| Acknowledgment| 2     |
```

## Step 4: Map Points to Manuscript Sections

For each point:
1. Identify which section(s) of the manuscript are affected (Abstract, Introduction, Methods, Results, Discussion, Figures, SI).
2. If the point references a specific line, paragraph, or figure, note the exact location.
3. If the point is about the paper as a whole (e.g., "the novelty is unclear"), map it to the section(s) most relevant for addressing it.

## Step 5: Draft Responses

For each point, draft a response following these principles:

### Response Style
- **Polite and professional:** Thank the reviewer for their insight, even when disagreeing.
- **Specific:** Address the exact concern raised, do not give generic responses.
- **Evidence-based:** When possible, point to data, analysis, or literature that supports your position.
- **Concise:** Be thorough but do not over-explain.

### Response Structure for Each Point

```markdown
### R1.1 [Brief summary of the reviewer's concern]

**Classification:** Major / Minor / Editorial

**Reviewer comment:**
> [Exact quoted text from the reviewer]

**Response:**
[Our response addressing the concern. Thank the reviewer, explain our approach, reference any new or existing evidence.]

**Manuscript change:**
[One of the following:]
- "We have revised [section] to [description]. The revised text reads: '[new text]'"
- "We have added [new content] to [section]."
- "We have added new [Figure X / analysis] to address this point."
- "No change made. [Explanation of why the current text is adequate.]"
```

### Handling Major Points
- **Flag for user attention** before drafting a full response. Present the point and ask: "This is a major point that may require new analysis or significant revision. How would you like to address it?"
- If the user provides direction, draft the response accordingly.
- If the point requires new analysis that has not been done, note this as a TODO rather than drafting a speculative response.

### Handling Disagreements
- If the reviewer's point is based on a misunderstanding, clarify politely: "We appreciate this point and recognize that our original text may not have been sufficiently clear. We have revised the text to clarify that..."
- If the reviewer is factually incorrect, provide evidence gently: "We respectfully note that [evidence]. We have added a sentence to the manuscript to clarify this point."
- Never dismiss a reviewer's concern outright. Always acknowledge the underlying issue.

### Common Response Patterns
- **"Add a reference":** "We thank the reviewer for this suggestion. We have added [Reference] to the discussion of [topic] in [section]."
- **"Clarify methodology":** "We have expanded the description of [method] in the Methods section to address this concern."
- **"Why not use method X?":** "We considered [method X] but chose [our method] because [specific reason]. We have added a brief note in the Methods section explaining this choice."
- **"Strengthen the claim":** "We have revised the language to more precisely state [revised claim]. The updated text reads: '[new text]'"

## Step 6: Generate the Response Document

Write the complete response document to `drafts/response_to_reviewers.md` using this structure:

```markdown
# Response to Reviewers

**Manuscript:** <title>
**Journal:** <journal>
**Date:** <today's date>

We thank the editor and reviewers for their constructive feedback. We have carefully addressed each point below. Reviewer comments are quoted in block quotes, followed by our response and a description of any manuscript changes. All changes in the revised manuscript are highlighted in blue.

---

## Response to Editor

### E.1 [Summary]
**Reviewer comment:**
> [quoted]

**Response:**
[response]

**Manuscript change:**
[change description]

---

## Response to Reviewer 1

### R1.1 [Summary]
**Classification:** Major
**Reviewer comment:**
> [quoted]

**Response:**
[response]

**Manuscript change:**
[change description]

### R1.2 [Summary]
**Classification:** Minor
...

---

## Response to Reviewer 2

### R2.1 [Summary]
...
```

## Step 7: Generate Tracking Checklist

After all responses are drafted, generate a checklist appended to the response document or saved separately:

```markdown
---

## Revision Checklist

| Point | Classification | Section | Status | Notes |
|-------|---------------|---------|--------|-------|
| E.1   | Minor         | Title   | [ ]    |       |
| R1.1  | Major         | Results | [ ]    | Needs new analysis |
| R1.2  | Minor         | Methods | [ ]    |       |
| R1.3  | Editorial     | Intro   | [ ]    |       |
| R2.1  | Major         | Discussion | [ ] | User to provide direction |
| R2.2  | Minor         | Figures | [ ]    |       |
```

This checklist allows the user to track which points have been addressed in the actual manuscript revision.

## Step 8: Verification

After all responses are drafted:

1. **Completeness check:** Verify every parsed point has a response. Report: "All N points have responses" or "Missing responses for: [list]."
2. **Major point check:** Verify every Major point has either a manuscript change or an explicit TODO. Flag any Major points with "No change made" that do not have strong justification.
3. **Consistency check:** Verify that proposed manuscript changes do not contradict each other (e.g., one response says "we removed this sentence" and another says "we revised this sentence").
4. **Cross-reference to manuscript:** For responses that quote revised text, verify the section exists in the manuscript.

Report the verification results to the user.

## Notes

- The response document is a draft for the user to review and refine. It should never be submitted without the user's review.
- For Major points requiring new analysis, clearly mark these as TODOs rather than inventing results.
- Maintain a respectful tone throughout, even for contentious points.
- If multiple reviewers raise the same concern, note this in the response: "This point was also raised by Reviewer N (see RN.M). We address both points here."
- The tracking checklist should be updated as the user works through the revision. Offer to update it as changes are made.
- Replace vague scope claims with a specific account of what was done; retain a broad adjective only when the response demonstrates that scope.
