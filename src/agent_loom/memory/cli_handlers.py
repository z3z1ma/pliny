from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from agent_loom.memory.cli_edit_options import _build_edit_options, _stdin_is_ready
from agent_loom.memory.cli_output import emit, payload_for
from agent_loom.memory.core import (
    add,
    around,
    edit,
    forget,
    grep,
    init,
    janitor,
    link,
    list_recent,
    open_note,
    prime,
    recall,
    reindex,
    show,
    timeline,
)
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.recall import print_index_warnings
from agent_loom.memory.utils import read_all_stdin_text
from agent_loom.memory.vault import resolve_vault_root, vault_paths


def _emit_and_ok(payload: Any, *, fmt: str) -> int:
    emit(payload, fmt)
    return 0


def _ensure_vault_ready(args: argparse.Namespace) -> None:
    vp = vault_paths(resolve_vault_root(str(args.vault), cwd=Path.cwd()))
    if not vp.root.exists():
        raise MemoryError(
            f"Vault not found at {vp.root}",
            code="NOT_FOUND",
            exit_code=2,
            hint="Initialize a vault or point --vault to an existing one.",
            suggestions=[
                f"loom memory init --vault {vp.root}",
                "export MEMORY_VAULT=.loom/memory",
            ],
            details={"vault": str(vp.root)},
        )
    if not vp.meta_path.exists():
        init(vault=str(args.vault))


