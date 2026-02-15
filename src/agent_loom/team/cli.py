from __future__ import annotations

import argparse
import difflib
import sys
from typing import Optional, Sequence

from agent_loom.team.commands.inbox import (
    cmd_inbox_ack,
    cmd_inbox_list,
    cmd_inbox_send,
    cmd_inbox_show,
)
from agent_loom.team.commands.lifecycle import (
    cmd_attach,
    cmd_disband,
    cmd_doctor,
    cmd_done,
    cmd_init,
    cmd_janitor,
    cmd_pause,
    cmd_prime,
    cmd_resume,
    cmd_start,
    cmd_status,
)
from agent_loom.team.commands.merge import (
    cmd_merge_done,
    cmd_merge_enqueue,
    cmd_merge_list,
    cmd_merge_next,
    cmd_ship,
)
from agent_loom.team.commands.objective import (
    cmd_objective_append,
    cmd_objective_set,
    cmd_objective_show,
    cmd_prep_sprint,
    cmd_sprint_clear,
    cmd_sprint_set,
    cmd_sprint_show,
)
from agent_loom.team.commands.utils import (
    cmd_bounce,
    cmd_capture,
    cmd_send,
    cmd_tui,
    cmd_wait,
)
from agent_loom.team.commands.workers import (
    cmd_mark_retirable,
    cmd_resume_worker,
    cmd_retire,
    cmd_spawn,
    cmd_spawn_integrator,
)
from agent_loom.team.constants import (
    DEFAULT_AUTOCAPTURE_LINES,
    DEFAULT_DISBAND_REMINDER_RESEND_S,
    DEFAULT_DONE_CHECK_S,
    DEFAULT_HARNESS,
    DEFAULT_IDLE_SCREEN_S,
    DEFAULT_MANAGER_WINDOW,
    DEFAULT_OBJECTIVE_NUDGE_S,
    ROLE_INVESTIGATOR,
    ROLE_WORKER,
)
from agent_loom.team.errors import TeamError
from agent_loom.team.core import inbox_ack
from agent_loom.team.output import _emit_error

__all__ = ["build_parser", "inbox_ack", "main"]


class ArgParseError(RuntimeError):
    pass


class TeamArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ArgParseError(message)


_FLAG_ALIASES = {
    "--repo-root": "--repo",
    "--worker": "--worker-id",
    "--worker_id": "--worker-id",
    "--worktree": "--worktree-key",
    "--worktree_key": "--worktree-key",
    "--no_nudge": "--no-nudge",
}


