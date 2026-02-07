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


class TestWorkspaceWorktreeParity(unittest.TestCase):
    def test_repo_worktree_ensure_defaults_path(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            _git_init_repo(repo)

            rc, out = _run_json(["init"], repo)
            self.assertEqual(rc, 0)
            self.assertTrue(out.get("ok"))

            rc2, out2 = _run_json(["worktree", "ensure", "feat"], repo)
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))
            data = out2.get("data") or {}
            wt_path = Path(str(data.get("path") or ""))
            self.assertTrue(wt_path.exists())
            self.assertTrue((wt_path / ".git").exists())

    def test_poly_worktree_ensure_alias_exists(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)
            _run_json(["poly", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)
            _run_json(["poly", "add", "one", str(r1), "--clone"], ws_root)

            rc, out = _run_json(
                ["poly", "worktree", "ensure", "g1", "--all"],
                ws_root,
            )
            self.assertEqual(rc, 0)
            self.assertTrue(out.get("ok"))

    def test_harness_worktree_add_accepts_path_override(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)
            _run_json(["harness", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)
            _run_json(["harness", "add", "one", str(r1), "--clone"], ws_root)

            base = ws_root / "_custom_worktrees" / "g1"
            rc1, out1 = _run_json(
                ["harness", "worktree", "add", "g1", "--all", "--path", str(base)],
                ws_root,
            )
            self.assertEqual(rc1, 0)
            self.assertTrue(out1.get("ok"))

            wt = base / "one"
            self.assertTrue(wt.exists())
            self.assertTrue((wt / ".git").exists())

            # Group status should resolve the overridden base path.
            rc2, out2 = _run_json(
                ["harness", "worktree", "status", "g1", "--all"], ws_root
            )
            self.assertEqual(rc2, 0)
            data2 = out2.get("data") or {}
            rows = data2.get("worktrees") or []
            self.assertTrue(bool(rows))
            self.assertEqual(str((rows[0] or {}).get("path") or ""), str(wt.resolve()))
