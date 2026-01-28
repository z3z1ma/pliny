from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from agent_loom.workspace.constants import REPO_INTERNAL_DIR
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.repo_ops import repo_root, repo_worktree_ensure
from agent_loom.workspace.utils import now_iso, run
from agent_loom.workspace.worktree_meta import repo_worktree_annotate


def _default_sandbox_name() -> str:
    # now_iso is like 2026-02-01T12:34:56Z
    s = now_iso()
    s = re.sub(r"[^0-9A-Za-z]+", "", s)
    return s or "sandbox"


def repo_sandbox_create(
    *,
    base_ref: str,
    name: str = "",
    ttl: str = "2h",
    purpose: str = "sandbox",
    root: Optional[Path] = None,
) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    base = str(base_ref or "").strip()
    if not base:
        raise WorkspaceError("Missing --base")

    sand = str(name or "").strip() or _default_sandbox_name()
    branch = f"sandbox/{sand}"
    rel = Path(REPO_INTERNAL_DIR) / "worktrees" / "sandbox" / sand
    wt = repo_worktree_ensure(branch=branch, path=str(rel), base_ref=base, root=repo)

    meta = repo_worktree_annotate(
        repo_root=repo,
        branch=branch,
        purpose=purpose,
        ttl=ttl,
        kind="sandbox",
    )
    return {"branch": branch, "path": wt.path, **meta}


def repo_sandbox_promote(
    *,
    from_branch: str,
    to_branch: str,
    root: Optional[Path] = None,
) -> dict:
    repo = root.resolve() if root is not None else repo_root()
    src = str(from_branch or "").strip()
    dst = str(to_branch or "").strip()
    if not src or not dst:
        raise WorkspaceError("Missing --from or --to")

    run(["git", "branch", "-m", src, dst], cwd=repo)

    # Rewrite metadata from src -> dst if present.
    try:
        from agent_loom.workspace.worktree_meta import repo_worktree_meta_path
        from agent_loom.workspace.utils import atomic_write_json, read_json

        srcp = repo_worktree_meta_path(repo, src)
        dstp = repo_worktree_meta_path(repo, dst)
        if srcp.exists():
            data = read_json(srcp)
            if isinstance(data, dict):
                data["branch"] = dst
                data["kind"] = "normal"
                data.pop("ttl_seconds", None)
                dstp.parent.mkdir(parents=True, exist_ok=True)
                atomic_write_json(dstp, data)
            srcp.unlink()
    except Exception:
        pass

    return {"from": src, "to": dst, "promoted": True}


def repo_sandbox_gc(
    *, confirm: bool, force: bool = False, root: Optional[Path] = None
) -> dict:
    if not confirm:
        raise WorkspaceError("Refusing to gc sandboxes without --yes")

    from agent_loom.workspace.cleanup_ops import (
        repo_worktree_cleanup_apply,
        repo_worktree_cleanup_suggest,
    )

    repo = root.resolve() if root is not None else repo_root()
    sug = repo_worktree_cleanup_suggest(root=repo)
    ids = [
        c.get("id")
        for c in (sug.get("candidates") or [])
        if str(c.get("id") or "").startswith("sandbox/")
    ]
    ids = [str(x) for x in ids if str(x).strip()]
    if not ids:
        return {"repo_root": str(repo.resolve()), "removed": [], "skipped": []}
    return repo_worktree_cleanup_apply(
        ids=ids, confirm=True, force=bool(force), root=repo
    )
