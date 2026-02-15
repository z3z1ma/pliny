from __future__ import annotations

import argparse
from pathlib import Path

from agent_loom.workspace.core import (
    lease_require_active,
    worktree_add,
    worktree_gc,
    worktree_group_check_clean,
    worktree_group_check_divergence,
    worktree_group_diff,
    worktree_group_status,
    worktree_ls,
    worktree_prune,
    worktree_push,
    worktree_rebase,
    worktree_rm,
)
from agent_loom.workspace.guards import harness_root

workspace_root = harness_root


def emit_result(args: argparse.Namespace, root: Path, result: object) -> None:
    from agent_loom.workspace.cli import emit_result as _emit_result

    _emit_result(args, root, result)


def cmd_worktree_add(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_add(
        group=args.group,
        base_ref=args.base_ref,
        path=str(getattr(args, "path", "") or "").strip() or None,
        clone=bool(args.clone),
        allow_dirty=bool(args.allow_dirty),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_rm(args: argparse.Namespace) -> None:
    root = workspace_root()
    req = str(getattr(args, "require_lease", "") or "").strip()
    if req:
        lease_require_active(key=req, root=root)
    res = worktree_rm(
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_ls(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_ls(root=root)
    emit_result(args, root, res)


def cmd_worktree_prune(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_prune(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_status(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_status(
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_check_clean(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_check_clean(
        group=args.group,
        allow_untracked=bool(args.allow_untracked),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_check_divergence(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_check_divergence(
        group=args.group,
        base=str(args.base),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_diff(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = worktree_group_diff(
        group=str(args.group),
        diff_mode=str(getattr(args, "mode", "dirty") or "dirty"),
        base=str(getattr(args, "base", "") or ""),
        repos=list(getattr(args, "repos", []) or []) or None,
        sets=list(getattr(args, "sets", []) or []) or None,
        tags=list(getattr(args, "tags", []) or []) or None,
        allow_all=bool(getattr(args, "all", False)),
        max_patch_bytes_per_repo=int(
            getattr(args, "max_bytes", 2_000_000) or 2_000_000
        ),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_group_annotate(args: argparse.Namespace) -> None:
    root = workspace_root()
    from agent_loom.workspace.worktree_meta import harness_group_annotate

    res = harness_group_annotate(
        ws_root=root,
        group=str(args.group),
        purpose=str(args.purpose),
        ticket_id=str(getattr(args, "ticket", "") or ""),
        owner=str(getattr(args, "owner", "") or ""),
        ttl=str(getattr(args, "ttl", "") or ""),
        kind=str(getattr(args, "kind", "normal") or "normal"),
    )
    emit_result(args, root, res)


def cmd_worktree_rebase(args: argparse.Namespace) -> None:
    root = workspace_root()
    req = str(getattr(args, "require_lease", "") or "").strip()
    if req:
        lease_require_active(key=req, root=root)
    res = worktree_rebase(
        group=args.group,
        base_ref=args.base_ref,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_push(args: argparse.Namespace) -> None:
    root = workspace_root()
    req = str(getattr(args, "require_lease", "") or "").strip()
    if req:
        lease_require_active(key=req, root=root)
    res = worktree_push(
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        force=bool(args.force),
        force_with_lease=bool(args.force_with_lease),
        set_upstream=bool(args.set_upstream),
        confirm_force=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_worktree_gc(args: argparse.Namespace) -> None:
    root = workspace_root()
    req = str(getattr(args, "require_lease", "") or "").strip()
    if req:
        lease_require_active(key=req, root=root)
    res = worktree_gc(
        older_than_days=int(args.older_than),
        skip_leased=bool(getattr(args, "skip_leased", False)),
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)
