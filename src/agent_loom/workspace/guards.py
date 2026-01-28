from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from agent_loom.workspace.constants import (
    INTERNAL_DIR,
    REPOS_DIR,
    WORKSPACE_FILE,
    WORKTREES_DIR,
)
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.state import (
    _is_within_dir,
    validate_workspace,
    ws_repos_dir,
    ws_worktrees_dir,
)
from agent_loom.workspace.utils import read_json


@dataclass(frozen=True)
class PolyContext:
    root: Optional[Path]
    zone: str  # none | control_plane | managed_zone
    ws: Optional[dict] = None
    ws_error: Optional[str] = None


def poly_context(cwd: Optional[Path] = None) -> PolyContext:
    """Classify the current directory relative to a workspace poly control plane.

    This is used ONLY for guardrails and UX checks.
    """

    cur = (cwd or Path.cwd()).resolve()
    root: Optional[Path] = None
    for parent in [cur] + list(cur.parents):
        if (parent / WORKSPACE_FILE).exists() and (parent / INTERNAL_DIR).exists():
            root = parent
            break

    if not root:
        return PolyContext(root=None, zone="none")

    ws: Optional[dict] = None
    ws_error: Optional[str] = None
    try:
        ws = validate_workspace(root, read_json(root / WORKSPACE_FILE))
    except Exception as e:
        ws_error = str(e)

    # If the workspace config is invalid/unreadable, fall back to defaults to
    # conservatively approximate the managed zone.
    repos_rel = ws_repos_dir(ws) if ws else REPOS_DIR
    worktrees_rel = ws_worktrees_dir(ws) if ws else WORKTREES_DIR
    repos_dir = (root / repos_rel).resolve()
    worktrees_dir = (root / worktrees_rel).resolve()

    zone = "control_plane"
    if _is_within_dir(cur, repos_dir) or _is_within_dir(cur, worktrees_dir):
        zone = "managed_zone"

    return PolyContext(root=root, zone=zone, ws=ws, ws_error=ws_error)


def workspace_root() -> Path:
    """Return the workspace root for `workspace poly`.

    Guardrails:
    - Require BOTH `workspace.json` and `.loom/` to avoid false-positive roots.
    - Refuse to operate from within poly-managed repos/worktrees.
    """

    cur = Path.cwd().resolve()
    ctx = poly_context(cur)
    if not ctx.root:
        raise WorkspaceError(
            f"Not in a loom workspace poly control plane (expected {WORKSPACE_FILE} + {INTERNAL_DIR}/ in this directory or a parent)."
        )
    if not ctx.ws:
        raise WorkspaceError(
            f"Invalid loom-repos poly workspace config at {ctx.root / WORKSPACE_FILE}: {ctx.ws_error}"
        )

    root, ws = ctx.root, ctx.ws

    repos_dir = (root / ws_repos_dir(ws)).resolve()
    worktrees_dir = (root / ws_worktrees_dir(ws)).resolve()
    if _is_within_dir(cur, repos_dir) or _is_within_dir(cur, worktrees_dir):
        raise WorkspaceError(
            "Refusing to run `workspace poly` from within a poly-managed repo/worktree. "
            "Run from the workspace root (or use `workspace` inside a repository)."
        )

    return root
