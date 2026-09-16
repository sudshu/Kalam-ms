---
name: km-new-manuscript
description: "Use when creating a new manuscript project. Copies the template folder, gathers metadata (title, authors, journal, research question, analysis folder), selects bibliography files, and initializes the manuscript. Invoke with /km-new-manuscript <short_name>."
---

# New Manuscript Setup

Create a new manuscript project from the template.

## Process

### Phase 1: Gather Information

Ask the user for the following (in batches of 2–3 questions):

**Batch 1 — Core Identity:**
1. What is the working title?
2. What is the research question or core finding (one sentence)?

**Batch 2 — Authors and Audience:**
3. Who are the co-authors? (Pre-fill first author from `../../resources/User/USER.md`)
4. Which communities should read this paper?

**Batch 3 — Journal and Format:**
5. What is the target journal? (Show list from `../../resources/journal_profiles/`)
6. Is there an external analysis folder with scripts/data? If so, what is the full path?

### Phase 2: Create the Manuscript Folder

1. Copy the template:
```bash
cp -r resources/manuscript_template/ manuscripts/<short_name>/
```

2. Fill `manuscripts/<short_name>/metadata.yaml` with gathered information:
   - title, short_title, project_name
   - authors (pre-fill user info from `../../resources/User/USER.md`)
   - target_journal, journal_profile (path to journal profile file)
   - research_question, core_finding
   - analysis_dir (if provided)
   - created: today's date
   - last_updated: today's date

3. The manuscript AGENTS.md reads from `metadata.yaml` dynamically — no header replacement needed.

### Phase 3: Bibliography Setup

1. If the user keeps a shared pool at `../../resources/bibliography/master.bib` (optional; see that folder's `README.md`), use it as the source
2. Start `manuscripts/<short_name>/references.bib` from `master.bib` when it exists — copy it and let `/km-ref-check` trim to cited keys at submission. With no shared pool, start from the template's empty `references.bib` and add entries as they are cited
3. Add any new entries directly to the manuscript's `references.bib` as you cite

### Phase 4: Identify Prior Publications

1. Read `../../resources/User/publications.md` if the user has added one (optional)
2. Identify 3–7 user publications relevant to this manuscript topic
3. Ensure they are in `references.bib`
4. Note them in `manuscripts/<short_name>/notes.md` as candidates for self-citation

### Phase 5: Report

Show the user:
- Manuscript folder created at `manuscripts/<short_name>/`
- Metadata summary
- Selected bibliography files
- Suggested self-citations
- Next step: "Run `/km-ideation` to begin Stage 1"

### Phase 6: NotebookLM Setup (Optional)

If NotebookLM MCP is available:

1. Create a notebook for this manuscript:
   ```
   notebook_create(title="<manuscript title>")
   ```
2. Save the returned `notebook_id` to `manuscripts/<short_name>/metadata.yaml`
3. Add any example or reference papers the user provides as file sources:
   ```
   source_add(notebook_id, source_type="file", file_path="<path>")
   ```
4. Add any key references the user mentioned as URL sources:
   ```
   source_add(notebook_id, source_type="url", url="<doi_url>")
   ```
5. Report: "NotebookLM notebook created. Use `/km-research` Mode 3 for automated literature search."

If NotebookLM MCP is NOT available:
- Tell the user: "Create a notebook at notebooklm.google.com titled '<title>' and paste the notebook ID into `metadata.yaml` under `notebook_id`."
