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


class TestWorkspaceHarnessCleanupTtl(unittest.TestCase):
    def test_ttl_cleanup_skips_claimed_groups(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)
            _run_json(["harness", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)

            _run_json(["harness", "add", "one", str(r1), "--clone"], ws_root)
            _run_json(["harness", "worktree", "add", "g1", "--all"], ws_root)
            _run_json(["harness", "worktree", "add", "g2", "--all"], ws_root)

            _run_json(
                [
                    "harness",
                    "worktree",
                    "annotate",
                    "g1",
                    "--purpose",
                    "t",
                    "--ttl",
                    "1s",
                ],
                ws_root,
            )
            _run_json(
                [
                    "harness",
                    "worktree",
                    "annotate",
                    "g2",
                    "--purpose",
                    "t",
                    "--ttl",
                    "1s",
                ],
                ws_root,
            )

            # Force expiry by backdating last_used_at.
            for g in ("g1", "g2"):
                p = ws_root / ".loom" / "workspaces" / "meta" / "groups" / f"{g}.json"
                meta = json.loads(p.read_text(encoding="utf-8"))
                meta["last_used_at"] = "2000-01-01T00:00:00Z"
                p.write_text(
                    json.dumps(meta, indent=2, sort_keys=True) + "\n", encoding="utf-8"
                )

            # Lease g1.
            _run_json(["harness", "lease", "acquire", "group:g1"], ws_root)

            rc, out = _run_json(
                [
                    "harness",
                    "cleanup",
                    "apply",
                    "--id",
                    "g1",
                    "--id",
                    "g2",
                    "--yes",
                ],
                ws_root,
            )
            self.assertEqual(rc, 0)
            self.assertTrue(out.get("ok"))

            # g1 remains, g2 removed.
            self.assertTrue(
                (ws_root / ".loom" / "workspaces" / "worktrees" / "g1" / "one").exists()
            )
            self.assertFalse(
                (ws_root / ".loom" / "workspaces" / "worktrees" / "g2" / "one").exists()
            )

            # g2 meta removed, g1 meta remains.
            self.assertTrue(
                (
                    ws_root / ".loom" / "workspaces" / "meta" / "groups" / "g1.json"
                ).exists()
            )
            self.assertFalse(
                (
                    ws_root / ".loom" / "workspaces" / "meta" / "groups" / "g2.json"
                ).exists()
            )


if __name__ == "__main__":
    unittest.main()
