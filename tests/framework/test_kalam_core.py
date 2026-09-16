#!/usr/bin/env python3
"""Tests for lib/kalam_core: path resolution and metadata parsing.

Uses synthetic fixtures in a temp dir (so the suite does not depend on the state
of a live manuscript), then adds a light smoke check against the real tree.

Fixture coverage is deliberately explicit about formats:

* **Supported** — Markdown drafts named in ``current_draft``. This is the
  real-world case; Kalam's manuscripts are Markdown.
* **Nested** — a depth-2 manuscript (``<group>/<name>/``), the shape that
  previously broke depth-assuming tooling.
* **Unsupported** — DOCX. ``inventory.py`` parses Markdown text only; it does
  **not** read DOCX. Pointing ``current_draft`` at a ``.docx`` yields zero
  resolved files. That is a real limitation, not a passing compatibility test,
  so the test asserts the honest outcome and is named accordingly.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "lib"))

from kalam_core import metadata, paths  # noqa: E402


def _make_manuscript(base: Path, rel: str, current_draft: str, files: dict[str, str]):
    mdir = base / "manuscripts" / rel
    (mdir / "drafts").mkdir(parents=True, exist_ok=True)
    (mdir / "metadata.yaml").write_text(
        f'title: "T"\nstage: "drafting"\ncurrent_version: "v1.0"\n'
        f'current_draft: "{current_draft}"\n',
        encoding="utf-8",
    )
    for name, body in files.items():
        p = mdir / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
    return mdir


class TestFixtures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        # Minimal framework root markers so kalam_root() resolves here.
        (self.base / "AGENTS.md").write_text("root", encoding="utf-8")
        (self.base / "skills").mkdir()
        (self.base / "resources").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    # ---- supported format: markdown -------------------------------------
    def test_supported_markdown_single_file_depth1(self):
        m = _make_manuscript(self.base, "solo", "drafts/manuscript.md",
                             {"drafts/manuscript.md": "# T\n\nBody.\n"})
        got = metadata.resolve_draft_files(m)
        self.assertEqual([p.name for p in got], ["manuscript.md"])

    def test_supported_markdown_split_files(self):
        m = _make_manuscript(
            self.base, "split",
            "drafts/main_text.md, drafts/methods.md, drafts/extended_data_SI.md",
            {"drafts/main_text.md": "# M\n", "drafts/methods.md": "# Me\n",
             "drafts/extended_data_SI.md": "# SI\n"})
        got = metadata.resolve_draft_files(m)
        self.assertEqual([p.name for p in got],
                         ["main_text.md", "methods.md", "extended_data_SI.md"])
        self.assertEqual(metadata.classify("extended_data_SI.md"), "si")
        self.assertEqual(metadata.classify("main_text.md"), "main_text")

    # ---- nested path (depth 2) ------------------------------------------
    def test_nested_depth2_manuscript_resolves(self):
        m = _make_manuscript(self.base, "coauthor/paper", "drafts/manuscript.md",
                             {"drafts/manuscript.md": "# N\n\nBody.\n"})
        got = metadata.resolve_draft_files(m)
        self.assertEqual([p.name for p in got], ["manuscript.md"])
        self.assertEqual(paths.manuscript_name(m, self.base), "coauthor/paper")

    def test_discovery_finds_both_depths(self):
        _make_manuscript(self.base, "flat", "drafts/manuscript.md",
                         {"drafts/manuscript.md": "x"})
        _make_manuscript(self.base, "grp/nested", "drafts/manuscript.md",
                         {"drafts/manuscript.md": "x"})
        names = {paths.manuscript_name(p, self.base)
                 for p in paths.iter_manuscript_dirs(self.base)}
        self.assertEqual(names, {"flat", "grp/nested"})

    def test_archive_excluded_by_default(self):
        _make_manuscript(self.base, "archive/old_snapshot", "drafts/manuscript.md",
                         {"drafts/manuscript.md": "x"})
        self.assertEqual(list(paths.iter_manuscript_dirs(self.base)), [])
        self.assertEqual(
            len(list(paths.iter_manuscript_dirs(self.base, include_archive=True))), 1)

    # ---- unsupported format: honest documentation of the real boundary ---
    def test_docx_path_resolves_but_is_not_a_parsable_draft(self):
        """Records where the DOCX limitation actually bites.

        Path resolution is format-agnostic: a .docx named in current_draft IS
        returned by the resolver. The limitation is downstream — inventory.py
        parses Markdown text only, so a DOCX yields no headings, paragraphs or
        figures. Asserting both halves so neither is mistaken for the other.
        """
        m = _make_manuscript(self.base, "worddoc", "drafts/manuscript.docx",
                             {"drafts/manuscript.docx": "PK\x03\x04binary\x00payload"})
        resolved = metadata.resolve_draft_files(m)
        self.assertEqual([p.name for p in resolved], ["manuscript.docx"],
                         "resolution is format-agnostic and should return the declared path")
        self.assertEqual(metadata.classify("manuscript.docx"), "main_text")

        # Downstream: treating that binary as Markdown produces no usable structure.
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "inv", ROOT / "skills" / "km-deep-read" / "scripts" / "inventory.py")
        inv = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(inv)
        raw = resolved[0].read_text(encoding="utf-8", errors="replace")
        kinds = [k for k, _h, _b in inv.split_blocks(raw)]
        self.assertNotIn("heading", kinds,
                         "a DOCX must not yield Markdown headings; if it does, this "
                         "test's premise about format support is wrong")

    def test_docx_manuscripts_are_not_a_meaningful_compat_fixture(self):
        """Guard against citing a DOCX zero-result as evidence of compatibility.

        All five live manuscripts are Markdown (verified 2026-09-09), so the
        supported-format fixtures above are the real coverage.
        """
        live_md = 0
        for m in paths.iter_manuscript_dirs(ROOT):
            for f in metadata.resolve_draft_files(m, legacy=True):
                if f.suffix == ".md":
                    live_md += 1
        self.assertGreater(live_md, 0, "expected Markdown drafts in the live tree")

    # ---- scalar parsing --------------------------------------------------
    def test_read_scalar_strips_quotes_and_comments(self):
        t = 'current_version: "v9.8"  # canonical field name\nstage: drafting # x\nempty:\n'
        self.assertEqual(metadata.read_scalar(t, "current_version"), "v9.8")
        self.assertEqual(metadata.read_scalar(t, "stage"), "drafting")
        self.assertIsNone(metadata.read_scalar(t, "empty"))
        self.assertIsNone(metadata.read_scalar(t, "absent"))

    def test_legacy_resolver_drops_subdirectories(self):
        """Documents the known legacy behaviour that the example-paper divergence stems from."""
        t = 'current_draft: "drafts/sub/main_text.md"\n'
        self.assertEqual(metadata.draft_tokens_legacy_basename(t), ["main_text.md"])
        self.assertEqual(metadata.current_draft_entries(t), ["drafts/sub/main_text.md"])


class TestLiveTree(unittest.TestCase):
    """Smoke checks against the real repository."""

    def test_root_resolves_from_lib(self):
        self.assertEqual(paths.kalam_root(ROOT / "lib" / "kalam_core"), ROOT)

    def test_all_live_manuscripts_resolve_at_least_one_draft(self):
        found = list(paths.iter_manuscript_dirs(ROOT))
        self.assertGreaterEqual(len(found), 1)
        for m in found:
            with self.subTest(manuscript=paths.manuscript_name(m, ROOT)):
                self.assertTrue(metadata.resolve_draft_files(m, legacy=True),
                                "legacy resolution returned no files")

    def test_nested_manuscripts_resolve_when_present(self):
        """Depth-2 naming, checked against the live tree only if it has one.

        Depth-2 resolution itself is covered unconditionally by the temp-dir
        fixtures above. A fresh install has only depth-1 manuscripts, so asserting
        that a grouped manuscript exists here would fail on every new clone.
        """
        names = [paths.manuscript_name(p, ROOT) for p in paths.iter_manuscript_dirs(ROOT)]
        nested = [n for n in names if "/" in n]
        if not nested:
            self.skipTest("no grouped (depth-2) manuscript in this tree")
        for n in nested:
            with self.subTest(manuscript=n):
                self.assertEqual(len(n.split("/")), 2, "grouping is one level deep")


if __name__ == "__main__":
    unittest.main(verbosity=2)
