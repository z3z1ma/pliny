from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional

from agent_loom.workspace.core import (
    harness_cleanup_apply,
    harness_cleanup_suggest,
    harness_exec,
    harness_impact_repos,
    harness_impact_snapshot,
    harness_init,
    harness_repo_edit,
    harness_set_ls,
    harness_set_rm,
    harness_set_show,
    harness_set_upsert,
    lease_require_active,
)
from agent_loom.workspace.guards import harness_root
from agent_loom.workspace.harness.sandbox import (
    harness_sandbox_create,
    harness_sandbox_gc,
    harness_sandbox_promote,
)

workspace_root = harness_root


def emit_result(args: argparse.Namespace, root: Path, result: object) -> None:
    from agent_loom.workspace.cli import emit_result as _emit_result

    _emit_result(args, root, result)


def cmd_harness_init(args: argparse.Namespace) -> None:
    root_arg = str(getattr(args, "root", "") or "").strip()
    root = Path(root_arg).expanduser().resolve() if root_arg else Path.cwd().resolve()
    res = harness_init(root=root, symlinks=bool(getattr(args, "symlinks", False)))
    emit_result(args, root, res)


def cmd_harness_exec(args: argparse.Namespace) -> None:
    root = workspace_root()
    cmd = list(getattr(args, "cmd_argv", []) or [])
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    res = harness_exec(
        cmd=cmd,
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        jobs=int(args.jobs),
        require_clean=bool(args.require_clean),
        root=root,
    )
    emit_result(args, root, res)


def cmd_harness_repo_edit(args: argparse.Namespace) -> None:
    root = workspace_root()
    shallow: Optional[bool]
    if bool(getattr(args, "shallow", False)):
        shallow = True
    elif bool(getattr(args, "no_shallow", False)):
        shallow = False
    else:
        shallow = None

    res = harness_repo_edit(
        name=args.name,
        remote=getattr(args, "remote", None),
        default_branch=getattr(args, "default_branch", None),
        add_tags=getattr(args, "add_tag", None),
        rm_tags=getattr(args, "rm_tag", None),
        description=getattr(args, "description", None),
        shallow=shallow,
        depth=getattr(args, "depth", None),
        root=root,
    )
    emit_result(args, root, res)


def cmd_harness_set_upsert(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_set_upsert(name=args.name, items=args.items, root=root)
    emit_result(args, root, res)


def cmd_harness_set_rm(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_set_rm(name=args.name, root=root)
    emit_result(args, root, res)


def cmd_harness_set_show(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_set_show(name=args.name, root=root)
    emit_result(args, root, res)


def cmd_harness_set_ls(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_set_ls(root=root)
    emit_result(args, root, res)


def cmd_harness_sandbox_create(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_sandbox_create(
        group=str(args.group),
        base_ref=str(args.base_ref),
        ttl=str(getattr(args, "ttl", "2h") or "2h"),
        purpose=str(getattr(args, "purpose", "sandbox") or "sandbox"),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        clone=bool(getattr(args, "clone", False)),
        root=root,
    )
    emit_result(args, root, res)


def cmd_harness_sandbox_promote(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_sandbox_promote(group=str(args.group), root=root)
    emit_result(args, root, res)


def cmd_harness_sandbox_gc(args: argparse.Namespace) -> None:
    root = workspace_root()
    req = str(getattr(args, "require_lease", "") or "").strip()
    if req:
        lease_require_active(key=req, root=root)
    res = harness_sandbox_gc(confirm=bool(args.yes), force=bool(args.force), root=root)
    emit_result(args, root, res)


def cmd_harness_cleanup_suggest(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_cleanup_suggest(root=root)
    emit_result(args, root, res)


def cmd_harness_cleanup_apply(args: argparse.Namespace) -> None:
    root = workspace_root()
    req = str(getattr(args, "require_lease", "") or "").strip()
    if req:
        lease_require_active(key=req, root=root)
    res = harness_cleanup_apply(
        ids=list(args.id or []),
        confirm=bool(args.yes),
        force=bool(args.force),
        root=root,
    )
    emit_result(args, root, res)


def cmd_harness_impact_repos(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_impact_repos(changed=list(args.changed or []), root=root)
    emit_result(args, root, res)


def cmd_harness_impact_snapshot(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = harness_impact_snapshot(
        name=str(args.name),
        include_missing=not bool(getattr(args, "no_missing", False)),
        root=root,
    )
    emit_result(args, root, res)
