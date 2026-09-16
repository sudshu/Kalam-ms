---
name: km-abstract
description: "Use when the user wants to draft or revise a journal-specific abstract with structured quality checks. Reads the full manuscript and journal profile to produce an abstract that meets word limits, follows the 6-sentence structure (context, gap, 'Here we show', evidence, implication, hook), and passes quality checks (word count, number cross-referencing, acronym definitions, jargon flagging). Invoke with /km-abstract. Use this whenever the user says 'write abstract', 'draft abstract', 'revise abstract', 'abstract too long', 'check abstract', or 'abstract for submission'."
---

> **Manuscript writing policy (read first).** Follow the canonical policy in `resources/conventions/writing_style.md`; `skills/Manuscript_writing_instuctions.md` supplies the operational rules. Explicit user/coauthor instructions and recorded manuscript decisions take precedence.
>
> **Empirical estimates versus algebraic constraints.** Avoid categorical mathematical shorthand; separate empirical estimates from algebraic constraints and state the conditions explicitly. Say whether a number is estimated from data or implied by the definitions, and under what conditions it holds.

# Draft or Revise a Journal-Specific Abstract

Draft a structured, journal-compliant abstract with integrated quality checks, or revise an existing abstract to meet journal requirements.

## When to Use

- When drafting the abstract for a new manuscript
- When switching target journals (word limits and reference rules differ)
- When the manuscript has changed significantly and the abstract needs updating
- When the user wants a quality check on an existing abstract

## Prerequisites

- `metadata.yaml` with journal and core_finding fields
- Full manuscript text, resolved from `metadata.yaml` → `current_draft` (comma-separated paths; see `resources/conventions/manuscript_files.md`). Falls back to `drafts/manuscript.md` (or `.tex`).
- Journal profile in `resources/journal_profiles/`

---

## Step 1: Read Metadata

1. Read `metadata.yaml` to extract:
   - `journal`: target journal name
   - `core_finding`: one-sentence summary of the main result
2. If `core_finding` is missing, read the manuscript to infer it and confirm with the user.

## Step 2: Read Journal Profile for Abstract Rules

Read the target journal's profile from `resources/journal_profiles/` (the authoritative source; quick-reference limits in `resources/conventions/journal_families.md`) and extract the abstract-specific rules. The per-journal notes below are indicative — the profile wins:

### Nature / Nature Geoscience / Nature Climate Change
- **Word limit:** take from the journal profile in `resources/journal_profiles/` (authoritative) — e.g. Nature is ~150 words, not 200. Do not hardcode a number here; the profile is the single source of truth.
- **References:** Not allowed in abstract
- **Heading:** No "Abstract" heading (it is implicit)
- **Other:** Must be a single paragraph; no equations

### Nature Communications
- **Word limit:** 150 words maximum
- **References:** Not allowed in abstract
- **Heading:** No "Abstract" heading
- **Other:** Single paragraph; must be accessible to non-specialists

### AGU Advances / GRL
- **Word limit:** 250 words maximum
- **References:** Allowed
- **Heading:** "Abstract" heading present
- **Other:** May use key points (3 bullet points, 140 characters each) in addition

### ACP / Copernicus Journals
- **Word limit:** 350 words maximum
- **References:** Allowed
- **Heading:** "Abstract" heading present
- **Other:** Can be longer and more detailed

### PNAS
- **Word limit:** 250 words maximum
- **References:** Not allowed in abstract
- **Heading:** Present
- **Other:** Separate "Significance Statement" required (120 words max, no jargon)

### Other / Unknown
- Default to 250 words, no references. Ask the user for specific journal rules.

Record the word limit, reference policy, and any other constraints for use in quality checks.

## Step 3: Read the Full Manuscript

1. Read the manuscript file(s) resolved from `metadata.yaml` → `current_draft` (see `resources/conventions/manuscript_files.md`; fallback `drafts/manuscript.md`/`.tex`) in their entirety.
2. Identify:
   - The core quantitative finding(s) and their exact numbers
   - The methodology used
   - The key evidence supporting the main claim
   - The broader significance or implications stated in the discussion
   - All defined acronyms
3. This thorough reading ensures the abstract accurately reflects the full paper, not just the introduction.

## Step 4: Draft the Abstract

Use the 6-sentence structure as a guide. The final abstract may have more or fewer sentences depending on the word limit, but it should cover all six elements:

### Sentence 1: Context / Background
- What is known in the field. Set the stage for the problem.
- Keep brief (1-2 sentences). Avoid starting with "In recent years..." or other cliches.
- Aim for a statement that a broad scientific audience can understand.

