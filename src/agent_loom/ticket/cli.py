import argparse
import contextlib
import difflib
import json
import os
import select
import stat
import sys
import uuid
from dataclasses import asdict
from pathlib import Path
from typing import Any, NoReturn, Optional, Sequence

from agent_loom.core.cli_output import emit_json, make_error_envelope, make_ok_envelope

import yaml

from agent_loom.core.git import git_repo_root
from agent_loom.core.time import utcnow
from agent_loom.ticket.constants import (
    AUDIT_LOGGER,
    AUDIT_MODE,
    SUBSYSTEM_NAME,
    TICKET_DIR_OVERRIDE,  # noqa: F401
)
from agent_loom.ticket.core import (
    add_note,
    blocked,
    claim,
    close,
    closed,
    create,
    default_agent_id,
    dep,
    dep_add,
    dep_cycle,
    dep_rm,
    find_tickets_dir,
    heartbeat,
    init,
    link,
    list_tickets,
    prime,
    query,
    ready,
    release,
    reopen,
    show,
    sprint_clear,
    sprint_set,
    sprint_show,
    start,
    status,
    swarm,
    sync,
    sync_external,
    unlink,
    update,
    version,
    view,
)
from agent_loom.ticket.models import TicketListResult, TicketShowResult
from agent_loom.ticket.normalize import (
    normalize_priority,
    normalize_status,
    normalize_ticket_ref,
)
from agent_loom.ticket.errors import TicketArgError, TicketUserErrorMixin
from agent_loom.ticket.store import AuditLogger, LockError, TicketStore


class ArgParseError(RuntimeError):
    pass


class TicketArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise ArgParseError(message)


def _arg_status(v: str) -> str:
    return normalize_status(v)


def _arg_status_optional(v: str) -> str:
    s = str(v or "")
    if not s.strip():
        return ""
    return normalize_status(s)


def _arg_ticket_ref(v: str) -> str:
    return normalize_ticket_ref(v)


def _arg_priority(v: str) -> int:
    try:
        return normalize_priority(v)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e)) from e


_WRITE_COMMANDS = {
    "init",
    "create",
    "status",
    "start",
    "close",
    "reopen",
    "dep-add",
    "dep-rm",
    "link",
    "unlink",
    "add-note",
    "note",
    "claim",
    "release",
    "heartbeat",
    "sync",
    "sync-external",
    "update",
}


def _should_audit_cmd(cmd: str) -> bool:
    if AUDIT_MODE == "off":
        return False
    if AUDIT_MODE == "writes":
        return cmd in _WRITE_COMMANDS
    return True


def _emit_json(obj: Any) -> None:
    if not isinstance(obj, dict):
        envelope = make_ok_envelope(obj)
    elif "ok" not in obj:
        envelope = {"ok": True, **obj}
    else:
        envelope = obj
    emit_json(envelope, minified=True)


def _emit_error(
    *,
    error: str,
    code: str,
    json_mode: bool,
    hint: str = "",
    suggestions: Optional[Sequence[str]] = None,
    details: Optional[dict[str, Any]] = None,
) -> None:
    if json_mode:
        envelope = make_error_envelope(
            error=error,
            code=code,
            hint=hint,
            suggestions=list(suggestions) if suggestions else None,
            details=dict(details) if details else None,
        )
        emit_json(envelope, minified=True)
        return
_VALUE_FLAGS = {"-p", "-m", "-a", "-T", "-N"}
_FLAG_ALIASES = {
    "--ticket-dir": "--tickets-dir",
    "--noaudit": "--no-audit",
    "--dryrun": "--dry-run",
}


def _normalize_argv(argv: list[str]) -> list[str]:
    """Normalize common plausible argv variants before argparse.

    This is agent UX: agents often guess flags like --ticket-dir, or glue short
    flags with values like -p1.
    """

    out: list[str] = []
    for tok in argv:
        if tok in _FLAG_ALIASES:
            out.append(_FLAG_ALIASES[tok])
            continue

        if tok.startswith(tuple(f + "=" for f in _FLAG_ALIASES)):
            for src, dst in _FLAG_ALIASES.items():
                if tok.startswith(src + "="):
                    out.append(dst + tok[len(src) :])
                    break
            else:
                out.append(tok)
            continue

        # Expand glued short flag values like -p1, -mmsg.
        if len(tok) > 2 and tok.startswith("-") and not tok.startswith("--"):
            flag = tok[:2]
            if flag in _VALUE_FLAGS:
                val = tok[2:]
                if val:
                    out.extend([flag, val])
                    continue

        out.append(tok)

    return out


def _did_you_mean(value: str, choices: Sequence[str]) -> list[str]:
    v = str(value or "").strip()
    if not v:
        return []
    return difflib.get_close_matches(v, list(choices), n=3, cutoff=0.6)




