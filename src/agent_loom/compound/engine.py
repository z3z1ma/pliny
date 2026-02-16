from __future__ import annotations

import json
import os
import re
import shlex
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agent_loom.compound.instincts import (
    Instinct,
    InstinctStore,
    load_instincts,
    save_instincts,
    sync_instincts_markdown,
)
from agent_loom.compound.observations import (
    count_observations,
    ingest_observations_since,
    observations_prefix_sha256,
)
from agent_loom.compound.paths import CompoundPaths, compound_paths
from agent_loom.compound.state import CompoundState, load_state, save_state
from agent_loom.core.exec import run
from agent_loom.core.time import now_iso_precise

_PLACEHOLDER_RE = re.compile(r"\{([a-z0-9_]+)\}")


def _parse_iso(text: str) -> datetime | None:
    s = str(text or "").strip()
    if not s:
        return None
    try:
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)
    except Exception:
        return None


def _short(text: str, *, max_len: int) -> str:
    s = str(text or "").replace("\n", " ").strip()
    if len(s) <= max_len:
        return s
    if max_len <= 3:
        return s[:max_len]
    return s[: max_len - 3] + "..."


def _observations_compact(
    observations: list[dict[str, Any]], *, max_rows: int
) -> list[dict[str, Any]]:
    rows = observations[-max(1, int(max_rows)) :]
    out: list[dict[str, Any]] = []
    for row in rows:
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        item = {
            "ts": _short(str(row.get("ts") or ""), max_len=48),
            "event": _short(str(row.get("event") or ""), max_len=64),
            "harness": _short(str(row.get("harness") or ""), max_len=24),
            "tool": _short(str(row.get("tool") or ""), max_len=48),
            "command": _short(str(row.get("command") or ""), max_len=180),
            "ok": bool(row.get("ok")) if row.get("ok") is not None else None,
            "exit_code": row.get("exit_code")
            if isinstance(row.get("exit_code"), int)
            else None,
            "reason": _short(str(row.get("reason") or ""), max_len=180),
            "output": _short(str(row.get("output") or ""), max_len=240),
            "prompt_excerpt": _short(
                str((metadata or {}).get("prompt_excerpt") or ""), max_len=220
            ),
        }
        out.append({k: v for k, v in item.items() if v not in (None, "")})
    return out


