from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any


def jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if is_dataclass(obj) and not isinstance(obj, type):
        return asdict(obj)
    if isinstance(obj, (list, tuple)):
        return [jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    return obj


def ok(*, data: Any = None, meta: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "ok": True,
        "data": jsonable(data),
        "error": None,
        "meta": dict(meta or {}),
    }


def err(
    *,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "data": None,
        "error": {
            "code": str(code),
            "message": str(message),
            "details": dict(details or {}),
        },
        "meta": dict(meta or {}),
    }