def _render_ticket_line(row: dict[str, Any]) -> str:
    bits = [
        f"- `{row.get('id', '')}`",
        f"P{row.get('priority', '')}",
        row.get("status", ""),
        "-",
        row.get("title", ""),
    ]
    extras: list[str] = []
    deps = row.get("deps") or []
    if deps:
        extras.append("deps:" + ",".join([str(x) for x in deps]))
    blockers = row.get("blockers") or []
    if blockers:
        extras.append("blockers:" + ",".join([str(x) for x in blockers]))
    claimed_by = row.get("claimed_by") or ""
    if claimed_by:
        extras.append("claim:" + str(claimed_by))
    mtime = row.get("mtime") or ""
    if mtime:
        extras.append("mtime:" + str(mtime))
    if extras:
        bits.append("(" + "; ".join(extras) + ")")
    return " ".join([b for b in bits if str(b).strip()])


def _render_list(title: str, result: TicketListResult) -> str:
    lines = [f"# {title} ({result.count})"]
    for row in result.tickets:
        lines.append(_render_ticket_line(asdict(row)))
    return "\n".join(lines).rstrip() + "\n"


def _render_show(result: TicketShowResult) -> str:
    t = result.ticket
    rel = result.relationships
    lines: list[str] = [f"# {t.id} - {t.title}", ""]
    meta: list[str] = []
    meta.append(f"- status: `{t.status}`")
    meta.append(f"- priority: `P{t.priority}`")
    if t.type:
        meta.append(f"- type: `{t.type}`")
    if t.assignee:
        meta.append(f"- assignee: `{t.assignee}`")
    if t.tags:
        meta.append("- tags: " + ", ".join([f"`{x}`" for x in t.tags]))
    if t.deps:
        meta.append("- deps: " + ", ".join([f"`{x}`" for x in t.deps]))
    if t.external_ref:
        meta.append(f"- external_ref: `{t.external_ref}`")
    if t.parent:
        meta.append(f"- parent: `{t.parent}`")
    if t.claimed_by:
        meta.append(f"- claimed_by: `{t.claimed_by}`")
    if rel.blockers:
        meta.append("- blockers: " + ", ".join([f"`{x}`" for x in rel.blockers]))
    lines.extend(meta)

    lines.append("")
    lines.append("## Relationships")
    if rel.blockers:
        lines.append("- blockers: " + ", ".join([f"`{x}`" for x in rel.blockers]))
    if rel.blocking:
        lines.append("- blocking: " + ", ".join([f"`{x}`" for x in rel.blocking]))
    if rel.children:
        lines.append("- children: " + ", ".join([f"`{x}`" for x in rel.children]))
    if rel.linked:
        lines.append("- linked: " + ", ".join([f"`{x}`" for x in rel.linked]))

    lines.append("")
    lines.append("## Body")
    lines.append("")
    body = result.body.lstrip("\n")
    lines.append(body.rstrip())
    return "\n".join(lines).rstrip() + "\n"


