from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

from agent_loom.compound.blocks import block_markers


SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_newlines(text: str) -> str:
    return str(text or "").replace("\r\n", "\n")


def validate_skill_name(name: str) -> str:
    n = str(name or "").strip()
    if len(n) < 1 or len(n) > 64:
        raise ValueError("skill.name must be 1-64 chars")
    if not SKILL_NAME_RE.fullmatch(n):
        raise ValueError("skill.name must be kebab-case")
    return n


@dataclass(frozen=True)
class ParsedSkill:
    fm: Dict[str, object]
    managed_body: str
    manual_notes: str


def parse_skill_markdown(md: str) -> ParsedSkill:
    text = _normalize_newlines(md)
    if not text.startswith("---\n"):
        return ParsedSkill(fm={}, managed_body=text.strip(), manual_notes="")
    end = text.find("\n---\n", 4)
    if end == -1:
        return ParsedSkill(fm={}, managed_body=text.strip(), manual_notes="")

    fm_raw = text[4:end].strip()
    rest = text[end + len("\n---\n") :]

    fm: Dict[str, object] = {}
    metadata: Dict[str, str] = {}
    in_metadata = False
    for line in fm_raw.split("\n"):
        line_txt = line.rstrip("\n")
        if not line_txt.strip():
            continue
        if re.fullmatch(r"\s*metadata\s*:\s*", line_txt):
            in_metadata = True
            continue
        if in_metadata:
            m = re.match(r"^\s+([a-zA-Z0-9_\-]+)\s*:\s*\"?(.*?)\"?\s*$", line_txt)
            if m:
                metadata[m.group(1)] = m.group(2).replace('\\"', '"')
            continue
        m = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.+)\s*$", line_txt)
        if not m:
            continue
        key = m.group(1)
        val = m.group(2).strip()
        if val.startswith('"') and val.endswith('"') and len(val) >= 2:
            val = val[1:-1]
        fm[key] = val
    if metadata:
        fm["metadata"] = metadata

    begin, end_marker = block_markers("skill-managed")
    b = rest.find(begin)
    e = rest.find(end_marker)
    if b != -1 and e != -1 and e > b:
        body = rest[b + len(begin) : e].strip()
        manual = rest[e + len(end_marker) :].strip()
        return ParsedSkill(fm=fm, managed_body=body, manual_notes=manual)

    # Back-compat: older skills may have "## Manual notes" instead of explicit markers.
    m2 = re.search(r"(^|\n)##\s+manual\s+notes\b", rest, flags=re.IGNORECASE)
    if m2:
        idx = int(m2.start())
        if rest[idx : idx + 1] == "\n":
            idx += 1
        body = rest[:idx].strip()
        manual = rest[idx:].strip()
        return ParsedSkill(fm=fm, managed_body=body, manual_notes=manual)

    return ParsedSkill(fm=fm, managed_body=rest.strip(), manual_notes="")


def _render_frontmatter(
    *,
    name: str,
    description: str,
    license: str,
    compatibility: str,
    metadata: Dict[str, str],
) -> str:
    def esc(v: str) -> str:
        return str(v).replace('"', '\\"')

    lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"license: {license}",
        f"compatibility: {compatibility}",
        "metadata:",
    ]
    for k in sorted(metadata.keys()):
        lines.append(f'  {k}: "{esc(metadata[k])}"')
    lines.extend(["---", ""])
    return "\n".join(lines)


def build_skill_markdown(
    *,
    name: str,
    description: str,
    body: str,
    license: str = "MIT",
    compatibility: str = "opencode,claude",
    version: int,
    created_at: Optional[str] = None,
    updated_at: Optional[str] = None,
    tags: Optional[list[str]] = None,
    metadata: Optional[Dict[str, str]] = None,
    manual_notes: Optional[str] = None,
) -> str:
    created = created_at or _now_iso()
    updated = updated_at or _now_iso()

    meta: Dict[str, str] = {
        "created_at": created,
        "updated_at": updated,
        "version": str(int(version)),
    }
    if tags:
        meta["tags"] = ",".join([t.strip() for t in tags if t.strip()])
    if metadata:
        meta.update({str(k): str(v) for k, v in metadata.items()})

    fm = _render_frontmatter(
        name=name,
        description=description,
        license=license,
        compatibility=compatibility,
        metadata=meta,
    )

    begin, end_marker = block_markers("skill-managed")
    managed = "\n".join([begin, _normalize_newlines(body).strip(), end_marker])

    placeholder_manual = "\n".join(
        [
            "## Manual notes",
            "",
            "_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._",
            "",
        ]
    )
    tail = (
        _normalize_newlines(manual_notes).rstrip() + "\n"
        if (manual_notes and manual_notes.strip())
        else placeholder_manual
    )

    return fm + managed + "\n\n" + tail


def _parse_csv(s: str) -> list[str]:
    parts = [p.strip() for p in str(s or "").split(",")]
    return [p for p in parts if p]


def _format_csv(items: Iterable[str]) -> str:
    out: list[str] = []
    for it in items:
        s = str(it or "").strip()
        if s and s not in out:
            out.append(s)
    return ",".join(out)


