---
name: km-research
description: "Use when the user needs background research for a manuscript. Three modes: (1) internet research using web search, (2) deep research workflow generating prompts for Google/Claude/ChatGPT Deep Research, (3) NotebookLM automated research. Saves results to the manuscript's research/ directory. Invoke with /km-research."
---

# Research Support

Three modes of research to support manuscript development at any stage.

## Setup

1. Read `metadata.yaml` to identify the manuscript and current stage
2. Ask the user: **Internet research**, **Deep research**, or **NotebookLM research**?

---

## Mode 1: Internet Research

Search the web for background knowledge, references, and supporting evidence.

### Process

1. Ask the user for the research question or topic
2. Search the web for relevant papers, datasets, and context
3. For promising results, fetch the page content from allowed academic domains
4. For each finding, create a structured note:

```markdown
# [Topic] — Internet Research Notes

Date: [TODAY]
Query: "[search query used]"
Manuscript: [name]
Stage: [current stage]

## Finding 1: [title]
- **Source**: [URL]
- **Key point**: [1–2 sentences]
- **Relevance**: [how this connects to the manuscript]
- **BibTeX**: (if a citable paper)

## Finding 2: [title]
...

## Summary
[2–3 sentence synthesis of what was learned]

## Action Items
- [ ] Add [reference] to references.bib
- [ ] Mention in [section] of the manuscript
```

5. Save to `research/background_research/[topic]_[date].md`
6. Add new BibTeX entries to `references.bib`
7. Present summary to user

---

## Mode 2: Deep Research Workflow

Generate optimized prompts for external deep research tools, then integrate the results.

### Phase 1: Generate Prompt

1. Ask the user:
   - What question needs deep research?
   - Which platform? (Google Deep Research / Claude / ChatGPT / other)
   - What scope? (time period, fields, geographic focus)

2. Generate an optimized prompt:

```markdown
# Deep Research Prompt

**Topic**: [topic]
**For manuscript**: [title]
**Platform**: [Google/Claude/ChatGPT]
**Date**: [TODAY]

## Question
[The specific, well-scoped research question]

## Scope
- Time period: [e.g., 2020–2025]
- Fields: [e.g., atmospheric science, remote sensing]
- Focus: [what to prioritize]
- Exclude: [what to skip]

## Desired Output
- Key findings from recent literature (2020–present preferred)
- Comparison of methods/approaches relevant to [topic]
- Unresolved questions in the field
- Full citations (author, year, journal, DOI) for every reference mentioned

## Context
[Brief description of the manuscript and why this research is needed.
Include the core finding so the research tool can prioritize relevant results.]
```

3. Save prompt to `research/deep_research/prompt_[topic]_[date].md`
4. Tell the user: "Copy this prompt into [platform]. Save the result to `research/deep_research/result_[topic]_[date].md`"

### Phase 2: Integrate Results

When the user says the result file is saved:

1. Read `research/deep_research/result_[topic]_[date].md`
2. Extract:
   - Key findings relevant to the manuscript
   - New references with full citations
   - Comparison points and context
   - Unresolved questions or contradictions
3. Create structured literature notes in `research/literature_notes/[topic].md`:

```markdown
# Literature Notes: [Topic]

Source: Deep research result from [platform], [date]

## Key Findings
1. [finding with citation]

## New References
- [Author et al., Year, Journal] — [why it matters]

## Integration Points
- Introduction: [what to add]
- Methods: [what to reference]
- Discussion: [what to compare]

## Open Questions
-
```

4. Add new BibTeX entries to `references.bib`
5. Log in `notes.md` what was researched and what was integrated

---

## Mode 3: NotebookLM Research

Automated research using the NotebookLM MCP. Requires `notebook_id` in `metadata.yaml`.

### Prerequisites

1. Check `metadata.yaml` for `notebook_id`
2. If empty, ask: "Create a NotebookLM notebook first? Or use Mode 1/2 instead?"
3. If user says yes, create one: `notebook_create(title="<manuscript title>")` and save `notebook_id` to `metadata.yaml`

### Process

1. Ask the user for the research question or topic
2. Ask: **Fast research** (~30s, ~10 sources) or **Deep research** (~5min, ~40 sources)?

3. Start the research:
   ```
   research_start(query="<question>", notebook_id="<id>", mode="fast|deep")
   ```

4. Poll for completion:
   ```
   research_status(notebook_id="<id>", max_wait=300)
   ```

5. Review discovered sources. Ask user which to import:
   ```
   research_import(notebook_id="<id>", task_id="<task_id>", source_indices=[...])
   ```

6. Query the imported sources for synthesis:
   ```
   notebook_query(notebook_id="<id>", query="Summarize the key findings about <topic>")
   notebook_query(notebook_id="<id>", query="What methods have been used to study <topic>?")
   notebook_query(notebook_id="<id>", query="What are the unresolved questions about <topic>?")
   ```

7. Optionally generate a Briefing Doc:
   ```
   studio_create(notebook_id="<id>", artifact_type="report", report_format="Briefing Doc", confirm=True)
   ```
   Then download:
   ```
   download_artifact(notebook_id="<id>", artifact_type="report", output_path="research/literature_notes/<topic>_briefing.md")
   ```

8. Create structured notes from the synthesis:

```markdown
# [Topic] — NotebookLM Research Notes

Date: [TODAY]
Query: "[research query]"
Mode: [fast/deep]
Manuscript: [name]
Stage: [current stage]
Sources imported: [count]

## Key Findings
1. [finding with citation from notebook_query response]

## New References
- [Author et al., Year, Journal] — [why it matters]

## Integration Points
- Introduction: [what to add]
- Methods: [what to reference]
- Discussion: [what to compare]

## Open Questions
-
```

9. Save to `research/background_research/[topic]_nlm_[date].md`
10. Extract BibTeX entries from discovered sources → add to `references.bib`
11. Log in `notes.md`: "NotebookLM [fast/deep] research on [topic] — [count] sources imported"
12. Present summary to user

### Ongoing Source Management

At any point during the manuscript workflow:
- **Add a paper**: `source_add(notebook_id, source_type="url", url="https://doi.org/...")`
- **Add pasted text**: `source_add(notebook_id, source_type="text", text="...", title="...")`
- **Ask a question**: `notebook_query(notebook_id, query="...")`
- **Get overview**: `notebook_describe(notebook_id)`
- **List sources**: `notebook_get(notebook_id)`

---

## Research Quality Rules

- Always cite the **primary source**, not the research summary
- Verify DOIs when possible
- Flag if a finding contradicts existing claims in the manuscript
- Do not include references that cannot be verified
- Mark uncertain findings with "[needs verification]"
