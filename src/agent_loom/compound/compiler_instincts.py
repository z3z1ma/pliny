from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple

from agent_loom.compound.instincts import Instinct, InstinctStore


def _as_str(v: object) -> str:
    return str(v or "").strip()


def _as_float(v: object, default: float) -> float:
    try:
        return float(v)  # type: ignore[arg-type]
    except Exception:
        return float(default)


def _clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))


@dataclass(frozen=True)
class InstinctCandidate:
    id: str
    title: str
    trigger: str
    action: str
    confidence: float
    tags: List[str]
    notes: str


def parse_instinct_candidates(proposals: Dict[str, Any]) -> List[InstinctCandidate]:
    raw = proposals.get("instinct_candidates")
    if not isinstance(raw, list):
        return []
    out: List[InstinctCandidate] = []
    for it in raw:
        if not isinstance(it, dict):
            continue
        ident = _as_str(it.get("id"))
        if not ident:
            continue
        title = _as_str(it.get("title")) or ident
        trigger = _as_str(it.get("trigger"))
        action = _as_str(it.get("action"))
        if not trigger or not action:
            continue
        conf = _clamp(_as_float(it.get("confidence"), 0.6), 0.0, 1.0)
        tags_raw = it.get("tags")
        tags: List[str] = []
        if isinstance(tags_raw, list):
            tags = sorted({str(t).strip() for t in tags_raw if str(t).strip()})
        notes = _as_str(it.get("notes"))
        out.append(
            InstinctCandidate(
                id=ident,
                title=title,
                trigger=trigger,
                action=action,
                confidence=conf,
                tags=tags,
                notes=notes,
            )
        )
    out.sort(key=lambda x: x.id)
    return out


def _episode_already_in_evidence(inst: Instinct, episode_id: str) -> bool:
    for ev in inst.evidence:
        try:
            if str(ev.get("episode_id") or "") == episode_id:
                return True
        except Exception:
            continue
    return False


def apply_instinct_candidates(
    *,
    store: InstinctStore,
    candidates: Iterable[InstinctCandidate],
    episode_id: str,
    episode_ts: str,
    head_sha: str,
    patch_sha256: str,
) -> Tuple[int, int]:
    by_id: Dict[str, Instinct] = {i.id: i for i in store.instincts}
    created = 0
    updated = 0

    for c in candidates:
        existing = by_id.get(c.id)
        if existing is None:
            inst = Instinct(
                id=c.id,
                title=c.title,
                trigger=c.trigger,
                action=c.action,
                tags=list(c.tags),
                confidence=float(c.confidence),
                status="active",
                skill=None,
                notes=c.notes or None,
                created_at=episode_ts,
                updated_at=episode_ts,
                evidence=[
                    {
                        "ts": episode_ts,
                        "episode_id": episode_id,
                        "head_sha": head_sha,
                        "patch_sha256": patch_sha256,
                    }
                ],
            )
            store.instincts.append(inst)
            by_id[inst.id] = inst
            created += 1
            continue

        if _episode_already_in_evidence(existing, episode_id):
            continue

        changed = False
        if existing.title != c.title:
            existing.title = c.title
            changed = True
        if existing.trigger != c.trigger:
            existing.trigger = c.trigger
            changed = True
        if existing.action != c.action:
            existing.action = c.action
            changed = True
        if list(existing.tags) != list(c.tags):
            existing.tags = list(c.tags)
            changed = True
        if float(existing.confidence or 0.0) != float(c.confidence):
            existing.confidence = float(c.confidence)
            changed = True
        if c.notes and (existing.notes or "") != c.notes:
            existing.notes = c.notes
            changed = True

        existing.evidence.append(
            {
                "ts": episode_ts,
                "episode_id": episode_id,
                "head_sha": head_sha,
                "patch_sha256": patch_sha256,
            }
        )
        changed = True

        if changed:
            existing.updated_at = episode_ts
            updated += 1

    store.instincts.sort(key=lambda x: x.id)
    return created, updated
