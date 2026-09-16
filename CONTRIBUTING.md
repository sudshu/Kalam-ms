# Contributing

Kalam is mostly Markdown: prompts, conventions and journal profiles. The most useful
contributions are correspondingly small.

## Most wanted

1. **New journal profiles.** Copy the closest file in `resources/journal_profiles/`,
   then fill it in **from that journal's own author guidelines** and cite them in the
   file. Never estimate a word limit or a display-item count — a wrong number in a
   profile is worse than a missing profile, because skills trust it.
2. **Bug reports against the scripts.** `inventory.py`, `count_words.py`,
   `bump_version.py` and the export scripts all do real parsing and have real edge
   cases. A failing example is worth more than a description.
3. **Writing-policy disagreements**, argued. `resources/conventions/writing_style.md` is
   opinionated on purpose. If a rule produces worse prose in your field, open an issue
   with a before/after example.

## Before opening a pull request

```bash
python tests/framework/test_skill_registry.py   # skills ↔ AGENTS.md table, no absolute interpreter paths
python tests/framework/test_kalam_core.py       # path resolution and metadata parsing
python tests/framework/test_registry.py         # registry ↔ live tree
```

All three must pass. They are stdlib-only and take under a second.

## Conventions that the tests enforce

- **Every skill appears in the `AGENTS.md` table, and every table row points at a skill
  that exists.** Adding `skills/km-foo/SKILL.md` means adding its row.
- **A skill's frontmatter `name:` matches its directory name.**
- **No absolute interpreter paths in a `SKILL.md`.** Use `"${KALAM_PYTHON:-python3}"`;
  see `resources/conventions/tooling.md`.

## Conventions the tests cannot enforce

- **One concern per skill.** If your new check overlaps an existing skill, extend that
  skill instead. The six checking skills carry a "Delegation (do not duplicate)" table;
  respect it.
- **No hardcoded journal limits in skill files.** Read them from the journal profile.
- **Never make a skill invent content** — a reference, a number, a claim about the user.
  `[VERIFY: ...]` is the correct output when information is missing.
- **Keep personal data out.** No names, affiliations, institutional paths, grant numbers
  or local filesystem paths in framework files. Examples should reference the demo
  manuscript or a generic placeholder.

## Before you publish a fork

`resources/User/USER.md` is tracked, because its placeholder is what triggers onboarding.
After `/km-onboard` it holds your name, affiliation and email:

```bash
git rm --cached resources/User/USER.md
echo "resources/User/USER.md" >> .gitignore
```

Check your manuscripts too — `manuscripts/` is not ignored, and unpublished drafts are
easy to commit by accident.
