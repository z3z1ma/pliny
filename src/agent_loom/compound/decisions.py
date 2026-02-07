from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent_loom.compound.episodes import canonical_json_bytes, pretty_json


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def compute_decision_id(version: int, payload: Dict[str, Any]) -> str:
    return sha256(
        canonical_json_bytes({"version": int(version), **payload})
    ).hexdigest()


@dataclass(frozen=True)
class Decision:
    version: int
    decision_id: str
    created_at: str
    episode_id: str
    proposal_blob_sha256: str
    ops: List[Dict[str, Any]]

    def identity_payload(self) -> Dict[str, Any]:
        return {
            "created_at": str(self.created_at),
            "episode_id": str(self.episode_id),
            "proposal_blob_sha256": str(self.proposal_blob_sha256 or ""),
            "ops": list(self.ops or []),
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": int(self.version),
            "decision_id": str(self.decision_id),
            "created_at": str(self.created_at),
            "episode_id": str(self.episode_id),
            **(
                {"proposal_blob_sha256": str(self.proposal_blob_sha256)}
                if str(self.proposal_blob_sha256 or "").strip()
                else {}
            ),
            "ops": list(self.ops or []),
        }


def decision_path_for_id(
    *, decisions_dir: Path, created_at: str, decision_id: str
) -> Path:
    try:
        dt = datetime.fromisoformat(str(created_at).replace("Z", "+00:00"))
    except Exception:
        dt = datetime.now(timezone.utc)
    return decisions_dir / f"{dt.year:04d}" / f"{dt.month:02d}" / f"{decision_id}.json"


def load_decision(path: Path) -> Decision:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("decision file must be a JSON object")
    version = int(data.get("version") or 1)
    decision_id = str(data.get("decision_id") or "").strip()
    created_at = str(data.get("created_at") or "").strip() or _now_iso()
    episode_id = str(data.get("episode_id") or "").strip()
    proposal_blob_sha256 = str(data.get("proposal_blob_sha256") or "").strip()
    ops_raw = data.get("ops")
    ops: List[Dict[str, Any]] = []
    if isinstance(ops_raw, list):
        for it in ops_raw:
            if isinstance(it, dict):
                ops.append(dict(it))

    tmp = Decision(
        version=version,
        decision_id=decision_id,
        created_at=created_at,
        episode_id=episode_id,
        proposal_blob_sha256=proposal_blob_sha256,
        ops=ops,
    )
    if not tmp.decision_id:
        computed = compute_decision_id(tmp.version, tmp.identity_payload())
        tmp = Decision(
            version=tmp.version,
            decision_id=computed,
            created_at=tmp.created_at,
            episode_id=tmp.episode_id,
            proposal_blob_sha256=tmp.proposal_blob_sha256,
            ops=tmp.ops,
        )
    return tmp


def write_decision(path: Path, decision: Decision, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(pretty_json(decision.to_dict()), encoding="utf-8")


def build_decision(
    *,
    created_at: Optional[str],
    episode_id: str,
    proposal_blob_sha256: str,
    ops: List[Dict[str, Any]],
) -> Decision:
    ts = str(created_at or "").strip() or _now_iso()
    tmp = Decision(
        version=1,
        decision_id="",
        created_at=ts,
        episode_id=str(episode_id or ""),
        proposal_blob_sha256=str(proposal_blob_sha256 or ""),
        ops=list(ops or []),
    )
    decision_id = compute_decision_id(tmp.version, tmp.identity_payload())
    return Decision(
        version=tmp.version,
        decision_id=decision_id,
        created_at=tmp.created_at,
        episode_id=tmp.episode_id,
        proposal_blob_sha256=tmp.proposal_blob_sha256,
        ops=tmp.ops,
    )


def list_decisions(decisions_dir: Path) -> List[Path]:
    if not decisions_dir.exists() or not decisions_dir.is_dir():
        return []
    paths = [p for p in decisions_dir.rglob("*.json") if p.is_file()]
    scored: list[tuple[str, str, Path]] = []
    for p in paths:
        try:
            d = load_decision(p)
            scored.append((str(d.created_at), str(d.decision_id), p))
        except Exception:
            scored.append(("", p.as_posix(), p))
    scored.sort(key=lambda t: (t[0], t[1]))
    return [p for _, _, p in scored]


__all__ = [
    "Decision",
    "build_decision",
    "decision_path_for_id",
    "list_decisions",
    "load_decision",
    "write_decision",
]
