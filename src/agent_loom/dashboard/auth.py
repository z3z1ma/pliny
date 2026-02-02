from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from flask import Request


@dataclass(frozen=True)
class AuthResult:
    ok: bool
    reason: str


def _extract_token(req: Request) -> str:
    # Prefer Authorization: Bearer <token>, fall back to X-Loom-Token.
    auth = str(req.headers.get("Authorization") or "").strip()
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return str(req.headers.get("X-Loom-Token") or "").strip()


def authorize_request(*, req: Request, token: str, require_token: bool) -> AuthResult:
    if not require_token:
        return AuthResult(ok=True, reason="token_not_required")

    expected = str(token or "").strip()
    if not expected:
        return AuthResult(ok=False, reason="server_missing_token")

    got = _extract_token(req)
    if got == expected:
        return AuthResult(ok=True, reason="ok")
    return AuthResult(ok=False, reason="invalid_token")


def require_confirm(payload: Any) -> bool:
    if not isinstance(payload, dict):
        return False
    return bool(payload.get("confirm"))
