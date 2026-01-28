from __future__ import annotations

import json
import sys
from typing import Any, Mapping, Sequence


def _eprint(*a: object) -> None:
    print(*a, file=sys.stderr)


def _emit_json(payload: Any) -> None:
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


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
        payload: dict[str, Any] = {"ok": False, "code": str(code), "error": str(error)}
        if hint:
            payload["hint"] = str(hint)
        if suggestions:
            payload["suggestions"] = [str(s) for s in suggestions if str(s).strip()]
        if details:
            payload["details"] = dict(details)
        _emit_json(payload)
        return

    _eprint(f"Error: {error}")
    if hint:
        _eprint(f"Hint: {hint}")
    if suggestions:
        for s in suggestions:
            if str(s).strip():
                _eprint(f"Try: {s}")


__all__ = ["_eprint", "_emit_error", "_emit_json"]
