import contextlib
import importlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Callable, cast


workspace_cli_mod = importlib.import_module("agent_loom.workspace.cli")
workspace_cli = cast(Callable[[list[str]], int], getattr(workspace_cli_mod, "main"))


def _run_text(argv: list[str], cwd: Path) -> tuple[int, str]:
    buf = io.StringIO()
    old = Path.cwd()
    try:
        os.chdir(cwd)
        with contextlib.redirect_stdout(buf):
            rc = int(workspace_cli(argv))
    finally:
        os.chdir(old)
    return rc, buf.getvalue()


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


class TestWorkspaceCliUx(unittest.TestCase):
    def test_prime_prints_cookbook(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            rc, text = _run_text(["prime"], Path(td))
            self.assertEqual(rc, 0)
            self.assertIn("Workspace Cookbook", text)
            self.assertIn("loom workspace poly init", text)

    def test_prime_json_includes_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            rc, payload = _run_json(["prime"], Path(td))
            self.assertEqual(rc, 0)
            self.assertTrue(payload.get("ok"))
            data = payload.get("data") or {}
            content = str(data.get("markdown") or "")
            self.assertIn("Workspace Cookbook", content)


if __name__ == "__main__":
    unittest.main()
