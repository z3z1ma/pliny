from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping, NoReturn, Sequence

from agent_loom.core.time import now_iso as core_now_iso
from agent_loom.memory.constants import FENCED_CODE_RE, FENCED_TILDE_RE
from agent_loom.memory.errors import MemoryError


def eprint(*a: Any, **k: Any) -> None:
    print(*a, file=sys.stderr, **k)


def die(msg: str, *, code: int = 2) -> NoReturn:
    # Backwards-compatible escape hatch.
    # Prefer raising MemoryError directly so CLI can emit structured guidance.
    raise MemoryError(
        str(msg), code="ARG" if int(code) == 2 else "ERROR", exit_code=int(code)
    )


def _coerce_jsonable(obj: Any) -> Any:
    if obj is None:
        return None
    if isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, list):
        return [_coerce_jsonable(x) for x in obj]
    if isinstance(obj, tuple):
        return [_coerce_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            out[str(k)] = _coerce_jsonable(v)
        return out
    return str(obj)


def emit_error(
    *,
    code: str,
    error: str,
    fmt: str,
    hint: str = "",
    suggestions: Sequence[str] | None = None,
    details: Mapping[str, Any] | None = None,
) -> None:
    if fmt in {"json", "jsonl"}:
        payload: dict[str, Any] = {"ok": False, "code": str(code), "error": str(error)}
        if hint:
            payload["hint"] = str(hint)
        if suggestions:
            payload["suggestions"] = [str(s) for s in suggestions if str(s).strip()]
        if details:
            payload["details"] = _coerce_jsonable(dict(details))

        if fmt == "jsonl":
            print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        else:
            print(format_json(payload))
        return

    # text|md|prompt => errors go to stderr
    eprint(f"Error: {error}")
    if hint:
        eprint(f"Hint: {hint}")
    if suggestions:
        for s in suggestions:
            if str(s).strip():
                eprint(f"Try: {s}")


def now_iso() -> str:
    return core_now_iso()


def format_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)


def read_all_stdin_text() -> str:
    return sys.stdin.read()


def safe_mkdir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="replace")).hexdigest()


def is_windows() -> bool:
    return os.name == "nt"


def normcase(s: str) -> str:
    return s.casefold() if is_windows() else s


def strip_fenced_code_blocks(md: str) -> str:
    t = (md or "").replace("\r\n", "\n").replace("\r", "\n")
    t = FENCED_CODE_RE.sub("", t)
    t = FENCED_TILDE_RE.sub("", t)
    return t


__all__ = [
    "die",
    "eprint",
    "emit_error",
    "format_json",
    "is_windows",
    "normcase",
    "now_iso",
    "read_all_stdin_text",
    "safe_mkdir",
    "sha256_text",
    "strip_fenced_code_blocks",
]
