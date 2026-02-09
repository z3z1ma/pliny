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


class TestWorkspaceMetadata(unittest.TestCase):
    def test_repo_edit_and_set_upsert(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)

            rc0, out0 = _run_json(["harness", "init"], ws_root)
            self.assertEqual(rc0, 0)
            self.assertTrue(out0.get("ok"))

            # Add a repo entry without cloning
            rc1, out1 = _run_json(
                [
                    "harness",
                    "add",
                    "svc",
                    "file:///tmp/does-not-need-to-exist",
                    "--force",
                ],
                ws_root,
            )
            self.assertEqual(rc1, 0)
            self.assertTrue(out1.get("ok"))

            rc2, out2 = _run_json(
                [
                    "harness",
                    "repo",
                    "edit",
                    "svc",
                    "--description",
                    "Service A",
                    "--add-tag",
                    "core",
                ],
                ws_root,
            )
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))
            entry = (out2.get("data") or {}).get("entry") or {}
            self.assertEqual(str(entry.get("description") or ""), "Service A")
            self.assertIn("core", entry.get("tags") or [])

            rc3, out3 = _run_json(
                ["harness", "set", "upsert", "backend", "svc"],
                ws_root,
            )
            self.assertEqual(rc3, 0)
            self.assertTrue(out3.get("ok"))

            rc4, out4 = _run_json(["harness", "set", "show", "backend"], ws_root)
            self.assertEqual(rc4, 0)
            self.assertEqual((out4.get("data") or {}).get("items"), ["svc"])
