from __future__ import annotations

import argparse
from pathlib import Path

from agent_loom.workspace.core import (
    components_refresh_index,
    services_refresh_index,
    deps_show,
    deps_who_uses,
    deps_closure,
    deps_impacted,
)
from agent_loom.workspace.guards import harness_root

workspace_root = harness_root


def emit_result(args: argparse.Namespace, root: Path, result: object) -> None:
    """Import emit_result from parent CLI module."""
    from agent_loom.workspace.cli import emit_result as _emit_result

    _emit_result(args, root, result)


def cmd_components_refresh_index(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = components_refresh_index(root=root)
    emit_result(args, root, res)


def cmd_services_refresh_index(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = services_refresh_index(root=root)
    emit_result(args, root, res)


def cmd_deps_show(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_show(component=args.component, root=root)
    emit_result(args, root, res)


def cmd_deps_who_uses(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_who_uses(component=args.component, root=root)
    emit_result(args, root, res)


def cmd_deps_closure(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_closure(component=args.component, root=root)
    emit_result(args, root, res)


def cmd_deps_impacted(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deps_impacted(component=args.component, root=root)
    emit_result(args, root, res)
