from __future__ import annotations

import argparse
import select
import sys
from dataclasses import dataclass

from agent_loom.memory.errors import MemoryError
from agent_loom.memory.utils import read_all_stdin_text


def _stdin_is_ready() -> bool:
    if sys.stdin.isatty():
        return False
    try:
        r, _w, _x = select.select([sys.stdin], [], [], 0)
        return bool(r)
    except Exception:
        # In-memory streams used in tests support getvalue(); non-readable capture
        # wrappers should not be treated as ready.
        return bool(hasattr(sys.stdin, "getvalue"))


@dataclass(frozen=True)
class _EditRunOptions:
    note_id: str
    title: str | None
    visibility: str | None
    status: str | None
    tag: list[str]
    remove_tag: list[str]
    clear_tags: bool
    alias: list[str]
    remove_alias: list[str]
    clear_aliases: bool
    link: list[str]
    remove_link: list[str]
    clear_links: bool
    related: list[str]
    scope: list[str]
    command: str | None
    remove_scope: list[str]
    clear_scopes: bool
    allow_missing_scopes: bool
    body: str | None
    append: str | None
    interactive: bool


def _build_edit_options(args: argparse.Namespace) -> _EditRunOptions:
    cmd = str(getattr(args, "cmd", "") or "")
    is_append_cmd = cmd in {"append", "add-note", "append-note"}

    body_override = getattr(args, "body", None)
    body_append = getattr(args, "append", None)
    from_stdin = bool(getattr(args, "from_stdin", False))
    append_from_stdin = bool(getattr(args, "append_from_stdin", False))
    interactive = bool(getattr(args, "interactive", False))

    title = getattr(args, "title", None)
    visibility = getattr(args, "visibility", None)
    status = getattr(args, "status", None)
    tag = list(getattr(args, "tag", []) or [])
    remove_tag = list(getattr(args, "remove_tag", []) or [])
    clear_tags = bool(getattr(args, "clear_tags", False))
    alias = list(getattr(args, "alias", []) or [])
    remove_alias = list(getattr(args, "remove_alias", []) or [])
    clear_aliases = bool(getattr(args, "clear_aliases", False))
    link_values = list(getattr(args, "link", []) or [])
    remove_link = list(getattr(args, "remove_link", []) or [])
    clear_links = bool(getattr(args, "clear_links", False))
    related = list(getattr(args, "related", []) or [])
    scope = list(getattr(args, "scope", []) or [])
    command = getattr(args, "command", None)
    remove_scope = list(getattr(args, "remove_scope", []) or [])
    clear_scopes = bool(getattr(args, "clear_scopes", False))
    allow_missing_scopes = bool(getattr(args, "allow_missing_scopes", False))

    if is_append_cmd:
        append_from_stdin = bool(getattr(args, "from_stdin", False))
        from_stdin = False
        if body_append is None:
            body_append = getattr(args, "text", None)
        if body_append is None:
            body_append = body_override
        body_override = None
        interactive = False
        title = None
        visibility = None
        status = None
        tag = []
        remove_tag = []
        clear_tags = False
        alias = []
        remove_alias = []
        clear_aliases = False
        link_values = []
        remove_link = []
        clear_links = False
        scope = []
        command = None
        remove_scope = []
        clear_scopes = False
        allow_missing_scopes = False

    if from_stdin and append_from_stdin:
        raise MemoryError(
            "edit: cannot combine --from-stdin and --append-from-stdin",
            code="ARG",
            exit_code=2,
            hint="Pick exactly one stdin mode.",
            suggestions=[
                "cat file.md | loom memory edit <id> --from-stdin",
                "cat file.md | loom memory edit <id> --append-from-stdin",
            ],
        )

    stdin_ready = _stdin_is_ready()
    uses_stdin = from_stdin or append_from_stdin
    if (
        stdin_ready
        and not uses_stdin
        and body_override is None
        and body_append is None
        and not interactive
    ):
        raise MemoryError(
            "stdin is piped but no body mode was selected",
            code="ARG",
            exit_code=2,
            hint="Choose whether stdin should replace or append to the note body.",
            suggestions=[
                "cat file.md | loom memory edit <id> --from-stdin",
                "cat file.md | loom memory edit <id> --append-from-stdin",
            ],
        )

    if body_override == "-":
        if not _stdin_is_ready():
            raise MemoryError(
                "--body - requires piped stdin",
                code="ARG",
                exit_code=2,
                hint="Pipe body text into stdin.",
            )
        body_override = read_all_stdin_text()
    if from_stdin:
        if sys.stdin.isatty():
            raise MemoryError(
                "edit --from-stdin requires piped stdin",
                code="ARG",
                exit_code=2,
                hint="Pipe content: cat file.md | loom memory edit <id> --from-stdin",
            )
        body_override = read_all_stdin_text()

    if body_append == "-":
        if not _stdin_is_ready():
            raise MemoryError(
                "--append - requires piped stdin",
                code="ARG",
                exit_code=2,
                hint="Pipe append text into stdin.",
            )
        body_append = read_all_stdin_text()
    if append_from_stdin:
        if sys.stdin.isatty():
            raise MemoryError(
                "edit --append-from-stdin requires piped stdin",
                code="ARG",
                exit_code=2,
                hint="Pipe content: cat file.md | loom memory edit <id> --append-from-stdin",
            )
        body_append = read_all_stdin_text()

    if is_append_cmd and body_append is None and not related:
        raise MemoryError(
            "append requires text (--append/--text/--body) or piped stdin",
            code="ARG",
            exit_code=2,
            hint="Provide append text directly or pipe it on stdin.",
            suggestions=[
                "loom memory append <id> --append 'New findings'",
                "cat update.md | loom memory append <id> --from-stdin",
            ],
        )

    return _EditRunOptions(
        note_id=str(getattr(args, "id", "") or ""),
        title=(str(title) if title is not None else None),
        visibility=(str(visibility).strip().lower() if visibility is not None else None),
        status=(str(status).strip().lower() if status is not None else None),
        tag=tag,
        remove_tag=remove_tag,
        clear_tags=clear_tags,
        alias=alias,
        remove_alias=remove_alias,
        clear_aliases=clear_aliases,
        link=link_values,
        remove_link=remove_link,
        clear_links=clear_links,
        related=related,
        scope=scope,
        command=(str(command) if command is not None else None),
        remove_scope=remove_scope,
        clear_scopes=clear_scopes,
        allow_missing_scopes=allow_missing_scopes,
        body=(str(body_override) if body_override is not None else None),
        append=(str(body_append) if body_append is not None else None),
        interactive=interactive,
    )
