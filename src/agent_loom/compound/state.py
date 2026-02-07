from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class CompoundState:
    version: int
    observations_offset_bytes: int
    observations_prefix_sha256: str
    observations_count: int
    observations_tail_sha256: str
    last_episode_id: str
    updated_at: str


def load_state(path: Path) -> CompoundState:
    if not path.exists():
        return CompoundState(
            version=2,
            observations_offset_bytes=0,
            observations_prefix_sha256="",
            observations_count=0,
            observations_tail_sha256="",
            last_episode_id="",
            updated_at="",
        )
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return CompoundState(
            version=2,
            observations_offset_bytes=0,
            observations_prefix_sha256="",
            observations_count=0,
            observations_tail_sha256="",
            last_episode_id="",
            updated_at="",
        )

    if not isinstance(parsed, dict):
        return CompoundState(
            version=2,
            observations_offset_bytes=0,
            observations_prefix_sha256="",
            observations_count=0,
            observations_tail_sha256="",
            last_episode_id="",
            updated_at="",
        )

    ver = int(parsed.get("version") or 0)
    if ver == 1:
        # v1 was count+tail based; keep those but start offset-based cursor from zero.
        return CompoundState(
            version=2,
            observations_offset_bytes=0,
            observations_prefix_sha256="",
            observations_count=int(parsed.get("observations_count") or 0),
            observations_tail_sha256=str(parsed.get("observations_tail_sha256") or ""),
            last_episode_id=str(parsed.get("last_episode_id") or ""),
            updated_at=str(parsed.get("updated_at") or ""),
        )

    if ver != 2:
        return CompoundState(
            version=2,
            observations_offset_bytes=0,
            observations_prefix_sha256="",
            observations_count=0,
            observations_tail_sha256="",
            last_episode_id="",
            updated_at="",
        )

    return CompoundState(
        version=2,
        observations_offset_bytes=int(parsed.get("observations_offset_bytes") or 0),
        observations_prefix_sha256=str(parsed.get("observations_prefix_sha256") or ""),
        observations_count=int(parsed.get("observations_count") or 0),
        observations_tail_sha256=str(parsed.get("observations_tail_sha256") or ""),
        last_episode_id=str(parsed.get("last_episode_id") or ""),
        updated_at=str(parsed.get("updated_at") or ""),
    )


def save_state(path: Path, state: CompoundState) -> None:
    payload = {
        "version": 2,
        "observations_offset_bytes": int(state.observations_offset_bytes),
        "observations_prefix_sha256": str(state.observations_prefix_sha256 or ""),
        "observations_count": int(state.observations_count),
        "observations_tail_sha256": str(state.observations_tail_sha256 or ""),
        "last_episode_id": str(state.last_episode_id or ""),
        "updated_at": str(state.updated_at or _now_iso()),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
