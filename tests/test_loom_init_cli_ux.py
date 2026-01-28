import io
import json
import os
import subprocess
import tempfile
import unittest
import contextlib
import sys
from pathlib import Path


import agent_loom.cli as loom


def _git_init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True)


def _run_root_json(argv: list[str], *, cwd: Path) -> tuple[int, dict]:
    out = io.StringIO()
    err = io.StringIO()
    old = Path.cwd()
    try:
        os.chdir(cwd)
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = int(loom.main(argv))
    finally:
        os.chdir(old)
    payload = out.getvalue().strip()
    return rc, (json.loads(payload) if payload else {})


class _TtyStdin(io.StringIO):
    def isatty(self) -> bool:  # type: ignore[override]
        return True


class TestLoomInitCliUx(unittest.TestCase):
    def test_root_help_mentions_init(self) -> None:
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = int(loom.main(["--help"]))
        self.assertEqual(rc, 0)
        self.assertIn("init", err.getvalue())

    def test_init_yes_json_in_git_repo_initializes_everything(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            _git_init_repo(root)

            rc, payload = _run_root_json(
                ["init", "--yes", "--json", "--workspace-mode", "repo"],
                cwd=root,
            )
            self.assertEqual(rc, 0)
            self.assertTrue(bool(payload.get("ok")))
            self.assertEqual(str(payload.get("cmd") or ""), "init")
            self.assertTrue(bool(payload.get("git", {}).get("ok")))

            self.assertTrue((root / ".loom-repo" / "worktrees").exists())
            self.assertTrue((root / ".tickets").exists())
            self.assertTrue((root / ".memory" / "meta.json").exists())
            self.assertTrue((root / ".opencode").exists())
            self.assertTrue((root / ".opencode" / "agents").exists())
            self.assertTrue((root / ".claude" / "agents").exists())

    def test_init_yes_json_outside_git_skips_team(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rc, payload = _run_root_json(
                ["init", "--yes", "--json", "--workspace-mode", "poly"],
                cwd=root,
            )
            self.assertEqual(rc, 0)
            self.assertTrue(bool(payload.get("ok")))
            self.assertFalse(bool(payload.get("git", {}).get("ok")))

            self.assertTrue((root / "workspace.json").exists())
            self.assertTrue((root / ".tickets").exists())
            self.assertTrue((root / ".memory" / "meta.json").exists())
            self.assertTrue((root / ".opencode").exists())

            selected = payload.get("selected") or {}
            self.assertFalse(bool(selected.get("team")))

    def test_interactive_path_completes_with_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            _git_init_repo(root)

            out = io.StringIO()
            err = io.StringIO()
            old = Path.cwd()
            old_stdin = sys.stdin
            try:
                os.chdir(root)
                sys.stdin = _TtyStdin("\n" * 7)
                with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                    rc = int(loom.main(["init"]))
            finally:
                sys.stdin = old_stdin
                os.chdir(old)
            self.assertEqual(rc, 0)
