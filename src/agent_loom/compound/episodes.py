from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def canonical_json_bytes(obj: object) -> bytes:
    # Stable, whitespace-free encoding for hashing.
    return json.dumps(
        obj,
        sort_keys=True,
        ensure_ascii=True,
        separators=(",", ":"),
    ).encode("utf-8")


def pretty_json(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


@dataclass(frozen=True)
class EpisodeGit:
    head_sha: str
    base_sha: str
    base_ref: str
    dirty: bool
    diffstat: str
    diffstat_sha256: str
    patch: str
    patch_sha256: str
    patch_omitted: bool
    patch_blob_sha256: str
    changed_files: List[str]


@dataclass(frozen=True)
class EpisodeObservationCursor:
    start_count: int
    end_count: int
    tail_sha256: str
    reset_detected: bool
    start_offset_bytes: int = 0
    end_offset_bytes: int = 0
    file_prefix_sha256: str = ""


@dataclass(frozen=True)
class EpisodeObservation:
    cursor: EpisodeObservationCursor
    included: List[Dict[str, Any]]
    omitted: bool


@dataclass(frozen=True)
class EpisodeTriage:
    status: str  # pending|accepted|rejected
    tags: List[str]
    notes: str


@dataclass(frozen=True)
class Episode:
    version: int
    episode_id: str
    created_at: str
    git: EpisodeGit
    observations: EpisodeObservation
    proposals: Dict[str, Any]
    triage: EpisodeTriage

    def identity_payload(self) -> Dict[str, Any]:
        # Fields that define episode identity (created_at and triage are excluded).
        included_sha = (
            sha256(canonical_json_bytes(self.observations.included)).hexdigest()
            if self.observations.included
            else ""
        )
        return {
            "git": {
                "head_sha": self.git.head_sha,
                "base_sha": self.git.base_sha,
                "base_ref": self.git.base_ref,
                "dirty": bool(self.git.dirty),
                "diffstat_sha256": self.git.diffstat_sha256,
                "patch_sha256": self.git.patch_sha256,
                "patch_omitted": bool(self.git.patch_omitted),
                "changed_files": list(self.git.changed_files),
            },
            "observations": {
                "cursor": {
                    "start_count": int(self.observations.cursor.start_count),
                    "end_count": int(self.observations.cursor.end_count),
                    "tail_sha256": self.observations.cursor.tail_sha256,
                    "reset_detected": bool(self.observations.cursor.reset_detected),
                    "start_offset_bytes": int(
                        self.observations.cursor.start_offset_bytes
                    ),
                    "end_offset_bytes": int(self.observations.cursor.end_offset_bytes),
                    "file_prefix_sha256": str(
                        self.observations.cursor.file_prefix_sha256 or ""
                    ),
                },
                "included_sha256": included_sha,
                "omitted": bool(self.observations.omitted),
            },
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": int(self.version),
            "episode_id": self.episode_id,
            "created_at": self.created_at,
            "git": {
                "head_sha": self.git.head_sha,
                "base_sha": self.git.base_sha,
                "base_ref": self.git.base_ref,
                "dirty": bool(self.git.dirty),
                "diffstat": self.git.diffstat,
                "diffstat_sha256": self.git.diffstat_sha256,
                "patch": self.git.patch,
                "patch_sha256": self.git.patch_sha256,
                "patch_omitted": bool(self.git.patch_omitted),
                **(
                    {"patch_blob_sha256": str(self.git.patch_blob_sha256)}
                    if str(self.git.patch_blob_sha256 or "").strip()
                    else {}
                ),
                "changed_files": list(self.git.changed_files),
            },
            "observations": {
                "cursor": {
                    "start_count": int(self.observations.cursor.start_count),
                    "end_count": int(self.observations.cursor.end_count),
                    "tail_sha256": self.observations.cursor.tail_sha256,
                    "reset_detected": bool(self.observations.cursor.reset_detected),
                    "start_offset_bytes": int(
                        self.observations.cursor.start_offset_bytes
                    ),
                    "end_offset_bytes": int(self.observations.cursor.end_offset_bytes),
                    "file_prefix_sha256": str(
                        self.observations.cursor.file_prefix_sha256 or ""
                    ),
                },
                "included": list(self.observations.included),
                "omitted": bool(self.observations.omitted),
            },
            "proposals": dict(self.proposals or {}),
            "triage": {
                "status": self.triage.status,
                "tags": list(self.triage.tags),
                "notes": self.triage.notes,
            },
        }


def compute_episode_id(version: int, identity_payload: Dict[str, Any]) -> str:
    payload = {"version": int(version), "identity": identity_payload}
    return sha256(canonical_json_bytes(payload)).hexdigest()


def episode_path_for_id(
    *, episodes_dir: Path, created_at: str, episode_id: str
) -> Path:
    # created_at is ISO8601 Zulu.
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except Exception:
        dt = datetime.now(timezone.utc)
    return episodes_dir / f"{dt.year:04d}" / f"{dt.month:02d}" / f"{episode_id}.json"


def find_episode_by_id(*, episodes_dir: Path, episode_id: str) -> Optional[Path]:
    ident = str(episode_id or "").strip()
    if not ident:
        return None
    target = f"{ident}.json"
    if not episodes_dir.exists():
        return None
    for p in episodes_dir.rglob(target):
        if p.is_file() and p.name == target:
            return p
    return None


def load_episode(path: Path) -> Episode:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("episode file must be a JSON object")
    version = int(data.get("version") or 1)
    ep_id = str(data.get("episode_id") or "").strip()
    created_at = str(data.get("created_at") or "").strip() or _now_iso()

    git_obj = data.get("git")
    git: Dict[str, Any] = git_obj if isinstance(git_obj, dict) else {}
    obs_obj = data.get("observations")
    obs: Dict[str, Any] = obs_obj if isinstance(obs_obj, dict) else {}
    cursor_obj = obs.get("cursor")
    cursor: Dict[str, Any] = cursor_obj if isinstance(cursor_obj, dict) else {}

    ep_git = EpisodeGit(
        head_sha=str(git.get("head_sha") or ""),
        base_sha=str(git.get("base_sha") or ""),
        base_ref=str(git.get("base_ref") or ""),
        dirty=bool(git.get("dirty") or False),
        diffstat=str(git.get("diffstat") or ""),
        diffstat_sha256=str(git.get("diffstat_sha256") or ""),
        patch=str(git.get("patch") or ""),
        patch_sha256=str(git.get("patch_sha256") or ""),
        patch_omitted=bool(git.get("patch_omitted") or False),
        patch_blob_sha256=str(git.get("patch_blob_sha256") or ""),
        changed_files=list(git.get("changed_files") or []),
    )
    ep_cursor = EpisodeObservationCursor(
        start_count=int(cursor.get("start_count") or 0),
        end_count=int(cursor.get("end_count") or 0),
        tail_sha256=str(cursor.get("tail_sha256") or ""),
        reset_detected=bool(cursor.get("reset_detected") or False),
        start_offset_bytes=int(cursor.get("start_offset_bytes") or 0),
        end_offset_bytes=int(cursor.get("end_offset_bytes") or 0),
        file_prefix_sha256=str(cursor.get("file_prefix_sha256") or ""),
    )
    ep_obs = EpisodeObservation(
        cursor=ep_cursor,
        included=list(obs.get("included") or []),
        omitted=bool(obs.get("omitted") or False),
    )
    triage_raw = data.get("triage")
    triage_obj: Dict[str, Any] = triage_raw if isinstance(triage_raw, dict) else {}
    triage = EpisodeTriage(
        status=str(triage_obj.get("status") or "pending"),
        tags=list(triage_obj.get("tags") or []),
        notes=str(triage_obj.get("notes") or ""),
    )
    proposals_raw = data.get("proposals")
    proposals: Dict[str, Any] = proposals_raw if isinstance(proposals_raw, dict) else {}

    ep = Episode(
        version=version,
        episode_id=ep_id,
        created_at=created_at,
        git=ep_git,
        observations=ep_obs,
        proposals=dict(proposals),
        triage=triage,
    )
    if not ep.episode_id:
        computed = compute_episode_id(ep.version, ep.identity_payload())
        ep = Episode(
            version=ep.version,
            episode_id=computed,
            created_at=ep.created_at,
            git=ep.git,
            observations=ep.observations,
            proposals=ep.proposals,
            triage=ep.triage,
        )
    return ep


def write_episode(path: Path, episode: Episode, *, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(pretty_json(episode.to_dict()), encoding="utf-8")


def build_episode(
    *,
    created_at: Optional[str],
    git: EpisodeGit,
    observations: EpisodeObservation,
    proposals: Optional[Dict[str, Any]] = None,
    triage_status: str = "pending",
    triage_tags: Optional[Iterable[str]] = None,
    triage_notes: str = "",
) -> Episode:
    ts = str(created_at or "").strip() or _now_iso()
    triage = EpisodeTriage(
        status=str(triage_status or "pending"),
        tags=sorted({str(t).strip() for t in (triage_tags or []) if str(t).strip()}),
        notes=str(triage_notes or ""),
    )
    tmp = Episode(
        version=1,
        episode_id="",
        created_at=ts,
        git=git,
        observations=observations,
        proposals=dict(proposals or {}),
        triage=triage,
    )
    ep_id = compute_episode_id(tmp.version, tmp.identity_payload())
    return Episode(
        version=tmp.version,
        episode_id=ep_id,
        created_at=tmp.created_at,
        git=tmp.git,
        observations=tmp.observations,
        proposals=tmp.proposals,
        triage=tmp.triage,
    )


def bounded_text(text: str, *, max_bytes: int) -> Tuple[str, bool]:
    b = text.encode("utf-8")
    if len(b) <= max_bytes:
        return text, False
    # Truncate on byte boundary.
    trunc = b[: max(0, max_bytes - 1000)]
    out = trunc.decode("utf-8", errors="ignore")
    out = out.rstrip() + "\n\n(...truncated)\n"
    return out, True
