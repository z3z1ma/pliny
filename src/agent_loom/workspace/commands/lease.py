from __future__ import annotations

import argparse
from pathlib import Path

from agent_loom.workspace.core import (
    lease_acquire,
    lease_list,
    lease_release,
    lease_renew,
    lease_show,
)
from agent_loom.workspace.guards import harness_root

workspace_root = harness_root


def emit_result(args: argparse.Namespace, root: Path, result: object) -> None:
    from agent_loom.workspace.cli import emit_result as _emit_result

    _emit_result(args, root, result)


def cmd_lease_acquire(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_acquire(
        key=args.key,
        ttl=str(getattr(args, "ttl", "") or ""),
        force=bool(args.force),
        root=root,
    )
    emit_result(args, root, res)


def cmd_lease_release(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_release(key=args.key, root=root)
    emit_result(args, root, res)


def cmd_lease_ls(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_list(root=root)
    emit_result(args, root, res)


def cmd_lease_show(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_show(key=args.key, root=root)
    emit_result(args, root, res)


def cmd_lease_renew(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = lease_renew(key=args.key, ttl=str(getattr(args, "ttl", "") or ""), root=root)
    emit_result(args, root, res)
