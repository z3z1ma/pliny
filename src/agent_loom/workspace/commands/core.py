from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any
from agent_loom.core.cli_output import emit_json, normalize_payload
from agent_loom.core.time import now_iso
from agent_loom.workspace.core import (
    add_repo,
    branch,
    context,
    deepen,
    list_repos,
    prime,
    remove_repo,
    snapshot,
    snapshot_diff,
    snapshot_restore,
    status,
    sync,
)
from agent_loom.workspace.guards import harness_root


workspace_root = harness_root


def _cmd_name(args: argparse.Namespace) -> str:
    top = getattr(args, "cmd", "") or ""
    if top == "harness":
        cmd = getattr(args, "harness_cmd", "") or ""
        if cmd == "worktree":
            cmd = f"worktree {getattr(args, 'worktree_cmd', '')}".strip()
        elif cmd == "snapshot":
            cmd = f"snapshot {getattr(args, 'snapshot_cmd', '')}".strip()
        elif cmd == "repo":
            cmd = f"repo {getattr(args, 'repo_cmd', '')}".strip()
        elif cmd == "set":
            cmd = f"set {getattr(args, 'set_cmd', '')}".strip()
        elif cmd == "lease":
            cmd = f"lease {getattr(args, 'lease_cmd', '')}".strip()
        elif cmd in {"components", "services"}:
            cmd = f"{cmd} {getattr(args, 'components_cmd', '')}".strip()
        elif cmd == "deps":
            cmd = f"deps {getattr(args, 'deps_cmd', '')}".strip()
        elif cmd == "sandbox":
            cmd = f"sandbox {getattr(args, 'sandbox_cmd', '')}".strip()
        elif cmd == "cleanup":
            cmd = f"cleanup {getattr(args, 'cleanup_cmd', '')}".strip()
        elif cmd == "impact":
            cmd = f"impact {getattr(args, 'impact_cmd', '')}".strip()
        return f"{top} {cmd}".strip()

    cmd = top
    if cmd == "worktree":
        cmd = f"worktree {getattr(args, 'worktree_cmd', '')}".strip()
    elif cmd == "snapshot":
        cmd = f"snapshot {getattr(args, 'snapshot_cmd', '')}".strip()
    elif cmd == "cleanup":
        cmd = f"cleanup {getattr(args, 'cleanup_cmd', '')}".strip()
    elif cmd == "sandbox":
        cmd = f"sandbox {getattr(args, 'sandbox_cmd', '')}".strip()
    elif cmd == "merge":
        cmd = f"merge {getattr(args, 'merge_cmd', '')}".strip()
    return cmd


def emit_ok(
    args: argparse.Namespace, root: Path, data: Any = None
) -> None:
    emit_json(
        {
            "ok": True,
            "cmd": _cmd_name(args),
            "root": str(root.resolve()),
            "data": normalize_payload(data),
            "meta": {"generated_at": now_iso()},
        },
        indent=2,
    )


def _render_prime_text(payload: dict[str, Any]) -> str:
    text = str(payload.get("markdown") or "")
    if text:
        return text.rstrip() + "\n"
    return ""


def emit_result(args: argparse.Namespace, root: Path, result: Any) -> None:
    if getattr(args, "json", False):
        emit_ok(args, root, result)
        return

    from agent_loom.workspace.cli import _render_text
    sys.stdout.write(_render_text(result))


def cmd_add(args: argparse.Namespace) -> None:
    root = harness_root()
    res = add_repo(
        name=args.name,
        remote=args.remote,
        default_branch=args.default_branch,
        shallow=bool(args.shallow),
        depth=int(args.depth),
        clone=bool(args.clone),
        force=bool(args.force),
        root=root,
    )
    emit_result(args, root, res)


def cmd_remove(args: argparse.Namespace) -> None:
    root = harness_root()
    res = remove_repo(
        name=args.name,
        delete_clone=bool(args.delete_clone),
        delete_component_md=bool(getattr(args, "delete_component_md", False)),
        confirm_delete=bool(args.yes_delete),
        root=root,
    )
    emit_result(args, root, res)


def cmd_list(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = list_repos(root=root)
    emit_result(args, root, res)


def cmd_sync(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = sync(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        clone=bool(args.clone),
        jobs=int(args.jobs),
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_status(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = status(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        jobs=int(args.jobs),
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_context(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = context(
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        jobs=int(args.jobs),
        root=root,
    )
    emit_result(args, root, res)


def cmd_branch(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = branch(
        branch=args.branch,
        reset=bool(args.reset),
        allow_dirty=bool(args.allow_dirty),
        clone=bool(args.clone),
        base_ref=args.base_ref,
        refresh_index=bool(args.refresh_index),
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        confirm_reset=bool(args.yes),
        root=root,
    )
    emit_result(args, root, res)


def cmd_snapshot_capture(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = snapshot(
        name=args.name,
        group=args.group,
        repos=args.repos,
        sets=args.sets,
        tags=args.tags,
        allow_all=bool(args.all),
        root=root,
    )
    emit_result(args, root, res)


def cmd_snapshot_diff(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = snapshot_diff(name=args.name, root=root)
    emit_result(args, root, res)


def cmd_snapshot_restore(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = snapshot_restore(
        name=args.name,
        confirm=bool(args.yes),
        force_clean=bool(args.force_clean),
        root=root,
    )
    emit_result(args, root, res)


def cmd_deepen(args: argparse.Namespace) -> None:
    root = workspace_root()
    res = deepen(repo=args.repo, depth=int(args.depth), root=root)
    emit_result(args, root, res)


def cmd_prime(args: argparse.Namespace) -> None:
    res = prime()
    payload = res.payload
    root = Path.cwd().resolve()
    if getattr(args, "json", False):
        emit_json(
            {
                "ok": True,
                "cmd": "prime",
                "root": str(root),
                "data": payload,
                "meta": {"generated_at": now_iso()},
            },
            indent=2,
        )
        return
    sys.stdout.write(_render_prime_text(payload))
