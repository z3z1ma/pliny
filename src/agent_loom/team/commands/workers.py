"""Team worker command handlers."""

from __future__ import annotations

import argparse
from pathlib import Path

from agent_loom.team.constants import ENV_TICKET_DIR, ROLE_WORKER
from agent_loom.team.core import (
    mark_retirable,
    resume_worker,
    retire,
    spawn,
    spawn_integrator,
)


def emit_json_result(result: object) -> None:
    from agent_loom.core.cli_output import emit_json, make_ok_envelope, normalize_payload

    emit_json(make_ok_envelope(normalize_payload(result)), indent=2)


def cmd_spawn(args: argparse.Namespace) -> None:
    res = spawn(
        team=args.team,
        ticket_id=args.ticket_id,
        role=str(args.role or ROLE_WORKER),
        worker_id=str(args.worker_id or ""),
        window=str(args.window or ""),
        worktree_key=str(args.worktree_key or ""),
        branch=str(args.branch or ""),
        base_ref=str(args.base_ref or ""),
        resume=bool(getattr(args, "resume", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    worker = res.worker
    print(f"spawned {worker.get('worker_id')} ({worker.get('role')})")
    print(f"- ticket: {worker.get('ticket_id')}")
    print(f"- branch: {worker.get('branch')}")
    print(f"- base: {worker.get('base')}")
    print(f"- window: {worker.get('window')}")
    print(f"- worktree: {worker.get('worktree')}")
    print(f"- tickets_dir: {res.tickets_dir} ({ENV_TICKET_DIR} injected into pane)")


def cmd_spawn_integrator(args: argparse.Namespace) -> None:
    res = spawn_integrator(
        team=args.team,
        worker_id=str(args.worker_id or "integrator"),
        window=str(args.window or "integrator"),
        worktree=str(args.worktree or "merge-queue"),
        branch=str(args.branch or ""),
        base_ref=str(args.base_ref or ""),
        force=bool(getattr(args, "force", False)),
        require_clean=bool(getattr(args, "require_clean", False)),
        target_branch=str(getattr(args, "target_branch", "") or ""),
        remote=str(getattr(args, "remote", "") or ""),
        push=getattr(args, "push", None),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    if not res.respawned:
        print("exists")
        return
    print(res.worker_id)


def cmd_retire(args: argparse.Namespace) -> None:
    res = retire(
        team=args.team,
        worker_id=str(args.worker_id or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(f"retired {res.worker_id}")


def cmd_mark_retirable(args: argparse.Namespace) -> None:
    res = mark_retirable(
        team=args.team,
        worker_id=str(args.worker_id or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(f"marked_retirable {res.worker_id}")


def cmd_resume_worker(args: argparse.Namespace) -> None:
    res = resume_worker(
        team=args.team,
        worker_id=str(args.worker_id or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    worker = res.worker
    print(f"resumed {worker.get('worker_id')} ({worker.get('role')})")
    print(f"- ticket: {worker.get('ticket_id')}")
    print(f"- branch: {worker.get('branch')}")
    print(f"- base: {worker.get('base')}")
    print(f"- window: {worker.get('window')}")
    print(f"- worktree: {worker.get('worktree')}")
