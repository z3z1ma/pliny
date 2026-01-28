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


class TestWorkspaceLeasesGc(unittest.TestCase):
    def test_worktree_gc_skips_claimed_groups(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)
            _run_json(["poly", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)

            _run_json(["poly", "add", "one", str(r1), "--clone"], ws_root)

            _run_json(["poly", "worktree", "add", "g1", "--all"], ws_root)
            _run_json(["poly", "worktree", "add", "g2", "--all"], ws_root)

            # Claim g1
            rc1, out1 = _run_json(["poly", "lease", "acquire", "group:g1"], ws_root)
            self.assertEqual(rc1, 0)
            self.assertTrue(out1.get("ok"))

            # GC unclaimed only should remove g2's worktree but skip g1.
            rc2, out2 = _run_json(
                ["poly", "worktree", "gc", "--unclaimed-only", "--yes"],
                ws_root,
            )
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))

            wt_g1 = ws_root / "worktrees" / "g1" / "one"
            wt_g2 = ws_root / "worktrees" / "g2" / "one"
            self.assertTrue(wt_g1.exists())
            self.assertFalse(wt_g2.exists())
