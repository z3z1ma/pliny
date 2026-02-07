from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from agent_loom.compound.skills import (
    parse_skill_markdown,
    validate_skill_name,
    write_or_update_skill,
)


def _as_str(v: object) -> str:
    return str(v or "").strip()


def _parse_csv(s: str) -> List[str]:
    parts = [p.strip() for p in str(s or "").split(",")]
    return [p for p in parts if p]


@dataclass(frozen=True)
class SkillCandidate:
    name: str
    description: str
    body: str
    tags: List[str]
    source_instinct_ids: List[str]


def parse_skill_candidates(proposals: Dict[str, Any]) -> List[SkillCandidate]:
    raw = proposals.get("skill_candidates")
    if not isinstance(raw, list):
        return []
    out: List[SkillCandidate] = []
    for it in raw:
        if not isinstance(it, dict):
            continue
        name = _as_str(it.get("name"))
        if not name:
            continue
        try:
            name = validate_skill_name(name)
        except Exception:
            continue
        desc = _as_str(it.get("description"))
        body = _as_str(it.get("body"))
        if not body:
            continue
        tags_raw = it.get("tags")
        tags: List[str] = []
        if isinstance(tags_raw, list):
            tags = sorted({str(t).strip() for t in tags_raw if str(t).strip()})
        src_raw = it.get("source_instinct_ids")
        src: List[str] = []
        if isinstance(src_raw, list):
            src = sorted({str(s).strip() for s in src_raw if str(s).strip()})
        out.append(
            SkillCandidate(
                name=name,
                description=desc or f"Skill: {name}",
                body=body,
                tags=tags,
                source_instinct_ids=src,
            )
        )
    out.sort(key=lambda x: x.name)
    return out


def _episode_already_applied(meta: Dict[str, str], episode_id: str) -> bool:
    eps = _parse_csv(meta.get("source_episode_ids", ""))
    return episode_id in eps


def apply_skill_candidates(
    *,
    skills_dir: Path,
    candidates: Iterable[SkillCandidate],
    episode_id: str,
    episode_ts: str,
    mirror_claude_dir: Optional[Path] = None,
) -> Tuple[int, int]:
    created = 0
    updated = 0

    for c in candidates:
        skill_dir = skills_dir / c.name
        skill_path = skill_dir / "SKILL.md"
        exists = skill_path.exists()

        meta: Dict[str, str] = {}
        if exists:
            parsed = parse_skill_markdown(skill_path.read_text(encoding="utf-8"))
            fm = parsed.fm
            meta_obj = fm.get("metadata")
            meta = {
                str(k): str(v)
                for k, v in (meta_obj.items() if isinstance(meta_obj, dict) else [])
            }
            if _episode_already_applied(meta, episode_id):
                continue

        action, out_path = write_or_update_skill(
            skills_dir=skills_dir,
            name=c.name,
            description=c.description,
            body=c.body,
            mirror_claude_dir=mirror_claude_dir,
            tags=c.tags or None,
            source_episode_ids=[episode_id],
            source_instinct_ids=c.source_instinct_ids or None,
            created_at=episode_ts,
            updated_at=episode_ts,
        )

        if action == "updated":
            updated += 1
        elif action == "created":
            created += 1
        else:
            # Defensive: treat unknown as updated.
            if out_path.exists():
                updated += 1

    return created, updated