def _run_prime(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    del args, quiet
    res = prime()
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_init(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    del quiet
    res = init(vault=str(args.vault))
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_add(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    del quiet
    body = args.body
    if body == "-":
        if not _stdin_is_ready():
            raise MemoryError(
                "--body - requires piped stdin",
                code="ARG",
                exit_code=2,
                hint="Pipe body text into stdin.",
                suggestions=[
                    "cat file.md | loom memory add --title 'Title' --body -",
                ],
            )
        body = read_all_stdin_text()
    if body is None and not sys.stdin.isatty():
        body = read_all_stdin_text()
    res = add(
        vault=str(args.vault),
        title=args.title,
        visibility=str(args.visibility or "shared").strip().lower(),
        status=str(args.status or "active").strip().lower(),
        tag=args.tag,
        alias=args.alias,
        link=getattr(args, "link", None),
        related=getattr(args, "related", None),
        scope=args.scope,
        command=args.command,
        allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
        body=body,
        interactive=bool(args.interactive),
        note_id=args.id,
        folder=args.folder or "",
    )
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_edit(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    del quiet
    options = _build_edit_options(args)
    res = edit(
        vault=str(args.vault),
        note_id=options.note_id,
        title=options.title,
        visibility=options.visibility,
        status=options.status,
        tag=options.tag,
        remove_tag=options.remove_tag,
        clear_tags=options.clear_tags,
        alias=options.alias,
        remove_alias=options.remove_alias,
        clear_aliases=options.clear_aliases,
        link=options.link,
        remove_link=options.remove_link,
        clear_links=options.clear_links,
        related=options.related,
        scope=options.scope,
        command=options.command,
        remove_scope=options.remove_scope,
        clear_scopes=options.clear_scopes,
        allow_missing_scopes=options.allow_missing_scopes,
        body=options.body,
        append=options.append,
        interactive=options.interactive,
    )
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_recall(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    res = recall(
        vault=str(args.vault),
        query=args.query or "",
        limit=int(args.limit),
        tag=args.tag,
        not_tag=args.not_tag,
        scope=args.scope,
        not_scope=args.not_scope,
        command=args.command or "",
        visibility=args.visibility,
        include_deprecated=bool(args.include_deprecated),
        since=args.since,
        until=getattr(args, "until", None),
        and_mode=bool(args.and_mode),
        scoped_only=bool(args.scoped_only),
        full=bool(args.full),
        max_body_chars=args.max_body_chars,
        expand=int(args.expand or 0),
        max_chars=int(args.max_chars),
        context=bool(args.context),
        deterministic=bool(getattr(args, "deterministic", False)),
        quiet=quiet,
        allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
        format=fmt,
        or_mode=bool(getattr(args, "or_mode", False)),
        fts_raw=bool(getattr(args, "fts_raw", False)),
    )
    if not quiet and res.warnings:
        print_index_warnings(list(res.warnings))
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_list(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    res = list_recent(
        vault=str(args.vault),
        limit=int(args.limit),
        tag=args.tag,
        not_tag=args.not_tag,
        scope=args.scope,
        not_scope=args.not_scope,
        command=args.command or "",
        visibility=args.visibility,
        include_deprecated=bool(args.include_deprecated),
        since=args.since,
        until=getattr(args, "until", None),
        and_mode=False,
        scoped_only=False,
        deterministic=bool(getattr(args, "deterministic", False)),
        quiet=quiet,
        allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
        sort=str(getattr(args, "sort", "updated") or "updated"),
    )
    if not quiet and res.warnings:
        print_index_warnings(list(res.warnings))
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_grep(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    payload = grep(
        vault=str(args.vault),
        pattern=str(args.pattern),
        limit=int(args.limit),
        tag=args.tag,
        not_tag=args.not_tag,
        scope=args.scope,
        not_scope=args.not_scope,
        command=args.command or "",
        visibility=args.visibility,
        include_deprecated=bool(args.include_deprecated),
        since=args.since,
        until=getattr(args, "until", None),
        and_mode=bool(getattr(args, "and_mode", False)),
        scoped_only=bool(getattr(args, "scoped_only", False)),
        quiet=quiet,
        allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
        ignore_case=bool(getattr(args, "ignore_case", False)),
    )
    return _emit_and_ok(payload, fmt=fmt)


def _run_show(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    del quiet
    text = show(vault=str(args.vault), note_id=str(args.id), meta_only=bool(args.meta))
    return _emit_and_ok(text, fmt=fmt)


def _run_open(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    del quiet
    rel = open_note(vault=str(args.vault), note_id=str(args.id))
    return _emit_and_ok(rel, fmt=fmt)


def _run_forget(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    payload = forget(
        vault=str(args.vault),
        query=args.query or "",
        limit=int(args.limit),
        tag=args.tag,
        not_tag=args.not_tag,
        scope=args.scope,
        not_scope=args.not_scope,
        command=args.command or "",
        visibility=args.visibility,
        include_deprecated=bool(args.include_deprecated),
        since=args.since,
        until=getattr(args, "until", None),
        and_mode=False,
        scoped_only=False,
        deterministic=bool(getattr(args, "deterministic", False)),
        quiet=quiet,
        allow_missing_scopes=bool(getattr(args, "allow_missing_scopes", False)),
        or_mode=bool(getattr(args, "or_mode", False)),
        fts_raw=bool(getattr(args, "fts_raw", False)),
        apply=bool(getattr(args, "apply", False)),
        hard=bool(getattr(args, "hard", False)),
    )
    return _emit_and_ok(payload, fmt=fmt)


def _run_around(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    payload = around(
        vault=str(args.vault),
        note_id=str(args.id),
        k=int(getattr(args, "k", 12) or 12),
        by=str(getattr(args, "by", "updated") or "updated"),
        window_days=int(getattr(args, "window_days", 14) or 14),
        visibility=args.visibility,
        include_deprecated=bool(getattr(args, "include_deprecated", False)),
        quiet=quiet,
    )
    return _emit_and_ok(payload, fmt=fmt)


def _run_timeline(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    payload = timeline(
        vault=str(args.vault),
        days=int(getattr(args, "days", 30) or 30),
        by=str(getattr(args, "by", "updated") or "updated"),
        visibility=args.visibility,
        include_deprecated=bool(getattr(args, "include_deprecated", False)),
        quiet=quiet,
    )
    return _emit_and_ok(payload, fmt=fmt)


def _run_reindex(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    res = reindex(vault=str(args.vault), quiet=quiet)
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_janitor(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    res = janitor(
        vault=str(args.vault),
        cmd=args.janitor_cmd,
        visibility=args.visibility,
        limit=int(args.limit),
        apply=bool(getattr(args, "apply", False)),
        quiet=quiet,
    )
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


def _run_link(args: argparse.Namespace, *, fmt: str, quiet: bool) -> int:
    res = link(
        vault=str(args.vault),
        cmd=args.link_cmd,
        note_id=getattr(args, "id", ""),
        limit=int(getattr(args, "limit", 200) or 200),
        k=int(getattr(args, "k", 1) or 1),
        include_unresolved=bool(getattr(args, "include_unresolved", False)),
        visibility=getattr(args, "visibility", None),
        include_deprecated=bool(getattr(args, "include_deprecated", False)),
        quiet=quiet,
    )
    if not quiet and res.warnings:
        print_index_warnings(list(res.warnings))
    return _emit_and_ok(payload_for(res, fmt=fmt), fmt=fmt)


_RUN_HANDLERS: dict[str, Any] = {
    "prime": _run_prime,
    "init": _run_init,
    "add": _run_add,
    "note": _run_add,
    "save": _run_add,
    "edit": _run_edit,
    "update": _run_edit,
    "append": _run_edit,
    "add-note": _run_edit,
    "append-note": _run_edit,
    "recall": _run_recall,
    "get": _run_recall,
    "remember": _run_recall,
    "list": _run_list,
    "ls": _run_list,
    "recent": _run_list,
    "grep": _run_grep,
    "show": _run_show,
    "open": _run_open,
    "forget": _run_forget,
    "archive": _run_forget,
    "around": _run_around,
    "timeline": _run_timeline,
    "reindex": _run_reindex,
    "janitor": _run_janitor,
    "link": _run_link,
}


def _run_with_args(args: argparse.Namespace, *, fmt: str) -> int:
    quiet = bool(getattr(args, "quiet", False))
    cmd = str(getattr(args, "cmd", "") or "")
    handler = _RUN_HANDLERS.get(cmd)
    if handler is None:
        raise MemoryError(
            f"Unknown command: {args.cmd}",
            code="ARG",
            exit_code=2,
            hint="Run `loom memory -h` to see commands.",
            suggestions=["loom memory -h"],
            details={"cmd": cmd},
        )

    if cmd not in {"prime", "init"}:
        _ensure_vault_ready(args)

    return int(handler(args, fmt=fmt, quiet=quiet))
