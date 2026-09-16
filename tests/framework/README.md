# Framework tests

Structural regression tests for the Kalam framework itself (not for manuscript
science). Standard-library `unittest` only — no third-party dependency.

```bash
"${KALAM_PYTHON:-python3}" -m unittest discover -s tests/framework -p 'test_*.py'
```

| File | Guards against |
|---|---|
| `test_kalam_core.py` | path/metadata resolver regressions; depth-1 **and** depth-2 manuscripts; archive exclusion; the legacy-vs-canonical resolver divergence; the real DOCX boundary |
| `test_skill_registry.py` | `AGENTS.md` skills table drifting from `skills/km-*/`; frontmatter `name` ≠ directory; hardcoded absolute interpreter paths; orphaned convention files; overstated delegation-table claims |
| `test_registry.py` | `manuscripts/registry.yaml` drifting from the live tree or contradicting a `metadata.yaml`; the metadata validator staying advisory and non-mutating |

## Notes on fixtures

`test_kalam_core.py` builds synthetic manuscripts in a temp directory so the
suite does not depend on the state of a live paper, then adds a few smoke checks
against the real tree.

**Format coverage is deliberate.** All five live manuscripts are Markdown
(verified 2026-09-09), so the Markdown fixtures — single-file, split-file, and
nested depth-2 — are the real coverage. DOCX is *not* parsed by `inventory.py`;
`test_docx_path_resolves_but_is_not_a_parsable_draft` records where that
limitation actually bites (path resolution succeeds; Markdown structure
extraction yields nothing) precisely so a zero-file DOCX result is never cited as
evidence of compatibility.

## Not covered here

- Word/DOCX export fidelity — see `/km-export-docx`'s own verifier.
- Manuscript prose, numbers, figures or references — `/km-presubmit-audit` and
  friends own those.
- `count_words.py` and `inventory.py` output values. They are pinned by
  before/after baselines captured at reorganization time under the backup's
  `baselines/` directory.
