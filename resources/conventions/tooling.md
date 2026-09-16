# Tooling conventions

## Python interpreter

Skills and bundled scripts must **not** hardcode an absolute interpreter path.
Use `$KALAM_PYTHON`, falling back to `python3`:

```bash
"${KALAM_PYTHON:-python3}" <skill_base_dir>/scripts/example.py <args>
```

If your scientific Python lives in a virtualenv or conda environment rather than on
`PATH`, export the interpreter once per environment - in your shell profile, so every
session inherits it:

```bash
export KALAM_PYTHON=/path/to/your/env/bin/python
```

Plain `python3` is enough for every bundled script; `$KALAM_PYTHON` matters when a
manuscript's figure or analysis code needs a specific environment.

**Why this rule exists.** An absolute interpreter path in a `SKILL.md` breaks the
framework for every other machine, and it has crept back in more than once.
`tests/framework/test_skill_registry.py::TestNoHardcodedInterpreter` fails if one
reappears, so the
convention is enforced rather than merely documented.

Scope: this covers `skills/**/SKILL.md`. Manuscript-local analysis scripts may
pin an interpreter — they are not portable framework code.

## Shared helpers

Reusable, framework-level Python lives in `lib/kalam_core/`:

| Module | Purpose |
|---|---|
| `paths.py` | `kalam_root()`, `manuscript_dir()` — depth-agnostic path resolution |
| `metadata.py` | the single `metadata.yaml` loader and `current_draft` resolver |
| `validate.py` | advisory metadata-schema validator (reports; never rewrites) |

Import it from a bundled script without depending on the working directory:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / "lib"))
from kalam_core import metadata
```

## Script invocation and stable paths

Invoke bundled scripts as `<skill_base_dir>/scripts/<name>.py`.

Two engines are load-bearing at their current absolute paths and must not be
moved without updating every caller:

- `skills/km-deep-read/scripts/inventory.py`
- `skills/km-wordcount/scripts/count_words.py`

Both are loaded as **modules** by manuscript-side verification scripts via
`importlib.util.spec_from_file_location`, in addition to being run as
subprocesses. Their public function names are part of that contract.
