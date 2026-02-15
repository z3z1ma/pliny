from __future__ import annotations

import sys
from typing import Any, Mapping, Sequence

from agent_loom.core.cli_output import emit_json as _core_emit_json, make_error_envelope


def _eprint(*a: object) -> None:
    print(*a, file=sys.stderr)


def _emit_json(payload: Any) -> None:
    _core_emit_json(payload, indent=2)


def _emit_error(
    *,
    code: str,
    error: str,
    json_mode: bool,
    hint: str = "",
    suggestions: Sequence[str] | None = None,
    details: Mapping[str, Any] | None = None,
) -> None:
    if json_mode:
        envelope = make_error_envelope(
            error=error,
            code=code,
            hint=hint,
            suggestions=[str(s) for s in suggestions if str(s).strip()] if suggestions else None,
            details=dict(details) if details else None,
        )
        _emit_json(envelope)
        return
    if hint:
        _eprint(f"Hint: {hint}")
    if suggestions:
        for s in suggestions:
            if str(s).strip():
                _eprint(f"Try: {s}")


__all__ = ["_eprint", "_emit_error", "_emit_json"]
