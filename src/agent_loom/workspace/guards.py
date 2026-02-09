from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from agent_loom.workspace.constants import (
    REPOS_DIR,
    WORKSPACE_FILE,
    WORKTREES_DIR,
)
from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.state import (
    _is_within_dir,
    harness_manifest_path,
    validate_workspace,
    ws_repos_dir,
    ws_worktrees_dir,
)
from agent_loom.core.io import read_json


@dataclass(frozen=True)
class HarnessContext:
    root: Optional[Path]
    zone: str  # none | control_plane | managed_zone
    ws: Optional[dict] = None
    ws_error: Optional[str] = None


def harness_context(cwd: Optional[Path] = None) -> HarnessContext:
    """Classify the current directory relative to a workspace harness control plane.

    This is used ONLY for guardrails and UX checks.
    """

    cur = (cwd or Path.cwd()).resolve()
    root: Optional[Path] = None
    for parent in [cur] + list(cur.parents):
        if harness_manifest_path(parent).exists():
            root = parent
            break

    if not root:
        return HarnessContext(root=None, zone="none")

    ws: Optional[dict] = None
    ws_error: Optional[str] = None
    try:
        ws = validate_workspace(root, read_json(harness_manifest_path(root)))
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

    return HarnessContext(root=root, zone=zone, ws=ws, ws_error=ws_error)


def harness_root() -> Path:
    """Return the workspace root for `workspace harness`.

    Guardrails:
    - Require the harness manifest (the harness indicator) to avoid false-positive roots.
    - Refuse to operate from within harness-managed repos/worktrees.
    """

    cur = Path.cwd().resolve()
    ctx = harness_context(cur)
    if not ctx.root:
        # If a legacy layout is detected, provide a targeted hint.
        for parent in [cur] + list(cur.parents):
            legacy = parent / WORKSPACE_FILE
            if legacy.exists():
                raise WorkspaceError(
                    "Legacy harness layout detected. Move the manifest to "
                    f"{harness_manifest_path(parent).relative_to(parent)} and re-run. "
                    f"Found legacy file at: {legacy}"
                )
        raise WorkspaceError(
            "Not in a loom workspace harness control plane (expected "
            f"{harness_manifest_path(Path('.')).as_posix()} in this directory or a parent)."
        )
    if not ctx.ws:
        raise WorkspaceError(
            "Invalid workspace harness config at "
            f"{harness_manifest_path(ctx.root)}: {ctx.ws_error}"
        )

    root, ws = ctx.root, ctx.ws

    repos_dir = (root / ws_repos_dir(ws)).resolve()
    worktrees_dir = (root / ws_worktrees_dir(ws)).resolve()
    if _is_within_dir(cur, repos_dir) or _is_within_dir(cur, worktrees_dir):
        raise WorkspaceError(
            "Refusing to run `workspace harness` from within a harness-managed repo/worktree. "
            "Run from the harness root (or use `workspace` inside a repository)."
        )

    return root


__all__ = [
    "HarnessContext",
    "harness_context",
    "harness_root",
]
