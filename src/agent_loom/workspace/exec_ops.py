from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.git_ops import git_is_dirty, require_git
from agent_loom.workspace.guards import workspace_root
from agent_loom.workspace.models import PolyExecResult
from agent_loom.workspace.selection import poly_resolve_repo_names
from agent_loom.workspace.state import (
    iter_repos,
    load_workspace,
    worktrees_base,
    ws_repos_dir,
)
from agent_loom.workspace.utils import is_git_repo, run


def _truncate(s: str, *, max_chars: int) -> tuple[str, bool]:
    if len(s) <= max_chars:
        return s, False
    return s[:max_chars] + "\n...<truncated>\n", True


def poly_exec(
    *,
    cmd: Sequence[str],
    group: Optional[str] = None,
    repos: Optional[Sequence[str]] = None,
    sets: Optional[Sequence[str]] = None,
    tags: Optional[Sequence[str]] = None,
    allow_all: bool = False,
    jobs: int = 1,
    require_clean: bool = False,
    max_output_chars: int = 4000,
    root: Optional[Path] = None,
) -> PolyExecResult:
    require_git()
    ws_root = root.resolve() if root is not None else workspace_root()
    ws = load_workspace(ws_root)
    repo_map = iter_repos(ws)

    argv = [str(x) for x in cmd if str(x).strip()]
    if not argv:
        raise WorkspaceError(
            "Missing command (use: loom workspace poly exec -- <cmd...>)"
        )

    names = poly_resolve_repo_names(
        ws,
        repo_map,
        repo_names=repos,
        sets=sets,
        tags=tags,
        require_intent_for_multi=True,
        allow_all=allow_all,
    )

    target: dict[str, Any] = {"kind": "repos"}
    base = (ws_root / ws_repos_dir(ws)).resolve()
    if group:
        target = {"kind": "worktrees", "group": str(group)}
        base = worktrees_base(ws_root, ws, str(group)).resolve()

    def _one(repo_name: str) -> Dict[str, Any]:
        p = (base / repo_name).resolve()
        rec: Dict[str, Any] = {
            "repo": repo_name,
            "path": str(p),
            "status": "unknown",
        }

        if not p.exists():
            rec.update({"status": "skip", "reason": "not_found"})
            return rec
        if not is_git_repo(p):
            rec.update({"status": "skip", "reason": "not_a_repo"})
            return rec
        if require_clean and git_is_dirty(p):
            rec.update({"status": "skip", "reason": "dirty"})
            return rec

        start = time.monotonic()
        proc = run(list(argv), cwd=p, check=False)
        dur_ms = int((time.monotonic() - start) * 1000)

        stdout, stdout_trunc = _truncate(proc.stdout or "", max_chars=max_output_chars)
        stderr, stderr_trunc = _truncate(proc.stderr or "", max_chars=max_output_chars)

        rec.update(
            {
                "status": "success" if proc.returncode == 0 else "fail",
                "exit_code": int(proc.returncode),
                "duration_ms": dur_ms,
                "stdout": stdout,
                "stderr": stderr,
                "stdout_truncated": bool(stdout_trunc),
                "stderr_truncated": bool(stderr_trunc),
            }
        )
        return rec

    # Keep ordering deterministic.
    from agent_loom.workspace.utils import parallel_map

    results = parallel_map(_one, names, int(jobs or 1))

    summary = {
        "repos": len(results),
        "success": sum(1 for r in results if r.get("status") == "success"),
        "fail": sum(1 for r in results if r.get("status") == "fail"),
        "skip": sum(1 for r in results if r.get("status") == "skip"),
    }
    return PolyExecResult(
        cmd=list(argv), target=target, results=results, summary=summary
    )
