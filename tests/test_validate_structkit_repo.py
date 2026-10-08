#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_structkit_repo import find_struct_files, is_struct_file  # noqa: E402


class FindStructFilesTests(unittest.TestCase):
    def test_is_struct_file_matches_canonical_named_and_legacy(self) -> None:
        self.assertTrue(is_struct_file(Path(".structkit.yaml")))
        self.assertTrue(is_struct_file(Path(".structkit.yml")))
        self.assertTrue(is_struct_file(Path("app.structkit.yaml")))
        self.assertTrue(is_struct_file(Path("app.structkit.yml")))
        self.assertTrue(is_struct_file(Path(".struct.yaml")))
        self.assertTrue(is_struct_file(Path(".struct.yml")))
        self.assertTrue(is_struct_file(Path("app.struct.yaml")))
        self.assertTrue(is_struct_file(Path("app.struct.yml")))
        self.assertFalse(is_struct_file(Path("other.yaml")))
        self.assertFalse(is_struct_file(Path("structkit.yaml")))
        self.assertFalse(is_struct_file(Path(".structkit.yaml.bak")))

    def test_find_struct_files_discovers_hidden_and_named_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "structures" / "nested"
            nested.mkdir(parents=True)

            expected = {
                root / ".structkit.yaml",
                root / ".structkit.yml",
                root / ".struct.yaml",
                root / ".struct.yml",
                nested / "app.structkit.yaml",
                nested / "app.structkit.yml",
                nested / "legacy.struct.yaml",
                nested / "legacy.struct.yml",
            }
            for path in expected:
                path.write_text("files: []\n", encoding="utf-8")
            (root / "other.yaml").write_text("not: a struct file\n", encoding="utf-8")
            (nested / "readme.md").write_text("# docs\n", encoding="utf-8")

            found = set(find_struct_files(root))
            self.assertEqual(found, expected)

    def test_find_struct_files_includes_repo_templates(self) -> None:
        found = {path.name for path in find_struct_files(ROOT)}
        self.assertIn("basic-structure.struct.yaml", found)
        self.assertIn("repo-scaffold.struct.yaml", found)


if __name__ == "__main__":
    unittest.main()
