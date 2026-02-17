from __future__ import annotations

import sys
from typing import Optional, Sequence

from agent_loom.memory.cli_handlers import _run_with_args
from agent_loom.memory.cli_parser import (
    _effective_format,
    _infer_error_format,
    _normalize_argv,
    _parse_args,
)
from agent_loom.memory.errors import MemoryError
from agent_loom.memory.utils import emit_error


def main(argv: Optional[Sequence[str]] = None) -> int:
    argv_list = list(argv) if argv is not None else sys.argv[1:]
    argv_list = _normalize_argv(argv_list)
    fmt_for_parse_errors = _infer_error_format(argv_list)

    args = _parse_args(argv_list, fmt_for_parse_errors=fmt_for_parse_errors)
    if args is None:
        return 2

    fmt = _effective_format(args)
    if args.format is None:
        args.format = fmt

    try:
        return _run_with_args(args, fmt=fmt)
    except MemoryError as e:
        hint = str(getattr(e, "hint", "") or "")
        if not hint and str(getattr(e, "code", "")) in {"ARG", "ARGPARSE"}:
            hint = "Run `loom memory -h` or `loom memory <command> -h`."
        emit_error(
            code=str(getattr(e, "code", "ERROR")),
            error=str(e),
            fmt=fmt,
            hint=hint,
            suggestions=list(getattr(e, "suggestions", []) or []),
            details=getattr(e, "details", None),
        )
        return int(getattr(e, "exit_code", 1) or 1)
    except FileExistsError as e:
        emit_error(
            code="CONFLICT",
            error=str(e),
            fmt=fmt,
            hint="Choose a different id/folder or remove the existing file.",
        )
        return 2
    except FileNotFoundError as e:
        emit_error(
            code="NOT_FOUND",
            error=str(e),
            fmt=fmt,
            hint="Confirm the id/path, or search with `loom memory recall <query>`.",
        )
        return 2
    except ValueError as e:
        emit_error(
            code="ARG",
            error=str(e),
            fmt=fmt,
            hint="Run `loom memory -h` or `loom memory <command> -h`.",
        )
        return 2
    except Exception as e:
        emit_error(code="ERROR", error=str(e), fmt=fmt)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
