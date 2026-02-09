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
            _run_json(["harness", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)

            _run_json(["harness", "add", "one", str(r1), "--clone"], ws_root)

            _run_json(["harness", "worktree", "add", "g1", "--all"], ws_root)
            _run_json(["harness", "worktree", "add", "g2", "--all"], ws_root)

            # Claim g1
            rc1, out1 = _run_json(["harness", "lease", "acquire", "group:g1"], ws_root)
            self.assertEqual(rc1, 0)
            self.assertTrue(out1.get("ok"))

            # GC skip-leased should remove g2's worktree but skip g1.
            rc2, out2 = _run_json(
                ["harness", "worktree", "gc", "--skip-leased", "--yes"],
                ws_root,
            )
            self.assertEqual(rc2, 0)
            self.assertTrue(out2.get("ok"))

            wt_g1 = ws_root / ".loom" / "workspaces" / "worktrees" / "g1" / "one"
            wt_g2 = ws_root / ".loom" / "workspaces" / "worktrees" / "g2" / "one"
            self.assertTrue(wt_g1.exists())
            self.assertFalse(wt_g2.exists())

    def test_expired_lease_is_pruned_and_does_not_block_gc(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)
            _run_json(["harness", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)
            _run_json(["harness", "add", "one", str(r1), "--clone"], ws_root)

            _run_json(["harness", "worktree", "add", "g1", "--all"], ws_root)

            # Acquire a lease, then backdate it so it is expired.
            _run_json(
                ["harness", "lease", "acquire", "group:g1", "--ttl", "1s"], ws_root
            )
            leases_dir = ws_root / ".loom" / "workspaces" / "leases"
            lease_files = list(leases_dir.glob("*.json"))
            self.assertTrue(bool(lease_files))

            target = None
            for p in lease_files:
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    continue
                if isinstance(data, dict) and data.get("key") == "group:g1":
                    target = p
                    data["ttl_seconds"] = 1
                    data["updated_at"] = "2000-01-01T00:00:00Z"
                    p.write_text(
                        json.dumps(data, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8",
                    )
                    break
            self.assertIsNotNone(target)

            rc_ls, out_ls = _run_json(["harness", "lease", "ls"], ws_root)
            self.assertEqual(rc_ls, 0)
            data_ls = out_ls.get("data") or {}
            self.assertEqual(int(data_ls.get("pruned_expired") or 0), 1)

            # GC skip-leased should now remove g1 (since lease was pruned).
            rc_gc, out_gc = _run_json(
                ["harness", "worktree", "gc", "--skip-leased", "--yes"],
                ws_root,
            )
            self.assertEqual(rc_gc, 0)
            self.assertTrue(out_gc.get("ok"))
            wt_g1 = ws_root / ".loom" / "workspaces" / "worktrees" / "g1" / "one"
            self.assertFalse(wt_g1.exists())

    def test_require_lease_blocks_worktree_rm(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws_root = Path(td) / "ws"
            ws_root.mkdir(parents=True, exist_ok=True)
            _run_json(["harness", "init"], ws_root)

            remotes = ws_root / "_remotes"
            r1 = remotes / "one"
            _git_init_repo(r1)
            _run_json(["harness", "add", "one", str(r1), "--clone"], ws_root)

            _run_json(["harness", "worktree", "add", "g1", "--all"], ws_root)
            wt_g1 = ws_root / ".loom" / "workspaces" / "worktrees" / "g1" / "one"
            self.assertTrue(wt_g1.exists())

            # Without the lease, --require-lease should fail and not delete.
            rc, out = _run_json(
                [
                    "harness",
                    "worktree",
                    "rm",
                    "g1",
                    "--all",
                    "--yes",
                    "--require-lease",
                    "group:g1",
                ],
                ws_root,
            )
            self.assertEqual(rc, 2)
            self.assertFalse(bool(out.get("ok")))
            self.assertTrue(wt_g1.exists())
