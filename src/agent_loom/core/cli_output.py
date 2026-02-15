"""Shared CLI output and serialization helpers for consistent JSON/text behavior."""

import dataclasses
import json
import sys
from typing import Any


def normalize_payload(obj: Any) -> Any:
    """
    Normalize an object to a JSON-serializable payload.

    Supports objects with `to_dict()` method and dataclasses.
    Returns the object as-is if already serializable.
    """
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    return obj


def emit_json(obj: object, *, indent: int | None = None, minified: bool = False) -> None:
    """
    Emit a JSON object to stdout with a trailing newline.

    Args:
        obj: Object to serialize (must be JSON-serializable or normalizable via normalize_payload).
        indent: Number of spaces for indentation (default: None for compact).
        minified: If True, use compact separators (ignores indent).
    """
    if minified:
        sys.stdout.write(json.dumps(obj, sort_keys=True, separators=(",", ":")))
    else:
        if indent is not None:
            sys.stdout.write(json.dumps(obj, indent=indent, sort_keys=True))
        else:
            sys.stdout.write(json.dumps(obj, sort_keys=True))
    sys.stdout.write("\n")


def make_ok_envelope(payload: Any) -> dict[str, Any]:
    """
    Wrap a payload in a standard `{"ok": True, ...}` envelope.

    If payload is a dict, merge it into the envelope.
    Otherwise, wrap it under the `data` key.
    """
    normalized = normalize_payload(payload)
    if isinstance(normalized, dict):
        return {"ok": True, **normalized}
    return {"ok": True, "data": normalized}


def make_error_envelope(
    error: str,
    code: str,
    hint: str = "",
    suggestions: list[str] | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create a standard error envelope for JSON output.

    Returns:
        {"ok": False, "error": ..., "code": ..., "hint": ..., "suggestions": ..., "details": ...}
    """
    envelope: dict[str, Any] = {"ok": False, "error": error, "code": code}
    if hint:
        envelope["hint"] = hint
    if suggestions:
        envelope["suggestions"] = suggestions
    if details:
        envelope["details"] = details
    return envelope
