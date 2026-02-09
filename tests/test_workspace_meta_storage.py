import tempfile
import unittest
from pathlib import Path


from agent_loom.core.fs import fs_escape
from agent_loom.workspace.worktree_meta import (
    harness_group_annotate,
    repo_worktree_annotate,
)


class TestWorkspaceMetaStorage(unittest.TestCase):
    def test_repo_worktree_meta_writes_under_meta_dir(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            repo.mkdir(parents=True, exist_ok=True)
            branch = "feature/one"

            res = repo_worktree_annotate(
                repo_root=repo,
                branch=branch,
                purpose="test",
                ttl="1d",
            )
            meta_path = Path(str(res.get("meta_path") or "")).resolve()
            self.assertTrue(meta_path.exists())
            self.assertIn(
                str(repo / ".loom" / "workspace" / "meta" / "worktrees"),
                str(meta_path),
            )

            old = (
                repo / ".loom" / "workspace" / "worktrees" / f"{fs_escape(branch)}.json"
            )
            self.assertFalse(old.exists())

    def test_harness_group_meta_writes_under_meta_dir(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = Path(td) / "ws"
            ws.mkdir(parents=True, exist_ok=True)
            group = "g/one"

            res = harness_group_annotate(
                ws_root=ws,
                group=group,
                purpose="test",
                ttl="1d",
            )
            meta_path = Path(str(res.get("meta_path") or "")).resolve()
            self.assertTrue(meta_path.exists())
            self.assertIn(
                str(ws / ".loom" / "workspaces" / "meta" / "groups"),
                str(meta_path),
            )

            old = ws / ".loom" / "workspace" / "worktrees" / f"{fs_escape(group)}.json"
            self.assertFalse(old.exists())


if __name__ == "__main__":
    unittest.main()
