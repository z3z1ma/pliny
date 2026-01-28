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


def _git_commit(path: Path, msg: str) -> str:
    (path / "x.txt").write_text(msg + "\n", encoding="utf-8")
    subprocess.run(["git", "add", "x.txt"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-m", msg], cwd=path, check=True)
    out = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=path,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return out.stdout.strip()


class TestWorkspaceRepoSnapshots(unittest.TestCase):
    def test_repo_snapshot_capture_diff_restore(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            _git_init_repo(repo)
            _run_json(["init"], repo)

            # Create a branch worktree
            rc1, out1 = _run_json(["worktree", "ensure", "feat"], repo)
            self.assertEqual(rc1, 0)
            wt_path = Path(str((out1.get("data") or {}).get("path") or ""))
            self.assertTrue(wt_path.exists())

            # Capture snapshot on that worktree
            rc2, out2 = _run_json(
                ["snapshot", "capture", "s1", "--worktree", str(wt_path)],
                repo,
            )
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))

            # Mutate worktree
            _git_commit(wt_path, "change")

            rc3, out3 = _run_json(["snapshot", "diff", "s1"], repo)
            self.assertEqual(rc3, 0)
            data3 = out3.get("data") or {}
            self.assertFalse(bool(data3.get("ok")))

            rc4, out4 = _run_json(
                ["snapshot", "restore", "s1", "--yes", "--force-clean"],
                repo,
            )
            self.assertEqual(rc4, 0)
            self.assertTrue(out4.get("ok"))

            rc5, out5 = _run_json(["snapshot", "diff", "s1"], repo)
            self.assertEqual(rc5, 0)
            self.assertTrue(bool((out5.get("data") or {}).get("ok")))
