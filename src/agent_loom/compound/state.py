from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from agent_loom.core.time import now_iso_precise


@dataclass
class CompoundState:
    version: int
    observations_offset_bytes: int
    observations_prefix_sha256: str
    observations_count: int
    observations_tail_sha256: str
    last_auto_run_at: str
    last_auto_apply_at: str
    updated_at: str


_EMPTY_STATE = CompoundState(
    version=3,
    observations_offset_bytes=0,
    observations_prefix_sha256="",
    observations_count=0,
    observations_tail_sha256="",
    last_auto_run_at="",
    last_auto_apply_at="",
    updated_at="",
)


def load_state(path: Path) -> CompoundState:
    if not path.exists():
        return CompoundState(**_EMPTY_STATE.__dict__)
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return CompoundState(**_EMPTY_STATE.__dict__)

    if not isinstance(parsed, dict):
        return CompoundState(**_EMPTY_STATE.__dict__)

    ver = int(parsed.get("version") or 0)
    if ver == 1:
        return CompoundState(
            version=3,
            observations_offset_bytes=0,
            observations_prefix_sha256="",
            observations_count=int(parsed.get("observations_count") or 0),
            observations_tail_sha256=str(parsed.get("observations_tail_sha256") or ""),
            last_auto_run_at="",
            last_auto_apply_at="",
            updated_at=str(parsed.get("updated_at") or ""),
        )

    if ver == 2:
        return CompoundState(
            version=3,
            observations_offset_bytes=int(parsed.get("observations_offset_bytes") or 0),
            observations_prefix_sha256=str(
                parsed.get("observations_prefix_sha256") or ""
            ),
            observations_count=int(parsed.get("observations_count") or 0),
            observations_tail_sha256=str(parsed.get("observations_tail_sha256") or ""),
            last_auto_run_at="",
            last_auto_apply_at="",
            updated_at=str(parsed.get("updated_at") or ""),
        )

    if ver != 3:
        return CompoundState(**_EMPTY_STATE.__dict__)

    return CompoundState(
        version=3,
        observations_offset_bytes=int(parsed.get("observations_offset_bytes") or 0),
        observations_prefix_sha256=str(parsed.get("observations_prefix_sha256") or ""),
        observations_count=int(parsed.get("observations_count") or 0),
        observations_tail_sha256=str(parsed.get("observations_tail_sha256") or ""),
        last_auto_run_at=str(parsed.get("last_auto_run_at") or ""),
        last_auto_apply_at=str(parsed.get("last_auto_apply_at") or ""),
        updated_at=str(parsed.get("updated_at") or ""),
    )


def save_state(path: Path, state: CompoundState) -> None:
    payload = {
        "version": 3,
        "observations_offset_bytes": int(state.observations_offset_bytes),
        "observations_prefix_sha256": str(state.observations_prefix_sha256 or ""),
        "observations_count": int(state.observations_count),
        "observations_tail_sha256": str(state.observations_tail_sha256 or ""),
        "last_auto_run_at": str(state.last_auto_run_at or ""),
        "last_auto_apply_at": str(state.last_auto_apply_at or ""),
        "updated_at": str(state.updated_at or now_iso_precise()),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
