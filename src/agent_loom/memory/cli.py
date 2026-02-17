from __future__ import annotations

from agent_loom.memory.cli_parser import (
    MemoryArgumentParser,
    _effective_format,
    _infer_error_format,
    _normalize_argv,
    _parse_args,
    build_parser,
)
from agent_loom.memory.cli_output import (
    emit,
    payload_for,
    render_link_validate,
    render_mutation_result,
    render_recall_results,
)
from agent_loom.memory.cli_runtime import (
    _run_with_args,
    main,
)

__all__ = [
    "MemoryArgumentParser",
    "_effective_format",
    "_infer_error_format",
    "_normalize_argv",
    "_parse_args",
    "_run_with_args",
    "build_parser",
    "emit",
    "main",
    "payload_for",
    "render_link_validate",
    "render_mutation_result",
    "render_recall_results",
]


if __name__ == "__main__":
    raise SystemExit(main())
