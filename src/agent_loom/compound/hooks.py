from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from agent_loom.compound.paths import compound_paths
from agent_loom.core.time import now_iso_precise

_SECRET_KEY_RE = re.compile(
    r"pass(word)?|secret|token|api[_-]?key|auth(orization)?|cookie|session|private[_-]?key",
    re.IGNORECASE,
)

_SECRET_VALUE_RES = [
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{16,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"),
    re.compile(r"(Authorization\s*:\s*Bearer)\s+[^\s\"']+", re.IGNORECASE),
    re.compile(r"(Bearer)\s+[^\s\"']+", re.IGNORECASE),
    re.compile(r"-----BEGIN[\s\S]{0,2000}?-----END[^-]*-----"),
]


@dataclass(frozen=True)
class HookLimits:
    max_bytes: int
    max_backups: int
    max_string_chars: int
    max_object_keys: int


def _limits_from_env() -> HookLimits:
    return HookLimits(
        max_bytes=max(
            4096,
            int(
                os.environ.get("COMPOUND_OBSERVATIONS_MAX_BYTES", "33554432")
                or 33554432
            ),
        ),
        max_backups=max(
            0, int(os.environ.get("COMPOUND_OBSERVATIONS_MAX_BACKUPS", "5") or 5)
        ),
        max_string_chars=max(
            64,
            int(
                os.environ.get("COMPOUND_OBSERVATIONS_MAX_STRING_CHARS", "2000") or 2000
            ),
        ),
        max_object_keys=max(
            1, int(os.environ.get("COMPOUND_OBSERVATIONS_MAX_OBJECT_KEYS", "50") or 50)
        ),
    )


def _truncate(text: str, max_len: int) -> str:
    s = str(text or "")
    if max_len <= 0:
        return ""
    if len(s) <= max_len:
        return s
    return s[: max(0, max_len - 24)] + f"... (len={len(s)})"


def _scrub_string(text: str, *, max_len: int) -> str:
    out = str(text or "")
    for rx in _SECRET_VALUE_RES:
        out = rx.sub("[REDACTED]", out)
    return _truncate(out, max_len)


def _safe_json(
    value: Any,
    *,
    key: str = "",
    max_depth: int = 4,
    max_keys: int,
    max_string_chars: int,
) -> Any:
    if max_depth <= 0:
        return "{...}"
    if _SECRET_KEY_RE.search(str(key or "")):
        return "[REDACTED]"
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        items = list(value.items())[: max(0, int(max_keys))]
        for k, v in items:
            out[str(k)] = _safe_json(
                v,
                key=str(k),
                max_depth=max_depth - 1,
                max_keys=max_keys,
                max_string_chars=max_string_chars,
            )
        if len(value) > len(items):
            out["_compound_truncated_keys"] = True
        return out
    if isinstance(value, list):
        return [
            _safe_json(
                v,
                key=key,
                max_depth=max_depth - 1,
                max_keys=max_keys,
                max_string_chars=max_string_chars,
            )
            for v in value[:50]
        ]
    if isinstance(value, str):
        return _scrub_string(value, max_len=max_string_chars)
    return value


def _read_payload(
    stdin_text: str, *, payload_json: str, event: str, event_key: str
) -> dict[str, Any]:
    if payload_json:
        parsed = json.loads(payload_json)
        if isinstance(parsed, dict):
            return parsed
    if stdin_text.strip():
        parsed = json.loads(stdin_text)
        if isinstance(parsed, dict):
            return parsed
    if event:
        return {event_key: event}
    return {}


def _rotate_observations(file_path: Path, *, max_backups: int) -> None:
    if not file_path.exists() or max_backups < 0:
        return

    if max_backups == 0:
        file_path.unlink(missing_ok=True)
        return

    oldest = file_path.with_name(f"{file_path.name}.{max_backups}.bak")
    oldest.unlink(missing_ok=True)

    for idx in range(max_backups - 1, 0, -1):
        src = file_path.with_name(f"{file_path.name}.{idx}.bak")
        dst = file_path.with_name(f"{file_path.name}.{idx + 1}.bak")
        if src.exists():
            src.rename(dst)

    if file_path.exists():
        file_path.rename(file_path.with_name(f"{file_path.name}.1.bak"))


def _append_observation(
    file_path: Path,
    observation: dict[str, Any],
    *,
    limits: HookLimits,
) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(observation, sort_keys=True, separators=(",", ":"))
    new_bytes = len((line + "\n").encode("utf-8"))

    current_size = int(file_path.stat().st_size) if file_path.exists() else 0
    if current_size + new_bytes > int(limits.max_bytes):
        _rotate_observations(file_path, max_backups=int(limits.max_backups))

    with file_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _extract_exit_code(payload: dict[str, Any]) -> int | None:
    tool_response = payload.get("tool_response")
    tr: dict[str, Any] = tool_response if isinstance(tool_response, dict) else {}
    metadata = tr.get("metadata")
    md: dict[str, Any] = metadata if isinstance(metadata, dict) else {}
    for key in ["exitCode", "exit_code", "code"]:
        val = md.get(key)
        if isinstance(val, int):
            return int(val)
    for key in ["exitCode", "exit_code", "code"]:
        val = tr.get(key)
        if isinstance(val, int):
            return int(val)
    return None


def _event_to_canonical(event_name: str, harness: str) -> str:
    raw = str(event_name or "").strip()
    if not raw:
        return "unknown"

    key = raw.lower()
    if harness == "claude":
        mapping = {
            "pretooluse": "tool_start",
            "posttooluse": "tool_complete",
            "posttoolusefailure": "tool_complete",
            "sessionstart": "session_start",
            "sessionend": "session_end",
            "userpromptsubmit": "prompt_submit",
            "stop": "session_stop",
            "subagentstop": "subagent_stop",
            "notification": "notification",
            "precompact": "pre_compact",
        }
        return mapping.get(key, key)

    if harness == "opencode":
        mapping = {
            "tool.execute.before": "tool_start",
            "tool.execute.after": "tool_complete",
            "message.updated": "prompt_submit",
            "session.idle": "idle",
        }
        return mapping.get(key, key)

    if harness == "omp":
        mapping = {
            "before_agent_start": "session_start",
            "tool_call": "tool_start",
            "tool_result": "tool_complete",
            "turn_end": "idle",
        }
        return mapping.get(key, key)

    return key


def _tool_output(payload: dict[str, Any], *, limits: HookLimits) -> Any:
    tool_response = payload.get("tool_response")
    tr: dict[str, Any] = tool_response if isinstance(tool_response, dict) else {}
    output = tr.get("output")
    if not isinstance(output, str):
        output = tr.get("stderr")
    if not isinstance(output, str):
        return ""
    return _scrub_string(output, max_len=min(4000, int(limits.max_string_chars)))


def _command_signature(cmd: str, *, max_len: int) -> str:
    txt = str(cmd or "").replace("\n", " ").strip()
    if not txt:
        return ""
    toks = [t for t in txt.split(" ") if t][:4]
    return _truncate(" ".join(toks), max_len)


def _normalized_observation(
    payload: dict[str, Any],
    *,
    event_name: str,
    canonical_event: str,
    cwd: str,
    harness: str,
    limits: HookLimits,
) -> dict[str, Any]:
    tool_name = str(payload.get("tool_name") or "").strip()
    tool_input = (
        payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    )

    obs: dict[str, Any] = {
        "id": str(uuid4()),
        "ts": now_iso_precise(),
        "event": canonical_event,
        "session_id": str(payload.get("session_id") or ""),
        "cwd": str(payload.get("cwd") or cwd),
        "harness": str(harness),
    }

    if tool_name:
        obs["tool"] = tool_name
    if tool_input:
        obs["input"] = _safe_json(
            tool_input,
            max_keys=int(limits.max_object_keys),
            max_string_chars=int(limits.max_string_chars),
        )
        if tool_name.lower() in {"bash", "shell"}:
            sig = _command_signature(
                str(tool_input.get("command") or ""),
                max_len=min(280, int(limits.max_string_chars)),
            )
            if sig:
                obs["command"] = sig

    explicit_ok = payload.get("ok")
    if isinstance(explicit_ok, bool):
        obs["ok"] = bool(explicit_ok)
    elif canonical_event == "tool_complete":
        obs["ok"] = str(event_name or "").strip() != "PostToolUseFailure"

    exit_code = _extract_exit_code(payload)
    if exit_code is not None:
        obs["exit_code"] = int(exit_code)

    out = _tool_output(payload, limits=limits)
    if out:
        obs["output"] = out

    reason = str(payload.get("reason") or payload.get("error") or "").strip()
    if reason:
        obs["reason"] = _truncate(
            _scrub_string(reason, max_len=int(limits.max_string_chars)),
            min(280, int(limits.max_string_chars)),
        )

    prompt = str(payload.get("prompt") or "").strip()
    metadata_src = payload.get("metadata")
    metadata_extra = metadata_src if isinstance(metadata_src, dict) else {}
    obs["metadata"] = _safe_json(
        {
            "raw_event": event_name,
            "permission_mode": payload.get("permission_mode"),
            "source": payload.get("source"),
            "transcript_path": payload.get("transcript_path"),
            "prompt_excerpt": _scrub_string(
                _truncate(prompt, 800), max_len=min(800, int(limits.max_string_chars))
            )
            if prompt
            else "",
            "prompt_len": len(prompt) if prompt else 0,
            **metadata_extra,
        },
        max_keys=int(limits.max_object_keys),
        max_string_chars=int(limits.max_string_chars),
    )
    return obs


def _nudge_observer(nudge_file: Path) -> None:
    nudge_file.parent.mkdir(parents=True, exist_ok=True)
    nudge_file.touch()


@dataclass(frozen=True)
class HookResult:
    ok: bool
    event: str
    harness: str
    observation_logged: bool
    instincts_update_invoked: bool
    instincts_update_applied: bool
    error: str


def _run_hook_adapter(
    *,
    repo: Path,
    stdin_text: str,
    payload_json: str,
    event: str,
    harness: str,
) -> HookResult:
    payload = _read_payload(
        stdin_text,
        payload_json=payload_json,
        event=event,
        event_key="hook_event_name",
    )
    event_name = str(event or payload.get("hook_event_name") or "").strip() or "unknown"
    harness_name = str(harness or "unknown").strip() or "unknown"

    log_observations = (
        str(os.environ.get("COMPOUND_LOG_OBSERVATIONS", "1")).strip() or "1"
    ) != "0"
    if log_observations:
        limits = _limits_from_env()
        paths = compound_paths(repo)
        obs = _normalized_observation(
            payload,
            event_name=event_name,
            canonical_event=_event_to_canonical(event_name, harness_name),
            cwd=str(repo),
            harness=harness_name,
            limits=limits,
        )
        _append_observation(paths.observations_file, obs, limits=limits)
        _nudge_observer(paths.observer_nudge_file)

    return HookResult(
        ok=True,
        event=event_name,
        harness=harness_name,
        observation_logged=bool(log_observations),
        instincts_update_invoked=False,
        instincts_update_applied=False,
        error="",
    )


def run_claude_hook(
    *,
    repo: Path,
    stdin_text: str,
    payload_json: str,
    event: str,
) -> HookResult:
    return _run_hook_adapter(
        repo=repo,
        stdin_text=stdin_text,
        payload_json=payload_json,
        event=event,
        harness="claude",
    )


def _extract_opencode_session_id(payload: dict[str, Any]) -> str:
    candidates = [
        payload.get("session_id"),
        payload.get("sessionID"),
        payload.get("sessionId"),
    ]
    props = cast(
        dict[str, Any],
        payload.get("properties")
        if isinstance(payload.get("properties"), dict)
        else {},
    )
    candidates.extend([props.get("sessionID"), props.get("sessionId"), props.get("id")])
    for v in candidates:
        s = str(v or "").strip()
        if s:
            return s
    return ""


def _extract_opencode_prompt(payload: dict[str, Any]) -> str:
    direct = str(payload.get("prompt") or "").strip()
    if direct:
        return direct

    props = cast(
        dict[str, Any],
        payload.get("properties")
        if isinstance(payload.get("properties"), dict)
        else {},
    )
    candidates: list[Any] = [
        payload.get("message"),
        props.get("message"),
        props.get("info"),
        props.get("payload"),
        props,
    ]
    for c in candidates:
        if not isinstance(c, dict):
            continue
        info_obj = cast(
            dict[str, Any], c.get("info") if isinstance(c.get("info"), dict) else {}
        )
        role = str(c.get("role") or info_obj.get("role") or "").strip().lower()
        if role and role != "user":
            continue
        parts = cast(
            list[Any], c.get("parts") if isinstance(c.get("parts"), list) else []
        )
        from_parts = "\n".join(
            str(p.get("text") or "")
            for p in parts
            if isinstance(p, dict)
            and str(p.get("type") or "").strip().lower() == "text"
            and str(p.get("text") or "").strip()
        ).strip()
        from_text = str(c.get("text") or "").strip()
        if from_parts:
            return from_parts
        if from_text:
            return from_text
    return ""


def _normalize_opencode_payload(
    raw: dict[str, Any], *, event_override: str
) -> tuple[str, dict[str, Any]]:
    event_name = (
        str(event_override or "").strip()
        or str(raw.get("hook_event_name") or raw.get("type") or "").strip()
        or "unknown"
    )

    normalized: dict[str, Any] = {
        "hook_event_name": event_name,
        "session_id": _extract_opencode_session_id(raw),
    }

    tool_name = str(raw.get("tool_name") or raw.get("toolName") or "").strip()
    if not tool_name:
        input_obj = cast(
            dict[str, Any],
            raw.get("input") if isinstance(raw.get("input"), dict) else {},
        )
        output_obj = cast(
            dict[str, Any],
            raw.get("output") if isinstance(raw.get("output"), dict) else {},
        )
        tool_name = str(
            input_obj.get("tool")
            or input_obj.get("name")
            or output_obj.get("tool")
            or output_obj.get("name")
            or ""
        ).strip()

    tool_input = (
        raw.get("tool_input") if isinstance(raw.get("tool_input"), dict) else None
    )
    if tool_input is None:
        input_obj = cast(
            dict[str, Any],
            raw.get("input") if isinstance(raw.get("input"), dict) else {},
        )
        output_obj = cast(
            dict[str, Any],
            raw.get("output") if isinstance(raw.get("output"), dict) else {},
        )
        for candidate in [
            raw.get("args"),
            output_obj.get("args"),
            input_obj.get("args"),
        ]:
            if isinstance(candidate, dict):
                tool_input = candidate
                break

    if tool_name:
        normalized["tool_name"] = tool_name
    if isinstance(tool_input, dict):
        normalized["tool_input"] = tool_input

    tool_response = (
        raw.get("tool_response") if isinstance(raw.get("tool_response"), dict) else None
    )
    if tool_response is None and isinstance(raw.get("output"), dict):
        tool_response = cast(dict[str, Any], raw.get("output"))
    if isinstance(tool_response, dict):
        normalized["tool_response"] = tool_response

    explicit_ok = raw.get("ok")
    if isinstance(explicit_ok, bool):
        normalized["ok"] = bool(explicit_ok)

    reason = str(raw.get("reason") or raw.get("error") or "").strip()
    if reason:
        normalized["reason"] = reason

    prompt = _extract_opencode_prompt(raw)
    if prompt:
        normalized["prompt"] = prompt

    normalized["metadata"] = {
        "source": "opencode",
        "event_type": str(raw.get("type") or event_name),
    }

    return event_name, normalized


def run_opencode_hook(
    *,
    repo: Path,
    stdin_text: str,
    payload_json: str,
    event: str,
) -> HookResult:
    raw = _read_payload(
        stdin_text,
        payload_json=payload_json,
        event=event,
        event_key="type",
    )
    event_name, normalized = _normalize_opencode_payload(raw, event_override=event)
    return _run_hook_adapter(
        repo=repo,
        stdin_text="",
        payload_json=json.dumps(normalized),
        event=event_name,
        harness="opencode",
    )


def _extract_omp_session_id(payload: dict[str, Any]) -> str:
    for key in ["session_id", "sessionID", "sessionId", "session"]:
        val = payload.get(key)
        if isinstance(val, dict):
            for nested in ["id", "sessionID", "sessionId"]:
                s_nested = str(val.get(nested) or "").strip()
                if s_nested:
                    return s_nested
        s = str(val or "").strip()
        if s:
            return s
    return ""


def _normalize_omp_payload(
    raw: dict[str, Any], *, event_override: str
) -> tuple[str, dict[str, Any]]:
    event_name = (
        str(event_override or "").strip()
        or str(raw.get("event_name") or raw.get("hook_event_name") or "").strip()
        or "unknown"
    )

    normalized: dict[str, Any] = {
        "hook_event_name": event_name,
        "session_id": _extract_omp_session_id(raw),
        "metadata": {
            "source": "omp",
            "event_type": event_name,
        },
    }

    if event_name == "before_agent_start":
        prompt = str(raw.get("prompt") or "").strip()
        if prompt:
            normalized["prompt"] = prompt

    tool_name = str(raw.get("tool_name") or raw.get("toolName") or "").strip()
    tool_input = (
        raw.get("tool_input") if isinstance(raw.get("tool_input"), dict) else None
    )
    tool_response = (
        raw.get("tool_response") if isinstance(raw.get("tool_response"), dict) else None
    )

    if not tool_name:
        tool_name = str(raw.get("tool") or "").strip()
    if tool_input is None:
        candidate = raw.get("input")
        if isinstance(candidate, dict):
            tool_input = cast(dict[str, Any], candidate)
    if tool_response is None:
        candidate = raw.get("output")
        if isinstance(candidate, dict):
            tool_response = cast(dict[str, Any], candidate)

    if tool_name:
        normalized["tool_name"] = tool_name
    if isinstance(tool_input, dict):
        normalized["tool_input"] = tool_input
    if isinstance(tool_response, dict):
        normalized["tool_response"] = tool_response

    explicit_ok = raw.get("ok")
    if isinstance(explicit_ok, bool):
        normalized["ok"] = bool(explicit_ok)

    explicit_err = raw.get("is_error")
    if isinstance(explicit_err, bool):
        normalized["ok"] = not bool(explicit_err)

    reason = str(raw.get("reason") or raw.get("error") or "").strip()
    if reason:
        normalized["reason"] = reason

    return event_name, normalized


def run_omp_hook(
    *,
    repo: Path,
    stdin_text: str,
    payload_json: str,
    event: str,
) -> HookResult:
    raw = _read_payload(
        stdin_text,
        payload_json=payload_json,
        event=event,
        event_key="event_name",
    )
    event_name, normalized = _normalize_omp_payload(raw, event_override=event)
    return _run_hook_adapter(
        repo=repo,
        stdin_text="",
        payload_json=json.dumps(normalized),
        event=event_name,
        harness="omp",
    )


__all__ = [
    "HookResult",
    "run_claude_hook",
    "run_opencode_hook",
    "run_omp_hook",
]
