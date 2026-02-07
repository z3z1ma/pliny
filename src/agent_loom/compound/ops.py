from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from agent_loom.compound.compiler_instincts import InstinctCandidate
from agent_loom.compound.compiler_skills import SkillCandidate


@dataclass(frozen=True)
class ParsedOps:
    instincts: List[InstinctCandidate]
    skills: List[SkillCandidate]


def parse_ops(ops: Iterable[Dict[str, Any]]) -> ParsedOps:
    instincts: List[InstinctCandidate] = []
    skills: List[SkillCandidate] = []
    for it in ops:
        if not isinstance(it, dict):
            continue
        op = str(it.get("op") or "").strip()
        if op == "instinct.upsert":
            ident = str(it.get("id") or "").strip()
            trigger = str(it.get("trigger") or "").strip()
            action = str(it.get("action") or "").strip()
            if not ident or not trigger or not action:
                continue
            title = str(it.get("title") or ident).strip() or ident
            conf_raw = it.get("confidence")
            try:
                conf = float(conf_raw) if conf_raw is not None else 0.6
            except Exception:
                conf = 0.6
            tags_raw = it.get("tags")
            tags: List[str] = []
            if isinstance(tags_raw, list):
                tags = sorted({str(t).strip() for t in tags_raw if str(t).strip()})
            notes = str(it.get("notes") or "").strip()
            instincts.append(
                InstinctCandidate(
                    id=ident,
                    title=title,
                    trigger=trigger,
                    action=action,
                    confidence=max(0.0, min(1.0, conf)),
                    tags=tags,
                    notes=notes,
                )
            )
            continue

        if op == "skill.upsert":
            name = str(it.get("name") or "").strip()
            body = str(it.get("body") or "").strip()
            if not name or not body:
                continue
            desc = str(it.get("description") or "").strip() or f"Skill: {name}"
            tags_raw = it.get("tags")
            skill_tags: List[str] = []
            if isinstance(tags_raw, list):
                skill_tags = sorted(
                    {str(t).strip() for t in tags_raw if str(t).strip()}
                )
            src_raw = it.get("source_instinct_ids")
            src: List[str] = []
            if isinstance(src_raw, list):
                src = sorted({str(s).strip() for s in src_raw if str(s).strip()})
            skills.append(
                SkillCandidate(
                    name=name,
                    description=desc,
                    body=body,
                    tags=skill_tags,
                    source_instinct_ids=src,
                )
            )

    instincts.sort(key=lambda x: x.id)
    skills.sort(key=lambda x: x.name)
    return ParsedOps(instincts=instincts, skills=skills)


__all__ = [
    "ParsedOps",
    "parse_ops",
]