def _render_prime_text(payload: dict[str, Any]) -> str:
    md: list[str] = []
    md.append(f"# loom ticket (v{payload['tool']['version']})")
    md.append("")
    md.append("Run `loom ticket -h` to see every command and flag.")
    md.append("Run `loom ticket <command> -h` for command-specific help.")
    md.append("")
    md.append("## Purpose")
    md.append(f"- {payload['purpose']}")
    md.append("")
    md.append("## Storage")
    md.extend([f"- {k}: `{v}`" for k, v in payload["storage"].items()])
    md.append("")
    md.append("## Output")
    md.append(f"- default: {payload['output']['default']}")
    md.append(f"- json: {payload['output']['json']}")
    md.append("")
    md.append("## Concurrency")
    md.append(f"- {payload['concurrency']['claims']}")
    md.append(f"- {payload['concurrency']['enforcement']}")
    md.append("")
    md.append("## Environment")
    md.extend([f"- `{k}`: {v}" for k, v in payload["env"].items()])
    md.append("")
    md.append("## Zen")
    md.extend([f"- {x}" for x in payload["zen"]])
    md.append("")
    md.append("## Copy/paste")
    md.extend(payload["examples"]["copy_paste_for_agents_md"])
    md.append("")
    md.append("## Schema (frontmatter keys)")
    md.append("```yaml")
    md.append(
        yaml.safe_dump(payload["schema"]["frontmatter"], sort_keys=False).rstrip()
    )
    md.append("```")
    md.append("")
    md.append("## Canonical examples")
    for section, cmds in payload["examples"].items():
        if section == "copy_paste_for_agents_md":
            continue
        md.append(f"### {section}")
        md.extend([f"- `{c}`" for c in cmds])
        md.append("")
    return "\n".join(md).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    common = TicketArgumentParser(add_help=False)
    common.add_argument(
        "--json",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Emit machine-readable JSON",
    )
    common.add_argument(
        "--tickets-dir",
        dest="tickets_dir",
        default=argparse.SUPPRESS,
        help="Override tickets directory (absolute or repo-root-relative)",
    )
    common.add_argument(
        "--no-audit",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Disable audit logging",
    )
    common.add_argument(
        "--audit-writes-only",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Only audit write commands",
    )

    p = TicketArgumentParser(prog=SUBSYSTEM_NAME, add_help=True, parents=[common])
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("version", parents=[common], help="Print version")
    sub.add_parser("init", parents=[common], help="Initialize .loom/ticket")

    sp = sub.add_parser("create", parents=[common], help="Create a ticket")
    sp.add_argument("title_pos", nargs="?", default=None, metavar="title")
    sp.add_argument(
        "--title",
        default=None,
        help="Ticket title (alternative to positional title)",
    )
    sp.add_argument("-d", "--description", default="")
    sp.add_argument("--design", default="")
    sp.add_argument("--acceptance", default="")
    sp.add_argument("-t", "--type", default="task")
    sp.add_argument(
        "-p",
        "--priority",
        type=_arg_priority,
        default=2,
        help="Priority: 0..4, P0..P4, or critical|high|medium|low|trivial",
    )
    sp.add_argument("-a", "--assignee", default="")
    sp.add_argument("--external-ref", dest="external_ref", default="")
    sp.add_argument("--parent", default="")
    sp.add_argument("--tags", default="")
    sp.add_argument(
        "--no-sprint-tag",
        dest="no_sprint_tag",
        action="store_true",
        help="Do not auto-add sprint tag from ticket sprint context or TEAM_SPRINT_TAG",
    )

    sp = sub.add_parser("sprint", parents=[common], help="Manage sprint context")
    spr_sub = sp.add_subparsers(dest="sprint_cmd", required=True)

    spr_sub.add_parser("show", help="Show configured sprint context")

    spr_set = spr_sub.add_parser("set", help="Set sprint context")
    spr_set.add_argument("--name", required=True, help="Sprint name")
    spr_set.add_argument("--tag", required=True, help="Sprint tag")

    spr_sub.add_parser("clear", help="Clear sprint context")

    sp = sub.add_parser("status", parents=[common], help="Set ticket status")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("new_status", type=_arg_status)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("start", parents=[common], help="Set status=in_progress")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("close", parents=[common], help="Set status=closed")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("reopen", parents=[common], help="Set status=open")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("list", parents=[common], help="List tickets")
    sp.add_argument("--status", default="")
    sp.add_argument("--type", default="")
    sp.add_argument("--priority", type=_arg_priority, default=None)
    sp.add_argument("--prio-min", dest="prio_min", type=_arg_priority, default=None)
    sp.add_argument("--prio-max", dest="prio_max", type=_arg_priority, default=None)
    sp.add_argument("-a", "--assignee", default="")
    sp.add_argument("-T", "--tag", default="")
    sp.add_argument("--all", action="store_true", help="Include closed")
    sp.add_argument(
        "-N",
        "--limit",
        type=int,
        default=0,
        help="Maximum tickets to return (0 = unlimited)",
    )

    sp = sub.add_parser("ls", parents=[common], help="Alias for list")
    sp.add_argument("--status", default="")
    sp.add_argument("--type", default="")
    sp.add_argument("--priority", type=_arg_priority, default=None)
    sp.add_argument("--prio-min", dest="prio_min", type=_arg_priority, default=None)
    sp.add_argument("--prio-max", dest="prio_max", type=_arg_priority, default=None)
    sp.add_argument("-a", "--assignee", default="")
    sp.add_argument("-T", "--tag", default="")
    sp.add_argument("--all", action="store_true", help="Include closed")
    sp.add_argument(
        "-N",
        "--limit",
        type=int,
        default=0,
        help="Maximum tickets to return (0 = unlimited)",
    )

    sp = sub.add_parser("ready", parents=[common], help="List ready tickets")
    sp.add_argument("--type", default="")
    sp.add_argument("--priority", type=_arg_priority, default=None)
    sp.add_argument("--prio-min", dest="prio_min", type=_arg_priority, default=None)
    sp.add_argument("--prio-max", dest="prio_max", type=_arg_priority, default=None)
    sp.add_argument("-a", "--assignee", default="")
    sp.add_argument("-T", "--tag", default="")
    sp.add_argument(
        "-N",
        "--limit",
        type=int,
        default=0,
        help="Maximum tickets to return (0 = unlimited)",
    )

    sp = sub.add_parser("blocked", parents=[common], help="List blocked tickets")
    sp.add_argument("-a", "--assignee", default="")
    sp.add_argument("-T", "--tag", default="")

    sp = sub.add_parser(
        "closed", parents=[common], help="List recently modified closed"
    )
    sp.add_argument("--limit", type=int, default=20)
    sp.add_argument("-a", "--assignee", default="")
    sp.add_argument("-T", "--tag", default="")

    sp = sub.add_parser("show", parents=[common], help="Show a ticket")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--raw", action="store_true")

    sp = sub.add_parser("update", parents=[common], help="Atomically update a ticket")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--title", default="")
    sp.add_argument("--status", type=_arg_status_optional, default="")
    sp.add_argument("--priority", type=_arg_priority, default=None)
    sp.add_argument("--type", default="")
    sp.add_argument("--assignee", default="")
    sp.add_argument("--tags", default=None)
    sp.add_argument("--external-ref", dest="external_ref", default=None)
    sp.add_argument(
        "--parent",
        default=None,
        help="Set parent ticket (id/ref). Use 'none' to clear.",
    )
    sp.add_argument(
        "--remove-parent",
        action="store_true",
        help="Clear parent ticket (equivalent to --parent none).",
    )
    sp.add_argument(
        "--deps",
        default=None,
        help="Replace deps list (comma/space separated ids/refs). Use 'none' to clear.",
    )
    sp.add_argument(
        "--add-dep",
        action="append",
        default=[],
        dest="add_deps",
        help="Add a dependency (repeatable).",
    )
    sp.add_argument(
        "--remove-dep",
        action="append",
        default=[],
        dest="remove_deps",
        help="Remove a dependency (repeatable).",
    )
    sp.add_argument(
        "--links",
        default=None,
        help="Replace links list (comma/space separated ids/refs). Use 'none' to clear.",
    )
    sp.add_argument(
        "--add-link",
        action="append",
        default=[],
        dest="add_links",
        help="Add a link to another ticket (repeatable).",
    )
    sp.add_argument(
        "--remove-link",
        action="append",
        default=[],
        dest="remove_links",
        help="Remove a link to another ticket (repeatable).",
    )
    sp.add_argument("--body", default=None)
    sp.add_argument(
        "--add-note",
        nargs="?",
        default=None,
        const="",
        help="Alias for `add-note` (value or stdin). Not compatible with other update fields.",
    )
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("add-note", parents=[common], help="Append a note")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("note", nargs="?", default="")
    sp.add_argument(
        "--note",
        "--body",
        dest="note_flag",
        default=None,
        help="Note body (alternative to positional note; stdin also supported)",
    )
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("note", parents=[common], help="Alias for add-note")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("note", nargs="?", default="")
    sp.add_argument(
        "--note",
        "--body",
        dest="note_flag",
        default=None,
        help="Note body (alternative to positional note; stdin also supported)",
    )
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("dep", parents=[common], help="Show dependency tree")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--max-depth", type=int, default=0)

    sp = sub.add_parser("dep-add", parents=[common], help="Add dependency")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("dependency", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("dep-rm", parents=[common], help="Remove dependency")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("dependency", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sub.add_parser("dep-cycle", parents=[common], help="Find dep cycles")

    sp = sub.add_parser("link", parents=[common], help="Link tickets")
    sp.add_argument("tickets", nargs="+", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("unlink", parents=[common], help="Unlink tickets")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("target", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("view", parents=[common], help="Orchestration view")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--max-depth", type=int, default=0)

    sp = sub.add_parser("claim", parents=[common], help="Claim a ticket")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--ttl", default="30m")
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("heartbeat", parents=[common], help="Heartbeat for claim")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--extend", dest="extend", action="store_true", default=True)
    sp.add_argument("--no-extend", dest="extend", action="store_false")

    sp = sub.add_parser("release", parents=[common], help="Release claim")
    sp.add_argument("ticket", type=_arg_ticket_ref)
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("swarm", parents=[common], help="Show swarm activity")
    sp.add_argument("--active-within", default="2h")

    sp = sub.add_parser(
        "sync", parents=[common], help="Stage+commit .loom/ticket changes"
    )
    sp.add_argument(
        "-m",
        "--message",
        default="chore: tickets",
        help="Commit message (default: chore: tickets)",
    )

    sp = sub.add_parser("sync-external", parents=[common], help="Sync external refs")
    sp.add_argument("ticket", nargs="?", default="")
    sp.add_argument("--dry-run", action="store_true")
    sp.add_argument("--force", action="store_true")

    sp = sub.add_parser("query", parents=[common], help="Dump tickets")
    sp.add_argument("jmes", nargs="?", default="")
    sp.add_argument("--format", default="jsonl", choices=["jsonl", "json", "yaml"])

    sub.add_parser("prime", parents=[common], help="Print ticket cookbook")

    return p


def _maybe_read_stdin() -> Optional[str]:
    if sys.stdin is None or sys.stdin.isatty():
        return None

    try:
        st_mode = os.fstat(sys.stdin.fileno()).st_mode
    except Exception:
        return None

    # Only read when stdin is a pipe or file (common shell piping patterns).
    if not (stat.S_ISFIFO(st_mode) or stat.S_ISREG(st_mode)):
        return None

    # Avoid blocking on pipes when no data is available.
    if stat.S_ISFIFO(st_mode):
        try:
            ready, _, _ = select.select([sys.stdin], [], [], 0)
        except Exception:
            return None
        if not ready:
            return None

    try:
        return sys.stdin.read()
    except Exception:
        return None


def _configure_audit(
    args: argparse.Namespace,
    *,
    cmd: str,
    cwd: Path,
    argv_list: list[str],
    json_mode: bool,
) -> None:
    global AUDIT_MODE, AUDIT_LOGGER, TICKET_DIR_OVERRIDE

    mode = (os.getenv("TK_AUDIT_MODE") or "").strip().lower()
    if mode in {"off", "0", "false"}:
        AUDIT_MODE = "off"
    elif mode in {"writes", "write"}:
        AUDIT_MODE = "writes"
    else:
        AUDIT_MODE = "all"

    if getattr(args, "no_audit", False) is True:
        AUDIT_MODE = "off"
    if getattr(args, "audit_writes_only", False) is True and AUDIT_MODE != "off":
        AUDIT_MODE = "writes"

    if hasattr(args, "tickets_dir"):
        TICKET_DIR_OVERRIDE = str(getattr(args, "tickets_dir") or "").strip() or None

    repo_root = git_repo_root(cwd)
    tickets_dir: Optional[Path] = None
    if cmd:
        with contextlib.suppress(Exception):
            tickets_dir = find_tickets_dir(cmd, cwd)

    if tickets_dir is not None and _should_audit_cmd(cmd):
        AUDIT_LOGGER = AuditLogger(
            tickets_dir=tickets_dir,
            run_id=uuid.uuid4().hex,
            agent_id=default_agent_id(),
            cwd=cwd,
            repo_root=repo_root,
            argv=argv_list,
            audit_mode=AUDIT_MODE,
            json_mode=json_mode,
        )
        AUDIT_LOGGER.log({"event": "cmd_start", "cmd": cmd})


def _finalize_audit(cmd: str, *, started_at: Any) -> None:
    global AUDIT_LOGGER

    if AUDIT_LOGGER is not None and _should_audit_cmd(cmd):
        duration_ms = int((utcnow() - started_at).total_seconds() * 1000)
        AUDIT_LOGGER.log({"event": "cmd_end", "cmd": cmd, "duration_ms": duration_ms})

    AUDIT_LOGGER = None


def _handle_query_output(obj: Any, *, fmt: str, json_mode: bool) -> int:
    if fmt == "jsonl":
        if isinstance(obj, list):
            for item in obj:
                sys.stdout.write(
                    json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n"
                )
        else:
            sys.stdout.write(
                json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"
            )
        return 0
    if fmt == "json":
        if json_mode:
            _emit_json(obj)
        else:
            sys.stdout.write(
                json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n"
            )
        return 0
    if fmt == "yaml":
        if json_mode:
            _emit_error(
                error="`--json` output cannot be YAML",
                code="ARG",
                json_mode=True,
                hint="Use `--format jsonl` or `--format json`, or drop `--json` for YAML.",
            )
            raise SystemExit(2)
        sys.stdout.write(yaml.safe_dump(obj, sort_keys=False))
        if not str(obj).endswith("\n"):
            sys.stdout.write("\n")
        return 0
    raise ValueError("format must be one of: jsonl|json|yaml")


def _emit_list_result(title: str, result: TicketListResult, *, json_mode: bool) -> None:
    if json_mode:
        _emit_json(asdict(result))
    else:
        sys.stdout.write(_render_list(title, result))


def _handle_version(_args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = version()
    payload = {"tool": {"name": response.name, "version": response.version}}
    if json_mode:
        _emit_json(payload)
    else:
        sys.stdout.write(f"{response.name} {response.version}\n")
    return 0


def _handle_init(_args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = init()
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Initialized {response.initialized}\n")
    return 0


def _handle_create(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    title_flag = str(getattr(args, "title", "") or "").strip()
    title_pos = str(getattr(args, "title_pos", "") or "").strip()
    if title_flag and title_pos and title_flag != title_pos:
        raise TicketArgError(
            code="ARG",
            error="Title provided twice and differs",
            hint=f"positional={title_pos!r}, --title={title_flag!r}. Use one (recommended: --title).",
            suggestions=["loom ticket create --title 'Your title'"],
            details={"positional": title_pos, "flag": title_flag},
        )
    title = title_flag or title_pos or "Untitled"

    response = create(
        title=title,
        type=args.type,
        priority=int(args.priority),
        tags=args.tags or "",
        include_sprint_tag=not bool(getattr(args, "no_sprint_tag", False)),
        assignee=args.assignee or "",
        external_ref=args.external_ref or "",
        parent=args.parent or "",
        description=args.description or "",
        design=args.design or "",
        acceptance=args.acceptance or "",
    )
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"{response.id}\n")
    return 0


def _handle_status(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = status(
        ticket=args.ticket, new_status=args.new_status, force=bool(args.force)
    )
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Updated {response.id} -> {response.status}\n")
    return 0


def _handle_start(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = start(ticket=args.ticket, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Updated {response.id} -> {response.status}\n")
    return 0


def _handle_close(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = close(ticket=args.ticket, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Updated {response.id} -> {response.status}\n")
    return 0


def _handle_reopen(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = reopen(ticket=args.ticket, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Updated {response.id} -> {response.status}\n")
    return 0


def _handle_sprint(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    sprint_cmd = str(getattr(args, "sprint_cmd", "") or "")
    if sprint_cmd == "show":
        response = sprint_show()
    elif sprint_cmd == "set":
        response = sprint_set(name=args.name, tag=args.tag)
    elif sprint_cmd == "clear":
        response = sprint_clear()
    else:
        raise TicketArgError(
            code="ARG",
            error=f"Unknown sprint command: {sprint_cmd}",
            hint="Run `loom ticket sprint -h`.",
            suggestions=["loom ticket sprint -h"],
            details={"sprint_cmd": sprint_cmd},
        )

    if json_mode:
        _emit_json(asdict(response))
    else:
        if sprint_cmd == "clear":
            sys.stdout.write("Sprint context cleared\n")
        elif response.name or response.tag:
            sys.stdout.write(f"name: {response.name}\ntag: {response.tag}\n")
        else:
            sys.stdout.write("No sprint context set\n")
    return 0

def _handle_list(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = list_tickets(
        status=args.status,
        type=args.type,
        priority=args.priority,
        prio_min=args.prio_min,
        prio_max=args.prio_max,
        assignee=args.assignee,
        tag=args.tag,
        include_closed=bool(args.all),
        limit=int(getattr(args, "limit", 0) or 0),
    )
    _emit_list_result("Tickets", response, json_mode=json_mode)
    return 0


def _handle_ready(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = ready(
        type=args.type,
        priority=args.priority,
        prio_min=args.prio_min,
        prio_max=args.prio_max,
        assignee=args.assignee,
        tag=args.tag,
        limit=int(getattr(args, "limit", 0) or 0),
    )
    _emit_list_result("Ready", response, json_mode=json_mode)
    return 0


def _handle_blocked(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = blocked(assignee=args.assignee, tag=args.tag)
    _emit_list_result("Blocked", response, json_mode=json_mode)
    return 0


def _handle_closed(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = closed(limit=int(args.limit), assignee=args.assignee, tag=args.tag)
    _emit_list_result("Closed", response, json_mode=json_mode)
    return 0


def _handle_show(args: argparse.Namespace, json_mode: bool, cwd: Path) -> int:
    if bool(args.raw) and not json_mode:
        store = TicketStore(find_tickets_dir("show", cwd))
        t = store.load_ticket(args.ticket)
        sys.stdout.write(t.path.read_text(encoding="utf-8"))
        return 0
    response = show(ticket=args.ticket)
    if json_mode:
        payload = {
            "ticket": asdict(response.ticket),
            "relationships": asdict(response.relationships),
            "body": response.body,
            "frontmatter": response.frontmatter,
            "lease": response.lease,
        }
        _emit_json(payload)
    else:
        sys.stdout.write(_render_show(response))
    return 0


def _handle_update(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    if args.add_note is not None:
        # Agentic UX alias: accept `update <id> --add-note ...` as `add-note`.
        # Keep this strict: do not mix with other update fields.
        has_other = any(
            [
                bool(args.title),
                bool(args.status),
                args.priority is not None,
                bool(args.type),
                bool(args.assignee),
                args.tags is not None,
                args.external_ref is not None,
                args.parent is not None,
                bool(args.remove_parent),
                args.deps is not None,
                bool(args.add_deps),
                bool(args.remove_deps),
                args.links is not None,
                bool(args.add_links),
                bool(args.remove_links),
                args.body is not None,
            ]
        )
        if has_other:
            raise TicketArgError(
                code="ARG",
                error="`update --add-note` cannot be combined with other update fields",
                hint="Use `loom ticket add-note` for notes, and run `loom ticket update` separately for atomic field edits.",
                suggestions=[
                    "loom ticket add-note <id> 'Progress update...'",
                    "loom ticket update <id> --status in_progress",
                ],
            )

        note = str(args.add_note or "")
        if not note:
            note = _maybe_read_stdin() or ""
        response = add_note(ticket=args.ticket, note=note, force=bool(args.force))
        if json_mode:
            _emit_json(asdict(response))
        else:
            sys.stdout.write(f"Note added to {response.id}\n")
        return 0

    body = args.body
    if body is None:
        body = _maybe_read_stdin()
    response = update(
        ticket=args.ticket,
        title=args.title or None,
        status=args.status or "",
        priority=args.priority,
        type=args.type or "",
        assignee=args.assignee or "",
        tags=args.tags,
        external_ref=args.external_ref,
        parent=args.parent,
        remove_parent=bool(args.remove_parent),
        deps=args.deps,
        add_deps=list(getattr(args, "add_deps", []) or []),
        remove_deps=list(getattr(args, "remove_deps", []) or []),
        links=args.links,
        add_links=list(getattr(args, "add_links", []) or []),
        remove_links=list(getattr(args, "remove_links", []) or []),
        body=body,
        force=bool(args.force),
    )
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Updated {response.id}\n")
    return 0


def _handle_add_note(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    note_pos = str(getattr(args, "note", "") or "")
    note_flag_raw = getattr(args, "note_flag", None)
    note_flag = str(note_flag_raw or "")
    if (
        note_pos.strip()
        and note_flag_raw is not None
        and note_flag.strip()
        and note_pos != note_flag
    ):
        raise TicketArgError(
            code="ARG",
            error="Note provided twice and differs",
            hint="Use either the positional note or `--note/--body` (recommended: --note).",
            suggestions=["loom ticket add-note <id> --note 'your note'"],
            details={"positional": note_pos, "flag": note_flag},
        )

    note = note_pos or note_flag
    if not note:
        note = _maybe_read_stdin() or ""
    response = add_note(ticket=args.ticket, note=note, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Note added to {response.id}\n")
    return 0


def _handle_dep(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = dep(ticket=args.ticket)
    if json_mode:
        payload = {
            "root": response.root,
            "nodes": response.nodes,
            "edges": [asdict(e) for e in response.edges],
            "health": asdict(response.health),
        }
        _emit_json(payload)
    else:
        lines = [f"# Dependency tree: {response.root}", "", "```text"]
        lines.extend(response.nodes)
        lines.append("```")
        sys.stdout.write("\n".join(lines).rstrip() + "\n")
    return 0


def _handle_dep_add(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = dep_add(
        ticket=args.ticket, dependency=args.dependency, force=bool(args.force)
    )
    if json_mode:
        _emit_json(asdict(response))
    else:
        if response.changed:
            sys.stdout.write(
                f"Added dependency: {response.id} -> {response.dependency}\n"
            )
        else:
            sys.stdout.write("Dependency already exists\n")
    return 0


def _handle_dep_rm(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = dep_rm(
        ticket=args.ticket, dependency=args.dependency, force=bool(args.force)
    )
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(
            f"Removed dependency: {response.id} -/-> {response.dependency}\n"
        )
    return 0


def _handle_dep_cycle(_args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = dep_cycle()
    if json_mode:
        _emit_json(asdict(response))
    else:
        if not response.cycles:
            sys.stdout.write("No dependency cycles found\n")
        else:
            lines = [f"# Dependency cycles ({len(response.cycles)})"]
            for cyc in response.cycles:
                lines.append(
                    "- " + " -> ".join([f"`{x}`" for x in cyc] + [f"`{cyc[0]}`"])
                )
            sys.stdout.write("\n".join(lines).rstrip() + "\n")
    return 0


def _handle_link(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = link(tickets=list(args.tickets), force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        if response.changed == 0:
            sys.stdout.write("All links already exist\n")
        else:
            sys.stdout.write(
                f"Added {response.changed} link(s) between {len(response.ids)} tickets\n"
            )
    return 0


def _handle_unlink(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = unlink(ticket=args.ticket, target=args.target, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Removed link: {response.id} <-> {response.target}\n")
    return 0


def _handle_view(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = view(ticket=args.ticket)
    if json_mode:
        payload = {
            "ticket": asdict(response.ticket),
            "graph": {
                "nodes": response.graph.nodes,
                "edges": [asdict(e) for e in response.graph.edges],
            },
            "health": asdict(response.health),
        }
        _emit_json(payload)
    else:
        lines = [f"# View: {response.ticket.id} - {response.ticket.title}", ""]
        lines.append(f"- status: `{response.ticket.status}`")
        lines.append(f"- priority: `P{response.ticket.priority}`")
        lines.append("")
        lines.append("## Graph")
        lines.append("```text")
        lines.extend(response.graph.nodes)
        lines.append("```")
        sys.stdout.write("\n".join(lines).rstrip() + "\n")
    return 0


def _handle_claim(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = claim(ticket=args.ticket, ttl=args.ttl, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(
            f"Claimed {response.id} as {response.claimed_by} (ttl {args.ttl})\n"
        )
    return 0


def _handle_heartbeat(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = heartbeat(ticket=args.ticket, extend=bool(args.extend))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Heartbeat updated for {response.id}\n")
    return 0


def _handle_release(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = release(ticket=args.ticket, force=bool(args.force))
    if json_mode:
        _emit_json(asdict(response))
    else:
        sys.stdout.write(f"Released {response.id}\n")
    return 0


def _handle_swarm(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = swarm(active_within=args.active_within)
    if json_mode:
        _emit_json(asdict(response))
    else:
        if not response.agents:
            sys.stdout.write("No active claims\n")
        else:
            lines = [f"# Swarm ({len(response.agents)})"]
            for agent in response.agents:
                active = "active" if agent.active else "idle"
                claims = ",".join(agent.claims)
                lines.append(
                    f"- `{agent.agent}` {active} (last:{agent.last_heartbeat}) (claims:{claims})"
                )
            sys.stdout.write("\n".join(lines).rstrip() + "\n")
    return 0


def _handle_sync(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = sync(message=args.message)
    if json_mode:
        _emit_json(asdict(response))
    else:
        if not response.committed:
            sys.stdout.write("No ticket changes\n")
        else:
            sys.stdout.write(f"Committed {response.count} ticket(s): {response.sha}\n")
            for p in response.files:
                sys.stdout.write(f"- `{p}`\n")
    return 0


def _handle_sync_external(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = sync_external(
        ticket=args.ticket,
        dry_run=bool(args.dry_run),
        force=bool(args.force),
    )
    if json_mode:
        _emit_json(asdict(response))
    else:
        lines = [f"# Sync External ({len(response.results)})"]
        for r in response.results:
            ok = "ok" if r.ok else "err"
            note = r.note or r.error or ("changed" if r.changed else "")
            lines.append(f"- `{r.id}` {ok} `{r.external_ref}` {note}")
        sys.stdout.write("\n".join(lines).rstrip() + "\n")
    return 0


def _handle_query(args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = query(jmes=args.jmes)
    return _handle_query_output(response.result, fmt=args.format, json_mode=json_mode)


def _handle_prime(_args: argparse.Namespace, json_mode: bool, _cwd: Path) -> int:
    response = prime()
    if json_mode:
        _emit_json(asdict(response))
    else:
        text = str(response.payload.get("markdown") or "")
        if text:
            sys.stdout.write(text.rstrip() + "\n")
    return 0


def _dispatch(cmd: str, args: argparse.Namespace, *, json_mode: bool, cwd: Path) -> int:
    handlers = {
        "version": _handle_version,
        "init": _handle_init,
        "create": _handle_create,
        "status": _handle_status,
        "start": _handle_start,
        "close": _handle_close,
        "reopen": _handle_reopen,
        "sprint": _handle_sprint,
        "list": _handle_list,
        "ls": _handle_list,
        "ready": _handle_ready,
        "blocked": _handle_blocked,
        "closed": _handle_closed,
        "show": _handle_show,
        "update": _handle_update,
        "add-note": _handle_add_note,
        "note": _handle_add_note,
        "dep": _handle_dep,
        "dep-add": _handle_dep_add,
        "dep-rm": _handle_dep_rm,
        "dep-cycle": _handle_dep_cycle,
        "link": _handle_link,
        "unlink": _handle_unlink,
        "view": _handle_view,
        "claim": _handle_claim,
        "heartbeat": _handle_heartbeat,
        "release": _handle_release,
        "swarm": _handle_swarm,
        "sync": _handle_sync,
        "sync-external": _handle_sync_external,
        "query": _handle_query,
        "prime": _handle_prime,
    }
    handler = handlers.get(cmd)
    if not handler:
        hints = _did_you_mean(cmd, list(handlers.keys()))
        raise TicketArgError(
            code="ARG",
            error=f"Unknown command: {cmd}",
            hint=("Did you mean: " + ", ".join(hints))
            if hints
            else "Run `loom ticket -h`.",
            suggestions=["loom ticket -h"],
            details={"cmd": cmd, "known": sorted(list(handlers.keys()))},
        )
    return handler(args, json_mode, cwd)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    cmd = ""
    json_mode = False
    started_at = utcnow()
    argv_list = list(argv) if argv is not None else sys.argv[1:]
    argv_list = _normalize_argv(argv_list)
    cwd = Path.cwd().resolve()

    try:
        args = parser.parse_args(argv_list)
        cmd = str(getattr(args, "cmd", "") or "")
        json_mode = bool(getattr(args, "json", False))

        _configure_audit(
            args, cmd=cmd, cwd=cwd, argv_list=argv_list, json_mode=json_mode
        )

        if not cmd:
            if json_mode:
                _emit_error(
                    error="Missing command",
                    code="ARGPARSE",
                    json_mode=True,
                    hint="Run `loom ticket -h` to see available commands.",
                )
                raise SystemExit(2)
            parser.print_help()
            return 2

        return _dispatch(cmd, args, json_mode=json_mode, cwd=cwd)
    except TicketUserErrorMixin as e:
        _emit_error(
            error=str(e.error),
            code=str(e.code),
            json_mode=json_mode,
            hint=str(getattr(e, "hint", "") or ""),
            suggestions=list(getattr(e, "suggestions", ()) or ()),
            details=dict(getattr(e, "details", {}) or {}),
        )
        raise SystemExit(2)
    except ArgParseError as e:
        msg = str(e)
        _emit_error(
            error=msg,
            code="ARGPARSE",
            json_mode=json_mode,
            hint="Run `loom ticket -h` or `loom ticket <command> -h`.",
        )
        raise SystemExit(2)
    except FileNotFoundError as e:
        _emit_error(
            error=str(e),
            code="NOT_FOUND",
            json_mode=json_mode,
            hint="Run `loom ticket list` to see tickets, or `loom ticket init` to create `.loom/ticket/`.",
        )
        raise SystemExit(2)
    except PermissionError as e:
        _emit_error(
            error=str(e),
            code="PERMISSION",
            json_mode=json_mode,
            hint="If claims are enforced, run `loom ticket claim <id>` (or pass `--force`).",
        )
        raise SystemExit(2)
    except LockError as e:
        _emit_error(
            error=str(e),
            code="LOCK",
            json_mode=json_mode,
            hint="Another process is writing. Retry shortly; if stuck, remove the lock file.",
        )
        raise SystemExit(2)
    except ValueError as e:
        _emit_error(
            error=str(e),
            code="ARG",
            json_mode=json_mode,
            hint="Run `loom ticket -h` or `loom ticket <command> -h`.",
        )
        raise SystemExit(2)
    except SystemExit:
        raise
    except Exception as e:
        _emit_error(error=str(e), code="ERROR", json_mode=json_mode)
        raise SystemExit(1)
    finally:
        _finalize_audit(cmd, started_at=started_at)


if __name__ == "__main__":
    raise SystemExit(main())
