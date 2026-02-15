from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from agent_loom.workspace.core import (
    repo_init,
    repo_merge_attempt,
    repo_snapshot_capture,
    repo_snapshot_diff,
    repo_snapshot_restore,
    repo_status,
    repo_worktree_add,
    repo_worktree_check_clean,
    repo_worktree_check_divergence,
    repo_worktree_diff,
    repo_worktree_ensure,
    repo_worktree_ensure_detached,
    repo_worktree_ls,
    repo_worktree_prune,
    repo_worktree_rm,
    repo_worktree_rm_path,
    repo_worktree_status,
)
from agent_loom.workspace.repo.cleanup import (
    repo_worktree_cleanup_apply,
    repo_worktree_cleanup_suggest,
)
from agent_loom.workspace.repo.core import repo_root
from agent_loom.workspace.repo.sandbox import (
    repo_sandbox_create,
    repo_sandbox_gc,
    repo_sandbox_promote,
)


def emit_result(args: argparse.Namespace, root: Path, result: Any) -> None:
    """Emit result using workspace CLI's emit_result."""
    from agent_loom.workspace.cli import emit_result as _emit_result

    _emit_result(args, root, result)


def cmd_repo_status(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_status(root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_add(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_add(
        branch=args.branch,
        base_ref=args.base_ref,
        path=args.path,
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_ensure(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_ensure(
        branch=args.branch,
        path=getattr(args, "path", None),
        base_ref=args.base_ref,
        allow_dirty=bool(args.allow_dirty),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_rm(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_rm(
        branch=args.branch,
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_rm_path(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_rm_path(
        path=args.path,
        force=bool(args.force),
        confirm=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_prune(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_prune(root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_ensure_detached(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_ensure_detached(path=args.path, ref=args.ref, root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_ls(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_ls(root=root)
    emit_result(args, root, res)


def cmd_repo_worktree_status(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_status(
        worktree=str(getattr(args, "worktree", "") or ""), root=root
    )
    emit_result(args, root, res)


def cmd_repo_worktree_check_clean(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_check_clean(
        worktree=str(getattr(args, "worktree", "") or ""),
        allow_untracked=bool(getattr(args, "allow_untracked", False)),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_check_divergence(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_check_divergence(
        base=str(getattr(args, "base", "") or ""),
        worktree=str(getattr(args, "worktree", "") or ""),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_diff(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_diff(
        worktree=str(getattr(args, "worktree", "") or ""),
        diff_mode=str(getattr(args, "mode", "dirty") or "dirty"),
        base=str(getattr(args, "base", "") or ""),
        max_patch_bytes=int(getattr(args, "max_bytes", 2_000_000) or 2_000_000),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_worktree_annotate(args: argparse.Namespace) -> None:
    root = repo_root()
    from agent_loom.workspace.worktree_meta import repo_worktree_annotate

    res = repo_worktree_annotate(
        repo_root=root,
        branch=str(args.branch),
        purpose=str(args.purpose),
        ticket_id=str(getattr(args, "ticket", "") or ""),
        owner=str(getattr(args, "owner", "") or ""),
        ttl=str(getattr(args, "ttl", "") or ""),
        kind=str(getattr(args, "kind", "normal") or "normal"),
    )
    emit_result(args, root, res)


def cmd_repo_snapshot_capture(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_snapshot_capture(
        name=str(args.name),
        worktree=str(getattr(args, "worktree", "") or ""),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_snapshot_diff(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_snapshot_diff(name=str(args.name), root=root)
    emit_result(args, root, res)


def cmd_repo_snapshot_restore(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_snapshot_restore(
        name=str(args.name),
        confirm=bool(getattr(args, "yes", False)),
        force_clean=bool(getattr(args, "force_clean", False)),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_cleanup_suggest(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_cleanup_suggest(root=root)
    emit_result(args, root, res)


def cmd_repo_cleanup_apply(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_worktree_cleanup_apply(
        ids=list(args.id or []),
        confirm=bool(args.yes),
        force=bool(args.force),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_sandbox_create(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_sandbox_create(
        base_ref=str(args.base),
        name=str(getattr(args, "name", "") or ""),
        ttl=str(getattr(args, "ttl", "") or "2h"),
        purpose=str(getattr(args, "purpose", "sandbox") or "sandbox"),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_sandbox_promote(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_sandbox_promote(
        from_branch=str(args.from_branch),
        to_branch=str(args.to_branch),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_sandbox_gc(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_sandbox_gc(confirm=bool(args.yes), force=bool(args.force), root=root)
    emit_result(args, root, res)


def cmd_repo_merge_attempt(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_merge_attempt(
        worktree=args.worktree,
        base=args.base,
        topic=args.topic,
        force_clean=bool(args.force_clean),
        root=root,
    )
    emit_result(args, root, res)


def cmd_repo_init(args: argparse.Namespace) -> None:
    root = repo_root()
    res = repo_init(root=root)
    emit_result(args, root, res)
