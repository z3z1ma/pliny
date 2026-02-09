import contextlib
import importlib
import io
import json
import os
import subprocess
import tempfile
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


def test_repo_worktree_diff_json_contract() -> None:
    with tempfile.TemporaryDirectory() as td:
        repo = Path(td) / "repo"
        _git_init_repo(repo)
        _run_json(["init"], repo)
        rc, out = _run_json(["worktree", "ensure", "feat"], repo)
        assert rc == 0
        wt_path = Path(str((out.get("data") or {}).get("path") or ""))
        assert wt_path.exists()

        # Tracked change + untracked file
        (wt_path / "README.md").write_text("hello\nworld\n", encoding="utf-8")
        (wt_path / "UNTRACKED.txt").write_text("x\n", encoding="utf-8")

        rc2, out2 = _run_json(
            [
                "worktree",
                "diff",
                "--worktree",
                str(wt_path),
                "--max-bytes",
                "2000000",
            ],
            repo,
        )
        assert rc2 == 0
        assert out2.get("ok") is True
        data = out2.get("data") or {}
        files = data.get("files") or []
        assert files
        patch = (files[0] or {}).get("patch") or ""
        assert "diff --git a/README.md b/README.md" in patch
        assert "UNTRACKED.txt" in (data.get("untracked") or [])


def test_harness_worktree_group_diff_json_contract() -> None:
    with tempfile.TemporaryDirectory() as td:
        ws_root = Path(td) / "ws"
        ws_root.mkdir(parents=True, exist_ok=True)
        _run_json(["harness", "init"], ws_root)

        remotes = ws_root / "_remotes"
        r1 = remotes / "one"
        _git_init_repo(r1)
        _run_json(["harness", "add", "one", str(r1), "--clone"], ws_root)

        _run_json(["harness", "worktree", "ensure", "g1", "--all"], ws_root)

        wt_repo = ws_root / ".loom" / "workspaces" / "worktrees" / "g1" / "one"
        assert wt_repo.exists()
        (wt_repo / "README.md").write_text("hello\nharness\n", encoding="utf-8")

        rc, out = _run_json(
            [
                "harness",
                "worktree",
                "diff",
                "g1",
                "--repos",
                "one",
            ],
            ws_root,
        )
        assert rc == 0
        assert out.get("ok") is True
        res = (out.get("data") or {}).get("results") or []
        assert res
        row = res[0]
        assert row.get("repo") == "one"
        assert row.get("status") == "ok"
        files = row.get("files") or []
        assert files
        assert "diff --git a/README.md b/README.md" in (files[0] or {}).get("patch", "")
