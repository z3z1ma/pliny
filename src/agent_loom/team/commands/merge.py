"""Team merge queue command handlers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from agent_loom.core.cli_output import emit_json, make_ok_envelope, normalize_payload
from agent_loom.team.core import merge_done, merge_enqueue, merge_list, merge_next, ship


def emit_json_result(result: Any) -> None:
    emit_json(make_ok_envelope(normalize_payload(result)), indent=2)


def cmd_merge_enqueue(args: argparse.Namespace) -> None:
    res = merge_enqueue(
        team=args.team,
        branch=str(args.branch or ""),
        ticket_id=str(args.ticket or ""),
        from_worker=str(args.from_worker or ""),
        note=str(args.note or ""),
        nudge=bool(getattr(args, "nudge", True)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(res.item.get("id", ""))


def cmd_merge_list(args: argparse.Namespace) -> None:
    res = merge_list(
        team=args.team,
        include_done=bool(getattr(args, "all", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    for it in res.items:
        state = str(it.get("state") or "")
        tid = str(it.get("ticket_id") or "-")
        branch = str(it.get("branch") or "")
        cid = str(it.get("id") or "")
        claimed = str(it.get("claimed_by") or "")
        print(f"{cid} [{state}] ticket={tid} branch={branch} claimed_by={claimed}")


def cmd_merge_next(args: argparse.Namespace) -> None:
    res = merge_next(
        team=args.team,
        claim_by=str(getattr(args, "claim_by", "") or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    if not res.item:
        print("(empty)")
    else:
        print(json.dumps(res.item, indent=2))


def cmd_merge_done(args: argparse.Namespace) -> None:
    res = merge_done(
        team=args.team,
        item_id=str(args.item_id or ""),
        result=str(args.result or ""),
        note=str(args.note or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("done")


def cmd_ship(args: argparse.Namespace) -> None:
    res = ship(
        team=args.team,
        force_clean=bool(getattr(args, "force_clean", False)),
        push=getattr(args, "push", None),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    if res.merged:
        print(f"shipped {len(res.shipped_ids)} items to {res.target_branch}")
    else:
        print("not_shipped")
