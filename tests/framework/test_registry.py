#!/usr/bin/env python3
"""Checks that manuscripts/registry.yaml stays consistent with the live tree.

The registry is an index, not a source of truth: each manuscript's metadata.yaml
wins. These tests only assert that the index does not drift out of correspondence
with what is actually on disk.

Parsed with a deliberately small regex reader rather than PyYAML so the suite has
no third-party dependency, matching the rest of the framework's tooling.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib"))

from kalam_core import metadata, paths  # noqa: E402

REGISTRY = ROOT / "manuscripts" / "registry.yaml"


def registry_entries():
    """Return [{name, path, stage, current_version}] from registry.yaml."""
    text = REGISTRY.read_text(encoding="utf-8")
    entries, cur = [], None
    for line in text.splitlines():
        if re.match(r"\s*-\s+name:", line):
            if cur:
                entries.append(cur)
            cur = {"name": line.split("name:", 1)[1].strip().strip('"\'')}
        elif cur is not None:
            m = re.match(r"\s{4}(path|stage|current_version):\s*(.*)$", line)
            if m:
                # Strip a trailing comment BEFORE unquoting, or a quoted value
                # followed by a comment keeps its closing quote.
                val = re.sub(r"\s+#.*$", "", m.group(2).strip())
                cur[m.group(1)] = val.strip().strip('"\'')
    if cur:
        entries.append(cur)
    return entries


class TestRegistry(unittest.TestCase):
    def setUp(self):
        self.entries = registry_entries()
        self.discovered = {paths.manuscript_name(p, ROOT): p
                           for p in paths.iter_manuscript_dirs(ROOT)}

    def test_registry_parses(self):
        self.assertTrue(self.entries, "registry.yaml yielded no entries")

    def test_every_registry_path_exists(self):
        for e in self.entries:
            with self.subTest(name=e["name"]):
                self.assertTrue((ROOT / e["path"]).is_dir(), f"missing dir {e['path']}")
                self.assertTrue((ROOT / e["path"] / "metadata.yaml").is_file())

    def test_registry_name_matches_path(self):
        for e in self.entries:
            with self.subTest(name=e["name"]):
                self.assertEqual(e["path"], f"manuscripts/{e['name']}")

    def test_registry_covers_every_discovered_manuscript(self):
        listed = {e["name"] for e in self.entries}
        missing = sorted(set(self.discovered) - listed)
        self.assertFalse(missing, f"manuscripts on disk but not in registry.yaml: {missing}")

    def test_registry_lists_nothing_extra(self):
        listed = {e["name"] for e in self.entries}
        extra = sorted(listed - set(self.discovered))
        self.assertFalse(extra, f"registry.yaml lists non-discovered manuscripts: {extra}")

    def test_stage_and_version_match_metadata(self):
        """The index must not contradict metadata.yaml."""
        for e in self.entries:
            mdir = ROOT / e["path"]
            text = metadata.read_text(mdir)
            with self.subTest(name=e["name"]):
                if "stage" in e:
                    self.assertEqual(e["stage"], metadata.read_scalar(text, "stage"),
                                     "registry stage disagrees with metadata.yaml")
                if "current_version" in e:
                    self.assertEqual(e["current_version"],
                                     metadata.read_scalar(text, "current_version"),
                                     "registry current_version disagrees with metadata.yaml")


class TestValidatorIsAdvisory(unittest.TestCase):
    def test_validator_exits_zero_despite_findings(self):
        """The validator must never gate: exit 0 without --strict."""
        import subprocess
        r = subprocess.run(
            [sys.executable, str(ROOT / "lib" / "kalam_core" / "validate.py")],
            capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(r.returncode, 0,
                         f"advisory validator must exit 0; got {r.returncode}\n{r.stderr}")
        self.assertIn("Advisory only", r.stdout)

    def test_validator_does_not_modify_metadata(self):
        import hashlib, subprocess
        def digest():
            h = hashlib.sha256()
            for p in sorted(paths.iter_manuscript_dirs(ROOT)):
                h.update((p / "metadata.yaml").read_bytes())
            return h.hexdigest()
        before = digest()
        subprocess.run([sys.executable, str(ROOT / "lib" / "kalam_core" / "validate.py")],
                       capture_output=True, text=True, cwd=ROOT)
        self.assertEqual(before, digest(), "validator mutated a metadata.yaml")


if __name__ == "__main__":
    unittest.main(verbosity=2)
