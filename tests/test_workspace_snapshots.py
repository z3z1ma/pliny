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
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=path, check=True
    )
    subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)
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


class TestWorkspaceSnapshots(unittest.TestCase):
    def test_snapshot_diff_and_restore_on_repos(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)

            # Init poly workspace
            rc0, out0 = _run_json(["poly", "init"], ws_root)
            self.assertEqual(rc0, 0)
            self.assertTrue(out0.get("ok"))

            # Create local remotes
            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            r2 = remotes / "two"
            _git_init_repo(r1)
            _git_init_repo(r2)

            # Add and clone into workspace
            rc1, out1 = _run_json(["poly", "add", "one", str(r1), "--clone"], ws_root)
            self.assertEqual(rc1, 0)
            self.assertTrue(out1.get("ok"))

            rc2, out2 = _run_json(["poly", "add", "two", str(r2), "--clone"], ws_root)
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))

            # Snapshot capture
            rc3, out3 = _run_json(
                ["poly", "snapshot", "capture", "s1", "--all"], ws_root
            )
            self.assertEqual(rc3, 0)
            self.assertTrue(out3.get("ok"))
            snap_path = Path((out3.get("data") or {}).get("snapshot_path") or "")
            self.assertTrue(snap_path.exists())

            # Mutate one repo clone
            clone_one = ws_root / "repos" / "one"
            _ = _git_commit(clone_one, "change")

            # Diff should show changed=1
            rc4, out4 = _run_json(["poly", "snapshot", "diff", "s1"], ws_root)
            self.assertEqual(rc4, 0)
            self.assertTrue(out4.get("ok"))
            summary = (out4.get("data") or {}).get("summary") or {}
            self.assertEqual(int(summary.get("changed") or 0), 1)

            # Restore should reset to snapshot
            rc5, out5 = _run_json(
                ["poly", "snapshot", "restore", "s1", "--yes", "--force-clean"],
                ws_root,
            )
            self.assertEqual(rc5, 0)
            self.assertTrue(out5.get("ok"))

            rc6, out6 = _run_json(["poly", "snapshot", "diff", "s1"], ws_root)
            self.assertEqual(rc6, 0)
            summary2 = (out6.get("data") or {}).get("summary") or {}
            self.assertEqual(int(summary2.get("changed") or 0), 0)