def _looks_like_diff_or_patch(text: str) -> bool:
    t = _normalize_newlines(text)
    if "```diff" in t:
        return True
    if re.search(r"^\+\+\+\s+\S+", t, flags=re.MULTILINE) and re.search(
        r"^---\s+\S+", t, flags=re.MULTILINE
    ):
        return True
    if re.search(r"^@@\s+[-+0-9, ]+\s+@@", t, flags=re.MULTILINE):
        return True
    return False


def _non_empty_line_count(text: str) -> int:
    return len([ln for ln in _normalize_newlines(text).split("\n") if ln.strip()])


def _looks_like_partial_body_update(existing_body: str, next_body: str) -> bool:
    old = _normalize_newlines(existing_body).strip()
    new = _normalize_newlines(next_body).strip()
    if not old:
        return False
    if not new:
        return True
    if _looks_like_diff_or_patch(new):
        return True

    old_len = len(old)
    new_len = len(new)
    old_lines = _non_empty_line_count(old)
    new_lines = _non_empty_line_count(new)

    if old_len > 250 and new_len < 250:
        return True
    if old_lines >= 12 and new_lines < 8:
        return True
    if new_len < int(old_len * 0.3) and new_lines < 20:
        return True
    return False


def write_or_update_skill(
    *,
    skills_dir: Path,
    name: str,
    description: str,
    body: str,
    mirror_claude_dir: Optional[Path] = None,
    tags: Optional[list[str]] = None,
    metadata: Optional[Dict[str, str]] = None,
    source_episode_ids: Optional[list[str]] = None,
    source_instinct_ids: Optional[list[str]] = None,
    created_at: Optional[str] = None,
    updated_at: Optional[str] = None,
    version: Optional[int] = None,
) -> Tuple[str, Path]:
    n = validate_skill_name(name)
    desc = str(description or "").strip() or f"Skill: {n}"
    b = _normalize_newlines(body)
    if not b.strip():
        raise ValueError("skill.body is required")

    skill_dir = skills_dir / n
    skill_path = skill_dir / "SKILL.md"

    exists = skill_path.exists()
    next_version = int(version) if version is not None else 1
    next_created_at: Optional[str] = str(created_at) if created_at else None
    manual_notes = None
    existing_fm: Dict[str, object] = {}
    existing_body = ""
    existing_meta: Dict[str, str] = {}
    if exists:
        parsed = parse_skill_markdown(skill_path.read_text(encoding="utf-8"))
        existing_fm = parsed.fm
        existing_body = parsed.managed_body
        meta_obj = existing_fm.get("metadata")
        meta: Dict[str, object] = meta_obj if isinstance(meta_obj, dict) else {}
        existing_meta = {str(k): str(v) for k, v in meta.items()}
        try:
            if version is None:
                next_version = int(str(meta.get("version") or "1")) + 1
        except Exception:
            if version is None:
                next_version = 2
        if not next_created_at:
            next_created_at = str(meta.get("created_at") or "") or None
        manual_notes = parsed.manual_notes

    tags_final: Optional[list[str]] = tags
    if tags_final is None:
        tags_final = _parse_csv(existing_meta.get("tags", "")) or None

    if exists and existing_body and _looks_like_partial_body_update(existing_body, b):
        raise ValueError(
            "skill.body must be the full managed body (complete replacement), not a snippet/diff"
        )

    md = build_skill_markdown(
        name=n,
        description=desc,
        body=b,
        license=str(existing_fm.get("license") or "MIT"),
        compatibility=str(existing_fm.get("compatibility") or "opencode,claude"),
        version=int(next_version),
        created_at=(next_created_at or _now_iso()),
        updated_at=(str(updated_at) if updated_at else _now_iso()),
        tags=tags_final,
        manual_notes=manual_notes,
        metadata={
            k: v
            for k, v in existing_meta.items()
            if k
            not in {
                "created_at",
                "updated_at",
                "version",
                "tags",
                "source_episode_ids",
                "source_instinct_ids",
            }
        }
        | {
            **({str(k): str(v) for k, v in (metadata or {}).items()}),
            **(
                {
                    "source_episode_ids": _format_csv(
                        [
                            *_parse_csv(existing_meta.get("source_episode_ids", "")),
                            *(
                                [
                                    str(x)
                                    for x in (source_episode_ids or [])
                                    if str(x).strip()
                                ]
                            ),
                        ]
                    )
                }
                if (
                    source_episode_ids is not None
                    or existing_meta.get("source_episode_ids")
                )
                else {}
            ),
            **(
                {
                    "source_instinct_ids": _format_csv(
                        [
                            *_parse_csv(existing_meta.get("source_instinct_ids", "")),
                            *(
                                [
                                    str(x)
                                    for x in (source_instinct_ids or [])
                                    if str(x).strip()
                                ]
                            ),
                        ]
                    )
                }
                if (
                    source_instinct_ids is not None
                    or existing_meta.get("source_instinct_ids")
                )
                else {}
            ),
        }
        or None,
    )

    skill_dir.mkdir(parents=True, exist_ok=True)
    skill_path.write_text(md, encoding="utf-8")

    if mirror_claude_dir is not None:
        mirror_dir = mirror_claude_dir / n
        mirror_dir.mkdir(parents=True, exist_ok=True)
        (mirror_dir / "SKILL.md").write_text(md, encoding="utf-8")

    return ("updated" if exists else "created"), skill_path
