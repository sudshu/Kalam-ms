---
name: km-cover-letter
description: "Use when the user wants to draft or revise a journal-specific cover letter for manuscript submission. Reads metadata, abstract, and journal profile to produce a properly structured cover letter matching the target journal's conventions (Nature family: ~400 words, AGU: ~250 words, Copernicus: brief). Includes cross-checking of numbers against the manuscript. Invoke with /km-cover-letter. Use this whenever the user says 'write cover letter', 'draft cover letter', 'cover letter for submission', 'update cover letter', or 'prepare submission letter'."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Draft Journal-Specific Cover Letter

Draft a cover letter tailored to the target journal's conventions, drawing from the manuscript abstract, core finding, and journal profile.

## When to Use

- When preparing a manuscript for submission
- When switching target journals (cover letter conventions differ)
- When revising a cover letter after manuscript changes
- As part of the submission preparation workflow

## Prerequisites

- `metadata.yaml` with title, authors, journal, and core_finding fields
- Manuscript (containing the abstract), resolved from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`). Falls back to `drafts/manuscript.md` (or `.tex`).
- Journal profile in `resources/journal_profiles/`

---

## Step 1: Read Metadata

1. Read `metadata.yaml` to extract:
   - `title`: manuscript title
   - `journal`: target journal name
   - `core_finding`: one-sentence summary of the main result
   - `authors`: author list (for the closing)
   - `corresponding_author`: name and affiliation (if present)
2. If `core_finding` is missing, flag this and ask the user to provide it before proceeding.

## Step 2: Read the Manuscript Abstract

1. Resolve the manuscript file(s) from `metadata.yaml` → `current_draft` (see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`/`.tex`) and read the main-text file.
2. Extract the abstract section.
3. Identify the key quantitative result(s) stated in the abstract -- these will anchor the cover letter's opening paragraph.
4. Note the main methodological approach for potential use in paragraph 2.

## Step 3: Read the Journal Profile

1. Read the target journal's profile from `resources/journal_profiles/`.
2. Extract:
   - Journal scope and aims
   - Target readership
   - Any specific cover letter instructions or requirements
   - Editor name(s) if available

## Step 4: Determine Cover Letter Conventions

Apply journal-family-specific conventions. The lengths below are **indicative skill defaults** — cover-letter length is not a journal-published limit, so it is owned here rather than in a profile. Any *manuscript* limits you cite (word count, display items, references) must instead come from the journal profile / `resources/conventions/journal_families.md`, never hardcoded.

### Nature Family (Nature, Nature Geoscience, Nature Climate Change, Nature Communications)
- **Length:** 3-4 substantive paragraphs, approximately 400 words
- **Tone:** Formal but engaging; convey significance without overselling
- **Address to:** "Dear Editor" (or specific editor name if known)
- **Key requirement:** Explain why the work is timely and broadly significant

### AGU Family (AGU Advances, GRL, JGR, Global Biogeochemical Cycles)
- **Length:** 2-3 paragraphs, approximately 250 words
- **Tone:** Direct and concise
- **Address to:** "Dear Editor"
- **Key requirement:** Highlight novelty and relevance to AGU readership

### Copernicus (ACP, BG, GMD)
- **Length:** 2 paragraphs, brief
- **Tone:** Straightforward
- **Address to:** "Dear Editor"
- **Key requirement:** State the contribution clearly; Copernicus values brevity

### PNAS
- **Length:** 3 paragraphs, approximately 300 words
- **Tone:** Emphasize broad significance
- **Address to:** "Dear Editor" (or suggest an editor from the Editorial Board)
- **Key requirement:** Explain cross-disciplinary relevance

### Other / Unknown
- Default to 3 paragraphs, ~300 words, formal tone. Ask the user if they have specific journal requirements.

## Step 5: Draft the Cover Letter

Use the following 4-paragraph structure (condense to fewer paragraphs for shorter conventions):

### Paragraph 1: What the Paper Shows
- Open with a sentence that states the core finding directly.
- Draw from the abstract's "Here we show..." sentence.
- Include the key quantitative result (e.g., "We find that X increased by Y% over the period Z").
- Keep this concrete and specific -- avoid vague framing.

### Paragraph 2: What Is New
- Explain the advance beyond prior work.
- Cite 1-2 predecessor papers briefly (by author name and year, no formal citation keys).
- Articulate what gap this work fills or what assumption it overturns.
- If the method is novel, mention it here.

### Paragraph 3: Why This Journal
- Match the manuscript's contribution to the journal's stated scope (from the profile).
- Explain why the journal's readership would benefit from this work.
- Do not use generic flattery ("your prestigious journal"); be specific about topical fit.

### Paragraph 4: Timeliness and Broader Impact
- Connect to current scientific context, policy relevance, or emerging debates.
- If there is a timely hook (e.g., COP meeting, IPCC cycle, recent high-profile paper), mention it.
- Close with a brief statement of willingness to provide additional information.

For AGU/Copernicus (shorter formats), merge paragraphs 2 and 3, and condense paragraph 4 into a closing sentence.

## Step 6: Reviewer Suggestions

Ask the user:
1. "Do you have suggested reviewers? (Name, affiliation, email, brief reason)"
2. "Are there any reviewers you would like to exclude? (Name, brief reason)"

If the user provides suggestions, append a reviewer section to the cover letter:

```
## Suggested Reviewers
1. Dr. Jane Smith, MIT (expertise in X; published Y)
2. ...

## Reviewers to Exclude
1. Dr. John Doe (reason)
```

If the user declines, note that this section can be added later and proceed.

## Step 7: Cross-Check Numbers

Before finalizing:
1. Extract every number, percentage, and quantitative claim from the drafted cover letter.
2. Search the manuscript body for each number.
3. If any number in the cover letter does not appear in the manuscript (or does not match), flag it with a warning.
4. Report: "All N quantitative claims in the cover letter match the manuscript" or list discrepancies.

## Step 8: Write the Cover Letter

1. Check if `drafts/cover_letter.md` already exists.
2. **If it does not exist:** Write the new cover letter to `drafts/cover_letter.md`.
3. **If it already exists:** Proceed to Step 9 before overwriting.

## Step 9: Handle Existing Cover Letter

If `drafts/cover_letter.md` already exists:
1. Read the existing cover letter.
2. Show a side-by-side or inline comparison of proposed changes vs. the existing version.
3. Ask the user: "The cover letter already exists. Would you like me to (a) overwrite it with the new draft, (b) show you the differences so you can choose, or (c) save the new draft as `cover_letter_v2.md`?"
4. Proceed according to the user's choice.

## Notes

- Never fabricate journal metrics (acceptance rates, impact factors) in the cover letter. If the user asks to include such information, defer to them for the numbers.
- The cover letter should not simply restate the abstract. It should add context about novelty, fit, and timeliness that the abstract does not cover.
- Keep sentences direct. Avoid em-dash overuse and AI-sounding superlatives ("groundbreaking", "unprecedented").
