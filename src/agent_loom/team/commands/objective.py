from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from agent_loom.core.cli_output import emit_json, make_ok_envelope, normalize_payload
from agent_loom.team.core import (
    objective_append,
    objective_set,
    objective_show,
    prep_sprint,
    sprint_clear,
    sprint_set,
    sprint_show,
)


def emit_json_result(result: Any) -> None:
    emit_json(make_ok_envelope(normalize_payload(result)), indent=2)


def cmd_objective_show(args: argparse.Namespace) -> None:
    res = objective_show(
        team=args.team, repo=Path(args.repo).resolve() if args.repo else None
    )
    if args.json:
        emit_json_result(res)
        return
    sys.stdout.write(str(res.objective or "").rstrip("\n") + "\n")


def cmd_objective_set(args: argparse.Namespace) -> None:
    res = objective_set(
        team=args.team,
        message=str(getattr(args, "message", "") or ""),
        file_path=str(getattr(args, "file", "") or ""),
        stdin_ok=bool(getattr(args, "stdin", False)),
        nudge=bool(getattr(args, "nudge", True)),
        force=bool(getattr(args, "force", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("ok")


def cmd_objective_append(args: argparse.Namespace) -> None:
    res = objective_append(
        team=args.team,
        message=str(getattr(args, "message", "") or ""),
        file_path=str(getattr(args, "file", "") or ""),
        stdin_ok=bool(getattr(args, "stdin", False)),
        nudge=bool(getattr(args, "nudge", True)),
        force=bool(getattr(args, "force", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("ok")


def cmd_prep_sprint(args: argparse.Namespace) -> None:
    res = prep_sprint(
        team=args.team,
        name=str(getattr(args, "name", "") or ""),
        force=bool(getattr(args, "force", False)),
        spawn_investigator=not bool(getattr(args, "no_spawn", False)),
        ticket_type=str(getattr(args, "ticket_type", "task") or "task"),
        ticket_priority=int(getattr(args, "priority", 1) or 1),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    sprint = res.sprint or {}
    print(f"sprint: {sprint.get('name')}")
    print(f"tag: {sprint.get('tag')}")
    print(f"prep_ticket: {res.ticket_id}")
    if res.spawned:
        print(f"investigator: {res.worker_id}")


def cmd_sprint_show(args: argparse.Namespace) -> None:
    res = sprint_show(
        team=args.team,
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    sprint = res.sprint or {}
    if not sprint:
        print("(none)")
        return
    print(f"name: {sprint.get('name')}")
    print(f"tag: {sprint.get('tag')}")
    print(f"rev: {res.rev}")


def cmd_sprint_set(args: argparse.Namespace) -> None:
    res = sprint_set(
        team=args.team,
        name=str(args.name or "").strip(),
        tag=str(args.tag or "").strip() or None,
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("ok")


def cmd_sprint_clear(args: argparse.Namespace) -> None:
    res = sprint_clear(
        team=args.team,
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("ok")