### Sentence 2: Gap / Problem
- What is unknown, unresolved, or problematic.
- This is the motivation for the study.
- Frame it as a tension or open question, not just a lack of prior work.

### Sentence 3: "Here we show..."
- The core finding, stated directly and quantitatively.
- This is the most important sentence in the abstract.
- Must include at least one specific number or quantitative result from the manuscript.
- Prefer concrete verbs and visible actors, while retaining passive voice when the scientific object is the natural topic

### Sentence 4: Key Evidence / Method
- How the finding was established.
- Mention the method, dataset, or analytical approach briefly.
- Include a supporting quantitative result if space allows.

### Sentence 5: Broader Implication
- Why this matters beyond the immediate finding.
- Connect to the larger scientific question, societal relevance, or policy context.

### Sentence 6: Forward-Looking Hook
- What this work enables: new questions, new methods, new directions.
- Leave the reader with a reason to read the full paper.
- For very tight word limits (Nature Communications: 150 words), this may merge with sentence 5.

**Adaptation for word limits:**
- For 150-word abstracts: sentences 5 and 6 should merge; sentences 1 and 2 should be as concise as possible (1 sentence each).
- For 200-word abstracts: each element gets roughly one sentence.
- For 250-350-word abstracts: elements can expand, especially evidence (sentence 4) and implications (sentence 5).

## Step 5: Quality Checks

Run the following checks on the drafted abstract and report results:

### 5a: Word Count
- Count words in the abstract.
- Compare against the journal limit from Step 2.
- Report: "Abstract: X words (limit: Y)" with a PASS/FAIL indicator.
- If over the limit, identify which sentences could be trimmed and suggest specific cuts.

### 5b: Number Cross-Reference
- Extract every number, percentage, date, and quantitative claim from the abstract.
- Search the manuscript body for each one.
- Every number in the abstract must appear somewhere in the manuscript (Results, Methods, or figures).
- Report: list each number and its source location in the manuscript, or flag "NOT FOUND" for any mismatch.

### 5c: Acronym Check
- Identify all acronyms in the abstract.
- Verify each is defined on first use within the abstract (not relying on the main text).
- If the journal forbids acronyms in abstracts, flag any that appear.
- Report: list acronyms with DEFINED/UNDEFINED status.

### 5d: Reference Check
- If the journal forbids references in the abstract, verify none are present.
- If references are allowed, verify all cited keys exist in the bibliography.
- Report: PASS/FAIL.

### 5e: Jargon and Readability
- Flag technical terms that a non-specialist reader might not understand.
- Suggest plain-language alternatives where possible.
- This is advisory, not a hard fail -- the user decides what to keep.

### 5f: "Here We Show" Specificity
- Check that the core finding sentence (sentence 3) contains a specific quantitative result, not just a qualitative claim.
- BAD: "Here we show that the bias is significant."
- GOOD: "Here we show that the representativeness bias accounts for 15-30% of the apparent growth rate anomaly."
- Report: PASS (quantitative and specific) or FLAG (needs strengthening).

## Step 6: Present to User

Present the drafted abstract to the user with:
1. The abstract text, clearly formatted
2. Word count and journal limit
3. Quality check results as a summary table:
   ```
   | Check                  | Result |
   |------------------------|--------|
   | Word count             | PASS (187/200) |
   | Number cross-reference | PASS (all 4 numbers verified) |
   | Acronyms               | PASS (CO2 defined) |
   | References             | PASS (none, as required) |
   | Jargon                 | 2 terms flagged |
   | Specificity            | PASS |
   ```
4. Any flagged issues with suggested fixes.

Ask: "Would you like me to revise any part of this abstract, or shall I write it to the manuscript?"

## Step 7: Write to Manuscript

1. Read the main-text file (resolved from `metadata.yaml` → `current_draft`; fallback `drafts/manuscript.md`) to find the existing Abstract section.
2. If an abstract already exists:
   - Show the old abstract and the new one side by side.
   - Ask for confirmation before replacing.
3. Replace the Abstract section content with the new abstract.
4. If the journal requires a separate Significance Statement (PNAS), draft that as well and place it after the abstract.
5. Confirm the file has been updated and report the final word count.

## Notes

- The 6-sentence structure is a guide, not a rigid template. Some abstracts work better with 4-5 sentences; others need 7-8. The key is that all six elements are present.
- For PNAS: draft both the abstract (250 words) and the Significance Statement (120 words, no jargon, accessible to a broad audience).
- If the user asks to "check" an existing abstract rather than draft a new one, skip Step 4 and run Step 5 quality checks on the existing abstract, then suggest improvements.
- Avoid em-dash overuse and AI-sounding language ("groundbreaking", "novel insights", "comprehensive analysis").
