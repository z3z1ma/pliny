from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from agent_loom.core.cli_output import emit_json, make_ok_envelope, normalize_payload
from agent_loom.team.core import inbox_list, inbox_send, inbox_show
from agent_loom.team.strings import message_preview


def emit_json_result(result: Any) -> None:
    emit_json(make_ok_envelope(normalize_payload(result)), indent=2)


def cmd_inbox_list(args: argparse.Namespace) -> None:
    res = inbox_list(
        team=args.team,
        to=str(getattr(args, "to", "") or ""),
        unacked_only=bool(getattr(args, "unacked", False)),
        limit=int(getattr(args, "limit", 200)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    for m in reversed(res.messages):
        mid = str(m.get("id") or "")
        created = str(m.get("created_at") or "")
        sender = str(m.get("from") or "")
        to = str(m.get("to") or "")
        kind = str(m.get("kind") or "")
        acked = "ACK" if str(m.get("acked_at") or "").strip() else "UNACK"
        first = message_preview(m.get("message") or "", max_len=120)
        print(f"{created} [{acked}] {kind} {sender} -> {to} id={mid} | {first}")


def cmd_inbox_show(args: argparse.Namespace) -> None:
    res = inbox_show(
        team=args.team,
        msg_id=str(args.msg_id or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    sys.stdout.write(json.dumps(res.message, indent=2) + "\n")


def cmd_inbox_ack(args: argparse.Namespace) -> None:
    import importlib

    team_cli = importlib.import_module("agent_loom.team.cli")
    res = team_cli.inbox_ack(
        team=args.team,
        msg_id=str(args.msg_id or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return

    msg = res.message if isinstance(res.message, dict) else {}
    mid = str(msg.get("id") or str(args.msg_id or "")).strip()
    sender = str(msg.get("from") or "").strip()
    to = str(msg.get("to") or "").strip()
    kind = str(msg.get("kind") or "").strip()
    created_at = str(msg.get("created_at") or "").strip()
    acked_at = str(msg.get("acked_at") or "").strip()
    body = str(msg.get("message") or "")

    sys.stdout.write(f"id: {mid}\n")
    sys.stdout.write(f"from: {sender}\n")
    sys.stdout.write(f"to: {to}\n")
    sys.stdout.write(f"kind: {kind}\n")
    sys.stdout.write(f"created_at: {created_at}\n")
    sys.stdout.write(f"acked_at: {acked_at}\n")
    sys.stdout.write("\n")
    sys.stdout.write(body)
    if body and not body.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.write("\n")
    sys.stdout.write(f"acked id={mid}\n")


def cmd_inbox_send(args: argparse.Namespace) -> None:
    res = inbox_send(
        team=args.team,
        to=str(getattr(args, "to", "") or ""),
        message=str(getattr(args, "message", "") or ""),
        kind=str(getattr(args, "kind", "note") or "note"),
        sender=str(getattr(args, "sender", "team") or "team"),
        nudge=bool(getattr(args, "nudge", True)),
        force=bool(getattr(args, "force", False)),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print("sent")
