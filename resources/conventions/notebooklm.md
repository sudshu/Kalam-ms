# NotebookLM integration

Each manuscript can have a dedicated [NotebookLM](https://notebooklm.google.com) notebook for research and source management. The notebook ID is stored in `metadata.yaml` as `notebook_id`. Loaded on demand by `/km-research` (Mode 3) and `/km-advisor`.

## Capabilities

| Capability | What it does | When to use |
|------------|-------------|-------------|
| **Create notebook** | `notebook_create(title)` | During `/km-new-manuscript` setup |
| **Add sources** | `source_add(url/text/file)` | Add papers, web pages, or pasted text as sources |
| **Fast research** | `research_start(query, mode="fast")` | Quick search (~30s, ~10 sources) |
| **Deep research** | `research_start(query, mode="deep")` | Thorough search (~5min, ~40 sources) |
| **Query sources** | `notebook_query(query)` | Ask questions about collected sources |
| **Generate report** | `studio_create(artifact_type="report")` | Create Briefing Doc or Study Guide from sources |
| **Generate mind map** | `studio_create(artifact_type="mind_map")` | Visualize connections between sources |
| **Source summary** | `notebook_describe()` | Get AI summary of all sources |
| **Download artifacts** | `download_artifact()` | Save reports, mind maps locally |

## Cross-platform usage

- **Claude Code**: NotebookLM MCP tools are available directly. Use them as documented above.
- **OpenAI Codex / Google Gemini**: NotebookLM MCP is not available as direct tool calls. Instead:
  1. Use the `nlm` CLI if installed (`nlm login`, then API calls)
  2. Or: generate instructions for the user to perform actions manually at notebooklm.google.com
  3. The agent can still read/write research files in `research/` as before

## Workflow

1. **Setup** (`/km-new-manuscript`): Create a NotebookLM notebook → store `notebook_id` in `metadata.yaml` → add example papers as sources
2. **Research** (`/km-research` Mode 3): Use `research_start` for fast/deep web research → `research_import` to add sources → `notebook_query` to synthesize → save notes locally
3. **Any stage**: Use `notebook_query` to ask questions about collected literature
4. **Expert review** (`/km-advisor`): Use `notebook_describe` for source summary and literature context
