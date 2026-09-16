#!/usr/bin/env python3
"""Structural checks on the skill set and its documentation.

These exist because the AGENTS.md skills table had silently drifted three rows
behind the skills on disk (`km-orient`, `km-tidy-exports`, `km-editor-review`
were undocumented while being actively used).
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"
AGENTS = ROOT / "AGENTS.md"

#: Absolute interpreter paths must not be hardcoded in a SKILL.md.
#: See resources/conventions/tooling.md.
INTERPRETER_RE = re.compile(r"(?<!\$\{)(/(?:mnt|home|usr|opt)/[^\s`\"']*?/bin/python[0-9.]*)")


def skill_dirs():
    return sorted(p for p in SKILLS.glob("km-*") if (p / "SKILL.md").is_file())


class TestSkillRegistry(unittest.TestCase):
    def test_frontmatter_name_matches_directory(self):
        for d in skill_dirs():
            with self.subTest(skill=d.name):
                text = (d / "SKILL.md").read_text(encoding="utf-8")
                m = re.search(r"^name:\s*(\S+)", text, flags=re.M)
                self.assertIsNotNone(m, "SKILL.md has no `name:` frontmatter")
                self.assertEqual(m.group(1).strip().strip('"\''), d.name)

    def test_every_skill_appears_in_agents_table(self):
        table = AGENTS.read_text(encoding="utf-8")
        documented = set(re.findall(r"skills/(km-[a-z0-9-]+)/SKILL\.md", table))
        on_disk = {d.name for d in skill_dirs()}
        missing = sorted(on_disk - documented)
        self.assertFalse(missing, f"skills on disk but absent from the AGENTS.md table: {missing}")

    def test_no_table_row_points_at_a_missing_skill(self):
        table = AGENTS.read_text(encoding="utf-8")
        documented = set(re.findall(r"skills/(km-[a-z0-9-]+)/SKILL\.md", table))
        on_disk = {d.name for d in skill_dirs()}
        stale = sorted(documented - on_disk)
        self.assertFalse(stale, f"AGENTS.md references skills that do not exist: {stale}")

    def test_delegation_claim_matches_reality(self):
        """AGENTS.md must not claim a delegation table that a skill lacks."""
        table = AGENTS.read_text(encoding="utf-8")
        claims_all = re.search(r"each carries a \"Delegation \(do not duplicate\)\" table", table)
        if not claims_all:
            return  # claim already scoped; nothing to enforce
        review_skills = ["km-presubmit-audit", "km-wordcount", "km-ref-check",
                         "km-polish-audit", "km-deep-read", "km-supplementary", "km-figures"]
        without = [s for s in review_skills
                   if "Delegation (do not duplicate)" not in
                   (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")]
        self.assertFalse(
            without,
            f"AGENTS.md claims every checking skill carries a delegation table, but these "
            f"do not: {without}. Either add the table or scope the claim.")


class TestNoHardcodedInterpreter(unittest.TestCase):
    """Regression guard: the conda path was removed once and came back."""

    def test_no_absolute_interpreter_in_skill_docs(self):
        offenders = []
        for d in skill_dirs():
            text = (d / "SKILL.md").read_text(encoding="utf-8")
            for hit in INTERPRETER_RE.findall(text):
                offenders.append(f"{d.name}/SKILL.md: {hit}")
        self.assertFalse(
            offenders,
            "hardcoded absolute interpreter path(s) found; use \"${KALAM_PYTHON:-python3}\" "
            "per resources/conventions/tooling.md:\n  " + "\n  ".join(offenders))


class TestConventionsReferenced(unittest.TestCase):
    def test_every_convention_file_is_referenced_somewhere(self):
        conv = sorted((ROOT / "resources" / "conventions").glob("*.md"))
        self.assertTrue(conv, "no convention files found")
        haystack = "\n".join(
            p.read_text(encoding="utf-8", errors="replace")
            for p in [AGENTS, *SKILLS.rglob("SKILL.md"), *(ROOT / "resources" / "conventions").glob("*.md")]
        )
        orphans = [c.name for c in conv
                   if f"conventions/{c.name}" not in haystack]
        self.assertFalse(orphans, f"convention files nothing points at: {orphans}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
