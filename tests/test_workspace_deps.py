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


class TestWorkspaceDeps(unittest.TestCase):
    def test_deps_closure_and_impacted(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)

            _run_json(["poly", "init"], ws_root)
            _run_json(
                ["poly", "add", "a", "file:///tmp/a"],
                ws_root,
            )
            _run_json(
                ["poly", "add", "b", "file:///tmp/b"],
                ws_root,
            )

            # Edit service metadata for deps
            svc_a = ws_root / "services" / "a.md"
            text = svc_a.read_text(encoding="utf-8")
            # Put a single dependency under 'Depends on'
            text = text.replace("- (list other service repo names)", "- b")
            svc_a.write_text(text, encoding="utf-8")

            _run_json(["poly", "services", "refresh-index"], ws_root)

            rc1, out1 = _run_json(["poly", "deps", "closure", "a"], ws_root)
            self.assertEqual(rc1, 0)
            data = out1.get("data") or {}
            self.assertIn("b", data.get("depends_on_transitive") or [])

            rc2, out2 = _run_json(["poly", "deps", "impacted", "b"], ws_root)
            self.assertEqual(rc2, 0)
            data2 = out2.get("data") or {}
            self.assertIn("a", data2.get("impacted") or [])
