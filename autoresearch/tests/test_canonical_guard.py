import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from autoresearch import canonical_guard


class CanonicalGuardTest(unittest.TestCase):
    def test_snapshot_and_report_detect_unchanged_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _canonical_root(Path(tmp))
            before = canonical_guard.snapshot(root)
            after = canonical_guard.snapshot(root)
            report_path = canonical_guard.write_guard_report(
                root / "guard.json",
                before=before,
                after=after,
                require_clean=False,
            )
            report = json.loads(report_path.read_text(encoding="utf-8"))

            self.assertEqual([], canonical_guard.diff_snapshots(before, after))
            self.assertTrue(report["unchanged_during_run"])
            self.assertEqual([], report["changed_paths"])

    def test_changed_canonical_file_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _canonical_root(Path(tmp))
            before = canonical_guard.snapshot(root)
            (root / "SKILL.md").write_text("changed\n", encoding="utf-8")
            after = canonical_guard.snapshot(root)

            self.assertEqual(["SKILL.md"], canonical_guard.diff_snapshots(before, after))

    def test_require_clean_git_rejects_dirty_canonical_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = _canonical_root(Path(tmp))
            _git(root, "init")
            _git(root, "add", "SKILL.md", "autoresearch/program.md")
            _git(
                root,
                "-c",
                "user.email=test@example.com",
                "-c",
                "user.name=Test",
                "commit",
                "-m",
                "init",
            )
            (root / "SKILL.md").write_text("dirty\n", encoding="utf-8")

            with self.assertRaises(canonical_guard.CanonicalGuardError):
                canonical_guard.require_clean_git(root)


def _canonical_root(root: Path) -> Path:
    (root / "autoresearch").mkdir()
    (root / "SKILL.md").write_text("skill\n", encoding="utf-8")
    (root / "autoresearch/program.md").write_text("program\n", encoding="utf-8")
    return root


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )


if __name__ == "__main__":
    unittest.main()
