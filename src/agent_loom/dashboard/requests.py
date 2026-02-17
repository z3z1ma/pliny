from __future__ import annotations

from typing import Any

from flask import Request

from agent_loom.core.errors import LoomError


def is_loopback(host: str) -> bool:
    h = (host or "").strip().lower()
    return h in {"127.0.0.1", "localhost"}


def require_token_default(host: str, require_token: bool) -> bool:
    if require_token:
        return True
    # If bound to non-loopback, require a token by default.
    return not is_loopback(host)


def json_body(req: Request) -> dict[str, Any]:
    payload = req.get_json(silent=True)
    if payload is None:
        if req.get_data(cache=True, as_text=False):
            raise LoomError(
                "request body must be valid JSON",
                code="ARG",
                hint="Send a valid JSON object body.",
                http_status=400,
                exit_code=2,
            )
        return {}
    if isinstance(payload, dict):
        return payload
    raise LoomError(
        "request body must be a JSON object",
        code="ARG",
        hint="Send an object payload, not a list or scalar.",
        http_status=400,
        exit_code=2,
    )


def parse_int_field(
    body: dict[str, Any], *, field: str, default: int | None = None
) -> int | None:
    raw = body.get(field)
    if raw is None or (isinstance(raw, str) and not raw.strip()):
        return default
    if isinstance(raw, bool):
        raise LoomError(
            f"field '{field}' must be an integer",
            code="ARG",
            hint=f"Provide '{field}' as a numeric value.",
            http_status=400,
            exit_code=2,
            details={"field": field, "value": raw},
        )
    try:
        return int(raw)
    except (TypeError, ValueError) as exc:
        raise LoomError(
            f"field '{field}' must be an integer",
            code="ARG",
            hint=f"Provide '{field}' as a numeric value.",
            http_status=400,
            exit_code=2,
            details={"field": field, "value": raw},
        ) from exc