def _normalize_argv(argv: list[str]) -> list[str]:
    """Normalize common plausible argv variants before argparse."""

    out: list[str] = []
    i = 0
    while i < len(argv):
        tok = argv[i]

        # Normalize multi-word command aliases.
        if tok == "clock" and i + 1 < len(argv):
            nxt = str(argv[i + 1]).strip().lower()
            if nxt == "in":
                out.append("clock-in")
                i += 2
                continue
            if nxt == "out":
                out.append("clock-out")
                i += 2
                continue

        if tok in {"clockin", "clock-in"}:
            out.append("clock-in")
            i += 1
            continue
        if tok in {"clockout", "clock-out"}:
            out.append("clock-out")
            i += 1
            continue

        if tok in _FLAG_ALIASES:
            out.append(_FLAG_ALIASES[tok])
            i += 1
            continue

        if tok.startswith(tuple(f + "=" for f in _FLAG_ALIASES)):
            for src, dst in _FLAG_ALIASES.items():
                if tok.startswith(src + "="):
                    out.append(dst + tok[len(src) :])
                    break
            else:
                out.append(tok)
            i += 1
            continue

        # Normalize common choice aliases.
        if tok == "--role" and i + 1 < len(argv):
            val = str(argv[i + 1]).strip().lower()
            if val in {"inv", "invest", "investigation", "investigator"}:
                out.extend([tok, ROLE_INVESTIGATOR])
                i += 2
                continue
            if val in {"work", "worker"}:
                out.extend([tok, ROLE_WORKER])
                i += 2
                continue
        if tok == "--harness" and i + 1 < len(argv):
            val = str(argv[i + 1]).strip().lower().replace("-", "")
            if val in {"opencode", "openCode".lower(), "opencode"}:
                out.extend([tok, "opencode"])
                i += 2
                continue
            if val in {"claude"}:
                out.extend([tok, "claude"])
                i += 2
                continue
            if val in {"omp", "ohmypi"}:
                out.extend([tok, "omp"])
                i += 2
                continue
            if val in {"codex", "openaicodex"}:
                out.extend([tok, "codex"])
                i += 2
                continue
        if tok == "--result" and i + 1 < len(argv):
            val = str(argv[i + 1]).strip().lower()
            out.extend([tok, val])
            i += 2
            continue

        out.append(tok)
        i += 1

    # Positional fallbacks (safe, pattern-based).
    # objective set|append <TEAM> <text...>  ->  --message "text..."
    if len(out) >= 4 and out[0] == "objective" and out[2] in {"set", "append"}:
        has_text_flag = any(x in out for x in {"--message", "--file", "--stdin"})
        if not has_text_flag and len(out) > 3:
            team = out[1]
            subcmd = out[2]
            msg = " ".join(out[3:]).strip()
            if msg and not msg.startswith("-"):
                out = ["objective", team, subcmd, "--message", msg]

    # Inbox: common aliases and positional fallbacks.
    if len(out) >= 2 and out[0] == "inbox":
        # inbox <TEAM>  -> list
        if len(out) == 2:
            out = ["inbox", out[1], "list"]

        # inbox <TEAM> <cmd>
        if len(out) >= 3:
            subcmd = str(out[2] or "").strip().lower()

            # inbox <TEAM> ls|queue  -> list
            if subcmd in {"ls", "queue"}:
                out[2] = "list"
                subcmd = "list"

            # inbox <TEAM> --unacked  -> list --unacked
            if subcmd.startswith("-"):
                out = ["inbox", out[1], "list", *out[2:]]
                subcmd = "list"

            if subcmd == "list":
                flag_aliases = {
                    "--unread": "--unacked",
                    "--unacked-only": "--unacked",
                    "--unacked_only": "--unacked",
                    "--recipient": "--to",
                    "--target": "--to",
                    "--count": "--limit",
                }
                out = [flag_aliases.get(t, t) for t in out]

                # inbox <TEAM> list 20  -> --limit 20
                if len(out) == 4 and str(out[3] or "").strip().isdigit():
                    out = ["inbox", out[1], "list", "--limit", str(out[3]).strip()]

                # inbox <TEAM> list unread|unacked  -> --unacked
                if len(out) == 4 and str(out[3] or "").strip().lower() in {
                    "unread",
                    "unacked",
                }:
                    out = ["inbox", out[1], "list", "--unacked"]

            if subcmd in {"show", "ack"}:
                # inbox <TEAM> show|ack --id <id> -> positional id
                if len(out) >= 5 and str(out[3] or "") in {
                    "--id",
                    "--msg-id",
                    "--msg_id",
                }:
                    out = ["inbox", out[1], out[2], out[4], *out[5:]]

            if subcmd == "send":
                # inbox <TEAM> send ... -> always produce --to/--message when possible.
                team = out[1]
                rest = list(out[3:])

                send_flag_aliases = {
                    "--recipient": "--to",
                    "--target": "--to",
                    "--msg": "--message",
                    "--msg_text": "--message",
                    "--msg-text": "--message",
                    "--body": "--message",
                    "--text": "--message",
                }

                rest = [send_flag_aliases.get(t, t) for t in rest]

                known_value_flags = {"--to", "--message", "--kind", "--sender"}
                known_bool_flags = {"--no-nudge", "--force"}
                preserved: list[str] = []
                positional: list[str] = []
                to_val = ""
                msg_val = ""

                i = 0
                while i < len(rest):
                    tok = rest[i]
                    if tok in known_value_flags:
                        if i + 1 < len(rest):
                            val = rest[i + 1]
                            if tok == "--to":
                                to_val = str(val)
                            elif tok == "--message":
                                msg_val = str(val)
                            else:
                                preserved.extend([tok, str(val)])
                            i += 2
                            continue
                        preserved.append(tok)
                        i += 1
                        continue

                    if tok in known_bool_flags:
                        preserved.append(tok)
                        i += 1
                        continue

                    if tok.startswith("-") and "=" in tok:
                        k, v = tok.split("=", 1)
                        if k in known_value_flags:
                            if k == "--to":
                                to_val = v
                            elif k == "--message":
                                msg_val = v
                            else:
                                preserved.extend([k, v])
                            i += 1
                            continue

                    if tok.startswith("-"):
                        preserved.append(tok)
                        i += 1
                        continue

                    positional.append(str(tok))
                    i += 1

                if not to_val and positional:
                    to_val = positional.pop(0)

                if not msg_val and positional:
                    msg_val = " ".join(positional).strip()

                if to_val and msg_val:
                    out = [
                        "inbox",
                        team,
                        "send",
                        "--to",
                        to_val,
                        *preserved,
                        "--message",
                        msg_val,
                    ]

    # Merge queue: common aliases and positional fallbacks.
    if len(out) >= 2 and out[0] == "merge":
        # merge <TEAM>  -> list
        if len(out) == 2:
            out = ["merge", out[1], "list"]

        # merge <TEAM> <cmd>
        if len(out) >= 3:
            subcmd = str(out[2] or "").strip().lower()

            # merge <TEAM> queue|ls  -> list
            if subcmd in {"queue", "ls"}:
                out[2] = "list"
                subcmd = "list"

            # merge <TEAM> --all  -> list --all
            if subcmd.startswith("-"):
                out = ["merge", out[1], "list", *out[2:]]
                subcmd = "list"

            # merge <TEAM> list --include-done|--include-completed  -> --all
            if subcmd == "list":
                flag_aliases = {
                    "--include-done": "--all",
                    "--include_done": "--all",
                    "--include-completed": "--all",
                    "--include_completed": "--all",
                }
                out = [flag_aliases.get(t, t) for t in out]

                # merge <TEAM> list all  -> --all
                if len(out) == 4 and str(out[3] or "").strip().lower() == "all":
                    out = ["merge", out[1], "list", "--all"]

            # merge <TEAM> enqueue <branch> -> --branch
            if (
                len(out) >= 4
                and subcmd == "enqueue"
                and "--branch" not in out
                and not str(out[3] or "").startswith("-")
            ):
                out = ["merge", out[1], "enqueue", "--branch", out[3], *out[4:]]

            # merge <TEAM> next <claim_by> -> --claim-by
            if (
                len(out) >= 4
                and subcmd == "next"
                and "--claim-by" not in out
                and not str(out[3] or "").startswith("-")
            ):
                out = ["merge", out[1], "next", "--claim-by", out[3], *out[4:]]

    # merge <TEAM> done <item_id> <result> -> --result
    if (
        len(out) >= 5
        and out[0] == "merge"
        and out[2] == "done"
        and "--result" not in out
        and out[4].lower() in {"merged", "blocked", "dropped"}
    ):
        out = ["merge", out[1], "done", out[3], "--result", out[4].lower(), *out[5:]]

    return out


