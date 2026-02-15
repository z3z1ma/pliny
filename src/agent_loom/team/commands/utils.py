from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any

from agent_loom.core.cli_output import emit_json, make_ok_envelope, normalize_payload
from agent_loom.core.time import parse_duration_seconds
from agent_loom.team.constants import (
    DEFAULT_DISBAND_REMINDER_RESEND_S,
    DEFAULT_DONE_CHECK_S,
    DEFAULT_HARNESS,
    DEFAULT_IDLE_SCREEN_S,
    DEFAULT_OBJECTIVE_NUDGE_S,
    ENV_TEAM_ROLE,
    ENV_TEAM_WORKER_ID,
    ROLE_MANAGER,
)
from agent_loom.team.core import bounce, capture, send, tui, wait
from agent_loom.team.errors import TeamError
from agent_loom.team.strings import sanitize


def emit_json_result(result: Any) -> None:
    emit_json(make_ok_envelope(normalize_payload(result)), indent=2)


def cmd_capture(args: argparse.Namespace) -> None:
    res = capture(
        team=args.team,
        target=args.target,
        lines=int(args.lines),
        no_join=bool(args.no_join),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    if bool(getattr(args, "header", False)):
        sys.stdout.write(
            f"team capture at={res.captured_at} team={res.team} target={args.target} pane={res.pane.get('pane_id', '')} window={res.pane.get('window_name', '')} path={res.pane.get('path', '')}\n"
        )
        sys.stdout.write("---\n")
    sys.stdout.write(res.output)


def cmd_send(args: argparse.Namespace) -> None:
    msg_pos = str(getattr(args, "message", "") or "")
    msg_opt = str(getattr(args, "message_opt", "") or "")
    if msg_pos and msg_opt:
        raise TeamError(
            "Provide the message either positionally or via --message, not both",
            code="ARG",
            exit_code=2,
            hint='Examples: `loom team send <TEAM> <TARGET> "hi"` or `loom team send <TEAM> <TARGET> --message "hi"`.',
        )
    msg = msg_opt or msg_pos
    res = send(
        team=args.team,
        target=args.target,
        message=msg,
        force=bool(args.force),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    if res.delivered:
        print("sent")
    else:
        print(f"queued_in_inbox (tmux_delivery={res.delivery_reason or 'skipped'})")
        if res.suggestions:
            print("next:")
            for s in res.suggestions:
                print(f"- {s}")


def cmd_bounce(args: argparse.Namespace) -> None:
    res = bounce(
        team=args.team,
        target=str(args.target or ""),
        reason=str(getattr(args, "reason", "") or ""),
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    print(f"bounce requested worker={res.worker_id} inbox_id={res.inbox_id}")


def cmd_wait(args: argparse.Namespace) -> None:
    team = ""
    duration = ""
    if getattr(args, "duration", None):
        team = sanitize(str(args.team_or_duration or ""), max_len=80)
        duration = str(args.duration or "").strip()
    else:
        duration = str(args.team_or_duration or "").strip()
        team = ""

    if not team:
        inferred = None
        try:
            from agent_loom.team.core import _infer_team_from_tmux_env

            inferred = _infer_team_from_tmux_env()
        except Exception:
            inferred = None
        if inferred:
            team = inferred

    if not team:
        raise TeamError(
            "Team is required when not running inside a team tmux session",
            code="ARG",
            exit_code=2,
            hint="Provide a team name explicitly, or run inside the team tmux session so it can be inferred.",
            suggestions=["loom team wait <TEAM> <DUR>", "loom team status <TEAM>"],
        )

    try:
        seconds = parse_duration_seconds(duration)
    except ValueError as e:
        raise TeamError(str(e), code="ARG", exit_code=2) from e
    recipient = "manager"
    if os.environ.get("TMUX"):
        role = str(os.getenv(ENV_TEAM_ROLE) or "").strip().lower()
        if role and role != ROLE_MANAGER:
            wid = sanitize(str(os.getenv(ENV_TEAM_WORKER_ID) or ""), max_len=48)
            if wid:
                recipient = wid

    if not bool(getattr(args, "quiet", False)) and not args.json:
        print(f"waiting up to {seconds}s (wake on inbox to={recipient})")

    res = wait(
        team=team,
        duration=duration,
        repo=Path(args.repo).resolve() if args.repo else None,
    )
    if args.json:
        emit_json_result(res)
        return
    if not bool(getattr(args, "quiet", False)):
        print("awake")


def cmd_tui(args: argparse.Namespace) -> None:
    tui(
        project_dir=Path(args.project_dir),
        harness=str(getattr(args, "harness", DEFAULT_HARNESS) or DEFAULT_HARNESS),
        bin_override=str(getattr(args, "bin", "") or ""),
        agent=str(getattr(args, "agent", "") or ""),
        model=str(getattr(args, "model", "") or ""),
        prompt=str(getattr(args, "prompt", "") or ""),
        nudge_cooldown_s=float(getattr(args, "nudge_cooldown_s", 300.0) or 300.0),
        stall_threshold_s=float(getattr(args, "stall_threshold_s", 1080.0) or 1080.0),
        idle_screen_threshold_s=float(
            getattr(args, "idle_screen_threshold_s", DEFAULT_IDLE_SCREEN_S)
            or DEFAULT_IDLE_SCREEN_S
        ),
        respawn_cap=int(getattr(args, "respawn_cap", 3) or 3),
        respawn_window_s=float(getattr(args, "respawn_window_s", 3600.0) or 3600.0),
        objective_nudge_s=float(
            getattr(args, "objective_nudge_s", DEFAULT_OBJECTIVE_NUDGE_S)
            or DEFAULT_OBJECTIVE_NUDGE_S
        ),
        done_check_s=float(
            getattr(args, "done_check_s", DEFAULT_DONE_CHECK_S) or DEFAULT_DONE_CHECK_S
        ),
        disband_resend_s=float(
            getattr(args, "disband_resend_s", DEFAULT_DISBAND_REMINDER_RESEND_S)
            or DEFAULT_DISBAND_REMINDER_RESEND_S
        ),
    )
