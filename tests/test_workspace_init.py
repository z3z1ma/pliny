import contextlib
import importlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast


workspace_cli_mod = importlib.import_module("agent_loom.workspace.cli")
workspace_cli = cast(Callable[[list[str]], int], getattr(workspace_cli_mod, "main"))


def _run_json(argv: list[str], cwd: Path) -> tuple[int, dict]:
    buf = io.StringIO()
    old = Path.cwd()
    try:
        os.chdir(cwd)
        with contextlib.redirect_stdout(buf):
            rc = int(workspace_cli(["--json"] + argv))
    finally:
        os.chdir(old)
    payload = buf.getvalue().strip()
    return rc, (json.loads(payload) if payload else {})


def _git_init_repo(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-b", "main"], cwd=path, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=path, check=True
    )
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)
    (path / "README.md").write_text("hello\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=path, check=True)


class TestWorkspaceInit(unittest.TestCase):
    def test_harness_init_is_idempotent_and_updates_gitignore(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rc1, out1 = _run_json(["harness", "init"], root)
            self.assertEqual(rc1, 0)
            self.assertTrue(out1.get("ok"))

            gi = root / ".gitignore"
            self.assertTrue(gi.exists())
            text1 = gi.read_text(encoding="utf-8")
            self.assertIn(".loom/workspaces/repos/", text1)
            self.assertIn(".loom/workspaces/worktrees/", text1)
            self.assertIn(".loom/workspaces/states/", text1)
            self.assertIn(".loom/workspaces/components/index.json", text1)

            # Re-run should not duplicate baseline lines.
            rc2, out2 = _run_json(["harness", "init"], root)
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))
            text2 = gi.read_text(encoding="utf-8")
            self.assertEqual(text2.count(".loom/workspaces/repos/"), 1)
            self.assertEqual(text2.count(".loom/workspaces/worktrees/"), 1)
            self.assertEqual(text2.count(".loom/workspaces/states/"), 1)
            self.assertEqual(text2.count(".loom/workspaces/components/index.json"), 1)

    def test_harness_init_root_flag_initializes_target_dir(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            cwd = base / "cwd"
            target = base / "harness"
            cwd.mkdir(parents=True, exist_ok=True)

            rc, out = _run_json(["harness", "init", "--root", str(target)], cwd)
            self.assertEqual(rc, 0)
            self.assertTrue(out.get("ok"))
            self.assertTrue(
                (target / ".loom" / "workspaces" / "workspace.json").exists()
            )
            self.assertTrue((target / ".loom").exists())
            self.assertFalse((cwd / "workspace.json").exists())

    def test_workspace_init_in_git_repo_runs_repo_init(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            _git_init_repo(repo)
            rc, out = _run_json(["init"], repo)
            self.assertEqual(rc, 0)
            self.assertTrue(out.get("ok"))
            data = out.get("data") or {}
            self.assertIn(".loom/workspace", str(data.get("internal_dir") or ""))
            self.assertTrue((repo / ".loom" / "workspace" / "worktrees").exists())

            # Ensure ignore was written to .git/info/exclude
            exclude = repo / ".git" / "info" / "exclude"
            self.assertTrue(exclude.exists())
            self.assertIn(".loom/workspace/", exclude.read_text(encoding="utf-8"))

    def test_no_implicit_dispatch_from_harness_root(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rc0, out0 = _run_json(["harness", "init"], root)
            self.assertEqual(rc0, 0)
            self.assertTrue(out0.get("ok"))

            # `loom workspace status` is repo-local and should not behave like harness.
            rc1, out1 = _run_json(["status"], root)
            self.assertEqual(rc1, 2)
            self.assertFalse(bool(out1.get("ok")))