def _did_you_mean(value: str, choices: Sequence[str]) -> list[str]:
    v = str(value or "").strip()
    if not v:
        return []
    return difflib.get_close_matches(v, list(choices), n=3, cutoff=0.6)



def build_parser() -> argparse.ArgumentParser:
    p = TeamArgumentParser(
        prog="team",
        description="tmux-native agent orchestrator (manager + workers + integrator + merge queue)",
    )
    p.add_argument("--repo", help="Path inside repo (defaults to CWD)")
    p.add_argument(
        "--json", action="store_true", help="Emit JSON for machine consumption"
    )

    sub = p.add_subparsers(dest="cmd", required=True, parser_class=TeamArgumentParser)

    def add_wait_subcommand(name: str, *, help: str) -> argparse.ArgumentParser:
        sp = sub.add_parser(name, help=help)
        sp.add_argument(
            "team_or_duration",
            help="Either <duration> (when running inside team tmux) or <team> <duration>",
        )
        sp.add_argument("duration", nargs="?", help="Duration if <team> was provided")
        sp.add_argument("--quiet", action="store_true", help="Reduce stdout output")
        sp.set_defaults(func=cmd_wait)
        return sp

    # Run lifecycle
    ini = sub.add_parser(
        "init",
        help="Install/sync Team agent definitions (.opencode/agents and .claude/agents)",
    )
    ini.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing agent definitions on disk",
    )
    ini.add_argument(
        "--diff",
        action="store_true",
        help="Show diffs for skipped Team agent files",
    )
    ini.set_defaults(func=cmd_init)

    sp = sub.add_parser("start", help="Start or resume a team run")
    sp.add_argument("team", help="Team name")
    sp.add_argument("--objective", default="", help="High-level objective text")
    sp.add_argument(
        "--session",
        default="",
        help="Explicit tmux session name (defaults to team-<team>)",
    )
    sp.add_argument(
        "--harness",
        default="",
        choices=["opencode", "claude", "omp", "codex"],
        help="Agent harness for this run (default: existing run setting, else opencode)",
    )
    sp.add_argument(
        "--bin",
        default="",
        help="Override harness binary (wrapper/shim). Must be CLI-compatible with the selected harness",
    )
    sp.add_argument("--model", default="", help="Model override")
    sp.add_argument("--manager-model", default="", help="Manager model override")
    sp.add_argument(
        "--investigator-model", default="", help="Investigator model override"
    )
    sp.add_argument("--worker-model", default="", help="Worker model override")
    sp.add_argument("--integrator-model", default="", help="Integrator model override")
    sp.add_argument(
        "--manager-window",
        default=DEFAULT_MANAGER_WINDOW,
        help="tmux window name for manager",
    )
    sp.add_argument(
        "--mount",
        dest="mount",
        action="append",
        default=None,
        help="Symlink a repo-root path into worker worktrees (repeatable): SRC[:DEST]",
    )
    sp.add_argument(
        "--clear-mounts",
        dest="clear_mounts",
        action="store_true",
        help="Clear persisted mounts for this run",
    )
    sp.add_argument(
        "--max-headcount",
        dest="max_headcount",
        type=int,
        default=None,
        help="Maximum active worker+investigator count (0 = unlimited). Persisted in run state.",
    )
    sp.add_argument(
        "--target-branch",
        dest="target_branch",
        default="",
        help="Ship destination branch (default: main)",
    )
    sp.add_argument(
        "--remote",
        default="",
        help="Git remote used for ship push (default: origin)",
    )
    push_grp0 = sp.add_mutually_exclusive_group()
    push_grp0.add_argument(
        "--push",
        dest="push",
        action="store_const",
        const=True,
        default=None,
        help="Enable push after successful ship (default)",
    )
    push_grp0.add_argument(
        "--no-push",
        dest="push",
        action="store_const",
        const=False,
        default=None,
        help="Disable push after successful ship",
    )
    sp.add_argument(
        "--force", action="store_true", help="Recreate manager window even if exists"
    )
    sp.set_defaults(func=cmd_start)

    st = sub.add_parser("status", help="Show run status")
    st.add_argument("team", help="Team name")
    st.add_argument(
        "--show-dead",
        dest="show_dead",
        action="store_true",
        help="Include dead/unsafe workers in the listing",
    )
    st.set_defaults(func=cmd_status)

    cap = sub.add_parser("capture", help="Capture recent pane output")
    cap.add_argument("team", help="Team name")
    cap.add_argument(
        "target",
        help="Target: manager | worker_id | ticket_id | window | worktree_key (e.g. merge-queue)",
    )
    cap.add_argument(
        "--lines", type=int, default=DEFAULT_AUTOCAPTURE_LINES, help="Number of lines"
    )
    cap.add_argument(
        "--header",
        action="store_true",
        help="Print a one-line capture header before output",
    )
    cap.add_argument(
        "--no-join",
        dest="no_join",
        action="store_true",
        help="Do not join wrapped lines in tmux output",
    )
    cap.set_defaults(func=cmd_capture)

    att = sub.add_parser("attach", help="Attach to the manager tmux session")
    att.add_argument("team", help="Team name (or tmux session name)")
    att.set_defaults(func=cmd_attach)

    snd = sub.add_parser(
        "send", help="Send a message to a target (durable inbox + best-effort tmux)"
    )
    snd.add_argument("team", help="Team name")
    snd.add_argument(
        "target",
        help="Target: manager | worker_id | ticket_id | window | worktree_key (e.g. merge-queue)",
    )
    snd.add_argument("message", nargs="?", default="", help="Message text")
    snd.add_argument(
        "--message",
        dest="message_opt",
        default="",
        help="Message text (alternative to positional)",
    )
    snd.add_argument(
        "--force",
        action="store_true",
        help="Allow send even if pane not recognized",
    )
    snd.set_defaults(func=cmd_send)

    obj = sub.add_parser(
        "objective",
        help="Show/update run objective (updates CHARTER + notifies manager)",
    )
    obj.add_argument("team", help="Team name")
    obj_sub = obj.add_subparsers(
        dest="objective_cmd", required=True, parser_class=TeamArgumentParser
    )

    obj_show = obj_sub.add_parser("show", help="Show current objective")
    obj_show.set_defaults(func=cmd_objective_show)

    obj_set = obj_sub.add_parser("set", help="Replace objective")
    obj_set.add_argument(
        "--message", default="", help="Objective text (or use --file/--stdin)"
    )
    obj_set.add_argument("--file", default="", help="Read objective text from file")
    obj_set.add_argument(
        "--stdin", action="store_true", help="Read objective text from stdin"
    )
    obj_set.add_argument(
        "--no-nudge", dest="nudge", action="store_false", help="Do not nudge via tmux"
    )
    obj_set.add_argument(
        "--force", action="store_true", help="Allow nudge even if pane not recognized"
    )
    obj_set.set_defaults(func=cmd_objective_set)

    obj_app = obj_sub.add_parser("append", help="Append an objective update")
    obj_app.add_argument("--message", default="", help="Objective update text")
    obj_app.add_argument("--file", default="", help="Read update text from file")
    obj_app.add_argument(
        "--stdin", action="store_true", help="Read update text from stdin"
    )
    obj_app.add_argument(
        "--no-nudge", dest="nudge", action="store_false", help="Do not nudge via tmux"
    )
    obj_app.add_argument(
        "--force", action="store_true", help="Allow nudge even if pane not recognized"
    )
    obj_app.set_defaults(func=cmd_objective_append)

    dn = sub.add_parser(
        "done",
        help="Check if run is fully done; optionally notify manager to disband",
    )
    dn.add_argument("team", help="Team name")
    dn.add_argument(
        "--notify",
        action="store_true",
        help="Queue a durable disband reminder to manager (and nudge)",
    )
    dn.add_argument(
        "--resend-after-s",
        type=float,
        default=DEFAULT_DISBAND_REMINDER_RESEND_S,
        help="If previous reminder was acked, resend only after this many seconds",
    )
    dn.set_defaults(func=cmd_done)

    jn = sub.add_parser(
        "janitor",
        help="Prune long-retired workers and stale run/worktrees (safe + conservative)",
    )
    jn.add_argument("team", help="Team name")
    jn.add_argument(
        "--older-than",
        default="7d",
        help="Only remove things older than this (e.g. 7d, 24h, 90m)",
    )
    jn.add_argument(
        "--dry-run", action="store_true", help="Report actions, do not modify"
    )
    jn.add_argument(
        "--keep-worktrees", action="store_true", help="Do not remove ws worktrees"
    )
    jn.add_argument(
        "--prune-orphans",
        action="store_true",
        help="Also remove unreferenced run/worktrees dirs (dangerous; opt-in)",
    )
    jn.add_argument(
        "--keep-retired-workers",
        action="store_true",
        help="Do not remove retired workers from run.json",
    )
    jn.set_defaults(func=cmd_janitor)

    add_wait_subcommand("wait", help="Block for a duration; wake early on inbox")
    add_wait_subcommand("snooze", help="Alias for `loom team wait`")

    shp = sub.add_parser("ship", help="Ship merge-queue into target branch")
    shp.add_argument("team", help="Team name")
    shp.add_argument(
        "--force-clean",
        action="store_true",
        help="Force-clean worktree before attempting ship",
    )
    push_grp2 = shp.add_mutually_exclusive_group()
    push_grp2.add_argument(
        "--push",
        dest="push",
        action="store_const",
        const=True,
        default=None,
        help="Push after successful ship",
    )
    push_grp2.add_argument(
        "--no-push",
        dest="push",
        action="store_const",
        const=False,
        default=None,
        help="Do not push after ship",
    )
    shp.set_defaults(func=cmd_ship)

    tui_cmd = sub.add_parser("tui", help="Internal: sidecar harness")
    tui_cmd.add_argument("project_dir", help="Project directory")
    tui_cmd.add_argument(
        "--harness",
        default=DEFAULT_HARNESS,
        choices=["opencode", "claude", "omp", "codex"],
        help="Agent harness (opencode, claude, omp, or codex)",
    )
    tui_cmd.add_argument(
        "--bin",
        default="",
        help="Override harness binary (wrapper/shim). Must be CLI-compatible with the selected harness",
    )
    tui_cmd.add_argument("--agent", default="", help="OpenCode agent")
    tui_cmd.add_argument("--model", default="", help="Model")
    tui_cmd.add_argument("--prompt", default="", help="Initial OpenCode prompt")
    tui_cmd.add_argument("--nudge-cooldown-s", type=float, default=300.0)
    tui_cmd.add_argument("--stall-threshold-s", type=float, default=1080.0)
    tui_cmd.add_argument(
        "--idle-screen-threshold-s", type=float, default=DEFAULT_IDLE_SCREEN_S
    )
    tui_cmd.add_argument("--respawn-cap", type=int, default=3)
    tui_cmd.add_argument("--respawn-window-s", type=float, default=3600.0)
    tui_cmd.add_argument(
        "--objective-nudge-s", type=float, default=DEFAULT_OBJECTIVE_NUDGE_S
    )
    tui_cmd.add_argument("--done-check-s", type=float, default=DEFAULT_DONE_CHECK_S)
    tui_cmd.add_argument(
        "--disband-resend-s", type=float, default=DEFAULT_DISBAND_REMINDER_RESEND_S
    )
    tui_cmd.set_defaults(func=cmd_tui)

    prm = sub.add_parser("prime", help="Operating manual + canonical examples")
    prm.set_defaults(func=cmd_prime)

    # Inbox: loom team inbox <TEAM> <cmd> ...
    ib = sub.add_parser("inbox", help="Disk-backed inbox (durable messages)")
    ib.add_argument("team", help="Team name")
    ib_sub = ib.add_subparsers(
        dest="inbox_cmd", required=True, parser_class=TeamArgumentParser
    )

    ib_list = ib_sub.add_parser("list", help="List inbox messages")
    ib_list.add_argument("--to", default="", help="Filter recipient")
    ib_list.add_argument("--unacked", action="store_true", help="Only show unacked")
    ib_list.add_argument("--limit", type=int, default=200, help="Max messages")
    ib_list.set_defaults(func=cmd_inbox_list)

    ib_show = ib_sub.add_parser("show", help="Show a message by id")
    ib_show.add_argument("msg_id", help="Message id")
    ib_show.set_defaults(func=cmd_inbox_show)

    ib_ack = ib_sub.add_parser("ack", help="Ack a message by id")
    ib_ack.add_argument("msg_id", help="Message id")
    ib_ack.set_defaults(func=cmd_inbox_ack)

    ib_send = ib_sub.add_parser(
        "send", help="Send a durable inbox message (optional tmux nudge)"
    )
    ib_send.add_argument(
        "--to", required=True, help="Recipient: manager | worker_id | ticket_id"
    )
    ib_send.add_argument("--message", required=True, help="Message body")
    ib_send.add_argument("--kind", default="note", help="Message kind tag")
    ib_send.add_argument("--sender", default="team", help="Sender label")
    ib_send.add_argument(
        "--no-nudge", dest="nudge", action="store_false", help="Do not nudge via tmux"
    )
    ib_send.add_argument(
        "--force", action="store_true", help="Allow nudge even if pane not recognized"
    )
    ib_send.set_defaults(func=cmd_inbox_send)

    # Merge queue primitives: loom team merge <TEAM> <cmd> ...
    mg = sub.add_parser("merge", help="Merge queue primitives (enqueue/next/done/list)")
    mg.add_argument("team", help="Team name")
    mg_sub = mg.add_subparsers(
        dest="merge_cmd", required=True, parser_class=TeamArgumentParser
    )

    mg_enq = mg_sub.add_parser("enqueue", help="Enqueue a branch for merge")
    mg_enq.add_argument("--branch", required=True, help="Branch/ref to merge")
    mg_enq.add_argument("--ticket", default="", help="Optional loom ticket id")
    mg_enq.add_argument(
        "--from-worker", default="", help="Optional originating worker id"
    )
    mg_enq.add_argument("--note", default="", help="Optional note")
    mg_enq.add_argument(
        "--no-nudge",
        dest="nudge",
        action="store_false",
        help="Do not nudge integrator",
    )
    mg_enq.set_defaults(func=cmd_merge_enqueue)

    mg_ls = mg_sub.add_parser("list", help="List merge queue items")
    mg_ls.add_argument("--all", action="store_true", help="Include completed items")
    mg_ls.set_defaults(func=cmd_merge_list)

    mg_next = mg_sub.add_parser("next", help="Claim next merge item")
    mg_next.add_argument("--claim-by", default="", help="Worker id claiming")
    mg_next.set_defaults(func=cmd_merge_next)

    mg_done = mg_sub.add_parser("done", help="Mark a merge item done")
    mg_done.add_argument("item_id", help="Merge item id")
    mg_done.add_argument("--result", required=True, help="merged|blocked|dropped")
    mg_done.add_argument("--note", default="", help="Optional result note")
    mg_done.set_defaults(func=cmd_merge_done)

    sm = sub.add_parser(
        "spawn-integrator", help="Spawn persistent integrator (ticketless)"
    )
    sm.add_argument("team", help="Team name")
    sm.add_argument("--worker-id", default="integrator", help="Worker id")
    sm.add_argument("--window", default="integrator", help="tmux window name")
    sm.add_argument(
        "--worktree", default="merge-queue", help="Worktree key under run/worktrees"
    )
    sm.add_argument(
        "--branch",
        default="",
        help="Local branch name for merge worktree (defaults to per-run merge branch)",
    )
    sm.add_argument(
        "--base-ref",
        default="",
        help="Base ref when creating the merge branch (defaults to target branch)",
    )
    sm.add_argument(
        "--force",
        action="store_true",
        help="Recreate integrator worktree + respawn window (dangerous)",
    )
    sm.add_argument(
        "--require-clean",
        dest="require_clean",
        action="store_true",
        help="Refuse to spawn if merge-queue worktree is dirty",
    )
    sm.add_argument(
        "--target-branch",
        default="",
        help="Target branch name (defaults to run config)",
    )
    sm.add_argument(
        "--remote",
        default="",
        help="Remote name (defaults to run config)",
    )
    push_grp = sm.add_mutually_exclusive_group()
    push_grp.add_argument(
        "--push",
        dest="push",
        action="store_const",
        const=True,
        default=None,
        help="Default push enabled",
    )
    push_grp.add_argument(
        "--no-push",
        dest="push",
        action="store_const",
        const=False,
        default=None,
        help="Default push disabled",
    )
    sm.set_defaults(func=cmd_spawn_integrator)

    doc = sub.add_parser(
        "doctor",
        help="Diagnose tmux/run-state drift and suggest remediation commands",
    )
    doc.add_argument("team", help="Team name")
    doc.set_defaults(func=cmd_doctor)

    dis = sub.add_parser(
        "disband", help="Kill tmux session + optionally remove worktrees"
    )
    dis.add_argument("team", help="Team name")
    dis.add_argument(
        "--remove-worktrees",
        action="store_true",
        help="Remove all run worktrees (dangerous; janitor is preferred)",
    )
    dis.add_argument(
        "--keep-state",
        action="store_true",
        help="Do not remove .loom/team run state",
    )
    dis.set_defaults(func=cmd_disband)

    pau = sub.add_parser(
        "pause", help="Pause a team run (stop tmux session; keep state)"
    )
    pau.add_argument("team", help="Team name")
    pau.set_defaults(func=cmd_pause)

    clk_out = sub.add_parser("clock-out", help="Alias for `loom team pause`")
    clk_out.add_argument("team", help="Team name")
    clk_out.set_defaults(func=cmd_pause)

    res = sub.add_parser(
        "resume", help="Resume a team run (restore manager + active workers)"
    )
    res.add_argument("team", help="Team name")
    res.set_defaults(func=cmd_resume)

    clk_in = sub.add_parser("clock-in", help="Alias for `loom team resume`")
    clk_in.add_argument("team", help="Team name")
    clk_in.set_defaults(func=cmd_resume)

    # Worker lifecycle
    spw = sub.add_parser(
        "spawn", help="Spawn a worker or investigator for a loom ticket"
    )
    spw.add_argument("team", help="Team name")
    spw.add_argument("ticket_id", help="loom ticket id")
    spw.add_argument(
        "--role",
        choices=[ROLE_WORKER, ROLE_INVESTIGATOR],
        default=ROLE_WORKER,
    )
    spw.add_argument("--worker-id", default="", help="Explicit worker id")
    spw.add_argument("--window", default="", help="tmux window name")
    spw.add_argument(
        "--worktree-key",
        dest="worktree_key",
        default="",
        help="Directory key under run/worktrees (defaults to ticket id)",
    )
    spw.add_argument(
        "--branch",
        default="",
        help="Override worktree branch (defaults to team/<ticket_id>)",
    )
    spw.add_argument("--base-ref", default="", help="Base ref for ws worktree ensure")
    spw.add_argument(
        "--resume",
        action="store_true",
        help="Resume a retired worker in its existing worktree (requires --worker-id)",
    )
    spw.set_defaults(func=cmd_spawn)

    ret = sub.add_parser("retire", help="Retire a worker pane (worktree preserved)")
    ret.add_argument("team", help="Team name")
    ret.add_argument("worker_id", help="Worker id")
    ret.set_defaults(func=cmd_retire)

    mr = sub.add_parser(
        "mark-retirable",
        help="Mark a retired worker worktree eligible for janitor deletion",
    )
    mr.add_argument("team", help="Team name")
    mr.add_argument("worker_id", help="Worker id")
    mr.set_defaults(func=cmd_mark_retirable)

    rs = sub.add_parser(
        "resume-worker", help="Resume a retired worker in its existing worktree"
    )
    rs.add_argument("team", help="Team name")
    rs.add_argument("worker_id", help="Worker id")
    rs.set_defaults(func=cmd_resume_worker)

    ps = sub.add_parser(
        "prep-sprint",
        help="Start a sprint (set sprint + create+spawn investigator prep ticket)",
    )
    ps.add_argument("team", help="Team name")
    ps.add_argument("--name", required=True, help="Sprint name (2-5 words)")
    ps.add_argument(
        "--force", action="store_true", help="Overwrite existing sprint name"
    )
    ps.add_argument(
        "--no-spawn",
        action="store_true",
        help="Do not spawn investigator (only set sprint and create ticket)",
    )
    ps.add_argument(
        "--type",
        dest="ticket_type",
        default="task",
        help="Ticket type for prep ticket (default: task)",
    )
    ps.add_argument(
        "--priority",
        type=int,
        default=1,
        help="Ticket priority for prep ticket (default: 1)",
    )
    ps.set_defaults(func=cmd_prep_sprint)

    spr = sub.add_parser("sprint", help="Sprint lifecycle commands")
    spr.add_argument("team", help="Team name")
    spr_sub = spr.add_subparsers(
        dest="sprint_cmd", required=True, parser_class=TeamArgumentParser
    )

    spr_show = spr_sub.add_parser("show", help="Show current sprint")
    spr_show.set_defaults(func=cmd_sprint_show)

    spr_set = spr_sub.add_parser("set", help="Set/Update sprint name and/or tag")
    spr_set.add_argument("--name", required=True, help="Sprint name")
    spr_set.add_argument("--tag", help="Sprint tag (default: sprint:<slug>)")
    spr_set.set_defaults(func=cmd_sprint_set)

    spr_clear = spr_sub.add_parser("clear", help="Clear current sprint")
    spr_clear.set_defaults(func=cmd_sprint_clear)

    bn = sub.add_parser(
        "bounce",
        help="Bounce a worker (SIGKILL child process; sidecar auto-respawns)",
    )
    bn.add_argument("team", help="Team name")
    bn.add_argument("target", help="Target: worker_id | ticket_id")
    bn.add_argument("--reason", default="", help="Optional reason (recorded)")
    bn.set_defaults(func=cmd_bounce)

    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv_list = list(argv) if argv is not None else sys.argv[1:]
    argv_list = _normalize_argv(argv_list)
    json_mode = "--json" in argv_list

    parser = build_parser()
    try:
        args = parser.parse_args(argv_list)
        args.func(args)
        return 0
    except ArgParseError as e:
        # Best-effort: suggest the closest subcommand.
        first = ""
        for tok in argv_list:
            if not tok.startswith("-"):
                first = tok
                break
        cmds = []
        with_suggestions: list[str] = []
        try:
            sub = next(
                a
                for a in parser._actions
                if isinstance(a, argparse._SubParsersAction)  # type: ignore[attr-defined]
            )
            cmds = sorted(list(sub.choices.keys()))
        except Exception:
            cmds = []
        if first and cmds and first not in cmds:
            with_suggestions = [f"loom team {c}" for c in _did_you_mean(first, cmds)]

        _emit_error(
            code="ARGPARSE",
            error=str(e),
            json_mode=json_mode,
            hint="Run `loom team -h` or `loom team <command> -h`.",
            suggestions=with_suggestions or ["loom team -h"],
            details={"argv": argv_list},
        )
        return 2
    except TeamError as e:
        hint = str(getattr(e, "hint", "") or "")
        suggestions = list(getattr(e, "suggestions", []) or [])
        details = getattr(e, "data", None)

        if not hint:
            if str(e.code) in {"ARG", "ARGPARSE"}:
                hint = "Run `loom team -h` or `loom team <command> -h`."
            else:
                hint = "Re-run with `--json` to capture details, then apply the suggested remediation."

        _emit_error(
            code=str(e.code),
            error=str(e),
            json_mode=json_mode,
            hint=hint,
            suggestions=suggestions,
            details=details
            if isinstance(details, dict)
            else ({"data": details} if details else None),
        )
        return int(getattr(e, "exit_code", 1) or 1)
    except KeyboardInterrupt:
        _emit_error(
            code="INTERRUPTED",
            error="Interrupted",
            json_mode=json_mode,
            hint="If this was accidental, re-run the command.",
        )
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
