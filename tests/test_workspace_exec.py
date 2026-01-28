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


class TestWorkspaceExec(unittest.TestCase):
    def test_poly_exec_runs_command_in_each_repo(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)

            rc0, out0 = _run_json(["poly", "init"], ws_root)
            self.assertEqual(rc0, 0)
            self.assertTrue(out0.get("ok"))

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            r2 = remotes / "two"
            _git_init_repo(r1)
            _git_init_repo(r2)

            _run_json(["poly", "add", "one", str(r1), "--clone"], ws_root)
            _run_json(["poly", "add", "two", str(r2), "--clone"], ws_root)

            # Use a stable git command
            rc, out = _run_json(
                [
                    "poly",
                    "exec",
                    "--all",
                    "--",
                    "git",
                    "rev-parse",
                    "--is-inside-work-tree",
                ],
                ws_root,
            )
            self.assertEqual(rc, 0)
            self.assertTrue(out.get("ok"))
            data = out.get("data") or {}
            summary = data.get("summary") or {}
            self.assertEqual(int(summary.get("success") or 0), 2)