def _existing_instincts_compact(
    store: InstinctStore, *, max_rows: int
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for inst in list(store.instincts)[: max(1, int(max_rows))]:
        out.append(
            {
                "id": str(inst.id or ""),
                "title": _short(str(inst.title or ""), max_len=140),
                "trigger": _short(str(inst.trigger or ""), max_len=180),
                "action": _short(str(inst.action or ""), max_len=180),
                "domain": str(inst.domain or ""),
                "source": str(inst.source or ""),
                "tags": [str(t) for t in list(inst.tags or [])[:8]],
                "confidence": float(inst.confidence or 0.0),
                "status": str(inst.status or "active"),
            }
        )
    return out


def _build_freeform_prompt(
    *,
    paths: CompoundPaths,
    observations: list[dict[str, Any]],
    existing_instincts: InstinctStore,
    min_occurrences: int,
    max_candidates: int,
) -> str:
    now_iso = now_iso_precise()
    observations_json = json.dumps(
        _observations_compact(observations, max_rows=260),
        indent=2,
    )
    existing_json = json.dumps(
        _existing_instincts_compact(existing_instincts, max_rows=200),
        indent=2,
    )
    return (
        "You are Loom continuous-learning observer (ECC-style). "
        "Your job is to analyze observations and directly write/update instinct markdown files.\n\n"
        "CRITICAL EXECUTION RULES\n"
        "- Do not return JSON for parsing.\n"
        "- Write files directly to: " + str(paths.instincts_local_dir) + "\n"
        "- One instinct per file, filename: <id>.md\n"
        "- If no durable pattern is found, write nothing and exit successfully.\n"
        "- Be conservative: only create/update instincts with clear repeated evidence.\n\n"
        "MINIMUM PATTERN THRESHOLD\n"
        "- Minimum repeated observations before creating/updating an instinct: "
        + str(int(min_occurrences))
        + "\n"
        "- Maximum instincts to create/update in this run: "
        + str(int(max_candidates))
        + "\n\n"
        "REQUIRED FILE FORMAT (exact structure)\n"
        "---\n"
        "id: <kebab-case-id>\n"
        "title: <short title>\n"
        "trigger: <when this applies>\n"
        "confidence: <0.3000-0.9000>\n"
        "status: active\n"
        "domain: <workflow|debugging|tools|testing|general|...>\n"
        "source: local\n"
        "created_at: <ISO8601 UTC Z>\n"
        "updated_at: <ISO8601 UTC Z>\n"
        "tags: <comma-separated-tags>\n"
        "notes: <single-line summary>\n"
        "---\n\n"
        "## Action\n"
        "<specific behavioral action>\n\n"
        "## Evidence\n"
        "- ts=<ISO8601 UTC Z> source_id=<stable-id> source_hash=<hash-or-label>\n"
        "- ...\n\n"
        "## Notes\n"
        "<brief rationale>\n\n"
        "FORMAT REQUIREMENTS\n"
        "- Keep id stable for the same behavior. Update existing file instead of creating duplicates.\n"
        "- Preserve existing created_at when updating.\n"
        "- Set updated_at to current run time. Current run time: " + now_iso + "\n"
        "- Use domain=workflow for repeated tool-sequence behaviors.\n"
        "- Confidence guidance: tentative 0.3-0.5, moderate 0.6-0.7, strong 0.8-0.9.\n"
        "- Never include secrets or raw sensitive content.\n\n"
        "EXISTING INSTINCTS (JSON excerpt)\n" + existing_json + "\n\n"
        "NEW OBSERVATIONS (JSON excerpt)\n" + observations_json + "\n"
    )


def _load_derive_command_template(paths: CompoundPaths) -> list[str]:
    if not paths.config_file.exists():
        raise FileNotFoundError(
            f"Missing compound config: {paths.config_file}. Run `loom compound init --force` to install scaffold."
        )

    try:
        parsed = json.loads(paths.config_file.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"Invalid JSON in {paths.config_file}: {e}") from e

    if not isinstance(parsed, dict):
        raise ValueError(
            f"Invalid compound config shape in {paths.config_file}: expected object"
        )

    instincts = parsed.get("instincts")
    instincts_obj: dict[str, Any] = instincts if isinstance(instincts, dict) else {}
    command_raw = instincts_obj.get("derive_command")

    if isinstance(command_raw, list):
        template = [str(x) for x in command_raw]
    elif isinstance(command_raw, str):
        template = shlex.split(command_raw)
    else:
        raise ValueError(
            f"Invalid or missing instincts.derive_command in {paths.config_file}. "
            "Expected array or shell-style string."
        )

    template = [x for x in template if str(x).strip()]
    if not template:
        raise ValueError(
            f"instincts.derive_command resolved to empty command in {paths.config_file}"
        )
    return template


def _render_command(template: list[str], values: dict[str, str]) -> list[str]:
    out: list[str] = []
    for token in template:
        names = _PLACEHOLDER_RE.findall(token)
        rendered = token
        for name in names:
            if name not in values:
                raise ValueError(f"Unknown derive_command placeholder: {{{name}}}")
            rendered = rendered.replace("{" + name + "}", str(values[name]))
        out.append(rendered)
    return out


@dataclass(frozen=True)
class _LlmDeriveResult:
    command: str


def _invoke_derivation_command(
    *,
    paths: CompoundPaths,
    observations: list[dict[str, Any]],
    existing_instincts: InstinctStore,
    min_occurrences: int,
    max_candidates: int,
) -> _LlmDeriveResult:
    repo = paths.root

    prompt = _build_freeform_prompt(
        paths=paths,
        observations=observations,
        existing_instincts=existing_instincts,
        min_occurrences=min_occurrences,
        max_candidates=max_candidates,
    )
    values = {
        "repo": str(paths.root),
        "loom_compound_dir": str(paths.loom_compound_dir),
        "observations_file": str(paths.observations_file),
        "instincts_local_dir": str(paths.instincts_local_dir),
        "instincts_inherited_dir": str(paths.instincts_inherited_dir),
        "prompt": prompt,
        "min_occurrences": str(int(min_occurrences)),
        "max_candidates": str(int(max_candidates)),
    }

    command_template = _load_derive_command_template(paths)
    cmd = _render_command(command_template, values)

    p = run(cmd, cwd=repo, check=False, timeout=240)
    if int(p.returncode) != 0:
        stderr = _short(str(p.stderr or "").strip(), max_len=1200)
        stdout = _short(str(p.stdout or "").strip(), max_len=800)
        raise RuntimeError(
            f"Instinct derivation command failed (code={int(p.returncode)}). stderr={stderr!r} stdout={stdout!r}"
        )

    return _LlmDeriveResult(command=shlex.join(cmd))


def _cooldown_seconds() -> int:
    return max(
        0, int(os.environ.get("COMPOUND_INSTINCTS_COOLDOWN_SECONDS", "120") or 120)
    )


def _auto_cooldown_active(state: CompoundState) -> bool:
    cooldown = _cooldown_seconds()
    if cooldown <= 0:
        return False
    last = _parse_iso(state.last_auto_run_at)
    if last is None:
        return False
    elapsed = (datetime.now(timezone.utc) - last).total_seconds()
    return elapsed < float(cooldown)


def _instinct_fingerprint(inst: Instinct) -> tuple[Any, ...]:
    return (
        str(inst.title or ""),
        str(inst.trigger or ""),
        str(inst.action or ""),
        tuple(str(t) for t in list(inst.tags or [])),
        float(inst.confidence or 0.0),
        str(inst.status or ""),
        str(inst.domain or ""),
        str(inst.notes or ""),
    )


def _diff_instinct_stores(
    before: InstinctStore, after: InstinctStore
) -> tuple[int, int]:
    before_by_id = {i.id: i for i in list(before.instincts or [])}
    after_by_id = {i.id: i for i in list(after.instincts or [])}

    created = 0
    updated = 0
    for instinct_id, after_inst in after_by_id.items():
        before_inst = before_by_id.get(instinct_id)
        if before_inst is None:
            created += 1
            continue
        if _instinct_fingerprint(before_inst) != _instinct_fingerprint(after_inst):
            updated += 1

    return created, updated


@dataclass(frozen=True)
class InstinctsUpdateResult:
    ok: bool
    repo: str
    observations_ingested: int
    observations_parse_errors: int
    observations_reset_detected: bool
    instincts_candidates: int
    instincts_created: int
    instincts_updated: int
    wrote_instincts: bool
    wrote_instincts_md: bool
    state_updated: bool
    skipped: bool
    skip_reason: str
    derivation_command: str


def run_instincts_update(
    *,
    root: Path,
    auto: bool = False,
    dry_run: bool = False,
    min_new_observations: int = 12,
    min_occurrences: int = 3,
    max_candidates: int = 12,
) -> InstinctsUpdateResult:
    repo = root.resolve()
    paths = compound_paths(repo)

    state = load_state(paths.state_file)

    if auto and _auto_cooldown_active(state):
        return InstinctsUpdateResult(
            ok=True,
            repo=str(repo),
            observations_ingested=0,
            observations_parse_errors=0,
            observations_reset_detected=False,
            instincts_candidates=0,
            instincts_created=0,
            instincts_updated=0,
            wrote_instincts=False,
            wrote_instincts_md=False,
            state_updated=False,
            skipped=True,
            skip_reason="cooldown_active",
            derivation_command="",
        )

    obs_prefix = observations_prefix_sha256(paths.observations_file)
    start_offset = int(state.observations_offset_bytes or 0)
    reset_detected = False
    if paths.observations_file.exists() and start_offset > 0:
        try:
            sz = int(paths.observations_file.stat().st_size)
        except Exception:
            sz = 0
        if sz < start_offset:
            reset_detected = True
        elif state.observations_prefix_sha256 and obs_prefix:
            if str(state.observations_prefix_sha256) != str(obs_prefix):
                reset_detected = True
    if reset_detected:
        start_offset = 0

    ingested = ingest_observations_since(
        paths.observations_file,
        start_offset_bytes=int(start_offset),
    )
    included = [
        i
        for i in ingested.items
        if isinstance(i, dict) and not bool(i.get("_compound_parse_error"))
    ]
    new_obs = int(len(included))
    end_offset = int(ingested.end_offset_bytes)

    before_store = load_instincts(paths.instincts_file)

    if auto and new_obs < int(min_new_observations) and not reset_detected:
        wrote_instincts_md = False
        if not dry_run:
            sync_instincts_markdown(root=repo, store=before_store)
            wrote_instincts_md = True
        return InstinctsUpdateResult(
            ok=True,
            repo=str(repo),
            observations_ingested=int(new_obs),
            observations_parse_errors=int(ingested.parse_errors),
            observations_reset_detected=bool(reset_detected),
            instincts_candidates=0,
            instincts_created=0,
            instincts_updated=0,
            wrote_instincts=False,
            wrote_instincts_md=bool(wrote_instincts_md),
            state_updated=False,
            skipped=True,
            skip_reason="insufficient_new_observations",
            derivation_command="",
        )

    if dry_run:
        return InstinctsUpdateResult(
            ok=True,
            repo=str(repo),
            observations_ingested=int(new_obs),
            observations_parse_errors=int(ingested.parse_errors),
            observations_reset_detected=bool(reset_detected),
            instincts_candidates=0,
            instincts_created=0,
            instincts_updated=0,
            wrote_instincts=False,
            wrote_instincts_md=False,
            state_updated=False,
            skipped=True,
            skip_reason="dry_run_not_executed",
            derivation_command="",
        )

    llm_result = _invoke_derivation_command(
        paths=paths,
        observations=included,
        existing_instincts=before_store,
        min_occurrences=int(min_occurrences),
        max_candidates=int(max_candidates),
    )

    after_store = load_instincts(paths.instincts_file)
    created, updated = _diff_instinct_stores(before_store, after_store)

    obs_stats = count_observations(paths.observations_file)
    start_count = 0 if reset_detected else int(state.observations_count or 0)
    end_count = int(start_count + new_obs)

    now_iso = now_iso_precise()
    next_state = CompoundState(
        version=3,
        observations_offset_bytes=int(end_offset),
        observations_prefix_sha256=str(obs_prefix or ""),
        observations_count=int(end_count),
        observations_tail_sha256=str(obs_stats.tail_sha256 or ""),
        last_auto_run_at=(now_iso if auto else str(state.last_auto_run_at or "")),
        last_auto_apply_at=(
            now_iso
            if auto and (created or updated)
            else str(state.last_auto_apply_at or "")
        ),
        updated_at=now_iso,
    )

    save_state(paths.state_file, next_state)
    save_instincts(paths.instincts_file, after_store)
    sync_instincts_markdown(root=repo, store=after_store)

    return InstinctsUpdateResult(
        ok=True,
        repo=str(repo),
        observations_ingested=int(new_obs),
        observations_parse_errors=int(ingested.parse_errors),
        observations_reset_detected=bool(reset_detected),
        instincts_candidates=int(created + updated),
        instincts_created=int(created),
        instincts_updated=int(updated),
        wrote_instincts=True,
        wrote_instincts_md=True,
        state_updated=True,
        skipped=False,
        skip_reason="",
        derivation_command=str(llm_result.command or ""),
    )


__all__ = ["InstinctsUpdateResult", "run_instincts_update"]
