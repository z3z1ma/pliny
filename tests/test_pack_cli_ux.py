import contextlib
import importlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast

from agent_loom.pack.core import install_pack


pack_mod = importlib.import_module("agent_loom.pack.cli")
pack_cli = cast(Callable[[list[str]], int], getattr(pack_mod, "main"))


def _run_text(argv: list[str], *, cwd: Path) -> tuple[int, str, str]:
    out = io.StringIO()
    err = io.StringIO()
    old = Path.cwd()
    try:
        os.chdir(cwd)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = int(pack_cli(argv))
    finally:
        os.chdir(old)
    return rc, out.getvalue(), err.getvalue()


class TestPackCliUx(unittest.TestCase):
    def test_status_emits_note_when_drifted_without_diff(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            install_pack(repo_root=repo, pack_id="sample", dry_run=False)

            p = repo / ".opencode" / "commands" / "pack-sample.md"
            p.write_text("drift\n", encoding="utf-8")

            rc, out, err = _run_text(["status"], cwd=repo)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn('"drifted": 1', out)
        self.assertIn("rerun with --diff", out)

    def test_status_diff_prints_unified_diff_for_drifted_files(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            install_pack(repo_root=repo, pack_id="sample", dry_run=False)

            p = repo / ".opencode" / "commands" / "pack-sample.md"
            p.write_text("drift\n", encoding="utf-8")

            rc, out, err = _run_text(["status", "--diff"], cwd=repo)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("diff (drifted): sample/.opencode/commands/pack-sample.md", out)
        self.assertIn("--- pack:sample/.opencode/commands/pack-sample.md", out)
        self.assertIn("+drift", out)

    def test_install_conflict_is_visible_in_status(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)

            p = repo / ".opencode" / "commands" / "pack-sample.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("preexisting drift\n", encoding="utf-8")

            install_pack(repo_root=repo, pack_id="sample", dry_run=False)

            rc, out, err = _run_text(["status", "--json"], cwd=repo)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        payload = json.loads(out.strip())
        self.assertEqual(int(payload.get("drifted") or 0), 1)

    def test_install_prints_strong_drift_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)

            p = repo / ".opencode" / "commands" / "pack-sample.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("preexisting drift\n", encoding="utf-8")

            rc, out, err = _run_text(["install", "sample"], cwd=repo)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("IMPORTANT: pack has proposed updates to existing files", out)
        self.assertIn("loom pack install sample --diff", out)

    def test_install_diff_flag_prints_drifted_patch(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)

            p = repo / ".opencode" / "commands" / "pack-sample.md"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text("preexisting drift\n", encoding="utf-8")

            rc, out, err = _run_text(["install", "sample", "--diff"], cwd=repo)
        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        self.assertIn("diff (drifted): sample/.opencode/commands/pack-sample.md", out)
        self.assertIn("--- pack:sample/.opencode/commands/pack-sample.md", out)

    def test_status_invalid_lockfile_returns_structured_error(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            lock = repo / ".loom" / "pack" / "lock.json"
            lock.parent.mkdir(parents=True, exist_ok=True)
            lock.write_text(
                json.dumps({"version": 1, "packs": "bad-shape"}),
                encoding="utf-8",
            )
            rc, out, err = _run_text(["status", "--json"], cwd=repo)
        self.assertEqual(rc, 2)
        self.assertEqual(err, "")
        payload = json.loads(out.strip())
        self.assertEqual(payload.get("code"), "LOCK_INVALID")
        self.assertIn("loom pack doctor", str(payload.get("hint") or ""))

    def test_doctor_repairs_safe_duplicate_lock_entries(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            lock = repo / ".loom" / "pack" / "lock.json"
            lock.parent.mkdir(parents=True, exist_ok=True)
            sha = "a" * 64
            lock.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "packs": [
                            {
                                "id": "sample",
                                "version": "1.0.0",
                                "installed_at": "2026-01-01T00:00:00Z",
                                "files": [
                                    {
                                        "path": ".opencode/commands/pack-sample.md",
                                        "sha256": sha,
                                    },
                                    {
                                        "path": ".opencode/commands/pack-sample.md",
                                        "sha256": sha,
                                    },
                                ],
                            },
                            {
                                "id": "sample",
                                "version": "1.0.0",
                                "installed_at": "2026-01-01T00:00:00Z",
                                "files": [
                                    {
                                        "path": ".opencode/commands/pack-sample.md",
                                        "sha256": sha,
                                    }
                                ],
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )

            rc, out, err = _run_text(["doctor", "--json"], cwd=repo)

            repaired = json.loads(lock.read_text(encoding="utf-8"))

        self.assertEqual(rc, 0)
        self.assertEqual(err, "")
        payload = json.loads(out.strip())
        warnings = payload.get("warnings")
        self.assertIsInstance(warnings, list)
        self.assertGreaterEqual(len(cast(list[object], warnings)), 1)
        packs = repaired.get("packs")
        self.assertIsInstance(packs, list)
        self.assertEqual(len(cast(list[object], packs)), 1)

if __name__ == "__main__":
    unittest.main()
